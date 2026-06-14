# Security: fullscreen UI spoof using pdf prompt

| Field | Value |
|-------|-------|
| **Issue ID** | [40092145](https://issues.chromium.org/issues/40092145) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>HTML>Dialog, UI>Browser>FullScreen |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | zx...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2018-08-10 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36

Steps to reproduce the problem:
1. open http://test.au1ge.xyz/pdf.html
2. cick start

What is the expected behavior?
Full screen should be kicked out

What went wrong?
Just like https://bugs.chromium.org/p/chromium/issues/detail?id=871021
fullscreen notification was overlapped

Did this work before? N/A 

Chrome version: 68.0.3440.84  Channel: n/a
OS Version: OS X 10.13.6
Flash Version: Shockwave Flash 30.0 r0

## Timeline

### zx...@gmail.com (2018-08-10)

After you fill out the form in dialog, open http://test.au1ge.xyz/pw.txt to see your input

### ji...@chromium.org (2018-08-10)

kenrb@, and avi@, I think this is quite similar to https://bugs.chromium.org/p/chromium/issues/detail?id=871021. Could any of you help triage this issue? 

Thanks!

[Monorail components: Blink>HTML>Dialog UI>Browser>FullScreen]

### ji...@chromium.org (2018-08-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-11)

[Empty comment from Monorail migration]

### ji...@chromium.org (2018-08-12)

[Empty comment from Monorail migration]

### av...@chromium.org (2018-08-12)

Showing a dialog should have kicked the PDF out of fullscreen. Do PDF JS dialogs go through a different path than HTML JS dialogs?

### th...@chromium.org (2018-08-13)

avi: PDF alert dialogs go through PepperPDFHost::OnHostMsgShowAlertDialog(). 

### ke...@chromium.org (2018-08-13)

[Empty comment from Monorail migration]

### av...@chromium.org (2018-08-13)

thestig: WebContentsImpl::RunJavaScriptDialog() checks for fullscreen and drops out. Does that go through that?

### av...@chromium.org (2018-08-13)

This is very odd.

When the window goes fullscreen, IsWindowFullscreenForTabOrPending is true. However, by the time that the PDF dialog is shown, IsWindowFullscreenForTabOrPending goes false, and IsFullscreenForBrowser is true, which is absolutely incorrect.

What is going on here? Sarah, do you have thoughts?

### av...@chromium.org (2018-08-13)

bool FullscreenController::IsFullscreenForBrowser() const {
  return exclusive_access_manager()->context()->IsFullscreen() &&
         !IsFullscreenCausedByTab();
}

So if we're fullscreen, but it's not caused by a tab, then it's "browser fullscreen" which doesn't count towards kicking us out of fullscreen for dialogs.

Why is this happening with PDFs? Still investigating.

### av...@chromium.org (2018-08-13)

Of course. The PDF is in an inner WebContents that isn't fullscreen, but the outer one is.

### bu...@chromium.org (2018-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3dcaec6e30feebefc11ee6972a76d446257b28a6

commit 3dcaec6e30feebefc11ee6972a76d446257b28a6
Author: Avi Drissman <avi@chromium.org>
Date: Tue Aug 14 17:53:43 2018

Security drop fullscreen for any nested WebContents level.

BUG=873080
TEST=as in bug

Change-Id: Icd75715ac42789c84870967b11c9917a972ae086
Reviewed-on: https://chromium-review.googlesource.com/1173342
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Sidney San Martín <sdy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#582970}
[modify] https://crrev.com/3dcaec6e30feebefc11ee6972a76d446257b28a6/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/3dcaec6e30feebefc11ee6972a76d446257b28a6/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/3dcaec6e30feebefc11ee6972a76d446257b28a6/content/browser/web_contents/web_contents_impl_browsertest.cc


### av...@chromium.org (2018-08-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/95326269d0796e0e82d7d13b769a263674287855

commit 95326269d0796e0e82d7d13b769a263674287855
Author: Chris Mumford <cmumford@chromium.org>
Date: Tue Aug 14 23:13:10 2018

Revert "Security drop fullscreen for any nested WebContents level."

This reverts commit 3dcaec6e30feebefc11ee6972a76d446257b28a6.

Reason for revert: Failing Linux MSan tests

https://ci.chromium.org/p/chromium/builders/luci.chromium.ci/Linux%20MSan%20Tests/11191

DevTools listening on ws://127.0.0.1:34267/devtools/browser/a12caedc-549b-4d49-b9bb-a0519f91f318
==14126==WARNING: MemorySanitizer: use-of-uninitialized-value
    #0 0x3c2bb23 in ExitFullscreenModeForTab ./../../content/browser/web_contents/web_contents_impl_browsertest.cc:1561:9

Original change's description:
> Security drop fullscreen for any nested WebContents level.
> 
> BUG=873080
> TEST=as in bug
> 
> Change-Id: Icd75715ac42789c84870967b11c9917a972ae086
> Reviewed-on: https://chromium-review.googlesource.com/1173342
> Commit-Queue: Avi Drissman <avi@chromium.org>
> Reviewed-by: Sidney San Martín <sdy@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#582970}

TBR=avi@chromium.org,sdy@chromium.org

Change-Id: I52a9b29f2d17ea6e7db0128815653de624fa5b13
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 873080
Reviewed-on: https://chromium-review.googlesource.com/1174640
Reviewed-by: Chris Mumford <cmumford@chromium.org>
Commit-Queue: Chris Mumford <cmumford@chromium.org>
Cr-Commit-Position: refs/heads/master@{#583071}
[modify] https://crrev.com/95326269d0796e0e82d7d13b769a263674287855/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/95326269d0796e0e82d7d13b769a263674287855/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/95326269d0796e0e82d7d13b769a263674287855/content/browser/web_contents/web_contents_impl_browsertest.cc


### av...@chromium.org (2018-08-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d18c519758c2e6043f0e1f00e2b69a55b3d7997f

commit d18c519758c2e6043f0e1f00e2b69a55b3d7997f
Author: Avi Drissman <avi@chromium.org>
Date: Wed Aug 15 18:32:09 2018

Security drop fullscreen for any nested WebContents level.

This relands 3dcaec6e30feebefc11e with a fix to the test.

BUG=873080
TEST=as in bug

Change-Id: Ie68b197fc6b92447e9633f233354a68fefcf20c7
Reviewed-on: https://chromium-review.googlesource.com/1175925
Reviewed-by: Sidney San Martín <sdy@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#583335}
[modify] https://crrev.com/d18c519758c2e6043f0e1f00e2b69a55b3d7997f/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/d18c519758c2e6043f0e1f00e2b69a55b3d7997f/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/d18c519758c2e6043f0e1f00e2b69a55b3d7997f/content/browser/web_contents/web_contents_impl_browsertest.cc


### av...@chromium.org (2018-08-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-27)

The VRP panel decided to award $1,000 for this report - many thanks!

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-14)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-09-14)

no merge needed since this landed August 15th. 

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-11-22)

This issue was migrated from crbug.com/chromium/873080?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>Dialog, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092145)*
