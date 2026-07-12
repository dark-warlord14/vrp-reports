# OOB Write in CalculateNPOTTwiddleSparsePageMap3D cause android chrome gpu crash

| Field | Value |
|-------|-------|
| **Issue ID** | [490251699](https://issues.chromium.org/issues/490251699) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ge...@google.com |
| **Created** | 2026-03-06 |
| **Bounty** | $32,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

After careful analysis, I discovered another integer overflow vulnerability. The root cause has finally been identified. It is similar to the issue, but not in the same place. However, both of them call the CalculateNPOTTwiddleSparsePageMap and CalculateNPOTTwiddleSparsePageMap3D family functions to handle writes, so out-of-bounds writes occur here.`x0_19` is int32\_t, and the parameters passed in can bypass Chrome's syntax validation, thus causing a crash.

```
00556ad0    int64_t RenderbufferStorage.__uniq.237312041013645830485009770479023593730(GLES3Context_TAG* arg1, uint32_t arg2, int32_t arg3, uint32_t arg4, 
00556ad0      int32_t arg5, int32_t arg6)

......
00557094                int32_t* x0_19 = calloc(1, zx.q(x8_50.d))


```

VERSION

Chromium Version: [147.0.7721.0] + [stable, beta, or dev]

Operating System: [pixel0 latest]

REPRODUCTION CASE

1.open poc.html
2. logcat | grep DEBUG

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [gpu.]

```

Build fingerprint: 'google/frankel/frankel:16/CP1A.260305.018/14887507:user/release-keys'
Revision: 'MP1.0'
pid: 11087, tid: 11102, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0000007c379495c0 (write)

Stack Trace:
  RELADDR   FUNCTION                                                                          FILE:LINE
  00000000001259d0  CalculateNPOTTwiddleSparsePageMap+368) (BuildId: af33e0bbb85a052bfb98677c54834b2a  /vendor/lib64/hw/vulkan.powervr.so
  00000000000680bc  ImageCreate(_ALLOCATION_CONTEXT*, _DEVICE*, VkImageCreateInfo const*, _IMAGE*) (.__uniq.70668740889448621895728953958423221693)+3420) (BuildId: af33e0bbb85a052bfb98677c54834b2a  /vendor/lib64/hw/vulkan.powervr.so
  00000000001392c0  IMG_vkCreateImage+112) (BuildId: af33e0bbb85a052bfb98677c54834b2a                 /vendor/lib64/hw/vulkan.powervr.so
  v------>  rx::vk::Image::init(VkDevice_T*, VkImageCreateInfo const&)                        ../../third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1581:12
  0000000002f57108  rx::vk::ImageHelper::initExternal(rx::vk::ErrorContext*, gl::TextureType, VkExtent3D const&, angle::FormatID, angle::FormatID, int, unsigned int, unsigned int, rx::vk::ImageAccess, void const*, gl::LevelIndexWrapper<int>, unsigned int, unsigned int, bool, bool, rx::vk::TileMemory, rx::vk::YcbcrConversionDesc, void const*, rx::vk::ImageFormatReinterpretability)  ../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:5924:34
  0000000002ee5a64  rx::RenderbufferVk::setStorageImpl(gl::Context const*, int, unsigned int, int, int, gl::MultisamplingMode)  ../../third_party/angle/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp:133:23
  0000000003024450  gl::Renderbuffer::setStorage(gl::Context const*, unsigned int, int, int)          ../../third_party/angle/src/libANGLE/Renderbuffer.cpp:148:32
  0000000008fba53c  gpu::gles2::GLES2DecoderPassthroughImpl::DoRenderbufferStorage(unsigned int, unsigned int, int, int)  ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:2763:10
  0000000008fa8aec  gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:742:20
  0000000003cd0c48  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:267:35
  000000000906a964  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:504:22
  000000000906a6a8  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/command_buffer_stub.cc:173:7
  0000000009070078  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/gpu_channel.cc:833:13
  v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:740:12
  v------>  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, void, 0ul, 1ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>&&, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:956:5
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, 0ul, 1ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:1069:14
  0000000009072b38  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)  ../../base/functional/bind_internal.h:982:12
  v------>  base::OnceCallback<void (media::DemuxerStream*)>::Run(media::DemuxerStream*) &&   ../../base/functional/callback.h:155:12
  v------>  void base::internal::DecayedFunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*&&>::Invoke<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*>(base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&)  ../../base/functional/bind_internal.h:815:49
  v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, void, 0ul>::MakeItSo<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&)  ../../base/functional/bind_internal.h:932:12
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (media::DemuxerStream*)>, base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1069:14
  00000000036235a0  base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (BrowserWindowInterface*)>&&, base::raw_ptr<BrowserWindowInterface, (partition_alloc::internal::RawPtrTraits)1>&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (BrowserWindowInterface*)>, base::internal::UnretainedWrapper<BrowserWindowInterface, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)1>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:982:12
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  0000000003cd5f58  gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler.cc:707:29
  0000000003cd5758  gpu::Scheduler::RunNextTask()                                                     ../../gpu/command_buffer/service/scheduler.cc:625:3
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  0000000006742638  base::TaskAnnotator::RunTaskImpl(base::PendingTask&)                              ../../base/task/common/task_annotator.cc:229:34
  v------>  void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&)  ../../base/task/common/task_annotator.h:112:5
  000000000675c980  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
  000000000675c59c  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()   ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
  00000000066f8dc8  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)                       ../../base/message_loop/message_pump_default.cc:42:55
  000000000675cf98  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
  0000000006723b10  base::RunLoop::Run(base::Location const&)                                         ../../base/run_loop.cc:135:14
  000000000c079294  content::GpuMain(content::MainFunctionParams)                                     ../../content/gpu/gpu_main.cc:479:14
  00000000066d4558  content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)  ../../content/app/content_main_runner_impl.cc:762:14
  00000000066d53f8  content::ContentMainRunnerImpl::Run()                                             ../../content/app/content_main_runner_impl.cc:1152:10
  00000000066d2f6c  content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)  ../../content/app/content_main.cc:358:36
  00000000066d3ee0  content::StartContentMain(bool)                                                   ../../content/app/android/content_main_android.cc:54:10
  00000000002c2300  art_quick_generic_jni_trampoline+144) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  00000000006683e8  nterp_helper+152) (BuildId: 61c7a211c01ef3c0068b4fbe31051050                      /apex/com.android.art/lib64/libart.so
  000000000028c12a  offset 0x1ef4000) (dh1.run+570                                                    /data/app/~~1uKY6XI5Cduj56Au_QnOLg==/org.chromium.chrome-RU-hR0vF4Ttrq0BXF0rCYw==/base.apk/libmonochrome.so
  00000000003215f0  java.lang.Thread.run+64                                                           /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat
  00000000002aaf94  art_quick_invoke_stub+612) (BuildId: 61c7a211c01ef3c0068b4fbe31051050             /apex/com.android.art/lib64/libart.so
  00000000002709b0  art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  00000000004bdfc8  art::Thread::CreateCallback(void*)+1184) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  00000000004bdb18  art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  000000000008a914  __pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 8d65ea529c21c79c019713e50adb6675  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000007b5a4  __start_thread+68) (BuildId: 8d65ea529c21c79c019713e50adb6675                     /apex/com.android.runtime/lib64/bionic/libc.so


```

Solution: Verification at the angle level is likely impossible; this should be addressed through the PowerVR vendor.

## Attachments

- [oob2.html](attachments/oob2.html) (text/html, 1.0 KB)
- [about-gpu-2026-03-10T14-34-15-754Z.txt.phps](attachments/about-gpu-2026-03-10T14-34-15-754Z.txt.phps) (application/x-httpd-php-source, 44.0 KB)

## Timeline

### jd...@chromium.org (2026-03-09)

Due to the influx of bug reports, I'm not able to dedicate as much investigation to these vulnerability reports as I'd like. However, I'm conservatively calling this a web-accessible bug in an unsandboxed (GPU) process on Android, which qualifies as critical severity.

I'm sending this over to geofflang@ for further triage, verification, routing, etc.

I'm sorry for sending so much your way, Geoff. If there's a better recipient for future reports, please let me know.

### ch...@google.com (2026-03-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-10)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ge...@chromium.org (2026-03-10)

This one requires a non-shipping config (ANGLE Vulkan backend) to trigger. Lowering priority.

Reporter: can you list the flag changes you needed to trigger this?

### ha...@gmail.com (2026-03-10)

No configuration is required; it triggered automatically with my Chrome stable settings by default.

### ha...@gmail.com (2026-03-10)

I think this is quite important. It's triggered by default, and it seems the PC register can be controlled after heap spraying. Refer to another integer overflow vulnerability I mentioned.

### ge...@chromium.org (2026-03-10)

Can you post the contents of about:gpu on the device that reproduces? You may be in some experiment group.

### ha...@gmail.com (2026-03-10)

These settings are all default; I haven't enabled any flags.

### ha...@gmail.com (2026-03-10)

I think I understand why you said that. I have two Chrome instances, one stable and one custom-compiled. I provided the one with symbols because the VRP staff asked me to provide symbols, so I provided this.

### ge...@chromium.org (2026-03-10)

I'm not sure how you're getting ANGLE or Vulkan at all. The about:gpu you posted says neither of them are in use.

If this is a local ToT build, you would get Vulkan/Passthrough due to it being in [fieldtrial\_testing\_config](https://source.chromium.org/chromium/chromium/src/+/main:testing/variations/fieldtrial_testing_config.json;l=7968-7982;drc=8e94f3d885b6e5ebb19015539ff82acc159bd03a) but it's not enabled in the wild at all right now.

### ge...@chromium.org (2026-03-11)

Ok, I think given that this is a non-shipping config, it's not a security bug. I'm going to mark it as a Bug and lower the priority/severity.

Sending to syoussefi@ who looks at most vulkan backend bugs.

### ha...@gmail.com (2026-03-11)

Hello, what do you mean by "non-shipping configuration"? This vulnerability can be triggered by the default configuration; you can try to reproduce it. The vulnerability isn't defined the way you described.

### ha...@gmail.com (2026-03-12)

I don't understand why you think this vulnerability is a non-shipping configuration. Chrome Statble can reproduce it by default; you can reproduce it as long as you install Chrome.

```
signal 11 (SIGSEGV), code 2 (SEGV_ACCERR), fault addr 0x7221be7af0 in tid 3929 (CrGpuMain), pid 3910 (ileged_process2)
Build fingerprint: 'google/frankel/frankel:16/CP1A.260305.018/14887507:user/release-keys'
Revision: 'MP1.0'
pid: 3910, tid: 3929, name: CrGpuMain  >>> org.chromium.chrome:privileged_process2 <<<
signal 11 (SIGSEGV), code 2 (SEGV_ACCERR), fault addr 0x0000007221be7af0 (write)

Stack Trace:
  RELADDR   FUNCTION                                                                          FILE:LINE
  00000000000ce490  CalculateNPOTTwiddleSparsePageMap+448) (BuildId: cefd59f52838946b0e646aaf2bb04c76  /vendor/lib64/egl/libGLESv2_powervr.so
  000000000013c174  RenderbufferStorage(GLES3Context_TAG*, unsigned int, int, unsigned int, int, int) (.__uniq.237312041013645830485009770479023593730)+1572) (BuildId: cefd59f52838946b0e646aaf2bb04c76  /vendor/lib64/egl/libGLESv2_powervr.so
  00000000030fb90c  rx::ProgramExecutableGL::syncUniformBlockBindings()                               ../../third_party/angle/src/libANGLE/renderer/gl/ProgramExecutableGL.cpp:521:39
  v------>  std::__Cr::pair<std::__Cr::__tree_end_node<std::__Cr::__tree_node_base<void*>*>*, std::__Cr::__tree_node_base<void*>*&> std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, sh::BlockMemberInfo>, std::__Cr::__map_value_compare<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, sh::BlockMemberInfo>, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, sh::BlockMemberInfo>>>::__find_equal<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&)  gen/third_party/libc++/src/include/__tree:0:12
  v------>  std::__Cr::__tree_iterator<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, sh::BlockMemberInfo>, std::__Cr::__tree_node<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, sh::BlockMemberInfo>, void*>*, long> std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, sh::BlockMemberInfo>, std::__Cr::__map_value_compare<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, sh::BlockMemberInfo>, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, sh::BlockMemberInfo>>>::find<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&)  gen/third_party/libc++/src/include/__tree:1209:26
  v------>  std::__Cr::map<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, sh::BlockMemberInfo, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, sh::BlockMemberInfo>>>::find(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&)  gen/third_party/libc++/src/include/map:1313:95
  v------>  gl::(anonymous namespace)::InterfaceBlockInfo::getBlockMemberInfo(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*)  ../../third_party/angle/src/libANGLE/ProgramLinkedResources.cpp:692:34
  v------>  gl::ProgramLinkedResourcesLinker::linkResources(gl::ProgramState const&, gl::ProgramLinkedResources const&) const::$_1::operator()(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*) const  ../../third_party/angle/src/libANGLE/ProgramLinkedResources.cpp:1759:33
  v------>  std::__Cr::__invoke_result_impl<void, gl::ProgramLinkedResourcesLinker::linkResources(gl::ProgramState const&, gl::ProgramLinkedResources const&) const::$_1&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*>::type std::__Cr::__invoke<gl::ProgramLinkedResourcesLinker::linkResources(gl::ProgramState const&, gl::ProgramLinkedResources const&) const::$_1&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*>(gl::ProgramLinkedResourcesLinker::linkResources(gl::ProgramState const&, gl::ProgramLinkedResources const&) const::$_1&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*&&)  gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
  v------>  bool std::__Cr::__invoke_void_return_wrapper<bool, false>::__call<gl::ProgramLinkedResourcesLinker::linkResources(gl::ProgramState const&, gl::ProgramLinkedResources const&) const::$_1&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*>(gl::ProgramLinkedResourcesLinker::linkResources(gl::ProgramState const&, gl::ProgramLinkedResources const&) const::$_1&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*&&)  gen/third_party/libc++/src/include/__type_traits/invoke.h:342:12
  v------>  bool std::__Cr::__invoke_r<bool, gl::ProgramLinkedResourcesLinker::linkResources(gl::ProgramState const&, gl::ProgramLinkedResources const&) const::$_1&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*>(gl::ProgramLinkedResourcesLinker::linkResources(gl::ProgramState const&, gl::ProgramLinkedResources const&) const::$_1&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*&&)  gen/third_party/libc++/src/include/__type_traits/invoke.h:356:10
  0000000003024450  bool std::__Cr::__function::__policy_func<bool (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*)>::__call_func<gl::ProgramLinkedResourcesLinker::linkResources(gl::ProgramState const&, gl::ProgramLinkedResources const&) const::$_3>(std::__Cr::__function::__policy_storage const*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, sh::BlockMemberInfo*)  gen/third_party/libc++/src/include/__functional/function.h:443:12
  v------>  std::__Cr::char_traits<char>::copy(char*, char const*, unsigned long)             gen/third_party/libc++/src/include/__string/char_traits.h:147:5
  v------>  std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::__init(char const*, unsigned long)  gen/third_party/libc++/src/include/string:2663:3
  v------>  std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::basic_string(char const*, unsigned long)  gen/third_party/libc++/src/include/string:1082:5
  0000000008fba53c  gpu::gles2::GLES2DecoderPassthroughImpl::DoGetActiveUniformBlockName(unsigned int, unsigned int, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>*)  ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1510:24
  0000000008fa8aec  gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::PatchGetNumericResults<unsigned char>(unsigned int, int, unsigned char*)  ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:1707:3
  v------>  ui::(anonymous namespace)::ToWebPointerType(ui::MotionEvent::ToolType)            ../../ui/events/blink/blink_event_util.cc:121:7
  v------>  ui::SetWebPointerPropertiesFromMotionEventData(blink::WebPointerProperties&, int, float, float, float, float, float, float, int, ui::MotionEvent::ToolType)  ../../ui/events/blink/blink_event_util.cc:694:39
  v------>  ui::(anonymous namespace)::CreateWebTouchPoint(ui::MotionEvent const&, unsigned long)  ../../ui/events/blink/blink_event_util.cc:168:3
  0000000003cd0c48  ui::CreateWebTouchEventFromMotionEvent(ui::MotionEvent const&, bool, bool)        ../../ui/events/blink/blink_event_util.cc:261:25
  v------>  wgpu::ObjectBase<wgpu::SharedTextureMemory, WGPUSharedTextureMemoryImpl*>::Get() const  gen/third_party/dawn/include/dawn/webgpu_cpp.h:1189:16
  v------>  wgpu::SharedTextureMemory::EndAccess(wgpu::Texture const&, wgpu::SharedTextureMemoryEndAccessState*) const  gen/third_party/dawn/include/dawn/webgpu_cpp.h:9781:52
  000000000906a964  gpu::DawnAHardwareBufferImageRepresentation::EndAccess()                          ../../gpu/command_buffer/service/shared_image/dawn_ahardwarebuffer_image_representation.cc:168:30
  v------>  wgpu::SharedTextureMemory::CreateTexture(wgpu::TextureDescriptor const*) const    gen/third_party/dawn/include/dawn/webgpu_cpp.h:9776:19
  000000000906a6a8  gpu::DawnAHardwareBufferImageRepresentation::BeginAccess(wgpu::TextureUsage, wgpu::TextureUsage)  ../../gpu/command_buffer/service/shared_image/dawn_ahardwarebuffer_image_representation.cc:122:37
  v------>  std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>::__base_destruct_at_end(gpu::SyncToken*)  gen/third_party/libc++/src/include/__vector/vector.h:760:5
  v------>  std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>::clear()  gen/third_party/libc++/src/include/__vector/vector.h:549:5
  v------>  std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>::__destroy_vector::operator()()  gen/third_party/libc++/src/include/__vector/vector.h:248:16
  v------>  std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>::~vector()  gen/third_party/libc++/src/include/__vector/vector.h:259:67
  0000000009070078  gpu::CommandBufferStub::SignalSyncToken(gpu::SyncToken const&, unsigned int)      ../../gpu/ipc/service/command_buffer_stub.cc:582:3
  0000000009072b38  gpu::GLES2CommandBufferStub::Initialize(gpu::mojom::CreateCommandBufferParams const&, base::UnsafeSharedMemoryRegion)  ../../gpu/ipc/service/gles2_command_buffer_stub.cc:335:7
  00000000036235a0  media::FFmpegDemuxer::Initialize(media::DemuxerHost*, base::OnceCallback<void (media::TypedStatus<media::PipelineStatusTraits>)>)  ../../media/filters/ffmpeg_demuxer.cc:0:3
  v------>  void perfetto::EventContext::AddDebugAnnotation<char const*&, bool>(char const*&, bool&&)  ../../third_party/perfetto/include/perfetto/tracing/event_context.h:118:23
  v------>  void perfetto::internal::WriteTrackEventArgs<bool>(perfetto::EventContext, char const*, bool&&)  ../../third_party/perfetto/include/perfetto/tracing/internal/write_track_event_args.h:171:13
  v------>  void perfetto::internal::WriteTrackEventArgs<void*&, char const*, bool>(perfetto::EventContext, char const*, void*&, char const*&&, bool&&)  ../../third_party/perfetto/include/perfetto/tracing/internal/write_track_event_args.h:172:3
  0000000003cd5f58  void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::TraceForCategoryImplNoTimestamp<unsigned long, perfetto::StaticString, perfetto::Track, void, char const*, void*&, char const*, bool>(unsigned int, unsigned long const&, perfetto::StaticString const&, perfetto::protos::pbzero::perfetto_pbzero_enum_TrackEvent::Type, perfetto::Track const&, char const*&&, void*&, char const*&&, bool&&)::'lambda'(perfetto::DataSource<perfetto::internal::TrackEventDataSource, perfetto::internal::TrackEventDataSourceTraits>::TraceContext)::operator()(perfetto::DataSource<perfetto::internal::TrackEventDataSource, perfetto::internal::TrackEventDataSourceTraits>::TraceContext) const  ../../third_party/perfetto/include/perfetto/tracing/internal/track_event_data_source.h:1101:11
  v------>  perfetto::internal::TrackEventCategoryRegistry::GetCategoryState(unsigned long) const  ../../third_party/perfetto/include/perfetto/tracing/track_event_category_registry.h:229:13
  v------>  perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CategoryTracePointTraits::GetActiveInstances(perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CategoryTracePointTraits::TracePointData)  ../../third_party/perfetto/include/perfetto/tracing/internal/track_event_data_source.h:927:24
  v------>  void perfetto::internal::DataSourceType::FirstActiveInstance<perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CategoryTracePointTraits>(perfetto::internal::DataSourceType::InstancesIterator*, perfetto::internal::DataSourceThreadLocalState*, perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CategoryTracePointTraits::TracePointData)  ../../third_party/perfetto/include/perfetto/tracing/internal/data_source_type.h:289:13
  v------>  void perfetto::internal::DataSourceType::NextIteration<perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CategoryTracePointTraits>(perfetto::internal::DataSourceType::InstancesIterator*, perfetto::internal::DataSourceThreadLocalState*, perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CategoryTracePointTraits::TracePointData)  ../../third_party/perfetto/include/perfetto/tracing/internal/data_source_type.h:203:5
  0000000003cd5758  void perfetto::DataSource<perfetto::internal::TrackEventDataSource, perfetto::internal::TrackEventDataSourceTraits>::TraceWithInstances<perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CategoryTracePointTraits, void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::TraceForCategoryImplNoTimestamp<unsigned long, perfetto::StaticString, perfetto::Track, void, void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::TraceForCategoryLegacyWithIdBody<perfetto::Track const&, unsigned long, perfetto::StaticString, perfetto::legacy::PerfettoLegacyCurrentThreadId, blink::WebAudioMediaStreamAudioSink*, char const*, int, void>(unsigned int, unsigned long const&, perfetto::StaticString const&, perfetto::protos::pbzero::perfetto_pbzero_enum_TrackEvent::Type, perfetto::Track const&, char, unsigned int, perfetto::legacy::PerfettoLegacyCurrentThreadId, blink::WebAudioMediaStreamAudioSink*, char const*&&, int&&)::'lambda'(perfetto::EventContext)>(unsigned int, perfetto::Track const& const&, unsigned long const&, perfetto::protos::pbzero::perfetto_pbzero_enum_TrackEvent::Type, perfetto::StaticString const&, void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::TraceForCategoryLegacyWithIdBody<perfetto::Track const&, unsigned long, perfetto::StaticString, perfetto::legacy::PerfettoLegacyCurrentThreadId, blink::WebAudioMediaStreamAudioSink*, char const*, int, void>(unsigned int, unsigned long const&, perfetto::StaticString const&, perfetto::protos::pbzero::perfetto_pbzero_enum_TrackEvent::Type, perfetto::Track const&, char, unsigned int, perfetto::legacy::PerfettoLegacyCurrentThreadId, blink::WebAudioMediaStreamAudioSink*, char const*&&, int&&)::'lambda'(perfetto::EventContext)&&)::'lambda'(perfetto::DataSource<perfetto::internal::TrackEventDataSource, perfetto::internal::TrackEventDataSourceTraits>::TraceContext)>(unsigned int, unsigned long, perfetto::Track const&::TracePointData)  ../../third_party/perfetto/include/perfetto/tracing/data_source.h:463:47
  0000000006742638  base::SubstringSetMatcher::AhoCorasickNode::SetEdge(unsigned int, unsigned int)   ../../base/substring_set_matcher/substring_set_matcher.cc:465:5
  v------>  base::raw_ref<base::sequence_manager::internal::ThreadController::RunLevelTracker::TimeKeeper, (partition_alloc::internal::RawPtrTraits)0>::operator->() const  ../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ref.h:204:5
  v------>  base::sequence_manager::internal::ThreadController::RunLevelTracker::RunLevel::GetThreadName()  ../../base/task/sequence_manager/thread_controller.cc:102:8
  v------>  base::sequence_manager::internal::ThreadController::RunLevelTracker::RunLevel::GetSuffixForCatchAllHistogram()  ../../base/task/sequence_manager/thread_controller.cc:110:28
  000000000675c980  base::sequence_manager::internal::ThreadController::RunLevelTracker::RunLevel::LogIntervalMetric(char const*, base::TimeDelta, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller.cc:340:41
  v------>  base::raw_ptr<base::sequence_manager::internal::ThreadController::RunLevelTracker::TimeKeeper, (partition_alloc::internal::RawPtrTraits)4>::~raw_ptr()  ../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:444:20
  v------>  base::raw_ref<base::sequence_manager::internal::ThreadController::RunLevelTracker::TimeKeeper, (partition_alloc::internal::RawPtrTraits)0>::~raw_ref()  ../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ref.h:55:37
  000000000675c59c  base::sequence_manager::internal::ThreadController::RunLevelTracker::RunLevel::~RunLevel()  ../../base/task/sequence_manager/thread_controller.cc:312:1
  v------>  base::ReadOnlySharedMemoryRegion::ReadOnlySharedMemoryRegion(base::subtle::PlatformSharedMemoryRegion)  ../../base/memory/read_only_shared_memory_region.cc:103:7
  00000000066f8dc8  base::ReadOnlySharedMemoryRegion::Duplicate() const                               ../../base/memory/read_only_shared_memory_region.cc:72:10
  v------>  base::TimeDelta::operator+(base::TimeDelta) const                                 ../../base/time/time.h:366:19
  v------>  base::TimeDelta::operator+=(base::TimeDelta)                                      ../../base/time/time.h:261:27
  000000000675cf98  base::sequence_manager::internal::ThreadController::RunLevelTracker::RunLevel::LogOnIdleMetrics(base::LazyNow&)  ../../base/task/sequence_manager/thread_controller.cc:411:32
  v------>  base::internal::circular_deque_const_iterator<std::__Cr::unique_ptr<base::Unwinder, std::__Cr::default_delete<base::Unwinder>>>::circular_deque_const_iterator(base::circular_deque<std::__Cr::unique_ptr<base::Unwinder, std::__Cr::default_delete<base::Unwinder>>> const*, unsigned long)  ../../base/containers/circular_deque.h:247:24
  v------>  base::internal::circular_deque_iterator<std::__Cr::unique_ptr<base::Unwinder, std::__Cr::default_delete<base::Unwinder>>>::circular_deque_iterator(base::circular_deque<std::__Cr::unique_ptr<base::Unwinder, std::__Cr::default_delete<base::Unwinder>>> const*, unsigned long)  ../../base/containers/circular_deque.h:460:9
  0000000006723b10  base::circular_deque<std::__Cr::unique_ptr<base::Unwinder, std::__Cr::default_delete<base::Unwinder>>>::MakeRoomFor(unsigned long, base::internal::circular_deque_iterator<std::__Cr::unique_ptr<base::Unwinder, std::__Cr::default_delete<base::Unwinder>>>*, base::internal::circular_deque_iterator<std::__Cr::unique_ptr<base::Unwinder, std::__Cr::default_delete<base::Unwinder>>>*)  ../../base/containers/circular_deque.h:1191:19
  v------>  memcpy(void*, void const* pass_object_size0, unsigned long)                       ../../third_party/android_toolchain/ndk/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include/bits/fortify/string.h:53:12
  v------>  google::protobuf::io::EpsCopyOutputStream::WriteStringMaybeAliased(unsigned int, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, unsigned char*)  ../../third_party/protobuf/src/google/protobuf/io/coded_stream.h:707:5
  000000000c079294  sentencepiece::TrainerSpec::_InternalSerialize(unsigned char*, google::protobuf::io::EpsCopyOutputStream*) const  gen/third_party/sentencepiece/src/src/sentencepiece_model.pb.cc:1207:22
  v------>  base::PoissonAllocationSampler::OnFree(base::allocator::dispatcher::FreeNotificationData const&)  ../../base/sampling_heap_profiler/poisson_allocation_sampler.h:405:25
  v------>  void base::allocator::dispatcher::internal::PerformFreeNotification<base::PoissonAllocationSampler*, base::debug::tracer::AllocationTraceRecorder*, 0ul, 1ul>(std::__Cr::tuple<base::PoissonAllocationSampler*, base::debug::tracer::AllocationTraceRecorder*> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, base::allocator::dispatcher::FreeNotificationData const&)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:57:35
  v------>  base::allocator::dispatcher::internal::DispatcherImpl<base::PoissonAllocationSampler, base::debug::tracer::AllocationTraceRecorder>::DoNotifyFree(base::allocator::dispatcher::FreeNotificationData const&)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:367:5
  v------>  base::allocator::dispatcher::internal::DispatcherImpl<base::PoissonAllocationSampler, base::debug::tracer::AllocationTraceRecorder>::DoNotifyFreeForShim(void*)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:353:5
  00000000066d4558  base::allocator::dispatcher::internal::DispatcherImpl<base::PoissonAllocationSampler, base::debug::tracer::AllocationTraceRecorder>::AlignedFreeFn(void*, void*)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:336:5
  00000000066d53f8  base::allocator::dispatcher::internal::DispatcherImpl<base::PoissonAllocationSampler>::FreeWithSizeAndAlignmentFn(void*, unsigned long, unsigned long, void*)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:245:21
  00000000066d2f6c  base::allocator::dispatcher::internal::DispatcherImpl<base::PoissonAllocationSampler, base::debug::tracer::AllocationTraceRecorder>::AllocAlignedFn(unsigned long, unsigned long, partition_alloc::internal::base::StrongAlias<AllocTokenTag, unsigned long>, void*)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:183:5
  v------>  base::PoissonAllocationSampler::OnAllocation(base::allocator::dispatcher::AllocationNotificationData const&)  ../../base/sampling_heap_profiler/poisson_allocation_sampler.h:326:3
  v------>  void base::allocator::dispatcher::internal::PerformAllocationNotification<base::PoissonAllocationSampler*, base::debug::tracer::AllocationTraceRecorder*, 0ul, 1ul>(std::__Cr::tuple<base::PoissonAllocationSampler*, base::debug::tracer::AllocationTraceRecorder*> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, base::allocator::dispatcher::AllocationNotificationData const&)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:49:35
  v------>  base::allocator::dispatcher::internal::DispatcherImpl<base::PoissonAllocationSampler, base::debug::tracer::AllocationTraceRecorder>::DoNotifyAllocation(base::allocator::dispatcher::AllocationNotificationData const&)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:361:5
  v------>  base::allocator::dispatcher::internal::DispatcherImpl<base::PoissonAllocationSampler, base::debug::tracer::AllocationTraceRecorder>::DoNotifyAllocationForShim(void*, unsigned long)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:346:5
  00000000066d3ee0  base::allocator::dispatcher::internal::DispatcherImpl<base::PoissonAllocationSampler, base::debug::tracer::AllocationTraceRecorder>::AlignedMallocFn(unsigned long, unsigned long, partition_alloc::internal::base::StrongAlias<AllocTokenTag, unsigned long>, void*)  ../../base/allocator/dispatcher/internal/dispatcher_internal.h:287:5
  0000000000d5364c  art_jni_trampoline+108                                                            /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat
  00000000002803fc  dh1.run+2140                                                                      /data/dalvik-cache/arm64/data@app@~~1uKY6XI5Cduj56Au_QnOLg==@org.chromium.chrome-RU-hR0vF4Ttrq0BXF0rCYw==@base.apk@classes.dex
  00000000003215f0  java.lang.Thread.run+64                                                           /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat
  00000000002aaf94  art_quick_invoke_stub+612) (BuildId: 61c7a211c01ef3c0068b4fbe31051050             /apex/com.android.art/lib64/libart.so
  00000000002709b0  art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  00000000004bdfc8  art::Thread::CreateCallback(void*)+1184) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  00000000004bdb18  art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  000000000008a914  __pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 8d65ea529c21c79c019713e50adb6675  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000007b5a4  __start_thread+68) (BuildId: 8d65ea529c21c79c019713e50adb6675                     /apex/com.android.runtime/lib64/bionic/libc.so


```

### ha...@gmail.com (2026-03-12)

Please use chrome 145.0.7632.159 to reproduce.

### ge...@chromium.org (2026-03-12)

Ok, this is a different stack than what you posted in [comment #1](https://issues.chromium.org/issues/490251699#comment1).

### ge...@chromium.org (2026-03-12)

This has the same root bug as [issue 487444459](https://issues.chromium.org/issues/487444459) and is fixed by the same fix.

### ch...@google.com (2026-07-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490251699)*
