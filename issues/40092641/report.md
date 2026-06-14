# Security: pageCapture permission allows access to arbitrary local files and chrome:// pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40092641](https://issues.chromium.org/issues/40092641) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | bd...@chromium.org |
| **Created** | 2018-10-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The pageCapture permission allows an extension to call the chrome.pageCapture.saveAsMHTML method. This method will save the page data for any tab, regardless of whether it's a standard web page, chrome:// page or local file. This is true even if "Allow access to file URLs" is unchecked - while it's not possible to interact with the page content directly, it is possible to save a MHTML capture of the page.

**VERSION**  

Chrome Version: 69.0.3497.100 + stable  

Operating System: Windows 10 Pro, version 1803

**REPRODUCTION CASE**  

Once installed, the attached extension will perform the following actions:

1. Open a new tab, pointing to file:///C:/
2. Call saveAsMHTML(), to save the contents of the tab as MHTML. The generated MHTML will then be sent to the exfiltration server. Although it doesn't do so at the moment, it would be possible to extend the extension so that it parses the generated MHTML file locally (to retrieve a list of files and folders) and automatically traverses through directories.

The scope of this issue is similar to <https://bugs.chromium.org/p/chromium/issues/detail?id=810220>. In this case, the tab contents can be captured directly (rather than as an image).

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [pagecapture_poc.zip](attachments/pagecapture_poc.zip) (application/octet-stream, 1.0 KB)

## Timeline

### ji...@chromium.org (2018-10-08)

I feel this issue has a much higher friction than crbug.com/810220.
And in my opinion, if the attacker succeeds in tricking users into installing a malicious extension, there're much worse things could happen. 

rdevlin.cronin@ and meacer@, could you weigh in on this?

### rd...@chromium.org (2018-10-08)

My $0.02: We should tweak this, but it's probably low severity.

We've adjusted the permissions for the tabs.captureVisibleTab() API method to allow extensions to capture otherwise-restricted URLs if the user has granted activeTab, which serves as an extra layer of protection for user intent.  We've also ensured that file:// URLs are only capturable with the "Allow on file URLs" option enabled.  I think both of those are worth doing for this, as well.

In general, I think we should align all our capture logic to have similar requirements.  For these methods, that will probably mean the logic for captureVisibleTab(), but in the future, it would be nice to move everything to more of a chooser-model (like desktopCapture) has.

[Monorail components: Platform>Extensions>API]

### me...@google.com (2018-10-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### rd...@chromium.org (2018-10-24)

[Empty comment from Monorail migration]

### bd...@chromium.org (2018-11-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0660e08731fd42076d7242068e9eaed1482b14d5

commit 0660e08731fd42076d7242068e9eaed1482b14d5
Author: Bettina <bdea@chromium.org>
Date: Mon Dec 10 21:03:02 2018

Call CanCaptureVisiblePage in page capture API.

Currently the pageCapture permission allows access
to arbitrary local files and chrome:// pages which
can be a security concern. In order to address this,
the page capture API needs to be changed similar to
the captureVisibleTab API. The API will now only allow
extensions to capture otherwise-restricted URLs if the
user has granted activeTab. In addition, file:// URLs are
only capturable with the "Allow on file URLs" option enabled.

Bug: 893087

Change-Id: I6d6225a3efb70fc033e2e1c031c633869afac624
Reviewed-on: https://chromium-review.googlesource.com/c/1330689
Commit-Queue: Bettina Dea <bdea@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Varun Khaneja <vakh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#615248}
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/chrome/browser/extensions/active_tab_unittest.cc
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/chrome/browser/extensions/api/page_capture/page_capture_api.cc
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/chrome/browser/extensions/api/page_capture/page_capture_api.h
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/chrome/browser/extensions/api/page_capture/page_capture_apitest.cc
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/chrome/browser/extensions/extension_apitest.cc
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/chrome/browser/extensions/extension_apitest.h
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/chrome/common/extensions/permissions/permissions_data_unittest.cc
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/chrome/test/data/extensions/api_test/page_capture/test.js
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/extensions/common/manifest_constants.cc
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/extensions/common/manifest_constants.h
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/extensions/common/permissions/permissions_data.cc
[modify] https://crrev.com/0660e08731fd42076d7242068e9eaed1482b14d5/extensions/common/permissions/permissions_data.h


### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### bd...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-01)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-15)

Congrats the Panel decided to reward $500 for this report

### na...@google.com (2019-05-15)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

Looks like this was missed in previous release notes, so adding Release-0-M75 to pick it up in 75

### aw...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/893087?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092641)*
