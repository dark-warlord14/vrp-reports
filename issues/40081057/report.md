# Use-after-poison in v8::internal::compiler::InstructionSelector::InitializeCallBuffer

| Field | Value |
|-------|-------|
| **Issue ID** | [40081057](https://issues.chromium.org/issues/40081057) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@chromium.org |
| **Assignee** | dc...@chromium.org |
| **Created** | 2014-12-22 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4845633969061888

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8

Crash Type: Use-after-poison WRITE 8
Crash Address: 0x62f0000018c0
Crash State:
  v8::internal::compiler::InstructionSelector::InitializeCallBuffer
  v8::internal::compiler::InstructionSelector::VisitCall
  v8::internal::compiler::InstructionSelector::VisitNode
  
Regressed: V8: r25720:25861

Minimized Testcase (8.88 Kb): https://cluster-fuzz.appspot.com/download/AMIfv949M6d7nRJPujP-_Sv0DVsNZXTO57veMLx4FNSfaZLGb-BNqZMLk3Bnm3l3tl53oBWtCNpyxKOvGA6-hhmyCtCKCRAsqVx6y2e5j8jPGt5dA_2xa3u2oGKRZwBRZ08Nwhm9YLZb2ftDQA5o3tjuPFdzp16MsQ

Additional requirements: Requires Gestures

Filer: mbarbella

## Timeline

### mb...@chromium.org (2014-12-22)

ishell, could you please help find an owner for this one when you get a chance?

### cl...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-23)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### is...@chromium.org (2014-12-23)

Catches assert in turbofan in debug mode. ASAN is not needed.

### bu...@chromium.org (2014-12-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/0a03b5ef188e6d9dfbbed05652eb63d31db2a7da

commit 0a03b5ef188e6d9dfbbed05652eb63d31db2a7da
Author: Benedikt Meurer <bmeurer@chromium.org>
Date: Tue Dec 23 11:00:46 2014

[turbofan] Turn DCHECK for fixed slot index into a CHECK.

This is a temporary workaround to ensure that we crash in release mode
instead of running into undefined behavior.

BUG=chromium:444681
LOG=y
R=ishell@chromium.org

Review URL: https://codereview.chromium.org/800713006

Cr-Commit-Position: refs/heads/master@{#25933}

[modify] http://crrev.com/0a03b5ef188e6d9dfbbed05652eb63d31db2a7da/src/compiler/instruction.h


### bm...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### bm...@chromium.org (2014-12-23)

So this is not a new bug, but kind of a known limitation in the way we handle operands to the register allocator. We currently have only 2^10 bits for encoding stack slots (which are used to pass parameters to javascript function calls) including sign, which means max of 512 parameters for js function calls in TurboFan. There's no easy way to extend this now, so we turned that DCHECK into a CHECK as a temporary workaround to ensure that we crash in production instead of running into undefined behavior.

We have never seen any asm.js module which passes more than 512 parameters to a function call, so this should be fine in practice for now, and we can work on a real solution later.

### cl...@chromium.org (2014-12-23)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### dc...@chromium.org (2014-12-23)

i'll take the bug, as i was planning to change the vreg portion of the instruction operand to 32 bits in the new year, making this problem go away

### cl...@chromium.org (2014-12-24)

ClusterFuzz has detected this issue as fixed in range 25932:25934.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4845633969061888

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8

Crash Type: Use-after-poison WRITE 8
Crash Address: 0x62f0000018c0
Crash State:
  v8::internal::compiler::InstructionSelector::InitializeCallBuffer
  v8::internal::compiler::InstructionSelector::VisitCall
  v8::internal::compiler::InstructionSelector::VisitNode
  
Regressed: V8: r25720:25861
Fixed: V8: r25932:25934

Minimized Testcase (8.88 Kb): https://cluster-fuzz.appspot.com/download/AMIfv949M6d7nRJPujP-_Sv0DVsNZXTO57veMLx4FNSfaZLGb-BNqZMLk3Bnm3l3tl53oBWtCNpyxKOvGA6-hhmyCtCKCRAsqVx6y2e5j8jPGt5dA_2xa3u2oGKRZwBRZ08Nwhm9YLZb2ftDQA5o3tjuPFdzp16MsQ

Additional requirements: Requires Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### dc...@chromium.org (2014-12-24)

removing release block labels

### cl...@chromium.org (2014-12-24)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### bm...@chromium.org (2014-12-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-27)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congrats - $3500 for this report as well ($3000 for the bug, $500 ClusterFuzz bonus)

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-04)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-04-06)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/444681?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081057)*
