# Security: URL bar spoofing with Full-screen mode

| Field | Value |
|-------|-------|
| **Issue ID** | [40091816](https://issues.chromium.org/issues/40091816) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2018-06-29 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: 69.0.3476.0 (Developer Build) (64-bit)

Operating System: Mac

**REPRODUCTION CASE**

1. Lunch Chrome
2. Entering full screen mode with the green maximize Button.
3. Load the test case
4. Click on 'click-1' button
5. Click on 'click-2' button
6. spoofing

## Attachments

- [testcase.zip](attachments/testcase.zip) (application/octet-stream, 41.8 KB)
- [screen-223.mov](attachments/screen-223.mov) (video/quicktime, 1.7 MB)
- [Untitled.mov](attachments/Untitled.mov) (video/quicktime, 4.0 MB)

## Timeline

### in...@chromium.org (2018-06-29)

Not a convincing spoof.

[Monorail components: UI>Browser>FullScreen]

### ch...@gmail.com (2018-06-29)

Sometimes Chrome shows the bar omnibox and other times doesn't show it.
Note: this is a regression issue. I’m unable to repro this on stable.

### ch...@gmail.com (2018-07-10)

Any update on this bug? Thanks!

### kk...@chromium.org (2018-07-10)

I think I was mistakenly added to this bug; I don't work on Mac Chrome.  I'm marking as untriaged and adding the OS so this can be handled by someone more appropriate.

### me...@chromium.org (2018-07-10)

Am I understanding the PoC correctly: The second popup is automatically made fullscreen, possibly because the original window is made fullscreen by the user?


### av...@chromium.org (2018-07-11)

:(

A fullscreen page opening a popup should automatically lose fullscreen. I don't know what's up here.

### av...@chromium.org (2018-07-11)

Is this MacViews?

### el...@chromium.org (2018-07-13)

Mac triage: over to avi@ :)

### av...@chromium.org (2018-07-25)

I cannot reproduce this. Every time, clicking on the "click-2" button kicks the window out of fullscreen.

Can you still reproduce this, OP? If so, can you provide more detail?

Thank you.

### ch...@gmail.com (2018-07-25)

I'm still able to repro on the latest version of Canary. 

1. Enter full screen mode with the green maximizebButton.
2. Load https://permission.site
3. Click on "Fullscreen"
4. Click on "Popup"

### ch...@gmail.com (2018-07-26)

Sometimes when I click on the green maximize button, I get fullscreen.

### av...@chromium.org (2018-07-27)

Weili, I'm cc-ing you because you need to access this bug to repro https://crbug.com/chromium/868416.

### av...@chromium.org (2018-07-27)

Here's a summary of what's going on here.

Chrome's current behavior is that if a page is in HTML5 fullscreen, and it shows a popup, the page loses fullscreen.

In this POC, the user has put the page into user fullscreen, then the page goes into HTML5 fullscreen, then the page shows a popup. When the page shows the popup, it loses the HTML5 fullscreen but retains the user fullscreen. The question is what happens to the popup.

On Windows, showing the popup makes the page lose HTML5 fullscreen, and the popup appears as a small pop-up window on top of the original page, which remains in user fullscreen.

On Mac Cocoa, showing the popup makes the page lose HTML5 fullscreen, and the popup appears as a tab in the user fullscreen window.

On Mac Views (looking at 70.0.3504.0 canary), you get a different behavior. Showing the popup makes the page lose HTML5 fullscreen, and the popup gains user fullscreen, which has a URL bar at the top of the window. (This actually trips a DCHECK in development builds; filed as https://crbug.com/chromium/868416.)

It would probably be a good idea for the popup to not inherit the user fullscreen, but given that there is a URL bar at the top of the window, this isn't a spoof we're super worried about.

In none of these cases are we seeing the issue in the original comment. OP, looking at your video, it seems that you were using MacViews, which at the time didn't have a correctly-functioning fullscreen implementation. Things have changed quite a bit. Can you confirm with an updated Chrome 69/70 for repro?

Thank you!

### bu...@chromium.org (2018-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb

commit c552cd7b8a0862f6b3c8c6a07f98bda3721101eb
Author: Avi Drissman <avi@chromium.org>
Date: Fri Jul 27 19:44:37 2018

Mac: turn popups into new tabs while in fullscreen.

It's platform convention to show popups as new tabs while in
non-HTML5 fullscreen. (Popups cause tabs to lose HTML5 fullscreen.)

This was implemented for Cocoa in a BrowserWindow override, but
it makes sense to just stick it into Browser and remove a ton
of override code put in just to support this.

BUG=858929, 868416
TEST=as in bugs

Change-Id: I43471f242813ec1159d9c690bab73dab3e610b7d
Reviewed-on: https://chromium-review.googlesource.com/1153455
Reviewed-by: Sidney San Martín <sdy@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#578755}
[modify] https://crrev.com/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb/chrome/browser/ui/browser.cc
[modify] https://crrev.com/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb/chrome/browser/ui/browser_navigator.cc
[modify] https://crrev.com/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb/chrome/browser/ui/browser_window.h
[modify] https://crrev.com/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb/chrome/browser/ui/cocoa/browser_window_cocoa.h
[modify] https://crrev.com/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb/chrome/browser/ui/cocoa/browser_window_cocoa.mm
[modify] https://crrev.com/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb/chrome/browser/ui/views/frame/browser_view.cc
[modify] https://crrev.com/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb/chrome/browser/ui/views/frame/browser_view.h
[modify] https://crrev.com/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb/chrome/test/base/test_browser_window.cc
[modify] https://crrev.com/c552cd7b8a0862f6b3c8c6a07f98bda3721101eb/chrome/test/base/test_browser_window.h


### av...@chromium.org (2018-07-27)

This change restores the old Cocoa behavior to MacViews.

### av...@chromium.org (2018-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

Your change meets the bar and is auto-approved for M69. Please go ahead and merge the CL to branch 3497 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-07-29)


Please merge your change to M69 branch 3497 by 2:00 PM PT Monday, 07/30, so we can pick it up for next week last M69 Dev release. Thank you.


### bu...@chromium.org (2018-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c18c88413f1a3210e77fd73ef1242637481d9fc8

commit c18c88413f1a3210e77fd73ef1242637481d9fc8
Author: Avi Drissman <avi@chromium.org>
Date: Sun Jul 29 22:22:26 2018

Mac: turn popups into new tabs while in fullscreen.

It's platform convention to show popups as new tabs while in
non-HTML5 fullscreen. (Popups cause tabs to lose HTML5 fullscreen.)

This was implemented for Cocoa in a BrowserWindow override, but
it makes sense to just stick it into Browser and remove a ton
of override code put in just to support this.

BUG=858929, 868416
TEST=as in bugs

Change-Id: I43471f242813ec1159d9c690bab73dab3e610b7d
Reviewed-on: https://chromium-review.googlesource.com/1153455
Reviewed-by: Sidney San Martín <sdy@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#578755}(cherry picked from commit c552cd7b8a0862f6b3c8c6a07f98bda3721101eb)
Reviewed-on: https://chromium-review.googlesource.com/1154508
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/branch-heads/3497@{#192}
Cr-Branched-From: 271eaf50594eb818c9295dc78d364aea18c82ea8-refs/heads/master@{#576753}
[modify] https://crrev.com/c18c88413f1a3210e77fd73ef1242637481d9fc8/chrome/browser/ui/browser.cc
[modify] https://crrev.com/c18c88413f1a3210e77fd73ef1242637481d9fc8/chrome/browser/ui/browser_navigator.cc
[modify] https://crrev.com/c18c88413f1a3210e77fd73ef1242637481d9fc8/chrome/browser/ui/browser_window.h
[modify] https://crrev.com/c18c88413f1a3210e77fd73ef1242637481d9fc8/chrome/browser/ui/cocoa/browser_window_cocoa.h
[modify] https://crrev.com/c18c88413f1a3210e77fd73ef1242637481d9fc8/chrome/browser/ui/cocoa/browser_window_cocoa.mm
[modify] https://crrev.com/c18c88413f1a3210e77fd73ef1242637481d9fc8/chrome/browser/ui/views/frame/browser_view.cc
[modify] https://crrev.com/c18c88413f1a3210e77fd73ef1242637481d9fc8/chrome/browser/ui/views/frame/browser_view.h
[modify] https://crrev.com/c18c88413f1a3210e77fd73ef1242637481d9fc8/chrome/test/base/test_browser_window.cc
[modify] https://crrev.com/c18c88413f1a3210e77fd73ef1242637481d9fc8/chrome/test/base/test_browser_window.h


### aw...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-06)

$500 for this report, thanks!

### aw...@chromium.org (2018-08-06)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/858929?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091816)*
