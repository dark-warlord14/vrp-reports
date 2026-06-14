# use-after-poison in apps::AppShimManager::OnShimProcessConnectedForRegisterOnly

| Field | Value |
|-------|-------|
| **Issue ID** | [348793134](https://issues.chromium.org/issues/348793134) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Mac |
| **Reporter** | ha...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2024-06-22 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

I dont't known this vuln's root cause.but I provice the video to help reproduce


VERSION
Chrome Version: [x.x.x.x] + [stable, beta, or dev]
Operating System: [Please indicate OS, version, and service pack level]

REPRODUCTION CASE
1.first you need install the app
2.after install the app,./out/Default/Chromium.app/Contents/MacOS/Chromium  --enable-features=AppShimNotificationAttribution --user-data-dir=/xxxxx/tmp http://127.0.0.1:8080/
3. wait 1s and click the button




=================================================================
==28040==ERROR: AddressSanitizer: use-after-poison on address 0x606000940150 at pc 0x00011e24bbe0 bp 0x00016b3c85a0 sp 0x00016b3c8598
READ of size 8 at 0x606000940150 thread T0
==28040==WARNING: invalid path to external symbolizer!
==28040==WARNING: Failed to use and restart external symbolizer!
    #0 0x11e24bbdc in apps::AppShimManager::OnShimProcessConnectedForRegisterOnly(std::__Cr::unique_ptr<AppShimHostBootstrap, std::__Cr::default_delete<AppShimHostBootstrap>>)+0x2a8 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x225fbdc)
    #1 0x11e24d01c in apps::AppShimManager::OnShimProcessConnected(std::__Cr::unique_ptr<AppShimHostBootstrap, std::__Cr::default_delete<AppShimHostBootstrap>>)+0x60c (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x226101c)
    #2 0x11e23f374 in AppShimHostBootstrap::OnShimConnected(mojo::PendingReceiver<chrome::mojom::AppShimHost>, mojo::StructPtr<chrome::mojom::AppShimInfo>, base::OnceCallback<void (chrome::mojom::AppShimLaunchResult, variations::VariationsCommandLine, mojo::PendingReceiver<chrome::mojom::AppShim>)>)+0x1dc (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2253374)
    #3 0x11d10ebfc in chrome::mojom::AppShimHostBootstrapStubDispatch::AcceptWithResponder(chrome::mojom::AppShimHostBootstrap*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>)+0x364 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x1122bfc)
    #4 0x10614ac6c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x768 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x22c6c)
    #5 0x10615ec0c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x36c0c)
    #6 0x10614f068 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x154 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x27068)
    #7 0x10616a554 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x77c (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x42554)
    #8 0x106168bac in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x418 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x40bac)
    #9 0x10615ec0c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x36c0c)
    #10 0x1061392f4 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x378 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x112f4)
    #11 0x10613abd0 in mojo::Connector::ReadAllAvailableMessages()+0x23c (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x12bd0)
    #12 0x10613a6a8 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x126a8)
    #13 0x10613c85c in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x1485c)
    #14 0x10613c278 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x154 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x14278)
    #15 0x10613c04c in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x1404c)
    #16 0x1060c5400 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x19400)
    #17 0x1060c4e08 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x18e08)
    #18 0x1060c5d28 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x19d28)
    #19 0x10712f9fc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1879fc)
    #20 0x10719982c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f182c)
    #21 0x107198c98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f0c98)
    #22 0x1072e0674 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c4 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x338674)
    #23 0x1072cef90 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x326f90)
    #24 0x1072dec18 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x336c18)
    #25 0x195cbe4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)
    #26 0x4e47800195cbe468  (<unknown module>)
    #27 0xd607800195cbe1d8  (<unknown module>)
    #28 0xf15d000195cbcdc4  (<unknown module>)
    #29 0x177a000195cbc430  (<unknown module>)
    #30 0xc008001a0460198  (<unknown module>)
    #31 0x52028001a045ffd4  (<unknown module>)
    #32 0x235c0001a045fd2c  (<unknown module>)
    #33 0xd76700019951bd64  (<unknown module>)
    #34 0x608800199d11804  (<unknown module>)
    #35 0xee4e80011ee50554  (<unknown module>)
    #36 0x1072cef90 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x326f90)
    #37 0x11ee50218 in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x1a4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2e64218)
    #38 0x19950f098 in -[NSApplication run]+0x1d8 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2d098)
    #39 0x13560001072e2590  (<unknown module>)
    #40 0x1072dd834 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x28c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x335834)
    #41 0x10719addc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f2ddc)
    #42 0x1070c4870 in base::RunLoop::Run(base::Location const&)+0x438 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x11c870)
    #43 0x1122460f4 in content::BrowserMainLoop::RunMainMessageLoop()+0x178 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xd420f4)
    #44 0x11224c400 in content::BrowserMainRunnerImpl::Run()+0x30 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xd48400)
    #45 0x11223eb70 in content::BrowserMain(content::MainFunctionParams)+0x1f8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xd3ab70)
    #46 0x1145dc7e4 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*)+0x1b0 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30d87e4)
    #47 0x1145df178 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x8e4 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30db178)
    #48 0x1145de688 in content::ContentMainRunnerImpl::Run()+0x454 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30da688)
    #49 0x1145daa2c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x478 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30d6a2c)
    #50 0x1145db370 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30d7370)
    #51 0x11bff6f30 in ChromeMain+0x374 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0xaf30)
    #52 0x104a34b80 in main+0x1f8 (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000b80)
    #53 0x1958560dc  (<unknown module>)
    #54 0x3b4dfffffffffffc  (<unknown module>)

0x606000940150 is located 16 bytes before 64-byte region [0x606000940160,0x6060009401a0)
allocated by thread T0 here:
    #0 0x1055ec11c in __sanitizer_finish_switch_fiber+0x61c (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x6011c)
    #1 0x11e267420 in std::__Cr::pair<std::__Cr::__tree_iterator<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<apps::AppShimManager::AppState, std::__Cr::default_delete<apps::AppShimManager::AppState>>>, std::__Cr::__tree_node<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<apps::AppShimManager::AppState, std::__Cr::default_delete<apps::AppShimManager::AppState>>>, void*>*, long>, bool> std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<apps::AppShimManager::AppState, std::__Cr::default_delete<apps::AppShimManager::AppState>>>, std::__Cr::__map_value_compare<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<apps::AppShimManager::AppState, std::__Cr::default_delete<apps::AppShimManager::AppState>>>, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, true>, std::__Cr::allocator<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<apps::AppShimManager::AppState, std::__Cr::default_delete<apps::AppShimManager::AppState>>>>>::__emplace_unique_key_args<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<apps::AppShimManager::AppState, std::__Cr::default_delete<apps::AppShimManager::AppState>>>>(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<apps::AppShimManager::AppState, std::__Cr::default_delete<apps::AppShimManager::AppState>>>&&)+0x60 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x227b420)
    #2 0x11e24ab30 in apps::AppShimManager::GetOrCreateProfileState(Profile*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&)+0x2d4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x225eb30)
    #3 0x11e249784 in apps::AppShimManager::LaunchShimInBackgroundMode(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::OnceCallback<void (AppShimHost*)>)+0x1c0 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x225d784)
    #4 0x11e24a258 in apps::AppShimManager::ShowNotificationPermissionRequest(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::OnceCallback<void (mac_notifications::mojom::RequestPermissionResult)>)+0x4b4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x225e258)
    #5 0x124734370 in PermissionPromptNotificationsMac::ShowPrompt()+0x208 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x8748370)
    #6 0x124735038 in void base::internal::Invoker<base::internal::FunctorTraits<void (PermissionPromptNotificationsMac::*&&)(), base::WeakPtr<PermissionPromptNotificationsMac>&&>, base::internal::BindState<true, true, false, void (PermissionPromptNotificationsMac::*)(), base::WeakPtr<PermissionPromptNotificationsMac>>, void ()>::RunImpl<void (PermissionPromptNotificationsMac::*)(), std::__Cr::tuple<base::WeakPtr<PermissionPromptNotificationsMac>>, 0ul>(void (PermissionPromptNotificationsMac::*&&)(), std::__Cr::tuple<base::WeakPtr<PermissionPromptNotificationsMac>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x16c (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x8749038)
    #7 0x10712f9fc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1879fc)
    #8 0x10719982c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f182c)
    #9 0x107198c98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f0c98)
    #10 0x1072e0674 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c4 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x338674)
    #11 0x1072cef90 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x326f90)
    #12 0x1072dec18 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x336c18)
    #13 0x195cbe4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)
    #14 0x4e47800195cbe468  (<unknown module>)
    #15 0xd607800195cbe1d8  (<unknown module>)
    #16 0xf15d000195cbcdc4  (<unknown module>)
    #17 0x177a000195cbc430  (<unknown module>)
    #18 0xc008001a0460198  (<unknown module>)
    #19 0x52028001a045ffd4  (<unknown module>)
    #20 0x235c0001a045fd2c  (<unknown module>)
    #21 0xd76700019951bd64  (<unknown module>)
    #22 0x608800199d11804  (<unknown module>)
    #23 0xee4e80011ee50554  (<unknown module>)
    #24 0x1072cef90 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x326f90)
    #25 0x11ee50218 in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x1a4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2e64218)
    #26 0x19950f098 in -[NSApplication run]+0x1d8 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2d098)
    #27 0x13560001072e2590  (<unknown module>)
    #28 0x1072dd834 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x28c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x335834)
    #29 0x10719addc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f2ddc)

SUMMARY: AddressSanitizer: use-after-poison (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x225fbdc) in apps::AppShimManager::OnShimProcessConnectedForRegisterOnly(std::__Cr::unique_ptr<AppShimHostBootstrap, std::__Cr::default_delete<AppShimHostBootstrap>>)+0x2a8
Shadow bytes around the buggy address:
  0x60600093fe80: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fd
  0x60600093ff00: fa fa f7 fa 00 00 00 00 00 00 00 00 fa fa f7 fa
  0x60600093ff80: 00 00 00 00 00 00 00 00 fa fa f7 fa fd fd fd fd
  0x606000940000: fd fd fd fd fa fa f7 fa 00 00 00 00 00 00 00 fa
  0x606000940080: fa fa f7 fa 00 00 00 00 00 00 00 00 fa fa f7 fa
=>0x606000940100: 00 00 00 00 00 00 00 00 fa fa[f7]fa 00 00 00 00
  0x606000940180: 00 00 00 00 fa fa f7 fa fd fd fd fd fd fd fd fa
  0x606000940200: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
  0x606000940280: fd fd fd fd fd fd fd fd fa fa f7 fa 00 00 00 00
  0x606000940300: 00 00 00 fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x606000940380: fa fa f7 fa 00 00 00 00 00 00 00 fa fa fa f7 fa
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

==28040==ADDITIONAL INFO

==28040==Note: Please include this section with the ASan report.
Task trace:
    #0 0x1060c57e8 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x248 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x197e8)


==28040==END OF ADDITIONAL INFO





Note

This vulnerability should be P0/S0, please refer to issues 40059774

## Attachments

- [repro.mov](attachments/repro.mov) (video/quicktime, 14.3 MB)
- [pwamp.zip](attachments/pwamp.zip) (application/zip, 13.7 MB)
- [index.html](attachments/index.html) (text/html, 1.7 KB)

## Timeline

### ri...@google.com (2024-06-24)

Thanks for reporting, can you provide more information on what is executed from clicking the button? Also, please attach the POC files individually instead of a zip.

### ha...@gmail.com (2024-06-24)

hi,see video.The PoC file is big so I upload the zip file.You also can download <https://github.com/MicrosoftEdge/Demos/tree/main/pwamp>. and replace the index.html file.

### pe...@google.com (2024-06-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### ri...@google.com (2024-06-25)

Hi [mek@chromium.org](mailto:mek@chromium.org), I think this is similar work to your recent change - [crrev.com/c/5365944](https://crrev.com/c/5365944). Could you PTAL

### ri...@google.com (2024-06-25)

@reporter, which Chrome version are you using to reproduce?

### ha...@gmail.com (2024-06-25)

test ASAN version 128.0.6541.0

### pe...@google.com (2024-06-25)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2024-06-25)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### me...@chromium.org (2024-06-25)

The relevant part of the repro here appears to be that the repro page:

- requests notification permission
- and shortly after (while the permission request is pending/the app shim is still in the process of starting up) closes itself

While I haven't been able to repro it myself, I have been able to put together a unit test that replicates something that does result in very similar ASAN output. To get this to trigger the timing of when the page closes has to be quite precise, to make sure that not this happens after the permission request is triggered and the app shims has started launching, but before the app shim has finished launching. And additionally not only the browser has to be closed, but the entire Profile instance has to be deleted as well which takes a bit of time after the browser has closed.

While we could try to make sure to keep the profile alive while the permission request is pending, to make sure we can process the response to a permission request in this situation, that wouldn't work since the permission infrastructure is tied to the specific browser/web contents anyway, so as soon as the browser is closed we can't do anything with the response to the permission request anymore. So we just need to handle the case of the profile being unloaded on the app shim manager side, which should fix this crash.

### ha...@gmail.com (2024-06-25)

Thank you for your detailed analysis. I am a little confused that I just closed the tab page and did not close the entire browser. Will this also lead to profile deletion, or is it caused by the destruction of web contents?

### me...@chromium.org (2024-06-25)

"Browser" in the chrome code refers to a window. And closing the window, when it is the last one for a profile, will cause the profile to be unloaded if there is nothing else keeping the profile alive in memory.

### ha...@gmail.com (2024-06-25)

But I just closed a tab page, and I opened two pages at the same time, index.html and about:blank.Crash will also happen
./out/Default/Chromium.app/Contents/MacOS/Chromium --enable-features=AppShimNotificationAttribution --user-data-dir=/xxxxx/tmp <http://127.0.0.1:8080/> about:blank

### ap...@google.com (2024-06-26)

Project: chromium/src
Branch: main

commit 701a2e788ee872e9809c7d2a0fc9b7b95435132a
Author: Marijn Kruisselbrink <mek@chromium.org>
Date:   Wed Jun 26 16:33:20 2024

    Speculative fix use after poison in AppShimManager.
    
    OnShimProcessConnectedForRegisterOnly assumed that (for multi-profile
    apps) AppState::profiles would never be empty if we have a valid
    AppState. But this is not a correct assumption, as there are some
    edge cases where an AppState might be kept alive while profiles (i.e.
    the list of profiles that have open windows for the app) is empty.
    The current main case being when the app shim has a pending notification
    permission request.
    
    Bug: 348793134
    Change-Id: I205fa965399f0e9b437da46453b6c40b3e84e328
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5653582
    Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
    Reviewed-by: Daniel Murphy <dmurph@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1319826}

M       chrome/browser/apps/app_shim/app_shim_manager_mac.cc
M       chrome/browser/apps/app_shim/app_shim_manager_mac_unittest.cc

https://chromium-review.googlesource.com/5653582


### am...@chromium.org (2024-07-01)

updating as SI-None as this issue is specific to AppShimNotificationAttribution which is not enabled by default

### sp...@google.com (2024-07-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$2,000 for report of highly mitigated memory corruption in a non-sandboxed process, mitigated by precondition to install a malicious application, user gesture, and profile destruction 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-03)

Congratulations on another one. Thank you for reporting this issue to us!

### pe...@google.com (2024-10-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/348793134)*
