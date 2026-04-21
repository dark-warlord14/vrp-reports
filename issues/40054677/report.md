# UAP in MojoWatcher::OnHandleReady

| Field | Value |
|-------|-------|
| **Issue ID** | [40054677](https://issues.chromium.org/issues/40054677) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Internals>Mojo>Core |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2021-02-04 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:
Test with asan-linux-release-849869
1.python copy_mojo_js_bindings.py path/to/ASAN/gen/
2.python -m SimpleHTTPServer 8605
3.ASAN/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/noexit http://127.0.0.1:8605/uap.html
4. wait for a moment

What is the expected behavior?

What went wrong?
After load the uap.html, the render will crash, here is the ASAN log with '--no-sandbox' option (to get the symbol).
=================================================================
==1174203==ERROR: AddressSanitizer: use-after-poison on address 0x7edafd13bef0 at pc 0x560adbf5dae6 bp 0x7ffc7c964a90 sp 0x7ffc7c964a88
READ of size 8 at 0x7edafd13bef0 thread T0 (chrome)
    #0 0x560adbf5dae5 in operator* base/memory/scoped_refptr.h:231:13
    #1 0x560adbf5dae5 in blink::MojoWatcher::OnHandleReady(MojoTrapEvent const*) third_party/blink/renderer/core/mojo/mojo_watcher.cc:146:7
    #2 0x560ac49fcdb5 in mojo::core::WatcherDispatcher::InvokeWatchCallback(unsigned long, unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watcher_dispatcher.cc:94:3
    #3 0x560ac49fbe3a in mojo::core::Watch::InvokeCallback(unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watch.cc:78:13
    #4 0x560ac49efce2 in mojo::core::RequestContext::~RequestContext() mojo/core/request_context.cc:66:14
    #5 0x560ac49a057d in mojo::core::Core::Close(unsigned int) mojo/core/core.cc:263:1
    #6 0x560acb3743ff in Finalize third_party/blink/renderer/platform/heap/impl/heap_page.cc:95:5
    #7 0x560acb3743ff in blink::NormalPage::ToBeFinalizedObject::Finalize() third_party/blink/renderer/platform/heap/impl/heap_page.cc:1402:11
    #8 0x560acb374617 in blink::NormalPage::FinalizeSweep(blink::SweepResult) third_party/blink/renderer/platform/heap/impl/heap_page.cc:1411:12
    #9 0x560acb36bf42 in blink::BaseArena::LazySweepWithDeadline(base::TimeTicks) third_party/blink/renderer/platform/heap/impl/heap_page.cc:349:11
    #10 0x560acb35badd in blink::ThreadHeap::AdvanceLazySweep(base::TimeTicks) third_party/blink/renderer/platform/heap/impl/heap.cc:753:22
    #11 0x560acb38cf5e in blink::ThreadState::PerformIdleLazySweep(base::TimeTicks) third_party/blink/renderer/platform/heap/impl/thread_state.cc:453:30
    #12 0x560acb4212fa in Run base/callback.h:101:12
    #13 0x560acb4212fa in blink::scheduler::MainThreadSchedulerImpl::RunIdleTask(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks) third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:2404:19
    #14 0x560acb42fccc in Invoke<void (*)(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks), base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks> base/bind_internal.h:393:12
    #15 0x560acb42fccc in MakeItSo<void (*)(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks), base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks> base/bind_internal.h:637:12
    #16 0x560acb42fccc in RunImpl<void (*)(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks), std::tuple<base::OnceCallback<void (base::TimeTicks)> >, 0> base/bind_internal.h:710:12
    #17 0x560acb42fccc in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks), base::OnceCallback<void (base::TimeTicks)> >, void (base::TimeTicks)>::RunOnce(base::internal::BindStateBase*, base::TimeTicks&&) base/bind_internal.h:679:12
    #18 0x560acb3b2c78 in Run base/callback.h:101:12
    #19 0x560acb3b2c78 in blink::scheduler::SingleThreadIdleTaskRunner::RunTask(base::OnceCallback<void (base::TimeTicks)>) third_party/blink/renderer/platform/scheduler/common/single_thread_idle_task_runner.cc:87:24
    #20 0x560acb3b3fd6 in Invoke<void (blink::scheduler::SingleThreadIdleTaskRunner::*)(base::OnceCallback<void (base::TimeTicks)>), base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> > base/bind_internal.h:498:12
    #21 0x560acb3b3fd6 in MakeItSo<void (blink::scheduler::SingleThreadIdleTaskRunner::*)(base::OnceCallback<void (base::TimeTicks)>), base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> > base/bind_internal.h:657:5
    #22 0x560acb3b3fd6 in void base::internal::Invoker<base::internal::BindState<void (blink::scheduler::SingleThreadIdleTaskRunner::*)(base::OnceCallback<void (base::TimeTicks)>), base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> >, void ()>::RunImpl<void (blink::scheduler::SingleThreadIdleTaskRunner::*)(base::OnceCallback<void (base::TimeTicks)>), std::__1::tuple<base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> >, 0ul, 1ul>(void (blink::scheduler::SingleThreadIdleTaskRunner::*&&)(base::OnceCallback<void (base::TimeTicks)>), std::__1::tuple<base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> >&&, std::__1::integer_sequence<unsigned long, 0ul, 1ul>) base/bind_internal.h:710:12
    #23 0x560acc6a2407 in Run base/callback.h:101:12
    #24 0x560acc6a2407 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:163:33
    #25 0x560acc6e0503 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #26 0x560acc6dfcc4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264:36
    #27 0x560acc5a4430 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:39:55
    #28 0x560acc6e1d7c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460:12
    #29 0x560acc62aaa1 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:133:14
    #30 0x560ae1282d09 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:260:16
    #31 0x560acc383420 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:494:14
    #32 0x560acc386b4d in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:877:10
    #33 0x560acc3808ae in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:372:36
    #34 0x560acc380e9c in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:398:10
    #35 0x560ac0146ac7 in ChromeMain chrome/app/chrome_main.cc:141:12
    #36 0x7fc044ce30b2 in __libc_start_main /build/glibc-ZN95T4/glibc-2.31/csu/../csu/libc-start.c:308:16

Address 0x7edafd13bef0 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison base/memory/scoped_refptr.h:231:13 in operator*
Shadow bytes around the buggy address:
  0x0fdbdfa1f780: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdbdfa1f790: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdbdfa1f7a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdbdfa1f7b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00
  0x0fdbdfa1f7c0: 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fdbdfa1f7d0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7
  0x0fdbdfa1f7e0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdbdfa1f7f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdbdfa1f800: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdbdfa1f810: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdbdfa1f820: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==1174203==ABORTING

Did this work before? N/A 

Chrome version: 87.0.4280.88  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [uap.html](attachments/uap.html) (text/plain, 373 B)

## Timeline

### [Deleted User] (2021-02-04)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-02-04)

update the poc

### ts...@chromium.org (2021-02-04)

merc - do you need the MojoJs flag in order to do this, or it it just a way to make it more efficient to code?

### me...@gmail.com (2021-02-05)

This need the MojoJS flag and I find that I attach the wrong poc, so I update it again...

### [Deleted User] (2021-02-05)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2021-02-05)

rockot - could you take a look or re-assign as appropriate?  I'm not sure if the issue is in mojo itself, or in the blink/heap integration, or ...
Setting impact none since command line flag is required.

[Monorail components: Blink>MemoryAllocator>GarbageCollection Internals>Mojo>Core]

### me...@gmail.com (2021-02-07)

Note that asan-linux-release-851511 can also triger this bug with the new poc.

### ro...@google.com (2021-02-08)

Definitely looks like bad integration between a Mojo consumer and Blink heap.

I've been unable to repro locally though, so I can't really diagnose it further. If there's an ASAN repro, a symbolized output from that would be useful in tracking down the offending Blink code.

### me...@gmail.com (2021-02-09)

Here is the symbolized output with the new poc in Commnet 7. Maybe you need to wait a while to trigger the crash.
=================================================================
==598477==ERROR: AddressSanitizer: use-after-poison on address 0x7eed295ba3f8 at pc 0x5571ecb965e6 bp 0x7ffd75a04c70 sp 0x7ffd75a04c68
READ of size 8 at 0x7eed295ba3f8 thread T0 (chrome)
[598441:598455:0208/175417.501323:ERROR:ssl_client_socket_impl.cc(924)] handshake failed; returned -1, SSL error code 1, net_error -202
    #0 0x5571ecb965e5 in operator* base/memory/scoped_refptr.h:231:13
    #1 0x5571ecb965e5 in blink::MojoWatcher::OnHandleReady(MojoTrapEvent const*) third_party/blink/renderer/core/mojo/mojo_watcher.cc:146:7
    #2 0x5571d55b1295 in mojo::core::WatcherDispatcher::InvokeWatchCallback(unsigned long, unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watcher_dispatcher.cc:94:3
    #3 0x5571d55b031a in mojo::core::Watch::InvokeCallback(unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watch.cc:78:13
    #4 0x5571d55a41c2 in mojo::core::RequestContext::~RequestContext() mojo/core/request_context.cc:66:14
    #5 0x5571d555400d in mojo::core::Core::Close(unsigned int) mojo/core/core.cc:263:1
    #6 0x5571dbf5dbaf in Finalize third_party/blink/renderer/platform/heap/impl/heap_page.cc:95:5
    #7 0x5571dbf5dbaf in blink::NormalPage::ToBeFinalizedObject::Finalize() third_party/blink/renderer/platform/heap/impl/heap_page.cc:1402:11
    #8 0x5571dbf5ddc7 in blink::NormalPage::FinalizeSweep(blink::SweepResult) third_party/blink/renderer/platform/heap/impl/heap_page.cc:1411:12
    #9 0x5571dbf556f2 in blink::BaseArena::LazySweepWithDeadline(base::TimeTicks) third_party/blink/renderer/platform/heap/impl/heap_page.cc:349:11
    #10 0x5571dbf4528d in blink::ThreadHeap::AdvanceLazySweep(base::TimeTicks) third_party/blink/renderer/platform/heap/impl/heap.cc:753:22
    #11 0x5571dbf7667e in blink::ThreadState::PerformIdleLazySweep(base::TimeTicks) third_party/blink/renderer/platform/heap/impl/thread_state.cc:453:30
    #12 0x5571dc0089ba in Run base/callback.h:101:12
    #13 0x5571dc0089ba in blink::scheduler::MainThreadSchedulerImpl::RunIdleTask(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks) third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:2404:19
    #14 0x5571dc01738c in Invoke<void (*)(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks), base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks> base/bind_internal.h:393:12
    #15 0x5571dc01738c in MakeItSo<void (*)(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks), base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks> base/bind_internal.h:637:12
    #16 0x5571dc01738c in RunImpl<void (*)(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks), std::tuple<base::OnceCallback<void (base::TimeTicks)> >, 0> base/bind_internal.h:710:12
    #17 0x5571dc01738c in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (base::TimeTicks)>, base::TimeTicks), base::OnceCallback<void (base::TimeTicks)> >, void (base::TimeTicks)>::RunOnce(base::internal::BindStateBase*, base::TimeTicks&&) base/bind_internal.h:679:12
    #18 0x5571dbf9a348 in Run base/callback.h:101:12
    #19 0x5571dbf9a348 in blink::scheduler::SingleThreadIdleTaskRunner::RunTask(base::OnceCallback<void (base::TimeTicks)>) third_party/blink/renderer/platform/scheduler/common/single_thread_idle_task_runner.cc:87:24
    #20 0x5571dbf9b6a6 in Invoke<void (blink::scheduler::SingleThreadIdleTaskRunner::*)(base::OnceCallback<void (base::TimeTicks)>), base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> > base/bind_internal.h:498:12
    #21 0x5571dbf9b6a6 in MakeItSo<void (blink::scheduler::SingleThreadIdleTaskRunner::*)(base::OnceCallback<void (base::TimeTicks)>), base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> > base/bind_internal.h:657:5
    #22 0x5571dbf9b6a6 in void base::internal::Invoker<base::internal::BindState<void (blink::scheduler::SingleThreadIdleTaskRunner::*)(base::OnceCallback<void (base::TimeTicks)>), base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> >, void ()>::RunImpl<void (blink::scheduler::SingleThreadIdleTaskRunner::*)(base::OnceCallback<void (base::TimeTicks)>), std::__1::tuple<base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> >, 0ul, 1ul>(void (blink::scheduler::SingleThreadIdleTaskRunner::*&&)(base::OnceCallback<void (base::TimeTicks)>), std::__1::tuple<base::WeakPtr<blink::scheduler::SingleThreadIdleTaskRunner>, base::OnceCallback<void (base::TimeTicks)> >&&, std::__1::integer_sequence<unsigned long, 0ul, 1ul>) base/bind_internal.h:710:12
    #23 0x5571dd289777 in Run base/callback.h:101:12
    #24 0x5571dd289777 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:163:33
    #25 0x5571dd2c78c3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #26 0x5571dd2c7084 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264:36
    #27 0x5571dd18b7b0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:39:55
    #28 0x5571dd2c913c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460:12
    #29 0x5571dd211df1 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:133:14
    #30 0x5571f1eb5d79 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:260:16
    #31 0x5571dcf6a760 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:494:14
    #32 0x5571dcf6de8d in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:877:10
    #33 0x5571dcf67bd6 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:372:36
    #34 0x5571dcf681dc in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:398:10
    #35 0x5571d0cc9637 in ChromeMain chrome/app/chrome_main.cc:141:12
    #36 0x7f53c9a630b2 in __libc_start_main /build/glibc-ZN95T4/glibc-2.31/csu/../csu/libc-start.c:308:16

Address 0x7eed295ba3f8 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison base/memory/scoped_refptr.h:231:13 in operator*
Shadow bytes around the buggy address:
  0x0fde252af420: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fde252af430: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fde252af440: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fde252af450: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00
  0x0fde252af460: 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7 f7
=>0x0fde252af470: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]
  0x0fde252af480: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fde252af490: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fde252af4a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fde252af4b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fde252af4c0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==598477==ABORTING


### ro...@google.com (2021-02-11)

Actually it seems like either a bug in MojoWatcher, which -- just to confirm what has already been discussed -- can only be used if MojoJS is enabled.

I have attached a significantly simplified and reliable repro which does not need to load any bindings or require an HTTP server. It needs only --enable-blink-features=MojoJS, and --js-flags=--expose-gc (for faster repro)

I have a fix uploaded at https://chromium-review.googlesource.com/c/chromium/src/+/2690995 but I would also really like to understand how it's possible for the MojoWatcher to be GCed in this case.

### ro...@google.com (2021-02-11)

Meant to say, either a bug in MojoWatcher, or a bug in some aspect of the GC infra it relies on. More specifically I am confused about why an ActiveScriptWrappable would be GCed when it would definitely still return true from HasPendingActivity().

### ro...@google.com (2021-02-12)

+talp@ since based on commit history you seem to be quite familiar with ContextLifecycleObserver behavior.

For some background, there's MojoWatcher,[1] used by Mojo JS bindings. It's an ExecutionContextLifecycleObserver as well as an ActiveScriptWrappable. It registers itself with Mojo internals and can be called into by Mojo at any time from any thread. The callback we give to Mojo assumes the MojoWatcher object is still alive when invoked.

I believed this assumption was valid until this UAP appeared (see https://crbug.com/chromium/1174373#c10 for a small repro case), because HasPendingActivity() is always true as long as the object is registered with Mojo internals. It seems however that the MojoWatcher is getting GCed anyway. With the repro case, the Mojo callback is invoked after the MojoWatcher's memory has been poisoned.

After some investigation it seems that the ExecutionContext is destroyed (in the IsContextDestroyed() sense, but not actually deleted yet). That should be OK since this is an ECLO, except the MojoWatcher's ContextDestroyed() is not invoked as expected in this case. Do you think that could possibly be a bug, or is there some subtlety by which this is expected behavior?

I do have a fix ready to go in case it's expected behavior, but I want to avoid papering over a deeper issue if one exists.

Thanks!

[1] https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/mojo/mojo_watcher.h;drc=c80c8856745719bda4739d3eec11be3b4380e754;l=24


### ta...@google.com (2021-02-12)

> I believed this assumption was valid [...] because HasPendingActivity() is always true
I believe this is (at least part of) the issue. The ASW comment (and the CL description on the CL introducing it[1]) specifically mention that if GetExecutionContext() returns nullptr or a detached context, HasPendingActivity will be ignored.

> except the MojoWatcher's ContextDestroyed() is not invoked as expected in this case
The following all happen synchronously (on the EC's thread):
1. ExecutionContext setting its is_context_destroyed_ flag.
2. ECLOs' ContextDestroyed() is called.
3. ECLOs' internal EC reference is reset to null (=> causing GetExecutionContext to return nullptr).
So it should not be possible to observer IsContextDestroyed() without the ContextDestroyed() function having been called. The exception to that would be if the EC/ASW are accessed cross-thread - they are only intended to be accessed from the thread the EC is "associated" with (the main thread for frames, worker thread for workers).

Re: your proposed fix, I think holding on to the wrapper in a CrossThreadPersistent that lives for as long as the handle is valid would stop the object from being GCd, but note that it may still be triggered after the context is destroyed (not sure if that's an issue or not).

[1] crrev.com/2577053002

### ro...@google.com (2021-02-12)

The cross-thread issue could explain why I see IsContextDestroyed()==true since I was testing it from an arbitrary thread, but I guess still I don't see how the MojoWatcher can be GCed given the above information.

I have confirmed that ContextDestroyed() is never called on this object. As far as I can tell, since 1-3 happen synchronously on this (main) thread, that must mean that is_context_destroyed_ isn't true yet either**, so GetExecutionContext() must return non-null. But if that's the case then HasPendingActivity (which by now always returns true) cannot be ignored and the object shouldn't be GCed.

** Unless it's possible for a GC to happen between setting is_context_destroyed_ and invoking ContextDestroyed()?

### ta...@google.com (2021-02-15)

> I have confirmed that ContextDestroyed() is never called on this object
It used to be possible for the EC to be garbage-collected without being notified of destruction. I recently tried adding some DCHECKs to verify that it is indeed always called, but I wouldn't be surprised to discover there are still some flows where it isn't. (Note that the notification isn't automatic, ExecutionContext::NotifyContextDestroyed must be called manually). If there are flows where this happens, that does seem to be a bug that we should try to track down.

re: HasPendingActivity,
I am not that familiar with ASW, but if I understand its intent correctly, it's supposed to be bound to the EC, and once that is "gone" I'm not sure what guarantees still remain regarding its behavior. More specifically, I don't believe HasPendingActivity would prevent the object from being GCd.

Looking again at the MojoWatcher code, I do think your fix is "correct" - since MojoWatcher is an Oilpan object all long-lived references to it should be held in some sort of Persistent reference, and that should include the "context" passed to MojoAddTrigger.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c5f602528690e14542a24df5d2492fa389df711a

commit c5f602528690e14542a24df5d2492fa389df711a
Author: Ken Rockot <rockot@google.com>
Date: Wed Feb 17 08:17:37 2021

Fix UAP in Blink MojoWatcher

The MojoWatcher implementation had incorrectly assumed it would always
be alive when the underlying trap triggers, because we were relying on
its ActiveScriptWrappable::HasPendingActivity impl always returning true
as long as the trap is alive. However ASW cannot prevent the object
from being GCed when its ExecutionContext is destroyed, and this could
result in a UAP when Mojo attempts to signal the object.

This ensures that MojoWatcher retains a persistent reference to itself
as long as its underlying trap is active.

Fixed: 1174373
Change-Id: I47ebea231fbe96f5d5914379e63976ce6bb45375
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2690995
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#854669}

[modify] https://crrev.com/c5f602528690e14542a24df5d2492fa389df711a/third_party/blink/renderer/core/mojo/mojo_watcher.h
[modify] https://crrev.com/c5f602528690e14542a24df5d2492fa389df711a/third_party/blink/renderer/core/mojo/mojo_watcher.cc


### [Deleted User] (2021-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-25)

Congratulations, merc.ouc@! The VRP Panel has decided to award you $2,000 for this report. Nicely done!

### me...@gmail.com (2021-02-25)

Thank you.

### am...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### is...@google.com (2021-09-16)

This issue was migrated from crbug.com/chromium/1174373?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Internals>Mojo>Core]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054677)*
