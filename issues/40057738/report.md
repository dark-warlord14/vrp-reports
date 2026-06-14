# [LangFuzz] Crash on heap with invalid read from random address (32 bit)

| Field | Value |
|-------|-------|
| **Issue ID** | [40057738](https://issues.chromium.org/issues/40057738) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2012-05-06 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chrome 19 (and likely 20) as well as d8 trunk (rev 11517) on heap with an invalid read to a strange address. The address is not fixed, I have multiple tests that crash at different addresses so I assume it can be controlled somehow. The issue seems to affect 32 bit only.

**VERSION**  

Chrome Version: 19.0.1084.15 dev  

Operating System: Ubuntu 11.04 32 bit

I tested this on d8 trunk (Chrome 20) as well and it reproduces, but I did not have a machine with Chrome 20 and 32 bit handy for testing in addition to Chrome 19.

**REPRODUCTION CASE**  

assertEquals(1, eval("+'1'; 1"));  

function assertEquals ( assertEquals ) {  

return arguments[assertEquals];  

}  

const SMI\_MAX = (1 << 29) - 1 + (1 << 29);  

const SMI\_MIN = -SMI\_MAX - 1;  

function Sar1(x) {}  

assertEquals(-536870912, Sar1(SMI\_MIN));

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0x4cd22d3f in ?? ()  

(gdb) bt 8  

#0 0x4cd22d3f in ?? ()  

#1 0x4cd0db41 in ?? ()  

#2 0x4cd2eb99 in ?? ()  

#3 0x4cd21bf9 in ?? ()  

#4 0x4cd12c2a in ?? ()  

#5 0x00e8fe99 in ?? ()  

Backtrace stopped: previous frame inner to this frame (corrupt stack?)  

(gdb) x /i $pc  

=> 0x4cd22d3f: mov 0xf(%ebx,%eax,2),%ecx  

(gdb) info reg ebx eax ecx  

ebx 0x55741e11 1433673233  

eax 0xc0000000 -1073741824  

ecx 0x2 2  

(gdb)

Valgrind trace in d8:

==18760== Invalid read of size 4  

==18760== at 0x2BD10D40: ???  

==18760== by 0x2BD0EDC0: ???  

==18760== by 0x2BD35AB8: ???  

==18760== by 0x2BD0F3D8: ???  

==18760== by 0x2BD0A0A9: ???  

==18760== by 0x80B12C6: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==18760== Address 0xa374413c is not stack'd, malloc'd or (recently) free'd

## Timeline

### sc...@gmail.com (2012-05-07)

Danno, hope you don't mind if we continue to just toss these over the wall to you. We trust that decoder's reports are real by now ;-)

### da...@chromium.org (2012-05-07)

Nope, no problem at all. Hearing from decoder is always bittersweet... I wish we didn't have any crashers left at all, but him finds are always high quality and interesting to debug.

### da...@chromium.org (2012-05-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-05-08)

Commit: b10deab7527ad052fa030882ebc5e0eb47236e4c
 Email: danno@chromium.org@ce2b1a6d-e550-0410-aec6-3dcde31c8c00

Merged r11518, r11519 into trunk branch.

Fix unsigned-Smi check in MappedArgumentsLookup

Fix crash bug in VisitChoice

BUG=chromium:126414,chromium:126272
R=jkummerow@chromium.org
TEST=test/mjsunit/regress/regress-crbug-126414.js

Review URL: https://chromiumcodereview.appspot.com/10310041

git-svn-id: http://v8.googlecode.com/svn/trunk@11520 ce2b1a6d-e550-0410-aec6-3dcde31c8c00

M	src/arm/ic-arm.cc
M	src/ia32/ic-ia32.cc
M	src/jsregexp.cc
M	src/mips/ic-mips.cc
M	src/version.cc
M	test/mjsunit/regexp-capture-3.js
A	test/mjsunit/regress/regress-crbug-126414.js

### [Deleted User] (2012-05-08)

danno, was it possible to get something other than a bad read out of this? 

### jk...@chromium.org (2012-05-09)

I don't think you could exploit this for anything other than an invalid read. However, I'm not an exploiting expert and could be lacking imagination here :-)
The buggy behavior was a sign-check that checked the 28th instead of the 32nd bit, so a negative index into an "arguments" array would be used for an actual access as long as the 28th bit was not set; which in turn means that the read would happen from an address at least 256MB away from the actual array.

We've had this bug for a very long time; I'll merge the fix back to M18 and M19.

### [Deleted User] (2012-05-09)

Thanks

### [Deleted User] (2012-05-09)

+danno

### in...@chromium.org (2012-05-20)

Looks like we forgot to close this. fix already in c#4.

### sc...@gmail.com (2012-05-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-23)

Wild read => $500, thanks!

### sc...@gmail.com (2012-05-23)

[Empty comment from Monorail migration]

### jk...@chromium.org (2012-05-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

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

This issue was migrated from crbug.com/chromium/126414?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057738)*
