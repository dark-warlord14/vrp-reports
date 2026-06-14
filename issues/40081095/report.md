# Heap-buffer-overflow in SkBitmap::ReadRawPixels

| Field | Value |
|-------|-------|
| **Issue ID** | [40081095](https://issues.chromium.org/issues/40081095) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2015-01-01 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

This bug exists in the deserialisation routines for SKImageFilter, which can be triggered on the host process from a renderer through IPC (For example as part of an SwapCompositorFrame message). The filter\_fuzz\_stub binary can be used to reproduce the crash using the attached testcase (repro.fil).

ASAN output:

# [0101/140254:INFO:filter\_fuzz\_stub.cc(59)] Test case: submission3/repro.fil

==11019==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xecbcdd58 at pc 0x080b9942 bp 0xffdbadd8 sp 0xffdba9b8  

WRITE of size 96 at 0xecbcdd58 thread T0  

#0 0x80b9941 in **asan\_memmove ??:?  

#1 0x817b397 in SkBitmap::ReadRawPixels(SkReadBuffer\*, SkBitmap\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/skia/src/core/SkBitmap.cpp:1220  

#2 0x822ad3d in SkReadBuffer::readBitmap(SkBitmap\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.cpp:268  

#3 0x852a322 in SkBitmapSource::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkBitmapSource.cpp:34  

#4 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#5 0x81b9986 in SkValidatingDeserializeFlattenable(void const\*, unsigned int, SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#6 0x80f173f in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#7 0x80f1131 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#8 0x80f0cb4 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:81  

#9 0xf6e02a82 in \_\_libc\_start\_main ??:?

0xecbcdd58 is located 2728 bytes to the left of 100862232-byte region [0xecbce800,0xf2bff118)  

allocated by thread T0 here:  

#0 0x80d1ebb in **interceptor\_malloc ??:?  

#1 0x86338ab in sk\_malloc\_throw(unsigned int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/ext/SkMemory\_new\_handler.cpp:50  

#2 0x819ed53 in SkData::PrivateNewWithCopy(void const\*, unsigned int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/skia/src/core/SkData.cpp:66  

#3 0x819f113 in SkData::NewUninitialized(unsigned int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkData.cpp:101  

#4 0x817b2ce in SkBitmap::ReadRawPixels(SkReadBuffer\*, SkBitmap\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmap.cpp:1212  

#5 0x822ad3d in SkReadBuffer::readBitmap(SkBitmap\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.cpp:268  

#6 0x852a322 in SkBitmapSource::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkBitmapSource.cpp:34  

#7 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#8 0x81b9986 in SkValidatingDeserializeFlattenable(void const\*, unsigned int, SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#9 0x80f173f in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#10 0x80f1131 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#11 0x80f0cb4 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:81  

#12 0xf6e02a82 in \_\_libc\_start\_main ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x3d979b50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3d979b60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3d979b70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3d979b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3d979b90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x3d979ba0: fa fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa  

0x3d979bb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3d979bc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3d979bd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3d979be0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3d979bf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

Left alloca redzone: ca  

Right alloca redzone: cb  

==11019==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-v8-arm-linux-release-309788

**REPRODUCTION CASE**  

Attached as repro.fil. Use 32-bit build of filter\_fuzz\_stub to reproduce.

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 88 B)

## Timeline

### in...@chromium.org (2015-01-01)

Wow! Super nice knockout CloudFuzzer@. We were missing fuzzing the 32-bit filter fuzz binary. Starting fuzzing now, but you probably did it nicely already :)

Sugoi@, I enabled your fuzzer on newly created 32-bit job type linux_asan_filter_fuzz_stub_32bit.

### cl...@chromium.org (2015-01-01)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5759552904495104

### cl...@chromium.org (2015-01-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5759552904495104

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0xed4cdd58
Crash State:
  SkBitmap::ReadRawPixels
  SkReadBuffer::readBitmap
  SkBitmapSource::CreateProc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=291444:291576

Minimized Testcase (0.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95FKiEs2RCLejW2YtVEsEkaBaKuMM4KklnyXPbKwo9o39RIQiP1rxfPq65Jk70Kc-qCUtQp1BvCN3zz0ikJc5POLjtaQpaisjiTv9YTHXA7zvYvmm8O0H2pfMI5QBo3eU1J3cefgnUKxfwsS8bIKJyUoqFeVg



### cl...@chromium.org (2015-01-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-04)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4991856835297280

Fuzzer: Sugoi_filter_fuzzer
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0xf19fe7b8
Crash State:
  SkBitmap::ReadRawPixels
  SkReadBuffer::readBitmap
  SkBitmapSource::CreateProc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=291444:291576

Minimized Testcase (2.52 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97-Pjl9kfiJUoN0RFf606MHHvWizSVsY9sUuhK8_hfBDWXKQKrgU2S6br_xkcK_z5h9gPWUg8E_YfSWNTaZYUkvbMP5r-gt7TiFjECB7FtMxdYvRJKaie-n5xjxCXRnB87YDRursGU6vXAvk0MjMgk-qI4b0A

Filer: inferno

### fe...@chromium.org (2015-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2015-01-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### su...@chromium.org (2015-01-07)

Cause by a large height which pushes the overall size to exceed the 32b (size_t) range. Similar to crbug.com/445831, but caused by height instead of rowBytes. The fix for 445831 will also fix this issue and can be found here:
https://codereview.chromium.org/836733005/

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-01-08)

ClusterFuzz has detected this issue as fixed in range 310277:310430.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5759552904495104

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0xed4cdd58
Crash State:
  SkBitmap::ReadRawPixels
  SkReadBuffer::readBitmap
  SkBitmapSource::CreateProc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=291444:291576
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=310277:310430

Minimized Testcase (0.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95FKiEs2RCLejW2YtVEsEkaBaKuMM4KklnyXPbKwo9o39RIQiP1rxfPq65Jk70Kc-qCUtQp1BvCN3zz0ikJc5POLjtaQpaisjiTv9YTHXA7zvYvmm8O0H2pfMI5QBo3eU1J3cefgnUKxfwsS8bIKJyUoqFeVg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### se...@chromium.org (2015-01-08)

w00t! Thanks for the quick turnaround on this and the other 32-bit bugs, Alexis!

### cl...@chromium.org (2015-01-09)

ClusterFuzz has detected this issue as fixed in range 310277:310430.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4991856835297280

Fuzzer: Sugoi_filter_fuzzer
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0xf19fe7b8
Crash State:
  SkBitmap::ReadRawPixels
  SkReadBuffer::readBitmap
  SkBitmapSource::CreateProc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=291444:291576
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=310277:310430

Minimized Testcase (2.52 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97-Pjl9kfiJUoN0RFf606MHHvWizSVsY9sUuhK8_hfBDWXKQKrgU2S6br_xkcK_z5h9gPWUg8E_YfSWNTaZYUkvbMP5r-gt7TiFjECB7FtMxdYvRJKaie-n5xjxCXRnB87YDRursGU6vXAvk0MjMgk-qI4b0A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### pe...@google.com (2015-01-25)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### dx...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-26)

This is in M41 based on https://codereview.chromium.org/836733005/

### ti...@google.com (2015-03-03)

Unfortunately this appears to be dupe of the fix to https://crbug.com/chromium/445831 (see https://crbug.com/chromium/445809#c9), so it's not eligible for reward (fuzzer hit on the same day).

### ti...@google.com (2015-03-03)

TL;DR - $5,000 for this report, even though it collided with one of our fuzzers.

I was looking at the timing of 455831 and spoke to our FuzzerMasters. It turns out that based on this report, they retrained their fuzzers and 455831 popped out, so it would be unfair not to pay you $5,000 for this report.

I'll update with a CVE later.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-07)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-04-15)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### is...@google.com (2018-01-22)

This issue was migrated from crbug.com/chromium/445809?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081095)*
