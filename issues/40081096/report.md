# Heap-buffer-overflow in SkImageFilter::Common::unflatten

| Field | Value |
|-------|-------|
| **Issue ID** | [40081096](https://issues.chromium.org/issues/40081096) |
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

An integer overflow vulnerability exists in SkAutoSTArray::reset:

fArray = (T\*) sk\_malloc\_throw(count \* sizeof(T));

This may result in the allocation of an insufficiently sized buffer. This can for example be trigger through SkImageFilter::Common::allocInputs.

ASAN output:

# [0101/141438:INFO:filter\_fuzz\_stub.cc(59)] Test case: submission4/repro.fil

==11105==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf44009f0 at pc 0x081bef06 bp 0xffa7efd8 sp 0xffa7efd0  

WRITE of size 4 at 0xf44009f0 thread T0  

#0 0x81bef05 in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:89  

#1 0x858bdb1 in SkMergeImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkMergeImageFilter.cpp:112  

#2 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#3 0x81b9986 in SkValidatingDeserializeFlattenable(void const\*, unsigned int, SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#4 0x80f173f in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#5 0x80f1131 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#6 0x80f0cb4 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:81  

#7 0xf6ddfa82 in \_\_libc\_start\_main ??:?

0xf44009f1 is located 0 bytes to the right of 1-byte region [0xf44009f0,0xf44009f1)  

allocated by thread T0 here:  

#0 0x80d1ebb in **interceptor\_malloc ??:?  

#1 0x86338ab in sk\_malloc\_throw(unsigned int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/ext/SkMemory\_new\_handler.cpp:50  

#2 0x81be9ce in SkAutoSTArray<2, SkImageFilter\*>::reset(int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/skia/include/core/SkTemplates.h:295  

#3 0x81be8c9 in SkImageFilter::Common::allocInputs(int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:67  

#4 0x81bedd2 in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:86  

#5 0x858bdb1 in SkMergeImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkMergeImageFilter.cpp:112  

#6 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#7 0x81b9986 in SkValidatingDeserializeFlattenable(void const\*, unsigned int, SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#8 0x80f173f in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#9 0x80f1131 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#10 0x80f0cb4 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:81  

#11 0xf6ddfa82 in \_\_libc\_start\_main ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x3e8800e0: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa  

0x3e8800f0: fa fa 00 fa fa fa 00 fa fa fa 04 fa fa fa 04 fa  

0x3e880100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e880110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e880120: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x3e880130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa[01]fa  

0x3e880140: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x3e880150: fa fa fd fd fa fa fd fd fa fa 00 05 fa fa 00 04  

0x3e880160: fa fa 00 05 fa fa 00 07 fa fa 04 fa fa fa 00 fa  

0x3e880170: fa fa 04 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa  

0x3e880180: fa fa 00 fa fa fa 04 fa fa fa 00 fa fa fa 00 fa  

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

==11105==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-v8-arm-linux-release-309788

**REPRODUCTION CASE**  

Attached as repro.fil. Use 32-bit build of filter\_fuzz\_stub to reproduce.

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 36 B)

## Timeline

### in...@chromium.org (2015-01-01)

Wow! Super nice knockout CloudFuzzer@. We were missing fuzzing the 32-bit filter fuzz binary. Starting fuzzing now, but you probably did it nicely already :)

Sugoi@, I enabled your fuzzer on newly created 32-bit job type linux_asan_filter_fuzz_stub_32bit.

### cl...@chromium.org (2015-01-01)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6335076752162816

### cl...@chromium.org (2015-01-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6335076752162816

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xf5102ab0
Crash State:
  SkImageFilter::Common::unflatten
  SkMergeImageFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=284373:284382

Minimized Testcase (0.04 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95KINenjNPobXXfEikF-sNF4oKNGf9i2HNTwrCuP7pEf6Bebdi_8jox2j2daNyMiK4ynuB55A5fAA8cITUjPg-LtI5jQIQyoifAPpDv5ehwek4V9-SPhzi-6X1tWgB8HjNLETTQ4hekyPlYm8Ea6ELl37poxw



### cl...@chromium.org (2015-01-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5411215487533056

Fuzzer: Sugoi_filter_fuzzer
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xf5000e38
Crash State:
  SkImageFilter::Common::~Common
  SkMergeImageFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=284373:284382

Minimized Testcase (0.83 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94XG_7T1yTvJ6697FpckdIwwMtB013Lu0PJUQTC3m2eocZC-qtazgMIGaOAkMxeoNtTOADMQ4zXByfuACXZPxZFcFYYE5ZQooeGFKCo-m7TrQr4Ep5O0-2szna903kQj2od4-gMLlNOjEr10_TPQKZbLeKHTA

Filer: inferno

### fe...@chromium.org (2015-01-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### su...@chromium.org (2015-01-07)

This is running out of memory trying to allocate over a billion inputs at src/core/SkImageFilter.cpp:86

### [Deleted User] (2015-01-07)

Hmmm. running out of memory is fine (safe crash). I wonder if we just didn't allocate as much as we thought.

Could we have overflowed the computation of size here?

void SkImageFilter::Common::allocInputs(int count) {
    const size_t size = count * sizeof(SkImageFilter*);
    fInputs.reset(count);
    sk_bzero(fInputs.get(), size);
}

If size somehow was too small, then the reset() call could succeed, but not be big enough for all of count...

### su...@chromium.org (2015-01-07)

Yes, that's what's happening, just sent out a cl for review:
https://codereview.chromium.org/831583004/

### su...@chromium.org (2015-01-07)

cl has landed, marking as fixed.

### cl...@chromium.org (2015-01-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-01-08)

ClusterFuzz has detected this issue as fixed in range 310277:310430.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6335076752162816

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xf5102ab0
Crash State:
  SkImageFilter::Common::unflatten
  SkMergeImageFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=284373:284382
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=310277:310430

Minimized Testcase (0.04 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95KINenjNPobXXfEikF-sNF4oKNGf9i2HNTwrCuP7pEf6Bebdi_8jox2j2daNyMiK4ynuB55A5fAA8cITUjPg-LtI5jQIQyoifAPpDv5ehwek4V9-SPhzi-6X1tWgB8HjNLETTQ4hekyPlYm8Ea6ELl37poxw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-01-08)

ClusterFuzz has detected this issue as fixed in range 310277:310430.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5411215487533056

Fuzzer: Sugoi_filter_fuzzer
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xf5000e38
Crash State:
  SkImageFilter::Common::~Common
  SkMergeImageFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=284373:284382
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=310277:310430

Minimized Testcase (0.83 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94XG_7T1yTvJ6697FpckdIwwMtB013Lu0PJUQTC3m2eocZC-qtazgMIGaOAkMxeoNtTOADMQ4zXByfuACXZPxZFcFYYE5ZQooeGFKCo-m7TrQr4Ep5O0-2szna903kQj2od4-gMLlNOjEr10_TPQKZbLeKHTA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### pe...@google.com (2015-01-25)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### dx...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-23)

Did this end up on M40? If not, can someone confirm that this is *definitely* in M41?

### su...@chromium.org (2015-02-23)

It was not in m40. It is already in M41.

### aa...@google.com (2015-02-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $5000 for this report.

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/445810?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081096)*
