# Security: [swiftshader] heap-use-after-free on vk::Query::start (another)

| Field | Value |
|-------|-------|
| **Issue ID** | [40064253](https://issues.chromium.org/issues/40064253) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Windows |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-04-27 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

=================================================================  

==1660==ERROR: AddressSanitizer: heap-use-after-free on address 0x117014efa8e0 at pc 0x7ffcea2a610f bp 0x0001143fef50 sp 0x0001143fef98  

WRITE of size 4 at 0x117014efa8e0 thread T26  

==1660==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffcea2a610e in vk::Query::start C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueryPool.cpp:43  

#1 0x7ffcea381d54 in sw::DrawCall::run C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Device\Renderer.cpp:555  

#2 0x7ffcea37f5fc in sw::Renderer::draw C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Device\Renderer.cpp:491  

#3 0x7ffcea254224 in `anonymous namespace'::CmdDrawBase::draw C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:957 #4 0x7ffcea253c35 in` anonymous namespace'::CmdDraw::execute C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:985  

#5 0x7ffcea24de8e in vk::CommandBuffer::submit C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:2330  

#6 0x7ffcea2a8780 in vk::Queue::submitQueue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:104  

#7 0x7ffcea2a75f9 in vk::Queue::taskLoop C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:156  

#8 0x7ffcea2aa41d in std::Cr::\_\_thread\_proxy<std::Cr::tuple<std::Cr::unique\_ptr<std::Cr::\_\_thread\_struct,std::Cr::default\_delete[std::Cr::\_\_thread\_struct](javascript:void(0);) >,void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*> > C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:349  

#9 0x7ffceac9bc51 in thread\_start<unsigned int (\_\_cdecl\*)(void \*),1> C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:97  

#10 0x7ff66a085133 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#11 0x7ffd44677603 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017603)  

#12 0x7ffd448e26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x117014efa8e0 is located 96 bytes inside of 3096-byte region [0x117014efa880,0x117014efb498)  

freed by thread T21 here:  

#0 0x7ff66a08e3ad in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffcea2c4fe0 in vkDestroyQueryPool C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1843  

#2 0x7ffceeca78cb in rx::vk::DynamicQueryPool::destroyPoolImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:4013  

#3 0x7ffceeca7847 in rx::vk::DynamicallyGrowingPool[rx::vk::QueryPool](javascript:void(0);)::destroyEntryPool C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3910  

#4 0x7ffceea95fa2 in rx::ContextVk::onDestroy C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1197  

#5 0x7ffceedbf036 in gl::Context::onDestroy C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:874  

#6 0x7ffceee4603e in egl::Display::releaseContextImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:1772  

#7 0x7ffceee4e821 in egl::Display::makeCurrent C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:1629  

#8 0x7ffceee4f4fe in egl::Display::destroyContext C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:1814  

#9 0x7ffceea10690 in egl::DestroyContext C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\egl\_stubs.cpp:292  

#10 0x7ffceea1838f in EGL\_DestroyContext C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_egl\_autogen.cpp:217  

#11 0x7ffcb41214d7 in gl::GLContextEGL::Destroy C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_context\_egl.cc:396  

#12 0x7ffcb412325c in gl::GLContextEGL::~GLContextEGL C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_context\_egl.cc:577  

#13 0x7ffcb41232e3 in gl::GLContextEGL::~GLContextEGL C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_context\_egl.cc:576  

#14 0x7ffcb411554c in scoped\_refptr[gl::GLContext](javascript:void(0);)::reset C:\b\s\w\ir\cache\builder\src\base\memory\scoped\_refptr.h:310  

#15 0x7ffcbf28e734 in gpu::gles2::GLES2DecoderPassthroughImpl::Destroy C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:1519  

#16 0x7ffcb19043e0 in gpu::CommandBufferStub::Destroy C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:363  

#17 0x7ffcb190357e in gpu::CommandBufferStub::~CommandBufferStub C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:135  

#18 0x7ffcb83c7931 in gpu::GLES2CommandBufferStub::~GLES2CommandBufferStub C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gles2\_command\_buffer\_stub.cc:77  

#19 0x7ffcb49e8452 in gpu::GpuChannel::DestroyCommandBuffer C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:969  

#20 0x7ffcb49f6044 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(int),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#21 0x7ffcb30b9b00 in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post\_task\_and\_reply\_impl.cc:106  

#22 0x7ffcb30ba6c3 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#23 0x7ffcafb52b76 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#24 0x7ffcb30e5992 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#25 0x7ffcb30e470f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#26 0x7ffcafa900d0 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:212  

#27 0x7ffcafa8db56 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78

previously allocated by thread T21 here:  

#0 0x7ff66a08e4ad in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffcea6186da in sw::allocateZeroOrPoison C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\System\Memory.cpp:110  

#2 0x7ffcea2c4f23 in vk::ObjectBase<vk::QueryPool,VkNonDispatchableHandle<VkQueryPool\_T \*> >::Create<VkQueryPoolCreateInfo> C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:92  

#3 0x7ffcea2c4dfa in vkCreateQueryPool C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1835  

#4 0x7ffceeca8250 in rx::vk::DynamicQueryPool::allocatePoolImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:4047  

#5 0x7ffceeca7d95 in rx::vk::DynamicallyGrowingPool[rx::vk::QueryPool](javascript:void(0);)::allocatePoolEntries C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3971  

#6 0x7ffceeca7a23 in rx::vk::DynamicQueryPool::allocateQuery C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:4024  

#7 0x7ffceeb2116b in rx::QueryVk::setupBegin C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\QueryVk.cpp:296  

#8 0x7ffceeb213d9 in rx::QueryVk::begin C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\QueryVk.cpp:324  

#9 0x7ffceedcc527 in gl::Context::beginQuery C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:1483  

#10 0x7ffcc1fcc9f6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBeginQueryEXT C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:3803  

#11 0x7ffcc20072e2 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleBeginQueryEXT C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_handlers.cc:1445  

#12 0x7ffcbf286a75 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:974  

#13 0x7ffcbf285ee0 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:912  

#14 0x7ffcb49fc9ed in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:232  

#15 0x7ffcb190620a in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:518  

#16 0x7ffcb1904f78 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:154  

#17 0x7ffcb49e477d in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:714  

#18 0x7ffcb49f3268 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#19 0x7ffcb43d1510 in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler\_dfs.cc:763  

#20 0x7ffcb43cf609 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler\_dfs.cc:674  

#21 0x7ffcb43d7ed9 in base::internal::Invoker<base::internal::BindState<void (gpu::SchedulerDfs::\*)(),base::internal::UnretainedWrapper[gpu::SchedulerDfs,base::unretained\_traits::MayNotDangle,0](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#22 0x7ffcafb52b76 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#23 0x7ffcb30e5992 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#24 0x7ffcb30e470f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#25 0x7ffcafa900d0 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:212  

#26 0x7ffcafa8db56 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#27 0x7ffcb30e8047 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:651

Thread T26 created by T21 here:  

#0 0x7ff66a083c12 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffceac9bb1d in \_beginthreadex C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:209  

#2 0x7ffcea86f1b9 in std::Cr::\_\_libcpp\_thread\_create C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\src\support\win32\thread\_win32.cpp:203  

#3 0x7ffcea2a7902 in std::Cr::thread::thread<void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*&,void> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:365  

#4 0x7ffcea2a7336 in vk::Queue::Queue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:38  

#5 0x7ffcea25f66b in vk::Device::Device C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDevice.cpp:139  

#6 0x7ffcea2c0684 in vk::DispatchableObject<vk::Device,VkDevice\_T \*>::Create<VkDeviceCreateInfo,vk::PhysicalDevice \*,const VkPhysicalDeviceFeatures \*,std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);) > C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:147  

#7 0x7ffcea2bfffe in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1183  

#8 0x7ffd0baa90ea in terminator\_CreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:6095  

#9 0x7ffd0baac24a in loader\_create\_device\_chain C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5243  

#10 0x7ffd0baaab27 in loader\_layer\_create\_device C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4618  

#11 0x7ffd0bab9c84 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\trampoline.c:863  

#12 0x7ffceeb5436d in rx::RendererVk::initializeDevice C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:3229  

#13 0x7ffceeb505a5 in rx::RendererVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:1830  

#14 0x7ffceead0cbc in rx::DisplayVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\DisplayVk.cpp:111  

#15 0x7ffceecfcbe4 in rx::DisplayVkWin32::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\win32\DisplayVkWin32.cpp:62  

#16 0x7ffceee4262d in egl::Display::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:1019  

#17 0x7ffceea11b02 in egl::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\egl\_stubs.cpp:463  

#18 0x7ffceea197ba in EGL\_Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_egl\_autogen.cpp:402  

#19 0x7ffcb0eeadf9 in gl::GLDisplayEGL::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:787  

#20 0x7ffcb0ee9277 in gl::GLDisplayEGL::Initialize C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:673  

#21 0x7ffcb7e1eb39 in gl::init::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_display\_initializer.cc:255  

#22 0x7ffcb41ba671 in gl::init::InitializeGLOneOffPlatform C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_initializer\_win.cc:133  

#23 0x7ffcb0eff005 in gl::init::InitializeGLOneOffPlatformImplementation C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:211  

#24 0x7ffcb0efe848 in gl::init::`anonymous namespace'::InitializeGLOneOffPlatformHelper C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_factory.cc:135 #25 0x7ffcb0efebaa in gl::init::InitializeGLNoExtensionsOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_factory.cc:166 #26 0x7ffcb190174c in gpu::GpuInit::InitializeInProcess C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_init.cc:866 #27 0x7ffcb274f21b in content::InProcessGpuThread::Init C:\b\s\w\ir\cache\builder\src\content\gpu\in_process_gpu_thread.cc:63 #28 0x7ffcafb198ed in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:403 #29 0x7ffcafa6c421 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:133  

#30 0x7ff66a085133 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#31 0x7ffd44677603 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017603)  

#32 0x7ffd448e26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

Thread T21 created by T0 here:  

#0 0x7ff66a083c12 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffcafa6b1ff in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:198  

#2 0x7ffcafb18771 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:215  

#3 0x7ffcaa32acb8 in content::GpuProcessHost::Init C:\b\s\w\ir\cache\builder\src\content\browser\gpu\gpu\_process\_host.cc:890  

#4 0x7ffcaa329d55 in content::GpuProcessHost::Get C:\b\s\w\ir\cache\builder\src\content\browser\gpu\gpu\_process\_host.cc:585  

#5 0x7ffcab64f851 in content::VizProcessTransportFactory::ConnectHostFrameSinkManager C:\b\s\w\ir\cache\builder\src\content\browser\compositor\viz\_process\_transport\_factory.cc:189  

#6 0x7ffca9d08b04 in content::BrowserMainLoop::PostCreateThreadsImpl C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1327  

#7 0x7ffca9d07960 in content::BrowserMainLoop::PostCreateThreads C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:969  

#8 0x7ffca9d0ec6a in base::internal::Invoker<base::internal::BindState<int (content::BrowserMainLoop::\*)(),base::internal::UnretainedWrapper[content::BrowserMainLoop,base::unretained\_traits::MayNotDangle,0](javascript:void(0);) >,int ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#9 0x7ffcab1951fc in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup\_task\_runner.cc:44  

#10 0x7ffca9d06ca2 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:896  

#11 0x7ffca9d110ea in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:139  

#12 0x7ffca9d02665 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#13 0x7ffcae2fe0bd in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:706  

#14 0x7ffcae301e61 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1276  

#15 0x7ffcae3015d8 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1130  

#16 0x7ffcae2fc379 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#17 0x7ffcae2fceaf in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343  

#18 0x7ffca2461699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:187  

#19 0x7ff669fd6364 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#20 0x7ff669fd2bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#21 0x7ff66a40e9bb in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#22 0x7ffd44677603 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017603)  

#23 0x7ffd448e26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueryPool.cpp:43 in vk::Query::start  

Shadow bytes around the buggy address:  

0x117014efa600: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa  

0x117014efa680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x117014efa700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x117014efa780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x117014efa800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa  

=>0x117014efa880: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd  

0x117014efa900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x117014efa980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x117014efaa00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x117014efaa80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x117014efab00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==1660==ADDITIONAL INFO

==1660==Note: Please include this section with the ASan report.  

Task trace:

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==1660==END OF ADDITIONAL INFO  

==1660==ABORTING

**VERSION**  

Chrome Version: [115.0.5737.0] + [DevBuild + ASan]  

Operating System: [Windows]

**REPRODUCTION CASE**  

I am trying to minimize testcase will upload it later.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU Process  

Crash State: See asan.log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 21.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 2.7 KB)

## Timeline

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2023-04-27)

The stack trace and impact at the crash point is similar to https://crbug.com/chromium/1411210

The query is freed by ContextVk::onDestroy and reused by DrawCall::run.

But since query is not allocated from render pass, it seems to be caused by another cause.

### cl...@chromium.org (2023-04-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6230978316664832.

### cl...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### ad...@google.com (2023-04-28)

ClusterFuzz claims this is a duplicate of test case 6519548780675072, but... that's an invalid test case. Curious.

### ad...@google.com (2023-04-28)

I'm going to set some labels on this even though ClusterFuzz is still working on it.

UaF in the GPU process reachable directly from web content: currently regarded as High severity, though we will likely upgrade these to Critical severity imminently now we've started to abandon expectations of properly sandboxing the Android GPU process.
FoundIn: not sure yet, will wait for CF to finish regression task
Component: I'm not sure if the root cause here is Vulkan or Swiftshader but will assume Swiftshader for now

[Monorail components: Internals>GPU>SwiftShader]

### ad...@google.com (2023-05-02)

Regression range 1132683:1132702

### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2fec8ae8e3959f8f0a974db0ab8dd03e33e70357

commit 2fec8ae8e3959f8f0a974db0ab8dd03e33e70357
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue May 02 19:53:29 2023

Vulkan: Handle inactive render pass in draw-based clear

For simplicity, if a render pass is open for the current framebuffer but
is not active, a new one is started in UtilsVk::clearFramebuffer.  A
future optimization could decide to reactive the render pass instead,
but needs to check for whether that's possible (with a condition similar
to what's found in ContextVk::handleDirtyGraphicsRenderPass)

Bug: chromium:1440764
Change-Id: I727d4ecefc2bc0a1a9e399b8851c4cc830d20879
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4499765
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/2fec8ae8e3959f8f0a974db0ab8dd03e33e70357/src/libANGLE/renderer/vulkan/RendererVk.cpp
[modify] https://crrev.com/2fec8ae8e3959f8f0a974db0ab8dd03e33e70357/src/libANGLE/renderer/vulkan/UtilsVk.cpp
[modify] https://crrev.com/2fec8ae8e3959f8f0a974db0ab8dd03e33e70357/src/tests/gl_tests/OcclusionQueriesTest.cpp


### sy...@chromium.org (2023-05-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dc30f7ce84dd6aea1c82f81a211b2bd1a48f7f32

commit dc30f7ce84dd6aea1c82f81a211b2bd1a48f7f32
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu May 04 03:56:35 2023

Roll ANGLE from a88635c4981b to cd171d2ef3ca (25 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/a88635c4981b..cd171d2ef3ca

2023-05-03 abdolrashidi@google.com Vulkan: Enable async pipeline cache compression
2023-05-03 syoussefi@chromium.org WebGL: Limit total size of private data
2023-05-03 i.nazarov@samsung.com Revert "Vulkan: Simplify present history logic"
2023-05-03 syoussefi@chromium.org Vulkan: Handle inactive render pass in draw-based clear
2023-05-03 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll vulkan-deps from 7873f429a5c2 to 94976560d112 (18 revisions)
2023-05-03 i.nazarov@samsung.com Vulkan: Simplify present history logic
2023-05-03 cnorthrop@google.com Vulkan: Suppress new VUID-vkCmdDraw-None VVL errors
2023-05-03 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 4c9976e5d118 to 70803179b4b8 (627 revisions)
2023-05-02 abdolrashidi@google.com Vulkan: Add pending memory size for VMA images
2023-05-02 cnorthrop@google.com Vulkan: Restore stencil write mask workaround for ARM
2023-05-02 lexa.knyazev@gmail.com Vulkan: Implement polygon mode extensions
2023-05-02 cclao@google.com Vulkan: Dirty VertexArray binding bit if buffer storage change
2023-05-02 cclao@google.com Vulkan: Add bit mask vertex array buffer binding point.
2023-05-02 syoussefi@chromium.org Initialize display TLS at thread creation time
2023-05-02 romanl@google.com angle_end2end_tests Pixel 6 shards: 4 -> 8
2023-05-02 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 4b61bdad813f to 7873f429a5c2 (45 revisions)
2023-05-02 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from fe2d690d4674 to 4c9976e5d118 (429 revisions)
2023-05-02 syoussefi@chromium.org Vulkan: Adjust VVL suppression after VU consolidation
2023-05-02 syoussefi@chromium.org Vulkan: Remove DisplayVk param from ToEGL
2023-05-02 syoussefi@chromium.org Vulkan: Use thread-local space for EGL errors
2023-05-01 lexa.knyazev@gmail.com GL: Implement polygon mode extensions
2023-05-01 syoussefi@chromium.org Vulkan: Make eglPrepareSwapBuffersANGLE less special
2023-05-01 lexa.knyazev@gmail.com Add polygon mode extension stubs
2023-05-01 geofflang@chromium.org Metal: Embed precompiled default shaders.
2023-05-01 syoussefi@chromium.org Vulkan: Destroy the surface without holding the EGL lock

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,cnorthrop@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1385510,chromium:1431761,chromium:1440764,chromium:1441754
Tbr: cnorthrop@google.com
Test: Test: angle_trace_tests --gtest_filter="*pokemon_go*"
Test: Test: angle_trace_tests --gtest_filter="*slingshot_test2*"
Change-Id: I983bb70f237a9d51f5872d9d0970dca8295380d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4504035
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1139340}

[modify] https://crrev.com/dc30f7ce84dd6aea1c82f81a211b2bd1a48f7f32/DEPS


### [Deleted User] (2023-05-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-05-04)

ClusterFuzz testcase 6230978316664832 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1139337:1139355

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

Requesting merge to beta M114 because latest trunk commit (1139340) appears to be after beta branch point (1135570).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-06)

Requesting merge to beta M114 because latest trunk commit (1139340) appears to be after beta branch point (1135570).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-05-06)

1. https://chromium-review.googlesource.com/c/angle/angle/+/4499765
2. Change landed on May 4, I don't know the Canary schedule offhand
3. Relying on Canary reports for verification. I don't believe there to be a risk.
4. No
5. No

### [Deleted User] (2023-05-07)

Requesting merge to beta M114 because latest trunk commit (1139340) appears to be after beta branch point (1135570).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-08)

Requesting merge to beta M114 because latest trunk commit (1139340) appears to be after beta branch point (1135570).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-05-08)

M114 merge approved, please merge this fix to branch 5735 at your earliest convenience -- thank you

### gi...@appspot.gserviceaccount.com (2023-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cda96671f9d4225bd62a21f9b6b67dc89628137d

commit cda96671f9d4225bd62a21f9b6b67dc89628137d
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue May 02 19:53:29 2023

M114: Vulkan: Handle inactive render pass in draw-based clear

For simplicity, if a render pass is open for the current framebuffer but
is not active, a new one is started in UtilsVk::clearFramebuffer.  A
future optimization could decide to reactive the render pass instead,
but needs to check for whether that's possible (with a condition similar
to what's found in ContextVk::handleDirtyGraphicsRenderPass)

Bug: chromium:1440764
Change-Id: I727d4ecefc2bc0a1a9e399b8851c4cc830d20879
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4499765
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 2fec8ae8e3959f8f0a974db0ab8dd03e33e70357)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4515272
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/cda96671f9d4225bd62a21f9b6b67dc89628137d/src/libANGLE/renderer/vulkan/RendererVk.cpp
[modify] https://crrev.com/cda96671f9d4225bd62a21f9b6b67dc89628137d/src/libANGLE/renderer/vulkan/UtilsVk.cpp
[modify] https://crrev.com/cda96671f9d4225bd62a21f9b6b67dc89628137d/src/tests/gl_tests/OcclusionQueriesTest.cpp


### am...@google.com (2023-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-12)

Congratulations, n3sk! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1440764?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064253)*
