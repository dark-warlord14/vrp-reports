# [LangFuzz] Crash due to invalid free in v8::internal::Runtime_RegExpExecMultiple

| Field | Value |
|-------|-------|
| **Issue ID** | [40072605](https://issues.chromium.org/issues/40072605) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript, Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2012-09-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 23.0.1262.0 dev and d8 shell (trunk version as in Chrome 23.0.1262.0) with an invalid free in v8::internal::Runtime\_RegExpExecMultiple.

**VERSION**  

Chrome Version: 23.0.1262.0 dev  

Operating System: Ubuntu 12.04 64 bit

**REPRODUCTION CASE**  

var str = "ABX X";  

str = str.replace(/(\w)?X/g, function(match, capture) {});  

function test() {  

try {  

test(7, 'right');  

} catch(e) {  

"bar.foo baz......".replace(/(ba.).\*?f/g, function() { return "x";});  

}  

}  

test();

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash state:

third\_party/tcmalloc/chromium/src/tcmalloc.cc:285] Attempt to free invalid pointer 0x55555a1eda81

Program received signal SIGSEGV, Segmentation fault.  

0x0000555555bbfdd0 in ?? ()  

(gdb) bt  

#0 0x0000555555bbfdd0 in ?? ()  

#1 0x0000555555bc771c in ?? ()  

[...]  

(More stack frames follow...)  

(gdb) x /i $pc  

=> 0x555555bbfdd0: movb $0x21,0x39

Valgrind with d8:

==8067== Invalid free() / delete / delete[]  

==8067== at 0x4C2563E: operator delete (vg\_replace\_malloc.c:409)  

==8067== by 0x5EBA56: v8::internal::Runtime\_RegExpExecMultiple(v8::internal::Arguments, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8067== by 0xB31A8806361: ???  

==8067== by 0xB31A8841307: ???  

[...]  

==8067== Address 0x7fef09d58 is on thread 1's stack

## Timeline

### in...@chromium.org (2012-09-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-11)

[Empty comment from Monorail migration]

### ms...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### ya...@chromium.org (2012-09-12)

Fixed in r12491.

### in...@chromium.org (2012-09-12)

Was this a regression, if not, please merge to m22 as well.

### ya...@chromium.org (2012-09-12)

This does not affect M22.

### in...@chromium.org (2012-09-12)

Thanks for confirming.

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-25)

@decoder.oh: thanks for the regression catch! $1000

### sc...@gmail.com (2012-10-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

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

This issue was migrated from crbug.com/chromium/148378?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript, Internals]
[Monorail mergedwith: crbug.com/chromium/148891, crbug.com/chromium/149300]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072605)*
