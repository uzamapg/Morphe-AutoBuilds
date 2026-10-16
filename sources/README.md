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
