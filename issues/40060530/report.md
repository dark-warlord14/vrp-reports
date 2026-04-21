# Security: [ANGLE] Heap use-after-free caused by changing the framebuffer cache to sharing in context

| Field | Value |
|-------|-------|
| **Issue ID** | [40060530](https://issues.chromium.org/issues/40060530) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gg...@gmail.com |
| **Assignee** | cc...@google.com |
| **Created** | 2022-08-08 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap use-after-free vulnerability that exists in the Vulkan backend.

Before commit 72e457fee77e8859e1c916130268d76c7f20b178, |mFramebufferCache| was a member of FramebufferVk.  

But after commit, |mFramebufferCache| moved to a member of ShareGroupVk.  

And the code of the getFramebuffer function has been changed as follows.

**-------------------------** --------------------------------------------------------------  

angle::Result FramebufferVk::getFramebuffer(ContextVk \*contextVk,  

vk::Framebuffer \*\*framebufferOut,  

const vk::ImageView \*resolveImageViewIn,  

const SwapchainResolveMode swapchainResolveMode)  

{  

.....

- if (mFramebufferCache.get(contextVk, mCurrentFramebufferDesc, &framebufferHelper))

- if (contextVk->getShareGroup()->getFramebufferCache().get(contextVk, mCurrentFramebufferDesc,
- ```
                                                           mCurrentFramebuffer))  
  
  ```
  {  
  
  .....  
  
  }  
  
  **-------------------------** --------------------------------------------------------------

In the attached PoC, Framebuffer fb and fb2 have the same FramebufferDesc.  

On the first InvalidateFramebuffer call, the FramebufferCache is empty, so a new VkFramebuffer is allocated and cached.  

And on the second InvalidateFramebuffer call, a cache hit occurs because fb2 has the same FramebufferDesc.  

As a result, fb and fb2 will have the same VkFramebuffer handle.

And when deleteFramebuffer(fb) is called, the VkFramebuffer of fb/fb2 is added to the object garbage queue.  

After that, when the finish function is called, the CommandQueue::retireFinishedCommands function destroys the VkFramebuffer.  

(I used readPixels instead to call the finish function in Chrome.)

However, fb2 still has the destroyed VkFramebuffer handle.  

The attached PoC accesses the freed object when executed in Swiftshader.

**VERSION**  

Chrome Version: master (and tested on 105.0.5195.19 (Official Build) (64-bit) Beta)  

Operating System: Windows, Linux, ...

**REPRODUCTION CASE**  

Run the attached poc.html (with --disable-gpu)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==19948==ERROR: AddressSanitizer: heap-use-after-free on address 0x115d60562358 at pc 0x7ffa2128fbfd bp 0x0029b33ff240 sp 0x0029b33ff288  

READ of size 4 at 0x115d60562358 thread T4  

==19948==WARNING: Failed to use and restart external symbolizer!  

==19948==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==19948==\*\*\* Most likely this means that the app is already \*\*\*  

==19948==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==19948==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==19948==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffa2128fbfc in vk::Framebuffer::executeLoadOp C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkFramebuffer.cpp:83  

#1 0x7ffa2126d80b in `anonymous namespace'::CmdBeginRenderPass::execute C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:70  

#2 0x7ffa2126c6e5 in vk::CommandBuffer::submit C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:2344  

#3 0x7ffa212c0ef0 in vk::Queue::submitQueue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:104  

#4 0x7ffa212bfd5d in vk::Queue::taskLoop C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:156  

#5 0x7ffa212c2987 in std::Cr::\_\_thread\_proxy<std::Cr::tuple<std::Cr::unique\_ptr<std::Cr::\_\_thread\_struct,std::Cr::default\_delete[std::Cr::\_\_thread\_struct](javascript:void(0);) >,void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*> > C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:295  

#6 0x7ffa21c96035 in thread\_start<unsigned int (\_\_cdecl\*)(void \*),1> C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:97  

#7 0x7ff78df34193 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#8 0x7ffad2967033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#9 0x7ffad4082650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x115d60562358 is located 8 bytes inside of 40-byte region [0x115d60562350,0x115d60562378)  

freed by thread T0 here:  

#0 0x7ff78df2988c in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffa22e4df65 in rx::vk::GarbageObject::destroy C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_utils.cpp:763  

#2 0x7ffa22c2c3f8 in rx::vk::CommandQueue::retireFinishedCommands C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\CommandProcessor.cpp:970  

#3 0x7ffa22c24cfc in rx::vk::CommandQueue::finishToSerial C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\CommandProcessor.cpp:1077  

#4 0x7ffa22d04e28 in rx::RendererVk::finish C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:4412  

#5 0x7ffa22c4d611 in rx::ContextVk::finishImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:6730  

#6 0x7ffa22e32a86 in rx::vk::ImageHelper::readPixelsImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:9057  

#7 0x7ffa22e2f3c4 in rx::vk::ImageHelper::readPixels C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:8882  

#8 0x7ffa22c9b885 in rx::FramebufferVk::readPixelsImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:2895  

#9 0x7ffa22c9b15b in rx::FramebufferVk::readPixels C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:841  

#10 0x7ffa22567b1f in gl::Framebuffer::readPixels C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Framebuffer.cpp:1696  

#11 0x7ffa22505450 in gl::Context::readPixels C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:4706  

#12 0x7ffa22505567 in gl::Context::readPixelsRobust C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:4721  

#13 0x7ffa224a404a in GL\_ReadPixelsRobustANGLE C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_ext\_autogen.cpp:1947  

#14 0x7ffa043640ee in gl::GLApiBase::glReadPixelsRobustANGLEFn C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_bindings\_autogen\_gl.cc:5535  

#15 0x7ffa0fc3e986 in gpu::gles2::GLES2DecoderPassthroughImpl::DoReadPixels C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:2492  

#16 0x7ffa0fc742d5 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleReadPixels C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_handlers.cc:1104  

#17 0x7ffa0d760f85 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:894  

#18 0x7ffa0d76038a in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:832  

#19 0x7ffa04a35b47 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:218  

#20 0x7ffa01eaf084 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:498  

#21 0x7ffa01eae196 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:154  

#22 0x7ffa04a23fe9 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:706  

#23 0x7ffa04a2f1ed in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:819  

#24 0x7ffa01b7daa1 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:698  

#25 0x7ffa0073441a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#26 0x7ffa034812f9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:428  

#27 0x7ffa03480354 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:298

previously allocated by thread T0 here:  

#0 0x7ff78df2998c in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffa21630652 in sw::allocateZeroOrPoison C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\System\Memory.cpp:110  

#2 0x7ffa212e1007 in vk::ObjectBase<vk::Framebuffer,VkNonDispatchableHandle<VkFramebuffer\_T \*> >::Create<VkFramebufferCreateInfo> C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:92  

#3 0x7ffa22d9d34d in rx::vk::FramebufferHelper::init C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_cache\_utils.cpp:4000  

#4 0x7ffa22c96f8a in rx::FramebufferVk::getFramebuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:2247  

#5 0x7ffa22c9308a in rx::FramebufferVk::invalidateImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:1693  

#6 0x7ffa22c92a82 in rx::FramebufferVk::invalidate C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:399  

#7 0x7ffa0fc3c055 in gpu::gles2::GLES2DecoderPassthroughImpl::DoInvalidateFramebuffer C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:2262  

#8 0x7ffa0d760f85 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:894  

#9 0x7ffa0d76038a in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:832  

#10 0x7ffa04a35b47 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:218  

#11 0x7ffa01eaf084 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:498  

#12 0x7ffa01eae196 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:154  

#13 0x7ffa04a23fe9 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:706  

#14 0x7ffa04a2f1ed in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:819  

#15 0x7ffa01b7daa1 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:698  

#16 0x7ffa0073441a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#17 0x7ffa034812f9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:428  

#18 0x7ffa03480354 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:298  

#19 0x7ffa0345eb6a in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#20 0x7ffa0348338b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:581  

#21 0x7ffa006ce819 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#22 0x7ffa02cc5edc in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:391  

#23 0x7ffa002836f7 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:721  

#24 0x7ffa002858f2 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1070  

#25 0x7ffa00281cb5 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:433  

#26 0x7ffa00282488 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:461  

#27 0x7ff9f4a514ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182

Thread T4 created by T0 here:  

#0 0x7ff78df34c22 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffa21c95f02 in \_beginthreadex C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:209  

#2 0x7ffa21871e5b in std::Cr::\_\_libcpp\_thread\_create C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\src\support\win32\thread\_win32.cpp:203  

#3 0x7ffa212c0066 in std::Cr::thread::thread<void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*&,void> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:311  

#4 0x7ffa212bfa9f in vk::Queue::Queue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:38  

#5 0x7ffa2127cdc9 in vk::Device::Device C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDevice.cpp:138  

#6 0x7ffa212d8225 in vk::DispatchableObject<vk::Device,VkDevice\_T \*>::Create<VkDeviceCreateInfo,vk::PhysicalDevice \*,const VkPhysicalDeviceFeatures \*,std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);) > C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:147  

#7 0x7ffa212d7b14 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1093  

#8 0x7ffa2216f180 in terminator\_CreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5720  

#9 0x7ffa22169346 in loader\_create\_device\_chain C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4922  

#10 0x7ffa22167c49 in loader\_layer\_create\_device C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4355  

#11 0x7ffa2217e6d4 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\trampoline.c:848  

#12 0x7ffa22cf2c95 in rx::RendererVk::initializeDevice C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:2678  

#13 0x7ffa22ceb7ac in rx::RendererVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:1733  

#14 0x7ffa22c8e01f in rx::DisplayVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\DisplayVk.cpp:50  

#15 0x7ffa22e5098a in rx::DisplayVkWin32::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\win32\DisplayVkWin32.cpp:62  

#16 0x7ffa2254ba65 in egl::Display::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:988  

#17 0x7ffa22470609 in egl::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\egl\_stubs.cpp:468  

#18 0x7ffa22477d83 in EGL\_Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_egl\_autogen.cpp:330  

#19 0x7ffa04447674 in gl::GLDisplayEGL::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:876  

#20 0x7ffa04441edf in gl::GLDisplayEGL::Initialize C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:750  

#21 0x7ffa0442ded6 in gl::init::InitializeGLOneOffPlatform C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_initializer\_win.cc:132  

#22 0x7ffa01978e01 in gl::init::InitializeGLOneOffPlatformImplementation C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:219  

#23 0x7ffa0197864d in gl::init::`anonymous namespace'::InitializeGLOneOffPlatformHelper C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:143  

#24 0x7ffa0197898d in gl::init::InitializeGLNoExtensionsOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:174  

#25 0x7ffa01ebaa31 in gpu::GpuInit::InitializeAndStartSandbox C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_init.cc:478  

#26 0x7ffa02cc5bd6 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:322  

#27 0x7ffa002836f7 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:721  

#28 0x7ffa002858f2 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1070  

#29 0x7ffa00281cb5 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:433  

#30 0x7ffa00282488 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:461  

#31 0x7ff9f4a514ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182  

#32 0x7ff78de85a0e in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162  

#33 0x7ff78de82bd0 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#34 0x7ff78e2857bf in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#35 0x7ffad2967033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#36 0x7ffad4082650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkFramebuffer.cpp:83 in vk::Framebuffer::executeLoadOp  

Shadow bytes around the buggy address:  

0x03810c42c410: f7 fa fd fd fd fd fd fa f7 fa 00 00 00 00 00 fa  

0x03810c42c420: f7 fa fd fd fd fd fd fd f7 fa 00 00 00 00 00 fa  

0x03810c42c430: f7 fa 00 00 00 00 00 fa f7 fa fd fd fd fd fd fd  

0x03810c42c440: f7 fa 00 00 00 00 00 fa f7 fa 00 00 00 00 00 fa  

0x03810c42c450: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd  

=>0x03810c42c460: f7 fa fd fd fd fd fd fd f7 fa fd[fd]fd fd fd fa  

0x03810c42c470: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd  

0x03810c42c480: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd  

0x03810c42c490: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd  

0x03810c42c4a0: f7 fa 00 00 00 00 00 00 f7 fa fd fd fd fd fd fd  

0x03810c42c4b0: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd  

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

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to the crash.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.  

==19948==ABORTING  

[11092:16396:0809/034448.369:ERROR:gpu\_process\_host.cc(973)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: SeongHwan Park (SeHwa)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.0 KB)

## Timeline

### [Deleted User] (2022-08-08)

[Empty comment from Monorail migration]

### ma...@google.com (2022-08-08)

Based on the asan trace, I suspect this is a duplicate of 1223346. ANGLE owners, could you please triage this?

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2022-08-08)

[Empty comment from Monorail migration]

### ma...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ge...@chromium.org (2022-08-10)

[Empty comment from Monorail migration]

### cc...@google.com (2022-08-10)

[Empty comment from Monorail migration]

### cc...@google.com (2022-08-10)

Thanks for the bug report with such detailed explanation. Will fix soon. 

### gi...@appspot.gserviceaccount.com (2022-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/badfeecdeb5795e72edb17145fe1b6631c89706f

commit badfeecdeb5795e72edb17145fe1b6631c89706f
Author: Charlie Lao <cclao@google.com>
Date: Wed Aug 10 21:38:43 2022

Vulkan: Destroy fb1 should not affect fb2 with same attachments

If two FBOs has the same attachments. they will share the same
VkFramebuffers. Destroy one fbo should not cause trouble for the other
fbo.

Bug: chromium:1351170
Change-Id: I032da8cc12eb8556c3e325c8fd7a3de9974ae909
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3824302
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Yuxin Hu <yuxinhu@google.com>
Commit-Queue: Charlie Lao <cclao@google.com>

[modify] https://crrev.com/badfeecdeb5795e72edb17145fe1b6631c89706f/src/libANGLE/renderer/vulkan/SurfaceVk.cpp
[modify] https://crrev.com/badfeecdeb5795e72edb17145fe1b6631c89706f/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/badfeecdeb5795e72edb17145fe1b6631c89706f/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/badfeecdeb5795e72edb17145fe1b6631c89706f/src/libANGLE/renderer/vulkan/SurfaceVk.h
[modify] https://crrev.com/badfeecdeb5795e72edb17145fe1b6631c89706f/src/libANGLE/renderer/vulkan/RenderTargetVk.h
[modify] https://crrev.com/badfeecdeb5795e72edb17145fe1b6631c89706f/src/libANGLE/renderer/vulkan/FramebufferVk.h


### cc...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### cc...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7df4a715cdaee4e863b5d1d132b8cf45c1bf010f

commit 7df4a715cdaee4e863b5d1d132b8cf45c1bf010f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Aug 11 20:43:58 2022

Roll ANGLE from 87ed2c9d1eaf to c9360ccbd34a (7 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/87ed2c9d1eaf..c9360ccbd34a

2022-08-11 rafael.cintron@microsoft.com Reflect TextureD3D label updates with storage object
2022-08-11 chris@rive.app Require all PLS formats to consume exactly 4 bytes of storage
2022-08-11 cclao@google.com Vulkan: Destroy fb1 should not affect fb2 with same attachments
2022-08-11 chris@rive.app Make PLS coherent on Vulkan
2022-08-11 kpiddington@apple.com Separate Struct declarations earlier
2022-08-11 syoussefi@chromium.org Presubmit: Verify ANGLE_SH_VERSION update
2022-08-11 penghuang@chromium.org Fix EGL_ANGLE_program_cache_control for eglCreateContext

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC geofflang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1336126,chromium:1351170
Tbr: geofflang@google.com
Change-Id: I1c760d42c9d421cfe2b41d0d3acc7759711ab3a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3827086
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1034161}

[modify] https://crrev.com/7df4a715cdaee4e863b5d1d132b8cf45c1bf010f/DEPS


### [Deleted User] (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

Requesting merge to beta M105 because latest trunk commit (1034161) appears to be after beta branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-12)

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations, SeongHwan! The VRP Panel has decided to award you $15,000 for this report  (based on the updated VRP reward amounts [1]) + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us and nice work! 

### am...@chromium.org (2022-08-17)

105 merge approved, please merge this fix to branch 5195 at your earliest convenience -- thank you! 

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/464a5524426ab61a9109dea079ad73a817e3a56a

commit 464a5524426ab61a9109dea079ad73a817e3a56a
Author: Charlie Lao <cclao@google.com>
Date: Wed Aug 10 21:38:43 2022

Vulkan: Destroy fb1 should not affect fb2 with same attachments

If two FBOs has the same attachments. they will share the same
VkFramebuffers. Destroy one fbo should not cause trouble for the other
fbo.

Bug: chromium:1351170
Change-Id: I032da8cc12eb8556c3e325c8fd7a3de9974ae909
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3824302
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Yuxin Hu <yuxinhu@google.com>
Commit-Queue: Charlie Lao <cclao@google.com>
(cherry picked from commit badfeecdeb5795e72edb17145fe1b6631c89706f)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3849807
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

[modify] https://crrev.com/464a5524426ab61a9109dea079ad73a817e3a56a/src/libANGLE/renderer/vulkan/SurfaceVk.cpp
[modify] https://crrev.com/464a5524426ab61a9109dea079ad73a817e3a56a/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/464a5524426ab61a9109dea079ad73a817e3a56a/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/464a5524426ab61a9109dea079ad73a817e3a56a/src/libANGLE/renderer/vulkan/RenderTargetVk.h
[modify] https://crrev.com/464a5524426ab61a9109dea079ad73a817e3a56a/src/libANGLE/renderer/vulkan/SurfaceVk.h
[modify] https://crrev.com/464a5524426ab61a9109dea079ad73a817e3a56a/src/libANGLE/renderer/vulkan/FramebufferVk.h


### [Deleted User] (2022-08-23)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-08-23)

[Empty comment from Monorail migration]

### pb...@google.com (2022-08-23)

The Cl from https://crbug.com/chromium/1351170#c23 is causing Compile failures, thanks to avi@ for investigating the failure.

### av...@chromium.org (2022-08-23)

The cherrypick in https://crbug.com/chromium/1351170#c23 is a bad merge.

https://crbug.com/chromium/1351170#c23 merged https://chromium-review.googlesource.com/c/angle/angle/+/3824302. However, that CL relied on the change to vk_cache_util.h in https://chromium-review.googlesource.com/c/angle/angle/+/3780845. Doing that merge without merging the predecessor patch is causing failures on:

https://ci.chromium.org/ui/p/chrome/builders/official/win64-clang/4865/overview
https://ci.chromium.org/ui/p/chrome/builders/official/mac64/4723/overview
https://ci.chromium.org/ui/p/chrome/builders/official/linux64/4493/overview

among other bots.

../../third_party/angle/src\libANGLE/renderer/vulkan/RenderTargetVk.h(143,79): error: too many arguments to function call, expected 0, have 1
    void destroy(RendererVk *renderer) { mFramebufferCacheManager.destroyKeys(renderer); }
                                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ^~~~~~~~
../../third_party/angle/src\libANGLE/renderer/vulkan/vk_cache_utils.h(1625,10): note: 'destroyKeys' declared here
    void destroyKeys();
         ^
1 error generated.

Please revert the cherrypick in https://crbug.com/chromium/1351170#c23, and re-evaluate what the required predecessor merges will be before cherrypicking again.

### av...@chromium.org (2022-08-23)

(The compile failure from the bad cherrypick is filed as https://crbug.com/chromium/1355943.)

### pb...@google.com (2022-08-23)

This is blocking our M105 Stable RC cut, can we please either revert or make a call on the decency merge asap, so that we have builds ready for our test team.

### gi...@appspot.gserviceaccount.com (2022-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/0d377998eca94d7840bf444b06cb3aeacc06eebd

commit 0d377998eca94d7840bf444b06cb3aeacc06eebd
Author: Charlie Lao <cclao@google.com>
Date: Tue Aug 23 20:32:10 2022

Revert "Vulkan: Destroy fb1 should not affect fb2 with same attachments"

This reverts commit 464a5524426ab61a9109dea079ad73a817e3a56a.

Reason for revert: It breaks build.

Original change's description:
> Vulkan: Destroy fb1 should not affect fb2 with same attachments
>
> If two FBOs has the same attachments. they will share the same
> VkFramebuffers. Destroy one fbo should not cause trouble for the other
> fbo.
>
> Bug: chromium:1351170
> Change-Id: I032da8cc12eb8556c3e325c8fd7a3de9974ae909
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3824302
> Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
> Reviewed-by: Yuxin Hu <yuxinhu@google.com>
> Commit-Queue: Charlie Lao <cclao@google.com>
> (cherry picked from commit badfeecdeb5795e72edb17145fe1b6631c89706f)
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3849807
> Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

Bug: chromium:1351170
Change-Id: Ic3173bf61129a2d076886978a97d5beda21d89cf
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3852241
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/0d377998eca94d7840bf444b06cb3aeacc06eebd/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/0d377998eca94d7840bf444b06cb3aeacc06eebd/src/libANGLE/renderer/vulkan/SurfaceVk.cpp
[modify] https://crrev.com/0d377998eca94d7840bf444b06cb3aeacc06eebd/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/0d377998eca94d7840bf444b06cb3aeacc06eebd/src/libANGLE/renderer/vulkan/SurfaceVk.h
[modify] https://crrev.com/0d377998eca94d7840bf444b06cb3aeacc06eebd/src/libANGLE/renderer/vulkan/RenderTargetVk.h
[modify] https://crrev.com/0d377998eca94d7840bf444b06cb3aeacc06eebd/src/libANGLE/renderer/vulkan/FramebufferVk.h


### gi...@appspot.gserviceaccount.com (2022-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2f0d8ab049b10ee41f9b90cea8da8e80db076e38

commit 2f0d8ab049b10ee41f9b90cea8da8e80db076e38
Author: Charlie Lao <cclao@google.com>
Date: Wed Aug 10 21:38:43 2022

Reland "Vulkan: Destroy fb1 should not affect fb2 with same attachments"

This is a reland of commit 464a5524426ab61a9109dea079ad73a817e3a56a

Original change's description:
> Vulkan: Destroy fb1 should not affect fb2 with same attachments
>
> If two FBOs has the same attachments. they will share the same
> VkFramebuffers. Destroy one fbo should not cause trouble for the other
> fbo.
>
> Bug: chromium:1351170
> Change-Id: I032da8cc12eb8556c3e325c8fd7a3de9974ae909
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3824302
> Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
> Reviewed-by: Yuxin Hu <yuxinhu@google.com>
> Commit-Queue: Charlie Lao <cclao@google.com>
> (cherry picked from commit badfeecdeb5795e72edb17145fe1b6631c89706f)
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3849807
> Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

Bug: chromium:1351170
Change-Id: I846eeb62899f6b1ce727144093c7475c0394fe24
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3852261
Reviewed-by: Lingfeng Yang <lfy@google.com>
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

[modify] https://crrev.com/2f0d8ab049b10ee41f9b90cea8da8e80db076e38/src/libANGLE/renderer/vulkan/SurfaceVk.cpp
[modify] https://crrev.com/2f0d8ab049b10ee41f9b90cea8da8e80db076e38/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/2f0d8ab049b10ee41f9b90cea8da8e80db076e38/src/libANGLE/renderer/vulkan/SurfaceVk.h
[modify] https://crrev.com/2f0d8ab049b10ee41f9b90cea8da8e80db076e38/src/libANGLE/renderer/vulkan/RenderTargetVk.h
[modify] https://crrev.com/2f0d8ab049b10ee41f9b90cea8da8e80db076e38/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/2f0d8ab049b10ee41f9b90cea8da8e80db076e38/src/libANGLE/renderer/vulkan/FramebufferVk.h


### kb...@chromium.org (2022-08-23)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-25)

Most of the changed code isn't present in 102

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1351170?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1355943]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060530)*
