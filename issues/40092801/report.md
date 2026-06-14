# Security:  assert 'srcPos <= GetReceiverLengthProperty(sortState) - length' at array-sort.tq:613:

| Field | Value |
|-------|-------|
| **Issue ID** | [40092801](https://issues.chromium.org/issues/40092801) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-10-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest Debug build of d8 on ARM64

**VERSION**  

Chrome Version: v8 latest  

Operating System: Linux on ARM64

**REPRODUCTION CASE**  

function opt(ar){  

Array.prototype.unshift(2.3023e-320)  

}  

ar={};  

for(var xo=0;xo<20;xo++)opt([]);  

for(var xo=0;xo<20;xo++)opt(ar);  

for(var xo=0;xo<20;xo++)opt([]);  

for(var xo=0;xo<20;xo++)opt(ar);  

o31=[1.1,2.2,3.3];  

o31['37']=2.3023e-320;  

o51=o31.concat(false);  

o51.sort();

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Crash State: assert 'srcPos <= GetReceiverLengthProperty(sortState) - length' failed at ../../third\_party/v8/builtins/array-sort.tq:613:

## Timeline

### cl...@chromium.org (2018-10-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5189278035083264.

### cl...@chromium.org (2018-10-22)

Testcase 5189278035083264 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5189278035083264.

### cl...@chromium.org (2018-10-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6270400508723200.

### cl...@chromium.org (2018-10-22)

Testcase 6270400508723200 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6270400508723200.

### in...@chromium.org (2018-10-22)

 Does not reproduce on tip-of-tree trunk. If it still reproduces, please file a new bug.

### cl...@gmail.com (2018-10-22)

This does reproduce on a current trunk build (Debug ARM64, not simulator). Please note that this doesn't reproduce on an x64 ASAN Debug build with arm simulator for me.

### in...@chromium.org (2018-10-22)

Assigning to v8 sheriff to triage.

[Monorail components: Blink>JavaScript]

### ha...@chromium.org (2018-10-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-10-24)

Might be related to 898132.

### jg...@chromium.org (2018-10-24)

Possibly, if the error is in GetReceiverLengthProperty, but unlike https://crbug.com/898132 this is happening in Array.p.sort.

### jg...@chromium.org (2018-10-24)

Reduced repro:

// Fill up the Array prototype's elements.
for (let i = 0; i < 100; i++) Array.prototype.unshift(3.14);

// Create a holey double elements array.
const o31 = [1.1];
o31[37] = 2.2;

// Concat converts to dictionary elements.
const o51 = o31.concat(false);

// Sort triggers the bug.
o51.sort();

### jg...@chromium.org (2018-10-24)

This repros on a standard x64 debug build by the way.

### jg...@chromium.org (2018-10-24)

The JSArray state at the point of the crash:

srcPos is 51, array length is 50.

DebugPrint: 0x1512a750c2d9: [JSArray]
 - map: 0x2681e6d0a4a9 <Map(HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x173c6cf91451 <JSArray[100]>
 - elements: 0x1512a750d4f9 <FixedArray[77]> [HOLEY_ELEMENTS]
 - length: 50
 - properties: 0x18c597300c29 <FixedArray[0]> {
    #length: 0x1119f7c801a9 <AccessorInfo> (const accessor descriptor)
 }
 - elements: 0x1512a750d4f9 <FixedArray[77]> {
           0: 0x1512a750b6b9 <HeapNumber 1.1>
           1: 0x1512a750c2c9 <HeapNumber 2.2>
        2-49: 0x173c6cfa0011 <HeapNumber 3.14>
       50-76: 0x18c5973005b9 <the_hole>
 }
0x2681e6d0a4a9: [Map]
 - type: JS_ARRAY_TYPE
 - instance size: 32
 - inobject properties: 0
 - elements kind: HOLEY_ELEMENTS
 - unused property fields: 0
 - enum length: invalid
 - stable_map
 - back pointer: 0x18c5973004d9 <undefined>
 - prototype_validity cell: 0x1119f7c80609 <Cell value= 1>
 - instance descriptors (own) #1: 0x1512a750d4c1 <DescriptorArray[5]>
 - layout descriptor: (nil)
 - prototype: 0x173c6cf91451 <JSArray[100]>
 - constructor: 0x173c6cf91211 <JSFunction Array (sfi = 0x1119f7c8d849)>
 - dependent code: 0x18c5973002c9 <Other heap object (WEAK_FIXED_ARRAY_TYPE)>
 - construction counter: 0

It's interesting that there's less than 100 instances of 'HeapNumber 3.14' in the array. Maybe something is going wrong when copying from the prototype?

### jg...@chromium.org (2018-10-24)

Answer to #13: No, we don't copy from the prototype, this has already been done by Array.p.concat.

### jg...@chromium.org (2018-10-24)

Possibly we there's an invalid run on the PendingRuns stack. We pop 

baseB = 50
lengthB = 50

Whereas array.length == 39.

### jg...@chromium.org (2018-10-24)

The problem is that PrepareElementsForSort is returning a nofNonUndefined > array.length. This happens because array.__proto__ contains elements past array.length. 

The fix that comes to mind is to ensure PrepareElementsForSort always returns a number <= array.length.

### jg...@chromium.org (2018-10-24)

This also triggers another bug in RemoveArrayHolesGeneric which causes us to write undefined into wrong positions past the end of the original array length. There's no OOB write here but a correctness bug. 

https://cs.chromium.org/chromium/src/v8/src/runtime/runtime-array.cc?l=136&rcl=2e57da0a615e7ff922958cb01076c74e6cf44484

The following block which attempts to 'delete elements past undefineds' is also broken.

https://cs.chromium.org/chromium/src/v8/src/runtime/runtime-array.cc?l=148&rcl=2e57da0a615e7ff922958cb01076c74e6cf44484

Aliasing elements on the prototype chain seem to break all assumptions of RemoveArrayHolesGeneric, it looks like we'll have to redesign & rewrite this function.

### jg...@chromium.org (2018-10-24)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-10-24)

Possibly an additional security relevance: due to this bug, RemoveArrayHolesGeneric may change the elements kind. We might enter the wrong fast path.

### jg...@chromium.org (2018-10-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/0855fb151bcd914d3322886bdce097ec359db85e

commit 0855fb151bcd914d3322886bdce097ec359db85e
Author: Jakob Gruber <jgruber@chromium.org>
Date: Thu Oct 25 12:02:47 2018

[array] Ensure PrepareElementsForSort returns a legal value

PrepareElementsForSort must return a number less than or equal the array
length.

Bug: chromium:897512, v8:7382
Change-Id: If5f9c4d052e623ab9f3300b8534603abbee859fa
Reviewed-on: https://chromium-review.googlesource.com/c/1297958
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#56982}
[modify] https://crrev.com/0855fb151bcd914d3322886bdce097ec359db85e/src/runtime/runtime-array.cc
[add] https://crrev.com/0855fb151bcd914d3322886bdce097ec359db85e/test/mjsunit/regress/regress-897512.js
[modify] https://crrev.com/0855fb151bcd914d3322886bdce097ec359db85e/third_party/v8/builtins/array-sort.tq


### jg...@chromium.org (2018-10-25)

#21 works around the worst problem of possible OOB reads & wrong fast-paths in Array.p.sort. It's intended for backmerge once we have canary coverage.

Generic preprocessing should be fixed as well, filed v8:8369 for that.

### sh...@chromium.org (2018-10-25)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-10-25)

jgruber@, pls update bug with canary result tomorrow.

+hablich@ /awhalley@ for Merge review after canary baking.


### sh...@chromium.org (2018-10-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-25)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jg...@chromium.org (2018-10-26)

No canary coverage yet, deferring until Monday.

### jg...@chromium.org (2018-10-29)

Canary seems good:

commit 0855fb151bcd914d3322886bdce097ec359db85e
Author: Jakob Gruber <jgruber@chromium.org>
Date:   Thu Oct 25 13:21:32 2018 +0200

    [array] Ensure PrepareElementsForSort returns a legal value
    
    PrepareElementsForSort must return a number less than or equal the array
    length.
    
    Bug: chromium:897512, v8:7382
    Change-Id: If5f9c4d052e623ab9f3300b8534603abbee859fa
    Reviewed-on: https://chromium-review.googlesource.com/c/1297958
    Commit-Queue: Jakob Gruber <jgruber@chromium.org>
    Reviewed-by: Camillo Bruni <cbruni@chromium.org>
    Cr-Commit-Position: refs/heads/master@{#56982}
=====================ORIGINAL COMMIT END=====================
2.) General information:
Is LKGR:         True
Is on Canary:    3593
First V8 branch: 7.2.130 (Might not be the rolled version)

https://crash.corp.google.com/browse?q=product_name%3D%27Chrome%27+AND+product.version%3D%2772.0.3593.0%27+AND+expanded_custom_data.ChromeCrashProto.channel%3D%27canary%27

### ha...@chromium.org (2018-10-29)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-10-29)

Merges incoming.

70: https://crrev.com/c/1304354
71: https://crrev.com/c/1304318

### go...@chromium.org (2018-10-30)

Pls merge to M71 branch 3578 before 1:00 PM PT, tomorrow, Tuesday so we can pick it up for this week beta release. Thank you.

### bu...@chromium.org (2018-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ef123e3620e32eeb363bb09687a6173644dce98c

commit ef123e3620e32eeb363bb09687a6173644dce98c
Author: Jakob Gruber <jgruber@chromium.org>
Date: Tue Oct 30 09:13:21 2018

Merged: [array] Ensure PrepareElementsForSort returns a legal value

PrepareElementsForSort must return a number less than or equal the array
length.

No-Try: true
No-Presubmit: true
No-Treechecks: true
Bug: chromium:897512, v8:7382
Change-Id: If5f9c4d052e623ab9f3300b8534603abbee859fa
Reviewed-on: https://chromium-review.googlesource.com/c/1297958
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#56982}
Reviewed-on: https://chromium-review.googlesource.com/c/1304354
Reviewed-by: Peter Marshall <petermarshall@chromium.org>
Cr-Commit-Position: refs/branch-heads/7.0@{#67}
Cr-Branched-From: 6e2adae6f7f8e891cfd01f3280482b20590427a6-refs/heads/7.0.276@{#1}
Cr-Branched-From: bc08a8624cbbea7a2d30071472bc73ad9544eadf-refs/heads/master@{#55424}
[modify] https://crrev.com/ef123e3620e32eeb363bb09687a6173644dce98c/src/runtime/runtime-array.cc
[add] https://crrev.com/ef123e3620e32eeb363bb09687a6173644dce98c/test/mjsunit/regress/regress-897512.js
[modify] https://crrev.com/ef123e3620e32eeb363bb09687a6173644dce98c/third_party/v8/builtins/array-sort.tq


### bu...@chromium.org (2018-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/5ca53c0be33c1a405a18b285ddc7e92bdd961849

commit 5ca53c0be33c1a405a18b285ddc7e92bdd961849
Author: Jakob Gruber <jgruber@chromium.org>
Date: Tue Oct 30 09:14:23 2018

Merged: [array] Ensure PrepareElementsForSort returns a legal value

PrepareElementsForSort must return a number less than or equal the array
length.

No-Try: true
No-Presubmit: true
No-Treechecks: true
Bug: chromium:897512, v8:7382
Change-Id: If5f9c4d052e623ab9f3300b8534603abbee859fa
Reviewed-on: https://chromium-review.googlesource.com/c/1297958
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#56982}
Reviewed-on: https://chromium-review.googlesource.com/c/1304318
Reviewed-by: Peter Marshall <petermarshall@chromium.org>
Cr-Commit-Position: refs/branch-heads/7.1@{#22}
Cr-Branched-From: f70aaa8ab2e8815505a6145c745e50d8328cd28c-refs/heads/7.1.302@{#1}
Cr-Branched-From: 1dbcc78efa17a9047f7e923958087ef9eec43066-refs/heads/master@{#56462}
[modify] https://crrev.com/5ca53c0be33c1a405a18b285ddc7e92bdd961849/src/runtime/runtime-array.cc
[add] https://crrev.com/5ca53c0be33c1a405a18b285ddc7e92bdd961849/test/mjsunit/regress/regress-897512.js
[modify] https://crrev.com/5ca53c0be33c1a405a18b285ddc7e92bdd961849/third_party/v8/builtins/array-sort.tq


### jg...@chromium.org (2018-10-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-02)

And $1,000 for this one, thanks as always!

### aw...@google.com (2018-11-02)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-10)

This bug is a regression and does not impact stable. Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-11)

[Empty comment from Monorail migration]

### of...@google.com (2018-12-28)

jgruber: even with the patch to runtime-array.cc applied, I am still seeing a strange error on Node 10 (V8 6.8) using test-case from #11:

$ ./node ~/tmp/foo2.js
RangeError [ERR_INVALID_ASYNC_ID]: Invalid asyncId value: undefined
    at validateAsyncId (internal/async_hooks.js:122:16)
    at emitBeforeScript (internal/async_hooks.js:344:3)
    at process._tickCallback (internal/process/next_tick.js:46:9)
    at Function.Module.runMain (internal/modules/cjs/loader.js:745:11)
    at startup (internal/bootstrap/node.js:283:19)
    at bootstrapNodeJSCore (internal/bootstrap/node.js:743:3)

I suspect there is a still another OOB write on that version? Can you take a look?

### of...@google.com (2018-12-28)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-12-31)

ofrobots, no idea what that error is. The test from #11 may mess up some other parts of the system because it modifies the Array prototype's elements. 

We know that Array sort preprocessing behaves incorrectly for specific Array shapes (that are unlikely to occur in practice). I expect szuend@ will look into that soon (see also https://crbug.com/v8/8369).

### jg...@chromium.org (2019-01-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/4bf28a33ee83ae4b293209e681ab432a0cd11e9f

commit 4bf28a33ee83ae4b293209e681ab432a0cd11e9f
Author: Simon Zünd <szuend@chromium.org>
Date: Thu Jan 17 11:53:52 2019

[array] Fix prototype chain interaction in sort pre-processing

This CL fixes two bugs. First, when looking for a free spot while
moving elements to the front, the prototype chain was also considered,
even though an object at a specific index might have a hole (free
spot).

Second, when moving an element to the front, we are not allowed to
delete it immediately (to preserve semantics when interacting with
non-extensible objects). Such an element is then a free spot, but
won't be recognised as such. This CL sets that element to undefined
after it was moved, to mark it as a free spot.

R=jgruber@chromium.org

Bug: chromium:897512,v8:8369
Change-Id: I79207215b8b0a3c714f064450d8fe5ca0ea4a096
Reviewed-on: https://chromium-review.googlesource.com/c/1417171
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#58878}
[modify] https://crrev.com/4bf28a33ee83ae4b293209e681ab432a0cd11e9f/src/runtime/runtime-array.cc
[modify] https://crrev.com/4bf28a33ee83ae4b293209e681ab432a0cd11e9f/test/mjsunit/regress/regress-897512.js


### sh...@chromium.org (2019-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/897512?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/v8/8369]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092801)*
