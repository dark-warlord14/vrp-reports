# Security: Use-after-free in CXFA_FFWidget::OnKillFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40094498](https://issues.chromium.org/issues/40094498) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-04-03 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CXFA\_FFWidget::OnKillFocus

**VERSION**  

Operating System: Windows 10  

chrome with pdfium XFA enabled

**REPRODUCTION CASE**

1. Build chrome with XFA enabled + enable PageHeap
2. open file `poc.pdf` in chrome

Details when crash (part of callstack, to get full callstack you can look at the attached log file)

```
(3044.35b8): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\out\chromium_pdfium_xfa\chrome.dll  
eax=139acfbc ebx=3b18efd8 ecx=139acfbc edx=00740000 esi=006fad3c edi=3b490f98  
eip=601d927a esp=006faa1c ebp=006faa20 iopl=0         nv up ei pl nz na po nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210202  
chrome!fxcrt::UnownedPtr<CXFA_Node>::operator->+0xa:  
601d927a 8b01            mov     eax,dword ptr [ecx]  ds:002b:139acfbc=????????  
  
3:061> kp  
 # ChildEBP RetAddr    
00 006faa20 602ecf9b chrome!fxcrt::UnownedPtr<CXFA_Node>::operator->(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 102]   
01 006faa40 602ed0be chrome!CXFA_FFWidget::GetParent(void)+0x1b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 566]   
02 006faa68 602ea4de chrome!CXFA_FFWidget::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x00f50f78)+0x3e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 423]   
03 006faaac 602ca13a chrome!CXFA_FFTextEdit::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x00f50f78)+0x9e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fftextedit.cpp @ 182]   
04 006fab20 602c92d8 chrome!CXFA_FFDocView::SetFocus(class CXFA_FFWidget \* pNewFocus = 0x00f50f78)+0xca [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 286]   
05 006fab4c 602d5efe chrome!CXFA_FFDocView::SetFocusNode(class CXFA_Node \* node = 0x35ddef88)+0x48 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 312]   
06 006fab64 6002e0f0 chrome!CXFA_FFNotify::SetFocusWidgetNode(class CXFA_Node \* pNode = 0x35ddef88)+0x3e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 307]   
07 006fac20 6002bf5e chrome!CJX_HostPseudoModel::setFocus(class CFX_V8 \* runtime = 0x3b490f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x006fad3c)+0x390 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 462]   
08 006fac58 6003bc85 chrome!CJX_HostPseudoModel::setFocus_static(class CJX_Object \* node = 0x3b18efd8, class CFX_V8 \* runtime = 0x3b490f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x006fad3c)+0x7e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 39]   
09 006facb0 5ffe5ba2 chrome!CJX_Object::RunMethod(class fxcrt::WideString \* func = 0x006fae88, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x006fad3c)+0x105 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 179]   
0a 006fad5c 5ffdfea5 chrome!CFXJSE_Engine::NormalMethodCall(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x006faf00, class fxcrt::WideString \* functionName = 0x006fae88)+0x202 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 454]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\out\chromium_pdfium_xfa\v8.dll  
0b 006faee4 17ba1672 chrome!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x006faf00)+0x385 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111]   
0c 006faf50 17ba0098 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x272 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api-arguments-inl.h @ 157]   
0d 006fafc0 17b9e0e8 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x5c8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 109]   
0e 006fb018 17b9dc90 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x39ccc408)+0x198 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 139]   
0f 006fb090 18913b63 v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n6, unsigned int \* args_object = 0x006fb0c8, class v8::internal::Isolate \* isolate = 0x39ccc408)+0x70 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 127]   
10 006fb0ac 186c90fc v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit+0x43  
11 006fb0ec 186b5b1c v8!Builtins_InterpreterEntryTrampoline+0x31c  
12 006fb108 186c90fc v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
13 006fb150 186b5b1c v8!Builtins_InterpreterEntryTrampoline+0x31c  
14 006fb16c 186c0d9f v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
15 006fb184 186c0bbb v8!Builtins_JSEntryTrampoline+0x5f  
16 006fb1b0 17fa0157 v8!Builtins_JSEntry+0x5b  
17 006fb260 17f9fd68 v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = 0x00000006, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x006fb26c)+0x3d7 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 265]   
18 006fb2a8 17ad80e5 v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x39ccc408, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n1, class v8::internal::Handle<v8::internal::Object> \* argv = 0x006fb670)+0x78 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 357]   
19 006fb35c 5ffe2543 v8!v8::Function::Call(class v8::Local<v8::Context> context = class v8::Local<v8::Context>, class v8::Local<v8::Value> recv = class v8::Local<v8::Value>, int argc = 0n1, class v8::Local<v8::Value> \* argv = 0x006fb670)+0x1f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api.cc @ 4984]   
1a 006fb684 5ffe76f5 chrome!CFXJSE_Context::ExecuteScript(char \* szScript = 0x41b3815c ".//xfa.host.messageBox("[XFA Event] field 'cost': exit");.xfa.template.remerge();.field_description = xfa.resolveNode("category");.xfa.host.setFocus(field_description);.xfa.host.openList(field_description);..//xfa.host.messageBox("[XFA Event] field 'cost': exit - End");.", class CFXJSE_Value \* lpRetValue = 0x3b216ff0, class CFXJSE_Value \* lpNewThisObject = 0x37d10ff0)+0x9b3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_context.cpp @ 293]   
1b 006fb76c 60225b24 chrome!CFXJSE_Engine::RunScript(CXFA_Script::Type eScriptType = Javascript (0n1), <CLR type> wsScript = <unknown base type 80000013>, class CFXJSE_Value \* hRetValue = 0x3b216ff0, class CXFA_Object \* pThisObject = 0x35f62f88)+0x355 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 149]   
1c 006fb8a4 60223862 chrome!CXFA_Node::ExecuteBoolScript(class CXFA_FFDocView \* docView = 0x16436f90, class CXFA_Script \* script = 0x36606f88, class CXFA_EventParam \* pEventParam = 0x006fb9f4)+0x374 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2801]   
1d 006fb900 6022377f chrome!CXFA_Node::ExecuteScript(class CXFA_FFDocView \* docView = 0x16436f90, class CXFA_Script \* script = 0x36606f88, class CXFA_EventParam \* pEventParam = 0x006fb9f4)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2760]   
1e 006fb950 602232ef chrome!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* docView = 0x16436f90, XFA_AttributeValue iActivity = Exit (0n98), class CXFA_Event \* event = 0x3666ef88, class CXFA_EventParam \* pEventParam = 0x006fb9f4)+0xff [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2461]   
1f 006fb9c8 602ed1c7 chrome!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* docView = 0x16436f90, XFA_AttributeValue iActivity = Exit (0n98), class CXFA_EventParam \* pEventParam = 0x006fb9f4)+0x10f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2438]   
20 006fba30 602ed0a3 chrome!CXFA_FFWidget::EventKillFocus(void)+0x97 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 616]   
21 006fba58 602ea4de chrome!CXFA_FFWidget::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x00f50f78)+0x23 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 420]   
22 006fba9c 602ca13a chrome!CXFA_FFTextEdit::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x00f50f78)+0x9e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fftextedit.cpp @ 182]   
23 006fbb10 602c92d8 chrome!CXFA_FFDocView::SetFocus(class CXFA_FFWidget \* pNewFocus = 0x00f50f78)+0xca [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 286]   
24 006fbb3c 602d5efe chrome!CXFA_FFDocView::SetFocusNode(class CXFA_Node \* node = 0x35ddef88)+0x48 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 312]   
25 006fbb54 6002e0f0 chrome!CXFA_FFNotify::SetFocusWidgetNode(class CXFA_Node \* pNode = 0x35ddef88)+0x3e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 307]   
26 006fbc10 6002bf5e chrome!CJX_HostPseudoModel::setFocus(class CFX_V8 \* runtime = 0x3b490f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x006fbd2c)+0x390 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 462]   
27 006fbc48 6003bc85 chrome!CJX_HostPseudoModel::setFocus_static(class CJX_Object \* node = 0x3b18efd8, class CFX_V8 \* runtime = 0x3b490f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x006fbd2c)+0x7e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 39]   
28 006fbca0 5ffe5ba2 chrome!CJX_Object::RunMethod(class fxcrt::WideString \* func = 0x006fbe78, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x006fbd2c)+0x105 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 179]   
29 006fbd4c 5ffdfea5 chrome!CFXJSE_Engine::NormalMethodCall(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x006fbef0, class fxcrt::WideString \* functionName = 0x006fbe78)+0x202 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 454]   
2a 006fbed4 17ba1672 chrome!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x006fbef0)+0x385 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111]   
2b 006fbf40 17ba0098 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x272 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api-arguments-inl.h @ 157]   
2c 006fbfb0 17b9e0e8 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x5c8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 109]   
2d 006fc008 17b9dc90 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x39ccc408)+0x198 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 139]   
2e 006fc080 18913b63 v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n6, unsigned int \* args_object = 0x006fc0b8, class v8::internal::Isolate \* isolate = 0x39ccc408)+0x70 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 127]   
2f 006fc09c 186c90fc v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit+0x43  
30 006fc0dc 186b5b1c v8!Builtins_InterpreterEntryTrampoline+0x31c  
31 006fc0f8 186c90fc v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
32 006fc140 186b5b1c v8!Builtins_InterpreterEntryTrampoline+0x31c  
33 006fc15c 186c0d9f v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
34 006fc174 186c0bbb v8!Builtins_JSEntryTrampoline+0x5f  
35 006fc1a0 17fa0157 v8!Builtins_JSEntry+0x5b  
36 006fc250 17f9fd68 v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = 0x00000006, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x006fc25c)+0x3d7 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 265]   
37 006fc298 17ad80e5 v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x39ccc408, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n1, class v8::internal::Handle<v8::internal::Object> \* argv = 0x006fc660)+0x78 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 357]   
38 006fc34c 5ffe2543 v8!v8::Function::Call(class v8::Local<v8::Context> context = class v8::Local<v8::Context>, class v8::Local<v8::Value> recv = class v8::Local<v8::Value>, int argc = 0n1, class v8::Local<v8::Value> \* argv = 0x006fc660)+0x1f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api.cc @ 4984]   
39 006fc674 5ffe76f5 chrome!CFXJSE_Context::ExecuteScript(char \* szScript = 0x41b3801c ".//xfa.host.messageBox("[XFA Event] field 'cost': exit");.xfa.template.remerge();.field_description = xfa.resolveNode("category");.xfa.host.setFocus(field_description);.xfa.host.openList(field_description);..//xfa.host.messageBox("[XFA Event] field 'cost': exit - End");.", class CFXJSE_Value \* lpRetValue = 0x4a4b6ff0, class CFXJSE_Value \* lpNewThisObject = 0x37d10ff0)+0x9b3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_context.cpp @ 293]   
3a 006fc75c 60225b24 chrome!CFXJSE_Engine::RunScript(CXFA_Script::Type eScriptType = Javascript (0n1), <CLR type> wsScript = <unknown base type 80000013>, class CFXJSE_Value \* hRetValue = 0x4a4b6ff0, class CXFA_Object \* pThisObject = 0x35f62f88)+0x355 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 149]   
3b 006fc894 60223862 chrome!CXFA_Node::ExecuteBoolScript(class CXFA_FFDocView \* docView = 0x16436f90, class CXFA_Script \* script = 0x36606f88, class CXFA_EventParam \* pEventParam = 0x006fc9e4)+0x374 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2801]   
3c 006fc8f0 6022377f chrome!CXFA_Node::ExecuteScript(class CXFA_FFDocView \* docView = 0x16436f90, class CXFA_Script \* script = 0x36606f88, class CXFA_EventParam \* pEventParam = 0x006fc9e4)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2760]   
3d 006fc940 602232ef chrome!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* docView = 0x16436f90, XFA_AttributeValue iActivity = Exit (0n98), class CXFA_Event \* event = 0x3666ef88, class CXFA_EventParam \* pEventParam = 0x006fc9e4)+0xff [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2461]   
3e 006fc9b8 602ed1c7 chrome!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* docView = 0x16436f90, XFA_AttributeValue iActivity = Exit (0n98), class CXFA_EventParam \* pEventParam = 0x006fc9e4)+0x10f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2438]   
3f 006fca20 602ed0a3 chrome!CXFA_FFWidget::EventKillFocus(void)+0x97 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 616]   
40 006fca48 602ea4de chrome!CXFA_FFWidget::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x00ec2f80)+0x23 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 420]   
41 006fca8c 602ca13a chrome!CXFA_FFTextEdit::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x00ec2f80)+0x9e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fftextedit.cpp @ 182]   
42 006fcb00 602c92d8 chrome!CXFA_FFDocView::SetFocus(class CXFA_FFWidget \* pNewFocus = 0x00ec2f80)+0xca [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 286]   
43 006fcb2c 602d5efe chrome!CXFA_FFDocView::SetFocusNode(class CXFA_Node \* node = 0x3a9aef88)+0x48 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 312]   
44 006fcb44 6002e0f0 chrome!CXFA_FFNotify::SetFocusWidgetNode(class CXFA_Node \* pNode = 0x3a9aef88)+0x3e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 307]   
45 006fcc00 6002bf5e chrome!CJX_HostPseudoModel::setFocus(class CFX_V8 \* runtime = 0x3b490f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x006fcd1c)+0x390 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 462]   
46 006fcc38 6003bc85 chrome!CJX_HostPseudoModel::setFocus_static(class CJX_Object \* node = 0x3b18efd8, class CFX_V8 \* runtime = 0x3b490f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x006fcd1c)+0x7e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 39]   
  
...   

```

Call stack when object is freed

```
3:061> !heap -p -a 0x00f50f78  
    address 00f50f78 found in  
    _DPH_HEAP_ROOT @ 741000  
    in free-ed allocation (  DPH_HEAP_BLOCK:         VirtAddr         VirtSize)  
                                     ea27b8:           f50000             2000  
    6a7ead92 verifier!AVrfDebugPageHeapFree+0x000000c2  
    7739b5e9 ntdll!RtlDebugFreeHeap+0x0000003e  
    77343422 ntdll!RtlpFreeHeap+0x0004dfc2  
    772f50c1 ntdll!RtlFreeHeap+0x00000201  
    69e2dcf7 ucrtbased!_free_base+0x00000027 [minkernel\crts\ucrt\src\appcrt\heap\free_base.cpp @ 105]  
    69e2af0b ucrtbased!free_dbg_nolock+0x0000047b [minkernel\crts\ucrt\src\appcrt\heap\debug_heap.cpp @ 1001]  
    69e2d6dc ucrtbased!_free_dbg+0x0000007c [minkernel\crts\ucrt\src\appcrt\heap\debug_heap.cpp @ 1030]  
    65511c2e chrome!operator delete+0x0000000e [f:\dd\vctools\crt\vcstartup\src\heap\delete_scalar.cpp @ 34]  
    602c043c chrome!CXFA_FFComboBox::~CXFA_FFComboBox+0x0000003c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffcombobox.cpp @ 31]  
    6031eac8 chrome!XFA_ReleaseLayoutItem+0x00000118 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 34]  
    6031ea40 chrome!XFA_ReleaseLayoutItem+0x00000090 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 27]  
    6031ea40 chrome!XFA_ReleaseLayoutItem+0x00000090 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 27]  
    6031ea40 chrome!XFA_ReleaseLayoutItem+0x00000090 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 27]  
    6031ea40 chrome!XFA_ReleaseLayoutItem+0x00000090 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 27]  
    6031ea40 chrome!XFA_ReleaseLayoutItem+0x00000090 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 27]  
    6031ea40 chrome!XFA_ReleaseLayoutItem+0x00000090 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 27]  
    6031ea40 chrome!XFA_ReleaseLayoutItem+0x00000090 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 27]  
    6031ea40 chrome!XFA_ReleaseLayoutItem+0x00000090 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 27]  
    6031fb1a chrome!CXFA_LayoutPageMgr::PrepareLayout+0x000000ba [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutpagemgr.cpp @ 1955]  
    6031f35a chrome!CXFA_LayoutPageMgr::InitLayoutPage+0x0000002a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutpagemgr.cpp @ 353]  
    6032b27e chrome!CXFA_LayoutProcessor::StartLayout+0x0000013e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutprocessor.cpp @ 50]  
    6032b7a8 chrome!CXFA_LayoutProcessor::IncrementLayout+0x00000028 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutprocessor.cpp @ 102]  
    602c918a chrome!CXFA_FFDocView::RunLayout+0x0000002a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 451]  
    602c96c9 chrome!CXFA_FFDocView::UpdateDocView+0x00000179 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 190]  
    602d5ce0 chrome!CXFA_FFNotify::OpenDropDownList+0x00000070 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 267]  
    6002d20b chrome!CJX_HostPseudoModel::openList+0x0000045b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 316]  
    6002bbfe chrome!CJX_HostPseudoModel::openList_static+0x0000007e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 33]  
    6003bc85 chrome!CJX_Object::RunMethod+0x00000105 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 179]  
    5ffe5ba2 chrome!CFXJSE_Engine::NormalMethodCall+0x00000202 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 454]  
    5ffdfea5 chrome!`anonymous namespace'::DynPropGetterAdapter_MethodCallback+0x00000385 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111]  
    17ba1672 v8!v8::internal::FunctionCallbackArguments::Call+0x00000272 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api-arguments-inl.h @ 157]  
    17ba0098 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>+0x000005c8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 109]  
  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.8 MB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 46.5 KB)

## Timeline

### cl...@chromium.org (2019-04-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5161894053806080.

### cl...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-04-03)

Testcase 5161894053806080 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5161894053806080.

### mb...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### mb...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-04-03)

READ of size 8 at 0x6100000073a8 thread T0 (chrome)
    #0 0x55ec8a56c9cf in operator-> ./../../third_party/pdfium/core/fxcrt/unowned_ptr.h:102:34
    #1 0x55ec8a56c9cf in GetParent ./../../third_party/pdfium/xfa/fxfa/cxfa_ffwidget.cpp:566:0
    #2 0x55ec8a56c9cf in CXFA_FFWidget::OnKillFocus(CXFA_FFWidget*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffwidget.cpp:423:0
    #3 0x55ec8a565a52 in CXFA_FFTextEdit::OnKillFocus(CXFA_FFWidget*) ./../../third_party/pdfium/xfa/fxfa/cxfa_fftextedit.cpp:182:18
    #4 0x55ec8a532a45 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffdocview.cpp:286:16
    #5 0x55ec8a52f978 in CXFA_FFDocView::SetFocusNode(CXFA_Node*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffdocview.cpp:312:8
    #6 0x55ec8a10e082 in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_hostpseudomodel.cpp:461:12
    #7 0x55ec8a10896a in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #8 0x55ec8a124c18 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_object.cpp:177:10
    #9 0x55ec8a0766d8 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/xfa/cfxjse_engine.cpp:454:31
    #10 0x55ec8a070b39 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/pdfium/fxjs/xfa/cfxjse_class.cpp:112:7
    #11 0x55ec86aa2ea2 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api-arguments-inl.h:157:3
    #12 0x55ec86aa000d in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36
    #13 0x55ec86a9daa7 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:5
    #14 0x55ec88bcbe18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit ??:0:0
    #15 0x55ec88b3edc5 in Builtins_InterpreterEntryTrampoline ??:0:0
    #16 0x55ec88b382bb in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #17 0x55ec88b3edc5 in Builtins_InterpreterEntryTrampoline ??:0:0
    #18 0x55ec88b382bb in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #19 0x55ec88b3c73c in Builtins_JSEntryTrampoline ??:0:0
    #20 0x55ec88b3c4b7 in Builtins_JSEntry ??:0:0
    #21 0x55ec876112dd in Call ./../../v8/src/simulator.h:138:12
    #22 0x55ec876112dd in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution.cc:265:0
    #23 0x55ec87610538 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution.cc:357:10
    #24 0x55ec86922ae4 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api.cc:4985:7
    #25 0x55ec8a072b9e in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) ./../../third_party/pdfium/fxjs/xfa/cfxjse_context.cpp:293:21
    #26 0x55ec8a07b37f in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) ./../../third_party/pdfium/fxjs/xfa/cfxjse_engine.cpp:149:23
    #27 0x55ec8a48ba23 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2788:22
    #28 0x55ec8a4838e6 in ExecuteScript ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2747:26
    #29 0x55ec8a4838e6 in ProcessEvent ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2448:0
    #30 0x55ec8a4838e6 in CXFA_Node::ProcessEvent(CXFA_FFDocView*, XFA_AttributeValue, CXFA_EventParam*) ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2425:0
    #31 0x55ec8a56c687 in EventKillFocus ./../../third_party/pdfium/xfa/fxfa/cxfa_ffwidget.cpp:616:12
    #32 0x55ec8a56c687 in CXFA_FFWidget::OnKillFocus(CXFA_FFWidget*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffwidget.cpp:419:0
    #33 0x55ec8a565a52 in CXFA_FFTextEdit::OnKillFocus(CXFA_FFWidget*) ./../../third_party/pdfium/xfa/fxfa/cxfa_fftextedit.cpp:182:18
    #34 0x55ec8a532a45 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffdocview.cpp:286:16
    #35 0x55ec8a52f978 in CXFA_FFDocView::SetFocusNode(CXFA_Node*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffdocview.cpp:312:8
    #36 0x55ec8a10e082 in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_hostpseudomodel.cpp:461:12
    #37 0x55ec8a10896a in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #38 0x55ec8a124c18 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_object.cpp:177:10
    #39 0x55ec8a0766d8 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/xfa/cfxjse_engine.cpp:454:31
    #40 0x55ec8a070b39 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/pdfium/fxjs/xfa/cfxjse_class.cpp:112:7
    #41 0x55ec86aa2ea2 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api-arguments-inl.h:157:3
    #42 0x55ec86aa000d in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36
    #43 0x55ec86a9daa7 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:5
    #44 0x55ec88bcbe18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit ??:0:0
    #45 0x55ec88b3edc5 in Builtins_InterpreterEntryTrampoline ??:0:0
    #46 0x55ec88b382bb in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #47 0x55ec88b3edc5 in Builtins_InterpreterEntryTrampoline ??:0:0
    #48 0x55ec88b382bb in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #49 0x55ec88b3c73c in Builtins_JSEntryTrampoline ??:0:0
    #50 0x55ec88b3c4b7 in Builtins_JSEntry ??:0:0
    #51 0x55ec876112dd in Call ./../../v8/src/simulator.h:138:12
    #52 0x55ec876112dd in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution.cc:265:0
    #53 0x55ec87610538 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution.cc:357:10
    #54 0x55ec86922ae4 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api.cc:4985:7
    #55 0x55ec8a072b9e in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) ./../../third_party/pdfium/fxjs/xfa/cfxjse_context.cpp:293:21
    #56 0x55ec8a07b37f in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) ./../../third_party/pdfium/fxjs/xfa/cfxjse_engine.cpp:149:23
    #57 0x55ec8a48ba23 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2788:22
    #58 0x55ec8a4838e6 in ExecuteScript ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2747:26
    #59 0x55ec8a4838e6 in ProcessEvent ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2448:0
    #60 0x55ec8a4838e6 in CXFA_Node::ProcessEvent(CXFA_FFDocView*, XFA_AttributeValue, CXFA_EventParam*) ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2425:0
    #61 0x55ec8a56c687 in EventKillFocus ./../../third_party/pdfium/xfa/fxfa/cxfa_ffwidget.cpp:616:12
    #62 0x55ec8a56c687 in CXFA_FFWidget::OnKillFocus(CXFA_FFWidget*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffwidget.cpp:419:0
    #63 0x55ec8a565a52 in CXFA_FFTextEdit::OnKillFocus(CXFA_FFWidget*) ./../../third_party/pdfium/xfa/fxfa/cxfa_fftextedit.cpp:182:18
    #64 0x55ec8a532a45 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffdocview.cpp:286:16
    #65 0x55ec8a52f978 in CXFA_FFDocView::SetFocusNode(CXFA_Node*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffdocview.cpp:312:8
    #66 0x55ec8a10e082 in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_hostpseudomodel.cpp:461:12
    #67 0x55ec8a10896a in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #68 0x55ec8a124c18 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_object.cpp:177:10
    #69 0x55ec8a0766d8 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/xfa/cfxjse_engine.cpp:454:31
    #70 0x55ec8a070b39 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/pdfium/fxjs/xfa/cfxjse_class.cpp:112:7
    #71 0x55ec86aa2ea2 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api-arguments-inl.h:157:3
    #72 0x55ec86aa000d in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36
    #73 0x55ec86a9daa7 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:5
    #74 0x55ec88bcbe18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit ??:0:0
    #75 0x55ec88b3edc5 in Builtins_InterpreterEntryTrampoline ??:0:0
    #76 0x55ec88b382bb in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #77 0x55ec88b3edc5 in Builtins_InterpreterEntryTrampoline ??:0:0
    #78 0x55ec88b382bb in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #79 0x55ec88b3c73c in Builtins_JSEntryTrampoline ??:0:0
    #80 0x55ec88b3c4b7 in Builtins_JSEntry ??:0:0
    #81 0x55ec876112dd in Call ./../../v8/src/simulator.h:138:12
    #82 0x55ec876112dd in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution.cc:265:0
    #83 0x55ec87610538 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution.cc:357:10
    #84 0x55ec86922ae4 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api.cc:4985:7
    #85 0x55ec8a072b9e in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) ./../../third_party/pdfium/fxjs/xfa/cfxjse_context.cpp:293:21
    #86 0x55ec8a07b37f in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) ./../../third_party/pdfium/fxjs/xfa/cfxjse_engine.cpp:149:23
    #87 0x55ec8a48ba23 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2788:22
    #88 0x55ec8a4838e6 in ExecuteScript ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2747:26
    #89 0x55ec8a4838e6 in ProcessEvent ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2448:0
    #90 0x55ec8a4838e6 in CXFA_Node::ProcessEvent(CXFA_FFDocView*, XFA_AttributeValue, CXFA_EventParam*) ./../../third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp:2425:0
    #91 0x55ec89f47f65 in CPDFSDK_Widget::OnAAction(CPDF_AAction::AActionType, CPDFSDK_FieldAction*, CPDFSDK_PageView*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_widget.cpp:822:37
    #92 0x55ec8a240b75 in CFFL_InteractiveFormFiller::OnSetFocus(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*, unsigned int) ./../../third_party/pdfium/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:406:16
    #93 0x55ec89f2b4ec in CPDFSDK_FormFillEnvironment::SetFocusAnnot(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:672:23
    #94 0x55ec89ffc164 in CJS_Field::setFocus(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/cjs_field.cpp:2529:21
    #95 0x55ec8a01d5c8 in void JSMethod<CJS_Field, &(CJS_Field::setFocus(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/pdfium/fxjs/js_define.h:128:23
    #96 0x55ec86aa2ea2 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api-arguments-inl.h:157:3
    #97 0x55ec86aa000d in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36
    #98 0x55ec86a9daa7 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:5
    #99 0x55ec88bcbe18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit ??:0:0
    #100 0x55ec88b3edc5 in Builtins_InterpreterEntryTrampoline ??:0:0
    #101 0x55ec88b3c73c in Builtins_JSEntryTrampoline ??:0:0
    #102 0x55ec88b3c4b7 in Builtins_JSEntry ??:0:0
    #103 0x55ec876112dd in Call ./../../v8/src/simulator.h:138:12
    #104 0x55ec876112dd in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution.cc:265:0
    #105 0x55ec87610538 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution.cc:357:10
    #106 0x55ec868d7de3 in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api.cc:2174:7
    #107 0x55ec89f5e7ae in CFXJS_Engine::Execute(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cfxjs_engine.cpp:571:25
    #108 0x55ec8a052e1c in CJS_Runtime::ExecuteScript(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cjs_runtime.cpp:168:10
    #109 0x55ec89fd19a7 in CJS_EventContext::RunScript(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cjs_event_context.cpp:53:23
    #110 0x55ec89f6a959 in RunJsScript ./../../third_party/pdfium/fxjs/cjs_app.cpp:419:13
    #111 0x55ec89f6a959 in CJS_App::TimerProc(GlobalTimer*) ./../../third_party/pdfium/fxjs/cjs_app.cpp:406:0
    #112 0x55ec8a069066 in GlobalTimer::Trigger(int) ./../../third_party/pdfium/fxjs/global_timer.cpp:65:26
    #113 0x55ec8b995480 in Run ./../../base/callback.h:136:12
    #114 0x55ec8b995480 in base::RepeatingTimer::RunUserTask() ./../../base/timer/timer.cc:297:0
    #115 0x55ec8b8cb4f4 in Run ./../../base/callback.h:97:12
    #116 0x55ec8b8cb4f4 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:119:0
    #117 0x55ec8b90c7c0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:23
    #118 0x55ec8b90bf7f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:214:7
    #119 0x55ec8b7ec8fc in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #120 0x55ec8b90eab9 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:441:12
    #121 0x55ec8b90eab9 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #122 0x55ec8b86cd22 in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run_loop.cc:161:14
    #123 0x55ec8944bce4 in content::PpapiPluginMain(content::MainFunctionParams const&) ./../../content/ppapi_plugin/ppapi_plugin_main.cc:157:12
    #124 0x55ec8a5ef007 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:513:14
    #125 0x55ec8a5f31ed in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:881:10
    #126 0x55ec8a76a2ed in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:415:29
    #127 0x55ec8a5ecf38 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #128 0x55ec80189e7d in ChromeMain ./../../chrome/app/chrome_main.cc:103:12
    #129 0x7fad265fb2b0 in __libc_start_main ??:0:0

0x6100000073a8 is located 104 bytes inside of 184-byte region [0x610000007340,0x6100000073f8)
freed by thread T0 (chrome) here:
    #0 0x55ec80187f6d in operator delete(void*) _asan_rtl_:3
    #1 0x55ec8a5c4d9b in XFA_ReleaseLayoutItem(CXFA_LayoutItem*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutitem.cpp:26:5
    #2 0x55ec8a5c4d9b in XFA_ReleaseLayoutItem(CXFA_LayoutItem*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutitem.cpp:26:5
    #3 0x55ec8a5c4d9b in XFA_ReleaseLayoutItem(CXFA_LayoutItem*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutitem.cpp:26:5
    #4 0x55ec8a5c4d9b in XFA_ReleaseLayoutItem(CXFA_LayoutItem*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutitem.cpp:26:5
    #5 0x55ec8a5c4d9b in XFA_ReleaseLayoutItem(CXFA_LayoutItem*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutitem.cpp:26:5
    #6 0x55ec8a5c4d9b in XFA_ReleaseLayoutItem(CXFA_LayoutItem*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutitem.cpp:26:5
    #7 0x55ec8a5c4d9b in XFA_ReleaseLayoutItem(CXFA_LayoutItem*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutitem.cpp:26:5
    #8 0x55ec8a5c4d9b in XFA_ReleaseLayoutItem(CXFA_LayoutItem*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutitem.cpp:26:5
    #9 0x55ec8a5c7180 in CXFA_LayoutPageMgr::PrepareLayout() ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:1955:7
    #10 0x55ec8a5c6487 in CXFA_LayoutPageMgr::InitLayoutPage(CXFA_Node*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:352:3
    #11 0x55ec8a5d9e12 in CXFA_LayoutProcessor::StartLayout(bool) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutprocessor.cpp:50:26
    #12 0x55ec8a5da4ea in CXFA_LayoutProcessor::IncrementLayout() ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutprocessor.cpp:102:5
    #13 0x55ec8a52f5d6 in CXFA_FFDocView::RunLayout() ./../../third_party/pdfium/xfa/fxfa/cxfa_ffdocview.cpp:451:25
    #14 0x55ec8a5310d5 in CXFA_FFDocView::UpdateDocView() ./../../third_party/pdfium/xfa/fxfa/cxfa_ffdocview.cpp:190:7
    #15 0x55ec8a10bb38 in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_hostpseudomodel.cpp:315:12
    #16 0x55ec8a1083aa in CJX_HostPseudoModel::openList_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_hostpseudomodel.h:33:3
    #17 0x55ec8a124c18 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/xfa/cjx_object.cpp:177:10
    #18 0x55ec8a0766d8 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/xfa/cfxjse_engine.cpp:454:31
    #19 0x55ec8a070b39 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/pdfium/fxjs/xfa/cfxjse_class.cpp:112:7
    #20 0x55ec86aa2ea2 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api-arguments-inl.h:157:3
    #21 0x55ec86aa000d in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36
    #22 0x55ec86a9daa7 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:5
    #23 0x55ec88bcbe18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit ??:0:0
    #24 0x55ec88b3edc5 in Builtins_InterpreterEntryTrampoline ??:0:0
    #25 0x55ec88b382bb in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #26 0x55ec88b3edc5 in Builtins_InterpreterEntryTrampoline ??:0:0
    #27 0x55ec88b382bb in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #28 0x55ec88b3c73c in Builtins_JSEntryTrampoline ??:0:0
    #29 0x55ec88b3c4b7 in Builtins_JSEntry ??:0:0

previously allocated by thread T0 (chrome) here:
    #0 0x55ec8018770d in operator new(unsigned long) _asan_rtl_:3
    #1 0x55ec8a54a9b4 in MakeUnique<CXFA_FFNumericEdit, CXFA_Node *&> ./../../third_party/pdfium/third_party/base/ptr_util.h:56:29
    #2 0x55ec8a54a9b4 in CXFA_FFNotify::OnCreateContentLayoutItem(CXFA_Node*) ./../../third_party/pdfium/xfa/fxfa/cxfa_ffnotify.cpp:162:0
    #3 0x55ec8a5c29cf in CreateContentLayoutItem ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:643:23
    #4 0x55ec8a5c29cf in CXFA_ItemLayoutProcessor::DoLayoutField() ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2029:0
    #5 0x55ec8a5a787d in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2082:7
    #6 0x55ec8a5a9148 in CXFA_ItemLayoutProcessor::DoLayoutPositionedContainer(CXFA_LayoutContext*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1073:17
    #7 0x55ec8a5a7b21 in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2071:11
    #8 0x55ec8a5bc042 in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2348:29
    #9 0x55ec8a5b6def in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_LayoutContext*, bool) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1800:23
    #10 0x55ec8a5a7b9d in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2064:18
    #11 0x55ec8a5bc042 in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2348:29
    #12 0x55ec8a5b6def in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_LayoutContext*, bool) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1800:23
    #13 0x55ec8a5a7b9d in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2064:18
    #14 0x55ec8a5bc042 in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2348:29
    #15 0x55ec8a5b6def in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_LayoutContext*, bool) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1800:23
    #16 0x55ec8a5a7b9d in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2064:18
    #17 0x55ec8a5bc042 in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2348:29
    #18 0x55ec8a5b6def in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_LayoutContext*, bool) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1800:23
    #19 0x55ec8a5a7b9d in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2064:18
    #20 0x55ec8a5da19d in CXFA_LayoutProcessor::DoLayout() ./../../third_party/pdfium/xfa/fxfa/layout/cxfa_layoutprocessor.cpp:74:43
    #21 0x55ec8a52e19d in CXFA_FFDocView::DoLayout() ./../../third_party/pdfium/xfa/fxfa/cxfa_ffdocview.cpp:96:30
    #22 0x55ec8a5dc75e in CPDFXFA_Context::LoadXFADoc() ./../../third_party/pdfium/fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:131:18
    #23 0x55ec9e988def in FPDF_LoadXFA ./../../third_party/pdfium/fpdfsdk/fpdf_view.cpp:255:32
    #24 0x55ec9e912d0d in chrome_pdf::PDFiumEngine::LoadForm() ./../../pdf/pdfium/pdfium_engine.cc:2833:5
    #25 0x55ec9e8f1f47 in chrome_pdf::PDFiumEngine::LoadBody() ./../../pdf/pdfium/pdfium_engine.cc:2798:5
    #26 0x55ec9e9123a2 in chrome_pdf::PDFiumEngine::ContinueLoadingDocument(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) ./../../pdf/pdfium/pdfium_engine.cc:2706:3
    #27 0x55ec9e8f1985 in chrome_pdf::PDFiumEngine::LoadDocument() ./../../pdf/pdfium/pdfium_engine.cc:2628:5
    #28 0x55ec9e92807f in chrome_pdf::DocumentLoaderImpl::ReadComplete() ./../../pdf/document_loader_impl.cc:0:0
    #29 0x55ec9e92885b in chrome_pdf::DocumentLoaderImpl::DidRead(int) ./../../pdf/document_loader_impl.cc:319:14
    #30 0x55ec9e9299d8 in operator() ./../../ppapi/utility/completion_callback_factory.h:607:9
    #31 0x55ec9e9299d8 in pp::CompletionCallbackFactory<chrome_pdf::DocumentLoaderImpl, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome_pdf::DocumentLoaderImpl, pp::ThreadSafeThreadTraits>::Dispatcher0<void (chrome_pdf::DocumentLoaderImpl::*)(int)> >::Thunk(void*, int) ./../../ppapi/utility/completion_callback_factory.h:584:0
    #32 0x55ec9e932567 in chrome_pdf::URLLoaderWrapperImpl::DidRead(int) ./../../pdf/url_loader_wrapper_impl.cc:0:0



### ts...@chromium.org (2019-04-03)

Requires timers, so will not reproduce under pdfium_test.

### ts...@chromium.org (2019-07-02)

"Opposite side of the street" from https://crbug.com/chromium/978575

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-02)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13

commit c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jul 02 23:17:01 2019

Observe CFXA_FFWidget, part 2

Related to https://crbug.com/978575, but fires event upon losing
focus. Now that we can fix these with observables, it is a matter
of ensuring that the return is checked by all callers.

Bug: chromium:949032
Change-Id: Ia9ab0f84e2a06d93177008de9bf1316045b58c2e
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/57190
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_fflistbox.cpp
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_fffield.cpp
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_ffcombobox.h
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_fffield.h
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_fftextedit.h
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_ffwidget.h
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_ffwidget.cpp
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_ffdocview.cpp
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_fflistbox.h
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_fftextedit.cpp
[modify] https://crrev.com/c924a24fb4dfbc7928a25ca1c3e90a5f664e4a13/xfa/fxfa/cxfa_ffcombobox.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2d3b426aa72be30a928c0f3db04c0f2823d5c180

commit 2d3b426aa72be30a928c0f3db04c0f2823d5c180
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jul 03 21:43:03 2019

Roll src/third_party/pdfium 815726bc4c69..3dd6ef064898 (8 commits)

https://pdfium.googlesource.com/pdfium.git/+log/815726bc4c69..3dd6ef064898


git log 815726bc4c69..3dd6ef064898 --date=short --no-merges --format='%ad %ae %s'
2019-07-03 thestig@chromium.org Upgrade OpenJPEG to 2.3.1.
2019-07-03 thestig@chromium.org Remove extra files in third_party/libopenjpeg20.
2019-07-03 thestig@chromium.org Handle compressed data streams in CPDF_PageContentGenerator.
2019-07-03 thestig@chromium.org Add a pixel test for gradients.
2019-07-03 thestig@chromium.org Roll third_party/icu/ 64e5d7d43..fd97d4326 (6 commits)
2019-07-03 thestig@chromium.org Roll third_party/googletest/src/ f71fb4f9a..d7003576d (37 commits)
2019-07-02 nigi@chromium.org [SkiaPath] Fix issue with missing line.
2019-07-02 tsepez@chromium.org Observe CFXA_FFWidget, part 2


Created with:
  gclient setdep -r src/third_party/pdfium@3dd6ef064898

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:949032
TBR=pdfium-deps-rolls@chromium.org

Change-Id: Iab1f3e17bb30657dc85f6e8ce685c69475bbaa1c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1688310
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#674622}

[modify] https://crrev.com/2d3b426aa72be30a928c0f3db04c0f2823d5c180/DEPS


### hu...@gmail.com (2019-07-05)

I think this patch fix the bug. I tested with the poc file and it didn't crash anymore. 

### va...@chromium.org (2019-07-16)

tsepez@ -- I'm marking this as fixed based on https://crbug.com/chromium/949032#c11.
Please feel free to re-open if you disagree. Thanks.

### sh...@chromium.org (2019-07-16)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-22)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-30)

Congrats the Panel decided to reward $3,000 for this report!

### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-10-22)

This issue was migrated from crbug.com/chromium/949032?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094498)*
