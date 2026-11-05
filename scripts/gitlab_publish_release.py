#!/usr/bin/env python3
"""Publish built APKs to the GitLab 'latest' release.

Mirrors the GitHub patch.yml release flow:
1. Uploads every *.apk (+ manifest.json if present) in --apks-dir to the
   generic package registry (re-uploading the same filename overwrites).
2. Moves the 'latest' tag to the current commit and creates/updates the
   'latest' release.
3. Replaces the release's asset links with the current file set.
4. Deletes superseded older-version APKs (same identity prefix, not kept).

Usage:
    python scripts/gitlab_publish_release.py --apks-dir ./release-apks [--tag latest]
"""
import argparse
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import importlib.util as _ilu
def _load_gitlab_api():
    _spec = _ilu.spec_from_file_location(
        "gitlab_api", Path(__file__).resolve().parent.parent / "src" / "gitlab_api.py")
    _mod = _ilu.module_from_spec(_spec)
    sys.modules["gitlab_api"] = _mod
    _spec.loader.exec_module(_mod)
    return _mod
gitlab_api = _load_gitlab_api()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

# Same identity rule as scripts/cleanup_old_apks.py: {app}-{arch}- before -v{version}.apk
VERSION_MARKER = re.compile(r"-v\d[\d.()+\-]*\.apk$", re.IGNORECASE)


def identity_prefix(filename: str) -> str | None:
    m = VERSION_MARKER.search(filename)
    return filename[:m.start() + 1] if m else None


def build_release_notes(asset_names: list[str]) -> tuple[str, str]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    lines = ["# Morphe APKs - Auto Built (GitLab)", "", "## Available Apps", ""]
    for n in sorted(set(asset_names)):
        lines.append(f"- {n}")
    lines += [
        "", "---", "",
        "## Build Information",
        f"- **Auto-built {now} UTC**",
        "- **Multiple architecture support** (arm64-v8a, armeabi-v7a, universal)",
        "- **Latest Morphe patches**",
        "", "## Architecture Guide",
        "- **arm64-v8a**: Modern ARM devices (2014+)",
        "- **armeabi-v7a**: Older ARM devices",
        "- **universal**: All ARM devices (larger file)",
    ]
    return f"Morphe APKs - {now}", "\n".join(lines)


def rebuild_all_links(tag: str) -> int:
    """Recovery: ensure every APK in the package registry has a release asset link."""
    ref = os.environ.get("CI_COMMIT_SHA", "main")
    logging.info(f"Rebuilding asset links for release '{tag}' from package files...")

    pkg_files = gitlab_api.list_package_files()
    apk_files = [f for f in pkg_files if f.get("file_name", "").endswith(".apk")]
    logging.info(f"Found {len(apk_files)} APKs in package registry")

    # IMPORTANT: ensure_release() calls move_tag() which deletes/recreates the
    # tag. In GitLab, this wipes the release's asset links. So we must ensure
    # the release FIRST, then (re)create all links. Do NOT rely on a pre-wipe
    # listing of existing links.
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    gitlab_api.ensure_release(tag, f"Morphe APKs - {now}", "", ref)

    # After the tag move, existing links are gone. Create fresh for all APKs.
    # Use a set to deduplicate filenames in the package registry.
    seen = set()
    created = 0
    skipped = 0
    for pf in apk_files:
        name = pf["file_name"]
        if name in seen:
            skipped += 1
            continue
        seen.add(name)
        url = gitlab_api.package_file_url(name)
        try:
            r = gitlab_api.api("POST", f"/releases/{tag}/assets/links",
                                json={"name": name, "url": url, "link_type": "package"})
            r.raise_for_status()
        except Exception as e:
            logging.warning(f"Could not create link for {name}: {e}")
            continue
        created += 1
        if created % 20 == 0:
            logging.info(f"Created {created} links so far...")

    logging.info(f"Rebuild complete: {created} links created, {skipped} duplicates skipped.")
    return 0


def verify_release_healthy(tag: str) -> tuple[bool, str]:
    """Post-publish health check for the GitLab release.

    Returns (healthy, detail). The package registry is the source of truth:
    if it holds APKs but the release object is missing or has no asset
    links, the store shows every patched app as unavailable (seen 2026-10-09
    and 2026-10-22 when the publish step died after the tag move).
    list_asset_links() already retries through GitLab's consistency lag.
    """
    try:
        r = gitlab_api.api("GET", f"/releases/{tag}")
        if r.status_code == 404:
            return False, "release object is missing"
        r.raise_for_status()
    except Exception as e:
        return False, f"release check failed: {e}"[:200]
    links = gitlab_api.list_asset_links(tag)
    try:
        pkg_files = gitlab_api.list_package_files()
        expected = len({f.get("file_name", "") for f in pkg_files
                        if f.get("file_name", "").endswith(".apk")})
    except Exception as e:
        logging.warning(f"verify: could not list package files: {e}")
        expected = -1
    if expected > 0 and not links:
        return False, (f"release has 0 asset links but package registry "
                       f"holds {expected} APKs")
    return True, f"release OK ({len(links)} asset links)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apks-dir", required=False, default=None)
    ap.add_argument("--tag", default="latest")
    ap.add_argument("--merge", action="store_true",
                    help="Add/replace only these assets, keep existing links "
                         "(for single-app manual builds). Default replaces all.")
    ap.add_argument("--rebuild-links", action="store_true",
                    help="Recovery mode: rebuild all release asset links from "
                         "package files. Ignores --apks-dir.")
    ap.add_argument("--verify-only", action="store_true",
                    help="Check that the release exists and serves asset "
                         "links; exit 0 if healthy, 1 otherwise. "
                         "Ignores --apks-dir.")
    args = ap.parse_args()

    if args.rebuild_links:
        return rebuild_all_links(args.tag)

    if args.verify_only:
        healthy, detail = verify_release_healthy(args.tag)
        logging.info(f"Verify release '{args.tag}': {detail}")
        return 0 if healthy else 1

    if not args.apks_dir:
        ap.error("--apks-dir is required unless --rebuild-links is used")
    apks_dir = Path(args.apks_dir)
    apks = sorted(apks_dir.glob("*.apk"))
    manifest = apks_dir / "manifest.json"
    if not apks:
        logging.info("No APKs to publish; skipping release.")
        return 0

    # 1. Upload everything first (never delete before the new files are up).
    # GitLab rejects some filename characters (e.g. parentheses -> HTTP 400
    # "file_name is invalid"). Rename on disk first so build records,
    # manifest.json, asset links and package files all agree on the name.
    renames: dict[str, str] = {}
    for apk in apks:
        safe = gitlab_api.safe_filename(apk.name)
        if safe != apk.name:
            target = apk.with_name(safe)
            if target.exists():
                target.unlink()
            apk.rename(target)
            renames[apk.name] = safe
            logging.info(f"Renamed {apk.name} -> {safe} for GitLab")
            apk = target
    if renames and manifest.exists():
        try:
            import json as _json
            data = _json.loads(manifest.read_text(encoding="utf-8"))
            for entry in data.get("entries", {}).values():
                if entry.get("apk", "") in renames:
                    entry["apk"] = renames[entry["apk"]]
            manifest.write_text(_json.dumps(data, indent=2), encoding="utf-8")
            logging.info(f"Patched manifest.json for {len(renames)} renamed files")
        except Exception as e:
            logging.warning(f"Could not patch manifest.json filenames: {e}")
    apks = sorted(apks_dir.glob("*.apk"))

    urls: dict[str, str] = {}
    for apk in apks:
        urls[apk.name] = gitlab_api.upload_package_file(apk)
    if manifest.exists():
        urls[manifest.name] = gitlab_api.upload_package_file(manifest)

    # 2. Ensure release + set asset links.
    ref = os.environ.get("CI_COMMIT_SHA", "main")
    if args.merge:
        # Single-app manual build: keep existing assets, add/replace ours.
        # Preserve the existing release title/notes when the release exists.
        try:
            cur = gitlab_api.api("GET", f"/releases/{args.tag}").json()
            title, notes = cur.get("name") or "Morphe APKs", cur.get("description") or ""
        except Exception:
            title, notes = build_release_notes(list(urls))
        existing = {l["name"]: l for l in gitlab_api.list_asset_links(args.tag)}
        # The package registry is the source of truth for which APKs exist.
        # The asset-links API is flaky (consistency lag, empty listings), so
        # the restore set comes from package files, unioned with the link
        # listing. Relying on links alone meant a single empty API response
        # wiped every app from the release with nothing to restore.
        try:
            _pre_files = gitlab_api.list_package_files()
            _pre_apks = {f.get("file_name", "") for f in _pre_files
                         if f.get("file_name", "").endswith(".apk")}
        except Exception as e:
            logging.warning(f"Could not list package files pre-wipe: {e}")
            _pre_apks = set()
        restore_names = _pre_apks | {n for n in existing if n.endswith(".apk")}
        logging.info(f"Restore set: {len(restore_names)} APKs "
                     f"({len(_pre_apks)} from packages, {len(existing)} from links)")
        gitlab_api.ensure_release(args.tag, title, notes, ref)
        # NOTE: ensure_release() calls move_tag() which deletes/recreates the tag.
        # In GitLab, this wipes the release's asset links. Recreate links for
        # every APK in the restore set (old ones revived, new ones fresh below).
        _restored = 0
        for old_name in sorted(restore_names):
            if old_name in urls:
                continue  # Will be (re)created below as fresh upload
            url = gitlab_api.package_file_url(old_name)
            try:
                r = gitlab_api.api("POST", f"/releases/{args.tag}/assets/links",
                                    json={"name": old_name, "url": url, "link_type": "package"})
                if r.status_code in (200, 201):
                    _restored += 1
            except Exception:
                pass
        if _restored:
            logging.info(f"Restored {_restored} asset links wiped by tag move")
        for name, url in urls.items():
            # Old link was wiped by move_tag; just create the new one
            r = gitlab_api.api("POST", f"/releases/{args.tag}/assets/links",
                               json={"name": name, "url": url, "link_type": "package"})
            r.raise_for_status()
        # Build keep set from package files (reliable source of truth).
        # The asset-links API can return stale/empty data due to consistency
        # lag; never let a flaky listing cause mass deletion of good links.
        try:
            _pkg_files = gitlab_api.list_package_files()
            _pkg_apks = {f.get("file_name", "") for f in _pkg_files
                         if f.get("file_name", "").endswith(".apk")}
        except Exception as e:
            logging.warning(f"Could not list package files for keep-set: {e}")
            _pkg_apks = set()
        keep = set(urls) | _pkg_apks | (set(existing) - set(urls))
    else:
        title, notes = build_release_notes(list(urls))
        gitlab_api.ensure_release(args.tag, title, notes, ref)
        gitlab_api.replace_asset_links(args.tag, [(n, u) for n, u in urls.items()])
        keep = set(urls)
    # Clean up superseded APKs from the package registry.
    # The asset-links API is unreliable, so we list package files directly.
    # For each app prefix, keep only the files in 'keep' (current versions).
    try:
        all_files = gitlab_api.list_package_files()
        for f in all_files:
            name = f.get("file_name", "")
            if not name.endswith(".apk") or name in keep:
                continue
            prefix = identity_prefix(name)
            if not prefix:
                continue
            if any(k != name and k.startswith(prefix) for k in keep):
                logging.info(f"Deleting superseded package file: {name}")
                gitlab_api.delete_package_file(name)
    except Exception as e:
        logging.warning(f"Package cleanup failed: {e}")
    # Also clean up stale asset links if any exist
    all_links = gitlab_api.list_asset_links(args.tag)
    to_delete = []
    for link in all_links:
        name = link.get("name", "")
        if not name.endswith(".apk") or name in keep:
            continue
        prefix = identity_prefix(name)
        if not prefix:
            continue
        if any(k != name and (k.startswith(prefix)) for k in keep):
            to_delete.append(link)
    # Safety guard: refuse mass deletion (likely API inconsistency, not staleness)
    if all_links and len(to_delete) > len(all_links) * 0.3:
        raise RuntimeError(
            f"Refusing to delete {len(to_delete)}/{len(all_links)} asset links "
            f"(>30%). This likely indicates GitLab API inconsistency. Aborting."
        )
    for link in to_delete:
        logging.info(f"Deleting superseded asset link: {link.get('name')}")
        gitlab_api.delete_asset_link(args.tag, link["id"])

    if args.merge:
        # Refresh release notes from the final asset set: merge mode otherwise
        # preserves the old notes, which would list stale filenames.
        final_names = [l["name"] for l in gitlab_api.list_asset_links(args.tag)]
        if final_names:
            mtitle, mnotes = build_release_notes(final_names)
            # Do NOT call ensure_release() here: it calls move_tag(), which
            # deletes/recreates the tag and wipes all release asset links in
            # GitLab. Update the notes directly so the tag stays untouched.
            r = gitlab_api.api("PUT", f"/releases/{args.tag}",
                               json={"name": mtitle, "description": mnotes})
            r.raise_for_status()
            logging.info("Refreshed release notes (tag untouched)")

    logging.info("GitLab release publish complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
