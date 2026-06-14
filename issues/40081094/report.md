# Stack-buffer-overflow in SkPackBits::Unpack8

| Field | Value |
|-------|-------|
| **Issue ID** | [40081094](https://issues.chromium.org/issues/40081094) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2015-01-01 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

This bug exists in the deserialisation routines for SKImageFilter, which can be triggered on the host process from a renderer through IPC (For example as part of an SwapCompositorFrame message). The filter\_fuzz\_stub binary can be used to reproduce the crash using the attached testcase (repro.fil).

ASAN output:

# [0101/134451:INFO:filter\_fuzz\_stub.cc(59)] Test case: submission2/repro.fil

==10833==ERROR: AddressSanitizer: stack-buffer-overflow on address 0xf5300990 at pc 0x08607ec9 bp 0xff8bf168 sp 0xff8bf160  

WRITE of size 1 at 0xf5300990 thread T0  

#0 0x8607ec8 in small\_memcpy(void\*, void const\*, unsigned int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkPackBits.cpp:24  

#1 0x86080eb in SkPackBits::Unpack8(unsigned char const\*, unsigned int, unsigned char\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkPackBits.cpp:316  

#2 0x859fbe9 in SkTable\_ColorFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkTableColorFilter.cpp:221  

#3 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#4 0x81e81f3 in SkColorFilter\* SkReadBuffer::readFlattenable<SkColorFilter>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#5 0x81e563b in SkReadBuffer::readColorFilter() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:127  

#6 0x85435ca in SkColorFilterImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkColorFilterImageFilter.cpp:89  

#7 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#8 0x81c8763 in SkImageFilter\* SkReadBuffer::readFlattenable<SkImageFilter>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#9 0x81bf3cb in SkReadBuffer::readImageFilter() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:129  

#10 0x81bee2a in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:89  

#11 0x8568eee in (anonymous namespace)::SkDiffuseLightingImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkLightingImageFilter.cpp:974 (discriminator 1)  

#12 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#13 0x81c8763 in SkImageFilter\* SkReadBuffer::readFlattenable<SkImageFilter>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#14 0x81bf3cb in SkReadBuffer::readImageFilter() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:129  

#15 0x81bee2a in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:89  

#16 0x852d003 in SkBlurImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkBlurImageFilter.cpp:43 (discriminator 1)  

#17 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#18 0x81b9986 in SkValidatingDeserializeFlattenable(void const\*, unsigned int, SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#19 0x80f173f in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#20 0x80f1131 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#21 0x80f0cb4 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:81  

#22 0xf6e6ba82 in \_\_libc\_start\_main ??:?

Address 0xf5300990 is located in stack of thread T0 at offset 2448 in frame  

#0 0x859f9af in SkTable\_ColorFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkTableColorFilter.cpp:206

This frame has 2 object(s):  

[16, 1296) 'packedStorage'  

[1424, 2448) 'unpackedStorage' <== Memory access at offset 2448 overflows this variable  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext  

(longjmp and C++ exceptions \*are\* supported)  

SUMMARY: AddressSanitizer: stack-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x3ea600e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3ea600f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3ea60100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3ea60110: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3ea60120: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x3ea60130: 00 00[f3]f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3  

0x3ea60140: f3 f3 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3ea60150: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3ea60160: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3ea60170: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3ea60180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==10833==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-v8-arm-linux-release-309788  

asan-symbolized-linux-release-309428

**REPRODUCTION CASE**  

Attached as repro.fil. Use filter\_fuzz\_stub to reproduce.

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 432 B)

## Timeline

### in...@chromium.org (2015-01-01)

Wow! Super nice knockout CloudFuzzer@. We were missing fuzzing the 32-bit filter fuzz binary. Starting fuzzing now, but you probably did it nicely already :)

Sugoi@, I enabled your fuzzer on newly created 32-bit job type linux_asan_filter_fuzz_stub_32bit.

### cl...@chromium.org (2015-01-01)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5690389972385792

### cl...@chromium.org (2015-01-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5690389972385792

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Stack-buffer-overflow WRITE 1
Crash Address: 0xf56b0190
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=286685:286847

Minimized Testcase (0.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv964LTB7u6E0s7F7_qyLkx5oWoEeWNYYtp-EBDgp_V6itL_A5xeUYW6vgIzu00_axaeDiXIDH6tQMenDg2MkuGQn4MO5hSVkhNn3i_nrynDcyj7qaBVWnvS0PBGIBfd5fVx7Xg1qR0sSsScV_pJIycMKHjQQfA



### cl...@chromium.org (2015-01-01)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2015-01-05)

    uint8_t unpackedStorage[4*256];
    size_t unpackedSize = SkPackBits::Unpack8(packedStorage, packedSize, unpackedStorage);

Unpack8 needs to check for bad input...

### se...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### cl...@chromium.org (2015-01-20)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-03)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-17)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-04)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-19)

ClusterFuzz has detected this issue as fixed in range 321145:321361.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5690389972385792

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Stack-buffer-overflow WRITE 1
Crash Address: 0xf56b0190
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=286685:286847
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=321145:321361

Minimized Testcase (0.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv964LTB7u6E0s7F7_qyLkx5oWoEeWNYYtp-EBDgp_V6itL_A5xeUYW6vgIzu00_axaeDiXIDH6tQMenDg2MkuGQn4MO5hSVkhNn3i_nrynDcyj7qaBVWnvS0PBGIBfd5fVx7Xg1qR0sSsScV_pJIycMKHjQQfA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-03-20)

ClusterFuzz has detected this issue as fixed in range 321145:321361.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5690389972385792

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Stack-buffer-overflow WRITE 1
Crash Address: 0xf56b0190
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=286685:286847
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=321145:321361

Minimized Testcase (0.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv964LTB7u6E0s7F7_qyLkx5oWoEeWNYYtp-EBDgp_V6itL_A5xeUYW6vgIzu00_axaeDiXIDH6tQMenDg2MkuGQn4MO5hSVkhNn3i_nrynDcyj7qaBVWnvS0PBGIBfd5fVx7Xg1qR0sSsScV_pJIycMKHjQQfA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-03-24)

Speculatively marking as fixed based on clusterfuzz. Please re-open if there's more work to do here.

### cl...@chromium.org (2015-03-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-04-08)

Don't know what fixed it, will let it roll in M43.

### ti...@google.com (2015-04-14)

Congrats cloudfuzzer - $2000 for this report.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-06-30)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/445808?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081094)*
