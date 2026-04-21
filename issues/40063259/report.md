# Bypass 1349146, local file access checks can be bypassed by using `file:` instead of `file://`

| Field | Value |
|-------|-------|
| **Issue ID** | [40063259](https://issues.chromium.org/issues/40063259) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Mac |
| **Reporter** | ma...@fingerprint.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2023-02-26 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. Install the attached extension. Make sure to disable "Allows access to file URLs".
2. Open Developer Tools on the new tab opened by the extension.
3. You'll see an alert box with the contents of the /etc/hosts\* file.

\*Because of `/etc/hosts` this will only work on system where this file is available.

**Problem Description:**  

For more details please see <https://bugs.chromium.org/p/chromium/issues/detail?id=1349146>. The checks implemented in the original issue can be bypassed by using `file:` instead of `file://`.

I'm creating a new issue as the original is marked as Fixed (closed) already.

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5481.177 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [background.js](attachments/background.js) (text/plain, 183 B)
- [manifest.json](attachments/manifest.json) (text/plain, 200 B)
- [devtools.js](attachments/devtools.js) (text/plain, 245 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)

## Timeline

### ma...@fingerprint.com (2023-02-26)

https://bugs.chromium.org/p/chromium/issues/detail?id=1349146 is about to be disclosed within two weeks I believe. I think that should be postponed if that's possible. 

### [Deleted User] (2023-02-26)

[Empty comment from Monorail migration]

### ma...@fingerprint.com (2023-02-27)

Note that this will only work in case the embedding page's (the page with a resource specifying the sourceMappingURL) origin is `null`, otherwise `file:path` will be considered as a relative path.

### sr...@google.com (2023-02-27)

Thanks for the report! Over to dsv@ who handled the last report.

[Monorail components: Platform>Extensions]

### [Deleted User] (2023-02-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/cd1ab1eb0ffd1b78d7c6449726bbfc96ce9a7c33

commit cd1ab1eb0ffd1b78d7c6449726bbfc96ce9a7c33
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Feb 28 14:17:32 2023

Also handle file: URL without leading slashes when checking extension permissions.

Bug: 1419732
Change-Id: I7f6cef3e3319a60708d98dcd21aa8afe418a306f
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4295641
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Wolfgang Beyer <wolfi@chromium.org>
Commit-Queue: Wolfgang Beyer <wolfi@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/cd1ab1eb0ffd1b78d7c6449726bbfc96ce9a7c33/front_end/models/extensions/ExtensionAPI.ts


### [Deleted User] (2023-03-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tj...@chromium.org (2023-03-08)

@dsv: is this fixed with comment https://crbug.com/chromium/1419732#c7?

### [Deleted User] (2023-03-13)

dsv: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/985e7240669c996e70c9f4bfecbcf41a641b6fbd

commit 985e7240669c996e70c9f4bfecbcf41a641b6fbd
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Mar 21 09:04:21 2023

Update test to check for file: URL without slashes after the behavior change in the crrev.com/c/4295641

Bug: 1419732
Change-Id: I372d126501b1c1c0277c27167d143d797d67c672
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4294941
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1119820}

[modify] https://crrev.com/985e7240669c996e70c9f4bfecbcf41a641b6fbd/chrome/browser/devtools/devtools_browsertest.cc


### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations, Martin! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1419732?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063259)*
