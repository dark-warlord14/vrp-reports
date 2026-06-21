# Heap OOB read in RTCRtpTransport

| Field | Value |
|-------|-------|
| **Issue ID** | [488803429](https://issues.chromium.org/issues/488803429) |
| **Status** | Verified |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebRTC>RtpTransport |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | he...@google.com |
| **Created** | 2026-03-02 |
| **Bounty** | $2,000.00 |

## Description

Note: this vulnerability requires `--enable-features=RTCRtpTransport`, which will be enabled by default soon.

## VULNERABILITY DETAILS

There is a heap OOB read in the WebRTC RTCRtpTransport send path. In third\_party/webrtc/pc/datagram\_connection\_internal.cc, DatagramConnectionInternal::SendSinglePacket checks only packet.payload[0] to classify RTP/RTCP, then unconditionally reads packet.payload[1] at line 304:

- `if (IsRtpOrRtcpPacket(packet.payload[0])) { ...`
- `if (PayloadTypeIsReservedForRtcp(ParsePayloadType(packet.payload[1]))) { ... }`

Crash log:

```
=================================================================
==1443148==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b4145d383f1 at pc 0x7f21ab226a52 bp 0x7b207cd6b210 sp 0x7b207cd6b208
READ of size 1 at 0x7b4145d383f1 thread T9 (RtcTransport_ne)
    #0 0x7f21ab226a51 in webrtc::DatagramConnectionInternal::SendSinglePacket(webrtc::DatagramConnection::PacketSendParameters const&, bool) third_party/webrtc/pc/datagram_connection_internal.cc:304:55
    #1 0x7f21ab226183 in webrtc::DatagramConnectionInternal::SendPackets(webrtc::ArrayView<webrtc::DatagramConnection::PacketSendParameters, -4711l>) third_party/webrtc/pc/datagram_connection_internal.cc:260:5
    #2 0x7f215ce00a47 in base::internal::Invoker<base::internal::FunctorTraits<blink::(anonymous namespace)::AsyncDatagramConnectionImpl::SendPackets(std::__Cr::unique_ptr<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>, std::__Cr::default_delete<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>>>)::'lambda'(webrtc::scoped_refptr<webrtc::DatagramConnection>, std::__Cr::unique_ptr<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>, std::__Cr::default_delete<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>>>)&&, webrtc::scoped_refptr<webrtc::DatagramConnection>&&, std::__Cr::unique_ptr<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>, std::__Cr::default_delete<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>>>&&>, base::internal::BindState<false, false, false, blink::(anonymous namespace)::AsyncDatagramConnectionImpl::SendPackets(std::__Cr::unique_ptr<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>, std::__Cr::default_delete<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>>>)::'lambda'(webrtc::scoped_refptr<webrtc::DatagramConnection>, std::__Cr::unique_ptr<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>, std::__Cr::default_delete<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>>>), webrtc::scoped_refptr<webrtc::DatagramConnection>, std::__Cr::unique_ptr<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>, std::__Cr::default_delete<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>>>>, void ()>::RunOnce(base::internal::BindStateBase*) third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport.cc:201:36
    #3 0x7f21c46c9ed2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #4 0x7f21c474b3ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #5 0x7f21c474a3a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #6 0x7f21c456bea1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #7 0x7f21c474ca48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #8 0x7f21c4634512 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #9 0x7f21c47e2c62 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #10 0x7f21c47e3222 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #11 0x7f21c484725c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #12 0x55f2cdd7b146 in asan_thread_start(void*) asan_interceptors.cpp

0x7b4145d383f1 is located 0 bytes after 1-byte region [0x7b4145d383f0,0x7b4145d383f1)
allocated by thread T0 (chrome) here:
    #0 0x55f2cdd7d824 in malloc (/mnt/lvm_data/chromium/src/out/asan_nodcheck/chrome+0x6835824) (BuildId: f667536c8ff65a4b)
    #1 0x7f21c40ee6ff in void* partition_alloc::PartitionRoot::Alloc<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*) base/allocator/partition_allocator/src/partition_alloc/partition_root.h:2283:49
    #2 0x7f215b8e08f1 in blink::VectorBufferBase<unsigned char, blink::PartitionAllocator>::AllocateBufferNoBarrier(unsigned int) third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:42:9
    #3 0x7f215cdf4051 in blink::Vector<unsigned char, 0u, blink::PartitionAllocator>::Vector<base::span<unsigned char, 18446744073709551615ul, unsigned char*>, std::__Cr::identity>(T&&, std::__Cr::identity) third_party/blink/renderer/platform/wtf/vector.h:472:5
    #4 0x7f215cdf195e in blink::RtcTransport::sendPackets(blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, cppgc::internal::BasicMember<blink::RtcSendPacketParameters, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>) third_party/blink/renderer/platform/wtf/construct_traits.h:29:9
    #5 0x7f215b2c90e5 in blink::(anonymous namespace)::v8_rtc_transport::SendPacketsOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_transport.cc:288:17
    #6 0x7b2117dd06a3  (<unknown module>)
    #7 0x7b2117dce83b  (<unknown module>)
    #8 0x7b2117e1356d  (<unknown module>)
    #9 0x7b2117f01a29  (<unknown module>)
    #10 0x7b2117e01392  (<unknown module>)
    #11 0x7b2117dcb52a  (<unknown module>)
    #12 0x7f2162ef548d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #13 0x7f2162ef7689 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:534:18
    #14 0x7f2162ef7a8f in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*) v8/src/execution/execution.cc:638:10
    #15 0x7f2162fa01fc in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) v8/src/execution/microtask-queue.cc:185:22
    #16 0x7f2162fa1e90 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) v8/src/execution/microtask-queue.cc:129:3
    #17 0x7f216aa093df in blink::scheduler::EventLoop::PerformMicrotaskCheckpoint() third_party/blink/renderer/platform/scheduler/common/event_loop.cc:80:21
    #18 0x7f216aa3fc46 in blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint() third_party/blink/renderer/platform/scheduler/main_thread/agent_group_scheduler_impl.cc:117:12
    #19 0x7f216aa8313a in blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint() third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:1349:28
    #20 0x7f216aa94cef in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue>, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:2687:3
    #21 0x7f216aab4af9 in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) third_party/blink/renderer/platform/scheduler/main_thread/main_thread_task_queue.cc:140:29
    #22 0x7f216aab8486 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::* const&)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), blink::scheduler::MainThreadTaskQueue*>, base::internal::BindState<true, true, false, void (blink::scheduler::MainThreadTaskQueue::*)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::internal::BindStateBase*, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) base/functional/bind_internal.h:740:12
    #23 0x7f21c471f3ef in base::RepeatingCallback<void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) const & base/functional/callback.h:346:12
    #24 0x7f21c46ef580 in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::LazyNow*) base/task/sequence_manager/sequence_manager_impl.cc:852:35
    #25 0x7f21c46ef183 in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(base::LazyNow&) base/task/sequence_manager/sequence_manager_impl.cc:602:3
    #26 0x7f21c474b55f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:491:37
    #27 0x7f21c474a3a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #28 0x7f21c456bea1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #29 0x7f21c474ca48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12

Thread T9 (RtcTransport_ne) created by T0 (chrome) here:
    #0 0x55f2cdd60f71 in pthread_create (/mnt/lvm_data/chromium/src/out/asan_nodcheck/chrome+0x6818f71) (BuildId: f667536c8ff65a4b)
    #1 0x7f21c484691c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x7f21c47e17f0 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:228:26
    #3 0x7f215ce11358 in blink::RtcTransportProcessWideDeps::RtcTransportProcessWideDeps() third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport_dependencies.cc:77:21
    #4 0x7f215ce0a60a in blink::StaticSingleton<blink::RtcTransportProcessWideDeps>::StaticSingleton<blink::ProcessWideDeps()::$_0, blink::ProcessWideDeps()::$_1>(blink::ProcessWideDeps()::$_0 const&, blink::ProcessWideDeps()::$_1 const&) third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport_dependencies.cc:102:3
    #5 0x7f215ce0be75 in blink::RtcTransportDependencies::RtcTransportDependencies(blink::ExecutionContext&, base::PassKey<blink::RtcTransportDependencies>) third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport_dependencies.cc:102:3
    #6 0x7f215ce0aab5 in blink::RtcTransportDependencies::GetInitialized(blink::ExecutionContext&, base::OnceCallback<void (blink::RtcTransportDependencies*)>) v8/include/cppgc/allocation.h:239:32
    #7 0x7f215cded85f in blink::RtcTransport::Create(blink::ExecutionContext*, blink::RtcTransportConfig const*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport.cc:256:3
    #8 0x7f215b2c77fc in blink::(anonymous namespace)::v8_rtc_transport::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_transport.cc:213:23
    #9 0x7f2162bd4a6a in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) v8/src/api/api-arguments-inl.h:176:3
    #10 0x7f2162bd177e in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:117:27
    #11 0x7b2117e7fc75  (<unknown module>)
    #12 0x7b2117dcf169  (<unknown module>)
    #13 0x7b2117f89817  (<unknown module>)
    #14 0x7b2117dce83b  (<unknown module>)
    #15 0x7b2117dcb5db  (<unknown module>)
    #16 0x7b2117dcb32a  (<unknown module>)
    #17 0x7f2162ef5711 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #18 0x7f2162ef305e in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) v8/src/execution/execution.cc:564:10
    #19 0x7f2162aca0ea in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:5582:27
    #20 0x7f2171704630 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:855:48
    #21 0x7f2171551a7b in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:126:12
    #22 0x7f2175d610bb in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:73:13
    #23 0x7f2175d62493 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:133:15
    #24 0x7f2174c7e079 in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/blink/renderer/core/scheduler/scheduled_action.cc:145:18
    #25 0x7f2174c76867 in blink::DOMTimer::Fired() third_party/blink/renderer/core/scheduler/dom_timer.cc:446:11
    #26 0x7f216a580d65 in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:166:3
    #27 0x7f2173b7880c in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #28 0x7f21c46c9ed2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #29 0x7f21c474b3ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #30 0x7f21c474a3a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #31 0x7f21c456bea1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #32 0x7f21c474ca48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #33 0x7f21c4634512 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #34 0x7f21ba313bfe in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #35 0x7f21ba7460b7 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #36 0x7f21ba74721f in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #37 0x7f21ba74980a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #38 0x7f21ba743f53 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #39 0x7f21ba7442ea in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #40 0x55f2cddb8345 in ChromeMain chrome/app/chrome_main.cc:191:12
    #41 0x7f2154815d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/webrtc/pc/datagram_connection_internal.cc:304:55 in webrtc::DatagramConnectionInternal::SendSinglePacket(webrtc::DatagramConnection::PacketSendParameters const&, bool)
Shadow bytes around the buggy address:
  0x7b4145d38100: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa
  0x7b4145d38180: f7 fa 00 fa f7 fa 00 fa f7 fa 00 00 f7 fa 00 00
  0x7b4145d38200: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x7b4145d38280: f7 fa fd fd f7 fa fd fd f7 fa fd fa f7 fa 00 fa
  0x7b4145d38300: f7 fa 00 fa f7 fa 00 fa f7 fa fd fa f7 fa fd fa
=>0x7b4145d38380: f7 fa fd fa f7 fa 00 00 f7 fa 00 00 f7 fa[01]fa
  0x7b4145d38400: f7 fa fd fa f7 fa 00 00 f7 fa 00 00 f7 fa 01 fa
  0x7b4145d38480: f7 fa 00 00 f7 fa 00 00 f7 fa 03 fa f7 fa 00 00
  0x7b4145d38500: f7 fa 00 00 f7 fa 01 fa f7 fa 00 00 f7 fa 00 00
  0x7b4145d38580: f7 fa 01 fa f7 fa 00 00 f7 fa 00 00 f7 fa 01 fa
  0x7b4145d38600: f7 fa 00 00 f7 fa 00 00 f7 fa 03 fa f7 fa 00 00
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

==1443148==ADDITIONAL INFO

==1443148==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7f215cdfcf2d in blink::(anonymous namespace)::AsyncDatagramConnectionImpl::SendPackets(std::__Cr::unique_ptr<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>, std::__Cr::default_delete<blink::Vector<blink::Vector<unsigned char, 0u, blink::PartitionAllocator>, 0u, blink::PartitionAllocator>>>) third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport.cc:191:57


```
## VERSION

Chrome Version: Chromium 147.0.7703.0 + dev (local ASan source build)

Operating System: Ubuntu 22.04.3 LTS (Jammy Jellyfish), kernel 5.15.0-151-generic, x86\_64

## REPRODUCTION CASE

This weirdly can only be reproduced on a no DCHECK release + ASAN build. Just open the HTML with Chrome running with `--enable-features=RTCRtpTransport` a few times, sometimes it leads to nullptr dereference and sometimes heap buffer overflow.

Type of crash: tab/renderer

## CREDIT INFORMATION

Reporter credit: heapracer (@heapracer)

## Attachments

- [rtcrtp.html](attachments/rtcrtp.html) (text/html, 7.8 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4994201863258112.

### sh...@gmail.com (2026-03-05)

Looks like clusterfuzz hits the DCHECK. To reproduce, DCHECK needs to be disabled.

### ct...@chromium.org (2026-03-05)

It appears to be hitting a span size check (hardening assertion) in <https://webrtc.googlesource.com/src/+/9b43041fb76ae6f895f8c721165a3fdedbcfa550/pc/datagram_connection_internal.cc?pli=1#260>

```
gen/third_party/libc++/src/include/span:537: libc++ Hardening assertion __idx < size() failed: span<T>::operator[](index): index out of range

```

I'll try manually repro-ing tomorrow.

If you are able to make a more stable repro for the OOB read, that would also be helpful.

### 24...@project.gserviceaccount.com (2026-03-05)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-05)

Automatically assigning owner based on suspected regression changelist https://webrtc.googlesource.com/src/+/b70b78f732decdcdb2f4b462a836df7712b8aefe (Allow DatagramConnection (ie the RtcTransport web API) to send and receive real SRTP/SCTP

When wire protocol is set to kDtlsSrtp, take RTP/RTCP packets passed
to sendPackets and SRTP encrypt them in the same way as they would be
in a full PeerConnection, without the goofy wrapping in faked RTP
headers. Similarly decrypt received SRTP/SRTCP packets, decrypt them and
pass up to the client with the original headers inc seq num, ssrc etc.
For any other packets, just DTLS encrypt/decrypt, as in SrtpTransport.

This allows users of DatagramConnection to be wire-compatible with
a standard peerconnection.

Bug: chromium:443019066
Change-Id: I3bc3597b84b14fb03f3e7b6668638df0a5d86ef3
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/421782
Commit-Queue: Tony Herre <herre@google.com>
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#46240}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2026-03-05)

Detailed Report: https://clusterfuzz.com/testcase?key=4994201863258112

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Abrt
Crash Address: 0x053900000001
Crash State:
  webrtc::DatagramConnectionInternal::SendPackets
  base::TaskAnnotator::RunTaskImpl
  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImp
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1547883:1547900

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4994201863258112

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ct...@chromium.org (2026-03-06)

[security shepherd]

I am able to manually repro on Linux ASAN dev (M147) and ASAN stable (M145) using the supplied POC, triggering the heap-buffer-overflow. Clusterfuzz seems to be mainly hitting the abort, which is less interesting.

Renderer OOB read -> S2

### he...@google.com (2026-03-06)

Thanks for the report!

As stated at the top of #1, this is gated by the feature RTCRtpTransport, unlaunched everywhere, with no firm launch timeline, so priority isn't too high. I'll work on a fix.

### dx...@google.com (2026-03-10)

Project: src  

Branch:  main  

Author:  Tony Herre [herre@google.com](mailto:herre@google.com)  

Link:    <https://webrtc-review.googlesource.com/454280>

Check RtcTransport payload isn't too short before checking it's an RTP packet

---


Expand for full commit details
```
     
    Bug: chromium:488803429 
    Change-Id: Iaf6204c1f3bce1a8786c00ecfa7faabe78bb9021 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454280 
    Auto-Submit: Tony Herre <herre@google.com> 
    Reviewed-by: Stefan Holmer <stefan@webrtc.org> 
    Commit-Queue: Stefan Holmer <stefan@webrtc.org> 
    Reviewed-by: Philip Eliasson <philipel@webrtc.org> 
    Cr-Commit-Position: refs/heads/main@{#47101}

```

---

Files:

- M `pc/datagram_connection_internal.cc`
- M `pc/datagram_connection_unittest.cc`

---

Hash: 4a6be3888874f6412cb0b24fcacd5f4b59af5f1a  

Date: Fri Mar 6 11:32:08 2026


---

### dx...@google.com (2026-03-10)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7652958>

Roll WebRTC from 96625b9b4888 to 4a6be3888874 (2 revisions)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/96625b9b4888..4a6be3888874 
     
    2026-03-10 herre@google.com Check RtcTransport payload isn't too short before checking it's an RTP packet 
    2026-03-10 grulja@gmail.com PipeWire: call pw_deinit() only when running against PipeWire 3.49+ 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/webrtc-chromium-autoroll 
    Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:488803429,chromium:490340738 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: I198c1354da7e5431a7ab176d80fe545ce1568bbb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7652958 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1597028}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: [a43951bbd9041f5883d2fd0960be896242a41d44](https://chromiumdash.appspot.com/commit/a43951bbd9041f5883d2fd0960be896242a41d44)  

Date: Tue Mar 10 13:47:10 2026


---

### 24...@project.gserviceaccount.com (2026-03-11)

ClusterFuzz testcase 4994201863258112 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1597026:1597030

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488803429)*
