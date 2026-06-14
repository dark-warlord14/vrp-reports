# Security: Android selection magnifier persists after navigation, can obscure/spoof browser UI or page content

| Field | Value |
|-------|-------|
| **Issue ID** | [384033062](https://issues.chromium.org/issues/384033062) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Selection |
| **Platforms** | Android |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ya...@google.com |
| **Created** | 2024-12-14 |
| **Bounty** | $5,000.00 |

## Description

## SUMMARY

The Android text selection magnifier remains on screen with attacker-controlled content after navigating away from attacker page. This can result in browser UI or another site's content being obscured or spoofed.

It's a detailed report with proposed patch, but likely low/medium severity at best, so please enjoy your holiday breaks.

## VULNERABILITY DETAILS

The Android text selection magnifier is a rectangular box that shows the page content around a selection or insertion cursor/caret. The magnifier is shown when a user taps and holds a text handle. Text handles are shown when a user selects text in page or input field, or when there is an insertion caret in input fields or other content-editable elements.

When navigating to another page, Chromium will close an open magnifier in these cases:

- When a page load starts (but only after commit 3c58f9355 in October 2024, see Additional Context section)
- When a page load ends (if `TouchSelectionController` (TSC) hasn't changed, i.e. in most same-site navigations)
- When user lifts finger from text handle before page load ends

However, the magnifier will remain open with content from the previous page if:

- Page load starts, then user opens magnifier, then page load ends while magnifier is open. However, this only occurs if a new `TouchSelectionController` instance is created on page load start, which reliably occurs in cross-site navigations (see Root Cause section).

When the page load ends, the magnifier content stops being updated. The content will be the last content rendered on the previous page, which is attacker controlled. The magnifier will render over any page content or most browser UI, including the address bar and permission prompts.

Therefore, an attacker can either obscure or spoof browser UI or another page's content. For example, an attacker can show text over the address bar, show text/images or obscure buttons in permission prompts, or show text/images over another site's page.

The magnifier will remain shown until the user switches away from the Chromium browser to another app or turns off their screen. Opening a new magnifier does NOT dismiss the existing magnifier, so this can be repeated multiple times to obscure/spoof a larger area.

## VERSION

Chrome Version: 131.0.6778.105 Stable, 133.0.6889.0 Canary

Repros down to 69.0.3474.0 with `#enable-site-per-process` flag, 78.0.3877.0 without flags.

Operating System: Android 14, Android 12

## BISECT

There's a couple of bisects. These bisects were made with the PoC that opens magnifier before page load starts (`android-magnifier-minimal-no-delay.html`).

1. Without any overridden flags: <https://crrev.com/ab7700c387f9167d763484cfa659ef7931103890>
   
   `Enable ProactivelySwapBrowsingInstance in fieldtrial_testing_config` (August 2019)
   
   If there are other attacker-controllable conditions that force a RWHVA/TSC swap, then it may repro earlier without flags.
2. With `#enable-site-per-process` enabled: <https://crrev.com/2d7e42f08f486ca3d5e28176f5ea0e3fb5bde0e8> (June 2018)
   
   This commit added the Magnifier logic for Android.

## ADDITIONAL CONTEXT

Prior to commit 3c58f9355 [1] (October 2024), the magnifier will also remain open if:

- User opens magnifier, then page load starts, then page load ends while magnifier is open. Only if a new `TouchSelectionController` instance is created on page load start.

PoC and video are also provided for before commit 3c58f9355, see `android-magnifier-minimal-no-delay.html`. I verified the older behavior via bisect. Also verified separately by commenting out `ClearSelection()` call from `onPageLoadStarted()` in ToT local build.

After the commit, the `onPageLoadStarted()` [2] observer closes the magnifier by calling `SelectionPopupController::ClearSelection()` [3] when a navigation is started. This is why after the commit a user must open the magnifier after the navigation starts. Before the commit, there is no `ClearSelection()` call on page load start.

[1] <https://crrev.com/3c58f935519ca251c7ab32a423b66bd055c957ad> `[dnt] Back gesture clears text selection` Landed in 131.0.6766.0 on October 8th, and merged into 131.0.6778.39 Stable.

[2] `onPageLoadStarted()` <https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/ChromeActionModeHandler.java;l=102;drc=a0108592277483168bcedfd90b182a8b8ca5c5de>

[3] `ClearSelection()` <https://source.chromium.org/chromium/chromium/src/+/main:content/public/android/java/src/org/chromium/content/browser/selection/SelectionPopupControllerImpl.java;l=1701;drc=616d60fca655937c2b730db94fd32d37ddff3bb5>

## REPRODUCTION CASE

Minimal PoCs don't require any setup. Realistic PoCs use a signal server which requires some setup.

### Minimal PoC

This PoC is for current versions, after commit 3c58f9355. The magnifier must be opened after the navigation starts but before the nav finishes.

1. Navigate to <https://alesandroortiz.com/security/chromium/android-magnifier-minimal.html>
2. Tap an input field once, then touch and hold the text handle, then wait a few seconds for slow navigation to finish.

Observed:

- For top input field: Magnifier remains open over address bar. Address bar is partially obscured by magnifier.
- For center input field: Magnifier remains open over next page. The next page's content is partially obscured by magnifier.

Expected: Magnifier is dismissed when user stops holding text handle or when next page finishes loading.

### Minimal PoC, before commit 3c58f9355

This PoC works only before commit 3c58f9355 (r1365650). The magnifier can be opened before the navigation starts, so attack is easier to setup and perform.

1. Navigate to <https://alesandroortiz.com/security/chromium/android-magnifier-minimal-no-delay.html>
2. Tap an input field once, then touch and move the text handle, then wait a few moments for navigation to occur.

Observed/Expected: Same as previous Minimal PoC.

### Setup for self-hosting realistic PoCs:

The realistic PoCs use a signal server to avoid longer-than-needed navigation delay after magnifier is opened. For best results, the signal server should use HTTPS.

Signal server requires attached `signal-server.js` + `permission.html` + `spoof.html`

(If initial page is HTTPS, then signal server also requires HTTPS to avoid fetch being blocked due to mixed content. For permission prompt PoC, signal server must be on HTTPS due to permissions API requiring secure context.)

Important: The initial page and signal server MUST be on different sites for reliable repro, due to TSC swap requirement. Different ports on same hostname work fine for this purpose.

Setup HTTPS for signal server:

1. Generate cert (self-signed: `openssl req -x509 -nodes -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365`), then update `signal-server.js` to use the key pair in `https.createServer()` and disable the `http.createServer()` call.

Before running PoCs:

1. Run signal server. If using self-signed/untrusted cert, visit `https://signal-server-host:port/` once to accept unsafe connection warning.
2. Update `SIGNAL_SERVER` variable in initiator pages to reference your signal server (instead of the `https://aogarantiza.com:1337` signal server, which won't work for you)
3. Host initiator page on different site than signal server (e.g. using `npx http-server` locally; can be on HTTP)

### Address bar spoof PoC

Note: Ensure signal server is running and is on a different site than initiator page.

1. Navigate to initiator page: `android-magnifier-omnibox.html`
2. Tap or slide finger anywhere.
3. Slide finger as instructed by page.

Observed: Magnifier remains open over address bar. Address bar is partially obscured by magnifier.

Expected: Magnifier is dismissed when user stops holding text handle or when next page finishes loading.

### Permission prompt obscured button PoC

Note: Signal server must be on HTTPS. Ensure signal server is running and is on a different site than initiator page.

1. Navigate to intiator page: `android-magnifier-permission.html`
2. Tap or slide finger anywhere.
3. Slide finger as instructed by page.
4. Tap anywhere when instructed by page to open permission prompt.

Observed: Magnifier remains open over permission prompt. Permission prompt is partially obscured by magnifier.

Expected: Same as previous PoC.

## ROOT CAUSE

Observations below based on logs.

In cases where the `RenderWidgetHostViewAndroid` (RWHVA) [1] and `TouchSelectionController` (TSC) [2] instances stay alive across navigations, the magnifier is closed as expected when navigation finishes. When new instances of RWHVA and TSC are created, the magnifier remains open after navigation finishes.

I've observed that RWHVA and TSC are swapped for all cross-site navigations, and for some same-site navigations. Therefore, a cross-site navigation is an easy way to reliably reach the trigger conditions.

When a navigation commits, the renderer calls `LayerTreeHostImpl::GenerateCompositorFrame()` [5] which sends `RenderFrameMetadata` (RFM) to the browser. The RFM contains selection data.

The RFM selection data is calculated by `LayerTreeImpl::GetViewportSelection()` [3] (called by `LayerTreeHostImpl::MakeRenderFrameMetadata()` [4]). When a page loads, the RFM will indicate an empty selection (i.e. no selection) even when there was a selection in the previous page. This is expected behavior since the new page does not have a selection.

The RFM with selection data goes through this code path:

- RFM created: `LayerTreeHostImpl::GenerateCompositorFrame()` [5]
- `RenderFrameMetadataObserverImpl::OnRenderFrameSubmission()` [6] (renderer)
- `RenderFrameMetadataProviderImpl::OnRenderFrameMetadataChanged()` [7] (browser)
- `RenderWidgetHostViewAndroid::OnRenderFrameMetadataChangedBeforeActivation()` [8]
- `RenderWidgetHostViewAndroid::UpdateTouchSelectionController()` [9]
- `TouchSelectionControllerClientManagerAndroid::UpdateClientSelectionBounds()` [10]
- `TouchSelectionController::OnSelectionBoundsChanged()` [11]

There is a key difference in behavior in `TSC::OnSelectionBoundsChanged()` between the repro vs. non-repro scenarios.

- Repro (unexpected): For a newly-created TSC, the TSC's internal state will be initialized to empty/no selection. If the RFM also has an empty selection, `TSC::OnSelectionBoundsChanged()` will return early due to `start == start_ && end_ == end` being true.
- Non-repro (expected): The existing TSC will have selection data from the previous page. Since the selection has changed compared to the selection previously known to the TSC, the rest of the `OnSelectionBoundsChanged()` logic will run.

In non-repro (expected) cases, the code path continues from `OnSelectionBoundsChanged()`...

- `TouchSelectionController::OnSelectionBoundsChanged()` [11] updates the internal selection state
- `TouchSelectionController::HideHandles()` (`start/end.HasHandle()` are false)
- `TouchSelectionController::DeactivateInsertion()`
- `TouchHandle::SetEnabled(false)`
- `TouchHandle::EndDrag()`
- `TouchSelectionController::OnDragEnd()`
- `RenderWidgetHostViewAndroid::OnSelectionEvent(INSERTION_HANDLE_DRAG_STOPPED)`
- `SelectionPopupController::OnSelectionEvent()` (C++ -> Java) with `SelectionEventType.INSERTION_HANDLE_DRAG_STOPPED`
- `MagnifierAnimator::handleDragStopped()`
- `MagnifierWrapper::dismiss()` / `MagnifierSurfaceControl::dismiss()` which finally dismisses the Android magnifier.

The calls after `TSC::OnSelectionBoundsChanged()` are easier to follow, so please use the Code Search link [11] to find the functions mentioned above.

Given the above, the magnifier isn't cleared in the repro cases because:

- RWHVA and TSC change on navigation start, and are initialized as having no selection. TSC only dismisses the Magnifier if it knew of a previous selection and the new state is no selection.
- There are no other calls to `MagnifierWrapper::dismiss()`

[1] `RenderWidgetHostViewAndroid` <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_view_android.cc;drc=0f0c2e5c34d04fb5875b26061fc349152787dd2e>

[2] `TouchSelectionController` <https://source.chromium.org/chromium/chromium/src/+/main:ui/touch_selection/touch_selection_controller.cc;drc=5f8dea3b512f8d1769e0d5c83a1721beedd0b458>

[3] `LayerTreeImpl::GetViewportSelection()` <https://source.chromium.org/chromium/chromium/src/+/main:cc/trees/layer_tree_impl.cc;l=2878;drc=616d60fca655937c2b730db94fd32d37ddff3bb5>

[4] `LayerTreeHostImpl::MakeRenderFrameMetadata()` <https://source.chromium.org/chromium/chromium/src/+/main:cc/trees/layer_tree_host_impl.cc;l=2591;drc=616d60fca655937c2b730db94fd32d37ddff3bb5>

[5] `LayerTreeHotImpl::GenerateCompositorFrame()` calls `OnRenderFrameSubmission()` <https://source.chromium.org/chromium/chromium/src/+/main:cc/trees/layer_tree_host_impl.cc;l=3059;drc=616d60fca655937c2b730db94fd32d37ddff3bb5>

[6] `RenderFrameMetadataObserverImpl::OnRenderFrameSubmission()` <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/widget/compositing/render_frame_metadata_observer_impl.cc;l=100;drc=616d60fca655937c2b730db94fd32d37ddff3bb5>

[7] `RenderFrameMetadataProviderImpl::OnRenderFrameMetadataChanged()` <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_metadata_provider_impl.cc;l=118;drc=54fec6df88aed90af1239ebbf49f5deced265e8d>

[8] `RenderWidgetHostViewAndroid::OnRenderFrameMetadataChangedBeforeActivation()` <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_view_android.cc;l=879;drc=616d60fca655937c2b730db94fd32d37ddff3bb5>

[9] `RenderWidgetHostViewAndroid::UpdateTouchSelectionController()` <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_view_android.cc;l=1936;drc=616d60fca655937c2b730db94fd32d37ddff3bb5>

[10] `TouchSelectionControllerClientManagerAndroid::UpdateClientSelectionBounds()` <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/input/touch_selection_controller_client_manager_android.cc;l=64;drc=616d60fca655937c2b730db94fd32d37ddff3bb5>

[11] `TouchSelectionController::OnSelectionBoundsChanged()` <https://source.chromium.org/chromium/chromium/src/+/main:ui/touch_selection/touch_selection_controller.cc;l=77;drc=616d60fca655937c2b730db94fd32d37ddff3bb5>

## PATCH

The proposed patch to fix the issue adds a `onDidFinishNavigationInPrimaryMainFrame()` observer in `ChromeActionModeHandler` that makes a call to `SelectionPopupController::ClearSelection()`. This follows the same pattern used to clear the selection on page load start via `onPageLoadStarted()` observer.

The patch also adds a `MagnifierAnimator::handleDragStopped()` call within `SelectionPopupController::ClearSelection()`.

I scoped the fix to only Java code because existing code paths that lead to `MagnifierAnimator::handleDragStopped()` are short-circuited in multiple places in the C++ code, as shown in Root Cause section. Updating the C++ code path to make the Java call may cause unexpected behavior changes elsewhere, since the code path involves many layers and is shared with other scenarios, not just the page load finished scenario.

As far as I can tell, there are no unexpected behavior changes with this patch.

Behavior after applying patch is shown in videos named `fixed-*`.

## Credit Information

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- android-magnifier-minimal.html (text/html, 1.4 KB)
- android-magnifier-minimal-no-delay.html (text/html, 1.7 KB)
- android-magnifier-omnibox.html (text/html, 4.9 KB)
- android-magnifier-permission.html (text/html, 4.8 KB)
- slow.php (application/x-httpd-php, 121 B)
- signal-server.js (text/javascript, 2.9 KB)
- permission.html (text/html, 493 B)
- [spoof.html](attachments/spoof.html) (text/html, 734 B)
- [poc-minimal-center.mp4](attachments/poc-minimal-center.mp4) (video/mp4, 1.1 MB)
- [poc-minimal-top.mp4](attachments/poc-minimal-top.mp4) (video/mp4, 1.5 MB)
- [poc-permission.mp4](attachments/poc-permission.mp4) (video/mp4, 1.7 MB)
- [fixed-omnibar.mp4](attachments/fixed-omnibar.mp4) (video/mp4, 822.0 KB)
- [fixed-minimal-no-delay.mp4](attachments/fixed-minimal-no-delay.mp4) (video/mp4, 387.8 KB)
- [fixed-permission.mp4](attachments/fixed-permission.mp4) (video/mp4, 441.6 KB)
- [poc-minimal-no-delay-center.mp4](attachments/poc-minimal-no-delay-center.mp4) (video/mp4, 1.1 MB)
- [fixed-minimal.mp4](attachments/fixed-minimal.mp4) (video/mp4, 473.2 KB)
- [proposed-fix.patch](attachments/proposed-fix.patch) (text/x-diff, 2.3 KB)
- [poc-omnibox.mp4](attachments/poc-omnibox.mp4) (video/mp4, 2.5 MB)
- [poc-minimal-no-delay-top.mp4](attachments/poc-minimal-no-delay-top.mp4) (video/mp4, 1.1 MB)

## Timeline

### al...@alesandroortiz.com (2024-12-14)

Also want to note a user reported the persistent magnifier behavior as a functional bug in [issue 41490659](https://issues.chromium.org/issues/41490659) in January 2024.

I think I uploaded all relevant attachments, but please let me know if I missed any. The attachments aren't grouped together as I had uploaded them, so apologies for that. :/

I'll create CL for patch shortly.

### al...@alesandroortiz.com (2024-12-14)

CL: <https://crrev.com/c/6093444>

### al...@alesandroortiz.com (2024-12-15)

This should be Security\_Impact-Extended, since it repros down to M78 without flags.

### an...@chromium.org (2024-12-16)

[security shepherd]: Thank you for the report. [yaris@google.com](mailto:yaris@google.com), I see you've worked with this component, especially with Android text selection. Would you be able to look into this? There's a proposed CL to fix the issue. The main gist is that the Android text selection is spoofing the UI and can carry over different tabs.

### pe...@google.com (2024-12-16)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ji...@google.com (2025-01-07)

Adding boliu@ who worked on SurfaceControl magnifier

### bo...@chromium.org (2025-01-08)

Wow, thanks for the super detailed investigation and description. Can't say I read every word and file, but I think I got the gist.

I don't evaluate whether an issue has security impact or not, but imo it's a bit of a stretch for this one. This requires user to actively select text. So attacker doesn't control the position (and content) of the magnifier, and attacker can't control the size of the magnifier so it can't cover the entire url bar. So user not likely to be confused?

Definitely a functional bug though.

### al...@alesandroortiz.com (2025-01-08)

I agree this has very limited impacts, but still seems like a security issue. For reference, autofill prompts obscuring other browser UI or address bar have been considered security issues. Autofill prompts have similar limited size as magnifier.

The attacker does control the content being magnified, although yes the area obscured/spoofed is limited. While less practical, I've confirmed multiple magnifiers can remain open at once, so repeating the attack could cover larger areas. Although this is not necessary in the scenarios shown in the report.

For the address bar scenario, as shown in the video, it's most useful in cases when attacker is spoofing a short URL (such as google.com) and the area to the right of the address bar is empty. That allows for single magnifier to cover all the text in the address bar (e.g. from `attacker.com` to `google.com` since both strings are narrower than magnifier width, so real URL is obscured and spoofed URL fits within magnifier).

Other UI such as the "block" button is also narrow enough to cover with a single magnifier.

### ap...@google.com (2025-01-10)

Project: chromium/src  

Branch: main  

Author: Alesandro Ortiz <[alesandro@alesandroortiz.com](mailto:alesandro@alesandroortiz.com)>  

Link:      <https://chromium-review.googlesource.com/6093444>

Android: Dismiss text magnifier on RWHVA change

---


Expand for full commit details
```
Android: Dismiss text magnifier on RWHVA change 
 
Due to stale states and early returns, `handleDragStopped()` was not 
called after certain cross-process navigations. This meant text 
magnifier did not always dismiss when renderer process changed. 
See bug for more details. 
 
To fix this, we call `handleDragStopped()` when 
`SPC::UpdateRenderProcessConnection()` is called to dismiss the text 
magnifier. This ensures dismissal after renderer process changes. 
 
Fixed: 384033062 
Change-Id: I158529d40dba86f21b275c7031531797498635dc 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6093444 
Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org> 
Commit-Queue: Alesandro Ortiz <alesandro@alesandroortiz.com> 
Reviewed-by: Bo Liu <boliu@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1405064}

```

---

Files:

- M `content/browser/android/selection/selection_popup_controller.cc`
- M `content/public/android/java/src/org/chromium/content/browser/selection/SelectionPopupControllerImpl.java`

---

Hash: 9cf22ff04513c044411467ef06340e3354ccb468  

Date:  Fri Jan 10 15:46:09 2025


---

### al...@alesandroortiz.com (2025-01-12)

Thanks for reviewing CL, boliu@, jinsukkim@, and yaris@!

Verified as fixed on 134.0.6951.0 Canary.

### sp...@google.com (2025-01-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
high-quality, comprehensive report of moderate impact security UI issue, specifically the permissions spoof / bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-29)

Congratulations Alesandro! Thank you for your efforts on this very verbose report and reporting this issue and the various ways it manifests to us -- nice work!

### al...@alesandroortiz.com (2025-02-04)

Thanks for the reward!

Couple of questions regarding bonuses, which don't seem to be part of the reward:

1. I provided a few bisects: one without flags, one with flags, and a parallel bisect for the easier repro (commit 3c58f9355). Did these not qualify for the bisect bonus for some reason?
2. I also provided proposed patch via Gerrit and landed the CL. The merged CL code was slightly different based on CL feedback, but the general approach was the same (call `getMagnifierAnimator().handleDragStopped()` when RWHVA was swapped). The approach was based on the analysis I provided in report. Did this not qualify for the patch bonus for some reason?

If the bonuses were part of the reward, then a breakdown would be appreciated. :)

### ch...@google.com (2025-04-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/384033062)*
