#!/usr/bin/env python3
"""Audit patches/*.txt for silent no-ops.

The Morphe CLI drops an -e/-d name it does not recognise and drops an -e name
whose compatible-package list excludes the app - both without failing the
build. A patch file that drifts past an upstream rename therefore claims to
change the APK while doing nothing, which is the same silent failure that hid
the Material Capsule redirect to the Play Store.

For every patch file the build would actually read (patches/<app_name>-<source>.txt):

    DEAD-FILE      filename never matches any <app_name>-<source>: never read
    EMPTY-FILE     no +/- lines: file has no effect
    MISSING        name defined by none of the source's bundles: silently ignored
    INCOMPATIBLE   name defined, but not for this app's package: silently dropped
    NO-BUNDLE      source ships no .mpp bundle (ReVanced-style source)
    NO-PACKAGE     no apps/<store>/<app>.json package: compatibility unverified

src/__main__._unapplied_requested() logs the -e half of this at build time;
this script also covers -d and runs without building anything. Run it after any
source bump, since bundles are renamed upstream.

Usage:
    GITHUB_TOKEN=... python scripts/audit_patch_names.py    # exit 1 if findings
"""

import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(tempfile.gettempdir()) / "morphe-patch-audit"
OUT = CACHE / "out"

sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from src import utils  # noqa: E402  (needs cwd = repo root)

FAIL_KINDS = {"DEAD-FILE", "EMPTY-FILE", "MISSING", "INCOMPATIBLE"}


def app_package(app_name: str) -> str | None:
    for store in sorted(os.listdir("apps")):
        path = Path("apps") / store / f"{app_name}.json"
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if data.get("package"):
            return data["package"]
    return None


def source_entries(source: str) -> list[dict]:
    data = json.loads((Path("sources") / f"{source}.json").read_text(encoding="utf-8"))
    return data[1:] if isinstance(data, list) else []


def _entry_id(entry: dict) -> str:
    owner = entry.get("user") or entry.get("project") or "unknown"
    return owner.lower().replace("/", "-")


def fetch(key: str, url: str) -> Path:
    """Cache downloads by owner+asset name: several sources reuse a repo name
    (morphe-patches) and version, so the asset name alone collides."""
    dest = CACHE / key.replace("/", "-")
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": "morphe-patch-audit"})
    with urllib.request.urlopen(req, timeout=180) as resp, dest.open("wb") as fh:
        while chunk := resp.read(1 << 16):
            fh.write(chunk)
    return dest


def source_files(source: str) -> tuple[list[Path], Path | None, list[str]]:
    """The .mpp bundles and CLI jar the build would use for this source.

    Mirrors run_build: bundles are every .mpp asset except compilation
    artefacts (-sources/-javadoc), and the CLI comes from the morphe-cli
    entry, falling back to any jar.
    """
    bundles: list[Path] = []
    jars: list[tuple[str, Path]] = []
    notes: list[str] = []
    for entry in source_entries(source):
        try:
            assets = utils.detect_release(entry).get("assets") or []
        except Exception as exc:  # noqa: BLE001 - report, do not abort the audit
            notes.append(f"release lookup failed for {entry}: {type(exc).__name__}: {exc}")
            continue
        for asset in assets:
            name = asset["name"]
            url = asset["browser_download_url"]
            if name.endswith(".mpp") and "-sources." not in name.lower() and "-javadoc." not in name.lower():
                try:
                    bundles.append(fetch(f"{_entry_id(entry)}-{name}", url))
                except Exception as exc:  # noqa: BLE001
                    notes.append(f"download failed {name}: {type(exc).__name__}: {exc}")
            elif name.endswith(".jar") and "-sources." not in name.lower() and "-javadoc." not in name.lower():
                jars.append((f"{_entry_id(entry)}-{name}", name, url))
    cli = None
    ranked = sorted(jars, key=lambda item: 0 if "morphe-cli" in item[1] else 1 if "morphe" in item[1] else 2)
    for key, name, url in ranked:
        if "dev" not in name.lower() or cli is None:
            try:
                cli = fetch(f"cli-{key}", url)
            except Exception as exc:  # noqa: BLE001
                notes.append(f"CLI download failed {name}: {type(exc).__name__}: {exc}")
        if cli is not None:
            break
    return bundles, cli, notes


def universe(bundles: list[Path], cli: Path, tag: str) -> tuple[dict[str, set[str]] | None, str | None]:
    """{patch name -> set of compatible packages (empty = any app)}.

    Deliberately no -f/--filter-package-name: it reports zero matches for
    bundles that clearly do define patches for the package, so it cannot be
    trusted as the oracle here.
    """
    out_file = OUT / f"{tag}.txt"
    cmd = ["java", "-jar", str(cli), "list-patches"]
    for bundle in bundles:
        cmd += ["--patches", str(bundle)]
    cmd += ["--with-descriptions=false", "--with-packages", "--out", str(out_file)]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if res.returncode != 0:
        return None, f"CLI exit {res.returncode}: {(res.stderr or '')[-300:]}"
    text = out_file.read_text(encoding="utf-8", errors="replace") if out_file.exists() else res.stdout
    result: dict[str, set[str]] = {}
    for block in re.split(r"^Index:", text, flags=re.M)[1:]:
        match = re.search(r"^Name:\s*(.+?)\s*$", block, re.M)
        if not match:
            continue
        packages = set(re.findall(r"^\s*Package name:\s*(\S+)\s*$", block, re.M))
        result.setdefault(match.group(1), set()).update(packages)
    return result, None


def patch_file_names(path: Path) -> list[tuple[str, str]]:
    names = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and line[0] in "+-":
            names.append((line[0], line[1:].strip()))
    return names


def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    config = json.loads(Path("patch-config.json").read_text(encoding="utf-8"))["patch_list"]
    pairs = {(entry["app_name"], entry["source"]) for entry in config}
    stems = {f"{app}-{source}" for app, source in pairs}
    sources_by_app: dict[str, list[str]] = {}
    for app, source in pairs:
        sources_by_app.setdefault(app, []).append(source)

    findings: list[tuple[str, str, str, str, str]] = []
    cache: dict[str, tuple[list[Path], Path | None, list[str]]] = {}
    for file_name in sorted(f for f in os.listdir("patches") if f.endswith(".txt")):
        stem = file_name[:-4]
        if stem not in stems:
            hint = next((app for app in sources_by_app if stem.startswith(f"{app}-")), None)
            known = f"app exists with sources {sources_by_app[hint]}" if hint else "no matching app/source"
            findings.append(("DEAD-FILE", file_name, "-", "-", f"never read ({known})"))
            continue

        app, source = next(pair for pair in pairs if f"{pair[0]}-{pair[1]}" == stem)
        names = patch_file_names(Path("patches") / file_name)
        if not names:
            findings.append(("EMPTY-FILE", file_name, app, source, "no +/- lines -> no effect"))
            continue

        if source not in cache:
            cache[source] = source_files(source)
        bundles, cli, notes = cache[source]
        for note in notes:
            findings.append(("CHECK-FAIL", file_name, app, source, note))
        if not bundles:
            findings.append(("NO-BUNDLE", file_name, app, source, "source exposes no .mpp bundle"))
            continue
        if cli is None:
            findings.append(("CHECK-FAIL", file_name, app, source, "no CLI jar found for source"))
            continue

        packs, err = universe(bundles, cli, source)
        if packs is None:
            findings.append(("CHECK-FAIL", file_name, app, source, err or "list-patches failed"))
            continue

        package = app_package(app)
        if not package:
            findings.append(("NO-PACKAGE", file_name, app, source, "package unknown: compatibility not verified"))

        ok = 0
        for sign, name in names:
            if name not in packs:
                close = difflib.get_close_matches(name, packs, n=2)
                findings.append(("MISSING", file_name, app, source,
                                 f"'{sign}{name}' defined by no bundle (closest: {close})"))
            elif package and packs[name] and package not in packs[name]:
                findings.append(("INCOMPATIBLE", file_name, app, source,
                                 f"'{sign}{name}' targets {sorted(packs[name])}, not {package}"))
            else:
                ok += 1
        print(f"  {file_name}: {len(names)} name(s), {ok} ok, bundles={len(bundles)}, universe={len(packs)}")

    print("\n==== FINDINGS ====")
    if not findings:
        print("  none - every patch file resolves against the bundles its source ships")
    for kind, file_name, app, source, detail in findings:
        print(f"  [{kind:12s}] {file_name:46s} app={app} source={source} :: {detail}")

    failing = [f for f in findings if f[0] in FAIL_KINDS]
    print(f"\n{len(failing)} blocking finding(s), {len(findings)} total")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
