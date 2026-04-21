# Security: Bug 1238631 regression (Share dialog on Windows can render over address bar, window controls)

| Field | Value |
|-------|-------|
| **Issue ID** | [40062941](https://issues.chromium.org/issues/40062941) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>WebShare |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | mh...@microsoft.com |
| **Created** | 2023-02-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

I can reproduce <https://bugs.chromium.org/p/chromium/issues/detail?id=1238631> on latest Chrome and Windows.

**VERSION**  

Chrome Version: 109.0.5414.120 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 Version 21H2 (Build 19044.2486)

**REPRODUCTION CASE**  

Reusing same PoC as <https://bugs.chromium.org/p/chromium/issues/detail?id=1238631> (credit to Alesandro Ortiz)

1. Navigate <https://humdrum-somber-purple.glitch.me/share-shortwin.html>.
2. Double-click the link, web-share prompt covers the address bar of the short window.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [share-shortwin.html](attachments/share-shortwin.html) (text/plain, 1.0 KB)
- [share-shortwin-popup.html](attachments/share-shortwin-popup.html) (text/plain, 326 B)
- [Untitled_ Feb 7, 2023 4_15 PM.webm](attachments/Untitled_ Feb 7, 2023 4_15 PM.webm) (video/webm, 839.4 KB)
- [Untitled_ Feb 10, 2023 10_32 PM.webm](attachments/Untitled_ Feb 10, 2023 10_32 PM.webm) (video/webm, 1.0 MB)

## Timeline

### [Deleted User] (2023-02-07)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-08)

Thanks for the report!

mhochk@, since you fixed 1238631 and this looks like it's a regression, could you take a look at it, please?



[Monorail components: Blink>WebShare]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mh...@microsoft.com (2023-02-09)

Confirmed I'm seeing this in Chrome Stable, Beta, and Dev, but interestingly I am *not* seeing this in Chrome Canary (tested on Win 10 and Win 11) or a local build of 'main'. It's not clear yet if this was just recently fixed, or if this is actually dependent on the channel.

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-02-10)

mhochk@, I still see this on Canary (112.0.5587.2 (Official Build) canary (64-bit))

### mh...@microsoft.com (2023-02-10)

Bug understood (including why it is inconsistent). Should have a fix soon.

### gi...@appspot.gserviceaccount.com (2023-02-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/78350274d598741df546cca6c78feea57b998573

commit 78350274d598741df546cca6c78feea57b998573
Author: Hoch Hochkeppel <mhochk@microsoft.com>
Date: Mon Feb 13 19:40:40 2023

Direct HWND fetching for Windows navigator.Share

Updating how the Windows implementation of navigator.Share attempts to
fetch the HWND designated for accessibility with the WebContents. This
change allows it to successfully fetch said HWND, even if not all the
accessibility components have been initialized yet (which may happen if
no accessibility tools have been detected).

Bug: 1413618
Change-Id: Ia0ded852ea0c966ac35342c3cd23bf445ebf8305
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4245222
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Auto-Submit: Hoch Hochkeppel <mhochk@microsoft.com>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1104616}

[modify] https://crrev.com/78350274d598741df546cca6c78feea57b998573/chrome/browser/webshare/win/share_operation.cc


### mh...@microsoft.com (2023-02-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations, Axel! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-23)

This issue was migrated from crbug.com/chromium/1413618?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062941)*
