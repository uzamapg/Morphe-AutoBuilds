<div align="center">

# 🔧 Automated Android Build Pipeline

[![Daily Build](https://img.shields.io/github/actions/workflow/status/uzamapg/Morphe-AutoBuilds/patch.yml?label=Daily%20Build&style=for-the-badge&color=2ea44f)](https://github.com/uzamapg/Morphe-AutoBuilds/actions/workflows/patch.yml)
[![Patch Name Audit](https://img.shields.io/github/actions/workflow/status/uzamapg/Morphe-AutoBuilds/audit-patch-names.yml?label=Patch%20Name%20Audit&style=for-the-badge&color=2ea44f)](https://github.com/uzamapg/Morphe-AutoBuilds/actions/workflows/audit-patch-names.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <strong>Config-driven CI builds for Android</strong><br>
  Multi-source • Multi-architecture • GitHub Actions Powered
</p>

<p align="center">
A sophisticated, automated pipeline that assembles installable Android applications for <strong>non-rooted devices</strong>. The system fetches build tooling, downloads base APKs from multiple sources, applies community build configurations, and produces architecture-specific outputs.
</p>

[![Report Bug](https://img.shields.io/badge/Report%20Bug-0A0A0A?style=flat&logo=github&logoColor=white)](https://github.com/uzamapg/Morphe-AutoBuilds/issues)
[![Request Feature](https://img.shields.io/badge/Request%20Feature-0A0A0A?style=flat&logo=github&logoColor=white)](https://github.com/uzamapg/Morphe-AutoBuilds/issues)

</div>

---

> **ℹ️ Nothing is hosted in this repository.** There are no APK files here — this is the build automation.
> Builds run every day at **06:00 UTC** and are published to the
> [**`latest` release**](https://github.com/uzamapg/Morphe-AutoBuilds/releases/tag/latest).

> [!NOTE]
> **This repository is a fork.** It is based on
> [**RookieEnough/Morphe-AutoBuilds**](https://github.com/RookieEnough/Morphe-AutoBuilds), kept here as the
> `upstream` git remote — credit for the original pipeline belongs there.
>
> **Everything added in this fork is AI-assisted.** The extra patch sources and bundles, the
> patch-file repairs, the guard and audit tooling, and this README are all written with the help of
> AI coding agents, then verified by running the pipeline against the live bundles.

## ⚡ At a Glance

| Metric | Value |
|:----------------------------|:----------------------------------------------------------|
| 📱 **Apps configured** | **455** |
| 🧩 **Patch sources** | **63** community sources |
| 🔨 **App × source builds** | **562** configured combinations |
| 🏗️ **Architectures** | `universal`, `arm64-v8a`, `armeabi-v7a` — mixed per app |
| ⏱️ **Build schedule** | Daily at **06:00 UTC**, plus on-demand runs |
| 🔐 **Signing** | One consistent public keystore — updates install over the previous build |
| 📤 **Release model** | The `latest` release is replaced, never archived |

## 🚀 Getting a Build

1. Open the [**`latest` release**](https://github.com/uzamapg/Morphe-AutoBuilds/releases/tag/latest).
2. Download the asset matching your app — assets are named `<app>-<arch>-<source>-v<version>.apk`:
   * `universal` — every ARM ABI in a single file.
   * `arm64-v8a` / `armeabi-v7a` — smaller, split per architecture.
   * `<source>` — the patch bundle that produced it; the same app can be published from several sources.
3. Install it. Every build is signed with the same keystore, so a newer build installs straight over the
   previous one.

> **Dependency:** most patched apps expect **Morphe's MicroG-RE (GmsCore)** to be installed for sign-in and
> Play Services to work.

### 🩹 Troubleshooting

<details>
<summary><b>The accessibility service toggle does nothing (Android 13+ / OxygenOS 15)</b></summary>

<br>

Apps installed from a file manager count as sideloaded on Android 13+ and are
blocked from using accessibility services: the toggle in the system settings
silently reverts, and logcat shows
`Skipping enabling service disallowed by device admin policy`. OxygenOS 15 no
longer offers the "⋮ → Allow restricted settings" menu entry. Either fix
works:

* Install the APK with a **session-based installer** such as
  [InstallerX Revived](https://github.com/wxxsfxyzm/InstallerX-Revived) — the
  app is then not tagged as sideloaded. Recommended on OxygenOS 15.
* Or lift the restriction with adb (or an on-device shell such as Shizuku/LADB):

  ```bash
  adb shell cmd appops set <package> ACCESS_RESTRICTED_SETTINGS allow
  ```

  Verify with `cmd appops get <package> ACCESS_RESTRICTED_SETTINGS` (`allow`).

Both fixes are undone the next time an update is installed from a file
manager, so re-apply them after any such update.

</details>

<details>
<summary><b><code>App not installed</code> — an existing copy is signed with a different key</b></summary>

<br>

The device already has a build of the same package signed with another key —
typically the official app from the Play Store. Android refuses to replace it.
Uninstall the installed copy (this removes its data) and install the new build.
Every build published here shares one keystore, so later updates install over
the top without uninstalling again.

</details>

## 📦 Apps & Patch Sources

Each app is rebuilt for every community source that ships patches for it, which is why the same app can
appear under several sources — one APK per source. The list below is derived from
[`patch-config.json`](patch-config.json), [`arch-config.json`](arch-config.json), the app definitions in
[`apps/`](apps) and the option files in [`patches/`](patches).

<details>
<summary><b>Click to expand</b> — 455 apps · 562 app&nbsp;×&nbsp;source builds · 63 patch sources</summary>

Each source below is one entry of `patch-config.json`. A source that ships patches for an app produces its own APK (`<app>-<arch>-<source>-v<version>.apk`), so the same app can appear under several sources. `universal` means every ARM ABI in one file; an explicit list means the build was split per architecture (`arch-config.json`). A `—` in the *Package* column means the app definition under `apps/` carries no `package` value.

#### 🧩 Sources

| Source | Apps | Patch bundle source(s) |
|:-------|-----:|:-----------------------|
| `Hoo` | 49 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`hoo-dles/morphe-patches`](https://github.com/hoo-dles/morphe-patches) `@latest` |
| `adobo` | 5 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`jkennethcarino/adobo`](https://github.com/jkennethcarino/adobo) `@latest` |
| `aimal` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`hashtagbasit/aimal-patches`](https://github.com/hashtagbasit/aimal-patches) `@prerelease` |
| `akash-photos` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`Akash-Sriram/morphe-google-photos`](https://github.com/Akash-Sriram/morphe-google-photos) `@latest` |
| `almewty` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`Almewty/my-morphe-patches`](https://github.com/Almewty/my-morphe-patches) `@v1.0.0-dev.1` |
| `ample-dev` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`AmpleRevanced/revanced-patches`](https://github.com/AmpleRevanced/revanced-patches) `@dev` |
| `andrew` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`andrewliang25/morphe-patches`](https://github.com/andrewliang25/morphe-patches) `@latest` |
| `androidtv` | 15 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`ajstrick81/morphe-androidtv-patches`](https://github.com/ajstrick81/morphe-androidtv-patches) `@latest` |
| `binarymend` | 6 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`binarymend/morphe-patches`](https://github.com/binarymend/morphe-patches) `@latest` |
| `blazskufca` | 1 | [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) `@latest`<br>[`blazskufca/revanced-patch`](https://github.com/blazskufca/revanced-patch) `@latest` |
| `breal` | 15 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`brealorg/breal-morphe-patches`](https://github.com/brealorg/breal-morphe-patches) `@latest` |
| `brosssh` | 7 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`brosssh/morphe-patches`](https://github.com/brosssh/morphe-patches) `@latest` |
| `browzomje` | 2 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`browzomje/browzomje-patches`](https://github.com/browzomje/browzomje-patches) `@latest` |
| `bufferk` | 5 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`bufferk/morphe-patches`](https://github.com/bufferk/morphe-patches) `@latest` |
| `burgers` | 1 | [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) `@latest`<br>[`burgers1312/revanced-patches`](https://github.com/burgers1312/revanced-patches) `@latest` |
| `canh0chua` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`canh0chua/Morphe-patches`](https://github.com/canh0chua/Morphe-patches) `@latest` |
| `chiggi` | 6 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`durgesh0505/chiggi_morphe_patches`](https://github.com/durgesh0505/chiggi_morphe_patches) `@latest` |
| `chirag` | 6 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`chirag127/morphe-patches`](https://github.com/chirag127/morphe-patches) `@latest` |
| `d0nj` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`d0nj/morphe-patches`](https://github.com/d0nj/morphe-patches) `@latest` |
| `devanced` | 24 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`RookieEnough/De-Vanced`](https://github.com/RookieEnough/De-Vanced) `@prerelease` |
| `dmoniak` | 78 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`SatanMerde/D-moniakPatches`](https://github.com/SatanMerde/D-moniakPatches) `@latest` |
| `docbt` | 2 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`docbt/patched-up`](https://github.com/docbt/patched-up) `@latest` |
| `dropped` | 2 | [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) `@v5.0.1`<br>[`indrastorms/Dropped-Patches`](https://github.com/indrastorms/Dropped-Patches) `@latest` |
| `dudeks` | 7 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`dawidd612/dudeks-morphe-patches`](https://github.com/dawidd612/dudeks-morphe-patches) `@latest` |
| `epxec` | 14 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`epxec/android-patches`](https://github.com/epxec/android-patches) `@latest` |
| `fripe070` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`Fripe070/PixivPatches`](https://github.com/Fripe070/PixivPatches) `@latest` |
| `ftl` | 13 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`BlazeFTL/FTL-Patches`](https://github.com/BlazeFTL/FTL-Patches) `@latest` |
| `hakim` | 2 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`kim20598/hakim-morphe-patches`](https://github.com/kim20598/hakim-morphe-patches) `@latest` |
| `heinrich26` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`uzamapg/morphe-patches`](https://github.com/uzamapg/morphe-patches) `@latest`<br>[`kmru/nai64patches`](https://gitlab.com/kmru/nai64patches) `@latest`<br>[`kmru/nai64extrapatches`](https://gitlab.com/kmru/nai64extrapatches) `@latest`<br>[`MorpheApp/morphe-patches`](https://github.com/MorpheApp/morphe-patches) `@latest` |
| `heval` | 27 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`heval99/Heval-Morphe-Patches`](https://github.com/heval99/Heval-Morphe-Patches) `@latest` |
| `hooman` | 31 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`arandomhooman/hoomans-morphe-patches`](https://github.com/arandomhooman/hoomans-morphe-patches) `@latest` |
| `hoomans` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`arandomhooman/hoomans-morphe-patches`](https://github.com/arandomhooman/hoomans-morphe-patches) `@latest` |
| `hush-facebook` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`SysAdminDoc/HushFacebook`](https://github.com/SysAdminDoc/HushFacebook) `@latest` |
| `hush-feed` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`SysAdminDoc/HushFeed`](https://github.com/SysAdminDoc/HushFeed) `@latest` |
| `hush-gram` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`SysAdminDoc/HushGram`](https://github.com/SysAdminDoc/HushGram) `@latest` |
| `hush-messenger` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`SysAdminDoc/HushMessenger`](https://github.com/SysAdminDoc/HushMessenger) `@latest` |
| `hush-threads` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`SysAdminDoc/HushThreads`](https://github.com/SysAdminDoc/HushThreads) `@latest` |
| `hushmessenger` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`SysAdminDoc/HushMessenger`](https://github.com/SysAdminDoc/HushMessenger) `@latest` |
| `hxreborn` | 37 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`hxreborn/morphe-patches`](https://github.com/hxreborn/morphe-patches) `@latest` |
| `icysymmetra` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`icysymmetra/tiktok-patches-for-morphe`](https://github.com/icysymmetra/tiktok-patches-for-morphe) `@latest` |
| `jasonwu1994` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`jasonwu1994/Gboard-patches`](https://github.com/jasonwu1994/Gboard-patches) `@latest` |
| `jouss` | 22 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`Joussflls10/Jouss-Patches`](https://github.com/Joussflls10/Jouss-Patches) `@latest` |
| `kim20598` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`kim20598/hakim-morphe-patches`](https://github.com/kim20598/hakim-morphe-patches) `@latest` |
| `kondratjev` | 10 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`kondratjev/morphe-patches`](https://github.com/kondratjev/morphe-patches) `@latest` |
| `kveld` | 5 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`kveld9/kveld-morphe-patches`](https://github.com/kveld9/kveld-morphe-patches) `@latest` |
| `lain` | 24 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`kiraio-moe/Lain-Patches`](https://github.com/kiraio-moe/Lain-Patches) `@latest` |
| `liaralabs` | 1 | [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) `@latest`<br>[`liaralabs/revanced-patches`](https://github.com/liaralabs/revanced-patches) `@latest` |
| `media` | 11 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`HellLord77/media-patches`](https://github.com/HellLord77/media-patches) `@latest` |
| `morphe` | 3 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`MorpheApp/morphe-patches`](https://github.com/MorpheApp/morphe-patches) `@latest` |
| `mvaishak` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`mvaishak/letterboxd-morphe-patches`](https://github.com/mvaishak/letterboxd-morphe-patches) `@latest` |
| `okish` | 33 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`byehi98/okish-morphe-patches`](https://github.com/byehi98/okish-morphe-patches) `@latest` |
| `paresh` | 15 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`Paresh-Maheshwari/paresh-patches`](https://gitlab.com/Paresh-Maheshwari/paresh-patches) `@latest` |
| `piko` | 2 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`crimera/piko`](https://github.com/crimera/piko) `@latest` |
| `piko-newx` | 2 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`crimera/piko-newx`](https://github.com/crimera/piko-newx) `@latest` |
| `pixelpusher` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`PixelPusher247/morphe-patches`](https://github.com/PixelPusher247/morphe-patches) `@latest` |
| `pyflat` | 3 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`PyFlat-JR/Morphe-Patches`](https://github.com/PyFlat-JR/Morphe-Patches) `@latest` |
| `revanced-kitadai31` | 4 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`Peanut-Butter-bread/idk`](https://github.com/Peanut-Butter-bread/idk) `@latest` |
| `rookie` | 6 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`RookieEnough/De-ReVanced`](https://github.com/RookieEnough/De-ReVanced) `@latest` |
| `rushiranpise` | 17 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`rushiranpise/morphe-patches`](https://github.com/rushiranpise/morphe-patches) `@latest` |
| `ryykitty-twitch` | 1 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`ryykitty/twitch-patched`](https://github.com/ryykitty/twitch-patched) `@latest` |
| `taknok` | 1 | [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) `@latest`<br>[`Taknok/revanced-patches`](https://github.com/Taknok/revanced-patches) `@latest` |
| `xhehab` | 13 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`Xhehab/Xhehab-Patches`](https://github.com/Xhehab/Xhehab-Patches) `@latest` |
| `xtra` | 13 | [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) `@latest`<br>[`BholeyKaBhakt/android-patches-xtra`](https://github.com/BholeyKaBhakt/android-patches-xtra) `@latest` |

#### 📱 Apps by source

<details>
<summary><code>Hoo</code> — 49 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`hoo-dles/morphe-patches`](https://github.com/hoo-dles/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| adguard | `com.adguard.android` | `universal` | — |
| aiocal | `all.in.one.calculator` | `universal` | — |
| avocards | `com.avocards` | `universal` | — |
| bussu | — | `universal` | — |
| busuu | `com.busuu.android.enc` | `universal` | — |
| cake | `me.mycake` | `universal` | — |
| camscanner | `com.intsig.camscanner` | `universal` | — |
| crunchyroll | `com.crunchyroll.crunchyroid` | `universal` | — |
| duolingo | `com.duolingo` | `universal` | — |
| eggbun | `kr.eggbun.eggconvo` | `universal` | — |
| fotmob | `com.mobilefootie.wc2010` | `universal` | — |
| goodreads | `com.goodreads` | `universal` | — |
| google-news | `com.google.android.apps.magazines` | `universal` | — |
| hellochinese | `com.hellochinese` | `universal` | — |
| ibs_paint | `jp.ne.ibis.ibispaintx.app` | `universal` | [`ibs_paint-Hoo.txt`](patches/ibs_paint-Hoo.txt) |
| icon-packer | `cn.ommiao.iconpacker` | `universal` | — |
| lightroom | `com.adobe.lrmobile` | `universal` | — |
| lingory | `org.languageapp.lingory` | `universal` | [`lingory-Hoo.txt`](patches/lingory-Hoo.txt) |
| lyfta | `com.lyfta` | `universal` | — |
| macrofactor | `com.sbs.diet` | `universal` | — |
| macrofactor-workout | `com.sbs.train` | `universal` | — |
| meme | `com.zombodroid.MemeGenerator` | `universal` | — |
| mimo | `com.getmimo` | `universal` | — |
| mirinae | `com.mirinae.mirinae` | `universal` | — |
| my-expenses | `org.totschnig.myexpenses` | `universal` | — |
| myfitnesspal | `com.myfitnesspal.android` | `universal` | — |
| niagara | `bitpit.launcher` | `universal` | — |
| nomone | `nom.vrd` | `universal` | — |
| nova | `com.teslacoilsw.launcher` | `universal` | — |
| pandora | `com.pandora.android` | `universal` | — |
| podcast | `com.bambuna.podcastaddict` | `universal` | — |
| prime-video | `com.amazon.avod.thirdpartyclient` | `universal` | — |
| proton-vpn | `ch.protonvpn.android` | `universal` | — |
| pydroid | — | `universal` | — |
| sleep-android | `com.urbandroid.sleep` | `universal` | — |
| smart_launcher | `ginlemon.flowerfree` | `universal` | — |
| snorelab | `com.snorelab.app` | `universal` | — |
| sofascore | `com.sofascore.results` | `universal` | — |
| solid | `pl.solidexplorer2` | `universal` | — |
| soundcloud | `com.soundcloud.android` | `universal` | — |
| teuida | `net.teuida.teuida` | `universal` | — |
| ttmik-stories | `app.ttmikstories.android` | `universal` | — |
| ventusky | `cz.ackee.ventusky` | `universal` | — |
| wallcraft | `com.wallpaperscraft.wallpaper` | `universal` | — |
| webster | `com.merriamwebster` | `universal` | — |
| windy | `com.windyty.android` | `universal` | — |
| wps-office | `cn.wps.moffice_eng` | `universal` | — |
| xodo | `com.xodo.pdf.reader` | `universal` | — |
| xrecorder | `videoeditor.videorecorder.screenrecorder` | `universal` | — |

</details>

<details>
<summary><code>adobo</code> — 5 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`jkennethcarino/adobo`](https://github.com/jkennethcarino/adobo) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| gboard | `com.google.android.inputmethod.latin` | `universal` | — |
| imdb | `com.imdb.mobile` | `universal` | — |
| ninegag | `com.ninegag.android.app` | `universal` | — |
| pinterest | `com.pinterest` | `universal` | [`pinterest-adobo.txt`](patches/pinterest-adobo.txt) |
| reddit | `com.reddit.frontpage` | `universal` | — |

</details>

<details>
<summary><code>aimal</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`hashtagbasit/aimal-patches`](https://github.com/hashtagbasit/aimal-patches) @prerelease (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| disney-plus | `com.disney.disneyplus` | `universal` | — |

</details>

<details>
<summary><code>akash-photos</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`Akash-Sriram/morphe-google-photos`](https://github.com/Akash-Sriram/morphe-google-photos) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| google-photos | `com.google.android.apps.photos` | `universal` | [`google-photos-akash-photos.txt`](patches/google-photos-akash-photos.txt) |

</details>

<details>
<summary><code>almewty</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`Almewty/my-morphe-patches`](https://github.com/Almewty/my-morphe-patches) @v1.0.0-dev.1 (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| pokecardex | `com.application.pokecardex` | `arm64-v8a`, `armeabi-v7a` | — |

</details>

<details>
<summary><code>ample-dev</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`AmpleRevanced/revanced-patches`](https://github.com/AmpleRevanced/revanced-patches) @dev (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| kakaotalk | `com.kakao.talk` | `universal` | — |

</details>

<details>
<summary><code>andrew</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`andrewliang25/morphe-patches`](https://github.com/andrewliang25/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| line | `jp.naver.line.android` | `universal` | — |

</details>

<details>
<summary><code>androidtv</code> — 15 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`ajstrick81/morphe-androidtv-patches`](https://github.com/ajstrick81/morphe-androidtv-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| amazon-video | `com.amazon.amazonvideo.livingroom` | `universal` | — |
| atbat | `com.bamnetworks.mobile.android.gameday.atbat` | `universal` | — |
| disney-plus | `com.disney.disneyplus` | `universal` | — |
| espn | `com.espn.score_center` | `universal` | — |
| foxone | `com.fox.foxone` | `universal` | — |
| hbo-max | `com.wbd.hbomax` | `universal` | — |
| paramount | `com.cbs.ott` | `universal` | — |
| peacock | `com.peacocktv.peacockandroid` | `universal` | — |
| plex | `com.netflix.ninja` | `universal` | — |
| pluto-tv | `tv.pluto.android` | `universal` | — |
| rain | `it.rainet.androidtv` | `universal` | — |
| rte-player | `com.twentyfouri.tvbridge.rte` | `universal` | — |
| tubi | `com.tubitv` | `universal` | — |
| twitch | `tv.twitch.android.app` | `universal` | — |
| univision | `com.univision.prendetv` | `universal` | — |

</details>

<details>
<summary><code>binarymend</code> — 6 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`binarymend/morphe-patches`](https://github.com/binarymend/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| acalendar | `org.withouthat.acalendar` | `universal` | — |
| moonreader | `com.flyersoft.moonreader` | `universal` | — |
| notecal | `com.burton999.notecal` | `universal` | — |
| pinterest | `com.pinterest` | `universal` | — |
| quickcursor | `com.quickcursor` | `universal` | — |
| truecaller | `com.truecaller` | `universal` | — |

</details>

<details>
<summary><code>blazskufca</code> — 1 app</summary>

**Bundle source(s):** [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) @latest (GitHub), [`blazskufca/revanced-patch`](https://github.com/blazskufca/revanced-patch) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| mladinska | `com.mladinska.mkplus` | `universal` | — |

</details>

<details>
<summary><code>breal</code> — 15 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`brealorg/breal-morphe-patches`](https://github.com/brealorg/breal-morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| continuum | `org.cygnusx1.continuum` | `universal` | — |
| imgur | `com.imgur.mobile` | `universal` | — |
| infinity-for-reddit-plus | `ml.docilealligator.infinityforreddit.plus` | `universal` | — |
| joey | `o.o.joey` | `universal` | — |
| joey-dev | `o.o.joey.dev` | `universal` | — |
| joey-pro | `o.o.joey.pro` | `universal` | — |
| lemmysync | `io.syncapps.lemmy_sync` | `universal` | — |
| patreon | `ml.docilealligator.infinityforreddit.patreon` | `universal` | — |
| premium | `com.onelouder.baconreader.premium` | `universal` | — |
| reddit-sync-dev | `com.laurencedawson.reddit_sync.dev` | `universal` | — |
| reddit-sync-pro | `com.laurencedawson.reddit_sync.pro` | `universal` | — |
| redditdonation | `com.andrewshu.android.redditdonation` | `universal` | — |
| redditslide | `me.edgan.redditslide` | `universal` | — |
| redditsync | `com.laurencedawson.reddit_sync` | `universal` | — |
| relay-for-reddit | `reddit.news` | `universal` | [`relay-for-reddit-breal.txt`](patches/relay-for-reddit-breal.txt) |

</details>

<details>
<summary><code>brosssh</code> — 7 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`brosssh/morphe-patches`](https://github.com/brosssh/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| calistree | — | `universal` | — |
| chargeprice | `fr.chargeprice.app` | `universal` | — |
| geocaching | — | `universal` | — |
| hevy | `com.hevy` | `universal` | — |
| komoot | `de.komoot.android` | `universal` | — |
| mapy | `cz.seznam.mapy` | `universal` | — |
| park4night | `fr.tramb.park4night` | `universal` | — |

</details>

<details>
<summary><code>browzomje</code> — 2 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`browzomje/browzomje-patches`](https://github.com/browzomje/browzomje-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| easy-sudoku | `easy.sudoku.puzzle.solver.free` | `universal` | — |
| pinterest | `com.pinterest` | `universal` | — |

</details>

<details>
<summary><code>bufferk</code> — 5 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`bufferk/morphe-patches`](https://github.com/bufferk/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| bounce | `com.bounce.connect` | `universal` | — |
| medium | `com.medium.reader` | `universal` | — |
| mygate | `com.mygate.user` | `universal` | — |
| splitwise | `com.Splitwise.SplitwiseMobile` | `universal` | — |
| truecaller | `com.truecaller` | `universal` | — |

</details>

<details>
<summary><code>burgers</code> — 1 app</summary>

**Bundle source(s):** [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) @latest (GitHub), [`burgers1312/revanced-patches`](https://github.com/burgers1312/revanced-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| splitwise | `com.Splitwise.SplitwiseMobile` | `universal` | — |

</details>

<details>
<summary><code>canh0chua</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`canh0chua/Morphe-patches`](https://github.com/canh0chua/Morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| viber | `com.viber.voip` | `universal` | [`viber-canh0chua.txt`](patches/viber-canh0chua.txt) |

</details>

<details>
<summary><code>chiggi</code> — 6 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`durgesh0505/chiggi_morphe_patches`](https://github.com/durgesh0505/chiggi_morphe_patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| crazygames | `com.crazygames.crazygamesapp` | `universal` | — |
| hotstar | `in.startv.hotstar` | `universal` | — |
| jiotvplus | `com.jio.media.jiotvplus` | `universal` | — |
| sonyliv | `com.sonyliv` | `universal` | — |
| threads | `com.instagram.barcelona` | `universal` | — |
| vimtv | `com.vimtv` | `universal` | — |

</details>

<details>
<summary><code>chirag</code> — 6 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`chirag127/morphe-patches`](https://github.com/chirag127/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| creativeassistant | `com.google.android.apps.pixel.creativeassistant` | `universal` | — |
| github | `com.github.android` | `universal` | — |
| google-news | `com.google.android.apps.magazines` | `universal` | — |
| linkedin | `com.linkedin.android` | `universal` | — |
| truecaller | `com.truecaller` | `universal` | — |
| whatsapp | `com.whatsapp` | `universal` | — |

</details>

<details>
<summary><code>d0nj</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`d0nj/morphe-patches`](https://github.com/d0nj/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| niagara | `bitpit.launcher` | `universal` | — |

</details>

<details>
<summary><code>devanced</code> — 24 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`RookieEnough/De-Vanced`](https://github.com/RookieEnough/De-Vanced) @prerelease (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| amazon-music | `com.amazon.mp3` | `universal` | — |
| amazon-shopping | `com.amazon.mShop.android.shopping` | `universal` | — |
| angulus | `com.drinkplusplus.angulus` | `universal` | — |
| bandcamp | `com.bandcamp.android` | `universal` | — |
| cricbuzz | `com.cricbuzz.android` | `universal` | — |
| facebook | `com.facebook.katana` | `universal` | — |
| gmx-mail | `de.gmx.mobile.android.mail` | `universal` | — |
| google-photos | `com.google.android.apps.photos` | `universal` | — |
| google-recorder | `com.google.android.apps.recorder` | `universal` | — |
| hexeditor | `com.myprog.hexedit` | `universal` | — |
| icon-pack-studio | — | `universal` | — |
| irplus | `net.binarymode.android.irplus` | `universal` | — |
| letterboxd | `com.letterboxd.letterboxd` | `universal` | — |
| messenger | `com.facebook.orca` | `universal` | — |
| nothing-x | `com.nothing.smartcenter` | `universal` | — |
| nu-nl | `nl.sanomamedia.android.nu` | `universal` | — |
| officelens | `com.microsoft.office.officelens` | `universal` | — |
| peacock | `com.peacocktv.peacockandroid` | `universal` | — |
| photomath | `com.microblink.photomath` | `universal` | — |
| photoshop-mix | `com.adobe.photoshopmix` | `universal` | — |
| pixiv | `jp.pxv.android` | `universal` | — |
| strava | `com.strava` | `universal` | — |
| twitch | `tv.twitch.android.app` | `universal` | — |
| viber | `com.viber.voip` | `universal` | — |

</details>

<details>
<summary><code>dmoniak</code> — 78 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`SatanMerde/D-moniakPatches`](https://github.com/SatanMerde/D-moniakPatches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| alltrails | `com.alltrails.alltrails` | `universal` | — |
| altosadventure | `com.noodlecake.altosadventure` | `universal` | — |
| baba | `com.rovio.baba` | `universal` | — |
| bard | `com.google.android.apps.bard` | `universal` | — |
| bitwarden | `com.x8bit.bitwarden` | `universal` | — |
| brave | `com.brave.browser` | `universal` | — |
| camscanner | `com.intsig.camscanner` | `universal` | — |
| canva | `com.canva.editor` | `universal` | — |
| chatgpt | `com.openai.chatgpt` | `universal` | — |
| claude | `com.anthropic.claude` | `universal` | — |
| client | `org.nextcloud.client` | `universal` | — |
| coinidentifyer | `com.coinidentifyer.ai` | `universal` | — |
| crash-of-titans | `com.zeptolab.ctr.ads` | `universal` | — |
| crossyroad | `com.yodo1.crossyroad` | `universal` | — |
| dantheman | `com.halfbrick.dantheman` | `universal` | — |
| deepl | `com.deepl.mobile.android` | `universal` | — |
| dialer | `com.google.android.dialer` | `universal` | — |
| doodle-jump | `com.lima.doodlejump` | `universal` | — |
| drive | `me.proton.android.drive` | `universal` | — |
| dubox | `com.dubox.drive` | `universal` | — |
| duolingo | `com.duolingo` | `universal` | — |
| euria | `com.infomaniak.euria` | `universal` | — |
| firefox | `org.mozilla.firefox` | `universal` | — |
| flightradar24 | `com.flightradar24free` | `universal` | — |
| fruitninja | `com.halfbrick.fruitninja` | `universal` | — |
| geometryjump | `com.robtopx.geometryjump` | `universal` | — |
| google-docs | `com.google.android.apps.docs` | `universal` | — |
| google-maps | `com.google.android.apps.maps` | `universal` | — |
| google-photos | `com.google.android.apps.photos` | `universal` | — |
| googleplay | `com.vectorunit.cobalt.googleplay` | `universal` | — |
| guessthecountry | `com.qbis.guessthecountry` | `universal` | — |
| hideme-vpn | `hideme.android.vpn` | `universal` | — |
| hill-climb | `com.fingersoft.hillclimb` | `universal` | — |
| hungry-shark-evolution | `com.fgol.HungrySharkEvolution` | `universal` | — |
| hungrysharkheroes | `com.ubisoft.hungrysharkheroes` | `universal` | — |
| hungrysharkworld | `com.ubisoft.hungrysharkworld` | `universal` | — |
| jetpackjoyride | `com.halfbrick.jetpackjoyride` | `universal` | — |
| lat-vpn | `com.vpn.lat` | `universal` | — |
| loki-messenger | `network.loki.messenger` | `universal` | — |
| memrise | `com.memrise.android.memrisecompanion` | `universal` | — |
| mx-player | `com.mxtech.videoplayer.ad` | `universal` | — |
| mx-player-tv | `com.movix.app` | `universal` | — |
| peak | `com.brainbow.peak.app` | `universal` | — |
| perplexity | `ai.perplexity.app.android` | `universal` | — |
| photomath | `com.microblink.photomath` | `universal` | — |
| pinterest | `com.pinterest` | `universal` | — |
| privacy | `mega.privacy.android.app` | `universal` | — |
| proton-mail | `ch.protonmail.android` | `universal` | — |
| proton-pass | `proton.android.pass` | `universal` | — |
| pvzfreerow | `com.ea.game.pvzfree_row` | `universal` | — |
| robbery-bob | `com.chillingo.robberybobfree.android.row` | `universal` | — |
| securesms | `org.thoughtcrime.securesms` | `universal` | — |
| shades | `com.nekki.shadowfight.shades` | `universal` | — |
| shadowfight | `com.nekki.shadowfight` | `universal` | — |
| shadowfight3 | `com.nekki.shadowfight3` | `universal` | — |
| shadowfightarena | `com.nekki.shadowfightarena` | `universal` | — |
| shazam | `com.shazam.android` | `universal` | — |
| simplex | `chat.simplex.app` | `universal` | — |
| snapchat | `com.snapchat.android` | `universal` | — |
| soundcloud | `com.soundcloud.android` | `universal` | — |
| specialedition | `com.nekki.shadowfight2.specialedition` | `universal` | — |
| speedtest | `org.zwanoo.android.speedtest` | `universal` | — |
| spotify | `com.spotify.music` | `universal` | — |
| stellarium | `com.noctuasoftware.stellarium` | `universal` | — |
| stellarium-free | `com.noctuasoftware.stellarium_free` | `universal` | — |
| strava | `com.strava` | `universal` | — |
| subwaysurf | `com.kiloo.subwaysurf` | `universal` | — |
| telegram | `org.telegram.messenger` | `universal` | — |
| templerun2 | `com.imangi.templerun2` | `universal` | — |
| truecaller | `com.truecaller` | `universal` | — |
| turbovpn | `free.vpn.unblock.proxy.turbovpn` | `universal` | — |
| twitch | `tv.twitch.android.app` | `universal` | — |
| vector2 | `com.nekki.vector2` | `universal` | — |
| vlc | `org.videolan.vlc` | `universal` | — |
| waze | `com.waze` | `universal` | — |
| windscribe | `com.windscribe.vpn` | `universal` | — |
| windy | `com.windyty.android` | `universal` | — |
| xingseus | `cn.danatech.xingseus` | `universal` | — |

</details>

<details>
<summary><code>docbt</code> — 2 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`docbt/patched-up`](https://github.com/docbt/patched-up) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| google-news | `com.google.android.apps.magazines` | `universal` | — |
| kleinanzeigen | `com.ebay.kleinanzeigen` | `universal` | — |

</details>

<details>
<summary><code>dropped</code> — 2 apps</summary>

**Bundle source(s):** [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) @v5.0.1 (GitHub), [`indrastorms/Dropped-Patches`](https://github.com/indrastorms/Dropped-Patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| fxfile | `nextapp.fx` | `universal` | — |
| tasker | `net.dinglisch.android.taskerm` | `universal` | — |

</details>

<details>
<summary><code>dudeks</code> — 7 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`dawidd612/dudeks-morphe-patches`](https://github.com/dawidd612/dudeks-morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| andropods | `pro.vitalii.andropods` | `universal` | — |
| calendar | `com.google.android.calendar` | `universal` | — |
| coffeebusiness | `com.tapblaze.coffeebusiness` | `universal` | — |
| gardenscapes | `com.playrix.gardenscapes` | `universal` | — |
| instagram | `com.instagram.android` | `universal` | — |
| pizzabusiness | `com.tapblaze.pizzabusiness` | `universal` | — |
| tiktok | `com.zhiliaoapp.musically` | `universal` | — |

</details>

<details>
<summary><code>epxec</code> — 14 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`epxec/android-patches`](https://github.com/epxec/android-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| dailyreminder | `dmytro.palamarchuk.dailyreminder` | `universal` | — |
| daylio | `net.daylio` | `universal` | — |
| decompile | `com.apktools.app.decompile` | `universal` | — |
| dictionary | `com.mazii.dictionary` | `universal` | — |
| fast | `com.halo.reels.movie.fast.pro` | `universal` | — |
| freereels | `com.freereels.app` | `universal` | — |
| jpnews | `mobi.eup.jpnews` | `universal` | — |
| textbasedrpg | `com.techyonic.textbasedrpg` | `universal` | — |
| touch | `com.notch.touch` | `universal` | — |
| vaultyfree | `com.theronrogers.vaultyfree` | `universal` | — |
| vtubestudio | `com.denchi.vtubestudio` | `universal` | — |
| wallet | `com.droid4you.application.wallet` | `universal` | — |
| wavelet | `com.pittvandewitt.wavelet` | `universal` | — |
| xeq | `com.frack.xeq` | `universal` | — |

</details>

<details>
<summary><code>fripe070</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`Fripe070/PixivPatches`](https://github.com/Fripe070/PixivPatches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| pixiv | `jp.pxv.android` | `universal` | — |

</details>

<details>
<summary><code>ftl</code> — 13 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`BlazeFTL/FTL-Patches`](https://github.com/BlazeFTL/FTL-Patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| bangla-dictionary | `com.hdictionary.bn` | `universal` | — |
| downloader | `videoplayer.videodownloader.downloader` | `universal` | — |
| es-file-explorer | `com.estrongs.android.pop` | `universal` | — |
| filemanager | `files.fileexplorer.filemanager` | `universal` | — |
| firefox-fenix | `org.mozilla.fenix` | `universal` | — |
| mixplorer | `com.mixplorer` | `universal` | — |
| mx-player | `com.mxtech.videoplayer.ad` | `universal` | — |
| planner | `calendar.agenda.schedule.event.advance.calendar.planner` | `universal` | — |
| printflow | `com.bytedz.printflow` | `universal` | — |
| videodownloader | `video.downloader.videodownloader` | `universal` | — |
| wifianalyzerpro | `abdelrahman.wifianalyzerpro` | `universal` | — |
| wpsapppro | `com.themausoft.wpsapppro` | `universal` | — |
| wpswpatester | `com.tester.wpswpatester` | `universal` | — |

</details>

<details>
<summary><code>hakim</code> — 2 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`kim20598/hakim-morphe-patches`](https://github.com/kim20598/hakim-morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| busuu | `com.busuu.android.enc` | `universal` | — |
| letterboxd | `com.letterboxd.letterboxd` | `universal` | — |

</details>

<details>
<summary><code>heinrich26</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`uzamapg/morphe-patches`](https://github.com/uzamapg/morphe-patches) @latest (GitHub), [`kmru/nai64patches`](https://gitlab.com/kmru/nai64patches) @latest (GitLab), [`kmru/nai64extrapatches`](https://gitlab.com/kmru/nai64extrapatches) @latest (GitLab), [`MorpheApp/morphe-patches`](https://github.com/MorpheApp/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| material-capsule | `com.pryshedko.mtisland` | `universal` | [`material-capsule-heinrich26.txt`](patches/material-capsule-heinrich26.txt) |

</details>

<details>
<summary><code>heval</code> — 27 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`heval99/Heval-Morphe-Patches`](https://github.com/heval99/Heval-Morphe-Patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| anydesk | `com.anydesk.anydeskandroid` | `universal` | — |
| aquamail | `org.kman.AquaMail` | `universal` | — |
| bluecoins | `com.rammigsoftware.bluecoins` | `universal` | — |
| boxbox | `club.boxbox.android` | `universal` | — |
| brave | `com.brave.browser` | `universal` | — |
| email | `eu.faircode.email` | `universal` | — |
| fishbuddyplayground | `no.fishbuddy_playground.app` | `universal` | — |
| flashscore | `eu.livesport.FlashScore_com` | `universal` | — |
| fotmob | `com.mobilefootie.wc2010` | `universal` | — |
| futbin | `com.futbin` | `universal` | — |
| iliga | `de.motain.iliga` | `universal` | — |
| iptv | `ru.iptvremote.android.iptv` | `universal` | — |
| jetaudio | `com.jetappfactory.jetaudio` | `universal` | — |
| librepods | `me.kavishdevar.librepods` | `universal` | — |
| livescore | `com.livescore` | `universal` | — |
| monefy | `com.monefy.app.lite` | `universal` | — |
| myfitnesspal | `com.myfitnesspal.android` | `universal` | — |
| note | `easynotes.notes.notepad.notebook.privatenotes.note` | `universal` | — |
| osmand | `net.osmand` | `universal` | — |
| p-c-w | `com.pocketcolorwheel.PCW` | `universal` | — |
| remote | `com.Relmtech.Remote` | `universal` | — |
| saphelink | `my.saphelink` | `universal` | — |
| scores365 | `com.scores365` | `universal` | — |
| sofascore | `com.sofascore.results` | `universal` | — |
| tasker | `net.dinglisch.android.taskerm` | `universal` | — |
| textra | `com.textra` | `universal` | — |
| weather24 | `com.wunderground.android.weather` | `universal` | — |

</details>

<details>
<summary><code>hooman</code> — 31 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`arandomhooman/hoomans-morphe-patches`](https://github.com/arandomhooman/hoomans-morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| at4k | `com.overdevs.at4k` | `universal` | — |
| audiobookplayer | `ak.alizandro.smartaudiobookplayer` | `universal` | — |
| bandlab | `com.bandlab.bandlab` | `universal` | — |
| batteryguru | `com.paget96.batteryguru` | `universal` | — |
| chatboost | `studio.muggle.chatboost` | `universal` | — |
| collectr | `com.collectrinc.collectr` | `universal` | — |
| cronometer | `com.cronometer.android.gold` | `universal` | — |
| dialer | `com.google.android.dialer` | `universal` | — |
| finch | `com.finch.finch` | `universal` | — |
| flightradar24 | `com.flightradar24free` | `universal` | [`flightradar24-hooman.txt`](patches/flightradar24-hooman.txt) |
| foldersync | `dk.tacit.android.foldersync.lite` | `universal` | — |
| hevy | `com.hevy` | `universal` | — |
| iamsober | `com.thehungrywasp.iamsober` | `universal` | — |
| instashot | `com.camerasideas.instashot` | `universal` | — |
| linewebtoon | `com.naver.linewebtoon` | `universal` | — |
| moneta | `currency.converter.moneta` | `universal` | — |
| photogallery | `com.soepic.photogallery.release` | `universal` | — |
| powerplayer | `com.maxmpz.audioplayer` | `universal` | — |
| quizlet | `com.quizlet.quizletandroid` | `universal` | — |
| remux | `app.remux.video.converter` | `universal` | — |
| retro-music | `app.symfonik.music.player` | `universal` | — |
| rumble-battles | `com.rumble.battles` | `universal` | — |
| sofascore | `com.sofascore.results` | `universal` | — |
| stash | `io.stashteam.games.tracker.stashapp` | `universal` | — |
| swiftkey | `com.touchtype.swiftkey` | `universal` | — |
| teachmeanatomy | `com.atomengineapps.teachmeanatomy` | `universal` | — |
| todoist | `com.todoist` | `universal` | — |
| tranzmate | `com.tranzmate` | `universal` | — |
| tumblr | `com.tumblr` | `universal` | — |
| twitch | `tv.twitch.android.app` | `universal` | — |
| videostudio | `com.dv.adm` | `universal` | — |

</details>

<details>
<summary><code>hoomans</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`arandomhooman/hoomans-morphe-patches`](https://github.com/arandomhooman/hoomans-morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| tumblr | `com.tumblr` | `universal` | — |

</details>

<details>
<summary><code>hush-facebook</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`SysAdminDoc/HushFacebook`](https://github.com/SysAdminDoc/HushFacebook) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| facebook | `com.facebook.katana` | `arm64-v8a` | — |

</details>

<details>
<summary><code>hush-feed</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`SysAdminDoc/HushFeed`](https://github.com/SysAdminDoc/HushFeed) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| tiktok | `com.zhiliaoapp.musically` | `arm64-v8a` | — |

</details>

<details>
<summary><code>hush-gram</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`SysAdminDoc/HushGram`](https://github.com/SysAdminDoc/HushGram) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| instagram | `com.instagram.android` | `arm64-v8a` | — |

</details>

<details>
<summary><code>hush-messenger</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`SysAdminDoc/HushMessenger`](https://github.com/SysAdminDoc/HushMessenger) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| messenger | `com.facebook.orca` | `arm64-v8a` | — |

</details>

<details>
<summary><code>hush-threads</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`SysAdminDoc/HushThreads`](https://github.com/SysAdminDoc/HushThreads) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| threads | `com.instagram.barcelona` | `arm64-v8a` | — |

</details>

<details>
<summary><code>hushmessenger</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`SysAdminDoc/HushMessenger`](https://github.com/SysAdminDoc/HushMessenger) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| messenger | `com.facebook.orca` | `universal` | [`messenger-hushmessenger.txt`](patches/messenger-hushmessenger.txt) |

</details>

<details>
<summary><code>hxreborn</code> — 37 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`hxreborn/morphe-patches`](https://github.com/hxreborn/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| aiocal | `all.in.one.calculator` | `universal` | — |
| alpinequest | `psyberia.alpinequest.free` | `universal` | — |
| atlas-maps | `com.atlogis.atlomaps` | `universal` | — |
| atvtools | `dev.vodik7.atvtools` | `universal` | — |
| audible | `com.audible.application` | `universal` | — |
| blurwallpaper | `apps.automan.blurwallpaper` | `universal` | — |
| cxxdroid | `ru.iiec.cxxdroid` | `universal` | — |
| dubox | `com.dubox.drive` | `universal` | — |
| etsy | `com.etsy.android` | `universal` | — |
| expressweather | `com.handmark.expressweather` | `universal` | — |
| file-explorer | `com.cxinventor.file.explorer` | `universal` | — |
| forus | `com.myvitale.forus` | `universal` | — |
| gamma | `com.gamma.scan` | `universal` | — |
| gymtracker | `app.rubberbands.fit` | `universal` | — |
| hinducalendar | `com.alokmandavgane.hinducalendar` | `universal` | — |
| imo | `com.imo.android.imoim` | `universal` | — |
| jvdroid | `ru.iiec.jvdroid` | `universal` | — |
| kick | `com.kick.mobile` | `universal` | — |
| klassikradio | `de.klassikradio.app` | `universal` | — |
| musixmatch | `com.musixmatch.android.lyrify` | `universal` | — |
| notesnook | `com.streetwriters.notesnook` | `universal` | — |
| perplexity | `ai.perplexity.app.android` | `universal` | — |
| photoeditor | `photo.editor.photoeditor.photoeditorpro` | `universal` | — |
| proton-mail | `ch.protonmail.android` | `universal` | [`proton-mail-hxreborn.txt`](patches/proton-mail-hxreborn.txt) |
| proton-pass | `proton.android.pass` | `universal` | — |
| proton-vpn | `ch.protonvpn.android` | `universal` | — |
| psiphon | `com.psiphon3.subscription` | `universal` | — |
| quranify | `com.mchutov.Quranify` | `universal` | — |
| readera | `org.readera` | `universal` | — |
| realme-link | `com.realme.link` | `universal` | — |
| retro-music | `app.symfonik.music.player` | `universal` | — |
| seven-tv | `de.prosiebensat1digital.seventv` | `universal` | — |
| showly2 | `com.michaldrabik.showly2` | `universal` | — |
| smartcamera | `com.yunyi.smartcamera` | `universal` | — |
| trainline | `com.thetrainline` | `universal` | — |
| vimo | `com.darinsoft.vimo` | `universal` | — |
| vpnify | `com.vpn.free.hotspot.secure.vpnify` | `universal` | — |

</details>

<details>
<summary><code>icysymmetra</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`icysymmetra/tiktok-patches-for-morphe`](https://github.com/icysymmetra/tiktok-patches-for-morphe) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| tiktok | `com.zhiliaoapp.musically` | `universal` | — |

</details>

<details>
<summary><code>jasonwu1994</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`jasonwu1994/Gboard-patches`](https://github.com/jasonwu1994/Gboard-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| gboard | `com.google.android.inputmethod.latin` | `universal` | — |

</details>

<details>
<summary><code>jouss</code> — 22 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`Joussflls10/Jouss-Patches`](https://github.com/Joussflls10/Jouss-Patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| alarmo | `com.bytesong.missionalarm` | `universal` | — |
| camscanner-fast | `com.cv.docscanner` | `universal` | — |
| crex | `in.cricketexchange.app.cricketexchange` | `universal` | — |
| cricbuzz | `com.cricbuzz.android` | `universal` | — |
| eyecon | `com.eyecon.global` | `universal` | — |
| fing | `com.overlook.android.fing` | `universal` | — |
| hotstar | `in.startv.hotstar` | `universal` | — |
| lumina | `com.lumina.wallpapers` | `universal` | — |
| macrodroid | `com.arlosoft.macrodroid` | `universal` | — |
| mark | `com.markOne.ss_app` | `universal` | — |
| plus | `org.telegram.plus` | `universal` | — |
| prompter | `com.solid.teleprompter` | `universal` | — |
| proton-vpn | `ch.protonvpn.android` | `universal` | — |
| sdmse | `eu.darken.sdmse` | `universal` | — |
| starsense | `com.celestron.skybox` | `universal` | — |
| taskmanager | `com.rk.taskmanager` | `universal` | — |
| ticktick | `com.ticktick.task` | `universal` | — |
| trackit | `app.vinztech.trackit` | `universal` | — |
| truecaller | `com.truecaller` | `universal` | — |
| videoplayer | `com.mxtech.videoplayer.pro` | `universal` | — |
| vivredarija | `com.vivredarija` | `universal` | — |
| vlog | `com.frontrow.vlog` | `universal` | — |

</details>

<details>
<summary><code>kim20598</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`kim20598/hakim-morphe-patches`](https://github.com/kim20598/hakim-morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| letterboxd | `com.letterboxd.letterboxd` | `universal` | — |

</details>

<details>
<summary><code>kondratjev</code> — 10 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`kondratjev/morphe-patches`](https://github.com/kondratjev/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| fatsecret | `com.fatsecret.android` | `universal` | — |
| lyfta | `com.lyfta` | `universal` | — |
| medsafe | `com.medisafe.android.client` | `universal` | — |
| ornament | `com.ornament.monitor` | `universal` | — |
| parcels | `com.brightstripe.parcels` | `universal` | — |
| pillo | `xyz.rtrvr.pillo` | `universal` | — |
| shapeupclub | `com.sillens.shapeupclub` | `universal` | — |
| soundcloud | `com.soundcloud.android` | `universal` | — |
| strength | `air.com.musclemotion.strength.mobile` | `universal` | — |
| yazio | `com.yazio.android` | `universal` | — |

</details>

<details>
<summary><code>kveld</code> — 5 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`kveld9/kveld-morphe-patches`](https://github.com/kveld9/kveld-morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| brave | `com.brave.browser` | `universal` | — |
| hevy | `com.hevy` | `universal` | — |
| mi-earphone | `com.mi.earphone` | `universal` | — |
| nokoprint | `com.nokoprint` | `universal` | — |
| tiktok | `com.zhiliaoapp.musically` | `universal` | — |

</details>

<details>
<summary><code>lain</code> — 24 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`kiraio-moe/Lain-Patches`](https://github.com/kiraio-moe/Lain-Patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| audioconnect | `com.azefsw.audioconnect` | `universal` | — |
| boorusama | `com.degenk.boorusama` | `universal` | — |
| camera | `com.flavionet.android.camera.lite` | `universal` | — |
| chatboost | `studio.muggle.chatboost` | `universal` | — |
| cinema | `com.flavionet.android.cinema.lite` | `universal` | — |
| cing | `com.kcstream.cing` | `universal` | — |
| epic | `com.getepic.Epic` | `universal` | — |
| fakegpslocation | `com.hopefactory2021.fakegpslocation` | `universal` | — |
| hermitcrab | `com.chimbori.hermitcrab` | `universal` | — |
| ilovepdf | `com.ilovepdf.www` | `arm64-v8a` | — |
| keymate | `net.nemostudio.keymate` | `universal` | — |
| mangaplus | `jp.co.shueisha.mangaplus` | `universal` | — |
| medibangpro | `com.medibang.android.medibangpro` | `universal` | — |
| photofancie | `com.surmin.photofancie.lite` | `universal` | — |
| pixel-studio | `com.PixelStudio` | `universal` | — |
| pixellab | `com.imaginstudio.imagetools.pixellab` | `universal` | — |
| proxyevery | `cn.adonet.proxyevery` | `universal` | — |
| science | `com.jlindemann.science` | `universal` | — |
| sets | `com.ceyhan.sets` | `universal` | — |
| sketchbook | `com.adsk.sketchbook` | `universal` | — |
| superproxy | `com.scheler.superproxy` | `universal` | — |
| tablet | `com.medibang.android.paint.tablet` | `universal` | — |
| timestampcamerafree | `com.jeyluta.timestampcamerafree` | `universal` | — |
| timestampcamerafreeent | `com.jeyluta.timestampcamerafreeent` | `universal` | — |

</details>

<details>
<summary><code>liaralabs</code> — 1 app</summary>

**Bundle source(s):** [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) @latest (GitHub), [`liaralabs/revanced-patches`](https://github.com/liaralabs/revanced-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| gamehub | `com.xiaoji.egggame` | `universal` | — |

</details>

<details>
<summary><code>media</code> — 11 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`HellLord77/media-patches`](https://github.com/HellLord77/media-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| bongobd | `com.bongo.bongobd` | `universal` | — |
| bongobdandroidtv | `com.bongo.bongobdandroidtv` | `universal` | — |
| chorki | `com.prothomalo.chorki` | `universal` | — |
| deeptotv | `com.gotipath.deeptotv` | `universal` | — |
| deeptotvapp | `com.gotipath.deeptotvapp` | `universal` | — |
| kabbik | `com.kabbik.app` | `universal` | — |
| klikk | `com.angel.klikk` | `universal` | — |
| klikk-tv | `com.angel.klikk.tv` | `universal` | — |
| prothomalo | `com.prothomalo` | `universal` | — |
| shadhin | `com.gm.shadhin` | `universal` | — |
| toffee | `com.banglalink.toffee` | `universal` | — |

</details>

<details>
<summary><code>morphe</code> — 3 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`MorpheApp/morphe-patches`](https://github.com/MorpheApp/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| reddit | `com.reddit.frontpage` | `universal` | — |
| youtube | `com.google.android.youtube` | `universal` | [`youtube-morphe.txt`](patches/youtube-morphe.txt) |
| youtube-music | `com.google.android.apps.youtube.music` | `arm64-v8a`, `armeabi-v7a` | [`youtube-music-morphe.txt`](patches/youtube-music-morphe.txt) |

</details>

<details>
<summary><code>mvaishak</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`mvaishak/letterboxd-morphe-patches`](https://github.com/mvaishak/letterboxd-morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| letterboxd | `com.letterboxd.letterboxd` | `universal` | — |

</details>

<details>
<summary><code>okish</code> — 33 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`byehi98/okish-morphe-patches`](https://github.com/byehi98/okish-morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| adda247 | `com.adda247.app` | `universal` | — |
| aliensdrivemecrazy | `com.rebeltwins.aliensdrivemecrazy` | `universal` | — |
| altosadventure | `com.noodlecake.altosadventure` | `universal` | — |
| altosodyssey | `com.noodlecake.altosodyssey` | `universal` | — |
| bighunter | `com.kakarod.bighunter` | `universal` | — |
| burrito-bison-3 | `com.kongregate.mobile.burritobison3.google` | `universal` | — |
| camscanner-fast | `com.cv.docscanner` | `universal` | — |
| crossyroad | `com.yodo1.crossyroad` | `universal` | — |
| dantheman | `com.halfbrick.dantheman` | `universal` | — |
| deadtrigger | `com.madfingergames.deadtrigger` | `arm64-v8a` | — |
| doodle-jump | `com.lima.doodlejump` | `universal` | — |
| drdriving | `com.ansangha.drdriving` | `universal` | — |
| earntodie2 | `com.notdoppler.earntodie2` | `universal` | — |
| fancypants | `com.overthetopgames.fancypants` | `universal` | — |
| freejobalert | `com.freejobalert` | `universal` | — |
| haaktestb | `com.blingame.haaktestb` | `arm64-v8a` | — |
| hill-climb | `com.fingersoft.hillclimb` | `universal` | — |
| injustice | `com.wb.goog.injustice` | `universal` | — |
| into-the-dead | `com.sidheinteractive.sif.DR` | `universal` | — |
| jetpackjoyride | `com.halfbrick.jetpackjoyride` | `universal` | — |
| lumina | `com.lumina.wallpapers` | `universal` | — |
| missiles | `pl.macaque.Missiles` | `universal` | — |
| onlyone | `com.rebelbinary.onlyone` | `universal` | — |
| plagueinc | `com.miniclip.plagueinc` | `universal` | — |
| rodeo-safari | `com.yodo1.rodeo.safari` | `arm64-v8a` | — |
| smashhit | `com.mediocre.smashhit` | `universal` | — |
| swiftbackup | `org.swiftapps.swiftbackup` | `universal` | — |
| swordigo | `com.touchfoo.swordigo` | `universal` | — |
| tentacle-wars | `com.fdgentertainment.tentaclewars.gp.free` | `universal` | — |
| trafficracer | `com.skgames.trafficracer` | `universal` | — |
| trafficrider | `com.skgames.trafficrider` | `universal` | — |
| truecloud | `com.generalcomp.truecloud` | `universal` | — |
| vector | `com.nekki.vector` | `universal` | — |

</details>

<details>
<summary><code>paresh</code> — 15 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`Paresh-Maheshwari/paresh-patches`](https://gitlab.com/Paresh-Maheshwari/paresh-patches) @latest (GitLab)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| alarmo | `com.bytesong.missionalarm` | `universal` | — |
| camscanner-fast | `com.cv.docscanner` | `universal` | — |
| crex | `in.cricketexchange.app.cricketexchange` | `universal` | — |
| documentscanner | — | `universal` | — |
| eyecon | `com.eyecon.global` | `universal` | — |
| fing | `com.overlook.android.fing` | `universal` | — |
| lumina | `com.lumina.wallpapers` | `universal` | — |
| macrodroid | `com.arlosoft.macrodroid` | `universal` | — |
| mark | `com.markOne.ss_app` | `universal` | — |
| prompter | `com.solid.teleprompter` | `universal` | — |
| starsense | `com.celestron.skybox` | `universal` | — |
| telegram | `org.telegram.messenger` | `universal` | — |
| ticktick | `com.ticktick.task` | `universal` | — |
| vlog | `com.frontrow.vlog` | `universal` | — |
| vn | — | `universal` | — |

</details>

<details>
<summary><code>piko</code> — 2 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`crimera/piko`](https://github.com/crimera/piko) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| instagram | `com.instagram.android` | `arm64-v8a` | — |
| x | `com.twitter.android` | `universal` | — |

</details>

<details>
<summary><code>piko-newx</code> — 2 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`crimera/piko-newx`](https://github.com/crimera/piko-newx) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| x | `com.twitter.android` | `universal` | — |
| x-new | — | `universal` | — |

</details>

<details>
<summary><code>pixelpusher</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`PixelPusher247/morphe-patches`](https://github.com/PixelPusher247/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| trakt | — | `universal` | — |

</details>

<details>
<summary><code>pyflat</code> — 3 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`PyFlat-JR/Morphe-Patches`](https://github.com/PyFlat-JR/Morphe-Patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| disney-plus | `com.disney.disneyplus` | `universal` | — |
| kicker | `com.netbiscuits.kicker` | `universal` | — |
| swr3 | `de.swr.avp.ard` | `universal` | — |

</details>

<details>
<summary><code>revanced-kitadai31</code> — 4 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`Peanut-Butter-bread/idk`](https://github.com/Peanut-Butter-bread/idk) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| crunchyroll | `com.crunchyroll.crunchyroid` | `universal` | — |
| material-capsule | `com.pryshedko.mtisland` | `universal` | [`material-capsule-revanced-kitadai31.txt`](patches/material-capsule-revanced-kitadai31.txt) |
| teuida | `net.teuida.teuida` | `universal` | [`teuida-revanced-kitadai31.txt`](patches/teuida-revanced-kitadai31.txt) |
| wps-office | `cn.wps.moffice_eng` | `universal` | — |

</details>

<details>
<summary><code>rookie</code> — 6 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`RookieEnough/De-ReVanced`](https://github.com/RookieEnough/De-ReVanced) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| google-photos | `com.google.android.apps.photos` | `arm64-v8a`, `armeabi-v7a` | [`google-photos-rookie.txt`](patches/google-photos-rookie.txt) |
| letterboxd | `com.letterboxd.letterboxd` | `universal` | — |
| messenger | `com.facebook.orca` | `universal` | — |
| photomath | `com.microblink.photomath` | `universal` | — |
| pixiv | `jp.pxv.android` | `universal` | — |
| strava | `com.strava` | `universal` | — |

</details>

<details>
<summary><code>rushiranpise</code> — 17 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`rushiranpise/morphe-patches`](https://github.com/rushiranpise/morphe-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| accubattery | `com.digibites.accubattery` | `universal` | — |
| accuweather | `com.accuweather.android` | `universal` | — |
| acrobat | `com.adobe.reader` | `universal` | — |
| calm | `com.calm.android` | `universal` | — |
| cloudflare-one | `com.cloudflare.onedotonedotonedotone` | `universal` | — |
| cpu-z | `com.cpuid.cpu_z` | `universal` | — |
| ms-excel | `com.microsoft.office.excel` | `universal` | — |
| ms-teams | `com.microsoft.teams` | `universal` | — |
| ms-word | `com.microsoft.office.word` | `universal` | — |
| nova | `com.teslacoilsw.launcher` | `universal` | — |
| picsart | `com.picsart.studio` | `universal` | — |
| rar | `com.rarlab.rar` | `universal` | — |
| strava | `com.strava` | `universal` | — |
| telegram-web | `org.telegram.messenger.web` | `universal` | — |
| tomtom | `com.tomtom.gplay.navapp` | `universal` | — |
| transit | `com.thetransitapp.droid` | `universal` | — |
| udisc | `com.regasoftware.udisc` | `universal` | — |

</details>

<details>
<summary><code>ryykitty-twitch</code> — 1 app</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`ryykitty/twitch-patched`](https://github.com/ryykitty/twitch-patched) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| twitch | `tv.twitch.android.app` | `universal` | [`twitch-ryykitty-twitch.txt`](patches/twitch-ryykitty-twitch.txt) |

</details>

<details>
<summary><code>taknok</code> — 1 app</summary>

**Bundle source(s):** [`revanced/revanced-cli`](https://github.com/revanced/revanced-cli) @latest (GitHub), [`Taknok/revanced-patches`](https://github.com/Taknok/revanced-patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| dialer | `com.google.android.dialer` | `universal` | — |

</details>

<details>
<summary><code>xhehab</code> — 13 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`Xhehab/Xhehab-Patches`](https://github.com/Xhehab/Xhehab-Patches) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| appv2 | `com.bws.appv2` | `universal` | — |
| boostcamp | `com.bpmhealth.boostcamp` | `universal` | — |
| bromleyapp | `com.skynetcoaching.bromleyapp` | `universal` | — |
| cbum | `uni.cbum` | `universal` | — |
| fitness | `app.mhphysique.fitness` | `universal` | — |
| fst7 | `com.influencers.fst7` | `universal` | — |
| hypertrophy | `com.rp.hypertrophy` | `universal` | — |
| juggernautai | `com.jtsstrength.juggernautai` | `universal` | — |
| method | `com.ganbaru.method` | `universal` | — |
| myoadapt | `com.myoadapt.app.android` | `universal` | — |
| thenx | `com.sysops.thenx` | `universal` | — |
| trainwiseapp | `com.trainwiseapp.app` | `universal` | — |
| video-player | `video.player.videoplayer` | `universal` | — |

</details>

<details>
<summary><code>xtra</code> — 13 apps</summary>

**Bundle source(s):** [`MorpheApp/morphe-cli`](https://github.com/MorpheApp/morphe-cli) @latest (GitHub), [`BholeyKaBhakt/android-patches-xtra`](https://github.com/BholeyKaBhakt/android-patches-xtra) @latest (GitHub)

| App | Package | Builds | Patch file |
|:----|:--------|:-------|:-----------|
| atmfee | `com.atmfee` | `universal` | — |
| automate | `com.llamalab.automate` | `universal` | — |
| autosync | `com.ttxapps.autosync` | `universal` | — |
| backdrop | `com.backdrops.wallpapers` | `universal` | — |
| blocker | `io.funswitch.blocker` | `universal` | — |
| circuit | `com.proto.circuitsimulator` | `universal` | — |
| inshorts | `com.nis.app` | `universal` | — |
| sky-tonight | `com.vitotechnology.sky.tonight.map.star.walk` | `universal` | — |
| solid | `pl.solidexplorer2` | `universal` | — |
| speedtest | `org.zwanoo.android.speedtest` | `universal` | — |
| starwalk2 | `com.vitotechnology.StarWalk2Free` | `universal` | — |
| velnet | `com.ufovpn.connect.velnet` | `universal` | — |
| vpnify | `com.vpn.free.hotspot.secure.vpnify` | `universal` | — |

</details>

</details>

---

## 🛠️ Development

<details>
<summary><b>Development &amp; maintainer documentation</b> — pipeline design, configuration, local builds, workflows, patch-name auditing</summary>

<br>

### ✨ Key Features

This repository utilizes a robust Python-based pipeline to ensure high reliability and optimization.

* **Fully Automated:** the GitHub Actions workflow executes daily at 06:00 UTC, requiring zero manual intervention.
* **Architecture Optimization:** builds specific `arm64-v8a`, `armeabi-v7a`, and `universal` APKs to reduce file size and improve performance on target devices.
* **Multi-Source Downloads:** intelligent fetching from APKMirror, APKPure, Uptodown, APKCombo, APKFab, Aptoide, Codeberg and GitHub keeps success rates high even when one source is down.
* **Multi-Source Patching:** 63 community patch bundles are supported; each app is rebuilt once per source that patches it.
* **Granular Build Control:** simple text-based configuration allows for precise inclusion or exclusion of individual patches.
* **Smart Failover:** the system automatically switches download sources if a fetch attempt fails.
* **Auto-Signing:** all APKs are signed with a consistent public keystore, making them ready to install immediately.
* **Patch-Name Auditing:** every requested patch name is checked against the bundle that should define it — at build time and in a daily CI job — so a stale name can no longer ship an APK that differs from what its patch file claims.
* **Clean Release Cycle:** previous releases are replaced rather than archived, preventing clutter and making it easy for external managers (like Orion) to track updates.

### 📁 Repository Structure

```text
Morphe-AutoBuilds/
├── .github/workflows/             # GitHub Actions automation
│   ├── patch.yml                  # Daily builds (06:00 UTC) + manual dispatch
│   ├── manual-patch.yml           # On-demand single-app builds
│   ├── audit-patch-names.yml      # Patch-name audit (daily 07:30 UTC, and on push)
│   ├── generate-configs.yml       # Recreate a predefined batch of app definitions
│   ├── migrate-releases-to-*.yml  # One-time release mirrors (Codeberg / GitLab)
│   └── rebuild-gitlab-links.yml   # Refresh GitLab release asset links
├── apps/                          # Base-APK definitions, one folder per store
│   ├── apkcombo/  apkfab/  apkmirror/  apkpure/
│   └── aptoide/   codeberg/ github/    uptodown/
├── keystore/                      # Public keystore every build is signed with
├── patches/                       # Build option files (<app_name>-<source>.txt)
├── scripts/                       # CI helpers (manifest, audit, publishing)
├── sources/                       # Patch-bundle source definitions (+ README)
├── src/                           # Build pipeline (fetch → patch → sign)
├── arch-config.json               # Architecture matrix per app × source
├── patch-config.json              # The apps × sources to build
├── requirements.txt               # Python dependencies
└── LICENSE                        # GPL-3.0
```

### ⚙️ Configuration Guide

The builder is highly configurable. These files define the build output.

#### 1. App Selection — `patch-config.json`

Which applications the pipeline should build, as `(app_name, source)` pairs. `app_name` matches a definition
under `apps/`, `source` matches a file in `sources/`.

```json
{
  "patch_list": [
    { "app_name": "youtube", "source": "morphe" },
    { "app_name": "youtube-music", "source": "morphe" },
    { "app_name": "material-capsule", "source": "heinrich26" }
  ]
}
```

#### 2. Architecture Matrix — `arch-config.json`

Which CPU architectures to build for a given pair. Pairs that are not listed are built as `universal`.

```json
[
  {
    "app_name": "youtube-music",
    "source": "morphe",
    "arches": ["arm64-v8a", "armeabi-v7a"]
  },
  {
    "app_name": "instagram",
    "source": "piko",
    "arches": ["arm64-v8a"]
  }
]
```

#### 3. App Definitions — `apps/<store>/<app_name>.json`

Where the base APK comes from. Example for `apps/apkmirror/youtube.json`:

```json
{
  "org": "google-inc",
  "name": "youtube",
  "type": "APK",
  "arch": "universal",
  "dpi": "nodpi",
  "package": "com.google.android.youtube",
  "version": ""
}
```

An empty `version` means "newest available". The folder (`apkmirror`, `apkpure`, `uptodown`, `apkcombo`,
`apkfab`, `aptoide`, `codeberg`, `github`) selects the downloader used to fetch the APK.

#### 4. Build Options — `patches/<app_name>-<source>.txt`

Optional per-pair patch instructions. `+` forces a patch on, `-` keeps one off. Only a file named exactly
`<app_name>-<source>.txt` is ever read — other names in `patches/` are ignored.

```text
# patches/material-capsule-heinrich26.txt
+ Pairip Bypass
+ Disable Play Store updates
```

```text
# patches/youtube-morphe.txt
- Custom branding
```

Names are resolved against the bundle's own list for that app, and the CLI **silently ignores** an unknown
name, so a name that drifts with an upstream rename would otherwise ship an APK that differs from what the
file claims. See *Patch-Name Auditing & Build Freezing* below.

#### 5. Patch Sources — `sources/<source>.json`

What each source consumes. The first entry names the source; the rest point at the CLI and the patch bundles
it should load (GitHub or GitLab, pinned to a tag or `latest`).

```json
[
  { "name": "heinrich26" },
  { "provider": "github", "user": "MorpheApp", "repo": "morphe-cli", "tag": "latest" },
  { "provider": "github", "user": "uzamapg", "repo": "morphe-patches", "tag": "latest" },
  { "provider": "gitlab", "project": "kmru/nai64patches", "tag": "latest" },
  { "provider": "github", "user": "MorpheApp", "repo": "morphe-patches", "tag": "latest" }
]
```

A source declares every bundle it wants to combine, and the CLI is invoked once per bundle — with the
`+`/`-` flags repeated for each one. See [`sources/README.md`](sources/README.md) for how a source gets its
own fork or mirror, and how the guards behave.

### 🚀 Local Build Instructions

If you prefer to build the APKs on your own machine, follow these steps.

#### Prerequisites

* Python 3.11 or higher (CI uses 3.11)
* Java 21 (CI uses Temurin 21), required by the CLI
* `zip` utility
* `apksigner` (part of Android SDK Build-Tools)

#### Installation & Execution

1. **Clone the repository:**

```bash
git clone https://github.com/uzamapg/Morphe-AutoBuilds.git
cd Morphe-AutoBuilds
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the build** for a specific app and source:

```bash
export GITHUB_TOKEN="$(gh auth token)"                # bundle and release lookups
export APP_NAME="youtube"
export SOURCE="morphe"
python -m src
```

4. **Target a specific architecture (optional):**

```bash
export APP_NAME="youtube"
export SOURCE="morphe"
export ARCH="arm64-v8a"    # arm64-v8a, armeabi-v7a, universal
python -m src
```

Add `export GITHUB_REPOSITORY="uzamapg/Morphe-AutoBuilds"` only when the run should publish a release.

### 🔄 GitHub Actions Workflows

* **`patch.yml`** — *daily at 06:00 UTC, plus manual dispatch.* The main pipeline: fetch the tooling, work out
  which pairs actually changed, patch and sign them in a sharded job matrix, then replace the `latest`
  release. Manual runs accept `force_full_rebuild` to ignore the incremental check.
* **`manual-patch.yml`** — *manual only.* Build a single app/source on demand: choose the architectures, pin
  an APK version, and either update the public release or keep artifacts only. It can also publish to the
  GitLab mirror project.
* **`audit-patch-names.yml`** — *daily at 07:30 UTC, plus on any push touching `patches/**`, `sources/**`,
  `apps/**`, `patch-config.json`, the audit script or the workflow.* Verifies every patch name against the
  bundles its source ships, without building anything. The run fails on findings, and also on `CHECK-FAIL`
  ("nothing could be verified").
* **`generate-configs.yml`** — *manual only.* Recreates a fixed, hardcoded batch of app definition files under
  `apps/` and commits them. It does **not** discover new apps, and running it overwrites those files.
* **`migrate-releases-to-codeberg.yml`** / **`migrate-releases-to-gitlab.yml`** — *manual only.* One-time
  mirrors that copy every `latest` asset to Codeberg or GitLab and verify each file by name and size. Run
  with `dry_run` first.
* **`rebuild-gitlab-links.yml`** — *manual only.* Rebuilds the GitLab release asset links after a mirror
  refresh.

### 🩹 Patch-Name Auditing & Build Freezing

The CLI drops an `-e`/`-d` name it does not define for the app's package, without failing the build. A patch
file can therefore drift past an upstream rename and still produce a green run that ignores it. Two guards
cover that gap:

* **Build-time guard** (`src/__main__.py`): after patching, any requested name that never reported
  `Applied:` raises `FreezeBuild`. The pair keeps its last good APK instead of publishing a mismatched one,
  the run stays green, and `manifest.json` records `frozen: true` together with a `freeze_reason`. A frozen
  pair is skipped by later runs until it is force-rebuilt.
* **CI audit** (`scripts/audit_patch_names.py`, run by `audit-patch-names.yml`): compares every `+`/`-` line
  with the bundles' own patch lists, without building. Findings are `DEAD-FILE` (the filename matches no
  pair), `EMPTY-FILE`, `MISSING` (no bundle defines the name), `INCOMPATIBLE` (defined, but not for this
  app's package), `NO-BUNDLE` and `NO-PACKAGE`.

To recover a frozen pair, correct the name in `patches/<app>-<source>.txt` and dispatch `patch.yml` with
`force_full_rebuild`. Run the audit locally after any source bump:

```bash
GITHUB_TOKEN="$(gh auth token)" GITHUB_REPOSITORY="uzamapg/Morphe-AutoBuilds" \
  python scripts/audit_patch_names.py
```

### 🤝 Contributing

Contributions to improve the toolchain or add support for new apps are welcome.

1. **Fork** the repository.
2. **Create** a feature branch (`git checkout -b feature/new-app`).
3. **Test** your changes locally using the Python scripts.
4. **Commit** your changes (`git commit -m "Add support for new-app"`).
5. **Push** to the branch (`git push origin feature/new-app`).
6. **Open** a Pull Request.

When adding a patch name, run the audit above first — a name that no bundle defines for the app is ignored at
build time.

### 📝 Operational Notes

* The original repository is tracked as the `upstream` git remote; `origin` is this fork.
* Maintenance here is AI-assisted (see the note at the top of this file). Patch sources, patch
  files, guards, tooling and documentation are AI-drafted and then checked against the live bundles
  with `scripts/audit_patch_names.py` plus a `workflow_dispatch` run of `patch.yml`.
* The pipeline was initially triggered via the push trigger on 2026-10-11 16:09.

</details>

---

## ⚠️ Disclaimer & Legal

> **Important:** This repository is a build-automation toolkit. It contains **no APK files, no binaries, and no copyrighted media** of any kind. Nothing here is a downloadable app.

* **No binaries hosted:** All build outputs are produced locally or in CI and are never committed to this repository.
* **Educational purpose:** The workflows and scripts are provided for educational and research purposes, to demonstrate automated Android build pipelines.
* **Affiliation:** This is a fork of [RookieEnough/Morphe-AutoBuilds](https://github.com/RookieEnough/Morphe-AutoBuilds), maintained independently. It is **not** affiliated with the Morphe Team or with any app publisher whose software it can process.
* **AI-assisted maintenance:** Additions and fixes made in this fork are produced with AI coding agents and reviewed by running the pipeline; nothing is merged on the strength of the draft alone.
* **Your responsibility:** You are responsible for complying with the licenses and terms of service of the apps and build sources you choose to use. Do not redistribute builds in ways that violate those terms.
* **Use at your own risk:** Builds are generated automatically from third-party sources and may contain experimental features.
* **GmsCore:** Morphe's MicroG-RE is required for these non-root apps to function correctly.

---

<div align="center">

**If you found this project helpful, please consider giving it a ⭐ Star.**  
<br>
**Made with 💜 by RookieZ**
<br>
Fork of [RookieEnough/Morphe-AutoBuilds](https://github.com/RookieEnough/Morphe-AutoBuilds), maintained with AI assistance.

</div>
