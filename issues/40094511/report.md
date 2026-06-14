# Use-after-free in CXFA_FFComboBox::OnProcessEvent                                                                                                

| Field | Value |
|-------|-------|
| **Issue ID** | [40094511](https://issues.chromium.org/issues/40094511) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-04-05 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CXFA\_FFComboBox::OnProcessEvent

**VERSION**  

Operating System: Windows 10  

chrome with pdfium XFA enabled

**REPRODUCTION CASE**

1. Build chrome with XFA enabled + enable PageHeap
2. open file `poc.pdf` in chrome

Details when crash (part of callstack, to get full callstack you can look at the attached log file)

```
(2fe8.14b4): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\out\chromium_pdfium_xfa\chrome.dll  
eax=13b64ff4 ebx=00afc3d0 ecx=13b64ff4 edx=00c00000 esi=00afc200 edi=00afc108  
eip=60a8de1a esp=00afc0fc ebp=00afc100 iopl=0         nv up ei pl nz ac po nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210212  
chrome!fxcrt::UnownedPtr<IFWL_WidgetDelegate>::operator->+0xa:  
60a8de1a 8b01            mov     eax,dword ptr [ecx]  ds:002b:13b64ff4=????????  
  
3:057> kp  
 # ChildEBP RetAddr    
00 00afc100 60a9037a chrome!fxcrt::UnownedPtr<IFWL_WidgetDelegate>::operator->(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 102]   
01 00afc148 6092701b chrome!CXFA_FFComboBox::OnProcessEvent(class CFWL_Event \* pEvent = 0x00afc200)+0x12a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffcombobox.cpp @ 358]   
02 00afc17c 60936ee0 chrome!CFWL_EventTarget::ProcessEvent(class CFWL_Event \* pEvent = 0x00afc200)+0xab [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_eventtarget.cpp @ 29]   
03 00afc1b4 609434e5 chrome!CFWL_NoteDriver::SendEvent(class CFWL_Event \* pNote = 0x00afc200)+0xb0 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_notedriver.cpp @ 34]   
04 00afc1d4 60919e39 chrome!CFWL_Widget::DispatchEvent(class CFWL_Event \* pEvent = 0x00afc200)+0x65 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_widget.cpp @ 299]   
05 00afc22c 60a9038d chrome!CFWL_ComboBox::OnProcessEvent(class CFWL_Event \* pEvent = 0x00afc2c8)+0xb9 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_combobox.cpp @ 495]   
06 00afc274 609434bd chrome!CXFA_FFComboBox::OnProcessEvent(class CFWL_Event \* pEvent = 0x00afc2c8)+0x13d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffcombobox.cpp @ 358]   
07 00afc294 60921fb5 chrome!CFWL_Widget::DispatchEvent(class CFWL_Event \* pEvent = 0x00afc2c8)+0x3d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_widget.cpp @ 295]   
08 00afc2f8 6098d285 chrome!CFWL_Edit::OnTextWillChange(struct CFDE_TextEditEngine::TextChange \* change = 0x00afc3bc)+0xa5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_edit.cpp @ 303]   
09 00afc3e4 6092117d chrome!CFDE_TextEditEngine::Insert(unsigned int idx = 0, class fxcrt::WideString \* request_text = 0x00afc468, CFDE_TextEditEngine::RecordOperation add_operation = kInsertRecord (0n0))+0x135 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fde\cfde_texteditengine.cpp @ 284]   
0a 00afc408 60917acf chrome!CFWL_Edit::SetText(class fxcrt::WideString \* wsText = 0x00afc468)+0x4d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_edit.cpp @ 166]   
0b 00afc4f0 609174d0 chrome!CFWL_ComboBox::Layout(void)+0x38f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_combobox.cpp @ 310]   
0c 00afc500 60a9c8a0 chrome!CFWL_ComboBox::Update(void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_combobox.cpp @ 82]   
0d 00afc518 60a9c6b3 chrome!CXFA_FFField::PerformLayout(void)+0x70 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fffield.cpp @ 165]   
0e 00afc534 60a8ea6f chrome!CXFA_FFField::LoadWidget(void)+0x43 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fffield.cpp @ 133]   
0f 00afc5c4 60a9a188 chrome!CXFA_FFComboBox::LoadWidget(void)+0x2cf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffcombobox.cpp @ 70]   
10 00afc638 60a992d8 chrome!CXFA_FFDocView::SetFocus(class CXFA_FFWidget \* pNewFocus = 0x13b64f78)+0x118 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 292]   
11 00afc664 60aa5efe chrome!CXFA_FFDocView::SetFocusNode(class CXFA_Node \* node = 0x32d98f88)+0x48 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 312]   
12 00afc67c 607fe0f0 chrome!CXFA_FFNotify::SetFocusWidgetNode(class CXFA_Node \* pNode = 0x32d98f88)+0x3e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 307]   
13 00afc738 607fbf5e chrome!CJX_HostPseudoModel::setFocus(class CFX_V8 \* runtime = 0x38deaf98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x00afc854)+0x390 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 462]   
14 00afc770 6080bc85 chrome!CJX_HostPseudoModel::setFocus_static(class CJX_Object \* node = 0x37ea2fd8, class CFX_V8 \* runtime = 0x38deaf98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x00afc854)+0x7e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 39]   
15 00afc7c8 607b5ba2 chrome!CJX_Object::RunMethod(class fxcrt::WideString \* func = 0x00afc9a0, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x00afc854)+0x105 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 179]   
16 00afc874 607afea5 chrome!CFXJSE_Engine::NormalMethodCall(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x00afca18, class fxcrt::WideString \* functionName = 0x00afc9a0)+0x202 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 454]   
17 00afc9fc 17a31672 chrome!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x00afca18)+0x385 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111]   
18 00afca68 17a30098 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x272 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api-arguments-inl.h @ 157]   
19 00afcad8 17a2e0e8 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x5c8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 109]   
1a 00afcb30 17a2dc90 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x399fe408)+0x198 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 139]   
1b 00afcba8 187a3b63 v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n6, unsigned int \* args_object = 0x00afcbe0, class v8::internal::Isolate \* isolate = 0x399fe408)+0x70 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 127]   
1c 00afcbc4 185590fc v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit+0x43  
1d 00afcc0c 18545b1c v8!Builtins_InterpreterEntryTrampoline+0x31c  
1e 00afcc28 185590fc v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
1f 00afcc70 18545b1c v8!Builtins_InterpreterEntryTrampoline+0x31c  
20 00afcc8c 18550d9f v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
21 00afcca4 18550bbb v8!Builtins_JSEntryTrampoline+0x5f  
22 00afccd0 17e30157 v8!Builtins_JSEntry+0x5b  
23 00afcd80 17e2fd68 v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = 0x00000006, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x00afcd8c)+0x3d7 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 265]   
24 00afcdc8 179680e5 v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x399fe408, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n1, class v8::internal::Handle<v8::internal::Object> \* argv = 0x00afd190)+0x78 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 357]   
25 00afce7c 607b2543 v8!v8::Function::Call(class v8::Local<v8::Context> context = class v8::Local<v8::Context>, class v8::Local<v8::Value> recv = class v8::Local<v8::Value>, int argc = 0n1, class v8::Local<v8::Value> \* argv = 0x00afd190)+0x1f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api.cc @ 4984]   
26 00afd1a4 607b76f5 chrome!CFXJSE_Context::ExecuteScript(char \* szScript = 0x3a32025c ".    try.    {.        xfa.host.title = "1";.        field_description = xfa.resolveNode("receipt");.        xfa.host.setFocus(field_description);.    } .    catch(e).    {.        xfa.host.messageBox("Exception: "+e);.    }.", class CFXJSE_Value \* lpRetValue = 0x174dcff0, class CFXJSE_Value \* lpNewThisObject = 0x176acff0)+0x9b3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_context.cpp @ 293]   
27 00afd28c 609f5b24 chrome!CFXJSE_Engine::RunScript(CXFA_Script::Type eScriptType = Javascript (0n1), <CLR type> wsScript = <unknown base type 80000013>, class CFXJSE_Value \* hRetValue = 0x174dcff0, class CXFA_Object \* pThisObject = 0x352daf88)+0x355 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 149]   
28 00afd3c4 609f3862 chrome!CXFA_Node::ExecuteBoolScript(class CXFA_FFDocView \* docView = 0x13aaaf90, class CXFA_Script \* script = 0x3541cf88, class CXFA_EventParam \* pEventParam = 0x00afd5e8)+0x374 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2801]   
29 00afd420 609f377f chrome!CXFA_Node::ExecuteScript(class CXFA_FFDocView \* docView = 0x13aaaf90, class CXFA_Script \* script = 0x3541cf88, class CXFA_EventParam \* pEventParam = 0x00afd5e8)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2760]   
2a 00afd470 609f32ef chrome!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* docView = 0x13aaaf90, XFA_AttributeValue iActivity = Enter (0n233), class CXFA_Event \* event = 0x3540af88, class CXFA_EventParam \* pEventParam = 0x00afd5e8)+0xff [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2461]   
2b 00afd4e8 60abee3a chrome!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* docView = 0x13aaaf90, XFA_AttributeValue iActivity = Enter (0n233), class CXFA_EventParam \* pEventParam = 0x00afd5e8)+0x10f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2438]   
2c 00afd550 606f26e8 chrome!CXFA_FFWidgetHandler::ProcessEvent(class CXFA_Node \* pNode = 0x352daf88, class CXFA_EventParam \* pParam = 0x00afd5e8)+0x22a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidgethandler.cpp @ 256]   
2d 00afd62c 608b380b chrome!CPDFSDK_Widget::OnAAction(CPDF_AAction::AActionType type = kGetFocus (0n4), struct CPDFSDK_FieldAction \* data = 0x00afd6a0, class CPDFSDK_PageView \* pPageView = 0x4dc7cfb8)+0x1c8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_widget.cpp @ 822]   
2e 00afd6d0 606f4047 chrome!CFFL_InteractiveFormFiller::OnSetFocus(class fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr \* pAnnot = 0x00afd7e0, unsigned int nFlag = 0)+0x1cb [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\formfiller\cffl_interactiveformfiller.cpp @ 406]   
2f 00afd700 606cb13f chrome!CPDFSDK_WidgetHandler::OnSetFocus(class fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr \* pAnnot = 0x00afd7e0, unsigned int nFlag = 0)+0x67 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_widgethandler.cpp @ 233]   
30 00afd72c 606dde5c chrome!CPDFSDK_AnnotHandlerMgr::Annot_OnSetFocus(class fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr \* pAnnot = 0x00afd7e0, unsigned int nFlag = 0)+0x7f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_annothandlermgr.cpp @ 248]   
31 00afd77c 60768f3b chrome!CPDFSDK_FormFillEnvironment::SetFocusAnnot(class fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr \* pAnnot = 0x00afd7e0)+0x18c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp @ 672]   
32 00afd7f8 60779e2e chrome!CJS_Field::setFocus(class CJS_Runtime \* pRuntime = 0x2a77efa0, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x00afd8cc)+0x22b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_field.cpp @ 2528]   
33 00afd8f4 60759f4b chrome!JSMethod<CJS_Field,&CJS_Field::setFocus>(char \* method_name_string = 0x66022624 "setFocus", char \* class_name_string = 0x6602234c "Field", class v8::FunctionCallbackInfo<v8::Value> \* info = 0x00afd928)+0x25e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\js_define.h @ 128]   
34 00afd90c 17a31672 chrome!CJS_Field::setFocus_static(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x00afd928)+0x2b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_field.h @ 113]   
35 00afd978 17a30098 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x272 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api-arguments-inl.h @ 157]   
36 00afd9e8 17a2e0e8 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x5c8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 109]   
37 00afda40 17a2dc90 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x399fe408)+0x198 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 139]   
38 00afdab8 187a3b63 v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n5, unsigned int \* args_object = 0x00afdaec, class v8::internal::Isolate \* isolate = 0x399fe408)+0x70 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 127]   
39 00afdad4 185590fc v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit+0x43  
3a 00afdb10 18550d9f v8!Builtins_InterpreterEntryTrampoline+0x31c  
3b 00afdb24 18550bbb v8!Builtins_JSEntryTrampoline+0x5f  
3c 00afdb50 17e30157 v8!Builtins_JSEntry+0x5b  
3d 00afdc00 17e2fd68 v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = 0x00000005, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x00afdc0c)+0x3d7 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 265]   
3e 00afdc48 179477e4 v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x399fe408, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n0, class v8::internal::Handle<v8::internal::Object> \* argv = 0x00000000)+0x78 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 357]   
3f 00afdd14 60704135 v8!v8::Script::Run(class v8::Local<v8::Context> context = class v8::Local<v8::Context>)+0x2a4 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api.cc @ 2173]   
40 00afded4 6079cfee chrome!CFXJS_Engine::Execute(class fxcrt::WideString \* script = 0x00afe050)+0x3c5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cfxjs_engine.cpp @ 571]   
41 00afdef8 6075331d chrome!CJS_Runtime::ExecuteScript(class fxcrt::WideString \* script = 0x00afe050)+0x2e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_runtime.cpp @ 168]   
42 00afdfe8 60712ea9 chrome!CJS_EventContext::RunScript(class fxcrt::WideString \* script = 0x00afe050)+0x31d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_event_context.cpp @ 53]   
43 00afe030 60712d93 chrome!CJS_App::RunJsScript(class CJS_Runtime \* pRuntime = 0x2a77efa0, class fxcrt::WideString \* wsScript = 0x00afe050)+0x89 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_app.cpp @ 419]   
44 00afe058 607a8bd1 chrome!CJS_App::TimerProc(class GlobalTimer \* pTimer = 0x4899efd8)+0x83 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_app.cpp @ 406]   
45 00afe084 633e3867 chrome!GlobalTimer::Trigger(int nTimerID = 0n1)+0xb1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\global_timer.cpp @ 65]   
46 00afe09c 633e382a chrome!base::internal::FunctorTraits<void (<function> \*\* function = 0x37d9eff4, int \* args = 0x37d9eff8)+0x37 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 399]   
47 00afe0b8 633e37ea chrome!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x37d9eff4, int \* args = 0x37d9eff8)+0x3a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 599]   
48 00afe0d4 633e36bf chrome!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x37d9eff4, class std::__1::tuple<int> \* bound = 0x37d9eff8)+0x4a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 672]   
49 00afe0fc 6a981c81 chrome!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x37d9efe0)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 654]   
4a 00afe118 6ac19fa1 base!base::RepeatingCallback<void (void)+0x31 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 136]   
4b 00afe148 6ac196e5 base!base::RepeatingTimer::RunUserTask(void)+0x71 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\timer\timer.cc @ 299]   
4c 00afe1a4 6ac1956c base!base::internal::TimerBase::RunScheduledTask(void)+0x125 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\timer\timer.cc @ 227]   
4d 00afe1b8 6ac1aa2c base!base::internal::BaseTimerTaskInternal::Run(void)+0x3c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\timer\timer.cc @ 50]   
4e 00afe1c8 6ac1a98f base!base::internal::FunctorTraits<void (<function> \* method = 0x6ac19530, class base::internal::BaseTimerTaskInternal \*\* receiver_ptr = 0x00afe204)+0x1c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 499]   
4f 00afe1ec 6ac1a8e5 base!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x488d0ff4, class base::internal::BaseTimerTaskInternal \*\* args = 0x00afe204)+0x4f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 599]   
50 00afe20c 6ac1a794 base!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x488d0ff4, class std::__1::tuple<base::internal::OwnedWrapper<base::internal::BaseTimerTaskInternal> > \* bound = 0x488d0ff8)+0x55 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 672]   
51 00afe234 6a987770 base!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x488d0fe0)+0x54 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 641]   
52 00afe258 6ab48257 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 98]   
53 00afe4e0 6ab8e89c base!base::TaskAnnotator::RunTask(char \* trace_event_name = 0x6ad0dba8 "ThreadController::Task", struct base::PendingTask \* pending_task = 0x00afe750)+0x597 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\common\task_annotator.cc @ 121]   
54 00afe7b0 6ab8e1a8 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow \* continuation_lazy_now = 0x00afe830, bool \* ran_task = 0x00afe84b)+0x54c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 339]   
55 00afe858 6aa40454 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xa8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 219]   
56 00afe8bc 6ab8f716 base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x35c74f34)+0x64 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_pump_default.cc @ 39]   
57 00afea48 6aae06cd base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application_tasks_allowed = true)+0x256 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 408]   
58 00afeccc 576f846b base!base::RunLoop::Run(void)+0x39d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 157]   
59 00afeedc 5b58a02f content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x00afef5c)+0x5cb [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 160]   
5a 00afef14 5b58b035 content!content::RunOtherNamedProcessTypeMain(class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* process_type = 0x00afef78, struct content::MainFunctionParams \* main_function_params = 0x00afef5c, class content::ContentMainDelegate \* delegate = 0x00aff558)+0xaf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 581]   
5b 00aff0d0 5b587b92 content!content::ContentMainRunnerImpl::Run(bool start_service_manager_only = false)+0x2c5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 881]   
5c 00aff0e8 2cae2475 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x32 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_service_manager_main_delegate.cc @ 52]   
5d 00aff478 5b589e4c embedder!service_manager::Main(struct service_manager::MainParams \* params = 0x00aff49c)+0x6e5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\services\service_manager\embedder\main.cc @ 415]   
5e 00aff4c4 5db2132d content!content::ContentMain(struct content::ContentMainParams \* params = 0x00aff53c)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main.cc @ 20]   
5f 00aff5a0 01238ef3 chrome!ChromeMain(struct HINSTANCE__ \* instance = 0x01230000, struct sandbox::SandboxInterfaceInfo \* sandbox_info = 0x00aff634, int64 exe_entry_point_ticks = 0n340398037313)+0x1ed [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_main.cc @ 103]   
60 00aff698 01231476 chrome_exe!MainDllLoader::Launch(struct HINSTANCE__ \* instance = 0x01230000, class base::TimeTicks exe_entry_point_ticks = class base::TimeTicks)+0x453 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\main_dll_loader_win.cc @ 202]   
61 00aff984 01484eee chrome_exe!wWinMain(struct HINSTANCE__ \* instance = 0x01230000, struct HINSTANCE__ \* prev = 0x00000000)+0x476 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_exe_main_win.cc @ 229]   
62 00aff99c 01485041 chrome_exe!invoke_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123]   
63 00aff9f4 0148510d chrome_exe!__scrt_common_main_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283]   
64 00aff9fc 01485118 chrome_exe!__scrt_common_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 326]   
65 00affa04 75fc0179 chrome_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17]   
66 00affa14 7731662d KERNEL32!BaseThreadInitThunk+0x19  
67 00affa70 773165fd ntdll!__RtlUserThreadStart+0x2f  
68 00affa80 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

Call stack when object is freed

```
3:057> !heap -p -a 13b64ff4  
    address 13b64ff4 found in  
    _DPH_HEAP_ROOT @ c01000  
    in free-ed allocation (  DPH_HEAP_BLOCK:         VirtAddr         VirtSize)  
                                   13c20958:         13b64000             2000  
    6aefad92 verifier!AVrfDebugPageHeapFree+0x000000c2  
    7739b5e9 ntdll!RtlDebugFreeHeap+0x0000003e  
    77343422 ntdll!RtlpFreeHeap+0x0004dfc2  
    772f50c1 ntdll!RtlFreeHeap+0x00000201  
    6a4fdcf7 ucrtbased!_free_base+0x00000027 [minkernel\crts\ucrt\src\appcrt\heap\free_base.cpp @ 105]  
    6a4faf0b ucrtbased!free_dbg_nolock+0x0000047b [minkernel\crts\ucrt\src\appcrt\heap\debug_heap.cpp @ 1001]  
    6a4fd6dc ucrtbased!_free_dbg+0x0000007c [minkernel\crts\ucrt\src\appcrt\heap\debug_heap.cpp @ 1030]  
    65ce1c2e chrome!operator delete+0x0000000e [f:\dd\vctools\crt\vcstartup\src\heap\delete_scalar.cpp @ 34]  
    5db2bd77 chrome!std::__1::_DeallocateCaller::__do_call+0x00000017 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\new @ 319]  
    5db2bd4d chrome!std::__1::_DeallocateCaller::__do_deallocate_handle_size+0x0000001d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\new @ 277]  
    5db2bd1c chrome!std::__1::_DeallocateCaller::__do_deallocate_handle_size_align+0x0000002c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\new @ 247]  
    5db2bce4 chrome!std::__1::__libcpp_deallocate+0x00000034 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\new @ 326]  
    60814ff1 chrome!std::__1::allocator<std::__1::__tree_node<const CXFA_Node \*,void \*> >::deallocate+0x00000031 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\memory @ 1816]  
    60814f32 chrome!std::__1::allocator_traits<std::__1::allocator<std::__1::__tree_node<const CXFA_Node \*,void \*> > >::deallocate+0x00000032 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\memory @ 1554]  
    60814e48 chrome!std::__1::__tree<const CXFA_Node \*,std::__1::less<const CXFA_Node \*>,std::__1::allocator<const CXFA_Node \*> >::destroy+0x00000088 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\__tree @ 1863]  
    60814daf chrome!std::__1::__tree<const CXFA_Node \*,std::__1::less<const CXFA_Node \*>,std::__1::allocator<const CXFA_Node \*> >::~__tree+0x0000001f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\__tree @ 1849]  
    608117cf chrome!std::__1::set<const CXFA_Node \*,std::__1::less<const CXFA_Node \*>,std::__1::allocator<const CXFA_Node \*> >::~set+0x0000000f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\set @ 441]  
    6080e53f chrome!CJX_Object::GetMapModuleValue+0x0000017f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 912]  
    6080d98b chrome!CJX_Object::TryEnum+0x0000007b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 372]  
    6080e9aa chrome!CJX_Object::GetEnum+0x0000003a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 393]  
    60a70b8f chrome!CXFA_Stroke::GetStrokeType+0x0000001f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_stroke.cpp @ 95]  
    609ad111 chrome!`anonymous namespace'::Style3D+0x000000f1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_box.cpp @ 39]  
    609ace8d chrome!CXFA_Box::Get3DStyle+0x0000009d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_box.cpp @ 128]  
    609f6e3b chrome!CXFA_Node::GetUIMargin+0x000001ab [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 3040]  
    60ac2011 chrome!CXFA_FWLTheme::GetUIMargin+0x00000071 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fwltheme.cpp @ 155]  
    6091f635 chrome!CFWL_Edit::Layout+0x00000105 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_edit.cpp @ 747]  
    6091f4df chrome!CFWL_Edit::Update+0x0000007f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_edit.cpp @ 108]  
    60a9c8a0 chrome!CXFA_FFField::PerformLayout+0x00000070 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fffield.cpp @ 165]  
    60a9c6b3 chrome!CXFA_FFField::LoadWidget+0x00000043 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fffield.cpp @ 133]  
    60aab33f chrome!CXFA_FFNumericEdit::LoadWidget+0x000001cf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnumericedit.cpp @ 44]  
    60aa67c1 chrome!CXFA_FFNotify::OnLayoutItemAdded+0x000001a1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 480]  
    60af7438 chrome!`anonymous namespace'::SyncContainer+0x00000108 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutpagemgr.cpp @ 125]  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.8 MB)

## Timeline

### cl...@chromium.org (2019-04-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5674315587649536.

### cl...@chromium.org (2019-04-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-04-05)

Testcase 5674315587649536 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5674315587649536.

### mb...@chromium.org (2019-04-05)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### mb...@chromium.org (2019-04-05)

thestig, tsepez: Could either of you take a look at this?

### hu...@gmail.com (2019-07-24)

Hi guys, 

May i ask there is any update for this issue please?

### ts...@chromium.org (2019-11-04)

Hi, sorry, the XFA bugs don't always get a lot of attention since XFA isn't shipped with chrome.  I'm going through some of these old ones now to see if they still reproduce with an eye towards fixing some of the easier ones.

### th...@chromium.org (2019-11-04)

Indeed, sorry for taking so long on XFA bugs.

### ts...@chromium.org (2019-11-04)

A recent build (Happens to be 2019-10-30 d9161d5a2b) is now giving a segv under ASAN rather than a UaF.  Can you confirm?

### ts...@chromium.org (2019-11-04)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-11-04)

And fixing the segv mentioned above (additonal null check added in CPDFSDK_PageView::GetAnnotByXFAWidget()), we get the same UaF once again.

### th...@chromium.org (2020-02-24)

I see the segfault still, but fixing it with the following patch does not generate a UaF again. I suspect https://pdfium-review.googlesource.com/66730 fixed this?

diff --git a/fpdfsdk/cpdfsdk_pageview.cpp b/fpdfsdk/cpdfsdk_pageview.cpp
index b32fbeabd..5a168ceed 100644
--- a/fpdfsdk/cpdfsdk_pageview.cpp
+++ b/fpdfsdk/cpdfsdk_pageview.cpp
@@ -188,6 +188,8 @@ CPDFSDK_Annot* CPDFSDK_PageView::GetAnnotByXFAWidget(CXFA_FFWidget* hWidget) {
     return nullptr;
 
   for (CPDFSDK_Annot* pAnnot : m_SDKAnnotArray) {
+    if (!ToXFAWidget(pAnnot))
+      continue;
     if (ToXFAWidget(pAnnot)->GetXFAFFWidget() == hWidget)
       return pAnnot;
   }

### th...@chromium.org (2020-02-24)

Or https://pdfium-review.googlesource.com/c/64712 fixed this. In any case, I think all we have to do is avoid the nullptr dereference at this point.

### th...@chromium.org (2020-02-24)

https://pdfium-review.googlesource.com/66910

### th...@chromium.org (2020-02-25)

+dsinclair FYI.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-25)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/5e575006797aa94c42113be9f9196161690ffd5f

commit 5e575006797aa94c42113be9f9196161690ffd5f
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Feb 25 13:50:35 2020

Avoid nullptr deference in CPDFSDK_PageView::GetAnnotByXFAWidget().

When a CPDFSDK_Annot is not a CPDFXFA_Widget, ToXFAWidget() returns
nullptr. Handle this case. This is the secendary problem for the bug in
question. Other CLs, as noted on the bug, already fixed the main memory
error.

Bug: chromium:949913
Change-Id: I6307b5449b0229ac2550bb2a0930ff24b398c98e
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/66910
Reviewed-by: dsinclair <dsinclair@chromium.org>
Commit-Queue: dsinclair <dsinclair@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/5e575006797aa94c42113be9f9196161690ffd5f/fpdfsdk/cpdfsdk_pageview.h
[modify] https://pdfium.googlesource.com/pdfium/+/5e575006797aa94c42113be9f9196161690ffd5f/fpdfsdk/cpdfsdk_pageview.cpp


### th...@chromium.org (2020-02-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-25)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/278d3bce53433a0031ea38d327a78b08b67549ed

commit 278d3bce53433a0031ea38d327a78b08b67549ed
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Feb 26 02:37:04 2020

Roll src/third_party/pdfium c93fa1ff0194..6e167903252f (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c93fa1ff0194..6e167903252f

git log c93fa1ff0194..6e167903252f --date=short --first-parent --format='%ad %ae %s'
2020-02-25 nigi@chromium.org Make WriteBitmapToPng() handle FPDFBitmap_BGR format.
2020-02-25 thestig@chromium.org Update Mac test expectations for macOS 10.15.
2020-02-25 thestig@chromium.org Avoid nullptr deference in CPDFSDK_PageView::GetAnnotByXFAWidget().
2020-02-24 thestig@chromium.org Remove reference to full_wpo_on_official.

Created with:
  gclient setdep -r src/third_party/pdfium@6e167903252f

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1048352,chromium:1053958,chromium:949913
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I06183702f3cde02d40e0a32b4df51b05186cbce2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2072406
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#744516}

[modify] https://crrev.com/278d3bce53433a0031ea38d327a78b08b67549ed/DEPS


### na...@google.com (2020-03-02)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-05)

Congrats! The Panel decided to award $3,000 for this report! 

### na...@google.com (2020-03-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-06-02)

This issue was migrated from crbug.com/chromium/949913?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094511)*
