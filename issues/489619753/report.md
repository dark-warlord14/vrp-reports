# heap-use-after-free in extensions::ChromeContentRulesRegistry::RemoveRulesImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [489619753](https://issues.chromium.org/issues/489619753) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2026-03-04 |
| **Bounty** | $5,000.00 |

## Description

```
=================================================================
==63616==ERROR: AddressSanitizer: heap-use-after-free on address 0x12170e631828 at pc 0x7ffa468cf5ba bp 0x00b79e3fd7e0 sp 0x00b79e3fd828
READ of size 8 at 0x12170e631828 thread T0
    #0 0x7ffa468cf5b9 in extensions::ChromeContentRulesRegistry::RemoveRulesImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\declarative_content\chrome_content_rules_registry.cc:363
    #1 0x7ffa43b8d764 in extensions::RulesRegistry::RemoveRules C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\rules_registry.cc:176
    #2 0x7ffa43b84299 in extensions::EventsEventRemoveRulesFunction::RunInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\declarative_api.cc:256
    #3 0x7ffa43b8229b in extensions::RulesFunction::Run C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\declarative_api.cc:193
    #4 0x7ffa43dddffa in ExtensionFunction::RunWithValidation C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function.cc:494
    #5 0x7ffa43dee30e in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:458
    #6 0x7ffa43def06d in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:248
    #7 0x7ffa43f60171 in extensions::ServiceWorkerHost::RequestWorker C:\b\s\w\ir\cache\builder\src\extensions\browser\service_worker\service_worker_host.cc:278
    #8 0x7ffa440ea7ad in extensions::mojom::ServiceWorkerHostStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\extensions\common\mojom\service_worker_host.mojom.cc:1648
    #9 0x7ffa43f638dc in extensions::mojom::ServiceWorkerHostStub<mojo::RawPtrImplRefTraits<extensions::mojom::ServiceWorkerHost> >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\extensions\common\mojom\service_worker_host.mojom.h:201
    #10 0x7ffa4baaa26d in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036
    #11 0x7ffa4baa703d in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #12 0x7ffa4bab09ae in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747
    #13 0x7ffa4ba91e61 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1204
    #14 0x7ffa4ba903de in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:790
    #15 0x7ffa4baa703d in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #16 0x7ffa4baceebe in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:568
    #17 0x7ffa4bad07b8 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:629
    #18 0x7ffa4bad1550 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(),base::WeakPtr<mojo::Connector> &&>,base::internal::BindState<1,1,0,void (mojo::Connector::*)(),base::WeakPtr<mojo::Connector> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982
    #19 0x7ffa4bd84f08 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229
    #20 0x7ffa4bd551e1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475
    #21 0x7ffa4bd54043 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #22 0x7ffa4bbdb82c in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:260
    #23 0x7ffa4bbd91e4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:87
    #24 0x7ffa4bd56f2f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650
    #25 0x7ffa4bdfc89c in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135
    #26 0x7ffa41097977 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1103
    #27 0x7ffa4109f779 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:151
    #28 0x7ffa4108ddf6 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:32
    #29 0x7ffa47982f6a in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:696
    #30 0x7ffa479865ec in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1320
    #31 0x7ffa47985c72 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1150
    #32 0x7ffa47979a1f in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358
    #33 0x7ffa4797a1c2 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371
    #34 0x7ffa377c2b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191
    #35 0x7ff601ef4807 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:204
    #36 0x7ff601ef2074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351
    #37 0x7ff6023ed91f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #38 0x7ffb9f6ae8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #39 0x7ffba07ac40b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

0x12170e631828 is located 8 bytes inside of 88-byte region [0x12170e631820,0x12170e631878)
freed by thread T0 here:
    #0 0x7ffab848f036 in operator delete+0x96 (C:\Users\Admin\Downloads\chrome-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005f036)
    #1 0x7ffa468cf23c in extensions::ChromeContentRulesRegistry::RemoveRulesImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\declarative_content\chrome_content_rules_registry.cc:363
    #2 0x7ffa43b8d764 in extensions::RulesRegistry::RemoveRules C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\rules_registry.cc:176
    #3 0x7ffa43b84299 in extensions::EventsEventRemoveRulesFunction::RunInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\declarative_api.cc:256
    #4 0x7ffa43b8229b in extensions::RulesFunction::Run C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\declarative_api.cc:193
    #5 0x7ffa43dddffa in ExtensionFunction::RunWithValidation C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function.cc:494
    #6 0x7ffa43dee30e in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:458
    #7 0x7ffa43def06d in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:248
    #8 0x7ffa43f60171 in extensions::ServiceWorkerHost::RequestWorker C:\b\s\w\ir\cache\builder\src\extensions\browser\service_worker\service_worker_host.cc:278
    #9 0x7ffa440ea7ad in extensions::mojom::ServiceWorkerHostStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\extensions\common\mojom\service_worker_host.mojom.cc:1648
    #10 0x7ffa43f638dc in extensions::mojom::ServiceWorkerHostStub<mojo::RawPtrImplRefTraits<extensions::mojom::ServiceWorkerHost> >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\extensions\common\mojom\service_worker_host.mojom.h:201
    #11 0x7ffa4baaa26d in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036
    #12 0x7ffa4baa703d in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #13 0x7ffa4bab09ae in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747
    #14 0x7ffa4ba91e61 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1204
    #15 0x7ffa4ba903de in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:790
    #16 0x7ffa4baa703d in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #17 0x7ffa4baceebe in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:568
    #18 0x7ffa4bad07b8 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:629
    #19 0x7ffa4bad1550 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(),base::WeakPtr<mojo::Connector> &&>,base::internal::BindState<1,1,0,void (mojo::Connector::*)(),base::WeakPtr<mojo::Connector> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982
    #20 0x7ffa4bd84f08 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229
    #21 0x7ffa4bd551e1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475
    #22 0x7ffa4bd54043 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #23 0x7ffa4bbdb82c in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:260
    #24 0x7ffa4bbd91e4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:87
    #25 0x7ffa4bd56f2f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650
    #26 0x7ffa4bdfc89c in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135
    #27 0x7ffa41097977 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1103

previously allocated by thread T0 here:
    #0 0x7ffab848e46f in operator new+0x8f (C:\Users\Admin\Downloads\chrome-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005e46f)
    #1 0x7ffa468d0615 in std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::pair<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,std::__Cr::unique_ptr<const extensions::ChromeContentRulesRegistry::ContentRule,std::__Cr::default_delete<const extensions::ChromeContentRulesRegistry::ContentRule> > >,std::__Cr::__map_value_compare<std::__Cr::pair<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,std::__Cr::pair<const std::__Cr::pair<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,std::__Cr::unique_ptr<const extensions::ChromeContentRulesRegistry::ContentRule,std::__Cr::default_delete<const extensions::ChromeContentRulesRegistry::ContentRule> > >,std::__Cr::less<std::__Cr::pair<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > > > >,std::__Cr::allocator<std::__Cr::pair<const std::__Cr::pair<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,std::__Cr::unique_ptr<const extensions::ChromeContentRulesRegistry::ContentRule,std::__Cr::default_delete<const extensions::ChromeContentRulesRegistry::ContentRule> > > > >::__insert_range_unique<std::__Cr::move_iterator<std::__Cr::__map_iterator<std::__Cr::__tree_iterator<std::__Cr::__value_type<std::__Cr::pair<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,std::__Cr::unique_ptr<const extensions::ChromeContentR C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree:1131
    #2 0x7ffa468cdce1 in extensions::ChromeContentRulesRegistry::AddRulesImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\declarative_content\chrome_content_rules_registry.cc:307
    #3 0x7ffa43b8b740 in extensions::RulesRegistry::AddRulesNoFill C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\rules_registry.cc:114
    #4 0x7ffa43b8ca41 in extensions::RulesRegistry::AddRulesInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\rules_registry.cc:159
    #5 0x7ffa43b8c70c in extensions::RulesRegistry::AddRules C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\rules_registry.cc:143
    #6 0x7ffa43b833bf in extensions::EventsEventAddRulesFunction::RunInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\declarative_api.cc:212
    #7 0x7ffa43b8229b in extensions::RulesFunction::Run C:\b\s\w\ir\cache\builder\src\extensions\browser\api\declarative\declarative_api.cc:193
    #8 0x7ffa43dddffa in ExtensionFunction::RunWithValidation C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function.cc:494
    #9 0x7ffa43dee30e in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:458
    #10 0x7ffa43def06d in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:248
    #11 0x7ffa43f60171 in extensions::ServiceWorkerHost::RequestWorker C:\b\s\w\ir\cache\builder\src\extensions\browser\service_worker\service_worker_host.cc:278
    #12 0x7ffa440ea7ad in extensions::mojom::ServiceWorkerHostStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\extensions\common\mojom\service_worker_host.mojom.cc:1648
    #13 0x7ffa43f638dc in extensions::mojom::ServiceWorkerHostStub<mojo::RawPtrImplRefTraits<extensions::mojom::ServiceWorkerHost> >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\extensions\common\mojom\service_worker_host.mojom.h:201
    #14 0x7ffa4baaa26d in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036
    #15 0x7ffa4baa703d in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #16 0x7ffa4bab09ae in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747
    #17 0x7ffa4ba91e61 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1204
    #18 0x7ffa4ba903de in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:790
    #19 0x7ffa4baa703d in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #20 0x7ffa4baceebe in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:568
    #21 0x7ffa4bad07b8 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:629
    #22 0x7ffa4bad1550 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(),base::WeakPtr<mojo::Connector> &&>,base::internal::BindState<1,1,0,void (mojo::Connector::*)(),base::WeakPtr<mojo::Connector> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982
    #23 0x7ffa4bd84f08 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229
    #24 0x7ffa4bd551e1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475
    #25 0x7ffa4bd54043 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #26 0x7ffa4bbdb82c in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:260
    #27 0x7ffa4bbd91e4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:87

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\declarative_content\chrome_content_rules_registry.cc:363 in extensions::ChromeContentRulesRegistry::RemoveRulesImpl
Shadow bytes around the buggy address:
  0x12170e631580: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12170e631600: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12170e631680: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12170e631700: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x12170e631780: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
=>0x12170e631800: fa fa f7 fa fd[fd]fd fd fd fd fd fd fd fd fd fa
  0x12170e631880: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x12170e631900: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12170e631980: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12170e631a00: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x12170e631a80: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
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

==63616==ADDITIONAL INFO

==63616==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffa4bad11d2 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:612
    #1 0x7ffa4bad11d2 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:612
    #2 0x7ffa4c3a823b in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:103


Command line: `"C:\Users\Admin\Downloads\chrome-asan\chrome.exe" --disable-extensions-except="C:\Users\Admin\Downloads\Extension" --load-extension="C:\Users\Admin\Downloads\Extension" --user-data-dir="C:\\Users\\Admin\\AppData\\Local\\Temp\\tmpuzg50refsdsddsdd" --flag-switches-begin --flag-switches-end --file-url-path-alias="/gen=C:\Users\Admin\Downloads\chrome-asan\gen"`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==63616==END OF ADDITIONAL INFO

==63616==ABORTING


```
#### VERSION

Version 147.0.7710.0 (Developer Build) (64-bit)

#### REPRODUCTION CASE

Build: [asan-win32-release\_x64-1591961](https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1591961.zip?generation=1772257263596065&alt=media)

> Note: Download the attached files **background.js** and **manifest.json** into a folder named **Extension** and load them using the command below.

Run: `.\chrome-asan\chrome.exe --disable-extensions-except=C:\Users\Admin\Downloads\Extension --load-extension=C:\Users\Admin\Downloads\Extension`

---

Reporter credit: Shaheen Fazim

## Attachments

- [background.js](attachments/background.js) (text/javascript, 899 B)
- [manifest.json](attachments/manifest.json) (application/json, 368 B)

## Timeline

### fa...@gmail.com (2026-03-04)

# Root Cause Analysis: Heap-Use-After-Free in `extensions::ChromeContentRulesRegistry::RemoveRulesImpl`

---

## Summary

[RemoveRulesImpl](javascript:void(0);) does not deduplicate the incoming `rule_identifiers` list before processing. When the same rule ID appears multiple times, the function looks up the **same `std::map` iterator** multiple times and appends it to a vector. It then iterates that vector calling `content_rules_.erase(it)` the first erase frees the underlying map node (and the `unique_ptr<ContentRule>` it owns), and every subsequent erase on the same (now-dangling) iterator is a **use-after-free**.

---

## Vulnerable Code (Primary)

[RemoveRulesImpl](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry.cc;l=319-367;drc=ec69d4ae24eaefabaf8e609a0a6d4d818b75d7f5) — the function that owns the bug:

```
std::string ChromeContentRulesRegistry::RemoveRulesImpl(
    const ExtensionId& extension_id,
    const std::vector<std::string>& rule_identifiers) {
  EvaluationScope evaluation_scope(this, IGNORE_REQUESTS);

  std::vector<RulesMap::iterator> rules_to_erase;          // ← (A) collects iterators
  std::vector<const void*> predicate_groups_to_stop_tracking;

  for (const std::string& id : rule_identifiers) {         // ← (B) iterates ALL IDs, including duplicates
    auto content_rules_entry =
        content_rules_.find(std::make_pair(extension_id, id));
    if (content_rules_entry == content_rules_.end()) {
      continue;  // skip unknown rules — but does NOT skip already-collected IDs
    }

    const ContentRule* rule = content_rules_entry->second.get();

    // Remove the ContentRule from active_rules_.
    for (auto& tab_rules_pair : active_rules_) {
      if (tab_rules_pair.second.contains(rule)) {
        /* ... revert actions ... */
        tab_rules_pair.second.erase(rule);
      }
    }

    rules_to_erase.push_back(content_rules_entry);         // ← (C) SAME iterator pushed AGAIN for duplicates
    predicate_groups_to_stop_tracking.push_back(rule);      //   dangling ptr after first erase
  }

  for (const auto& evaluator : evaluators_)
    evaluator->StopTrackingPredicates(predicate_groups_to_stop_tracking);

  for (auto it : rules_to_erase) {   // ← (D) erases the same iterator TWICE
    content_rules_.erase(it);         //   1st erase: frees the map node + unique_ptr<ContentRule>
  }                                   //   2nd erase: use-after-free on the freed node

  return std::string();
}

```

[Line 362-363](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry.cc;l=362-363;drc=ec69d4ae24eaefabaf8e609a0a6d4d818b75d7f5) is the exact crash site. `content_rules_.erase(it)` is called with a **dangling iterator** — the map node it pointed to was already freed by the previous iteration.

The [find()](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry.cc;l=331-332;drc=ec69d4ae24eaefabaf8e609a0a6d4d818b75d7f5) at line 331 looks up the rule in `content_rules_` but the rule is only removed from `content_rules_` at the very end (step D). So when the loop encounters `'testrule'` a second time, the entry **still exists** in the map, and the same iterator is pushed to `rules_to_erase` again.

---

## Vulnerable Caller (No Validation)

[RulesRegistry::RemoveRules](https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/declarative/rules_registry.cc;l=163-189;drc=ec69d4ae24eaefabaf8e609a0a6d4d818b75d7f5) passes duplicates through without any deduplication:

```
std::string RulesRegistry::RemoveRules(
    const ExtensionId& extension_id,
    const std::vector<std::string>& rule_identifiers) {
  // ...
  std::string error = RemoveRulesImpl(extension_id, rule_identifiers);  // ← duplicates forwarded as-is
  // ...
  for (auto i = rule_identifiers.cbegin(); i != rule_identifiers.cend(); ++i) {
    RulesDictionaryKey lookup_key(extension_id, *i);
    rules_.erase(lookup_key);   // ← erase-by-key is safe (no-op if missing)
  }
  // ...
}

```

The parent's own `rules_` map uses **erase-by-key** which is safe for duplicates. But [RemoveRulesImpl](javascript:void(0);) uses **erase-by-iterator**, which is UB if the iterator is already invalidated.

---

## Suggested Fix

Deduplicate `rule_identifiers` at the top of [RemoveRulesImpl](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry.cc;l=319;drc=ec69d4ae24eaefabaf8e609a0a6d4d818b75d7f5) before processing begins. Convert the incoming `std::vector<std::string>` into a `base::flat_set<std::string>` (or a `std::set`) and iterate over the deduplicated set instead.

This ensures each rule ID is looked up, reverted, tracked-for-stop, and erased **exactly once**, eliminating the possibility of collecting the same iterator twice. The same deduplication should also be applied in [RulesRegistry::RemoveRules](https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/declarative/rules_registry.cc;l=163;drc=ec69d4ae24eaefabaf8e609a0a6d4d818b75d7f5) as defense-in-depth so that no [RemoveRulesImpl](javascript:void(0);) override in any subclass can be exposed to duplicate IDs.

### ct...@google.com (2026-03-06)

Thanks for the report. I can repro on macOS Dev ASAN and Stable ASAN

```
==84603==ERROR: AddressSanitizer: heap-use-after-free on address 0x608000556e28 at pc 0x00030da58aa4 bp 0x00016bc642f0 sp 0x00016bc642e8
READ of size 8 at 0x608000556e28 thread T0
Chromium Helper(84624,0x2077fa240) malloc: nano zone abandoned due to inability to reserve vm space.
==84603==WARNING: invalid path to external symbolizer!
==84603==WARNING: Failed to use and restart external symbolizer!
    #0 0x00030da58aa0 in extensions::ChromeContentRulesRegistry::RemoveRulesImpl(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>> const&)+0xef0 (/Users/cthomp/scratch/asan-dev/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7703.0/Chromium Framework:arm64+0xda58aa0)
    #1 0x00030aea2b44 in extensions::RulesRegistry::RemoveRules(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>> const&)+0x45c (/Users/cthomp/scratch/asan-dev/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7703.0/Chromium Framework:arm64+0xaea2b44)
    #2 0x00030ae994b0 in extensions::EventsEventRemoveRulesFunction::RunInternal()+0x198 (/Users/cthomp/scratch/asan-dev/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7703.0/Chromium Framework:arm64+0xae994b0)
    #3 0x00030ae9758c in extensions::RulesFunction::Run()+0x4a0 (/Users/cthomp/scratch/asan-dev/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7703.0/Chromium Framework:arm64+0xae9758c)

```

This is a browser UAF but requires a malicious extension, so setting Sev-High (S1).

Passing this to Extensions team.

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  Andrea Orru [andreaorru@chromium.org](mailto:andreaorru@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7644438>

[Extensions] Deduplicate rule identifiers in RemoveRules

---


Expand for full commit details
```
     
    When removing declarative content rules, a given list of rule 
    identifiers may contain duplicates. Both RulesRegistry::RemoveRules and 
    ChromeContentRulesRegistry::RemoveRulesImpl previously processed the 
    incoming rule_identifiers list without deduplicating it. 
     
    When the same rule ID appears multiple times, the function looks up the 
    same map iterator multiple times, and the second erase call on the same 
    (now-dangling) iterator results in a heap-use-after-free. 
     
    This CL creates a deduplicated vector to ensure each rule ID is 
    processed and erased exactly once, preventing memory corruption. 
     
    Fixed: 489619753 
    Change-Id: Ib23e3b9771fdd64d3e1342ddc8d097d5ebc0cc04 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644438 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Andrea Orru <andreaorru@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1595764}

```

---

Files:

- M `chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry.cc`
- M `chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry_unittest.cc`
- M `extensions/browser/api/declarative/rules_registry.cc`

---

Hash: [98a65b0c6572e8263e7d5a9cf91e9cba5d4d1350](https://chromiumdash.appspot.com/commit/98a65b0c6572e8263e7d5a9cf91e9cba5d4d1350)  

Date: Fri Mar 6 23:50:15 2026


---

### ch...@google.com (2026-03-07)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-07)

Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1595764) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1595764) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-08)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-08)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-03-09)

No crashes in Canary. Approving merge to M146. We don't plan more releases for M145, so removing that label.

### ch...@google.com (2026-03-13)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### an...@chromium.org (2026-03-13)

1. Yes
2. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7644438>
3. Yes
4. No
5. No

### ch...@google.com (2026-03-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-13)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Andrea Orru [andreaorru@chromium.org](mailto:andreaorru@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7666898>

[Extensions] Deduplicate rule identifiers in RemoveRules

---


Expand for full commit details
```
     
    When removing declarative content rules, a given list of rule 
    identifiers may contain duplicates. Both RulesRegistry::RemoveRules and 
    ChromeContentRulesRegistry::RemoveRulesImpl previously processed the 
    incoming rule_identifiers list without deduplicating it. 
     
    When the same rule ID appears multiple times, the function looks up the 
    same map iterator multiple times, and the second erase call on the same 
    (now-dangling) iterator results in a heap-use-after-free. 
     
    This CL creates a deduplicated vector to ensure each rule ID is 
    processed and erased exactly once, preventing memory corruption. 
     
    (cherry picked from commit 98a65b0c6572e8263e7d5a9cf91e9cba5d4d1350) 
     
    Fixed: 489619753 
    Change-Id: Ib23e3b9771fdd64d3e1342ddc8d097d5ebc0cc04 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644438 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Andrea Orru <andreaorru@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1595764} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666898 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Andrea Orru <andreaorru@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2515} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry.cc`
- M `chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry_unittest.cc`
- M `extensions/browser/api/declarative/rules_registry.cc`

---

Hash: [496bcac938c02b5a7eaafd11c188ebf8c61ef4fd](https://chromiumdash.appspot.com/commit/496bcac938c02b5a7eaafd11c188ebf8c61ef4fd)  

Date: Fri Mar 13 19:00:04 2026


---

### pe...@google.com (2026-03-13)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-17)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7665862
2. Low - There was no conflict.
3. 146
4. Yes, the places where the fix is modified have existed for many years ago [1][2][3]. Thus, I think M138 also has the issue.

[1] https://codereview.chromium.org/49693003
[2] https://codereview.chromium.org/1158693006
[3] https://codereview.chromium.org/49693003

### an...@google.com (2026-03-27)

Approved for LTS 138.

### dx...@google.com (2026-04-03)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Andrea Orru [andreaorru@chromium.org](mailto:andreaorru@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7665862>

[M138-LTS][Extensions] Deduplicate rule identifiers in RemoveRules

---


Expand for full commit details
```
     
    When removing declarative content rules, a given list of rule 
    identifiers may contain duplicates. Both RulesRegistry::RemoveRules and 
    ChromeContentRulesRegistry::RemoveRulesImpl previously processed the 
    incoming rule_identifiers list without deduplicating it. 
     
    When the same rule ID appears multiple times, the function looks up the 
    same map iterator multiple times, and the second erase call on the same 
    (now-dangling) iterator results in a heap-use-after-free. 
     
    This CL creates a deduplicated vector to ensure each rule ID is 
    processed and erased exactly once, preventing memory corruption. 
     
    (cherry picked from commit 98a65b0c6572e8263e7d5a9cf91e9cba5d4d1350) 
     
    (cherry picked from commit 496bcac938c02b5a7eaafd11c188ebf8c61ef4fd) 
     
    Fixed: 489619753 
    Change-Id: Ib23e3b9771fdd64d3e1342ddc8d097d5ebc0cc04 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644438 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Andrea Orru <andreaorru@chromium.org> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1595764} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666898 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Andrea Orru <andreaorru@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Original-Commit-Position: refs/branch-heads/7680@{#2515} 
    Cr-Original-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665862 
    Reviewed-by: Andrea Orru <andreaorru@chromium.org> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3519} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry.cc`
- M `chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry_unittest.cc`
- M `extensions/browser/api/declarative/rules_registry.cc`

---

Hash: [ddbade8f294a12a8f6331cc20a14478e9a97f646](https://chromiumdash.appspot.com/commit/ddbade8f294a12a8f6331cc20a14478e9a97f646)  

Date: Fri Apr 3 02:04:27 2026


---

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Mildly mitigated (non-sandboxed) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-11)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7825629>
2. Low - There was no conflict.
3. 146
4. Yes, the bug has existed for a long year.

### dx...@google.com (2026-05-18)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Andrea Orru [andreaorru@chromium.org](mailto:andreaorru@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7825629>

[M144-LTS][Extensions] Deduplicate rule identifiers in RemoveRules

---


Expand for full commit details
```
     
    When removing declarative content rules, a given list of rule 
    identifiers may contain duplicates. Both RulesRegistry::RemoveRules and 
    ChromeContentRulesRegistry::RemoveRulesImpl previously processed the 
    incoming rule_identifiers list without deduplicating it. 
     
    When the same rule ID appears multiple times, the function looks up the 
    same map iterator multiple times, and the second erase call on the same 
    (now-dangling) iterator results in a heap-use-after-free. 
     
    This CL creates a deduplicated vector to ensure each rule ID is 
    processed and erased exactly once, preventing memory corruption. 
     
    (cherry picked from commit 98a65b0c6572e8263e7d5a9cf91e9cba5d4d1350) 
     
    Fixed: 489619753 
    Change-Id: Ib23e3b9771fdd64d3e1342ddc8d097d5ebc0cc04 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644438 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Andrea Orru <andreaorru@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1595764} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7825629 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Reviewed-by: Andrea Orru <andreaorru@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4866} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry.cc`
- M `chrome/browser/extensions/api/declarative_content/chrome_content_rules_registry_unittest.cc`
- M `extensions/browser/api/declarative/rules_registry.cc`

---

Hash: [35e358098a037ef9b85605ac47e5f33c61284e41](https://chromiumdash.appspot.com/commit/35e358098a037ef9b85605ac47e5f33c61284e41)  

Date: Mon May 18 05:48:06 2026


---

### ch...@google.com (2026-06-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489619753)*
