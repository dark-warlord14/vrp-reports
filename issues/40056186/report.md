# Security: [ANGLE] Out-of-bounds write in Renderer11::blitRenderbufferRect

| Field | Value |
|-------|-------|
| **Issue ID** | [40056186](https://issues.chromium.org/issues/40056186) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | gg...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2021-06-11 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

There is a out-of-bounds write bug that is caused by the Renderer11::blitRenderbufferRect function when blitFramebuffer function is called.

blitFramebuffer(srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, dstX1, dstY1, mask, filter);

The blitFramebuffer function copies a specific area from READ\_FRAMEBUFFER to DRAW\_FRAMEBUFFER. This areas is a rectangle, so this function needs the coordinates of two points representing the rectangle.

Possible cases are (x0,y0)-(x1,y1) or (x1,y1)-(x0,y0) or (x1,y0)-(x0,y1) or (x0,y1)-(x1,y0).  

This function should handle all cases, so the blitFramebuffer should normalize its arguments.  

(For example, "blitFramebuffer(0, 0, 10, 10, 0, 0, 10 10);" and "blitFramebuffer(10, 0, 0, 10, 0, 0, 10, 10);" have the same effect.  

So in this case, function needs to flip srcX0 and srcX1.)

**-------------------------** --------------------------------------------------------------  

void Context::blitFramebuffer(GLint srcX0,  

GLint srcY0,  

GLint srcX1,  

GLint srcY1,  

GLint dstX0,  

GLint dstY0,  

GLint dstX1,  

GLint dstY1,  

GLbitfield mask,  

GLenum filter)  

{  

.....

```
Rectangle srcArea(srcX0, srcY0, srcX1 - srcX0, srcY1 - srcY0);  
Rectangle dstArea(dstX0, dstY0, dstX1 - dstX0, dstY1 - dstY0);  

if (dstArea.width == 0 || dstArea.height == 0)  
{  
    return;  
}  

ANGLE_CONTEXT_TRY(syncStateForBlit());  

ANGLE_CONTEXT_TRY(drawFramebuffer->blit(this, srcArea, dstArea, mask, filter));  

```

}  

**-------------------------** --------------------------------------------------------------

In Context::blitFramebuffer, the width and height of areas are calculated as (X1 - X0) and (Y1 - Y0).  

If srcX0 is greater than srcX1, width will be negative.

Next, the blitRenderbufferRect function will be called.  

(readRectIn is srcArea, and drawRectIn is dstArea)

**-------------------------** --------------------------------------------------------------  

angle::Result Renderer11::blitRenderbufferRect(const gl::Context \*context,  

const gl::Rectangle &readRectIn,  

const gl::Rectangle &drawRectIn,  

RenderTargetD3D \*readRenderTarget,  

RenderTargetD3D \*drawRenderTarget,  

GLenum filter,  

const gl::Rectangle \*scissor,  

bool colorBlit,  

bool depthBlit,  

bool stencilBlit)  

{  

.....

```
gl::Rectangle readRect = readRectIn;  
gl::Rectangle drawRect = drawRectIn;  
if (readRect.isReversedX())  
{  
    readRect.x     = readRect.x + readRect.width;  
    readRect.width = -readRect.width;  
    drawRect.x     = drawRect.x + drawRect.width;  
    drawRect.width = -drawRect.width;  
}  
if (readRect.isReversedY())  
{  
    readRect.y      = readRect.y + readRect.height;  
    readRect.height = -readRect.height;  
    drawRect.y      = drawRect.y + drawRect.height;  
    drawRect.height = -drawRect.height;  
}  

.....  

else  
{  
    gl::Box readArea(readRect.x, readRect.y, 0, readRect.width, readRect.height, 1);  
    gl::Box drawArea(drawRect.x, drawRect.y, 0, drawRect.width, drawRect.height, 1);  

    if (depthBlit && stencilBlit)  
    {  
        ANGLE_TRY(mBlit->copyDepthStencil(context, readTexture, readSubresource, readArea,  
                                          readSize, drawTexture, drawSubresource, drawArea,  
                                          drawSize, scissor));  
    }  

....  

```

**-------------------------** --------------------------------------------------------------

The isReservedX method returns true when width is negative.  

If readRect.width is negative, the flip operation will be executed.  

However, the flip operation will also be executed on drawRect where drawRect.width may be positive.  

If drawRect.width is positive, the above code will be executed and drawRect.width will be negative.

In order to trigger this vulnerability, the copyDepthStencil function in above code should be executed.  

The copyDepthStencil function can call the StretchedBlitNearest\_RowByRow function.

**-------------------------** --------------------------------------------------------------  

void StretchedBlitNearest\_RowByRow(const gl::Box &sourceArea,  

const gl::Box &destArea,  

const gl::Rectangle &clippedDestArea,  

const gl::Extents &sourceSize,  

unsigned int sourceRowPitch,  

unsigned int destRowPitch,  

size\_t pixelSize,  

const uint8\_t \*sourceData,  

uint8\_t \*destData)  

{  

int srcHeightSubOne = (sourceArea.height - 1);  

size\_t copySize = pixelSize \* destArea.width; <== destArea.width can be negative.  

size\_t srcOffset = sourceArea.x \* pixelSize;  

size\_t destOffset = destArea.x \* pixelSize;

```
for (int y = clippedDestArea.y; y < clippedDestArea.y + clippedDestArea.height; y++)  
{  
    float yPerc = static_cast<float>(y - destArea.y) / (destArea.height - 1);  

    // Interpolate using the original source rectangle to determine which row to sample from  
    // while clamping to the edges  
    unsigned int readRow = static_cast<unsigned int>(  
        gl::clamp(sourceArea.y + floor(yPerc \* srcHeightSubOne + 0.5f), 0, srcHeightSubOne));  
    unsigned int writeRow = y;  

    const uint8_t \*sourceRow = sourceData + readRow \* sourceRowPitch + srcOffset;  
    uint8_t \*destRow         = destData + writeRow \* destRowPitch + destOffset;  
    memcpy(destRow, sourceRow, copySize);                           <== oob write  
}  

```

}  

**-------------------------** --------------------------------------------------------------

The StretchedBlitNearest\_RowByRow function calls memcpy with length = destArea.width \* pixelSize.  

So if destArea.width is negative, memcpy will write out of bounds.  

In a 32bit process, the attached poc.html can set the memcpy length to any value.

**VERSION**  

Chrome Version: master (and tested on 91.0.4472.101 (Official Build) (32-bit) Stable)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**  

Run the attached poc.html

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==10020==ERROR: AddressSanitizer: negative-size-param: (size=-4293918720)  

==10020==WARNING: Failed to use and restart external symbolizer!  

==10020==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==10020==\*\*\* Most likely this means that the app is already \*\*\*  

==10020==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==10020==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==10020==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff77a04693f in \_\_asan\_memcpy C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:22  

#1 0x7ffcbba0b2e5 in rx::`anonymous namespace'::StretchedBlitNearest C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp:155  

#2 0x7ffcbba0c088 in rx::Blit11::copyAndConvertImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp:1269  

#3 0x7ffcbba0a5b7 in rx::Blit11::copyAndConvert C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp:1311  

#4 0x7ffcbba0992b in rx::Blit11::copyDepthStencilImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp:1214  

#5 0x7ffcbba0a248 in rx::Blit11::copyDepthStencil C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp:1151  

#6 0x7ffcbba8693d in rx::Renderer11::blitRenderbufferRect C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Renderer11.cpp:3749  

#7 0x7ffcbba40d68 in rx::Framebuffer11::blitImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Framebuffer11.cpp:374  

#8 0x7ffcbbb20804 in rx::FramebufferD3D::blit C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\FramebufferD3D.cpp:246  

#9 0x7ffcbb5ba45f in gl::Framebuffer::blit C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Framebuffer.cpp:1691  

#10 0x7ffcbb55cadf in gl::Context::blitFramebuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:4104  

#11 0x7ffcbb48a277 in GL\_BlitFramebuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_3\_0\_autogen.cpp:227  

#12 0x7ffcd0efc32f in gl::GLApiBase::glBlitFramebufferFn C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_bindings\_autogen\_gl.cc:3223  

#13 0x7ffcd840611b in gpu::gles2::GLES2DecoderPassthroughImpl::DoBlitFramebufferCHROMIUM C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:3324  

#14 0x7ffcd84312cc in gpu::gles2::GLES2DecoderPassthroughImpl::HandleBlitFramebufferCHROMIUM C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_handlers\_autogen.cc:3701  

#15 0x7ffcd4758ce4 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:858  

#16 0x7ffcd4758136 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:796  

#17 0x7ffcd168fed6 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#18 0x7ffccedd99c7 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:506  

#19 0x7ffccedd8b98 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:149  

#20 0x7ffccede70e1 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:772  

#21 0x7ffccedf1db5 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:690  

#22 0x7ffccea2b664 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:685  

#23 0x7ffccd78112a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#24 0x7ffccfec8593 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360  

#25 0x7ffccfec7c02 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260  

#26 0x7ffccfe9c7e7 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#27 0x7ffccfec9a6e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467  

#28 0x7ffccd706af3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#29 0x7ffccfaa175b in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:428  

#30 0x7ffccd493579 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:958  

#31 0x7ffccd490906 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:386  

#32 0x7ffccd490f1f in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:412  

#33 0x7ffcc321145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:151  

#34 0x7ff779fa5bb4 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#35 0x7ff779fa2be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:381  

#36 0x7ff77a38fbff in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#37 0x7ffd21597033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#38 0x7ffd23202650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

Address 0x13193c863000 is a wild pointer inside of access range of size 0x000000000001.  

SUMMARY: AddressSanitizer: negative-size-param C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:22 in \_\_asan\_memcpy  

==10020==ABORTING  

[9332:8120:0612/081700.753:ERROR:gpu\_process\_host.cc(995)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: Seong-Hwan Park (SeHwa) of SecunologyLab

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2021-06-11)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-06-13)

Thank you for the report. jmadill@ could you please take a look?

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2021-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-13)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-06-14)

Can repro.

### gi...@appspot.gserviceaccount.com (2021-06-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/bd797f75ffa55dc6c55b30efe47d92b0066429b5

commit bd797f75ffa55dc6c55b30efe47d92b0066429b5
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Jun 14 15:27:27 2021

D3D11: Fix OOB write in Blit11.

This could happen for specific values of the 'dest' target.

Bug: chromium:1219082
Change-Id: Ic19a5dc4a95531f9513403ad9c97a4b4c5dc5a6f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2961070
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/bd797f75ffa55dc6c55b30efe47d92b0066429b5/src/libANGLE/renderer/d3d/d3d11/Blit11.cpp
[modify] https://crrev.com/bd797f75ffa55dc6c55b30efe47d92b0066429b5/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/bd797f75ffa55dc6c55b30efe47d92b0066429b5/src/tests/gl_tests/BlitFramebufferANGLETest.cpp


### gi...@appspot.gserviceaccount.com (2021-06-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb367dfcce5f2ff950bf1fc6ce5a7219f27579d6

commit bb367dfcce5f2ff950bf1fc6ce5a7219f27579d6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jun 25 20:17:33 2021

Roll ANGLE from cc280ff33e21 to da17d56184fa (2 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/cc280ff33e21..da17d56184fa

2021-06-25 jmadill@chromium.org Trace Tests: Use xvfb consistently on Linux.
2021-06-25 jmadill@chromium.org D3D11: Fix OOB write in Blit11.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jonahr@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win-asan;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1219082
Tbr: jonahr@google.com
Change-Id: I983a2d3ae8d235fd6b042cfb9f69e6f96e63edfe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2987736
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#896177}

[modify] https://crrev.com/bb367dfcce5f2ff950bf1fc6ce5a7219f27579d6/DEPS


### jm...@chromium.org (2021-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

Requesting merge to stable M91 because latest trunk commit (896177) appears to be after stable branch point (870763).

Requesting merge to beta M92 because latest trunk commit (896177) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-28)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-06-28)

1. yes
2. https://chromium-review.googlesource.com/c/angle/angle/+/2961070
3. yes
4. M91/M92
5. security bug - OOB write
6. no
7. n/a


### sr...@google.com (2021-06-29)

Merge approved for M92 branch:4515 please merge asap ( beta RC build cut off is 3pm PST today for this weeks beta release)

### gi...@appspot.gserviceaccount.com (2021-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/6bbd095aa49baade6cd231ce873910492af53efd

commit 6bbd095aa49baade6cd231ce873910492af53efd
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Jun 14 15:27:27 2021

D3D11: Fix OOB write in Blit11.

This could happen for specific values of the 'dest' target.

Bug: chromium:1219082
(cherry picked from commit bd797f75ffa55dc6c55b30efe47d92b0066429b5)
Change-Id: I1895d2c614269f79376f49dbd87e279ca52c00a4
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2994730
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/6bbd095aa49baade6cd231ce873910492af53efd/src/libANGLE/renderer/d3d/d3d11/Blit11.cpp


### sr...@google.com (2021-06-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-01)

At this time there isn't another security refreshed planned for M91. Merge approved to M91 to prepare for any potential security refresh scenarios before M92 release. Please merge to branch 4472 at your convenience. Thanks! 

### gi...@appspot.gserviceaccount.com (2021-07-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d15be77864e18f407c317be6f6bc06ee2b7d070a

commit d15be77864e18f407c317be6f6bc06ee2b7d070a
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Jun 14 15:27:27 2021

D3D11: Fix OOB write in Blit11.

This could happen for specific values of the 'dest' target.

Bug: chromium:1219082
(cherry picked from commit bd797f75ffa55dc6c55b30efe47d92b0066429b5)
Change-Id: I1895d2c614269f79376f49dbd87e279ca52c00a4
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2994730
Reviewed-by: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 6bbd095aa49baade6cd231ce873910492af53efd)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3003382

[modify] https://crrev.com/d15be77864e18f407c317be6f6bc06ee2b7d070a/src/libANGLE/renderer/d3d/d3d11/Blit11.cpp


### am...@google.com (2021-07-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-07-02)

Congratulations, SeHwa! The VRP Panel has decided to award you $7500 for this report. Nice work! 

### am...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/85563d520530b0da6b804ac6fd99e21ff14ac648

commit 85563d520530b0da6b804ac6fd99e21ff14ac648
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Jun 14 15:27:27 2021

[M90-LTS] D3D11: Fix OOB write in Blit11.

This could happen for specific values of the 'dest' target.

Bug: chromium:1219082
Change-Id: Ic19a5dc4a95531f9513403ad9c97a4b4c5dc5a6f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2961070
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit bd797f75ffa55dc6c55b30efe47d92b0066429b5)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3044033
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/85563d520530b0da6b804ac6fd99e21ff14ac648/src/libANGLE/renderer/d3d/d3d11/Blit11.cpp
[modify] https://crrev.com/85563d520530b0da6b804ac6fd99e21ff14ac648/src/tests/gl_tests/BlitFramebufferANGLETest.cpp


### rz...@google.com (2021-07-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1219082?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056186)*
