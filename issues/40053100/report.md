# container-overflow in blink::MediaStreamSource

| Field | Value |
|-------|-------|
| **Issue ID** | [40053100](https://issues.chromium.org/issues/40053100) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2020-08-17 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36

Steps to reproduce the problem:
Chromium 86.0.4236.0(gs://chromium-browser-asan/linux-release/asan-linux-release-798506.zip)
1.python3.6m -m http.server 8000
2.google-chrome --user-dir=/tmp/222 --use-fake--for-media-stream --use-fake-device-for-media-stream  --incognito http://127.0.0.1:8000/main.html

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: container-overflow on address 0x7edd41054f80 at pc 0x55f97d454d07 bp 0x7ffdd1edcd00 sp 0x7ffdd1edccf8
READ of size 8 at 0x7edd41054f80 thread T0 (chrome)
    #0 0x55f97d454d06 in GetRaw ./../../third_party/blink/renderer/platform/heap/member.h:250:44
    #1 0x55f97d454d06 in operator blink::MediaStreamSource * ./../../third_party/blink/renderer/platform/heap/member.h:184:32
    #2 0x55f97d454d06 in Construct<blink::MemberBase<blink::MediaStreamSource, blink::TracenessMemberConfiguration::kTraced>::AtomicCtorTag, const blink::Member<blink::MediaStreamSource> &> ./../../third_party/blink/renderer/platform/heap/member.h:514:26
    #3 0x55f97d454d06 in ConstructAndNotifyElement<const blink::Member<blink::MediaStreamSource> &> ./../../third_party/blink/renderer/platform/heap/member.h:528:9
    #4 0x55f97d454d06 in void WTF::Vector<blink::Member<blink::MediaStreamSource>, 0u, blink::HeapAllocator>::AppendSlowCase<blink::Member<blink::MediaStreamSource> const&>(blink::Member<blink::MediaStreamSource> const&) ./../../third_party/blink/renderer/platform/wtf/vector.h:1923:3
    #5 0x55f97d45473c in push_back<const blink::Member<blink::MediaStreamSource> &> ./../../third_party/blink/renderer/platform/wtf/vector.h:1873:3
    #6 0x55f97d45473c in std::__1::back_insert_iterator<blink::HeapVector<blink::Member<blink::MediaStreamSource>, 0u> >::operator=(blink::Member<blink::MediaStreamSource> const&) ./../../buildtools/third_party/libc++/trunk/include/iterator:835:21
    #7 0x55f97d43390b in copy_if<blink::Member<blink::MediaStreamSource> *, std::__1::back_insert_iterator<blink::HeapVector<blink::Member<blink::MediaStreamSource>, 0> >, (lambda at ../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:725:16)> ./../../buildtools/third_party/libc++/trunk/include/algorithm:1783:23
    #8 0x55f97d43390b in blink::UserMediaProcessor::DetermineExistingAudioSessionId() ./../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:723:3
    #9 0x55f97d43103e in blink::UserMediaProcessor::SetupVideoInput() ./../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:753:9
    #10 0x55f97d4328fd in blink::UserMediaProcessor::SelectAudioSettings(blink::UserMediaRequest*, WTF::Vector<blink::AudioDeviceCaptureCapability, 0u, WTF::PartitionAllocator> const&) ./../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:710:3
    #11 0x55f97d433305 in blink::UserMediaProcessor::SelectAudioDeviceSettings(blink::UserMediaRequest*, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>) ./../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:668:3
    #12 0x55f97d453582 in void base::internal::FunctorTraits<void (blink::UserMediaProcessor::*)(blink::UserMediaRequest*, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>), void>::Invoke<void (blink::UserMediaProcessor::*)(blink::UserMediaRequest*, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>), blink::WeakPersistent<blink::UserMediaProcessor>, blink::Persistent<blink::UserMediaRequest>, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator> >(void (blink::UserMediaProcessor::*)(blink::UserMediaRequest*, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>), blink::WeakPersistent<blink::UserMediaProcessor>&&, blink::Persistent<blink::UserMediaRequest>&&, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>&&) ./../../base/bind_internal.h:498:12
    #13 0x55f96a2a079c in Run ./../../base/callback.h:99:12
    #14 0x55f96a2a079c in blink::mojom::blink::MediaDevicesDispatcherHost_GetAudioInputCapabilities_ForwardToCallback::Accept(mojo::Message*) ./gen/third_party/blink/public/mojom/mediastream/media_devices.mojom-blink.cc:1186:26
    #15 0x55f96f0b6e0e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:549:23
    #16 0x55f96f0c3186 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #17 0x55f96f0ceda5 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #18 0x55f96f0cd57b in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #19 0x55f96f0c3186 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #20 0x55f96f0b010e in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:509:49
    #21 0x55f96f0b1a6b in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:567:14
    #22 0x55f96f115a43 in Run ./../../base/callback.h:133:12
    #23 0x55f96f115a43 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:292:14
    #24 0x55f96eb32625 in Run ./../../base/callback.h:99:12
    #25 0x55f96eb32625 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #26 0x55f96eb6bd3f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:331:23
    #27 0x55f96eb6b5bf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:251:36
    #28 0x55f96ea68c20 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #29 0x55f96eb6d0a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:445:12
    #30 0x55f96eae09ea in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #31 0x55f9800ee012 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:230:16
    #32 0x55f96d9ed4af in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:503:14
    #33 0x55f96d9f0988 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:883:10
    #34 0x55f96db8eb4d in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:453:29
    #35 0x55f96d9eb93f in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #36 0x55f963bd1e83 in ChromeMain ./../../chrome/app/chrome_main.cc:117:12
    #37 0x7f089cffab96 in __libc_start_main /build/glibc-2ORdQG/glibc-2.27/csu/../csu/libc-start.c:310:0

Address 0x7edd41054f80 is a wild pointer.
HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow (/home/cowboy/asan-linux-release/chrome+0x23135d06)
Shadow bytes around the buggy address:
  0x0fdc282029a0: f7 f7 f7 f7 f7 00 00 00 00 00 00 f7 f7 f7 f7 f7
  0x0fdc282029b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdc282029c0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdc282029d0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdc282029e0: f7 f7 f7 f7 f7 f7 00 f7 f7 f7 00 f7 f7 f7 f7 f7
=>0x0fdc282029f0:[fc]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdc28202a00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdc28202a10: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdc28202a20: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdc28202a30: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdc28202a40: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==1==ABORTING
Received signal 6
    #0 0x55f963b6225b in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4176:13
    #1 0x55f96ec0a639 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:840:39
    #2 0x55f96ea19a73 in StackTrace ./../../base/debug/stack_trace.cc:206:12
    #3 0x55f96ea19a73 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:203:28
    #4 0x55f96ec0922e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345:3
    #5 0x7f08a44e48a0 in __funlockfile ??:?
    #6 0x7f08a44e48a0 in ?? ??:0
    #7 0x7f089d017f47 in __libc_signal_restore_set /build/glibc-2ORdQG/glibc-2.27/signal/../sysdeps/unix/sysv/linux/nptl-signals.h:80:0
    #8 0x7f089d017f47 in raise /build/glibc-2ORdQG/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:48:0
    #9 0x7f089d0198b1 in abort /build/glibc-2ORdQG/glibc-2.27/stdlib/abort.c:79:0
    #10 0x55f963bbe747 in __sanitizer::Abort() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:161:3
    #11 0x55f963bbd2c1 in __sanitizer::Die() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58:5
    #12 0x55f963ba97e4 in __asan::ScopedInErrorReport::~ScopedInErrorReport() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:189:7
    #13 0x55f963bab1ce in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:477:1
    #14 0x55f963baba88 in __asan_report_load8 /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:120:1
    #15 0x55f97d454d07 in GetRaw ./../../third_party/blink/renderer/platform/heap/member.h:250:44
    #16 0x55f97d454d07 in operator blink::MediaStreamSource * ./../../third_party/blink/renderer/platform/heap/member.h:184:32
    #17 0x55f97d454d07 in Construct<blink::MemberBase<blink::MediaStreamSource, blink::TracenessMemberConfiguration::kTraced>::AtomicCtorTag, const blink::Member<blink::MediaStreamSource> &> ./../../third_party/blink/renderer/platform/heap/member.h:514:26
    #18 0x55f97d454d07 in ConstructAndNotifyElement<const blink::Member<blink::MediaStreamSource> &> ./../../third_party/blink/renderer/platform/heap/member.h:528:9
    #19 0x55f97d454d07 in void WTF::Vector<blink::Member<blink::MediaStreamSource>, 0u, blink::HeapAllocator>::AppendSlowCase<blink::Member<blink::MediaStreamSource> const&>(blink::Member<blink::MediaStreamSource> const&) ./../../third_party/blink/renderer/platform/wtf/vector.h:1923:3
    #20 0x55f97d45473d in push_back<const blink::Member<blink::MediaStreamSource> &> ./../../third_party/blink/renderer/platform/wtf/vector.h:1873:3
    #21 0x55f97d45473d in std::__1::back_insert_iterator<blink::HeapVector<blink::Member<blink::MediaStreamSource>, 0u> >::operator=(blink::Member<blink::MediaStreamSource> const&) ./../../buildtools/third_party/libc++/trunk/include/iterator:835:21
    #22 0x55f97d43390c in copy_if<blink::Member<blink::MediaStreamSource> *, std::__1::back_insert_iterator<blink::HeapVector<blink::Member<blink::MediaStreamSource>, 0> >, (lambda at ../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:725:16)> ./../../buildtools/third_party/libc++/trunk/include/algorithm:1783:23
    #23 0x55f97d43390c in blink::UserMediaProcessor::DetermineExistingAudioSessionId() ./../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:723:3
    #24 0x55f97d43103f in blink::UserMediaProcessor::SetupVideoInput() ./../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:753:9
    #25 0x55f97d4328fe in blink::UserMediaProcessor::SelectAudioSettings(blink::UserMediaRequest*, WTF::Vector<blink::AudioDeviceCaptureCapability, 0u, WTF::PartitionAllocator> const&) ./../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:710:3
    #26 0x55f97d433306 in blink::UserMediaProcessor::SelectAudioDeviceSettings(blink::UserMediaRequest*, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>) ./../../third_party/blink/renderer/modules/mediastream/user_media_processor.cc:668:3
    #27 0x55f97d453583 in void base::internal::FunctorTraits<void (blink::UserMediaProcessor::*)(blink::UserMediaRequest*, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>), void>::Invoke<void (blink::UserMediaProcessor::*)(blink::UserMediaRequest*, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>), blink::WeakPersistent<blink::UserMediaProcessor>, blink::Persistent<blink::UserMediaRequest>, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator> >(void (blink::UserMediaProcessor::*)(blink::UserMediaRequest*, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>), blink::WeakPersistent<blink::UserMediaProcessor>&&, blink::Persistent<blink::UserMediaRequest>&&, WTF::Vector<mojo::StructPtr<blink::mojom::blink::AudioInputDeviceCapabilities>, 0u, WTF::PartitionAllocator>&&) ./../../base/bind_internal.h:498:12
    #28 0x55f96a2a079d in Run ./../../base/callback.h:99:12
    #29 0x55f96a2a079d in blink::mojom::blink::MediaDevicesDispatcherHost_GetAudioInputCapabilities_ForwardToCallback::Accept(mojo::Message*) ./gen/third_party/blink/public/mojom/mediastream/media_devices.mojom-blink.cc:1186:26
    #30 0x55f96f0b6e0f in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:549:23
    #31 0x55f96f0c3187 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #32 0x55f96f0ceda6 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #33 0x55f96f0cd57c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #34 0x55f96f0c3187 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #35 0x55f96f0b010f in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:509:49
    #36 0x55f96f0b1a6c in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:567:14
    #37 0x55f96f115a44 in Run ./../../base/callback.h:133:12
    #38 0x55f96f115a44 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:292:14
    #39 0x55f96eb32626 in Run ./../../base/callback.h:99:12
    #40 0x55f96eb32626 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #41 0x55f96eb6bd40 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:331:23
    #42 0x55f96eb6b5c0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:251:36
    #43 0x55f96ea68c21 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #44 0x55f96eb6d0a7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:445:12
    #45 0x55f96eae09eb in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #46 0x55f9800ee013 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:230:16
    #47 0x55f96d9ed4b0 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:503:14
    #48 0x55f96d9f0989 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:883:10
    #49 0x55f96db8eb4e in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:453:29
    #50 0x55f96d9eb940 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #51 0x55f963bd1e84 in ChromeMain ./../../chrome/app/chrome_main.cc:117:12
    #52 0x7f089cffab97 in __libc_start_main /build/glibc-2ORdQG/glibc-2.27/csu/../csu/libc-start.c:310:0
    #53 0x55f963b2ad6a in _start ??:0:0
  r8: 0000000000000000  r9: 00007ffdd1edbd40 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007ffdd1edccf8 r13: 00007ffdd1edcd00 r14: 00007ffdd1edcca0 r15: 000055f98312e288
  di: 0000000000000002  si: 00007ffdd1edbd40  bp: 00007ffdd1edccd0  bx: 000055f98309be18
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007f089d017f47  sp: 00007ffdd1edbd40
  ip: 00007f089d017f47 efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Chromium 86.0.4236.0  Channel: stable
OS Version: 20.04
Flash Version:

## Attachments

- [crash.zip](attachments/crash.zip) (application/octet-stream, 32.2 KB)
- [poc2.zip](attachments/poc2.zip) (application/octet-stream, 32.3 KB)

## Timeline

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5711406573355008.

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5112272325771264.

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5677312183435264.

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6287977814228992.

### va...@chromium.org (2020-08-17)

[Empty comment from Monorail migration]

[Monorail components: Blink>GetUserMedia]

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5651838733189120.

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5765979367342080.

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5688914769936384.

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5676159186042880.

### va...@chromium.org (2020-08-17)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-08-17)

[Empty comment from Monorail migration]

### va...@chromium.org (2020-08-17)

Adding Impact-HEAD since I've been unable to reproduce this and the report states 86.*

### em...@gmail.com (2020-08-18)

I modified the POC. Now it's very stable to repro. Please try crash2.html in the attachment.
According to  actual environment,  may need to modify the path of *.js files in the crash2.html.

### [Deleted User] (2020-08-18)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-08-27)

cc haraken@ for more context in the code review.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9fc47affa89b9daa044de206d683d31d5c424c01

commit 9fc47affa89b9daa044de206d683d31d5c424c01
Author: Guido Urdaneta <guidou@chromium.org>
Date: Fri Aug 28 05:28:28 2020

[getUserMedia] Use copy of MediaStreamSource in iteration

This CL makes a copy of the MediaStreamSource pointer stored
in |local_sources_| in UserMediaProcessor when iterating to
select the audio sources that match a specific device ID.

Drive-by: Add some thread-checker DCHECKs.

Bug: 1116903
Change-Id: Iae0b5bb2b17a70ad57d5d1b33200728c94788361
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2379779
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/master@{#802518}

[modify] https://crrev.com/9fc47affa89b9daa044de206d683d31d5c424c01/third_party/blink/renderer/modules/mediastream/user_media_processor.cc


### gu...@chromium.org (2020-08-28)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-29)

Your change meets the bar and is auto-approved for M86. Please go ahead and merge the CL to branch 4240 (refs/branch-heads/4240) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e6573ef3b53fd7f3c8ac2ef7ae2c5b7eaaa4df92

commit e6573ef3b53fd7f3c8ac2ef7ae2c5b7eaaa4df92
Author: Guido Urdaneta <guidou@chromium.org>
Date: Sun Aug 30 07:06:45 2020

[getUserMedia] Use copy of MediaStreamSource in iteration

This CL makes a copy of the MediaStreamSource pointer stored
in |local_sources_| in UserMediaProcessor when iterating to
select the audio sources that match a specific device ID.

Drive-by: Add some thread-checker DCHECKs.

(cherry picked from commit 9fc47affa89b9daa044de206d683d31d5c424c01)

Bug: 1116903
Change-Id: Iae0b5bb2b17a70ad57d5d1b33200728c94788361
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2379779
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#802518}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2384030
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#250}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/e6573ef3b53fd7f3c8ac2ef7ae2c5b7eaaa4df92/third_party/blink/renderer/modules/mediastream/user_media_processor.cc


### ad...@google.com (2020-08-31)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-09-08)

guidou@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-09-09)

OOB read, so setting to medium severity.

### gu...@chromium.org (2020-09-09)

Note that there is really no OOB read as far as I can tell. I suspect this was an Asan false positive, or some issue in Oilpan.
The fix consisted in doing the iteration differently, but, in principle, I saw nothing wrong in the original code.

### ad...@google.com (2020-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-09)

emilykim8708@gmail.com - Congratulations! The VRP panel has decided to award $2000 for this bug. Someone from our finance team will get in touch. How would you like to be credited in the Chrome release notes?

### ad...@google.com (2020-09-10)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-05)

Hello OP/emilykim@, we consider attachments/pocs included with reports to be an integral part of the report (https://bughunters.google.com/about/rules/5745167867576320), so I've undeleted them. Thank you! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1116903?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053100)*
