# Heap-buffer-overflow in CJBig2_Context::parseSymbolDict

| Field | Value |
|-------|-------|
| **Issue ID** | [40082587](https://issues.chromium.org/issues/40082587) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **CVE IDs** | CVE-2015-6778 |
| **Reporter** | ka...@skomski.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2015-07-28 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

Both bugs are executed via multiple dictionaries feeded to CJBig2\_Context::parseSymbolDict via a crafted jbig2 image:

Heap-Buffer-Overflow:

```
m_pStream->readShortInteger(&wFlags)  
pSymbolDictDecoder->SDTEMPLATE = (wFlags >> 10) & 0x0003; <-- setting true on the first dictionary but false on the second  

```

--------- lower  

if((wFlags & 0x0100) && pLRSeg && pLRSeg->m\_Result.sd->m\_bContextRetained) { <-- setting flag 0x00100 true for second run  

if (pSymbolDictDecoder->SDHUFF == 0) {  

dwTemp = pSymbolDictDecoder->SDTEMPLATE == 0 ? 65536 : pSymbolDictDecoder->SDTEMPLATE == 1 ?  

8192 : 1024;  

gbContext = (JBig2ArithCtx\*)m\_pModule->JBig2\_Malloc2(sizeof(JBig2ArithCtx), dwTemp);  

JBIG2\_memcpy(gbContext, pLRSeg->m\_Result.sd->m\_gbContext, sizeof(JBig2ArithCtx)\*dwTemp);  

}  

} else {  

if (pSymbolDictDecoder->SDHUFF == 0) {  

dwTemp = pSymbolDictDecoder->SDTEMPLATE == 0 ? 65536 : pSymbolDictDecoder->SDTEMPLATE == 1 ?  

8192 : 1024;  

gbContext = (JBig2ArithCtx\*)m\_pModule->JBig2\_Malloc2(sizeof(JBig2ArithCtx), dwTemp);  

JBIG2\_memset(gbContext, 0, sizeof(JBig2ArithCtx)\*dwTemp);  

}  

}

Uninitialized memory write:  

m\_pStream->readShortInteger(&wFlags)  

pSymbolDictDecoder->SDHUFF = wFlags & 0x0001; <-- setting SDHUFF true on second run to prevent first heap-buffer-overflow  

pSymbolDictDecoder->SDREFAGG = (wFlags >> 1) & 0x0001; <-- setting SDREFAGG true on second run  

pSymbolDictDecoder->SDTEMPLATE = (wFlags >> 10) & 0x0003;  

pSymbolDictDecoder->SDRTEMPLATE = (wFlags >> 12) & 0x0003;  

--------- lower  

if((wFlags & 0x0100) && pLRSeg && pLRSeg->m\_Result.sd->m\_bContextRetained) { <-- setting flag 0x00100 true for second run  

if (pSymbolDictDecoder->SDHUFF == 0) {  

dwTemp = pSymbolDictDecoder->SDTEMPLATE == 0 ? 65536 : pSymbolDictDecoder->SDTEMPLATE == 1 ?  

8192 : 1024;  

gbContext = (JBig2ArithCtx\*)m\_pModule->JBig2\_Malloc2(sizeof(JBig2ArithCtx), dwTemp);  

JBIG2\_memcpy(gbContext, pLRSeg->m\_Result.sd->m\_gbContext, sizeof(JBig2ArithCtx)\*dwTemp);  

}  

if (pSymbolDictDecoder->SDREFAGG == 1) {  

dwTemp = pSymbolDictDecoder->SDRTEMPLATE ? 1 << 10 : 1 << 13;  

grContext = (JBig2ArithCtx\*)m\_pModule->JBig2\_Malloc2(sizeof(JBig2ArithCtx), dwTemp);  

JBIG2\_memcpy(grContext, pLRSeg->m\_Result.sd->m\_grContext, sizeof(JBig2ArithCtx)\*dwTemp);  

}  

} else {  

if (pSymbolDictDecoder->SDHUFF == 0) {  

dwTemp = pSymbolDictDecoder->SDTEMPLATE == 0 ? 65536 : pSymbolDictDecoder->SDTEMPLATE == 1 ?  

8192 : 1024;  

gbContext = (JBig2ArithCtx\*)m\_pModule->JBig2\_Malloc2(sizeof(JBig2ArithCtx), dwTemp);  

JBIG2\_memset(gbContext, 0, sizeof(JBig2ArithCtx)\*dwTemp);  

}  

if (pSymbolDictDecoder->SDREFAGG == 1) {  

dwTemp = pSymbolDictDecoder->SDRTEMPLATE ? 1 << 10 : 1 << 13;  

grContext = (JBig2ArithCtx\*)m\_pModule->JBig2\_Malloc2(sizeof(JBig2ArithCtx), dwTemp);  

JBIG2\_memset(grContext, 0, sizeof(JBig2ArithCtx)\*dwTemp);  

}  

}  

----- lower  

if(wFlags & 0x0200) { <-- setting flag 0x00200 true for first run  

pSegment->m\_Result.sd->m\_bContextRetained = TRUE;  

if(pSymbolDictDecoder->SDHUFF == 0) {  

pSegment->m\_Result.sd->m\_gbContext = gbContext;  

}  

if(pSymbolDictDecoder->SDREFAGG == 1) {  

pSegment->m\_Result.sd->m\_grContext = grContext;  

}  

bUsed = TRUE;  

} else {  

bUsed = FALSE;  

}

==28633==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x62500000e900 at pc 0x00000049ba24 bp 0x7ffeac351f40 sp 0x7ffeac3516f0  

READ of size 524288 at 0x62500000e900 thread T0  

#0 0x49ba23 in \_\_asan\_memcpy /home/skomski/Code/llvm-related/llvm/projects/compiler-rt/lib/asan/asan\_interceptors.cc:421  

#1 0x7a90ae in CJBig2\_Context::parseSymbolDict(CJBig2\_Segment\*, IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:768:13  

#2 0x7a4da2 in CJBig2\_Context::ProcessiveParseSegmentData(CJBig2\_Segment\*, IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:501:20  

#3 0x79f5df in CJBig2\_Context::parseSegmentData(CJBig2\_Segment\*, IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:491:19  

#4 0x79f5df in CJBig2\_Context::decode\_SquentialOrgnazation(IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:143  

#5 0x7a3dc0 in CJBig2\_Context::Continue(IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:257:24  

#6 0x7a39bf in CJBig2\_Context::getFirstPage(unsigned char\*, int, int, int, IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:244:15  

#7 0x786e68 in CCodec\_Jbig2Module::Decode(unsigned int, unsigned int, unsigned char const\*, unsigned int, unsigned char const\*, unsigned int, unsigned char\*, unsigned int) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/codec/fx\_codec\_jbig.cpp:38:15  

#8 0x4df2a6 in main /home/skomski/Code/pdf\_fuzzer/out/Release/../../samples/decoder\_main\_fuzzer.cc:27:3  

#9 0x7fa84efdd78f in \_\_libc\_start\_main (/usr/lib/libc.so.6+0x2078f)  

#10 0x41a828 in \_start (/home/skomski/Code/pdf\_fuzzer/out/Release/pdfium\_decoder\_main\_fuzzer+0x41a828)

0x62500000e900 is located 0 bytes to the right of 8192-byte region [0x62500000c900,0x62500000e900)  

allocated by thread T0 here:  

#0 0x4b09b0 in \_\_interceptor\_calloc /home/skomski/Code/llvm-related/llvm/projects/compiler-rt/lib/asan/asan\_malloc\_linux.cc:56  

#1 0x76d521 in FX\_AllocOrDie(unsigned long, unsigned long) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/codec/../../../include/fxcodec/../fxcrt/fx\_memory.h:37:24  

#2 0x76d521 in CPDF\_Jbig2Interface::JBig2\_Malloc2(unsigned int, unsigned int) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/codec/codec\_int.h:220

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/skomski/Code/llvm-related/llvm/projects/compiler-rt/lib/asan/asan\_interceptors.cc:421

==30822==ERROR: AddressSanitizer: SEGV on unknown address 0x000000001ff0 (pc 0x7f85208f9f29 bp 0x7ffc467b5f40 sp 0x7ffc467b56d8 T0)  

#0 0x7f85208f9f28 in \_\_memmove\_ssse3\_back (/usr/lib/libc.so.6+0x136f28)  

#1 0x49bacb in \_\_asan\_memcpy /home/skomski/Code/llvm-related/llvm/projects/compiler-rt/lib/asan/asan\_interceptors.cc:421  

#2 0x7a91f7 in CJBig2\_Context::parseSymbolDict(CJBig2\_Segment\*, IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:773:13  

#3 0x7a4da2 in CJBig2\_Context::ProcessiveParseSegmentData(CJBig2\_Segment\*, IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:501:20  

#4 0x79f5df in CJBig2\_Context::parseSegmentData(CJBig2\_Segment\*, IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:491:19  

#5 0x79f5df in CJBig2\_Context::decode\_SquentialOrgnazation(IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:143  

#6 0x7a3dc0 in CJBig2\_Context::Continue(IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:257:24  

#7 0x7a39bf in CJBig2\_Context::getFirstPage(unsigned char\*, int, int, int, IFX\_Pause\*) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/jbig2/JBig2\_Context.cpp:244:15  

#8 0x786e68 in CCodec\_Jbig2Module::Decode(unsigned int, unsigned int, unsigned char const\*, unsigned int, unsigned char const\*, unsigned int, unsigned char\*, unsigned int) /home/skomski/Code/pdf\_fuzzer/out/Release/../../core/src/fxcodec/codec/fx\_codec\_jbig.cpp:38:15  

#9 0x4df2a6 in main /home/skomski/Code/pdf\_fuzzer/out/Release/../../samples/decoder\_main\_fuzzer.cc:27:3  

#10 0x7f85207e378f in \_\_libc\_start\_main (/usr/lib/libc.so.6+0x2078f)  

#11 0x41a828 in \_start (/home/skomski/Code/pdf\_fuzzer/out/Release/pdfium\_decoder\_main\_fuzzer+0x41a828)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/usr/lib/libc.so.6+0x136f28) in \_\_memmove\_ssse3\_back

**REPRODUCTION CASE**

Attached a sample pdf.

## Attachments

- [pdfium-parseSymbolDict-Overflow.pdf](attachments/pdfium-parseSymbolDict-Overflow.pdf) (application/pdf, 532 B)
- [Screen Shot 2015-07-28 at 18.27.53.png](attachments/Screen Shot 2015-07-28 at 18.27.53.png) (image/png, 76.4 KB)
- [0001-Jbig2-Fix-multiple-bugs-in-JBig2_Context.patch](attachments/0001-Jbig2-Fix-multiple-bugs-in-JBig2_Context.patch) (application/octet-stream, 8.5 KB)
- [0001-Jbig2-Fix-multiple-bugs-in-JBig2_Context.patch](attachments/0001-Jbig2-Fix-multiple-bugs-in-JBig2_Context_53264104.patch) (application/octet-stream, 7.8 KB)

## Timeline

### lg...@chromium.org (2015-07-29)

Definitely causes a sadface for me.

Tom: As grand master of PDFium, would you mind triaging further?

### lg...@chromium.org (2015-07-29)

Remaining labels.

Tom, if a crash of the PDF plugin (in all tabs) usually considered low severity?

### ka...@skomski.com (2015-07-31)

I thought this would be at least medium severity. Based on the http://googlechromereleases.blogspot.de/2015/07/stable-channel-update_21.html pdfium issues are rated high severity because pdfium is not sandboxed per PDF and a malicious pdf could violate the same-origin-policy with buffer overflows or do these bugs all allow code execution? It's at least an out-of-bounds memory read/write.

I attached a patch that fixes this issue and multiple others that I encountered during fuzzing in Jbig2_Context.cpp.

### cl...@chromium.org (2015-07-31)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6230313728999424

### cl...@chromium.org (2015-07-31)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6502158382399488

### cl...@chromium.org (2015-07-31)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6230313728999424

Uploader: mbarbella@google.com
Job Type: linux_asan_pdfium
Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0x631000010800
Crash State:
  CJBig2_Context::parseSymbolDict
  CJBig2_Context::ProcessiveParseSegmentData
  CJBig2_Context::decode_SquentialOrgnazation
  

Minimized Testcase (0.52 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97elrISR10Rr14OWo3_8kdn12YvzRoGIzr_6fGbj4Kge8eA4_v0g8-WfkvZchC-K1ZjoCK5tOUXVmzjwWXA05aD3nl8C7ZKTjIwW-3FKTrQn-87z2omU1NygufF2hK0CELD8cwOvQL_oHw5NxbZqcOqoTYGPA



### mb...@chromium.org (2015-07-31)

It seems like this may be the same issue as https://crbug.com/chromium/476107. The test cases from that bug were never tagged as fixed by ClusterFuzz, and still seem to be reproducing in pdfium_test.

Also, agreed that medium severity seems more appropriate here.

### mb...@chromium.org (2015-07-31)

[Empty comment from Monorail migration]

### ka...@skomski.com (2015-08-17)

Rebased my patch on master because I continued fuzzing :)

### th...@chromium.org (2015-08-17)

Tim: Are there any issues with security bug reporters submitting fixes?
Karl: Assume there's no issues and you are interested... care to submit the patch for review rather than maintaining it here?

### ka...@skomski.com (2015-08-20)

Open to review: https://codereview.chromium.org/1298923002/

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-08)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### th...@chromium.org (2015-09-08)

I'll take this one. I'm working on just sanitizing the JBig2 code right now.

### cl...@chromium.org (2015-09-30)

thestig@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-10-09)

The JBig2 code has received a lot of cleaning in the last month. https://codereview.chromium.org/1388203003/ should kill off this bug.

There's still some bits in https://codereview.chromium.org/1298923002/ that may be relevant and can be submitted separately.

### bu...@chromium.org (2015-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1ef74c77625095af2d15ef993859b93157750447

commit 1ef74c77625095af2d15ef993859b93157750447
Author: thestig <thestig@chromium.org>
Date: Fri Oct 09 22:22:20 2015

Roll PDFium a398ca6..3acb1ef

https://pdfium.googlesource.com/pdfium.git/+log/a398ca6..3acb1ef

BUG=497357,541323,514891
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1403563002

Cr-Commit-Position: refs/heads/master@{#353405}

[modify] http://crrev.com/1ef74c77625095af2d15ef993859b93157750447/DEPS


### th...@chromium.org (2015-10-10)

tsepez: Should we try to merge this to M46? It'll take a bit more work.

I'll do the M47 merge early next week.

### ti...@google.com (2015-10-10)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2015-10-10)

[Empty comment from Monorail migration]

### ka...@skomski.com (2015-10-12)

Is this eligible for a bounty maybe in association with the provided patch?

### ss...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-10-12)

Yes it will be. In some time, it will automatically go for reward panel's consideration

### th...@chromium.org (2015-10-12)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-10-13)

The M-47 merge is not trivial, but out for review:
https://codereview.chromium.org/1396013005/
https://codereview.chromium.org/1399243003/

### bu...@chromium.org (2015-10-13)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=79532

------------------------------------------------------------------
r79532 | thestig@google.com | 2015-10-13T22:52:43.867170Z

-----------------------------------------------------------------

### th...@chromium.org (2015-10-13)

Merging to M46 is non-trivial, so I'm going to skip unless someone says otherwise.

### ti...@google.com (2015-11-10)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Congratulations Karl - our reward panel awarded you $2,000 for this report!

We'll credit you in our release notes as "karl@skomski.com". If you would like to use another name, please update with your preferred credit name and we can update the release notes. We'll also provide a CVE ID within a few hours for your reference.

A member from our finance team should reach out within a week to collect details. If that doesn't happen, please either update this bug or reach out to me directly at timwillis@.

Thanks again for your report!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2015-12-01)

CVE-2015-6778

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-16)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/514891?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082587)*
