# Source definitions

Each `<name>.json` here defines a patch bundle source, keyed by the `<source>`
value used in `patch-config.json` (see `sources/heinrich26.json`). The first
entry is always `{"name": "<name>"}`; the remaining entries are GitHub/GitLab
release references whose assets are downloaded and combined.

## `heinrich26` — points at a fork (read this before changing it)

`sources/heinrich26.json` references **`uzamapg/morphe-patches`** (a fork of
[`heinrich26/morphe-patches`](https://github.com/heinrich26/morphe-patches)),
not the upstream repo directly.

**Why:** the upstream `Unlock Pro` patch for Material Capsule
(`com.pryshedko.mtisland`) only works on the **unreleased** `main` branch. The
released `v1.0.1` bundle still uses the old `example` package, whose
`GetProStatusFingerprint` matches on non-obfuscated class/method names
(`Lcom/pryshedko/mtisland/model/datastore/DataStoreRepositoryBilling;` /
`getProStatus1`). Real release builds are R8-obfuscated, so that fingerprint
never matches and the patch fails with `Failed to match the fingerprint`.

The fork publishes a **rebuild of upstream `main`** as release `v1.0.2`
(asset `patches-1.0.2.mpp`), so the CI can consume the fix. Upstream is
GPL-3.0; the fork carries the complete corresponding source.

**Maintenance — when upstream publishes the fix:**

1. Check whether `heinrich26/morphe-patches` has a new release containing the
   generic-fingerprint `Unlock Pro` patch.
2. If so, switch `sources/heinrich26.json` back to
   `{"user": "heinrich26", "repo": "morphe-patches", "tag": "latest"}` and
   delete/archive the fork.
3. Verify by building `material-capsule`/`heinrich26` and confirming the log
   shows `Applied: Unlock Pro`.

To refresh the fork in the meantime (e.g. upstream pushes another fix to
`main` before releasing): sync the fork, rebuild the bundle with
`./gradlew :patches:build` (the Android `extensions/` module is not required by
this patch and can be excluded), then upload the new `patches-*.mpp` to a fresh
release.

## `heinrich26` also pulls in the Nai64 GitLab bundles

Besides the fork above, `sources/heinrich26.json` lists two GitLab bundles by
[kmru](https://gitlab.com/kmru):

- **`kmru/nai64patches`** — base bundle. Provides **`Pairip Bypass`**, the fix
  for Material Capsule's Play Store redirect.
- **`kmru/nai64extrapatches`** — companion bundle (400+ generic patches), a
  superset of the universal patches. Kept available so individual patches can be
  reachable for other apps; nothing is auto-applied from it.

**Why:** Material Capsule is protected by **Google Play PairIP**
(`com.pairip.licensecheck.LicenseClient` / `LicenseActivity`). On a repackaged
build, PairIP's license check fails and the app redirects to the Play Store.
`Pairip Bypass` (defaults `localInstallerChecks`, `storeSpoofChecks`,
`startupLauncherChecks` and `disableFirebase` all `true`) neutralises the
local installer check and spoofs a Play Store install source. This app has no
PairIP `StartupLauncher`, so those strategies simply do not match. See
`patches/material-capsule-heinrich26.txt`.

All patches in both Nai64 bundles are `default = false`, so nothing is
auto-applied to this app; only the explicitly listed ones run. The Nai64
bundles are plain `gitlab` source entries, resolved via the GitLab releases API
(`releases/permalink/latest`) — no token required, unlike GitHub.

**Bundle order:** `sources/heinrich26.json` lists the app-specific fork first
(its `.mpp` is the first one seen, which is what drives version detection),
then the targeted fix bundles, with the generic upstream `MorpheApp/morphe-patches`
last. Enable/disable flags are applied per bundle (see `src/__main__.py`), so
order does not affect which patches can be selected.

## Patch files (`patches/<app_name>-<source>.txt`)

A patch file is read only when its name is exactly `<app_name>-<source>.txt` for
an entry in `patch-config.json`: `+Name` enables a patch (`-e`) and `-Name`
disables one (`-d`). Every other line is ignored, and a file whose app or source
has since been renamed is never read at all.

The Morphe CLI **silently ignores** a name it does not define for the app's
package, and `--continue-on-error` keeps the build green when a patch's
fingerprint fails. A stale name therefore ships an APK that differs from what
the file claims, with no error anywhere - this is how the Material Capsule Play
Store redirect stayed hidden. Two guards exist:

- `src/__main__.py` (`_unapplied_requested`) logs an error when an `-e` name was
  requested but never reported as `Applied:` during the build.
- `scripts/audit_patch_names.py` audits every patch file against the bundles its
  source ships and the app's declared `package`, covering `-e` and `-d` without
  building anything. Run it after any source bump, because upstream renames
  patches between bundle versions (e.g. `BTTV and 7TV emotes` became
  `BTTV, FFZ and 7TV emotes`; ReVanced-era `Custom branding name/icon for
  YouTube` is now the single `Custom branding` patch):

      GITHUB_TOKEN=... python scripts/audit_patch_names.py   # exit 1 on findings
