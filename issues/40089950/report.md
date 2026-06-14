# Heap-buffer-overflow in SkRecorder::onDrawPosTextH

| Field | Value |
|-------|-------|
| **Issue ID** | [40089950](https://issues.chromium.org/issues/40089950) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2017-12-19 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36

Steps to reproduce the problem:
1. build https://chromium.googlesource.com/chromium/src/+/65.0.3294.6/
2. run ./filter_fuzz_stub poc 

[1219/185539.631743:INFO:filter_fuzz_stub.cc(61)] Test case: ./poc234
=================================================================
==19983==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60d0000004d4 at pc 0x00000091335f bp 0x7ffe3748ff70 sp 0x7ffe3748ff68
READ of size 16 at 0x60d0000004d4 thread T0
    #0 0x91335e in copy<float> /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkRecorder.cpp:100
    #1 0x91335e in onDrawPosTextH /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkRecorder.cpp:269
    #2 0x91335e in ?? ??:0
    #3 0x7fb972 in _ZN8SkCanvas12drawPosTextHEPKvmPKffRK7SkPaint /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkCanvas.cpp:2587
    #4 0x7fb972 in ?? ??:0
    #5 0xf2ead3 in _ZN17SkPicturePlayback8handleOpEP12SkReadBuffer8DrawTypejP8SkCanvasRK8SkMatrix /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkPicturePlayback.cpp:530
    #6 0xf2ead3 in ?? ??:0
    #7 0xf2b40b in _ZN17SkPicturePlayback4drawEP8SkCanvasPN9SkPicture13AbortCallbackEP12SkReadBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkPicturePlayback.cpp:116
    #8 0xf2b40b in ?? ??:0
    #9 0xf2193c in Forwardport /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkPicture.cpp:142
    #10 0xf2193c in MakeFromBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkPicture.cpp:239
    #11 0xf2193c in ?? ??:0
    #12 0x1032cda in _ZN20SkPictureImageFilter10CreateProcER12SkReadBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/effects/SkPictureImageFilter.cpp:63
    #13 0x1032cda in ?? ??:0
    #14 0x8edb15 in _ZN12SkReadBuffer15readFlattenableEN13SkFlattenable4TypeE /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.cpp:444
    #15 0x8edb15 in ?? ??:0
    #16 0x85547e in readFlattenable<SkImageFilter> /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.h:149
    #17 0x85547e in readImageFilter /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.h:153
    #18 0x85547e in unflatten /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkImageFilter.cpp:130
    #19 0x85547e in ?? ??:0
    #20 0x1030222 in _ZN19SkOffsetImageFilter10CreateProcER12SkReadBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/effects/SkOffsetImageFilter.cpp:110
    #21 0x1030222 in ?? ??:0
    #22 0x8edb15 in _ZN12SkReadBuffer15readFlattenableEN13SkFlattenable4TypeE /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.cpp:444
    #23 0x8edb15 in ?? ??:0
    #24 0x85547e in readFlattenable<SkImageFilter> /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.h:149
    #25 0x85547e in readImageFilter /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.h:153
    #26 0x85547e in unflatten /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkImageFilter.cpp:130
    #27 0x85547e in ?? ??:0
    #28 0x1030222 in _ZN19SkOffsetImageFilter10CreateProcER12SkReadBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/effects/SkOffsetImageFilter.cpp:110
    #29 0x1030222 in ?? ??:0
    #30 0x8edb15 in _ZN12SkReadBuffer15readFlattenableEN13SkFlattenable4TypeE /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.cpp:444
    #31 0x8edb15 in ?? ??:0
    #32 0x8509ff in _ZN13SkFlattenable11DeserializeENS_4TypeEPKvmPK15SkDeserialProcs /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkFlattenable.cpp:145
    #33 0x8509ff in ?? ??:0
    #34 0x850c7f in _Z34SkValidatingDeserializeImageFilterPKvm /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkFlattenableSerialization.cpp:22
    #35 0x850c7f in ?? ??:0
    #36 0x4f14b0 in RunTestCase /home/qex/Repo/chromium/src/out/test/../../skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:33
    #37 0x4f14b0 in ReadAndRunTestCase /home/qex/Repo/chromium/src/out/test/../../skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:67
    #38 0x4f14b0 in main /home/qex/Repo/chromium/src/out/test/../../skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:87
    #39 0x4f14b0 in ?? ??:0
    #40 0x7fb10d2c382f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291
    #41 0x7fb10d2c382f in ?? ??:0

0x60d0000004d4 is located 0 bytes to the right of 132-byte region [0x60d000000450,0x60d0000004d4)
allocated by thread T0 here:
    #0 0x4ede42 in _Znwm _asan_rtl_
    #1 0x4ede42 in ?? ??:0
    #2 0x831671 in _ZN6SkData18PrivateNewWithCopyEPKvm /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkData.cpp:69
    #3 0x831671 in ?? ??:0
    #4 0x831a95 in _ZN6SkData17MakeUninitializedEm /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkData.cpp:104
    #5 0x831a95 in ?? ??:0
    #6 0xf25ffc in _ZN13SkPictureData14parseBufferTagER12SkReadBufferjj /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkPictureData.cpp:575
    #7 0xf25ffc in ?? ??:0
    #8 0xf28578 in parseBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkPictureData.cpp:653
    #9 0xf28578 in CreateFromBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkPictureData.cpp:622
    #10 0xf28578 in ?? ??:0
    #11 0xf218a3 in _ZN9SkPicture14MakeFromBufferER12SkReadBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkPicture.cpp:238
    #12 0xf218a3 in ?? ??:0
    #13 0x1032cda in _ZN20SkPictureImageFilter10CreateProcER12SkReadBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/effects/SkPictureImageFilter.cpp:63
    #14 0x1032cda in ?? ??:0
    #15 0x8edb15 in _ZN12SkReadBuffer15readFlattenableEN13SkFlattenable4TypeE /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.cpp:444
    #16 0x8edb15 in ?? ??:0
    #17 0x85547e in readFlattenable<SkImageFilter> /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.h:149
    #18 0x85547e in readImageFilter /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.h:153
    #19 0x85547e in unflatten /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkImageFilter.cpp:130
    #20 0x85547e in ?? ??:0
    #21 0x1030222 in _ZN19SkOffsetImageFilter10CreateProcER12SkReadBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/effects/SkOffsetImageFilter.cpp:110
    #22 0x1030222 in ?? ??:0
    #23 0x8edb15 in _ZN12SkReadBuffer15readFlattenableEN13SkFlattenable4TypeE /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.cpp:444
    #24 0x8edb15 in ?? ??:0
    #25 0x85547e in readFlattenable<SkImageFilter> /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.h:149
    #26 0x85547e in readImageFilter /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.h:153
    #27 0x85547e in unflatten /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkImageFilter.cpp:130
    #28 0x85547e in ?? ??:0
    #29 0x1030222 in _ZN19SkOffsetImageFilter10CreateProcER12SkReadBuffer /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/effects/SkOffsetImageFilter.cpp:110
    #30 0x1030222 in ?? ??:0
    #31 0x8edb15 in _ZN12SkReadBuffer15readFlattenableEN13SkFlattenable4TypeE /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkReadBuffer.cpp:444
    #32 0x8edb15 in ?? ??:0
    #33 0x8509ff in _ZN13SkFlattenable11DeserializeENS_4TypeEPKvmPK15SkDeserialProcs /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkFlattenable.cpp:145
    #34 0x8509ff in ?? ??:0
    #35 0x850c7f in _Z34SkValidatingDeserializeImageFilterPKvm /home/qex/Repo/chromium/src/out/test/../../third_party/skia/src/core/SkFlattenableSerialization.cpp:22
    #36 0x850c7f in ?? ??:0
    #37 0x4f14b0 in RunTestCase /home/qex/Repo/chromium/src/out/test/../../skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:33
    #38 0x4f14b0 in ReadAndRunTestCase /home/qex/Repo/chromium/src/out/test/../../skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:67
    #39 0x4f14b0 in main /home/qex/Repo/chromium/src/out/test/../../skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:87
    #40 0x4f14b0 in ?? ??:0
    #41 0x7fb10d2c382f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291
    #42 0x7fb10d2c382f in ?? ??:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/qex/Repo/chromium/src/out/test/filter_fuzz_stub+0x91335e)
Shadow bytes around the buggy address:
  0x0c1a7fff8040: 00 00 00 00 00 00 00 00 00 00 00 00 04 fa fa fa
  0x0c1a7fff8050: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c1a7fff8060: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c1a7fff8070: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1a7fff8080: fd fd fa fa fa fa fa fa fa fa 00 00 00 00 00 00
=>0x0c1a7fff8090: 00 00 00 00 00 00 00 00 00 00[04]fa fa fa fa fa
  0x0c1a7fff80a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1a7fff80b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1a7fff80c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1a7fff80d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1a7fff80e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==19983==ABORTING

What is the expected behavior?
no crash

What went wrong?
I will update root cause analysis asap.

Did this work before? N/A 

Chrome version: 65.0.3294.6  Channel: dev
OS Version: 14.0
Flash Version:

## Attachments

- [poc234](attachments/poc234) (text/plain, 372 B)

## Timeline

### el...@chromium.org (2017-12-19)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### cl...@chromium.org (2017-12-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6338957565755392.

### cl...@chromium.org (2017-12-19)

Detailed report: https://clusterfuzz.com/testcase?key=6338957565755392

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x6110000013c4
Crash State:
  SkRecorder::onDrawPosTextH
  SkCanvas::drawPosTextH
  SkPicturePlayback::handleOp
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=522280:522288

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6338957565755392

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### cl...@chromium.org (2017-12-19)

Automatically assigning owner based on suspected regression changelist https://skia.googlesource.com/skia/+/fadbfcd4aba676d44dfb08de1a83143a1c63b95c (upgrade SkReadBuffer to always validate).

If this is incorrect, please remove the owner and apply the Test-Predator-Wrong-CLs label.

### sh...@chromium.org (2017-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-20)

[Empty comment from Monorail migration]

### m....@gmail.com (2017-12-22)

when i test poc on version 64.0.3282.24, not crash occur,So I look for differences in them.

The very important point was found in SkPictureImageFilter::CreateProc

sk_sp<SkFlattenable> SkPictureImageFilter::CreateProc(SkReadBuffer& buffer) {
    sk_sp<SkPicture> picture;
    SkRect cropRect;

    if (buffer.isCrossProcess() && SkPicture::PictureIOSecurityPrecautionsEnabled()) {
        buffer.validate(!buffer.readBool());        <<--[1]
    } else {
        if (buffer.readBool()) {
            picture = SkPicture::MakeFromBuffer(buffer); <<--[2]
        }
    }
    
In version 64.0.3282.24,code will be executed to point [1]

In version 65.0.3294.6,code will be executed to point [2]

The reason they are different is the value of buffer.fFlags is different.

64.0.3282.24:fFlags = 0x8 
65.0.3294.6:fFlags = 0x6

enum Flags {
    kCrossProcess_Flag  = 1 << 0,
    kScalarIsFloat_Flag = 1 << 1,
    kPtrIs64Bit_Flag    = 1 << 2,
    kValidation_Flag    = 1 << 3,
};


So I keep looking for why fFlasg values are different

64.0.3282.24 will call setFlags to set value of fFlasg,but 65.0.3294.6 is not reach this function.

Breakpoint 3, 0x00007ffff7233834 in SkReadBuffer::setFlags (this=0x7fffffffc910, flags=0x8f0) at ../src/third_party/skia/src/core/SkReadBuffer.h:105
105	    void setFlags(uint32_t flags) { fFlags = flags; }
gdb$ bt
#0  0x00007ffff7233834 in SkReadBuffer::setFlags (this=0x7fffffffc910, flags=0x8f0) at ../src/third_party/skia/src/core/SkReadBuffer.h:105
#1  0x00007ffff72e0a12 in SkValidatingReadBuffer::SkValidatingReadBuffer (this=0x7fffffffc910, data=0x8f0a0343e20, size=0x174) at ../src/third_party/skia/src/core/SkValidatingReadBuffer.cpp:17
#2  0x00007ffff7184220 in SkValidatingDeserializeFlattenable (data=0x8f0a0343e20, size=0x174, type=SkFlattenable::kSkImageFilter_Type) at ../src/third_party/skia/src/core/SkFlattenableSerialization.cpp:25
#3  0x00007ffff71842af in SkValidatingDeserializeImageFilter (data=0x8f0a0343e20, size=0x174) at ../src/third_party/skia/src/core/SkFlattenableSerialization.cpp:30
#4  0x0000000000217a9b in (anonymous namespace)::RunTestCase (ipc_filter_message=..., bitmap=..., canvas=0x7fffffffd1a0) at ../src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:33
#5  0x0000000000217476 in (anonymous namespace)::ReadAndRunTestCase (filename=0x7fffffffe6cf "./poc234", bitmap=..., canvas=0x7fffffffd1a0) at ../src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:67
#6  0x00000000002171ea in main (argc=0x2, argv=0x7fffffffe408) at ../src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:87

I'm not quite sure what this fFlasg represents, but I think it is the root cause of the problem.

### cl...@chromium.org (2017-12-22)

ClusterFuzz has detected this issue as fixed in range 525782:525784.

Detailed report: https://clusterfuzz.com/testcase?key=6338957565755392

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x6110000013c4
Crash State:
  SkRecorder::onDrawPosTextH
  SkCanvas::drawPosTextH
  SkPicturePlayback::handleOp
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=522280:522288
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=525782:525784

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6338957565755392

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-12-22)

ClusterFuzz testcase 6338957565755392 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-12-22)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-02)

Hi reed@, #8 suggests the underlying bug might still exist, mind taking a look?

### sh...@chromium.org (2018-01-03)

reed: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-01-03)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/d1c65d6708de536a5971575809d7172fa4f54b37

commit d1c65d6708de536a5971575809d7172fa4f54b37
Author: Mike Reed <reed@google.com>
Date: Wed Jan 03 18:13:39 2018

remove unneeded readbuffer flags

- buffers are always 'cross-process'
- readbuffer is always validating

Bug:796107
Change-Id: I59614e9c29490c0b029c60d2aafe2806671bc9e1
Reviewed-on: https://skia-review.googlesource.com/90560
Reviewed-by: Mike Klein <mtklein@google.com>
Commit-Queue: Mike Reed <reed@google.com>

[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/effects/SkPictureImageFilter.cpp
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/core/SkPaint.cpp
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/core/SkReadBuffer.cpp
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/shaders/SkPictureShader.cpp
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/core/SkPicture.cpp
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/tools/debugger/SkJsonWriteBuffer.h
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/core/SkRecordedDrawable.cpp
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/tools/skpinfo.cpp
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/core/SkWriteBuffer.h
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/core/SkReadBuffer.h
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/core/SkPictureData.h
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/core/SkWriteBuffer.cpp
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/include/core/SkPicture.h
[modify] https://crrev.com/d1c65d6708de536a5971575809d7172fa4f54b37/src/core/SkPictureData.cpp


### re...@google.com (2018-01-04)

re: #8

Skia has removed those flags, ensuring that we always take the same code paths.

### hc...@google.com (2018-01-05)

I wanted to kick off a new CF run but cannot see the report on any of my accounts, trying to make myself owner to see if that helps (though I thought that restriction had been fixed/lifted?)

### hc...@google.com (2018-01-05)

CF shows fixed. 

After reed's change in #14 I think all issues are addressed here- mark as fixed?

### aw...@google.com (2018-01-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-01-12)

Groovy! The VRP Panel decided to reward $2,000 for this report. 

### aw...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### m....@gmail.com (2018-01-12)

[Comment Deleted]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2018-04-18)

Is this Issue assigned CVE?

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/796107?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089950)*
