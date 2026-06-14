# Use after free in v8::internal::IncrementalMarking::Step

| Field | Value |
|-------|-------|
| **Issue ID** | [40055557](https://issues.chromium.org/issues/40055557) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-03-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 19.0.1077.3 dev and d8 shell (trunk version as in Chrome 19) in function v8::internal::IncrementalMarking::Step with an invalid read from a random address (could be uninitialized memory).

**VERSION**  

Chrome Version: 19.0.1077.3 dev  

Operating System: Ubuntu 11.10 64 bit

**REPRODUCTION CASE**  

var a = new Array(500);  

for (var i = 0; "if ('p' in undefined) { }" && this || this || this || this || this; i++) a[i] = { idx:i };

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0x000055555666d841 in ?? ()  

(gdb) bt 8  

#0 0x000055555666d841 in ?? ()  

#1 0x000055555676e6cd in ?? ()  

#2 0x000055555661ec70 in ?? ()  

#3 0x000055555661f263 in ?? ()  

#4 0x00005555566d8c95 in ?? ()  

#5 0x00005555566dacde in ?? ()  

#6 0x00005555566db8d5 in ?? ()  

#7 0x00005555566dbfc8 in ?? ()  

(More stack frames follow...)  

(gdb) x /2i $pc  

=> 0x55555666d841: movzbl 0x7(%rax),%r12d  

0x55555666d846: shl $0x3,%r12d  

(gdb) info reg rax r12d  

rax 0x2d5ed2b14da100 12770632962777344  

r12d 0xa7204160 -1491058336

Trace from D8 with Valgrind:

==19247== Warning: set address range perms: large range [0x3e6519dbf000, 0x3e6539dbf000) (noaccess)  

==19247== Invalid read of size 1  

==19247== at 0x4FCF53: v8::internal::IncrementalMarking::Step(long) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19247== by 0x5FD90A: v8::internal::NewSpace::SlowAllocateRaw(int) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19247== by 0x4B16FB: v8::internal::Heap::CopyJSObject(v8::internal::JSObject\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19247== by 0x5C9B87: v8::internal::Runtime\_CreateObjectLiteralShallow(v8::internal::Arguments, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19247== by 0x3E6519E06301: ???  

==19247== by 0x3E6519E365CB: ???  

==19247== by 0x3E6519E0C406: ???  

==19247== by 0x3E6519E060F5: ???  

==19247== by 0x46E87F: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19247== by 0x4702AD: v8::internal::Execution::Call(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*, bool) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19247== by 0x40E854: v8::Script::Run() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19247== by 0x6ABF3D: v8::Shell::ExecuteString(v8::Handle[v8::String](javascript:void(0);), v8::Handle[v8::Value](javascript:void(0);), bool, bool) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19247== Address 0x26ef06e1045907 is not stack'd, malloc'd or (recently) free'd

## Timeline

### sc...@gmail.com (2012-03-24)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-03-25)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-03-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=30000421

Uploader: kenrb@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  v8::internal::IncrementalMarking::Step
  v8::internal::LargeObjectSpace::AllocateRaw
  

Minimized Testcase (0.15 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94T--uAfyYFE3hjFWMdkHI-hakSoWb2jjatAOww7gKUfbjZ4h_az155fTD4v4vQmvS3yQIozwSKpS_Tqa-t3P6lICl7QaIsibb4b6eRjAYySinmLiCJEH62Jiv46nxrZXW3IZWaUecQD7OrTUhJCmxf8Iqn1A

### ke...@chromium.org (2012-03-25)

ASAN is showing a lot of UNKNOWN errors in v8 lately. Are they the same underlying cause? I'm leaving as unconfirmed because it's not clear if these are real bugs. I can't repro on Windows box, but cluster-fuzz gives the above report with very little information.

### in...@chromium.org (2012-03-25)

ASAN does not work with v8 atm.

### jk...@chromium.org (2012-03-25)

@4: This is definitely a real bug.

I can further reduce the test case as follows:

var a = new Array(500);
for (var i = 0; i < 1000000; i++) {
  a[i] = { idx:0 };
}

This crashes (in debug mode) with:
(gdb) bt
#0  0x000000000040a29e in v8::internal::Map::instance_type (this=0x1beefdad0beefdaf) at ../src/objects-inl.h:2797
#1  0x0000000000409b58 in v8::internal::Object::IsOddball (this=0x152c9df04121) at ../src/objects-inl.h:613
#2  0x0000000000409c22 in v8::internal::Object::IsTheHole (this=0x152c9df04121) at ../src/objects-inl.h:786
#3  0x00000000005aa973 in v8::internal::JSObject::GetElementsCapacityAndUsage (this=0x1690634c9621, 
    capacity=0x7fffffffca28, used=0x7fffffffca24) at ../src/objects.cc:9791
#4  0x00000000005aab17 in v8::internal::JSObject::ShouldConvertToSlowElements (this=0x1690634c9621, 
    new_capacity=234002) at ../src/objects.cc:9840
#5  0x00000000005a76bf in v8::internal::JSObject::SetFastElement (this=0x1690634c9621, index=155990, 
    value=0x152c9ce9e6e1, strict_mode=v8::internal::kNonStrictMode, check_prototype=true) at ../src/objects.cc:9128

where 0x1beefdad0beefdaf == kFromSpaceZapValue. Exactly one Mark-Sweep GC pass happens before the crash. Apparently, when a map is kept alive only by elements inside an array, it is killed (or moved without updating the objects referring to it). The following, slightly modified test case passes:

var a = new Array(500);
var b = { idx:0 };
for (var i = 0; i < 1000000; i++) {
  a[i] = b;
}

CC'ing GC guys who might know more.

### ke...@chromium.org (2012-03-25)

I'm setting flags based on it sounding like a use after free condition. Am I correct in guessing that this is a regression that doesn't repro on stable or beta?

### ve...@chromium.org (2012-03-25)

I am on it. From what verify heap tells me we have a missing write-barrier somewhere so the pointer from LO space into new space is not being updated.

### ve...@chromium.org (2012-03-25)

This is caused by the revision r11070 (9 days ago).

http://code.google.com/p/v8/source/detail?r=11070

In JSObject::SetFastElementsCapacityAndLength we started skipping write-barrier when copying backing stores for FAST_ELEMENTS objects which is incorrect.

Reassigning to Danno who was the author of the change. We should also review 11070 to find other potential WB unsafety.


### da...@chromium.org (2012-03-25)

Reintroduced missing WB, patch on the way.

### kc...@chromium.org (2012-03-25)

Is there something we could do in asan to make similar bugs easier to understand? 

### bu...@chromium.org (2012-03-26)

Commit: c740616f92d7ff45c8dbe985fb3a288492fcec97
 Email: danno@chromium.org@ce2b1a6d-e550-0410-aec6-3dcde31c8c00

Merged r11133, r11134 into trunk branch.

Check double array bounds in HasElementImpl.

Fix missing write barrier in CopyObjectToObjectElements.

BUG=chromium:119925,chromium:119926

R=jkummerow@chromium.org

Review URL: https://chromiumcodereview.appspot.com/9856012

git-svn-id: http://v8.googlecode.com/svn/trunk@11136 ce2b1a6d-e550-0410-aec6-3dcde31c8c00

M	src/elements.cc
M	src/elements.h
M	src/objects.cc
M	src/version.cc
A	test/mjsunit/regress/regress-119925.js
A	test/mjsunit/regress/regress-crbug-119926.js

### jk...@chromium.org (2012-03-26)

Patch landed on Chromium trunk, marking this issue as fixed.

FWIW, I don't see how this would be exploitable (other than to trigger a crash), but then again I'm not an exploits expert.

### de...@googlemail.com (2012-03-26)

Your description in https://crbug.com/chromium/119926#c6 sounds like a use-after-free condition for the map object. This kind of flaw usually allows arbitrary control over the whole object being freed (map in this case). I don't know the details of your map object, but usually controlling an object in the JS engine gives you quite a few ways to continue exploiting.

### ve...@chromium.org (2012-03-26)

It is not map that is being freed, it is an object in new space which gets relocated without pointer to it being updated. This is relatively easy to exploit as GC is pretty deterministic and attacker has a relatively good control over contents of the new space so he can try to forge an object in new space. It is not completely clear to me how one can get a hold on map space location to make this forgery successful. But if this is possible then one can potentially forge JSFunction with arbitrary address in the code field. Calling such a function would cause V8 to call that arbitrary address.

### ke...@chromium.org (2012-03-26)

You guys are awesome for taking care of this v8 bug flurry on a weekend.

### ke...@chromium.org (2012-03-26)

[Empty comment from Monorail migration]

### dh...@google.com (2012-04-02)

Is this fix released? There were still traces of this crash in 20.0.1088.0 - http://crash/reportdetail?reportid=f83fd370641f3ec3

### ke...@chromium.org (2012-04-03)

The fix should be out... perhaps that crash is a different bug?

### sc...@gmail.com (2012-05-04)

etc. etc.
$1000

### sc...@gmail.com (2012-05-10)

Payment in system (part of a $5000 batch)

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

This issue was migrated from crbug.com/chromium/119926?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/119927, crbug.com/chromium/119960, crbug.com/chromium/120133, crbug.com/chromium/120492]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055557)*
