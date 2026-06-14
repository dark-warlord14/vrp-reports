# Heap-buffer-overflow in blink::FindBuffer::RangeFromBufferIndex

| Field | Value |
|-------|-------|
| **Issue ID** | [40050795](https://issues.chromium.org/issues/40050795) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Editing |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ra...@chromium.org |
| **Created** | 2019-11-25 |
| **Bounty** | $3,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5177948977889280

Fuzzer: jesse_avalanche
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x6030000a1688
Crash State:
  blink::FindBuffer::RangeFromBufferIndex
  blink::FindBuffer::FindMatchInRange
  blink::FindStringBetweenPositions
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=716881:716883

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5177948977889280

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5177948977889280 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### cl...@chromium.org (2019-11-25)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Editing]

### cl...@chromium.org (2019-11-25)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/bcc01c0c6c4a16226262444d78461144fe54a42a (Use unicode max codepoint for delimiter instead of ORC, and skip buffers with null NGOffsetMapping).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### me...@chromium.org (2019-11-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2019-11-26)

Looks like finding the Utf16 version of maxcodepoint is crashing stuff, oops. Will fix this week

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/41baf87e8a3f63e89d3c83be05e29a8a77addf59

commit 41baf87e8a3f63e89d3c83be05e29a8a77addf59
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Mon Dec 02 10:14:15 2019

Fix crashes due to matching max codepoint by skipping invalid matches

We should check each ICU match to make sure they are valid (aren't
empty or start/end in non-offset-in-anchor positions).

Bug: 1028152
Change-Id: I1e99075a65e474cb7bf7fc14b08730f801df6541
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1939159
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/master@{#720425}

[modify] https://crrev.com/41baf87e8a3f63e89d3c83be05e29a8a77addf59/third_party/blink/renderer/core/editing/finder/find_buffer.cc
[modify] https://crrev.com/41baf87e8a3f63e89d3c83be05e29a8a77addf59/third_party/blink/renderer/core/editing/finder/find_buffer.h
[modify] https://crrev.com/41baf87e8a3f63e89d3c83be05e29a8a77addf59/third_party/blink/renderer/core/editing/finder/find_buffer_test.cc
[modify] https://crrev.com/41baf87e8a3f63e89d3c83be05e29a8a77addf59/third_party/blink/renderer/core/editing/finder/find_task_controller.cc
[modify] https://crrev.com/41baf87e8a3f63e89d3c83be05e29a8a77addf59/third_party/blink/renderer/core/page/scrolling/text_fragment_finder.cc


### cl...@chromium.org (2019-12-02)

ClusterFuzz testcase 5177948977889280 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=720424:720425

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-12-03)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-12-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-17)

Congrats! The Panel decided to reward $3,000 for this report

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-03-10)

This issue was migrated from crbug.com/chromium/1028152?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1029138]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050795)*
