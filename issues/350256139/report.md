# Pip window can cover PWA Install Dialogue

| Field | Value |
|-------|-------|
| **Issue ID** | [350256139](https://issues.chromium.org/issues/350256139) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Windows |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | di...@google.com |
| **Created** | 2024-06-30 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

1. Set pip window in center
2. Click in page
3. Click PWA Install

# Problem Description

Serve file in server
Attaching video
Version 126.0.6478.127 (Official Build) (64-bit)
Version 128.0.6559.0 (Official Build) dev (64-bit)

# Summary

Pip window can cover PWA Install Dialogue

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [screen-capture (16).webm](attachments/screen-capture (16).webm) (video/webm, 438.7 KB)
- [manifest.json](attachments/manifest.json) (application/json, 947 B)
- [script.js](attachments/script.js) (text/javascript, 84 B)
- [sw.js](attachments/sw.js) (text/javascript, 142 B)
- [tt.html](attachments/tt.html) (text/html, 1.1 KB)

## Timeline

### ah...@google.com (2024-07-01)

[primary security shepherd]
Hello dmurph@chromium.org ,
I was not able to repro on my machine. Could you please check if this is on your end?

Setting severity to Medium 
Setting found in to the current extended stable
Provisionally setting OS to windows




### pe...@google.com (2024-07-02)

Setting milestone because of s2 severity.

### pe...@google.com (2024-07-02)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dm...@chromium.org (2024-07-08)

I was able to confirm this should happen. We don't close the install dialog if the window loses focus. We could close the install dialogs when the window loses focus.

I'm not sure if this is OK or not - there is a clear window over the install dialog.

@robko - what do you think?

### dm...@chromium.org (2024-07-08)

Dibya - how difficult do you think it would be to dismiss install dialogs when the page is no longer visible / on top? I thought we has something like this for the old dialog maybe?



### di...@chromium.org (2024-07-08)

I'll have to look into how the PIP window covers the page, let me try and reproduce this. If the visibility of the install dialog changes and it gets hidden, it should automatically close the dialog as per [this function](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/web_apps/web_app_install_dialog_delegate.cc;l=195-200;drc=6d0ae42edc5f1bca00bdbd076d469ee675d3306c;bpv=1;bpt=1).

### dm...@chromium.org (2024-07-08)

Ah - maybe we also need to check for OCCLUDED / check against VISIBLE.

### dm...@chromium.org (2024-07-08)

Hm - testing with https://pwa-pip.glitch.me/, I noticed that we still don't get a visibility change with the pip window over the content.

We'll have to figure out another way to abort this.

### di...@chromium.org (2024-07-09)

Hmmmm, there seems to be a `WebContentsObserver::MediaPictureInPictureChanged()` [1] which works a bit flakily to observe if a PiP window has opened for the site.

Based on my experiments with the PoC and pwa-pip.glitch.me, the PiP window opened in a corner of the desktop screen and not on the top of the dialog itself, so it doesn't really seem like a vulnerability unless someone has a smaller Chrome window and screen so that the PiP window shadows the dialog. Another way this could be a vulnerability is if the PiP window is somehow moved via a mouse to shadow the dialog.

The hard part here is figuring out the visibility of the dialog from the position of the PiP window with respect to the Chrome window, which I'm looking at.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/web_contents_observer.h;l=851?q=WebContentsObserver::MediaPictureInPictureChanged&ss=chromium%2Fchromium%2Fsrc>

### di...@chromium.org (2024-07-10)

CL out and LGTM'd: <https://chromium-review.googlesource.com/c/chromium/src/+/5689758>, waiting for one final review from an OWNER in Picture-in-picture land before landing.

### ap...@google.com (2024-07-12)

Project: chromium/src
Branch: main

commit 7d1fee1458cdd1adc7785856c2e4b5a4d933d74c
Author: Dibyajyoti Pal <dibyapal@google.com>
Date:   Fri Jul 12 02:24:42 2024

    [PWA] Create base PiP window testing class for web applications
    
    In c/b/ui/web_applications/, AppBrowserDocumentPictureInPictureBrowserTest
    has enough logic to be resuable across the web_applications/ area in
    various tests that verify workings of the web_applications/ system with
    respect to PiP windows.
    
    This CL moves that logic into a separate mixin class so that it can be
    used across multiple test bases and reused anywhere for web applications/ code. This will make writing tests for
    crrev.com/c/5689758 very easy.
    
    To make this work, PostRunTestOnMainThread() had to be implemented inside MixinBasedInProcessBrowserTest, hence the changes in
    chrome/test/base.
    
    Bug: 350256139
    Change-Id: Ib2cd14e8b7355ecf5847017232ed7bd6d0315d4b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5696468
    Reviewed-by: Daniel Murphy <dmurph@chromium.org>
    Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org>
    Reviewed-by: Scott Violet <sky@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1326519}

M       chrome/browser/ui/web_applications/app_browser_document_picture_in_picture_browsertest.cc
A       chrome/browser/ui/web_applications/test/web_app_picture_in_picture_mixin_test_base.cc
A       chrome/browser/ui/web_applications/test/web_app_picture_in_picture_mixin_test_base.h
M       chrome/test/BUILD.gn
M       chrome/test/base/mixin_based_in_process_browser_test.cc
M       chrome/test/base/mixin_based_in_process_browser_test.h

https://chromium-review.googlesource.com/5696468


### ap...@google.com (2024-07-12)

Project: chromium/src
Branch: main

commit 1e2c639d42694225c09cf18eb09b9df75ecd16a3
Author: Dibyajyoti Pal <dibyapal@google.com>
Date:   Fri Jul 12 14:31:30 2024

    [PWA] Fix picture-in-picture window occluding PWA install dialogs
    
    This CL fixes a vulnerability where picture-in-picture windows were
    occluding the install dialogs. Based on investigation and
    discussions, if a picture-in-picture window is occluding the install dialog, the PiP window will be closed to give priority to the web
    modal dialog.
    
    Tested manually with the 3 install dialogs using
    https://excited-dented-seashore.glitch.me/, which is a rough repro
    of the files listed in the bug.
    
    Bug: 350256139
    Change-Id: I86c88ab06682b195114a842efb805f91c70a2477
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5689758
    Reviewed-by: Daniel Murphy <dmurph@chromium.org>
    Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1326758}

M       chrome/browser/ui/views/web_apps/simple_install_dialog_bubble_view_browsertest.cc
M       chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog.cc
M       chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog_browsertest.cc
M       chrome/browser/ui/views/web_apps/web_app_diy_install_dialog.cc
M       chrome/browser/ui/views/web_apps/web_app_diy_install_dialog_browsertest.cc
M       chrome/browser/ui/views/web_apps/web_app_install_dialog_delegate.cc
M       chrome/browser/ui/views/web_apps/web_app_install_dialog_delegate.h
M       chrome/browser/ui/views/web_apps/web_app_simple_install_dialog.cc
M       chrome/browser/ui/web_applications/test/web_app_picture_in_picture_mixin_test_base.cc
M       chrome/browser/ui/web_applications/test/web_app_picture_in_picture_mixin_test_base.h

https://chromium-review.googlesource.com/5689758


### pe...@google.com (2024-07-13)

Requesting merge to beta (M127) because latest trunk commit (1326758) appears to be after beta branch point (1313161).
Merge review required: M127 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-07-15)

Since this is a textually large change that involves UI elements that was just recently landed and this won't have a chance to make it to M127 beta before M127 Stable RC is cut tomorrow, I'm going to defer merge approval for now. Given the preconditions to exploit here, it may seem prudent to defer merge outright and let this fix matriculate into M128 Stable release without backmerging.

### sp...@google.com (2024-07-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
$500 reward for report of low impact issue with significant preconditions for potential exploitation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-31)

Thank you for the report. There is low potential for user harm and substantial preconditions here that seem unlikely this could be exploited in a real world scenario; however, since we were able to make a security beneficial change, we are extending a $500 thank you reward for your efforts

### pe...@google.com (2024-10-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/350256139)*
