# Security:  access-violation on unknown address 0x12dfa490bbaa in dawn::native::TextureBase::TextureBase(browser process) 

| Field | Value |
|-------|-------|
| **Issue ID** | [40060520](https://issues.chromium.org/issues/40060520) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Dawn, Internals>Skia>Compositing |
| **Platforms** | Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2022-08-06 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

access-violation on unknown address 0x12dfa490bbaa in dawn::native::TextureBase::TextureBase

**VERSION**  

Chromium 106.0.5223.0 (Developer Build) (64-bit)  

Revision 150265d5721034653c4be83721c4c266e6071175-refs/heads/main@{#1032249}  

OS Windows 10 Version 21H2 (Build 19044.1826)

**REPRODUCTION CASE**

1. Download the latest asan build: asan-win32-release\_x64-1032249
2. Run the command :  
   
   chrome --user-data-dir=C:/tmp/any --no-sandbox --enable-features=SkiaDawn --enable-low-end-device-mode --in-process-gpu <https://www.google.com>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser]  

Crash State:

=================================================================  

==14972==ERROR: AddressSanitizer: access-violation on unknown address 0x12dfa490bbaa (pc 0x7ff905f25f9f bp 0x00c60bffe4a0 sp 0x00c60bffe420 T22)  

==14972==The signal is caused by a READ memory access.  

==14972==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff905f25f9e in dawn::native::TextureBase::TextureBase C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\Texture.cpp:538  

#1 0x7ff905fcc5ae in dawn::native::d3d12::Texture::Texture C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\d3d12\TextureD3D12.cpp:648  

#2 0x7ff905fcc305 in dawn::native::d3d12::Texture::Create C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\d3d12\TextureD3D12.cpp:499  

#3 0x7ff905f6da9f in dawn::native::d3d12::Device::CreateTextureImpl C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\d3d12\DeviceD3D12.cpp:439  

#4 0x7ff905e3d8f8 in dawn::native::DeviceBase::CreateTexture C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\Device.cpp:1740  

#5 0x7ff905e4e382 in dawn::native::DeviceBase::APICreateTexture C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\Device.cpp:1216  

#6 0x7ff905d82323 in wgpu::Device::CreateTexture C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\dawn\src\dawn\webgpu\_cpp.cpp:2218  

#7 0x7ff9142ae430 in GrDawnGpu::onCreateBackendTexture C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\dawn\GrDawnGpu.cpp:362  

#8 0x7ff9142479de in GrGpu::createBackendTexture C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\GrGpu.cpp:893  

#9 0x7ff9117975c3 in create\_and\_clear\_backend\_texture C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\GrDirectContext.cpp:510  

#10 0x7ff91179704c in GrDirectContext::createBackendTexture C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\GrDirectContext.cpp:582  

#11 0x7ff91a46393d in viz::ImageContextImpl::CreateFallbackImage C:\b\s\w\ir\cache\builder\src\components\viz\service\display\_embedder\image\_context\_impl.cc:77  

#12 0x7ff91a463eb3 in viz::ImageContextImpl::BeginAccessIfNecessary C:\b\s\w\ir\cache\builder\src\components\viz\service\display\_embedder\image\_context\_impl.cc:118  

#13 0x7ff91a43d021 in viz::SkiaOutputSurfaceImplOnGpu::BeginAccessImages C:\b\s\w\ir\cache\builder\src\components\viz\service\display\_embedder\skia\_output\_surface\_impl\_on\_gpu.cc:1585  

#14 0x7ff91a43c26e in viz::SkiaOutputSurfaceImplOnGpu::PromiseImageAccessHelper::BeginAccess C:\b\s\w\ir\cache\builder\src\components\viz\service\display\_embedder\skia\_output\_surface\_impl\_on\_gpu.cc:192  

#15 0x7ff91a442fb0 in viz::SkiaOutputSurfaceImplOnGpu::FinishPaintCurrentFrame C:\b\s\w\ir\cache\builder\src\components\viz\service\display\_embedder\skia\_output\_surface\_impl\_on\_gpu.cc:489  

#16 0x7ff916352a01 in base::internal::Invoker<base::internal::BindState<void (viz::SkiaOutputSurfaceImplOnGpu::\*)(sk\_sp<SkDeferredDisplayList>, sk\_sp<SkDeferredDisplayList>, std::Cr::vector<viz::ImageContextImpl \*,std::Cr::allocator<viz::ImageContextImpl \*> >, std::Cr::vector<gpu::SyncToken,std::Cr::allocator[gpu::SyncToken](javascript:void(0);) >, base::OnceCallback<void ()>, base::OnceCallback<void (gfx::GpuFenceHandle)>, absl::optional[gfx::Rect](javascript:void(0);)),base::internal::UnretainedWrapper[viz::SkiaOutputSurfaceImplOnGpu](javascript:void(0);),sk\_sp<SkDeferredDisplayList>,sk\_sp<SkDeferredDisplayList>,std::Cr::vector<viz::ImageContextImpl \*,std::Cr::allocator<viz::ImageContextImpl \*> >,std::Cr::vector<gpu::SyncToken,std::Cr::allocator[gpu::SyncToken](javascript:void(0);) >,base::OnceCallback<void ()>,base::OnceCallback<void (gfx::GpuFenceHandle)>,absl::optional[gfx::Rect](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:819  

#17 0x7ff916357227 in base::internal::Invoker<base::internal::BindState<`lambda at ../../components/viz/service/display_embedder/skia_output_surface_impl.cc:1092:7',std::Cr::vector<base::OnceCallback<void ()>,std::Cr::allocator<base::OnceCallback<void ()> > >,viz::SkiaOutputSurfaceImpl::SyncMode,base::internal::UnretainedWrapper<base::WaitableEvent>,base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu>,bool,bool,base::TimeTicks>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:819 #18 0x7ff912311fa1 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:698 #19 0x7ff910ec8c4a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135 #20 0x7ff913c11299 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:428 #21 0x7ff913c102f4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:298 #22 0x7ff910f7a776 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:214 #23 0x7ff910f7884b in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78 #24 0x7ff913c1332b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:581 #25 0x7ff910e63089 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141 #26 0x7ff910f16f79 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:337 #27 0x7ff910f174a3 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:408 #28 0x7ff910f9946a in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:132  

#29 0x7ff6d1334193 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#30 0x7ff9a1b47033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#31 0x7ff9a2822650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\Texture.cpp:538 in dawn::native::TextureBase::TextureBase  

Thread T22 created by T0 here:  

#0 0x7ff6d1334c22 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ff910f98834 in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:197  

#2 0x7ff910f161b7 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:210  

#3 0x7ff909a127d5 in content::GpuProcessHost::Init C:\b\s\w\ir\cache\builder\src\content\browser\gpu\gpu\_process\_host.cc:909  

#4 0x7ff909a119bb in content::GpuProcessHost::Get C:\b\s\w\ir\cache\builder\src\content\browser\gpu\gpu\_process\_host.cc:606  

#5 0x7ff9099d98e8 in content::BrowserGpuChannelHostFactory::EstablishRequest::Establish C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:157  

#6 0x7ff9099d962a in content::BrowserGpuChannelHostFactory::EstablishRequest::Create C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:129  

#7 0x7ff9099dc25d in content::BrowserGpuChannelHostFactory::EstablishGpuChannel C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:380  

#8 0x7ff9099dbd61 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:332  

#9 0x7ff9099dae92 in content::BrowserGpuChannelHostFactory::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:260  

#10 0x7ff9095508a0 in content::BrowserMainLoop::PostCreateThreadsImpl C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1266  

#11 0x7ff90954fc92 in content::BrowserMainLoop::PostCreateThreads C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:932  

#12 0x7ff90a504f7e in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup\_task\_runner.cc:43  

#13 0x7ff90954f322 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:860  

#14 0x7ff909557954 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:136  

#15 0x7ff90954bbc4 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:26  

#16 0x7ff910a17d73 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:679  

#17 0x7ff910a1ad24 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1203  

#18 0x7ff910a1a60c in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1068  

#19 0x7ff910a169a1 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:433  

#20 0x7ff910a17174 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:461  

#21 0x7ff9051f14ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182  

#22 0x7ff6d1285a0e in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162  

#23 0x7ff6d1282bd0 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#24 0x7ff6d16854bf in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#25 0x7ff9a1b47033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#26 0x7ff9a2822650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

==14972==ABORTING

## Timeline

### [Deleted User] (2022-08-06)

[Empty comment from Monorail migration]

### ma...@google.com (2022-08-08)

Have not yet reproduced this on. Tentatively Security_Severity-High for GPU process memory corruption, Security_Impact-None because this feature doesn't look enabled anywhere.

dawn owners, PTAL?

[Monorail components: Internals>GPU>Dawn]

### [Deleted User] (2022-08-08)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-08-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia>Compositing]

### en...@chromium.org (2022-08-08)

Dropping this to P2. --enable-features=SkiaDawn is not a configuration that is not shipped anywhere and not well supported at this time to my knowledge.

### ba...@chromium.org (2022-08-08)

Did a quick ASAN build to see if I could repro and while I'm seeing a crash it's consistently coming back with a different stack:

[39084:33744:0808/151911.284:FATAL:skia_output_device.cc(377)] Check failed: characterization.isTextureable() == surface_characterization.isTextureable() (1 vs. 0)
Backtrace:
        base::debug::CollectStackTrace [0x00007FFB9AE5FB92+18] (C:\src\chrome\src\base\debug\stack_trace_win.cc:329)
        base::debug::StackTrace::StackTrace [0x00007FFB9AC2C56A+26] (C:\src\chrome\src\base\debug\stack_trace.cc:218)
        logging::LogMessage::~LogMessage [0x00007FFB9AC71C9A+650] (C:\src\chrome\src\base\logging.cc:665)
        logging::LogMessage::~LogMessage [0x00007FFB9AC74D20+16] (C:\src\chrome\src\base\logging.cc:658)
        viz::SkiaOutputDevice::Draw [0x00007FFBA9D0E4AE+2910] (C:\src\chrome\src\components\viz\service\display_embedder\skia_output_device.cc:377)
        viz::SkiaOutputSurfaceImplOnGpu::FinishPaintCurrentFrame [0x00007FFBA5B4DBB1+2129] (C:\src\chrome\src\components\viz\service\display_embedder\skia_output_surface_impl_on_gpu.cc:499)
        base::internal::Invoker<base::internal::BindState<void (viz::SkiaOutputSurfaceImplOnGpu::*)(sk_sp<SkDeferredDisplayList>, sk_sp<SkDeferredDisplayList>, std::Cr::vector<viz::ImageContextImpl *,std::Cr::allocator<viz::ImageContextImpl *> >, std::Cr::vector< [0x00007FFBA0EB9F52+914] (C:\src\chrome\src\base\bind_internal.h:819)
        base::internal::Invoker<base::internal::BindState<`lambda at ../../components/viz/service/display_embedder/skia_output_surface_impl.cc:1092:7',std::Cr::vector<base::OnceCallback<void ()>,std::Cr::allocator<base::OnceCallback<void ()> > >,viz::SkiaOutputSu [0x00007FFBA0EBFE6F+1039] (C:\src\chrome\src\base\bind_internal.h:819)
        gpu::Scheduler::RunNextTask [0x00007FFB9C4C470F+3603] (C:\src\chrome\src\gpu\command_buffer\service\scheduler.cc:698)
        base::TaskAnnotator::RunTaskImpl [0x00007FFB9AD92835+1045] (C:\src\chrome\src\base\task\common\task_annotator.cc:135)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFB9E1A41C5+4229] (C:\src\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:428)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFB9E1A2466+486] (C:\src\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:298)
        base::MessagePumpForUI::DoRunLoop [0x00007FFB9AE7BE55+677] (C:\src\chrome\src\base\message_loop\message_pump_win.cc:214)
        base::MessagePumpWin::Run [0x00007FFB9AE791A5+533] (C:\src\chrome\src\base\message_loop\message_pump_win.cc:78)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFB9E1A6F9F+1775] (C:\src\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:581)
        base::RunLoop::Run [0x00007FFB9AD1D8C9+1625] (C:\src\chrome\src\base\run_loop.cc:141)
        base::Thread::Run [0x00007FFB9AE09972+562] (C:\src\chrome\src\base\threading\thread.cc:337)
        base::Thread::ThreadMain [0x00007FFB9AE0A139+1817] (C:\src\chrome\src\base\threading\thread.cc:411)
        base::`anonymous namespace'::ThreadFunc [0x00007FFB9AEA2351+673] (C:\src\chrome\src\base\threading\platform_thread_win.cc:132)
        __asan::AsanThread::ThreadStart [0x00007FF651F438D4+132] (C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:277)
        BaseThreadInitThunk [0x00007FFC377C7034+20]
        RtlUserThreadStart [0x00007FFC38902651+33]

### 0x...@gmail.com (2022-08-09)

Reproduce:
Download the latest win-asan build:
gsutil cp gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-1032766.zip .
then run:
chrome --user-data-dir=C:/tmp/any --no-sandbox --enable-features=SkiaDawn --enable-low-end-device-mode --in-process-gpu https://www.google.com    will trigger the crash.

I can reproduce this issue in different computers.

### nh...@google.com (2022-11-30)

Security marshal here: bajones@, can you provide an update on what the plan is for this bug?

### ba...@chromium.org (2022-12-01)

Downloaded the latest win-asan build (win32-release_x64_asan-win32-release_x64-1078212), and still getting the same issue, this time with a stack that's more similar to the first one. (Attached at the bottom of this comment.) It gives a little bit more information and shows that the failure is specifically coming from trying to resolve the texture format in Dawn.

If we trace where that format is coming from up the stack, we eventually run into `SkiaOutputSurfaceImpl::GetGrBackendFormatForTexture()` (https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/display_embedder/skia_output_surface_impl.cc;l=1190;drc=2df668b7cbf6c1d0766b6ee0ae8147adc8830f2e), which gets the format that's being passed with the `ToDawnFormat()` function. (https://source.chromium.org/chromium/chromium/src/+/main:components/viz/common/resources/resource_format_utils.cc;l=562;drc=2df668b7cbf6c1d0766b6ee0ae8147adc8830f2e).

That function has the opportunity to return `wgpu::TextureFormat::Undefined;`, which may be getting passed all the way down to the Dawn texture constructor at which point it triggers invalid lookup. We do have validation checks in place that should be rejecting a texture that attempts to use Undefined as the format, but it appears that when viz is using Dawn without DCHECKs being enabled, is disables that validation. (https://source.chromium.org/chromium/chromium/src/+/main:components/viz/common/gpu/dawn_context_provider.cc;l=63?q=skip_validation&ss=chromium%2Fchromium%2Fsrc) I don't know exactly what arguments the asan builds are created with, but I think there's a high likelyhood that they don't have DCHECK enabled. 

So what it looks like is that Skia is passing Dawn a bad texture format while we're simultaneously removing Dawn's ability to report that it was a bad format.

Given that this is likely a problem that needs to be fixed on the Skia end, I'm unassigning from myself and assigning hob@chromium.org, since it looks as if they've touched the skia->dawn format mapping code previously and hopefully at least know who to ping about this.

// ASAN failure stack:

[822976:826588:1201/131659.076:ERROR:shared_image_factory.cc(584)] CreateSharedImage: could not create backing.
[822976:826588:1201/131659.076:ERROR:shared_image_stub.cc(199)] SharedImageStub: Unable to create shared image
[822976:826588:1201/131659.221:ERROR:shared_image_factory.cc(584)] CreateSharedImage: could not create backing.
[822976:826588:1201/131659.221:ERROR:shared_image_stub.cc(199)] SharedImageStub: Unable to create shared image
[822976:826588:1201/131659.231:ERROR:shared_image_manager.cc(189)] SharedImageManager::ProduceSkia: Trying to Produce a Skia representation from a non-existent mailbox.
=================================================================
==822976==ERROR: AddressSanitizer: breakpoint on unknown address 0x7ff959e43cc8 (pc 0x7ff959e43cc8 bp 0x00931effdf20 sp 0x00931effde38 T19)
==822976==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff959e43cc7 in absl::internal_statusor::ThrowBadStatusOrAccess C:\b\s\w\ir\cache\builder\src\third_party\abseil-cpp\absl\status\statusor.cc:93
    #1 0x7ff95b839c1d in dawn::native::DeviceBase::GetValidInternalFormat C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:747
    #2 0x7ff95b9316c9 in dawn::native::TextureBase::TextureBase C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Texture.cpp:530
    #3 0x7ff95b9e07ea in dawn::native::d3d12::Texture::Texture C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\TextureD3D12.cpp:656
    #4 0x7ff95b9e0493 in dawn::native::d3d12::Texture::Create C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\TextureD3D12.cpp:503
    #5 0x7ff95b980202 in dawn::native::d3d12::Device::CreateTextureImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\DeviceD3D12.cpp:471
    #6 0x7ff95b83b8a5 in dawn::native::DeviceBase::CreateTexture C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1722
    #7 0x7ff95b84c1cd in dawn::native::DeviceBase::APICreateTexture C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1178
    #8 0x7ff95b76f6d7 in wgpu::Device::CreateTexture C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\webgpu_cpp.cpp:2295
    #9 0x7ff96a818acc in GrDawnGpu::onCreateBackendTexture C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\dawn\GrDawnGpu.cpp:365
    #10 0x7ff96a7ae512 in GrGpu::createBackendTexture C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrGpu.cpp:894
    #11 0x7ff96796c9aa in create_and_clear_backend_texture C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDirectContext.cpp:513
    #12 0x7ff96796c408 in GrDirectContext::createBackendTexture C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDirectContext.cpp:586
    #13 0x7ff970c1ae52 in viz::ImageContextImpl::CreateFallbackImage C:\b\s\w\ir\cache\builder\src\components\viz\service\display_embedder\image_context_impl.cc:73
    #14 0x7ff970c1b3fa in viz::ImageContextImpl::BeginAccessIfNecessary C:\b\s\w\ir\cache\builder\src\components\viz\service\display_embedder\image_context_impl.cc:119
    #15 0x7ff970bed82e in viz::SkiaOutputSurfaceImplOnGpu::BeginAccessImages C:\b\s\w\ir\cache\builder\src\components\viz\service\display_embedder\skia_output_surface_impl_on_gpu.cc:1568
    #16 0x7ff970becbe9 in viz::SkiaOutputSurfaceImplOnGpu::PromiseImageAccessHelper::BeginAccess C:\b\s\w\ir\cache\builder\src\components\viz\service\display_embedder\skia_output_surface_impl_on_gpu.cc:187
    #17 0x7ff970bf430e in viz::SkiaOutputSurfaceImplOnGpu::FinishPaintCurrentFrame C:\b\s\w\ir\cache\builder\src\components\viz\service\display_embedder\skia_output_surface_impl_on_gpu.cc:479
    #18 0x7ff96c4fdf78 in base::internal::Invoker<base::internal::BindState<void (viz::SkiaOutputSurfaceImplOnGpu::*)(sk_sp<SkDeferredDisplayList>, sk_sp<SkDeferredDisplayList>, std::Cr::vector<viz::ImageContextImpl *,std::Cr::allocator<viz::ImageContextImpl *> >, std::Cr::vector<gpu::SyncToken,std::Cr::allocator<gpu::SyncToken> >, base::OnceCallback<void ()>, base::OnceCallback<void (gfx::GpuFenceHandle)>, absl::optional<gfx::Rect>),base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu,base::RawPtrBanDanglingIfSupported>,sk_sp<SkDeferredDisplayList>,sk_sp<SkDeferredDisplayList>,std::Cr::vector<viz::ImageContextImpl *,std::Cr::allocator<viz::ImageContextImpl *> >,std::Cr::vector<gpu::SyncToken,std::Cr::allocator<gpu::SyncToken> >,base::OnceCallback<void ()>,base::OnceCallback<void (gfx::GpuFenceHandle)>,absl::optional<gfx::Rect> >,void ()>::RunImpl<void (viz::SkiaOutputSurfaceImplOnGpu::*)(sk_sp<SkDeferredDisplayList>, sk_sp<SkDeferredDisplayList>, std::Cr::vector<viz::ImageContextImpl *,std::Cr::allocator<viz::ImageContextImpl *> >, std::Cr::vector<gpu::SyncToken,std::Cr::allocator<gpu::SyncToken> >, base::OnceCallback<void ()>, base::OnceCallback<void (gfx::GpuFenceHandle)>, absl::optional<gfx::Rect>),std::Cr::tuple<base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu,base::RawPtrBanDanglingIfSupported>,sk_sp<SkDeferredDisplayList>,sk_sp<SkDeferredDisplayList>,std::Cr::vector<viz::ImageContextImpl *,std::Cr::allocator<viz::ImageContextImpl *> >,std::Cr::vector<gpu::SyncToken,std::Cr::allocator<gpu::SyncToken> >,base::OnceCallback<void ()>,base::OnceCallback<void (gfx::GpuFenceHandle)>,absl::optional<gfx::Rect> >,0,1,2,3,4,5,6,7> C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:943
    #19 0x7ff96c502e32 in base::internal::Invoker<base::internal::BindState<`lambda at ../../components/viz/service/display_embedder/skia_output_surface_impl.cc:1107:7',std::Cr::vector<base::OnceCallback<void ()>,std::Cr::allocator<base::OnceCallback<void ()> > >,viz::SkiaOutputSurfaceImpl::SyncMode,base::internal::UnretainedWrapper<base::WaitableEvent,base::RawPtrBanDanglingIfSupported>,base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu,base::RawPtrBanDanglingIfSupported>,bool,bool,base::TimeTicks>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:894
    #20 0x7ff967ff1982 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:726
    #21 0x7ff967ffb4a3 in base::internal::Invoker<base::internal::BindState<void (gpu::Scheduler::*)(),base::internal::UnretainedWrapper<gpu::Scheduler,base::RawPtrBanDanglingIfSupported> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:894
    #22 0x7ff966a402d9 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:156
    #23 0x7ff969a8d321 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:450
    #24 0x7ff969a8be12 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:301
    #25 0x7ff966af2182 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:214
    #26 0x7ff966af0300 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #27 0x7ff969a8f753 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:610
    #28 0x7ff9669cc7ae in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #29 0x7ff966a9403d in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:344
    #30 0x7ff966a94455 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:414
    #31 0x7ff966b14391 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:134
    #32 0x7ff6925eeab3 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:277
    #33 0x7ffa5193554f in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x18001554f)
    #34 0x7ffa524a485a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18000485a)

### an...@chromium.org (2022-12-09)

Hi hob@, a friendly ping from the security marshal! Have you had a chance to look at this bug, specifically https://crbug.com/chromium/1350740#c9? Please feel free to re-assign if necessary. Thanks!

### ho...@chromium.org (2022-12-19)

Apologies for the delay on this.

Unfortunately, I don't have a Windows device handy to test with, but I wonder if the fix is as printing out which ResourceFormat is returning the wgpu::TextureFormat::Undefined and adding a corresponding mapping.

Tentatively reassigning to kylechar@ because I think they have more experience developing on Windows. Feel free to reassign as needed!

### ma...@google.com (2022-12-21)

Looks like kylechar@ is currently OOO.

### ky...@chromium.org (2023-01-03)

The SkiaDawn feature (which makes Skia use the Dawn backend) isn't a real configuration that's intended to be shipped. I don't see any reason to fix this.

We should probably actually just remove the SkiaDawn feature for now since making Skia ganesh Dawn backend work is a non goal AFAIK? zmo/sunnyps what do you think? Or do we need this feature for Skia graphite Dawn backend too?

It's possible this error is relevant for Skia graphite Dawn backend at some point. Assigning to sunnyps@ to check.

### su...@chromium.org (2023-01-27)

https://chromium-review.googlesource.com/c/chromium/src/+/4200081 should fix this - if we return an invalid GrBackendTexture() then Skia will not call Dawn with the wgpu undefined format. This is the simplest way to fix this bug.

FWIW we do need the feature for Skia Graphite Dawn too at least in the prototype (which isn't on trunk).

### gi...@appspot.gserviceaccount.com (2023-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b9c050d1181ba430362d6770bc1909ee7829cad8

commit b9c050d1181ba430362d6770bc1909ee7829cad8
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Mon Jan 30 15:17:33 2023

viz: Handle undefined dawn format

gpu::ToDawnFormat returns wgpu::TextureFormat::Undefined for several
common formats. When wrapped in a GrBackendFormat, Skia assumes that the
format is valid and passes it back to Dawn CreateTexture. When Dawn
validation is disabled in release builds this can cause security issues.

Bug: 1350740
Change-Id: I00b6fd3145c46a8f412e45fcb461f6fad083c8a6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4200081
Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
Commit-Queue: Saifuddin Hitawala <hitawala@chromium.org>
Reviewed-by: Saifuddin Hitawala <hitawala@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1098595}

[modify] https://crrev.com/b9c050d1181ba430362d6770bc1909ee7829cad8/components/viz/service/display_embedder/skia_output_surface_impl.cc


### su...@chromium.org (2023-01-31)

Requesting M111 merge - do we need to merge to M110 as well - I don't think this CL will cleanly apply due to recent refactoring, but we can prepare a similar fix if need be.

### [Deleted User] (2023-01-31)

Merge approved: your change passed merge requirements and is auto-approved for M111. Please go ahead and merge the CL to branch 5563 (refs/branch-heads/5563) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7d9282743115f260c61df81c2037be83f52445e4

commit 7d9282743115f260c61df81c2037be83f52445e4
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Tue Jan 31 20:35:20 2023

[m111] viz: Handle undefined dawn format

gpu::ToDawnFormat returns wgpu::TextureFormat::Undefined for several
common formats. When wrapped in a GrBackendFormat, Skia assumes that the
format is valid and passes it back to Dawn CreateTexture. When Dawn
validation is disabled in release builds this can cause security issues.

(cherry picked from commit b9c050d1181ba430362d6770bc1909ee7829cad8)

Bug: 1350740
Change-Id: I00b6fd3145c46a8f412e45fcb461f6fad083c8a6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4200081
Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
Commit-Queue: Saifuddin Hitawala <hitawala@chromium.org>
Reviewed-by: Saifuddin Hitawala <hitawala@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1098595}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4210828
Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5563@{#64}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/7d9282743115f260c61df81c2037be83f52445e4/components/viz/service/display_embedder/skia_output_surface_impl.cc


### su...@chromium.org (2023-01-31)

I won't pursue merging to M110 given that 1) this bug is really not high severity since it requires the user to pass in the --enable-features=SkiaDawn flag, and 2) the code in question has been refactored substantially so an M110 fix would essentially be a new CL on that branch rather than a merge.

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### wf...@chromium.org (2023-02-08)

Re: https://crbug.com/chromium/1350740#c13 - is there a bug to track the full removal of the SkiaDawn feature?

### cw...@chromium.org (2023-02-09)

From https://crbug.com/chromium/1350740#c14, this feature is used in the development of Graphite-Dawn and bugs such as this one will be fixed as part of the enablement of Skia-Graphite on Dawn in Chromium. So I don't think we want to remove the feature.

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-09)

Thank you for this report! Based on this report and how this bug is triggered, we are certain that this issue would have been discovered and resolved before this code would have shipped. Given this is not shipping, but we did make a change to negate this bug, we are offering a partial reward. The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-10)

This issue was migrated from crbug.com/chromium/1350740?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>GPU>Dawn, Internals>Skia>Compositing]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060520)*
