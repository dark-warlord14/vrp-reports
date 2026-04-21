# Security: ASan reports wild reads in swiftshader

| Field | Value |
|-------|-------|
| **Issue ID** | [40057770](https://issues.chromium.org/issues/40057770) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU, Internals>GPU>SwiftShader |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ao...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2021-10-29 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports nondeterministically segfaults with high addresses when the attached page is opened.

**VERSION**  

Chrome Version: 934356, prebuilt asan  

Operating System: Linux, Debian 10.11

**REPRODUCTION CASE**  

The attached rather large file can be used to reproduce this issue by opening it in an ASan build and either reloading the page a few times, or by opening at once several copies of it e.g. with $ chrome wild-read-swift.html{,,,,,,,,,,,}.

An alternative way to reproduce this is to change one number from a WebGL conformance test bundled with Chromium. Go to chromium/src/third\_party/webgl/src/sdk/tests/conformance2/extensions, cat ovr\_multiview2\_flat\_varying.html | sed -e 's/0, views/1, views/' > repro.html and open it similarly.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Crash Type: GPU thread?  

Crash State:  

==1123984==ERROR: AddressSanitizer: SEGV on unknown address 0x7f8832943850 (pc 0x7f88356c5983 bp 0x7f8844fb1450 sp 0x7f8844fb1290 T7)  

==1123984==The signal is caused by a READ memory access.  

SCARINESS: 20 (wild-addr-read)  

LLVMSymbolizer: error reading file: No such file or directory  

#0 0x7f88356c5983 (/memfd:swiftshader\_jit (deleted)+0x983)  

#1 0x7f88488c8ac6 in operator() buildtools/third\_party/libc++/trunk/include/functional:2228:16  

#2 0x7f88488c8ac6 in operator() buildtools/third\_party/libc++/trunk/include/functional:2567:12  

#3 0x7f88488c8ac6 in operator() third\_party/swiftshader/third\_party/marl/include/marl/task.h:97:3  

#4 0x7f88488c8ac6 in marl::Scheduler::Worker::runUntilIdle() third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:707:7  

#5 0x7f88488c6adf in marl::Scheduler::Worker::runUntilShutdown() third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:592:5  

#6 0x7f88488c82f5 in marl::Scheduler::Worker::run() third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:585:3  

#7 0x7f88488d13cb in operator() third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:389:11  

#8 0x7f88488d13cb in \_\_invoke<(lambda at ../../third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:376:44) &> buildtools/third\_party/libc++/trunk/include/type\_traits:3956:1  

#9 0x7f88488d13cb in \_\_call<(lambda at ../../third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:376:44) &> buildtools/third\_party/libc++/trunk/include/\_\_functional\_base:348:9  

#10 0x7f88488d13cb in operator() buildtools/third\_party/libc++/trunk/include/functional:1615:12  

#11 0x7f88488d13cb in void std::\_\_1::\_\_function::\_\_policy\_invoker<void ()>::\_\_call\_impl<std::\_\_1::\_\_function::\_\_default\_alloc\_func<marl::Scheduler::Worker::start()::$*1, void ()> >(std::*  

#12 0x7f88488dc152 in operator() buildtools/third\_party/libc++/trunk/include/functional:2228:16  

#13 0x7f88488dc152 in operator() buildtools/third\_party/libc++/trunk/include/functional:2567:12  

#14 0x7f88488dc152 in operator() third\_party/swiftshader/third\_party/marl/src/thread.cpp:365:11  

#15 0x7f88488dc152 in \_\_invoke<(lambda at ../../third\_party/swiftshader/third\_party/marl/src/thread.cpp:363:67)> buildtools/third\_party/libc++/trunk/include/type\_traits:3956:1  

#16 0x7f88488dc152 in \_\_thread\_execute<std::\_\_1::unique\_ptr<std::\_\_1::\_\_thread\_struct, std::\_\_1::default\_delete[std::\_\_1::\_\_thread\_struct](javascript:void(0);) >, (lambda at ../../third\_party/swiftshader/thir  

#17 0x7f88488dc152 in void\* std::\_\_1::\_\_thread\_proxy<std::\_\_1::tuple<std::\_\_1::unique\_ptr<std::\_\_1::\_\_thread\_struct, std::\_\_1::default\_delete[std::\_\_1::\_\_thread\_struct](javascript:void(0);) >, marl::Thread::I  

#18 0x7f8852bae608 in start\_thread /build/glibc-eX1tMB/glibc-2.31/nptl/pthread\_create.c:477:8

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/memfd:swiftshader\_jit (deleted)+0x983)  

Thread T7 (Thread<05>) created by T0 (chrome) here:  

#0 0x5562ed7dcdec in pthread\_create /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cpp:207:3  

#1 0x7f88488dbf3f in \_\_libcpp\_thread\_create buildtools/third\_party/libc++/trunk/include/\_\_threading\_support:513:10  

#2 0x7f88488dbf3f in std::\_\_1::thread::thread<marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::\_\_1::function<void ()>&&)::'lambda'(), void>(marl::Thread::Impl::Impl(marl::Thread::A  

#3 0x7f88488db817 in marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::\_\_1::function<void ()>&&) third\_party/swiftshader/third\_party/marl/src/thread.cpp:363:60  

#4 0x7f88488db640 in marl::Thread::Thread(marl::Thread::Affinity&&, std::\_\_1::function<void ()>&&) third\_party/swiftshader/third\_party/marl/src/thread.cpp:402:16  

#5 0x7f88488c2dac in marl::Scheduler::Worker::start() third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:376:16  

#6 0x7f88488c3fd7 in marl::Scheduler::Scheduler(marl::Scheduler::Config const&) third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:144:23  

#7 0x7f88488b1073 in \_\_shared\_ptr\_emplace<marl::Scheduler::Config &> buildtools/third\_party/libc++/trunk/include/\_\_memory/shared\_ptr.h:293:37  

#8 0x7f88488b1073 in allocate\_shared<marl::Scheduler, std::\_\_1::allocator[marl::Scheduler](javascript:void(0);), marl::Scheduler::Config &, void> buildtools/third\_party/libc++/trunk/include/\_\_memory/shared\_pt  

#9 0x7f88488b1073 in make\_shared<marl::Scheduler, marl::Scheduler::Config &, void> buildtools/third\_party/libc++/trunk/include/\_\_memory/shared\_ptr.h:1110:12  

#10 0x7f88488b1073 in getOrCreateScheduler third\_party/swiftshader/src/Vulkan/libVulkan.cpp:151:10  

#11 0x7f88488b1073 in vkCreateDevice third\_party/swiftshader/src/Vulkan/libVulkan.cpp:954:19  

#12 0x7f8849c6a1a5 in terminator\_CreateDevice third\_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5801:11  

#13 0x7f8849c64d4b in loader\_create\_device\_chain third\_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5151:15  

#14 0x7f8849c634f5 in loader\_layer\_create\_device third\_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4664:11  

#15 0x7f8849c79a46 in vkCreateDevice third\_party/vulkan-deps/vulkan-loader/src/loader/trampoline.c:789:20  

#16 0x7f884af34d2c in rx::RendererVk::initializeDevice(rx::DisplayVk\*, unsigned int) third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:2113:5  

#17 0x7f884af2d8b6 in rx::RendererVk::initialize(rx::DisplayVk\*, egl::Display\*, char const\*, char const\*) third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:1393:9  

#18 0x7f884aed2a58 in rx::DisplayVk::initialize(egl::Display\*) third\_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:40:39  

#19 0x7f884b0956e9 in rx::DisplayVkXcb::initialize(egl::Display\*) third\_party/angle/src/libANGLE/renderer/vulkan/linux/xcb/DisplayVkXcb.cpp:65:23  

#20 0x7f884a8ee714 in egl::Display::initialize() third\_party/angle/src/libANGLE/Display.cpp:890:36  

#21 0x7f884a7d7349 in egl::Initialize(egl::Thread\*, egl::Display\*, int\*, int\*) third\_party/angle/src/libGLESv2/egl\_stubs.cpp:448:5  

#22 0x7f884a7dd784 in EGL\_Initialize third\_party/angle/src/libGLESv2/entry\_points\_egl\_autogen.cpp:311:12  

#23 0x5562fef3fa70 in gl::GLSurfaceEGL::InitializeDisplay(gl::EGLDisplayPlatform) ui/gl/gl\_surface\_egl.cc:1379:10  

#24 0x5562fef3d592 in gl::GLSurfaceEGL::InitializeOneOff(gl::EGLDisplayPlatform) ui/gl/gl\_surface\_egl.cc:963:3  

#25 0x5562efbd661d in ui::GLOzoneEGL::InitializeGLOneOffPlatform() ui/ozone/common/gl\_ozone\_egl.cc:19:8  

#26 0x5562ff14aa28 in gl::init::InitializeGLOneOffPlatformImplementation(bool, bool, bool) ui/gl/init/gl\_factory.cc:242:22  

#27 0x5562ff14a527 in gl::init::(anonymous namespace)::InitializeGLOneOffPlatformHelper(bool) ui/gl/init/gl\_factory.cc:163:10  

#28 0x5562ff14a7d0 in gl::init::InitializeGLNoExtensionsOneOff(bool) ui/gl/init/gl\_factory.cc:198:10  

#29 0x5563015f7a2e in gpu::GpuInit::InitializeAndStartSandbox(base::CommandLine\*, gpu::GpuPreferences const&) gpu/ipc/service/gpu\_init.cc:405:11  

#30 0x5563077c0a10 in content::GpuMain(content::MainFunctionParams const&) content/gpu/gpu\_main.cc:345:39  

#31 0x5562fa7ad8b4 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:615:14  

#32 0x5562fa7b1911 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:1006:10  

#33 0x5562fa7aaee7 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content/app/content\_main.cc:390:36  

#34 0x5562fa7acb02 in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:418:10  

#35 0x5562ed823c25 in ChromeMain chrome/app/chrome\_main.cc:172:12  

#36 0x7f8850c240b2 in \_\_libc\_start\_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Aki Helin, Solita

## Attachments

- [wild-read-swift.html](attachments/wild-read-swift.html) (text/plain, 118.9 KB)
- [wild-read-swift-2.html](attachments/wild-read-swift-2.html) (text/plain, 119.0 KB)

## Timeline

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-11-02)

This would be a memory bug in the GPU process, which has a sandbox but is a reduced-sandbox. Somewhere between High and Critical. Since Android doesn't have a GPU sandbox, but also doesn't use Swiftshader (right?) I will lean to High.

Not sure if ios uses swiftshader but I don't think so.

[Monorail components: Internals>GPU Internals>GPU>SwiftShader]

### cl...@chromium.org (2021-11-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6266242648047616.

### da...@chromium.org (2021-11-02)

I can reproduce on TOT Linux by doing, with ASAN build:

1. Edit third_party/webgl/src/sdk/tests/conformance2/extensions, cat ovr_multiview2_flat_varying.html to replace '0, views' with '1, views'
2. out_desktop/Release/chrome -d third_party/webgl/src/sdk/tests/conformance2/extensions/ovr_multiview2_flat_varying.html{,,,,,,,,,,,} --disable-gpu-compositing
3. Switch tabs and reload them a bit.
4. Get this:

[1102/100841.745218:WARNING:exception_snapshot_linux.cc(427)] Unhandled signal -1
[2018256:2018256:1102/100841.805279:ERROR:gpu_process_host.cc(967)] GPU process exited unexpectedly: exit_code=512
[1102/100857.029948:WARNING:exception_snapshot_linux.cc(427)] Unhandled signal -1
[2018256:2018256:1102/100857.089366:ERROR:gpu_process_host.cc(967)] GPU process exited unexpectedly: exit_code=512
[1102/100912.318280:WARNING:exception_snapshot_linux.cc(427)] Unhandled signal -1
[2018256:2018256:1102/100912.375194:ERROR:gpu_process_host.cc(967)] GPU process exited unexpectedly: exit_code=512
[2018900:2018900:1102/100912.716228:ERROR:sandbox_linux.cc(376)] InitializeSandbox() called with multiple threads in process gpu-process.
[2018900:2018900:1102/100913.283768:ERROR:gl_utils.cc(318)] [.WebGL-0x61b00000d280]GL Driver Message (OpenGL, Performance, GL_CLOSE_PATH_NV, High): GPU stall due to ReadPixels
[2018900:2018900:1102/100913.374227:ERROR:gl_utils.cc(318)] [.WebGL-0x61b00000d280]GL Driver Message (OpenGL, Performance, GL_CLOSE_PATH_NV, High): GPU stall due to ReadPixels
[2018900:2018900:1102/100913.422983:ERROR:gl_utils.cc(318)] [.WebGL-0x61b00000d280]GL Driver Message (OpenGL, Performance, GL_CLOSE_PATH_NV, High): GPU stall due to ReadPixels
[2018900:2018900:1102/100913.450411:ERROR:gl_utils.cc(318)] [.WebGL-0x61b00000d280]GL Driver Message (OpenGL, Performance, GL_CLOSE_PATH_NV, High): GPU stall due to ReadPixels (this message will no longer repeat)
[2018256:2018272:1102/100916.498802:ERROR:chrome_browser_main_extra_parts_metrics.cc(226)] crbug.com/1216328: Checking Bluetooth availability started. Please report if there is no report that this ends.
[2018256:2018272:1102/100916.498860:ERROR:chrome_browser_main_extra_parts_metrics.cc(229)] crbug.com/1216328: Checking Bluetooth availability ended.
[2018256:2018272:1102/100916.498881:ERROR:chrome_browser_main_extra_parts_metrics.cc(232)] crbug.com/1216328: Checking default browser status started. Please report if there is no report that this ends.
[2018256:2018272:1102/100916.573985:ERROR:chrome_browser_main_extra_parts_metrics.cc(236)] crbug.com/1216328: Checking default browser status ended.
AddressSanitizer: CHECK failed: sanitizer_allocator_secondary.h:199 "((nearest_chunk)) >= ((h->map_beg))" (0x7f9455859000, 0xff0000ffff0000ff) (tid=2018900)
    #0 0x55d826bd95b1 in __asan::CheckUnwind() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:67:3
    #1 0x55d826beac24 in __sanitizer::CheckFailed(char const*, int, char const*, unsigned long long, unsigned long long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:86:5
    #2 0x55d826b54242 in __sanitizer::LargeMmapAllocator<__asan::AsanMapUnmapCallback, __sanitizer::LargeMmapAllocatorPtrArrayDynamic, __sanitizer::LocalAddressSpaceView>::GetBlockBegin(void const*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_allocator_secondary.h:199:5
    #3 0x55d826b53f18 in GetBlockBegin /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_allocator_combined.h:134:23
    #4 0x55d826b53f18 in __asan::QuarantineCallback::Recycle(__asan::AsanChunk*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_allocator.cpp:201:31
    #5 0x55d826b53e5c in __sanitizer::Quarantine<__asan::QuarantineCallback, __asan::AsanChunk>::DoRecycle(__sanitizer::QuarantineCache<__asan::QuarantineCallback>*, __asan::QuarantineCallback) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_quarantine.h:193:12
    #6 0x55d826b539e3 in __sanitizer::Quarantine<__asan::QuarantineCallback, __asan::AsanChunk>::Recycle(unsigned long, __asan::QuarantineCallback) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_quarantine.h:181:5
    #7 0x55d826b55c11 in Put /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_quarantine.h:112:7
    #8 0x55d826b55c11 in __asan::Allocator::QuarantineChunk(__asan::AsanChunk*, void*, __sanitizer::BufferedStackTrace*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_allocator.cpp:666:18
    #9 0x55d826bfed65 in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #10 0x7f947cf1c295 in angle::PackedEnumMap<gl::ShaderType, std::__Cr::vector<unsigned int, std::__Cr::allocator<unsigned int> >, 6ul>::~PackedEnumMap() third_party/angle/src/common/PackedEnums.h:71:7
    #11 0x7f947cf1c295 in rx::ProgramInfo::initProgram(rx::ContextVk*, gl::ShaderType, bool, bool, rx::ShaderInfo const&, rx::ProgramTransformOptions, rx::ShaderInterfaceVariableInfoMap const&) third_party/angle/src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:236:1
    #12 0x7f947cf2ea9f in rx::ProgramVk::initProgram(rx::ContextVk*, gl::ShaderType, bool, rx::ProgramTransformOptions, rx::ProgramInfo*, rx::ShaderInterfaceVariableInfoMap const&) third_party/angle/src/libANGLE/renderer/vulkan/ProgramVk.h:207:13
    #13 0x7f947cf2ea9f in rx::ProgramVk::initGraphicsShaderProgram(rx::ContextVk*, gl::ShaderType, bool, rx::ProgramTransformOptions, rx::ProgramInfo*, rx::ShaderInterfaceVariableInfoMap const&) third_party/angle/src/libANGLE/renderer/vulkan/ProgramVk.h:151:16
    #14 0x7f947cf2ea9f in rx::ProgramExecutableVk::getGraphicsPipeline(rx::ContextVk*, gl::PrimitiveMode, rx::vk::GraphicsPipelineDesc const&, angle::BitSetT<16ul, unsigned long, unsigned long> const&, rx::vk::GraphicsPipelineDesc const**, rx::vk::PipelineHelper**) third_party/angle/src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:866:13
    #15 0x7f947ce6bc70 in rx::ContextVk::handleDirtyGraphicsPipelineDesc(angle::BitSetT<18ul, unsigned long, unsigned long>::Iterator*, angle::BitSetT<18ul, unsigned long, unsigned long>) third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:1386:9
    #16 0x7f947ce8959d in rx::ContextVk::setupDraw(gl::Context const*, gl::PrimitiveMode, int, int, int, gl::DrawElementsType, void const*, angle::BitSetT<18ul, unsigned long, unsigned long>) third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:894:9
    #17 0x7f947ce9c4b5 in rx::ContextVk::drawArrays(gl::Context const*, gl::PrimitiveMode, int, int) third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:2540:9
    #18 0x7f947c03020a in gl::Context::drawArrays(gl::PrimitiveMode, int, int) third_party/angle/src/libANGLE/Context.inl.h:132:5
    #19 0x7f947c03020a in GL_DrawArrays third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1063:22
    #20 0x7f94b84ec169 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1216:10
    #21 0x7f94b84aa425 in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858:20
    #22 0x7f94db006708 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18
    #23 0x7f94b7b9df2f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken> > const&) gpu/ipc/service/command_buffer_stub.cc:500:22
    #24 0x7f94b7b9cab4 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:152:7
    #25 0x7f94b7bbfc1b in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:666:13
    #26 0x7f94b7bcec1e in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:531:12
    #27 0x7f94b7bcec1e in void base::internal::InvokeHelper<true, void>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:731:5
    #28 0x7f94db0214fe in base::OnceCallback<void ()>::Run() && base/callback.h:142:12
    #29 0x7f94db0214fe in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:685:26
    #30 0x7f94ed1a2d6f in base::OnceCallback<void ()>::Run() && base/callback.h:142:12
    #31 0x7f94ed1a2d6f in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #32 0x7f94ed212574 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:357:23
    #33 0x7f94ed211218 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:30
    #34 0x7f94ed213381 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #35 0x7f94ed004c99 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:375:46
    #36 0x7f94ed004c99 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:125:43
    #37 0x7f94908cc85a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5385a)
    #38 0x7f94908ccb07  (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x53b07)
    #39 0x7f94908ccbbe in g_main_context_iteration (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x53bbe)
    #40 0x7f94ed0037cf in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:401:30
    #41 0x7f94ed214175 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:462:12
    #42 0x7f94ed0e88eb in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #43 0x7f94de2ff394 in content::GpuMain(content::MainFunctionParams const&) content/gpu/gpu_main.cc:430:14
    #44 0x7f94e254cc64 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:615:14
    #45 0x7f94e25525eb in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:1006:10
    #46 0x7f94e2549d51 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #47 0x7f94e254bb32 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #48 0x55d826c00cf3 in ChromeMain chrome/app/chrome_main.cc:172:12
    #49 0x7f948fff4e49 in __libc_start_main csu/../csu/libc-start.c:314:16
    #50 0x55d826b50619 in _start (/home/danakj/s/c/src/out_desktop/Release/chrome+0x509f619)

[2018256:2018256:1102/100921.324599:ERROR:gpu_process_host.cc(967)] GPU process exited unexpectedly: exit_code=256


### cl...@chromium.org (2021-11-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4875470824603648.

### da...@chromium.org (2021-11-02)

The first cluster fuzz disables WebGL so ignore that one. The second one should be better. But manual repro is possible.

### da...@chromium.org (2021-11-02)

Does not repro, and the webgl test passes reliably with this change on 95.

M96 (96.0.4664.27) crashes in ASAN immediately, and the WebGL test fails compilatoin.

### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-11-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-02)

Testcase 4875470824603648 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4875470824603648.

### [Deleted User] (2021-11-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ao...@gmail.com (2021-11-02)

This version calls a few instances of runFlatVaryingTest via a timeout. It seems to reproduce this almost every time for me, without need to open several pages or reload. It also seems to trigger an occasional wild write. Tested with Chrome 937236.

### cl...@chromium.org (2021-11-02)

This crash occurs very frequently on linux platform and is likely preventing the fuzzer None from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add the ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### cl...@chromium.org (2021-11-02)

ClusterFuzz testcase 6266242648047616 appears to be flaky, updating reproducibility label.

### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-11-02)

Ok, I reproduced it locally, although with slightly modified steps. Notes:

1) I reproduced the issue using the html file in https://crbug.com/chromium/1264988#c4 (along with the modification). I had to explicitly set SwANGLE in the command line, using:
out/Default/chrome --allow-file-access-from-files --use-gl=angle --use-angle=swiftshader third_party/webgl/src/sdk/tests/conformance2/extensions/ovr_multiview2_flat_varying.html
@danakj: maybe this command line would allow the issue to be reproduced in 95, it is possible '--disable-gpu-compositing' only falls back to SwANGLE on 96.

2) I have also been able to repro the ASAN error mentioned in https://crbug.com/chromium/1264988#c13, although I get the ASAN error inside DrawPixmap (instead of inside SwiftShader):
https://source.chromium.org/chromium/chromium/src/+/main:ui/base/x/x11_util.cc;l=273
@aohelin: maybe it's a different issue?

### su...@chromium.org (2021-11-02)

Actually, both cases might be the same issue. I got a similar stack trace using the other test case too. Not sure why it wasn't showing the SwiftShader side stack trace in the output. Anyway, we'll know once I figure out a proper fix for this.

### su...@chromium.org (2021-11-02)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-11-03)

This validation is missing in ANGLE:

From https://www.khronos.org/registry/OpenGL/extensions/OVR/OVR_multiview.txt

    Add the following to the list of conditions required for framebuffer
    attachment completeness in section 9.4.1 (Framebuffer Attachment
    Completeness):

    "If <image> is a two-dimensional array and the attachment
    is multiview, all the selected layers, [<baseViewIndex>,
    <baseViewIndex> + <numViews>), are less than the layer count of the
    texture."

Delegating to syoussefi@ to add this missing validation.

### sr...@google.com (2021-11-03)

Pls get the fix landed on trunk asap and get it verified, we are cutting stable RC for M96 early next week , so lets get the CL ready for merge before Monday next week.

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/30b01d8fd1cfceffd9403227968f0a62e5d444af

commit 30b01d8fd1cfceffd9403227968f0a62e5d444af
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Nov 03 19:56:47 2021

Fix multiview framebuffer completeness check

In the process of dropping ANGLE_multiview in favor of OVR_multiview,
the framebuffer completeness checks have become stale.  In particular:

- There is no requirement that the base layer of the attachments match
- There _is_ a requirement that base+count layers are within the texture
  boundaries.

Bug: chromium:1264988
Change-Id: I86837b587ad5befaa6a545c5a24507e8dff0b568
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3259272
Reviewed-by: Alexis Hetu <sugoi@google.com>
Reviewed-by: Alexis Hétu <sugoi@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/30b01d8fd1cfceffd9403227968f0a62e5d444af/src/libANGLE/Framebuffer.cpp
[modify] https://crrev.com/30b01d8fd1cfceffd9403227968f0a62e5d444af/src/tests/gl_tests/FramebufferMultiviewTest.cpp


### sy...@chromium.org (2021-11-04)

The above should fix it, but it looks the autoroller has been disabled for a week. I just resumed it and will rerun clusterfuzz once the change rolls.

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7f64f374d50125be6ba80836adf5d96f23d30b37

commit 7f64f374d50125be6ba80836adf5d96f23d30b37
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Nov 04 21:02:50 2021

Roll ANGLE from d2b4d9aec159 to 8c9b8f03e0f3 (35 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/d2b4d9aec159..8c9b8f03e0f3

2021-11-04 timvp@google.com Capture/Replay: Don't finish() destroyed Contexts
2021-11-04 cnorthrop@google.com Skip world_cricket_championship_2 Intel Linux
2021-11-04 cnorthrop@google.com Tests: Skip zillow trace on desktop Vulkan
2021-11-04 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 7a571328541a to e733a26e2ba0 (1 revision)
2021-11-04 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from d388b3abde67 to a46607dbd322 (20 revisions)
2021-11-04 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from b8a060d71358 to ff76252a7394 (1883 revisions)
2021-11-04 syoussefi@chromium.org Fix multiview framebuffer completeness check
2021-11-03 cnorthrop@google.com GLES1: Create multiple shaders based on state
2021-11-03 timvp@google.com Capture/Replay: Skip failing UniformTest tests
2021-11-03 kpiddington@apple.com Metal: Reduce memory usage of attribute re-writing
2021-11-03 abdolrashidi@google.com Env var for EXT_framebuffer_fetch_non_coherent
2021-11-03 yuxinhu@google.com Add World Cricket Championship 2 Trace
2021-11-03 timvp@google.com Vulkan: Don't submit XFB queries when XFB is inactive
2021-11-03 cnorthrop@google.com DEPS: Update Android SDK source to android-31
2021-11-03 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 542593f0e311 to 7a571328541a (2 revisions)
2021-11-02 kpiddington@apple.com Metal: Anonymous unused uniform structs not named.
2021-11-02 gman@chromium.org Metal: Use Depth32F for DEPTH_COMPONENT16
2021-11-02 kpiddington@apple.com Expose translator issues with struct samplers.
2021-11-02 syoussefi@chromium.org Vulkan: Regression test for xfb query before resume
2021-11-02 jmadill@chromium.org Fix out of range access in MemoryBarrierTest.
2021-11-02 timvp@google.com AOSP: Use '-Os' rather than '-Oz'
2021-11-02 senorblanco@chromium.org Implement ANGLE_FALLTHROUGH macro.
2021-11-02 gert.wollny@collabora.com Capture/Replay: Capture name in GetProgramResourceIndex
2021-11-02 gert.wollny@collabora.com Capture/Replay: Add ES3_1_Vulkan_SwiftShader expectations
2021-11-02 jmadill@chromium.org infra: Expose ASAN configs in try.
2021-11-02 gert.wollny@collabora.com Capture/Replay: Mark test to be flaky on Windows
2021-11-02 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 9d8950e082d8 to 542593f0e311 (3 revisions)
2021-11-02 abdolrashidi@google.com Complete validation of glGetAttribLocation()
2021-11-01 yuxinhu@google.com Add detachShader capture calls in MEC
2021-11-01 steven@valvesoftware.com d3d11: fix typo in pixel shader function signatures
2021-11-01 angle-autoroll@skia-public.iam.gserviceaccount.com Roll VK-GL-CTS from 49afd2823061 to 06492d671a2d (6 revisions)
2021-11-01 jmadill@chromium.org infra: Add ANGLE-side configuration for ASAN tests.
2021-11-01 gman@chromium.org Template gl::Rectangle so it can be used for float
2021-11-01 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from a03d00bd2a78 to d388b3abde67 (16 revisions)
2021-10-30 syoussefi@chromium.org Suppress failing test

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
Bug: chromium:1264988,chromium:1264995
Tbr: cnorthrop@google.com
Test: Test: TransformFeedbackTest.TransformFeedbackQueryPausedDrawThenResume
Test: Test: angle_perftests --gtest_filter="*world_cricket_championship_2*"
Test: Test: dEQP.GLES3/functional_transform_feedback*
Change-Id: I0983e835e00c71b474689798a1226f9f657b3d56
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3262423
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#938496}

[modify] https://crrev.com/7f64f374d50125be6ba80836adf5d96f23d30b37/DEPS


### sr...@google.com (2021-11-05)

[Empty comment from Monorail migration]

### sy...@chromium.org (2021-11-06)

[Empty comment from Monorail migration]

### sy...@chromium.org (2021-11-06)

Clusterfuzz confirms that this is ok now:

[2021-11-06 02:45:20 UTC] syoussefi@chromium.org: Redo task(s): progression
[2021-11-06 02:55:11 UTC] clusterfuzz-linux-v6cp: Progression task started: r939048.
[2021-11-06 03:27:40 UTC] clusterfuzz-linux-v6cp: Progression task errored out: Known crash revision 937349 did not crash, will retry on another bot to confirm result.
[2021-11-06 03:27:40 UTC] clusterfuzz-linux-v6cp: Progression task finished.

I presume this needs to merge into M96 and M97?

### [Deleted User] (2021-11-06)

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

### [Deleted User] (2021-11-06)

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

### [Deleted User] (2021-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-07)

[Empty comment from Monorail migration]

### sy...@chromium.org (2021-11-08)

1. Per https://crbug.com/chromium/1264988#c21
2. https://chromium-review.googlesource.com/c/angle/angle/+/3259272
3. Rolled on Nov 4 (See https://crbug.com/chromium/1264988#c24), so should be about 3 days in Canary (though weekend). I haven't seen any reports about this so far.
4. No.
5. N/A
6. No, it fixes validation of an OpenGL API entry, so it strictly affects shaders that issue incorrect code.

### pb...@google.com (2021-11-08)

I see that the change is already part of M97 Branch https://chromiumdash.appspot.com/commit/30b01d8fd1cfceffd9403227968f0a62e5d444af so don't think we need any merges to M97 if true please goahead and drop Merge-Review-97 label.

### sy...@chromium.org (2021-11-08)

Ack, looks like it made the cut at the last minute.

### am...@chromium.org (2021-11-08)

merge approved for M96, as long as there are no stability issues or other concerns, please merge to branch 4664 ASAP/by EOD today, Monday 8 November so this fix can be included in stable cut 

### gi...@appspot.gserviceaccount.com (2021-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2de728d6ea3c18de20ae4d5c67590e472dc9258b

commit 2de728d6ea3c18de20ae4d5c67590e472dc9258b
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Nov 03 19:56:47 2021

M96: Fix multiview framebuffer completeness check

In the process of dropping ANGLE_multiview in favor of OVR_multiview,
the framebuffer completeness checks have become stale.  In particular:

- There is no requirement that the base layer of the attachments match
- There _is_ a requirement that base+count layers are within the texture
  boundaries.

Bug: chromium:1264988
Change-Id: I86837b587ad5befaa6a545c5a24507e8dff0b568
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3259272
Reviewed-by: Alexis Hetu <sugoi@google.com>
Reviewed-by: Alexis Hétu <sugoi@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3271552
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/2de728d6ea3c18de20ae4d5c67590e472dc9258b/src/tests/gl_tests/FramebufferMultiviewTest.cpp
[modify] https://crrev.com/2de728d6ea3c18de20ae4d5c67590e472dc9258b/src/libANGLE/Framebuffer.cpp


### sy...@chromium.org (2021-11-10)

Done. Sorry I missed your comment yesterday, but this should still make it to M96 as I understand.

### am...@chromium.org (2021-11-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-11)

Congratulations, Aki! The VRP Panel has decided to award you $5000 for this report. Excellent work and thank you for this report! 

### [Deleted User] (2021-11-18)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M97, which branched on 2021-11-04 (Chromium branch: 4692, Chromium branch position: 938553)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### sy...@chromium.org (2021-11-19)

Per https://crbug.com/chromium/1264988#c33, the necessary change is already a part of M97.

### [Deleted User] (2022-02-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1264988?no_tracker_redirect=1

[Multiple monorail components: Internals>GPU, Internals>GPU>SwiftShader]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057770)*
