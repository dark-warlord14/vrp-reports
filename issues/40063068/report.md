# Security: Document PiP can spoof top-level page origin, show attacker content in PiP window, open PiP windows from iframes

| Field | Value |
|-------|-------|
| **Issue ID** | [40063068](https://issues.chromium.org/issues/40063068) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-02-14 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

Based on <https://crbug.com/chromium/1413813> (reported by NDevTK), Document PiP from a subframe will show the top-page origin. This report expands on that crbug.

A regular renderer requires two user interactions to show arbitrary content in the PiP window (this scenario will be fixed by CL [1]).

However, a compromised renderer can, with a single user interaction (click or keypress):

1. Open Document PiPs from iframes.
2. Show arbitrary content in the new window.

CL [1] does not appear to mitigate the behaviors above.

Document PiP is currently in origin trial and can also be enabled via flag.

[1] <https://chromium-review.googlesource.com/c/chromium/src/+/4242019>

ADDITIONAL CONTEXT  

Note: The PoC also uses another issue (to be filed) to resize and move window.

As far as NDevTK and I can tell, the document PiP feature is intended to only be used from top-level pages, therefore the logic also assumes that the top-level page is always the opener. This is reflected in PictureInPictureBrowserFrameView::GetURL() and other methods in that class that use WebContents (tabs) instead of a specific frame's RFH as data sources.

The address bar for the document PiP window is set using omnibox logic: <https://source.chromium.org/chromium/chromium/src/+/main:components/omnibox/browser/location_bar_model_impl.cc;l=140;drc=c13d0b19698dacedfa4d2d71d8c4e18be0b2ee01>

delegate\_ in this case refers to PictureInPictureBrowserFrameView.

PictureInPictureBrowserFrameView::GetURL() provides the URL shown in the address bar:  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc;l=559;drc=38f3aa1a1ac40adc24cb13d6bac2e9eb183f09f5>

The active WebContents within PiP logic is set here:  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc;l=105;drc=c13d0b19698dacedfa4d2d71d8c4e18be0b2ee01>

Which comes from params->source\_contents when calling browser\_navigator's Navigate(): <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=875;drc=c13d0b19698dacedfa4d2d71d8c4e18be0b2ee01>

Which comes from the normal open popup code path below...  

browser\_tabstrip's AddWebContents(): <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_tabstrip.cc;l=87;drc=8ce391bed5ee336e59ccd87b8869760c30e2aad7>

browser's AddWebContents(): <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser.cc;l=1709;drc=8ce391bed5ee336e59ccd87b8869760c30e2aad7>

WebContentsImpl::CreateNewWindow(): <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=7664;drc=c13d0b19698dacedfa4d2d71d8c4e18be0b2ee01>

(and potentially WebContentsImpl::ShowCreatedWindow(): <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=4339;drc=c13d0b19698dacedfa4d2d71d8c4e18be0b2ee01> )

Some potential solutions:  

\* Browser-side enforcement to prevent PiP windows from being created by subframes, fencedframes, or anything that isn't the top-level page in a tab or regular window. Not sure if this is feasible or easy to implement.  

\* For the Document PiP window, use the URL from the WebContents or RFH shown in the Document PiP window (not the WebContents of the opener). If somehow an attacker is able to show their content in a PiP window, this ensures the address bar is shown correctly. This should be feasible (since regular popup windows do it already), and could be added as a defense-in-depth measure in addition to other solutions.

Based on my analysis, there is no other spoofing other than in the address bar (and associated controls, such as Page Info). Other UI and logic, including permissions UI and logic, is not spoofed since it uses other data sources for the URL and origin.

**VERSION**  

Chrome Version: 112.0.5589.0 local build based on commit 5fa7fe43cbd6a5e2f87e762ac1f872a114798fe5 from February 10th  

Operating System: Windows 10 Version 21H2 (Build 19044.2486)

**REPRODUCTION CASE**  

Setup:

1. Apply renderer.patch and rebuild Chromium to simulate compromised renderer.
2. Enable Document PiP flag: chrome://flags/#document-picture-in-picture-api  
   
   Note: There is a Origin Trial that can also be used instead of enabling the flag.

PoC:  

Prerequisites: Compromised/patched renderer + enabled Document PiP flag.

1. Navigate to <https://alesandroortiz.com/security/chromium/documentpip.html>
2. Click within iframe or press any key.

Observed: Document PiP window's address bar shows origin of top-level page of opener tab. Document PiP window shows content from different origin  

Expected: Document PiP window's address bar shows origin of page shown within the Document PiP window. Document PiP window does not show content from different origin.

**CREDIT INFORMATION**  

Reporter credit: NDevTK and Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [documentpip.html](attachments/documentpip.html) (text/plain, 368 B)
- [pip-frame.html](attachments/pip-frame.html) (text/plain, 1.6 KB)
- [renderer.patch](attachments/renderer.patch) (text/plain, 2.7 KB)
- [documentpip-origin-spoof.mp4](attachments/documentpip-origin-spoof.mp4) (video/mp4, 2.1 MB)

## Timeline

### al...@alesandroortiz.com (2023-02-14)

Please cc ndevtk@protonmail.com when possible.

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-02-14)

Also recommend restricting https://crbug.com/chromium/1413813 since it has security implications as detailed in this report.

### al...@alesandroortiz.com (2023-02-14)

Filed related https://crbug.com/chromium/1416380 re: moving and resizing windows.

### th...@chromium.org (2023-02-15)

[Empty comment from Monorail migration]

### li...@google.com (2023-02-15)

[Empty comment from Monorail migration]

### li...@google.com (2023-02-15)

I agree that adding some additional restrictions in the browser is worthwhile.  Since it requires a compromised renderer, leaving at p3.

### li...@google.com (2023-02-15)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-02-15)

I think this is a security issue per https://chromium.googlesource.com/chromium/src/+/master/docs/security/compromised-renderers.md#security_sensitive-ui_chrome-elements-e_g_omnibox normally priority is assigned based of the Security_Severity label.

### th...@chromium.org (2023-02-15)

^ This is correct. I haven't triaged this ticket yet, but will do so soon.

### th...@chromium.org (2023-02-15)

Setting the severity as medium since this allows spoofing the apparent address bar assuming a compromised renderer.

liberato@, could you help triage this issue as appropriate?

[Monorail components: Blink>Media>PictureInPicture]

### [Deleted User] (2023-02-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-02-15)

Forgot to mention -- I can reproduce this on Linux on M110.

### [Deleted User] (2023-02-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-02)

liberato: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-17)

liberato: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f4b889f5c7616ea7b1276421c01b1680a22bacd

commit 0f4b889f5c7616ea7b1276421c01b1680a22bacd
Author: Tommy Steimel <steimel@chromium.org>
Date: Mon Apr 10 23:47:55 2023

pip2: Add browser-side check that non-topmost frames can't open PiP

Only topmost frames are allowed to open document PiP windows. However,
we currently only check this in the renderer, so a comprimised renderer
could theoretically bypass that logic to open a PiP window. This CL
adds a check in the browser side to ensure that only topmost frames can
open document PiP windows.

Bug: 1416350
Change-Id: If3f9893a2ae0999ade1b39c1e25e8a2f60a04f76
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4408542
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1128406}

[modify] https://crrev.com/0f4b889f5c7616ea7b1276421c01b1680a22bacd/content/browser/renderer_host/render_frame_host_impl.cc


### st...@chromium.org (2023-04-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-20)

Congratulations, Alesandro! The VRP Panel has decided to award you $4,000 for this report. Thank you for your efforts and reporting this issue to us! 

### al...@alesandroortiz.com (2023-04-22)

Thanks for the reward on this issue, and for the reward to NDevTK on https://crbug.com/chromium/1413813!

CL looks good, although I don't have a recent build environment to properly verify fix with compromised renderer. Considering as fixed.

### am...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1416350?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063068)*
