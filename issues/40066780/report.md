# Security: Document PIP URL address spoofing using long about:blank URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40066780](https://issues.chromium.org/issues/40066780) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-07-03 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to spoof document PIP address by using a long about:blank URL containing URL fragment.

**VERSION**  

Chrome Version: 117.0.5868.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows 10 Version 22H2 (Build 19045.3086)

**REPRODUCTION CASE**

1. Go to pip-exploit.html.
2. Click on make payment.
3. Document PIP window spawned with the fake subdomain of paypal.com but the actual URL is "about:blank#very-super-duper-long-subdomain.paypal.com"

Tested on both stable and latest canary.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [pip-exploit.html](attachments/pip-exploit.html) (text/plain, 413 B)
- [Untitled_ Jul 3, 2023 10_57 PM.webm](attachments/Untitled_ Jul 3, 2023 10_57 PM.webm) (video/webm, 613.3 KB)
- [pip-exploit.html](attachments/pip-exploit.html) (text/plain, 486 B)
- [doc-pip-long-domain-spoof.webm](attachments/doc-pip-long-domain-spoof.webm) (video/webm, 500.1 KB)
- [betterspoof.html](attachments/betterspoof.html) (text/plain, 486 B)
- [betterspoof.png](attachments/betterspoof.png) (image/png, 32.0 KB)

## Timeline

### [Deleted User] (2023-07-03)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-07-03)

Website: https://cream-stellar-mole.glitch.me/pip-exploit.html

### ha...@gmail.com (2023-07-03)

Video of POC on latest canary

### dc...@chromium.org (2023-07-05)

This is a known issue and already being worked on.

### ha...@gmail.com (2023-07-10)

Whilst looking at the CL you put up for 1451592, dcheng@ I think you made whilst marking this bug duplicate. This bug does not involve triggering
the about:blank#blocked condition of your fix in https://chromium-review.googlesource.com/c/chromium/src/+/4624360/15/content/browser/renderer_host/render_frame_host_impl.cc#5613. But rather, by adding a really loooooong hash to an about:blank URL, the URL shown in the document PIP window will be able to be spoofed because the full URL is too long to be shown in the document PIP omnibox

### ha...@gmail.com (2023-07-10)

made a mistake whilst marking this bug duplicate*

### dc...@chromium.org (2023-07-13)

Hmm, OK, I'll throw this back in the triage queue then.

I am not sure what the security properties of the document picture-in-picture title are intended to be.

[Monorail components: Blink>Media>PictureInPicture]

### ha...@gmail.com (2023-07-13)

Currently, while inspecting the fix in another of my bug report, https://bugs.chromium.org/p/chromium/issues/detail?id=1451543, it should handle the test case but I think it is a good idea to leave it open and assign the same owner as well just in case

### dc...@chromium.org (2023-07-17)

I think this probably needs more input from UX and the document picture-in-picture team.

On Android, this opens up a new tab, and we trim the right side of the URL, so the origin is always visible.

Document PiP probably should be doing something similar (or just not showing the fragment at all, since that's what the Omnibox seems to do)

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

steimel: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2023-07-21)

steimel@ I wonder whether in https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc;l=593, turning *url = 

GetActiveWebContents()->GetLastCommittedURL(); 

to *url = GetActiveWebContents()->GetPrimaryMainFrame()
        ->GetLastCommittedOrigin().GetURL();

would solve both this problem and https://bugs.chromium.org/p/chromium/issues/detail?id=1451543.

Based on my understanding reading some browser test cases, GetPrimaryMainFrame would return a RFH which we can use GetLastCommittedOrigin() on to get the origin of the parent about:blank opener which we can use GetURL() on to reformat to a URL.

Patch here: https://chromium-review.googlesource.com/c/chromium/src/+/4705373

### [Deleted User] (2023-08-02)

steimel: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2023-08-07)

[Empty comment from Monorail migration]

### za...@google.com (2023-08-10)

steimel@chromium.org is there any update on this bug? Thanks. 

### ha...@gmail.com (2023-08-10)

Reporter here, a renderer patch has been landed to solve this issue. currently what's left is the browser patch which I submitted https://chromium-review.googlesource.com/c/chromium/src/+/4746980 and waiting for review.

### gi...@appspot.gserviceaccount.com (2023-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/444b0a82fb9f59dd2c3c05dfbccc56fc16c124d2

commit 444b0a82fb9f59dd2c3c05dfbccc56fc16c124d2
Author: Haxatron Sec <haxatron1@gmail.com>
Date: Fri Aug 11 21:03:01 2023

Disallow document pip for non-https / file resources. (browser-side)

browser-side followup of https://chromium-review.googlesource.com/c/chromium/src/+/4595397

Fixed: 1451543, 1460025
Change-Id: Id726c087b3d9994ed5a152b8e40f2094338840de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4746980
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1182779}

[modify] https://crrev.com/444b0a82fb9f59dd2c3c05dfbccc56fc16c124d2/content/browser/renderer_host/render_frame_host_impl.cc


### [Deleted User] (2023-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-12)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-08-15)

Updated pip-exploit.html to include the "Key in card details" part.

Demo: https://cream-stellar-mole.glitch.me/pip-exploit.html



### ha...@gmail.com (2023-09-05)

Please also see betterspoof.png what I think is a better spoofing via using long path to hide the about:blank start domain

DEMO: https://cream-stellar-mole.glitch.me/pip-exploit-better.html

### am...@chromium.org (2023-09-11)

It appears there is potentially more work to be done here, so I am reopening this issue; steimel@ can you PTAL? 

### ha...@gmail.com (2023-09-11)

Hello, reporter here. Both the renderer patch and browser patch in 1451543 should have resolved both bugs (verified in Canary). I'll let steimel@ verify this as well.

### ha...@gmail.com (2023-09-11)

Nvm, it looks like the renderer patch missed out on the about:blank case which will trigger the code mentioned in the browser patch, which causes the BAD_MESSAGE error to be reported by the browser code, which seems weird to me

### am...@chromium.org (2023-09-11)

[Comment Deleted]

### am...@chromium.org (2023-09-11)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-09-11)

I suspect this has to do with about:blank inheriting its parent

### ha...@gmail.com (2023-09-12)

For all intents and purposes, there aren't no longer any security implications after the browser patch as it handles both bugs. It's just that the browser patch will report a bad_message (as the renderer does not handle the about:blank url) to the renderer and cause instruct it to hang, which isn't nice but is not a security issue.



### ha...@gmail.com (2023-09-12)

Correction: there are no longer any security implications*

### [Deleted User] (2023-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/57b48499000515a4d8ebee662f35ec92c4ebe9f7

commit 57b48499000515a4d8ebee662f35ec92c4ebe9f7
Author: Haxatron Sec <haxatron1@gmail.com>
Date: Wed Sep 13 19:57:30 2023

Do not hang the renderer if attempting to open document pip window from about:blank URL

When a parent window opens an about:blank window, the new window will inherit its document URL from the parent window while the URL in the omnibox shows "about:blank". This means that the renderer code in  https://chromium-review.googlesource.com/c/chromium/src/+/4595397 fails to detect that the URL in the omnibox is about:blank and cause the code to reach  https://chromium-review.googlesource.com/c/chromium/src/+/4746980 without a compromised  renderer. This will cause the browser to report bad_message and instruct the renderer to hang,  which doesn't have any security implications but it isn't nice.

Unfortunately, AFAICT, there isn't a way to detect the exact URL (whether it is about:blank or not) in the omnibox from the renderer. Therefore, change the browser-side code such that attempting to open document pip windows from such URLs doesn't hang the renderer.

Fixed: 1460025

Change-Id: I355bcfbc8ba791f73645cdcc4e546186706e199f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4853095
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1196209}

[modify] https://crrev.com/57b48499000515a4d8ebee662f35ec92c4ebe9f7/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/57b48499000515a4d8ebee662f35ec92c4ebe9f7/chrome/browser/ui/browser_navigator.cc
[modify] https://crrev.com/57b48499000515a4d8ebee662f35ec92c4ebe9f7/chrome/browser/ui/browser_navigator_browsertest.cc


### ha...@gmail.com (2023-09-13)

Note to panel: see https://crbug.com/chromium/1460025#c3 and https://crbug.com/chromium/1460025#c22 for summary of the different spoofs for this report.

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations, Axel! The VRP Panel has decided to award you $3,000 for this report + $2,000 patch bonus. Thank you for all your work here -- even writing a browser test. Impressive and great work! 


### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

It looks like this fix shipped in the M119 Stable milestone release; updating with release label accordingly and tagging for release notes update
(cc: pgrace@)

### [Deleted User] (2023-12-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1460025?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1470187]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066780)*
