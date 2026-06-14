# Heap-use-after-free in GIFImageReader::decode

| Field | Value |
|-------|-------|
| **Issue ID** | [40077282](https://issues.chromium.org/issues/40077282) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Image |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-03-22 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

Ubuntu 12.04
Chromium ASAN 27.0.1450.0 (Developer Build 189819)


ASAN-report:

==10372== ERROR: AddressSanitizer: heap-use-after-free on address 0x601800020e70 at pc 0x7f4de44b3514 bp 0x7fff77adc1d0 sp 0x7fff77adc1c8
WRITE of size 1 at 0x601800020e70 thread T0 (chrome)
    #0 0x7f4de44b3513 in GIFImageReader::decode(WebCore::GIFImageDecoder::GIFQuery, unsigned int) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/platform/image-decoders/gif/GIFImageReader.cpp:364:0
    #1 0x7f4de4497848 in WebCore::GIFImageDecoder::decode(unsigned int, WebCore::GIFImageDecoder::GIFQuery) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/platform/image-decoders/gif/GIFImageDecoder.cpp:315:0
    #2 0x7f4de44972f7 in WebCore::GIFImageDecoder::isSizeAvailable() /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/platform/image-decoders/gif/GIFImageDecoder.cpp:60:0
    #3 0x7f4de403beba in WebCore::DeferredImageDecoder::isSizeAvailable() /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/platform/graphics/chromium/DeferredImageDecoder.cpp:151:0
    #4 0x7f4de3f64953 in WebCore::ImageSource::isSizeAvailable() /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/platform/graphics/ImageSource.cpp:104:0
    #5 0x7f4de3a7c447 in WebCore::BitmapImage::isSizeAvailable() /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/platform/graphics/BitmapImage.cpp:286:0
.
.
.
0x601800020e70 is located 112 bytes inside of 120-byte region [0x601800020e00,0x601800020e78)
freed by thread T0 (chrome) here:
    #0 0x7f4e0cb375f2 in free ??:0
    #1 0x7f4de0fac086 in WTF::fastFree(void*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:347:0
    #2 0x7f4de44a56d1 in GIFImageReader::operator delete(void*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/platform/image-decoders/gif/GIFImageReader.h:227:0
    #3 0x7f4de44a5441 in void WTF::deleteOwnedPtr<GIFImageReader>(GIFImageReader*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WTF/wtf/OwnPtrCommon.h:63:0
    #4 0x7f4de44a1cc4 in WTF::OwnPtr<GIFImageReader>::clear() /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WTF/wtf/OwnPtr.h:119:0
    #5 0x7f4de4499032 in WebCore::GIFImageDecoder::setFailed() /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/platform/image-decoders/gif/GIFImageDecoder.cpp:132:0
.
.
.


## Attachments

- [chrome-heap-use-after-free-GIFImageReaderdecode9.gif](attachments/chrome-heap-use-after-free-GIFImageReaderdecode9.gif) (image/gif; charset=binary, 30.8 KB)

## Timeline

### in...@chromium.org (2013-03-22)

Attekett told me this is a recent regression. CF report coming - https://cluster-fuzz.appspot.com/testcase?key=173921106

### in...@chromium.org (2013-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2013-03-22)

Thanks for reporting this. I think that's the problem. I'll submit a patch shortly.


### [Deleted User] (2013-03-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-03-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=173921106

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x60200002edf0
Crash State:
  - crash stack -
  GIFImageReader::decode
  WebCore::GIFImageDecoder::decode
  - free stack -
  WebCore::GIFImageDecoder::setFailed
  WebCore::GIFImageDecoder::setSize
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=189155:189667

Minimized Testcase (30.75 Kb): https://cluster-fuzz.appspot.com/download/AMIfv946trvg9DgJd0DCMpnzt57FEmhTMRA0Syn2vQuZtGEKMYzCzZM2EtX3QVakHJZbdBKKo70O1CEkBeIFnyQNJ9ckQ7V_uGe4Ti5B-JZvMiKfsq2Y9lUDjjkMwPdMpzwZN7AtErplwszn51LyU1CmvdB7sk4hXG2zF6NEqJ1XyAiq8uB9u_E

### in...@chromium.org (2013-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2013-03-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-24)

https://bugs.webkit.org/show_bug.cgi?id=113141


### in...@chromium.org (2013-03-25)

http://trac.webkit.org/changeset/146737

### in...@chromium.org (2013-03-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-03-27)

This bug still reproduces on chromium r190826 (with webkit "146873"). Aki's fuzzer confirms this. Reopening.

### [Deleted User] (2013-03-27)

Is there a trace for the latest repro? It doesn't crash the file provided. I have a hunch but it's good to confirm with a trace.


### in...@chromium.org (2013-03-27)

hclam, are you using an address sanitizer build ? you can always get the new crash stack, by uploading testcase to https://cluster-fuzz.appspot.com/#uploadusertestcase

### [Deleted User] (2013-03-27)

Okay will try.

### in...@chromium.org (2013-03-28)

Hclam@, The new stacktrace looks the same - see https://cluster-fuzz.appspot.com/testcase?key=172901502

### in...@chromium.org (2013-03-29)

fyi for the panel, Aki deserves a reward for this. Since his fuzzer corrected us that this bug is not fixed and acted as an easy regression test.

### [Deleted User] (2013-03-30)

Oooooh I see what's going on now. I'll have a fix in WebKit shortly.

### [Deleted User] (2013-04-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-04-02)

http://trac.webkit.org/changeset/147392

### [Deleted User] (2013-04-03)

Do I need to merge this to M27? I tried using drover but it's asking me for svn passwords in WebKit.


### sc...@gmail.com (2013-04-03)

We'll do it for you :)

### [Deleted User] (2013-04-03)

Whooops I merged already..

### [Deleted User] (2013-04-03)

Actually not! drover hanged for some reasons. This patch still needs to be merged.


### cl...@chromium.org (2013-04-16)

ClusterFuzz has detected this issue as fixed in range 191833:192049.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=173921106

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x60200002edf0
Crash State:
  - crash stack -
  GIFImageReader::decode
  WebCore::GIFImageDecoder::decode
  - free stack -
  WebCore::GIFImageDecoder::setFailed
  WebCore::GIFImageDecoder::setSize
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=189155:189667
Fixed: https://cluster-fuzz.appspot.com/revisions?range=191833:192049

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv946trvg9DgJd0DCMpnzt57FEmhTMRA0Syn2vQuZtGEKMYzCzZM2EtX3QVakHJZbdBKKo70O1CEkBeIFnyQNJ9ckQ7V_uGe4Ti5B-JZvMiKfsq2Y9lUDjjkMwPdMpzwZN7AtErplwszn51LyU1CmvdB7sk4hXG2zF6NEqJ1XyAiq8uB9u_E

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-04-16)

M27: https://src.chromium.org/viewvc/blink?view=rev&revision=148421

### sc...@gmail.com (2013-05-03)

Thank you attekett! $1000

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/223238?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/225481]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077282)*
