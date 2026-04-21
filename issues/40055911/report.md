# Security: [ANGLE] Out-of-bound write in rx::Image11::GenerateMipmap

| Field | Value |
|-------|-------|
| **Issue ID** | [40055911](https://issues.chromium.org/issues/40055911) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | gg...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2021-05-18 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

There is a out-of-bound write bug in the ANGLE d3d11 renderer that is caused by the Image11::redefine function when generateMipmap function is called with 3D textures.

ANGLE uses the TextureD3D\_3D::redefineImage function when setting the properties of a 3D texture in the d3d renderer.  

For example, the texImage[23]D function takes explicit arguments and sets properties (width, height, depth, ...). And the generateMipmap function does not takes property arguments, but sets properties of some texture levels because it needs to be reset to the newly calculated value.

The TextureD3D::generateMipmap function calls the initMipmapImages function to set the property values before copying the texture pixel data. If the target is |TEXTURE\_3D|, the TextureD3D\_3D::initMipmapImages function is called. The initMipmapImages function executes a loop that calls redefineImages function for setting properties for each texture level.

The redefineImage function does not set if the current attribute value and the new attribute value are the same.  

(if the |forceRelease| argument is true, above condition is ignored and reset properties. However the initMipmapImages function calls the redefineImages function with the |forceRelease| = false.)

This bug occurs by incorrect validation in the Image11::redefine function.  

**-------------------------** --------------------------------------------------------------  

bool Image11::redefine(gl::TextureType type,  

GLenum internalformat,  

const gl::Extents &size,  

bool forceRelease)  

{  

if (mWidth != size.width || mHeight != size.height || mInternalFormat != internalformat ||  

forceRelease)  

{  

......  

**-------------------------** --------------------------------------------------------------

2D textures use width and height properties, and 3D textures additionally use depth property.  

However, the above condition does not check the depth property value.  

For example, if the current texture's (width, height, depth) is (10, 10, 500) and the new value is (10, 10, 1), the properties are not changed.

**-------------------------** --------------------------------------------------------------  

template <typename T>  

inline void GenerateMip(size\_t sourceWidth, size\_t sourceHeight, size\_t sourceDepth,  

const uint8\_t \*sourceData, size\_t sourceRowPitch, size\_t sourceDepthPitch,  

uint8\_t \*destData, size\_t destRowPitch, size\_t destDepthPitch)  

{  

size\_t mipWidth = std::max<size\_t>(1, sourceWidth >> 1);  

size\_t mipHeight = std::max<size\_t>(1, sourceHeight >> 1);  

size\_t mipDepth = std::max<size\_t>(1, sourceDepth >> 1); <== But the size of destData hasn't changed.

```
priv::MipGenerationFunction generationFunction = priv::GetMipGenerationFunction<T>(sourceWidth, sourceHeight, sourceDepth);  
ASSERT(generationFunction != nullptr);  

generationFunction(sourceWidth, sourceHeight, sourceDepth, sourceData, sourceRowPitch, sourceDepthPitch,  
                   mipWidth, mipHeight, mipDepth, destData, destRowPitch, destDepthPitch);  

```

}  

**-------------------------** --------------------------------------------------------------

However, in the next Mipmap processes don't get property members. GenerateMip function recalculate (w, h, d).  

This leads to out of bounds read and write on |destData|.  

The attached poc.html copies data of size 128\*128\*(100/2)\*4 to the allocated memory in 128\*128\*1\*4 size.

The redefine function existed before the renderer was split into d3d9 and d3d11.  

And commit |4760c563c3d41b97c1677454c9e700595c25a04b| added the depth property for WebGL 2.  

However, this commit only changes the redefine function of d3d9 and not the redefine function of d3d11.  

So this bug only exists in the d3d11 renderer. And it can be triggered starting from Chrome 56, which first supported WebGL 2.0.

An example patch is as follows:  

**-------------------------** --------------------------------------------------------------  

bool Image11::redefine(gl::TextureType type,  

GLenum internalformat,  

const gl::Extents &size,  

bool forceRelease)  

{

- if (mWidth != size.width || mHeight != size.height || mInternalFormat != internalformat ||

- if (mWidth != size.width || mHeight != size.height || mDepth != size.depth || mInternalFormat != internalformat ||  
  
  forceRelease)  
  
  {  
  
  **-------------------------** --------------------------------------------------------------

**VERSION**  

Chrome Version: master (and tested on 90.0.4430.212 (Official Build) (64-bit) Stable)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**  

Run the attached poc.html

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==7696==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x120ee3c8c800 at pc 0x7ff95b51acdc bp 0x0044a5bfe0b0 sp 0x0044a5bfe0f8  

WRITE of size 4 at 0x120ee3c8c800 thread T0  

==7696==WARNING: Failed to use and restart external symbolizer!  

==7696==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==7696==\*\*\* Most likely this means that the app is already \*\*\*  

==7696==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==7696==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==7696==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff95b51acdb in angle::R8G8B8A8::average C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\image\_util\imageformats.cpp:357  

#1 0x7ff95abe48ed in angle::priv::GenerateMip\_XYZ[angle::R8G8B8A8](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\image\_util\generatemip.inc:215  

#2 0x7ff95abddb53 in angle::GenerateMip[angle::R8G8B8A8](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\image\_util\generatemip.inc:264  

#3 0x7ff95af01374 in rx::Image11::GenerateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:68  

#4 0x7ff95b02df2e in rx::TextureD3D::generateMipmapUsingImages C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:540  

#5 0x7ff95b02d46b in rx::TextureD3D::generateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:469  

#6 0x7ff95ab6d1c9 in gl::Texture::generateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Texture.cpp:1680  

#7 0x7ff95a94f819 in GL\_GenerateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1387  

#8 0x7ff971309f14 in gpu::gles2::GLES2DecoderPassthroughImpl::DoGenerateMipmap C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1462  

#9 0x7ff96d6c7bb6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:858  

#10 0x7ff96d6c7008 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:796  

#11 0x7ff96a6b09ce in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:69  

#12 0x7ff967e4b8d2 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:510  

#13 0x7ff967e4b382 in IPC::MessageT<GpuCommandBufferMsg\_AsyncFlush\_Meta,std::\_\_1::tuple<int,unsigned int,std::\_\_1::vector<gpu::SyncToken,std::\_\_1::allocator[gpu::SyncToken](javascript:void(0);) > >,void>::Dispatch<gpu::CommandBufferStub,gpu::CommandBufferStub,void,void (gpu::CommandBufferStub::\*)(int, unsigned int, const std::vector[gpu::SyncToken](javascript:void(0);) &)> C:\b\s\w\ir\cache\builder\src\ipc\ipc\_message\_templates.h:140  

#14 0x7ff967e48a9c in gpu::CommandBufferStub::OnMessageReceived C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:166  

#15 0x7ff967e5c299 in gpu::GpuChannel::HandleMessageHelper C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:651  

#16 0x7ff967e55ed7 in gpu::GpuChannel::HandleMessage C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:609  

#17 0x7ff967a9eee7 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:648  

#18 0x7ff9667a559a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:173  

#19 0x7ff968ef005f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#20 0x7ff968eef6d9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:264  

#21 0x7ff968ec341f in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#22 0x7ff968ef1704 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:460  

#23 0x7ff96672c603 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:133  

#24 0x7ff968b42cfa in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:429  

#25 0x7ff9664c36c4 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:958  

#26 0x7ff9664c0a56 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#27 0x7ff9664c1040 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#28 0x7ff95c51145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:151  

#29 0x7ff6b7905bed in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#30 0x7ff6b7902c47 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:369  

#31 0x7ff6b7ce959f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#32 0x7ff9d9397033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#33 0x7ff9d9702650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x120ee3c8c800 is located 0 bytes to the right of 65536-byte region [0x120ee3c7c800,0x120ee3c8c800)  

allocated by thread T0 here:  

#0 0x7ff6b79a335b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff95b4fba3c in angle::MemoryBuffer::resize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\common\MemoryBuffer.cpp:46  

#2 0x7ff95af0cccb in rx::MappedSubresourceVerifier11::wrap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\MappedSubresourceVerifier11.cpp:91  

#3 0x7ff95af01634 in rx::Image11::map C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:650  

#4 0x7ff95af011b4 in rx::Image11::GenerateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:56  

#5 0x7ff95b02df2e in rx::TextureD3D::generateMipmapUsingImages C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:540  

#6 0x7ff95b02d46b in rx::TextureD3D::generateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:469  

#7 0x7ff95ab6d1c9 in gl::Texture::generateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Texture.cpp:1680  

#8 0x7ff95a94f819 in GL\_GenerateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1387  

#9 0x7ff971309f14 in gpu::gles2::GLES2DecoderPassthroughImpl::DoGenerateMipmap C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1462  

#10 0x7ff96d6c7bb6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:858  

#11 0x7ff96d6c7008 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:796  

#12 0x7ff96a6b09ce in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:69  

#13 0x7ff967e4b8d2 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:510  

#14 0x7ff967e4b382 in IPC::MessageT<GpuCommandBufferMsg\_AsyncFlush\_Meta,std::\_\_1::tuple<int,unsigned int,std::\_\_1::vector<gpu::SyncToken,std::\_\_1::allocator[gpu::SyncToken](javascript:void(0);) > >,void>::Dispatch<gpu::CommandBufferStub,gpu::CommandBufferStub,void,void (gpu::CommandBufferStub::\*)(int, unsigned int, const std::vector[gpu::SyncToken](javascript:void(0);) &)> C:\b\s\w\ir\cache\builder\src\ipc\ipc\_message\_templates.h:140  

#15 0x7ff967e48a9c in gpu::CommandBufferStub::OnMessageReceived C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:166  

#16 0x7ff967e5c299 in gpu::GpuChannel::HandleMessageHelper C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:651  

#17 0x7ff967e55ed7 in gpu::GpuChannel::HandleMessage C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:609  

#18 0x7ff967a9eee7 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:648  

#19 0x7ff9667a559a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:173  

#20 0x7ff968ef005f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#21 0x7ff968eef6d9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:264  

#22 0x7ff968ec341f in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#23 0x7ff968ef1704 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:460  

#24 0x7ff96672c603 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:133  

#25 0x7ff968b42cfa in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:429  

#26 0x7ff9664c36c4 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:958  

#27 0x7ff9664c0a56 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#28 0x7ff9664c1040 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\image\_util\imageformats.cpp:357 in angle::R8G8B8A8::average  

Shadow bytes around the buggy address:  

0x03eec03118b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x03eec03118c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x03eec03118d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x03eec03118e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x03eec03118f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x03eec0311900:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03eec0311910: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03eec0311920: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03eec0311930: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03eec0311940: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03eec0311950: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

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

Shadow gap: cc  

==7696==ABORTING  

[9112:2676:0515/072552.498:ERROR:gpu\_process\_host.cc(1003)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: Seong-Hwan Park (SeHwa) of SecunologyLab

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 597 B)

## Timeline

### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-05-20)

jmadill@ assigning to you based on OWNERS and `git blame`.
If you're not the right person to own this, could you please help find that person? Thanks.

Also CC'ing other @chromium OWNERS.

[Monorail components: Internals>GPU>ANGLE]

### va...@chromium.org (2021-05-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-05-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5652952384339968.

### va...@chromium.org (2021-05-20)

Tentatively setting the Security_Impact to Stable based on the issue description. Hopefully ClusterFuzz will be able to confirm that.

### cl...@chromium.org (2021-05-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5755385592741888.

### cl...@chromium.org (2021-05-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5719515451949056.

### jm...@chromium.org (2021-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-20)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2697358464cf20576701987f60300b6c4086c11e

commit 2697358464cf20576701987f60300b6c4086c11e
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu May 20 16:22:46 2021

D3D11: Fix respecifying 3D textures.

The missing check for the "Depth" dimension could lead to a bug
where we would not recreate a texture when the dimension changed.

Bug: chromium:1210414
Change-Id: Id59097ad14ae77ff80d27081f61786dad17a77ea
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2911032
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/2697358464cf20576701987f60300b6c4086c11e/src/libANGLE/renderer/d3d/d3d11/Image11.cpp
[modify] https://crrev.com/2697358464cf20576701987f60300b6c4086c11e/src/tests/gl_tests/MipmapTest.cpp


### gi...@appspot.gserviceaccount.com (2021-05-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/97c16fd4f4df507444e586ff6f9b1bd0b5fcddc7

commit 97c16fd4f4df507444e586ff6f9b1bd0b5fcddc7
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri May 21 06:17:55 2021

Roll ANGLE from f871545d293f to 44fabb7b8864 (68 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/f871545d293f..44fabb7b8864

2021-05-21 ynovikov@chromium.org Revert "Vulkan: Add support for EXT_texture_border_clamp"
2021-05-20 ynovikov@chromium.org Don't use VK_EXT_debug_utils with non-Android Vulkan < 1.1.91
2021-05-20 jmadill@chromium.org D3D11: Fix respecifying 3D textures.
2021-05-20 timvp@google.com Fix Loading ANGLE.apk in Android
2021-05-20 jonahr@google.com Reland Change to module directory when loading swiftshader ICD.
2021-05-20 ruperts@google.com Remove .find_ignore files
2021-05-20 jmadill@chromium.org infra: Add dEQP tests to the Pixel 4.
2021-05-20 gert.wollny@collabora.com FrameCapture: Write the frame cpp file even if frame is empty
2021-05-20 cnorthrop@google.com Add MultisampledRenderToTexture Pixel4 expectations
2021-05-20 mark@lunarg.com Balance debuglabel begin/end pairs for skipped drawcalls
2021-05-20 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 0ca03fb2907c to 3b9a1a795f1e (4 revisions)
2021-05-20 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from baa6900ec346 to 15fd0774bd48 (5 revisions)
2021-05-20 jplate@google.com CL: Fix querying default device if non exists
2021-05-20 gert.wollny@collabora.com Capture/Replay: Emit SetupReplay() late
2021-05-20 gert.wollny@collabora.com Capture/Replay: Don't try to serialize blob without data
2021-05-20 jplate@google.com CL: command queues for front end and pass-through
2021-05-20 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 2b00cebcd5b5 to b625560cb068 (1025 revisions)
2021-05-19 cnorthrop@google.com Update skip list for Texture2DTest.TextureSize
2021-05-19 b.schade@samsung.com Vulkan: Fix geometry shader qualifier validation
2021-05-19 syoussefi@chromium.org Vulkan: Generate SPIR-V directly from the translator; Part 1
2021-05-19 timvp@google.com Add angle.iml to .gitignore
2021-05-19 jmadill@chromium.org Use the same url for 'requests' as chromium.
2021-05-19 geofflang@chromium.org Revert "[Vulkan] Add DisplayVkNull"
2021-05-19 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 3d799e0e9b08 to baa6900ec346 (3 revisions)
2021-05-18 syoussefi@chromium.org Revert "Vulkan: Disable BufferVk suballocation"
2021-05-18 gert.wollny@collabora.com Capture: Make writeCppReplayIndexFiles a method of FrameCapture
2021-05-18 jmadill@chromium.org infra: Add tests to Android Pixel 4 bot.
2021-05-18 jmadill@chromium.org Improve test expectations overlap check.
2021-05-18 jonahr@google.com Revert "Reland Change to module directory when loading swiftshader ICD."
2021-05-18 m.maiya@samsung.com Vulkan: Add support for EXT_texture_border_clamp
2021-05-18 cnorthrop@google.com Tests: Skip pokemon_go on Intel Linux Vulkan
2021-05-18 cnorthrop@google.com Tests: Add SAKURA School Simulator trace
2021-05-18 cnorthrop@google.com Capture/Replay: Ignore delete of non-genned buffers
2021-05-18 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from af907708adb3 to 0ca03fb2907c (1 revision)
2021-05-18 jplate@google.com CL: Load OpenCL without search path modification
2021-05-18 jplate@google.com CL: Add front end object references to back end objects
2021-05-18 jplate@google.com CL: Move object cast from entry points to stubs and front end
2021-05-18 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 9b886afc6e79 to 2b00cebcd5b5 (497 revisions)
2021-05-18 lexa.knyazev@gmail.com Vulkan: Support GL_EXT_texture_sRGB_RG8
2021-05-18 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 055e71b2a367 to 3d799e0e9b08 (25 revisions)
2021-05-18 syoussefi@chromium.org Vulkan: Optimize respecifying an image
2021-05-18 syoussefi@chromium.org Vulkan: Fix a bug releasing DynamicBuffer-owned buffer
2021-05-18 cnorthrop@google.com Tests: Add Pokemon Go trace
2021-05-18 cnorthrop@google.com Capture/Replay: Add const to string pointer
2021-05-18 cnorthrop@google.com Capture/Replay: Skip glGetActiveUniform
2021-05-18 cnorthrop@google.com Capture/Replay: Reset programs on loop
2021-05-17 cnorthrop@google.com Skip Texture2DTest.TextureSize on Linux+GL+TSAN
2021-05-17 jmadill@chromium.org ANGLETest: Skip test setup/teardown on major error.
2021-05-17 jonahr@google.com Fix out_of_range error in System_utils_posix
2021-05-17 syoussefi@chromium.org Vulkan: Cleanup texture image respecify
2021-05-17 syoussefi@chromium.org Vulkan: Fix desc set cache bug with xfb offset
2021-05-17 jmadill@chromium.org Gold Tests: Implement flaky retries and sharding.
2021-05-17 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from c4d054c6ad41 to af907708adb3 (2 revisions)
2021-05-17 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 3b747dab7bb3 to 9b886afc6e79 (485 revisions)
2021-05-17 gert.wollny@collabora.com Capture/Replay: Add suffix to label for test file search
2021-05-17 gert.wollny@collabora.com Capture/Replay: Print context diff also with frame gaps
2021-05-17 gert.wollny@collabora.com Capture/Replay: track robustResourceInit
2021-05-15 cclao@google.com Vulkan: Add webgl conformance/texture-size test
2021-05-15 ianelliott@google.com Vulkan: Fix AGI hierarchy
2021-05-15 cclao@google.com Skip Texture2DArrayIntegerTestES3.NonZeroBaseLevel on OSX+OpenGL
2021-05-15 syoussefi@chromium.org Vulkan: Disable BufferVk suballocation
2021-05-14 angle-autoroll@skia-public.iam.gserviceaccount.com Roll VK-GL-CTS from 1c4a387382ea to 535dfe49fc49 (1 revision)
2021-05-14 geofflang@google.com GL: Recreate textures on eglReleaseTexImage.
2021-05-14 m.maiya@samsung.com Bug fix in glTexParameter and glGetTexParameter validation
2021-05-14 cclao@google.com Fix IOSurfaceClientBufferTest.RenderToBGRX8888IOSurface on OSX+OpenGL
2021-05-14 jmadill@chromium.org Test Runner: Add test expectations parser.
2021-05-14 jonahr@google.com Reland Change to module directory when loading swiftshader ICD.
2021-05-14 sergeyu@google.com [Vulkan] Add DisplayVkNull

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC cnorthrop@google.com,ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win-asan;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1181068,chromium:1197905,chromium:1198567,chromium:1203879,chromium:1205999,chromium:1209197,chromium:1210414
Tbr: cnorthrop@google.com,ynovikov@google.com
Test: Test: KHR-GLES32.core.geometry_shader.nonarray_input.*
Test: Test: Pokemon Go MEC
Test: Test: SAKURA School Simulator MEC
Test: Test: TH
Test: Test: angle_perftest --gtest_filter="*pokemon_go*"
Test: Test: angle_perftests --gtest_filter="*sakura_school_simulator*"
Test: Test: dEQP-GLES31.functional.texture.border_clamp*
Test: Test: dEQP.KHR_GLES31/core_texture_border_clamp_texparameteri_errors
Change-Id: Ie46139abe2a82c9f19b85af77255d6f27b4c2bf7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2911708
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#885402}

[modify] https://crrev.com/97c16fd4f4df507444e586ff6f9b1bd0b5fcddc7/DEPS


### jm...@chromium.org (2021-05-21)

Thanks for the clear & concise bug report. This seems like a serious security bug. Should be fixed in Canary tonight or on Monday. I'll let it set a few days before requesting a merge.

### [Deleted User] (2021-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-21)

Requesting merge to stable M90 because latest trunk commit (885402) appears to be after stable branch point (857950).

Requesting merge to beta M91 because latest trunk commit (885402) appears to be after beta branch point (870763).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-21)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### jm...@chromium.org (2021-05-25)

1. yes
2. https://chromium-review.googlesource.com/c/angle/angle/+/2911032
3. yes
4. 92
5. serious security issue (out of bounds write)
6. no
7. n/a


### ad...@google.com (2021-05-26)

Approving merge to M92, branch 4515. We'll consider M91 merges later.

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/10b8a6d1c1a11be89cfc504106bd6446f5792d11

commit 10b8a6d1c1a11be89cfc504106bd6446f5792d11
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu May 20 16:22:46 2021

D3D11: Fix respecifying 3D textures.

The missing check for the "Depth" dimension could lead to a bug
where we would not recreate a texture when the dimension changed.

Bug: chromium:1210414
Change-Id: Id59097ad14ae77ff80d27081f61786dad17a77ea
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2911032
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 2697358464cf20576701987f60300b6c4086c11e)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2921448
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/10b8a6d1c1a11be89cfc504106bd6446f5792d11/src/libANGLE/renderer/d3d/d3d11/Image11.cpp
[modify] https://crrev.com/10b8a6d1c1a11be89cfc504106bd6446f5792d11/src/tests/gl_tests/MipmapTest.cpp


### ad...@google.com (2021-06-03)

Approving merge to M91. Please merge to branch 4472. We plan to cut a security refresh tomorrow.

### pb...@google.com (2021-06-03)

Your change has been approved for M91. Please go ahead and merge the CL to M91 branch : 4472 (refs/branch-heads/4472) manually asap.

### gi...@appspot.gserviceaccount.com (2021-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/3d4f87ab5b9ba4c720cedf1f219cc0884038b140

commit 3d4f87ab5b9ba4c720cedf1f219cc0884038b140
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu May 20 16:22:46 2021

D3D11: Fix respecifying 3D textures.

The missing check for the "Depth" dimension could lead to a bug
where we would not recreate a texture when the dimension changed.

Bug: chromium:1210414
Change-Id: Id59097ad14ae77ff80d27081f61786dad17a77ea
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2911032
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 2697358464cf20576701987f60300b6c4086c11e)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2937026
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/3d4f87ab5b9ba4c720cedf1f219cc0884038b140/src/libANGLE/renderer/d3d/d3d11/Image11.cpp
[modify] https://crrev.com/3d4f87ab5b9ba4c720cedf1f219cc0884038b140/src/tests/gl_tests/MipmapTest.cpp


### am...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-09)

Issue only targets Windows APIs, ChromeOS LTS is not affected.

### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congratulations, Seong-Hwan - the VRP Panel has decided to award you $7,500 for this report. Someone from our finance team will be in touch soon to arrange payment. Nice work!

### kb...@chromium.org (2021-06-11)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1210414?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055911)*
