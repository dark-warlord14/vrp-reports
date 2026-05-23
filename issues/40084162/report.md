# Security: Due to out of index of 'Node' object , attacker can control all contents of 'Node' object

| Field | Value |
|-------|-------|
| **Issue ID** | [40084162](https://issues.chromium.org/issues/40084162) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **CVE IDs** | CVE-2016-1665 |
| **Reporter** | gk...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2016-04-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

On multi-processable environment, I can control the all contents of object named ‘Node’ that is used for optimization in v8 engine.  

When v8 engine optimizes the code which includes ’with’ statement, it occurs out of index on ‘Node’ object.  

I don’t know why out of index occurs exactly, optimization procedure with multi-threading has some problem such as race condition.  

If I allocate a fake object at the address of ‘Node’ object that out of index indicates, I can control the all contents of ‘Node’ object.  

Making some fake ‘Node’ object to exploit the chrome browser may be highly possible.

**VERSION**  

Chrome Version: 50.0.2661.87 m (32bit) [stable]  

Operating System: Windows 7( I tested on only Windows 7, but It will crash on any OS which supports multi-processing.)

**REPRODUCTION CASE**  

I attached ‘poc.html’.  

This bug is based on multi-threading, my PoC code may not be 100% reliable.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: v8  

**Crash State: [see link above: stack trace, registers, exception record]**  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Program Files (x86)\Google\Chrome\Application\50.0.2661.87\chrome\_child.dll -  

eax=41414141 ebx=0025e098 ecx=40b94400 edx=00000000 esi=04268120 edi=04268128  

eip=5e5a22bc esp=0025e008 ebp=0025e008 iopl=0 nv up ei pl zr na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010246  

chrome\_child!GetHandleVerifier+0xa87e8f:  

5e5a22bc 6683780429 cmp word ptr [eax+4],29h ds:002b:41414145=????  

0:000> dd ecx  

40b94400 41414141 41414141 41414141 41414141  

40b94410 41414141 41414141 41414141 41414141  

40b94420 41414141 41414141 41414141 41414141  

40b94430 41414141 41414141 41414141 41414141  

40b94440 41414141 41414141 41414141 41414141  

40b94450 41414141 41414141 41414141 41414141  

40b94460 41414141 41414141 41414141 41414141  

40b94470 41414141 41414141 41414141 41414141

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 321 B)
- [poc.html](attachments/poc.html) (text/plain, 312 B)
- [d8_poc.js](attachments/d8_poc.js) (text/plain, 339 B)

## Timeline

### va...@chromium.org (2016-04-24)

Hi there, thanks for reporting the issue but I am unable to reproduce it.
I'm marking this as WontFix but please open it back if you have a more reliable PoC.

### gk...@gmail.com (2016-04-24)

I tested OSX(Intel(R) Core(TM) i5-4278U CPU @ 2.60GHz), Windows7(Intel(R) Core(TM) i5-4690 CPU @ 3.50GHz)
In my test environment, 'poc.html' works well.
I think your test environment does not support multi-processing.
This crash requires multi-processable environment.
Please check it again.
Thanks

### gk...@gmail.com (2016-04-24)

'This bug is based on multi-threading, my PoC code may not be 100% reliable.' means that poc code always occurs crash, but it sometimes control the all contents of 'Node' object.
Thnaks

### gk...@gmail.com (2016-04-24)

The number of processor core should be larger than 1. It means that my poc works on 2, 3, 4... processor cores.

### cl...@chromium.org (2016-04-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5869986622472192

### mb...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-26)

+v8 sheriffs

I haven't been able to reproduce this.

### gk...@gmail.com (2016-04-26)

I attach new poc.html file that remove 'alert'.
And this bug is based on multi-threading, you should test this on multi-core.

### gk...@gmail.com (2016-04-26)

And v8 version is 5.0.71.32.

### ma...@chromium.org (2016-04-26)

Cc stability and clusterfuzz sheriffs.

### jk...@chromium.org (2016-04-26)

I can repro with M50 but not with M51. d8 built from branch-heads/5.0 reproduces it too. Bisecting where it got fixed.

### jk...@chromium.org (2016-04-26)

The repro no longer crashes after d00da47b61462681b48e48bdff4a80a33da1a6d6. This commit was backmerged to the 5.0 branch in https://chromium.googlesource.com/v8/v8/+/0843a173996f5f63eca749d6fe8c20d4813537d9 but subsequently reverted from the branch in https://chromium.googlesource.com/v8/v8/+/d5cf399450548164e69521ecd739ad9b6c613e67 because it broke something.

Before the fix, debug builds crashed as follows:

#
# Fatal error in ../src/compiler/verifier.cc, line 1225
# Check failed: OperatorProperties::GetTotalInputCount(node->op()) == node->InputCount() (9 vs. 8).
#

==== C stack trace ===============================

 1: V8_Fatal
 2: v8::internal::compiler::Verifier::VerifyNode(v8::internal::compiler::Node*)
 3: v8::internal::compiler::NodeProperties::ChangeOp(v8::internal::compiler::Node*, v8::internal::compiler::Operator const*)
 4: v8::internal::compiler::JSGenericLowering::ReplaceWithRuntimeCall(v8::internal::compiler::Node*, v8::internal::Runtime::FunctionId, int)
 5: v8::internal::compiler::JSGenericLowering::LowerJSCreateWithContext(v8::internal::compiler::Node*)
 6: v8::internal::compiler::JSGenericLowering::Reduce(v8::internal::compiler::Node*)
 7: v8::internal::compiler::GraphReducer::Reduce(v8::internal::compiler::Node*)
 8: v8::internal::compiler::GraphReducer::ReduceTop()
 9: v8::internal::compiler::GraphReducer::ReduceNode(v8::internal::compiler::Node*)
10: v8::internal::compiler::GraphReducer::ReduceGraph()
11: v8::internal::compiler::GenericLoweringPhase::Run(v8::internal::compiler::PipelineData*, v8::internal::Zone*)
12: void v8::internal::compiler::Pipeline::Run<v8::internal::compiler::GenericLoweringPhase>()
13: v8::internal::compiler::Pipeline::GenerateCode()
14: v8::internal::OptimizedCompileJob::CreateGraph()

Whereas release builds crash with a NULL deref in DeadCodeElimination::Reduce, see e.g. go/crash/e4a9c4d200000000.

Based on these findings, I don't see how this bug has security implications; however it is a crash and as such deserves fixing. Benedikt, what can we do to fix this on the 5.0 branch? (See #8 for a reliable repro, the content of the <script>...</script> tag also works in d8.)

### rs...@chromium.org (2016-04-26)

[Empty comment from Monorail migration]

### rs...@chromium.org (2016-04-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### gk...@gmail.com (2016-04-27)

I attach the d8_poc.js and you can execute on v8.

### bm...@chromium.org (2016-04-27)

Well the fix was already in 5.0 and got reverted because of some funky mjsunit test (which is just useless anyway, since it tests comparison of undetectable JSReceivers, which doesn't matter in practice). I don't know why the security fix was reverted and not relanded back then.

### bu...@chromium.org (2016-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0

commit e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0
Author: bmeurer <bmeurer@chromium.org>
Date: Wed Apr 27 05:40:37 2016

[turbofan] Don't use the CompareIC in JSGenericLowering.

This is essentially a cherry-pick that was applied before plus the
removal of a test that is now failing because it depends on more
involved changes. The test case checks comparison of different
undetectable JSReceivers, which is not relevant in practice, as there's
only one of these at most, which is document.all.

Merged 55b4df7357557eb16377ad9227e4e0a4224b7885
Merged d00da47b61462681b48e48bdff4a80a33da1a6d6
Merged 4da2e3dbcfc686f68e56c0ad5575257dc2d8ccf1
Merged c1507e158780b170f25f0f1da87cb5d78a56faee

[runtime] Unify comparison operator runtime entries.

[turbofan] Don't use the CompareIC in JSGenericLowering.

PPC: [runtime] Unify comparison operator runtime entries.

PPC: [turbofan] Don't use the CompareIC in JSGenericLowering.

R=yangguo@chromium.org
BUG=chromium:590832,v8:4788,chromium:606181
LOG=N
NOTRY=true
NOPRESUBMIT=true

Cr-Commit-Position: refs/branch-heads/5.0@{#13}
Cr-Branched-From: ad16e6c2cbd2c6b0f2e8ff944ac245561c682ac2-refs/heads/5.0.71@{#1}
Cr-Branched-From: bd9df50d75125ee2ad37b3d92c8f50f0a8b5f030-refs/heads/master@{#34215}

Review URL: https://codereview.chromium.org/1925463003

Cr-Commit-Position: refs/branch-heads/5.0@{#44}
Cr-Branched-From: ad16e6c2cbd2c6b0f2e8ff944ac245561c682ac2-refs/heads/5.0.71@{#1}
Cr-Branched-From: bd9df50d75125ee2ad37b3d92c8f50f0a8b5f030-refs/heads/master@{#34215}

[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/include/v8-version.h
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/arm/code-stubs-arm.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/arm64/code-stubs-arm64.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/compiler/js-generic-lowering.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/compiler/js-generic-lowering.h
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/ia32/code-stubs-ia32.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/interpreter/interpreter.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/mips/code-stubs-mips.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/mips64/code-stubs-mips64.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/objects-inl.h
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/ppc/code-stubs-ppc.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/runtime/runtime-interpreter.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/runtime/runtime-object.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/runtime/runtime-operators.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/runtime/runtime.h
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/src/x64/code-stubs-x64.cc
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/test/mjsunit/mjsunit.status
[add] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/test/mjsunit/regress/regress-4788-1.js
[add] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/test/mjsunit/regress/regress-4788-2.js
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/test/mjsunit/undetectable-compare.js
[modify] https://crrev.com/e64fd96a6c38ccc46b8bd99cc6adb83a978fbef0/test/unittests/runtime/runtime-interpreter-unittest.cc


### bm...@chromium.org (2016-04-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-02)

As mentioned via email - thanks for your report! The reward panel decided on $1,000 for this report.

The CVE-ID for this issue is CVE-2016-1665.

Our finance team should be in contact within 7 days to collect payment details. If that doesn't happen, please email me or update this bug.

Congratulations!

### ti...@google.com (2016-05-02)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/606181?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084162)*
