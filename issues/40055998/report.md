# AddressSanitizer: use-after-poison frame_or_worker_scheduler.cc:88 in blink::FrameOrWorkerScheduler::NotifyLifecycleObservers

| Field | Value |
|-------|-------|
| **Issue ID** | [40055998](https://issues.chromium.org/issues/40055998) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Scheduling, Internals>Core, Internals>Skia |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | sh...@chromium.org |
| **Created** | 2021-05-25 |
| **Bounty** | $8,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4494.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-880310.zip

#Reproduce
python3.6m -m http.server 8000
chrome.exe --no-sandbox --js-flags='--expose_gc' --enable-blink-test-features --single-process --autoplay-policy=no-user-gesture-required --use-fake-device-for-media-stream --no-default-browser-check --disable-extensions --user-data-dir=chrome_test
open http://localhost:8000/fuzz-00027.html

The reason for the vulnerability is that multi-threaded race conditions cause the iterator to fail, so it is difficult to reproduce.
Here, you can use WINDBG to add the following breakpoints for observation.
It can be observed that the thread "Chrome_InProcRendererThread" and "DedicatedWorker thread" will call the function Add Remove Notify with out lock, which is the root cause of the vulnerability.

bp blink_platform!blink::FrameOrWorkerScheduler::NotifyLifecycleObservers ".echo 'NotifyLifecycleObservers';~#;gc"
bp blink_platform!blink::FrameOrWorkerScheduler::AddLifecycleObserver ".echo 'AddLifecycleObserver';~#;gc"
bp blink_platform!blink::FrameOrWorkerScheduler::RemoveLifecycleObserver ".echo 'RemoveLifecycleObserver';~#;gc"

```
'NotifyLifecycleObservers'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'AddLifecycleObserver'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'AddLifecycleObserver'
. 72  Id: 326c.3b00 Suspend: 1 Teb: 0000003a`c0b69000 Unfrozen "DedicatedWorker thread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'RemoveLifecycleObserver'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'AddLifecycleObserver'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'NotifyLifecycleObservers'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
...
CUT
...

'NotifyLifecycleObservers'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'NotifyLifecycleObservers'
. 72  Id: 326c.3b00 Suspend: 1 Teb: 0000003a`c0b69000 Unfrozen "DedicatedWorker thread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'NotifyLifecycleObservers'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'NotifyLifecycleObservers'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'NotifyLifecycleObservers'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'RemoveLifecycleObserver'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'RemoveLifecycleObserver'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'RemoveLifecycleObserver'
. 72  Id: 326c.3b00 Suspend: 1 Teb: 0000003a`c0b69000 Unfrozen "DedicatedWorker thread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'RemoveLifecycleObserver'
. 43  Id: 326c.2660 Suspend: 1 Teb: 0000003a`c0aff000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ffd`ecc10a10)
      Priority: 0  Priority class: 32  Affinity: ffff

=================================================================
==5852==ERROR: AddressSanitizer: use-after-poison on address 0x7eb2bf3230d8 at pc 0x7ffc20210982 bp 0x00000e25f640 sp 0x00000e25f688
READ of size 8 at 0x7eb2bf3230d8 thread T373
==5852==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffc20210981  (C:\chrome_asan\asan-win32-release_x64-880310\chrome.dll+0x188cc0981)
    #1 0x7ffc2189101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #2 0x7ffc23ff1a5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:357
    #3 0x7ffc23ff10d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:270
    #4 0x7ffc23fc520f in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #5 0x7ffc23ff3104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:466
    #6 0x7ffc21816ba3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #7 0x7ffc2029a454 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc:154
    #8 0x7ffc21962a1f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #9 0x7ff60db5dac7 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:279
    #10 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #11 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

Address 0x7eb2bf3230d8 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\common\frame_or_worker_scheduler.cc:88 in blink::FrameOrWorkerScheduler::NotifyLifecycleObservers
Shadow bytes around the buggy address:
  0x0fd6d7e645c0: 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd6d7e645d0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd6d7e645e0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd6d7e645f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd6d7e64600: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fd6d7e64610: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7
  0x0fd6d7e64620: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd6d7e64630: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd6d7e64640: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd6d7e64650: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd6d7e64660: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
Thread T373 created by T33 here:
    #0 0x7ff60db5e5b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffc21961dfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ffc218d5460 in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple_thread.cc:51
    #3 0x7ffc2021bcb6 in blink::Thread::CreateThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\common\thread.cc:86
    #4 0x7ffc2a9d41ab in blink::WorkerBackingThread::WorkerBackingThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_backing_thread.cc:60
    #5 0x7ffc31e9ac22 in blink::DedicatedWorkerThread::DedicatedWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker_thread.cc:59
    #6 0x7ffc3144c6aa in blink::DedicatedWorkerMessagingProxy::CreateWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker_messaging_proxy.cc:270
    #7 0x7ffc2fd03ee3 in blink::ThreadedMessagingProxyBase::InitializeWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\threaded_messaging_proxy_base.cc:73
    #8 0x7ffc31449b8b in blink::DedicatedWorkerMessagingProxy::StartWorkerGlobalScope C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker_messaging_proxy.cc:73
    #9 0x7ffc31e949b7 in blink::DedicatedWorker::ContinueStart C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker.cc:401
    #10 0x7ffc31e93595 in blink::DedicatedWorker::OnHostCreated C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker.cc:260
    #11 0x7ffc31e9a697 in base::internal::Invoker<base::internal::BindState<void (blink::DedicatedWorker::*)(mojo::PendingRemote<network::mojom::blink::URLLoaderFactory>, const network::CrossOriginEmbedderPolicy &),blink::WeakPersistent<blink::DedicatedWorker>,mojo::PendingRemote<network::mojom::blink::URLLoaderFactory> >,void (const network::CrossOriginEmbedderPolicy &)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
    #12 0x7ffc19e9352c in blink::mojom::DedicatedWorkerHostFactory_CreateWorkerHost_ForwardToCallback::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\worker\dedicated_worker_host_factory.mojom.cc:681
    #13 0x7ffc21cf0825 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:853
    #14 0x7ffc2444f2a6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #15 0x7ffc21d07a53 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1076
    #16 0x7ffc21d06a2e in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:705
    #17 0x7ffc2444f2a6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #18 0x7ffc21ceb471 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:539
    #19 0x7ffc21cece77 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:597
    #20 0x7ffc21d3c2fc in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #21 0x7ffc2189101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #22 0x7ffc23fecb0c in base::sequence_manager::internal::ThreadControllerImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_impl.cc:199
    #23 0x7ffc23fef7d3 in base::internal::Invoker<base::internal::BindState<void (base::sequence_manager::internal::ThreadControllerImpl::*)(base::sequence_manager::internal::ThreadControllerImpl::WorkType),base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl>,base::sequence_manager::internal::ThreadControllerImpl::WorkType>,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:703
    #24 0x7ffc2189101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #25 0x7ffc23ff1a5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:357
    #26 0x7ffc23ff10d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:270
    #27 0x7ffc21941c70 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #28 0x7ffc2193fe58 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #29 0x7ffc23ff3104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:466
    #30 0x7ffc21816ba3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #31 0x7ffc218d78f9 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:312
    #32 0x7ffc218d7e10 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:383
    #33 0x7ffc21962a1f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #34 0x7ff60db5dac7 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:279
    #35 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #36 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

Thread T33 created by T0 here:
    #0 0x7ff60db5e5b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffc21961dfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ffc218d6bca in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:187
    #3 0x7ffc1bb127ba in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1861
    #4 0x7ffc1baf55d2 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2806
    #5 0x7ffc1baecdb5 in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3032
    #6 0x7ffc1baeab48 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1052
    #7 0x7ffc1bae970c in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:807
    #8 0x7ffc1b86f5e5 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:532
    #9 0x7ffc1ba29c5f in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:596
    #10 0x7ffc1b99957e in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3302
    #11 0x7ffc1b998734 in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1136
    #12 0x7ffc23adafb9 in `anonymous namespace'::LoadURLInContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:386
    #13 0x7ffc23ad8316 in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:658
    #14 0x7ffc2afac291 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:313
    #15 0x7ffc2afae06f in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:582
    #16 0x7ffc2afab438 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:429
    #17 0x7ffc2afaaaa0 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:218
    #18 0x7ffc26f9ce4e in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:689
    #19 0x7ffc26fa37ff in StartupBrowserCreator::ProcessLastOpenedProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1259
    #20 0x7ffc26fa2d43 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1209
    #21 0x7ffc26f9c349 in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1127
    #22 0x7ffc26f9a973 in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:624
    #23 0x7ffc2412c310 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1647
    #24 0x7ffc24129dbe in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1039
    #25 0x7ffc1b0271de in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:960
    #26 0x7ffc1bdbf283 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
    #27 0x7ffc1b0266e8 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:868
    #28 0x7ffc1b02e125 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
    #29 0x7ffc1b022cd4 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
    #30 0x7ffc215acbe8 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:597
    #31 0x7ffc215af51f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1080
    #32 0x7ffc215ae72f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:955
    #33 0x7ffc215aba97 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372
    #34 0x7ffc215ac08b in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #35 0x7ffc1755145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:151
    #36 0x7ff60dab5bd1 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #37 0x7ff60dab2c1d in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:369
    #38 0x7ff60de9bb7f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #39 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #40 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

==5852==ABORTING

What is the expected behavior?

What went wrong?
crashed

Did this work before? N/A 

Chrome version: 92.0.4494.0  Channel: dev
OS Version: 10.0
Flash Version:

## Attachments

- [fuzz-00027.html](attachments/fuzz-00027.html) (text/plain, 63.7 KB)
- [viper.mp3](attachments/viper.mp3) (application/octet-stream, 3.3 KB)
- [viper.ogg](attachments/viper.ogg) (application/octet-stream, 2.5 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 1.5 KB)
- deleted (application/octet-stream, 0 B)
- [gc1.png](attachments/gc1.png) (image/png, 93.0 KB)
- [gc2.png](attachments/gc2.png) (image/png, 68.8 KB)

## Timeline

### [Deleted User] (2021-05-25)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-05-25)

Add a lock to resolve the race condition vulnerability
```
diff --git a/frame_or_worker_scheduler.cc b/frame_or_worker_scheduler.cc
index d84ae60..53e9599 100644
--- a/frame_or_worker_scheduler.cc
+++ b/frame_or_worker_scheduler.cc
@@ -72,18 +72,21 @@ FrameOrWorkerScheduler::AddLifecycleObserver(ObserverType type,
                                              Observer* observer) {
   DCHECK(observer);
   observer->OnLifecycleStateChanged(CalculateLifecycleState(type));
+  AutoLock(lifecycle_observers_lock_);
   lifecycle_observers_.Set(observer, type);
   return std::make_unique<LifecycleObserverHandle>(this, observer);
 }
 
 void FrameOrWorkerScheduler::RemoveLifecycleObserver(Observer* observer) {
   DCHECK(observer);
+  AutoLock(lifecycle_observers_lock_);
   const auto found = lifecycle_observers_.find(observer);
   DCHECK(lifecycle_observers_.end() != found);
   lifecycle_observers_.erase(found);
 }
 
 void FrameOrWorkerScheduler::NotifyLifecycleObservers() {
+  AutoLock(lifecycle_observers_lock_);
   for (const auto& observer : lifecycle_observers_) {
     observer.key->OnLifecycleStateChanged(
         CalculateLifecycleState(observer.value));
diff --git a/frame_or_worker_scheduler.h b/frame_or_worker_scheduler.h
index 8b7cf12..fb04c26 100644
--- a/frame_or_worker_scheduler.h
+++ b/frame_or_worker_scheduler.h
@@ -144,6 +144,7 @@ class PLATFORM_EXPORT FrameOrWorkerScheduler {
 
   // Observers are not owned by the scheduler.
   HashMap<Observer*, ObserverType> lifecycle_observers_;
+  base::Lock lifecycle_observers_lock_;
   base::WeakPtrFactory<FrameOrWorkerScheduler> weak_factory_{this};
 };

```


### m....@gmail.com (2021-05-25)

I found that using TSAN version test is very easy to reproduce
“gs://chromium-browser-tsan/linux-release/tsan-linux-release-886199.zip”

but you can't set external_symbolizer_path,if you set external_symbolizer_path poc will not reproduce~~,i don't why yet!


### cl...@chromium.org (2021-05-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5676798160207872.

### ad...@google.com (2021-05-25)

I reproduced a crash here as follows:

* Redshell Linux
* asan-linux-debug-885994
* ASAN_OPTIONS=detect_odr_violation=0 ./chrome --js-flags='--expose_gc' --enable-blink-test-features  --autoplay-policy=no-user-gesture-required --use-fake-device-for-media-stream --no-sandbox --single-process

[5124:5211:0525/184227.366194:FATAL:sequence_checker.h(136)] Check failed: checker.CalledOnValidSequence(&bound_at). 
#0 0x55e8e4c7e89b (/home/adetaylor/asan-linux-debug-885994/chrome+0x920289a)
#1 0x7ff712204c6f (/home/adetaylor/asan-linux-debug-885994/libbase.so+0xd70c6e)
#2 0x7ff711aa6b04 (/home/adetaylor/asan-linux-debug-885994/libbase.so+0x612b03)
#3 0x7ff711aa6975 (/home/adetaylor/asan-linux-debug-885994/libbase.so+0x612974)
#4 0x7ff711b83ae9 (/home/adetaylor/asan-linux-debug-885994/libbase.so+0x6efae8)
#5 0x7ff711b84bc9 (/home/adetaylor/asan-linux-debug-885994/libbase.so+0x6f0bc8)
#6 0x7ff7119e85d8 (/home/adetaylor/asan-linux-debug-885994/libbase.so+0x5545d7)
#7 0x7ff70dcfec58 (/home/adetaylor/asan-linux-debug-885994/libui_base.so+0x314c57)
#8 0x7ff70dcf8918 (/home/adetaylor/asan-linux-debug-885994/libui_base.so+0x30e917)
#9 0x7ff70dd36da7 (/home/adetaylor/asan-linux-debug-885994/libui_base.so+0x34cda6)
#10 0x7ff70dd36640 (/home/adetaylor/asan-linux-debug-885994/libui_base.so+0x34c63f)

I'm not sure why I'm not getting symbolized output; I can't reproduce any problems except in single-process mode.

This is a debug build so quite possibly I'd have hit the same UaP in a release build.

I think this is enough for me to confirm that there's a real problem here, and pass it onto the relevant engineering team. I'll try to gather a little more information about the impacted versions before doing so.

(I also tried feeding this to ClusterFuzz, we'll see what happens there).

### ad...@google.com (2021-05-25)

The story so far:
* I am not convinced the TSAN stack traces are related. They might be. I'm not an expert at understanding the TSAN ignorelist and I get a lot of TSAN noise anyway.
* I can't reliably reproduce a problem with release ASAN builds.
* I get a different, but suggestive, problem with debug ASAN builds.

So overall I'm just failing to bisect this to work out which channels are impacted. I also can't start to remove the extra flags to figure out if this is Security_Impact-None or not. I think therefore we'll just have to wait a day to see if ClusterFuzz can make progress on it. _If_ ClusterFuzz reproduces it reliably (which is a big 'if') then we'll get lots of good diagnostics.

[Monorail components: Blink>Scheduling]

### cl...@chromium.org (2021-05-26)

ClusterFuzz testcase 5676798160207872 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2021-05-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5676798160207872

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  base::DiscardableMemoryAllocator::AllocateLockedDiscardableMemoryWithRetryOrDie
  SkDiscardableMemory::Create
  SkResourceCache::newCachedData
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=886469

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5676798160207872

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5676798160207872 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### m....@gmail.com (2021-05-26)

#5 Can ClusterFuzz test tsan version?

Aslo i think it can be clearly understood by setting breakpoints.

### cl...@chromium.org (2021-05-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5676798160207872

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  base::DiscardableMemoryAllocator::AllocateLockedDiscardableMemoryWithRetryOrDie
  SkDiscardableMemory::Create
  SkResourceCache::newCachedData
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=886469

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5676798160207872

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5676798160207872 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### cl...@chromium.org (2021-05-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core Internals>Skia]

### m....@gmail.com (2021-05-26)

The logs of TSAN and ClusterFuzz are incorrect, I still recommend using debuggers to confirm the problem.

### ad...@google.com (2021-05-26)

[Comment Deleted]

### ad...@google.com (2021-05-26)

(previous comment deleted where I mistakenly set this to Critical)

I agree ClusterFuzz has come up with something unrelated.

I still can't reproduce this but I think the evidence presented about the missing lock is compelling, so altimin@ I'd like to pass this onto you to see what you think.

As a renderer UaF this is high severity.

I'm setting this to Security_Impact-Stable because the code lacking the locks hasn't changed for ages and dedicated workers have been around for a while. However, if any of those extra command line flags are actually required (which seems unlikely?) then this may be Security_Impact-None as it doesn't affect the shipping configuration of Chrome. Let me know! Thanks.

### [Deleted User] (2021-05-27)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### ad...@google.com (2021-06-02)

[Comment Deleted]

### ad...@google.com (2021-06-02)

Adding FoundIn to correspond to Security_Impact. It does not imply I've done any additional testing.

### [Deleted User] (2021-06-08)

altimin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-22)

altimin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2021-06-23)

After more in-depth analysis, I found that the initial analysis was incorrect.
The root cause of the problem maybe store raw pointers to on-heap objects.
ResourceLoadScheduler is an on-heap object,AddLifecycleObserver[1] pass it to LifecycleObserverHandle[2] which is off-heap object.
observer.key[3] may have been freed when NotifyLifecycleObservers is called, resulting in UAF

After reading Oilpan 101: Basics, Common Pitfalls, I think there may be 2 GC usage errors here,i'm not sure!
1.If your class' (possibly implicit) destructor has any work to do, your class needs to inherit from GarbageCollectedFinalized<T> instead of GarbageCollected<T>.
2.Don't store raw pointers to on-heap objects.

[1]
third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc:78
ResourceLoadScheduler::ResourceLoadScheduler(
    ThrottlingPolicy initial_throttling_policy,
    ThrottleOptionOverride throttle_option_override,

...CUT...

  scheduler_observer_handle_ = frame_or_worker_scheduler->AddLifecycleObserver(
      FrameScheduler::ObserverType::kLoader, this);
}

[2]
third_party/blink/renderer/platform/scheduler/public/frame_or_worker_scheduler.h:40
class PLATFORM_EXPORT LifecycleObserverHandle {
USING_FAST_MALLOC(LifecycleObserverHandle);

public:
LifecycleObserverHandle(FrameOrWorkerScheduler* scheduler,
						Observer* observer);
LifecycleObserverHandle(const LifecycleObserverHandle&) = delete;
LifecycleObserverHandle& operator=(const LifecycleObserverHandle&) = delete;
~LifecycleObserverHandle();

private:
base::WeakPtr<FrameOrWorkerScheduler> scheduler_;
Observer* observer_;
};

[3]
third_party/blink/renderer/platform/scheduler/common/frame_or_worker_scheduler.cc:86
void FrameOrWorkerScheduler::NotifyLifecycleObservers() {
  for (const auto& observer : lifecycle_observers_) {
    observer.key->OnLifecycleStateChanged(
        CalculateLifecycleState(observer.value));
  }
}

[4]
third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.h
class PLATFORM_EXPORT ResourceLoadScheduler final
    : public GarbageCollected<ResourceLoadScheduler>,
      public FrameOrWorkerScheduler::Observer {
 public:
 
 ...CUT...

  // Handle to throttling observer.
  std::unique_ptr<FrameOrWorkerScheduler::LifecycleObserverHandle>
      scheduler_observer_handle_;

  const Member<DetachableConsoleLogger> console_logger_;

  const base::Clock* clock_;


### [Deleted User] (2021-07-24)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-09-03)

altimin: can you please comment on this issue or help us find someone to investigate?

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-10-08)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-10-08)

Friendly ping on this high severity bug. Adding more folks from scheduler for input.

### xi...@chromium.org (2021-10-08)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-23)

altmin: Can you please take a look at this high-severity security bug, or find someone who can? We have exceeded our deadline for fixing this.

### m....@gmail.com (2021-12-16)

I also found the same problem with the fuzzer running on clusterfuzz, but it still can't reproduce stably.

https://clusterfuzz.com/testcase-detail/5130056256782336 (May need request permission)


### gi...@appspot.gserviceaccount.com (2022-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3c60616245d4928ee89ad842e1031bd8d3a6121d

commit 3c60616245d4928ee89ad842e1031bd8d3a6121d
Author: Scott Haseley <shaseley@chromium.org>
Date: Wed Jan 12 04:28:13 2022

[scheduler] Refactor lifecycle observers as callbacks

Before this CL, FrameOrWorkerScheduler lifecycle callbacks were
implemented as an observer interface and we held a raw pointer to the
observer. These observers could be either on-heap or off-heap objects
which violates the rule of not storing raw pointers to on-heap objects
since this risks UAF.

To work around this, this CL changes the lifecycle observers to
callbacks, with the observers using WrapWeakPersistent with Bind where
needed. This is relatively clean since the observer interface only has
one method. We could alternatively store WeakPersistent references
to the on-heap obejcts, but this is more complicated since we need to
handle both on-heap and off-heap obejcts (possible, but probably overly
complicated for this case).

Bug: 1281239, 1212957
Change-Id: I13a14c3228b1fd7043f94becfacf8ec5429329ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3373869
Reviewed-by: Alexander Timin <altimin@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Reviewed-by: Chrome Cunningham <chcunningham@chromium.org>
Commit-Queue: Scott Haseley <shaseley@chromium.org>
Cr-Commit-Position: refs/heads/main@{#957925}

[modify] https://crrev.com/3c60616245d4928ee89ad842e1031bd8d3a6121d/third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.h
[modify] https://crrev.com/3c60616245d4928ee89ad842e1031bd8d3a6121d/third_party/blink/renderer/modules/webcodecs/reclaimable_codec.h
[modify] https://crrev.com/3c60616245d4928ee89ad842e1031bd8d3a6121d/third_party/blink/renderer/platform/scheduler/main_thread/frame_scheduler_impl_unittest.cc
[modify] https://crrev.com/3c60616245d4928ee89ad842e1031bd8d3a6121d/third_party/blink/renderer/platform/scheduler/common/frame_or_worker_scheduler.cc
[modify] https://crrev.com/3c60616245d4928ee89ad842e1031bd8d3a6121d/third_party/blink/renderer/modules/webcodecs/reclaimable_codec.cc
[modify] https://crrev.com/3c60616245d4928ee89ad842e1031bd8d3a6121d/third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc
[modify] https://crrev.com/3c60616245d4928ee89ad842e1031bd8d3a6121d/third_party/blink/renderer/platform/scheduler/public/frame_or_worker_scheduler.h
[modify] https://crrev.com/3c60616245d4928ee89ad842e1031bd8d3a6121d/third_party/blink/renderer/platform/scheduler/worker/worker_scheduler_proxy.cc
[modify] https://crrev.com/3c60616245d4928ee89ad842e1031bd8d3a6121d/third_party/blink/renderer/platform/scheduler/worker/worker_scheduler_proxy.h


### sh...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

Requesting merge to extended stable M96 because latest trunk commit (957925) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (957925) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (957925) appears to be after beta branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-13)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-13)

Merge review required: M97 is already shipping to stable.

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

### [Deleted User] (2022-01-13)

Merge review required: M96 is already shipping to stable.

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

### sh...@chromium.org (2022-01-13)

[Empty comment from Monorail migration]

### pb...@google.com (2022-01-14)

+amyressler@ for M97 and M96 Merge decision

### sh...@chromium.org (2022-01-14)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches

The bug is flagged as high-severity security bug which IIUC meets the merge criteria for M96, M97, and M98.

- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3373869.

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.

### am...@chromium.org (2022-01-14)

merge approved to M96 and M97, please merge to branches 4664 and 4692 ASAP/immediately before 12p PST today -- thank you 

### sr...@google.com (2022-01-14)

Merge approved for M98 as well Branch:4758

### gi...@appspot.gserviceaccount.com (2022-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f779b38a3fd3ef532075081dd918b4be398c8c1f

commit f779b38a3fd3ef532075081dd918b4be398c8c1f
Author: Scott Haseley <shaseley@chromium.org>
Date: Tue Jan 18 18:11:43 2022

[scheduler] Refactor lifecycle observers as callbacks

Merge to release branch 4758.

Before this CL, FrameOrWorkerScheduler lifecycle callbacks were
implemented as an observer interface and we held a raw pointer to the
observer. These observers could be either on-heap or off-heap objects
which violates the rule of not storing raw pointers to on-heap objects
since this risks UAF.

To work around this, this CL changes the lifecycle observers to
callbacks, with the observers using WrapWeakPersistent with Bind where
needed. This is relatively clean since the observer interface only has
one method. We could alternatively store WeakPersistent references
to the on-heap obejcts, but this is more complicated since we need to
handle both on-heap and off-heap obejcts (possible, but probably overly
complicated for this case).

(cherry picked from commit 3c60616245d4928ee89ad842e1031bd8d3a6121d)

Bug: 1281239, 1212957
Change-Id: I13a14c3228b1fd7043f94becfacf8ec5429329ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3373869
Reviewed-by: Alexander Timin <altimin@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Reviewed-by: Chrome Cunningham <chcunningham@chromium.org>
Commit-Queue: Scott Haseley <shaseley@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#957925}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389968
Reviewed-by: Dan Sanders <sandersd@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#721}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/f779b38a3fd3ef532075081dd918b4be398c8c1f/third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.h
[modify] https://crrev.com/f779b38a3fd3ef532075081dd918b4be398c8c1f/third_party/blink/renderer/platform/scheduler/main_thread/frame_scheduler_impl_unittest.cc
[modify] https://crrev.com/f779b38a3fd3ef532075081dd918b4be398c8c1f/third_party/blink/renderer/modules/webcodecs/reclaimable_codec.h
[modify] https://crrev.com/f779b38a3fd3ef532075081dd918b4be398c8c1f/third_party/blink/renderer/platform/scheduler/common/frame_or_worker_scheduler.cc
[modify] https://crrev.com/f779b38a3fd3ef532075081dd918b4be398c8c1f/third_party/blink/renderer/modules/webcodecs/reclaimable_codec.cc
[modify] https://crrev.com/f779b38a3fd3ef532075081dd918b4be398c8c1f/third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc
[modify] https://crrev.com/f779b38a3fd3ef532075081dd918b4be398c8c1f/third_party/blink/renderer/platform/scheduler/public/frame_or_worker_scheduler.h
[modify] https://crrev.com/f779b38a3fd3ef532075081dd918b4be398c8c1f/third_party/blink/renderer/platform/scheduler/worker/worker_scheduler_proxy.cc
[modify] https://crrev.com/f779b38a3fd3ef532075081dd918b4be398c8c1f/third_party/blink/renderer/platform/scheduler/worker/worker_scheduler_proxy.h


### gi...@appspot.gserviceaccount.com (2022-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c05d486542abfa0def40dbdcf2ba79e19fb964f3

commit c05d486542abfa0def40dbdcf2ba79e19fb964f3
Author: Scott Haseley <shaseley@chromium.org>
Date: Tue Jan 18 19:36:11 2022

[scheduler] Refactor lifecycle observers as callbacks

Merge to release branch 4692.
Note: changes to reclaimable_codec.* are omitted from cherry-picked CL
as the observer was added later.

Before this CL, FrameOrWorkerScheduler lifecycle callbacks were
implemented as an observer interface and we held a raw pointer to the
observer. These observers could be either on-heap or off-heap objects
which violates the rule of not storing raw pointers to on-heap objects
since this risks UAF.

To work around this, this CL changes the lifecycle observers to
callbacks, with the observers using WrapWeakPersistent with Bind where
needed. This is relatively clean since the observer interface only has
one method. We could alternatively store WeakPersistent references
to the on-heap obejcts, but this is more complicated since we need to
handle both on-heap and off-heap obejcts (possible, but probably overly
complicated for this case).

(cherry picked from commit 3c60616245d4928ee89ad842e1031bd8d3a6121d)

Bug: 1212957
Change-Id: Iaefc7c0d8cb42b1db7c7761888824d0a3b2945d8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3373869
Reviewed-by: Alexander Timin <altimin@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Reviewed-by: Chrome Cunningham <chcunningham@chromium.org>
Commit-Queue: Scott Haseley <shaseley@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#957925}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389724
Cr-Commit-Position: refs/branch-heads/4692@{#1454}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/c05d486542abfa0def40dbdcf2ba79e19fb964f3/third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.h
[modify] https://crrev.com/c05d486542abfa0def40dbdcf2ba79e19fb964f3/third_party/blink/renderer/platform/scheduler/main_thread/frame_scheduler_impl_unittest.cc
[modify] https://crrev.com/c05d486542abfa0def40dbdcf2ba79e19fb964f3/third_party/blink/renderer/platform/scheduler/common/frame_or_worker_scheduler.cc
[modify] https://crrev.com/c05d486542abfa0def40dbdcf2ba79e19fb964f3/third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc
[modify] https://crrev.com/c05d486542abfa0def40dbdcf2ba79e19fb964f3/third_party/blink/renderer/platform/scheduler/public/frame_or_worker_scheduler.h
[modify] https://crrev.com/c05d486542abfa0def40dbdcf2ba79e19fb964f3/third_party/blink/renderer/platform/scheduler/worker/worker_scheduler_proxy.cc
[modify] https://crrev.com/c05d486542abfa0def40dbdcf2ba79e19fb964f3/third_party/blink/renderer/platform/scheduler/worker/worker_scheduler_proxy.h


### gi...@appspot.gserviceaccount.com (2022-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b0cb408e775cb022a90f2632c4d6f3e1ea46e0de

commit b0cb408e775cb022a90f2632c4d6f3e1ea46e0de
Author: Scott Haseley <shaseley@chromium.org>
Date: Tue Jan 18 19:36:05 2022

[scheduler] Refactor lifecycle observers as callbacks

Merge to release branch 4664.
Note: changes to reclaimable_codec.* are omitted from cherry-picked CL
as the observer was added later.

Before this CL, FrameOrWorkerScheduler lifecycle callbacks were
implemented as an observer interface and we held a raw pointer to the
observer. These observers could be either on-heap or off-heap objects
which violates the rule of not storing raw pointers to on-heap objects
since this risks UAF.

To work around this, this CL changes the lifecycle observers to
callbacks, with the observers using WrapWeakPersistent with Bind where
needed. This is relatively clean since the observer interface only has
one method. We could alternatively store WeakPersistent references
to the on-heap obejcts, but this is more complicated since we need to
handle both on-heap and off-heap obejcts (possible, but probably overly
complicated for this case).

(cherry picked from commit 3c60616245d4928ee89ad842e1031bd8d3a6121d)

Bug: 1212957
Change-Id: I89ec5ae4effbb6c35e45a91f0253326951182215
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3373869
Reviewed-by: Alexander Timin <altimin@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Reviewed-by: Chrome Cunningham <chcunningham@chromium.org>
Commit-Queue: Scott Haseley <shaseley@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#957925}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389722
Cr-Commit-Position: refs/branch-heads/4664@{#1411}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/b0cb408e775cb022a90f2632c4d6f3e1ea46e0de/third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.h
[modify] https://crrev.com/b0cb408e775cb022a90f2632c4d6f3e1ea46e0de/third_party/blink/renderer/platform/scheduler/main_thread/frame_scheduler_impl_unittest.cc
[modify] https://crrev.com/b0cb408e775cb022a90f2632c4d6f3e1ea46e0de/third_party/blink/renderer/platform/scheduler/common/frame_or_worker_scheduler.cc
[modify] https://crrev.com/b0cb408e775cb022a90f2632c4d6f3e1ea46e0de/third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc
[modify] https://crrev.com/b0cb408e775cb022a90f2632c4d6f3e1ea46e0de/third_party/blink/renderer/platform/scheduler/public/frame_or_worker_scheduler.h
[modify] https://crrev.com/b0cb408e775cb022a90f2632c4d6f3e1ea46e0de/third_party/blink/renderer/platform/scheduler/worker/worker_scheduler_proxy.cc
[modify] https://crrev.com/b0cb408e775cb022a90f2632c4d6f3e1ea46e0de/third_party/blink/renderer/platform/scheduler/worker/worker_scheduler_proxy.h


### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Congratulations - the VRP Panel has decided to award you $7500 for this report + $1000 bonus for your additional efforts and analysis and fuzzing. Thank you for this report and your efforts throughout. 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-04-20)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1212957?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Scheduling, Internals>Core, Internals>Skia]
[Monorail mergedwith: crbug.com/chromium/1257946, crbug.com/chromium/1281239]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055998)*
