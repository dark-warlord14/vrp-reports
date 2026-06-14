# [LangFuzz] Crash at JSObject::LocalLookupRealNamedProperty with invalid read on gc

| Field | Value |
|-------|-------|
| **Issue ID** | [40092542](https://issues.chromium.org/issues/40092542) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | de...@googlemail.com |
| **Assignee** | km...@chromium.org |
| **Created** | 2011-07-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached code crashes Chromium dev and the shell with an invalid read in JSObject::LocalLookupRealNamedProperty. The code requires a garbage collect at the end so I wrote a custom gc() function that should trigger a gc. The original test crashed at v8::internal::FlexibleBodyVisitor but with approximately the same address.

**VERSION**  

Chrome Version: 14.0.803.0 dev  

Operating System: Ubuntu Linux 10.04 - 64 bit

**REPRODUCTION CASE**  

See attached file

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

GDB trace from running Chromium:

Program received signal SIGSEGV, Segmentation fault.  

0x00007fde606ba563 in ?? ()  

(gdb) bt  

#0 0x00007fde606ba563 in ?? ()  

#1 0x0000000000000000 in ?? ()  

(gdb) info reg  

rax 0x100000000 4294967296  

[...]  

(gdb) x /4i $pc  

0x7fde606ba563: mov 0x20(%rax),%rax  

[...]

Trace on shell:

==7397== Invalid read of size 8  

==7397== at 0x512CDE: v8::internal::JSObject::LocalLookupRealNamedProperty(v8::internal::String\*, v8::internal::LookupResult\*) (in /scratch/holler/LangFuzz/v8-bisect/shell)  

==7397== by 0x56164B: v8::internal::Runtime\_GetOwnProperty(v8::internal::Arguments, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-bisect/shell)  

==7397== by 0x9F48341: ???  

==7397== by 0x9F6D699: ???  

==7397== by 0x9F6CA91: ???  

==7397== by 0x9F6B068: ???  

==7397== by 0x9F493E6: ???  

==7397== by 0x9F48127: ???  

==7397== by 0x447DC8: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Object\*\*\*, bool\*) (in /scratch/holler/LangFuzz/v8-bisect/shell)  

==7397== by 0x448288: v8::internal::Execution::Call(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Object\*\*\*, bool\*) (in /scratch/holler/LangFuzz/v8-bisect/shell)  

==7397== by 0x414989: v8::Script::Run() (in /scratch/holler/LangFuzz/v8-bisect/shell)  

==7397== by 0x402F33: ExecuteString(v8::Handle[v8::String](javascript:void(0);), v8::Handle[v8::Value](javascript:void(0);), bool, bool) (in /scratch/holler/LangFuzz/v8-bisect/shell)  

==7397== Address 0x100000020 is not stack'd, malloc'd or (recently) free'd  

==7397==  

==7397==  

==7397== Process terminating with default action of signal 11 (SIGSEGV)  

==7397== Access not within mapped region at address 0x100000020

## Attachments

- [testLocalLookup.js](attachments/testLocalLookup.js) (text/plain; charset=us-ascii, 872 B)

## Timeline

### in...@chromium.org (2011-07-10)

[Empty comment from Monorail migration]

### ri...@chromium.org (2011-07-10)

Kevin, this looks like the arguments object (there is even a todo(kevin) at the spot where we hit an assert in debug mode. It seems we do not have neither fast or dictionary elements. I am actually not totally sure if Kevin wen't on vacation already (calendar says tuesday, but I am not sure). If he is not in tomorrow I will take a look, but I did not really look into the new implementation of the arguments object yet

### km...@chromium.org (2011-07-11)

Proposed fix: http://codereview.chromium.org/7335002/

BTW, I nicer way to get a GC is to use the GC extension to call the garbage collector directly.  This requires passing the flag --expose-gc to the shell.  Take a look at the test case in the code review to see it used.

### km...@chromium.org (2011-07-11)

Fixed in V8 bleeding_edge revision 8587.

### in...@chromium.org (2011-07-11)

Checked with Kevin, it only affects m14.

### sc...@gmail.com (2011-07-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-12)

Looks like a type confusion to me, so we'll definitely consider it for reward.

### sc...@gmail.com (2011-08-24)

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

### sc...@gmail.com (2011-08-29)

Payment in system...

### js...@chromium.org (2011-10-05)

Batch update.

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### aj...@chromium.org (2014-06-19)

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

This issue was migrated from crbug.com/chromium/88858?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092542)*
