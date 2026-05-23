# Security: heap-use-after-free in v8::Isolate::SuppressMicrotaskExecutionScope::~SuppressMicrotaskExe

| Field | Value |
|-------|-------|
| **Issue ID** | [471257336](https://issues.chromium.org/issues/471257336) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 143.0.0.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2025-12-24 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

1. compile asan chromium on MacOS

```
git checkout ae55321b9e200251d87f1a5c3f83c9b29b81dad1
git apply poc.diff
gn gen out/asan-1220 --args="is_component_build=true is_debug=false is_asan=true symbol_level=2 dcheck_always_on=false treat_warnings_as_errors=false"

```

2. run asan chromium on MacOS:

```
./out/asan-1220/Chromium.app/Contents/MacOS/Chromium --no-sandbox --user-data-dir=/tmp/userdata/t1 http://127.0.0.1/poc.html

```

Avoid deploying index.html in the HTTP service whenever possible; preserve the ability to list directories.Multiple visits to poc.html will reliably trigger the UAF.See poc.mov.

# Problem Description

RCA and bisect commit coming soon!

# Summary

Security: heap-use-after-free in v8::Isolate::SuppressMicrotaskExecutionScope::~SuppressMicrotaskExe

# Custom Questions

#### Type of crash:

--type=renderer

#### Crash state:

```
=================================================================
==33240==ERROR: AddressSanitizer: heap-use-after-free on address 0x60d0001db7f4 at pc 0x00015bb8e600 bp 0x00016ef3d7c0 sp 0x00016ef3d7b8
READ of size 4 at 0x60d0001db7f4 thread T0
==33240==WARN: Invalid dyld module map detected. This is most likely a bug in the sanitizer.
==33240==WARN: Backtraces may be unreliable.
==33240==WARNING: invalid path to external symbolizer!
==33240==WARNING: Failed to use and restart external symbolizer!
    #0 0x00015bb8e5fc in v8::Isolate::SuppressMicrotaskExecutionScope::~SuppressMicrotaskExecutionScope()+0xa4 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x27e5fc)
    #1 0x00014edebda0 in blink::LocalFrame::~LocalFrame()+0x1e8 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x1647da0)
    #2 0x00015dfb5660 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizePage(cppgc::internal::(anonymous namespace)::SweepingState::SweptPageState*)+0xc4 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x26a5660)
    #3 0x00015dfb8c40 in cppgc::internal::(anonymous namespace)::MutatorThreadSweeper::FinalizeAndSweepWithDeadline(cppgc::internal::StatsCollector::ScopeId, cppgc::internal::(anonymous namespace)::SweepingState&, v8::base::TimeTicks, cppgc::internal::(anonymous namespace)::MutatorThreadSweepingMode)+0x2cc (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x26a8c40)
    #4 0x00015dfaabb0 in cppgc::internal::Sweeper::SweeperImpl::PerformSweepOnMutatorThread(v8::base::TimeDelta, cppgc::internal::StatsCollector::ScopeId, cppgc::internal::(anonymous namespace)::MutatorThreadSweepingMode)+0x584 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x269abb0)
    #5 0x00015dfb1b40 in cppgc::internal::Sweeper::SweeperImpl::SweepInForegroundTaskImpl(v8::base::TimeDelta, cppgc::internal::StatsCollector::ScopeId)+0xd0 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x26a1b40)
    #6 0x00015dfb181c in cppgc::internal::Sweeper::SweeperImpl::SweepForLowPriorityTask(v8::base::TimeDelta)+0x4c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x26a181c)
    #7 0x0001405993a8 in base::internal::Invoker<base::internal::FunctorTraits<void (v8::Task::*&&)(), std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>&&>, base::internal::BindState<true, true, false, void (v8::Task::*)(), std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x11c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libgin.dylib:arm64+0x1d3a8)
    #8 0x0001033c9b40 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x1f9b40)
    #9 0x000103447190 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x860 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x277190)
    #10 0x000103446574 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x276574)
    #11 0x00010326c828 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x204 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x9c828)
    #12 0x000103448538 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x278538)
    #13 0x000103335538 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x165538)
    #14 0x000133f632e8 in content::RendererMain(content::MainFunctionParams)+0x8dc (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3ad72e8)
    #15 0x00013419eef0 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x42c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3d12ef0)
    #16 0x0001341a0f40 in content::ContentMainRunnerImpl::Run()+0x474 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3d14f40)
    #17 0x00013419c8fc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3d108fc)
    #18 0x00013419cdec in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3d10dec)
    #19 0x000118a1cbf8 in ChromeMain+0x490 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libchrome_dll.dylib:arm64+0xcbf8)
    #20 0x000100ec0b94 in main+0x254 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/145.0.7588.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000b94)
    #21 0x000187799d50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

0x60d0001db7f4 is located 68 bytes inside of 136-byte region [0x60d0001db7b0,0x60d0001db838)
freed by thread T0 here:
    #0 0x000101719438 in __sanitizer_finish_switch_fiber+0xa04 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libclang_rt.asan_osx_dynamic.dylib:arm64+0x65438)
    #1 0x00015bfc07a0 in v8::internal::MicrotaskQueue::~MicrotaskQueue()+0xf0 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x6b07a0)
    #2 0x000157a7b3c4 in blink::scheduler::EventLoop::~EventLoop()+0x80 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_platform.dylib:arm64+0xc833c4)
    #3 0x00014eb2e564 in blink::Agent::~Agent()+0xac (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x138a564)
    #4 0x00015dfb5660 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizePage(cppgc::internal::(anonymous namespace)::SweepingState::SweptPageState*)+0xc4 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x26a5660)
    #5 0x00015dfb8c40 in cppgc::internal::(anonymous namespace)::MutatorThreadSweeper::FinalizeAndSweepWithDeadline(cppgc::internal::StatsCollector::ScopeId, cppgc::internal::(anonymous namespace)::SweepingState&, v8::base::TimeTicks, cppgc::internal::(anonymous namespace)::MutatorThreadSweepingMode)+0x2cc (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x26a8c40)
    #6 0x00015dfaabb0 in cppgc::internal::Sweeper::SweeperImpl::PerformSweepOnMutatorThread(v8::base::TimeDelta, cppgc::internal::StatsCollector::ScopeId, cppgc::internal::(anonymous namespace)::MutatorThreadSweepingMode)+0x584 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x269abb0)
    #7 0x00015dfb1b40 in cppgc::internal::Sweeper::SweeperImpl::SweepInForegroundTaskImpl(v8::base::TimeDelta, cppgc::internal::StatsCollector::ScopeId)+0xd0 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x26a1b40)
    #8 0x00015dfb181c in cppgc::internal::Sweeper::SweeperImpl::SweepForLowPriorityTask(v8::base::TimeDelta)+0x4c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x26a181c)
    #9 0x0001405993a8 in base::internal::Invoker<base::internal::FunctorTraits<void (v8::Task::*&&)(), std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>&&>, base::internal::BindState<true, true, false, void (v8::Task::*)(), std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x11c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libgin.dylib:arm64+0x1d3a8)
    #10 0x0001033c9b40 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x1f9b40)
    #11 0x000103447190 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x860 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x277190)
    #12 0x000103446574 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x276574)
    #13 0x00010326c828 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x204 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x9c828)
    #14 0x000103448538 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x278538)
    #15 0x000103335538 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x165538)
    #16 0x000133f632e8 in content::RendererMain(content::MainFunctionParams)+0x8dc (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3ad72e8)
    #17 0x00013419eef0 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x42c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3d12ef0)
    #18 0x0001341a0f40 in content::ContentMainRunnerImpl::Run()+0x474 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3d14f40)
    #19 0x00013419c8fc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3d108fc)
    #20 0x00013419cdec in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3d10dec)
    #21 0x000118a1cbf8 in ChromeMain+0x490 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libchrome_dll.dylib:arm64+0xcbf8)
    #22 0x000100ec0b94 in main+0x254 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/145.0.7588.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000b94)
    #23 0x000187799d50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

previously allocated by thread T0 here:
    #0 0x000101719050 in __sanitizer_finish_switch_fiber+0x61c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libclang_rt.asan_osx_dynamic.dylib:arm64+0x65050)
    #1 0x00015bfc0140 in v8::internal::MicrotaskQueue::New(v8::internal::Isolate*)+0x24 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x6b0140)
    #2 0x00015bb93b38 in v8::MicrotaskQueue::New(v8::Isolate*, v8::MicrotasksPolicy)+0x1c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x283b38)
    #3 0x00014eb46700 in blink::WindowAgent::WindowAgent(blink::AgentGroupScheduler&, bool, bool)+0x124 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x13a2700)
    #4 0x00014eb47774 in blink::WindowAgentFactory::GetAgentForOrigin(bool, blink::SecurityOrigin const*, bool, bool)+0x91c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x13a3774)
    #5 0x000150439c28 in blink::DocumentLoader::InitializeWindow(blink::Document*)+0x9f0 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x2c95c28)
    #6 0x00015043cc70 in blink::DocumentLoader::CommitNavigation()+0x33c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x2c98c70)
    #7 0x00015049a42c in blink::FrameLoader::CommitDocumentLoader(blink::DocumentLoader*, blink::HistoryItem*, blink::CommitReason)+0x508 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x2cf642c)
    #8 0x0001504a3dec in blink::FrameLoader::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_delete<blink::WebDocumentLoader::ExtraData>>, blink::CommitReason)+0x13b4 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x2cffdec)
    #9 0x00014f05042c in blink::WebLocalFrameImpl::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_delete<blink::WebDocumentLoader::ExtraData>>)+0x390 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x18ac42c)
    #10 0x000133ed0eb4 in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)+0xe20 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3a44eb4)
    #11 0x000133f1b1a4 in void base::internal::DecayedFunctorTraits<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&>::Invoke<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl> const&, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>>(void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl> const&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>&&)+0x384 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3a8f1a4)
    #12 0x000133f1ad74 in base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameImpl::*&&)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&>, base::internal::BindState<true, true, false, void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>>, void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>&&)+0x164 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3a8ed74)
    #13 0x000133ed1ce4 in base::OnceCallback<void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)>::Run(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>) &&+0x148 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3a45ce4)
    #14 0x000133ecd514 in content::RenderFrameImpl::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, std::__Cr::optional<std::__Cr::vector<network::ParsedPermissionsPolicyDeclaration, std::__Cr::allocator<network::ParsedPermissionsPolicyDeclaration>>> const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>)+0x2300 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3a41514)
    #15 0x000133eae98c in content::NavigationClient::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, std::__Cr::optional<std::__Cr::vector<network::ParsedPermissionsPolicyDeclaration, std::__Cr::allocator<network::ParsedPermissionsPolicyDeclaration>>> const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>)+0x514 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3a2298c)
    #16 0x000130a55564 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(content::mojom::NavigationClient*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>)+0xec8 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x5c9564)
    #17 0x000101169dec in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8b8 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libmojo_public_cpp_bindings.dylib:arm64+0x25dec)
    #18 0x000101180060 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libmojo_public_cpp_bindings.dylib:arm64+0x3c060)
    #19 0x00010116f024 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libmojo_public_cpp_bindings.dylib:arm64+0x2b024)
    #20 0x000106919be4 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)+0x3e8 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libipc.dylib:arm64+0x39be4)
    #21 0x00010691bc50 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1b8 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libipc.dylib:arm64+0x3bc50)
    #22 0x0001033c9b40 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x1f9b40)
    #23 0x000103447190 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x860 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x277190)
    #24 0x000103446574 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x276574)
    #25 0x00010326c828 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x204 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x9c828)
    #26 0x000103448538 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x278538)
    #27 0x000103335538 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libbase.dylib:arm64+0x165538)
    #28 0x000133f632e8 in content::RendererMain(content::MainFunctionParams)+0x8dc (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3ad72e8)
    #29 0x00013419eef0 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x42c (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libcontent.dylib:arm64+0x3d12ef0)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libv8.dylib:arm64+0x27e5fc) in v8::Isolate::SuppressMicrotaskExecutionScope::~SuppressMicrotaskExecutionScope()+0xa4
Shadow bytes around the buggy address:
  0x60d0001db500: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x60d0001db580: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x60d0001db600: f7 fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x60d0001db680: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd
  0x60d0001db700: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
=>0x60d0001db780: fa fa fa fa f7 fa fd fd fd fd fd fd fd fd[fd]fd
  0x60d0001db800: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
  0x60d0001db880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x60d0001db900: fd fd fa fa fa fa fa fa f7 fa fd fd fd fd fd fd
  0x60d0001db980: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x60d0001dba00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
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

==33240==ADDITIONAL INFO

==33240==Note: Please include this section with the ASan report.
Task trace:
    #0 0x000140598a9c in gin::V8ForegroundTaskRunner::PostNonNestableTaskImpl(std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>, v8::SourceLocation const&)+0xe0 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libgin.dylib:arm64+0x1ca9c)
    #1 0x0001515b4810 in blink::HTMLDocumentParser::SchedulePumpTokenizer(bool)+0x1f8 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libblink_core.dylib:arm64+0x3e10810)
    #2 0x00010690f708 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*)+0x790 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libipc.dylib:arm64+0x2f708)
    #3 0x0001026284b0 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x230 (/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/libmojo_public_system_cpp.dylib:arm64+0x1c4b0)

Command line: `/Users/zh1x1an1221/chrome_source/src-chromium/src/out/asan-1220/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/145.0.7588.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=/tmp/userdata/t1 --enable-isolated-web-apps-in-renderer --no-sandbox --lang=zh-CN --touch-selection-strategy=direction --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=6 --time-ticks-at-unix-epoch=-1763876156903056 --launch-time-ticks=2700923538415 --shared-files --metrics-shmem-handle=1752395122,r,10973751167872732220,14562857273337120962,2097152 --field-trial-handle=1718379636,r,16261221570192847312,13063363047131094528,262144 --disable-features=AsanBrpExtractionCheck,BindReceiversEverytime,CancelNavigationsDuringBrowserContextShutdown,ConnectionAllowlists,ConnectionKeepAliveForHttp2,DataCollectionModeForScreen2x,EnableDrDc,InitialWebUI,NoCompositorFrameAcks,RawDraw,RebindPreconnectReceivers,ScreenAITestMode,SegmentationPlatformFeedSegmentFeature,SoftNavigationDetection,TransientKeepAlivePolicy,TreesInViz,UseLayerListsByDefault,UseNewTabbedBrowserLayout,VerticalTabs,VizDirectCompositorThreadIpcFrameSinkManager,VizDirectCompositorThreadIpcNonRoot,Webium --variations-seed-version --trace-process-track-uuid=3190708991934122588`

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==33240==END OF ADDITIONAL INFO

==33240==ABORTING

```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 37.8 KB)
- [poc.diff](attachments/poc.diff) (text/x-diff, 577.6 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 81.3 MB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [a.html](attachments/a.html) (text/html, 2.2 KB)
- [b.html](attachments/b.html) (text/html, 4.6 KB)
- [newpoc.mov](attachments/newpoc.mov) (video/quicktime, 100.1 MB)

## Timeline

### zh...@gmail.com (2025-12-24)

After simplification, triggering this vulnerability requires only one feature: `BackForwardCachePauseMicrotasks`

```
--no-sandbox --user-data-dir=/tmp/userdata/t1 http://127.0.0.1 --enable-features=BackForwardCachePauseMicrotasks

```

### zh...@gmail.com (2025-12-24)

## Bisect commit:

<https://chromium-review.googlesource.com/c/chromium/src/+/7256111>

### zh...@gmail.com (2025-12-24)

Incidentally, the vulnerability cannot be triggered via the above proof-of-concept (PoC) on Windows and Linux; it can only be triggered on macOS.

### zh...@gmail.com (2025-12-25)

## RCA here

To understand this vulnerability, we need to first understand the lifecycle of the relevant class objects one by one:
The first class is [MicrotaskQueue](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/execution/microtask-queue.h;drc=bfb4a0495275f0eead9d6a91ea1475745bb64385;l=27) This class is responsible for storing and scheduling microtasks; and maintaining a count of "microtasks suppressions".

<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/execution/microtask-queue.h;l=78-81;drc=46c1a6ef75cc6ea1367e43d14c9529aadb07c683;bpv=0;bpt=1>

```
// Possibly nested microtasks suppression scopes prevent microtasks
  // from running.
  void IncrementMicrotasksSuppressions() { ++microtasks_suppressions_; }
  void DecrementMicrotasksSuppressions() { --microtasks_suppressions_; }
  bool HasMicrotasksSuppressions() const {
    return microtasks_suppressions_ != 0;
  }

```

The second class is [SuppressMicrotaskExecutionScope](https://source.chromium.org/chromium/chromium/src/+/main:v8/include/v8-isolate.h;l=454;drc=bfb4a0495275f0eead9d6a91ea1475745bb64385) ，It is the RAII-style "pause microtask execution" scope. It stores `internal::MicrotaskQueue* const microtask_queue_;` ,Therefore, this vulnerability cannot be protected by the miracle pointer.

```
/**
   * Do not run microtasks while this scope is active, even if microtasks are
   * automatically executed otherwise.
   */
  class V8_EXPORT V8_NODISCARD SuppressMicrotaskExecutionScope {
   public:
    explicit SuppressMicrotaskExecutionScope(
        Isolate* isolate, MicrotaskQueue* microtask_queue = nullptr);
    ~SuppressMicrotaskExecutionScope();

    // Prevent copying of Scope objects.
    SuppressMicrotaskExecutionScope(const SuppressMicrotaskExecutionScope&) =
        delete;
    SuppressMicrotaskExecutionScope& operator=(
        const SuppressMicrotaskExecutionScope&) = delete;

   private:
    internal::Isolate* const i_isolate_;
    internal::MicrotaskQueue* const microtask_queue_; // Not protected by the miracle pointer
    internal::Address previous_stack_height_;

    friend class internal::ThreadLocalTop;
  };

```

Let's take a look at the constructor and destructor code of the `SuppressMicrotaskExecutionScope` class:
<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/api/api.cc;l=10124-10137;drc=bfb4a0495275f0eead9d6a91ea1475745bb64385?q=content:%22Isolate::SuppressMicrotaskExecutionScope::SuppressMicrotaskExecutionScope(%22>

```
Isolate::SuppressMicrotaskExecutionScope::SuppressMicrotaskExecutionScope( // SuppressMicrotaskExecutionScope constructor
    Isolate* v8_isolate, MicrotaskQueue* microtask_queue)
    : i_isolate_(reinterpret_cast<i::Isolate*>(v8_isolate)),
      microtask_queue_(microtask_queue
                           ? static_cast<i::MicrotaskQueue*>(microtask_queue)
                           : i_isolate_->default_microtask_queue()) {
  i_isolate_->thread_local_top()->IncrementCallDepth<true>(this);
  microtask_queue_->IncrementMicrotasksSuppressions();
}

Isolate::SuppressMicrotaskExecutionScope::~SuppressMicrotaskExecutionScope() { // SuppressMicrotaskExecutionScope destructor
  microtask_queue_->DecrementMicrotasksSuppressions();
  i_isolate_->thread_local_top()->DecrementCallDepth(this);
}

```

During construction, `IncrementMicrotasksSuppressions()` is executed on a specific `MicrotaskQueue`.
During destruction, `DecrementMicrotasksSuppressions()` is executed on the same queue.

Because the `SuppressMicrotaskExecutionScope` class stores a raw pointer to `MicrotaskQueue`, the lifetime of the `SuppressMicrotaskExecutionScope` class cannot be outlive `MicrotaskQueue`. Otherwise, when `SuppressMicrotaskExecutionScope` is destructed, the dangling pointer will be dereferenced, resulting in a UAF (Undefined Action Default).

Having explained the `SuppressMicrotaskExecutionScope` and `MicrotaskQueue` classes, we also need to look at `blink::scheduler::EventLoop` and `EventLoop::PauseMicrotasksHandle`:
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/scheduler/public/event_loop.h;l=57-136?q=class%20PauseMicrotasksHandle%20%7B>

It is Blink's event loop object; it holds a `std::unique_ptr<v8::MicrotaskQueue>` (which is the actual owner of the queue) and provides the `PauseMicrotasks` function, which produces a `handle` to pause `microtasks` for the duration of the `handle`. Focus on the following:

```
class PauseMicrotasksHandle {
 public:
  ~PauseMicrotasksHandle() = default;

 private:
  friend class EventLoop;
  PauseMicrotasksHandle(scoped_refptr<EventLoop> keep_alive,
                        v8::Isolate* isolate,
                        v8::MicrotaskQueue* queue);

  // Keep |microtask_queue_| alive while |scope_|'s destructor runs.
  scoped_refptr<EventLoop> keep_alive_;
  v8::Isolate::SuppressMicrotaskExecutionScope scope_; // PauseMicrotasksHandle own SuppressMicrotaskExecutionScope
};

std::unique_ptr<v8::MicrotaskQueue> microtask_queue_;

```

Because `PauseMicrotasksHandle` owns `SuppressMicrotaskExecutionScope`, the destruction of `PauseMicrotasksHandle` will trigger the destruction of `SuppressMicrotaskExecutionScope`. Therefore, `handle` must ensure that the `MicrotaskQueue` it references is still alive before its destruction.

Let's look at the key functions that trigger the vulnerability: `blink::LocalFrame::HookBackForwardCacheEviction` and `blink::LocalFrame::RemoveBackForwardCacheEviction`.

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/local_frame.cc;l=1183-1235>

```
void LocalFrame::HookBackForwardCacheEviction() {
  TRACE_EVENT0("blink", "LocalFrame::HookBackForwardCacheEviction");
  // Register a callback dispatched when JavaScript is executed on the frame.
  // The callback evicts the frame. If a frame is frozen by BackForwardCache,
  // the frame must not be mutated e.g., by JavaScript execution, then the
  // frame must be evicted in such cases.
  DCHECK(RuntimeEnabledFeatures::BackForwardCacheEnabled());
  if (base::FeatureList::IsEnabled(
          features::kBackForwardCachePauseMicrotasks)) {
    if (LocalDOMWindow* window = DomWindow()) {
      microtasks_pauser_ = window->GetAgent()->event_loop()->PauseMicrotasks();
    }
  }
  static_cast<LocalWindowProxyManager*>(GetWindowProxyManager())
      ->SetAbortScriptExecution(
          [](v8::Isolate* isolate, v8::Local<v8::Context> context) {
            ScriptState* script_state = ScriptState::From(isolate, context);
            LocalDOMWindow* window = LocalDOMWindow::From(script_state);
            DCHECK(window);
            LocalFrame* frame = window->GetFrame();
            if (frame) {
              SourceLocation* source_location = nullptr;
              if (base::FeatureList::IsEnabled(
                      features::kCaptureJSExecutionLocation)) {
                // Capture the source location of the JS execution if the flag
                // is enabled.
                source_location = CaptureSourceLocation();
              }
              frame->EvictFromBackForwardCache(
                  mojom::blink::RendererEvictionReason::kJavaScriptExecution,
                  source_location);
              if (base::FeatureList::IsEnabled(
                      features::kBackForwardCacheDWCOnJavaScriptExecution)) {
                // Adding |DumpWithoutCrashing()| here to make sure this is not
                // happening in any tests, except for when this is expected.
                base::debug::DumpWithoutCrashing();
              }
            }
          });
}

void LocalFrame::RemoveBackForwardCacheEviction() {
  TRACE_EVENT0("blink", "LocalFrame::RemoveBackForwardCacheEviction");
  DCHECK(RuntimeEnabledFeatures::BackForwardCacheEnabled());
  static_cast<LocalWindowProxyManager*>(GetWindowProxyManager())
      ->SetAbortScriptExecution(nullptr);

  // The page is being restored, and from this point eviction should not happen
  // for any reason. Change the deferring state from |kBufferIncoming| to
  // |kStrict| so that network related eviction cannot happen.
  GetDocument()->Fetcher()->SetDefersLoading(LoaderFreezeMode::kStrict);
  microtasks_pauser_.reset();
}

```

When the page enters BFCache, a callback is registered when JavaScript is executed on the frame; and when `features::kBackForwardCachePauseMicrotasks` is enabled, a microtasks\_pauser\_ is created to pause microtasks; and when the page is restored, `microtasks_pauser_.reset();` is executed.

In any case, the release of `microtasks_pauser_` must occur while the `EventLoop/MicrotaskQueue` it depends on is still alive.

An expected call chain should look like this:

1. Navigation initialization of `WindowAgent` creates `v8::MicrotaskQueue`, which is then handed over to `blink::Agent`. Internally, the Agent creates and holds an `EventLoop`, which in turn holds the queue (unique\_ptr owner).
2. Entering `BFCache` (i.e., `LocalFrame::HookBackForwardCacheEviction`), `microtasks_pauser_ = event_loop->PauseMicrotasks()` is executed. Then, the scope constructor executes `++microtasks_suppressions_;` on the queue.
3. Exiting `BFCache` (i.e., `LocalFrame::RemoveBackForwardCacheEviction()`), `microtasks_pauser_.reset()` is executed. Then, the scope destructor executes `--microtasks_suppressions_` on the queue (the queue is still alive at this point).
4. Ensuring all `handles/scopes` are destroyed, then destroying them. Finally, release the MicrotaskQueue from the EventLoop.

However, the code cannot guarantee that the above logic will always hold true. Asan has proven that the lifecycle can be reversed, for the following reasons:

1. When `LocalFrame` enters `BFCache`, it creates a member `microtasks_pauser_` (not a local variable, but held across time).
2. `Agent` and `LocalFrame` are destructed by `Oilpan/cppgc` during the `sweep` phase (GC finalization).
3. The GC destruction order is not guaranteed to be sequential: if `Agent` is finalized first, it will release the last `EventLoop` reference, causing `EventLoop` to be destroyed and `MicrotaskQueue` to be deleted.
4. Only then is `LocalFrame` finalized. Although the function body of `LocalFrame::~LocalFrame()` is very short, it destroys its member `microtasks_pauser_` when the destruction ends. The destruction of `microtasks_pauser_` triggers the internal `SuppressMicrotaskExecutionScope` destruction, thus accessing the already released `MicrotaskQueue` ultimately leads to Undefined Activity Frame (UAF).

The READ size of 4 in ASAN is because `microtasks_suppressions_` is an integer, which is 4 bytes.

If you understand my analysis above, then the following will be easy to understand: the lifecycle of `PauseMicrotasksHandle` should be less than or equal to the lifecycle of the EventLoop/MicrotaskQueue it references.

However, `LocalFrame::microtasks_pauser_` is a `handle` held across phases, but it has no mechanism to ensure that `EventLoop` is destructed later than LocalFrame during GC finalization. Under Oilpan GC, it is perfectly reasonable for Agent to be destructed first, so the order of "queue freed first, handle destructed later" is reversed, and UAF is finally triggered when SuppressMicrotaskExecutionScope is destructed.

Disclaimer: I am not a professional Chromium developer. Based on the analysis of the above vulnerability, I believe one suggestion to fix this vulnerability is to make `PauseMicrotasksHandle` strongly reference `EventLoop`, thereby indirectly ensuring the survival of `MicrotaskQueue` until `SuppressMicrotaskExecutionScope` is destructed.

### zh...@gmail.com (2025-12-25)

Again, this is for reference only. I can confirm that this diff perfectly fixes the vulnerability on my computer, but it doesn't mean it's the most professional solution. I'm not a professional Chromium developer; the final decision rests with you.

```
diff --git a/third_party/blink/renderer/platform/scheduler/common/event_loop.cc b/third_party/blink/renderer/platform/scheduler/common/event_loop.cc
index 7f1228c0db466..df6c0ea635d0b 100644
--- a/third_party/blink/renderer/platform/scheduler/common/event_loop.cc
+++ b/third_party/blink/renderer/platform/scheduler/common/event_loop.cc
@@ -18,9 +18,10 @@ namespace blink {
 namespace scheduler {
 
 EventLoop::PauseMicrotasksHandle::PauseMicrotasksHandle(
+    scoped_refptr<EventLoop> keep_alive,
     v8::Isolate* isolate,
     v8::MicrotaskQueue* queue)
-    : scope_(isolate, queue) {}
+    : keep_alive_(std::move(keep_alive)), scope_(isolate, queue) {}
 
 EventLoop::EventLoop(Delegate* delegate,
                      v8::Isolate* isolate,
@@ -103,7 +104,8 @@ bool EventLoop::IsSchedulerAttachedForTest(FrameOrWorkerScheduler* scheduler) {
 
 std::unique_ptr<EventLoop::PauseMicrotasksHandle> EventLoop::PauseMicrotasks() {
   return base::WrapUnique(
-      new PauseMicrotasksHandle(isolate_, microtask_queue_.get()));
+      new PauseMicrotasksHandle(scoped_refptr<EventLoop>(this), isolate_,
+                                microtask_queue_.get()));
 }
 
 // static
diff --git a/third_party/blink/renderer/platform/scheduler/public/event_loop.h b/third_party/blink/renderer/platform/scheduler/public/event_loop.h
index 4066b809992fc..d77239664e80e 100644
--- a/third_party/blink/renderer/platform/scheduler/public/event_loop.h
+++ b/third_party/blink/renderer/platform/scheduler/public/event_loop.h
@@ -9,6 +9,7 @@
 
 #include "base/functional/callback.h"
 #include "base/memory/raw_ptr.h"
+#include "base/memory/scoped_refptr.h"
 #include "third_party/blink/renderer/platform/heap/garbage_collected.h"
 #include "third_party/blink/renderer/platform/heap/persistent.h"
 #include "third_party/blink/renderer/platform/platform_export.h"
@@ -104,8 +105,12 @@ class PLATFORM_EXPORT EventLoop final : public RefCounted<EventLoop> {
 
    private:
     friend class EventLoop;
-    PauseMicrotasksHandle(v8::Isolate* isolate, v8::MicrotaskQueue* queue);
+    PauseMicrotasksHandle(scoped_refptr<EventLoop> keep_alive,
+                          v8::Isolate* isolate,
+                          v8::MicrotaskQueue* queue);
 
+    // Keep |microtask_queue_| alive while |scope_|'s destructor runs.
+    scoped_refptr<EventLoop> keep_alive_;
     v8::Isolate::SuppressMicrotaskExecutionScope scope_;
   };
 


```

### cl...@appspot.gserviceaccount.com (2025-12-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5195346204360704.

### 24...@project.gserviceaccount.com (2025-12-26)

Testcase 5195346204360704 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5195346204360704.

### zh...@gmail.com (2025-12-26)

Hi team, I've updated the PoC to make it easier for you to test with clusterfuzz. The old PoC had some unoptimized user interactions, which might have made reproducing it with fuzzing more difficult. The new PoC mainly consists of two parts: `a.html` and `b.html`. Please ensure that a.html and b.html are in the same directory and that an HTTP service is running. Simply execute the following command, see `newpoc.mov`:

```
rm -rf /tmp/userdata/t1 ; ./out/asan-1225/Chromium.app/Contents/MacOS/Chromium --no-sandbox --user-data-dir=/tmp/userdata/t1 --enable-features=BackForwardCachePauseMicrotasks http://127.0.0.1/a.html

```

You can use the optimized PoC for testing within clusterfuzz.

### cl...@appspot.gserviceaccount.com (2025-12-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4560196776951808.

### sk...@google.com (2025-12-26)

Unable to reproduce. Assigning to the V8 shepherd and setting provisional severity/priority/FoundIn.

### ch...@google.com (2025-12-27)

Setting milestone because of s2 severity.

### ch...@google.com (2025-12-29)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ca...@chromium.org (2025-12-29)

This codepath has been disabled by flipping the kill switch (<https://crrev.com/c/7270265>) and a corresponding Finch update, so RB should no longer apply. Deduping into older issue, though thanks a lot to OP for filing, as this contains a more useful stack compared to what we've had before.

### zh...@gmail.com (2025-12-30)

Hi, according to the Chrome Vulnerability Reward Program Rules:<https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules>

> Duplicate reports

> Traditionally our policy related to duplicates has been strictly: "the earliest filed bug report in the bug tracker is considered the first report." Often we receive later versions of an earlier-reported security bug that are of such high quality that we use those components in advancing the triage or resolution of that issue. While this is against the core foundations of our policy around duplicate reports, we have made numerous exceptions and issued a small reward to the later reporter for their contributions that result in getting the security issue resolved.

> The Chrome VRP wants to better acknowledge and consistently reward these contributions. When a later-submitted report is of higher quality and is actively used by the security team or engineers to improve triage, reproduction, investigation, or root cause analysis of an earlier-reported issue, both reports may be eligible for the VRP reward -- with the total reward amount being divided between the two reports.

> This policy will only take effect when the security or engineering teams have actively used or acknowledged artifacts from a duplicate report to work toward resolution of a security issue. This policy is not applicable based solely on the existence of a duplicate report submitted in the same general period of time.

I saw the commit for the "Duplicate" report at <https://chromium-review.googlesource.com/q/message:+469686890>. In that report, I didn't see a reasonable analysis or proper fix for this vulnerability. The commit merely speculated and disabled the feature that triggered the issue, without resolving it. Therefore, I don't think it's reasonable or fair to simply label my high-quality analysis report as duplicate. As stated in the Chrome Vulnerability Reward Program Rules, please reconsider. I don't believe two reports with significant differences in quality can be labeled as Duplicate. Thank you.

### zh...@gmail.com (2025-12-30)

I carefully read <https://chromium-review.googlesource.com/q/message:469686890>, and I believe it completely fails to fix this issue:

1. Previous reports completely failed to recognize this as a heap-use-after-free memory vulnerability. You simply brute-forced rollbacks of potentially related commits, including:

```
7278708: Revert "[soft navs] Refactor pending ICP entry buffering",
7272305: Revert "[soft navs] Use a prefinalizer instead of UntracedMember for SoftNavigationContext",
7270524: Revert "[heap] Add notes for preempting/finishing jobs"

```

This rollback is meaningless and has nothing to do with the vulnerability. Because you didn't understand the root cause, this is just speculation and brute-force rollback.

2. The previous fix completely failed to resolve this heap-use-after-free memory vulnerability. I can still trigger the vulnerability in the latest version using `--enable-features=BackForwardCachePauseMicrotasks`, and I provided a detailed proof-of-concept (POC), reproduction steps, a bisect commit, and remediation suggestions—all of which were missing from the previous report.
3. If you believe my report is a duplicate of <https://chromium-review.googlesource.com/q/message:469686890>, do you think simply changing a feature from `ENABLED_BY_DEFAULT` back to `DISABLED_BY_DEFAULT` is the solution? This is unreasonable.

In other words, the previous "fix" did not address the root cause of this problem, and the vulnerability can still be triggered in the latest version.
Therefore, I disagree that the previous report has any right to duplicate my report; it was merely blind speculation and a brute-force rollback of unrelated commits, solving absolutely no problem.

### ca...@chromium.org (2025-12-30)

Ok, I've labeled this as duplicate because it is caused by the same root cause, and this was not a production issue at the moment of reporting since we've identified the problem and flipped the kill switch. That said, your report does provide valuable additional details. I will re-open the issue and defer to vulnerability reward program managers to make a call whether vulnerabilities detected in a code not enabled in production are eligible.

### zh...@gmail.com (2025-12-31)

Hi, thank you for your reply. However, blocking vulnerability trigger paths by toggling on/off switches is generally not a good choice. Good code maintains its lifecycle management without issues regardless of the trigger path, and it itself is free of vulnerabilities. As I suggested in #6, this is the most valuable patch for fixing a potential vulnerability. If all vulnerability fixes involve blocking trigger paths by disabling feature startup, instead of addressing the root cause of the vulnerability, then Chrome will retain a large number of potential memory safety issues. You never know when certain features might become the default startup setting and trigger which vulnerabilities, leading to increasingly poor code quality. Blocking trigger paths is not a good idea; fixing the root cause of the vulnerability is the truly effective solution.

### ca...@chromium.org (2026-01-02)

You can rest assured that we will land a proper fix, this is tracked by the issue this one was de-duped into. The flag flip is just for the sake of simplified release process. As for the chrome being less safe with certain command-line flags, there's already plenty of well known and well documented cases of that.

### ch...@google.com (2026-02-05)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-02-09)

Looks like this merge request slipped through the cracks (my bad). No merges are needed here though, as the Finch flag was enabled and then disabled again in M145.

### sp...@google.com (2026-02-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High quality memory corruption in a sandboxed process with a bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High quality memory corruption in a sandboxed process with a bisect

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/471257336)*
