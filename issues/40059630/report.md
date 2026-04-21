# Heap-use-after-free in blink::NGHighlightPainter::NGHighlightPainter

| Field | Value |
|-------|-------|
| **Issue ID** | [40059630](https://issues.chromium.org/issues/40059630) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fu...@chromium.org |
| **Created** | 2022-05-10 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5627760148152320

Fuzzer: miaubiz_css_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x11af675c6f74
Crash State:
  blink::NGHighlightPainter::NGHighlightPainter
  blink::NGTextFragmentPainter::Paint
  blink::NGBoxFragmentPainter::PaintTextItem
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=1001461:1001462

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5627760148152320

Issue filed automatically.



## Timeline

### [Deleted User] (2022-05-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-05-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-05-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Paint]

### cl...@chromium.org (2022-05-10)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/c5f66f4464a569b6735ce51a01d2cb6c57a8ec6c (Replace cached ::first-line style from getComputedStyle).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### fu...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-05-11)

Culprit reverted: https://chromium-review.googlesource.com/c/chromium/src/+/3641525

### cl...@chromium.org (2022-05-11)

ClusterFuzz testcase 6542923189649408 is verified as fixed in https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=1001970:1001986

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2022-05-11)

This crash occurs very frequently on windows platform and is likely preventing the fuzzer miaubiz_css_fuzzer from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add the ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### [Deleted User] (2022-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-14)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M103. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-14)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-05-18)

revert already landed in 103; no merge needed here 

### am...@chromium.org (2022-05-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-18)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-24)

Congratulations! The VRP Panel has decided to reward you $5,000 for this report + $1,000 fuzzer bonus. Thank you for your contributions to Chrome Fuzzing! 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-17)

This issue was migrated from crbug.com/chromium/1324302?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1324305, crbug.com/chromium/1324363, crbug.com/chromium/1324364, crbug.com/chromium/1324368, crbug.com/chromium/1324369, crbug.com/chromium/1324470, crbug.com/chromium/1324471, crbug.com/chromium/1324593, crbug.com/chromium/1324712]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059630)*
