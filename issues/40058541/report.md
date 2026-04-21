# Security: heap-use-after-free in TemplateURLFetcher::RequestDelegate::OnTemplateURLParsed 

| Field | Value |
|-------|-------|
| **Issue ID** | [40058541](https://issues.chromium.org/issues/40058541) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Search |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2022-01-21 |
| **Bounty** | $7,000.00 |

## Description


When #1278322 was fixed, I found another vulnerability, which should have existed before, not introduced later 


[0] https://source.chromium.org/chromium/chromium/src/+/main:components/search_engines/template_url_fetcher.h;l=77
  std::vector<std::unique_ptr<RequestDelegate>> requests_;  //RequestDelegate is owned by TemplateURLFetcher ,while TemplateURLFetcher destroyed,RequestDelegate will be free

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/search_engines/template_url_fetcher.cc;l=190;
......
  TemplateURLParser::Parse(
      &fetcher_->template_url_service_->search_terms_data(),
      *response_body.get(), TemplateURLParser::ParameterFilter(),
      base::BindOnce(&RequestDelegate::OnTemplateURLParsed,
                     base::Unretained(this)));    //bind callback ,but RequestDelegate was destroyed
.......


reproduce step:
1.out\Default\chrome http://www.baidu.com/
2.wait 2 sec and then close the window immediately 
3. UAF trigger


=================================================================
==17236==ERROR: AddressSanitizer: heap-use-after-free on address 0x11f4db1324d0 at pc 0x7ffc1649cfe5 bp 0x0092c2df9660 sp 0x0092c2df96a8
READ of size 8 at 0x11f4db1324d0 thread T0
    #0 0x7ffc1649cfe4 in std::__1::unique_ptr<TemplateURL,std::__1::default_delete<TemplateURL> >::reset E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:312
    #1 0x7ffc18d30312 in TemplateURLFetcher::RequestDelegate::OnTemplateURLParsed E:\src\chromium\src\components\search_engines\template_url_fetcher.cc:152
    #2 0x7ffc18d32054 in base::internal::Invoker<base::internal::BindState<void (TemplateURLFetcher::RequestDelegate::*)(std::__1::unique_ptr<TemplateURL,std::__1::default_delete<TemplateURL> >),base::internal::UnretainedWrapper<TemplateURLFetcher::RequestDelegate> >,void (std::__1::unique_ptr<TemplateURL,std::__1::default_delete<TemplateURL> >)>::RunOnce E:\src\chromium\src\base\bind_internal.h:741
    #3 0x7ffc1a5988a0 in base::OnceCallback<void (std::__1::unique_ptr<TemplateURL,std::__1::default_delete<TemplateURL> >)>::Run E:\src\chromium\src\base\callback.h:142
    #4 0x7ffc1a59740a in `anonymous namespace'::SafeTemplateURLParser::OnXmlParseComplete E:\src\chromium\src\components\search_engines\template_url_parser.cc:225
    #5 0x7ffc1a599207 in base::internal::Invoker<base::internal::BindState<void ((anonymous namespace)::SafeTemplateURLParser::*)(data_decoder::DataDecoder::ResultOrError<base::Value>),std::__1::unique_ptr<(anonymous namespace)::SafeTemplateURLParser,std::__1::default_delete<(anonymous namespace)::SafeTemplateURLParser> > >,void (data_decoder::DataDecoder::ResultOrError<base::Value>)>::RunOnce E:\src\chromium\src\base\bind_internal.h:741
    #6 0x7ffc1218d067 in base::internal::Invoker<base::internal::BindState<`lambda at ../../services/data_decoder/public/cpp/data_decoder.cc:261:16',std::__1::unique_ptr<data_decoder::DataDecoder,std::__1::default_delete<data_decoder::DataDecoder> >,base::OnceCallback<void (data_decoder::DataDecoder::ResultOrError<base::Value>)> >,void (data_decoder::DataDecoder::ResultOrError<base::Value>)>::RunOnce E:\src\chromium\src\base\bind_internal.h:741
    #7 0x7ffc121877fb in data_decoder::`anonymous namespace'::ValueParseRequest<data_decoder::mojom::XmlParser,base::Value>::OnServiceValueOrError E:\src\chromium\src\services\data_decoder\public\cpp\data_decoder.cc:91
    #8 0x7ffc1218cd7d in base::internal::Invoker<base::internal::BindState<void (data_decoder::(anonymous namespace)::ValueParseRequest<data_decoder::mojom::XmlParser,base::Value>::*)(absl::optional<base::Value>, const absl::optional<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > > &),scoped_refptr<data_decoder::(anonymous namespace)::ValueParseRequest<data_decoder::mojom::XmlParser,base::Value> > >,void (absl::optional<base::Value>, const absl::optional<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > > &)>::RunOnce E:\src\chromium\src\base\bind_internal.h:741
    #9 0x7ffc121b2a31 in base::OnceCallback<void (absl::optional<base::Value>, const absl::optional<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > > &)>::Run E:\src\chromium\src\base\callback.h:142
    #10 0x7ffc121b8a0d in data_decoder::mojom::XmlParser_Parse_ForwardToCallback::Accept E:\src\chromium\src\out\Default\gen\services\data_decoder\public\mojom\xml_parser.mojom.cc:205
    #11 0x7ffc6fe1aa14 in mojo::InterfaceEndpointClient::HandleValidatedMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:896
    #12 0x7ffc6fe2ae18 in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #13 0x7ffc6fe1e4ec in mojo::InterfaceEndpointClient::HandleIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:658
    #14 0x7ffc6fe37ad2 in mojo::internal::MultiplexRouter::ProcessIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1104
    #15 0x7ffc6fe36827 in mojo::internal::MultiplexRouter::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:724
    #16 0x7ffc6fe2ae18 in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #17 0x7ffc6fe09ba1 in mojo::Connector::DispatchMessageW E:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:556
    #18 0x7ffc6fe0b4fa in mojo::Connector::ReadAllAvailableMessages E:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:614
    #19 0x7ffc7bcf4559 in mojo::SimpleWatcher::OnHandleReady E:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:278
    #20 0x7ffc5cb85eb4 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task_annotator.cc:135
    #21 0x7ffc5cbd8379 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #22 0x7ffc5cbd7a48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #23 0x7ffc5ccd5e76 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message_loop\message_pump_win.cc:220
    #24 0x7ffc5ccd392f in base::MessagePumpWin::Run E:\src\chromium\src\base\message_loop\message_pump_win.cc:78
    #25 0x7ffc5cbd9af3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #26 0x7ffc5cad0923 in base::RunLoop::Run E:\src\chromium\src\base\run_loop.cc:140
    #27 0x7ffc0cbcab53 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser_main_loop.cc:1053
    #28 0x7ffc0cbd09eb in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser_main_runner_impl.cc:155
    #29 0x7ffc0cbc405f in content::BrowserMain E:\src\chromium\src\content\browser\browser_main.cc:30
    #30 0x7ffc0eca7cbe in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content_main_runner_impl.cc:637
    #31 0x7ffc0ecaade1 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content_main_runner_impl.cc:1152
    #32 0x7ffc0eca9f0f in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content_main_runner_impl.cc:1018
    #33 0x7ffc0eca5cff in content::RunContentProcess E:\src\chromium\src\content\app\content_main.cc:399
    #34 0x7ffc0eca6db5 in content::ContentMain E:\src\chromium\src\content\app\content_main.cc:427
    #35 0x7ffc118d14a5 in ChromeMain E:\src\chromium\src\chrome\app\chrome_main.cc:176
    #36 0x7ff7e57d54e6 in MainDllLoader::Launch E:\src\chromium\src\chrome\app\main_dll_loader_win.cc:167
    #37 0x7ff7e57d2a02 in main E:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:382
    #38 0x7ff7e599c3bb in __scrt_common_main_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #39 0x7ffc99d67033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #40 0x7ffc9b822650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x11f4db1324d0 is located 16 bytes inside of 296-byte region [0x11f4db1324c0,0x11f4db1325e8)
freed by thread T0 here:
    #0 0x7ffc5b9df96b in operator delete+0x8b (E:\src\chromium\src\out\Default\clang_rt.asan_dynamic-x86_64.dll+0x18003f96b)
    #1 0x7ffc18d32234 in std::__1::__vector_base<std::__1::unique_ptr<TemplateURLFetcher::RequestDelegate,std::__1::default_delete<TemplateURLFetcher::RequestDelegate> >,std::__1::allocator<std::__1::unique_ptr<TemplateURLFetcher::RequestDelegate,std::__1::default_delete<TemplateURLFetcher::RequestDelegate> > > >::clear E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\vector:372
    #2 0x7ffc18d32191 in std::__1::__vector_base<std::__1::unique_ptr<TemplateURLFetcher::RequestDelegate,std::__1::default_delete<TemplateURLFetcher::RequestDelegate> >,std::__1::allocator<std::__1::unique_ptr<TemplateURLFetcher::RequestDelegate,std::__1::default_delete<TemplateURLFetcher::RequestDelegate> > > >::~__vector_base E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\vector:466
    #3 0x7ffc18d30eb9 in TemplateURLFetcher::~TemplateURLFetcher E:\src\chromium\src\components\search_engines\template_url_fetcher.cc:238
    #4 0x7ffc18d31ceb in TemplateURLFetcher::~TemplateURLFetcher E:\src\chromium\src\components\search_engines\template_url_fetcher.cc:237
    #5 0x7ffc74dceeb2 in std::__1::__tree<std::__1::__value_type<void *,std::__1::unique_ptr<KeyedService,std::__1::default_delete<KeyedService> > >,std::__1::__map_value_compare<void *,std::__1::__value_type<void *,std::__1::unique_ptr<KeyedService,std::__1::default_delete<KeyedService> > >,std::__1::less<void *>,1>,std::__1::allocator<std::__1::__value_type<void *,std::__1::unique_ptr<KeyedService,std::__1::default_delete<KeyedService> > > > >::erase E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2422
    #6 0x7ffc74dcd9d8 in KeyedServiceFactory::Disassociate E:\src\chromium\src\components\keyed_service\core\keyed_service_factory.cc:97
    #7 0x7ffc74dcdc68 in KeyedServiceFactory::ContextDestroyed E:\src\chromium\src\components\keyed_service\core\keyed_service_factory.cc:107
    #8 0x7ffc74dcb5df in DependencyManager::PerformInterlockedTwoPhaseShutdown E:\src\chromium\src\components\keyed_service\core\dependency_manager.cc:129
    #9 0x7ffc16410235 in ProfileImpl::~ProfileImpl E:\src\chromium\src\chrome\browser\profiles\profile_impl.cc:913
    #10 0x7ffc16413e79 in ProfileImpl::~ProfileImpl E:\src\chromium\src\chrome\browser\profiles\profile_impl.cc:860
    #11 0x7ffc1642694b in ProfileDestroyer::DestroyOriginalProfileNow E:\src\chromium\src\chrome\browser\profiles\profile_destroyer.cc:133
    #12 0x7ffc16426150 in ProfileDestroyer::DestroyProfileWhenAppropriate E:\src\chromium\src\chrome\browser\profiles\profile_destroyer.cc:61
    #13 0x7ffc151653d9 in ProfileManager::ProfileInfo::~ProfileInfo E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1703
    #14 0x7ffc1516e45d in std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> >::reset E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315
    #15 0x7ffc1516ec08 in std::__1::__tree<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::__map_value_compare<base::FilePath,std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::less<base::FilePath>,1>,std::__1::allocator<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > > > >::erase E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2422
    #16 0x7ffc1516eb5d in std::__1::__tree<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::__map_value_compare<base::FilePath,std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::less<base::FilePath>,1>,std::__1::allocator<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > > > >::__erase_unique<base::FilePath> E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2445
    #17 0x7ffc15162dc4 in ProfileManager::RemoveProfile E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1808
    #18 0x7ffc15162b62 in ProfileManager::DeleteProfileIfNoKeepAlive E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1538
    #19 0x7ffc151626ac in ProfileManager::RemoveKeepAlive E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1495
    #20 0x7ffc5cb85eb4 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task_annotator.cc:135
    #21 0x7ffc5cbd8379 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #22 0x7ffc5cbd7a48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #23 0x7ffc5ccd5e76 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message_loop\message_pump_win.cc:220
    #24 0x7ffc5ccd392f in base::MessagePumpWin::Run E:\src\chromium\src\base\message_loop\message_pump_win.cc:78
    #25 0x7ffc5cbd9af3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #26 0x7ffc5cad0923 in base::RunLoop::Run E:\src\chromium\src\base\run_loop.cc:140
    #27 0x7ffc0cbcab53 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser_main_loop.cc:1053

previously allocated by thread T0 here:
    #0 0x7ffc5b9df67b in operator new+0x8b (E:\src\chromium\src\out\Default\clang_rt.asan_dynamic-x86_64.dll+0x18003f67b)
    #1 0x7ffc18d3147f in TemplateURLFetcher::ScheduleDownload E:\src\chromium\src\components\search_engines\template_url_fetcher.cc:270
    #2 0x7ffc17b77395 in SearchEngineTabHelper::PageHasOpenSearchDescriptionDocument E:\src\chromium\src\chrome\browser\ui\search_engines\search_engine_tab_helper.cc:160
    #3 0x7ffc11909506 in chrome::mojom::OpenSearchDescriptionDocumentHandlerStubDispatch::Accept E:\src\chromium\src\out\Default\gen\chrome\common\open_search_description_document_handler.mojom.cc:158
    #4 0x7ffc6fe1aba4 in mojo::InterfaceEndpointClient::HandleValidatedMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:901
    #5 0x7ffc6fe2ad2a in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48
    #6 0x7ffc6fe1e4ec in mojo::InterfaceEndpointClient::HandleIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:658
    #7 0x7ffc6f88eaad in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread E:\src\chromium\src\ipc\ipc_mojo_bootstrap.cc:1008
    #8 0x7ffc6f888128 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce E:\src\chromium\src\base\bind_internal.h:741
    #9 0x7ffc5cb85eb4 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task_annotator.cc:135
    #10 0x7ffc5cbd8379 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #11 0x7ffc5cbd7a48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #12 0x7ffc5ccd5e76 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message_loop\message_pump_win.cc:220
    #13 0x7ffc5ccd392f in base::MessagePumpWin::Run E:\src\chromium\src\base\message_loop\message_pump_win.cc:78
    #14 0x7ffc5cbd9af3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #15 0x7ffc5cad0923 in base::RunLoop::Run E:\src\chromium\src\base\run_loop.cc:140
    #16 0x7ffc0cbcab53 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser_main_loop.cc:1053
    #17 0x7ffc0cbd09eb in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser_main_runner_impl.cc:155
    #18 0x7ffc0cbc405f in content::BrowserMain E:\src\chromium\src\content\browser\browser_main.cc:30
    #19 0x7ffc0eca7cbe in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content_main_runner_impl.cc:637
    #20 0x7ffc0ecaade1 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content_main_runner_impl.cc:1152
    #21 0x7ffc0eca9f0f in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content_main_runner_impl.cc:1018
    #22 0x7ffc0eca5cff in content::RunContentProcess E:\src\chromium\src\content\app\content_main.cc:399
    #23 0x7ffc0eca6db5 in content::ContentMain E:\src\chromium\src\content\app\content_main.cc:427
    #24 0x7ffc118d14a5 in ChromeMain E:\src\chromium\src\chrome\app\chrome_main.cc:176
    #25 0x7ff7e57d54e6 in MainDllLoader::Launch E:\src\chromium\src\chrome\app\main_dll_loader_win.cc:167
    #26 0x7ff7e57d2a02 in main E:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:382
    #27 0x7ff7e599c3bb in __scrt_common_main_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288

SUMMARY: AddressSanitizer: heap-use-after-free E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:312 in std::__1::unique_ptr<TemplateURL,std::__1::default_delete<TemplateURL> >::reset
Shadow bytes around the buggy address:
  0x040f76426440: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x040f76426450: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x040f76426460: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x040f76426470: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x040f76426480: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
=>0x040f76426490: fa fa fa fa fa fa fa fa fd fd[fd]fd fd fd fd fd
  0x040f764264a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x040f764264b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x040f764264c0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x040f764264d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x040f764264e0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
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
==17236==ABORTING

## Timeline

### [Deleted User] (2022-01-21)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-21)

Thanks - do you have a poc you can attach? This will help with testing.

rsesek: it looks like you made the last change here in https://chromium-review.googlesource.com/c/chromium/src/+/1879973

Sev=High for browser uaf mitigated by needing profile destruction to trigger.
FoundIn=96 as last commit is quite old.

[Monorail components: UI>Browser>Search]

### [Deleted User] (2022-01-21)

[Empty comment from Monorail migration]

### to...@chromium.org (2022-01-21)

I think I know how to fix this one too, I'll send a patch to rsesek.

### to...@chromium.org (2022-01-21)

By the way, thanks hackyzh002, your reports are very comprehensive and helpful.

### gi...@appspot.gserviceaccount.com (2022-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/65080d25a92a1a4fb45d052277702ae2aac19be4

commit 65080d25a92a1a4fb45d052277702ae2aac19be4
Author: Tommy Li <tommycli@chromium.org>
Date: Fri Jan 21 23:15:42 2022

[omnibox] Fix base::Unretained usage in TemplateURLFetcher (UAF bug)

The base::Unretained usage here is problematic when Chrome is shutting
down, leading to UAF bugs.

This CL fixes that using weak pointers in all the three locations where
we previously used base::Unretained.

Bug: 1289523
Change-Id: Ie91416d09efe3ff127abc00ec88e8e37acf039a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3408176
Auto-Submit: Tommy Li <tommycli@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#962132}

[modify] https://crrev.com/65080d25a92a1a4fb45d052277702ae2aac19be4/components/search_engines/template_url_fetcher.cc


### to...@chromium.org (2022-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

Requesting merge to extended stable M96 because latest trunk commit (962132) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (962132) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (962132) appears to be after beta branch point (950365).

Requesting merge to dev M99 because latest trunk commit (962132) appears to be after dev branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-22)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-22)

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

### [Deleted User] (2022-01-22)

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

### [Deleted User] (2022-01-22)

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

### am...@chromium.org (2022-01-25)

based on this fix, presuming no concern and approving merge to M98, please merge to branch 4758 ASAP/ NLT 11am PST tomorrow/Tuesday, 25 January so this fix can be included in tomorrow's stable cut of M98 -- thank you 

### am...@chromium.org (2022-01-25)

[Empty comment from Monorail migration]

### go...@chromium.org (2022-01-25)

Please merge to M98 branch 4758 ASAP so we can take it in for today's M98 Stable RC cut. Thank you. 

### to...@chromium.org (2022-01-25)

It's going through CQ right now: https://chromium-review.googlesource.com/c/chromium/src/+/3415317

Thanks for the reminder govind.

### am...@chromium.org (2022-01-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5b60f6559fee6a01a5d8a3ffd644369dc646ed88

commit 5b60f6559fee6a01a5d8a3ffd644369dc646ed88
Author: Tommy Li <tommycli@chromium.org>
Date: Wed Jan 26 00:40:15 2022

[Merge 98] [omnibox] Fix base::Unretained usage in TemplateURLFetcher (UAF bug)

The base::Unretained usage here is problematic when Chrome is shutting
down, leading to UAF bugs.

This CL fixes that using weak pointers in all the three locations where
we previously used base::Unretained.

(cherry picked from commit 65080d25a92a1a4fb45d052277702ae2aac19be4)

Bug: 1289523
Change-Id: Ie91416d09efe3ff127abc00ec88e8e37acf039a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3408176
Auto-Submit: Tommy Li <tommycli@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#962132}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3415317
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#912}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/5b60f6559fee6a01a5d8a3ffd644369dc646ed88/components/search_engines/template_url_fetcher.cc


### [Deleted User] (2022-01-26)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-01-26)

[Empty comment from Monorail migration]

### pb...@google.com (2022-01-27)

Your change has been approved for M99 branch 4844,please go ahead and merge the CL's manually asap so that they would be part of tomorrow's M99 Dev release.

### gi...@appspot.gserviceaccount.com (2022-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/75d5730e0f71e85595580fcc0d83723e21878769

commit 75d5730e0f71e85595580fcc0d83723e21878769
Author: Tommy Li <tommycli@chromium.org>
Date: Thu Jan 27 22:41:04 2022

[Merge 99] [omnibox] Fix base::Unretained usage in TemplateURLFetcher (UAF bug)

The base::Unretained usage here is problematic when Chrome is shutting
down, leading to UAF bugs.

This CL fixes that using weak pointers in all the three locations where
we previously used base::Unretained.

(cherry picked from commit 65080d25a92a1a4fb45d052277702ae2aac19be4)

Bug: 1289523
Change-Id: Ie91416d09efe3ff127abc00ec88e8e37acf039a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3408176
Auto-Submit: Tommy Li <tommycli@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#962132}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3421087
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/branch-heads/4844@{#94}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/75d5730e0f71e85595580fcc0d83723e21878769/components/search_engines/template_url_fetcher.cc


### am...@google.com (2022-01-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-28)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. Thanks for your efforts and reporting this issue to us. 

### am...@google.com (2022-01-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-31)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-03)

1. Number of CLs needed for this fix and links to them.
1 CL, https://crrev.com/c/3417212

2. Level of complexity (High, Medium, Low - Explain)
Low, only conflicting includes

3. Has this been merged to a stable release? beta release?
98, 99

4. Overall Recommendation (Yes, No)
Yes


### gm...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/77982678b1b4fb97b4bc2c3f75edcbbec4a282a7

commit 77982678b1b4fb97b4bc2c3f75edcbbec4a282a7
Author: Tommy Li <tommycli@chromium.org>
Date: Fri Feb 04 12:21:07 2022

[M96-LTS][omnibox] Fix base::Unretained usage in TemplateURLFetcher (UAF bug)

M96 merge issues:
  conflicting includes

The base::Unretained usage here is problematic when Chrome is shutting
down, leading to UAF bugs.

This CL fixes that using weak pointers in all the three locations where
we previously used base::Unretained.

(cherry picked from commit 65080d25a92a1a4fb45d052277702ae2aac19be4)

Bug: 1289523
Change-Id: Ie91416d09efe3ff127abc00ec88e8e37acf039a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3408176
Auto-Submit: Tommy Li <tommycli@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#962132}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3417212
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1449}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/77982678b1b4fb97b4bc2c3f75edcbbec4a282a7/components/search_engines/template_url_fetcher.cc


### rz...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1289523?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058541)*
