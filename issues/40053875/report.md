# Security: Some WebUI pages enable MojoJS bindings for the subsequently-navigated site

| Field | Value |
|-------|-------|
| **Issue ID** | [40053875](https://issues.chromium.org/issues/40053875) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>WebUI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2020-11-15 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When a tab is navigated to certain WebUI pages, such as chrome://process-internals/, the browser intentionally enables MojoJS bindings via RenderFrameHostImpl::EnableMojoJsBindings() [1]. However, if the same tab is navigated to another page, MojoJS bindings remain enabled for the non-WebUI page and any subsequent same-site navigations.

The MojoJS bindings are only available to the site navigated immediately after the WebUI page (e.g. chrome://.../ -> host-one.tld). This means any navigation to another page or subdomain of host-one.tld keeps MojoJS bindings enabled.

Navigating to a different site (e.g. host-one.tld -> host-two.tld) restores expected behavior (no MojoJS bindings). The process can be repeated to obtain the bindings.

Per <https://crbug.com/chromium/1055656> there's intent to enable MojoJS bindings in other WebUIs, therefore in the future more WebUIs could be used to obtain a renderer with bindings. It's currently only used in chrome://process-internals/ and chrome://conversion-internals/ WebUIs.

As far as I can tell, all the regular bindings which would be enabled with --enable-blink-features=MojoJS are available.

The WebUI page's specific bindings are protected by browser-side checks [2].

Based on my understanding, impacts should be similar to that of a compromised renderer.

I think navigations to WebUI URLs are only possible via browser-initiated navigation, therefore an attacker would need to convince a user to navigate to the WebUI page and then navigate to an attacker page. I vaguely recall vulns in the past where a page could navigate to WebUI URLs; similar vulns could reduce friction.

Relevant code:  

[1] RenderFrameHostImpl::EnableMojoJsBindings():  

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/renderer_host/render_frame_host_impl.cc;l=9523;drc=09f1f16d69ed13e420ebb4be3af7b856b6ca1848>  

The DCHECK in EnableMojoJsBindings() will be hit; comment it out to repro on a DCHECK-enabled build.

ProcessInternalsUI::RenderFrameCreated() which calls RFHI method above:  

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/process_internals/process_internals_ui.cc;l=57;drc=308c5d3b43be5a647b51c9a9361a5434798fb328>

ConversionInternalsUI::RenderFrameCreated which calls RFHI method above:  

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/conversions/conversion_internals_ui.cc;l=48;drc=308c5d3b43be5a647b51c9a9361a5434798fb328>

[2] For example, BindProcessInternalsHandler() will fail here due to the lack of WebUI -- I imagine it's difficult to bypass this check: <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/browser_interface_binders.cc;l=297;drc=308c5d3b43be5a647b51c9a9361a5434798fb328>

**VERSION**  

Chrome Version: 86.0.4240.183 (Official Build) (64-bit) (cohort: Stable) and 88.0.4311.0 (Developer Build) (64-bit) 256b94711e4f3f2bc105990db2b25e9f9059da26-refs/heads/master@{#822938}  

Operating System: Windows 10 OS Version 2004 (Build 19041.572)

**REPRODUCTION CASE**

1. Navigate a tab to chrome://process-internals/ or chrome://conversion-internals/
2. Navigate same tab to any page, such as <https://alesandroortiz.com/security/chromium/mojo-check.html>

Expected behavior:  

window.Mojo, window.MojoHandle, window.MojoWatcher are not available.

Observed behavior:  

window.Mojo, etc. are available.

To repro same-site behavior on same hostname:  

\* Perform steps 1 and 2 from main repro.  

3. Navigate to another same-site page, such as <https://alesandroortiz.com/security/> (will 404, that's okay)  

4. Use DevTools to check existence of window.Mojo (will exist)

To repro same-site behavior on different hostname:  

\* Perform steps 1 and 2 from main repro.  

3. Navigate to a subdomain, such as <https://c2.alesandroortiz.com/security/chromium/mojo-check.html>  

4. Use DevTools to check existence of window.Mojo (will exist)

To repro different-site behavior:  

\* Perform steps 1 and 2 from main repro.  

3. Navigate to another site, such as <https://aogarantiza.com>  

4. Use DevTools to check existence of window.Mojo (will not exist)

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [WebUI-MojoJS.mp4](attachments/WebUI-MojoJS.mp4) (video/mp4, 1.0 MB)
- [mojo-check.html](attachments/mojo-check.html) (text/plain, 383 B)
- [stack-trace-from-logs.txt](attachments/stack-trace-from-logs.txt) (text/plain, 10.9 KB)
- [crbug-1062091.html](attachments/crbug-1062091.html) (text/plain, 1.0 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 358 B)
- [background.js](attachments/background.js) (text/plain, 476 B)
- [crbug-1149215-escalation-via-crbug-1062091.mp4](attachments/crbug-1149215-escalation-via-crbug-1062091.mp4) (video/mp4, 6.2 MB)
- [addl-checks-crbug-1149215.diff](attachments/addl-checks-crbug-1149215.diff) (text/plain, 2.1 KB)

## Timeline

### [Deleted User] (2020-11-15)

[Empty comment from Monorail migration]

### dr...@chromium.org (2020-11-16)

Assigning Low severity. We frequently use a renderer with MojoJS bindings as a stand-in for a compromised renderer, so this seems like a extremely limited way to effectively compromise a renderer. Triaging to a content/ OWNER, since there doesn't seem to be a more specific OWNER file.

alexmos@ - can you take a look? 

[Monorail components: UI>Browser>WebUI]

### al...@alesandroortiz.com (2020-11-16)

I remembered any extension can navigate to chrome:// WebUI URLs (no permissions required), therefore the PoC below will work from an extension's background page. The PoC runs once on extension install (and any other time the background page is made active), but it can be called at any moment. Can also perform this on an existing tab instead of a new tab.

background.js:
chrome.tabs.create({ url: "chrome://process-internals/" }, function(tab) {
  chrome.tabs.update({ url: "https://alesandroortiz.com/security/chromium/mojo-check.html" });
});

manifest.json
{
	"name": "PoC for crbug 1149125",
	"author": "Alesandro Ortiz",
	"homepage_url": "https://AlesandroOrtiz.com",
	"version": "1.0",
	"description": "This extension will attempt to create a new WebUI tab and then navigate it to an attacker site.",
	"manifest_version": 2,
	"background": {
	  "scripts": ["background.js"],
	  "persistent": false
	}
}

### al...@alesandroortiz.com (2020-11-17)

Also verified on Chrome for Android Stable 86.0.4240.185 using same repro steps (navigate to chrome://process-internals/ and then mojo-check.html). Seems to have identical behavior as desktop.

### al...@alesandroortiz.com (2020-11-24)

Friendly ping: Any compromised or malicious extension can trivially gain access to MojoJS. I believe this can be leveraged to perform attacks which require a compromised renderer. I'm working on some PoCs to determine further impacts of an extension-initiated attack.

Perhaps nasko@ could take a look at this report? They implemented this functionality initially in https://source.chromium.org/chromium/chromium/src/+/8a73f7d87f14997fcbd9bd166813ae0e7bc88991



### al...@alesandroortiz.com (2020-11-29)

After further investigation, I noticed that content scripts loaded in the tab also have access to MojoJS. You can verify this using DevTools: change script context to any content script and check for existence of window.Mojo .

I also determined the issue is probably due to differing expectations about the lifetime of the WebContents observer added by ProcessInternalsUI when the WebUI is created.

When navigating to a new page on a different site instance, a new RenderFrameHost is created alongside the existing RenderFrameHost. On RFH creation, the WebContents calls RenderFrameCreated() for each of its observers. This is called prior to the existing RFH being unloaded or destroyed, therefore any observers which would be removed on RFH unload or destruct are still called.

The ProcessInternalsUI observer is removed on destruction of the ProcessInternalsUI instance itself, which at the earliest occurs when the prior RFH is unloaded [1] or destroyed (both events call RFHI::ClearWebUI()). Therefore, when the new RFH is created, the ProcessInternalsUI observer still exists and RenderFrameCreated() is called. This enables MojoJS for the new RFH, which effectively enables MojoJS for as long as the RFH is alive (typically stays alive until there's a site instance change).

Some other observers, such as ExtensionWebContentsObserver [2], perform checks to ensure they're being called in safe/expected conditions. It's not clear to me if the extension observer's checks were added knowing an observer is expected to sometimes be called with a non-extension RFH, or if they were added as a proactive precaution.

If the WebUI observer is intended to be called on creation of a non-WebUI RFH, then the fix could be to add similar checks to WebUI observers to ensure they're called only for WebUI RFHs.

If the WebUI observer is not intended to be called in this scenario, then other observers might currently be causing undesired behavior if they're called unexpectedly and don't have appropriate checks.

I've attached the stack trace of my local build at the point the DCHECK is hit. The relevant calls start after the RenderFrameHostManager::GetFrameHostForNavigation() call.

[1] RFHI::OnUnloaded() calls ClearWebUI() here: https://source.chromium.org/chromium/chromium/src/+/master:content/browser/renderer_host/render_frame_host_impl.cc;l=3422;drc=e2442de95e2d116c97dc81828a1200c8251f54c1

[2] https://source.chromium.org/chromium/chromium/src/+/master:extensions/browser/extension_web_contents_observer.cc;l=108;drc=28d989a1fc83edb779c034cad48572775696bc66

### al...@alesandroortiz.com (2020-11-30)

Attached are files for a PoC extension which uses this renderer compromise to trigger the UAF from https://crbug.com/chromium/1062091 without user interaction or extension permissions. Video of repro also attached.

Set up:
1. Download and extract ASan build for 82.0.4058.0, which is vulnerable to https://crbug.com/chromium/1062091 and this issue: https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release_x64/asan-win32-release_x64-740999
2. Download the attached crbug-1062091.html into the "gen" directory of the extracted ASan build.
3. Run a local HTTP server in the "gen" directory (e.g. npx http-server) to make crbug-1062091.html available over HTTP.
4. In a dedicated directory, download the attached manifest.json and background.js. If necessary, update the PoC URL in background.js.
5. Start the ASan browser and install the unpacked extension from step 4. (It will repro on install and on browser startup.)

To repeat repro: Start ASan browser and wait for repro execution.

To disable repro on start: In manifest.json, set background.persistent to false. With this value set to false, it will only run on extension install or extension reload.

### al...@alesandroortiz.com (2020-11-30)

Per https://bugs.chromium.org/u/3267981708/ owner is OOO until 12/7 (next week); perhaps someone else can take a look this week?

### dp...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### dp...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### dc...@chromium.org (2020-12-01)

I think there's an argument for this to be medium or high, as MojoJS + another IPC bug = full sandbox escape. Tentatively marking as high.

### dc...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### cr...@chromium.org (2020-12-01)

Thanks dcheng@!  I agree this sounds high severity at first glance, potentially with a mitigating factor that web attackers can't trigger the WebUI navigation for setting up the issue (though extensions can).  Let's look at possible solutions as well as ways to avoid issues like this in the future, as we discussed on chat.

Thanks also to dpapad@ for looping more of us in while alexmos@ is OOO, and to the reporter for the frequent pings!

### [Deleted User] (2020-12-01)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@chromium.org (2020-12-01)

I think this is a duplicate of https://crbug.com/chromium/1148682, but I will investigate a bit later today or tomorrow.

### dc...@chromium.org (2020-12-01)

The fix should be simple, but the browser test I'm trying to write doesn't seem to trigger this, despite the fact that the speculative RFH is, in fact, created while the WebUIController for chrome://conversion-internals is still live...

### al...@alesandroortiz.com (2020-12-01)

dcheng@: The following info might be helpful for https://crbug.com/chromium/1149125#c16.

Based on logs, I noticed some WebUIs such as chrome://sandbox (Sandbox Internals) have their observer RenderFrameCreated() called only once (on expected RFH), while others such as Process Internals are called twice (on expected + unexpected RFHs). The main difference I see between both types of WebUIs is they are created differently ([1] vs [2]). Perhaps the way the WebUIs are created (or something else about them) is why it won't repro in the tests.

Info above might also be useful to understand how other observer methods might be unexpectedly executed (I'm currently auditing other places of interest, but nothing jumps out as having a security impact other than this reported issue).

[1] Process Internals UI: https://source.chromium.org/chromium/chromium/src/+/master:content/browser/webui/content_web_ui_controller_factory.cc;l=92;drc=d81c5852498699fe3cd812e78d31c77c28e29281

[2] Sandbox Internals UI: https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/webui/chrome_web_ui_controller_factory.cc;l=931;drc=d81c5852498699fe3cd812e78d31c77c28e29281

### dc...@chromium.org (2020-12-01)

OK, for some reason, it's only process-internals that leaks the MojoJS binding like this in the test. It's unclear why.

### dc...@chromium.org (2020-12-01)

OK, mystery solved: it's because WebUIController and WebContentsObserver *both* provide RenderFrameCreated overrides.
ConversionInternalsUI never registers its WCO and never observes anything, so only gets the WebUIController callback.
ProcessInternalsUI registers its WCO and gets the WebUIController *and* WCO callbacks.

### al...@alesandroortiz.com (2020-12-01)

Ah, makes sense. I thought chrome://conversion-internals/ also repro'd issue but I just re-checked and it definitely doesn't. Must have written down the incorrect result in in my notes, apologies for that. Thanks for investigating!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0d360f554b501d57b72d4a2ccb744645e662e200

commit 0d360f554b501d57b72d4a2ccb744645e662e200
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Dec 01 23:11:42 2020

[WebUI] Use WebUIController::RenderFrameCreated() to request MojoJS.

ConversionInternalsUI and ProcessInternalsUI don't need to be
WebContentsObservers at all, since WebUIController already provides a
RenderFrameCreated() override that is scoped WebUI-specific
RenderFrameHosts.

Bug: 1148682, 1149125
Change-Id: Iebef544d7fb7c8938d273c84279ce7e8b19f90a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2566889
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#832563}

[modify] https://crrev.com/0d360f554b501d57b72d4a2ccb744645e662e200/content/browser/conversions/conversion_internals_browsertest.cc
[modify] https://crrev.com/0d360f554b501d57b72d4a2ccb744645e662e200/content/browser/conversions/conversion_internals_ui.h
[modify] https://crrev.com/0d360f554b501d57b72d4a2ccb744645e662e200/content/browser/process_internals/process_internals_browsertest.cc
[modify] https://crrev.com/0d360f554b501d57b72d4a2ccb744645e662e200/content/browser/process_internals/process_internals_ui.cc
[modify] https://crrev.com/0d360f554b501d57b72d4a2ccb744645e662e200/content/browser/process_internals/process_internals_ui.h


### dc...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-02)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2020-12-02)

Thanks for fix and review, dcheng@ and nasko@! I'll wait for it to hit Canary tomorrow to verify.

Can someone add Android to the OS labels? Per https://crbug.com/chromium/1149125#c4, I've verified on Chrome for Android. There's no extensions there, so would require significant user interaction to perform from the web, but still possible with sufficient convincing by attacker (same goes for web-based attacks on desktop platforms).

### [Deleted User] (2020-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-02)

Requesting merge to stable M87 because latest trunk commit (832563) appears to be after stable branch point (812852).

Requesting merge to beta M87 because latest trunk commit (832563) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-02)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2020-12-04)

To add a layer of defense against other bugs caused by spurious RFHI::EnableMojoJsBindings() calls, Navigator::CheckWebUIRendererDoesNotDisplayNormalURL() [1] could be updated to check if the RFH has ever enabled MojoJS for its RF. It already checks if sensitive bindings were enabled via other methods and the name fits, so it seems like a good place to check if sensitive bindings were enabled via RFHI::EnableMojoJsBindings().

A patch is attached (runs on my local build but haven't run tests against it). After applying patch, navigating from chrome://process-internals/ to another URL will result in a blocked commit if RFHI::EnableMojoJsBindings() has ever been called. That may not be ideal behavior (perhaps a RFH swap is a better user experience), but at least is safer and would have prevented the originally reported issue.

Another option is to only call GetFrameBindingsControl()->EnableMojoJsBindings() within RFHI::EnableMojoJsBindings() if the DCHECK conditions pass (i.e. change DCHECK into a normal conditional statement). Yet another option is to change the DCHECK into a CHECK, but that's even more disruptive to the user experience than a blocked commit.

[1] https://source.chromium.org/chromium/chromium/src/+/master:content/browser/renderer_host/navigator.cc;l=103;drc=ad1bf93c9867095aaef3f2e47e1435ac14c3bb19

### al...@alesandroortiz.com (2020-12-07)

Verified as fixed in Canary 89.0.4347.0 on Windows and Android.

### cr...@chromium.org (2020-12-08)

Thanks for all the helpful comments!  (Also CC'ing alexmos@, who was dropped earlier but is back from OOO.)

https://crbug.com/chromium/1149125#c24: Adding Android label accordingly; this will be relevant for merge review.

https://crbug.com/chromium/1149125#c28: Thanks for the suggestion!  This does seem to be a case where CheckWebUIRendererDoesNotDisplayNormalURL() might have helped.  We'll take a closer look.

### ad...@chromium.org (2020-12-09)

Looks to me like this would need a merge to M88 as well as M87.

### [Deleted User] (2020-12-09)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-12-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-10)

Congratulations! The VRP panel has decided to award $7,500 for this bug.

### ad...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### sr...@google.com (2020-12-10)

adetaylor@ pls review and approve merges for M87/M88

### ad...@chromium.org (2020-12-10)

dcheng@ any thoughts on whether it's wise to merge to M87/M88? (in theory we need a reply to https://crbug.com/chromium/1149125#c32 but the main thing is just to comment on any stability risks)

### dc...@chromium.org (2020-12-10)

This is a very low risk merge. It makes ProcessInternalsUI consistent with ConversionInternalsUI, so it should be fine for both 87 and 88.

### ad...@chromium.org (2020-12-10)

OK, approving merge to M88, branch 4324.

I'll do a round of M87 approvals later.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6039f2bbf74d6c9f9609390099068be3df90c6d2

commit 6039f2bbf74d6c9f9609390099068be3df90c6d2
Author: Daniel Cheng <dcheng@chromium.org>
Date: Thu Dec 10 22:01:06 2020

[WebUI] Use WebUIController::RenderFrameCreated() to request MojoJS.

ConversionInternalsUI and ProcessInternalsUI don't need to be
WebContentsObservers at all, since WebUIController already provides a
RenderFrameCreated() override that is scoped WebUI-specific
RenderFrameHosts.

(cherry picked from commit 0d360f554b501d57b72d4a2ccb744645e662e200)

Bug: 1148682, 1149125
Change-Id: Iebef544d7fb7c8938d273c84279ce7e8b19f90a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2566889
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#832563}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2585586
Commit-Queue: Nasko Oskov <nasko@chromium.org>
Auto-Submit: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#796}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/6039f2bbf74d6c9f9609390099068be3df90c6d2/content/browser/process_internals/process_internals_ui.cc
[modify] https://crrev.com/6039f2bbf74d6c9f9609390099068be3df90c6d2/content/browser/conversions/conversion_internals_browsertest.cc
[modify] https://crrev.com/6039f2bbf74d6c9f9609390099068be3df90c6d2/content/browser/process_internals/process_internals_ui.h
[modify] https://crrev.com/6039f2bbf74d6c9f9609390099068be3df90c6d2/content/browser/conversions/conversion_internals_ui.h
[modify] https://crrev.com/6039f2bbf74d6c9f9609390099068be3df90c6d2/content/browser/process_internals/process_internals_browsertest.cc


### ad...@google.com (2020-12-11)

Approving merge to M87, branch 4280.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0778396b74e05120da7d55fd841d250e1892ce4d

commit 0778396b74e05120da7d55fd841d250e1892ce4d
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Dec 15 11:11:53 2020

[M87][WebUI] Use WebUIController::RenderFrameCreated() to request MojoJS.

ConversionInternalsUI and ProcessInternalsUI don't need to be
WebContentsObservers at all, since WebUIController already provides a
RenderFrameCreated() override that is scoped WebUI-specific
RenderFrameHosts.

(cherry picked from commit 0d360f554b501d57b72d4a2ccb744645e662e200)

Bug: 1148682, 1149125
Change-Id: Iebef544d7fb7c8938d273c84279ce7e8b19f90a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2566889
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#832563}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587708
Auto-Submit: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1878}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/0778396b74e05120da7d55fd841d250e1892ce4d/content/browser/process_internals/process_internals_ui.cc
[modify] https://crrev.com/0778396b74e05120da7d55fd841d250e1892ce4d/content/browser/conversions/conversion_internals_browsertest.cc
[modify] https://crrev.com/0778396b74e05120da7d55fd841d250e1892ce4d/content/browser/process_internals/process_internals_ui.h
[modify] https://crrev.com/0778396b74e05120da7d55fd841d250e1892ce4d/content/browser/conversions/conversion_internals_ui.h
[modify] https://crrev.com/0778396b74e05120da7d55fd841d250e1892ce4d/content/browser/process_internals/process_internals_browsertest.cc


### ad...@google.com (2021-01-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### ke...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b2ba2b2c71c069a8a2a0cfead1c51d0b149f0bcc

commit b2ba2b2c71c069a8a2a0cfead1c51d0b149f0bcc
Author: Daniel Cheng <dcheng@chromium.org>
Date: Sat Jan 09 19:58:54 2021

[M86-LTS][WebUI] Use WebUIController::RenderFrameCreated() to request MojoJS.

ConversionInternalsUI and ProcessInternalsUI don't need to be
WebContentsObservers at all, since WebUIController already provides a
RenderFrameCreated() override that is scoped WebUI-specific
RenderFrameHosts.

(cherry picked from commit 0d360f554b501d57b72d4a2ccb744645e662e200)

(cherry picked from commit 0778396b74e05120da7d55fd841d250e1892ce4d)

Bug: 1148682, 1149125
Change-Id: Iebef544d7fb7c8938d273c84279ce7e8b19f90a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2566889
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#832563}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587708
Auto-Submit: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#1878}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617107
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1503}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/b2ba2b2c71c069a8a2a0cfead1c51d0b149f0bcc/content/browser/process_internals/process_internals_ui.cc
[modify] https://crrev.com/b2ba2b2c71c069a8a2a0cfead1c51d0b149f0bcc/content/browser/conversions/conversion_internals_browsertest.cc
[modify] https://crrev.com/b2ba2b2c71c069a8a2a0cfead1c51d0b149f0bcc/content/browser/process_internals/process_internals_ui.h
[modify] https://crrev.com/b2ba2b2c71c069a8a2a0cfead1c51d0b149f0bcc/content/browser/conversions/conversion_internals_ui.h
[modify] https://crrev.com/b2ba2b2c71c069a8a2a0cfead1c51d0b149f0bcc/content/browser/process_internals/process_internals_browsertest.cc


### [Deleted User] (2021-01-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2021-07-01)

[Empty comment from Monorail migration]

### cr...@chromium.org (2021-07-02)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1149125?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>WebUI]
[Monorail blocked-on: crbug.com/chromium/1225704, crbug.com/chromium/1225929]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053875)*
