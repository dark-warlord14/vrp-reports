# pdfium(XFA) heap-use-after-free in CXFA_FFField::OnSetFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40052303](https://issues.chromium.org/issues/40052303) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-05-14 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36

Steps to reproduce the problem:
1.build pdfium_test with XFA
2. ./pdfium_test uaf7.pdf
3.

What is the expected behavior?

What went wrong?
It seems like that `CXFA_FFWidget::OnSetFocus(pOldWidget)` in CXFA_FFField::OnSetFocus at xfa/fxfa/cxfa_fffield.cpp:546 will free widget object. Then it will be used in `GetNormalWidget()` at line 549 ==> UAF.
```
(gdb) l xfa/fxfa/cxfa_fffield.cpp:546
541
542       return true;
543     }
544
545     bool CXFA_FFField::OnSetFocus(CXFA_FFWidget* pOldWidget) {
546       if (!CXFA_FFWidget::OnSetFocus(pOldWidget))  // free here
547         return false;
548
549       if (!GetNormalWidget())   // use here
550         return false;
```

And here is the ASAN log.

Rendering PDF file crash/uaf7.pdf.
Document has invalid cross reference table
=================================================================
==76690==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e000003e00 at pc 0x5646921b0075 bp 0x7ffe6428ba70 sp 0x7ffe6428ba68
READ of size 8 at 0x60e000003e00 thread T0
    #0 0x5646921b0074 in get buildtools/third_party/libc++/trunk/include/memory:2606:19
    #1 0x5646921b0074 in GetNormalWidget xfa/fxfa/cxfa_fffield.cpp:135:26
    #2 0x5646921b0074 in CXFA_FFField::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fffield.cpp:549:8
    #3 0x5646921a08cd in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:304:28
    #4 0x56469219d2ef in CXFA_FFDocView::SetFocusNode(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:335:8
    #5 0x56468f956c9c in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:447:12
    #6 0x56468f9517f4 in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #7 0x56468f96db95 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:178:10
    #8 0x56468f8bb4a4 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:490:31
    #9 0x56468f8b4cad in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:103:7
    #10 0x56468fb0c330 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #11 0x56468fb0971e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #12 0x56468fb072f9 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #13 0x564691f6a737 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x429e737)
    #14 0x564691efd7f4 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x42317f4)
    #15 0x564691ef72fe in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422b2fe)
    #16 0x564691efd7f4 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x42317f4)
    #17 0x564691ef72fe in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422b2fe)
    #18 0x564691efb339 in Builtins_JSEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422f339)
    #19 0x564691efb117 in Builtins_JSEntry (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422f117)
    #20 0x56468fe128d1 in Call v8/src/execution/simulator.h:142:12
    #21 0x56468fe128d1 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:367:33
    #22 0x56468fe114cf in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:461:10
    #23 0x56468f9df07d in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:4873:7
    #24 0x56468f8b73c3 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:286:21
    #25 0x56468f8c0458 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:160:23
    #26 0x5646923f06a8 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2750:22
    #27 0x5646923e8c29 in ExecuteScript xfa/fxfa/parser/cxfa_node.cpp:2710:10
    #28 0x5646923e8c29 in ProcessEventInternal xfa/fxfa/parser/cxfa_node.cpp:2414:14
    #29 0x5646923e8c29 in CXFA_Node::ProcessEvent(CXFA_FFDocView*, XFA_AttributeValue, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2391:9
    #30 0x5646921e3cda in CXFA_FFWidget::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffwidget.cpp:442:12
    #31 0x5646921afd33 in CXFA_FFField::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fffield.cpp:546:23
    #32 0x5646921a09aa in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:317:23
    #33 0x56469219d2ef in CXFA_FFDocView::SetFocusNode(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:335:8
    #34 0x56468f956c9c in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:447:12
    #35 0x56468f9517f4 in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #36 0x56468f96db95 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:178:10
    #37 0x56468f8bb4a4 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:490:31
    #38 0x56468f8b4cad in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:103:7
    #39 0x56468fb0c330 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #40 0x56468fb0971e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #41 0x56468fb072f9 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #42 0x564691f6a737 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x429e737)
    #43 0x564691efd7f4 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x42317f4)
    #44 0x564691ef72fe in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422b2fe)
    #45 0x564691efd7f4 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x42317f4)
    #46 0x564691ef72fe in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422b2fe)
    #47 0x564691efb339 in Builtins_JSEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422f339)
    #48 0x564691efb117 in Builtins_JSEntry (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422f117)
    #49 0x56468fe128d1 in Call v8/src/execution/simulator.h:142:12
    #50 0x56468fe128d1 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:367:33
    #51 0x56468fe114cf in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:461:10
    #52 0x56468f9df07d in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:4873:7
    #53 0x56468f8b73c3 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:286:21
    #54 0x56468f8c0458 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:160:23
    #55 0x5646923f06a8 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2750:22
    #56 0x5646923e8c29 in ExecuteScript xfa/fxfa/parser/cxfa_node.cpp:2710:10
    #57 0x5646923e8c29 in ProcessEventInternal xfa/fxfa/parser/cxfa_node.cpp:2414:14
    #58 0x5646923e8c29 in CXFA_Node::ProcessEvent(CXFA_FFDocView*, XFA_AttributeValue, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2391:9
    #59 0x56468f94844f in CJX_EventPseudoModel::emit(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_eventpseudomodel.cpp:188:19
    #60 0x56468f946c24 in CJX_EventPseudoModel::emit_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_eventpseudomodel.h:44:3
    #61 0x56468f96db95 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:178:10
    #62 0x56468f8bb4a4 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:490:31
    #63 0x56468f8b4cad in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:103:7
    #64 0x56468fb0c330 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #65 0x56468fb0971e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #66 0x56468fb072f9 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #67 0x564691f6a737 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x429e737)
    #68 0x564691efd7f4 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x42317f4)
    #69 0x564691ef72fe in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422b2fe)
    #70 0x564691efd7f4 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x42317f4)
    #71 0x564691ef72fe in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422b2fe)
    #72 0x564691efb339 in Builtins_JSEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422f339)
    #73 0x564691efb117 in Builtins_JSEntry (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422f117)
    #74 0x56468fe128d1 in Call v8/src/execution/simulator.h:142:12
    #75 0x56468fe128d1 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:367:33
    #76 0x56468fe114cf in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:461:10
    #77 0x56468f9df07d in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:4873:7
    #78 0x56468f8b73c3 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:286:21
    #79 0x56468f8c0458 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:160:23
    #80 0x5646923f06a8 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2750:22
    #81 0x5646923e8c29 in ExecuteScript xfa/fxfa/parser/cxfa_node.cpp:2710:10
    #82 0x5646923e8c29 in ProcessEventInternal xfa/fxfa/parser/cxfa_node.cpp:2414:14
    #83 0x5646923e8c29 in CXFA_Node::ProcessEvent(CXFA_FFDocView*, XFA_AttributeValue, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2391:9
    #84 0x56469219bbae in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:430:35
    #85 0x56469219b953 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:417:20
    #86 0x56469219c724 in CXFA_FFDocView::StopLayout() xfa/fxfa/cxfa_ffdocview.cpp:130:3
    #87 0x564692480d77 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:171:18
    #88 0x56468eee30a3 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:209:22
    #89 0x56468ee410a9 in RenderPdf samples/pdfium_test.cc:955:12
    #90 0x56468ee410a9 in main samples/pdfium_test.cc:1203:5
    #91 0x7fcd8cd2e82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

0x60e000003e00 is located 128 bytes inside of 152-byte region [0x60e000003d80,0x60e000003e18)
freed by thread T0 here:
    #0 0x56468ee367cd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x5646922ff662 in operator() buildtools/third_party/libc++/trunk/include/memory:2378:5
    #2 0x5646922ff662 in reset buildtools/third_party/libc++/trunk/include/memory:2633:7
    #3 0x5646922ff662 in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2587:19
    #4 0x5646922ff662 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:29:1
    #5 0x5646922ff81c in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #6 0x5646921e3dac in Release core/fxcrt/retained_tree_node.h:71:7
    #7 0x5646921e3dac in operator() core/fxcrt/retain_ptr.h:20:47
    #8 0x5646921e3dac in reset buildtools/third_party/libc++/trunk/include/memory:2633:7
    #9 0x5646921e3dac in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2587:19
    #10 0x5646921e3dac in ~RetainPtr core/fxcrt/retain_ptr.h:25:7
    #11 0x5646921e3dac in CXFA_FFWidget::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffwidget.cpp:444:1
    #12 0x5646921afd33 in CXFA_FFField::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fffield.cpp:546:23
    #13 0x5646921a08cd in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:304:28
    #14 0x56469219d2ef in CXFA_FFDocView::SetFocusNode(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:335:8
    #15 0x56468f956c9c in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:447:12
    #16 0x56468f9517f4 in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #17 0x56468f96db95 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:178:10
    #18 0x56468f8bb4a4 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:490:31
    #19 0x56468f8b4cad in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:103:7
    #20 0x56468fb0c330 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #21 0x56468fb0971e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #22 0x56468fb072f9 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #23 0x564691f6a737 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x429e737)
    #24 0x564691efd7f4 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x42317f4)
    #25 0x564691ef72fe in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422b2fe)
    #26 0x564691efd7f4 in Builtins_InterpreterEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x42317f4)
    #27 0x564691ef72fe in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422b2fe)
    #28 0x564691efb339 in Builtins_JSEntryTrampoline (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422f339)
    #29 0x564691efb117 in Builtins_JSEntry (/home/krace/tools/src/pdfium/out/Debug/pdfium_test+0x422f117)
    #30 0x56468fe128d1 in Call v8/src/execution/simulator.h:142:12
    #31 0x56468fe128d1 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:367:33
    #32 0x56468fe114cf in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:461:10
    #33 0x56468f9df07d in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:4873:7
    #34 0x56468f8b73c3 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:286:21
    #35 0x56468f8c0458 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:160:23
    #36 0x5646923f06a8 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2750:22
    #37 0x5646923e8c29 in ExecuteScript xfa/fxfa/parser/cxfa_node.cpp:2710:10
    #38 0x5646923e8c29 in ProcessEventInternal xfa/fxfa/parser/cxfa_node.cpp:2414:14
    #39 0x5646923e8c29 in CXFA_Node::ProcessEvent(CXFA_FFDocView*, XFA_AttributeValue, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2391:9
    #40 0x5646921e3cda in CXFA_FFWidget::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffwidget.cpp:442:12

previously allocated by thread T0 here:
    #0 0x56468ee35f6d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x5646921bd69b in MakeUnique<CXFA_FFComboBox, CXFA_Node *&> third_party/base/ptr_util.h:56:29
    #2 0x5646921bd69b in CXFA_FFNotify::OnCreateContentLayoutItem(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:134:19
    #3 0x564692300fd4 in CXFA_ContentLayoutProcessor::CreateContentLayoutItem(CXFA_Node*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:644:27
    #4 0x564692328961 in CXFA_ContentLayoutProcessor::DoLayoutField() xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2026:19
    #5 0x56469230eae7 in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2086:7
    #6 0x564692321083 in CXFA_ContentLayoutProcessor::InsertFlowedItem(CXFA_ContentLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<fxcrt::RetainPtr<CXFA_ContentLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2356:29
    #7 0x56469231c2f8 in CXFA_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1797:23
    #8 0x56469230ee13 in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2068:18
    #9 0x564692321083 in CXFA_ContentLayoutProcessor::InsertFlowedItem(CXFA_ContentLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<fxcrt::RetainPtr<CXFA_ContentLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2356:29
    #10 0x56469231c2f8 in CXFA_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1797:23
    #11 0x56469230ee13 in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2068:18
    #12 0x56469232dce9 in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:80:36
    #13 0x56469219c261 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:97:38
    #14 0x564692480d5c in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:170:18
    #15 0x56468eee30a3 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:209:22
    #16 0x56468ee410a9 in RenderPdf samples/pdfium_test.cc:955:12
    #17 0x56468ee410a9 in main samples/pdfium_test.cc:1203:5
    #18 0x7fcd8cd2e82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/memory:2606:19 in get
Shadow bytes around the buggy address:
  0x0c1c7fff8770: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c1c7fff8780: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa
  0x0c1c7fff8790: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1c7fff87a0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c1c7fff87b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c1c7fff87c0:[fd]fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd
  0x0c1c7fff87d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1c7fff87e0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c1c7fff87f0: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c1c7fff8800: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1c7fff8810: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
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
==76690==ABORTING

Did this work before? N/A 

Chrome version: 81.0.4044.138  Channel: stable
OS Version: ubuntu16
Flash Version:

## Attachments

- [uaf7.pdf](attachments/uaf7.pdf) (application/pdf, 4.7 KB)

## Timeline

### ct...@chromium.org (2020-05-14)

[Sheriff] Setting some security labels: Impact-None due to us not shipping XFA yet, Severity-High for UAF. tsepez@ could you help investigate this report? Thanks!

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2020-05-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/2da665244251bb8e0db77d8a996063b0294f612d

commit 2da665244251bb8e0db77d8a996063b0294f612d
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu May 14 21:58:43 2020

Retain owning layout items earlier in CXFA_FFField

Safer, even on the paths where we know we short-circuit.

Bug: chromium:1082597
Change-Id: Ie4116dba8bfac54c7a4fcb181fecbd3d7ee1389e
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/69910
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/2da665244251bb8e0db77d8a996063b0294f612d/testing/resources/javascript/xfa_specific/bug_1082597_expected.txt
[add] https://pdfium.googlesource.com/pdfium/+/2da665244251bb8e0db77d8a996063b0294f612d/testing/resources/javascript/xfa_specific/bug_1082597.in
[modify] https://pdfium.googlesource.com/pdfium/+/2da665244251bb8e0db77d8a996063b0294f612d/xfa/fxfa/cxfa_fffield.cpp


### ts...@chromium.org (2020-05-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/64b4f3e61b44e2419b3e587e8f67342a8c6f9873

commit 64b4f3e61b44e2419b3e587e8f67342a8c6f9873
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri May 15 00:09:53 2020

Roll src/third_party/pdfium 3e36f6883143..2da665244251 (10 commits)

https://pdfium.googlesource.com/pdfium.git/+log/3e36f6883143..2da665244251

git log 3e36f6883143..2da665244251 --date=short --first-parent --format='%ad %ae %s'
2020-05-14 tsepez@chromium.org Retain owning layout items earlier in CXFA_FFField
2020-05-14 thestig@chromium.org Remove unreachable code in ProgressiveDecoder.
2020-05-14 thestig@chromium.org Remove non-const reference params in ProgressiveDecoder.
2020-05-14 thestig@chromium.org Rename ModuleIface to ProgressiveDecoderIface.
2020-05-14 thestig@chromium.org Add another test case for FPDFImageObj_GetImageMetadata().
2020-05-14 thestig@chromium.org Remove fx_freetype_warnings config.
2020-05-14 thestig@chromium.org Remove JpxModule.
2020-05-14 thestig@chromium.org Remove an unused flag in fx_lcms2_warnings config.
2020-05-14 thestig@chromium.org Limit fx_libopenjpeg_warnings config.
2020-05-14 nigi@chromium.org Fix FPDFAnnotEmbedderTest.AddAndModifyText for Skia.

Created with:
  gclient setdep -r src/third_party/pdfium@2da665244251

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1082597
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I49c33a1fb1f965fc82d6a4ba20037a42218cc76c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2203179
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#769067}

[modify] https://crrev.com/64b4f3e61b44e2419b3e587e8f67342a8c6f9873/DEPS


### [Deleted User] (2020-05-15)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-19)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-21)

Congrats! The Panel decided to award $7,500 for this report! 

### me...@gmail.com (2020-05-21)

thx :)

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-08-21)

This issue was migrated from crbug.com/chromium/1082597?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052303)*
