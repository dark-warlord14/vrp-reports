# Security: heap-use-after-free in MacNotificationServiceUN::CloseNotificationsForProfile

| Field | Value |
|-------|-------|
| **Issue ID** | [343302586](https://issues.chromium.org/issues/343302586) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Notifications |
| **Platforms** | Mac |
| **Chrome Version** | 127.0.0.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2024-05-29 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

1. This vulnerability needs to be triggered on macos. I chose to compile asan from source code. It can be triggered on two different versions and is relatively stable on my Macos M3 test device. I will optimize the triggering method as much as possible in the future.
2. Both different versions can be stably triggered. You can choose one of them:

```
git checkout e725fef94d8f4e6b0be2db8e37e00e8c8c2d765a
git apply features1.diff
or
git checkout 888d897d972ff83858c048e78510deb6593057f4
git apply features2.diff

```

gn args are exactly the same

```
is_component_build = true
is_debug = false
is_asan = true
symbol_level = 2
dcheck_always_on = false
treat_warnings_as_errors = false

```

3. Use puppeteer-core is more convenient to trigger the vulnerability. You need to change the launchCommand in the asan1.js file to your Mac asan chromium file path

```
npm install puppeteer-core
node asan1.js 2>&1 | grep -E "AddressSanitizer" -A 100

```

Wait patiently to trigger UAF. For complete asan log information, refer to `asan.txt` and `uaf.mov`

# Problem Description

Security: heap-use-after-free in MacNotificationServiceUN::CloseNotificationsForProfile

# Summary

Security: heap-use-after-free in MacNotificationServiceUN::CloseNotificationsForProfile

# Custom Questions

#### Type of crash:

browser

#### Crash state:

```
=================================================================
==13039==ERROR: AddressSanitizer: heap-use-after-free on address 0x61600002a3f0 at pc 0x000119a267ac bp 0x000176785f10 sp 0x000176785f08
READ of size 8 at 0x61600002a3f0 thread T15
==13039==WARNING: invalid path to external symbolizer!
==13096==WARNING: invalid path to external symbolizer!
==13096==WARNING: Failed to use and restart external symbolizer!
==13039==WARNING: Failed to use and restart external symbolizer!
    #0 0x119a267a8 in invocation function for block in mac_notifications::MacNotificationServiceUN::CloseNotificationsForProfile(mojo::InlinedStructPtr<mac_notifications::mojom::ProfileIdentifier>)+0x5e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libchrome_dll.dylib:arm64+0x240e7a8)
    #1 0x101c68240 in __asan_memmove+0x1da4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libclang_rt.asan_osx_dynamic.dylib:arm64+0x50240)
    #2 0x19dad874c in _dispatch_call_block_and_release+0x1c (/usr/lib/system/libdispatch.dylib:arm64+0x274c)
    #3 0xeb6d80019dada3e4  (<unknown module>)
    #4 0x3d0e00019dae1a10  (<unknown module>)
    #5 0x3f0d00019dae2574  (<unknown module>)
    #6 0x4d2900019daed2cc  (<unknown module>)
    #7 0xfb6800019daecb40  (<unknown module>)
    #8 0xee1a80019dc87008  (<unknown module>)
    #9 0x576680019dc85d24  (<unknown module>)

0x61600002a3f0 is located 112 bytes inside of 592-byte region [0x61600002a380,0x61600002a5d0)
freed by thread T0 here:
    #0 0x101c78524 in __sanitizer_finish_switch_fiber+0xa24 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libclang_rt.asan_osx_dynamic.dylib:arm64+0x60524)
    #1 0x119a14cb8 in mac_notifications::MacNotificationProviderImpl::~MacNotificationProviderImpl()+0x1a4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libchrome_dll.dylib:arm64+0x23fccb8)
    #2 0x119a14e8c in mac_notifications::MacNotificationProviderImpl::~MacNotificationProviderImpl()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libchrome_dll.dylib:arm64+0x23fce8c)
    #3 0x1204cfa14 in mojo::ServiceFactory::InstanceHolder<mac_notifications::MacNotificationProviderImpl>::~InstanceHolder()+0x74 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libchrome_dll.dylib:arm64+0x8eb7a14)
    #4 0x102722858 in std::__Cr::vector<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase>>, std::__Cr::allocator<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase>>>>::erase(std::__Cr::__wrap_iter<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase>> const*>, std::__Cr::__wrap_iter<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase>> const*>)+0x17c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x66858)
    #5 0x10271fad4 in mojo::ServiceFactory::OnInstanceDisconnected(mojo::ServiceFactory::InstanceHolderBase*)+0x198 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x63ad4)
    #6 0x102720ee0 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::ServiceFactory::*&&)(mojo::ServiceFactory::InstanceHolderBase*), base::WeakPtr<mojo::ServiceFactory>&&, mojo::ServiceFactory::InstanceHolderBase*&&>, base::internal::BindState<true, true, false, void (mojo::ServiceFactory::*)(mojo::ServiceFactory::InstanceHolderBase*), base::WeakPtr<mojo::ServiceFactory>, base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (mojo::ServiceFactory::*)(mojo::ServiceFactory::InstanceHolderBase*), std::__Cr::tuple<base::WeakPtr<mojo::ServiceFactory>, base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul>(void (mojo::ServiceFactory::*&&)(mojo::ServiceFactory::InstanceHolderBase*), std::__Cr::tuple<base::WeakPtr<mojo::ServiceFactory>, base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>)+0x208 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x64ee0)
    #7 0x1027218c4 in base::internal::ThenHelper<base::OnceCallback<void ()>, base::OnceCallback<void ()>>::CreateTrampoline()::'lambda'(base::OnceCallback<void ()>, base::OnceCallback<void ()>)::operator()(base::OnceCallback<void ()>, base::OnceCallback<void ()>) const+0x17c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x658c4)
    #8 0x102721668 in base::internal::Invoker<base::internal::FunctorTraits<base::internal::ThenHelper<base::OnceCallback<void ()>, base::OnceCallback<void ()>>::CreateTrampoline()::'lambda'(base::OnceCallback<void ()>, base::OnceCallback<void ()>)&&, base::OnceCallback<void ()>&&, base::OnceCallback<void ()>&&>, base::internal::BindState<false, false, false, base::internal::ThenHelper<base::OnceCallback<void ()>, base::OnceCallback<void ()>>::CreateTrampoline()::'lambda'(base::OnceCallback<void ()>, base::OnceCallback<void ()>), base::OnceCallback<void ()>, base::OnceCallback<void ()>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x150 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x65668)
    #9 0x1027207dc in mojo::ServiceFactory::InstanceHolderBase::OnPipeSignaled(unsigned int, mojo::HandleSignalsState const&)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x647dc)
    #10 0x1027212e4 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::ServiceFactory::InstanceHolderBase::* const&)(unsigned int, mojo::HandleSignalsState const&), mojo::ServiceFactory::InstanceHolderBase*>, base::internal::BindState<true, true, false, void (mojo::ServiceFactory::InstanceHolderBase::*)(unsigned int, mojo::HandleSignalsState const&), base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0x194 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x652e4)
    #11 0x1015e79e8 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_system_cpp.dylib:arm64+0x179e8)
    #12 0x1015e73f0 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_system_cpp.dylib:arm64+0x173f0)
    #13 0x1015e8310 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_system_cpp.dylib:arm64+0x18310)
    #14 0x1032abfc4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x18bfc4)
    #15 0x1033143d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x1f43d8)
    #16 0x103313844 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x1f3844)
    #17 0x10345d2e8 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x33d2e8)
    #18 0x10344b9f4 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x32b9f4)
    #19 0x10345b88c in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x33b88c)
    #20 0x19dd6a4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)
    #21 0x3b7d80019dd6a468  (<unknown module>)
    #22 0x2d4280019dd6a1d8  (<unknown module>)
    #23 0xaa6180019dd68dc4  (<unknown module>)
    #24 0xfc2080019dd68430  (<unknown module>)
    #25 0x127d0001a850c198  (<unknown module>)
    #26 0x896a8001a850bfd4  (<unknown module>)
    #27 0x8f768001a850bd2c  (<unknown module>)
    #28 0xce240001a15c7d64  (<unknown module>)
    #29 0x934a0001a1dbd804  (<unknown module>)

previously allocated by thread T0 here:
    #0 0x101c7811c in __sanitizer_finish_switch_fiber+0x61c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libclang_rt.asan_osx_dynamic.dylib:arm64+0x6011c)
    #1 0x119a153fc in std::__Cr::__unique_if<mac_notifications::MacNotificationServiceUN>::__unique_single std::__Cr::make_unique<mac_notifications::MacNotificationServiceUN, mojo::PendingRemote<mac_notifications::mojom::MacNotificationActionHandler>, base::internal::DoNothingCallbackTag, UNUserNotificationCenter* __strong>(mojo::PendingRemote<mac_notifications::mojom::MacNotificationActionHandler>&&, base::internal::DoNothingCallbackTag&&, UNUserNotificationCenter* __strong&&)+0xd0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libchrome_dll.dylib:arm64+0x23fd3fc)
    #2 0x119a14fcc in mac_notifications::MacNotificationProviderImpl::BindNotificationService(mojo::PendingReceiver<mac_notifications::mojom::MacNotificationService>, mojo::PendingRemote<mac_notifications::mojom::MacNotificationActionHandler>)+0x134 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libchrome_dll.dylib:arm64+0x23fcfcc)
    #3 0x118743cec in mac_notifications::mojom::MacNotificationProviderStubDispatch::Accept(mac_notifications::mojom::MacNotificationProvider*, mojo::Message*)+0x248 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libchrome_dll.dylib:arm64+0x112bcec)
    #4 0x1026de9e4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x7ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x229e4)
    #5 0x1026f2914 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x36914)
    #6 0x1026e2d9c in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x26d9c)
    #7 0x1026fe244 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x77c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x42244)
    #8 0x1026fc89c in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x418 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x4089c)
    #9 0x1026f2914 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x36914)
    #10 0x1026ccff8 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x378 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x10ff8)
    #11 0x1026ce930 in mojo::Connector::ReadAllAvailableMessages()+0x23c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x12930)
    #12 0x1026ce408 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x12408)
    #13 0x1026d05a0 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x145a0)
    #14 0x1026cffbc in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x13fbc)
    #15 0x1026cfd90 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_cpp_bindings.dylib:arm64+0x13d90)
    #16 0x1015e79e8 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_system_cpp.dylib:arm64+0x179e8)
    #17 0x1015e73f0 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_system_cpp.dylib:arm64+0x173f0)
    #18 0x1015e8310 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libmojo_public_system_cpp.dylib:arm64+0x18310)
    #19 0x1032abfc4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x18bfc4)
    #20 0x1033143d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x1f43d8)
    #21 0x103313844 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x1f3844)
    #22 0x10345d2e8 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x33d2e8)
    #23 0x10344b9f4 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x32b9f4)
    #24 0x10345b88c in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libbase.dylib:arm64+0x33b88c)
    #25 0x19dd6a4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)
    #26 0x3b7d80019dd6a468  (<unknown module>)
    #27 0x2d4280019dd6a1d8  (<unknown module>)
    #28 0xaa6180019dd68dc4  (<unknown module>)
    #29 0xfc2080019dd68430  (<unknown module>)

Thread T15 created by T0 here:
    <empty stack>

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0527/libchrome_dll.dylib:arm64+0x240e7a8) in invocation function for block in mac_notifications::MacNotificationServiceUN::CloseNotificationsForProfile(mojo::InlinedStructPtr<mac_notifications::mojom::ProfileIdentifier>)+0x5e0
Shadow bytes around the buggy address:
  0x61600002a100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61600002a180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61600002a200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61600002a280: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x61600002a300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x61600002a380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd
  0x61600002a400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61600002a480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61600002a500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61600002a580: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x61600002a600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
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

==13039==ADDITIONAL INFO

==13039==Note: Please include this section with the ASan report.
Task trace:

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==13039==END OF ADDITIONAL INFO
==13039==ABORTING
Received signal 6
 [0x00010343516c]
 [0x0001033f5ff4]
 [0x000103434c88]
 [0x00019dcbb584]
 [0x00019dc8ac20]
 [0x00019db97a30]
 [0x000101c8eaf0]
 [0x000101c8e130]
 [0x000101c713ac]
 [0x000101c7066c]
 [0x000101c71b80]
 [0x000119a267ac]
 [0x000101c68244]
 [0x00019dad8750]
 [0x00019dada3e8]
 [0x00019dae1a14]
 [0x00019dae2578]
 [0x00019daed2d0]
 [0x00019daecb44]
 [0x00019dc8700c]
 [0x00019dc85d28]
[end of stack trace]

```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 19.8 KB)
- [features1.diff](attachments/features1.diff) (text/x-diff, 330.2 KB)
- [features2.diff](attachments/features2.diff) (text/x-diff, 330.9 KB)
- [main.html](attachments/main.html) (text/html, 39 B)
- [asan1.js](attachments/asan1.js) (text/javascript, 1.4 KB)
- [asan2.js](attachments/asan2.js) (text/javascript, 1.4 KB)
- [uaf.mov](attachments/uaf.mov) (video/quicktime, 462.2 MB)

## Timeline

### zh...@gmail.com (2024-05-29)

Sorry for forgetting to submit the most critical asan1.js、asan2.js and uaf.mov

If the one-time reproduction fails, you can try:

```
killall -9 Chromium
pkill -f chromium
node asan1.js 2>&1 | grep -E "AddressSanitizer" -A 100

```

### zh...@gmail.com (2024-05-29)

### Bisect commit

<https://chromiumdash.appspot.com/commit/4a2ff2211f744210fc09966f356f95e25d5e796c>

### zh...@gmail.com (2024-05-29)

I'm sorry that `uaf.mov` is 462M in size. I hope you can understand. I just want to show in more detail that I can reproduce the vulnerability stably and get a complete asan log.

One thing that confuses me is that the Mac terminal often does not display the complete asan log, that is, there is no function call stack information. I asked this question on Twitter:
<https://x.com/zh1x1an1221/status/1791055442535436688>
At present, I have not found a good solution on Mac. Usually, I have to wait patiently for the vulnerability to be triggered multiple times, and then the asan log will contain the complete function call stack information. In the uaf.mov video, I waited patiently until the complete asan log was displayed, so the entire video file is very large

If you know how to solve this problem, please let me know. Thank you very much

### mp...@google.com (2024-05-30)

mek@ based on the ASan report and the bisected commit, do you happen to know what might be happening here?

### me...@chromium.org (2024-05-30)

None of the MacNotificationServiceUN code is used/reachable yet in chrome, unless the NewMacNotificationAPI feature (for usage in the browser process) or AppShimNotificationAttribution feature (for usage in app shim processes) is enabled, so users shouldn't directly be effected by this.

But I think I see what's going on. The objective-c block in MacNotificationServiceUN::CloseNotificationsForProfile implicitly captures `this` by value, and then dereferences that to access its `notification_center_` member. Should be a pretty easy fix (and I really wish objective-C blocks didn't make it so easy to shoot yourself in the foot...)

### pg...@google.com (2024-05-30)

FoundIn based on the bisect in [comment #3](https://issues.chromium.org/issues/343302586#comment3) and Impact based on [comment #6](https://issues.chromium.org/issues/343302586#comment6) (: thank you both!

### pg...@google.com (2024-05-30)

setting severity=s0 due to uaf in browser with no mitigations in place as far as I can see, though the diffs applied enable about a thousand disabled-by-default features so impact is still solidly None

### am...@chromium.org (2024-06-05)

reducing this issue to high severity; profile destruction (closing the notification service) appears to be a precondition to triggering this issue

### sp...@google.com (2024-06-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$3,000 for report of moderately mitigated memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-05)

Congratulations! The reward amount for this issue was decided upon based on this issue being mitigated by profile destruction and closing the notifications service as well as the precondition to enable multiple non-default features to trigger this issue based on your demonstration of it, the non-minimized POC was also a part of reward consideration given the complexities with demonstrating this issue.
Thanks for your efforts and reporting this issue to us!

### zh...@gmail.com (2024-06-06)

Thank you very much, cheers 🍻

### pe...@google.com (2024-09-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/343302586)*
