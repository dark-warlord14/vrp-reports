# UAF in BackgroundProcessor::OnDataPipeReadable

| Field | Value |
|-------|-------|
| **Issue ID** | [337998760](https://issues.chromium.org/issues/337998760) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2024-04-30 |
| **Bounty** | $3,000.00 |

## Description

tested os:
-   ubuntu 22.04
tested chrome version:
-   Chromium 126.0.6431.0
-   Chromium 125.0.6368.2

repro steps:
1. Add sleep in BackgroundProcessor::OnDataPipeReadable for delay access to the |client_|.
diff --git a/third_party/blink/renderer/bindings/core/v8/script_streamer.cc b/third_party/blink/renderer/bindings/core/v8/script_streamer.cc
index a2b9721b70627..25f1042738dab 100644
--- a/third_party/blink/renderer/bindings/core/v8/script_streamer.cc
+++ b/third_party/blink/renderer/bindings/core/v8/script_streamer.cc
+1422,9 @@ void BackgroundResourceScriptStreamer::BackgroundProcessor::OnDataPipeReadable(
   DCHECK_CALLED_ON_VALID_SEQUENCE(background_sequence_checker_);
   TRACE_EVENT0("v8,devtools.timeline," TRACE_DISABLED_BY_DEFAULT("v8.compile"),
                "BackgroundProcessor::OnDataPipeReadable");
+  base::PlatformThread::Sleep(base::Milliseconds(100));
+  //LOG(ERROR) << "OnDataPipeReadable: " << ready_result;
   if (!client_) {
     CHECK_EQ(state_, BackgroundProcessorState::kCancelled);
     // The request was canceled while waiting for the data pipe to be

2. Usage: ./script_name <executable_path> <url> <number_of_executions>
./launcher.sh ./chrome http://localhost:8880/crash.html 10 2>&1|grep -E 'heap-use'

The original chrome was unstable in reproduction, so I added a sleep at the point where the UAF (Use-After-Free) occurs, to increase the likelihood of accessing the |client_| variable after triggering garbage collection. By combining this with a script that opens multiple browsers simultaneously, the issue can be reproduced very quickly. In local testing, it can be reproduced within a few seconds.

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x511000252838 at pc 0x5a4769144e97 bp 0x70ae058c5910 sp 0x70ae058c5908
READ of size 8 at 0x511000252838 thread T10 (ThreadPoolForeg)
    #0 0x5a4769144e96 in blink::BackgroundResourceScriptStreamer::BackgroundProcessor::OnDataPipeReadable(unsigned int, mojo::HandleSignalsState const&) ./../../third_party/blink/renderer/bindings/core/v8/script_streamer.cc:1420:8
    #1 0x5a476915074e in Invoke<void (blink::BackgroundResourceScriptStreamer::BackgroundProcessor::*)(unsigned int, const mojo::HandleSignalsState &), blink::BackgroundResourceScriptStreamer::BackgroundProcessor *, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:738:12
    #2 0x5a476915074e in MakeItSo<void (blink::BackgroundResourceScriptStreamer::BackgroundProcessor::*const &)(unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<WTF::UnretainedWrapper<blink::BackgroundResourceScriptStreamer::BackgroundProcessor> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:930:12
    #3 0x5a476915074e in RunImpl<void (blink::BackgroundResourceScriptStreamer::BackgroundProcessor::*const &)(unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<WTF::UnretainedWrapper<blink::BackgroundResourceScriptStreamer::BackgroundProcessor> > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #4 0x5a476915074e in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundResourceScriptStreamer::BackgroundProcessor::* const&)(unsigned int, mojo::HandleSignalsState const&), blink::BackgroundResourceScriptStreamer::BackgroundProcessor*>, base::internal::BindState<true, true, false, void (blink::BackgroundResourceScriptStreamer::BackgroundProcessor::*)(unsigned int, mojo::HandleSignalsState const&), WTF::UnretainedWrapper<blink::BackgroundResourceScriptStreamer::BackgroundProcessor>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind_internal.h:987:12
    #5 0x5a475d7acd5b in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
    #6 0x5a475d7ac683 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #7 0x5a475d7ad8c4 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind_internal.h:738:12
    #8 0x5a475d7ad8c4 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind_internal.h:954:5
    #9 0x5a475d7ad8c4 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind_internal.h:1067:14
    #10 0x5a475c036ba4 in Run ./../../base/functional/callback.h:156:12
    #11 0x5a475c036ba4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #12 0x5a475c0b814b in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:680:35)> ./../../base/task/common/task_annotator.h:90:5
    #13 0x5a475c0b814b in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:679:19
    #14 0x5a475c0b839c in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:664:3
    #15 0x5a475c0b76a5 in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:694:7
    #16 0x5a475c0b76a5 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker.cc:521:5
    #17 0x5a475c0b6734 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:416:5
    #18 0x5a475c0f6280 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:438:36
    #19 0x5a475c0f5327 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:322:3
    #20 0x5a475c0f4df0 in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread_pool/worker_thread.cc:302:7
    #21 0x5a475c1637b7 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:101:13
    #22 0x5a4749e84fb6 in asan_thread_start(void*) _asan_rtl_:28

0x511000252838 is located 184 bytes inside of 256-byte region [0x511000252780,0x511000252880)
freed by thread T0 (chrome) here:
    #0 0x5a4749e872e6 in __interceptor_free _asan_rtl_:3
    #1 0x5a47517c5978 in operator() ./../../v8/src/heap/cppgc/sweeper.cc:465:15
    #2 0x5a47517c5978 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizePage(cppgc::internal::(anonymous namespace)::SpaceState::SweptPageState*) ./../../v8/src/heap/cppgc/sweeper.cc:479:7
    #3 0x5a47517bc241 in cppgc::internal::Sweeper::SweeperImpl::SweepForAllocationIfRunning(cppgc::internal::NormalPageSpace*, unsigned long, v8::base::TimeDelta) ./../../v8/src/heap/cppgc/sweeper.cc:896:19
    #4 0x5a47517a7cc9 in cppgc::internal::ObjectAllocator::TryRefillLinearAllocationBuffer(cppgc::internal::NormalPageSpace&, unsigned long) ./../../v8/src/heap/cppgc/object-allocator.cc:217:15
    #5 0x5a47517a6da7 in cppgc::internal::ObjectAllocator::OutOfLineAllocateImpl(cppgc::internal::NormalPageSpace&, unsigned long, cppgc::internal::AlignVal, unsigned short) ./../../v8/src/heap/cppgc/object-allocator.cc:173:8
    #6 0x5a47517a6896 in cppgc::internal::ObjectAllocator::OutOfLineAllocateGCSafePoint(cppgc::internal::NormalPageSpace&, unsigned long, cppgc::internal::AlignVal, unsigned short, void**) ./../../v8/src/heap/cppgc/object-allocator.cc:121:13
    #7 0x5a47517763b0 in OutOfLineAllocate ./../../v8/src/heap/cppgc/object-allocator.h:182:3
    #8 0x5a47517763b0 in AllocateObjectOnSpace ./../../v8/src/heap/cppgc/object-allocator.h:241:12
    #9 0x5a47517763b0 in AllocateObject ./../../v8/src/heap/cppgc/object-allocator.h:120:10
    #10 0x5a47517763b0 in cppgc::internal::MakeGarbageCollectedTraitInternal::Allocate(cppgc::AllocationHandle&, unsigned long, unsigned short) ./../../v8/src/heap/cppgc/allocation.cc:38:48
    #11 0x5a47586373ec in Invoke ./../../v8/include/cppgc/allocation.h:94:14
    #12 0x5a47586373ec in Allocate ./../../v8/include/cppgc/allocation.h:180:12
    #13 0x5a47586373ec in Call<blink::ResponseBodyLoader *> ./../../v8/include/cppgc/allocation.h:241:9
    #14 0x5a47586373ec in MakeGarbageCollected<blink::ResponseBodyLoader::Buffer, blink::ResponseBodyLoader *> ./../../v8/include/cppgc/allocation.h:280:7
    #15 0x5a47586373ec in MakeGarbageCollected<blink::ResponseBodyLoader::Buffer, blink::ResponseBodyLoader *> ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:37:10
    #16 0x5a47586373ec in blink::ResponseBodyLoader::ResponseBodyLoader(blink::BytesConsumer&, blink::ResponseBodyLoaderClient&, scoped_refptr<base::SingleThreadTaskRunner>, blink::BackForwardCacheLoaderHelper*) ./../../third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:382:18
    #17 0x5a47585f0201 in Call<blink::BytesConsumer &, blink::ResponseBodyLoaderClient &, scoped_refptr<base::SingleThreadTaskRunner> &, blink::BackForwardCacheLoaderHelper *> ./../../v8/include/cppgc/allocation.h:242:32
    #18 0x5a47585f0201 in MakeGarbageCollected<blink::ResponseBodyLoader, blink::BytesConsumer &, blink::ResponseBodyLoaderClient &, scoped_refptr<base::SingleThreadTaskRunner> &, blink::BackForwardCacheLoaderHelper *> ./../../v8/include/cppgc/allocation.h:280:7
    #19 0x5a47585f0201 in blink::ResponseBodyLoader* blink::MakeGarbageCollected<blink::ResponseBodyLoader, blink::BytesConsumer&, blink::ResponseBodyLoaderClient&, scoped_refptr<base::SingleThreadTaskRunner>&, blink::BackForwardCacheLoaderHelper*>(blink::BytesConsumer&, blink::ResponseBodyLoaderClient&, scoped_refptr<base::SingleThreadTaskRunner>&, blink::BackForwardCacheLoaderHelper*&&) ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:37:10
    #20 0x5a47585efc6e in blink::ResourceLoader::DidStartLoadingResponseBodyInternal(blink::BytesConsumer&) ./../../third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:393:27
    #21 0x5a47585fc441 in blink::ResourceLoader::DidReceiveResponse(blink::WebURLResponse const&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>) ./../../third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:819:3
    #22 0x5a475865fe3f in blink::BackgroundURLLoader::Context::OnReceivedResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int) ./../../third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:562:14
    #23 0x5a475866031c in void base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>::Invoke<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int>(void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&, int&&) ./../../base/functional/bind_internal.h:738:12
    #24 0x5a4758660081 in MakeItSo<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer> >, int> ./../../base/functional/bind_internal.h:930:12
    #25 0x5a4758660081 in RunImpl<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer> >, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind_internal.h:1067:14
    #26 0x5a4758660081 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>, void (int)>::RunOnce(base::internal::BindStateBase*, int) ./../../base/functional/bind_internal.h:980:12
    #27 0x5a4753ca4ace in Run ./../../base/functional/callback.h:156:12
    #28 0x5a4753ca4ace in Invoke<base::OnceCallback<void (int)>, int> ./../../base/functional/bind_internal.h:813:49
    #29 0x5a4753ca4ace in MakeItSo<base::OnceCallback<void (int)>, std::__Cr::tuple<int> > ./../../base/functional/bind_internal.h:930:12
    #30 0x5a4753ca4ace in RunImpl<base::OnceCallback<void (int)>, std::__Cr::tuple<int>, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #31 0x5a4753ca4ace in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, int>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #32 0x5a475865cea9 in Run ./../../base/functional/callback.h:156:12
    #33 0x5a475865cea9 in Run ./../../third_party/blink/renderer/platform/wtf/functional.h:341:33
    #34 0x5a475865cea9 in blink::BackgroundURLLoader::Context::RunTasksOnMainThread() ./../../third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:524:23
    #35 0x5a4758654f44 in Invoke<void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context> > ./../../base/functional/bind_internal.h:738:12
    #36 0x5a4758654f44 in MakeItSo<void (blink::BackgroundURLLoader::Context::*)(), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context> > > ./../../base/functional/bind_internal.h:930:12
    #37 0x5a4758654f44 in RunImpl<void (blink::BackgroundURLLoader::Context::*)(), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context> >, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #38 0x5a4758654f44 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #39 0x5a475c036ba4 in Run ./../../base/functional/callback.h:156:12
    #40 0x5a475c036ba4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #41 0x5a475c097614 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #42 0x5a475c097614 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #43 0x5a475c09652d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #44 0x5a475c09834a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #45 0x5a475bf2e43d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #46 0x5a475c098fc6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12
    #47 0x5a475bfc7eef in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #48 0x5a47735dd003 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:368:16
    #49 0x5a475972d5d9 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #50 0x5a475972eb2e in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #51 0x5a47597316c1 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1153:10
    #52 0x5a475972b900 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:332:36
    #53 0x5a475972bf7b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:345:10

previously allocated by thread T0 (chrome) here:
    #0 0x5a4749e8757f in __interceptor_malloc _asan_rtl_:3
    #1 0x5a475c27e54b in AllocInternal<(partition_alloc::internal::AllocFlags)0> ./../../base/allocator/partition_allocator/src/partition_alloc/partition_root.h:2072:51
    #2 0x5a475c27e54b in AllocInline<(partition_alloc::internal::AllocFlags)0> ./../../base/allocator/partition_allocator/src/partition_alloc/partition_root.h:511:12
    #3 0x5a475c27e54b in void* partition_alloc::PartitionRoot::Alloc<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*) ./../../base/allocator/partition_allocator/src/partition_alloc/partition_root.h:505:12
    #4 0x5a4769148e73 in operator new ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:55:3
    #5 0x5a4769148e73 in MakeRefCounted<blink::BackgroundResourceScriptStreamer::BackgroundProcessor, cppgc::internal::BasicMember<blink::ScriptResource, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer> &> ./../../base/memory/scoped_refptr.h:150:12
    #6 0x5a4769148e73 in blink::BackgroundResourceScriptStreamer::BackgroundResourceScriptStreamer(blink::ScriptResource*) ./../../third_party/blink/renderer/bindings/core/v8/script_streamer.cc:1640:11
    #7 0x5a476a0e71a1 in Call<blink::ScriptResource *> ./../../v8/include/cppgc/allocation.h:242:32
    #8 0x5a476a0e71a1 in MakeGarbageCollected<blink::BackgroundResourceScriptStreamer, blink::ScriptResource *> ./../../v8/include/cppgc/allocation.h:280:7
    #9 0x5a476a0e71a1 in MakeGarbageCollected<blink::BackgroundResourceScriptStreamer, blink::ScriptResource *> ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:37:10
    #10 0x5a476a0e71a1 in blink::ScriptResource::MaybeCreateBackgroundResponseProcessor() ./../../third_party/blink/renderer/core/loader/resource/script_resource.cc:609:7
    #11 0x5a47585f5099 in blink::ResourceLoader::RequestAsynchronously() ./../../third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1335:37
    #12 0x5a47585e2c26 in blink::ResourceLoadScheduler::Run(unsigned long, blink::ResourceLoadSchedulerClient*, bool, blink::WebURLRequest::Priority) ./../../third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc:384:11
    #13 0x5a47585e1f32 in blink::ResourceLoadScheduler::MaybeRun() ./../../third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc:369:5
    #14 0x5a47585e2632 in blink::ResourceLoadScheduler::Request(blink::ResourceLoadSchedulerClient*, blink::ResourceLoadScheduler::ThrottleOption, blink::WebURLRequest::Priority, int, unsigned long*) ./../../third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc:181:3
    #15 0x5a47585eedee in blink::ResourceLoader::Start() ./../../third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:385:15
    #16 0x5a475859f590 in blink::ResourceFetcher::StartLoad(blink::Resource*, blink::ResourceRequestBody, blink::ResourceFetcher::ImageLoadBlockingPolicy, blink::RenderBlockingBehavior) ./../../third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc:2416:11
    #17 0x5a475859a32a in blink::ResourceFetcher::RequestResource(blink::FetchParameters&, blink::ResourceFactory const&, blink::ResourceClient*) ./../../third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc:1364:10
    #18 0x5a476a0df00e in blink::ScriptResource::Fetch(blink::FetchParameters&, blink::ResourceFetcher*, blink::ResourceClient*, v8::Isolate*, blink::ScriptResource::StreamingAllowed, blink::v8_compile_hints::V8CrowdsourcedCompileHintsProducer*, blink::v8_compile_hints::V8CrowdsourcedCompileHintsConsumer*) ./../../third_party/blink/renderer/core/loader/resource/script_resource.cc:108:48
    #19 0x5a476a0af892 in blink::PreloadHelper::StartPreload(blink::ResourceType, blink::FetchParameters&, blink::Document&) ./../../third_party/blink/renderer/core/loader/preload_helper.cc:939:18
    #20 0x5a476bd78776 in blink::PreloadRequest::Start(blink::Document*) ./../../third_party/blink/renderer/core/html/parser/preload_request.cc:201:10
    #21 0x5a476bcfdadf in blink::HTMLResourcePreloader::Preload(std::__Cr::unique_ptr<blink::PreloadRequest, std::__Cr::default_delete<blink::PreloadRequest>>) ./../../third_party/blink/renderer/core/html/parser/html_resource_preloader.cc:77:12
    #22 0x5a476bd7913c in blink::ResourcePreloader::TakeAndPreload(WTF::Vector<std::__Cr::unique_ptr<blink::PreloadRequest, std::__Cr::default_delete<blink::PreloadRequest>>, 0u, WTF::PartitionAllocator>&) ./../../third_party/blink/renderer/core/html/parser/resource_preloader.cc:17:5
    #23 0x5a476bc2be0b in blink::HTMLDocumentParser::FetchQueuedPreloads() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1585:17
    #24 0x5a476bc2d192 in blink::HTMLDocumentParser::ProcessPreloadData(std::__Cr::unique_ptr<blink::PendingPreloadData, std::__Cr::default_delete<blink::PendingPreloadData>>) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1573:3
    #25 0x5a476bc21c03 in blink::HTMLDocumentParser::ScanAndPreload(blink::HTMLPreloadScanner*) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1462:3
    #26 0x5a476bc248b4 in blink::HTMLDocumentParser::Append(WTF::String const&) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1025:7
    #27 0x5a4769f8763c in blink::DocumentLoader::CommitData(blink::DocumentLoader::BodyData&) ./../../third_party/blink/renderer/core/loader/document_loader.cc:1515:8
    #28 0x5a4769f83b0d in blink::DocumentLoader::ProcessDataBuffer(blink::DocumentLoader::BodyData*) ./../../third_party/blink/renderer/core/loader/document_loader.cc:1742:5
    #29 0x5a4769f82894 in blink::DocumentLoader::BodyDataReceivedImpl(blink::DocumentLoader::BodyData&) ./../../third_party/blink/renderer/core/loader/document_loader.cc:1238:3
    #30 0x5a4769f830bf in blink::DocumentLoader::DecodedBodyDataReceived(blink::WebString const&, blink::WebEncodingData const&, base::span<char const, 18446744073709551615ul, char const*>) ./../../third_party/blink/renderer/core/loader/document_loader.cc:1194:3
    #31 0x5a47586864d9 in blink::NavigationBodyLoader::ProcessOffThreadData() ./../../third_party/blink/renderer/platform/loader/fetch/url_loader/navigation_body_loader.cc:496:14
    #32 0x5a4758687105 in blink::NavigationBodyLoader::BindURLLoaderAndStartLoadingResponseBodyIfPossible() ./../../third_party/blink/renderer/platform/loader/fetch/url_loader/navigation_body_loader.cc:567:5
    #33 0x5a4758686df4 in blink::NavigationBodyLoader::StartLoadingBody(blink::WebNavigationBodyLoader::Client*) ./../../third_party/blink/renderer/platform/loader/fetch/url_loader/navigation_body_loader.cc:425:3
    #34 0x5a4769f8cf8d in blink::DocumentLoader::StartLoadingResponse() ./../../third_party/blink/renderer/core/loader/document_loader.cc:0:0
    #35 0x5a4769f9a409 in blink::DocumentLoader::CommitNavigation() ./../../third_party/blink/renderer/core/loader/document_loader.cc:3002:3
    #36 0x5a4769ffbb9a in blink::FrameLoader::CommitDocumentLoader(blink::DocumentLoader*, blink::HistoryItem*, blink::CommitReason) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1356:21

Thread T10 (ThreadPoolForeg) created by T9 (Preload scanner) here:
    #0 0x5a4749e6d011 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x5a475c162d10 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:146:13
    #2 0x5a475c0f421a in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) ./../../base/task/thread_pool/worker_thread.cc:199:3
    #3 0x5a475c0ba9ff in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() ./../../base/task/thread_pool/thread_group.cc:110:13
    #4 0x5a475c0ba4ff in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group.cc:85:3
    #5 0x5a475c0ec072 in ~SemaphoreScopedCommandsExecutor ./../../base/task/thread_pool/thread_group_semaphore.cc:48:3
    #6 0x5a475c0ec072 in base::internal::ThreadGroupSemaphore::PushTaskSourceAndWakeUpWorkers(base::internal::RegisteredTaskSourceAndTransaction) ./../../base/task/thread_pool/thread_group_semaphore.cc:173:1
    #7 0x5a475c0cd922 in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped_refptr<base::internal::Sequence>) ./../../base/task/thread_pool/thread_pool_impl.cc:464:38
    #8 0x5a475c0cdeda in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped_refptr<base::internal::Sequence>) ./../../base/task/thread_pool/thread_pool_impl.cc:487:12
    #9 0x5a475c0cc3e9 in base::internal::ThreadPoolImpl::PostDelayedTask(base::Location const&, base::TaskTraits const&, base::OnceCallback<void ()>, base::TimeDelta) ./../../base/task/thread_pool/thread_pool_impl.cc:285:10
    #10 0x5a475c0aec4e in PostDelayedTask ./../../base/task/thread_pool.cc:67:31
    #11 0x5a475c0aec4e in base::ThreadPool::PostTask(base::Location const&, base::TaskTraits const&, base::OnceCallback<void ()>) ./../../base/task/thread_pool.cc:58:10
    #12 0x5a4758445b0d in blink::worker_pool::PostTask(base::Location const&, base::TaskTraits const&, WTF::CrossThreadOnceFunction<void ()>) ./../../third_party/blink/renderer/platform/scheduler/common/worker_pool.cc:23:3
    #13 0x5a476bcfa950 in blink::BackgroundHTMLScanner::ScriptTokenScanner::ScanToken(blink::HTMLToken const&) ./../../third_party/blink/renderer/core/html/parser/background_html_scanner.cc:208:11
    #14 0x5a476bce6e33 in blink::HTMLPreloadScanner::Scan(blink::KURL const&) ./../../third_party/blink/renderer/core/html/parser/html_preload_scanner.cc:1271:30
    #15 0x5a476bce7b75 in blink::HTMLPreloadScanner::ScanInBackground(WTF::String const&, blink::KURL const&) ./../../third_party/blink/renderer/core/html/parser/html_preload_scanner.cc:1304:21
    #16 0x5a476bc3c650 in Invoke<void (blink::HTMLPreloadScanner::*)(const WTF::String &, const blink::KURL &), const base::WeakPtr<blink::HTMLPreloadScanner> &, WTF::String, blink::KURL> ./../../base/functional/bind_internal.h:738:12
    #17 0x5a476bc3c650 in MakeItSo<void (blink::HTMLPreloadScanner::*)(const WTF::String &, const blink::KURL &), std::__Cr::tuple<base::WeakPtr<blink::HTMLPreloadScanner>, WTF::String, blink::KURL> > ./../../base/functional/bind_internal.h:954:5
    #18 0x5a476bc3c650 in void base::internal::Invoker<base::internal::FunctorTraits<void (blink::HTMLPreloadScanner::*&&)(WTF::String const&, blink::KURL const&), base::WeakPtr<blink::HTMLPreloadScanner>&&, WTF::String&&, blink::KURL&&>, base::internal::BindState<true, true, false, void (blink::HTMLPreloadScanner::*)(WTF::String const&, blink::KURL const&), base::WeakPtr<blink::HTMLPreloadScanner>, WTF::String, blink::KURL>, void ()>::RunImpl<void (blink::HTMLPreloadScanner::*)(WTF::String const&, blink::KURL const&), std::__Cr::tuple<base::WeakPtr<blink::HTMLPreloadScanner>, WTF::String, blink::KURL>, 0ul, 1ul, 2ul>(void (blink::HTMLPreloadScanner::*&&)(WTF::String const&, blink::KURL const&), std::__Cr::tuple<base::WeakPtr<blink::HTMLPreloadScanner>, WTF::String, blink::KURL>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>) ./../../base/functional/bind_internal.h:1067:14
    #19 0x5a475c036ba4 in Run ./../../base/functional/callback.h:156:12
    #20 0x5a475c036ba4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #21 0x5a475c097614 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #22 0x5a475c097614 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #23 0x5a475c09652d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #24 0x5a475c09834a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #25 0x5a475bf2e43d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #26 0x5a475c098fc6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12
    #27 0x5a475bfc7eef in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #28 0x5a47584ecf19 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:188:14
    #29 0x5a475c1637b7 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:101:13
    #30 0x5a4749e84fb6 in asan_thread_start(void*) _asan_rtl_:28

Thread T9 (Preload scanner) created by T0 (chrome) here:
    #0 0x5a4749e6d011 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x5a475c162d10 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:146:13
    #2 0x5a475c116228 in base::SimpleThread::StartAsync() ./../../base/threading/simple_thread.cc:55:13
    #3 0x5a47584eabba in blink::NonMainThread::CreateThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:41:11
    #4 0x5a476bc10616 in operator() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:153:3
    #5 0x5a476bc10616 in InstanceStorage<(lambda at ../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:153:3), (lambda at ../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:153:3)> ./../../third_party/blink/renderer/platform/wtf/std_lib_extras.h:137:7
    #6 0x5a476bc10616 in WTF::StaticSingleton<std::__Cr::unique_ptr<blink::NonMainThread, std::__Cr::default_delete<blink::NonMainThread>>>::StaticSingleton<blink::GetPreloadScannerThread()::$_0, blink::GetPreloadScannerThread()::$_1>(blink::GetPreloadScannerThread()::$_0 const&, blink::GetPreloadScannerThread()::$_1 const&) ./../../third_party/blink/renderer/platform/wtf/std_lib_extras.h:85:9
    #7 0x5a476bc129db in GetPreloadScannerThread ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:153:3
    #8 0x5a476bc129db in blink::HTMLDocumentParser::HTMLDocumentParser(blink::Document&, blink::ParserContentPolicy, blink::ParserSynchronizationPolicy, blink::ParserPrefetchPolicy) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:440:5
    #9 0x5a476bc11598 in blink::HTMLDocumentParser::HTMLDocumentParser(blink::HTMLDocument&, blink::ParserSynchronizationPolicy, blink::ParserPrefetchPolicy) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:372:7
    #10 0x5a476b8deba0 in Call<blink::HTMLDocument &, blink::ParserSynchronizationPolicy &> ./../../v8/include/cppgc/allocation.h:242:32
    #11 0x5a476b8deba0 in MakeGarbageCollected<blink::HTMLDocumentParser, blink::HTMLDocument &, blink::ParserSynchronizationPolicy &> ./../../v8/include/cppgc/allocation.h:280:7
    #12 0x5a476b8deba0 in MakeGarbageCollected<blink::HTMLDocumentParser, blink::HTMLDocument &, blink::ParserSynchronizationPolicy &> ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:37:10
    #13 0x5a476b8deba0 in blink::Document::CreateParser() ./../../third_party/blink/renderer/core/dom/document.cc:3437:12
    #14 0x5a476b8e1845 in blink::Document::ImplicitOpen(blink::ParserSynchronizationPolicy) ./../../third_party/blink/renderer/core/dom/document.cc:3803:13
    #15 0x5a476b8e29be in blink::Document::OpenForNavigation(blink::ParserSynchronizationPolicy, WTF::AtomicString const&, WTF::AtomicString const&) ./../../third_party/blink/renderer/core/dom/document.cc:3774:28
    #16 0x5a4769f8dc7b in blink::DocumentLoader::CreateParserPostCommit() ./../../third_party/blink/renderer/core/loader/document_loader.cc:3087:23
    #17 0x5a4769f8c5be in blink::DocumentLoader::StartLoadingResponse() ./../../third_party/blink/renderer/core/loader/document_loader.cc:1936:3
    #18 0x5a4769f9a409 in blink::DocumentLoader::CommitNavigation() ./../../third_party/blink/renderer/core/loader/document_loader.cc:3002:3
    #19 0x5a4769ffbb9a in blink::FrameLoader::CommitDocumentLoader(blink::DocumentLoader*, blink::HistoryItem*, blink::CommitReason) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1356:21
    #20 0x5a4769ffae47 in blink::FrameLoader::Init(base::TokenType<blink::DocumentTokenTypeMarker> const&, std::__Cr::unique_ptr<blink::PolicyContainer, std::__Cr::default_delete<blink::PolicyContainer>>, blink::StorageKey const&, long, blink::KURL const&) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:259:3
    #21 0x5a4768abab89 in blink::LocalFrame::Init(blink::Frame*, base::TokenType<blink::DocumentTokenTypeMarker> const&, std::__Cr::unique_ptr<blink::PolicyContainer, std::__Cr::default_delete<blink::PolicyContainer>>, blink::StorageKey const&, long, blink::KURL const&) ./../../third_party/blink/renderer/core/frame/local_frame.cc:389:11
    #22 0x5a4768d489b4 in blink::WebLocalFrameImpl::InitializeCoreFrameInternal(blink::Page&, blink::FrameOwner*, blink::WebFrame*, blink::WebFrame*, blink::FrameInsertType, WTF::AtomicString const&, blink::WindowAgentFactory*, blink::WebFrame*, base::TokenType<blink::DocumentTokenTypeMarker> const&, std::__Cr::unique_ptr<blink::PolicyContainer, std::__Cr::default_delete<blink::PolicyContainer>>, blink::StorageKey const&, long, blink::KURL const&, network::mojom::WebSandboxFlags) ./../../third_party/blink/renderer/core/frame/web_local_frame_impl.cc:2312:11
    #23 0x5a4768d4647b in InitializeCoreFrame ./../../third_party/blink/renderer/core/frame/web_local_frame_impl.cc:2254:3
    #24 0x5a4768d4647b in blink::WebLocalFrameImpl::CreateProvisional(blink::WebLocalFrameClient*, blink::InterfaceRegistry*, base::TokenType<blink::LocalFrameTokenTypeMarker> const&, blink::WebFrame*, blink::FramePolicy const&, blink::WebString const&, blink::WebView*) ./../../third_party/blink/renderer/core/frame/web_local_frame_impl.cc:2126:14
    #25 0x5a477336f4c3 in content::RenderFrameImpl::CreateFrame(content::AgentSchedulingGroup&, base::TokenType<blink::LocalFrameTokenTypeMarker> const&, int, mojo::PendingAssociatedReceiver<content::mojom::Frame>, mojo::PendingRemote<blink::mojom::BrowserInterfaceBroker>, mojo::PendingAssociatedRemote<blink::mojom::AssociatedInterfaceProvider>, blink::WebView*, std::__Cr::optional<blink::MultiToken<base::TokenType<blink::LocalFrameTokenTypeMarker>, base::TokenType<blink::RemoteFrameTokenTypeMarker>>> const&, std::__Cr::optional<blink::MultiToken<base::TokenType<blink::LocalFrameTokenTypeMarker>, base::TokenType<blink::RemoteFrameTokenTypeMarker>>> const&, std::__Cr::optional<blink::MultiToken<base::TokenType<blink::LocalFrameTokenTypeMarker>, base::TokenType<blink::RemoteFrameTokenTypeMarker>>> const&, std::__Cr::optional<blink::MultiToken<base::TokenType<blink::LocalFrameTokenTypeMarker>, base::TokenType<blink::RemoteFrameTokenTypeMarker>>> const&, base::UnguessableToken const&, blink::mojom::TreeScopeType, mojo::StructPtr<blink::mojom::FrameReplicationState>, mojo::StructPtr<content::mojom::CreateFrameWidgetParams>, mojo::StructPtr<blink::mojom::FrameOwnerProperties>, bool, base::TokenType<blink::DocumentTokenTypeMarker> const&, mojo::StructPtr<blink::mojom::PolicyContainer>, bool) ./../../content/renderer/render_frame_impl.cc:1774:17
    #26 0x5a47734d7519 in content::AgentSchedulingGroup::CreateFrame(mojo::StructPtr<content::mojom::CreateFrameParams>) ./../../content/renderer/agent_scheduling_group.cc:420:3
    #27 0x5a474f11f058 in content::mojom::AgentSchedulingGroupStubDispatch::Accept(content::mojom::AgentSchedulingGroup*, mojo::Message*) ./gen/content/common/agent_scheduling_group.mojom.cc:659:13
    #28 0x5a475d72a387 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #29 0x5a475d7463aa in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #30 0x5a475d72f565 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #31 0x5a475e53b25e in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1198:24
    #32 0x5a475e53c8c3 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:738:12
    #33 0x5a475e53c8c3 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:930:12
    #34 0x5a475e53c8c3 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #35 0x5a475e53c8c3 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #36 0x5a475c036ba4 in Run ./../../base/functional/callback.h:156:12
    #37 0x5a475c036ba4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #38 0x5a475c097614 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #39 0x5a475c097614 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #40 0x5a475c09652d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #41 0x5a475c09834a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #42 0x5a475bf2e43d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #43 0x5a475c098fc6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12
    #44 0x5a475bfc7eef in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #45 0x5a47735dd003 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:368:16
    #46 0x5a475972d5d9 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #47 0x5a475972eb2e in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #48 0x5a47597316c1 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1153:10
    #49 0x5a475972b900 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:332:36
    #50 0x5a475972bf7b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:345:10
    #51 0x5a4749ec00d8 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #52 0x70ae72e29d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/asan-linux-release/chrome+0x2dc79e96) (BuildId: 6e446cb7a79af4cb)
Shadow bytes around the buggy address:
  0x511000252580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x511000252600: fa fa fa fa fa fa f7 fa fa fa fa fa fa fa fa fa
  0x511000252680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x511000252700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x511000252780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x511000252800: fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd
  0x511000252880: fa fa fa fa fa fa f7 fa fa fa fa fa fa fa fa fa
  0x511000252900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x511000252980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x511000252a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x511000252a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==1==ADDITIONAL INFO

==1==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5a475d7ad267 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:102:13


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1==END OF ADDITIONAL INFO
==1==ABORTING
  

## Attachments

- [crash.html](attachments/crash.html) (text/html, 207 B)
- [launcher.sh](attachments/launcher.sh) (text/x-sh, 811 B)
- [asan.log](attachments/asan.log) (text/plain, 44.9 KB)
- crash.html (text/html, 197 B)
- [child.html](attachments/child.html) (text/html, 421 B)
- [1.js](attachments/1.js) (text/javascript, 292 B)

## Timeline

### th...@chromium.org (2024-04-30)

I see that crash.html currently opens a specific link. Could you instead upload a POC without that baidu URL? The goal is for the POC not to have dependencies on things that might change in the future.

### pe...@google.com (2024-05-01)

The NextAction date has arrived: 2024-05-01 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### th...@chromium.org (2024-05-01)

I've applied the patch locally on HEAD on gLinux, and have run the script, but am not able to reproduce this ~5-10 minutes after the script has started running.

Reporter, is the baidu URL required? A minimized POC without dynamic dependencies would be helpful to make sure we're running the same test case.

### em...@gmail.com (2024-05-02)

In fact, the Baidu URL is not necessary; it just so happens that the JS file loading code on Baidu's homepage allows me to reproduce the issue stably locally.

I have revised the PoC. Could you please test it again?

repro steps
1. Copy 10 js files.
    for i in {2..10}; do cp 1.js $i.js; done
2. ./launcher.sh ./chrome http://localhost:8880/crash.html 10 2>&1

### pe...@google.com (2024-05-02)

Thank you for providing more feedback. Adding the requester to the CC list.

### th...@chromium.org (2024-05-02)

Thanks for the revised POC and the clear repro steps. Unfortunately I still can't reproduce this. This is on a local asan build with the patch on gLinux, Chromium version 126.0.6449.0. I see that the version I'm using is slightly newer than the version you used. Reporter - could you sanity check that you're still able to reproduce this on HEAD? Also, let me know if there's any other setup you think I'm missing.

leszeks@ - the Security Team is unable to reproduce this issue based on information provided. If you can diagnose and fix the issue based on the asan stack trace (or if you are able to reproduce it with the provided POC in [#comment5](https://issues.chromium.org/issues/337998760#comment5)), please proceed accordingly. Please provide a comment about when this issue may have been introduced or which active release branches of Chrome may be impacted.

This information is critical so that we can ensure fixes are released urgently to help protect against n-day exploitation of newly landed security fixes, and so that we can avoid release of security regressions.

Setting the severity based on the stack trace - high, since this is a UAF in the renderer process, not protected by MiraclePtr. Not setting a Found In -- we can set one if leszeks@ is able to comment on when the issue may have been introduced.

### le...@chromium.org (2024-05-02)

horo@, PTAL -- it looks like in `BackgroundResourceScriptStreamer::BackgroundProcessor`, calling `watcher_->Watch` with a bound `WTF::Unretained(this)` isn't safe (I guess the `BackgroundProcessor` can die between the watcher posting the callback for execution, and the posted task actually executing). I'm thinking that `this` should be passed in by weak reference rather than unretained, similar to how the non-background `ResourceScriptStreamer` does it.

### le...@chromium.org (2024-05-02)

thefrog@, this is a relatively new feature and is currently being finched at 1% stable from M124 behind the BackgroundResourceFetch feature. As near as I can tell, I think it's a legitimate UAF.

### th...@chromium.org (2024-05-02)

Thanks! Setting the Found In to 124. Not setting the Security\_Impact-None hotlist since this is the default configuration for some users.

### pe...@google.com (2024-05-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-02)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-05-02)

The NextAction date has arrived: 2024-05-02 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ho...@chromium.org (2024-05-07)

I can't reproduce it using Chromium. But I can reproduce it in an unit test.

I created <https://chromium-review.googlesource.com/c/chromium/src/+/5514715> to fix this issue.

The BackgroundResourceFetch feature is not enabled on Stable yet. So I think the Severity of this issue is lower than S1.

### em...@gmail.com (2024-05-07)

I confirm that the issue has not been reproduced after applying the patch mentioned above.

### ho...@chromium.org (2024-05-07)

Re: [#comment15](https://issues.chromium.org/issues/337998760#comment15)

Thank you very much for verifying it.

### ap...@google.com (2024-05-08)

Project: chromium/src
Branch: main

commit 125bc950b30728d400f1dadc46715443f6d011e2
Author: Tsuyoshi Horo <horo@chromium.org>
Date:   Wed May 08 14:16:52 2024

    Fix UAF issue in BackgroundProcessor::OnDataPipeReadable
    
    There is an UAF issue in BackgroundProcessor::OnDataPipeReadable.
    BackgroundProcessor::MaybeStartProcessingResponse() is calling
    SimpleWatcher::Watch() with a bound WTF::Unretained(this). This is not
    safe. BackgroundProcessor::OnDataPipeReadable() can be called even after
    the BackgroundProcessor is deleted in the main thread (not in the
    background thread). This is because the SimpleWatcher will not be
    canceled until the deletion task is executed in the background thread.
    
    To fix this issue, this CL changes BackgroundProcessor::
    MaybeStartProcessingResponse() method to call SimpleWatcher::Watch()
    with a scoped_refptr(this), and changes BackgroundProcessor::Cancel()
    to reset the SimpleWatcher.
    
    Fixed: 337998760
    Change-Id: I7d376a25dad3a992510e3575075b0e471ef4ebf9
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5514715
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Commit-Queue: Kouhei Ueno <kouhei@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1298079}

M       third_party/blink/renderer/bindings/core/v8/DEPS
M       third_party/blink/renderer/bindings/core/v8/script_streamer.cc
M       third_party/blink/renderer/bindings/core/v8/script_streamer_test.cc

https://chromium-review.googlesource.com/5514715


### pe...@google.com (2024-05-08)

Requesting merge to stable (M124) because latest trunk commit (1298079) appears to be after stable branch point (1274542).
Requesting merge to beta (M125) because latest trunk commit (1298079) appears to be after beta branch point (1287751).
Merge review required: a commit with DEPS changes was detected.


Merge review required: a commit with DEPS changes was detected.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-05-09)

Hi horo@, thanks fre [comment #14](https://issues.chromium.org/issues/337998760#comment14) `The BackgroundResourceFetch feature is not enabled on Stable yet. So I think the Severity of this issue is lower than S1.`

It seems that BackgroundResourceFetch is being finched at 1% on Stable as per c#9, as such this would remain a P1/S1 and should undergo security merge review. Since this fix just landed today, it should get a bit more bake time before we review it for potential backmerge, so we will reassess tomorrow or Friday. Thanks!

### ho...@chromium.org (2024-05-09)

I think the [comment #9](https://issues.chromium.org/issues/337998760#comment9) is not correct. We are running Finch preperiod. 1% Stable experiment is not started yet. See cl/623379656.

### am...@chromium.org (2024-05-09)

Ah, thanks for linking the CL. I just checked finch the UMA metrics it looks like BackgroundResourceFetch is enabled in Beta. So I don't think this fix needs to be backmerged to M124 Stable, but does need backmerged to M125 Beta.

### ho...@chromium.org (2024-05-09)


1. Which CLs should be backmerged? (Please include Gerrit links.)
  https://chromium-review.googlesource.com/c/chromium/src/+/5514715
2. Has this fix been verified on Canary to not pose any stability regressions?
  Yes
3. Does this fix pose any potential non-verifiable stability risks?
  No
4. Does this fix pose any known compatibility risks?
  No
5. Does it require manual verification by the test team? If so, please describe required testing.
  No

### ho...@chromium.org (2024-05-10)

According to [Chromium Dash](https://chromiumdash.appspot.com/schedule), M126 will go to Beta in May 15.

[amyressler@chromium.org](mailto:amyressler@chromium.org)

Do you think we still need to merge the CL to M125?

### am...@chromium.org (2024-05-11)

That's true, I suppose this does not need to be backmerged since it won't make it to the 125 before Stable promotion

### sp...@google.com (2024-05-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$3,000 for this report of mildly mitigated memory corruption in a sandboxed process, mitigated by race condition; this seems like a very tight race, but we also appreciate the revised POC and additional information you provided after the original report

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### pe...@google.com (2024-08-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/337998760)*
