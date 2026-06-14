# Security: heap-buffer-overflow in SkGradientShaderBase::SkGradientShaderBase

| Field | Value |
|-------|-------|
| **Issue ID** | [40081376](https://issues.chromium.org/issues/40081376) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2015-02-09 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

The latest 32-bit ASAN build of filter\_fuzz\_stub crashes as follows:

=================================================================  

==29942==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf2a03ec0 at pc 0x085bff70 bp 0xffd32c18 sp 0xffd32c10  

WRITE of size 4 at 0xf2a03ec0 thread T0  

#0 0x85bff6f in SkGradientShaderBase::SkGradientShaderBase(SkGradientShaderBase::Descriptor const&, SkMatrix const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkGradientShader.cpp:185  

#1 0x85ca9e4 in SkLinearGradient::SkLinearGradient(SkPoint const\*, SkGradientShaderBase::Descriptor const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkLinearGradient.cpp:60  

#2 0x85c4f18 in SkGradientShader::CreateLinear(SkPoint const\*, unsigned int const\*, float const\*, int, SkShader::TileMode, unsigned int, SkMatrix const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkGradientShader.cpp:783  

#3 0x85cb258 in SkLinearGradient::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkLinearGradient.cpp:71  

#4 0x8297a9a in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#5 0x81e94d3 in SkShader\* SkReadBuffer::readFlattenable<SkShader>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#6 0x81e648b in SkReadBuffer::readShader() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:133  

#7 0x85b47fc in SkRectShaderImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkRectShaderImageFilter.cpp:39  

#8 0x8297a9a in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#9 0x81c9fc3 in SkImageFilter\* SkReadBuffer::readFlattenable<SkImageFilter>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#10 0x81c134b in SkReadBuffer::readImageFilter() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:129  

#11 0x81c0daa in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:89  

#12 0x85a0891 in SkMergeImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkMergeImageFilter.cpp:112  

#13 0x8297a9a in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#14 0x81c9fc3 in SkImageFilter\* SkReadBuffer::readFlattenable<SkImageFilter>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#15 0x81c134b in SkReadBuffer::readImageFilter() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:129  

#16 0x81c0daa in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:89  

#17 0x85417e3 in SkBlurImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkBlurImageFilter.cpp:43 (discriminator 1)  

#18 0x8297a9a in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#19 0x81bb896 in SkValidatingDeserializeFlattenable(void const\*, unsigned int, SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#20 0x80f176f in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#21 0x80f1161 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#22 0x80f0ce4 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:81  

#23 0xf6d8ba82 in \_\_libc\_start\_main ??:?

0xf2a03ec0 is located 0 bytes to the right of 576-byte region [0xf2a03c80,0xf2a03ec0)  

allocated by thread T0 here:  

#0 0x80d1eeb in **interceptor\_malloc ??:?  

#1 0x864e86b in sk\_malloc\_throw(unsigned int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/ext/SkMemory\_new\_handler.cpp:50  

#2 0x85beebc in SkGradientShaderBase::SkGradientShaderBase(SkGradientShaderBase::Descriptor const&, SkMatrix const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkGradientShader.cpp:111  

#3 0x85ca9e4 in SkLinearGradient::SkLinearGradient(SkPoint const\*, SkGradientShaderBase::Descriptor const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkLinearGradient.cpp:60  

#4 0x85c4f18 in SkGradientShader::CreateLinear(SkPoint const\*, unsigned int const\*, float const\*, int, SkShader::TileMode, unsigned int, SkMatrix const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkGradientShader.cpp:783  

#5 0x85cb258 in SkLinearGradient::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkLinearGradient.cpp:71  

#6 0x8297a9a in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#7 0x81e94d3 in SkShader\* SkReadBuffer::readFlattenable<SkShader>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#8 0x81e648b in SkReadBuffer::readShader() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:133  

#9 0x85b47fc in SkRectShaderImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkRectShaderImageFilter.cpp:39  

#10 0x8297a9a in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#11 0x81c9fc3 in SkImageFilter\* SkReadBuffer::readFlattenable<SkImageFilter>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#12 0x81c134b in SkReadBuffer::readImageFilter() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:129  

#13 0x81c0daa in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:89  

#14 0x85a0891 in SkMergeImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkMergeImageFilter.cpp:112  

#15 0x8297a9a in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#16 0x81c9fc3 in SkImageFilter\* SkReadBuffer::readFlattenable<SkImageFilter>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#17 0x81c134b in SkReadBuffer::readImageFilter() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:129  

#18 0x81c0daa in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:89  

#19 0x85417e3 in SkBlurImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkBlurImageFilter.cpp:43 (discriminator 1)  

#20 0x8297a9a in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#21 0x81bb896 in SkValidatingDeserializeFlattenable(void const\*, unsigned int, SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#22 0x80f176f in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#23 0x80f1161 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#24 0x80f0ce4 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:81  

#25 0xf6d8ba82 in \_\_libc\_start\_main ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x3e540780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e540790: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3e5407a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3e5407b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3e5407c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x3e5407d0: 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa fa fa  

0x3e5407e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e5407f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e540800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e540810: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e540820: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==29942==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-v8-arm-linux-release-315263

**REPRODUCTION CASE**  

Attached as repro.fil

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 372 B)

## Timeline

### js...@chromium.org (2015-02-09)

sugoi@ - Would you be the right person to take a look at this one?

### su...@chromium.org (2015-02-09)

Fix under review here:
https://codereview.chromium.org/904833003/

### js...@chromium.org (2015-02-09)

Thanks. Any idea how old this is? Specifially, if it impacts stable or beta?

### su...@chromium.org (2015-02-09)

The code I fixed is old, but the path that leads to it in this bug is fairly recent, so I'm not certain if it was possible to get there with these arguments before.

Also to note, this filter is marked as invalid right after this ASAN error occurs (even in 64 bits where the ASAN error wouldn't occur) and the filters are then deleted, so even if it's not recent, the validation code still works properly.

### js...@chromium.org (2015-02-09)

Thanks for the background. The memory will still be corrupted by the invalid write, even if the invalidity is detected, meaning it's still potentially exploitable. to be safe, I'll flag it as high and impacting stable for 32-bit only.

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-02-23)

sugoi: Looks like https://codereview.chromium.org/904833003/ already landed. Can we close this bug as fixed?

### su...@chromium.org (2015-02-23)

Yes, I'll mark it as fixed, but I wasn't sure if Justin wanted to request a merge for M41.

### cl...@chromium.org (2015-02-23)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-26)

@jschuh: let me know if you want to try to push this in a M41 patch, or whether we can let it roll into M42 (based on #7, it's already in M42).

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

Spoke to jschuh: let this roll into M42

### ti...@google.com (2015-04-09)

Congrats - $5,000 for this report.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-01)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/456828?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081376)*
