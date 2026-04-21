# Security: UAF in validation_message_overlay_delegate

| Field | Value |
|-------|-------|
| **Issue ID** | [40061660](https://issues.chromium.org/issues/40061660) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sp...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2022-11-08 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

use after free in ValidationMessageOverlayDelegate::GetElementById

Chrome Version: 109.0.5410.0 (Developer Build) (64-bit)  

Operating System: UBUNTU64

**REPRODUCTION CASE**

run asan build of chromium with the poc attached

Type of crash: Use after free

**CREDIT INFORMATION**  

Reporter credit: Aviv A.

## Attachments

- [asan_symbolize.txt](attachments/asan_symbolize.txt) (text/plain, 29.0 KB)
- [poc1.html](attachments/poc1.html) (text/plain, 635 B)

## Timeline

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6155215922462720.

### wf...@chromium.org (2022-11-09)

Thanks for your report, and your great proof of concept. I can reproduce this. Triage will follow shortly.

[Monorail components: Blink>Forms]

### wf...@chromium.org (2022-11-09)

Adding some forms folks. Will diagnose regression range(s) shortly.

### wf...@chromium.org (2022-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-09)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-09)

[Empty comment from Monorail migration]

### ja...@chromium.org (2022-11-09)

I am happy to look into this, but since an owner was assigned and so many people have been cc'd I don't know if anyone has started yet.

### wf...@chromium.org (2022-11-09)

jarhar@chromium.org thank you! :) I've assigned the bug to you. Initial owner assignment is sometimes guesswork, and the sheriff guesses wrong.

### cl...@chromium.org (2022-11-10)

Detailed Report: https://clusterfuzz.com/testcase?key=6155215922462720

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60f0000515c8
Crash State:
  blink::ValidationMessageOverlayDelegate::GetElementById
  blink::ValidationMessageOverlayDelegate::CreatePage
  blink::ValidationMessageClientImpl::ShowValidationMessage
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=762928:762949

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6155215922462720

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ja...@chromium.org (2022-11-10)

ccing my code reviewer

### ja...@chromium.org (2022-11-10)

patch is up: https://chromium-review.googlesource.com/c/chromium/src/+/4019655

### [Deleted User] (2022-11-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a37b66ded21af7ff1442bddd2ec3a0845535b3d6

commit a37b66ded21af7ff1442bddd2ec3a0845535b3d6
Author: Joey Arhar <jarhar@chromium.org>
Date: Tue Nov 15 16:50:15 2022

Avoid use-after-free in ValidationMessageOverlayDelegate

When ValidationMessageOverlayDelegate calls
ForceSynchronousDocumentInstall, it can somehow cause another validation
overlay to be created and delete the ValidationMessageOverlayDelegate.
This patch avoids additional code from being run inside the deleted
ValidationMessageOverlayDelegate.

Fixed: 1382581
Change-Id: I044f91ecb55c77c4a5c40030b6856fc9a8ac7f6f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4019655
Reviewed-by: David Baron <dbaron@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1071652}

[modify] https://crrev.com/a37b66ded21af7ff1442bddd2ec3a0845535b3d6/third_party/blink/renderer/core/page/validation_message_overlay_delegate.h
[add] https://crrev.com/a37b66ded21af7ff1442bddd2ec3a0845535b3d6/third_party/blink/web_tests/external/wpt/html/semantics/forms/constraints/reportValidity-crash.html
[modify] https://crrev.com/a37b66ded21af7ff1442bddd2ec3a0845535b3d6/third_party/blink/renderer/core/page/validation_message_overlay_delegate.cc


### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

Requesting merge to extended stable M106 because latest trunk commit (1071652) appears to be after extended stable branch point (1036826).

Requesting merge to stable M107 because latest trunk commit (1071652) appears to be after stable branch point (1047731).

Requesting merge to beta M108 because latest trunk commit (1071652) appears to be after beta branch point (1058933).

Requesting merge to dev M109 because latest trunk commit (1071652) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-16)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-16)

Merge review required: M108 has already been cut for stable release.

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

### [Deleted User] (2022-11-16)

Merge review required: M107 is already shipping to stable.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-16)

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

### gi...@appspot.gserviceaccount.com (2022-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fb2bc66e8483c76ce56d2021e2ff82883bd16f87

commit fb2bc66e8483c76ce56d2021e2ff82883bd16f87
Author: Joey Arhar <jarhar@chromium.org>
Date: Wed Nov 16 20:36:16 2022

Avoid use-after-free in ValidationMessageOverlayDelegate

When ValidationMessageOverlayDelegate calls
ForceSynchronousDocumentInstall, it can somehow cause another validation
overlay to be created and delete the ValidationMessageOverlayDelegate.
This patch avoids additional code from being run inside the deleted
ValidationMessageOverlayDelegate.

(cherry picked from commit a37b66ded21af7ff1442bddd2ec3a0845535b3d6)

Fixed: 1382581
Change-Id: I044f91ecb55c77c4a5c40030b6856fc9a8ac7f6f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4019655
Reviewed-by: David Baron <dbaron@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1071652}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4032526
Auto-Submit: Joey Arhar <jarhar@chromium.org>
Commit-Queue: David Baron <dbaron@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#85}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/fb2bc66e8483c76ce56d2021e2ff82883bd16f87/third_party/blink/renderer/core/page/validation_message_overlay_delegate.h
[add] https://crrev.com/fb2bc66e8483c76ce56d2021e2ff82883bd16f87/third_party/blink/web_tests/external/wpt/html/semantics/forms/constraints/reportValidity-crash.html
[modify] https://crrev.com/fb2bc66e8483c76ce56d2021e2ff82883bd16f87/third_party/blink/renderer/core/page/validation_message_overlay_delegate.cc


### [Deleted User] (2022-11-16)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-11-16)

ClusterFuzz testcase 6155215922462720 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1071641:1071655

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### vo...@google.com (2022-11-17)

[Empty comment from Monorail migration]

### vo...@google.com (2022-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-18)

There are no further releases for 106/Extended and 107/Stable planned; Stable RC for M108 has already been cut, we have some time before stable respin, so will return to reassess for merge approval to 108 early next week. 

### gm...@google.com (2022-11-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-21)

M108 merge approved, please merge this fix to branch 5359 at your earliest convenience -- ty 

### gi...@appspot.gserviceaccount.com (2022-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/42e15c2055c4969f2b234f704a15a7a874d58c5e

commit 42e15c2055c4969f2b234f704a15a7a874d58c5e
Author: Joey Arhar <jarhar@chromium.org>
Date: Tue Nov 22 00:12:31 2022

Avoid use-after-free in ValidationMessageOverlayDelegate

When ValidationMessageOverlayDelegate calls
ForceSynchronousDocumentInstall, it can somehow cause another validation
overlay to be created and delete the ValidationMessageOverlayDelegate.
This patch avoids additional code from being run inside the deleted
ValidationMessageOverlayDelegate.

(cherry picked from commit a37b66ded21af7ff1442bddd2ec3a0845535b3d6)

Fixed: 1382581
Change-Id: I044f91ecb55c77c4a5c40030b6856fc9a8ac7f6f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4019655
Reviewed-by: David Baron <dbaron@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1071652}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4043489
Commit-Queue: David Baron <dbaron@chromium.org>
Auto-Submit: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#911}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/42e15c2055c4969f2b234f704a15a7a874d58c5e/third_party/blink/renderer/core/page/validation_message_overlay_delegate.h
[add] https://crrev.com/42e15c2055c4969f2b234f704a15a7a874d58c5e/third_party/blink/web_tests/external/wpt/html/semantics/forms/constraints/reportValidity-crash.html
[modify] https://crrev.com/42e15c2055c4969f2b234f704a15a7a874d58c5e/third_party/blink/renderer/core/page/validation_message_overlay_delegate.cc


### vo...@google.com (2022-11-22)

1. https://crrev.com/c/4033088
2. Low, no conflicts
3. Stable M108
4. Yes

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations, Aviv! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### gm...@google.com (2022-12-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5150eee00f2f90fddb297772a38c6744b95d8b3f

commit 5150eee00f2f90fddb297772a38c6744b95d8b3f
Author: Joey Arhar <jarhar@chromium.org>
Date: Wed Dec 07 03:52:32 2022

[M102-LTS] Avoid use-after-free in ValidationMessageOverlayDelegate

When ValidationMessageOverlayDelegate calls
ForceSynchronousDocumentInstall, it can somehow cause another validation
overlay to be created and delete the ValidationMessageOverlayDelegate.
This patch avoids additional code from being run inside the deleted
ValidationMessageOverlayDelegate.

(cherry picked from commit a37b66ded21af7ff1442bddd2ec3a0845535b3d6)

(cherry picked from commit fb2bc66e8483c76ce56d2021e2ff82883bd16f87)

Fixed: 1382581
Change-Id: I044f91ecb55c77c4a5c40030b6856fc9a8ac7f6f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4019655
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1071652}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4032526
Auto-Submit: Joey Arhar <jarhar@chromium.org>
Commit-Queue: David Baron <dbaron@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5414@{#85}
Cr-Original-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4033088
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#1398}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/5150eee00f2f90fddb297772a38c6744b95d8b3f/third_party/blink/renderer/core/page/validation_message_overlay_delegate.h
[add] https://crrev.com/5150eee00f2f90fddb297772a38c6744b95d8b3f/third_party/blink/web_tests/external/wpt/html/semantics/forms/constraints/reportValidity-crash.html
[modify] https://crrev.com/5150eee00f2f90fddb297772a38c6744b95d8b3f/third_party/blink/renderer/core/page/validation_message_overlay_delegate.cc


### vo...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1382581?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061660)*
