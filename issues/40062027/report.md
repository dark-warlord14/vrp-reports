# Security: heap-use-after-free third_party/swiftshader/src/WSI/VkSwapchainKHR.cpp:43:13

| Field | Value |
|-------|-------|
| **Issue ID** | [40062027](https://issues.chromium.org/issues/40062027) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Vulkan |
| **Platforms** | Linux |
| **Reporter** | rh...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2022-12-03 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. This bug is found by accident, so there's no PoC.
2. If this bug is not worth to looking for or not risky at all, it's fine to set won't fix.
3. If run with '--disable-gpu', no crash occurred.

**Problem Description:**  

see asan.log

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5455.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 32.7 KB)

## Timeline

### [Deleted User] (2022-12-03)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-12-05)

It's very hard to act on this bug as it stands, do you have any more information about what you were doing when the crash was triggered?

### ad...@google.com (2022-12-06)

From the "steps to reproduce the problem" I am not hopeful that we'll get a PoC or better reproduction steps from the reporter.

So:

penghuang@ – the Security Team is unable to reproduce this issue based on information provided. If you can diagnose and fix the issue based on the ASAN log in asan.log, please do so. Please provide a comment about when this issue may have been introduced or which active release branches of Chrome may be impacted. We need to know so that we can ensure we merge fixes to the right release branches to frustrate n-day attackers, and so we can avoid release of security regressions.

If you can't figure out the root cause from the asan.log then it's OK to WontFix this, but please try. Or, if this doesn't look like a problem in your area, please pass it onto the right person.

Provisionally marking as High severity as this is a GPU process crash. We don't know if it's mitigated by user interaction or similar.

[Monorail components: Internals>GPU>Vulkan]

### gi...@appspot.gserviceaccount.com (2022-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/736d6c8e2f18554272f186a6a39fccaef4c6e753

commit 736d6c8e2f18554272f186a6a39fccaef4c6e753
Author: Peng Huang <penghuang@chromium.org>
Date: Tue Dec 06 16:25:14 2022

Defer releasing VulkanSurface

For resizing, we will defer releasing the old VulkanSwapChian with
VulkanFenceHelper. In some cases, we may release VulkanSurface before
releasing an old VulkanSwapChain. It cause use-after-release problem.
Fix the problem, by also releasing VulkanSurface with VulkanFenceHelper
as well.

Bug: 1395542
Change-Id: Iefdb29e4224dc539c4b2c23323314ae5fcd02433
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4081750
Commit-Queue: Peng Huang <penghuang@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Auto-Submit: Peng Huang <penghuang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1079797}

[modify] https://crrev.com/736d6c8e2f18554272f186a6a39fccaef4c6e753/components/viz/service/display_embedder/skia_output_device_vulkan.cc


### pe...@chromium.org (2022-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-06)

Discussed via chat, labelling appropriately.

### ad...@google.com (2022-12-06)

penghuang@ says that this is probably what causes it: "The user have to resizing a window and then close the window immediately in theory base on the stack."

Unlike most destruction bugs, I assume this doesn't require a website to close its _last_ window, so this may be remotely exploitable. I'll keep it at High.

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

Requesting merge to stable M108 because latest trunk commit (1079797) appears to be after stable branch point (1058933).

Requesting merge to beta M109 because latest trunk commit (1079797) appears to be after beta branch point (1070088).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-07)

Merge review required: M109 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-07)

Merge review required: M108 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2022-12-07)

1. Why does your merge fit within the merge criteria for these milestones?
The change fixes security issue

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/4081750

3. Have the changes been released and tested on canary?
Not yet. Waiting on Linux Dev release.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
Not a new feature

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No.

### am...@chromium.org (2022-12-09)

M109 merge approved, please merge this fix to branch 5414 
M108 merge approved, please merge this fix to branch 5359 by 10am Pacific tomorrow, Friday 9 December so this fix can be included in the M108 security refresh 

### gi...@appspot.gserviceaccount.com (2022-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7ee03b65be60b7df209aaeb923b6f3be66f35ac6

commit 7ee03b65be60b7df209aaeb923b6f3be66f35ac6
Author: Peng Huang <penghuang@chromium.org>
Date: Fri Dec 09 02:06:28 2022

Defer releasing VulkanSurface

For resizing, we will defer releasing the old VulkanSwapChian with
VulkanFenceHelper. In some cases, we may release VulkanSurface before
releasing an old VulkanSwapChain. It cause use-after-release problem.
Fix the problem, by also releasing VulkanSurface with VulkanFenceHelper
as well.

(cherry picked from commit 736d6c8e2f18554272f186a6a39fccaef4c6e753)

Bug: 1395542
Change-Id: Iefdb29e4224dc539c4b2c23323314ae5fcd02433
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4081750
Commit-Queue: Peng Huang <penghuang@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Auto-Submit: Peng Huang <penghuang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1079797}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4090065
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5414@{#563}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/7ee03b65be60b7df209aaeb923b6f3be66f35ac6/components/viz/service/display_embedder/skia_output_device_vulkan.cc


### gi...@appspot.gserviceaccount.com (2022-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e2d111054e8ad3ff28b5a4593e08ba0ab34efd69

commit e2d111054e8ad3ff28b5a4593e08ba0ab34efd69
Author: Peng Huang <penghuang@chromium.org>
Date: Fri Dec 09 03:31:06 2022

Defer releasing VulkanSurface

For resizing, we will defer releasing the old VulkanSwapChian with
VulkanFenceHelper. In some cases, we may release VulkanSurface before
releasing an old VulkanSwapChain. It cause use-after-release problem.
Fix the problem, by also releasing VulkanSurface with VulkanFenceHelper
as well.

(cherry picked from commit 736d6c8e2f18554272f186a6a39fccaef4c6e753)

Bug: 1395542
Change-Id: Iefdb29e4224dc539c4b2c23323314ae5fcd02433
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4081750
Commit-Queue: Peng Huang <penghuang@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Auto-Submit: Peng Huang <penghuang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1079797}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4089608
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1142}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/e2d111054e8ad3ff28b5a4593e08ba0ab34efd69/components/viz/service/display_embedder/skia_output_device_vulkan.cc


### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of this highly mitigated security bug. Thank you for your efforts in discovering and reporting this issue! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### pe...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### pe...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1395542?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1405684, crbug.com/chromium/1405790]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062027)*
