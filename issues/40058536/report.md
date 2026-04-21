# Security: [ANGLE] Heap-buffer-overflow in ImageHelper::SubresourceUpdate::isUpdateToLayers

| Field | Value |
|-------|-------|
| **Issue ID** | [40058536](https://issues.chromium.org/issues/40058536) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gg...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-01-20 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap buffer overflow vulnerability in the Vulkan backend that could be triggered in Swiftshader.  

I think it seems that ImageHelper::SubresourceUpdate::isUpdateToLayers is the cause.  

This vulnerability started in commit 56330564295ef041b63c82283142eed8b98e2087.

**-------------------------** --------------------------------------------------------------  

-- bool ImageHelper::SubresourceUpdate::isUpdateToLayer(uint32\_t layerIndex) const  

++ bool ImageHelper::SubresourceUpdate::isUpdateToLayers(uint32\_t layerIndex, uint32\_t layerCount) const  

{  

uint32\_t updateBaseLayer, updateLayerCount;  

getDestSubresource(gl::ImageIndex::kEntireLevel, &updateBaseLayer, &updateLayerCount);

-- return updateBaseLayer == layerIndex;  

++ return updateBaseLayer == layerIndex && (updateLayerCount == layerCount || updateLayerCount == VK\_REMAINING\_ARRAY\_LAYERS);  

}  

**-------------------------** --------------------------------------------------------------

When redefining the texture, the code before the commit above removes levelUpdates as long as the layerIndex is the same.  

However, since the condition "updateLayerCount == layerCount" has been added, levelUpdates will not be removed if the depth(layerCount) in texImage3D is different.  

This will lead to incorrect behavior. Also this can lead to heap buffer overflow.  

(In addition to this vulnerability, if levelUpdates is not properly removed for any reason, memory corruption may occur in vk::Image::copy, copy... functions.)

**VERSION**  

Chrome Version: master (and tested on 97.0.4692.99 (Official Build) (64-bit) Stable)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**  

Run the attached poc.html (with --disable-gpu)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==5044==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12bfe18a5d18 at pc 0x7ff68f1626b7 bp 0x0074881fefa0 sp 0x0074881fefe0  

WRITE of size 1024 at 0x12bfe18a5d18 thread T4  

==5044==WARNING: Failed to use and restart external symbolizer!  

==5044==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

[5044:3136:0121/060615.383:ERROR:gl\_utils.cc(319)] [.WebGL-000011F41A359C80]GL Driver Message (OpenGL, Performance, GL\_CLOSE\_PATH\_NV, High): GPU stall due to ReadPixels  

==5044==\*\*\* Most likely this means that the app is already \*\*\*  

==5044==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==5044==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==5044==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff68f1626b6 in \_\_asan\_memcpy C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:22  

#1 0x7ff9270c9072 in vk::Image::copy C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkImage.cpp:632  

#2 0x7ff927099ca1 in vk::CommandBuffer::submit C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:1757  

#3 0x7ff9270e7a1c in vk::Queue::submitQueue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:236  

#4 0x7ff9270e6735 in vk::Queue::taskLoop C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:288  

#5 0x7ff9270e954f in std::\_\_1::\_\_thread\_proxy<std::\_\_1::tuple<std::\_\_1::unique\_ptr<std::\_\_1::\_\_thread\_struct,std::\_\_1::default\_delete[std::\_\_1::\_\_thread\_struct](javascript:void(0);) >,void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*> > C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:291  

#6 0x7ff927a48aa7 in thread\_start<unsigned int (\_\_cdecl\*)(void \*),1> C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:97  

#7 0x7ff68f16d5a3 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#8 0x7ff95dbc7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#9 0x7ff95dd02650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x12bfe18a5d18 is located 0 bytes to the right of 23320-byte region [0x12bfe18a0200,0x12bfe18a5d18)  

allocated by thread T0 here:  

#0 0x7ff68f162c2b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff92741b50e in sw::allocateZeroOrPoison C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\System\Memory.cpp:116  

#2 0x7ff9270b4d84 in vk::DeviceMemory::allocateBuffer C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDeviceMemory.cpp:323  

#3 0x7ff9270b4031 in vk::DeviceMemory::Allocate C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDeviceMemory.cpp:103  

#4 0x7ff9270ff8b4 in vkAllocateMemory C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1094  

#5 0x7ff92a0b94cd in rx::`anonymous namespace'::FindAndAllocateCompatibleMemory C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_utils.cpp:103 #6 0x7ff92a0b5588 in rx::`anonymous namespace'::AllocateAndBindBufferOrImageMemory[rx::vk::Image](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_utils.cpp:144  

#7 0x7ff92a0b51e2 in rx::vk::AllocateImageMemory C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_utils.cpp:728  

#8 0x7ff92a07f039 in rx::vk::ImageHelper::initMemory C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:4971  

#9 0x7ff929fe4fe2 in rx::TextureVk::initImage C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp:2964  

#10 0x7ff929fdbdfb in rx::TextureVk::ensureImageInitialized C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp:2377  

#11 0x7ff929feeefb in rx::TextureVk::syncState C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp:2671  

#12 0x7ff929993a7c in gl::Texture::generateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Texture.cpp:1772  

#13 0x7ff9297b3c8e in GL\_GenerateMipmap C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1445  

#14 0x7ff8e6d0d494 in gpu::gles2::GLES2DecoderPassthroughImpl::DoGenerateMipmap C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1454  

#15 0x7ff8e314f213 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:859  

#16 0x7ff8e314e65a in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:797  

#17 0x7ff8e0070d12 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#18 0x7ff8dd55a780 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:499  

#19 0x7ff8dd55995a in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:151  

#20 0x7ff8dd5661db in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:669  

#21 0x7ff8dd570ffd in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#22 0x7ff8dd18dac6 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:684  

#23 0x7ff8dbef3214 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#24 0x7ff8dea67545 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#25 0x7ff8dea66c18 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#26 0x7ff8dea3fb67 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:38  

#27 0x7ff8dea68c11 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468

Thread T4 created by T0 here:  

#0 0x7ff68f16e032 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ff927a48982 in \_beginthreadex C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:209  

#2 0x7ff92765ac93 in std::\_\_1::\_\_libcpp\_thread\_create C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\src\support\win32\thread\_win32.cpp:207  

#3 0x7ff9270e6a41 in std::\_\_1::thread::thread<void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*&,void> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:307  

#4 0x7ff9270e6477 in vk::Queue::Queue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:170  

#5 0x7ff9270a9510 in vk::Device::Device C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDevice.cpp:138  

#6 0x7ff9270ff00d in vk::DispatchableObject<vk::Device,VkDevice\_T \*>::Create<VkDeviceCreateInfo,vk::PhysicalDevice \*,const VkPhysicalDeviceFeatures \*,std::\_\_1::shared\_ptr[marl::Scheduler](javascript:void(0);) > C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:147  

#7 0x7ff9270fe8bd in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:984  

#8 0x7ff932eace48 in terminator\_CreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5952  

#9 0x7ff932ea7636 in loader\_create\_device\_chain C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5192  

#10 0x7ff932ea6119 in loader\_layer\_create\_device C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4705  

#11 0x7ff932ebd054 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\trampoline.c:900  

#12 0x7ff929f9c6c9 in rx::RendererVk::initializeDevice C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:2306  

#13 0x7ff929f94fbb in rx::RendererVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:1475  

#14 0x7ff929f34973 in rx::DisplayVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\DisplayVk.cpp:46  

#15 0x7ff92a0b9d9d in rx::DisplayVkWin32::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\win32\DisplayVkWin32.cpp:62  

#16 0x7ff929886adb in egl::Display::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:940  

#17 0x7ff9297911fc in egl::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\egl\_stubs.cpp:448  

#18 0x7ff929798e6c in EGL\_Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_egl\_autogen.cpp:330  

#19 0x7ff8dcf5dbd9 in gl::GLSurfaceEGL::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_surface\_egl.cc:1427  

#20 0x7ff8dcf5ae66 in gl::GLSurfaceEGL::InitializeOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_surface\_egl.cc:988  

#21 0x7ff8df9b131d in gl::init::InitializeGLOneOffPlatform C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_initializer\_win.cc:141  

#22 0x7ff8dcf97853 in gl::init::InitializeGLOneOffPlatformImplementation C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:246  

#23 0x7ff8dcf970da in gl::init::`anonymous namespace'::InitializeGLOneOffPlatformHelper C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:167  

#24 0x7ff8dcf973f9 in gl::init::InitializeGLNoExtensionsOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:202  

#25 0x7ff8dd5885f3 in gpu::GpuInit::InitializeAndStartSandbox C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_init.cc:402  

#26 0x7ff8de47dddb in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:321  

#27 0x7ff8d7a72775 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:669  

#28 0x7ff8d7a7434b in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1020  

#29 0x7ff8d7a70579 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:399  

#30 0x7ff8d7a71652 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:427  

#31 0x7ff8d12d148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#32 0x7ff68f0b5b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#33 0x7ff68f0b2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#34 0x7ff68f4b2fff in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#35 0x7ff95dbc7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#36 0x7ff95dd02650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:22 in \_\_asan\_memcpy  

Shadow bytes around the buggy address:  

0x04c3ddb94b50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x04c3ddb94b60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x04c3ddb94b70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x04c3ddb94b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x04c3ddb94b90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x04c3ddb94ba0: 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa fa  

0x04c3ddb94bb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04c3ddb94bc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04c3ddb94bd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04c3ddb94be0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04c3ddb94bf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==5044==ABORTING  

[7424:5996:0121/060617.431:ERROR:gpu\_process\_host.cc(972)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: SeongHwan Park (SeHwa)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 618 B)
- [asan.log](attachments/asan.log) (text/plain, 16.2 KB)

## Timeline

### [Deleted User] (2022-01-20)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-21)

Thanks this repros on HEAD.

Assigning based on linked CL.
FoundIn=96 as this is the latest deployed version (although this predates 96)
Severity=High for RCE in a sandboxed process (gpu).

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2022-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-01-24)

Hi syoussefi - any progress?

### sy...@chromium.org (2022-01-25)

Yes, I have a candidate fix: https://chromium-review.googlesource.com/c/angle/angle/+/3413004

### gi...@appspot.gserviceaccount.com (2022-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2ad5f350c55575d73585e47ee2f50e90035cc4ec

commit 2ad5f350c55575d73585e47ee2f50e90035cc4ec
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Jan 25 17:15:16 2022

Vulkan: Fix texture array level redefinition

When a level of a texture is redefined, all staged updates to that level
should be removed, not the ones specific to the new layers.  The bug
fixed was that if the texture was redefined to have its number of layers
changed, the staged higher-layer-count update to the image was not
removed.

Bug: chromium:1289383
Change-Id: I9b90025f78af80ab19a280f90b58510716da31d2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3413004
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Tim Van Patten <timvp@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/2ad5f350c55575d73585e47ee2f50e90035cc4ec/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/2ad5f350c55575d73585e47ee2f50e90035cc4ec/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/2ad5f350c55575d73585e47ee2f50e90035cc4ec/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2022-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fe5811a1e4ca6e7dc226adea186f7e67b53fabe5

commit fe5811a1e4ca6e7dc226adea186f7e67b53fabe5
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jan 27 04:36:15 2022

Roll ANGLE from 45237a047d68 to 2ad5f350c555 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/45237a047d68..2ad5f350c555

2022-01-27 syoussefi@chromium.org Vulkan: Fix texture array level redefinition

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1289383
Tbr: ynovikov@google.com
Change-Id: I6b78b826566988235e143306e5c2b90b117cce01
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3419463
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#963886}

[modify] https://crrev.com/fe5811a1e4ca6e7dc226adea186f7e67b53fabe5/DEPS


### sy...@chromium.org (2022-01-27)

@ajgo, this should be fixed now. Can you please verify?

(how come this didn't end up in Clusterfuzz like usual?)

### sy...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### aj...@chromium.org (2022-01-27)

Yes - please mark this as Fixed - thanks for getting to it quickly!

I did not upload to CF as I repro'd it easily.

### sy...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-27)

Requesting merge to extended stable M96 because latest trunk commit (963886) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (963886) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (963886) appears to be after beta branch point (950365).

Requesting merge to dev M99 because latest trunk commit (963886) appears to be after dev branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-27)

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
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-27)

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

### [Deleted User] (2022-01-27)

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

### [Deleted User] (2022-01-27)

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2022-01-27)

Answers for all four:

1. Security bug
2. https://chromium-review.googlesource.com/c/angle/angle/+/3413004
3. Not yet. Will be in a few days
4. No
5. N/A
6. N/A

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-04)

Congratulations! The VRP Panel has decided to award you $10,000 for this report! Thank you for this report and great work! 

### am...@chromium.org (2022-02-04)

while I am here; M98 is now stable, so merge to m96 and m97 is no longer needed. Merge approved to M99, please merge to branch 4844 at your earliest convenience. Thank you! 

### am...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/49e8ff16f1fe411460bc778d703a59bbaab3b5fe

commit 49e8ff16f1fe411460bc778d703a59bbaab3b5fe
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Jan 25 17:15:16 2022

M99: Vulkan: Fix texture array level redefinition

When a level of a texture is redefined, all staged updates to that level
should be removed, not the ones specific to the new layers.  The bug
fixed was that if the texture was redefined to have its number of layers
changed, the staged higher-layer-count update to the image was not
removed.

Bug: chromium:1289383
Change-Id: Iab79c38d846d1abbdd92e11b1b60a3adf0fbde4c
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3441309
Reviewed-by: Lingfeng Yang <lfy@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/49e8ff16f1fe411460bc778d703a59bbaab3b5fe/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/49e8ff16f1fe411460bc778d703a59bbaab3b5fe/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/49e8ff16f1fe411460bc778d703a59bbaab3b5fe/src/libANGLE/renderer/vulkan/TextureVk.cpp


### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-28)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-03-01)

merge approved to M98 for Extended Stable support, please merge to branch 4758 at your earliest convenience 

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-03-01)

1. Just https://crrev.com/c/3495124
2. Low, no conflicts
3. 99
4. Yes

Note: ran the tests locally: https://crrev.com/c/3495124/comments/d14bd4c3_6c232d93

### gm...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/33d2555cc1199c5435ce6fbddd514d7073754a01

commit 33d2555cc1199c5435ce6fbddd514d7073754a01
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Jan 25 17:15:16 2022

[M96-LTS] Vulkan: Fix texture array level redefinition

When a level of a texture is redefined, all staged updates to that level
should be removed, not the ones specific to the new layers.  The bug
fixed was that if the texture was redefined to have its number of layers
changed, the staged higher-layer-count update to the image was not
removed.

Bug: chromium:1289383
Change-Id: I9b90025f78af80ab19a280f90b58510716da31d2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3413004
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 2ad5f350c55575d73585e47ee2f50e90035cc4ec)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3495124
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/33d2555cc1199c5435ce6fbddd514d7073754a01/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/33d2555cc1199c5435ce6fbddd514d7073754a01/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/33d2555cc1199c5435ce6fbddd514d7073754a01/src/libANGLE/renderer/vulkan/TextureVk.cpp


### rz...@google.com (2022-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/937303239c746776a39cf568bda5a22ef096ca14

commit 937303239c746776a39cf568bda5a22ef096ca14
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Jan 25 17:15:16 2022

Vulkan: Fix texture array level redefinition

When a level of a texture is redefined, all staged updates to that level
should be removed, not the ones specific to the new layers.  The bug
fixed was that if the texture was redefined to have its number of layers
changed, the staged higher-layer-count update to the image was not
removed.

Bug: chromium:1289383
Change-Id: I9b90025f78af80ab19a280f90b58510716da31d2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3413004
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Tim Van Patten <timvp@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 2ad5f350c55575d73585e47ee2f50e90035cc4ec)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3516531
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/937303239c746776a39cf568bda5a22ef096ca14/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/937303239c746776a39cf568bda5a22ef096ca14/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/937303239c746776a39cf568bda5a22ef096ca14/src/libANGLE/renderer/vulkan/TextureVk.cpp


### [Deleted User] (2022-05-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1289383?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058536)*
