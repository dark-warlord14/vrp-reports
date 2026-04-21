# Security: stack-use-after-scope

| Field | Value |
|-------|-------|
| **Issue ID** | [40068844](https://issues.chromium.org/issues/40068844) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | f0...@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2023-08-05 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

AddressSanitizer: stack-use-after-scope (/home/chrome/asan-linux-debug-1179983/libblink\_core.so+0x6af7998) (BuildId: ebadccb81a5fae33)

**VERSION**  

Chrome Version: asan-linux-debug-1179983 and asan-linux-release-1179983  

Operating System: Ubuntu 23.04

**REPRODUCTION CASE**

1. start a server: `python3 -m http.server`
2. ./chrome --incognito <http://127.0.0.1:8000/poc.html>

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 169 B)
- [chrome_asan_debug.log](attachments/chrome_asan_debug.log) (text/plain, 10.9 KB)

## Timeline

### [Deleted User] (2023-08-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5267970886139904.

### cl...@chromium.org (2023-08-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-08)

Detailed Report: https://clusterfuzz.com/testcase?key=5267970886139904

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Stack-use-after-scope READ 4
Crash Address: 0x7dc3eef8db20
Crash State:
  blink::RuleFeatureSet::AddFeaturesToInvalidationSetsForLogicalCombinationInHas
  blink::RuleFeatureSet::AddFeaturesToInvalidationSetsForHasPseudoClass
  blink::RuleFeatureSet::AddFeaturesToInvalidationSetsForSimpleSelector
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1015824:1015832

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5267970886139904

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-08-08)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>CSS]

### cl...@chromium.org (2023-08-08)

Automatically adding ccs based on suspected regression changelists:

Enable CSSPseudoHas by blee@igalia.com - https://chromium.googlesource.com/chromium/src/+/6fab0635006e8f6658a9b0db50855d9d374e25a2

In style_perftest, support running style recalc multiple times. by sesse@chromium.org - https://chromium.googlesource.com/chromium/src/+/7fca40e491de27121eac3a15ccd549cf3f1a8863

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label.

### sr...@google.com (2023-08-08)

[Empty comment from Monorail migration]

### fu...@chromium.org (2023-08-08)

[Empty comment from Monorail migration]

### fu...@chromium.org (2023-08-08)

https://chromium-review.googlesource.com/c/chromium/src/+/4759326

### [Deleted User] (2023-08-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5e213507a2f0d6e3c96904a710407b01493670bd

commit 5e213507a2f0d6e3c96904a710407b01493670bd
Author: Rune Lillesveen <futhark@chromium.org>
Date: Wed Aug 09 08:48:16 2023

Don't keep pointer to popped stack memory for :has()

The sibling_features pass into UpdateFeaturesFromCombinator may be
initialized to last_compound_in_adjacent_chain_features if null. The
outer while loop in
AddFeaturesToInvalidationSetsForLogicalCombinationInHas() could then
reference to the last_compound_in_adjacent_chain_features which is
popped from the stack on every outer iteration. That caused an ASAN
failure for reading stack memory that had been popped.

Instead make sure each inner iteration restarts with the same
sibling_features pointer, which seems to have been the intent here.

Bug: 1470477
Change-Id: I260c93016f8ab0d165e4b29ca1aea810bede5b97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4759326
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1181365}

[modify] https://crrev.com/5e213507a2f0d6e3c96904a710407b01493670bd/third_party/blink/renderer/core/css/rule_feature_set.cc
[add] https://crrev.com/5e213507a2f0d6e3c96904a710407b01493670bd/third_party/blink/web_tests/external/wpt/css/selectors/has-sibling-chrome-crash.html


### fu...@chromium.org (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-09)

Requesting merge to extended stable M114 because latest trunk commit (1181365) appears to be after extended stable branch point (1135570).

Requesting merge to stable M115 because latest trunk commit (1181365) appears to be after stable branch point (1148114).

Requesting merge to beta M116 because latest trunk commit (1181365) appears to be after beta branch point (1160321).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-08-09)

ClusterFuzz testcase 5267970886139904 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1181359:1181366

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-08-10)

Merge review required: M116 has already been cut for stable release.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-10)

Merge review required: M115 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-10)

Merge review required: M114 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-08-14)

117 and 116 merges approved for https://crrev.com/c/4759326
please merge this fix to 117 / branch 5938 and 116 / branch 5845 at your earliest convenience -- ty

### am...@chromium.org (2023-08-14)

to add to the above approvals, please merge to 117 by 10am Pacific tomorrow so this fix can be included in the first 117/beta
and please merge to 116 by EOD Thursday, 17 August so this fix can be included in next week's M116/Stable security refresh


### am...@chromium.org (2023-08-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9c712f720606ad8e560155565cd36688d80d8c9e

commit 9c712f720606ad8e560155565cd36688d80d8c9e
Author: Rune Lillesveen <futhark@chromium.org>
Date: Tue Aug 15 13:59:46 2023

Don't keep pointer to popped stack memory for :has()

The sibling_features pass into UpdateFeaturesFromCombinator may be
initialized to last_compound_in_adjacent_chain_features if null. The
outer while loop in
AddFeaturesToInvalidationSetsForLogicalCombinationInHas() could then
reference to the last_compound_in_adjacent_chain_features which is
popped from the stack on every outer iteration. That caused an ASAN
failure for reading stack memory that had been popped.

Instead make sure each inner iteration restarts with the same
sibling_features pointer, which seems to have been the intent here.

(cherry picked from commit 5e213507a2f0d6e3c96904a710407b01493670bd)

Bug: 1470477
Change-Id: I260c93016f8ab0d165e4b29ca1aea810bede5b97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4759326
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1181365}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4774465
Cr-Commit-Position: refs/branch-heads/5938@{#137}
Cr-Branched-From: 2b50cb4bcc2318034581a816714d9535dc38966d-refs/heads/main@{#1181205}

[modify] https://crrev.com/9c712f720606ad8e560155565cd36688d80d8c9e/third_party/blink/renderer/core/css/rule_feature_set.cc
[add] https://crrev.com/9c712f720606ad8e560155565cd36688d80d8c9e/third_party/blink/web_tests/external/wpt/css/selectors/has-sibling-chrome-crash.html


### [Deleted User] (2023-08-15)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/34e544e4dedf299211f104a2822d98ce1db80f61

commit 34e544e4dedf299211f104a2822d98ce1db80f61
Author: Rune Lillesveen <futhark@chromium.org>
Date: Tue Aug 15 15:04:39 2023

Don't keep pointer to popped stack memory for :has()

The sibling_features pass into UpdateFeaturesFromCombinator may be
initialized to last_compound_in_adjacent_chain_features if null. The
outer while loop in
AddFeaturesToInvalidationSetsForLogicalCombinationInHas() could then
reference to the last_compound_in_adjacent_chain_features which is
popped from the stack on every outer iteration. That caused an ASAN
failure for reading stack memory that had been popped.

Instead make sure each inner iteration restarts with the same
sibling_features pointer, which seems to have been the intent here.

(cherry picked from commit 5e213507a2f0d6e3c96904a710407b01493670bd)

Bug: 1470477
Change-Id: I260c93016f8ab0d165e4b29ca1aea810bede5b97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4759326
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1181365}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4777251
Cr-Commit-Position: refs/branch-heads/5845@{#1482}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/34e544e4dedf299211f104a2822d98ce1db80f61/third_party/blink/renderer/core/css/rule_feature_set.cc
[add] https://crrev.com/34e544e4dedf299211f104a2822d98ce1db80f61/third_party/blink/web_tests/external/wpt/css/selectors/has-sibling-chrome-crash.html


### fu...@chromium.org (2023-08-15)

> LTS Milestone M114
> 
> This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
> 1. Was this issue a regression for the milestone it was found in?

No, this seems to have been in since M104 which is before the feature was enabled in M105.

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.


### vo...@google.com (2023-08-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-18)

Congratulations! The VRP Panel has decided to award you $2,000 for this report, as this appears to be an OOB read / information leak / user information disclosure. A member of our finance team will be in touch with you soon to arrange payment. In the meantime, please let us know what name or other identifier you would like us to us in acknowledging you for this finding. Thank you for your efforts and reporting this issue to us. 

### f0...@gmail.com (2023-08-18)

Reporter credit: Francisco Alonso (@revskills)

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-22)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-24)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-08-24)

1. One https://crrev.com/c/4809702
2. Low - small change, no conflicts
3. M116, M117
4. Yes

### gm...@google.com (2023-08-24)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### gm...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c6afc6586a6b0a70acc2b4ba448df4e9e46c022e

commit c6afc6586a6b0a70acc2b4ba448df4e9e46c022e
Author: Rune Lillesveen <futhark@chromium.org>
Date: Thu Sep 07 15:27:40 2023

[M114-LTS] Don't keep pointer to popped stack memory for :has()

The sibling_features pass into UpdateFeaturesFromCombinator may be
initialized to last_compound_in_adjacent_chain_features if null. The
outer while loop in
AddFeaturesToInvalidationSetsForLogicalCombinationInHas() could then
reference to the last_compound_in_adjacent_chain_features which is
popped from the stack on every outer iteration. That caused an ASAN
failure for reading stack memory that had been popped.

Instead make sure each inner iteration restarts with the same
sibling_features pointer, which seems to have been the intent here.

(cherry picked from commit 5e213507a2f0d6e3c96904a710407b01493670bd)

(cherry picked from commit 34e544e4dedf299211f104a2822d98ce1db80f61)

Bug: 1470477
Change-Id: I260c93016f8ab0d165e4b29ca1aea810bede5b97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4759326
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1181365}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4777251
Cr-Original-Commit-Position: refs/branch-heads/5845@{#1482}
Cr-Original-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4809702
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1587}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/c6afc6586a6b0a70acc2b4ba448df4e9e46c022e/third_party/blink/renderer/core/css/rule_feature_set.cc
[add] https://crrev.com/c6afc6586a6b0a70acc2b4ba448df4e9e46c022e/third_party/blink/web_tests/external/wpt/css/selectors/has-sibling-chrome-crash.html


### rz...@google.com (2023-09-07)

[Empty comment from Monorail migration]

### rz...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1470477?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068844)*
