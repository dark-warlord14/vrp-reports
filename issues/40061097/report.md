# Security: custom_element_registry use-after-poison

| Field | Value |
|-------|-------|
| **Issue ID** | [40061097](https://issues.chromium.org/issues/40061097) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML>CustomElements |
| **Platforms** | Linux |
| **Reporter** | sp...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-09-22 |
| **Bounty** | $7,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

"when\_defined\_promise\_map\_"(WhenDefinedPromiseMap) may trigger UAP when erased after resolve of a promise

**VERSION**  

Chrome Version: 108.0.5316.0 (Developer Build) (64-bit)  

Operating System: UBUNTU20.04 64

**REPRODUCTION CASE**

run asan build of chromium with the poc.html attached

Type of crash: Use after poison

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Aviv A.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 455 B)
- [asan_log_symbolized.txt](attachments/asan_log_symbolized.txt) (text/plain, 15.5 KB)

## Timeline

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### sp...@gmail.com (2022-09-22)

[Comment Deleted]

### sp...@gmail.com (2022-09-22)

FYI
https://bugs.chromium.org/p/chromium/issues/detail?id=1366781
I reported as a regular bug by mistake,sorry.

### hc...@google.com (2022-09-22)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-22)

re: https://crbug.com/chromium/1366813#c3, thanks, duplicated and restricted view of the regular bug.

Confirmed reproducability, trying to figure out routing for this bug. One moment.

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-22)

xiaochengh@, mind taking a look at this? Reproduced on linux with asan-linux-release-1048944(108.0.5312.0 (Developer Build) (64-bit))

[Monorail components: Blink>HTML>CustomElements]

### hc...@google.com (2022-09-22)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ed87ab54b29898a96a87e8fd497425db32539350

commit ed87ab54b29898a96a87e8fd497425db32539350
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Fri Sep 23 22:44:27 2022

Ensure iterator validity in CustomElementRegistry::DefineInternal()

Currently, this function first resolves a promise, and then erases an
iterator from a hash map, but the promise resolving may run synchronous
JavaScript that invalidates the iterator.

This patch switches the ordering so that we always use the iterator when
it's valid.

Fixed: 1366813
Change-Id: Iaa6631db5f3ad47049f46ddf909f18a49e5880c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3915346
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1050816}

[add] https://crrev.com/ed87ab54b29898a96a87e8fd497425db32539350/third_party/blink/web_tests/external/wpt/custom-elements/when-defined-reentry-crash.html
[modify] https://crrev.com/ed87ab54b29898a96a87e8fd497425db32539350/third_party/blink/renderer/core/html/custom/custom_element_registry.cc


### [Deleted User] (2022-09-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-26)

This issue appears to have been introduced via 9c43194c180d8d50cc486445b891bf5090c865b0, which goes back to 105. This security fix should be backmerged.  M106 will be stable channel tomorrow and will be Extended support thereafter. Updating foundin and security impact accordingly so sheriffbot can apply appropriate merge request/review labels.

### xi...@chromium.org (2022-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

Merge approved: your change passed merge requirements and is auto-approved for M107. Please go ahead and merge the CL to branch 5304 (refs/branch-heads/5304) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b0bfc4334369bd1d44bc6507dfefc012afb7e12d

commit b0bfc4334369bd1d44bc6507dfefc012afb7e12d
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Sep 27 19:57:14 2022

[M107] Ensure iterator validity in CustomElementRegistry::DefineInternal()

Currently, this function first resolves a promise, and then erases an
iterator from a hash map, but the promise resolving may run synchronous
JavaScript that invalidates the iterator.

This patch switches the ordering so that we always use the iterator when
it's valid.

(cherry picked from commit ed87ab54b29898a96a87e8fd497425db32539350)

Fixed: 1366813
Change-Id: Iaa6631db5f3ad47049f46ddf909f18a49e5880c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3915346
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1050816}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3922738
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Auto-Submit: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/branch-heads/5304@{#203}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[add] https://crrev.com/b0bfc4334369bd1d44bc6507dfefc012afb7e12d/third_party/blink/web_tests/external/wpt/custom-elements/when-defined-reentry-crash.html
[modify] https://crrev.com/b0bfc4334369bd1d44bc6507dfefc012afb7e12d/third_party/blink/renderer/core/html/custom/custom_element_registry.cc


### xi...@chromium.org (2022-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

Merge review required: M106 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-09-27)

1. High-severity security issue & stable release blocker
2. https://chromium-review.googlesource.com/c/chromium/src/+/3915346
3. Yes
4. No
5. N/A
6. Run asan build of chromium with the poc.html attached in this issue


### am...@chromium.org (2022-09-28)

This is not a release blocking issue, was incorrectly labeled as such due to the incorrect foundin being set. Corrected in https://crbug.com/chromium/1366813#c17. This is still a sev high fixed and should be backmerged to 106, which is now Stable channel. 
M106 merge approved, please merge this fix to branch 5249 at your earliest convenience. 

### gi...@appspot.gserviceaccount.com (2022-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9bebe8549a3642672829236b40bad289d1d13a3a

commit 9bebe8549a3642672829236b40bad289d1d13a3a
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Wed Sep 28 19:09:02 2022

[M106] Ensure iterator validity in CustomElementRegistry::DefineInternal()

Currently, this function first resolves a promise, and then erases an
iterator from a hash map, but the promise resolving may run synchronous
JavaScript that invalidates the iterator.

This patch switches the ordering so that we always use the iterator when
it's valid.

(cherry picked from commit ed87ab54b29898a96a87e8fd497425db32539350)

(cherry picked from commit b0bfc4334369bd1d44bc6507dfefc012afb7e12d)

Fixed: 1366813
Change-Id: Iaa6631db5f3ad47049f46ddf909f18a49e5880c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3915346
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1050816}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3922738
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Auto-Submit: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5304@{#203}
Cr-Original-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3924290
Cr-Commit-Position: refs/branch-heads/5249@{#686}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[add] https://crrev.com/9bebe8549a3642672829236b40bad289d1d13a3a/third_party/blink/web_tests/external/wpt/custom-elements/when-defined-reentry-crash.html
[modify] https://crrev.com/9bebe8549a3642672829236b40bad289d1d13a3a/third_party/blink/renderer/core/html/custom/custom_element_registry.cc


### am...@google.com (2022-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-30)

Congratulations, Aviv! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in reporting this issue to us -- nice work! 

### am...@chromium.org (2022-09-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-03)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1366813?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1366781]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061097)*
