# AddressSanitizer: heap-use-after-free in cc::LayerTreeHost::RemoveSurfaceRange

| Field | Value |
|-------|-------|
| **Issue ID** | [397601495](https://issues.chromium.org/issues/397601495) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Services>Viz |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2025-02-19 |
| **Bounty** | $26,000.00 |

## Description



VULNERABILITY DETAILS
In the function LayerTreeHost::ActivateCommitState
the pending_commit_state that is created may be accessed by multiple threads
As shown in the vulnerability below, a use-after-free issue can occur
when the main thread has already reset the CommitState currently pointed 
to by pending_commit_state, while other threads are still using it.

NOTE
Since the threads race for different positions each time
the results of reproducing the crash may appear inconsistent
but the root cause remains the same.

VERSION
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-1419723.zip
win11x64

REPRODUCTION CASE
chrome --user-data-dir=user_profile_0  --enable-logging=stderr poc.html poc.html poc.html poc.html poc.html

Type of crash: [browser]


CREDIT INFORMATION
Reporter credit: [f4]

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.1 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### m....@gmail.com (2025-02-19)

Since the issue can be stably reproduced and triggered directly from the render process,
leading to a vulnerability in the browser process without requiring any interaction,
NOT PROTECTED by MiraclePtr,
it should be classified as a CRITICAL severity level.

### m....@gmail.com (2025-02-19)

There was also a reproduction on CF, but the link will expire soon.
https://clusterfuzz.com/testcase-detail/5817960530640896

```
=================================================================
==121496==ERROR: AddressSanitizer: heap-use-after-free on address 0x77725fdb7c88 at pc 0x5ad88e6258d4 bp 0x75d256ef1410 sp 0x75d256ef1408
READ of size 8 at 0x77725fdb7c88 thread T5 (ThreadPoolForeg)
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x5ad88e6258d3 in end third_party/libc++/src/include/__vector/vector.h:352:57
    #1 0x5ad88e6258d3 in base::internal::flat_tree<viz::SurfaceRange, base::internal::GetFirst, std::__Cr::less<void>, std::__Cr::vector<std::__Cr::pair<viz::SurfaceRange, int>, std::__Cr::allocator<std::__Cr::pair<viz::SurfaceRange, int>>>>::erase(std::__Cr::__wrap_iter<std::__Cr::pair<viz::SurfaceRange, int>*>) base/containers/flat_tree.h:861:3
    #2 0x5ad88e618bf4 in cc::LayerTreeHost::RemoveSurfaceRange(viz::SurfaceRange const&) cc/trees/layer_tree_host.cc:1699:44
    #3 0x5ad88e61891a in cc::ScopedKeepSurfaceAlive::~ScopedKeepSurfaceAlive() cc/trees/layer_tree_host.cc:570:12
    #4 0x5ad890530632 in operator() third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #5 0x5ad890530632 in reset third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #6 0x5ad890530632 in ~unique_ptr third_party/libc++/src/include/__memory/unique_ptr.h:269:71
    #7 0x5ad890530632 in ~pair third_party/libc++/src/include/__utility/pair.h:63:29
    #8 0x5ad890530632 in __destroy_at<std::__Cr::pair<base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int>, std::__Cr::unique_ptr<cc::ScopedKeepSurfaceAlive, std::__Cr::default_delete<cc::ScopedKeepSurfaceAlive> > >, 0> third_party/libc++/src/include/__memory/construct_at.h:63:11
    #9 0x5ad890530632 in destroy<std::__Cr::pair<base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int>, std::__Cr::unique_ptr<cc::ScopedKeepSurfaceAlive, std::__Cr::default_delete<cc::ScopedKeepSurfaceAlive> > >, void, 0> third_party/libc++/src/include/__memory/allocator_traits.h:329:5
    #10 0x5ad890530632 in __base_destruct_at_end third_party/libc++/src/include/__vector/vector.h:746:7
    #11 0x5ad890530632 in __destruct_at_end third_party/libc++/src/include/__vector/vector.h:664:5
    #12 0x5ad890530632 in std::__Cr::vector<std::__Cr::pair<base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int>, std::__Cr::unique_ptr<cc::ScopedKeepSurfaceAlive, std::__Cr::default_delete<cc::ScopedKeepSurfaceAlive>>>, std::__Cr::allocator<std::__Cr::pair<base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int>, std::__Cr::unique_ptr<cc::ScopedKeepSurfaceAlive, std::__Cr::default_delete<cc::ScopedKeepSurfaceAlive>>>>>::erase(std::__Cr::__wrap_iter<std::__Cr::pair<base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int>, std::__Cr::unique_ptr<cc::ScopedKeepSurfaceAlive, std::__Cr::default_delete<cc::ScopedKeepSurfaceAlive>>> const*>, std::__Cr::__wrap_iter<std::__Cr::pair<base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int>, std::__Cr::unique_ptr<cc::ScopedKeepSurfaceAlive, std::__Cr::default_delete<cc::ScopedKeepSurfaceAlive>>> const*>) third_party/libc++/src/include/__vector/vector.h:1158:11
    #13 0x5ad890529052 in erase base/containers/flat_tree.h:898:16
    #14 0x5ad890529052 in erase base/containers/flat_tree.h:879:3
    #15 0x5ad890529052 in ui::Compositor::RemoveScopedKeepSurfaceAlive(base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int> const&) ui/compositor/compositor.cc:1060:27
    #16 0x5ad89052b003 in Invoke<void (ui::Compositor::*)(const base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int> &), const base::WeakPtr<ui::Compositor> &, base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int> > base/functional/bind_internal.h:728:12
    #17 0x5ad89052b003 in MakeItSo<void (ui::Compositor::*)(const base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int> &), std::__Cr::tuple<base::WeakPtr<ui::Compositor>, base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int> > > base/functional/bind_internal.h:944:5
    #18 0x5ad89052b003 in RunImpl<void (ui::Compositor::*)(const base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int> &), std::__Cr::tuple<base::WeakPtr<ui::Compositor>, base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int> >, 0UL, 1UL> base/functional/bind_internal.h:1057:14
    #19 0x5ad89052b003 in base::internal::Invoker<base::internal::FunctorTraits<void (ui::Compositor::*&&)(base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int> const&), base::WeakPtr<ui::Compositor>&&, base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int>&&>, base::internal::BindState<true, true, false, void (ui::Compositor::*)(base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int> const&), base::WeakPtr<ui::Compositor>, base::StrongAlias<ui::PendingSurfaceCopyIdTag, unsigned int>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:970:12
    #20 0x5ad888aa2be6 in Run base/functional/callback.h:156:12
    #21 0x5ad888aa2be6 in base::ScopedClosureRunner::RunAndReset() base/functional/callback_helpers.cc:32:25
    #22 0x5ad880fa80dd in operator() content/browser/renderer_host/delegated_frame_host.cc:166:37
    #23 0x5ad880fa80dd in Invoke<(lambda at ../../content/browser/renderer_host/delegated_frame_host.cc:162:11), base::OnceCallback<void (const SkBitmap &)>, base::ScopedClosureRunner, std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult> > > base/functional/bind_internal.h:646:12
    #24 0x5ad880fa80dd in MakeItSo<(lambda at ../../content/browser/renderer_host/delegated_frame_host.cc:162:11), std::__Cr::tuple<base::OnceCallback<void (const SkBitmap &)>, base::ScopedClosureRunner>, std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult> > > base/functional/bind_internal.h:920:12
    #25 0x5ad880fa80dd in RunImpl<(lambda at ../../content/browser/renderer_host/delegated_frame_host.cc:162:11), std::__Cr::tuple<base::OnceCallback<void (const SkBitmap &)>, base::ScopedClosureRunner>, 0UL, 1UL> base/functional/bind_internal.h:1057:14
    #26 0x5ad880fa80dd in base::internal::Invoker<base::internal::FunctorTraits<content::DelegatedFrameHost::CopyFromCompositingSurface(gfx::Rect const&, gfx::Size const&, base::OnceCallback<void (SkBitmap const&)>)::$_0&&, base::OnceCallback<void (SkBitmap const&)>&&, base::ScopedClosureRunner&&>, base::internal::BindState<false, false, false, content::DelegatedFrameHost::CopyFromCompositingSurface(gfx::Rect const&, gfx::Size const&, base::OnceCallback<void (SkBitmap const&)>)::$_0, base::OnceCallback<void (SkBitmap const&)>, base::ScopedClosureRunner>, void (std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult>>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult>>&&) base/functional/bind_internal.h:970:12
    #27 0x5ad878756c52 in base::OnceCallback<void (std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult>>)>::Run(std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult>>) && base/functional/callback.h:156:12
    #28 0x5ad878756a3d in Invoke<base::OnceCallback<void (std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult> >)>, std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult> > > base/functional/bind_internal.h:803:49
    #29 0x5ad878756a3d in MakeItSo<base::OnceCallback<void (std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult> >)>, std::__Cr::tuple<std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult> > > > base/functional/bind_internal.h:920:12
    #30 0x5ad878756a3d in RunImpl<base::OnceCallback<void (std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult> >)>, std::__Cr::tuple<std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult> > >, 0UL> base/functional/bind_internal.h:1057:14
    #31 0x5ad878756a3d in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult>>)>&&, std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult>>&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult>>)>, std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult>>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:970:12
    #32 0x5ad888c04402 in Run base/functional/callback.h:156:12
    #33 0x5ad888c04402 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:209:34
    #34 0x5ad888c960da in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:692:35)> base/task/common/task_annotator.h:106:5
    #35 0x5ad888c960da in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:691:19
    #36 0x5ad888c9632c in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:676:3
    #37 0x5ad888c94904 in RunTaskWithShutdownBehavior base/task/thread_pool/task_tracker.cc:706:7
    #38 0x5ad888c94904 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:504:5
    #39 0x5ad888c93834 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:394:5
    #40 0x5ad888ccd1e3 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #41 0x5ad888ccc317 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #42 0x5ad888ccbdfe in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #43 0x5ad888d38859 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:103:13
    #44 0x5ad873ca58c6 in asan_thread_start(void*) third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28
    #45 0x79d262ebe608 in start_thread /build/glibc-LcI20x/glibc-2.31/nptl/pthread_create.c:477:8
    #46 0x79d26170a352 in __clone /build/glibc-LcI20x/glibc-2.31/sysdeps/unix/sysv/linux/x86_64/clone.S:95
0x77725fdb7c88 is located 8 bytes inside of 1240-byte region [0x77725fdb7c80,0x77725fdb8158)
freed by thread T0 (chrome) here:
    #0 0x5ad873ce240d in operator delete(void*) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x5ad88e965d6b in operator() third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #2 0x5ad88e965d6b in reset third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #3 0x5ad88e965d6b in cc::SingleThreadProxy::DoCommit(viz::BeginFrameArgs const&) cc/trees/single_thread_proxy.cc:253:16
    #4 0x5ad88e92dc7a in cc::Scheduler::ProcessScheduledActions() cc/scheduler/scheduler.cc:962:18
    #5 0x5ad88e92fabd in cc::Scheduler::NotifyReadyToCommit(std::__Cr::unique_ptr<cc::BeginMainFrameMetrics, std::__Cr::default_delete<cc::BeginMainFrameMetrics>>) cc/scheduler/scheduler.cc:231:3
    #6 0x5ad88e971c11 in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) cc/trees/single_thread_proxy.cc:1131:3
    #7 0x5ad88e975a73 in Invoke<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), const base::WeakPtr<cc::SingleThreadProxy> &, viz::BeginFrameArgs> base/functional/bind_internal.h:728:12
    #8 0x5ad88e975a73 in MakeItSo<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), std::__Cr::tuple<base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> > base/functional/bind_internal.h:944:5
    #9 0x5ad88e975a73 in RunImpl<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), std::__Cr::tuple<base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, 0UL, 1UL> base/functional/bind_internal.h:1057:14
    #10 0x5ad88e975a73 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::SingleThreadProxy::*&&)(viz::BeginFrameArgs const&), base::WeakPtr<cc::SingleThreadProxy>&&, viz::BeginFrameArgs&&>, base::internal::BindState<true, true, false, void (cc::SingleThreadProxy::*)(viz::BeginFrameArgs const&), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:970:12
    #11 0x5ad888c04402 in Run base/functional/callback.h:156:12
    #12 0x5ad888c04402 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:209:34
    #13 0x5ad888c71f88 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:106:5
    #14 0x5ad888c71f88 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #15 0x5ad888c70e6c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #16 0x5ad888c72cba in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #17 0x5ad888ddc46d in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:702:48
    #18 0x5ad888c7387c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #19 0x5ad888b9318f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #20 0x5ad87ef9ba22 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1089:18
    #21 0x5ad87efa352c in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:156:15
    #22 0x5ad87ef92b4b in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:32:28
    #23 0x5ad885c0f78f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:716:10
    #24 0x5ad885c12de5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1297:10
    #25 0x5ad885c124c6 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1151:12
    #26 0x5ad885c0d17d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:353:36
    #27 0x5ad885c0d76b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:366:10
    #28 0x5ad873ce34bf in ChromeMain chrome/app/chrome_main.cc:222:12
    #29 0x79d26160f082 in __libc_start_main /build/glibc-LcI20x/glibc-2.31/csu/libc-start.c:308:16
previously allocated by thread T0 (chrome) here:
    #0 0x5ad873ce1bad in operator new(unsigned long) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x5ad88e616713 in make_unique<cc::CommitState, cc::CommitState &, 0> third_party/libc++/src/include/__memory/unique_ptr.h:767:26
    #2 0x5ad88e616713 in cc::LayerTreeHost::ActivateCommitState() cc/trees/layer_tree_host.cc:458:27
    #3 0x5ad88e615efe in cc::LayerTreeHost::WillCommit(std::__Cr::unique_ptr<cc::CompletionEvent, std::__Cr::default_delete<cc::CompletionEvent>>, bool) cc/trees/layer_tree_host.cc:427:14
    #4 0x5ad88e965a65 in cc::SingleThreadProxy::DoCommit(viz::BeginFrameArgs const&) cc/trees/single_thread_proxy.cc:238:25
    #5 0x5ad88e92dc7a in cc::Scheduler::ProcessScheduledActions() cc/scheduler/scheduler.cc:962:18
    #6 0x5ad88e92fabd in cc::Scheduler::NotifyReadyToCommit(std::__Cr::unique_ptr<cc::BeginMainFrameMetrics, std::__Cr::default_delete<cc::BeginMainFrameMetrics>>) cc/scheduler/scheduler.cc:231:3
    #7 0x5ad88e971c11 in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) cc/trees/single_thread_proxy.cc:1131:3
    #8 0x5ad88e975a73 in Invoke<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), const base::WeakPtr<cc::SingleThreadProxy> &, viz::BeginFrameArgs> base/functional/bind_internal.h:728:12
    #9 0x5ad88e975a73 in MakeItSo<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), std::__Cr::tuple<base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> > base/functional/bind_internal.h:944:5
    #10 0x5ad88e975a73 in RunImpl<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), std::__Cr::tuple<base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, 0UL, 1UL> base/functional/bind_internal.h:1057:14
    #11 0x5ad88e975a73 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::SingleThreadProxy::*&&)(viz::BeginFrameArgs const&), base::WeakPtr<cc::SingleThreadProxy>&&, viz::BeginFrameArgs&&>, base::internal::BindState<true, true, false, void (cc::SingleThreadProxy::*)(viz::BeginFrameArgs const&), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:970:12
    #12 0x5ad888c04402 in Run base/functional/callback.h:156:12
    #13 0x5ad888c04402 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:209:34
    #14 0x5ad888c71f88 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:106:5
    #15 0x5ad888c71f88 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #16 0x5ad888c70e6c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #17 0x5ad888c72cba in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #18 0x5ad888ddbb38 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:656:46
    #19 0x5ad888dde8c8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:275:43
    #20 0x79d262dce17c in g_main_context_dispatch
Thread T5 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x5ad873c8c0d1 in ___interceptor_pthread_create third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:250:3
    #1 0x5ad888d37dd8 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:151:13
    #2 0x5ad888ccae8e in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x5ad888c97eac in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:89:13
    #4 0x5ad888c97b40 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:80:3
    #5 0x5ad888cbfcea in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread_pool/thread_group_impl.cc:42:3
    #6 0x5ad888cbf7d7 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>) base/task/thread_pool/thread_group_impl.cc:250:1
    #7 0x5ad888ca3cfc in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) base/task/thread_pool/thread_pool_impl.cc:196:35
    #8 0x5ad88097ef96 in content::StartBrowserThreadPool() content/browser/startup_helper.cc:100:36
    #9 0x5ad885c12f92 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1232:5
    #10 0x5ad885c124c6 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1151:12
    #11 0x5ad885c0d17d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:353:36
    #12 0x5ad885c0d76b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:366:10
    #13 0x5ad873ce34bf in ChromeMain chrome/app/chrome_main.cc:222:12
    #14 0x79d26160f082 in __libc_start_main /build/glibc-LcI20x/glibc-2.31/csu/libc-start.c:308:16
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chromium-browser-asan_linux-release-media_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/chrome+0x299918d3) (BuildId: 44343fd647f1f8bc)
Shadow bytes around the buggy address:
  0x77725fdb7a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77725fdb7a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77725fdb7b00: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x77725fdb7b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x77725fdb7c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x77725fdb7c80: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77725fdb7d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77725fdb7d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77725fdb7e00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77725fdb7e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x77725fdb7f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
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
==121496==ADDITIONAL INFO
==121496==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5ad88e36ee22 in viz::CopyOutputRequest::SendResult(std::__Cr::unique_ptr<viz::CopyOutputResult, std::__Cr::default_delete<viz::CopyOutputResult>>) components/viz/common/frame_sinks/copy_output_request.cc:136:20
    #1 0x5ad89e51694e in ShareThisTabSourceView::OnCaptureHandled(unsigned int, std::__Cr::optional<gfx::ImageSkia> const&) chrome/browser/ui/views/desktop_capture/share_this_tab_source_view.cc:190:7
    #2 0x5ad89e51703b in (anonymous namespace)::HandleCapturedBitmap(base::OnceCallback<void (unsigned int, std::__Cr::optional<gfx::ImageSkia> const&)>, std::__Cr::optional<unsigned int>, gfx::Size, SkBitmap const&) chrome/browser/ui/views/desktop_capture/share_this_tab_source_view.cc:72:7
    #3 0x5ad89e5162f3 in ShareThisTabSourceView::Refresh() chrome/browser/ui/views/desktop_capture/share_this_tab_source_view.cc:171:7
Command line: `/mnt/scratch0/clusterfuzz/bot/builds/chromium-browser-asan_linux-release-media_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/chrome --user-data-dir=/mnt/scratch0/tmp/user_profile_0 --window-size=497,114 --window-position=64,106 --enable-logging=stderr --v=1 --ignore-gpu-blacklist --allow-file-access-from-files --disable-gesture-requirement-for-media-playback --disable-click-to-play --disable-hang-monitor --dns-prefetch-disable --disable-default-apps --disable-component-update --safebrowsing-disable-auto-update --metrics-recording-only --disable-gpu-watchdog --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-experimental-extension-apis --enable-extension-apps --force-internal-pdf --js-flags=--expose-gc --verify-heap --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --use-gl=angle --use-angle=swiftshader --enable-shadow-dom --enable-media-stream --enable-mp3-stream-parser --disable-in-process-stack-traces --enable-features=WebMachineLearningNeuralNetwork --site-per-process --flag-switches-begin --flag-switches-end /mnt/scratch0/clusterfuzz/bot/inputs/fuzzer-testcases/fuzz-00080.html`
MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

```

### m....@gmail.com (2025-02-19)

Bisect
<https://chromium-review.googlesource.com/c/chromium/src/+/2201762>

This CL is the root cause of the thread race

```
void CopyOutputRequest::SendResult(std::unique_ptr<CopyOutputResult> result) {
  TRACE_EVENT_NESTABLE_ASYNC_END2(
      "viz", "CopyOutputRequest", this, "success", !result->IsEmpty(),
      "has_provided_task_runner", !!result_task_runner_);
  // Serializing the result requires an expensive copy, so to not block the
  // any important thread we PostTask onto the threadpool by default, but if the
  // user has provided a task runner use that instead.
  auto runner =
      result_task_runner_
          ? result_task_runner_
          : base::ThreadPool::CreateSequencedTaskRunner({base::MayBlock()});
  runner->PostTask(FROM_HERE, base::BindOnce(std::move(result_callback_),
                                             std::move(result)));
  // Remove the reference to the task runner (no-op if we didn't have one).
  result_task_runner_ = nullptr;
}

```

### cl...@appspot.gserviceaccount.com (2025-02-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6361527078551552.

### cl...@appspot.gserviceaccount.com (2025-02-20)

Detailed Report: https://clusterfuzz.com/testcase?key=5817960530640896

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x77725fdb7c88
Crash State:
  cc::LayerTreeHost::RemoveSurfaceRange
  cc::ScopedKeepSurfaceAlive::~ScopedKeepSurfaceAlive
  ui::Compositor::RemoveScopedKeepSurfaceAlive
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&revision=1419723

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5817960530640896

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2025-02-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### mp...@google.com (2025-02-20)

I can't seem to reproduce this locally, which is probably due to some strangeness with my system configuration. It's obviously flaky so it's difficult to reproduce on Clusterfuzz, though you managed to get one reproduction on Clusterfuzz.

I think this will be critical severity, but the clusterfuzz job you reproduced this on has a lot of flags, do you know how many of those are necessary? Do you have a video PoC?

The ScopedKeepAlive that seems to racily access a freed variable was added in <https://chromium-review.googlesource.com/c/chromium/src/+/5348259>, which is the only really recent change to this code, which makes me think that this is the culprit.

There was a speculative fix for a similar looking bug landed yesterday <https://chromium-review.googlesource.com/c/chromium/src/+/6216395>, so I'm going to CC the author and reviewers of these 2 CLs.

### m....@gmail.com (2025-02-20)

This issue can be reproduced without any special flags,
The attached file is the reproduction video I provided.

### mp...@google.com (2025-02-21)

jonross@ can you take a look at this? It does look critical severity.

[sahir.vellani@microsoft.com](mailto:sahir.vellani@microsoft.com) do you think this is the bug you were speculatively fixing from edge crash dumps?

### mp...@google.com (2025-02-21)

Tentatively adding all OSes since we've seen this bug trigger on both Windows and Linux.

Also tentatively marking FoundIn as M134, since that is when <https://chromium-review.googlesource.com/c/chromium/src/+/5348259> landed.

When we find the root cause here, we might need to adjust FoundIn.

### sa...@microsoft.com (2025-02-21)

It definitely seems related, I'm not sure if the fix I made would solve this UAF. It's interesting to note that in the clusterfuzz repro log, I see the following:

`[121564:121599:0213/085228.128343:ERROR:gpu_child_thread.cc(69)] Mojo error in GPU process: Received bad user message: Validation failed for viz.mojom.CompositorFrameSink.4 [VALIDATION_ERROR_DESERIALIZATION_FAILED]`

This means that a `SubmitCompositorFrame` was called with an invalid param (exact same thing we saw in Edge). In Edge's case, the surface range on the compositor frame metadata was invalid. I wonder if perhaps `ScopedKeepSurfaceAlive` was created with an invalid local surface id, and that causes an issue in its destructor when we `RemoveSurfaceRange` with an invalid `range_`. All other calls to `RemoveSurfaceRange` are gated by a check for a valid range param.

### ch...@google.com (2025-02-21)

Setting milestone because of s0/s1 severity.

### jo...@chromium.org (2025-02-21)

The speculative fix: <https://chromium-review.googlesource.com/c/chromium/src/+/6216395> prevents the `ScopedKeepAlive` from being created with an invalid Surface. Though it still creates a request to `CopyFromCompositingSurfaceInternal` with an invalid `SurfaceId`. We should stop that.

This portion itself is not a `heap-use-after-free`. During a navigation `DelegatedFrameHost` will clear its internal `LocalSurfaceId` and await a new one to begin embedding once navigation completes.

Typical flow:

```
0x122c07d11cc0 DelegatedFrameHost::DidNavigateMainFramePreCommit  lsid LocalSurfaceId(4, 1, 13F5...)
0x122c07d11cc0 DelegatedFrameHost::EmbedSurface  lsid LocalSurfaceId(0, 0, 0000...) new_lsid LocalSurfaceId(5, 1, 13F5...)
0x122c07d11cc0 DelegatedFrameHost::EmbedSurface  lsid LocalSurfaceId(5, 1, 13F5...) new_lsid LocalSurfaceId(5, 1, 13F5...)
0x122c07d11cc0 DelegatedFrameHost::DidNavigate lsid LocalSurfaceId(5, 1, 13F5...)


```

For the tabs that are attempting to copy invalid surfaces, the `EmbedSurface` is never being called, but `DidNavigate` is:

```
0x122c085c00c0 DelegatedFrameHost::DidNavigateMainFramePreCommit  lsid LocalSurfaceId(2, 1, 1C7C...)
0x122c085c00c0 DelegatedFrameHost::DidNavigate lsid LocalSurfaceId(0, 0, 0000...)


```

This is expected, as the Browser process will not attempt to `EmbedSurface` if a navigation occurs while a tab is hidden.

What is expected is that `RenderWidgetHostViewBase::OnShowWithPageVisibility(PageVisibilityState::kHiddenButPainting)` is called whenever we want to take a capture of a backgrounded tab. This is what leads to `DelegatedFrameHost::EmbedSurface` to actually tell Viz to start rendering with the content. So there is a bug in `navigator.mediaDevices.getDisplayMedia` when we have same-origin page across multiple tabs. +jrummell@ who I see added tests for it in `media/test/data/eme_and_get_display_media.html` and +dalecurtis@ from media.

Post speculative fix, this is no longer the `heap-use-after-free` also mentioned in #3 for a ClusterFuzz run. I'l remove fix to see if it repros that

### jo...@chromium.org (2025-02-21)

One other thing to note about #3 is that the `ui::Compositor` is using `cc::SingleThreadedProxy` so that is not a threading race condition as mentioned in the initial issue

### jo...@chromium.org (2025-02-21)

So without the speculative fix there is a path to a `heap-use-after-free`, `DCHECK` build validates this. `DelegatedFrameHost::CopyFromCompositingSurfaceInternal` only sets the callback thread if it succeeds in creating the `CopyOutputRequest`. This was fine previously. The addition of `ScopedKeepSurfaceAlive` is now trying to use a `WeakPtr` to `LayerTreeHostImpl`. If the request fails at creation, then we run the callback on a worker thread.

I'll update `DelegatedFrameHost` to address this issue, while also preventing even attempting to create these invalid requests.

### jo...@chromium.org (2025-02-21)

Dropping priority since the speculative fix prevents any `heap-use-after-free`

### mp...@google.com (2025-02-21)

The original bug is in 134 right? And the speculative fix is in 135? Let's make sure we merge a fix before stable cut (next Tuesday). If the speculative fix is simple enough to merge to 134 then we can attach the speculative fix CL to this bug, mark this bug as fixed to get merge automation started, and file further bugs for follow-on work.

### am...@chromium.org (2025-02-22)

[edited because I was somehow a week ahead] We would not drop this issue to P2 because a speculative fix has been landed, because that impacts backmerge and other security automation and pings. M134 Stable RC will be cut on Tuesday for release the following week.

Race is often considered a mitigation, especially wrt to browser UAF. I'm not willing to rely on that in terms of a backmerge decision since clusterfuzz was able to reproduce this, albeit flakily.

### am...@chromium.org (2025-02-22)

To get this backmerged and not botch up other automation, we should close this issue as fixed and a new child issue should be opened for further work here.

### am...@chromium.org (2025-02-22)

<https://crrev.com/c/6216395> landed on 19 February; looking at Canary date for the past three days, there do not seem to be any issues related to this fix
Please merge to M134 / Branch 6998 ASAP, by EOD Monday, so this fix can be included in the M134 Stable RC being cut on Tuesday.

### ch...@google.com (2025-02-22)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M134. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [134].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### jo...@google.com (2025-02-24)

Sent out merge review: <https://chromium-review.googlesource.com/c/chromium/src/+/6298470>

### bo...@chromium.org (2025-02-24)

Looking at the CF stacks in #3.. maybe latest trunk code is fixed, but I don't see how it happens?

It says `cc::ScopedKeepSurfaceAlive::~ScopedKeepSurfaceAlive` is using a UAF pointer to CommitState. But I don't see how that happens? First the LayerTreeHost pointer *should* be valid because of the WeakPtr check:
https://source.chromium.org/chromium/chromium/src/+/main:cc/trees/layer_tree_host.cc;drc=05401be858fce13f572977457ff78cea16418569;l=571

Then LayerTreeHost::RemoveSurfaceRange should be fine because it's just accessing its own internal pending_commit_state(), which afaict looks correct since it's never null (but can change).

So for pending_commit_state() to be pointing to an old value, somehow the LayerTreeHost pointer has to be corrupted in the first place? How does that happen in a way that CF isn't detecting that error first though? Eg if LayerTreeHost pointer in ScopedKeepSurfaceAlive constructor is already garbage, I would expect CF to detect that first?

### jo...@chromium.org (2025-02-24)

The repro page involves launching multiple tabs at startup, each of which triggers readback.

- Tabs are being created and switched so fast that they are never `PageVisibilityState::Visible`
- `RenderWidgetHostView*` does not call `DelegatedFrameHost::EmbedSurface` for hidden tabs, so that Viz doesn't try to work with non-visible content
- `navigator.mediaDevices.getDisplayMedia` programmatically triggers the read-back of content
- This generates a pop-up to get user permission via `chrome/browser/ui/views/desktop_capture/share_this_tab_source_view.h`
- This does trigger `DelegatedFrameHost::CopyFromCompositingSurface` however it does not first ensure that `RenderWidgetHostViewBase::OnShowWithPageVisibility(PageVisibilityState::kHiddenButPainting)` is called
- This was leading to `ui::Compositor::ScopedKeepSurfaceAliveCallback` being created for an invalid `viz::SurfaceId`
- `DelegatedFrameHost::CopyFromCompositingSurfaceInternal` has an early exit for `!CanCopyFromCompositingSurface()`
- However it creates the `viz::CopyOutputRequest` regardless to run callbacks
- `CopyOutputRequest::SendResult` will grab a threadpool thread if none has been set `base::ThreadPool::CreateSequencedTaskRunner`
- `DelegatedFrameHost::CopyFromCompositingSurfaceInternal` only sets the UI-thread as the runner if we can copy
- `cc::ScopedKeepSurfaceAlive::~ScopedKeepSurfaceAlive` ends up running on a thread-pool accessing `pending_commit_state` from the wrong thread
- The `WeakPtr` check is only valid on the thread it is bound on. So it is incorrectly passing on the background tread. DCHECK builds crash when we check it with this repro.

### bo...@chromium.org (2025-02-24)

Ahh did not notice the wrong thread bit. So should fix the threading I guess? The speculative one is only kinda only avoiding this specific case?

### ap...@google.com (2025-02-24)

Project: chromium/src  

Branch: refs/branch-heads/6998  

Author: Sahir Vellani <[sahir.vellani@microsoft.com](mailto:sahir.vellani@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6298470>

Create ScopedKeepSurfaceAlive only if compositing surface can be copied

---


Expand for full commit details
```
Create ScopedKeepSurfaceAlive only if compositing surface can be copied 
 
This is a speculative fix for an issue in Edge where Compositor Frames 
are submitted with surface ranges that have invalid local_surface_id's. 
 
The issue started due to change:5348259. 
 
The hypothesis is that if TakeScopedKeepSurfaceAliveCallback is called 
with an invalid local_surface_id_, the LayerTreeHost will still register 
the associated surface range. However, the CopyOutputRequest will not be 
fulfilled because CopyFromCompositingSurfaceInternal will early out if 
the local_surface_id_ is invalid. Therefore, the SurfaceRange is added 
to the commit state but never removed. When it's time for 
SubmitCompositorFrame, an invalid SurfaceRange can be present in the 
list. 
 
In order to fix this issue, check whether the local surface is valid for 
copy before calling TakeScopedKeepSurfaceAliveCallback. 
 
(cherry picked from commit fc7e46cc3314fd00771e1d5ccd2e33d84d21cb8a) 
 
Bug: 40276723, 397601495 
Change-Id: I6d2591ed0ee98ba0414887ea7611d640788d607b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6216395 
Reviewed-by: Bo Liu <boliu@chromium.org> 
Commit-Queue: Sahir Vellani <sahir.vellani@microsoft.com> 
Reviewed-by: Jonathan Ross <jonross@chromium.org> 
Reviewed-by: Shubham Gupta <shubham.gupta@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1422253} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6298470 
Commit-Queue: Jonathan Ross <jonross@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6998@{#1370} 
Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}

```

---

Files:

- M `content/browser/renderer_host/delegated_frame_host.cc`
- M `ui/compositor/compositor.cc`

---

Hash: 92d26167e4b277bebe10fc949759951a93561590  

Date:  Mon Feb 24 09:01:01 2025


---

### bo...@chromium.org (2025-02-24)

And I guess this feels like a pretty big footgun of maximizing surprise:
https://source.chromium.org/chromium/chromium/src/+/main:components/viz/common/frame_sinks/copy_output_request.cc;drc=ccea09835fd67b49ef0d4aed8dda1a5f22a409c8;l=129

Ideally should be safe(r) by default, and opt into fast and potentially unsafe if client wants it..

### pe...@google.com (2025-02-24)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### jo...@chromium.org (2025-02-24)

Re #26/28, yeah I'm working on a follow up to address that `DelegatedFrameHost` could run on the wrong thread. Along with tests that repro this failure path to guard against future regressions.

For the underlying surprise in CopyOutputRequest, yeah we should definitely address that. Worth a separate follow-up as well

### jo...@chromium.org (2025-02-24)

Re #29 the patch that lead to this only landed in M134, no need to merge back to LTS M132 for ChromeOS

### jo...@chromium.org (2025-02-24)

Removing Android from OS list, since this is tied to `DelegatedFrameHost` which is separate from Android's `DelegatedFrameHostAndroid`

### rz...@google.com (2025-02-25)

Labelling as not applicable for 126, "keep\_surface\_alive" isn't used in the changed calls.

### rz...@google.com (2025-02-25)

Also, see #31, labelling as not applicable for 132 as well.

### sp...@google.com (2025-02-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $26000.00 for this report.

Rationale for this decision:
$25,000 for report of memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-27)

Congratulations! Thank you for your efforts finding and reporting this browser UAF and reporting it to us -- nice work!

### ch...@google.com (2025-06-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $25,000 for report of memory corruption in a non-sandboxed process + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/397601495)*
