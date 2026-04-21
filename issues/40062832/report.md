# Security: [swiftshader] heap-use-after-free on vk::Query::start

| Field | Value |
|-------|-------|
| **Issue ID** | [40062832](https://issues.chromium.org/issues/40062832) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-01-30 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

==1192==ERROR: AddressSanitizer: heap-use-after-free on address 0x11dfc3ef0eb0 at pc 0x7ffae8ef45cf bp 0x008b6abff050 sp 0x008b6abff098  

WRITE of size 4 at 0x11dfc3ef0eb0 thread T26  

==1192==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffae8ef45ce in vk::Query::start C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueryPool.cpp:43  

#1 0x7ffae8fcfdf8 in sw::DrawCall::run C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Device\Renderer.cpp:555  

#2 0x7ffae8fcd68c in sw::Renderer::draw C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Device\Renderer.cpp:491  

#3 0x7ffae8ea2a99 in `anonymous namespace'::CmdDrawBase::draw C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:957 #4 0x7ffae8ea24a5 in` anonymous namespace'::CmdDraw::execute C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:985  

#5 0x7ffae8e9c8a0 in vk::CommandBuffer::submit C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:2330  

#6 0x7ffae8ef6bfd in vk::Queue::submitQueue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:104  

#7 0x7ffae8ef5a75 in vk::Queue::taskLoop C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:156  

#8 0x7ffae8ef871a in std::Cr::\_\_thread\_proxy<std::Cr::tuple<std::Cr::unique\_ptr<std::Cr::\_\_thread\_struct,std::Cr::default\_delete[std::Cr::\_\_thread\_struct](javascript:void(0);) >,void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*> > C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:293  

#9 0x7ffae98e5ab5 in thread\_start<unsigned int (\_\_cdecl\*)(void \*),1> C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:97  

#10 0x7ff68608cb13 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#11 0x7ffb26ea7613 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017613)  

#12 0x7ffb27ca26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

0x11dfc3ef0eb0 is located 48 bytes inside of 3096-byte region [0x11dfc3ef0e80,0x11dfc3ef1a98)  

freed by thread T21 here:  

#0 0x7ff686081a0d in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffae8f129e8 in vkDestroyQueryPool C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1843  

#2 0x7ffaf2331dcf in rx::vk::DynamicQueryPool::destroyPoolImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3798  

#3 0x7ffaf2331d4b in rx::vk::DynamicallyGrowingPool[rx::vk::QueryPool](javascript:void(0);)::destroyEntryPool C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3695  

#4 0x7ffaf2126f2d in rx::ContextVk::onDestroy C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1186  

#5 0x7ffaf2446920 in gl::Context::onDestroy C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:855  

#6 0x7ffaf24c546a in egl::Display::releaseContextImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:1761  

#7 0x7ffaf24cd311 in egl::Display::makeCurrent C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:1618  

#8 0x7ffaf24ce270 in egl::Display::destroyContext C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:1803  

#9 0x7ffaf20a0553 in egl::DestroyContext C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\egl\_stubs.cpp:291  

#10 0x7ffaf20a8055 in EGL\_DestroyContext C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_egl\_autogen.cpp:205  

#11 0x7ffabe064697 in gl::GLContextEGL::Destroy C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_context\_egl.cc:383  

#12 0x7ffabe06634c in gl::GLContextEGL::~GLContextEGL C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_context\_egl.cc:558  

#13 0x7ffabe0663d3 in gl::GLContextEGL::~GLContextEGL C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_context\_egl.cc:557  

#14 0x7ffabdfeef40 in scoped\_refptr[gl::GLContext](javascript:void(0);)::reset C:\b\s\w\ir\cache\builder\src\base\memory\scoped\_refptr.h:310  

#15 0x7ffac8b84908 in gpu::gles2::GLES2DecoderPassthroughImpl::Destroy C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:1448  

#16 0x7ffabb8ff8b5 in gpu::CommandBufferStub::Destroy C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:361  

#17 0x7ffabb8fe866 in gpu::CommandBufferStub::~CommandBufferStub C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:135  

#18 0x7ffac21d1761 in gpu::GLES2CommandBufferStub::~GLES2CommandBufferStub C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gles2\_command\_buffer\_stub.cc:77  

#19 0x7ffabe84748f in gpu::GpuChannel::DestroyCommandBuffer C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:945  

#20 0x7ffabe854c6a in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(int),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:970  

#21 0x7ffabcfc5020 in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post\_task\_and\_reply\_impl.cc:106  

#22 0x7ffabcfc5be6 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:970  

#23 0x7ffab9beff47 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:165  

#24 0x7ffabcfa9647 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:484  

#25 0x7ffabcfa8163 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:335  

#26 0x7ffab9cace65 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#27 0x7ffab9caaa9d in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78

previously allocated by thread T21 here:  

#0 0x7ff686081b0d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffae9260fde in sw::allocateZeroOrPoison C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\System\Memory.cpp:110  

#2 0x7ffae8f1292b in vk::ObjectBase<vk::QueryPool,VkNonDispatchableHandle<VkQueryPool\_T \*> >::Create<VkQueryPoolCreateInfo> C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:92  

#3 0x7ffae8f12802 in vkCreateQueryPool C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1835  

#4 0x7ffaf2332756 in rx::vk::DynamicQueryPool::allocatePoolImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3832  

#5 0x7ffaf233229a in rx::vk::DynamicallyGrowingPool[rx::vk::QueryPool](javascript:void(0);)::allocatePoolEntries C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3756  

#6 0x7ffaf2331f27 in rx::vk::DynamicQueryPool::allocateQuery C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3809  

#7 0x7ffaf21ad465 in rx::QueryVk::onRenderPassStart C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\QueryVk.cpp:211  

#8 0x7ffaf214db03 in rx::ContextVk::resumeRenderPassQueriesIfActive C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:7597  

#9 0x7ffaf226a6ea in rx::UtilsVk::clearFramebuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\UtilsVk.cpp:2315  

#10 0x7ffaf2175a59 in rx::FramebufferVk::clearWithDraw C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:2561  

#11 0x7ffaf21735f7 in rx::FramebufferVk::clearImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:722  

#12 0x7ffaf2172798 in rx::FramebufferVk::clear C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:467  

#13 0x7ffabdf54e09 in gl::RealGLApi::glClearFn C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_gl\_api\_implementation.cc:428  

#14 0x7ffacb225110 in gpu::gles2::GLES2DecoderPassthroughImpl::DoClear C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:693  

#15 0x7ffac8b7ca89 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:901  

#16 0x7ffac8b7bef4 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:839  

#17 0x7ffabe85b614 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:225  

#18 0x7ffabb9016ce in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:516  

#19 0x7ffabb900356 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:154  

#20 0x7ffabe843959 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:694  

#21 0x7ffabe8521bc in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:970  

#22 0x7ffabe262856 in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler\_dfs.cc:763  

#23 0x7ffabe260954 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler\_dfs.cc:674  

#24 0x7ffabe2691ef in base::internal::Invoker<base::internal::BindState<void (gpu::SchedulerDfs::\*)(),base::internal::UnretainedWrapper[gpu::SchedulerDfs,base::unretained\_traits::MayNotDangle](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:970  

#25 0x7ffab9beff47 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:165  

#26 0x7ffabcfa9647 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:484  

#27 0x7ffabcfa8163 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:335

Thread T26 created by T21 here:  

#0 0x7ff68608d6d2 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffae98e5982 in \_beginthreadex C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:209  

#2 0x7ffae94b8781 in std::Cr::\_\_libcpp\_thread\_create C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\src\support\win32\thread\_win32.cpp:203  

#3 0x7ffae8ef5d7e in std::Cr::thread::thread<void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*&,void> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:309  

#4 0x7ffae8ef57b2 in vk::Queue::Queue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:38  

#5 0x7ffae8eadaf1 in vk::Device::Device C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDevice.cpp:139  

#6 0x7ffae8f0df70 in vk::DispatchableObject<vk::Device,VkDevice\_T \*>::Create<VkDeviceCreateInfo,vk::PhysicalDevice \*,const VkPhysicalDeviceFeatures \*,std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);) > C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:147  

#7 0x7ffae8f0d8d1 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1183  

#8 0x7ffaf1eb620d in terminator\_CreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5796  

#9 0x7ffaf1eb0025 in loader\_create\_device\_chain C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4953  

#10 0x7ffaf1eae943 in loader\_layer\_create\_device C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4370  

#11 0x7ffaf1ec4f1d in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\trampoline.c:842  

#12 0x7ffaf21e155b in rx::RendererVk::initializeDevice C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:2985  

#13 0x7ffaf21d9c5a in rx::RendererVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:1817  

#14 0x7ffaf21621d6 in rx::DisplayVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\DisplayVk.cpp:130  

#15 0x7ffaf23867d4 in rx::DisplayVkWin32::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\win32\DisplayVkWin32.cpp:62  

#16 0x7ffaf24c10b3 in egl::Display::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:1010  

#17 0x7ffaf20a1968 in egl::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\egl\_stubs.cpp:461  

#18 0x7ffaf20a941c in EGL\_Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_egl\_autogen.cpp:373  

#19 0x7ffabe069edb in gl::GLDisplayEGL::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:722  

#20 0x7ffabe06828f in gl::GLDisplayEGL::Initialize C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:627  

#21 0x7ffac1db67a1 in gl::init::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_display\_initializer.cc:261  

#22 0x7ffabe05d33d in gl::init::InitializeGLOneOffPlatform C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_initializer\_win.cc:133  

#23 0x7ffabaf297be in gl::init::InitializeGLOneOffPlatformImplementation C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:219  

#24 0x7ffabaf28fa5 in gl::init::`anonymous namespace'::InitializeGLOneOffPlatformHelper C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_factory.cc:143 #25 0x7ffabaf29363 in gl::init::InitializeGLNoExtensionsOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_factory.cc:174 #26 0x7ffabb9146ee in gpu::GpuInit::InitializeInProcess C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_init.cc:867 #27 0x7ffabc69f04c in content::InProcessGpuThread::Init C:\b\s\w\ir\cache\builder\src\content\gpu\in_process_gpu_thread.cc:63 #28 0x7ffab9c51bdd in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:403 #29 0x7ffab9cd1a11 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:134  

#30 0x7ff68608cb13 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#31 0x7ffb26ea7613 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017613)  

#32 0x7ffb27ca26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

Thread T21 created by T0 here:  

#0 0x7ff68608d6d2 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffab9cd076f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:199  

#2 0x7ffab9c50962 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:217  

#3 0x7ffab453ab19 in content::GpuProcessHost::Init C:\b\s\w\ir\cache\builder\src\content\browser\gpu\gpu\_process\_host.cc:897  

#4 0x7ffab4539bb5 in content::GpuProcessHost::Get C:\b\s\w\ir\cache\builder\src\content\browser\gpu\gpu\_process\_host.cc:592  

#5 0x7ffab57f726d in content::VizProcessTransportFactory::ConnectHostFrameSinkManager C:\b\s\w\ir\cache\builder\src\content\browser\compositor\viz\_process\_transport\_factory.cc:189  

#6 0x7ffab3f45aff in content::BrowserMainLoop::PostCreateThreadsImpl C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1321  

#7 0x7ffab3f44959 in content::BrowserMainLoop::PostCreateThreads C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:963  

#8 0x7ffab3f4bc3a in base::internal::Invoker<base::internal::BindState<int (content::BrowserMainLoop::\*)(),base::internal::UnretainedWrapper[content::BrowserMainLoop,base::unretained\_traits::MayNotDangle](javascript:void(0);) >,int ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:970  

#9 0x7ffab530cbe0 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup\_task\_runner.cc:44  

#10 0x7ffab3f43ca4 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:890  

#11 0x7ffab3f4e0a4 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:141  

#12 0x7ffab3f3f73f in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:28  

#13 0x7ffab83fe669 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:715  

#14 0x7ffab84023f1 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1263  

#15 0x7ffab8401b02 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1117  

#16 0x7ffab83fc5a4 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:324  

#17 0x7ffab83fd494 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:352  

#18 0x7ffaac94168c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:180  

#19 0x7ff685fd6378 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#20 0x7ff685fd2bb1 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#21 0x7ff68643f02b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#22 0x7ffb26ea7613 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017613)  

#23 0x7ffb27ca26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueryPool.cpp:43 in vk::Query::start  

Shadow bytes around the buggy address:  

0x11dfc3ef0c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11dfc3ef0c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x11dfc3ef0d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x11dfc3ef0d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x11dfc3ef0e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa  

=>0x11dfc3ef0e80: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd  

0x11dfc3ef0f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11dfc3ef0f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11dfc3ef1000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11dfc3ef1080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11dfc3ef1100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==1192==ADDITIONAL INFO

==1192==Note: Please include this section with the ASan report.  

Task trace:

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==1192==END OF ADDITIONAL INFO  

==1192==ABORTING

**VERSION**  

Chrome Version: 111.0.5560.0 (Developer Build) (64-bit) with ASan  

Operating System: [Windows 10]

**REPRODUCTION CASE**  

I am trying to minimize testcase will upload it later.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU Process  

Crash State: See asan.log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 21.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.8 KB)
- [windbg.log](attachments/windbg.log) (text/plain, 11.1 KB)

## Timeline

### [Deleted User] (2023-01-30)

[Empty comment from Monorail migration]

### fl...@google.com (2023-02-02)

Hello & thanks for the report!  Are you still working on minimizing that testcase?

I can't fully triage/reproduce this bug as-is.  If you could provide a testcase, reproduction steps, and/or bisection, that will allow us to  prioritize this accordingly, and greatly increase the time to resolution and fix.

geofflang@, I was told you're a good contact for swiftshader issues.  If it's possible for you to diagnose and fix the issue based on the provided ASAN stacktrace, please do so (and please comment if you do so, about when the issue may have been introduced / which branches may be affected).

I'll set NextAction for this for a week from now.  nesk@, if you can provide new actionable information before then, that'll help us avoid closing this as WontFix.

[Monorail components: Internals>GPU>SwiftShader]

### fl...@google.com (2023-02-02)

(reassigning owner based on away status)

### sy...@chromium.org (2023-02-02)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2023-02-02)

I've attached a minimized testcase.

when testing in chrome, the following parameters are required to use the swiftshader renderer.

```
asan-win32-release_x64-1096728\chrome.exe --no-sandbox --single-process --disable-gpu poc.html
```

### ne...@nesk.kr (2023-02-02)


VULNERABILITY DETAILS

the use-after-free is caused by the occlusionQuery (vk::Query) object. [1]

```
void DrawCall::setup()
{
	if(occlusionQuery != nullptr)
	{
		occlusionQuery->start();
	}
```

The query object is allocated by gl.clear([2]) and set by gl.beginQuery as a member variable of the Renderer.

```
void Renderer::addQuery(vk::Query *query)
{
	ASSERT(query->getType() == VK_QUERY_TYPE_OCCLUSION);
	ASSERT(!occlusionQuery);
	occlusionQuery = query;
}
```

This query object is freed by vkDestroyQueryPool([4]), which seems to be caused by location.href [5]

However, during the Context::onDestroy process, no one called Renderer::removeQuery, and `occlusionQuery` still has a reference to the freed pointer [6]

I think the patch should reset the occlusionQuery pointer via removeQuery in the destroy process.

[1] https://swiftshader.googlesource.com/SwiftShader/+/dd7bb92b9a7a813ebc2da9fe3f6484c34cc69363/src/Device/Renderer.cpp#495
[2] https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=585206#57
[3] https://swiftshader.googlesource.com/SwiftShader/+/dd7bb92b9a7a813ebc2da9fe3f6484c34cc69363/src/Device/Renderer.cpp#1210
[4] https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=585206#25
[5] https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=585638#67
[6] https://swiftshader.googlesource.com/SwiftShader/+/dd7bb92b9a7a813ebc2da9fe3f6484c34cc69363/src/Device/Renderer.cpp#1218


### [Deleted User] (2023-02-02)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-02)

[Empty comment from Monorail migration]

### cc...@google.com (2023-02-02)

The query oject in the backtrace is a renderPass query (since it is allocated from  rx::QueryVk::onRenderPassStart). 
renderPass query's queue serial is set when endQuery is called, (from QueryHelper::endRenderPassQuery()) 
renderPass query's mUse is merged into  DynamicallyGrowingPool<Pool>'s mUse when query is freed. (From DynamicallyGrowingPool<Pool>::onEntryFreed())
So the ResourceUse tracking appears okay, even though a bit confusing.

The other big question is the context is already destroyed, but the query is still actively used by swiftshader. This indicates some how renderer->finish() call is not actually finishing. Note that the query pool is per context. When we destroy context, we make sure all commands on the context has been finished. If there is a bug in that code path, then you will run into this. But looking at the implementation, I am also not seeing obvious bug here.


### cc...@google.com (2023-02-02)

Looking at the test case (poc.html), it calls beginQuery, but missing endQuery call. And there is no flush as well, how come ANGLE receive any commands at all? If someone could generate the OpenGLES API call sequence, that will be helpful. 

### [Deleted User] (2023-02-16)

syoussefi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-02-16)

This is triggering an assert failure:

UtilsVk.cpp:2311 (clearFramebuffer): 	! Assert failed in clearFramebuffer (../../src/libANGLE/renderer/vulkan/UtilsVk.cpp:2311): contextVk->hasActiveRenderPass()

That's probably why thinks go awry. I'll work on a fix ASAP

### gi...@appspot.gserviceaccount.com (2023-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/05e62f39412e8c6bfc98582f5e7a49041991c97b

commit 05e62f39412e8c6bfc98582f5e7a49041991c97b
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Fri Feb 17 04:16:46 2023

Vulkan: Don't close render pass if rebind to same fbo

In the Vulkan backend, the render pass can occasionally (and
transiently) be in a state of "open but inactive".  This is when the
render pass is closed, but has the potential for future modifications
(for example to add a resolve attachment).  Under many circumstances, it
is expected that an open render pass cannot be in such a state.

This assumption can be broken in this scenario:

- Open render pass, draw, etc
- Change framebuffer binding
- Change framebuffer binding back to original
- Masked Clear

When ContextVk is synced before clear, it sees that the framebuffer
binding is changed (though it hasn't really), and it closes the render
passes and sets the render pass dirty bit.  If a draw were to follow, a
new render pass would have started (unnecessarily).  However, in the
case of a masked clear, UtilsVk notices that the render pass is started,
assumes it must be active, and continues recording to it.  While the
operation itself succeeds, the assumption that the render pass is active
is false (and fails assertion).

This change makes sure that framebuffer binding change is no-oped if the
framebuffer is the same one that has opened the current render pass.  If
any application does unnecessary binding changes and back, it will be
optimized by this change as well.

Bug: chromium:1411210
Change-Id: I37a3a9f2eaa1a81a1b3393840b9458ec71a87377
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4261215
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/05e62f39412e8c6bfc98582f5e7a49041991c97b/src/tests/gl_tests/ClearTest.cpp
[modify] https://crrev.com/05e62f39412e8c6bfc98582f5e7a49041991c97b/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
[modify] https://crrev.com/05e62f39412e8c6bfc98582f5e7a49041991c97b/src/libANGLE/renderer/vulkan/ContextVk.cpp


### sy...@chromium.org (2023-02-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e5767a688a67908055f9447a463e7baca95bf776

commit e5767a688a67908055f9447a463e7baca95bf776
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Feb 18 08:11:53 2023

Roll ANGLE from e1dfc00aa66b to 05e62f39412e (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/e1dfc00aa66b..05e62f39412e

2023-02-17 syoussefi@chromium.org Vulkan: Don't close render pass if rebind to same fbo

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,ianelliott@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1411210
Tbr: ianelliott@google.com
Change-Id: I679b23deed71318adb91f691fa33d6b13f12d2c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4265586
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1107137}

[modify] https://crrev.com/e5767a688a67908055f9447a463e7baca95bf776/DEPS


### [Deleted User] (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-27)

This looks like this issue goes back to at least M110, but the FoundIn was never updated with the POC and new info; updating accordingly


### am...@chromium.org (2023-02-27)

Given deadlines and time since CL was landed and on canary, I'm going to go ahead of the bot and review this for merge. 
Approving for merge to M111 and M110 
Please merge to branches 5563 and 5481 respectively, ASAP (before 9am Pacific tomorrow, Tuesday 28 February) so this fix can be included in M111/Stable RC cut M110/Extended 

### am...@chromium.org (2023-02-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-27)

[Empty comment from Monorail migration]

### pb...@google.com (2023-02-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/6da1a8953313032d2c19bcf83876700d818a0ccb

commit 6da1a8953313032d2c19bcf83876700d818a0ccb
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Fri Feb 17 04:16:46 2023

M110: Vulkan: Don't close render pass if rebind to same fbo

In the Vulkan backend, the render pass can occasionally (and
transiently) be in a state of "open but inactive".  This is when the
render pass is closed, but has the potential for future modifications
(for example to add a resolve attachment).  Under many circumstances, it
is expected that an open render pass cannot be in such a state.

This assumption can be broken in this scenario:

- Open render pass, draw, etc
- Change framebuffer binding
- Change framebuffer binding back to original
- Masked Clear

When ContextVk is synced before clear, it sees that the framebuffer
binding is changed (though it hasn't really), and it closes the render
passes and sets the render pass dirty bit.  If a draw were to follow, a
new render pass would have started (unnecessarily).  However, in the
case of a masked clear, UtilsVk notices that the render pass is started,
assumes it must be active, and continues recording to it.  While the
operation itself succeeds, the assumption that the render pass is active
is false (and fails assertion).

This change makes sure that framebuffer binding change is no-oped if the
framebuffer is the same one that has opened the current render pass.  If
any application does unnecessary binding changes and back, it will be
optimized by this change as well.

Bug: chromium:1411210
Change-Id: I37a3a9f2eaa1a81a1b3393840b9458ec71a87377
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4261215
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 05e62f39412e8c6bfc98582f5e7a49041991c97b)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4296296
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>

[modify] https://crrev.com/6da1a8953313032d2c19bcf83876700d818a0ccb/src/tests/gl_tests/ClearTest.cpp
[modify] https://crrev.com/6da1a8953313032d2c19bcf83876700d818a0ccb/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
[modify] https://crrev.com/6da1a8953313032d2c19bcf83876700d818a0ccb/src/libANGLE/renderer/vulkan/ContextVk.cpp


### gi...@appspot.gserviceaccount.com (2023-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cd45d155bf4cf7404061f37e974a048914ca4610

commit cd45d155bf4cf7404061f37e974a048914ca4610
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Fri Feb 17 04:16:46 2023

M111: Vulkan: Don't close render pass if rebind to same fbo

In the Vulkan backend, the render pass can occasionally (and
transiently) be in a state of "open but inactive".  This is when the
render pass is closed, but has the potential for future modifications
(for example to add a resolve attachment).  Under many circumstances, it
is expected that an open render pass cannot be in such a state.

This assumption can be broken in this scenario:

- Open render pass, draw, etc
- Change framebuffer binding
- Change framebuffer binding back to original
- Masked Clear

When ContextVk is synced before clear, it sees that the framebuffer
binding is changed (though it hasn't really), and it closes the render
passes and sets the render pass dirty bit.  If a draw were to follow, a
new render pass would have started (unnecessarily).  However, in the
case of a masked clear, UtilsVk notices that the render pass is started,
assumes it must be active, and continues recording to it.  While the
operation itself succeeds, the assumption that the render pass is active
is false (and fails assertion).

This change makes sure that framebuffer binding change is no-oped if the
framebuffer is the same one that has opened the current render pass.  If
any application does unnecessary binding changes and back, it will be
optimized by this change as well.

Bug: chromium:1411210
Change-Id: I37a3a9f2eaa1a81a1b3393840b9458ec71a87377
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4261215
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 05e62f39412e8c6bfc98582f5e7a49041991c97b)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4296297
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/cd45d155bf4cf7404061f37e974a048914ca4610/src/tests/gl_tests/ClearTest.cpp
[modify] https://crrev.com/cd45d155bf4cf7404061f37e974a048914ca4610/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
[modify] https://crrev.com/cd45d155bf4cf7404061f37e974a048914ca4610/src/libANGLE/renderer/vulkan/ContextVk.cpp


### gi...@appspot.gserviceaccount.com (2023-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/6da1a8953313032d2c19bcf83876700d818a0ccb

commit 6da1a8953313032d2c19bcf83876700d818a0ccb
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Fri Feb 17 04:16:46 2023

M110: Vulkan: Don't close render pass if rebind to same fbo

In the Vulkan backend, the render pass can occasionally (and
transiently) be in a state of "open but inactive".  This is when the
render pass is closed, but has the potential for future modifications
(for example to add a resolve attachment).  Under many circumstances, it
is expected that an open render pass cannot be in such a state.

This assumption can be broken in this scenario:

- Open render pass, draw, etc
- Change framebuffer binding
- Change framebuffer binding back to original
- Masked Clear

When ContextVk is synced before clear, it sees that the framebuffer
binding is changed (though it hasn't really), and it closes the render
passes and sets the render pass dirty bit.  If a draw were to follow, a
new render pass would have started (unnecessarily).  However, in the
case of a masked clear, UtilsVk notices that the render pass is started,
assumes it must be active, and continues recording to it.  While the
operation itself succeeds, the assumption that the render pass is active
is false (and fails assertion).

This change makes sure that framebuffer binding change is no-oped if the
framebuffer is the same one that has opened the current render pass.  If
any application does unnecessary binding changes and back, it will be
optimized by this change as well.

Bug: chromium:1411210
Change-Id: I37a3a9f2eaa1a81a1b3393840b9458ec71a87377
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4261215
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 05e62f39412e8c6bfc98582f5e7a49041991c97b)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4296296
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>

[modify] https://crrev.com/6da1a8953313032d2c19bcf83876700d818a0ccb/src/tests/gl_tests/ClearTest.cpp
[modify] https://crrev.com/6da1a8953313032d2c19bcf83876700d818a0ccb/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
[modify] https://crrev.com/6da1a8953313032d2c19bcf83876700d818a0ccb/src/libANGLE/renderer/vulkan/ContextVk.cpp


### [Deleted User] (2023-02-28)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-03-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/8b9f8a92f6c0e089aa36ecbcd3d2ef04647e3779

commit 8b9f8a92f6c0e089aa36ecbcd3d2ef04647e3779
Author: Geoff Lang <geofflang@chromium.org>
Date: Wed Mar 01 18:48:44 2023

Revert "M110: Vulkan: Don't close render pass if rebind to same fbo"

This reverts commit 6da1a8953313032d2c19bcf83876700d818a0ccb.

Reason for revert: Breaks build on M110 branch.

Original change's description:
> M110: Vulkan: Don't close render pass if rebind to same fbo
>
> In the Vulkan backend, the render pass can occasionally (and
> transiently) be in a state of "open but inactive".  This is when the
> render pass is closed, but has the potential for future modifications
> (for example to add a resolve attachment).  Under many circumstances, it
> is expected that an open render pass cannot be in such a state.
>
> This assumption can be broken in this scenario:
>
> - Open render pass, draw, etc
> - Change framebuffer binding
> - Change framebuffer binding back to original
> - Masked Clear
>
> When ContextVk is synced before clear, it sees that the framebuffer
> binding is changed (though it hasn't really), and it closes the render
> passes and sets the render pass dirty bit.  If a draw were to follow, a
> new render pass would have started (unnecessarily).  However, in the
> case of a masked clear, UtilsVk notices that the render pass is started,
> assumes it must be active, and continues recording to it.  While the
> operation itself succeeds, the assumption that the render pass is active
> is false (and fails assertion).
>
> This change makes sure that framebuffer binding change is no-oped if the
> framebuffer is the same one that has opened the current render pass.  If
> any application does unnecessary binding changes and back, it will be
> optimized by this change as well.
>
> Bug: chromium:1411210
> Change-Id: I37a3a9f2eaa1a81a1b3393840b9458ec71a87377
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4261215
> Reviewed-by: Charlie Lao <cclao@google.com>
> Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
> (cherry picked from commit 05e62f39412e8c6bfc98582f5e7a49041991c97b)
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4296296
> Commit-Queue: Geoff Lang <geofflang@chromium.org>
> Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
> Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>

Bug: chromium:1411210
Change-Id: I9e72e29f76d25261b460d9a38235537e765407ea
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4299831
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/8b9f8a92f6c0e089aa36ecbcd3d2ef04647e3779/src/tests/gl_tests/ClearTest.cpp
[modify] https://crrev.com/8b9f8a92f6c0e089aa36ecbcd3d2ef04647e3779/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
[modify] https://crrev.com/8b9f8a92f6c0e089aa36ecbcd3d2ef04647e3779/src/libANGLE/renderer/vulkan/ContextVk.cpp


### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations Jaehun! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### rz...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-03-17)

1. Just https://crrev.com/c/4303738
2. Low, only a couple of simple conflicts
3. 110, 111
4. Yes

### gm...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/55e2b6daba9d6b10cb2ff97afcf08cece0a43754

commit 55e2b6daba9d6b10cb2ff97afcf08cece0a43754
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Fri Feb 17 04:16:46 2023

[M108-LTS] Vulkan: Don't close render pass if rebind to same fbo

M108 merge issues:
  src/libANGLE/renderer/vulkan/ContextVk.cpp:
    - hasActiveRenderPass named hasStartedRenderPass in 108
    - getLastRenderPassQueueSerial named getLastRenderPassSerial in 108

In the Vulkan backend, the render pass can occasionally (and
transiently) be in a state of "open but inactive".  This is when the
render pass is closed, but has the potential for future modifications
(for example to add a resolve attachment).  Under many circumstances, it
is expected that an open render pass cannot be in such a state.

This assumption can be broken in this scenario:

- Open render pass, draw, etc
- Change framebuffer binding
- Change framebuffer binding back to original
- Masked Clear

When ContextVk is synced before clear, it sees that the framebuffer
binding is changed (though it hasn't really), and it closes the render
passes and sets the render pass dirty bit.  If a draw were to follow, a
new render pass would have started (unnecessarily).  However, in the
case of a masked clear, UtilsVk notices that the render pass is started,
assumes it must be active, and continues recording to it.  While the
operation itself succeeds, the assumption that the render pass is active
is false (and fails assertion).

This change makes sure that framebuffer binding change is no-oped if the
framebuffer is the same one that has opened the current render pass.  If
any application does unnecessary binding changes and back, it will be
optimized by this change as well.

Bug: chromium:1411210
Change-Id: I37a3a9f2eaa1a81a1b3393840b9458ec71a87377
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4261215
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 05e62f39412e8c6bfc98582f5e7a49041991c97b)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4303738
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/55e2b6daba9d6b10cb2ff97afcf08cece0a43754/src/tests/gl_tests/ClearTest.cpp
[modify] https://crrev.com/55e2b6daba9d6b10cb2ff97afcf08cece0a43754/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
[modify] https://crrev.com/55e2b6daba9d6b10cb2ff97afcf08cece0a43754/src/libANGLE/renderer/vulkan/ContextVk.cpp


### rz...@google.com (2023-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-06)

Hello n3sk, we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted comments #5 and #6 with containing this information. Please refrain from deleting comments with this type of data in the future. Thank you! 

### is...@google.com (2023-07-06)

This issue was migrated from crbug.com/chromium/1411210?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062832)*
