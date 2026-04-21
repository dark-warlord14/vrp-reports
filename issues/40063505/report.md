# Security: Bypass https://chromium-review.googlesource.com/c/chromium/src/+/4294941 using upper-cased file: protocol (Source maps support for file:// URLs gives devtools_page extensions local file access)

| Field | Value |
|-------|-------|
| **Issue ID** | [40063505](https://issues.chromium.org/issues/40063505) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2023-03-10 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

<https://chromium-review.googlesource.com/c/chromium/src/+/4294941> patched a bypass to <https://bugs.chromium.org/p/chromium/issues/detail?id=1349146>. But I found that is possible to bypass this new fix on Canary. By using camel case (ie. File:etc/hosts

**VERSION**  

Chrome Version: 113.0.5640.0 (Official Build) canary (x86\_64)  

Operating System: macOS Version 11.7 (Build 20G817)

**REPRODUCTION CASE**

1. Download Canary to absorb the fix for <https://chromium-review.googlesource.com/c/chromium/src/+/4294941>.
2. Download the attached extension and set such that it no local file access (but devtools access)
3. Inspect element and notice that an alert box with /etc/hosts content popped

## Attachments

- [background.js](attachments/background.js) (text/plain, 184 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [devtools.js](attachments/devtools.js) (text/plain, 216 B)
- [manifest.json](attachments/manifest.json) (text/plain, 201 B)
- [background.js](attachments/background.js) (text/plain, 194 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [devtools.js](attachments/devtools.js) (text/plain, 216 B)
- [manifest.json](attachments/manifest.json) (text/plain, 201 B)

## Timeline

### ha...@gmail.com (2023-03-10)

[Comment Deleted]

### ha...@gmail.com (2023-03-10)

Reason why the new fix is insufficient: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4295641/2/front_end/models/extensions/ExtensionAPI.ts

Here, we can see that we check if the resource URL startsWith file:, therefore if the resource URL starts with File: instead it completely bypasses this checking. As mentioned in https://crbug.com/chromium/1423258#c1, best way to solve this would be to use new URL().

### [Deleted User] (2023-03-10)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-03-10)

Here are the files if you would like to test the bug on Chrome Canary for Windows. The original one works for MacOS and I guess Linux too.

### ha...@gmail.com (2023-03-10)

Also the title should be corrected to use the fix https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4295641, the one in the title, https://chromium-review.googlesource.com/c/chromium/src/+/4294941 is the test for https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4295641.

### ma...@chromium.org (2023-03-10)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions]

### [Deleted User] (2023-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/9169474e0b2de2564fbf29cab349f3528f3fb0a1

commit 9169474e0b2de2564fbf29cab349f3528f3fb0a1
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Mar 13 08:45:13 2023

Also handle uppercase FILE: URLs.

Bug: 1423258
Change-Id: Ibc92cd14a3dd11871ea7a98c416334c32fdd653a
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4333916
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Wolfgang Beyer <wolfi@chromium.org>
Commit-Queue: Wolfgang Beyer <wolfi@chromium.org>

[modify] https://crrev.com/9169474e0b2de2564fbf29cab349f3528f3fb0a1/front_end/models/extensions/ExtensionAPI.ts


### ds...@chromium.org (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-15)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-15)

M112 merge approved, please merge this fix to branch 5615 at your earliest convenience -- thank you!

### gi...@appspot.gserviceaccount.com (2023-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/c18b0bc6bdf1167d90bf504d614e23770d1bb8c2

commit c18b0bc6bdf1167d90bf504d614e23770d1bb8c2
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Mar 13 08:45:13 2023

[M112] Also handle uppercase FILE: URLs.

Bug: 1423258
Change-Id: Ibc92cd14a3dd11871ea7a98c416334c32fdd653a
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4333916
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Wolfgang Beyer <wolfi@chromium.org>
Commit-Queue: Wolfgang Beyer <wolfi@chromium.org>
(cherry picked from commit 9169474e0b2de2564fbf29cab349f3528f3fb0a1)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4345492

[modify] https://crrev.com/c18b0bc6bdf1167d90bf504d614e23770d1bb8c2/front_end/models/extensions/ExtensionAPI.ts


### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations, Axel! The VRP Panel has decided to award you $5,000 for this report. Nice catch! Thank you for your efforts and reporting this issue to us! 

### gi...@appspot.gserviceaccount.com (2023-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/26dfd4e48b0e7771b69fd45b5e51d72a9e1062c4

commit 26dfd4e48b0e7771b69fd45b5e51d72a9e1062c4
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Mar 27 18:04:59 2023

Extended DevToolsExtensionFileAccessTest to cover mixed case scheme

Bug: 1423258
Change-Id: I414d6c4128612d948d7d9a0ae84940d20a0165e3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4372948
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Alex Gough <ajgo@chromium.org>
Reviewed-by: Alex Gough <ajgo@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1122527}

[modify] https://crrev.com/26dfd4e48b0e7771b69fd45b5e51d72a9e1062c4/chrome/browser/devtools/devtools_browsertest.cc


### gi...@appspot.gserviceaccount.com (2023-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/b2e370509bf6ce159ac9ea48a72d66b4432a571b

commit b2e370509bf6ce159ac9ea48a72d66b4432a571b
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Mar 24 12:50:43 2023

Use built-in URL class instead of string comparison in file URL check.

Bug: 1423258
Change-Id: Ie6ea865fbe363c138b372d45d98daf1db6434671
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4370246
Commit-Queue: Alex Gough <ajgo@chromium.org>
Reviewed-by: Alex Gough <ajgo@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/b2e370509bf6ce159ac9ea48a72d66b4432a571b/front_end/models/extensions/ExtensionAPI.ts


### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-07-06)

[Empty comment from Monorail migration]

### gm...@google.com (2023-07-13)

[Comment Deleted]

### gm...@google.com (2023-07-13)

@voit, please evaluate for LTS-108.

### vo...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-07-17)

1. https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4685532
2. Low - simple change with minimal conflicts.
3. M112
4. Yes

### gm...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/4cacb948b55744f67af7020c5e1faf2412f02944

commit 4cacb948b55744f67af7020c5e1faf2412f02944
Author: Zakhar Voit <voit@google.com>
Date: Mon Jul 17 01:03:37 2023

[M108-LTS] Use built-in URL class instead of string comparison in file URL check.

Bug: 1423258
Change-Id: Ie6ea865fbe363c138b372d45d98daf1db6434671
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4370246
Commit-Queue: Alex Gough <ajgo@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit b2e370509bf6ce159ac9ea48a72d66b4432a571b)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4685532
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/4cacb948b55744f67af7020c5e1faf2412f02944/front_end/models/extensions/ExtensionAPI.ts


### vo...@google.com (2023-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1423258?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063505)*
