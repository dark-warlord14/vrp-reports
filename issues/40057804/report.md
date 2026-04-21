# Use after free in getSamplerTexture

| Field | Value |
|-------|-------|
| **Issue ID** | [40057804](https://issues.chromium.org/issues/40057804) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | sj...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2021-11-03 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36

Steps to reproduce the problem:
1. open poc.html
2.
3.

What is the expected behavior?

What went wrong?
## Title 
    Use after free in getSamplerTexture

## Test environment
    - Linux Chrome 95.0.4638.69 (Official Build) (64-bit) 
        - Revision hash : 6a1600ed572fedecd573b6c2b90a22fe6392a410
    - Linux Chromium 97.0.4691.0 (Developer Build) (64-bit)
        - Revision hash : d280097004c4553307e15b6f021e0d10aadcc5c6

## Details

I did analysed on 97.0.4691.0 Developer build.

* ./third_party/angle/src/libANGLE/State.h:312
```c++
Texture *getSamplerTexture(unsigned int sampler, TextureType type) const
{
    ASSERT(sampler < mSamplerTextures[type].size());
    return mSamplerTextures[type][sampler].get(); //[1] here, occur to use after free.
}
```

## PoC
- attached as `poc.html`

## Stable crash log
```plaintext
Thread 1 "chrome" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7f89651dee00 (LWP 281853)]
0x00007f8960fd9cfd in ?? () from /opt/google/chrome/libGLESv2.so
(gdb) x/i $pc
=> 0x7f8960fd9cfd:	cmp    0x260(%rbx),%eax
(gdb) reg r rbx
Undefined command: "reg".  Try "help".
(gdb) x/a $rbx
0xffc61aff2dd0ffff:	Cannot access memory at address 0xffc61aff2dd0ffff
(gdb) x/10i $pc
=> 0x7f8960fd9cfd:	cmp    0x260(%rbx),%eax
   0x7f8960fd9d03:	jne    0x7f8960fd9d19
   0x7f8960fd9d05:	mov    0x2a4(%rbx),%ecx
   0x7f8960fd9d0b:	cmp    0x40(%r15),%ecx
   0x7f8960fd9d0f:	jne    0x7f8960fd9d19
   0x7f8960fd9d11:	mov    0x2a8(%rbx),%al
   0x7f8960fd9d17:	jmp    0x7f8960fd9d4a
   0x7f8960fd9d19:	add    $0x10,%r14
   0x7f8960fd9d1d:	mov    %eax,0x260(%rbx)
   0x7f8960fd9d23:	lea    0x264(%rbx),%rdi
(gdb) reg r
Undefined command: "reg".  Try "help".
(gdb) i r
rax            0x8                 8
rbx            0xffc61aff2dd0ffff  -16295865361563649
rcx            0x2fd203dce000      52579054444544
rdx            0x0                 0
rsi            0x2fd20114f800      52579007789056
rdi            0xffc61aff2dd0ffff  -16295865361563649
rbp            0x7fffa8a08170      0x7fffa8a08170
rsp            0x7fffa8a08150      0x7fffa8a08150
r8             0x2fd2026df800      52579030398976
r9             0x0                 0
r10            0x46f30630          1190331952
r11            0x0                 0
r12            0x0                 0
r13            0x2fd20114f800      52579007789056
r14            0x2fd20114f800      52579007789056
r15            0xffc61aff2dd100cb  -16295865361563445
rip            0x7f8960fd9cfd      0x7f8960fd9cfd
eflags         0x10246             [ PF ZF IF RF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
(gdb) p/a $rbx
$1 = 0xffc61aff2dd0ffff
(gdb) 
```

## ASAN log
- attached as `asan.txt`

Did this work before? N/A 

Chrome version: 95.0.4638.69  Channel: stable
OS Version: Ubuntu

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 16.7 KB)
- [more_analysis.md](attachments/more_analysis.md) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2021-11-03)

[Empty comment from Monorail migration]

### sj...@gmail.com (2021-11-03)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-03)

I haven't reproduced this yet but adding component and owners for now.

[Monorail components: Internals>GPU>ANGLE]

### va...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5849286879019008.

### va...@chromium.org (2021-11-03)

Heap-use-after-free READ in the GPU process so assigning Medium severity.

==4070090==ERROR: AddressSanitizer: heap-use-after-free on address 0x6170000b9f88 at pc 0x7f491b09cf48 bp 0x7ffdfed66900 sp 0x7ffdfed668f8
READ of size 8 at 0x6170000b9f88 thread T0 (chrome)
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x7f491b09cf47 in get third_party/angle/src/libANGLE/RefCountObject.h:158:38
    #1 0x7f491b09cf47 in getSamplerTexture third_party/angle/src/libANGLE/State.h:312:48
    #2 0x7f491b09cf47 in gl::Framebuffer::formsRenderingFeedbackLoopWith(gl::Context const*) const third_party/angle/src/libANGLE/Framebuffer.cpp:2147:42
    #3 0x7f491b3134ea in gl::ValidateDrawStates(gl::Context const*) third_party/angle/src/libANGLE/validationES.cpp:4107:30
    #4 0x7f491b051b70 in gl::StateCache::getBasicDrawStatesErrorImpl(gl::Context const*) const third_party/angle/src/libANGLE/Context.cpp:9346:62
    #5 0x7f491af8005d in getBasicDrawStatesError third_party/angle/src/libANGLE/Context.h:185:16
    #6 0x7f491af8005d in ValidateDrawBase third_party/angle/src/libANGLE/validationES.h:430:57
    #7 0x7f491af8005d in ValidateDrawArraysCommon third_party/angle/src/libANGLE/validationES.h:1010:10
    #8 0x7f491af8005d in ValidateDrawArrays third_party/angle/src/libANGLE/validationES2.h:24:12
    #9 0x7f491af8005d in GL_DrawArrays third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1105:29
    #10 0x55b118502129 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1216:10
    #11 0x55b1184d070f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858:20
    #12 0x55b118946755 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18
    #13 0x55b11893a24f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) gpu/ipc/service/command_buffer_stub.cc:500:22
    #14 0x55b1189397f9 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:152:7
    #15 0x55b11894d232 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:666:13
    #16 0x55b118959a7e in Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > base/bind_internal.h:533:12
    #17 0x55b118959a7e in void base::internal::InvokeHelper<true, void>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:728:5
    #18 0x55b117352d37 in Run base/callback.h:142:12
    #19 0x55b117352d37 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:685:26
    #20 0x55b112d3e833 in Run base/callback.h:142:12
    #21 0x55b112d3e833 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:157:32
    #22 0x55b112d7bb03 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:115:5
    #23 0x55b112d7bb03 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #24 0x55b112d7b317 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #25 0x55b112d7c6d1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #26 0x55b112c3566a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #27 0x55b112d7cd9b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #28 0x55b112cb7529 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #29 0x55b11eb85137 in content::GpuMain(content::MainFunctionParams const&) content/gpu/gpu_main.cc:401:14
    #30 0x55b111af48f4 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:615:14
    #31 0x55b111af8951 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:1006:10
    #32 0x55b111af1f27 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #33 0x55b111af3b42 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #34 0x55b104b97c95 in ChromeMain chrome/app/chrome_main.cc:172:12
    #35 0x7f4926aef82f in __libc_start_main /build/glibc-LK5gWL/glibc-2.23/csu/libc-start.c:291
0x6170000b9f88 is located 8 bytes inside of 688-byte region [0x6170000b9f80,0x6170000ba230)
freed by thread T0 (chrome) here:
    #0 0x55b104b95c8d in operator delete(void*) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x7f491b174a4c in release third_party/angle/src/libANGLE/RefCountObject.h:46:13
    #2 0x7f491b174a4c in DeleteObject third_party/angle/src/libANGLE/ResourceManager.cpp:231:14
    #3 0x7f491b174a4c in gl::TypedResourceManager<gl::Texture, gl::TextureManager, gl::TextureID>::deleteObject(gl::Context const*, gl::TextureID) third_party/angle/src/libANGLE/ResourceManager.cpp:96:9
    #4 0x7f491b0345ae in gl::Context::deleteTextures(int, gl::TextureID const*) third_party/angle/src/libANGLE/Context.cpp:6617:13
    #5 0x7f491af7f812 in GL_DeleteTextures third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:945:22
    #6 0x55b118646094 in gpu::gles2::TexturePassthrough::~TexturePassthrough() gpu/command_buffer/service/texture_manager.cc:546:5
    #7 0x55b1184ff886 in DeleteInternal<gpu::gles2::TexturePassthrough> base/memory/ref_counted.h:354:5
    #8 0x55b1184ff886 in Destruct base/memory/ref_counted.h:317:5
    #9 0x55b1184ff886 in Release base/memory/ref_counted.h:343:7
    #10 0x55b1184ff886 in Release base/memory/scoped_refptr.h:321:8
    #11 0x55b1184ff886 in ~scoped_refptr base/memory/scoped_refptr.h:223:7
    #12 0x55b1184ff886 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDeleteTextures(int, unsigned int const volatile*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1136:3
    #13 0x55b1184d070f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858:20
    #14 0x55b118946755 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18
    #15 0x55b11893a24f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) gpu/ipc/service/command_buffer_stub.cc:500:22
    #16 0x55b1189397f9 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:152:7
    #17 0x55b11894d232 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:666:13
    #18 0x55b118959a7e in Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > base/bind_internal.h:533:12
    #19 0x55b118959a7e in void base::internal::InvokeHelper<true, void>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:728:5
    #20 0x55b117352d37 in Run base/callback.h:142:12
    #21 0x55b117352d37 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:685:26
    #22 0x55b112d3e833 in Run base/callback.h:142:12
    #23 0x55b112d3e833 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:157:32
    #24 0x55b112d7bb03 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:115:5
    #25 0x55b112d7bb03 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #26 0x55b112d7b317 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #27 0x55b112d7c6d1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #28 0x55b112c3566a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #29 0x55b112d7cd9b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #30 0x55b112cb7529 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #31 0x55b11eb85137 in content::GpuMain(content::MainFunctionParams const&) content/gpu/gpu_main.cc:401:14
    #32 0x55b111af48f4 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:615:14
    #33 0x55b111af8951 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:1006:10
    #34 0x55b111af1f27 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #35 0x55b111af3b42 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #36 0x55b104b97c95 in ChromeMain chrome/app/chrome_main.cc:172:12
    #37 0x7f4926aef82f in __libc_start_main /build/glibc-LK5gWL/glibc-2.23/csu/libc-start.c:291
previously allocated by thread T0 (chrome) here:
    #0 0x55b104b9542d in operator new(unsigned long) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x7f491b18165d in gl::TextureManager::AllocateNewObject(rx::GLImplFactory*, gl::TextureID, gl::TextureType) third_party/angle/src/libANGLE/ResourceManager.cpp:223:24
    #2 0x7f491b051f9f in gl::Texture* gl::TypedResourceManager<gl::Texture, gl::TextureManager, gl::TextureID>::checkObjectAllocationImpl<gl::TextureType>(rx::GLImplFactory*, gl::TextureID, gl::TextureType) third_party/angle/src/libANGLE/ResourceManager.h:117:32
    #3 0x7f491b003855 in checkObjectAllocation<gl::TextureType> third_party/angle/src/libANGLE/ResourceManager.h:104:16
    #4 0x7f491b003855 in checkTextureAllocation third_party/angle/src/libANGLE/ResourceManager.h:205:16
    #5 0x7f491b003855 in gl::Context::bindTexture(gl::TextureType, gl::TextureID) third_party/angle/src/libANGLE/Context.cpp:1214:37
    #6 0x7f491af7d16e in GL_BindTexture third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:194:22
    #7 0x55b1184f6cce in gpu::gles2::GLES2DecoderPassthroughImpl::DoBindTexture(unsigned int, unsigned int) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:527:10
    #8 0x55b1184d070f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858:20
    #9 0x55b118946755 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18
    #10 0x55b11893a24f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) gpu/ipc/service/command_buffer_stub.cc:500:22
    #11 0x55b1189397f9 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:152:7
    #12 0x55b11894d232 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:666:13
    #13 0x55b118959a7e in Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > base/bind_internal.h:533:12
    #14 0x55b118959a7e in void base::internal::InvokeHelper<true, void>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:728:5
    #15 0x55b117352d37 in Run base/callback.h:142:12
    #16 0x55b117352d37 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:685:26
    #17 0x55b112d3e833 in Run base/callback.h:142:12
    #18 0x55b112d3e833 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:157:32
    #19 0x55b112d7bb03 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:115:5
    #20 0x55b112d7bb03 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #21 0x55b112d7b317 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #22 0x55b112d7c6d1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #23 0x55b112c3566a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #24 0x55b112d7cd9b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #25 0x55b112cb7529 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #26 0x55b11eb85137 in content::GpuMain(content::MainFunctionParams const&) content/gpu/gpu_main.cc:401:14
    #27 0x55b111af48f4 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:615:14
    #28 0x55b111af8951 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:1006:10
    #29 0x55b111af1f27 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #30 0x55b111af3b42 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #31 0x55b104b97c95 in ChromeMain chrome/app/chrome_main.cc:172:12
    #32 0x7f4926aef82f in __libc_start_main /build/glibc-LK5gWL/glibc-2.23/csu/libc-start.c:291
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chromium-browser-asan_linux-release_4392242b7f59878a2775b4607420a2b37e17ff13/revisions/asan-linux-release-938035/libGLESv2.so+0x8f2f47)
Shadow bytes around the buggy address:
  0x0c2e8000f3a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000f3b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000f3c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000f3d0: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8000f3e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c2e8000f3f0: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000f400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000f410: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000f420: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000f430: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000f440: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
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
==4070090==ABORTING

### va...@chromium.org (2021-11-03)

Setting severity to High per ClusterFuzz's recommendation.
Will wait for ClusterFuzz to bisect before setting Impact.

### cl...@chromium.org (2021-11-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-04)

Detailed Report: https://clusterfuzz.com/testcase?key=5849286879019008

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6170000b7588
Crash State:
  gl::Framebuffer::formsRenderingFeedbackLoopWith
  gl::ValidateDrawStates
  gl::StateCache::getBasicDrawStatesErrorImpl
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=800914:800915

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5849286879019008

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5849286879019008 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2021-11-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/019ddad5932eb56b6bc185105de602aed9f45b40

commit 019ddad5932eb56b6bc185105de602aed9f45b40
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Nov 04 17:22:47 2021

Reset cache in ProgramExecutable::updateActiveSamplers.

This missing reset was causing incorrect state validation to
persist in a few instances.

Bug: chromium:1266437
Change-Id: I7ab47c81bf9f855e3ad75048f9d1aaefbc2291df
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3262477
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/019ddad5932eb56b6bc185105de602aed9f45b40/src/libANGLE/ProgramExecutable.cpp
[modify] https://crrev.com/019ddad5932eb56b6bc185105de602aed9f45b40/src/tests/gl_tests/StateChangeTest.cpp


### gi...@appspot.gserviceaccount.com (2021-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e8964308c6f755669b699c1a872f4a3ba87734f6

commit e8964308c6f755669b699c1a872f4a3ba87734f6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Nov 05 18:36:19 2021

Roll ANGLE from fab56bdb6fc7 to 019ddad5932e (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/fab56bdb6fc7..019ddad5932e

2021-11-05 jmadill@chromium.org Reset cache in ProgramExecutable::updateActiveSamplers.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC cnorthrop@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1266437
Tbr: cnorthrop@google.com
Change-Id: If4e5b80e9c228326e745e4e20396a6ecad94b99e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3264157
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#938867}

[modify] https://crrev.com/e8964308c6f755669b699c1a872f4a3ba87734f6/DEPS


### sj...@gmail.com (2021-11-06)

Please fill in the credit with the following information. Thank you.


Jeonghoon Shin(@singi21a) of Theori 


### cl...@chromium.org (2021-11-06)

ClusterFuzz testcase 5849286879019008 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=938865:938875

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-07)

Requesting merge to dev M97 because latest trunk commit (938867) appears to be after dev branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-07)

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

### jm...@chromium.org (2021-11-08)

1. use-after-free
2. https://chromium-review.googlesource.com/c/angle/angle/+/3262477
3. yes
4. no

### pb...@google.com (2021-11-08)

Approving the change to M96 Branch 4692, please goahead and get the change merged asap

### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/5805aa96af940456c564ce72d5ee92b94dfe70be

commit 5805aa96af940456c564ce72d5ee92b94dfe70be
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Nov 04 17:22:47 2021

Reset cache in ProgramExecutable::updateActiveSamplers.

This missing reset was causing incorrect state validation to
persist in a few instances.

Bug: chromium:1266437
Change-Id: I7ab47c81bf9f855e3ad75048f9d1aaefbc2291df
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3262477
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 019ddad5932eb56b6bc185105de602aed9f45b40)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3265531
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/5805aa96af940456c564ce72d5ee92b94dfe70be/src/libANGLE/ProgramExecutable.cpp
[modify] https://crrev.com/5805aa96af940456c564ce72d5ee92b94dfe70be/src/tests/gl_tests/StateChangeTest.cpp


### am...@google.com (2021-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-11)

Congratulations, the VRP Panel has decided to award you $5000 for this report! Nice work!!

### sj...@gmail.com (2021-11-11)

Thanks!!

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1266437?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1277572]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057804)*
