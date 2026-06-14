# Use-after-poison in void blink::Visitor::HandleWeakCell<blink::SVGElement>

| Field | Value |
|-------|-------|
| **Issue ID** | [40092093](https://issues.chromium.org/issues/40092093) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Linux, Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ke...@chromium.org |
| **Created** | 2018-08-02 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5058318557773824

Fuzzer: miaubiz_svg_fuzzer
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ee5e1a2d628
Crash State:
  void blink::Visitor::HandleWeakCell<blink::SVGElement>
  blink::ThreadHeap::WeakProcessing
  blink::ThreadState::MarkPhaseEpilogue
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=579734:579746

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5058318557773824

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Timeline

### sh...@chromium.org (2018-08-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-08-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-08-02)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>MemoryAllocator>GarbageCollection]

### sh...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-08-04)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-08-06)

keishi@, could you please take a look? Seems like https://chromium-review.googlesource.com/c/chromium/src/+/1125892 might be a culprit.

### ml...@chromium.org (2018-08-06)

The CL has already been reverted.

Looks like we touch a slot that has already been released during weak processing.

### cl...@chromium.org (2018-08-07)

ClusterFuzz has detected this issue as fixed in range 580848:580852.

Detailed report: https://clusterfuzz.com/testcase?key=5058318557773824

Fuzzer: miaubiz_svg_fuzzer
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ee5e1a2d628
Crash State:
  void blink::Visitor::HandleWeakCell<blink::SVGElement>
  blink::ThreadHeap::WeakProcessing
  blink::ThreadState::MarkPhaseEpilogue
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=579734:579746
Fixed: https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=580848:580852

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5058318557773824

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-08-07)

ClusterFuzz testcase 5058318557773824 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### ml...@chromium.org (2018-08-07)

Not sure this is related to https://crbug.com/chromium/870196. 

Building on mac now to try to reproduce.

### ml...@chromium.org (2018-08-07)

I am able to reproduce this with incremental marking turned on on Linux now using

out/Release/chrome --enable-blink-features=HeapIncrementalMarkingStress ~/Downloads/clusterfuzz-testcase-5058318557773824.html

The fix suggested at [1] does not fix this u-a-f.

My best guess is that we somehow have a key or value in a hashmap that is treated strongly containing a WeakMember. In this case kWeakHandlingFlag would be false and we would promptly free the object during incremental marking even though we have a slot registered.

Will try to verify these thoughts now.

### ml...@chromium.org (2018-08-07)

I could verify that in the scenario of having std::pair<WeakMember<T>, _> we indeed have kWeakHandlingFlag == false and do promptly free the backing store. Not it is just a matter of having a WeakMember that already registered a slot to cause a u-a-f during HandleWeakCell.

### sh...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f3e02276ecbbaf87c8c5143a6361582faff3ca33

commit f3e02276ecbbaf87c8c5143a6361582faff3ca33
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Thu Aug 09 11:30:03 2018

[heap] Incremental marking: Do not promptly free HashTable backings

Previously we checked whether a backing could be freed during
incremental marking using the provided Traits and kWeakHandlingFlag. It
turns out that WeakMember may also be part of otherwise strongly treated
in-place constructed objects, e.g., std::pair<WeakMember<T>,U>.

Completely turn off promptly freeing for HashTable backings during
incremental marking.

Bug: chromium:870306, chromium:757440
Change-Id: I94aacad0dbba707a4e0fb8c8119591fd413f9314
Reviewed-on: https://chromium-review.googlesource.com/1165353
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Keishi Hattori <keishi@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#581865}
[modify] https://crrev.com/f3e02276ecbbaf87c8c5143a6361582faff3ca33/third_party/blink/renderer/platform/heap/heap_allocator.cc
[modify] https://crrev.com/f3e02276ecbbaf87c8c5143a6361582faff3ca33/third_party/blink/renderer/platform/heap/heap_allocator.h
[modify] https://crrev.com/f3e02276ecbbaf87c8c5143a6361582faff3ca33/third_party/blink/renderer/platform/heap/incremental_marking_test.cc
[modify] https://crrev.com/f3e02276ecbbaf87c8c5143a6361582faff3ca33/third_party/blink/renderer/platform/wtf/allocator/partition_allocator.cc
[modify] https://crrev.com/f3e02276ecbbaf87c8c5143a6361582faff3ca33/third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h
[modify] https://crrev.com/f3e02276ecbbaf87c8c5143a6361582faff3ca33/third_party/blink/renderer/platform/wtf/hash_table.h


### sh...@chromium.org (2018-08-09)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-08-09)

+awhalley@ (Security TPM) for M69 merge review.

### ml...@chromium.org (2018-08-10)

The culprit was incremental marking which was only enabled on Canary for a few days. There's nothing to backmerge here.

### sh...@chromium.org (2018-08-10)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-10)

Rejecting merge to M69 based on https://crbug.com/chromium/870306#c18.

### aw...@chromium.org (2018-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-13)

$3,000 for the bug and a $500 clusterfuzz bonus - thanks!

### aw...@google.com (2018-08-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bea6537a032fb89f8f3fd6ee839267f9963fddfe

commit bea6537a032fb89f8f3fd6ee839267f9963fddfe
Author: Keishi Hattori <keishi@chromium.org>
Date: Wed Aug 15 04:00:10 2018

Change SMILTimeContainer::scheduled_animations_ to use ephemeron

WeakMember as part of a HashMap entry can cause unexpected clearing when incremental marking is enabled.

This CL changes SMILTimeContainer::scheduled_animations_ to use a epehemeron instead.

Bug: 870306
Cq-Include-Trybots: luci.chromium.try:linux_layout_tests_slimming_paint_v2;master.tryserver.blink:linux_trusty_blink_rel
Change-Id: I8b653825de0bc683a5151576385716141c78c454
Reviewed-on: https://chromium-review.googlesource.com/1166753
Commit-Queue: Keishi Hattori <keishi@chromium.org>
Reviewed-by: Philip Rogers <pdr@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#583156}
[modify] https://crrev.com/bea6537a032fb89f8f3fd6ee839267f9963fddfe/third_party/blink/renderer/core/svg/animation/smil_time_container.cc
[modify] https://crrev.com/bea6537a032fb89f8f3fd6ee839267f9963fddfe/third_party/blink/renderer/core/svg/animation/smil_time_container.h


### bu...@chromium.org (2018-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/82088ec92ba4d366cc1092aeee7040d110249d13

commit 82088ec92ba4d366cc1092aeee7040d110249d13
Author: Keishi Hattori <keishi@chromium.org>
Date: Wed Aug 15 14:51:09 2018

Revert "Change SMILTimeContainer::scheduled_animations_ to use ephemeron"

This reverts commit bea6537a032fb89f8f3fd6ee839267f9963fddfe.

Reason for revert: clusterfuzz found many issues
crbug.com/874396
crbug.com/874420
crbug.com/874431
crbug.com/874425
crbug.com/874430
crbug.com/874429
crbug.com/874423
crbug.com/874404

Original change's description:
> Change SMILTimeContainer::scheduled_animations_ to use ephemeron
> 
> WeakMember as part of a HashMap entry can cause unexpected clearing when incremental marking is enabled.
> 
> This CL changes SMILTimeContainer::scheduled_animations_ to use a epehemeron instead.
> 
> Bug: 870306
> Cq-Include-Trybots: luci.chromium.try:linux_layout_tests_slimming_paint_v2;master.tryserver.blink:linux_trusty_blink_rel
> Change-Id: I8b653825de0bc683a5151576385716141c78c454
> Reviewed-on: https://chromium-review.googlesource.com/1166753
> Commit-Queue: Keishi Hattori <keishi@chromium.org>
> Reviewed-by: Philip Rogers <pdr@chromium.org>
> Reviewed-by: Kentaro Hara <haraken@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#583156}

TBR=pdr@chromium.org,haraken@chromium.org,keishi@chromium.org,mlippautz@chromium.org

Change-Id: Id727b6da2d0a42341bde5d9f6c2c9f32a43d447e
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 870306
Cq-Include-Trybots: luci.chromium.try:linux_layout_tests_slimming_paint_v2;master.tryserver.blink:linux_trusty_blink_rel
Reviewed-on: https://chromium-review.googlesource.com/1175881
Reviewed-by: Keishi Hattori <keishi@chromium.org>
Commit-Queue: Keishi Hattori <keishi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#583247}
[modify] https://crrev.com/82088ec92ba4d366cc1092aeee7040d110249d13/third_party/blink/renderer/core/svg/animation/smil_time_container.cc
[modify] https://crrev.com/82088ec92ba4d366cc1092aeee7040d110249d13/third_party/blink/renderer/core/svg/animation/smil_time_container.h


### aw...@google.com (2018-08-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/870306?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092093)*
