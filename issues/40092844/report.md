# Security: Use-after-free in CPWL_Wnd::Destroy

| Field | Value |
|-------|-------|
| **Issue ID** | [40092844](https://issues.chromium.org/issues/40092844) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-10-24 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CPWL\_Wnd::Destroy

**VERSION**  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Build chrome without XFA enabled
2. open file `poc_controlEIP.pdf` in chrome

(13c4.4d8): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\out\chromium\_pdfium\_xfa\_03\_10\chrome.dll  

chrome!CPWL\_Wnd::Destroy+0x33:  

672ae793 ff92a8000000 call dword ptr [edx+0A8h] ds:002b:414141e9=????????

3:067:x86> kp

# ChildEBP RetAddr

00 00deb4f0 66e085c0 chrome!CPWL\_Wnd::Destroy(void)+0x33 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\pwl\cpwl\_wnd.cpp @ 177]  

01 00deb56c 672be845 chrome!CFFL\_FormFiller::DestroyPDFWindow(class CPDFSDK\_PageView \* pPageView = 0x17d872e8)+0xb0 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_formfiller.cpp @ 419]  

02 00deb5b0 66e07a36 chrome!CFFL\_TextObject::ResetPDFWindow(class CPDFSDK\_PageView \* pPageView = 0x17d872e8, bool bRestoreValue = false)+0x65 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_textobject.cpp @ 14]  

03 00deb614 66e0788f chrome!CFFL\_FormFiller::CommitData(class CPDFSDK\_PageView \* pPageView = 0x17d872e8, unsigned int nFlag = 0)+0xe6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_formfiller.cpp @ 523]  

04 00deb660 664903ab chrome!CFFL\_FormFiller::KillFocusForAnnot(class CPDFSDK\_Annot \* pAnnot = 0x17d1ffb8, unsigned int nFlag = 0)+0x6f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_formfiller.cpp @ 309]  

05 00deb6e0 66e12b4c chrome!CFFL\_InteractiveFormFiller::OnKillFocus(class fxcrt::Observable<CPDFSDK\_Annot>::ObservedPtr \* pAnnot = 0x00deb794, unsigned int nFlag = 0)+0xeb [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_interactiveformfiller.cpp @ 420]  

06 00deb710 6648d08f chrome!CPDFSDK\_WidgetHandler::OnKillFocus(class fxcrt::Observable<CPDFSDK\_Annot>::ObservedPtr \* pAnnot = 0x00deb794, unsigned int nFlag = 0)+0x7c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_widgethandler.cpp @ 262]  

07 00deb73c 65348982 chrome!CPDFSDK\_AnnotHandlerMgr::Annot\_OnKillFocus(class fxcrt::Observable<CPDFSDK\_Annot>::ObservedPtr \* pAnnot = 0x00deb794, unsigned int nFlag = 0)+0x7f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 270]  

08 00deb7a0 65349b03 chrome!CPDFSDK\_FormFillEnvironment::KillFocusAnnot(unsigned int nFlag = 0)+0xd2 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_formfillenvironment.cpp @ 694]  

09 00deb7f0 66cc23eb chrome!CPDFSDK\_FormFillEnvironment::SetFocusAnnot(class fxcrt::Observable<CPDFSDK\_Annot>::ObservedPtr \* pAnnot = 0x00deb854)+0x93 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_formfillenvironment.cpp @ 653]  

0a 00deb86c 66cd34e7 chrome!CJS\_Field::setFocus(class CJS\_Runtime \* pRuntime = 0x17dcbe88, class std::vector<v8::Local[v8::Value](javascript:void(0);),std::allocator<v8::Local[v8::Value](javascript:void(0);) > > \* params = 0x00deb940)+0x22b [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fxjs\cjs\_field.cpp @ 2535]  

0b 00deb96c 66cb336b chrome!JSMethod<CJS\_Field,&CJS\_Field::setFocus>(char \* method\_name\_string = 0x67fc51d8 "setFocus", char \* class\_name\_string = 0x67fc4ea4 "Field", class v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) \* info = 0x00deb998)+0x267 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fxjs\js\_define.h @ 135]  

0c 00deb984 0fef62b6 chrome!CJS\_Field::setFocus\_static(class v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) \* info = 0x00deb998)+0x2b [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fxjs\cjs\_field.h @ 112]  

0d 00deb9e8 0fef525d v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo \* handler = 0x18d1a0ed)+0x266 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\v8\src\api-arguments-inl.h @ 140]  

0e 00deba50 0fef3f34 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = 0x17c9efb0, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x29d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\v8\src\builtins\builtins-api.cc @ 111] 0f 00debaa4 0fef3a64 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x17c9efb0)+0x164 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\v8\src\builtins\builtins-api.cc @ 139] 10 00debb18 290c890a v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n5, class v8::internal::Object \*\* args_object = 0x00debb50, class v8::internal::Isolate \* isolate = 0x17c9efb0)+0x64 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\v8\src\builtins\builtins-api.cc @ 127] WARNING: Frame IP not in any known module. Following frames may be wrong. 11 00debb38 2cc1c8f5 0x290c890a 12 00debb7c 2cc1525c 0x2cc1c8f5 13 00debb90 2cc07971 0x2cc1525c 14 00debbbc 103c9176 0x2cc07971 15 00debc44 103c8c67 v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = 0x00000005, bool is\_construct = <Value unavailable error>, class v8::internal::Handle[v8::internal::Object](javascript:void(0);) target = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), class v8::internal::Handle[v8::internal::Object](javascript:void(0);) receiver = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), int argc = 0n0, class v8::internal::Handle[v8::internal::Object](javascript:void(0);) \* args = 0x00000000, class v8::internal::Handle[v8::internal::Object](javascript:void(0);) new\_target = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling message\_handling = kReport (0n0), v8::internal::Execution::Target execution\_target = kCallable (0n0))+0x446 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\v8\src\execution.cc @ 155]  

16 00debc7c 103c8bb1 v8!v8::internal::`anonymous namespace'::CallInternal(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle[v8::internal::Object](javascript:void(0);) callable = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), class v8::internal::Handle[v8::internal::Object](javascript:void(0);) receiver = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), int argc = 0n0, class v8::internal::Handle[v8::internal::Object](javascript:void(0);) \* argv = 0x00000000, v8::internal::Execution::MessageHandling message\_handling = kReport (0n0), v8::internal::Execution::Target target = kCallable (0n0))+0xa7 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\v8\src\execution.cc @ 191]  

17 00debca0 0fdd8c0d v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x17c9efb0, class v8::internal::Handle[v8::internal::Object](javascript:void(0);) callable = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), class v8::internal::Handle[v8::internal::Object](javascript:void(0);) receiver = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), int argc = 0n0, class v8::internal::Handle[v8::internal::Object](javascript:void(0);) \* argv = 0x00000000)+0x21 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\v8\src\execution.cc @ 202]  

18 00debd64 6639a896 v8!v8::Script::Run(class v8::Local[v8::Context](javascript:void(0);) context = class v8::Local[v8::Context](javascript:void(0);))+0x2fd [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\v8\src\api.cc @ 2114]  

19 00debf0c 663a7fee chrome!CFXJS\_Engine::Execute(class fxcrt::WideString \* script = 0x00dec144)+0x396 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fxjs\cfxjs\_engine.cpp @ 534]  

1a 00debf30 66cff62e chrome!CJS\_Runtime::ExecuteScript(class fxcrt::WideString \* script = 0x00dec144)+0x2e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fxjs\cjs\_runtime.cpp @ 176]  

1b 00dec020 65414a31 chrome!CJS\_EventContext::RunScript(class fxcrt::WideString \* script = 0x00dec144)+0x31e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fxjs\cjs\_event\_context.cpp @ 53]  

1c 00dec070 654143c0 chrome!CPDFSDK\_ActionHandler::RunScript(class CPDFSDK\_FormFillEnvironment \* pFormFillEnv = 0x17c9cd60, class fxcrt::WideString \* script = 0x00dec144, class std::function<void (IJS\_EventContext \*)> \* cb = 0x00dec0a8)+0x81 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_actionhandler.cpp @ 546]  

1d 00dec0e8 65413132 chrome!CPDFSDK\_ActionHandler::RunDocumentPageJavaScript(class CPDFSDK\_FormFillEnvironment \* pFormFillEnv = 0x17c9cd60, CPDF\_AAction::AActionType type = ClosePage (0n11), class fxcrt::WideString \* script = 0x00dec144)+0x90 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_actionhandler.cpp @ 465]  

1e 00dec16c 65412fd6 chrome!CPDFSDK\_ActionHandler::ExecuteDocumentPageAction(class CPDF\_Action \* action = 0x00dec20c, CPDF\_AAction::AActionType type = ClosePage (0n11), class CPDFSDK\_FormFillEnvironment \* pFormFillEnv = 0x17c9cd60, class std::set<const CPDF\_Dictionary \*,std::less<const CPDF\_Dictionary \*>,std::allocator<const CPDF\_Dictionary \*> > \* visited = 0x00dec1a8)+0x122 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_actionhandler.cpp @ 190]  

1f 00dec1c0 63e82bf4 chrome!CPDFSDK\_ActionHandler::DoAction\_Page(class CPDF\_Action \* action = 0x00dec20c, CPDF\_AAction::AActionType eType = ClosePage (0n11), class CPDFSDK\_FormFillEnvironment \* pFormFillEnv = 0x17c9cd60)+0x66 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_actionhandler.cpp @ 68]  

20 00dec220 62dc20fa chrome!FORM\_DoPageAAction(struct fpdf\_page\_t\_\_ \* page = 0x17d7de18, struct fpdf\_form\_handle\_t\_\_ \* hHandle = 0x17c9cd60, int aaType = 0n1)+0x164 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\third\_party\pdfium\fpdfsdk\fpdf\_formfill.cpp @ 712]  

21 00dec24c 62daffd2 chrome!chrome\_pdf::PDFiumEngine::SetCurrentPage(int index = 0n2)+0xba [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\pdf\pdfium\pdfium\_engine.cc @ 3391]  

22 00dec338 62db051a chrome!chrome\_pdf::PDFiumEngine::CalculateVisiblePages(void)+0x512 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\pdf\pdfium\pdfium\_engine.cc @ 2845]  

23 00dec378 62dd7cae chrome!chrome\_pdf::PDFiumEngine::ScrolledToYPosition(int position = 0n104)+0x5a [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\pdf\pdfium\pdfium\_engine.cc @ 750]  

24 00dedf08 61521739 chrome!chrome\_pdf::OutOfProcessInstance::HandleMessage(class pp::Var \* message = 0x00dedf30)+0x17be [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\pdf\out\_of\_process\_instance.cc @ 637]  

25 00dedf70 0bf10674 chrome!pp::Messaging\_HandleMessage(int pp\_instance = 0n-1181972555, struct PP\_Var var = struct PP\_Var)+0xb9 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\ppapi\cpp\module.cc @ 141]  

26 00dedfc4 0bf0fe24 ppapi\_proxy!ppapi::CallWhileUnlocked<void,int,PP\_Var,int,PP\_Var>(<function> \* function = 0x61521680, int \* p1 = 0x00dee044, struct PP\_Var \* p2 = 0x00dee018)+0x84 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\ppapi\shared\_impl\proxy\_lock.h @ 136]  

27 00dee03c 0bf10bd1 ppapi\_proxy!ppapi::proxy::PPP\_Messaging\_Proxy::OnMsgHandleMessage(int instance = 0n-1181972555, class ppapi::proxy::SerializedVarReceiveInput message\_data = class ppapi::proxy::SerializedVarReceiveInput)+0x154 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\ppapi\proxy\ppp\_messaging\_proxy.cc @ 110]  

28 00dee084 0bf10b14 ppapi\_proxy!base::DispatchToMethodImpl<ppapi::proxy::PPP\_Messaging\_Proxy \*,void (class ppapi::proxy::PPP\_Messaging\_Proxy \*\* obj = 0x00dee114, <function> \* method = 0x0bf0fcd0, class std::tuple<int,ppapi::proxy::SerializedVar> \* args = 0x00dee170)+0xa1 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\tuple.h @ 52]  

29 00dee0cc 0bf108fa ppapi\_proxy!base::DispatchToMethod<ppapi::proxy::PPP\_Messaging\_Proxy \*,void (class ppapi::proxy::PPP\_Messaging\_Proxy \*\* obj = 0x00dee114, <function> \* method = 0x0bf0fcd0, class std::tuple<int,ppapi::proxy::SerializedVar> \* args = 0x00dee170)+0x74 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\tuple.h @ 60]  

2a 00dee10c 0bf0fc78 ppapi\_proxy!IPC::DispatchToMethod<ppapi::proxy::PPP\_Messaging\_Proxy,void (class ppapi::proxy::PPP\_Messaging\_Proxy \* obj = 0x17d82fa8, <function> \* method = 0x0bf0fcd0, class std::tuple<int,ppapi::proxy::SerializedVar> \* tuple = 0x00dee170)+0x6a [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\ipc\ipc\_message\_templates.h @ 51]  

2b 00dee1ac 0bf0fa3b ppapi\_proxy!IPC::MessageT<PpapiMsg\_PPPMessaging\_HandleMessage\_Meta,std::tuple<int,ppapi::proxy::SerializedVar>,void>::Dispatch<ppapi::proxy::PPP\_Messaging\_Proxy,ppapi::proxy::PPP\_Messaging\_Proxy,void,void (class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\out\chromium\_pdfium\_xfa\_03\_10\message\_support.dll  

msg = 0x17b34710 {size = 0x150}, class ppapi::proxy::PPP\_Messaging\_Proxy \* obj = 0x17d82fa8, class ppapi::proxy::PPP\_Messaging\_Proxy \* sender = 0x17d82fa8, void \* parameter = 0x00000000, <function> \* func = 0x0bf0fcd0)+0x1a8 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\ipc\ipc\_message\_templates.h @ 147]  

2c 00dee210 0be2d511 ppapi\_proxy!ppapi::proxy::PPP\_Messaging\_Proxy::OnMessageReceived(class IPC::Message \* msg = 0x17b34710 {size = 0x150})+0xcb [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\ppapi\proxy\ppp\_messaging\_proxy.cc @ 77]  

2d 00dee308 0be9204b ppapi\_proxy!ppapi::proxy::Dispatcher::OnMessageReceived(class IPC::Message \* msg = 0x17b34710 {size = 0x150})+0x111 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\ppapi\proxy\dispatcher.cc @ 70]  

2e 00dee3d4 687ff723 ppapi\_proxy!ppapi::proxy::PluginDispatcher::OnMessageReceived(class IPC::Message \* msg = 0x17b34710 {size = 0x150})+0x2bb [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\ppapi\proxy\plugin\_dispatcher.cc @ 272]  

2f 00dee3f8 688060cf ipc!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message \* message = 0x17b34710 {size = 0x150})+0x93 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\ipc\ipc\_channel\_proxy.cc @ 320]  

30 00dee420 68805f8c ipc!base::internal::FunctorTraits<void (<function> \* method = 0x687ff690, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* receiver\_ptr = 0x17b34760 [0x68870620] 0x179e5f98 {...}, class IPC::Message \* args = 0x17b34710 {size = 0x150})+0x4f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\bind\_internal.h @ 516]  

31 00dee460 68805eff ipc!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x17b34708, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* args = 0x17b34760 [0x68870620] 0x179e5f98 {...}, class IPC::Message \* args = 0x17b34710 {size = 0x150})+0x7c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\bind\_internal.h @ 616]  

32 00dee484 68805daf ipc!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x17b34708, class std::tuple<scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);),IPC::Message> \* bound = 0x17b34710)+0x6f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\bind\_internal.h @ 689]  

33 00dee4ac 70c4e890 ipc!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x17b346f0)+0x3f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\bind\_internal.h @ 671]  

34 00dee4d0 70cb1053 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\callback.h @ 100]  

35 00dee648 70d44c2f base!base::debug::TaskAnnotator::RunTask(char \* queue\_function = 0x7105bb97 "MessageLoop::PostTask", struct base::PendingTask \* pending\_task = 0x00dee848)+0x433 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\debug\task\_annotator.cc @ 101]  

36 00dee804 70d45129 base!base::MessageLoop::RunTask(struct base::PendingTask \* pending\_task = 0x00dee848)+0x38f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\message\_loop\message\_loop.cc @ 434]  

37 00dee840 70d45608 base!base::MessageLoop::DeferOrRunPendingTask(struct base::PendingTask pending\_task = struct base::PendingTask)+0x49 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\message\_loop\message\_loop.cc @ 448]  

38 00dee948 70d50c71 base!base::MessageLoop::DoWork(void)+0x188 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\message\_loop\message\_loop.cc @ 517]  

39 00dee998 70d44526 base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x00deeed8)+0x51 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\message\_loop\message\_pump\_default.cc @ 37]  

3a 00deeb50 70e16028 base!base::MessageLoop::Run(bool application\_tasks\_allowed = true)+0x1e6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\message\_loop\message\_loop.cc @ 386]  

3b 00deedd8 589b1fcf base!base::RunLoop::Run(void)+0x1e8 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\base\run\_loop.cc @ 102]  

3c 00def170 5cbd41af content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x00def21c)+0x52f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\content\ppapi\_plugin\ppapi\_plugin\_main.cc @ 160]  

3d 00def1a8 5cbd52fa content!content::RunOtherNamedProcessTypeMain(class std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > \* process\_type = 0x00def3b0, struct content::MainFunctionParams \* main\_function\_params = 0x00def21c, class content::ContentMainDelegate \* delegate = 0x00def8e4)+0xaf [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\content\app\content\_main\_runner\_impl.cc @ 564]  

3e 00def3d0 5cbd1a62 content!content::ContentMainRunnerImpl::Run(bool start\_service\_manager\_only = false)+0x3ba [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\content\app\content\_main\_runner\_impl.cc @ 899]  

3f 00def3e8 50463ef3 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x32 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\content\app\content\_service\_manager\_main\_delegate.cc @ 53]  

40 00def800 5cbd3fcc embedder!service\_manager::Main(struct service\_manager::MainParams \* params = 0x00def824)+0x713 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\services\service\_manager\embedder\main.cc @ 472]  

41 00def84c 5f08132f content!content::ContentMain(struct content::ContentMainParams \* params = 0x00def8c4)+0x5c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\content\app\content\_main.cc @ 20]  

42 00def930 0027b9ef chrome!ChromeMain(struct HINSTANCE\_\_ \* instance = 0x00270000, struct sandbox::SandboxInterfaceInfo \* sandbox\_info = 0x00def9c4, int64 exe\_entry\_point\_ticks = 0n1140578957397)+0x1ef [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\chrome\app\chrome\_main.cc @ 102]  

43 00defa68 00271478 chrome\_exe!MainDllLoader::Launch(struct HINSTANCE\_\_ \* instance = 0x00270000, class base::TimeTicks exe\_entry\_point\_ticks = class base::TimeTicks)+0x44f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\chrome\app\main\_dll\_loader\_win.cc @ 201]  

44 00defdbc 004e8c0e chrome\_exe!wWinMain(struct HINSTANCE\_\_ \* instance = 0x00270000, struct HINSTANCE\_\_ \* prev = 0x00000000)+0x478 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\_03\_10\_18\src\chrome\app\chrome\_exe\_main\_win.cc @ 229]  

45 00defdd4 004e8d61 chrome\_exe!invoke\_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 123]  

46 00defe2c 004e8e2d chrome\_exe!\_\_scrt\_common\_main\_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 283]  

47 00defe34 004e8e38 chrome\_exe!\_\_scrt\_common\_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 326]  

48 00defe3c 740a8484 chrome\_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_wwinmain.cpp @ 17]  

49 00defe50 7704305a KERNEL32!BaseThreadInitThunk+0x24  

4a 00defe98 7704302a ntdll\_76fe0000!\_\_RtlUserThreadStart+0x2f  

4b 00defea8 00000000 ntdll\_76fe0000!\_RtlUserThreadStart+0x1b

## Attachments

- [poc_controlEIP.pdf](attachments/poc_controlEIP.pdf) (application/pdf, 5.5 KB)
- [stacktrace_NoPageHeap.txt](attachments/stacktrace_NoPageHeap.txt) (text/plain, 21.0 KB)
- [stacktrace_PageHeap.txt](attachments/stacktrace_PageHeap.txt) (text/plain, 21.9 KB)
- [bug_898531.in](attachments/bug_898531.in) (application/octet-stream, 2.5 KB)
- [bug_898531.txt](attachments/bug_898531.txt) (text/plain, 23.0 KB)

## Timeline

### th...@chromium.org (2018-10-24)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2018-10-24)

XFA not shipping => impact none.

[Monorail components: -Internals>Plugins>PDF]

### ts...@chromium.org (2018-10-24)

Requires chrome, not just pdfium_test.

### hu...@gmail.com (2018-10-24)

I think this bug can be triggered with chrome WITHOUT XFA enable. I'm building the lastest chromium to test this.

### hu...@gmail.com (2018-10-24)

Here is the stacktrace when run poc file on Chrome Version 70.0.3538.67 (Official Build) (64-bit)

5:099> r
rax=00007ff816495260 rbx=000002d8eeb65850 rcx=000002d8eeb65850
rdx=000002d8ecf66ac0 rsi=000002d8eeb65850 rdi=000002d8efccfbb0
rip=0000000000000064 rsp=000000dfe05fcd28 rbp=0000000000000001
 r8=0000000000000201  r9=00000000000003b8 r10=00000000000002b1
r11=0000000000000445 r12=00007ff816b98dd0 r13=000002d8ecf3c4a0
r14=000002d8edfbee00 r15=000002d8edfa2400
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
00000000`00000064 ??              ???

5:099> kp
 # Child-SP          RetAddr           Call Site
00 000000df`e05fcd28 00007ff8`1607a821 0x64
01 000000df`e05fcd30 00007ff8`15e62fda chrome_child!CPWL_Wnd::Destroy(void)+0x1f [C:\b\c\b\win64_clang\src\third_party\pdfium\fpdfsdk\pwl\cpwl_wnd.cpp @ 178] 
02 000000df`e05fcd70 00007ff8`1607ceca chrome_child!CFFL_FormFiller::DestroyPDFWindow(class CPDFSDK_PageView * pPageView = <Value unavailable error>)+0x74 [C:\b\c\b\win64_clang\src\third_party\pdfium\fpdfsdk\formfiller\cffl_formfiller.cpp @ 419] 
03 000000df`e05fcdd0 00007ff8`15e62bb2 chrome_child!CFFL_TextObject::ResetPDFWindow(class CPDFSDK_PageView * pPageView = 0x000002d8`ecf27010, bool bRestoreValue = false)+0x5a [C:\b\c\b\win64_clang\src\third_party\pdfium\fpdfsdk\formfiller\cffl_textobject.cpp @ 18] 
04 000000df`e05fce50 00007ff8`15e62a25 chrome_child!CFFL_FormFiller::CommitData(class CPDFSDK_PageView * pPageView = 0x000002d8`ecf27010, unsigned int nFlag = 0)+0x13e [C:\b\c\b\win64_clang\src\third_party\pdfium\fpdfsdk\formfiller\cffl_formfiller.cpp @ 0] 
05 000000df`e05fcef0 00007ff8`15a9a98d chrome_child!CFFL_FormFiller::KillFocusForAnnot(class CPDFSDK_Annot * pAnnot = <Value unavailable error>, unsigned int nFlag = 0)+0x41 [C:\b\c\b\win64_clang\src\third_party\pdfium\fpdfsdk\formfiller\cffl_formfiller.cpp @ 309] 
06 000000df`e05fcf30 00007ff8`156fe8a0 chrome_child!CFFL_InteractiveFormFiller::OnKillFocus(class fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr * pAnnot = 0x000000df`e05fd008, unsigned int nFlag = <Value unavailable error>)+0x5b [C:\b\c\b\win64_clang\src\third_party\pdfium\fpdfsdk\formfiller\cffl_interactiveformfiller.cpp @ 422] 
07 000000df`e05fcfe0 00007ff8`156fef03 chrome_child!CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int nFlag = <Value unavailable error>)+0xa4 [C:\b\c\b\win64_clang\src\third_party\pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp @ 0] 
08 000000df`e05fd070 00007ff8`15e2f0a0 chrome_child!CPDFSDK_FormFillEnvironment::SetFocusAnnot(class fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr * pAnnot = 0x000000df`e05fd0e8)+0x3f [C:\b\c\b\win64_clang\src\third_party\pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp @ 653] 
09 000000df`e05fd0b0 00007ff8`15e34212 chrome_child!CJS_Field::setFocus(class CJS_Runtime * pRuntime = <Value unavailable error>, class std::vector<v8::Local<v8::Value>,std::allocator<v8::Local<v8::Value> > > * params = <Value unavailable error>)+0xc6 [C:\b\c\b\win64_clang\src\third_party\pdfium\fxjs\cjs_field.cpp @ 2536] 
0a 000000df`e05fd160 00007ff8`128c13ac chrome_child!JSMethod<CJS_Field,&CJS_Field::setFocus>(char * method_name_string = 0x00007ff8`16e4b99b "setFocus", char * class_name_string = 0x00007ff8`16e4bbd0 "Field", class v8::FunctionCallbackInfo<v8::Value> * info = 0x000000df`e05fd2d0)+0xe1 [C:\b\c\b\win64_clang\src\third_party\pdfium\fxjs\js_define.h @ 137] 
0b 000000df`e05fd220 00007ff8`135b43cd chrome_child!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo * handler = <Value unavailable error>)+0x24c [C:\b\c\b\win64_clang\src\v8\src\api-arguments-inl.h @ 120] 
0c 000000df`e05fd340 00007ff8`135b3ed1 chrome_child!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate * isolate = 0x000002d8`ecf4f680, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = <Value unavailable error>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments * args = 0x000000df`e05fd480)+0x1ed [C:\b\c\b\win64_clang\src\v8\src\builtins\builtins-api.cc @ 111] 
0d 000000df`e05fd440 00007ff8`128c0ef1 chrome_child!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments * args = 0x00000000`00000005, class v8::internal::Isolate * isolate = 0x000002d8`ecf4f680)+0x111 [C:\b\c\b\win64_clang\src\v8\src\builtins\builtins-api.cc @ 0] 
0e 000000df`e05fd500 00007ff8`13baa4f2 chrome_child!v8::internal::Builtin_HandleApiCall(int args_length = 0n5, class v8::internal::Object ** args_object = 0x000000df`e05fd5e0, class v8::internal::Isolate * isolate = 0x000002d8`ecf4f680)+0x41 [C:\b\c\b\win64_clang\src\v8\src\builtins\builtins-api.cc @ 127] 
0f 000000df`e05fd560 00000000`00000006 chrome_child!v8::internal::NativesCollection<v8::internal::EXPERIMENTAL_EXTRAS>::GetScriptName+0x92f52
10 000000df`e05fd568 000000df`e05fd5d8 0x6
11 000000df`e05fd570 0000027d`1c1854cc 0x000000df`e05fd5d8
12 000000df`e05fd578 00002a8c`bcd315f9 0x0000027d`1c1854cc
13 000000df`e05fd580 00002a8c`bcd5d269 0x00002a8c`bcd315f9
14 000000df`e05fd588 0000799d`36df80e1 0x00002a8c`bcd5d269
15 000000df`e05fd590 00000000`00000018 0x0000799d`36df80e1
16 000000df`e05fd598 0000027d`1c1191c1 0x18
17 000000df`e05fd5a0 000000df`e05fd560 0x0000027d`1c1191c1
18 000000df`e05fd5a8 00000000`00000006 0x000000df`e05fd560
19 000000df`e05fd5b0 000000df`e05fd640 0x6
1a 000000df`e05fd5b8 0000027d`1c1087bf 0x000000df`e05fd640
1b 000000df`e05fd5c0 00005819`f5a825b1 0x0000027d`1c1087bf
1c 000000df`e05fd5c8 00002a8c`bcd60511 0x00005819`f5a825b1
1d 000000df`e05fd5d0 00000005`00000000 0x00002a8c`bcd60511
1e 000000df`e05fd5d8 00005819`f5a82691 0x00000005`00000000
1f 000000df`e05fd5e0 000004d5`03902309 0x00005819`f5a82691
20 000000df`e05fd5e8 00002a8c`bcd52fb1 0x000004d5`03902309
21 000000df`e05fd5f0 00002a8c`bcd5d269 0x00002a8c`bcd52fb1
22 000000df`e05fd5f8 000004d5`03902309 0x00002a8c`bcd5d269
23 000000df`e05fd600 000004d5`03902309 0x000004d5`03902309
24 000000df`e05fd608 00002a8c`bcd60511 0x000004d5`03902309
25 000000df`e05fd610 00002a8c`bcd315f9 0x00002a8c`bcd60511
26 000000df`e05fd618 00005819`f5a825b1 0x00002a8c`bcd315f9
27 000000df`e05fd620 00000067`00000000 0x00005819`f5a825b1
28 000000df`e05fd628 00002a8c`bcd62451 0x00000067`00000000
29 000000df`e05fd630 00002a8c`bcd62511 0x00002a8c`bcd62451
2a 000000df`e05fd638 00002a8c`bcd315f9 0x00002a8c`bcd62511
2b 000000df`e05fd640 000000df`e05fd668 0x00002a8c`bcd315f9
2c 000000df`e05fd648 00007ff8`13b1d4a4 0x000000df`e05fd668
2d 000000df`e05fd650 0000485c`f0e04a51 chrome_child!v8::internal::NativesCollection<v8::internal::EXPERIMENTAL_EXTRAS>::GetScriptName+0x5f04
2e 000000df`e05fd658 00002a8c`bcd62511 0x0000485c`f0e04a51
2f 000000df`e05fd660 00000000`00000020 0x00002a8c`bcd62511
30 000000df`e05fd668 000000df`e05fd780 0x20
31 000000df`e05fd670 0000027d`1c106bd2 0x000000df`e05fd780
32 000000df`e05fd678 00000000`00000000 0x0000027d`1c106bd2


### hu...@gmail.com (2018-10-24)

I'm working on spraying to control EIP on chrome without XFA enabled. 

### ts...@chromium.org (2018-10-24)

We'll assume you can get EIP and call it impact stable for now.

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2018-10-24)

Minimize testcase that works in non-xfa attached.

### ts...@chromium.org (2018-10-24)

Stack trace showing re-entrancy from C -> JS -> C-> JS -> C.

### bu...@chromium.org (2018-10-24)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/333165a2c7b7812effdea3cd1ae386850cd3f310

commit 333165a2c7b7812effdea3cd1ae386850cd3f310
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Oct 24 23:56:43 2018

Fix CPLW_Wnd ownership model in CFFL_FormFiller.

CFFL_FormFiller::DestroyPDFWindow() might get re-entered, so
do not leave any dangling references in maps. Use unique_ptr
to be more sure that we have it right.

Bug: chromium:898531
Change-Id: I7b61940ff4e88c8a7e3219fefb0479f33bbbfae1
Reviewed-on: https://pdfium-review.googlesource.com/c/44542
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_combobox.h
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_formfiller.h
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_formfiller.cpp
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_pushbutton.cpp
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_checkbox.h
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_textfield.cpp
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_listbox.h
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_listbox.cpp
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_pushbutton.h
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_radiobutton.h
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_textfield.h
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_checkbox.cpp
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_radiobutton.cpp
[modify] https://crrev.com/333165a2c7b7812effdea3cd1ae386850cd3f310/fpdfsdk/formfiller/cffl_combobox.cpp


### bu...@chromium.org (2018-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5141c56ec8df7234c01e2576d35dd5c56238d069

commit 5141c56ec8df7234c01e2576d35dd5c56238d069
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Oct 25 02:58:20 2018

Roll src/third_party/pdfium e835574db56d..333165a2c7b7 (6 commits)

https://pdfium.googlesource.com/pdfium.git/+log/e835574db56d..333165a2c7b7


git log e835574db56d..333165a2c7b7 --date=short --no-merges --format='%ad %ae %s'
2018-10-24 tsepez@chromium.org Fix CPLW_Wnd ownership model in CFFL_FormFiller.
2018-10-24 thestig@chromium.org Clean up CFX_ImageTransformer parameters.
2018-10-24 thestig@chromium.org Remove FXDIB_BLEND_UNSUPPORTED.
2018-10-24 thestig@chromium.org Initialize CPDF_GeneralState::StateData in the header.
2018-10-24 thestig@chromium.org Use ASSERT() consistently. Replace assert() usage.
2018-10-24 thestig@chromium.org Assert CPDF_Image::m_pDocument is never nullptr.


Created with:
  gclient setdep -r src/third_party/pdfium@333165a2c7b7

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:898531
TBR=dsinclair@chromium.org

Change-Id: I943bf7e494b5ae34f5ae7371477f845d78d7271d
Reviewed-on: https://chromium-review.googlesource.com/c/1298283
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#602592}
[modify] https://crrev.com/5141c56ec8df7234c01e2576d35dd5c56238d069/DEPS


### oc...@chromium.org (2018-10-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-10-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-28)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-10-29)

+awhalley@ (Security TPM) for M71 merge review.

### aw...@google.com (2018-10-30)

[Comment Deleted]

### aw...@google.com (2018-10-30)

govind@ - good for 71

### go...@chromium.org (2018-10-30)

Approving merge to M71 branch 3578 based on https://crbug.com/chromium/898531#c21. Pls merge befor 1:00 PM PT today so we can pick it up for tomorrow's beta release. Thank you.

### bu...@chromium.org (2018-10-30)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/6cb2ade2e0541330d00143c5fe32a60eac0c842e

commit 6cb2ade2e0541330d00143c5fe32a60eac0c842e
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Oct 30 16:44:06 2018

Fix CPLW_Wnd ownership model in CFFL_FormFiller.

CFFL_FormFiller::DestroyPDFWindow() might get re-entered, so
do not leave any dangling references in maps. Use unique_ptr
to be more sure that we have it right.

Bug: chromium:898531
Change-Id: I7b61940ff4e88c8a7e3219fefb0479f33bbbfae1
Reviewed-on: https://pdfium-review.googlesource.com/c/44542
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 333165a2c7b7812effdea3cd1ae386850cd3f310)
Reviewed-on: https://pdfium-review.googlesource.com/c/44870
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_combobox.h
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_formfiller.h
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_formfiller.cpp
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_pushbutton.cpp
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_checkbox.h
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_textfield.cpp
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_listbox.h
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_listbox.cpp
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_pushbutton.h
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_radiobutton.h
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_textfield.h
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_checkbox.cpp
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_radiobutton.cpp
[modify] https://crrev.com/6cb2ade2e0541330d00143c5fe32a60eac0c842e/fpdfsdk/formfiller/cffl_combobox.cpp


### aw...@chromium.org (2018-10-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-02)

Nice one huyna89@! The VRP panel decided to award $5,000 for this report :-)

### aw...@google.com (2018-11-02)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/898531?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092844)*
