# OOB Read in WebGL2 clearBufferuiv

| Field | Value |
|-------|-------|
| **Issue ID** | [486505680](https://issues.chromium.org/issues/486505680) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-02-22 |
| **Bounty** | $2,000.00 |

## Description

```
=================================================================
==21228==ERROR: AddressSanitizer: access-violation on unknown address 0x132c00004000 (pc 0x7ffc1e81dc26 bp 0x00c87c9faa80 sp 0x00c87c9fa9f8 T0)
==21228==The signal is caused by a READ memory access.
==21228==*** WARNING: Failed to initialize DbgHelp!              ***
==21228==*** Most likely this means that the app is already      ***
==21228==*** using DbgHelp, possibly with incompatible flags.    ***
==21228==*** Due to technical reasons, symbolization might crash ***
==21228==*** or produce wrong results.                           ***
    #0 0x7ffc1e81dc25  (C:\WINDOWS\System32\ucrtbase.dll+0x1800edc25)
    #1 0x7ffb8829b4d2  (C:\Users\Admin\Downloads\win32-release_x64_asan-win32-release_x64-1588360\clang_rt.asan_dynamic-x86_64.dll+0x18004b4d2)
    #2 0x7ffad78191cb in gpu::gles2::cmds::ClearBufferuivImmediate::Init C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\common\gles2_cmd_format_autogen.h:1045
    #3 0x7ffad78191cb in gpu::gles2::GLES2CmdHelper::ClearBufferuivImmediate C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\client\gles2_cmd_helper_autogen.h:218
    #4 0x7ffad78191cb in gpu::gles2::GLES2Implementation::ClearBufferuiv(unsigned int, int, unsigned int const *) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\client\gles2_implementation_impl_autogen.h:302:12
    #5 0x7ffae6586609 in blink::WebGL2RenderingContextBase::clearBufferuiv(unsigned int, int, class base::span<unsigned int const, -1, unsigned int const *>, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webgl\webgl2_rendering_context_base.cc:3445:16
    #6 0x7ffae2c38d70 in blink::`anonymous namespace'::v8_webgl2_rendering_context::ClearBufferuivOperationCallback C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\bindings\modules\v8\v8_webgl2_rendering_context.cc:1542:17
    #7 0x7ffaeaf948e4 in Builtins_CallApiCallbackGeneric (C:\Users\Admin\Downloads\win32-release_x64_asan-win32-release_x64-1588360\chrome.dll+0x1ad1548e4)
    #8 0x7ffaeaf92a3b in Builtins_InterpreterEntryTrampoline (C:\Users\Admin\Downloads\win32-release_x64_asan-win32-release_x64-1588360\chrome.dll+0x1ad152a3b)
    #9 0x7ffaeaf92a3b in Builtins_InterpreterEntryTrampoline (C:\Users\Admin\Downloads\win32-release_x64_asan-win32-release_x64-1588360\chrome.dll+0x1ad152a3b)
    #10 0x7ffaeaf8f7db in Builtins_JSEntryTrampoline (C:\Users\Admin\Downloads\win32-release_x64_asan-win32-release_x64-1588360\chrome.dll+0x1ad14f7db)
    #11 0x7ffaeaf8f33e in Builtins_JSEntry (C:\Users\Admin\Downloads\win32-release_x64_asan-win32-release_x64-1588360\chrome.dll+0x1ad14f33e)
    #12 0x7ffac312ae5f in v8::internal::GeneratedCode<unsigned long long,unsigned long long,unsigned long long,unsigned long long,unsigned long long,long long,unsigned long long **>::Call C:\b\s\w\ir\cache\builder\src\v8\src\execution\simulator.h:216
    #13 0x7ffac312ae5f in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:442:22
    #14 0x7ffac312d821 in v8::internal::Execution::CallScript(class v8::internal::Isolate *, class v8::internal::DirectHandle<class v8::internal::JSFunction>, class v8::internal::DirectHandle<class v8::internal::Object>, class v8::internal::DirectHandle<class v8::internal::Object>) C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:542:10
    #15 0x7ffac2bcb6e6 in v8::Script::Run(class v8::Local<class v8::Context>, class v8::Local<class v8::Data>) C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:2031:7
    #16 0x7ffae05c8779 in blink::V8ScriptRunner::RunCompiledScript(class v8::Isolate *, class v8::Local<class v8::Script>, class v8::Local<class v8::Data>, class blink::ExecutionContext *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:511:22
    #17 0x7ffae05ca27c in blink::V8ScriptRunner::CompileAndRunScript(class blink::ScriptState *, class blink::ClassicScript *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:635:22
    #18 0x7ffadcce2059 in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(class blink::ScriptState *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\classic_script.cc:227:10
    #19 0x7ffadcc92ac9 in blink::Script::RunScriptOnScriptState(class blink::ScriptState *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script.cc:35:17
    #20 0x7ffadcc92f63 in blink::Script::RunScript(class blink::LocalDOMWindow *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script.cc:42:3
    #21 0x7ffadd5f6016 in blink::PendingScript::ExecuteScriptBlockInternal(class blink::Script *, class blink::ScriptElementBase *, bool, bool, bool, class base::TimeTicks, bool) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\pending_script.cc:312:13
    #22 0x7ffadd5f5016 in blink::PendingScript::ExecuteScriptBlock(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\pending_script.cc:209:3
    #23 0x7ffadd678e7a in blink::ScriptLoader::PrepareScript(enum blink::ScriptLoader::ParserBlockingInlineOption, class blink::TextPosition const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script_loader.cc:1175:60
    #24 0x7ffae1638407 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(class blink::Element *, class blink::TextPosition const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\html_parser_script_runner.cc:587:52
    #25 0x7ffae1637c3a in blink::HTMLParserScriptRunner::ProcessScriptElement(class blink::Element *, class blink::TextPosition const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\html_parser_script_runner.cc:297:3
    #26 0x7ffae167329e in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:662:21
    #27 0x7ffae166f32d in blink::HTMLDocumentParser::CanTakeNextToken C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.h:211
    #28 0x7ffae166f32d in blink::HTMLDocumentParser::PumpTokenizer(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:731:36
    #29 0x7ffae166d7d3 in blink::HTMLDocumentParser::PumpTokenizerIfPossible(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:625:15
    #30 0x7ffae167c130 in blink::HTMLDocumentParser::FinishAppend(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1028:5
    #31 0x7ffae167a77f in blink::HTMLDocumentParser::Append(class blink::String const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1021:3
    #32 0x7ffadf993714 in blink::DecodedDataDocumentParser::UpdateDocument C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\decoded_data_document_parser.cc:106
    #33 0x7ffadf993714 in blink::DecodedDataDocumentParser::AppendBytes(class base::span<unsigned char const, -1, unsigned char const *>) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\decoded_data_document_parser.cc:70:3
    #34 0x7ffae1681205 in blink::HTMLDocumentParser::AppendBytes(class base::span<unsigned char const, -1, unsigned char const *>) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1394:30
    #35 0x7ffadd778620 in blink::DocumentLoader::EncodedBodyData::AppendToParser(class blink::DocumentLoader *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:484:22
    #36 0x7ffadd756208 in blink::DocumentLoader::CommitData(class blink::DocumentLoader::BodyData &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:1626:8
    #37 0x7ffadd752b53 in blink::DocumentLoader::ProcessDataBuffer(class blink::DocumentLoader::BodyData *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:1862:5
    #38 0x7ffadd75149a in blink::DocumentLoader::BodyDataReceivedImpl(class blink::DocumentLoader::BodyData &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:1352:3
    #39 0x7ffadd750d1e in blink::DocumentLoader::BodyDataReceived(class base::span<char const, -1, char const *>) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:1298:3
    #40 0x7ffacb7a8771 in blink::NavigationBodyLoader::MainThreadBodyReader::DataReceived(class base::span<char const, -1, char const *>) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\navigation_body_loader.cc:346:23
    #41 0x7ffacb7a0d51 in blink::`anonymous namespace'::ReadFromDataPipeImpl C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\navigation_body_loader.cc:147:17
    #42 0x7ffacb7a05ef in blink::NavigationBodyLoader::ReadFromDataPipe(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\navigation_body_loader.cc:548:3
    #43 0x7ffacb79bbdc in blink::NavigationBodyLoader::OnReadable(unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\navigation_body_loader.cc:507:3
    #44 0x7ffacb79e935 in blink::NavigationBodyLoader::BindURLLoaderAndStartLoadingResponseBodyIfPossible(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\navigation_body_loader.cc:605:3
    #45 0x7ffacb79e339 in blink::NavigationBodyLoader::StartLoadingBody(class blink::WebNavigationBodyLoader::Client *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\navigation_body_loader.cc:452:3
    #46 0x7ffadd75c59d in blink::DocumentLoader::StartLoadingResponse(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:2140:19
    #47 0x7ffadd76c3b8 in blink::DocumentLoader::CommitNavigation(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:3180:3
    #48 0x7ffadd5b4224 in blink::FrameLoader::CommitDocumentLoader(class blink::DocumentLoader *, class blink::HistoryItem *, enum blink::CommitReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:1461:21
    #49 0x7ffadd5c0592 in blink::FrameLoader::CommitNavigation(class std::__Cr::unique_ptr<struct blink::WebNavigationParams, struct std::__Cr::default_delete<struct blink::WebNavigationParams>>, class std::__Cr::unique_ptr<class blink::WebDocumentLoader::ExtraData, struct std::__Cr::default_delete<class blink::WebDocumentLoader::ExtraData>>, enum blink::CommitReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:1273:3
    #50 0x7ffadeddbee9 in blink::WebLocalFrameImpl::CommitNavigation(class std::__Cr::unique_ptr<struct blink::WebNavigationParams, struct std::__Cr::default_delete<struct blink::WebNavigationParams>>, class std::__Cr::unique_ptr<class blink::WebDocumentLoader::ExtraData, struct std::__Cr::default_delete<class blink::WebDocumentLoader::ExtraData>>) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_local_frame_impl.cc:2824:24
    #51 0x7ffadca523c4 in content::RenderFrameImpl::CommitNavigationWithParams(class mojo::StructPtr<class blink::mojom::CommonNavigationParams>, class mojo::StructPtr<class blink::mojom::CommitNavigationParams>, class std::__Cr::unique_ptr<class blink::PendingURLLoaderFactoryBundle, struct std::__Cr::default_delete<class blink::PendingURLLoaderFactoryBundle>>, class std::__Cr::optional<class std::__Cr::vector<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>, class std::__Cr::allocator<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>>>>, class mojo::StructPtr<class blink::mojom::ControllerServiceWorkerInfo>, class mojo::StructPtr<class blink::mojom::ServiceWorkerContainerInfoForClient>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingAssociatedRemote<class blink::mojom::FetchLaterLoaderFactory>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::StructPtr<class content::mojom::CookieManagerInfo>, class mojo::StructPtr<class content::mojom::StorageInfo>, class std::__Cr::unique_ptr<class content::DocumentState, struct std::__Cr::default_delete<class content::DocumentState>>, class std::__Cr::unique_ptr<struct blink::WebNavigationParams, struct std::__Cr::default_delete<struct blink::WebNavigationParams>>) C:\b\s\w\ir\cache\builder\src\content\renderer\render_frame_impl.cc:3001:11
    #52 0x7ffadcab0c94 in ??@d03c3135e0a1a833bdf4f2cd124434b5@ C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740:12
    #53 0x7ffadcab0733 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (content::RenderFrameImpl::*&&)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> >, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState,std::__Cr::default_delete<content::DocumentState> >, std::__Cr::unique_ptr<blink::WebNavigationParams,std::__Cr::default_delete<blink::WebNavigationParams> >),base::WeakPtr<content::RenderFrameImpl> &&,mojo::StructPtr<blink::mojom::CommonNavigationParams> &&,mojo::StructPtr<blink::mojom::CommitNavigationParams> &&,std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> > &&,std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > > &&,mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo> &&,mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient> &&,mojo::PendingRemote<network::mojom::URLLoaderFactory> &&,mojo::PendingRemote<network::mojom::URLLoaderFactory> &&,mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory> &&,mojo::PendingRemote<blink::mojom::CodeCacheHost> &&,mojo::PendingRemote<blink::mojom::CodeCacheHost> &&,mojo::StructPtr<content::mojom::CookieManagerInfo> &&,mojo::StructPtr<content::mojom::StorageInfo> &&,std::__Cr::unique_ptr<content::DocumentState,std::__Cr::default_delete<content::DocumentState> > &&>,void,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:956
    #54 0x7ffadcab0733 in base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameImpl::*&&)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> >, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState,std::__Cr::default_delete<content::DocumentState> >, std::__Cr::unique_ptr<blink::WebNavigationParams,std::__Cr::default_delete<blink::WebNavigationParams> >),base::WeakPtr<content::RenderFrameImpl> &&,mojo::StructPtr<blink::mojom::CommonNavigationParams> &&,mojo::StructPtr<blink::mojom::CommitNavigationParams> &&,std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> > &&,std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > > &&,mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo> &&,mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient> &&,mojo::PendingRemote<network::mojom::URLLoaderFactory> &&,mojo::PendingRemote<network::mojom::URLLoaderFactory> &&,mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory> &&,mojo::PendingRemote<blink::mojom::CodeCacheHost> &&,mojo::PendingRemote<blink::mojom::CodeCacheHost> &&,mojo::StructPtr<content::mojom::CookieManagerInfo> &&,mojo::StructPtr<content::mojom::StorageInfo> &&,std::__Cr::unique_ptr<content::DocumentState,std::__Cr::default_delete<content::DocumentState> > &&>,base::internal::BindState<1,1,0,void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> >, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState,std::__Cr::default_delete<content::DocumentState> >, std::__Cr::unique_ptr<blink::WebNavigationParams,std::__Cr::default_delete<blink::WebNavigationParams> >),base::WeakPtr<content::RenderFrameImpl>,mojo::StructPtr<blink::mojom::CommonNavigationParams>,mojo::StructPtr<blink::mojom::CommitNavigationParams>,std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> >,std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >,mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>,mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>,mojo::PendingRemote<network::mojom::URLLoaderFactory>,mojo::PendingRemote<network::mojom::URLLoaderFactory>,mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>,mojo::PendingRemote<blink::mojom::CodeCacheHost>,mojo::PendingRemote<blink::mojom::CodeCacheHost>,mojo::StructPtr<content::mojom::CookieManagerInfo>,mojo::StructPtr<content::mojom::StorageInfo>,std::__Cr::unique_ptr<content::DocumentState,std::__Cr::default_delete<content::DocumentState> > >,void (std::__Cr::unique_ptr<blink::WebNavigationParams,std::__Cr::default_delete<blink::WebNavigationParams> >)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #55 0x7ffadcab0733 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl content::RenderFrameImpl::*&&)(class mojo::StructPtr<class blink::mojom::CommonNavigationParams>, class mojo::StructPtr<class blink::mojom::CommitNavigationParams>, class std::__Cr::unique_ptr<class blink::PendingURLLoaderFactoryBundle, struct std::__Cr::default_delete<class blink::PendingURLLoaderFactoryBundle>>, class std::__Cr::optional<class std::__Cr::vector<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>, class std::__Cr::allocator<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>>>>, class mojo::StructPtr<class blink::mojom::ControllerServiceWorkerInfo>, class mojo::StructPtr<class blink::mojom::ServiceWorkerContainerInfoForClient>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingAssociatedRemote<class blink::mojom::FetchLaterLoaderFactory>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::StructPtr<class content::mojom::CookieManagerInfo>, class mojo::StructPtr<class content::mojom::StorageInfo>, class std::__Cr::unique_ptr<class content::DocumentState, struct std::__Cr::default_delete<class content::DocumentState>>, class std::__Cr::unique_ptr<struct blink::WebNavigationParams, struct std::__Cr::default_delete<struct blink::WebNavigationParams>>), class base::WeakPtr<class content::RenderFrameImpl> &&, class mojo::StructPtr<class blink::mojom::CommonNavigationParams> &&, class mojo::StructPtr<class blink::mojom::CommitNavigationParams> &&, class std::__Cr::unique_ptr<class blink::PendingURLLoaderFactoryBundle, struct std::__Cr::default_delete<class blink::PendingURLLoaderFactoryBundle>> &&, class std::__Cr::optional<class std::__Cr::vector<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>, class std::__Cr::allocator<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>>>> &&, class mojo::StructPtr<class blink::mojom::ControllerServiceWorkerInfo> &&, class mojo::StructPtr<class blink::mojom::ServiceWorkerContainerInfoForClient> &&, class mojo::PendingRemote<class network::mojom::URLLoaderFactory> &&, class mojo::PendingRemote<class network::mojom::URLLoaderFactory> &&, class mojo::PendingAssociatedRemote<class blink::mojom::FetchLaterLoaderFactory> &&, class mojo::PendingRemote<class blink::mojom::CodeCacheHost> &&, class mojo::PendingRemote<class blink::mojom::CodeCacheHost> &&, class mojo::StructPtr<class content::mojom::CookieManagerInfo> &&, class mojo::StructPtr<class content::mojom::StorageInfo> &&, class std::__Cr::unique_ptr<class content::DocumentState, struct std::__Cr::default_delete<class content::DocumentState>> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl content::RenderFrameImpl::*)(class mojo::StructPtr<class blink::mojom::CommonNavigationParams>, class mojo::StructPtr<class blink::mojom::CommitNavigationParams>, class std::__Cr::unique_ptr<class blink::PendingURLLoaderFactoryBundle, struct std::__Cr::default_delete<class blink::PendingURLLoaderFactoryBundle>>, class std::__Cr::optional<class std::__Cr::vector<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>, class std::__Cr::allocator<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>>>>, class mojo::StructPtr<class blink::mojom::ControllerServiceWorkerInfo>, class mojo::StructPtr<class blink::mojom::ServiceWorkerContainerInfoForClient>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingAssociatedRemote<class blink::mojom::FetchLaterLoaderFactory>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::StructPtr<class content::mojom::CookieManagerInfo>, class mojo::StructPtr<class content::mojom::StorageInfo>, class std::__Cr::unique_ptr<class content::DocumentState, struct std::__Cr::default_delete<class content::DocumentState>>, class std::__Cr::unique_ptr<struct blink::WebNavigationParams, struct std::__Cr::default_delete<struct blink::WebNavigationParams>>), class base::WeakPtr<class content::RenderFrameImpl>, class mojo::StructPtr<class blink::mojom::CommonNavigationParams>, class mojo::StructPtr<class blink::mojom::CommitNavigationParams>, class std::__Cr::unique_ptr<class blink::PendingURLLoaderFactoryBundle, struct std::__Cr::default_delete<class blink::PendingURLLoaderFactoryBundle>>, class std::__Cr::optional<class std::__Cr::vector<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>, class std::__Cr::allocator<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>>>>, class mojo::StructPtr<class blink::mojom::ControllerServiceWorkerInfo>, class mojo::StructPtr<class blink::mojom::ServiceWorkerContainerInfoForClient>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingAssociatedRemote<class blink::mojom::FetchLaterLoaderFactory>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::StructPtr<class content::mojom::CookieManagerInfo>, class mojo::StructPtr<class content::mojom::StorageInfo>, class std::__Cr::unique_ptr<class content::DocumentState, struct std::__Cr::default_delete<class content::DocumentState>>>, (class std::__Cr::unique_ptr<struct blink::WebNavigationParams, struct std::__Cr::default_delete<struct blink::WebNavigationParams>>)>::RunOnce(class base::internal::BindStateBase *, class std::__Cr::unique_ptr<struct blink::WebNavigationParams, struct std::__Cr::default_delete<struct blink::WebNavigationParams>> &&) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #56 0x7ffadca53b84 in base::OnceCallback<(class std::__Cr::unique_ptr<struct blink::WebNavigationParams, struct std::__Cr::default_delete<struct blink::WebNavigationParams>>)>::Run(class std::__Cr::unique_ptr<struct blink::WebNavigationParams, struct std::__Cr::default_delete<struct blink::WebNavigationParams>>) && C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155:12
    #57 0x7ffadca4c26d in content::RenderFrameImpl::CommitNavigation(class mojo::StructPtr<class blink::mojom::CommonNavigationParams>, class mojo::StructPtr<class blink::mojom::CommitNavigationParams>, class mojo::StructPtr<class network::mojom::URLResponseHead>, class mojo::ScopedHandleBase<class mojo::DataPipeConsumerHandle>, class mojo::StructPtr<class network::mojom::URLLoaderClientEndpoints>, class std::__Cr::unique_ptr<class blink::PendingURLLoaderFactoryBundle, struct std::__Cr::default_delete<class blink::PendingURLLoaderFactoryBundle>>, class std::__Cr::optional<class std::__Cr::vector<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>, class std::__Cr::allocator<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>>>>, class mojo::StructPtr<class blink::mojom::ControllerServiceWorkerInfo>, class mojo::StructPtr<class blink::mojom::ServiceWorkerContainerInfoForClient>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingAssociatedRemote<class blink::mojom::FetchLaterLoaderFactory>, class base::TokenType<class blink::DocumentTokenTypeMarker> const &, class base::UnguessableToken const &, class base::Uuid const &, class mojo::StructPtr<class blink::mojom::PolicyContainer>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::StructPtr<class content::mojom::CookieManagerInfo>, class mojo::StructPtr<class content::mojom::StorageInfo>, class base::OnceCallback<(class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) C:\b\s\w\ir\cache\builder\src\content\renderer\render_frame_impl.cc:2859:33
    #58 0x7ffadcacb557 in content::NavigationClient::CommitNavigation(class mojo::StructPtr<class blink::mojom::CommonNavigationParams>, class mojo::StructPtr<class blink::mojom::CommitNavigationParams>, class mojo::StructPtr<class network::mojom::URLResponseHead>, class mojo::ScopedHandleBase<class mojo::DataPipeConsumerHandle>, class mojo::StructPtr<class network::mojom::URLLoaderClientEndpoints>, class std::__Cr::unique_ptr<class blink::PendingURLLoaderFactoryBundle, struct std::__Cr::default_delete<class blink::PendingURLLoaderFactoryBundle>>, class std::__Cr::optional<class std::__Cr::vector<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>, class std::__Cr::allocator<class mojo::StructPtr<class blink::mojom::TransferrableURLLoader>>>>, class mojo::StructPtr<class blink::mojom::ControllerServiceWorkerInfo>, class mojo::StructPtr<class blink::mojom::ServiceWorkerContainerInfoForClient>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingRemote<class network::mojom::URLLoaderFactory>, class mojo::PendingAssociatedRemote<class blink::mojom::FetchLaterLoaderFactory>, class base::TokenType<class blink::DocumentTokenTypeMarker> const &, class base::UnguessableToken const &, class base::Uuid const &, class mojo::StructPtr<class blink::mojom::PolicyContainer>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::PendingRemote<class blink::mojom::CodeCacheHost>, class mojo::StructPtr<class content::mojom::CookieManagerInfo>, class mojo::StructPtr<class content::mojom::StorageInfo>, class base::OnceCallback<(class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) C:\b\s\w\ir\cache\builder\src\content\renderer\navigation_client.cc:87:18
    #59 0x7ffac2a566a1 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(class content::mojom::NavigationClient *, class mojo::Message *, class std::__Cr::unique_ptr<class mojo::MessageReceiverWithStatus, struct std::__Cr::default_delete<class mojo::MessageReceiverWithStatus>>) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\content\common\navigation_client.mojom.cc:1746:13
    #60 0x7ffadcacf47c in content::mojom::NavigationClientStub<struct mojo::RawPtrImplRefTraits<class content::mojom::NavigationClient>>::AcceptWithResponder(class mojo::Message *, class std::__Cr::unique_ptr<class mojo::MessageReceiverWithStatus, struct std::__Cr::default_delete<class mojo::MessageReceiverWithStatus>>) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\content\common\navigation_client.mojom.h:184:12
    #61 0x7ffad207537d in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036:56
    #62 0x7ffad207211d in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44:19
    #63 0x7ffad207babe in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747:20
    #64 0x7ffad5aaf986 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1199:24
    #65 0x7ffad5ab1ea1 in base::internal::DecayedFunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740
    #66 0x7ffad5ab1ea1 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932
    #67 0x7ffad5ab1ea1 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),scoped_refptr<IPC::ChannelAssociatedGroupController>,mojo::Message,IPC::`anonymous namespace'::ScopedUrgentMessageNotification>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #68 0x7ffad5ab1ea1 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),scoped_refptr<IPC::ChannelAssociatedGroupController>,mojo::Message,IPC::`anonymous namespace'::ScopedUrgentMessageNotification>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #69 0x7ffad234e7e8 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #70 0x7ffad234e7e8 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229:34
    #71 0x7ffad231ec31 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:112
    #72 0x7ffad231ec31 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475:23
    #73 0x7ffad231da93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #74 0x7ffad2488f40 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #75 0x7ffad232097f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650:12
    #76 0x7ffad23c621c in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135:14
    #77 0x7ffadc9295df in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:364:16
    #78 0x7ffacdf3133f in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:762:14
    #79 0x7ffacdf33aab in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1152:10
    #80 0x7ffacdf2789f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358:36
    #81 0x7ffacdf28042 in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371:10
    #82 0x7ffabde42b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191:12
    #83 0x7ff62ce34807 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:204:12
    #84 0x7ff62ce32074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351:20
    #85 0x7ff62d32cc7f in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #86 0x7ff62d32cc7f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #87 0x7ffc203ae8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #88 0x7ffc2154c40b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

==21228==Register values:
rax = 2a1af280444  rbx = 2a1af280444  rcx = 2a1af280444  rdx = 132c00004000
rdi = 132c00004000  rsi = 10  rbp = c87c9faa80  rsp = c87c9fa9f8
r8  = 10  r9  = 5435e5008a  r10 = 7ffc1e730000  r11 = 0
r12 = 5435e50087  r13 = 2a1aff80000  r14 = 2a1af280444  r15 = ffffffffffffffcf
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation (C:\WINDOWS\System32\ucrtbase.dll+0x1800edc25)

==21228==ADDITIONAL INFO

==21228==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffad5aa97a9 in IPC::ChannelAssociatedGroupController::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1138:13


Command line: `"C:\Users\Admin\Downloads\win32-release_x64_asan-win32-release_x64-1588360\chrome.exe" --type=renderer --origin-trial-disabled-features=CanvasTextNg|WebAssemblyCustomDescriptors --no-pre-read-main-dll --no-sandbox --file-url-path-alias="/gen=C:\Users\Admin\Downloads\win32-release_x64_asan-win32-release_x64-1588360\gen" --video-capture-use-gpu-memory-buffer --lang=en-GB --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1771721622136947 --launch-time-ticks=27161602209 --metrics-shmem-handle=3828,i,9772016731351981910,9808478740064636497,2097152 --field-trial-handle=1892,i,14155882457508387962,16691606363809584392,262144 --variations-seed-version --pseudonymization-salt-handle=2056,i,7195198084768945281,5447165799788727503,4 --trace-process-track-uuid=3190708990997080739 --mojo-platform-channel-handle=3844 /prefetch:1`


==21228==END OF ADDITIONAL INFO

==21228==ABORTING


```
#### VERSION

Version 147.0.7700.0 (Developer Build) (64-bit)

#### REPRODUCTION CASE

Build: [asan-win32-release\_x64-1588360](https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1588360.zip?generation=1771721862773027&alt=media)

Run: `./chrome.exe --no-sandbox poc.html`

---

Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/html, 922 B)
- [testcase.html](attachments/testcase.html) (text/html, 2.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6513259855151104.

### an...@chromium.org (2026-02-22)

Clusterfuzz was unable to repro. zmo@ can you PTAL at the attached ASAN trace to see if is helpful? Thanks!

### fa...@gmail.com (2026-02-23)

deleted

### ch...@google.com (2026-02-23)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-23)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2026-03-09)

zmo: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fa...@gmail.com (2026-03-09)

# Root Cause Analysis — clearBuffer\*v OOB Read

## Bug Class

**TOCTOU (Time-of-Check-Time-of-Use) → OOB Read on detached ArrayBuffer**

## Affected Functions

| Function | Buffer Type | Source File Line |
| --- | --- | --- |
| `clearBufferiv` | `Int32Array` | `webgl2_rendering_context_base.cc:3426` |
| `clearBufferuiv` | `Uint32Array` | `webgl2_rendering_context_base.cc:3446` |
| `clearBufferfv` | `Float32Array` | `webgl2_rendering_context_base.cc:3465` |

## Root Cause

The WebGL2 `clearBuffer*v(buffer, drawbuffer, value, srcOffset)` methods accept a TypedArray `value` and a `srcOffset` parameter. The V8 bindings convert the TypedArray into a `base::span<const T>` **before** coercing `srcOffset` to an integer (which calls `valueOf()`).

**The TOCTOU race:**

1. **Check** — V8 bindings extract the TypedArray's backing `ArrayBuffer` data pointer and length → creates `base::span<const GLint>` (for `clearBufferiv`)
2. **Use-valueOf** — The engine coerces `srcOffset` by calling `valueOf()` on the attacker-supplied object
3. **Detach** — Inside `valueOf()`, `ArrayBuffer.prototype.transfer(0)` detaches the buffer, deallocating the backing store
4. **Use** — Blink C++ code calls `value.subspan(src_offset).data()` → **dangling pointer to unmapped memory**

```
// webgl2_rendering_context_base.cc (clearBufferiv)
ContextGL()->ClearBufferiv(buffer, drawbuffer,
                           value.subspan(src_offset).data());  // <-- span points to freed memory

```

The span's `.data()` pointer is now stale — the backing store was freed during `valueOf()`.

## Validation Gap

`ValidateClearBuffer()` validates `value.size()` and `src_offset` bounds, but the span was created before `valueOf()` ran. By the time `subspan()` is called, the backing store is already freed. The validation checks the *cached size* (snapshot before detachment), not whether the backing store is still alive.

## Crash Signature (ASan)

```
==44896==ERROR: AddressSanitizer: access-violation on unknown address 0x123800004000 (pc 0x7ff967eddc1a bp ... sp ... T83)
==44896==The signal is caused by a READ memory access.
    #0 0x7ff967eddc19 in memcpy+0x119 (ucrtbase.dll)
    #1 0x7ff9045db532 in _asan_memcpy+0x422 (clang_rt.asan_dynamic-x86_64.dll)
    #2 0x7ff825672a6b in gpu::gles2::GLES2Implementation::ClearBufferiv ...gles2_implementation_impl_autogen.h:281
    #3 0x7ff83445d176 in blink::WebGL2RenderingContextBase::clearBufferiv ...webgl2_rendering_context_base.cc:3426
    #4 0x7ff830b05314 in blink::...v8_webgl2_rendering_context::ClearBufferivOperationCallback ...v8_webgl2_rendering_context.cc:1469
SUMMARY: AddressSanitizer: access-violation (ucrtbase.dll) in memcpy+0x119

```
## Impact

- **OOB Read** from unmapped/freed memory in the renderer process
- Potential information leak if memory is reclaimed before the read

### Reproduction - Selecting Individual Tests

Append `?test=N` to the URL to run a specific sub-test:

| `?test=` | Function |
| --- | --- |
| `1` | `clearBufferiv` (default) |
| `2` | `clearBufferuiv` |
| `3` | `clearBufferfv` |

Example:

```
chrome.exe --no-sandbox testcase.html?test=2

```

Omit `?test=` or use `?test=0` to list all available tests and auto-run test 1.

### ds...@google.com (2026-04-20)

This sounds like a WebGL issue, going to send over to Geoff for WebGL triage.

### ds...@google.com (2026-04-20)

From the description this sounds like a potential OOB read in the GPU process, going to move it up to S1 from S2.

### fa...@gmail.com (2026-04-24)

I lost access to this issue. Thanks for adding me back.

> Status: Duplicate of 490118036

Hi, this is incorrect—the issue I reported was filed earlier than the one marked as duplicate, as is evident.

### ch...@google.com (2026-04-24)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ge...@google.com (2026-04-24)

Fixed landed and merged in [issue 490118036](https://issues.chromium.org/issues/490118036)

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M149. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M149. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514926077](https://crbug.com/514926077) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514929756](https://crbug.com/514929756) to have this merge reviewed.**

### fa...@gmail.com (2026-05-26)

Hi,

I would like to request a reevaluation of this issue for High Quality Report consideration. I provided an RCA for the issue here: <https://issues.chromium.org/issues/486505680#comment8>.

As mentioned in the Root cause, `ArrayBuffer.prototype.transfer(0)` inside `valueOf()` detaches the buffer and deallocates the backing store. A similarly is fixed: “Perform detach check when passing span instead of retaining underlying array buffer”:
<https://chromium-review.googlesource.com/c/chromium/src/+/7716642>

I believe this supports the validity and accuracy of the reported root cause.

Thank you, and best regards.

### kb...@chromium.org (2026-05-26)

To be honest, the Chrome team didn't look at this bug report when fixing the bug. It was reported at least four times in different ways by different individuals: here, in [Issue 489325431](https://issues.chromium.org/issues/489325431), in [Issue 490118036](https://issues.chromium.org/issues/490118036), and in [Issue 490810422](https://issues.chromium.org/issues/490810422). Other of the reports were clearer in their description and led to a rapid resolution.

### fa...@gmail.com (2026-05-26)

That’s nice. I was thinking that if the RCA contains the correct details, shouldn’t this report be considered for a higher quality reward? I was somehow able to find this earlier, and I also do not want to miss the bonus reward if everything looks good. I do not mean this in an egotistical way.

Thank you, and best regards.

### fa...@gmail.com (2026-05-26)

Also, I hate to bring this up, but as a human myself, I missed a CVE and recognition on chromium releases and ended up getting locked out of my own report, which was quite frustrating.

### wf...@chromium.org (2026-06-02)

[vrp panel] This is an OOB read which is 2k as it's information disclosure baseline/lower impact - this is because the rules state "In cases where a report displays an out-of-bounds read or access to a value without demonstrating a write or the potential for attacker control of that value or RCE, these issues may be considered for a lower reward amount, consistent with an information disclosure.". The panel considered this and decided to keep the reward here at $2k.

### fa...@gmail.com (2026-06-02)

I appreciate the clarification and agree with the panel’s assessment. Thank you for the review.

### vi...@google.com (2026-06-10)

This was already merged in M144-LTS: <https://chromium-review.git.corp.google.com/c/chromium/src/+/7755304> (mentioned also in [comment#13](https://issues.chromium.org/issues/486505680#comment13))

### ch...@google.com (2026-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486505680)*
