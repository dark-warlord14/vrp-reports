# Safebrowsing does not trigger a malware warning for malware loaded through an embed

| Field | Value |
|-------|-------|
| **Issue ID** | [40059875](https://issues.chromium.org/issues/40059875) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | xp...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-06-06 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. Create an embed and set the src attribute to malware targeted by safebrowsing e.g. <https://testsafebrowsing.appspot.com/s/malware.html>

OR

Download my simple PoC.html and run in Chrome.

**Problem Description:**  

Safebrowsing should trigger for malware that is loaded through an embed.... but it doesn't e.g. <embed src="https://testsafebrowsing.appspot.com/s/malware.html">

**Additional Comments:**

\*\*Chrome version: \*\* 104.0.5104.0 \*\*Channel: \*\* Stable

**OS:** Windows

## Attachments

- [PoC.html](attachments/PoC.html) (text/plain, 204 B)

## Timeline

### dt...@chromium.org (2022-06-07)

[Empty comment from Monorail migration]

[Monorail components: Services>Safebrowsing]

### am...@chromium.org (2022-06-14)

Due to an issue with the monorail wizard workflow, this issue was not labeled as a security bug and, therefore, this issue did not make it to the security team bug queue for triage. 

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### xp...@gmail.com (2022-06-14)

Created https://bugs.chromium.org/p/chromium/issues/detail?id=1336095, which is similar/dupe of this issue.

### fl...@chromium.org (2022-06-14)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-14)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-14)

Thanks for the report. I'm able to reproduce. Note that <embed src="https://testsafebrowsing.appspot.com/s/malware.html"> doesn't trigger a warning but <embed src="https://testsafebrowsing.appspot.com/s/image_large.html"> does trigger a warning. I'll look into it further.

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-14)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-07-26)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-07-26)

Thanks for the report! The warning is not shown because Chrome currently only triggers a warning of malware landing page[1] when the URL is mainframe or subframe[2] (i.e. excluding other resources like js, video or image). The reason is to reduce potential false positives. 

We do believe that loading malware landing pages as object and embed can potentially cause similar harm as loading them as subframes. I'll work on including object and embed in the check here[3].

[1] https://developers.google.com/safe-browsing/v4/metadata?hl=en#malware-sites
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/safe_browsing/content/browser/base_ui_manager.cc;l=211-215;drc=593a308ce797aa2fee55bdf0a617ab5529543c18
[3] https://source.chromium.org/chromium/chromium/src/+/main:components/safe_browsing/content/browser/base_ui_manager.cc;l=210;drc=593a308ce797aa2fee55bdf0a617ab5529543c18

### gi...@appspot.gserviceaccount.com (2022-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/acb933d418845fb73e5705ff499e414a021f160c

commit acb933d418845fb73e5705ff499e414a021f160c
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Fri Jul 29 23:31:45 2022

Show warning on malware landing sites loaded as object or embed

Currently malware landing pages only trigger warnings when they are
loaded as mainframe or subframe. We should treat pages loaded as
<object> or <embed> the same as subframes, because they can also
display contents and execute js.

Bug: 1333623
Change-Id: Ie4b3baf4ed1bfaa25dc1d7190328ce2c4cc2b25b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788508
Reviewed-by: Daniel Rubery <drubery@chromium.org>
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1029992}

[modify] https://crrev.com/acb933d418845fb73e5705ff499e414a021f160c/components/safe_browsing/core/browser/db/BUILD.gn
[modify] https://crrev.com/acb933d418845fb73e5705ff499e414a021f160c/components/safe_browsing/content/browser/base_ui_manager.cc
[modify] https://crrev.com/acb933d418845fb73e5705ff499e414a021f160c/components/safe_browsing/core/browser/db/fake_database_manager.cc
[modify] https://crrev.com/acb933d418845fb73e5705ff499e414a021f160c/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc
[add] https://crrev.com/acb933d418845fb73e5705ff499e414a021f160c/chrome/test/data/safe_browsing/malware4.html
[modify] https://crrev.com/acb933d418845fb73e5705ff499e414a021f160c/components/safe_browsing/core/browser/db/fake_database_manager.h


### xi...@chromium.org (2022-07-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations, Sven! The VRP Panel has decided to award you $5,000 fro this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### xp...@gmail.com (2022-08-17)

Thank you.

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-11-05)

This issue was migrated from crbug.com/chromium/1333623?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1336095]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059875)*
