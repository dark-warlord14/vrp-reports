# use after free in  sharing_hub::ScreenshotCapturedBubbleController::Capture

| Field | Value |
|-------|-------|
| **Issue ID** | [40056871](https://issues.chromium.org/issues/40056871) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | km...@chromium.org |
| **Created** | 2021-08-13 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36

Steps to reproduce the problem:
1.fllow my step in video.
2.you shoul enable two flags  #sharing-desktop-screenshots and  #sharing-hub-desktop-omnibox 
3.

What is the expected behavior?
normal capture screenshots.

What went wrong?
heap use after free 

Did this work before? N/A 

Chrome version: 92.0.4515.131  Channel: stable
OS Version: 10.0

## Attachments

- [uaf.txt](attachments/uaf.txt) (text/plain, 22.5 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 10.6 MB)
- [patch.PNG](attachments/patch.PNG) (image/png, 40.9 KB)
- [patch.PNG](attachments/patch.PNG) (image/png, 43.7 KB)

## Timeline

### wx...@gmail.com (2021-08-13)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-08-13)

my chromium version is 587fd797d9e8e88a58f2ba01790e9619cca481a1

you should use the latest version. 

### [Deleted User] (2021-08-13)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-08-13)

this is my suggest  patch, after this patch  it still crash but just shows that :FATAL:weak_ptr.h(255)] Check failed: ref_.IsValid().


### wx...@gmail.com (2021-08-13)

 I  also find some similar bug pattern and the reason is the same,  I will try to submit all but no poc now.

### wx...@gmail.com (2021-08-13)

you can use this patch, and this will not crash any more.

### wx...@gmail.com (2021-08-13)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-08-13)

The root reason is that browser's view could be deleted before the callback execute.

### wf...@chromium.org (2021-08-13)

Thanks for your report. I didn't even know about this feature :) kmilka@chromium.org can you take a look?

THis is behind a flag so it's security impact none. Normally it would be critical for a browser UAF but user gesture mitigates this to High.

[Monorail components: UI>Browser>Sharing]

### km...@chromium.org (2021-08-13)

Thanks for the report. This is addressed by the fix for https://crbug.com/chromium/1239201.  Going to mark as duplicate, but please re-open or file a new bug if you see this or any other issue!

### wx...@gmail.com (2021-08-18)

hello, I think https://crbug.com/chromium/1239201 is different with this, from the https://chromium-review.googlesource.com/c/chromium/src/+/3092935, it just prevent the crash that you close the tab when the tab is  being captured.

### wx...@gmail.com (2021-08-18)

When I patch the code(https://chromium-review.googlesource.com/c/chromium/src/+/3092935), the crash in this bug still exist. 

### km...@chromium.org (2021-08-18)

I can take another look here, and implement the suggested fix

### sk...@chromium.org (2021-08-19)

thanks  wxhusst for the report and kmilka for cc'ing/granting access to this bug, +1 that this wouldn't be fixed by 1239201 and a local change makes sense, though code around the screenshot code will be checked too (also, any of our other bubbles launched on similar callbacks?)

### wx...@gmail.com (2021-08-19)

I don't find any similar callbacks in screenshot code, but I find a similar bug as 1239201 in screenshot code. I have submit it as https://crbug.com/chromium/1241024

### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4ea1e7cd1fb65adbf8b4421e24b6832fc8e7d992

commit 4ea1e7cd1fb65adbf8b4421e24b6832fc8e7d992
Author: Kyle Milka <kmilka@chromium.org>
Date: Mon Aug 23 20:43:46 2021

[DesktopScreenshots] Fix crash when window closed mid-capture

Pass the WebContents rather than the Browser to the
screenshot_flow callback, as the Browser may be destroyed
before capture is complete.

Bug: 1239516
Change-Id: Icfd1f5064fab3f4ee0894698dd9b4198e662e4b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3107742
Reviewed-by: Travis Skare <skare@chromium.org>
Commit-Queue: Kyle Milka <kmilka@chromium.org>
Cr-Commit-Position: refs/heads/main@{#914511}

[modify] https://crrev.com/4ea1e7cd1fb65adbf8b4421e24b6832fc8e7d992/chrome/browser/ui/sharing_hub/screenshot/screenshot_captured_bubble_controller.cc


### km...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-08)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Nice work! 
Also, for future reference and to be eligible for patch bonuses in the future, please use submit your patch suggestions via Gerrit https://chromium-review.googlesource.com/ (See: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/commit_checklist.md#13_Upload-the-CL-to-Gerrit) or submit a patch file rather than a png for consideration. :) 

### wx...@gmail.com (2021-09-08)

[Comment Deleted]

### wx...@gmail.com (2021-09-09)

[Comment Deleted]

### am...@chromium.org (2021-09-09)

Oh apologies that you did that. I meant for future submissions of patches for your next bug report(s). Since this one is already patched on our side we didn't need it this time around, but in the future we'd like to be able to better leverage your patches and also provide a patch bonus. Apologies that I wasn't clearer!

### wx...@gmail.com (2021-09-09)

It is ok, still waiting for you in next bug.

### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2021-12-08)

Original reporter deleted the video, and repro steps say "[follow] my step in video."

Can reporter or someone else share repro steps or restore the video?

### is...@google.com (2021-12-08)

This issue was migrated from crbug.com/chromium/1239516?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1239201]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056871)*
