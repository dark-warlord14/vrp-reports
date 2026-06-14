# Security: pdfium(XFA) heap-use-after-free in CXFA_FFComboBox::OnProcessEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40050936](https://issues.chromium.org/issues/40050936) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-12-10 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36

Steps to reproduce the problem:
1.build pdfium_test with XFA enable
2../pdfium_test uaf0.pdf
3.

What is the expected behavior?

What went wrong?
ASAN log here,  I'll post the details later.

Rendering PDF file crash/uaf0.pdf.
Document has invalid cross reference table
=================================================================
==59169==ERROR: AddressSanitizer: heap-use-after-free on address 0x60d00001b038 at pc 0x55fc0e8fe62d bp 0x7fff173856f0 sp 0x7fff173856e8
READ of size 8 at 0x60d00001b038 thread T0
    #0 0x55fc0e8fe62c in operator-> core/fxcrt/unowned_ptr.h:112:34
    #1 0x55fc0e8fe62c in CXFA_FFComboBox::OnProcessEvent(CFWL_Event*) xfa/fxfa/cxfa_ffcombobox.cpp:361
    #2 0x55fc0ea1ccdd in CFWL_EventTarget::ProcessEvent(CFWL_Event*) xfa/fwl/cfwl_eventtarget.cpp:29:14
    #3 0x55fc0ea39c80 in CFWL_NoteDriver::SendEvent(CFWL_Event*) xfa/fwl/cfwl_notedriver.cpp:33:20
    #4 0x55fc0ea018c4 in CFWL_ComboBox::OnProcessEvent(CFWL_Event*) xfa/fwl/cfwl_combobox.cpp:496:5
    #5 0x55fc0e8fe54b in CXFA_FFComboBox::OnProcessEvent(CFWL_Event*) xfa/fxfa/cxfa_ffcombobox.cpp:361:19
    #6 0x55fc0ea12bec in OnTextWillChange xfa/fwl/cfwl_edit.cpp:305:3
    #7 0x55fc0ea12bec in non-virtual thunk to CFWL_Edit::OnTextWillChange(CFDE_TextEditEngine::TextChange*) xfa/fwl/cfwl_edit.cpp
    #8 0x55fc0e9a3a42 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:283:16
    #9 0x55fc0e9fe6d6 in CFWL_ComboBox::SetCurSel(int) xfa/fwl/cfwl_combobox.cpp:153:16
    #10 0x55fc0e8fc781 in CXFA_FFComboBox::UpdateFWLData() xfa/fxfa/cxfa_ffcombobox.cpp:199:16
    #11 0x55fc0eb5a027 in CXFA_Node::UpdateUIDisplay(CXFA_FFDocView*, CXFA_FFWidget*) xfa/fxfa/parser/cxfa_node.cpp:3086:14
    #12 0x55fc0e90c47c in ResetSingleNodeData xfa/fxfa/cxfa_ffdocview.cpp:218:10
    #13 0x55fc0e90c47c in CXFA_FFDocView::ResetNode(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:245
    #14 0x55fc0c4075cc in CJX_HostPseudoModel::resetData(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:404:14
    #15 0x55fc0c402184 in CJX_HostPseudoModel::resetData_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:37:3
    #16 0x55fc0c41efa3 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:177:10
    #17 0x55fc0c36fe67 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:483:31
    #18 0x55fc0c369e59 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #19 0x55fc0c5a957a in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #20 0x55fc0c5a6a1c in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #21 0x55fc0c5a475a in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #22 0x55fc0e6edf18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3efff18)
    #23 0x55fc0e66dca3 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7fca3)
    #24 0x55fc0e66761b in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7961b)
    #25 0x55fc0e66dca3 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7fca3)
    #26 0x55fc0e66761b in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7961b)
    #27 0x55fc0e66b65c in Builtins_JSEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7d65c)
    #28 0x55fc0e66b437 in Builtins_JSEntry (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7d437)
    #29 0x55fc0c88b5db in Call v8/src/execution/simulator.h:138:12
    #30 0x55fc0c88b5db in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:267
    #31 0x55fc0c88a9d4 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:359:10
    #32 0x55fc0c48d23c in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:4762:7
    #33 0x55fc0c36c026 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:301:21
    #34 0x55fc0c375013 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:153:23
    #35 0x55fc0eb60005 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2696:22
    #36 0x55fc0eb57fda in ExecuteScript xfa/fxfa/parser/cxfa_node.cpp:2656:10
    #37 0x55fc0eb57fda in ProcessEventInternal xfa/fxfa/parser/cxfa_node.cpp:2360
    #38 0x55fc0eb57fda in CXFA_Node::ProcessEvent(CXFA_FFDocView*, XFA_AttributeValue, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2337
    #39 0x55fc0e8fdace in FWLEventSelChange xfa/fxfa/cxfa_ffcombobox.cpp:137:12
    #40 0x55fc0e8fdace in CXFA_FFComboBox::OnTextChanged(CFWL_Widget*, fxcrt::WideString const&) xfa/fxfa/cxfa_ffcombobox.cpp:308
    #41 0x55fc0e8fe21a in CXFA_FFComboBox::OnProcessEvent(CFWL_Event*) xfa/fxfa/cxfa_ffcombobox.cpp:347:7
    #42 0x55fc0ea1ccdd in CFWL_EventTarget::ProcessEvent(CFWL_Event*) xfa/fwl/cfwl_eventtarget.cpp:29:14
    #43 0x55fc0ea39c80 in CFWL_NoteDriver::SendEvent(CFWL_Event*) xfa/fwl/cfwl_notedriver.cpp:33:20
    #44 0x55fc0ea018c4 in CFWL_ComboBox::OnProcessEvent(CFWL_Event*) xfa/fwl/cfwl_combobox.cpp:496:5
    #45 0x55fc0e8fe54b in CXFA_FFComboBox::OnProcessEvent(CFWL_Event*) xfa/fxfa/cxfa_ffcombobox.cpp:361:19
    #46 0x55fc0ea12bec in OnTextWillChange xfa/fwl/cfwl_edit.cpp:305:3
    #47 0x55fc0ea12bec in non-virtual thunk to CFWL_Edit::OnTextWillChange(CFDE_TextEditEngine::TextChange*) xfa/fwl/cfwl_edit.cpp
    #48 0x55fc0e9a3a42 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:283:16
    #49 0x55fc0e9fd10d in CFWL_ComboBox::Layout() xfa/fwl/cfwl_combobox.cpp:311:14
    #50 0x55fc0e916428 in CXFA_FFField::PerformLayout() xfa/fxfa/cxfa_fffield.cpp:182:24
    #51 0x55fc0e915bfe in CXFA_FFField::LoadWidget() xfa/fxfa/cxfa_fffield.cpp:150:3
    #52 0x55fc0e8fc0be in CXFA_FFComboBox::LoadWidget() xfa/fxfa/cxfa_ffcombobox.cpp:73:24
    #53 0x55fc0e90ceb3 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:295:20
    #54 0x55fc0e9098cf in CXFA_FFDocView::SetFocusNode(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:316:8
    #55 0x55fc0c407cdc in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:466:12
    #56 0x55fc0c4022e4 in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #57 0x55fc0c41efa3 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:177:10
    #58 0x55fc0c36fe67 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:483:31
    #59 0x55fc0c369e59 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #60 0x55fc0c5a957a in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #61 0x55fc0c5a6a1c in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #62 0x55fc0c5a475a in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #63 0x55fc0e6edf18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3efff18)
    #64 0x55fc0e66dca3 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7fca3)
    #65 0x55fc0e66761b in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7961b)
    #66 0x55fc0e66dca3 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7fca3)
    #67 0x55fc0e66761b in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7961b)
    #68 0x55fc0e66b65c in Builtins_JSEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7d65c)
    #69 0x55fc0e66b437 in Builtins_JSEntry (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7d437)
    #70 0x55fc0c88b5db in Call v8/src/execution/simulator.h:138:12
    #71 0x55fc0c88b5db in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:267
    #72 0x55fc0c88a9d4 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:359:10
    #73 0x55fc0c48d23c in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:4762:7
    #74 0x55fc0c36c026 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:301:21
    #75 0x55fc0c375013 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:153:23
    #76 0x55fc0eb60005 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2696:22
    #77 0x55fc0eb591b9 in ExecuteScript xfa/fxfa/parser/cxfa_node.cpp:2656:10
    #78 0x55fc0eb591b9 in CXFA_Node::ProcessCalculate(CXFA_FFDocView*) xfa/fxfa/parser/cxfa_node.cpp:2395
    #79 0x55fc0e907a93 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:389:12
    #80 0x55fc0e907793 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:400:20
    #81 0x55fc0e907793 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:400:20
    #82 0x55fc0c400b20 in CJX_Form::recalculate(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_form.cpp:96:12
    #83 0x55fc0c400344 in CJX_Form::recalculate_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_form.h:27:3
    #84 0x55fc0c41efa3 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:177:10
    #85 0x55fc0c36fe67 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:483:31
    #86 0x55fc0c369e59 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #87 0x55fc0c5a957a in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #88 0x55fc0c5a6a1c in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #89 0x55fc0c5a475a in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #90 0x55fc0e6edf18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3efff18)
    #91 0x55fc0e66dca3 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7fca3)
    #92 0x55fc0e66761b in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7961b)
    #93 0x55fc0e66dca3 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7fca3)
    #94 0x55fc0e66761b in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7961b)
    #95 0x55fc0e66b65c in Builtins_JSEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7d65c)
    #96 0x55fc0e66b437 in Builtins_JSEntry (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7d437)
    #97 0x55fc0c88b5db in Call v8/src/execution/simulator.h:138:12
    #98 0x55fc0c88b5db in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:267
    #99 0x55fc0c88a9d4 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:359:10
    #100 0x55fc0c48d23c in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:4762:7
    #101 0x55fc0c36c026 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:301:21
    #102 0x55fc0c375013 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:153:23
    #103 0x55fc0eb60005 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2696:22
    #104 0x55fc0eb57fda in ExecuteScript xfa/fxfa/parser/cxfa_node.cpp:2656:10
    #105 0x55fc0eb57fda in ProcessEventInternal xfa/fxfa/parser/cxfa_node.cpp:2360
    #106 0x55fc0eb57fda in CXFA_Node::ProcessEvent(CXFA_FFDocView*, XFA_AttributeValue, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2337
    #107 0x55fc0e9079e3 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:413:35
    #108 0x55fc0e907793 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:400:20
    #109 0x55fc0e907793 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:400:20
    #110 0x55fc0e908793 in InitLayout xfa/fxfa/cxfa_ffdocview.cpp:68:3
    #111 0x55fc0e908793 in CXFA_FFDocView::StopLayout() xfa/fxfa/cxfa_ffdocview.cpp:125
    #112 0x55fc0ebec6f7 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:130:18
    #113 0x55fc0b984cd3 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:262:22
    #114 0x55fc0b8e2e17 in RenderPdf samples/pdfium_test.cc:905:12
    #115 0x55fc0b8e2e17 in main samples/pdfium_test.cc:1151
    #116 0x7f7a30c2b82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

0x60d00001b038 is located 136 bytes inside of 144-byte region [0x60d00001afb0,0x60d00001b040)
freed by thread T0 here:
    #0 0x55fc0b8da2dd in operator delete(void*) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:166:3
    #1 0x55fc0ea6be6f in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #2 0x55fc0ea6be6f in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #3 0x55fc0ea6be6f in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2605
    #4 0x55fc0ea6be6f in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:29
    #5 0x55fc0ea6c01c in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #6 0x55fc0ea999c8 in Release core/fxcrt/retained_tree_node.h:71:7
    #7 0x55fc0ea999c8 in operator() core/fxcrt/retain_ptr.h:20
    #8 0x55fc0ea999c8 in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #9 0x55fc0ea999c8 in operator= core/fxcrt/retain_ptr.h:69
    #10 0x55fc0ea999c8 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:25
    #11 0x55fc0ea998f3 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:24:5
    #12 0x55fc0ea998f3 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:24:5
    #13 0x55fc0ea998f3 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:24:5
    #14 0x55fc0ea9e89d in CXFA_ViewLayoutProcessor::PrepareLayout() xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:1906:7
    #15 0x55fc0ea9d502 in CXFA_ViewLayoutProcessor::InitLayoutPage(CXFA_Node*) xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:352:3
    #16 0x55fc0ea9aef5 in CXFA_LayoutProcessor::StartLayout(bool) xfa/fxfa/layout/cxfa_layoutprocessor.cpp:55:32
    #17 0x55fc0ea9b747 in CXFA_LayoutProcessor::IncrementLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:107:5
    #18 0x55fc0e90957b in CXFA_FFDocView::RunLayout() xfa/fxfa/cxfa_ffdocview.cpp:457:25
    #19 0x55fc0e90af26 in CXFA_FFDocView::UpdateDocView() xfa/fxfa/cxfa_ffdocview.cpp:189:7
    #20 0x55fc0c405ba7 in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:320:12
    #21 0x55fc0c401da4 in CJX_HostPseudoModel::openList_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:33:3
    #22 0x55fc0c41efa3 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:177:10
    #23 0x55fc0c36fe67 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:483:31
    #24 0x55fc0c369e59 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #25 0x55fc0c5a957a in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #26 0x55fc0c5a6a1c in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #27 0x55fc0c5a475a in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #28 0x55fc0e6edf18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3efff18)
    #29 0x55fc0e66dca3 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7fca3)
    #30 0x55fc0e66761b in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7961b)
    #31 0x55fc0e66dca3 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7fca3)
    #32 0x55fc0e66761b in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7961b)
    #33 0x55fc0e66b65c in Builtins_JSEntryTrampoline (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7d65c)
    #34 0x55fc0e66b437 in Builtins_JSEntry (/home/krace/tools/pdfium/out/Debug/pdfium_test+0x3e7d437)
    #35 0x55fc0c88b5db in Call v8/src/execution/simulator.h:138:12
    #36 0x55fc0c88b5db in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:267
    #37 0x55fc0c88a9d4 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:359:10

previously allocated by thread T0 here:
    #0 0x55fc0b8d9a7d in operator new(unsigned long) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:105:3
    #1 0x55fc0e92653b in MakeUnique<CXFA_FFComboBox, CXFA_Node *&> third_party/base/ptr_util.h:56:29
    #2 0x55fc0e92653b in CXFA_FFNotify::OnCreateContentLayoutItem(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:146
    #3 0x55fc0ea6db14 in CXFA_ContentLayoutProcessor::CreateContentLayoutItem(CXFA_Node*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:644:27
    #4 0x55fc0ea95b11 in CXFA_ContentLayoutProcessor::DoLayoutField() xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2024:19
    #5 0x55fc0ea7b79b in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2084:7
    #6 0x55fc0ea78c89 in CXFA_ContentLayoutProcessor::DoLayoutPositionedContainer(CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1079:17
    #7 0x55fc0ea7ba87 in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2073:11
    #8 0x55fc0ea9b277 in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:80:36
    #9 0x55fc0e9080a1 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:98:30
    #10 0x55fc0ebec6dc in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:129:18
    #11 0x55fc0b984cd3 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:262:22
    #12 0x55fc0b8e2e17 in RenderPdf samples/pdfium_test.cc:905:12
    #13 0x55fc0b8e2e17 in main samples/pdfium_test.cc:1151
    #14 0x7f7a30c2b82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-use-after-free core/fxcrt/unowned_ptr.h:112:34 in operator->
Shadow bytes around the buggy address:
  0x0c1a7fffb5b0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x0c1a7fffb5c0: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1a7fffb5d0: fd fd fd fa fa fa fa fa fa fa fa fa 00 00 00 00
  0x0c1a7fffb5e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
  0x0c1a7fffb5f0: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
=>0x0c1a7fffb600: fd fd fd fd fd fd fd[fd]fa fa fa fa fa fa fa fa
  0x0c1a7fffb610: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1a7fffb620: fd fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd
  0x0c1a7fffb630: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c1a7fffb640: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c1a7fffb650: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==59169==ABORTING

Did this work before? N/A 

Chrome version:   Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [uaf0.pdf](attachments/uaf0.pdf) (application/pdf, 2.2 KB)

## Timeline

### cl...@chromium.org (2019-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6495585695760384.

### cl...@chromium.org (2019-12-10)

Automatically adding ccs based on OWNERS file / target commit history.

If this is incorrect, please add the ClusterFuzz-Wrong label.

### cl...@chromium.org (2019-12-10)

Detailed Report: https://clusterfuzz.com/testcase?key=6495585695760384

Fuzzing Engine: libFuzzer
Fuzz Target: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d000016d98
Crash State:
  fxcrt::UnownedPtr<IFWL_WidgetDelegate>::operator->
  CXFA_FFComboBox::OnProcessEvent
  CFWL_EventTarget::ProcessEvent
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=570849:570850

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6495585695760384

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### cl...@chromium.org (2019-12-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-12-10)

Automatically assigning owner based on suspected regression changelist https://pdfium.googlesource.com/pdfium/+/2d7cb9267899902ce455165303e2373ac38c867d (Use unowned ptr for IFWL_ delegates).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### sh...@chromium.org (2019-12-10)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-10)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-12-10)

XFA == not shipped.

### ts...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### me...@gmail.com (2019-12-11)

[Comment Deleted]

### ts...@chromium.org (2019-12-13)

This is going to take a while to disentangle, but for now we can trap at the point of the bad destruction and thereby change a security issue into a functional issue (hard crash).  That's a small step forward at https://pdfium-review.googlesource.com/c/pdfium/+/63751


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-13)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/fc3b3ed16213f819c28ed77f782f725b9bf66e69

commit fc3b3ed16213f819c28ed77f782f725b9bf66e69
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Dec 13 21:27:17 2019

Ensure CFWL_Widgets are not locked during destruction.

This is a strong signal that there is active code below us on
the stack that requires the widget to persist, yet through a twisty
series of callbacks we may reach this spot. Ideally, we'd notice
this earlier and unwind cleanly, but for now it is likely that the
only documents that would reach this case are trying to muck with us,
so aborting may be appropriate.

Bug: chromium:1032422
Change-Id: I78e242cbc157c38666ffb1f248edcde2d79dbca3
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/63751
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/fc3b3ed16213f819c28ed77f782f725b9bf66e69/xfa/fwl/cfwl_widget.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7c1facb77236490fea0909b89aa2c63e929fbe83

commit 7c1facb77236490fea0909b89aa2c63e929fbe83
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Dec 14 01:23:11 2019

Roll src/third_party/pdfium b2cb4336f2e5..fc3b3ed16213 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/b2cb4336f2e5..fc3b3ed16213

git log b2cb4336f2e5..fc3b3ed16213 --date=short --first-parent --format='%ad %ae %s'
2019-12-13 tsepez@chromium.org Ensure CFWL_Widgets are not locked during destruction.
2019-12-13 thestig@chromium.org Clang-format some more code in core/.

Created with:
  gclient setdep -r src/third_party/pdfium@fc3b3ed16213

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1032422
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I82cc98e9b932c0203be0513cf25308d3f10af71b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1967890
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#724872}

[modify] https://crrev.com/7c1facb77236490fea0909b89aa2c63e929fbe83/DEPS


### cl...@chromium.org (2019-12-14)

ClusterFuzz testcase 6495585695760384 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=724871:724872

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### me...@gmail.com (2019-12-14)

[Comment Deleted]

### sh...@chromium.org (2019-12-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-16)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-12-18)

hi tsepez the CL landed in #13 implies this might be an early abort before the underlying UAF is hit, I wonder if there are further CLs to land here to fix the underlying issue?

### ts...@chromium.org (2019-12-18)

Not a priority.  The only PDFs that would hit this are crafted ones trying to mess with us.

### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $5,000 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### me...@gmail.com (2019-12-20)

Thank you for the reward!

### [Deleted User] (2020-03-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1032422?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050936)*
