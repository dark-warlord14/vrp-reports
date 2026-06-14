# Security: The sharing dialog can appear over the wrong tab (spoof)

| Field | Value |
|-------|-------|
| **Issue ID** | [40050837](https://issues.chromium.org/issues/40050837) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | kn...@chromium.org |
| **Created** | 2019-11-29 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 80.0.3979.0 (Official Build) canary (64-bit)  

Operating System: macOS

**REPRODUCTION CASE**  

This is the same bug as <https://crbug.com/chromium/1005596>.

1. Lunch the test case
2. Click on the button and wait.

The sharing dialog should not be displayed over the wrong tab because the victim would think that the wrong page ('<https://www.apple.com/contact/>') intended to make a call.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 1.1 MB)
- [poc (1).html](attachments/poc (1).html) (text/plain, 192 B)

## Timeline

### ch...@gmail.com (2019-11-29)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-12-02)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Sharing]

### pa...@chromium.org (2019-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kn...@chromium.org (2019-12-03)

Thanks again for the report! This seems to be caused by using the wrong WebContents when creating the dialog. CL with a fix is up for review: https://crrev.com/c/1948838

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/249cd0d75bf19f6374d8372101dcdcc68d16a445

commit 249cd0d75bf19f6374d8372101dcdcc68d16a445
Author: Richard Knoll <knollr@chromium.org>
Date: Wed Dec 04 09:54:44 2019

Use active WebContents for SharingDialogs

Instead of using the WebContents from the tab that initiated showing a
SharingDialog, always use the one from the currently shown tab. This
makes sure that we show the origin if the initiating one does not match
the one in the active tab.

Bug: 1029414
Change-Id: Idf79aeff17db3c5cf3137af19727bdaf79989bf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1948838
Commit-Queue: Richard Knoll <knollr@chromium.org>
Reviewed-by: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Cr-Commit-Position: refs/heads/master@{#721409}

[modify] https://crrev.com/249cd0d75bf19f6374d8372101dcdcc68d16a445/chrome/browser/sharing/click_to_call/click_to_call_ui_controller.cc
[modify] https://crrev.com/249cd0d75bf19f6374d8372101dcdcc68d16a445/chrome/browser/sharing/shared_clipboard/shared_clipboard_ui_controller.cc
[modify] https://crrev.com/249cd0d75bf19f6374d8372101dcdcc68d16a445/chrome/browser/ui/views/sharing/click_to_call_browsertest.cc
[modify] https://crrev.com/249cd0d75bf19f6374d8372101dcdcc68d16a445/chrome/browser/ui/views/sharing/sharing_browsertest.cc


### kn...@chromium.org (2019-12-05)

This is fixed in 80.0.3986.0, it now correctly shows the initiating origin.

### sh...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-17)

Congrats! The Panel decided to reward $2,000 for this report

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-03-12)

This issue was migrated from crbug.com/chromium/1029414?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050837)*
