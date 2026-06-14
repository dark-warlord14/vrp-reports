# Security: PDFium (XFA) Use-after-free in CJX_HostPseudoModel::openList

| Field | Value |
|-------|-------|
| **Issue ID** | [40095983](https://issues.chromium.org/issues/40095983) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2019-08-13 |
| **Bounty** | $9,500.00 |

## Description

**VULNERABILITY DETAILS**  

CXFA\_FFWidget object use-after-free in function CJX\_HostPseudoModel::openList.

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe with PageHeap is enabled.  

Scroll to the second page and click RIGHT mouse button to a combobox `Field 6` to trigger crash.

DETAIL INFORMATION

This bug is in function `CJX_HostPseudoModel::openList`

```
CJS_Result CJX_HostPseudoModel::openList(  
    CFX_V8\* runtime,  
    const std::vector<v8::Local<v8::Value>>& params) {  
  if (!GetDocument()->GetScriptContext()->IsRunAtClient())  
    return CJS_Result::Success();  
  
... (skip)  
  
  if (!pNode)  
    return CJS_Result::Success();  
  
  auto\* pDocLayout = CXFA_LayoutProcessor::FromDocument(GetDocument());  
  CXFA_LayoutItem\* pLayoutItem = pDocLayout->GetLayoutItem(pNode);  
  if (!pLayoutItem)  
    return CJS_Result::Success();  
  
  CXFA_FFWidget\* hWidget = XFA_GetWidgetFromLayoutItem(pLayoutItem);  
  if (!hWidget)  
    return CJS_Result::Success();  
  
  CXFA_FFDoc\* hDoc = pNotify->GetHDOC();  
  hDoc->GetDocEnvironment()->SetFocusWidget(hDoc, hWidget);		// => trigger JS to destroy |CXFA_FFWidget| object!!!  
  pNotify->OpenDropDownList(hWidget);  
  return CJS_Result::Success();  
}  

```

Function `SetFocusWidget` can trigger the JS callback that can destroy widget object `hWidget`. This object is used again in function `OpenDropDownList`

CRASH INFORMATION

```
(3eb0.45cc): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
eax=3ea92fb4 ebx=43b6afd8 ecx=3ea92fb4 edx=3ea92f98 esi=2ef92bb0 edi=2b3b8f98  
eip=2e81716a esp=0097c2e8 ebp=0097c2ec iopl=0         nv up ei pl nz ac pe nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010216  
pdfium!fxcrt::UnownedPtr<CXFA_Node>::Get+0xa:  
2e81716a 8b00            mov     eax,dword ptr [eax]  ds:002b:3ea92fb4=????????  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\v8.dll  
3:058> kp  
 # ChildEBP RetAddr    
00 0097c2ec 2e814564 pdfium!fxcrt::UnownedPtr<CXFA_Node>::Get(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 91]   
01 0097c2f8 2e9c996f pdfium!CXFA_FFWidget::GetNode(void)+0x14 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.h @ 132]   
02 0097c314 2e96f5f5 pdfium!CXFA_FFNotify::OpenDropDownList(class CXFA_FFWidget \* hWidget = 0x3ea92f98)+0x1f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 254]   
03 0097c3dc 2e96dffe pdfium!CJX_HostPseudoModel::openList(class CFX_V8 \* runtime = 0x2b3b8f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0097c4fc { size=1 })+0x445 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 316]   
04 0097c414 2e97d9e3 pdfium!CJX_HostPseudoModel::openList_static(class CJX_Object \* node = 0x43b6afd8, class CFX_V8 \* runtime = 0x2b3b8f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0097c4fc { size=1 })+0x7e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 33]   
05 0097c46c 2e92788e pdfium!CJX_Object::RunMethod(class fxcrt::WideString \* func = 0x0097c66c, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0097c4fc { size=1 })+0x103 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 179]   
06 0097c51c 2e9218c2 pdfium!CFXJSE_Engine::NormalMethodCall(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x0097c6d8, class fxcrt::WideString \* functionName = 0x0097c66c)+0x20e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 459]   
07 0097c6bc 1f8db0a3 pdfium!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x0097c6d8)+0x3c2 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111]   
08 0097c72c 1f8d9bd8 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x253 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api-arguments-inl.h @ 158]   
09 0097c798 1f8d8426 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x308 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 113]   
0a 0097c7e8 1f8d7ff2 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x42188af8)+0x166 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 141]   
0b 0097c860 20673ac3 v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n6, unsigned int \* args_object = 0x0097c898, class v8::internal::Isolate \* isolate = 0x42188af8)+0x72 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 129]   
0c 0097c87c 20460ddc v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x43  
0d 0097c8bc 2044d1fc v8!Builtins_InterpreterEntryTrampoline+0x31c  
0e 0097c8d8 20460ddc v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
0f 0097c920 2044d1fc v8!Builtins_InterpreterEntryTrampoline+0x31c  
10 0097c93c 2045895f v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
11 0097c954 2045877b v8!Builtins_JSEntryTrampoline+0x5f  
12 0097c980 1fa097a4 v8!Builtins_JSEntry+0x5b  
13 (Inline) -------- v8!v8::internal::GeneratedCode<unsigned int,unsigned int,unsigned int,unsigned int,unsigned int,int,unsigned int \*\*>::Call+0xf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\simulator.h @ 138]   
14 0097ca3c 1fa08f8e v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = <Value unavailable error>, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x0097ca48)+0x804 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 266]   
15 0097ca80 1f8339fb v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x42188af8, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n1, class v8::internal::Handle<v8::internal::Object> \* argv = 0x0097ce74)+0x6e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 358]   
16 0097cb38 2e92411d v8!v8::Function::Call(class v8::Local<v8::Context> context = class v8::Local<v8::Context>, class v8::Local<v8::Value> recv = class v8::Local<v8::Value>, int argc = 0n1, class v8::Local<v8::Value> \* argv = 0x0097ce74)+0x2fb [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api.cc @ 4822]   
17 0097ce88 2e929569 pdfium!CFXJSE_Context::ExecuteScript(char \* szScript = 0x4374801c ".    xfa_log_print("|field6| enter: BEGIN");..    f0 = xfa.resolveNode("xfa.form..field0");.    xfa_log_print("xfa.host.openList(f0);");.    xfa.host.openList(f0);..    xfa_log_print("|field6| enter: END");.", class CFXJSE_Value \* lpRetValue = 0x3adfcff0, class CFXJSE_Value \* lpNewThisObject = 0x3a988ff0)+0xa0d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_context.cpp @ 300]   
18 0097cf68 2ea5bace pdfium!CFXJSE_Engine::RunScript(CXFA_Script::Type eScriptType = Javascript (0n1), class fxcrt::StringViewTemplate<wchar_t> wsScript = class fxcrt::StringViewTemplate<wchar_t>, class CFXJSE_Value \* hRetValue = 0x3adfcff0, class CXFA_Object \* pThisObject = 0x3d0e8f80)+0x349 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 153]   
19 0097d078 2ea59992 pdfium!CXFA_Node::ExecuteBoolScript(class CXFA_FFDocView \* pDocView = 0x3bd22f60, class CXFA_Script \* script = 0x3d170f80, class CXFA_EventParam \* pEventParam = 0x0097d1b0)+0x33e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2700]   
1a 0097d0c0 2ea598e5 pdfium!CXFA_Node::ExecuteScript(class CXFA_FFDocView \* pDocView = 0x3bd22f60, class CXFA_Script \* script = 0x3d170f80, class CXFA_EventParam \* pEventParam = 0x0097d1b0)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2660]   
1b 0097d0f4 2ea5948f pdfium!CXFA_Node::ProcessEventInternal(class CXFA_FFDocView \* pDocView = 0x3bd22f60, XFA_AttributeValue iActivity = Enter (0n233), class CXFA_Event \* event = 0x3d16cf80, class CXFA_EventParam \* pEventParam = 0x0097d1b0)+0xe5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2360]   
1c 0097d168 2e9e23f4 pdfium!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* pDocView = 0x3bd22f60, XFA_AttributeValue iActivity = Enter (0n233), class CXFA_EventParam \* pEventParam = 0x0097d1b0)+0x10f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2336]   
1d 0097d1f4 2e9c1a60 pdfium!CXFA_FFWidget::OnSetFocus(class CXFA_FFWidget \* pOldWidget = 0x3eb5efa0)+0x144 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 412]   
1e 0097d23c 2e9b9c78 pdfium!CXFA_FFField::OnSetFocus(class CXFA_FFWidget \* pOldWidget = 0x3eb5efa0)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fffield.cpp @ 502]   
1f 0097d298 2e85489b pdfium!CXFA_FFDocView::SetFocus(class CXFA_FFWidget \* pNewFocus = 0x3f13ef98)+0x188 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 296]   
20 0097d2ec 2e7dfcb5 pdfium!CPDFSDK_XFAWidgetHandler::OnXFAChangedFocus(class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pOldAnnot = 0x0097d36c, class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pNewAnnot = 0x0097d3a8)+0x14b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_xfawidgethandler.cpp @ 541]   
21 0097d32c 2e802893 pdfium!CPDFSDK_AnnotHandlerMgr::Annot_OnChangeFocus(class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pSetAnnot = 0x0097d3a8, class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pKillAnnot = 0x0097d36c)+0xe5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_annothandlermgr.cpp @ 289]   
22 0097d378 2e8115e3 pdfium!CPDFSDK_FormFillEnvironment::SetFocusAnnot(class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pAnnot = 0x0097d3a8)+0x153 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp @ 654]   
23 0097d3b8 2e836c38 pdfium!CPDFSDK_PageView::OnFocus(class CFX_PTemplate<float> \* point = 0x0097d3fc, unsigned int nFlag = 0)+0xa3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_pageview.cpp @ 296]   
24 0097d410 1a614076 pdfium!FORM_OnFocus(struct fpdf_form_handle_t__ \* hHandle = 0x3f5a2fb8, struct fpdf_page_t__ \* page = 0x3fed8fe8, int modifier = 0n0, double page_x = 128.2499847412109375, double page_y = 26.999998092651367188)+0xc8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdf_formfill.cpp @ 391]   
25 0097d784 1a610d4d chrome!chrome_pdf::PDFiumEngine::OnRightMouseDown(class pp::MouseInputEvent \* event = 0x0097d7b4)+0x606 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 1182]   
26 0097d7c8 1a61084d chrome!chrome_pdf::PDFiumEngine::OnMouseDown(class pp::MouseInputEvent \* event = 0x0097d91c)+0xcd [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 996]   
27 0097d9d0 1a6357cd chrome!chrome_pdf::PDFiumEngine::HandleEvent(class pp::InputEvent \* event = 0x0097db40)+0x12d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 766]   
28 0097db54 18dd6046 chrome!chrome_pdf::OutOfProcessInstance::HandleInputEvent(class pp::InputEvent \* event = 0x0097db84)+0x60d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\out_of_process_instance.cc @ 838]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ppapi_proxy.dll  
29 0097db94 5013a457 chrome!pp::InputEvent_HandleEvent(int pp_instance = 0n1967730785, int resource = 0n654)+0x96 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\cpp\module.cc @ 53]   
2a 0097dbc4 5013a3ea ppapi_proxy!ppapi::CallWhileUnlocked<PP_Bool,int,int,int,int>(<function> \* function = 0x18dd5fb0, int \* p1 = 0x0097dc18, int \* p2 = 0x0097dbfc)+0x47 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\shared_impl\proxy_lock.h @ 136]   
2b 0097dc10 5013ad8e ppapi_proxy!ppapi::proxy::PPP_InputEvent_Proxy::OnMsgHandleFilteredInputEvent(int instance = 0n1967730785, struct ppapi::InputEventData \* data = 0x0097dde8, <unnamed-tag> \* result = 0x0097dd38)+0xaa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\ppp_input_event_proxy.cc @ 107]   
2c 0097dc54 5013acb8 ppapi_proxy!base::DispatchToMethodImpl<ppapi::proxy::PPP_InputEvent_Proxy \*,void (class ppapi::proxy::PPP_InputEvent_Proxy \*\* obj = 0x0097debc, <function> \* method = 0x5013a340, class std::__1::tuple<int,ppapi::InputEventData> \* in = 0x0097dde0, class std::__1::tuple<PP_Bool> \* out = 0x0097dd38)+0x8e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\tuple.h @ 96]   
2d 0097dcb8 5013a2ac ppapi_proxy!base::DispatchToMethod<ppapi::proxy::PPP_InputEvent_Proxy \*,void (class ppapi::proxy::PPP_InputEvent_Proxy \*\* obj = 0x0097debc, <function> \* method = 0x5013a340, class std::__1::tuple<int,ppapi::InputEventData> \* in = 0x0097dde0, class std::__1::tuple<PP_Bool> \* out = 0x0097dd38)+0x98 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\tuple.h @ 105]   
2e 0097deb0 50139c7d ppapi_proxy!IPC::MessageT<PpapiMsg_PPPInputEvent_HandleFilteredInputEvent_Meta,std::__1::tuple<int,ppapi::InputEventData>,std::__1::tuple<PP_Bool> >::Dispatch<ppapi::proxy::PPP_InputEvent_Proxy,ppapi::proxy::PPP_InputEvent_Proxy,void,void (class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\message_support.dll  
msg = 0x31234fb8 {size = 0x90}, class ppapi::proxy::PPP_InputEvent_Proxy \* obj = 0x4128efe8, class ppapi::proxy::PPP_InputEvent_Proxy \* sender = 0x4128efe8, <function> \* func = 0x5013a340)+0x2cc [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ipc\ipc_message_templates.h @ 205]   
2f 0097df28 50079627 ppapi_proxy!ppapi::proxy::PPP_InputEvent_Proxy::OnMessageReceived(class IPC::Message \* msg = 0x31234fb8 {size = 0x90})+0x14d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\ppp_input_event_proxy.cc @ 85]   
30 0097e004 500d5aa5 ppapi_proxy!ppapi::proxy::Dispatcher::OnMessageReceived(class IPC::Message \* msg = 0x31234fb8 {size = 0x90})+0x127 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\dispatcher.cc @ 70]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ipc.dll  
31 0097e0d8 628f8a1f ppapi_proxy!ppapi::proxy::PluginDispatcher::OnMessageReceived(class IPC::Message \* msg = 0x31234fb8 {size = 0x90})+0x2f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\plugin_dispatcher.cc @ 273]   
32 0097e0f8 628feb3f ipc!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message \* message = 0x31234fb8 {size = 0x90})+0x8f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ipc\ipc_channel_proxy.cc @ 323]   
33 0097e120 628fea1c ipc!base::internal::FunctorTraits<void (<function> \* method = 0x628f8990, class scoped_refptr<IPC::ChannelProxy::Context> \* receiver_ptr = 0x31234fb0 [0x629510d0] 0x41908f10 {...}, class IPC::Message \* args = 0x31234fb8 {size = 0x90})+0x4f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 499]   
34 0097e160 628fe94f ipc!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x31234fa8, class scoped_refptr<IPC::ChannelProxy::Context> \* args = 0x31234fb0 [0x629510d0] 0x41908f10 {...}, class IPC::Message \* args = 0x31234fb8 {size = 0x90})+0x7c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 599]   
35 0097e184 628fe804 ipc!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x31234fa8, class std::__1::tuple<scoped_refptr<IPC::ChannelProxy::Context>,IPC::Message> \* bound = 0x31234fb0)+0x6f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 672]   
36 0097e1ac 67821bb0 ipc!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x31234f90)+0x54 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 641]   
37 0097e1d0 679f9963 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 99]   
38 0097e458 67a50ed5 base!base::TaskAnnotator::RunTask(char \* trace_event_name = 0x67be321c "SequenceManager RunTask", struct base::PendingTask \* pending_task = 0x0097e7a0)+0x5b3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\common\task_annotator.cc @ 144]   
39 0097e810 67a50501 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow \* continuation_lazy_now = 0x0097e8b0, bool \* ran_task = 0x0097e8cb)+0x735 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 365]   
3a 0097e8d8 678e2300 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xb1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 218]   
3b 0097e938 67a5230c base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x3dd48f2c)+0x60 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_pump_default.cc @ 39]   
3c 0097ebcc 6798b535 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application_tasks_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x34c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 463]   
3d 0097edd0 6798b1e5 base!base::RunLoop::RunWithTimeout(class base::TimeDelta timeout = 9223372036854775807)+0x335 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 160]   
3e 0097edfc 5c955a9a base!base::RunLoop::Run(void)+0x45 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 135]   
3f 0097efe8 6068aeb6 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x0097f05c)+0x5ca [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 160]   
40 0097f014 6068bf05 content!content::RunOtherNamedProcessTypeMain(class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* process_type = 0x0097f078 "ppapi", struct content::MainFunctionParams \* main_function_params = 0x0097f05c, class content::ContentMainDelegate \* delegate = 0x0097f64c)+0xa6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 578]   
41 0097f1d0 606877f0 content!content::ContentMainRunnerImpl::Run(bool start_service_manager_only = false)+0x2c5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 871]   
42 0097f1e8 346222e1 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_service_manager_main_delegate.cc @ 52]   
43 0097f568 6068acdc embedder!service_manager::Main(struct service_manager::MainParams \* params = 0x0097f58c)+0x6d1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\services\service_manager\embedder\main.cc @ 423]   
44 0097f5b4 16711315 content!content::ContentMain(struct content::ContentMainParams \* params = 0x0097f62c)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main.cc @ 20]   
45 0097f690 00ab8e33 chrome!ChromeMain(struct HINSTANCE__ \* instance = 0x00ab0000, struct sandbox::SandboxInterfaceInfo \* sandbox_info = 0x0097f724, int64 exe_entry_point_ticks = 0n616507392072)+0x1f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_main.cc @ 110]   
46 0097f788 00ab147f chrome_exe!MainDllLoader::Launch(struct HINSTANCE__ \* instance = 0x00ab0000, class base::TimeTicks exe_entry_point_ticks = class base::TimeTicks)+0x453 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\main_dll_loader_win.cc @ 202]   
47 0097fa68 00ce6efe chrome_exe!wWinMain(struct HINSTANCE__ \* instance = 0x00ab0000, struct HINSTANCE__ \* prev = 0x00000000)+0x47f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_exe_main_win.cc @ 234]   
48 0097fa80 00ce7051 chrome_exe!invoke_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123]   
49 0097fad8 00ce711d chrome_exe!__scrt_common_main_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283]   
4a 0097fae0 00ce7128 chrome_exe!__scrt_common_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 326]   
4b 0097fae8 74d90419 chrome_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17]   
4c 0097faf8 7774662d KERNEL32!BaseThreadInitThunk+0x19  
4d 0097fb54 777465fd ntdll!__RtlUserThreadStart+0x2f  
4e 0097fb64 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 8.7 KB)
- [image_poc_doc.png](attachments/image_poc_doc.png) (image/png, 23.7 KB)
- [crash_info.txt](attachments/crash_info.txt) (text/plain, 26.6 KB)

## Timeline

### cl...@chromium.org (2019-08-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5138198901948416.

### cl...@chromium.org (2019-08-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-08-13)

Testcase 5138198901948416 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5138198901948416.

### mm...@chromium.org (2019-08-13)

Thanks for your report. I see only one page in the PDF you've attached. Is that a correct reproducer?

### hu...@gmail.com (2019-08-14)

This bug is only triggered when chromium is built with XFA is enabled! When XFA is on, the page is something like image i attach below. 
- The first page contains 2 field: "field 3" and combobox "Single"
- The second page contains 1 field: combo-box "Field 6" 

I also attach the full information when application is crashed (Context, Full stacktrace when crash, PageHeap stacktrace when object is freed).

### sh...@chromium.org (2019-08-14)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-08-14)

Ok, thanks for the info!

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/dd97e79717c83fdd68d6fb8134348060f2884b40

commit dd97e79717c83fdd68d6fb8134348060f2884b40
Author: huyna <huyna89@gmail.com>
Date: Thu Aug 22 18:22:33 2019

Observe CXFA_FFWidget across a function SetFocusWidget().

CXFA_FFWidget object is destroyed by JS code of field's exit event
triggered by calling SetFocusWidget().
Use ObservedPtr to catch this destruction.

Bug: chromium:993553
Change-Id: I694d63bb62cd01e4a9a038afdcd009425b0284b5
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/59410
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/dd97e79717c83fdd68d6fb8134348060f2884b40/fxjs/xfa/cjx_hostpseudomodel.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c5f766481b18df773690dd7c8df7be8ebd19c64f

commit c5f766481b18df773690dd7c8df7be8ebd19c64f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Aug 23 08:17:53 2019

Roll src/third_party/pdfium 88c370baef61..cf9147a73748 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/88c370baef61..cf9147a73748

git log 88c370baef61..cf9147a73748 --date=short --no-merges --format='%ad %ae %s'
2019-08-22 nigi@chromium.org [SkiaPaths] Fix missing texts in 5.5_simple_font.pdf.
2019-08-22 huyna89@gmail.com Observe CXFA_FFWidget across a function SetFocusWidget().

Created with:
  gclient setdep -r src/third_party/pdfium@cf9147a73748

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:993553
Change-Id: I3224d90bf848658f0fb594212125068095a8bd73
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1767499
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#689841}

[modify] https://crrev.com/c5f766481b18df773690dd7c8df7be8ebd19c64f/DEPS


### th...@chromium.org (2019-08-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-23)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-28)

Nice one! The Panel decided to reward $7,500 + $2,000 patch bonus for this report! 

### na...@google.com (2019-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-29)

This issue was migrated from crbug.com/chromium/993553?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095983)*
