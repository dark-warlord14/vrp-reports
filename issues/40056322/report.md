# [LangFuzz] Crash on heap with invalid write (32 bit only).

| Field | Value |
|-------|-------|
| **Issue ID** | [40056322](https://issues.chromium.org/issues/40056322) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | de...@googlemail.com |
| **Assignee** | er...@google.com |
| **Created** | 2012-04-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 19.0.1084.15 dev and d8 shell (trunk revision 11244) on heap with an invalid write to a strange address. The address is not fixed, I have multiple tests that crash at different addresses so I assume it can be controlled somehow. The issue seems to affect 32 bit only.

**VERSION**  

Chrome Version: 19.0.1084.15 dev  

Operating System: Ubuntu 11.04 32 bit

**REPRODUCTION CASE**  

"abel".replace(/b/g, function h() {});  

RegExp["$'"];

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0x3453127f in ?? ()  

(gdb) bt 8  

#0 0x3453127f in ?? ()  

#1 0x34531006 in ?? ()  

#2 0x34521bf9 in ?? ()  

#3 0x34512c2a in ?? ()  

#4 0x00e8fe99 in ?? ()  

Backtrace stopped: previous frame inner to this frame (corrupt stack?)  

(gdb) x /i $pc  

=> 0x3453127f: rep movsl %ds:(%esi),%es:(%edi)  

(gdb) info reg ds esi es edi  

ds 0x7b 123  

esi 0x220d9099 571314329  

es 0x7b 123  

edi 0x57800000 1468006400

Trace from D8 with Valgrind:

==3194== Invalid write of size 4  

==3194== at 0x29337F3F: ???  

==3194== by 0x29337CC5: ???  

==3194== by 0x2930F438: ???  

==3194== by 0x2930A0A9: ???  

==3194== by 0x80B1D36: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==3194== Address 0x2d800000 is not stack'd, malloc'd or (recently) free'd

## Timeline

### pa...@chromium.org (2012-04-06)

I was able to reproduce this on Chrome 20 on Windows (which always runs in 32-bit mode; my Linux is 64-bit). Crash ID 182dac08c8f08139. It does not repro on 18.

danno, can you please take a look at this?

### da...@chromium.org (2012-04-06)

Sure, will do. We'll take a look asap next week.

### js...@chromium.org (2012-04-08)

Flagging all high and critical- and high-severity beta regressions as release blockers.

### er...@google.com (2012-04-11)

I can repro this. Fix coming up. 

### er...@google.com (2012-04-12)

[Empty comment from Monorail migration]

### er...@google.com (2012-04-12)

The internal Substring function doesn't bounds check its inputs, because it is not callable with unchecked inputs.  Unfortunately the regexp code calls it on incorrect inputs, so we crash.  I don't know how one would go about exploiting this, but I would not be comfortable saying that it is not exploitable in some way.

### er...@google.com (2012-04-12)

Fix backported to the M16, M17, M18 and M19 branches.

### er...@google.com (2012-04-12)

Fix backported to M12 aka V8 3.2 for the sake of ICS.

### er...@google.com (2012-04-12)

Clarification: I backported it to 2.5, 3.2, 3.6, 3.7, 3.8 and 3.9 but it is only in 3.10 and 3.9 on IA32 that it is a crasher.  On other releases and on other architectures it is a non-security-related bug.

The crash is caused by memcpy on a negative length which gets interpreted as a high positive.

### in...@chromium.org (2012-04-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-04)

Thanks!! etc.
$1000

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/122337?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056322)*
