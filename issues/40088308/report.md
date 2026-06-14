# Security: heap-buffer-overflow in gpu::gles2::GLES2Implementation::ReadPixels

| Field | Value |
|-------|-------|
| **Issue ID** | [40088308](https://issues.chromium.org/issues/40088308) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Windows |
| **Reporter** | tk...@googlemail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2017-07-10 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

There is a heap-based buffer overflow (memory write) in gpu::gles2::GLES2Implementation::ReadPixels.

The attached testcase crashes the latest ASAN build of Chrome on Windows 10 as follows (the complete stack trace can be found in asan.txt):

=================================================================  

==2556==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x23375a40 at pc 0x015500cc bp 0x0096a354 sp 0x0096a344  

WRITE of size 1000000 at 0x23375a40 thread T0  

#0 0x15500e6 in \_\_asan\_memcpy e:\b\build\slave\win\_upload\_clang\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_interceptors.cc:462  

#1 0x14ceaf52 in gpu::gles2::GLES2Implementation::ReadPixels(int,int,int,int,unsigned int,unsigned int,void \*) C:\b\c\b\win\_asan\_release\src\gpu\command\_buffer\client\gles2\_implementation.cc:4158:7  

..

The arguments to memcpy are as follows (see WinDbg\_Chrome\_Stable.txt for more details):

- src : canvas pixel (framebuffer) data (user-controlled)
- dest : heap-based buffer (pixels array) + unchecked offset (user-controlled)
- count: canvas width \* canvas height \* 4 (user-controlled)

This bug is obviously exploitable for remote code execution.

To reliably trigger a crash, the width and height of the canvas are set to the value 500. This results in a value of 1000000 (500 \* 500 \* 4) bytes to copy (see the second line of the ASAN output 'WRITE of size 1000000 ..').

Relevant source code snippets (see the comments inline marked with ###):

See <https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/graphics/gpu/DrawingBuffer.cpp>:

..  

1056 bool DrawingBuffer::PaintRenderingResultsToImageData(  

1057 int& width,  

1058 int& height,  

1059 SourceDrawingBuffer source\_buffer,  

1060 WTF::ArrayBufferContents& contents) {  

1061 ScopedStateRestorer scoped\_state\_restorer(this);  

1062  

1063 DCHECK(!premultiplied\_alpha\_);  

1064 width = Size().Width();  

1065 height = Size().Height();  

1066  

1067 CheckedNumeric<int> data\_size = 4;  

1068 data\_size \*= width;  

1069 data\_size \*= height;  

1070 if (!data\_size.IsValid())  

1071 return false;  

1072  

1073 WTF::ArrayBufferContents pixels(width \* height, 4, ### allocation of the heap-based destination buffer  

1074 WTF::ArrayBufferContents::kNotShared,  

1075 WTF::ArrayBufferContents::kDontInitialize);  

..

See <https://cs.chromium.org/chromium/src/gpu/command_buffer/client/gles2_implementation.cc>:

..  

4001 void GLES2Implementation::ReadPixels(  

4002 GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format,  

4003 GLenum type, void\* pixels) {  

..  

4106 // Advance pixels pointer past the skip rows and skip pixels  

4107 dest += skip\_size; ### heap-based destination buffer + unchecked user-controlled offset  

..  

4153 if (padded\_row\_size == unpadded\_row\_size &&  

4154 (pack\_row\_length\_ == 0 || pack\_row\_length\_ == width) &&  

4155 result->row\_length == width && result->num\_rows == num\_rows) {  

4156 // The pixels are tightly packed.  

4157 uint32\_t copy\_size = unpadded\_row\_size \* num\_rows;  

4158 memcpy(dest, src, copy\_size); ### heap buffer overflow  

..

**VERSION**

Tested on:

- Chrome Stable Version 59.0.3071.115 (64-Bit, Windows 10)
- asan-win32-release-485195

**REPRODUCTION CASE**

Provided files:

- testcase.html -- Minimal testcase to trigger the issue.
- asan.txt -- Detailed ASAN output (Windows 10).
- WinDbg\_Chrome\_Stable.txt -- Further debugging information (Chrome Stable on Windows 10).

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: tab

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 623 B)
- [asan.txt](attachments/asan.txt) (text/plain, 7.6 KB)
- [WinDbg_Chrome_Stable.txt](attachments/WinDbg_Chrome_Stable.txt) (text/plain, 12.2 KB)

## Timeline

### cl...@chromium.org (2017-07-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5980605807591424.

### cl...@chromium.org (2017-07-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6622678185410560.

### ra...@chromium.org (2017-07-11)

jbauman: could you please help triage? 

[Monorail components: Internals>GPU>Internals]

### jb...@chromium.org (2017-07-11)

zmo@, I think the implementation of pack_skip_rows was added in https://chromium.googlesource.com/chromium/src/+/c6c114178c562feeddfc4d41a33b9999698a4144

### sh...@chromium.org (2017-07-11)

[Empty comment from Monorail migration]

### pi...@chromium.org (2017-07-11)

We need to reset pack parameters before ReadPixels. For example we currently reset GL_PACK_ALIGNMENT on https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/graphics/gpu/DrawingBuffer.cpp?l=1110 . But there are more such parameters in ES3/WebGL2 contexts, namely GL_PACK_ROW_LENGTH, GL_PACK_SKIP_ROWS, GL_PACK_SKIP_PIXELS.

I wonder if similar things might be true when uploading textures from e.g. images (GL_UNPACK_* states).

### pi...@chromium.org (2017-07-11)

Oh, GL_PIXEL_PACK_BUFFER needs to be reset too...

### zm...@chromium.org (2017-07-12)

[Empty comment from Monorail migration]

### zm...@chromium.org (2017-07-13)

Conformance test is added in https://github.com/KhronosGroup/WebGL/pull/2457/

Chromium side fix is in https://chromium-review.googlesource.com/c/570840/

### bu...@chromium.org (2017-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f6ac1dba5e36f338a490752a2cbef3339096d9fe

commit f6ac1dba5e36f338a490752a2cbef3339096d9fe
Author: Zhenyao Mo <zmo@chromium.org>
Date: Thu Jul 13 23:08:53 2017

Reset ES3 pixel pack parameters and PIXEL_PACK_BUFFER binding in DrawingBuffer before ReadPixels() and recover them later.

BUG=740603
TEST=new conformance test
R=kbr@chromium.org,piman@chromium.org

Change-Id: I3ea54c6cc34f34e249f7c8b9f792d93c5e1958f4
Reviewed-on: https://chromium-review.googlesource.com/570840
Reviewed-by: Antoine Labour <piman@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#486518}
[modify] https://crrev.com/f6ac1dba5e36f338a490752a2cbef3339096d9fe/third_party/WebKit/Source/modules/webgl/WebGL2RenderingContextBase.cpp
[modify] https://crrev.com/f6ac1dba5e36f338a490752a2cbef3339096d9fe/third_party/WebKit/Source/modules/webgl/WebGL2RenderingContextBase.h
[modify] https://crrev.com/f6ac1dba5e36f338a490752a2cbef3339096d9fe/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp
[modify] https://crrev.com/f6ac1dba5e36f338a490752a2cbef3339096d9fe/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.h
[modify] https://crrev.com/f6ac1dba5e36f338a490752a2cbef3339096d9fe/third_party/WebKit/Source/platform/graphics/gpu/DrawingBuffer.cpp
[modify] https://crrev.com/f6ac1dba5e36f338a490752a2cbef3339096d9fe/third_party/WebKit/Source/platform/graphics/gpu/DrawingBuffer.h
[modify] https://crrev.com/f6ac1dba5e36f338a490752a2cbef3339096d9fe/third_party/WebKit/Source/platform/graphics/gpu/DrawingBufferTestHelpers.h


### zm...@chromium.org (2017-07-14)

M59 is too late to merge in, but I think it's worth merging back to M60.

### sh...@chromium.org (2017-07-14)

This bug requires manual review: We are only 10 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-07-15)

Since we are only 10 days away from Stable, the bar for merges to M60 is very high. My recommendation is to wait until M61. I'm rejecting this merge for now, but if you think otherwise please re-apply Merge-Request-60 label with justification for why this should be merged, and if it's a very safe merge.

### ab...@chromium.org (2017-07-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-08-08)

tk.chromium@ - nice one! The VRP panel decided to award $5,000 for this bug!

Also, if this appears in Chrome release notes, how would you like to be credited?

### aw...@chromium.org (2017-08-09)

[Empty comment from Monorail migration]

### tk...@googlemail.com (2017-08-09)

Thanks for the award! Please credit me as "Tobias Klein (www.trapkit.de)".

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/740603?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088308)*
