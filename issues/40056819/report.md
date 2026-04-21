# Security: v8 CHECK Failed IsStruct_NonInline in Torgue Struct-Tq-Inl

| Field | Value |
|-------|-------|
| **Issue ID** | [40056819](https://issues.chromium.org/issues/40056819) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@yahoo.de |
| **Assignee** | cb...@chromium.org |
| **Created** | 2021-08-08 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Hello, I found this bug via fuzzing. It leads to the following CHECK:

# Fatal error in gen/torque-generated/src/objects/struct-tq-inl.inc, line 4

# Check failed: !v8::internal::FLAG\_enable\_slow\_asserts || (IsStruct\_NonInline(\*this)).

**VERSION**  

I verified this crash in v8 version v8 9.4.0 (commit hash: 185badc9122fe6274c1b2fe54e03fda5315cb80e)

I compiled it using:  

gn gen out/fuzzbuild --args='is\_debug=true dcheck\_always\_on=true v8\_static\_library=true v8\_enable\_slow\_dchecks=true v8\_enable\_v8\_checks=true v8\_enable\_verify\_heap=true v8\_enable\_verify\_csa=true v8\_fuzzilli=true v8\_enable\_verify\_predictable=true target\_cpu="x64"'

And I started d8 with the following flag:  

./d8 --interrupt-budget=1024 /path/to/crash.js

The "--interrupt-budget=1024" flag is important to trigger the CHECK.

**REPRODUCTION CASE**

for(var var\_2\_ = 0; var\_2\_ < 2; var\_2\_++) {  

Object.getOwnPropertyNames.call(Object.getOwnPropertyNames,this).forEach(function(var\_9\_) {  

try {  

if(var\_9\_ != "arguments") {  

this["foo"].find(null);  

} else {  

this["arguments"].find(isNaN);  

}  

["import('a');"].find(eval);  

} catch {}  

});  

}

**CREDIT INFORMATION**  

Reporter credit: Rene Freingruber (@ReneFreingruber)

## Attachments

- [broken.txt](attachments/broken.txt) (text/plain, 70.2 KB)
- [working.txt](attachments/working.txt) (text/plain, 35.0 KB)

## Timeline

### [Deleted User] (2021-08-08)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-08-09)

Thank you for the report.

ishell@: Can you please help triage this?

[Monorail components: Blink>JavaScript]

### is...@chromium.org (2021-08-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-16)

I can reproduce this with the gn args specified above. I can't get a symbolized stack trace though. Without all the gn flags I do get a different crash though which seems non-security. I cannot tell from the stack or the flags whether this bug has security implication. Can someone from the v8 team take a look at it?

### wf...@chromium.org (2021-08-16)

This only needs v8_enable_slow_dchecks = true to hit with supplied test case, but even running with an asan build without dcheck doesn't hit any memory corruption so I'm not sure exactly what the security implications of this are. Grateful if v8 team could take a closer look.

### jg...@chromium.org (2021-08-17)

Backtrace:

#3  0x00007f5b8443f440 in v8::internal::TorqueGeneratedStruct<v8::internal::Struct, v8::internal::HeapObject>::TorqueGeneratedStruct (this=0x7ffc6b458f68, ptr=63475455894453) at gen/torque-generated/src/objects/struct-tq-inl.inc:7
#4  v8::internal::Struct::Struct (this=0x7ffc6b458f68, ptr=63475455894453) at ../../src/objects/struct-inl.h:23
#5  v8::internal::TorqueGeneratedScript<v8::internal::Script, v8::internal::Struct>::TorqueGeneratedScript (this=0x7ffc6b458f68, ptr=63475455894453) at gen/torque-generated/src/objects/script-tq-inl.inc:273
#6  v8::internal::Script::Script (this=0x7ffc6b458f68, ptr=63475455894453) at ../../src/objects/script-inl.h:22
#7  v8::internal::TorqueGeneratedScript<v8::internal::Script, v8::internal::Struct>::cast (object=...) at gen/torque-generated/src/objects/script-tq.inc:77
#8  0x00007f5b84e48ba3 in v8::internal::__RT_impl_Runtime_DynamicImportCall (args=..., isolate=<optimized out>) at ../../src/runtime/runtime-module.cc:31
#9  0x00007f5b83d66eda in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvInRegister_NoBuiltinExit () from /usr/local/google/home/jgruber/src/v8/out/tmp/libv8.so
#10 0x00007f5b841394e2 in Builtins_CallRuntimeHandler () from /usr/local/google/home/jgruber/src/v8/out/tmp/libv8.so

The actual value of ptr is `undefined`.

### jg...@chromium.org (2021-08-17)

In

 script = handle(Script::cast(script->eval_from_shared().script()), isolate);

`script->eval_from_shared().script()` may be `undefined`, i.e. not a Script. A quick change to fix the potential security issue is to add a `CHECK(script->eval_from_shared().script().IsScript())`.

https://source.chromium.org/chromium/chromium/src/+/main:v8/src/runtime/runtime-module.cc;l=31;drc=068d917a72636ddbb64dfa7ecabe6bac71bd4b26


### jg...@chromium.org (2021-08-17)

[Empty comment from Monorail migration]

### cb...@chromium.org (2021-08-17)

[Empty comment from Monorail migration]

### cb...@chromium.org (2021-08-17)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-17)

given #6 #7 and mention of potential security issue I'm triaging as potential memory corruption.

### [Deleted User] (2021-08-17)

[Empty comment from Monorail migration]

### cb...@chromium.org (2021-08-17)

Seems like we fail to get the proper SFI when trying to get the EvalOrigin [1] when having optimized code on the stack

Printing the stacktrace at this position in the compiler yields:

WORKING (--noopt):
    0: builtin exit frame: eval(aka eval)(this=0x09a8080023b5 <undefined>,0x09a8080023b5 <undefined>,0x09a8082931c1 <String[12]: #import('a');>,0,0x09a80811ba61 <JSArray[1]>#1#)

    1: find [0x9a80828c1f5](this=0x09a80811ba61 <JSArray[1]>#1#,0x09a8082899b5 <JSFunction eval (sfi = 0x9a80820e401)>#2#)
    2: /* anonymous */ [0x9a8081137d9] [_test/import.js:8] [bytecode=0x9a80829324d offset=41](this=0x09a808283639 <JSGlobalProxy>#3#,0x09a808004029 <String[9]: #arguments>)

    3: forEach [0x9a80828c3d1](this=0x09a8081137c9 <JSArray[80]>#4#,0x09a8081137d9 <JSFunction (sfi = 0x9a808292fbd)>#5#)
    4: /* anonymous */ [0x9a808293121] [_test/import.js:3] [bytecode=0x9a80829301d offset=72](this=0x09a808283639 <JSGlobalProxy>#3#)
    5: InternalFrame [pc: 0x7f8cb4318c78]
    6: EntryFrame [pc: 0x7f8cb4318a07


BROKEN (--opt):
Security context: 0x09a808290ac9 <JSGlobalObject>#0#
    0: builtin exit frame: eval(aka eval)(this=0x09a8080023b5 <undefined>,0x09a8080023b5 <undefined>,0x09a8082931c1 <String[12]: #import('a');>,0,0x09a80811ba71 <JSArray[1]>#1#)

    1: /* anonymous */ [0x9a8081137d1] [_test/import.js:~3] [pc=0x9a800044df4](this=0x09a808283639 <JSGlobalProxy>#2#,0x09a808004029 <String[9]: #arguments>)

    2: forEach [0x9a80828c3d1](this=0x09a8081137c1 <JSArray[80]>#3#,0x09a8081137d1 <JSFunction (sfi = 0x9a808292fbd)>#4#)
    3: /* anonymous */ [0x9a808293121] [_test/import.js:3] [bytecode=0x9a80829301d offset=72](this=0x09a808283639 <JSGlobalProxy>#2#)
    4: InternalFrame [pc: 0x7f8133d67c78]
    5: EntryFrame [pc: 0x7f8133d67a07]

We see that frames 1 and 2 from the --noopt case are not present in the --opt case.
This results in using the wrong SFI for Script::set_eval_from_shared: Array.prototype.find instead of the top-level script


[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/codegen/compiler.cc;l=2214?q=set_eval_from_position&start=1

### cb...@chromium.org (2021-08-17)

Attaching detailed stdout prints of both versions

### cb...@chromium.org (2021-08-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler]

### [Deleted User] (2021-08-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cb...@chromium.org (2021-08-19)

Cleaner repro case:

function thrower() {
	throw new Error();
}
function doSomething() {
	return 1;
}

function helper(deopt) {
	try {
		if (!deopt) {
			thrower();
		} else {
			doSomething();
		}
		["import('a');"].find(eval);
	} catch { }
}

while (true) {
	for (let i = 0; i < 80; i++) helper(false);
	helper(true);
}


This reliably crashes in a debug build up to --interrupt-budget=1439 from there on it's less reliable.

I'm just addressing the security issue for now, since I'm stuck with the deopt/tf issue here.


out/debug/d8 --interrupt-budget=1440 _test/cf_1237730.js --allow-natives-syntax --trace-opt --trace-deopt --trace-osr
[marking 0x33f708293289 <JSFunction helper (sfi = 0x33f708293075)> for optimized recompilation, reason: small function]
[compiling method 0x33f708293289 <JSFunction helper (sfi = 0x33f708293075)> (target TURBOFAN) using TurboFan]
[optimizing 0x33f708293289 <JSFunction helper (sfi = 0x33f708293075)> (target TURBOFAN) - took 9.391, 12.108, 0.476 ms]
[completed optimizing 0x33f708293289 <JSFunction helper (sfi = 0x33f708293075)> (target TURBOFAN)]
[marking 0x33f7082931bd <JSFunction (sfi = 0x33f708292f9d)> for optimized recompilation, reason: small function]
[bailout (kind: deopt-soft, reason: Insufficient type feedback for call): begin. deoptimizing 0x33f708293289 <JSFunction helper (sfi = 0x33f708293075)>, opt id 0, node id 45, bytecode offset 20, deopt exit 1, FP to SP delta 32, caller SP 0x7ffeecc5cb58, pc 0x33f700904209]
[marking 0x33f708293289 <JSFunction helper (sfi = 0x33f708293075)> for optimized recompilation, reason: small function]
[compiling method 0x33f708293289 <JSFunction helper (sfi = 0x33f708293075)> (target TURBOFAN) using TurboFan]
[OSR - arming back edges in ]
[optimizing 0x33f708293289 <JSFunction helper (sfi = 0x33f708293075)> (target TURBOFAN) - took 11.319, 22.763, 0.561 ms]
[completed optimizing 0x33f708293289 <JSFunction helper (sfi = 0x33f708293075)> (target TURBOFAN)]

[Monorail components: -Blink>JavaScript]

### cb...@chromium.org (2021-08-19)

To clarify, the crash only happens after taking the infrequent branch for the second time.

### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7b07aa0e13322da5c1da36373d7469372773c009

commit 7b07aa0e13322da5c1da36373d7469372773c009
Author: Camillo Bruni <cbruni@chromium.org>
Date: Thu Aug 19 20:34:46 2021

[modules] Handle missing eval origin with dynamic imports

Bug: chromium:1237730
Change-Id: Ib604a5d3dc8931f195d6508048937ee735e18fd8
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3107306
Auto-Submit: Camillo Bruni <cbruni@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/main@{#76421}

[modify] https://crrev.com/7b07aa0e13322da5c1da36373d7469372773c009/src/execution/isolate.cc
[modify] https://crrev.com/7b07aa0e13322da5c1da36373d7469372773c009/src/execution/isolate.h
[modify] https://crrev.com/7b07aa0e13322da5c1da36373d7469372773c009/src/runtime/runtime-module.cc


### jg...@chromium.org (2021-08-23)

Thanks Camillo, I can look for the missing frame in a bit. Do we need to backmerge the security fix?

### jg...@chromium.org (2021-08-23)

Working off the repro in #17, and printing the summarized stack frames at `https://source.chromium.org/chromium/chromium/src/+/main:v8/src/codegen/compiler.cc;l=2213;drc=df2b169b3f65a3210dc5d75e7fac32940cea8e51: 

$ out/debug/d8 --interrupt-budget=1024 tmp.js 
----------------------------------------------------
0 (index in frame summary)
0x0b2308293075 <SharedFunctionInfo helper>
----------------------------------------------------
0
0x0b2308293075 <SharedFunctionInfo helper>
1
0x0b230820ff31 <SharedFunctionInfo find>

The first time this location is reached is from unoptimized code (we initially optimize, but then soft-deopt when reaching the `find` call). 

The second time, we reach it within optimized code.

For some reason, the optimized frame summary contains the `find` frame and the unoptimized summary does not. Maybe because optimized frames inline Array.find, and unoptimized frames call through the builtin. I'm not surprised at the presence of `find`, after all the callchain is

 helper -> Array.find -> eval -> import

`eval_from_shared` is

  // [eval_from_shared]: for eval scripts the shared function info for the
  // function from which eval was called.

https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/script.h;l=61;drc=0ce9df69ba9e32bafc53c3d90db8a707c243da40

It's still unclear to me what the expected behavior of `eval_from_shared` is in this case. Should SFI be the topmost caller SFI, or should it be the closest-to-topmost JS SFI?

[Monorail components: Blink>JavaScript>Runtime]

### jg...@chromium.org (2021-08-23)

In the unoptimized version, `find` has its own frame which is filtered out by `return js_frame->function().shared().IsSubjectToDebugging();`: https://source.chromium.org/chromium/chromium/src/+/main:v8/src/execution/frames.cc;l=213;drc=0ce9df69ba9e32bafc53c3d90db8a707c243da40.

This filtering does not happen when `find` is part of an inlined frame.

### jg...@chromium.org (2021-08-23)

Proposed fix: crrev.com/c/3110611

### cb...@chromium.org (2021-08-23)

Re https://crbug.com/chromium/1237730#c20: It's likely been out there for a while, but the fix is quite local, so I'd vote for backmerging (still waiting for M95 canary coverage)

### gi...@appspot.gserviceaccount.com (2021-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c400d8b0310e5421a445deea8ad604bb69120b88

commit c400d8b0310e5421a445deea8ad604bb69120b88
Author: Jakob Gruber <jgruber@chromium.org>
Date: Mon Aug 23 13:02:19 2021

[frames] Add convenience function to get the top valid from

.. from a StackTraceFrameIterator (STFI). This replaces the (incorrect)
pattern

 StackTraceFrameIterator it(isolate);
 FrameSummary fs = FrameSummary::GetTop(it.javascript_frame());

The STFI has filtering semantics that only iterate over certain JS and
Wasm frames. These semantics (e.g. skipping over frames that are not
subject to debugging) must be preserved when looking into inlined
optimized frames.

The new convenience function GetTopValidFrame encapsulates this logic.

Bug: chromium:1237730
Change-Id: I060b36b5ac6a5decef90da4de45e679516ff93fd
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3110611
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/main@{#76445}

[modify] https://crrev.com/c400d8b0310e5421a445deea8ad604bb69120b88/src/codegen/compiler.cc
[modify] https://crrev.com/c400d8b0310e5421a445deea8ad604bb69120b88/src/debug/debug.cc
[modify] https://crrev.com/c400d8b0310e5421a445deea8ad604bb69120b88/src/execution/frames.cc
[modify] https://crrev.com/c400d8b0310e5421a445deea8ad604bb69120b88/src/execution/frames.h
[modify] https://crrev.com/c400d8b0310e5421a445deea8ad604bb69120b88/src/execution/isolate.cc


### gi...@appspot.gserviceaccount.com (2021-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7b6b1b1df4723ff4a225a8d16cf4078405ebeea3

commit 7b6b1b1df4723ff4a225a8d16cf4078405ebeea3
Author: Camillo Bruni <cbruni@chromium.org>
Date: Tue Aug 24 09:55:19 2021

[modules] Add CHECK to dynamic import

https://crrev.com/c/3110611 has landed, thus we can revert the temporary
workaround.

Bug: chromium:1237730
Change-Id: Ieb39ff07baddd03dc41c716d921496eb4d539fae
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3114137
Commit-Queue: Camillo Bruni <cbruni@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/main@{#76449}

[modify] https://crrev.com/7b6b1b1df4723ff4a225a8d16cf4078405ebeea3/src/execution/isolate.cc
[modify] https://crrev.com/7b6b1b1df4723ff4a225a8d16cf4078405ebeea3/src/execution/isolate.h
[modify] https://crrev.com/7b6b1b1df4723ff4a225a8d16cf4078405ebeea3/src/runtime/runtime-module.cc


### va...@chromium.org (2021-08-31)

Any updates on this one? Do we need to back merge any fixes?

### cb...@chromium.org (2021-08-31)

I'd suggest backmerging the easy fix  https://crrev.com/7b07aa0e13322da5c1da36373d7469372773c009 to M94, maybe M93

### va...@chromium.org (2021-08-31)

What's the impact in case we don't back merge to M93?

### [Deleted User] (2021-08-31)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cb...@chromium.org (2021-08-31)

I'ts might be a security issue since we can read OOB (though likely only in read-only-space).

I can provide a simpler backmerge for M92 DCHECK => CHECK to mitigate potential security issues.

### va...@chromium.org (2021-09-02)

Moving all open V8 compiler issues to Blink>JavaScript>Compiler>Turbofan. Please adjust the component in case another compiler is affected by the issue

[Monorail components: -Blink>JavaScript>Compiler Blink>JavaScript>Compiler>Turbofan]

### sr...@google.com (2021-09-02)

can u pls answer https://crbug.com/chromium/1237730#c30 for review. 

### am...@chromium.org (2021-09-02)

hi cbruni@ and vahl@, if the CLs in comments #25 and #26 are the full fix for this issue, can you please make this as Fixed. This will help sherrifbot and us know if it's ready for the merge review processes. Thanks! 

### cb...@chromium.org (2021-09-07)

This is in the V8 repo not chrome.

Re https://crbug.com/chromium/1237730#c29: We can have a OOB read in the ReadyOnly roots, but I have no gaurantees to second order effects.
The release check is basically just what we do in a debug build (what caught the issue int he first place)





### cb...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript>Compiler>Turbofan]

### sr...@google.com (2021-09-08)

cbruni@ can you help comment on the merge to M94, ( https://crbug.com/chromium/1237730#c30) answer the questions so we can review and approve

### am...@chromium.org (2021-09-08)

hi cbruni@, security bugs in V8 are still a part of the merge review process for Chrome browser bugs so that we can ensure the bugs are merged appropriate so that the V8 security bug fixes make it to the V8 branch in time to be a part of the their channel release counterparts. 

Please update this issue to Fixed if all issues are fully addressed, so that merge review can take place and we can ensure the OOB read fix via   https://crrev.com/7b07aa0e13322da5c1da36373d7469372773c009 can make it into next week's M93 security refresh. This would need to be reviewed and merged into the appropriate V8 branch for M93 by 2pm PDT tomorrow. Thank you

### sr...@google.com (2021-09-10)

cbruni@ can you help answer https://crbug.com/chromium/1237730#c20 pls

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### cb...@chromium.org (2021-09-13)

Sorry, I've been OOO sick for the past week.

Let's backmerge a simple DCHECK => CHECK as this will have the lowest potential for conflicts.

### sr...@google.com (2021-09-13)

can you pls answer the comment for merge review with what CL you want to merge etc. 

### cb...@chromium.org (2021-09-14)

https://crrev.com/c/3157945 is going to be backmerged to 9.4

### gi...@appspot.gserviceaccount.com (2021-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/d273b57b98239b25ffa081167f3178482921a4a1

commit d273b57b98239b25ffa081167f3178482921a4a1
Author: Camillo Bruni <cbruni@chromium.org>
Date: Mon Sep 13 07:24:45 2021

Merged: [modules] Harden dynamic import runtime function

Bug: chromium:1237730
Change-Id: I3b78cce80bdf386cdf6ca3c022b068e384412558
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3157945
Commit-Queue: Camillo Bruni <cbruni@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.4@{#33}
Cr-Branched-From: 3b51863bc25492549a8bf96ff67ce481b1a3337b-refs/heads/9.4.146@{#1}
Cr-Branched-From: 2890419fc8fb9bdb507fdd801d76fa7dd9f022b5-refs/heads/master@{#76233}

[modify] https://crrev.com/d273b57b98239b25ffa081167f3178482921a4a1/src/runtime/runtime-module.cc


### sr...@google.com (2021-09-14)

thanks cbruni@ next time, please share the details of the CL to merge before hand for approval and then merge once the change is approved for merge. I am not sure if lutz@ approved this offline ( which is fine), but if not merges to release branches should have approval.

### sr...@google.com (2021-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### re...@yahoo.de (2021-10-05)

Hi,

is the status "started (open)" still correct? I think this one is already fixed, right?

best regards

### cb...@chromium.org (2021-10-06)

This has been backmerged to M94 and was fixed in M95.


### [Deleted User] (2021-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-13)

Congratulations, Rene! The VRP Panel has decided to award you $5,000 for this report. Thank you for this report and nice work! 

### am...@google.com (2021-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1237730?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056819)*
