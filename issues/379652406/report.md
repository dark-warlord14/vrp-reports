# Security: Android address bar hidden after slow navigation finishes, if slow nav is initiated on page load

| Field | Value |
|-------|-------|
| **Issue ID** | [379652406](https://issues.chromium.org/issues/379652406) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | sk...@google.com |
| **Created** | 2024-11-18 |
| **Bounty** | $7,000.00 |

## Description

#### SUMMARY

The address bar can be hidden by a page with no user interaction after 3 seconds. The page can then spoof the address bar within the page.

#### VULNERABILITY DETAILS

When a page loads and immediately starts a new navigation, if the navigation takes at least 3 seconds, the browser will hide the address bar when the slow navigation is completed.

I've also verified this works for navigations that take over a minute.

Hiding the address bar does not require any user interaction. There are no apparent prerequisites to the navigation (can be directly from address bar, or from another page with/without user interaction).

Expected behavior is that the user needs to be on a page for 3 seconds and then intentionally scroll down to hide the address bar. The observed behavior bypasses the user interaction requirement.

For some reason, the initiating page must have a `<style>` element for repro (can be empty). Repro also does not work if there is any delay in initiating the navigation, e.g. with `setTimeout(..., 0)`.

Focusing on input fields forces the address bar to show, but a user is more likely to check the address bar before interacting with the page, when the URL spoof is still displayed. (There's a chance a compromised renderer could prevent input focus from showing the address bar, but I'm not certain.)

#### VERSION

Chrome Version: 133.0.6835.0 Dev, 133.0.6838.0 Canary, 133.0.6844.0 Canary

Only seems to repro on branded Chrome builds. There's no repro on the same Chromium versions above.

Operating System: Android 12

#### BISECT

I'm still working on a bisect, but this is proving to be tricky since it only seems to repro on branded Chrome builds, not Chromium builds.
Bisect so far:

- Does not repro on 132.0.6834.5 Beta, 133.0.6822.0 Dev
- Repros on 133.0.6835.0 Dev, 133.0.6838.0 Canary, 133.0.6844.0 Canary

Based on the 132.0.6834.5 Beta - 133.0.6835.0 Dev range:
<https://chromium.googlesource.com/chromium/src/+log/e96bb49e536d5d504aba1b56874d190923ba44a2..2014f0f91242702a3fb80c9baae252fb6bec583c/>

This seems like a suspect CL, but not certain: <https://chromium.googlesource.com/chromium/src/+/0351d764b858cd585f2b0dae27e08e531e091fbb>

I'll continue trying to bisect with older branded Canary versions.

I've verified repro and versions above on multiple devices, and AFAICT from chrome://version/?show-variations-cmd my Canary and Dev browsers don't have field trials enabled, so it doesn't seem due to an experiment in Canary/Dev that isn't active in Beta/Stable.

#### REPRODUCTION CASE

Some aspects of the realistic PoC can be improved, such as matching browser's light/dark mode and hiding spoof on `window` `resize` event.

The realistic PoC prevents scrolling up from re-showing the address bar using CSS. The minimal PoC does not prevent scrolling up, so the address bar is easily re-shown.

In these PoCs, the initiator is cross-site from the destination, but the PoCs also work if both the initiator and destination pages are same-origin. This doesn't seem to affect behavior.

##### Setup for self-hosting (not required for hosted PoCs below):

1. Host a slow-loading page that takes at least 3 seconds to load. See attached slow.php and slow-android-hide-address-bar.php for examples.
2. Update the initiator pages to navigate to your hosted slow-loading page (instead of the `aogarantiza.com`-hosted pages)

##### Minimal PoC

1. Navigate to <https://alesandroortiz.com/security/chromium/android-hide-address-bar-minimal.html>
2. Wait for next page to load.

##### Realistic PoC

1. Navigate to <https://alesandroortiz.com/security/chromium/android-hide-address-bar.html>
2. Wait for next page to load.

For both PoCs:

Observed: When the next page is loaded, the address bar is hidden by the browser.

Expected: The address bar is always shown unless the address bar has been visible for at least 3 seconds since the last navigation and then the user scrolls down the page.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [android-hide-address-bar-minimal.html](attachments/android-hide-address-bar-minimal.html) (text/html, 264 B)
- [android-hide-address-bar.html](attachments/android-hide-address-bar.html) (text/html, 285 B)
- [slow.php](attachments/slow.php) (application/x-httpd-php, 122 B)
- [slow-android-hide-address-bar.php](attachments/slow-android-hide-address-bar.php) (application/x-httpd-php, 1.7 KB)
- [android-hide-address-bar-minimal.mp4](attachments/android-hide-address-bar-minimal.mp4) (video/mp4, 1.1 MB)
- [android-hide-address-bar-realistic.mp4](attachments/android-hide-address-bar-realistic.mp4) (video/mp4, 1.9 MB)
- [urlbar-google.jpg](attachments/urlbar-google.jpg) (image/jpeg, 19.6 KB)
- [repro-flags.txt](attachments/repro-flags.txt) (text/plain, 25.8 KB)
- [no-repro-logs.txt](attachments/no-repro-logs.txt) (text/plain, 3.7 KB)
- [repro-logs.txt](attachments/repro-logs.txt) (text/plain, 4.8 KB)

## Timeline

### al...@alesandroortiz.com (2024-11-18)

This seems somewhat similar to [issue 40064686](https://issues.chromium.org/issues/40064686).

Forgot to mention it also does NOT repro on 131.0.6778.39 Stable.

### al...@alesandroortiz.com (2024-11-19)

Hm, not sure about the bisect range now since I can repro on 131.0.6758.0 Canary and 132.0.6832.0 Canary. Will continue bisect and hopefully have something useful by tomorrow.

### al...@alesandroortiz.com (2024-11-19)

Seeing different behavior even on same version when clearing data or reinstalling, so must be a variation or something. Still looking for lowest version where there is *some* repro, and then will try to identify the variation (although that'll probably be a pain).

e.g. Have both repro and no repro on 129.0.6614.0. Also have repro/no repro on latest Canary (133.0.6845.0, as of Nov 18th).

### al...@alesandroortiz.com (2024-11-19)

Lowest version with consistent no repro AFAICT is 128.0.6613.7. First version with repro based on variation is 129.0.6614.0. So either an experiment with partial rollout starting with M129+ or some code change between those two versions.

### al...@alesandroortiz.com (2024-11-19)

Progress: Seems this has something to do with `RetainOmniboxOnFocus<RetainOmniboxOnFocus` being enabled, possibly in combination with other things. Still bisecting variations so will have more tomorrow.

In case someone jumps on this before I'm able to continue tomorrow: Attached are current flags that result in repro. When you only remove `RetainOmniboxOnFocus<RetainOmniboxOnFocus` from `--enable-features=`, issue stops reproducing.

To use these flags on Android, these are the steps I'm following on a non-rooted physical device:

- Use Canary (I'm using 133.0.6845.0 but anything at or above 129.x should work per [#comment4](https://issues.chromium.org/issues/379652406#comment4))
- Enable "Enable command line on non-rooted devices" in `chrome://flags` per [1]
- Write the flags to `/data/local/tmp/chrome-command-line` (`adb push` works fine for this), with an underscore followed by a space (`_` ) at the beginning of the file before the actual flags. e.g. `_ --flags-here=...` (also per [1])
- Before each test run, force stop Canary, then open Canary. This ensures the flag has kicked in and the latest command line flags are read.

I'll continue variations bisect tomorrow.

[1] <https://www.chromium.org/developers/how-tos/run-chromium-with-flags/#android>

### nh...@chromium.org (2024-11-20)

skym: Since you wrote <https://chromium-review.googlesource.com/c/chromium/src/+/4757919> to fix the similar issue [crbug.com/40064686](https://crbug.com/40064686), can you look into this one? It seems like the "wait 3 seconds" in that fix might be related to this issue where the server waits 3 seconds before sending the response. I haven't yet reproduced this.

### al...@alesandroortiz.com (2024-11-20)

For context, the 3 second delay requirement comes from `MAX_FULLSCREEN_LOAD_DELAY_MS` [1]. I've previously mentioned this in an older report: <https://issues.chromium.org/issues/343938078#comment3>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java;l=36;drc=aed2f60917e3aa3cc3da98a3c443edce5933b07a>

### al...@alesandroortiz.com (2024-11-20)

I've narrowed down repro to requiring these flags on branded Canary:

`--force-fieldtrials="*RenderDocumentWithNavigationQueueing/EnabledAllFramesWithQueueing_DelayLTV_20241112/" --force-fieldtrial-params="RenderDocumentWithNavigationQueueing.EnabledAllFramesWithQueueing_DelayLTV_20241112:level/all-frames/queueing_level/full" --enable-features="RenderDocument<RenderDocumentWithNavigationQueueing,RetainOmniboxOnFocus<RetainOmniboxOnFocus"` 

The 2024-11-12 date for one of the params makes sense since I started reproducing this on Nov 14th/15th.

Will verify on latest non-branded Chromium shortly. (Update: Verified Chromium repro with these flags.)

### al...@alesandroortiz.com (2024-11-20)

Not sure why `RetainOmniboxOnFocus` affected behavior when combined with the other flags in [#comment6](https://issues.chromium.org/issues/379652406#comment6).
With this minimal set of flags, `RetainOmniboxOnFocus` doesn't have an effect on repro. This still results in repro:

`--force-fieldtrials="*RenderDocumentWithNavigationQueueing/EnabledAllFramesWithQueueing_DelayLTV_20241112/" --force-fieldtrial-params="RenderDocumentWithNavigationQueueing.EnabledAllFramesWithQueueing_DelayLTV_20241112:level/all-frames/queueing_level/full" --enable-features="RenderDocument<RenderDocumentWithNavigationQueueing"`

Update: Verified repro on Chromium. On Chromium, (sometimes?) requires the flags from [#comment9](https://issues.chromium.org/issues/379652406#comment9) (with `RetainOmniboxOnFocus` explicitly enabled).

### al...@alesandroortiz.com (2024-11-20)

And with flags from [#comment10](https://issues.chromium.org/issues/379652406#comment10), also have repro on latest Stable: 131.0.6778.39, verified on two physical devices.

### al...@alesandroortiz.com (2024-11-20)

Experiments correspond to: <https://source.chromium.org/chromium/chromium/src/+/main:testing/variations/fieldtrial_testing_config.json;l=19554;drc=19cace29ba5a2a21bffd2b85a01ff50ec8954b9c>

```
{
    "name": "EnabledAllFramesWithQueueing",
    "params": {
        "level": "all-frames",
        "queueing_level": "full"
    },
    "enable_features": [
        "DelayLayerTreeViewDeletionOnLocalSwap",
        "QueueNavigationsWhileWaitingForCommit",
        "RenderDocument"
    ],
    "disable_features": [
        "RenderDocumentCompositorReuse"
    ]
}

```

### sk...@google.com (2024-11-20)

If this is related to EnabledAllFramesWithQueueing, rakina@, can you investigate?

### al...@alesandroortiz.com (2024-11-20)

Doing bisect in Chromium with flags now. So far repros down to r1303161 (May 2024), r1281001 (April 2024), r1241007 (Dec 2023), r1120996 (March 2023) so it's probably not a recent change.

Update: Potential bisect range 1094632 (known good) - 1094694 (first known bad). Looking at changelog now: <https://chromium.googlesource.com/chromium/src/+log/2253ea0e474b099ff66b94c0ca694fc7614410c7..71892e1b45fe7b38ba967a968e82b99c078af0b6>

### al...@alesandroortiz.com (2024-11-20)

My best *guess* so far is <https://chromium.googlesource.com/chromium/src/+/7ce309e3d383b135b88660e38c578c80e2b5581d> but given the distance from omnibox code, I'm not sure *why* it affects the address bar as observed.

### al...@alesandroortiz.com (2024-11-20)

I think I'm out of things to test, so please let me know if there's any additional testing or analysis I can do.

The commit in [#comment15](https://issues.chromium.org/issues/379652406#comment15) allows feature flags to enable `RenderDocument` for all frames, so hopefully Rakina and team can determine exactly *why* enabling that results in observed behavior based on info provided so far.

### al...@alesandroortiz.com (2024-11-20)

FYI, Rakina seems OOO until Nov 25 per Gerrit. Changing the flag params [1] to some earlier value (i.e. not `level/all-frames`) should be good enough mitigation for now. In one instance of Stable with no repro, I see params from server are `RenderDocumentWithNavigationQueueing.Default:level/subframe/queueing_level/full`.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/common/content_navigation_policy.h;l=48;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34>

### al...@alesandroortiz.com (2024-11-20)

For completeness, the `RenderDocumentLevel::kAllFrames` flag level was added in <https://chromium.googlesource.com/chromium/src/+/31cdfa32a9dd2d673111a0b66481362be8cd4058>

### cr...@chromium.org (2024-11-21)

Thanks for the report! As noted, Rakina is OOO until next week, so we should reassign this for the time being.

I'm puzzled by the RenderDocument connection, but that might be because I'm unfamiliar with the code that hides the address bar on Android and how it works. For context, RenderDocument's kAllFrames mode causes Chrome to switch to a new RenderFrameHost on all same-site cross-document navigations. However, none of those cases are involved in the repro-- there's only a cross-site navigation which would have switched RenderFrameHosts anyway.

I suspect that DelayLayerTreeViewDeletionOnLocalSwap may be the difference, because that experiment just started recently (Canary/Dev/Beta only), in an effort to improve RenderDocument performance. The name suggests it should only affect same-site RFH swaps, but maybe it affects cross-site RenderFrameHost swaps as well? I'll note that the experiment involving DelayLayerTreeViewDeletionOnLocalSwap was just turned off for Android in cl/697609453 for crashes observed in <https://crbug.com/41496745>, so it's possible that this bug might not repro anymore either.

skym@: Can you say more about how the code to hide the omnibox works, or point to it in the codebase? Hopefully there's some connection between it and LayerTreeViews which might explain how the experiment is connected?

I'll also CC khushalsagar@, who knows a bit about the DelayLayerTreeViewDeletionOnLocalSwap experiment, in case he's able to spot a connection.

### al...@alesandroortiz.com (2024-11-21)

As mentioned in the report:

> In these PoCs, the initiator is cross-site from the destination, but the PoCs also work if both the initiator and destination pages are same-origin. This doesn't seem to affect behavior.

I've verified cross-site and same-site behavior is the same on latest Canary+Chromium, and on the bisected Chromium version, so that didn't change over time.

I think I tried enabling `DelayLayerTreeViewDeletionOnLocalSwap` by itself and it didn't repro, but I'll re-check.

Update: I tried several flag combinations based on the config in [1] but none resulted in repro unless `RenderDocumentWithNavigationQueueing` was enabled with `level/all-frames` params. Maybe I'm holding something wrong, though.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/third_party/angle/testing/variations/fieldtrial_testing_config.json;l=19608;drc=220d6e677b98a817d0bffd5254b3ba5be7ab86f3>

### al...@alesandroortiz.com (2024-11-21)

The Stable config `RenderDocumentWithNavigationQueueing.Default:level/subframe/queueing_level/full` IIUC also enables `DelayLayerTreeViewDeletionOnLocalSwap`, so I'm currently leaning more towards it being a `RenderDocument` or `QueueNavigationsWhileWaitingForCommit` issue.

If it is indeed some navigation-related issue, it may be due to extra or missing IPC message(s) putting the address bar in the wrong state.

Update: While `queueing_level` param doesn't seem to have any effect on repro, the code does force this param to `full` if using `level/subframe` or `level/all-frames`, so there's still a chance `QueueNavigationsWhileWaitingForCommit` is involved.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/common/content_navigation_policy.cc;l=175;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34>

### sk...@google.com (2024-11-21)

> skym@: Can you say more about how the code to hide the omnibox works, or point to it in the codebase? Hopefully there's some connection between it and LayerTreeViews which might explain how the experiment is connected?

Generally, we have two options from the omnibox/toolbar side. We can decide we're in BrowserControlsState.SHOWN (must show Java view, no translating the toolbar) or we're in BrowserControlsState.BOTH mode (it's okay to swap to rendered bitmap, okay to translate/hide toolbar). When we have a navigation, we switch to SHOWN for the next 3 seconds, locking the toolbar. Then after 3 seconds are done, we go to BOTH mode, giving control back to the renderer side.

Presumably, in this case, the load happens, we send SHOWN, then after 3 seconds, we send BOTH. I'm a little confused if that 3 seconds starts at the start or end of the navigation. Looking at TabStateBrowserControlsVisibilityDelegate it looks like it should be the end (onPageLoadFinished), but something must be causing the toolbar to be shown during the navigation, and I don't fully understand what's controlling that.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java;l=118;drc=aed2f60917e3aa3cc3da98a3c443edce5933b07a>

There's also more logic in other places that also tries to keep the toolbar on the screen, mostly for performance reasons, but should be combined in a way that only makes it more restrictive, not less.

As someone that doesn't interact with security bugs very often, I don't quite understand the urgency here Charlie, instead of waiting 2 more work days for Rakina to get back. And how I should prioritize this against my other work.

### cr...@chromium.org (2024-11-21)

Thanks for the context and code pointer!

> As someone that doesn't interact with security bugs very often, I don't quite understand the urgency here Charlie, instead of waiting 2 more work days for Rakina to get back. And how I should prioritize this against my other work.

I assigned it back to you for a few reasons:

- It's [high severity](https://www.chromium.org/developers/severity-guidelines/#high-severity) (S1), and appears to match one of the examples for that category ("Complete control over the apparent origin in the omnibox"), which means we want to get a fix into the current stable milestone and out to all users in a short time frame (no later than 60 days). Given the holidays coming up, it seems like we can make progress on it before Rakina gets back and others disappear. And in general, high severity bugs should take priority over other work.
- I don't yet see a direct connection between RenderDocument's behavior and the omnibox hiding logic, even after what you describe, so I'm not sure whether Rakina will have much to add beyond a description of how the feature works, which I started to offer in [comment #19](https://issues.chromium.org/issues/379652406#comment19). There's obviously some connection between the two based on the reporter's findings, but so far it's not obvious to me.
- I suspect that diagnosing the bug will require debugging the omnibox hiding logic with and without that particular RenderDocument level enabled and observing the difference. That seems easier for someone familiar with the omnibox hiding logic (by just enabling and disabling the feature) than for someone familiar with RenderDocument (who may not have as much Chrome for Android knowledge or an Android debugging setup). Navigation folks like Rakina and myself are happy to answer questions about how the RenderDocument mode is behaving differently, but I think it would be harder for us to diagnose and fix the omnibox behavior.

> Presumably, in this case, the load happens, we send SHOWN, then after 3 seconds, we send BOTH. I'm a little confused if that 3 seconds starts at the start or end of the navigation. Looking at TabStateBrowserControlsVisibilityDelegate it looks like it should be the end (onPageLoadFinished), but something must be causing the toolbar to be shown during the navigation, and I don't fully understand what's controlling that.

Yes, this is a good question. Presumably the timer should start (or get reset if it's already in progress) after the navigation commits, rather than when the navigation starts. Hopefully that's usually the case, such as when this RenderDocument mode isn't enabled. It would be interesting to find out why we don't end up in SHOWN mode when the second navigation commits. Would you be able to take a closer look at that part? Thanks!

### al...@alesandroortiz.com (2024-11-21)

I added logging to the relevant nav logic, and counterintuitively, it does seem like `ShouldChangeRenderFrameHostOnSameSiteNavigation()` returns true here [1] even on cross-site navigations in this scenario, and the rest of the relevant RenderDocument code path seems to be the same as with same-site navigations.

With RenderDocument enabled, it uses a speculative RFH; if disabled, it uses current RFH.

I'll add logging around the toolbar logic on Thursday to see how `BrowserControlsState` is changing (and hopefully identify why), unless Sky gets to it first :) (thanks for taking an initial look!)

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=1722;drc=5d0194cbc9cddc2ad096da32f16d7d1eac5d4a34>

### cr...@chromium.org (2024-11-21)

> I added logging to the relevant nav logic, and counterintuitively, it does seem like ShouldChangeRenderFrameHostOnSameSiteNavigation() returns true here [1] even on cross-site navigations in this scenario, and the rest of the relevant RenderDocument code path seems to be the same as with same-site navigations.

Oh, that's probably because Android only has partial Site Isolation, and the two sites in this case likely don't require locked processes. That means they'll both end up in the same unlocked SiteInstance, and would use the current RFH unless RenderDocument is enabled (in which case all cross-document navigations create a new RFH).

This either suggests that an actual cross-process navigation in Android (to or from a site that requires a locked process) might also be vulnerable to omnibox hiding, or that there's another RenderDocument / DelayLayerTreeViewDeletionOnLocalSwap behavior involved as well. It's easy to test the cross-process case with your current repro URLs by turning on chrome://flags#enable-site-per-process.

### al...@alesandroortiz.com (2024-11-21)

Seems like your hunch is correct. On Chromium build and Stable, with no overridden flags, I'm able to repro with cross-site with #enable-site-per-process is enabled (and no repro on same-site). I verified there was no repro in both scenarios with site isolation at default.

That makes this is much more easy to exploit in Stable (and other channels), if attacker can force that cross-process scenario.

### pe...@google.com (2024-11-21)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-11-21)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@alesandroortiz.com (2024-11-21)

Added logging to `TabStateBrowserControlsVisibilityDelegate`. Taking closer look at logs and doing re-runs, but something that jumps out: `onPageLoadFinished` (of initial page) and `onPageLoadStarted` (of slow page) order is different, which results in significantly different code paths afterwards...

Repro: `onPageLoadStarted`, `onPageLoadFinished`

No repro: `onPageLoadFinished`, `onPageLoadStarted`

### sk...@google.com (2024-11-21)

Okay, pnoland@ did some investigating into the logic in TabStateBrowserControlsVisibilityDelegate and found some problems, sorry for being so skeptical here, I was wrong.

> Yes, this is a good question. Presumably the timer should start (or get reset if it's already in progress) after the navigation commits, rather than when the navigation starts. Hopefully that's usually the case, such as when this RenderDocument mode isn't enabled. It would be interesting to find out why we don't end up in SHOWN mode when the second navigation commits. Would you be able to take a closer look at that part? Thanks!

Okay, so there are 2 events going on here. Normally we get a onPageLoadStarted, and we lock the controls indefinitely. Then we get a onPageLoadFinished, and we start a 3 second timer to unlock.

Part of the problem here is that we are getting 2 navigations' events interleaved, <https://paste.googleplex.com/6444659982467072> . Okay so to reframe, there are 3 problems

1. Who ever is generating these events interleaves them for the 2 navigations/urls.
2. TabStateBrowserControlsVisibilityDelegate releases browser controls before the 2nd navigation finished. We're sending BOTH before onPageLoadFinished is even run, let alone 3 seconds. If the page was scrollable, you'd be able to scroll it off manually too fast.
3. Something on the render side far away is removing the browser controls without user interaction.

Looking back at the previous time we had a similar bug, I filed [crbug.com/40926082](https://crbug.com/40926082) to deal with interleaved events on our side but we never got around to it. And the previous version of #3 filed [crbug.com/40281408](https://crbug.com/40281408) to fix the renderer side, but that never got fixed either.

I don't see a nice band aid for #2 to avoid doing the wrong thing here. I can start tracking URLs in TabStateBrowserControlsVisibilityDelegate but we run the risk of leaving the browser controls locked (if I don't get a matching URLs) and a worse user experience. Really this kind of change/fix should be done in an A/B test and rolled out to verify we don't regress the user experience.

Toggling #enable-site-per-process, I see the same sequence of events for Enabled and Disabled. But it only repros on Enabled, so #3 must be the difference.

### al...@alesandroortiz.com (2024-11-21)

I can't see the paste, but seems like we're seeing the same thing (nav events in different order). I've been testing with #enable-site-per-process, to focus on the cross-process behavior and exclude any other `RenderDocument` behavior.

Thanks for digging into this!

I'm still trying to discern why `<style>` tag matters here in the first page. Without it, no repro. With it, repro. Although thinking about it, that's likely to affect when renderer considers document loaded, which would affect repro...

### sk...@google.com (2024-11-21)

Oh, sorry about that, I just added some logging to TabStateBrowserControlsVisibilityDelegate and reproed with your site.

```
11-21 09:38:08.243 26633 26633 E cr_TSBCVD: SKYM onPageLoadStarted https://alesandroortiz.com/security/chromium/android-hide-address-bar-minimal.html
11-21 09:38:08.243 26633 26633 E cr_TSBCVD: SKYM mIsFullscreenWaitingForLoad true
11-21 09:38:08.539 26633 26633 E cr_TSBCVD: SKYM onDidFinishNavigationInPrimaryMainFrame
11-21 09:38:08.645 26633 26633 E cr_TSBCVD: SKYM onPageLoadStarted https://aogarantiza.com/chromium/slow.php?s=3&ts=1732210688547
11-21 09:38:08.654 26633 26633 E cr_TSBCVD: SKYM onPageLoadFinished https://alesandroortiz.com/security/chromium/android-hide-address-bar-minimal.html
11-21 09:38:11.655 26633 26633 E cr_TSBCVD: SKYM mIsFullscreenWaitingForLoad false
11-21 09:38:12.004 26633 26633 E cr_TSBCVD: SKYM onDidFinishNavigationInPrimaryMainFrame
11-21 09:38:12.029 26633 26633 E cr_TSBCVD: SKYM onPageLoadFinished https://aogarantiza.com/chromium/slow.php?s=3&ts=1732210688547

```

### al...@alesandroortiz.com (2024-11-21)

Thanks, yep, we're seeing the same thing. Attached similar logs.

### al...@alesandroortiz.com (2024-11-21)

Also have these no-repro pages if helpful:

- <https://alesandroortiz.com/security/chromium/android-hide-address-bar-minimal-with-delay.html> (`setTimeout(nav, 0)`)
- <https://alesandroortiz.com/security/chromium/android-hide-address-bar-minimal-no-style-tag.html> (no style tag)

Logs above are actually with/without style tag.

### yf...@google.com (2024-11-21)

+Peilin FYI - as this might explain the graphical hitch with the omnibox we're seeing in BCIV (but is orthogonal to security in question).


### yf...@google.com (2024-11-21)

Overall, in the app layer I (think) this is breaking the mental model.

Like I would have generally assumed that there aren't interleaved start/finishes. Finish is modeled as "this page can be processed"

### sk...@google.com (2024-11-21)

Okay, have 3 versions of potential changes. I was trying to satisfy [crbug.com/40926082](https://crbug.com/40926082) at the same time, but it really feels like it introduces a bunch of risk.

onDidStartNavigationInPrimaryMainFrame w/ Set <https://chromium-review.googlesource.com/c/chromium/src/+/6040200>

onDidStartNavigationInPrimaryMainFrame w/ handle + assert <https://chromium-review.googlesource.com/c/chromium/src/+/6042421>

pnoland@'s no onPageLoadFinished <https://chromium-review.googlesource.com/c/chromium/src/+/6040202>

I'm leaning towards the approach that just removes onPageLoadFinished. It feels the safest. As far as we can tell, onDidFinishNavigationInPrimaryMainFrame w/ commit + onPageLoadFailed covers all the cases. I'm thinking I'll throw a default on feature flag as a kill switch, that hopefully doesn't need to be cached. I could add metrics now that we're not missing any cases, but it would bloat the CL and I'm not sure how to do them yet. And ideally as a follow up we roll out the simplification in an A/B.

Trying to read all the comments here, is this reproing on stable right now without any chrome://flags changes? Or just through Beta? Trying to understand if/how much merging is going to be needed. Or can we just turn off an experiment temporarily?

### yf...@google.com (2024-11-21)

Also discussion above shows how the experiment in question could be a performance degradation (?) if it forces process swaps on all navs?

### al...@alesandroortiz.com (2024-11-21)

Re: [#comment36](https://issues.chromium.org/issues/379652406#comment36), agreed, feels like something that can be improved in navigation.

Side note: I'm curious if `RenderDocument` results in Android WebView getting new renderer process for each nav. If so, then this will probably be an issue for apps that listen to specific events and assume correct order for their own address bar or some other security surface. (Similar to what's happening here.) If I'm able to repro this or some other issue due to out-of-order nav events in WebView, I'll report separately.

Sky: Thanks for the quick CLs!

Correct, this repros on Stable (and everywhere else) without any overridden flags if there's a cross-process navigation. So navigating to/from an origin listed in `chrome://process-internals/#site-isolation` will repro the issue. (Initially mentioned in [#comment25](https://issues.chromium.org/issues/379652406#comment25) and [#comment26](https://issues.chromium.org/issues/379652406#comment26).)

My Stable browser lists "COOP, Password Sites, Logged-in Sites" as places where site isolation is enforced, plus there's a bunch of built-in origins. I'll try to spin up a PoC for Stable that opts into site isolation, so there's no flags required.

### yf...@google.com (2024-11-21)

Yep, that's partial site isolation creis@ mentioned above.

So it seems like this _is_ a bug in navigation then? If we've changed the invariants? Or was it always the case that they could be interleaved?  (I may not have fully grokked all the discussion up thread)

### yf...@google.com (2024-11-21)

Oh sorry, I just re-read #39 - it was always a bug it's just higher incidence with the flag, as it increases process swaps. 

### yf...@google.com (2024-11-21)

> pnoland@'s no onPageLoadFinished https://chromium-review.googlesource.com/c/chromium/src/+/6040202

When do we unlock then?

Switching fgrom "PageLoad" to "Navigation" means omnibox will trigger on same-site nav's won't it (e.g. even history.{push,replace}State including when it happens on scroll) which I don't think we want? You would probobably filter out isSameSite at minimum.

https://chromium-review.googlesource.com/c/chromium/src/+/6040200 feels relatively safe if we can expect interleaving but ther'es a follow-up to look at other areas of app code :/

### al...@alesandroortiz.com (2024-11-21)

Okay, here is PoC that will work on Stable, no flag overrides required:

<https://alesandroortiz.com/security/chromium/android-hide-address-bar-minimal-coop.html> (the destination page sets COOP headers to force cross-process nav, `Cross-Origin-Opener-Policy: same-origin`)

### yf...@google.com (2024-11-21)

Consulted with some folks and was pointed ot https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/web_contents_observer.h;l=322?q=web_contents_observer.h&ss=chromium

So I think this was likely an existing bug in the app layer that is more prominent with the experiment.

### cr...@chromium.org (2024-11-21)

> Also discussion above shows how the experiment in question could be a performance degradation (?) if it forces process swaps on all navs?

If you're referring to RenderDocument, that's not what it does. RenderDocument does not change anything about how often process swaps occur. It only causes RenderFrameHost swaps on all cross-document navigations, staying within the same process. I don't know yet whether RenderDocument changes whether interleaved events are possible for different same-process navigations, but it sounds like that might be true.

> Side note: I'm curious if RenderDocument results in Android WebView getting new renderer process for each nav. If so, then this will probably be an issue for apps that listen to specific events and assume correct order for their own address bar or some other security surface. (Similar to what's happening here.) If I'm able to repro this or some other issue due to out-of-order nav events in WebView, I'll report separately.

As above, RenderDocument doesn't change how often there are cross-process navigations (even on Android WebView), but if it is the cause for any new interleaving of navigation events on same-process navigations, then that may affect the RenderDocument experiment on Android WebView. (Rakina will have to chime in on what channels Android WebView uses RenderDocument, and whether it ever includes kAllFrames or just subframe cases.) In general, Android WebView does almost no process swaps on navigations-- I think they only happen for SafeBrowsing warning pages.

I'll comment separately about the interleaving question.

### yf...@google.com (2024-11-21)

> It only causes RenderFrameHost swaps on all cross-document navigations, staying within the same process.

Ack! All good then.

Overall, it feels like the even more correct fix is to propagate PrimaryPageChanged up to Java (it's blissfully unaware :/) and use that but we can eliminate the race by ensuring no pending loads as in https://chromium-review.googlesource.com/c/chromium/src/+/6040200 ?

### al...@alesandroortiz.com (2024-11-21)

Did bisect based on COOP PoC in [#comment43](https://issues.chromium.org/issues/379652406#comment43) without any flag overrides. This repros all the way down to r684675 (78.0.3877.0) which enabled `ProactivelySwapBrowsingInstance` field test [1], so it's probably existed forever where there is a cross-process swap, regardless of what caused the swap to occur. :/ So probably repros well before that if there's some other reason to do a process swap.

[1] <https://crrev.com/ab7700c387f9167d763484cfa659ef7931103890>

### cr...@chromium.org (2024-11-21)

Regarding interleaving, I don't think there has ever been a guarantee that navigations won't overlap in time. Certainly navigations in different frames of a page can overlap in time, but I think even the same frame can have multiple NavigationRequests at once. For example, if one NavigationRequest is near the end but waiting for the renderer process to commit and then a new NavigationRequest is created, we'll probably hear the DidStartNavigation for the second one before hearing the DidFinishNavigation for the first, though I haven't confirmed this. yfriedman@ is correct that there's [no guarantee](https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/web_contents_observer.h;drc=6420d743079b4d60da566a6d5978ee8983b212e6;l=322) that DidFinishNavigation will be called for any particular navigation before DidStartNavigation is called on the next.

I'm not sure exactly what events onPageLoadFinished in the Java layer is called for, though-- does always correspond to a particular WebContentsObserver event, or could it be called in more cases?

### cr...@chromium.org (2024-11-21)

> Did bisect based on COOP PoC in [#comment43](https://issues.chromium.org/issues/379652406#comment43) without any flag overrides. This repros all the way down to r684675 (78.0.3877.0) which enabled ProactivelySwapBrowsingInstance field test [1], so it's probably existed forever where there is a cross-process swap, regardless of what caused the swap to occur. :/ So probably repros well before that if there's some other reason to do a process swap.

`ProactivelySwapBrowsingInstance` doesn't necessarily do a process swap either. It often creates a new RenderFrameHost in a different BrowsingInstance but the same process, if a process swap wasn't otherwise needed (e.g., for a site requiring a lock).

I'm suspecting that this bug becomes possible for any RenderFrameHost swap, whether it's cross-process or same-process. There are many things that can cause RenderFrameHost swaps, and more reasons are introduced over time:

- Since Chrome originally launched, it could do the equivalent of a RFH swap (with RenderViewHost) on some cross-site navigations, which were cross-process.
- When Site Isolation launched in M67, all cross-site navigations on desktop started doing RFH swaps, which were cross-process.
- Site Isolation on Android did RFH swaps to a new process for sites requiring a locked process.
- ProactivelySwapBrowsingInstance introduced RFH swaps (possibly within the same process) on some browser-initiated navigations, partly to make bfcache work on more pages ([see here](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/browsing_context_group_swap.h;drc=c325fff94cab7b3d378b5f367f75249662bbeaeb;l=34)).
- RenderDocument is introducing RFH swaps on all cross-document navigations, mostly affecting same-process navigations (without changing how many are cross-process).

RenderFrameHost swaps all involve creating a speculative RFH while the navigation is in progress, which might or might not change the order of certain events, and that could be contributing to the behavior here.

### al...@alesandroortiz.com (2024-11-21)

Ah, thanks for clarifying in [#comment49](https://issues.chromium.org/issues/379652406#comment49). Then we can probably replace "cross-process swaps" with "RFH swaps" in most of my comments above. As you noted, RFH swaps being cause definitely aligns with `RenderDocument` flag causing repro.

### yf...@google.com (2024-11-21)

> I'm not sure exactly what events onPageLoadFinished in the Java layer is called for, though-- does always correspond to a particular WebContentsObserver event, or could it be called in more cases?

It was supposed to link to WebContents + primary frame: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/android/web_contents_observer_proxy.cc;l=176;drc=c325fff94cab7b3d378b5f367f75249662bbeaeb;bpv=1;bpt=1?q=didFinishLoadInPrimaryMainFrame%20file:cc&ss=chromium%2Fchromium%2Fsrc

So it was only ever looking at one frame (agree would expect it across multiple frames). But looks like whenever this was done (many moons ago) it was a wrong assumption.

Additionally, looks like there are cases where the app layer forces a stop (including calling it on the WebContents) but it's work to determien if that would preven further notifications: 
https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabImpl.java;l=872;drc=c325fff94cab7b3d378b5f367f75249662bbeaeb;bpv=1;bpt=1

Long story short, Sky, I still think the immediate fix is probably https://chromium-review.googlesource.com/c/chromium/src/+/6040200 but only for document transitions

### sk...@google.com (2024-11-21)

> Switching fgrom "PageLoad" to "Navigation" means omnibox will trigger on same-site nav's won't it (e.g. even history.{push,replace}State including when it happens on scroll) which I don't think we want? You would probobably filter out isSameSite at minimum.

Oh no... I didn't think about this at all. We already had used onDidFinishNavigationInPrimaryMainFrame, is it possible our behavior wouldn't actually change here? I should test.

> Long story short, Sky, I still think the immediate fix is probably <https://chromium-review.googlesource.com/c/chromium/src/+/6040200> but only for document transitions

I'm sorry, I don't really understand things very well here. What is a "document transition"? How do I check for this?

### cr...@chromium.org (2024-11-22)

> Switching fgrom "PageLoad" to "Navigation" means omnibox will trigger on same-site nav's won't it (e.g. even history.{push,replace}State including when it happens on scroll) which I don't think we want? You would probobably filter out isSameSite at minimum.

I think you might mean same-document (e.g., pushState, fragment) rather than same-site (which could be cross-document URLs within example.com).

> What is a "document transition"? How do I check for this?

I think that is about ensuring that a cross-document navigation occurred. Most code checks [NavigationHandle::IsSameDocument()](https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/navigation_handle.h;drc=811a4b2a48b04198aa89f929988be18417f4022b;l=347) to determine that, similar to HasCommitted() to skip cases like downloads that don't actually commit.

### yf...@google.com (2024-11-22)

Yep, agree with cries on both, sorry for confusion

### ap...@google.com (2024-11-26)

Project: chromium/src  

Branch: main  

Author: Sky Malice <[skym@chromium.org](mailto:skym@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6040200>

Rework locking controls from navigations.

---


Expand for full commit details
```
Rework locking controls from navigations. 
 
Page load and navigation events are not guaranteed to be delivered for one navigation at a time. Instead they can be interleaved. This is causing a problem when a slow navigation starts before the previous navigation is completed. After the 3 second wait, we erroneously unlocked the browser controls when they should not be. 
 
To fix this, all page load events were switched to navigation events. And we now track navigation ids in a set, and only unlock when the set is empty. Special casing for same document navigations was added to handle the difference between navigation events and page load events. This approach has the potential danger of leaving browser controls locked forever if we miss an event. 
 
To mitigate this risk, this CL adds a kill switch and a histogram that counts the number of outstanding navigations when a navigation completes. 
 
Bug: 379652406 
Change-Id: I6a837b7f7b2103c6f811e130bf582ac38c66c763 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6040200 
Commit-Queue: Sky Malice <skym@chromium.org> 
Reviewed-by: Patrick Noland <pnoland@chromium.org> 
Reviewed-by: Sinan Sahin <sinansahin@google.com> 
Reviewed-by: Yaron Friedman <yfriedman@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1388487}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java`
- M `chrome/android/junit/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegateTest.java`
- M `chrome/browser/flags/android/chrome_feature_list.cc`
- M `chrome/browser/flags/android/chrome_feature_list.h`
- M `chrome/browser/flags/android/java/src/org/chromium/chrome/browser/flags/ChromeFeatureList.java`
- M `testing/variations/fieldtrial_testing_config.json`
- M `tools/metrics/histograms/metadata/android/histograms.xml`

---

Hash: 2a80258ed798263eeff7ca49f3c13d389eb87df8  

Date:  Tue Nov 26 22:13:00 2024


---

### al...@alesandroortiz.com (2024-11-30)

Verified as fixed on 133.0.6868.0 Canary using:

- No overridden flags + <https://alesandroortiz.com/security/chromium/android-hide-address-bar-minimal-coop.html> (from [#comment43](https://issues.chromium.org/issues/379652406#comment43))
- Enabling site-per-process + <https://alesandroortiz.com/security/chromium/android-hide-address-bar-minimal.html> (from main report)

Thanks for quick fix and discussion!

For VRP: Root cause (interleaved navigation events) was posted simultaneously in [#comment29](https://issues.chromium.org/issues/379652406#comment29) and [#comment30](https://issues.chromium.org/issues/379652406#comment30). Earlier comments show variations bisect work that eventually led to `RenderDocument`, which led to identifying RFH swap as requirement for repro. Any navigation can trigger repro if RFH swap occurs, and attacker can force RFH swap using COOP ([#comment43](https://issues.chromium.org/issues/379652406#comment43)). Also confirmed Stable repro in [#comment11](https://issues.chromium.org/issues/379652406#comment11) and [#comment43](https://issues.chromium.org/issues/379652406#comment43). This has similar triggers and impacts as [issue 40064686](https://issues.chromium.org/issues/40064686).

### pe...@google.com (2024-12-06)

skym: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### al...@alesandroortiz.com (2024-12-09)

Friendly ping: Can someone please mark this as fixed, so it can be merged back as needed and also go to VRP panel?

### al...@alesandroortiz.com (2024-12-09)

Thanks!

### pe...@google.com (2024-12-10)

Security Merge Request Consideration: Requesting merge to stable (M131) because latest trunk commit (1388487) appears to be after stable branch point (1368529).
Security Merge Request Consideration: Requesting merge to beta (M132) because latest trunk commit (1388487) appears to be after beta branch point (1381561).
Security Merge Request - Manual Review: Merge review required: M131 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M132 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [131, 132].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-12-10)

Thanks for your work on this, skym@ and thank you creis@ and yfriedman@ for the collaborative effort here to get this issue mitigated.

I don't quite trust the foundin here and suspect this issue goes back farther than current Stable channel; however, due to adding a new feature and the general potential risk here, I am only approving this fix for backmerge to M132 Beta. Thank you for adding a kill switch as well as histogram to gather navigation metrics, but seeing as how 131 is current Stable we are going into a release freeze in < 10 days, I'm going to decline a backmerge to Stable or older channels at this time.

Looking at substantial Canary and Dev data for Android so far, since this fix was landed on 26 November, I'm not seeing any issues related to this fix at this time, therefore, I'm approving backmerge to M132 Beta, please proceed with backmerging to branch 6834 at your convenience.

### al...@alesandroortiz.com (2024-12-10)

> suspect this issue goes back farther than current Stable channel

Most definitely, I was able to repro as far back as M78 with COOP + no overridden flags, and likely repro'd before that if RFH swap occurred for any reason (see [#comment47](https://issues.chromium.org/issues/379652406#comment47))

### yf...@google.com (2024-12-10)

FWIW, I agree on your assessment; while I don't think this is buggy, it's certainly not the easiest area to reason about. Given holiday seasons and lower coverage, next stable sgtm.

### ap...@google.com (2024-12-10)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Sky Malice <[skym@chromium.org](mailto:skym@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6086009>

Rework locking controls from navigations.

---


Expand for full commit details
```
Rework locking controls from navigations. 
 
Page load and navigation events are not guaranteed to be delivered for one navigation at a time. Instead they can be interleaved. This is causing a problem when a slow navigation starts before the previous navigation is completed. After the 3 second wait, we erroneously unlocked the browser controls when they should not be. 
 
To fix this, all page load events were switched to navigation events. And we now track navigation ids in a set, and only unlock when the set is empty. Special casing for same document navigations was added to handle the difference between navigation events and page load events. This approach has the potential danger of leaving browser controls locked forever if we miss an event. 
 
To mitigate this risk, this CL adds a kill switch and a histogram that counts the number of outstanding navigations when a navigation completes. 
 
(cherry picked from commit 2a80258ed798263eeff7ca49f3c13d389eb87df8) 
 
Bug: 379652406 
Change-Id: I6a837b7f7b2103c6f811e130bf582ac38c66c763 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6040200 
Commit-Queue: Sky Malice <skym@chromium.org> 
Reviewed-by: Patrick Noland <pnoland@chromium.org> 
Reviewed-by: Sinan Sahin <sinansahin@google.com> 
Reviewed-by: Yaron Friedman <yfriedman@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1388487} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6086009 
Commit-Queue: Calder Kitagawa <ckitagawa@chromium.org> 
Auto-Submit: Sky Malice <skym@chromium.org> 
Reviewed-by: Calder Kitagawa <ckitagawa@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6834@{#1951} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java`
- M `chrome/android/junit/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegateTest.java`
- M `chrome/browser/flags/android/chrome_feature_list.cc`
- M `chrome/browser/flags/android/chrome_feature_list.h`
- M `chrome/browser/flags/android/java/src/org/chromium/chrome/browser/flags/ChromeFeatureList.java`
- M `testing/variations/fieldtrial_testing_config.json`
- M `tools/metrics/histograms/metadata/android/histograms.xml`

---

Hash: d99919b35058a84e910bddb33c0f9a0ee8b6a22d  

Date:  Tue Dec 10 23:41:33 2024


---

### sp...@google.com (2024-12-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
$5,000 for report of high-quality, moderate impact security UI spoof + $1,000 bisect bonus + $1,000 bonus for overall helpfulness and responsiveness in investigation and resolution


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-12)

Thanks for your your helpfulness and responsiveness in reporting this issue, Alesandro -- great work!

### yf...@google.com (2024-12-12)

Nice, congrats Alesandro - and ya, definitely appreciate your effort to ease repro and comms :)

### al...@alesandroortiz.com (2024-12-12)

Thanks for reward and extra bonus, really appreciate it! :)

Was tricky to bisect and nail down some details, so the quick responses from Chromium folks were also very helpful. Thanks again, everyone!

### ch...@google.com (2025-03-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pe...@google.com (2025-04-30)

Circling back on this, I'm wondering if this fix made the toolbar unlock too soon in the navigation chain. Before this change, the intention was to wait until the page has fully loaded, and unlock the controls 3 seconds later. Now, the controls can be unlocked while the page is still loading.

### sk...@google.com (2025-04-30)

I don't quite follow your line of reasoning Peilin. We're responding to onDidFinishNavigationInPrimaryMainFrame, I don't see how the navigation would still be loading here. The main frame should be finished, right?

### pe...@google.com (2025-05-01)

The navigation being finished only means that the navigation has committed, but at this point loading hasn't started yet ([more info here](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/navigation.md#loading)). It could be a long time before loading finishes.

We used to respond to onPageLoadFinished, which is called by didFinishLoadInPrimaryMainFrame, which should always come after onDidFinishNavigationInPrimaryMainFrame, and could come tens of seconds later.

### yf...@google.com (2025-05-07)

I think Peilin might be right.

+Ted who probably wrote the initial heuristic and as lead.

Ted/Charlie: wdyt? Should we revise the timing

### sk...@google.com (2025-05-07)

Interesting, you're saying there's a difference between the navigation being committed, and the page loading finishing. Just having the right url in the url bar for 3 seconds might not be enough. We'd prefer to have the combination of rendered website and correct url in the url bar for 3 seconds, to give the user time to judge the validity of the website.

That conceptually makes sense to me, especially on slowly loading pages. However, we'd need to add an observer method equivalent to onPageLoadFinished/onPageLoadFailed that contains the NavigationHandle, right?

### al...@alesandroortiz.com (2025-05-07)

This crbug is public, so someone should temporarily restrict visibility if the discussed behavior is a security concern. (Afterwards, please derestrict if determined not to be a security issue or when new crbug is fixed.)

### yf...@google.com (2025-05-07)

Thanks, I don't know it's super sensitive, but we can restrict in the interim.

### te...@google.com (2025-05-08)

Responding to c#73. My recollection on the original signals is pretty vague, so take this with a grain of salt.

But if my memory is right, we wanted to lock the toolbar onscreen while a navigation is pending (e.g. not responded to by the server), but as soon as we have a commit back from the website, we would start the 3 second timer. We wanted to ensure the domain was fully visible for a sufficient enough time to be visible to users (3 seconds), and we also didn't want to force the toolbar to be locked on screen if a page was very slow to completely load.

I would argue in the ideal world we would lock the toolbar on screen when a navigation starts (pre-commit), and then start the 3s unlock timer as soon as we have some non-trivial content on the screen.

### ch...@google.com (2025-05-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### yf...@google.com (2025-05-08)

Ok, so based on that, what we have isn't far off. We could adjust to first meaningful paint

### cr...@chromium.org (2025-05-08)

I'm not opposed to starting the timer at first meaningful paint instead of at navigation commit time-- that seems like an improvement to me for the reasons mentioned. One issue for implementation is that the NavigationHandle is deleted at commit time (and many observers rely on this), so it can't stick around until the later stages of loading. That may just require a different technique for doing the bookkeeping for the timer, though.

## Bounty Award

> $5,000 for report of high-quality, moderate impact security UI spoof + $1,000 bisect bonus + $1,000 bonus for overall helpfulness and responsiveness in investigation and resolution

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/379652406)*
