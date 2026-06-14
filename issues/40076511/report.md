# Heap-use-after-free in skia::BGRAConvolve2D

| Field | Value |
|-------|-------|
| **Issue ID** | [40076511](https://issues.chromium.org/issues/40076511) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink, Blink>Layout |
| **Platforms** | Windows |
| **Reporter** | sl...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-10-25 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4

Steps to reproduce the problem:
Repro file:
----- crash1.html -----
<fieldset style="
    -webkit-margin-end: 99999;
    -webkit-animation: foo cubic-bezier(0.1, 0.1, 0.1, 0.1) 0s 1 normal both;
    -webkit-mask-box-image: url('foo.gif') 10000% 10000 9999999999%;
    ">
</fieldset>

What is the expected behavior?

What went wrong?
(1c3c.3dc): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=0322c002 ebx=00000000 ecx=0000002c edx=00000000 esi=0000001a edi=00000000
eip=54fa37e2 esp=0015d320 ebp=0015d354 iopl=0         nv up ei ng nz ac po cy
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010293
chrome_549d0000!skia::`anonymous namespace'::ConvolveHorizontally<0>+0x8b:
54fa37e2 0fb678fe        movzx   edi,byte ptr [eax-2]       ds:0023:0322c000=??

ExceptionAddress: 54fa37e2 (chrome_549d0000!skia::`anonymous namespace'::ConvolveHorizontally<0>+0x0000008b)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 0322c000
Attempt to read from address 0322c000

ChildEBP RetAddr  
0015d354 54e8b791 chrome_549d0000!skia::`anonymous namespace'::ConvolveHorizontally<0>+0x8b
0015d3cc 54e8a058 chrome_549d0000!skia::BGRAConvolve2D+0x127
0015d550 54e89a81 chrome_549d0000!skia::ImageOperations::ResizeBasic+0x2d5
0015d5b4 54e898b0 chrome_549d0000!WebCore::NativeImageSkia::resizedBitmap+0xea
0015d640 54e89575 chrome_549d0000!WebCore::extractScaledImageFragment+0x1f0
0015d764 54e55cef chrome_549d0000!WebCore::drawResampledBitmap+0x1df
0015d834 54e501b3 chrome_549d0000!WebCore::paintSkBitmap+0x34a
0015d894 54e4fff5 chrome_549d0000!WebCore::BitmapImage::draw+0x102
0015d8b0 54e4ff55 chrome_549d0000!WebCore::Image::draw+0x1e
0015d910 54e4f8e4 chrome_549d0000!WebCore::GraphicsContext::drawImage+0x14f
0015d958 551edbd3 chrome_549d0000!WebCore::GraphicsContext::drawImage+0x81
0015d9a4 54e7ec9e chrome_549d0000!WebCore::GraphicsContext::drawTiledImage+0x38
0015dab8 54f51919 chrome_549d0000!WebCore::RenderBoxModelObject::paintNinePieceImage+0x823
0015daf0 54f517cc chrome_549d0000!WebCore::RenderBox::paintMaskImages+0x144
0015db20 554755a7 chrome_549d0000!WebCore::RenderBox::paintMask+0x72
0015db50 54bad3ce chrome_549d0000!WebCore::RenderFieldset::paintMask+0x62
0015db98 54bb07b7 chrome_549d0000!WebCore::RenderBlock::paintObject+0x89
0015dbf0 54bac5a3 chrome_549d0000!WebCore::RenderBlock::paint+0x147
0015dd24 54babb18 chrome_549d0000!WebCore::RenderLayer::paintLayerContents+0xa21
0015dd58 54bab62e chrome_549d0000!WebCore::RenderLayer::paintLayerContentsAndReflection+0x7c
0015df5c 54bae352 chrome_549d0000!WebCore::RenderLayer::paintLayer+0x3a9
0015df98 54bac44f chrome_549d0000!WebCore::RenderLayer::paintList+0x5e
0015e0e4 54babb18 chrome_549d0000!WebCore::RenderLayer::paintLayerContents+0x8cd
0015e118 54bab62e chrome_549d0000!WebCore::RenderLayer::paintLayerContentsAndReflection+0x7c
0015e31c 54bae352 chrome_549d0000!WebCore::RenderLayer::paintLayer+0x3a9
0015e358 54bac44f chrome_549d0000!WebCore::RenderLayer::paintList+0x5e
0015e4a4 54babb18 chrome_549d0000!WebCore::RenderLayer::paintLayerContents+0x8cd
0015e4d8 54bab62e chrome_549d0000!WebCore::RenderLayer::paintLayerContentsAndReflection+0x7c
0015e6ec 54bab071 chrome_549d0000!WebCore::RenderLayer::paintLayer+0x3a9
0015e764 54baa29d chrome_549d0000!WebCore::RenderLayer::paint+0x7a
0015e7bc 55cf7659 chrome_549d0000!WebCore::FrameView::paintContents+0x21d
[...]

Did this work before? Yes 

Chrome version: 24.0.1305.3  Channel: dev
OS Version:

## Attachments

- [stack1.txt](attachments/stack1.txt) (text/x-c; charset=us-ascii, 14.1 KB)
- [crash1.html](attachments/crash1.html) (text/plain; charset=us-ascii, 229 B)
- [foo.gif](attachments/foo.gif) (image/gif; charset=binary, 23.6 KB)

## Timeline

### in...@chromium.org (2012-10-25)

Nice catch Slaweck! 

ClusterFuzz report coming.

### in...@chromium.org (2012-10-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=133031373

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f541c5d2450
Crash State:
  - crash stack -
  skia::BGRAConvolve2D
  skia::ImageOperations::ResizeBasic
  skia::ImageOperations::Resize
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=160318:160322

Minimized Testcase (22.11 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95qOsAmU4Ctp82dEHkvwiQy559DbwXEppKC4O3pRG-T1tCl2Bk7oJzMULg7Eu0UZ0KCsoLAaG9BPGb1EgjKovdJfl3S_o8r9mM03NJI1yYXwKBtMP2MpRB-Enmd3gaXJzQVwoo6SCX_S57T9qMHD_3yp1eItV8U1RNRiewYzkIpFG8AfKM

### in...@chromium.org (2012-10-25)

from regression range, definitely looks like https://trac.webkit.org/changeset/130412/

### [Deleted User] (2012-10-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=133343040

Fuzzer: Inferno_twister_custom_bundle

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f0a05f208b8
Crash State:
  - crash stack -
  skia::BGRAConvolve2D
  skia::ImageOperations::ResizeBasic
  - free stack -
  v8::internal::Zone::DeleteKeptSegment
  v8::internal::Compiler::BuildFunctionInfo
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=160318:160322

Minimized Testcase (0.67 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96SbkMLn-vqbMHzgG3RSWc74zhFIw1LTvo_PHYxClntOCrB6fiX9izoxQvID7TVZ4NICeWgxjCa_T0-NOEIe7LIM2OLj9-yknYVn7DhmbfmPyUZn79_08FIdeP9c5BkvYzGoGu_D5QyTZYz3QfdpJrlQBNPhC1o0fHSp_95z497qFL6cfI

### in...@chromium.org (2012-10-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=133147804

Fuzzer: Inferno_twister

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7ff00d9b47c0
Crash State:
  - crash stack -
  skia::BGRAConvolve2D
  skia::ImageOperations::ResizeBasic
  - free stack -
  v8::internal::Zone::DeleteKeptSegment
  v8::internal::Compiler::BuildFunctionInfo
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=160318:160322

Minimized Testcase (0.69 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95HKX_IyX2b-o3foL37mzEFXzC3xZeHz5T2w0MH6r-o22KSPgL5D2jCkzKNXN5LNxEo0Br7Ak_g2KvooMj6GoJFgA4C_UbsbntoCWAMHwf_9ux9UCtYAR6BPOOuX2dYKgdV0CfsTLa-09Ex2qCMuhL0GKZzFHJJXavgKQKUxF_G1qXl-BI

### [Deleted User] (2012-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2012-10-26)

Stepping through the trace. The source rectangle in paintSkBitmap gets way out of bounds. srcRect is {x=0, y=66, width=66, height=3355430} at paintSkBitmap.

While destRect is clipped to canvas there's nothing to prevent srcRect goes out of bound. I'll check previous code to see how this case is handled.



### [Deleted User] (2012-10-26)

Previous code use SkBitmap::extractSubset to get a sub-image first and then scale it while this code get the scaled image directly using scaled src-rect.

SkBitmap::extractSubset() returns an empty image if srcRect doesn't intersect and this logic should be used in paintSkBitmap. This should be a simple fix. I'll draft a patch with test.


### [Deleted User] (2012-10-27)

I have uploaded a patch to webkit: https://bugs.webkit.org/show_bug.cgi?id=100570.

Since this bug is an out-of-bounds access I made the change log implicit.


### in...@chromium.org (2012-10-29)

http://trac.webkit.org/changeset/132844. Since we are near branch point, we need to make sure that it is in. keeping merge-approved as a reminder.

### sc...@gmail.com (2012-11-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-11-20)

M24: http://trac.webkit.org/changeset/135210

### sc...@gmail.com (2012-12-04)

Thanks for catching this regression!
OOB read, with possible data egress => $500

### sc...@gmail.com (2012-12-14)

Payment in system.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/157845?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Layout]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076511)*
