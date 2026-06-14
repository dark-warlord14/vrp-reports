# [LangFuzz] Crash on Heap involving GC (invalid write)

| Field | Value |
|-------|-------|
| **Issue ID** | [40095931](https://issues.chromium.org/issues/40095931) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript, Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | km...@chromium.org |
| **Created** | 2011-10-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The HTML file attached (containing two JavaScripts) crashes Chrome 16 and V8 shell (d8 with the two scripts on command line) on heap with an invalid write.

NOTE: The test uses gc(), so you need --js-flags="-expose-gc" for the browser, respectively --expose-gc for d8. I did not test Chromium 15 because my builds of Chromium don't have the --js-flags option for some reason.

**VERSION**  

Chrome Version: 16.0.899.0 dev  

Operating System: Ubuntu 11.04, tested on 64 bit

**REPRODUCTION CASE**  

See attached HTML file.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

GDB Information from Chrome 16:

Program received signal SIGSEGV, Segmentation fault.  

[ Backtrace omitted, all heap, no symbols ]  

(gdb) x /4i $pc  

=> 0x2c8f63076246: mov %r10,0x8(%r9)  

0x2c8f6307624a: mov %rax,%rbx  

0x2c8f6307624d: mov %rdx,%rax  

0x2c8f63076250: or $0x1,%rax  

(gdb) info registers r9 r10  

r9 0x1a38b80ffff8 28830908547064  

r10 0x300000000 12884901888

Valgrind trace from V8 shell:

==8324== Invalid write of size 4  

==8324== at 0x3164C852: ???  

==8324== by 0x3164C3D0: ???  

==8324== by 0x210FEE19: ???  

==8324== by 0x210FE0A5: ???  

==8324== by 0x80AA347: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Object\*\*\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8324== Address 0x5e080000 is not stack'd, malloc'd or (recently) free'd  

==8324==  

==8324==  

==8324== Process terminating with default action of signal 11 (SIGSEGV)

## Attachments

- [testCrashHeapGC.html](attachments/testCrashHeapGC.html) (text/plain; charset=us-ascii, 448 B)

## Timeline

### sc...@gmail.com (2011-10-05)

Danno, possibly related to the new gc landing? Or not, as appropriate :)

### da...@chromium.org (2011-10-05)

GC hasn't landed yet, but that doesn't make this any less of a bug. Assigning to Kevin because it might actually not be a gc problem, and to make sure it gets attention but to Erik and Slava focus on any new GC issues that might pop up.

### in...@chromium.org (2011-10-05)

[Empty comment from Monorail migration]

### km...@chromium.org (2011-10-05)

I know what this is, and it is a GC-related bug.  It is a longstanding issue that is present in both the old and new collectors.

I'll have a fix for it tomorrow.

### km...@chromium.org (2011-10-05)

Looping in Slava.

### in...@chromium.org (2011-10-05)

[Empty comment from Monorail migration]

### km...@chromium.org (2011-10-05)

Proposed fix: http://codereview.chromium.org/8139037/

I want to get a standalone test case, and I don't understand enough about the inobject slack tracking to understand why it doesn't work.  I think I can put something together with eval tomorrow.

Severity: object's internal properties are shuffled and improperly initialized (but initialized to valid V8 values).  This gives wrong results.

The bug also writes past the new space allocation pointer, which is benign if the allocation pointer is not at the top of the space, but will try to write to the top of the next page if the allocation pointer is at the top of the space.

### km...@chromium.org (2011-10-10)

This is fixed in http://code.google.com/p/v8/source/detail?r=9540 with a regression test committed in http://code.google.com/p/v8/source/detail?r=9562.

The fix has been pushed to the V8 3.5 branch (Chrome 15) and the V8 3.4 branch (Chrome 14).  Chrome 13 and earlier are unaffected.

### js...@chromium.org (2011-10-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

@decoder.oh: nice. Looks like you helped the v8 team take care of a long standing stability / security issue :)
$1000

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

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2011-10-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/99167?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript, Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095931)*
