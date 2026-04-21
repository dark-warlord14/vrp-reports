# Security: Bypassing of security interstitials using devtools API

| Field | Value |
|-------|-------|
| **Issue ID** | [40070873](https://issues.chromium.org/issues/40070873) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | al...@google.com |
| **Created** | 2023-08-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Similar to <https://bugs.chromium.org/p/chromium/issues/detail?id=1268445> (which was for the debugger permission), a devtools API extension can debug and obtain scripting access to chrome-error://chromewebdata page, which allows it to bypass security interstitials. Note that for it to work we have to use .reload to inject our script. (eval, for an unknown reason doesn't work)

As a note, there are some targets that devtools extension cannot debug, such as chrome webstore and enterprise policy-blocked hosts. So bypassing SSL interstitials are more valuable for these targets.

**VERSION**  

Chrome Version: 116.0.5845.111 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 Version 22H2 (Build 19045.3324)

**REPRODUCTION CASE**

1. Inspect element and wait.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [background.js](attachments/background.js) (text/plain, 101 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [devtools.js](attachments/devtools.js) (text/plain, 274 B)
- [manifest.json](attachments/manifest.json) (text/plain, 183 B)

## Timeline

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-08-29)

Please see https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4824243 for the fix to this issue.

### ph...@chromium.org (2023-08-30)

I'm not sure how to install the extension and reproduce.  I'll leave it for the DevTool owner.

alexrudenko@: could you take a look?

[Monorail components: Platform>DevTools>Platform]

### [Deleted User] (2023-08-30)

[Empty comment from Monorail migration]

### al...@chromium.org (2023-08-31)

I am able to reproduce and I also verified that the proposed fix works. pfaffe@ dsv@ PTAL when you are back too.

### gi...@appspot.gserviceaccount.com (2023-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/c70dfc79e147c9a4d6732affbb8e28af4d058ab4

commit c70dfc79e147c9a4d6732affbb8e28af4d058ab4
Author: Haxatron Sec <haxatron1@gmail.com>
Date: Tue Aug 29 19:16:28 2023

block devtools extension access to interstitials

Change-Id: I7f6536e97eb659d12c240bc9a7ff8b239123c83a
Bug: 1476952
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4824243
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org>
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>

[modify] https://crrev.com/c70dfc79e147c9a4d6732affbb8e28af4d058ab4/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/c70dfc79e147c9a4d6732affbb8e28af4d058ab4/AUTHORS
[modify] https://crrev.com/c70dfc79e147c9a4d6732affbb8e28af4d058ab4/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### ct...@chromium.org (2023-09-11)

Current security shepherd here: Setting some security labels on this bug -- FoundIn-116 (as this affects current Stable) and Severity-Medium (this has the mitigating factor of requiring an extension so maybe borderline Sev-Low).

### [Deleted User] (2023-09-11)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-09-12)

alexrudenko@ can this be marked as fixed?

### [Deleted User] (2023-09-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2023-09-12)

I think it's fixed, thanks!

### [Deleted User] (2023-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations on another one, Axel! The Chrome VRP Panel has decided to award you $1,000 for this report + $1,000 patch bonus. 
Thank you for your efforts in writing and committing a patch and reporting this issue to us! 

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1476952?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070873)*
