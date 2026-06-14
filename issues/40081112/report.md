# Security: OOM situation can result in heap buffer overflow in CFX_BinaryBuf (pdfium)

| Field | Value |
|-------|-------|
| **Issue ID** | [40081112](https://issues.chromium.org/issues/40081112) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-01-04 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

CFX\_BinaryBuf::ExpandBuf is implemented as follows:

void CFX\_BinaryBuf::ExpandBuf(FX\_STRSIZE add\_size)  

{  

FX\_STRSIZE new\_size = add\_size + m\_DataSize;  

if (m\_AllocSize >= new\_size) {  

return;  

}  

int alloc\_step;  

if (m\_AllocStep == 0) {  

alloc\_step = m\_AllocSize / 4;  

if (alloc\_step < 128 ) {  

alloc\_step = 128;  

}  

} else {  

alloc\_step = m\_AllocStep;  

}  

new\_size = (new\_size + alloc\_step - 1) / alloc\_step \* alloc\_step;  

FX\_LPBYTE pNewBuffer = m\_pBuffer;  

if (pNewBuffer) {  

pNewBuffer = FX\_Realloc(FX\_BYTE, m\_pBuffer, new\_size);  

} else {  

pNewBuffer = FX\_Alloc(FX\_BYTE, new\_size);  

}  

if (pNewBuffer) {  

m\_pBuffer = pNewBuffer;  

m\_AllocSize = new\_size;  

}  

}

The function doesn't return an error code, so a calling function can't tell whether a reallocation failed. If the call to FX\_Realloc fails pNewBuffer will be zero and m\_pBuffer will not be reassigned and the code will continue to run with the insufficient buffer size. This can for example be exploited through calls to CFX\_WideTextBuf::AppendChar:

void CFX\_WideTextBuf::AppendChar(FX\_WCHAR ch)  

{  

if (m\_AllocSize < m\_DataSize + (FX\_STRSIZE)sizeof(FX\_WCHAR)) {  

ExpandBuf(sizeof(FX\_WCHAR));  

}  

ASSERT(m\_pBuffer != NULL);  

\*(FX\_WCHAR\*)(m\_pBuffer + m\_DataSize) = ch;  

m\_DataSize += sizeof(FX\_WCHAR);  

}

**VERSION**  

Chrome Version: tested against latest pdfium\_test 32 and 64-bit.

**REPRODUCTION CASE**  

Reproduction of OOM issues is a little tricky. I have written a custom ASAN patch which allows me to limit the overall malloc'ed size, which makes issues like this easier to find and reliable to reproduce. The patch simulates the behaviour of a real world allocator (return null on failed allocation). The patch is attached as asan\_alloc\_limit.patch

Using an ASAN build with this patch allows us to reproduce the issue reliable using the attached test.pdf:

ASAN\_OPTIONS=asan\_alloc\_limit\_mb=256,allocator\_may\_return\_null=1 ./pdfium\_test ./test.pdf

# ==20607==WARNING: Hit total allocation size limit of 256MB while trying to allocate 2450560 bytes

==20607==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f741cdc0202 at pc 0x00000073dd58 bp 0x7fff890f75d0 sp 0x7fff890f75c8  

WRITE of size 1 at 0x7f741cdc0202 thread T0  

#0 0x73dd57 in AppendChar /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/../../../include/fpdfapi/../fxcrt/fx\_basic.h:63  

#1 0x724817 in GetObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:2115  

#2 0x725efa in GetObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:2191  

#3 0x7272d2 in ParseIndirectObjectAt /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:1399  

#4 0x7283c5 in ParseIndirectObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:1202  

#5 0x6ea71a in GetIndirectObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_objects.cpp:1218  

#6 0x6f8375 in GetDirect /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_objects.cpp:231  

#7 0x6cb036 in Start /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_parser\_old.cpp:958  

#8 0x642070 in StartParse /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:900  

#9 0x642232 in ParseContent /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:905  

#10 0x4ef64d in FPDF\_LoadPage /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:310  

#11 0x4e9a6d in RenderPdf /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:412  

#12 0x4eafc8 in main /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:512  

#13 0x7f742f1e8ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x7f741cdc0202 is located 0 bytes to the right of 1960450-byte region [0x7f741cbe1800,0x7f741cdc0202)  

allocated by thread T0 here:  

#0 0x4c8095 in \_\_interceptor\_realloc *asan\_rtl* (discriminator 2)  

#1 0xc0a511 in CFX\_BinaryBuf::ExpandBuf(int) /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fxcrt/fx\_basic\_buffer.cpp:87  

#2 0x73c8f8 in AppendByte /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/../../../include/fpdfapi/../fxcrt/fx\_basic.h:61  

#3 0x724817 in GetObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:2115  

#4 0x725efa in GetObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:2191  

#5 0x7272d2 in ParseIndirectObjectAt /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:1399  

#6 0x7283c5 in ParseIndirectObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:1202  

#7 0x6ea71a in GetIndirectObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_objects.cpp:1218  

#8 0x6f8375 in GetDirect /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_objects.cpp:231  

#9 0x6cb036 in Start /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_parser\_old.cpp:958  

#10 0x642070 in StartParse /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:900  

#11 0x642232 in ParseContent /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:905  

#12 0x4ef64d in FPDF\_LoadPage /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:310  

#13 0x4e9a6d in RenderPdf /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:412  

#14 0x4eafc8 in main /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:512  

#15 0x7f742f1e8ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

By setting allocator\_may\_return\_null=0 we can also confirm that the reallocation is failing:

ASAN\_OPTIONS=asan\_alloc\_limit\_mb=256,allocator\_may\_return\_null=0 ./pdfium\_test ./test.pdf

==2203==WARNING: Hit total allocation size limit of 256MB while trying to allocate 2450560 bytes  

==2203==AddressSanitizer's allocator is terminating the process instead of returning 0  

==2203==If you don't like this behavior set allocator\_may\_return\_null=1  

==2203==AddressSanitizer CHECK failed: /home/nils/build/llvm/projects/compiler-rt/lib/sanitizer\_common/sanitizer\_allocator.cc:146 "((0)) != (0)" (0x0, 0x0)  

#0 0x4cf944 in AsanCheckFailed *asan\_rtl*  

#1 0x4d6571 in \_\_sanitizer::CheckFailed(char const\*, int, char const\*, unsigned long long, unsigned long long) /home/nils/build/llvm/projects/compiler-rt/lib/sanitizer\_common/sanitizer\_common.cc:125  

#2 0x4d4f53 in \_\_sanitizer::ReportAllocatorCannotReturnNull() /home/nils/build/llvm/projects/compiler-rt/lib/sanitizer\_common/sanitizer\_allocator.cc:146 (discriminator 2)  

#3 0x44224e in ReturnNullOrDie /home/nils/build/llvm/projects/compiler-rt/lib/sanitizer\_common/sanitizer\_allocator.h:1310  

#4 0x442cc2 in Reallocate *asan\_rtl*  

#5 0x4c815e in \_\_interceptor\_realloc *asan\_rtl*  

#6 0xc0a511 in CFX\_BinaryBuf::ExpandBuf(int) /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fxcrt/fx\_basic\_buffer.cpp:87  

#7 0x73c8f8 in AppendByte /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/../../../include/fpdfapi/../fxcrt/fx\_basic.h:61  

#8 0x724817 in GetObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:2115  

#9 0x725efa in GetObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:2191  

#10 0x7272d2 in ParseIndirectObjectAt /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:1399  

#11 0x7283c5 in ParseIndirectObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:1202  

#12 0x6ea71a in GetIndirectObject /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_objects.cpp:1218  

#13 0x6f8375 in GetDirect /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_objects.cpp:231  

#14 0x6cb036 in Start /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_parser\_old.cpp:958  

#15 0x642070 in StartParse /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:900  

#16 0x642232 in ParseContent /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:905  

#17 0x4ef64d in FPDF\_LoadPage /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:310  

#18 0x4e9a6d in RenderPdf /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:412  

#19 0x4eafc8 in main /home/nils/build/targets/chrome/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:512  

#20 0x7ff7fc2e7ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287  

#21 0x440a3e in \_start ??:?

## Attachments

- [asan_alloc_limit.patch](attachments/asan_alloc_limit.patch) (application/octet-stream, 3.2 KB)
- [test.pdf.gz](attachments/test.pdf.gz) (application/x-gzip, 35.2 KB)

## Timeline

### wf...@chromium.org (2015-01-04)

Thanks for this.  Another issue where malloc() returning NULL instead of terminating the process is potentially bad.  We need to make sure that all dependent libaries have the allocator shim in place that should enforce this behavior - see https://crbug.com/chromium/434397.

Are you finding that without allocator_may_return_null=1 set, the allocator can return NULL in release/production builds of Chrome?

### wf...@chromium.org (2015-01-04)

[Empty comment from Monorail migration]

### cl...@gmail.com (2015-01-04)

wfh - allocator_may_return_null=1 is an ASAN only option so it won't have an effect on prod builds. Unless chrome does anything special the default behaviour for malloc/realloc is to return null on failure (in accordance to the man page). Is there a shim in place for pdfium?

### wf...@chromium.org (2015-01-04)

There is a shim but I think it's only in place for the main chrome dlls and not pdfium or ffmpeg. It's on my list for next week to investigate this more and see if we can put the same shim in place for ffmpeg and pdfium.

We can also set the heap options to raise exception on allocation failure.  See the cl in the bug I linked if you have any comments.

### cl...@chromium.org (2015-01-04)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6611165059743744

### fe...@chromium.org (2015-01-04)

inferno@, I don't know how to run clusterfuzz with this patch added to asan. can you take a look?

### in...@chromium.org (2015-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### ju...@foxitsoftware.com (2015-01-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-27)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ju...@foxitsoftware.com (2015-01-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-11)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### wf...@chromium.org (2015-02-11)

re: #3 pdfium is now contained inside chrome_child.dll so should gain the same memory protections as the rest of chrome - i.e. 2gb limit and also raising an exception on OOM.  I think this means we can close this.

### ka...@foxitsoftware.com (2015-02-11)

thanks for the update. could you please go ahead to close it or Foxit needs to assign it back to you?  -- Kai



### wf...@chromium.org (2015-02-11)

Even though pdf will now exception on OOM - the underlying bug is that CFX_BinaryBuf::ExpandBuf does not return a value so there is no way for the caller to know whether it succeeded or not.  I think this should be fixed, and return code handling happen appropriately.

### ka...@foxitsoftware.com (2015-02-11)

got it. we will take care of it.

### [Deleted User] (2015-02-12)

xref https://crbug.com/chromium/401995

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-26)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-10)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### ti...@google.com (2015-03-11)

Marking as blocking unless proven otherwise.

### [Deleted User] (2015-03-12)

My quickly looking at this issue, I think the problem is fairly clear and can be fixed as suggested in the original comment.
The https://crbug.com/chromium/401995 can possibly be unrelated and in this case it still requires separate investigation.

That being said, I'd vote for reversing the blocks/blockedon dependency or removing it.

### ti...@google.com (2015-03-12)

@timurrr: ack, unblocked.

@kai_jing: Can you please take care of this?

### ti...@google.com (2015-03-24)

@kai_jing - ping on this one as well please! :)

### ka...@foxitsoftware.com (2015-03-24)

ok, I will take care of the issue now. Thanks for reminder.

### ka...@foxitsoftware.com (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-04-17)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-04-20)

cloudfuzzer, I have prepared a patch to fix this issue. However, I haven't reproduced the issue that you raised. Seem that the ASAN patch you provided doesn't work in the last version of ASAN (some files are changed). Can you give me the updated patch to reproduce this issue? Also, please tell me how to apply customized ASAN so that it can replace the default one. Thanks!  

### cl...@gmail.com (2015-04-21)

Newer versions of clang have adopted a similar implementation to my patch. The binary builds use this version already. You can easily reproduce this issue using the following command line:

ASAN_OPTIONS=soft_rss_limit_mb=256,allocator_may_return_null=1 ./asan-symbolized-linux-release-324711/pdfium_test test.pdf

This page has information on how to build chromium with a custom clang version: https://www.chromium.org/developers/testing/addresssanitizer

### mb...@chromium.org (2015-04-24)

jun_fang: I've been able to reproduce this locally, and this doesn't seem to be fixed. Could you try with the ASAN_OPTIONS from c#31?


### ju...@foxitsoftware.com (2015-04-24)

Hi mbarbella, I reproduced this issue after I built pdfium_test using the custom Clang. Using the default clang in chrome, it can't produce this issue. Thanks for the information. 

### ti...@google.com (2015-05-07)

jun_fang@ - based on #33, are you suggesting that a fix isn't necessary?

### ju...@foxitsoftware.com (2015-05-14)

It's pending in https://codereview.chromium.org/1131363004/.

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-05-15)

Fixed in https://pdfium.googlesource.com/pdfium/+/9f6f34892fdfff87c49a9df4c1e34790c0fa1272.

### cl...@chromium.org (2015-05-16)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-07-08)

Merge-Request to M44 (2403) PDFium branch

### pe...@google.com (2015-07-08)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### pe...@google.com (2015-07-09)

Merge approved for M44 (2403) pdfium branch.  Please get it merged before end of business PST Monday.

### pe...@google.com (2015-07-10)

**And let me know the new branch hash after you commit.

### th...@chromium.org (2015-07-13)

Merged to M44 in https://pdfium.googlesource.com/pdfium/+/ce95f50e0ed551f6280f163a05b58031a3d011a9

I imagine we'll just do one DEPS roll once all the M44 pdfium fixes have been merged?

### pe...@chromium.org (2015-07-13)

Yup.  Once we sort out the other three, I'll just take the top of the m44 branch.  Thanks stig.

### pe...@chromium.org (2015-07-13)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-07-17)

I think this bug should be marked as no particular severity due to https://code.google.com/p/chromium/issues/detail?id=446032#c14, right? Any OOM will just crash the pdfium process.

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-17)

Congrats - $3,000 for this report.

### cl...@chromium.org (2015-08-22)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/446032?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/459654, crbug.com/chromium/465435, crbug.com/chromium/465740]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081112)*
