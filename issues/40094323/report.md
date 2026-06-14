# use-after-free in libANGLE triggered by WebGL2 on Windows 10

| Field | Value |
|-------|-------|
| **Issue ID** | [40094323](https://issues.chromium.org/issues/40094323) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ta...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2019-03-19 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36

Steps to reproduce the problem:
Simply launch the attached PoC with the ASAN build of Chromium on Windows 10 (d3d11 supported).

=================================================================
==7164==ERROR: AddressSanitizer: heap-use-after-free on address 0x1224a614dd18 at pc 0x7ffbf293231d bp 0x00f6e37fae00 sp 0x00f6e37fae48
READ of size 8 at 0x1224a614dd18 thread T0
    #0 0x7ffbf293231c in rx::Buffer11::getBufferStorage<class rx::Buffer11::BufferStorage>(class gl::Context const *,enum rx::BufferUsage,class rx::Buffer11::BufferStorage * *) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:763:10
    #1 0x7ffbf293446b in rx::Buffer11::getBuffer(class gl::Context const *,enum rx::BufferUsage,struct ID3D11Buffer * *) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:651:5
    #2 0x7ffbf28adbb4 in rx::StateManager11::applyVertexBuffers(class gl::Context const *,enum gl::PrimitiveMode,enum gl::DrawElementsType,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\StateManager11.cpp:3010:17
    #3 0x7ffbf28a8338 in rx::StateManager11::syncVertexBuffersAndInputLayout(class gl::Context const *,enum gl::PrimitiveMode,int,int,enum gl::DrawElementsType,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\StateManager11.cpp:2946:5
    #4 0x7ffbf28a639e in rx::StateManager11::updateState(class gl::Context const *,enum gl::PrimitiveMode,int,int,enum gl::DrawElementsType,void const *,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\StateManager11.cpp:2251:17
    #5 0x7ffbf29be83f in rx::Context11::drawArraysInstanced(class gl::Context const *,enum gl::PrimitiveMode,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Context11.cpp:262:5
    #6 0x7ffbf2551148 in gl::Context::drawArraysInstanced(enum gl::PrimitiveMode,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:2184:5
    #7 0x7ffbf2291650 in gl::DrawArraysInstanced(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp:464:22
    #8 0x7ffc0432e9bd in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArraysInstancedANGLE(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:4233:10
    #9 0x7ffc033220c7 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleDrawArraysInstancedANGLE(unsigned int,void const volatile *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers.cc:1753:10
    #10 0x7ffc010099eb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:655:20
    #11 0x7ffc01008de6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:593:12
    #12 0x7ffc00f86e49 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:69:18
    #13 0x7ffbfe58851c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:543:22
    #14 0x7ffbfe587dff in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) C:\b\swarming\w\ir\cache\builder\src\ipc\ipc_message_templates.h:146:7
    #15 0x7ffbfe58515e in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:193:7
    #16 0x7ffbfc11583f in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:566:23
    #17 0x7ffbfc11011a in gpu::GpuChannel::HandleMessage(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:543:3
    #18 0x7ffbfbdcca37 in gpu::Scheduler::RunNextTask(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:529:24
    #19 0x7ffc002f1337 in base::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) C:\b\swarming\w\ir\cache\builder\src\base\task\common\task_annotator.cc:104:33
    #20 0x7ffbfd12cc93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:336:21
    #21 0x7ffbfd12c4da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:217:7
    #22 0x7ffbfd0e73f3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\swarming\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39:55
    #23 0x7ffbfd12e4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:403:12
    #24 0x7ffbfafe59a2 in base::RunLoop::Run(void) C:\b\swarming\w\ir\cache\builder\src\base\run_loop.cc:157:14
    #25 0x7ffbfcee695f in content::GpuMain(struct content::MainFunctionParams const &) C:\b\swarming\w\ir\cache\builder\src\content\gpu\gpu_main.cc:358:14
    #26 0x7ffbfaedcb5a in content::ContentMainRunnerImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:879:10
    #27 0x7ffbfaef284a in service_manager::Main(struct service_manager::MainParams const &) C:\b\swarming\w\ir\cache\builder\src\services\service_manager\embedder\main.cc:416:29
    #28 0x7ffbfaedb414 in content::ContentMain(struct content::ContentMainParams const &) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main.cc:19:10
    #29 0x7ffbf4181327 in ChromeMain C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_main.cc:103:12
    #30 0x7ff69bec7cdd in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) C:\b\swarming\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:202:12
    #31 0x7ff69bec2352 in main C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:229:20
    #32 0x7ff69c238927 in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #33 0x7ffc66a981f3  (C:\WINDOWS\System32\KERNEL32.DLL+0x1800181f3)
    #34 0x7ffc6715a250  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006a250)

0x1224a614dd18 is located 216 bytes inside of 400-byte region [0x1224a614dc40,0x1224a614ddd0)
freed by thread T0 here:
    #0 0x7ff69bf04310 in free C:\b\rr\tmpapv6or\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:52
    #1 0x7ffbf293b967 in rx::Buffer11::`scalar deleting destructor'(unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:329:1
    #2 0x7ffbf272c9a2 in gl::Buffer::~Buffer(void) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Buffer.cpp:51:5
    #3 0x7ffbf272d89b in gl::Buffer::`scalar deleting destructor'(unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Buffer.cpp:50:1
    #4 0x7ffbf25ce709 in gl::TypedResourceManager<class gl::Buffer,class gl::HandleAllocator,class gl::BufferManager>::deleteObject(class gl::Context const *,unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.cpp:96:9
    #5 0x7ffbf256965f in gl::Context::deleteBuffers(int,unsigned int const *) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:5471:9
    #6 0x7ffc04308a71 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDeleteBuffers(int,unsigned int const volatile *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:930:10
    #7 0x7ffc010099eb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:655:20
    #8 0x7ffc01008de6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:593:12
    #9 0x7ffc00f86e49 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:69:18
    #10 0x7ffbfe58851c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:543:22
    #11 0x7ffbfe587dff in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) C:\b\swarming\w\ir\cache\builder\src\ipc\ipc_message_templates.h:146:7
    #12 0x7ffbfe58515e in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:193:7
    #13 0x7ffbfc11583f in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:566:23
    #14 0x7ffbfc11011a in gpu::GpuChannel::HandleMessage(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:543:3
    #15 0x7ffbfbdcca37 in gpu::Scheduler::RunNextTask(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:529:24
    #16 0x7ffc002f1337 in base::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) C:\b\swarming\w\ir\cache\builder\src\base\task\common\task_annotator.cc:104:33
    #17 0x7ffbfd12cc93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:336:21
    #18 0x7ffbfd12c4da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:217:7
    #19 0x7ffbfd0e73f3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\swarming\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39:55
    #20 0x7ffbfd12e4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:403:12
    #21 0x7ffbfafe59a2 in base::RunLoop::Run(void) C:\b\swarming\w\ir\cache\builder\src\base\run_loop.cc:157:14
    #22 0x7ffbfcee695f in content::GpuMain(struct content::MainFunctionParams const &) C:\b\swarming\w\ir\cache\builder\src\content\gpu\gpu_main.cc:358:14
    #23 0x7ffbfaedcb5a in content::ContentMainRunnerImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:879:10
    #24 0x7ffbfaef284a in service_manager::Main(struct service_manager::MainParams const &) C:\b\swarming\w\ir\cache\builder\src\services\service_manager\embedder\main.cc:416:29
    #25 0x7ffbfaedb414 in content::ContentMain(struct content::ContentMainParams const &) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main.cc:19:10
    #26 0x7ffbf4181327 in ChromeMain C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_main.cc:103:12
    #27 0x7ff69bec7cdd in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) C:\b\swarming\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:202:12
    #28 0x7ff69bec2352 in main C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:229:20
    #29 0x7ff69c238927 in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288

previously allocated by thread T0 here:
    #0 0x7ff69bf043f0 in malloc C:\b\rr\tmpapv6or\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:68
    #1 0x7ffbf2e8e38e in operator new(unsigned __int64) d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffbf29be463 in rx::Context11::createBuffer(class gl::BufferState const &) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Context11.cpp:189:24
    #3 0x7ffbf272c771 in gl::Buffer::Buffer(class rx::GLImplFactory *,unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Buffer.cpp:43:22
    #4 0x7ffbf25c5f2b in gl::BufferManager::AllocateNewObject(class rx::GLImplFactory *,unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.cpp:115:26
    #5 0x7ffbf228e045 in ??$checkObjectAllocationImpl@$$V@?$TypedResourceManager@VBuffer@gl@@VHandleAllocator@2@VBufferManager@2@@gl@@AEAAPEAVBuffer@1@PEAVGLImplFactory@rx@@I@Z C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.h:106:32
    #6 0x7ffbf2283f58 in gl::BindBuffer(unsigned int,unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:78:22
    #7 0x7ffc043037aa in gpu::gles2::GLES2DecoderPassthroughImpl::DoBindBuffer(unsigned int,unsigned int) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:378:10
    #8 0x7ffc010099eb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:655:20
    #9 0x7ffc01008de6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:593:12
    #10 0x7ffc00f86e49 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:69:18
    #11 0x7ffbfe58851c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:543:22
    #12 0x7ffbfe587dff in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) C:\b\swarming\w\ir\cache\builder\src\ipc\ipc_message_templates.h:146:7
    #13 0x7ffbfe58515e in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:193:7
    #14 0x7ffbfc11583f in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:566:23
    #15 0x7ffbfc11011a in gpu::GpuChannel::HandleMessage(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:543:3
    #16 0x7ffbfbdcca37 in gpu::Scheduler::RunNextTask(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:529:24
    #17 0x7ffc002f1337 in base::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) C:\b\swarming\w\ir\cache\builder\src\base\task\common\task_annotator.cc:104:33
    #18 0x7ffbfd12cc93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:336:21
    #19 0x7ffbfd12c4da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:217:7
    #20 0x7ffbfd0e73f3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\swarming\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39:55
    #21 0x7ffbfd12e4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:403:12
    #22 0x7ffbfafe59a2 in base::RunLoop::Run(void) C:\b\swarming\w\ir\cache\builder\src\base\run_loop.cc:157:14
    #23 0x7ffbfcee695f in content::GpuMain(struct content::MainFunctionParams const &) C:\b\swarming\w\ir\cache\builder\src\content\gpu\gpu_main.cc:358:14
    #24 0x7ffbfaedcb5a in content::ContentMainRunnerImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:879:10
    #25 0x7ffbfaef284a in service_manager::Main(struct service_manager::MainParams const &) C:\b\swarming\w\ir\cache\builder\src\services\service_manager\embedder\main.cc:416:29
    #26 0x7ffbfaedb414 in content::ContentMain(struct content::ContentMainParams const &) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main.cc:19:10
    #27 0x7ffbf4181327 in ChromeMain C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_main.cc:103:12
    #28 0x7ff69bec7cdd in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) C:\b\swarming\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:202:12
    #29 0x7ff69bec2352 in main C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:229:20

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:763:10 in rx::Buffer11::getBufferStorage<class rx::Buffer11::BufferStorage>(class gl::Context const *,enum rx::BufferUsage,class rx::Buffer11::BufferStorage * *)
Shadow bytes around the buggy address:
  0x04413ad29b50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x04413ad29b60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x04413ad29b70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x04413ad29b80: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x04413ad29b90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x04413ad29ba0: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x04413ad29bb0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x04413ad29bc0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x04413ad29bd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04413ad29be0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04413ad29bf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==7164==ABORTING
[3940:7364:0318/232346.276:ERROR:gles2_cmd_decoder_passthrough_doers.cc(4455)] NOT IMPLEMENTED

OS

What is the expected behavior?
Nothing happens.

What went wrong?
ASAN detects UaF in the GPU process.

By Wen Xu of SSLab, Gatech

Did this work before? N/A 

Chrome version: 74.0.3726.0  Channel: n/a
OS Version: 10.0
Flash Version:

## Attachments

- [final.html](attachments/final.html) (text/plain, 1.3 KB)

## Timeline

### ta...@gmail.com (2019-03-19)

So on Windows, if GPU process crashes even with ASAN errors, the browser will not directly terminate. If I want to see the ASAN log output by the process (launched through a Python script), I manually close the entire browser window to get.

### ta...@gmail.com (2019-03-19)

It seems that in Chrome release, we must specify shader's type in <script>, like

<script id="vshader" type="x-shader/x-vertex">
<script id="fshader" type="x-shader/x-fragment">

### bu...@chromium.org (2019-03-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGL]

### ke...@chromium.org (2019-03-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2019-03-25)

Was able to reproduce. Looking now.

### jm...@chromium.org (2019-04-02)

I fixed this in the following CL but tagged the wrong issue. Listed below.

tarafans7@gmail.com can you verify?

commit f7f15ac20a354f71600b0c11789d54546a924d4c
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Mar 28 01:36:51 2019

Fix deleting a buffer not updating VAO validation.

Deleting a buffer that is bound to a VAO should act as if
the application unbound the buffer. Unbinding the buffer
should update relevant validation caches. But we were
missing the logic that updates the validation caches.

This CL adds the necessary cache updates. It does not include a
regression test. The test was causing an unrelated regression that is
going to be a bit longer. It should not block this fix.

Bug: chromium:943538
Change-Id: Ib073cd07a230ca073a5b14bc054e961158a0097d
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/1536491
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/f7f15ac20a354f71600b0c11789d54546a924d4c/src/libANGLE/State.h
[modify] https://crrev.com/f7f15ac20a354f71600b0c11789d54546a924d4c/src/libANGLE/VertexArray.h
[modify] https://crrev.com/f7f15ac20a354f71600b0c11789d54546a924d4c/src/libANGLE/VertexArray.cpp
[modify] https://crrev.com/f7f15ac20a354f71600b0c11789d54546a924d4c/src/libANGLE/State.cpp
[modify] https://crrev.com/f7f15ac20a354f71600b0c11789d54546a924d4c/src/libANGLE/Context.h

### bu...@chromium.org (2019-04-02)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-74; it appears the fix may have landed after branch point, meaning a merge might be required. The owner of this bug should confirm if a merge is required here. If so, add Merge-Request-74 label and indicate which commits/CLs are to be merged. Otherwise, remove Merge-TBD label. Thanks.

### sh...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-03)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE]

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-04-07)

[Empty comment from Monorail migration]

### ab...@google.com (2019-04-08)

branch:3729

### jm...@chromium.org (2019-04-08)

Merged here:

https://chromium-review.googlesource.com/c/angle/angle/+/1556697

Accidentally tagged with the wrong issue.

### ka...@chromium.org (2019-04-08)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-04-08)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $3,000 for this report. 

A member from our finance team will be in touch shortly. 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### ta...@gmail.com (2019-06-21)

Hi, I wonder if a CVE will be assigned to this issue?

### sh...@chromium.org (2019-07-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-10)

This issue was migrated from crbug.com/chromium/943424?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail blocking: crbug.com/chromium/951451]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094323)*
