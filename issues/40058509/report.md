# Security: [ANGLE] Heap-buffer-overflow in TextureVk::prepareForGenerateMipmap

| Field | Value |
|-------|-------|
| **Issue ID** | [40058509](https://issues.chromium.org/issues/40058509) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gg...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-01-17 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap buffer overflow vulnerability that is caused by the TextureVk::prepareForGenerateMipmap function.  

This vulnerability exists in the Vulkan backend, So in Chrome it can be triggered in Swiftshader.

**-------------------------** --------------------------------------------------------------  

void TextureVk::prepareForGenerateMipmap(ContextVk \*contextVk)  

{  

gl::LevelIndex baseLevel(mState.getEffectiveBaseLevel());  

gl::LevelIndex maxLevel(mState.getMipmapMaxLevel());

```
// Remove staged updates to the range that's being respecified (which is all the mips except  
// baseLevel).  
gl::LevelIndex firstGeneratedLevel = baseLevel + 1;  
mImage->removeStagedUpdates(contextVk, firstGeneratedLevel, maxLevel);  

static_assert(gl::IMPLEMENTATION_MAX_TEXTURE_LEVELS < 32,  
              "levels mask assumes 32-bits is enough");  
// Generate bitmask for (baseLevel, maxLevel]. `+1` because bitMask takes `the number of bits`  
// but levels start counting from 0  
gl::TexLevelMask levelsMask(angle::BitMask<uint32_t>(maxLevel.get() + 1));  
levelsMask &= static_cast<uint32_t>(~angle::Bit<uint32_t>(baseLevel.get()));                              <--- (1)  
// Remove (baseLevel, maxLevel] from mRedefinedLevels. These levels are no longer incompatibly            <--- (2)  
// defined if they previously were.  The corresponding bits in mRedefinedLevels should be  
// cleared.  
mRedefinedLevels &= ~levelsMask;  

```

**-------------------------** --------------------------------------------------------------

The intended behavior of the above code is to remove (baseLevel, maxLevel] from |mRedefinedLevels|, as commented in (2).  

However, the problem is that using angle::Bit in (1). So [0, baseLevel) range of the |mRedefinedLevels| will also be 0.  

This will lead to incorrect behavior. There are several ways to trigger a heap buffer overflow.  

An attacker can leverage this vulnerability to execute arbitrary code.

To create a bitmask that has the range (baseLevel, maxLevel], It needs to use angle::BitMask for baseLevel+1.

The attached poc1.html and poc2.html each trigger the vulnerability in different ways, and the location where the overflow occurs is also different. The asan log below is based on poc1.html.

**VERSION**  

Chrome Version: master (and tested on 97.0.4692.71 (Official Build) (64-bit) Stable)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**  

Run the attached poc1.html or poc2.html (with --disable-gpu)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==1664==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x118d6604f820 at pc 0x7ff635032627 bp 0x0017669ff120 sp 0x0017669ff160  

WRITE of size 32 at 0x118d6604f820 thread T4  

==1664==WARNING: Failed to use and restart external symbolizer!  

==1664==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==1664==\*\*\* Most likely this means that the app is already \*\*\*  

==1664==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==1664==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==1664==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff635032626 in \_\_asan\_memcpy C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:22  

#1 0x7ff9270c9226 in vk::Image::copy C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkImage.cpp:659  

#2 0x7ff927099ca1 in vk::CommandBuffer::submit C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:1757  

#3 0x7ff9270e7b1c in vk::Queue::submitQueue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:236  

#4 0x7ff9270e6835 in vk::Queue::taskLoop C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:288  

#5 0x7ff9270e964f in std::\_\_1::\_\_thread\_proxy<std::\_\_1::tuple<std::\_\_1::unique\_ptr<std::\_\_1::\_\_thread\_struct,std::\_\_1::default\_delete[std::\_\_1::\_\_thread\_struct](javascript:void(0);) >,void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*> > C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:291  

#6 0x7ff927a4bc47 in thread\_start<unsigned int (\_\_cdecl\*)(void \*),1> C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:97  

#7 0x7ff63503d513 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#8 0x7ff95dbc7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#9 0x7ff95dd02650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x118d6604f820 is located 3912 bytes to the right of 90328-byte region [0x118d66038800,0x118d6604e8d8)  

allocated by thread T0 here:  

#0 0x7ff635032b9b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff92741cb1a in sw::allocateZeroOrPoison C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\System\Memory.cpp:116  

#2 0x7ff9270b4d9c in vk::DeviceMemory::allocateBuffer C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDeviceMemory.cpp:323  

#3 0x7ff9270b4049 in vk::DeviceMemory::Allocate C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDeviceMemory.cpp:103  

#4 0x7ff9270ff9b2 in vkAllocateMemory C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1091  

#5 0x7ff92a0b8a57 in rx::`anonymous namespace'::FindAndAllocateCompatibleMemory C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_utils.cpp:103 #6 0x7ff92a0b4b14 in rx::`anonymous namespace'::AllocateAndBindBufferOrImageMemory[rx::vk::Image](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_utils.cpp:144  

#7 0x7ff92a0b476e in rx::vk::AllocateImageMemory C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_utils.cpp:728  

#8 0x7ff92a07e5f9 in rx::vk::ImageHelper::initMemory C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:4971  

#9 0x7ff929fe43d6 in rx::TextureVk::initImage C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp:2964  

#10 0x7ff929fdb327 in rx::TextureVk::ensureImageInitialized C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp:2377  

#11 0x7ff929fee2c9 in rx::TextureVk::syncState C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp:2671  

#12 0x7ff929993870 in gl::Texture::generateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Texture.cpp:1772  

#13 0x7ff9297b3cdf in GL\_GenerateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1445  

#14 0x7ff91478bd0a in gpu::gles2::GLES2DecoderPassthroughImpl::DoGenerateMipmap C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1454  

#15 0x7ff910bdd3d3 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:859  

#16 0x7ff910bdc81a in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:797  

#17 0x7ff90db002b6 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#18 0x7ff90aff2d4c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:499  

#19 0x7ff90aff1f26 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:151  

#20 0x7ff90affe7eb in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:669  

#21 0x7ff90b00960d in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#22 0x7ff90ac270e0 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:684  

#23 0x7ff909990ac4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#24 0x7ff90c4fb6c5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#25 0x7ff90c4fadf2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#26 0x7ff90c4d3c97 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:38  

#27 0x7ff90c4fcd91 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468

Thread T4 created by T0 here:  

#0 0x7ff63503dfa2 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ff927a4bb22 in \_beginthreadex C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:209  

#2 0x7ff92765c2cf in std::\_\_1::\_\_libcpp\_thread\_create C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\src\support\win32\thread\_win32.cpp:207  

#3 0x7ff9270e6b41 in std::\_\_1::thread::thread<void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*&,void> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:307  

#4 0x7ff9270e6577 in vk::Queue::Queue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:170  

#5 0x7ff9270a9542 in vk::Device::Device C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDevice.cpp:138  

#6 0x7ff9270ff10d in vk::DispatchableObject<vk::Device,VkDevice\_T \*>::Create<VkDeviceCreateInfo,vk::PhysicalDevice \*,const VkPhysicalDeviceFeatures \*,std::\_\_1::shared\_ptr[marl::Scheduler](javascript:void(0);) > C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:147  

#7 0x7ff9270fe9bd in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:981  

#8 0x7ff93305ca5d in terminator\_CreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5901  

#9 0x7ff9330575fc in loader\_create\_device\_chain C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5196  

#10 0x7ff9330560df in loader\_layer\_create\_device C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4709  

#11 0x7ff93306cbcc in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\trampoline.c:900  

#12 0x7ff929f9bc61 in rx::RendererVk::initializeDevice C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:2306  

#13 0x7ff929f945af in rx::RendererVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:1475  

#14 0x7ff929f33f2f in rx::DisplayVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\DisplayVk.cpp:46  

#15 0x7ff92a0b9329 in rx::DisplayVkWin32::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\win32\DisplayVkWin32.cpp:62  

#16 0x7ff929886b83 in egl::Display::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:940  

#17 0x7ff9297911fc in egl::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\egl\_stubs.cpp:448  

#18 0x7ff929798e78 in EGL\_Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_egl\_autogen.cpp:330  

#19 0x7ff90a9f76c9 in gl::GLSurfaceEGL::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_surface\_egl.cc:1427  

#20 0x7ff90a9f4956 in gl::GLSurfaceEGL::InitializeOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_surface\_egl.cc:988  

#21 0x7ff90d446235 in gl::init::InitializeGLOneOffPlatform C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_initializer\_win.cc:141  

#22 0x7ff90aa312d3 in gl::init::InitializeGLOneOffPlatformImplementation C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:246  

#23 0x7ff90aa30b5a in gl::init::`anonymous namespace'::InitializeGLOneOffPlatformHelper C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:167  

#24 0x7ff90aa30e79 in gl::init::InitializeGLNoExtensionsOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:202  

#25 0x7ff90b020923 in gpu::GpuInit::InitializeAndStartSandbox C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_init.cc:402  

#26 0x7ff90bf12d0b in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:321  

#27 0x7ff905528d65 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:678  

#28 0x7ff90552a93b in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1029  

#29 0x7ff905526b69 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:399  

#30 0x7ff905527c42 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:427  

#31 0x7ff8feda148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#32 0x7ff634f85b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#33 0x7ff634f82b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#34 0x7ff635382e7f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#35 0x7ff95dbc7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#36 0x7ff95dd02650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:22 in \_\_asan\_memcpy  

Shadow bytes around the buggy address:  

0x035b12c09eb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x035b12c09ec0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x035b12c09ed0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x035b12c09ee0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x035b12c09ef0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x035b12c09f00: fa fa fa fa[fa]fa fa fa fa fa fa fa fa fa fa fa  

0x035b12c09f10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x035b12c09f20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x035b12c09f30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x035b12c09f40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x035b12c09f50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==1664==ABORTING  

[8996:5588:0117/111237.124:ERROR:gpu\_process\_host.cc(972)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: SeongHwan Park (SeHwa)

## Attachments

- [poc1.html](attachments/poc1.html) (text/plain, 699 B)
- [poc2.html](attachments/poc2.html) (text/plain, 709 B)

## Timeline

### [Deleted User] (2022-01-17)

[Empty comment from Monorail migration]

### gg...@gmail.com (2022-01-17)

Here is the patch: https://crrev.com/c/3394468

### gi...@appspot.gserviceaccount.com (2022-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/9b231f090e1b51b716aab48451e2f0438005086e

commit 9b231f090e1b51b716aab48451e2f0438005086e
Author: SeongHwan Park <ggabu423@gmail.com>
Date: Mon Jan 17 19:49:08 2022

Vulkan: Fix incorrect bit test when mipmapping

Fixed an issue where angle::Bit was used instead of
angle::BitMask when should selecting [0, x) to set bit
range (x, y] in an n-bit bitmask.

Bug: chromium:1287962
Change-Id: I053fbc836ef12b0dfd30305fd527de3fabfdf525
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3394468
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/9b231f090e1b51b716aab48451e2f0438005086e/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/9b231f090e1b51b716aab48451e2f0438005086e/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2022-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f322782a9a8cb5b30737a73aea9b7be20e3cdc9c

commit f322782a9a8cb5b30737a73aea9b7be20e3cdc9c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jan 17 22:20:32 2022

Roll ANGLE from 158ecba6a01a to 9b231f090e1b (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/158ecba6a01a..9b231f090e1b

2022-01-17 ggabu423@gmail.com Vulkan: Fix incorrect bit test when mipmapping

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC syoussefi@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1287962
Tbr: syoussefi@google.com
Change-Id: I7a3cbbd6cde5e2cb67aafee1a71b02003baf0a22
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3396630
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#960199}

[modify] https://crrev.com/f322782a9a8cb5b30737a73aea9b7be20e3cdc9c/DEPS


### aj...@google.com (2022-01-18)

reporter - thanks for the report and patch. Does the patch completely fix the problem?

syoussefi: if so can this issue be marked as Fixed?

It looks this this was introduced in https://chromium-review.googlesource.com/c/angle/angle/+/3210726 / https://chromiumdash.appspot.com/commit/185e48a735d3fc42b6034623193699c20c1b8d55 so should not affect M96, hence FoundIn-97.

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-01-18)

Yes. I did find the same change that had broken this.

### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-18)

Requesting merge to stable M97 because latest trunk commit (960199) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (960199) appears to be after beta branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-18)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-18)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-01-18)

Please apply appropriate OSs label.

+M97 Release TPMS and Security TPM

### gg...@gmail.com (2022-01-19)

Sorry. I discovered that my patch might be incomplete. Would you please stop the merge process until I commit again?

### am...@chromium.org (2022-01-19)

Thanks for letting us know. This hasn't been approved to merge or merged to any branches yet, so this would only made it into Canary so far. 
Reopening this issue. 

### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### gg...@gmail.com (2022-01-19)

Sorry again. I analyzed another PoC because it crashed with the patch. As a result of the analysis, it seems to be another vulnerability. I will report it separately. Would you please continue the process of merging this vulnerability?

### am...@chromium.org (2022-01-19)

No problem, thanks again for letting us know. Setting this to fixed once again and once there is a bit more canary coverage, I'll review for merge approval. 

### am...@google.com (2022-01-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-20)

Congratulations! The VRP Panel has decided to award you $10,000 this report (based on updates to our reward amounts for GPU mem corruptions bugs: g.co/chrome/vrp). 
Thank you for your report and great work! 

### am...@chromium.org (2022-01-21)

hello, ggabu@ we've updated the reward amount to include a $2000 patch bonus. Apologies that we didn't include this the first time around. Thank you for your patch as well as including a test in the patch. Nice work and thanks for all your efforts!

### am...@chromium.org (2022-01-21)

merge approved to M98, please merge to branch 4758 at your earliest convenience NLT 11am PST, Tuesday, 25 January so this fix can be included in the m98 stable cut -- thank you! 

### am...@google.com (2022-01-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/343b7bb57268e1cb47da26fcb0ed40fe47e8ff5d

commit 343b7bb57268e1cb47da26fcb0ed40fe47e8ff5d
Author: SeongHwan Park <ggabu423@gmail.com>
Date: Mon Jan 17 19:49:08 2022

M98: Vulkan: Fix incorrect bit test when mipmapping

Fixed an issue where angle::Bit was used instead of
angle::BitMask when should selecting [0, x) to set bit
range (x, y] in an n-bit bitmask.

Bug: chromium:1287962
Change-Id: I3c69478f5ffaba5c52b50c791556e75af819fa0e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3412883
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/343b7bb57268e1cb47da26fcb0ed40fe47e8ff5d/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/343b7bb57268e1cb47da26fcb0ed40fe47e8ff5d/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2022-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a254f5c620cd868e080dafaa793024d4b5666ef8

commit a254f5c620cd868e080dafaa793024d4b5666ef8
Author: SeongHwan Park <ggabu423@gmail.com>
Date: Mon Jan 17 19:49:08 2022

M97: Vulkan: Fix incorrect bit test when mipmapping

Fixed an issue where angle::Bit was used instead of
angle::BitMask when should selecting [0, x) to set bit
range (x, y] in an n-bit bitmask.

Bug: chromium:1287962
Change-Id: I3677c4540cdcdc3ad684c7ef0de10558b88da087
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3412882
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/a254f5c620cd868e080dafaa793024d4b5666ef8/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/a254f5c620cd868e080dafaa793024d4b5666ef8/src/libANGLE/renderer/vulkan/TextureVk.cpp


### [Deleted User] (2022-01-24)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2022-01-25)

The regression happened after M96. I don't believe the issue applies to M96.

### gm...@google.com (2022-01-26)

Removing LTS candidate per https://crbug.com/chromium/1287962#c29

### am...@chromium.org (2022-01-31)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1287962?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058509)*
