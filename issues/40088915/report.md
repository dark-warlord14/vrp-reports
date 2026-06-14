# Security: heap-use-after-free in WebAudio

| Field | Value |
|-------|-------|
| **Issue ID** | [40088915](https://issues.chromium.org/issues/40088915) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | li...@gmail.com |
| **Assignee** | bi...@chromium.org |
| **Created** | 2017-09-04 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0

Steps to reproduce the problem:
1. browse the attached file

What is the expected behavior?

What went wrong?
==28908==ERROR: AddressSanitizer: heap-use-after-free on address 0x6020000be6d0 at pc 0x5555570df6f5 bp 0x7fffffff8130 sp 0x7fffffff78e0
READ of size 4 at 0x6020000be6d0 thread T0 (chrome)
    #0 0x5555570df6f4 in __asan_memcpy (/media/disk2/Download/chromium/src/out/ASAN/chrome+0x1b8b6f4)
    #1 0x7fffb2d8da7a in blink::AudioBuffer::copyToChannel(blink::NotShared<blink::DOMTypedArray<WTF::Float32Array, v8::Float32Array> >, long, unsigned long, blink::ExceptionState&) third_party/WebKit/Source/modules/webaudio/AudioBuffer.cpp:333:3
    #2 0x7fffb1213cd5 in blink::AudioBufferV8Internal::copyToChannelMethod(v8::FunctionCallbackInfo<v8::Value> const&) /media/disk2/Download/chromium/src/out/ASAN/gen/blink/bindings/modules/v8/V8AudioBuffer.cpp:204:9
    #3 0x7fffb1211fb9 in blink::V8AudioBuffer::copyToChannelMethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) /media/disk2/Download/chromium/src/out/ASAN/gen/blink/bindings/modules/v8/V8AudioBuffer.cpp:280:3
    #4 0x7fffc57bb493 in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:25:3
    #5 0x7fffc5a63ae1 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:112:36
    #6 0x7fffc5a5ffd2 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:142:5
    #7 0x7fffc5a5f26d in v8::internal::Builtin_HandleApiCall(int, v8::internal::Object**, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:130:1
    #8 0x7fff6b3845a3  (<unknown module>)
    #9 0x7fff6b48e29f  (<unknown module>)
    #10 0x7fff6b48b418  (<unknown module>)
    #11 0x7fff6b384100  (<unknown module>)
    #12 0x7fffc63bc618 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling) v8/src/execution.cc:145:13
    #13 0x7fffc63bb537 in v8::internal::(anonymous namespace)::CallInternal(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Execution::MessageHandling) v8/src/execution.cc:181:10
    #14 0x7fffc585bb54 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:5387:7
    #15 0x7fffbadf3bec in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:672:17
    #16 0x7fffbac6e7a9 in blink::ScheduledAction::Execute(blink::LocalFrame*) third_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:155:5
    #17 0x7fffbac6d411 in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:107:5
    #18 0x7fffbcbb274a in blink::DOMTimer::Fired() third_party/WebKit/Source/core/frame/DOMTimer.cpp:172:11
    #19 0x7fffb59d682c in blink::TimerBase::RunInternal() third_party/WebKit/Source/platform/Timer.cpp:174:3
    #20 0x7fffb59d9489 in void base::internal::FunctorTraits<void (blink::TimerBase::*)(), void>::Invoke<base::WeakPtr<blink::TimerBase> const&>(void (blink::TimerBase::*)(), base::WeakPtr<blink::TimerBase> const&) base/bind_internal.h:194:12
    #21 0x7fffb59d9188 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (blink::TimerBase::* const&)(), base::WeakPtr<blink::TimerBase> const&>(void (blink::TimerBase::* const&)(), base::WeakPtr<blink::TimerBase> const&) base/bind_internal.h:297:5
    #22 0x7fffb59d8f7f in void base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::*)(), base::WeakPtr<blink::TimerBase> >, void ()>::RunImpl<void (blink::TimerBase::* const&)(), std::__1::tuple<base::WeakPtr<blink::TimerBase> > const&, 0ul>(void (blink::TimerBase::* const&)(), std::__1::tuple<base::WeakPtr<blink::TimerBase> > const&, std::__1::integer_sequence<unsigned long, 0ul>) base/bind_internal.h:349:12
    #23 0x7fffb59d8ecb in base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::*)(), base::WeakPtr<blink::TimerBase> >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:331:12
    #24 0x7ffff66e4b6e in base::OnceCallback<void ()>::Run() && base/callback.h:64:12
    #25 0x7ffff67e5071 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:65:33
    #26 0x7fffb71e6fe2 in blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(blink::scheduler::internal::WorkQueue*, bool, blink::scheduler::LazyNow, base::TimeTicks*) third_party/WebKit/Source/platform/scheduler/base/task_queue_manager.cc:515:19
    #27 0x7fffb71d8902 in blink::scheduler::TaskQueueManager::DoWork(bool) third_party/WebKit/Source/platform/scheduler/base/task_queue_manager.cc:312:13
    #28 0x7fffb71ffadc in void base::internal::FunctorTraits<void (blink::scheduler::TaskQueueManager::*)(bool), void>::Invoke<base::WeakPtr<blink::scheduler::TaskQueueManager> const&, bool const&>(void (blink::scheduler::TaskQueueManager::*)(bool), base::WeakPtr<blink::scheduler::TaskQueueManager> const&, bool const&) base/bind_internal.h:194:12
    #29 0x7fffb71ff762 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (blink::scheduler::TaskQueueManager::* const&)(bool), base::WeakPtr<blink::scheduler::TaskQueueManager> const&, bool const&>(void (blink::scheduler::TaskQueueManager::* const&)(bool), base::WeakPtr<blink::scheduler::TaskQueueManager> const&, bool const&) base/bind_internal.h:297:5
    #30 0x7fffb71ff51c in void base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::*)(bool), base::WeakPtr<blink::scheduler::TaskQueueManager>, bool>, void ()>::RunImpl<void (blink::scheduler::TaskQueueManager::* const&)(bool), std::__1::tuple<base::WeakPtr<blink::scheduler::TaskQueueManager>, bool> const&, 0ul, 1ul>(void (blink::scheduler::TaskQueueManager::* const&)(bool), std::__1::tuple<base::WeakPtr<blink::scheduler::TaskQueueManager>, bool> const&, std::__1::integer_sequence<unsigned long, 0ul, 1ul>) base/bind_internal.h:349:12
    #31 0x7fffb71ff42b in base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::*)(bool), base::WeakPtr<blink::scheduler::TaskQueueManager>, bool>, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:331:12
    #32 0x7fffb59f6a8c in base::RepeatingCallback<void ()>::Run() const & base/callback.h:92:12
    #33 0x7fffb71884b8 in base::CancelableCallback<void ()>::Forward() const base/cancelable_callback.h:110:15
    #34 0x7fffb7188f19 in void base::internal::FunctorTraits<void (base::CancelableCallback<void ()>::*)() const, void>::Invoke<base::WeakPtr<base::CancelableCallback<void ()> > const&>(void (base::CancelableCallback<void ()>::*)() const, base::WeakPtr<base::CancelableCallback<void ()> > const&) base/bind_internal.h:209:12
    #35 0x7fffb7188c18 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (base::CancelableCallback<void ()>::* const&)() const, base::WeakPtr<base::CancelableCallback<void ()> > const&>(void (base::CancelableCallback<void ()>::* const&)() const, base::WeakPtr<base::CancelableCallback<void ()> > const&) base/bind_internal.h:297:5
    #36 0x7fffb7188a0f in void base::internal::Invoker<base::internal::BindState<void (base::CancelableCallback<void ()>::*)() const, base::WeakPtr<base::CancelableCallback<void ()> > >, void ()>::RunImpl<void (base::CancelableCallback<void ()>::* const&)() const, std::__1::tuple<base::WeakPtr<base::CancelableCallback<void ()> > > const&, 0ul>(void (base::CancelableCallback<void ()>::* const&)() const, std::__1::tuple<base::WeakPtr<base::CancelableCallback<void ()> > > const&, std::__1::integer_sequence<unsigned long, 0ul>) base/bind_internal.h:349:12
    #37 0x7fffb718895b in base::internal::Invoker<base::internal::BindState<void (base::CancelableCallback<void ()>::*)() const, base::WeakPtr<base::CancelableCallback<void ()> > >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:331:12
    #38 0x7ffff66e4b6e in base::OnceCallback<void ()>::Run() && base/callback.h:64:12
    #39 0x7ffff67e5071 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:65:33
    #40 0x7ffff69d37b9 in base::internal::IncomingTaskQueue::RunTask(base::PendingTask*) base/message_loop/incoming_task_queue.cc:143:19
    #41 0x7ffff69e05c4 in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:406:25
    #42 0x7ffff69e0de2 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message_loop/message_loop.cc:417:5
    #43 0x7ffff69e4d91 in base::MessageLoop::DoDelayedWork(base::TimeTicks*) base/message_loop/message_loop.cc:564:10
    #44 0x7ffff6a07ed2 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:37:27
    #45 0x7ffff69def40 in base::MessageLoop::Run() base/message_loop/message_loop.cc:346:10
    #46 0x7ffff6c2123c in base::RunLoop::Run() base/run_loop.cc:123:14
    #47 0x7fffe737c0fd in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:220:23
    #48 0x7fffe831e282 in content::RunNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:426:14
    #49 0x7fffe8325dbd in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:709:12
    #50 0x7fffe83175be in content::ContentServiceManagerMainDelegate::RunEmbedderProcess() content/app/content_service_manager_main_delegate.cc:51:32
    #51 0x7ffff797a2be in service_manager::Main(service_manager::MainParams const&) services/service_manager/embedder/main.cc:469:29
    #52 0x7fffe831bdac in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:10
    #53 0x55555710e893 in ChromeMain chrome/app/chrome_main.cc:122:12
    #54 0x55555710e4c1 in main chrome/app/chrome_exe_main_aura.cc:17:10
    #55 0x7fffa79d882f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

0x6020000be6d0 is located 0 bytes inside of 4-byte region [0x6020000be6d0,0x6020000be6d4)
freed by thread T0 (chrome) here:
    #0 0x5555570e0182 in __interceptor_free (/media/disk2/Download/chromium/src/out/ASAN/chrome+0x1b8c182)
    #1 0x7fffc7fcec18 in base::PartitionFreeGeneric(base::PartitionRootGeneric*, void*) base/allocator/partition_allocator/partition_alloc.h:818:3
    #2 0x7fffc81146bc in WTF::ArrayBufferContents::FreeMemory(void*) third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:160:3
    #3 0x7fffc81159ef in WTF::ArrayBufferContents::DataHandle::~DataHandle() third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.h:99:11
    #4 0x7fffc8114cb9 in WTF::ArrayBufferContents::DataHolder::~DataHolder() third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:194:1
    #5 0x7fffc81177f6 in WTF::ThreadSafeRefCounted<WTF::ArrayBufferContents::DataHolder>::Deref() third_party/WebKit/Source/platform/wtf/ThreadSafeRefCounted.h:63:7
    #6 0x7fffc81177a0 in void WTF::DerefIfNotNull<WTF::ArrayBufferContents::DataHolder>(WTF::ArrayBufferContents::DataHolder*) third_party/WebKit/Source/platform/wtf/PassRefPtr.h:60:10
    #7 0x7fffc8115b1c in WTF::RefPtr<WTF::ArrayBufferContents::DataHolder>::~RefPtr() third_party/WebKit/Source/platform/wtf/RefPtr.h:78:29
    #8 0x7fffc8113054 in WTF::ArrayBufferContents::~ArrayBufferContents() third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:90:46
    #9 0x7fffbaea06d2 in WTF::ArrayBuffer::~ArrayBuffer() third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBuffer.h:85:19
    #10 0x7fffbaea0696 in WTF::RefCounted<WTF::ArrayBuffer>::Deref() const third_party/WebKit/Source/platform/wtf/RefCounted.h:150:7
    #11 0x7fffbaea0640 in void WTF::DerefIfNotNull<WTF::ArrayBuffer>(WTF::ArrayBuffer*) third_party/WebKit/Source/platform/wtf/PassRefPtr.h:60:10
    #12 0x7fffbae9f7ac in WTF::RefPtr<WTF::ArrayBuffer>::~RefPtr() third_party/WebKit/Source/platform/wtf/RefPtr.h:78:29
    #13 0x7fffbaea02c9 in blink::DOMArrayBufferBase::~DOMArrayBufferBase() third_party/WebKit/Source/core/typed_arrays/DOMArrayBufferBase.h:19:34
    #14 0x7fffbf8156b4 in blink::DOMArrayBuffer::~DOMArrayBuffer() third_party/WebKit/Source/core/typed_arrays/DOMArrayBuffer.h:16:19
    #15 0x7fffb03d8c5d in blink::GarbageCollectedFinalized<blink::DOMArrayBufferBase>::FinalizeGarbageCollectedObject() third_party/WebKit/Source/platform/heap/GarbageCollected.h:224:67
    #16 0x7fffb03d8be4 in blink::FinalizerTraitImpl<blink::DOMArrayBufferBase, true>::Finalize(void*) third_party/WebKit/Source/platform/heap/GCInfo.h:36:27
    #17 0x7fffb03d8bc4 in blink::FinalizerTrait<blink::DOMArrayBufferBase>::Finalize(void*) third_party/WebKit/Source/platform/heap/GCInfo.h:62:5
    #18 0x7fffb6f6259a in blink::HeapObjectHeader::Finalize(unsigned char*, unsigned long) third_party/WebKit/Source/platform/heap/HeapPage.cpp:100:5
    #19 0x7fffb6f76987 in blink::NormalPage::Sweep() third_party/WebKit/Source/platform/heap/HeapPage.cpp:1342:15
    #20 0x7fffb6f666c2 in blink::BaseArena::SweepUnsweptPage() third_party/WebKit/Source/platform/heap/HeapPage.cpp:281:11
    #21 0x7fffb6f6747f in blink::BaseArena::CompleteSweep() third_party/WebKit/Source/platform/heap/HeapPage.cpp:335:5
    #22 0x7fffb6f93be1 in blink::ThreadState::CompleteSweep() third_party/WebKit/Source/platform/heap/ThreadState.cpp:993:17
    #23 0x7fffb6f72374 in blink::NormalPageArena::OutOfLineAllocate(unsigned long, unsigned long) third_party/WebKit/Source/platform/heap/HeapPage.cpp:920:21
    #24 0x7fffbab6114b in blink::NormalPageArena::AllocateObject(unsigned long, unsigned long) third_party/WebKit/Source/platform/heap/HeapPage.h:1023:10
    #25 0x7fffbab5f882 in blink::ThreadHeap::AllocateOnArenaIndex(blink::ThreadState*, unsigned long, int, unsigned long, char const*) third_party/WebKit/Source/platform/heap/Heap.h:601:14
    #26 0x7fffbac57967 in unsigned char* blink::ThreadHeap::Allocate<blink::Event>(unsigned long, bool) third_party/WebKit/Source/platform/heap/Heap.h:610:10
    #27 0x7fffbac578e4 in blink::GarbageCollected<blink::Event>::AllocateObject(unsigned long, bool) third_party/WebKit/Source/platform/heap/Heap.h:510:12
    #28 0x7fffbac578b6 in blink::GarbageCollected<blink::Event>::operator new(unsigned long) third_party/WebKit/Source/platform/heap/Heap.h:506:12
    #29 0x7fffbbe617d3 in blink::VisualViewportResizeEvent::Create() third_party/WebKit/Source/core/events/VisualViewportResizeEvent.h:17:12

previously allocated by thread T0 (chrome) here:
    #0 0x5555570e04c3 in __interceptor_malloc (/media/disk2/Download/chromium/src/out/ASAN/chrome+0x1b8c4c3)
    #1 0x7fffc7fcea42 in base::PartitionAllocGenericFlags(base::PartitionRootGeneric*, int, unsigned long, char const*) base/allocator/partition_allocator/partition_alloc.h:792:18
    #2 0x7fffc81145b0 in WTF::ArrayBufferContents::AllocateMemoryWithFlags(unsigned long, WTF::ArrayBufferContents::InitializationPolicy, int) third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:117:16
    #3 0x7fffc811460f in WTF::ArrayBufferContents::AllocateMemoryOrNull(unsigned long, WTF::ArrayBufferContents::InitializationPolicy) third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:127:10
    #4 0x7fffc81149da in WTF::ArrayBufferContents::CreateDataHandle(unsigned long, WTF::ArrayBufferContents::InitializationPolicy) third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:177:21
    #5 0x7fffc811205c in WTF::ArrayBufferContents::DataHolder::AllocateNew(unsigned int, WTF::ArrayBufferContents::SharingType, WTF::ArrayBufferContents::InitializationPolicy) third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:203:11
    #6 0x7fffc8111959 in WTF::ArrayBufferContents::ArrayBufferContents(unsigned int, unsigned int, WTF::ArrayBufferContents::SharingType, WTF::ArrayBufferContents::InitializationPolicy) third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:72:12
    #7 0x7fffb2d91aea in WTF::ArrayBuffer::CreateOrNull(unsigned int, unsigned int, WTF::ArrayBufferContents::InitializationPolicy) third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBuffer.h:179:23
    #8 0x7fffb2d91621 in WTF::ArrayBuffer::CreateOrNull(unsigned int, unsigned int) third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBuffer.h:153:10
    #9 0x7fffb2d91510 in WTF::RefPtr<WTF::Float32Array> WTF::TypedArrayBase<float>::CreateOrNull<WTF::Float32Array>(unsigned int) third_party/WebKit/Source/platform/wtf/typed_arrays/TypedArrayBase.h:96:34
    #10 0x7fffb2d8f2f9 in WTF::Float32Array::CreateOrNull(unsigned int) third_party/WebKit/Source/platform/wtf/typed_arrays/Float32Array.h:81:10
    #11 0x7fffb2d8afc6 in blink::AudioBuffer::CreateFloat32ArrayOrNull(unsigned long, blink::AudioBuffer::InitializationPolicy) third_party/WebKit/Source/modules/webaudio/AudioBuffer.cpp:165:16
    #12 0x7fffb2d8b4e3 in blink::AudioBuffer::AudioBuffer(unsigned int, unsigned long, float, blink::AudioBuffer::InitializationPolicy) third_party/WebKit/Source/modules/webaudio/AudioBuffer.cpp:190:9
    #13 0x7fffb2d89ee8 in blink::AudioBuffer::Create(unsigned int, unsigned long, float) third_party/WebKit/Source/modules/webaudio/AudioBuffer.cpp:52:11
    #14 0x7fffb2d8a589 in blink::AudioBuffer::Create(unsigned int, unsigned long, float, blink::ExceptionState&) third_party/WebKit/Source/modules/webaudio/AudioBuffer.cpp:94:7
    #15 0x7fffb2ed4b5d in blink::BaseAudioContext::createBuffer(unsigned int, unsigned long, float, blink::ExceptionState&) third_party/WebKit/Source/modules/webaudio/BaseAudioContext.cpp:239:25
    #16 0x7fffb1284298 in blink::BaseAudioContextV8Internal::createBufferMethod(v8::FunctionCallbackInfo<v8::Value> const&) /media/disk2/Download/chromium/src/out/ASAN/gen/blink/bindings/modules/v8/V8BaseAudioContext.cpp:216:31
    #17 0x7fffb1282df9 in blink::V8BaseAudioContext::createBufferMethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) /media/disk2/Download/chromium/src/out/ASAN/gen/blink/bindings/modules/v8/V8BaseAudioContext.cpp:770:3
    #18 0x7fffc57bb493 in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:25:3
    #19 0x7fffc5a63ae1 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:112:36
    #20 0x7fffc5a5ffd2 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:142:5
    #21 0x7fffc5a5f26d in v8::internal::Builtin_HandleApiCall(int, v8::internal::Object**, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:130:1
    #22 0x7fff6b3845a3  (<unknown module>)
    #23 0x7fff6b48e29f  (<unknown module>)
    #24 0x7fff6b48e29f  (<unknown module>)
    #25 0x7fff6b48e29f  (<unknown module>)
    #26 0x7fff6b48b418  (<unknown module>)
    #27 0x7fff6b384100  (<unknown module>)
    #28 0x7fffc63bc618 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling) v8/src/execution.cc:145:13
    #29 0x7fffc63bb537 in v8::internal::(anonymous namespace)::CallInternal(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Execution::MessageHandling) v8/src/execution.cc:181:10

SUMMARY: AddressSanitizer: heap-use-after-free (/media/disk2/Download/chromium/src/out/ASAN/chrome+0x1b8b6f4) in __asan_memcpy
Shadow bytes around the buggy address:
  0x0c048000fc80: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x0c048000fc90: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x0c048000fca0: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fd
  0x0c048000fcb0: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa
  0x0c048000fcc0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
=>0x0c048000fcd0: fa fa fd fd fa fa fd fd fa fa[fd]fa fa fa 04 fa
  0x0c048000fce0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x0c048000fcf0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x0c048000fd00: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa
  0x0c048000fd10: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x0c048000fd20: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
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
==28908==ABORTING

Did this work before? N/A 

Chrome version: 63.0.3205.0 (Developer Build) (64-bit)  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [min.html](attachments/min.html) (text/plain, 1.4 KB)

## Timeline

### do...@chromium.org (2017-09-04)

hongchan: can you please follow up on this? Looks like it needs an ASAN build to repro. Thanks!

[Monorail components: Blink>WebAudio]

### sh...@chromium.org (2017-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2017-09-05)

This is reproducible on OSX ASAN 63.0.3207.0.

### rt...@chromium.org (2017-09-05)

+binji, since you helped implement decodeAudioData neutering (transfering).

AFAIK, decodeAudioData neutering is working, but the repro case is a bit confusing.  It's basically doing this:

c0 = new AudioContext();
ab = c0.createBuffer(1,1,44100);
d = ab.getChannelData(0);
b = d.buffer;
c1 = new AudioContext();
c1.decodeAudioData(b);
ab.copyToChannel(b);

Since d is a reference to the actual underlying data in the AudioBuffer, the call to decodeAudioData will neuter b, and hence d and then the underlying array in AudioBuffer.

GC is deleting some ArrayBuffer while copyToChannel is running.  One thing I don't understand is why b has not been neutered so that the length of b is zero, which would make copyToChannel not do anything.


### bi...@chromium.org (2017-09-05)

Yeah, I was able to repro on Linux ASAN 63.0.3207.0 as well. I'll take a look.

### ho...@chromium.org (2017-09-05)

per #6, I am assigning this to binji@. Thanks for looking at this!

### bi...@chromium.org (2017-09-06)

OK, I think I understand the issue here. @rtoy, your rewrite is missing an important line, which is the second call to c1.decodeAudioData(b):

    c0 = new AudioContext();
    ab = c0.createBuffer(1,1,44100);
    d = ab.getChannelData(0);
    b = d.buffer;
    c1 = new AudioContext();
    c1.decodeAudioData(b);
    c1.decodeAudioData(b);
    ab.copyToChannel(b);

The trick is that the first c1.decodeAudioData call does not actually neuter b, because it can't. d is non-neuterable, so instead b is copied via ArrayBufferContents::CopyTo (See https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBuffer.cpp?l=33):

  if (all_views_are_neuterable) {
    contents_.Transfer(result);
  } else {
    contents_.CopyTo(result);
    if (!result.Data())
      return false;
  }

  while (first_view_) {
    ArrayBufferView* current = first_view_;
    RemoveView(current);
    if (all_views_are_neuterable || current->IsNeuterable())
      current->Neuter();
  }

After the data is copied, the original ArrayBuffer's views are all removed and neutered, but only if they are neuterable. The Float32Array is not neuterable so Neuter is not called on it. But it is still removed from the ArrayBuffer (via RemoveView). This removes it from the linked list.

The second time decodeAudioData is called, b is neuterable, since it no longer has any neuterable views (it was removed from the linked list the first time). So ArrayBufferContents::Transfer is called instead, which will clear this ArrayBuffer's contents (i.e. release the reference on its data).

The ArrayBufferContents is then transferred to the AsyncAudioDecoder, but the result of decodeAudioData is ignored. The blink gc eventually collects both ArrayBuffers created by decodeAudioData (see https://cs.chromium.org/chromium/src/third_party/WebKit/Source/modules/webaudio/BaseAudioContext.cpp?type=cs&l=325).

At this point, we have an ArrayBufferView that was not neutered (so it has non-zero length), but has a RefPtr to a neutered ArrayBuffer. Unfortunately, ArrayBufferView also has a cached baseAddress pointer. So when we call copyToChannel it uses the length (non-zero) and the data pointer (free'd because the ArrayBuffer was transferred to the async decoder) inside the call to memcpy (see https://cs.chromium.org/chromium/src/third_party/WebKit/Source/modules/webaudio/AudioBuffer.cpp?type=cs&q=copytochannel&l=333).

So I think the fix is to make sure that ArrayBuffer::Transfer doesn't neuter the arraybuffer views when the arraybuffer data is copied to a new ArrayBufferContents.

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### rt...@chromium.org (2017-09-06)

Thanks so much for the excellent analysis.  I'm a little confused about the paragraph talking about the result of decodeAudioData.  This does correctly reject the promise because the input buffers aren't valid encode audio files.

But in any case, the real fix is to modify ArrayBuffer::Transfer not to neuter the arraybuffer when the data is copied?

### rt...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### bi...@chromium.org (2017-09-06)

Yes, it rejects the promise in both cases. I just mean that nothing actually uses the promise... I realized now that this fact doesn't really matter though. The point is that the ArrayBuffer is transferred to the AsyncAudioDecoder, so the ArrayBuffer is destroyed when it's finished with it.

Yes, I think fixing ArrayBuffer::Transfer is correct. I don't believe neutering the arraybuffer is possible, since the ArrayBufferView is marked as non-neuterable (see https://cs.chromium.org/chromium/src/third_party/WebKit/Source/modules/webaudio/AudioBuffer.cpp?l=196).

### rt...@chromium.org (2017-09-06)

Also, while our implementation currently says an AudioBuffer can't be neutered, I'm not sure that's really compliant with the spec: https://webaudio.github.io/web-audio-api/#acquire-the-content

AudioBuffer's can be detached. Perhaps that's the appropriate fix here.  We haven't implemented this part of the spec yet.

### bi...@chromium.org (2017-09-06)

Haha, I was about to send you the same thing:

"Oh, perhaps you're right. It looks like the AudioBuffer's ArrayBuffers should be neuterable: https://webaudio.github.io/web-audio-api/#acquire-the-content

It's also worth noting that AudioBuffer seems to be the only example where SetNeuterable(false) is used: https://cs.chromium.org/search/?q=setneuterable&sq=package:chromium&type=cs"

### rt...@chromium.org (2017-09-06)

Heh.

Yeah, that was done long before my time on WebAudio.  I'm guessing the original author didn't want to take the hit if someone neutered the array while the AudioBufferSourceNode was in the middle of playing out the AudioBuffer.

Anyway, commenting out just that one line makes asan happy. I now get the error message:

min.html:28 Uncaught DOMException: Failed to execute 'copyToChannel' on 'AudioBuffer': The startInChannel provided (0) is outside the range [0, 0).
    at bang (http://localhost:7001/761801/min.html:28:24)

which makes sense.

I think this is a suitable fix for this issue, and something that we could merge to beta. I don't know what other implications this might have if we do just this little fix.

I think fixing all of the AudioBuffer detaching would be too big a CL to merge to beta. (But I haven't looked to see what it would take.)

### bi...@chromium.org (2017-09-06)

> Yeah, that was done long before my time on WebAudio.

I found the original commit: https://chromiumcodereview.appspot.com/19019002/. It was landed to fix this bug: https://bugs.chromium.org/p/chromium/issues/detail?id=254728.

> Anyway, commenting out just that one line makes asan happy.

Which line? The one to mark the arraybuffer as non-neuterable?

> I think fixing all of the AudioBuffer detaching would be too big a CL to merge to beta.

I think you're right. It would be good to have something more localized.

### rt...@chromium.org (2017-09-06)

Yeah, the marking of the arraybuffer as non-neuterable.

I was here when that CL was made. I don't remember seeing it though.

Maybe it will be remove the one line and to implement the transferring when AudioBufferSourceNode.start() is called.  That might be small enough while fixing this issue and not regressing crbug.com/254728.

### rt...@chromium.org (2017-09-06)

Er, maybe it will be enough to remove the line and implement detaching the buffer when start() is called.

### bi...@chromium.org (2017-09-06)

Sorry, I don't understand. Why would detaching in AudioBufferSourceNode.start help?

Seems to me if we know that the "CopyTo" branch of ArrayBuffer::Transfer only happens with an AudioBuffer's ArrayBuffer, and we know that it is already not spec compliant, we can just move the neutering of the ArrayBufferViews into the "Transfer" branch.

See https://chromium-review.googlesource.com/c/chromium/src/+/653489

### rt...@chromium.org (2017-09-07)

Here's my thinking. Could be totally wrong.

First remove the neutering from AudioBuffer.  That fixes this issue.

But based on https://bugs.chromium.org/p/chromium/issues/detail?id=254728, this will cause a regression if an AudioBufferSourceNode is playing out the AudioBuffer.  The spec on acquiring the contents says AudioBufferSourceNode.start() should detach the AudioBuffer.

But I'm ok if you want to land https://chromium-review.googlesource.com/c/chromium/src/+/653489 to fix this issue.  That gives me some time to go and fix the WebAudio parts, and maybe allowing you to revert (or whatever) 653489.

### rt...@chromium.org (2017-09-07)

Started looking at implementing the "acquire the contents" of AudioBuffer.  There will be lots of changes that would very likely be to complex to merge to beta.

So you're current plan and CL looks like the most viable option. I am concerned about the TODO you have about not being compliant, though.

### bi...@chromium.org (2017-09-07)

Yeah, it looks scarier than it is. The only time that path is taken is when one of the ArrayBufferViews is non-neuterable. That is only true for AudioBuffer -- and it already has this non-compliant behavior. So this is just spelling it out so that we fix it later.

### rt...@chromium.org (2017-09-07)

Works for me!

### bu...@chromium.org (2017-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e84445f6c1d2b4817d3510c94fcb82fd0e12df99

commit e84445f6c1d2b4817d3510c94fcb82fd0e12df99
Author: Ben Smith <binji@chromium.org>
Date: Fri Sep 08 00:33:57 2017

Only neuter ArrayBufferViews when all are neuterable

https://crbug.com/254728 was fixed by https://crrev.com/19019002/
a few years ago. The fix was to only transfer the array's data 
when no ArrayBufferViews were marked as non-neuterable. This feature 
is only used for WebAudio, where the AudioBuffer's channel data may
be in use while it was being detached. That fix is not spec compliant,
since the spec says that the AudioBuffer's ArrayBuffers may be
detached at any time. It's likely that this wasn't specified at the
time however.

ArrayBuffer::Transfer currently does the wrong thing in this case:
when an ArrayBufferView is marked as non-neuterable, its contents
are copied to the ArrayBufferContents object, and all ArrayBufferViews
are removed, but the ArrayBuffer is not neutered. This leaves any
ArrayBufferView in an inconsistent state; it has a pointer to its
ArrayBuffer, but the ArrayBuffer does not have a pointer to the
ArrayBufferView. Subsequent calls to ArrayBuffer::Transfer will
therefore not be able to check this ArrayBufferView's neuterable
flag, even though the ArrayBufferView has a pointer to the
ArrayBuffer's data.

BUG=chromium:761801

Change-Id: I1d24b3f7543675af2d997d44d455003b396d2c6d
Reviewed-on: https://chromium-review.googlesource.com/653489
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Ben Smith <binji@chromium.org>
Cr-Commit-Position: refs/heads/master@{#500452}
[modify] https://crrev.com/e84445f6c1d2b4817d3510c94fcb82fd0e12df99/third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBuffer.cpp


### rt...@chromium.org (2017-09-11)

Ran ToT build from this morning.  The repro case no longer causes an ASAN error.

binji: Do we need to merge this to 61? The change to decodeAudioData to detach the buffer landed in 59.

### bi...@chromium.org (2017-09-11)

Yes, it is probably a good idea.

### sh...@chromium.org (2017-09-11)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-09-11)

+awhalley@ for M61 merge review

### aw...@google.com (2017-09-11)

This is good to take in M62 (govind@, please approve if you agree)

We've got a M61 refresh being cut today, but the fix is outside our merge guidelines as it's not yet had bake time in Beta.  We can keep an eye on this for any future 61 spins.

### go...@chromium.org (2017-09-11)

+abdulsyed@ (Chrome Desktop M62 TPM) for M62 merge approval.

### ab...@google.com (2017-09-11)

Approving for M62 Merge. 

### ab...@google.com (2017-09-11)

branch: 3202

### bu...@chromium.org (2017-09-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4d1606b1d91b0477af82bac9de07e3d80c75bede

commit 4d1606b1d91b0477af82bac9de07e3d80c75bede
Author: Ben Smith <binji@chromium.org>
Date: Mon Sep 11 19:02:07 2017

Only neuter ArrayBufferViews when all are neuterable

https://crbug.com/254728 was fixed by https://crrev.com/19019002/
a few years ago. The fix was to only transfer the array's data
when no ArrayBufferViews were marked as non-neuterable. This feature
is only used for WebAudio, where the AudioBuffer's channel data may
be in use while it was being detached. That fix is not spec compliant,
since the spec says that the AudioBuffer's ArrayBuffers may be
detached at any time. It's likely that this wasn't specified at the
time however.

ArrayBuffer::Transfer currently does the wrong thing in this case:
when an ArrayBufferView is marked as non-neuterable, its contents
are copied to the ArrayBufferContents object, and all ArrayBufferViews
are removed, but the ArrayBuffer is not neutered. This leaves any
ArrayBufferView in an inconsistent state; it has a pointer to its
ArrayBuffer, but the ArrayBuffer does not have a pointer to the
ArrayBufferView. Subsequent calls to ArrayBuffer::Transfer will
therefore not be able to check this ArrayBufferView's neuterable
flag, even though the ArrayBufferView has a pointer to the
ArrayBuffer's data.

BUG=chromium:761801
TBR=binji@chromium.org

(cherry picked from commit e84445f6c1d2b4817d3510c94fcb82fd0e12df99)

Change-Id: I1d24b3f7543675af2d997d44d455003b396d2c6d
Reviewed-on: https://chromium-review.googlesource.com/653489
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Ben Smith <binji@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#500452}
Reviewed-on: https://chromium-review.googlesource.com/660808
Reviewed-by: Ben Smith <binji@chromium.org>
Cr-Commit-Position: refs/branch-heads/3202@{#142}
Cr-Branched-From: fa6a5d87adff761bc16afc5498c3f5944c1daa68-refs/heads/master@{#499098}
[modify] https://crrev.com/4d1606b1d91b0477af82bac9de07e3d80c75bede/third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBuffer.cpp


### sh...@chromium.org (2017-09-12)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-09-13)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-09-13)

Approving merge to M61 and M62.

### go...@chromium.org (2017-09-13)

+ awhalley@ (Security TPM) is waiting on more Canary/Dev coverage before approving merge to M61.

### aw...@chromium.org (2017-09-15)

Good for 61

### go...@chromium.org (2017-09-15)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/761801#c38 so it gets picked up for any future M61 releases if any.

### bu...@chromium.org (2017-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6f266f327adeaa71408edf1c19433ad0f6efd9fa

commit 6f266f327adeaa71408edf1c19433ad0f6efd9fa
Author: Brad Nelson <bradnelson@chromium.org>
Date: Fri Sep 15 17:33:32 2017

Only neuter AB Views when all are neuterable

https://crbug.com/254728 was fixed by https://crrev.com/19019002/
a few years ago. The fix was to only transfer the array's data
when no ArrayBufferViews were marked as non-neuterable. This feature
is only used for WebAudio, where the AudioBuffer's channel data may
be in use while it was being detached. That fix is not spec compliant,
since the spec says that the AudioBuffer's ArrayBuffers may be
detached at any time. It's likely that this wasn't specified at the
time however.

ArrayBuffer::Transfer currently does the wrong thing in this case:
when an ArrayBufferView is marked as non-neuterable, its contents
are copied to the ArrayBufferContents object, and all ArrayBufferViews
are removed, but the ArrayBuffer is not neutered. This leaves any
ArrayBufferView in an inconsistent state; it has a pointer to its
ArrayBuffer, but the ArrayBuffer does not have a pointer to the
ArrayBufferView. Subsequent calls to ArrayBuffer::Transfer will
therefore not be able to check this ArrayBufferView's neuterable
flag, even though the ArrayBufferView has a pointer to the
ArrayBuffer's data.

BUG=chromium:761801
TBR=binji@chromium.org

(cherry picked from commit e84445f6c1d2b4817d3510c94fcb82fd0e12df99)

Change-Id: I1d24b3f7543675af2d997d44d455003b396d2c6d
Reviewed-on: https://chromium-review.googlesource.com/653489
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Ben Smith <binji@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#500452}
Reviewed-on: https://chromium-review.googlesource.com/668758
Cr-Commit-Position: refs/branch-heads/3163@{#1208}
Cr-Branched-From: ff259bab28b35d242e10186cd63af7ed404fae0d-refs/heads/master@{#488528}
[modify] https://crrev.com/6f266f327adeaa71408edf1c19433ad0f6efd9fa/third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBuffer.cpp


### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-22)

Congratulations liangdong46@ - The VRP panel decided to award $3,000 for this bug. A member of our finance team will be in touch to arrange for payment.

Also, how would you like to be credited when this is included in release notes?

### aw...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-27)

This issue was migrated from crbug.com/chromium/761801?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088915)*
