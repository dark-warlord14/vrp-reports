# UNKNOWN in v8::internal::Invoke

| Field | Value |
|-------|-------|
| **Issue ID** | [40081070](https://issues.chromium.org/issues/40081070) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@chromium.org |
| **Assignee** | bm...@chromium.org |
| **Created** | 2014-12-28 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5797815971217408

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8_dbg

Crash Type: UNKNOWN
Crash Address: 0x6310800507f2
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Regressed: V8: r25900:25908

Minimized Testcase (10.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97k81jqC1aCtBRlG6FvUPYtlRnoVyIHqJK2sH4I84UZELTH_3fM6yXgQFIO5hSaycoBkbzqD5q6ARaXFecJ1zrHs9Yc4jSTz99j1DbKT9d5MHkxtPZACLWBromK_F1eNx5bPiZEnebtwqAZ8h9CD4C1ou7xjw

Filer: machenbach

## Timeline

### ma...@chromium.org (2014-12-28)

PTAL. Whoever is available.

### rs...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### bm...@chromium.org (2014-12-28)

Will try to look into this tomorrow...

### bm...@chromium.org (2014-12-28)

Ok, got a quickfix waiting for review (https://codereview.chromium.org/825403002).

### cl...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-29)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-12-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ef41f7068457bec8988732ce489f141ae67ad425

commit ef41f7068457bec8988732ce489f141ae67ad425
Author: bmeurer <bmeurer@chromium.org>
Date: Mon Dec 29 10:01:05 2014

[turbofan] Fix invalid bounds check with overflowing offset.

TEST=mjsunit/compiler/regress-445267
BUG=chromium:445267
LOG=y

Review URL: https://codereview.chromium.org/825403002

Cr-Commit-Position: refs/heads/master@{#25945}

[modify] http://crrev.com/ef41f7068457bec8988732ce489f141ae67ad425/src/compiler/x64/instruction-selector-x64.cc
[add] http://crrev.com/ef41f7068457bec8988732ce489f141ae67ad425/test/mjsunit/compiler/regress-445267.js


### bm...@chromium.org (2014-12-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-30)

ClusterFuzz has detected this issue as fixed in range 25944:25945.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5797815971217408

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8_dbg

Crash Type: UNKNOWN
Crash Address: 0x6310800507f2
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Regressed: V8: r25900:25908
Fixed: V8: r25944:25945

Minimized Testcase (10.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97k81jqC1aCtBRlG6FvUPYtlRnoVyIHqJK2sH4I84UZELTH_3fM6yXgQFIO5hSaycoBkbzqD5q6ARaXFecJ1zrHs9Yc4jSTz99j1DbKT9d5MHkxtPZACLWBromK_F1eNx5bPiZEnebtwqAZ8h9CD4C1ou7xjw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### bu...@chromium.org (2015-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8622f1c04708036830094d0e897a832086363db3

commit 8622f1c04708036830094d0e897a832086363db3
Author: Michael Achenbach <machenbach@chromium.org>
Date: Sat Jan 03 10:20:48 2015

Version 3.31.74.1 (cherry-pick)

Merged eeec886e5f5893fef86e9be08990de5b1272ea46
Merged 4f9193e047d50b1ffbca95e8185576af82c722b3
Merged bbe8b00d6a5704f547f8dcf78ff462c92ce10c17
Merged 4a8623c637b2847849ecb5a5a76af6809d152e57
Merged 96143d193143daab45b14cee840f59954d7a1036
Merged b5e8dd0e1228972eb579fd155442c1eb846b286b
Merged ef41f7068457bec8988732ce489f141ae67ad425
Merged 643ed5b8bec269c86cf68b93ed79de9c2410cd46
Merged a64ac4575a235fa7efc44b4f56a34c20e5634d9c
Merged cf866b7c612c25bace7d0f0ceb12456e5ad24d7f
Merged fb2643c858c96a783fced0c730a6ff89ea60eda5
Merged 26fce420dadfb8cd74289f31bfaeb36806f2386e

[turbofan] Deinlinify OperatorProperties implementation.

[turbofan] Cache float32 constants on the JSGraph level.

Don't pass -pie when building a shared library build on android

[turbofan] Turn IrOpcode::Mnemonic() into a table lookup.

Remove UNREACHABLE() statements from sys-info.cc

[turbofan] Raise max virtual registers and call parameter limit.

[turbofan] Fix invalid bounds check with overflowing offset.

[turbofan] Fix missing MachineOperator unittest.

Fix %NeverOptimizeFunction() intrinsic.

[x64] Rearrange code for OOB integer loads.

[turbofan] Truncation of Bit/Word8/16 to Word32 is a no-op.

[turbofan] Cache common Loop, Merge and Parameter operators.

BUG=chromium:445267,chromium:445732,chromium:445858,chromium:445859,v8:3544,v8:3786,v8:3792
LOG=N
TBR=bmeurer@chromium.org

Review URL: https://codereview.chromium.org/834003002

Cr-Commit-Position: refs/branch-heads/3.31@{#2}
Cr-Branched-From: ed47c2dcd9a30eea73c9cf7b7f120f2d089ad938-refs/heads/candidates@{#25349}

[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/BUILD.gn
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/build/android.gypi
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/base/sys-info.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/basic-block-instrumentor.cc
[add] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/common-node-cache.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/common-node-cache.h
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/common-operator.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/common-operator.h
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/graph-builder.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/graph-replay.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/graph.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/instruction.h
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/js-context-specialization.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/js-graph.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/machine-operator.h
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/node-cache.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/node-cache.h
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/node-properties-inl.h
[add] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/opcodes.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/opcodes.h
[rename] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/operator-properties.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/operator-properties.h
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/simplified-lowering.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/x64/code-generator-x64.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/compiler/x64/instruction-selector-x64.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/runtime/runtime-test.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/src/version.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/cctest/compiler/simplified-graph-builder.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/cctest/compiler/test-machine-operator-reducer.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/cctest/compiler/test-node-cache.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/cctest/compiler/test-typer.cc
[add] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/mjsunit/compiler/regress-3786.js
[add] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/mjsunit/compiler/regress-445267.js
[add] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/mjsunit/compiler/regress-445732.js
[add] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/mjsunit/compiler/regress-445858.js
[add] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/mjsunit/compiler/regress-445859.js
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/unittests/compiler/change-lowering-unittest.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/unittests/compiler/common-operator-unittest.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/unittests/compiler/control-equivalence-unittest.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/unittests/compiler/js-operator-unittest.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/unittests/compiler/machine-operator-unittest.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/unittests/compiler/node-test-utils.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/unittests/compiler/simplified-operator-unittest.cc
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/test/unittests/unittests.gyp
[modify] http://crrev.com/8622f1c04708036830094d0e897a832086363db3/tools/gyp/v8.gyp


### in...@chromium.org (2015-01-05)

Can this result in a OOB write ? or is it just read.

### bm...@chromium.org (2015-01-07)

This applies to both reads and writes.

### ti...@google.com (2015-01-22)

Congrats - $3500 for this report ($3000 for the bug, +$500 ClusterFuzz bonus).

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-06)

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

This issue was migrated from crbug.com/chromium/445267?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081070)*
