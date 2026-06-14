# Security: pdfium SEGV on unknown address / wild jump

| Field | Value |
|-------|-------|
| **Issue ID** | [40093153](https://issues.chromium.org/issues/40093153) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-11-21 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

SEGV on unknown address / wild jump in pdfium.

**VERSION**  

commit cf927b1f0823b51a519fcec6f1919b092a58918e  

Date: Sat Nov 17 07:27:28 2018 +0000

**REPRODUCTION CASE**  

Open attached file.

ADDITIONAL INFORMATION

# Rendering PDF file /workarea/samplestore/wip/pdfium/tomb/issue\_1/victory\_0053af103aa10c0ebc3c336323638801f9528c65e604a15e2b340bc605ad1c10. AddressSanitizer:DEADLYSIGNAL

==30359==ERROR: AddressSanitizer: SEGV on unknown address 0x55555582ca64 (pc 0x55555582ca64 bp 0x7fffffffa8b0 sp 0x7fffffffa798 T0)  

==30359==The signal is caused by a READ memory access.  

==30359==Hint: PC is at a non-executable region. Maybe a wild jump?  

#0 0x55555582ca63 in ?? ??:0  

#1 0x55555582ca63 in ?? ??:0  

#2 0x555557ef144c in CXFA\_FFTextEdit::OnSetFocus(CXFA\_FFWidget\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_fftextedit.cpp:167  

#3 0x555557ef144c in ?? ??:0  

#4 0x555557e96ee0 in CXFA\_FFDocView::SetFocus(CXFA\_FFWidget\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:288  

#5 0x555557e96ee0 in ?? ??:0  

#6 0x555557e942e5 in CXFA\_FFDocView::SetFocusNode(CXFA\_Node\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:306  

#7 0x555557e942e5 in ?? ??:0  

#8 0x555557eb880d in CXFA\_FFNotify::SetFocusWidgetNode(CXFA\_Node\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffnotify.cpp:302  

#9 0x555557eb880d in ?? ??:0  

#10 0x5555576e1558 in CJX\_HostPseudoModel::setFocus(CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fxjs/xfa/cjx\_hostpseudomodel.cpp:462  

#11 0x5555576e1558 in ?? ??:0  

#12 0x5555576e5101 in CJS\_Result JSMethod<CJX\_HostPseudoModel, &CJX\_HostPseudoModel::setFocus>(CJX\_HostPseudoModel\*, CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fxjs/jse\_define.h:22  

#13 0x5555576e5101 in ?? ??:0  

#14 0x5555576db98a in CJX\_HostPseudoModel::setFocus\_static(CJX\_Object\*, CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fxjs/xfa/cjx\_hostpseudomodel.h:36  

#15 0x5555576db98a in ?? ??:0  

#16 0x55555770b3e4 in CJX\_Object::RunMethod(fxcrt::WideString const&, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fxjs/xfa/cjx\_object.cpp:178  

#17 0x55555770b3e4 in ?? ??:0  

#18 0x555557606a85 in CFXJSE\_Engine::NormalMethodCall(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, fxcrt::WideString const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fxjs/cfxjse\_engine.cpp:452  

#19 0x555557606a85 in ?? ??:0  

#20 0x5555575f0616 in (anonymous namespace)::DynPropGetterAdapter\_MethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fxjs/cfxjse\_class.cpp:112  

#21 0x5555575f0616 in ?? ??:0  

#22 0x7ffff46db6f6 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../v8/src/api-arguments-inl.h:146  

#23 0x7ffff46db6f6 in ?? ??:0  

#24 0x7ffff46d7999 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../v8/src/builtins/builtins-api.cc:108  

#25 0x7ffff46d7999 in ?? ??:0  

#26 0x7ffff46d2e61 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../v8/src/builtins/builtins-api.cc:138  

#27 0x7ffff46d2e61 in ?? ??:0  

#28 0x7ffff46d1eb8 in v8::internal::Builtin\_HandleApiCall(int, unsigned long\*, v8::internal::Isolate\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../v8/src/builtins/builtins-api.cc:126  

#29 0x7ffff46d1eb8 in ?? ??:0  

#30 0x7ffff6ee8111 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit embedded.cc:?  

#31 0x7ffff6ee8111 in ?? ??:0  

#16 0x7eafde08ad0c (<unknown module>)  

#32 0x7ffff6c271a5 in Builtins\_ArgumentsAdaptorTrampoline embedded.cc:?  

#33 0x7ffff6c271a5 in ?? ??:0  

#18 0x7eafde08ad0c (<unknown module>)  

#34 0x7ffff6c271a5 in Builtins\_ArgumentsAdaptorTrampoline embedded.cc:?  

#35 0x7ffff6c271a5 in ?? ??:0  

#36 0x7ffff6c31402 in Builtins\_JSEntryTrampoline embedded.cc:?  

#37 0x7ffff6c31402 in ?? ??:0  

#21 0x7eafde082136 (<unknown module>)  

#38 0x7ffff5536e2a in Call /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../v8/src/simulator.h:113  

#39 0x7ffff5536e2a in Invoke /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../v8/src/execution.cc:156  

#40 0x7ffff5536e2a in ?? ??:0  

#41 0x7ffff55359af in v8::internal::(anonymous namespace)::CallInternal(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../v8/src/execution.cc:192  

#42 0x7ffff55359af in ?? ??:0  

#43 0x7ffff55356d6 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../v8/src/execution.cc:203  

#44 0x7ffff55356d6 in ?? ??:0  

#45 0x7ffff44880f2 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../v8/src/api.cc:5002  

#46 0x7ffff44880f2 in ?? ??:0  

#47 0x5555575fa1d8 in CFXJSE\_Context::ExecuteScript(char const\*, CFXJSE\_Value\*, CFXJSE\_Value\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fxjs/cfxjse\_context.cpp:304  

#48 0x5555575fa1d8 in ?? ??:0  

#49 0x55555760b240 in CFXJSE\_Engine::RunScript(CXFA\_Script::Type, fxcrt::StringViewTemplate<wchar\_t> const&, CFXJSE\_Value\*, CXFA\_Object\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fxjs/cfxjse\_engine.cpp:149  

#50 0x55555760b240 in ?? ??:0  

#51 0x555557cdcc57 in CXFA\_Node::ExecuteBoolScript(CXFA\_FFDocView\*, CXFA\_Script\*, CXFA\_EventParam\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:2372  

#52 0x555557cdcc57 in ?? ??:0  

#53 0x555557cd6fe9 in CXFA\_Node::ExecuteScript(CXFA\_FFDocView\*, CXFA\_Script\*, CXFA\_EventParam\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:2331  

#54 0x555557cd6fe9 in ?? ??:0  

#55 0x555557cd6d0c in CXFA\_Node::ProcessEvent(CXFA\_FFDocView\*, CXFA\_Event\*, CXFA\_EventParam\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:2032  

#56 0x555557cd6d0c in ?? ??:0  

#57 0x555557cd5e68 in CXFA\_Node::ProcessEvent(CXFA\_FFDocView\*, XFA\_AttributeEnum, CXFA\_EventParam\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:2014  

#58 0x555557cd5e68 in ?? ??:0  

#59 0x555557e975a7 in XFA\_ProcessEvent(CXFA\_FFDocView\*, CXFA\_Node\*, CXFA\_EventParam\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:355  

#60 0x555557e975a7 in ?? ??:0  

#61 0x555557e928ab in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:378  

#62 0x555557e928ab in ?? ??:0  

#63 0x555557e929f5 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:388  

#64 0x555557e929f5 in ?? ??:0  

#65 0x555557e929f5 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:388  

#66 0x555557e929f5 in ?? ??:0  

#67 0x555557e929f5 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:388  

#68 0x555557e929f5 in ?? ??:0  

#69 0x555557e929f5 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:388  

#70 0x555557e929f5 in ?? ??:0  

#71 0x555557e934e3 in CXFA\_FFDocView::StopLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:127  

#72 0x555557e934e3 in ?? ??:0  

#73 0x555557faff33 in CPDFXFA\_Context::LoadXFADoc() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:137  

#74 0x555557faff33 in ?? ??:0  

#75 0x555558107553 in FPDF\_LoadXFA /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_view.cpp:255  

#76 0x555558107553 in ?? ??:0  

#77 0x55555608faa3 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:790  

#78 0x55555608faa3 in ?? ??:0  

#79 0x55555608a708 in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:1002  

#80 0x55555608a708 in ?? ??:0  

#81 0x7ffff1a7482f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291  

#82 0x7ffff1a7482f in ?? ??:0

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/pdfium\_test+0x2d8a63)  

==30359==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [wild_jump.pdf](attachments/wild_jump.pdf) (application/pdf, 79.7 KB)

## Timeline

### cl...@chromium.org (2018-11-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5909434792148992.

### cl...@chromium.org (2018-11-21)

Testcase 5909434792148992 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5909434792148992.

### cl...@chromium.org (2018-11-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6531410430787584.

### mb...@chromium.org (2018-11-21)

dsinclair: Would you mind taking a look or reassigning this?

[Monorail components: Internals>Plugins>PDF]

### ds...@chromium.org (2018-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-11-22)

Detailed report: https://clusterfuzz.com/testcase?key=6531410430787584

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x562a025a2445
Crash State:
  CXFA_FFTextEdit::OnSetFocus
  CXFA_FFDocView::SetFocus
  CXFA_FFDocView::SetFocusNode
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=576003:576006

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6531410430787584

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reference.md for more information.

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### mb...@chromium.org (2018-11-22)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-11-26)

XFA is not shipped (yet).

### ts...@chromium.org (2018-11-26)

This is a job for VSAN, and it says:

./../xfa/fxfa/cxfa_ffwidget.cpp:564:12: runtime error: downcast of address 0x5653cecca800 which does not point to an object of type 'CXFA_FFWidget'
0x5653cecca800: note: object is of type 'CXFA_ContentLayoutItem'
 00 00 00 00  50 8f 0d cd 53 56 00 00  b0 9e cc ce 53 56 00 00  40 9f cc ce 53 56 00 00  40 a9 cc ce
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CXFA_ContentLayoutItem'
    #0 0x5653cbff3132 in CXFA_FFWidget::GetParent() ./../../xfa/fxfa/cxfa_ffwidget.cpp:564:12
    #1 0x5653cbff2c51 in CXFA_FFWidget::OnSetFocus(CXFA_FFWidget*) ./../../xfa/fxfa/cxfa_ffwidget.cpp:401:28
    #2 0x5653cbfeb035 in CXFA_FFTextEdit::OnSetFocus(CXFA_FFWidget*) ./../../xfa/fxfa/cxfa_fftextedit.cpp:167:18
    #3 0x5653cbfb06a2 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) ./../../xfa/fxfa/cxfa_ffdocview.cpp:288:18
    #4 0x5653cbfaecb6 in CXFA_FFDocView::SetFocusNode(CXFA_Node*) ./../../xfa/fxfa/cxfa_ffdocview.cpp:306:8
    #5 0x5653cb244d16 in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/xfa/cjx_hostpseudomodel.cpp:462:12
    #6 0x5653cb247f31 in CJS_Result JSMethod<CJX_HostPseudoModel, &(CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(CJX_HostPseudoModel*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/jse_define.h:22:10
    #7 0x5653cb23f9bc in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/xfa/cjx_hostpseudomodel.h:36:3
    #8 0x5653cb2688a7 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/xfa/cjx_object.cpp:178:10
    #9 0x5653cb1d86d7 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) ./../../fxjs/cfxjse_engine.cpp:452:31
    #10 0x5653cb1d426b in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./../../fxjs/cfxjse_class.cpp:112:7
    #11 0x5653cb30d897 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) ./../../v8/src/api-arguments-inl.h:146:3
    #12 0x5653cb30ce71 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:108:36
    #13 0x5653cb30c5ff in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:138:5
    #14 0x5653cbb8668a in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit ??:0:0

../../xfa/fxfa/cxfa_ffwidget.cpp:402:28: runtime error: member call on address 0x5653cecca800 which does not point to an object of type 'CXFA_FFWidget'
0x5653cecca800: note: object is of type 'CXFA_ContentLayoutItem'
 00 00 00 00  50 8f 0d cd 53 56 00 00  b0 9e cc ce 53 56 00 00  40 9f cc ce 53 56 00 00  40 a9 cc ce
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CXFA_ContentLayoutItem'
    #0 0x5653cbff2f5b in CXFA_FFWidget::OnSetFocus(CXFA_FFWidget*) ./../../xfa/fxfa/cxfa_ffwidget.cpp:402:28
    #1 0x5653cbfeb035 in CXFA_FFTextEdit::OnSetFocus(CXFA_FFWidget*) ./../../xfa/fxfa/cxfa_fftextedit.cpp:167:18
    #2 0x5653cbfb06a2 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) ./../../xfa/fxfa/cxfa_ffdocview.cpp:288:18
    #3 0x5653cbfaecb6 in CXFA_FFDocView::SetFocusNode(CXFA_Node*) ./../../xfa/fxfa/cxfa_ffdocview.cpp:306:8
    #4 0x5653cb244d16 in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/xfa/cjx_hostpseudomodel.cpp:462:12
    #5 0x5653cb247f31 in CJS_Result JSMethod<CJX_HostPseudoModel, &(CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(CJX_HostPseudoModel*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/jse_define.h:22:10
    #6 0x5653cb23f9bc in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/xfa/cjx_hostpseudomodel.h:36:3
    #7 0x5653cb2688a7 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/xfa/cjx_object.cpp:178:10
    #8 0x5653cb1d86d7 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) ./../../fxjs/cfxjse_engine.cpp:452:31
    #9 0x5653cb1d426b in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./../../fxjs/cfxjse_class.cpp:112:7
    #10 0x5653cb30d897 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) ./../../v8/src/api-arguments-inl.h:146:3
    #11 0x5653cb30ce71 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:108:36
    #12 0x5653cb30c5ff in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:138:5
    #13 0x5653cbb8668a in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit ??:0:0

../../xfa/fxfa/cxfa_ffwidget.cpp:403:14: runtime error: member call on address 0x5653cecca800 which does not point to an object of type 'CXFA_FFWidget'
0x5653cecca800: note: object is of type 'CXFA_ContentLayoutItem'
 00 00 00 00  50 8f 0d cd 53 56 00 00  b0 9e cc ce 53 56 00 00  40 9f cc ce 53 56 00 00  40 a9 cc ce
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CXFA_ContentLayoutItem'
    #0 0x5653cbff2f86 in CXFA_FFWidget::OnSetFocus(CXFA_FFWidget*) ./../../xfa/fxfa/cxfa_ffwidget.cpp:403:14
    #1 0x5653cbfeb035 in CXFA_FFTextEdit::OnSetFocus(CXFA_FFWidget*) ./../../xfa/fxfa/cxfa_fftextedit.cpp:167:18
    #2 0x5653cbfb06a2 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) ./../../xfa/fxfa/cxfa_ffdocview.cpp:288:18
    #3 0x5653cbfaecb6 in CXFA_FFDocView::SetFocusNode(CXFA_Node*) ./../../xfa/fxfa/cxfa_ffdocview.cpp:306:8
    #4 0x5653cb244d16 in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/xfa/cjx_hostpseudomodel.cpp:462:12
    #5 0x5653cb247f31 in CJS_Result JSMethod<CJX_HostPseudoModel, &(CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(CJX_HostPseudoModel*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/jse_define.h:22:10
    #6 0x5653cb23f9bc in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/xfa/cjx_hostpseudomodel.h:36:3
    #7 0x5653cb2688a7 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../fxjs/xfa/cjx_object.cpp:178:10
    #8 0x5653cb1d86d7 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) ./../../fxjs/cfxjse_engine.cpp:452:31
    #9 0x5653cb1d426b in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./../../fxjs/cfxjse_class.cpp:112:7
    #10 0x5653cb30d897 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) ./../../v8/src/api-arguments-inl.h:146:3
    #11 0x5653cb30ce71 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:108:36
    #12 0x5653cb30c5ff in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:138:5
    #13 0x5653cbb8668a in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit ??:0:0


### ts...@chromium.org (2018-11-26)

If you want to follow along, set the usual gn args plus these two:
  is_ubsan = true
  is_ubsan_vptr = true
then copy the files from chromium/src/tools/ubsan to a newly-created pdfium/tools/ubsan directory

### ts...@chromium.org (2018-11-26)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/45850

### bu...@chromium.org (2018-11-27)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/e26b6502c7e5b144b2f5e3d44ecc6f567493b123

commit e26b6502c7e5b144b2f5e3d44ecc6f567493b123
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Nov 27 00:08:24 2018

Use checked downcasts between CFXA_LayoutItem and CXFA_FFWidget.

Since not all CFXA_LayoutItems are CXFA_FFWidgets.
Move some conversion helpers to parent class while at it, and
use them in other places.

Bug: chromium:907430
Change-Id: I02f9f28be77dbf7e30baf7c7aed199a81401ca88
Reviewed-on: https://pdfium-review.googlesource.com/c/45850
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/cxfa_ffdocview.cpp
[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/parser/cxfa_traversestrategy_contentareacontainerlayoutitem.h
[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/cxfa_ffwidgethandler.cpp
[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/cxfa_ffwidget.cpp
[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/parser/cxfa_layoutitem.h
[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/cxfa_ffwidget.h
[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/parser/cxfa_contentlayoutitem.cpp
[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/parser/cxfa_node.cpp
[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/parser/cxfa_containerlayoutitem.h
[modify] https://crrev.com/e26b6502c7e5b144b2f5e3d44ecc6f567493b123/xfa/fxfa/parser/cxfa_contentlayoutitem.h


### bu...@chromium.org (2018-11-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/68459b912cf5c975558bde0a639cda62be5fd32f

commit 68459b912cf5c975558bde0a639cda62be5fd32f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Nov 27 10:00:49 2018

Roll src/third_party/pdfium cf927b1f0823..b4c95fe2ded4 (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/cf927b1f0823..b4c95fe2ded4


git log cf927b1f0823..b4c95fe2ded4 --date=short --no-merges --format='%ad %ae %s'
2018-11-27 tsepez@chromium.org Rename WideString::{UTF8,UTF16LE}_Encode() to To{UTF8,UTF16LE}().
2018-11-27 tsepez@chromium.org Rename WideString::FromLocal() to FromDefANSI().
2018-11-27 tsepez@chromium.org XFA: Do not use UnownedPtr between CXFA_Nodes.
2018-11-27 tsepez@chromium.org Use checked downcasts between CFXA_LayoutItem and CXFA_FFWidget.
2018-11-26 tsepez@chromium.org Break circular dependence between {Byte,Wide}String


Created with:
  gclient setdep -r src/third_party/pdfium@b4c95fe2ded4

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:907427,chromium:907430
TBR=dsinclair@chromium.org

Change-Id: I25a82288ee6ebf33c7fad0e1688c1d416bb8dbff
Reviewed-on: https://chromium-review.googlesource.com/c/1351883
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#611057}
[modify] https://crrev.com/68459b912cf5c975558bde0a639cda62be5fd32f/DEPS


### cl...@chromium.org (2018-11-28)

ClusterFuzz has detected this issue as fixed in range 611056:611063.

Detailed report: https://clusterfuzz.com/testcase?key=6531410430787584

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x562a025a2445
Crash State:
  CXFA_FFTextEdit::OnSetFocus
  CXFA_FFDocView::SetFocus
  CXFA_FFDocView::SetFocusNode
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=576003:576006
Fixed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=611056:611063

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6531410430787584

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reference.md for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-11-28)

ClusterFuzz testcase 6531410430787584 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-11-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-07)

Nice one! The Chrome VRP panel decided to award $3,000 for this report - cheers!

### aw...@google.com (2018-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-03-06)

This issue was migrated from crbug.com/chromium/907430?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093153)*
