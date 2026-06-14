# UNKNOWN in v8::internal::SemiSpaceIterator::Next

| Field | Value |
|-------|-------|
| **Issue ID** | [40062963](https://issues.chromium.org/issues/40062963) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-08-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes the d8 shell (revision 12259 as used in latest official Chrome Version 22.0.1229.0) in approximately 5% of all runs. This is likely some form of garbage collector corruption and it requires --expose-gc to reproduce. For that reason, I was not able to test it in the browser but I verified that the V8 version used in the browser is affected.

**VERSION**  

Chrome Version: 22.0.1229.0 dev (tested in d8 revision 12259)  

Operating System: Ubuntu 12.04 64 bit

**REPRODUCTION CASE**  

var n = 1;  

function assertFalse() {}  

function assertFalse(e,consCalled) {  

a[e + 4] = 2;  

a[e + 4] = e + 4;  

if (consCalled) {}  

}  

var a = [];  

var o = {};  

for (var i = 0x0020; i < 0x02ff; i += 2) {  

assertFalse('char:' + String.fromCharCode(i + 1) in o);  

}  

function test(a) {  

var res = a[0] + a[0];  

if (res == 0) {}  

gc();  

}  

var result = 0;  

for (var i = 0; i < n; ++i) {  

result += test(a);  

}

In order to reproduce, you might need to run the test more than once, e.g.:

for f in `seq 1 100` ; do d8 --expose-gc test.js ; done

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Tab

Trace from D8 with Valgrind:

==5281== Invalid read of size 1  

==5281== at 0x553D80: v8::internal::HeapObject::SizeFromMap(v8::internal::Map\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x55A84B: v8::internal::MarkCompactCollector::EvacuateNewSpace() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x55B64D: v8::internal::MarkCompactCollector::EvacuateNewSpaceAndCandidates() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x55C9E0: v8::internal::MarkCompactCollector::SweepSpaces() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x565721: v8::internal::MarkCompactCollector::CollectGarbage() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x4C1757: v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x4C1F73: v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const\*, char const\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x4C27BA: v8::internal::Heap::CollectAllGarbage(int, char const\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x472FEE: v8::internal::GCExtension::GC(v8::Arguments const&) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x43E7D7: v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5281== by 0x242011806361: ???  

==5281== by 0x24201183FFEE: ???  

==5281== Address 0x400000007 is not stack'd, malloc'd or (recently) free'd

## Attachments

- [disass.txt](attachments/disass.txt) (text/plain; charset=us-ascii, 81.7 KB)
- [141395.js](attachments/141395.js) (text/plain; charset=us-ascii, 229 B)

## Timeline

### [Deleted User] (2012-08-09)

ccing v8 team

https://cluster-fuzz.appspot.com/testcase?key=91040754

### [Deleted User] (2012-08-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=91040754

Uploader: cdn@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x000400000007
Crash State:
  - crash stack -
  v8::internal::SemiSpaceIterator::Next
  v8::internal::MarkCompactCollector::EvacuateNewSpace
  v8::internal::MarkCompactCollector::EvacuateNewSpaceAndCandidates
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=149679:149702

Minimized Testcase (0.41 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94rjah9OvBR3jZUkYf24MxH4LuQbxPuebvAQRWEJM7fG-zsk8Kf-TwHN7op-IVHaFZ-4EW5K25aP766drwG1ng9vi-TXkc5eRjhyvmOfTdqpSc1YeKd2qxBz8fWhqHTPrNNbJf3n7B1z79P9wF7NmbPQXsnjZAPTl04fG7ifywHEXGy1ns
<script>
var n = 1;
function assertFalse() {}
function assertFalse(e,consCalled) {
  a[e + 4] = 2;
  a[e + 4] = e + 4;
  if (consCalled) {}
}
var a = [];
var o = {};
for (var i = 0x0020; i < 0x02ff; i += 2) {
  assertFalse('char:' + String.fromCharCode(i + 1) in o);
}
function test(a) {
  var res = a[0] + a[0];
  if (res == 0) {}
  gc();
}
var result = 0;
for (var i = 0; i < n; ++i) {
  result += test(a);
}
</script>

### in...@chromium.org (2012-08-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-09)

I think Danno is on vacation. Michael, can you please help to triage and help with an owner.

### ms...@chromium.org (2012-08-10)

[Empty comment from Monorail migration]

### er...@google.com (2012-08-10)

I can't reproduce this on 64 bit Linux with the same V8 version that you have.

### er...@google.com (2012-08-10)

Do I have to run under valgrind to see the problem?

### de...@googlemail.com (2012-08-10)

I did not run under valgrind but as I stated in https://crbug.com/chromium/141395#c0, you need to run multiple times on d8 since the chance of reproducing is only about 5%. https://crbug.com/chromium/141395#c3 seems to indicate that it got reproduced in the browser though.

### er...@google.com (2012-08-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-10)

Since CF are slow machines. i would suggest running the testcase from command line with the flags listen in the report at https://cluster-fuzz.appspot.com/testcase?key=91040754 and running multiple instances. on CF, it looks pretty reliable.

### cl...@chromium.org (2012-08-10)

ClusterFuzz has detected this issue as fixed in range 150790:150794.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=91040754

Uploader: cdn@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x000400000007
Crash State:
  - crash stack -
  v8::internal::SemiSpaceIterator::Next
  v8::internal::MarkCompactCollector::EvacuateNewSpace
  v8::internal::MarkCompactCollector::EvacuateNewSpaceAndCandidates
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=149679:149702
Fixed: https://cluster-fuzz.appspot.com/revisions?range=150790:150794

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94rjah9OvBR3jZUkYf24MxH4LuQbxPuebvAQRWEJM7fG-zsk8Kf-TwHN7op-IVHaFZ-4EW5K25aP766drwG1ng9vi-TXkc5eRjhyvmOfTdqpSc1YeKd2qxBz8fWhqHTPrNNbJf3n7B1z79P9wF7NmbPQXsnjZAPTl04fG7ifywHEXGy1ns

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2012-08-10)

ClusterFuzz has detected this issue as fixed in range 150790:150794.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=91040754

Uploader: cdn@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x000400000007
Crash State:
  - crash stack -
  v8::internal::SemiSpaceIterator::Next
  v8::internal::MarkCompactCollector::EvacuateNewSpace
  v8::internal::MarkCompactCollector::EvacuateNewSpaceAndCandidates
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=149679:149702
Fixed: https://cluster-fuzz.appspot.com/revisions?range=150790:150794

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94rjah9OvBR3jZUkYf24MxH4LuQbxPuebvAQRWEJM7fG-zsk8Kf-TwHN7op-IVHaFZ-4EW5K25aP766drwG1ng9vi-TXkc5eRjhyvmOfTdqpSc1YeKd2qxBz8fWhqHTPrNNbJf3n7B1z79P9wF7NmbPQXsnjZAPTl04fG7ifywHEXGy1ns

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-08-10)

Christian, can you still reproduce it with trunk. Looks like the skia revert fixed it.

### de...@googlemail.com (2012-08-10)

I don't see how a skia revert can fix this. The issue is not a browser-only issue and it's in V8. You can reproduce this issue in the V8 shell (d8) without any skia being involved, so a skia revert cannot fix this.

### in...@chromium.org (2012-08-10)

Had a chat with Christian. Looks like this is a CF false positive due to test flakiness. Ignore c#12 to c#14.

### er...@google.com (2012-08-13)

I'm seeing this in V8 standalone now.

### er...@google.com (2012-08-13)

Smaller repro:


function assertFalse(e) {
  var x = e + 4;
  a[x] = 2;
  a[x] = 3;
}
var a = [];
var o = {};
for (var i = 0x0080; i < 0x1ff; i++) {
  assertFalse('char:' + String.fromCharCode(i) in o);
}
gc();


### er...@google.com (2012-08-14)

[Empty comment from Monorail migration]

### er...@google.com (2012-08-14)

The assertFalse method is being miscompiled due to array index dehoisting.  I have attached the assembly.  The e+4 is being fused into the second (not the first) array store, despite the fact that it is a string add.

Run the file with --allow-natives-syntax --hydrogen-filter=foo --nouse-inlining --expose-gc --print-code --code-comments

The array bounds check randomly succeeds or fails depending on memory layout, which is random.  By adjusting the size of the array and the integer offset (+ 4 in the above) you could make a relatively reliable read or write to arbitrary addresses.  So it's a genuine security issue.

Array dehoisting is off in V8-3.11 so the issue does not affect M21 (see flag-definitions.h).  Moving to M22.

### [Deleted User] (2012-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-08-14)

[Empty comment from Monorail migration]

### er...@google.com (2012-08-14)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

Thanks for catching v8 regressions as usual!
$1000

### sc...@gmail.com (2012-08-25)

@mmassi @mstarzinger @danno: is this merged to the M22 branch?

### er...@google.com (2012-08-25)

The M22 branch uses V8 version 3.12.  The fix has been merged in to the 3.12 branch at r12303, which is version 3.12.19.2.

### sc...@gmail.com (2012-08-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-12)

Paid as part of $1000 batch

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/141395?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062963)*
