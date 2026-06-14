# Security: PDFium Bad cast in ToNode in cxfa_object.cpp

| Field | Value |
|-------|-------|
| **Issue ID** | [40095672](https://issues.chromium.org/issues/40095672) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ba...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-07-11 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The bug present in ToNode() function in xfa/fxfa/parser/cxfa\_object.cpp file.  

To convert XFA\_Object pointer to CXFA\_Node pointer, ToNode() function is used.

CXFA\_Node\* ToNode(CXFA\_Object\* pObj) {  

return pObj ? pObj->AsNode() : nullptr;  

}

ToNode() function returns result of pObj->AsNode method call.

CXFA\_Node\* CXFA\_Object::AsNode() {  

return IsNode() ? static\_cast<CXFA\_Node\*>(this) : nullptr;  

}

AsNode() method check type of CXFA\_Object by calling IsNode() and cast self to CXFA\_Node pointer.

bool IsNode() const {  

return m\_objectType == XFA\_ObjectType::Node ||  

m\_objectType == XFA\_ObjectType::NodeC ||  

m\_objectType == XFA\_ObjectType::NodeV ||  

m\_objectType == XFA\_ObjectType::ModelNode ||  

m\_objectType == XFA\_ObjectType::TextNode ||  

m\_objectType == XFA\_ObjectType::ContainerNode ||  

m\_objectType == XFA\_ObjectType::ContentNode ||  

m\_objectType == XFA\_ObjectType::ThisProxy;  

}

As you can see, only 8 XFA object types is allowed to cast to CXFA\_Node pointer.  

The problem is that XFA\_ObjectType::ThisProxy is also allowed to cast to CXFA\_Node.  

m\_objectType is set to XFA\_ObjectType::ThisProxy once ThisProxy object is created.

CXFA\_ThisProxy::CXFA\_ThisProxy(CXFA\_Node\* pThisNode, CXFA\_Node\* pScriptNode)  

: CXFA\_Object(pThisNode->GetDocument(),  

XFA\_ObjectType::ThisProxy, // will be assigned to m\_objectType  

XFA\_Element::Object,  

pdfium::MakeUnique<CJX\_Object>(this)),  

m\_pThisNode(pThisNode),  

m\_pScriptNode(pScriptNode) {}

```
          +CXFA_Node  
          |  

```

CXFA\_Object<--+  

|  

+CXFA\_ThisProxy

Above is the diagram of inheritance. Both CXFA\_Node and CXFA\_ThisProxy are inherited from CXFA\_Object.  

but these have no relationship(parent/child) thus shouldn't be casted mutually. Therefore, type confusion(bad cast) will be occured once ToNode() function is called with CXFA\_ThisProxy object. PDFium will treat CXFA\_ThisProxy object as CXFA\_Node object.

Attached file is minimized PoC file. I used script node to set 'this' to CXFA\_ThisProxy object. CJX\_List::append method calls CXFA\_AttachNodeList::Append method and In CXFA\_AttachNodeList::Append method, member variables like m\_pPrevSibling which only exist on CXFA\_Node are used on CXFA\_ThisProxy object.

**VERSION**  

Chrome Version: PDFium with XFA enabled. Commit: 45e8cc7cb43a3a14ad3d3372dc2db39c5f8ea43f  

Operating System: All

**REPRODUCTION CASE**

1. Build pdfium\_test with XFA/ASAN enabled.
2. Load the attached poc pdf file
3. Crash occured

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: PDF plugin process  

Crash State: Address Sanitizer output

==63787==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60700008fab0 at pc 0x5651b5b80387 bp 0x7fff3c888410 sp 0x7fff3c888408  

READ of size 8 at 0x60700008fab0 thread T0  

#0 0x5651b5b80386 in RemoveChild core/fxcrt/tree\_node.h:110:54  

#1 0x5651b5b80386 in CXFA\_Node::RemoveChildAndNotify(CXFA\_Node\*, bool) xfa/fxfa/parser/cxfa\_node.cpp:1527  

#2 0x5651b5b0bca5 in CXFA\_AttachNodeList::Append(CXFA\_Node\*) xfa/fxfa/parser/cxfa\_attachnodelist.cpp:27:14  

#3 0x5651b3a6ca0a in CJX\_List::append(CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_list.cpp:49:17  

#4 0x5651b3a6c4fc in CJX\_List::append\_static(CJX\_Object\*, CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_list.h:23:3  

#5 0x5651b3a756fd in CJX\_Object::RunMethod(fxcrt::WideString const&, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_object.cpp:177:10  

#6 0x5651b39e5c13 in CFXJSE\_Engine::NormalMethodCall(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, fxcrt::WideString const&) fxjs/xfa/cfxjse\_engine.cpp:459:31  

#7 0x5651b39e11c4 in (anonymous namespace)::DynPropGetterAdapter\_MethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/xfa/cfxjse\_class.cpp:112:7  

#8 0x5651b3bc3998 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#9 0x5651b3bc17bb in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#10 0x5651b3bbf5d4 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#11 0x5651b5857a78 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x37dda78)  

#12 0x5651b57d7803 in Builtins\_InterpreterEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375d803)  

#13 0x5651b57d51bc in Builtins\_JSEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375b1bc)  

#14 0x5651b57d4f97 in Builtins\_JSEntry (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375af97)  

#15 0x5651b3e3b959 in Call v8/src/execution/simulator.h:138:12  

#16 0x5651b3e3b959 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:267  

#17 0x5651b3e3af35 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:359:10  

#18 0x5651b3aa9cc7 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api/api.cc:2126:7  

#19 0x5651b39e2e98 in CFXJSE\_Context::ExecuteScript(char const\*, CFXJSE\_Value\*, CFXJSE\_Value\*) fxjs/xfa/cfxjse\_context.cpp:272:20  

#20 0x5651b39ee8b3 in CFXJSE\_Engine::RunVariablesScript(CXFA\_Node\*) fxjs/xfa/cfxjse\_engine.cpp:525:29  

#21 0x5651b39e9f03 in CFXJSE\_Engine::GetOrCreateJSBindingFromMap(CXFA\_Object\*) fxjs/xfa/cfxjse\_engine.cpp:749:5  

#22 0x5651b3a8f62a in CJX\_Tree::resolveNode(CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_tree.cpp:61:44  

#23 0x5651b3a8edbc in CJX\_Tree::resolveNode\_static(CJX\_Object\*, CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_tree.h:24:3  

#24 0x5651b3a756fd in CJX\_Object::RunMethod(fxcrt::WideString const&, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_object.cpp:177:10  

#25 0x5651b39e5c13 in CFXJSE\_Engine::NormalMethodCall(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, fxcrt::WideString const&) fxjs/xfa/cfxjse\_engine.cpp:459:31  

#26 0x5651b39e11c4 in (anonymous namespace)::DynPropGetterAdapter\_MethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/xfa/cfxjse\_class.cpp:112:7  

#27 0x5651b3bc3998 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#28 0x5651b3bc17bb in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#29 0x5651b3bbf5d4 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#30 0x5651b5857a78 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x37dda78)  

#31 0x5651b57d7803 in Builtins\_InterpreterEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375d803)  

#32 0x5651b57d117b in Builtins\_ArgumentsAdaptorTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375717b)  

#33 0x5651b57d7803 in Builtins\_InterpreterEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375d803)  

#34 0x5651b57d117b in Builtins\_ArgumentsAdaptorTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375717b)  

#35 0x5651b57d51bc in Builtins\_JSEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375b1bc)  

#36 0x5651b57d4f97 in Builtins\_JSEntry (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375af97)  

#37 0x5651b3e3b959 in Call v8/src/execution/simulator.h:138:12  

#38 0x5651b3e3b959 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:267  

#39 0x5651b3e3af35 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:359:10  

#40 0x5651b3ad13a4 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api/api.cc:4762:7  

#41 0x5651b39e2cdd in CFXJSE\_Context::ExecuteScript(char const\*, CFXJSE\_Value\*, CFXJSE\_Value\*) fxjs/xfa/cfxjse\_context.cpp:300:21  

#42 0x5651b39e9bf1 in CFXJSE\_Engine::RunScript(CXFA\_Script::Type, fxcrt::StringViewTemplate<wchar\_t>, CFXJSE\_Value\*, CXFA\_Object\*) fxjs/xfa/cfxjse\_engine.cpp:153:23  

#43 0x5651b5b8fa0b in CXFA\_Node::ExecuteBoolScript(CXFA\_FFDocView\*, CXFA\_Script\*, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2700:22  

#44 0x5651b5b88d67 in ExecuteScript xfa/fxfa/parser/cxfa\_node.cpp:2660:10  

#45 0x5651b5b88d67 in ProcessEventInternal xfa/fxfa/parser/cxfa\_node.cpp:2360  

#46 0x5651b5b88d67 in CXFA\_Node::ProcessEvent(CXFA\_FFDocView\*, XFA\_AttributeValue, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2337  

#47 0x5651b5c1d15d in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:389:12  

#48 0x5651b5c1cf32 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20  

#49 0x5651b5c1cf32 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20  

#50 0x5651b5c1cf32 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20  

#51 0x5651b5c1d586 in CXFA\_FFDocView::StartLayout() xfa/fxfa/cxfa\_ffdocview.cpp:91:3  

#52 0x5651b5cb53cc in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:125:22  

#53 0x5651b31ad596 in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:270:32  

#54 0x5651b3149b52 in RenderPdf samples/pdfium\_test.cc:833:12  

#55 0x5651b3149b52 in main samples/pdfium\_test.cc:1059  

#56 0x7fc99936482f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

0x60700008fab0 is located 16 bytes to the left of 72-byte region [0x60700008fac0,0x60700008fb08)  

allocated by thread T0 here:  

#0 0x5651b314235d in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:99:3  

#1 0x5651b5be57c7 in MakeUnique<CJX\_Object, CXFA\_ThisProxy \*> third\_party/base/ptr\_util.h:56:29  

#2 0x5651b5be57c7 in CXFA\_ThisProxy::CXFA\_ThisProxy(CXFA\_Node\*, CXFA\_Node\*) xfa/fxfa/parser/cxfa\_thisproxy.cpp:17  

#3 0x5651b39ee02a in CFXJSE\_Engine::CreateVariablesContext(CXFA\_Node\*, CXFA\_Node\*) fxjs/xfa/cfxjse\_engine.cpp:477:34  

#4 0x5651b39ee81a in CFXJSE\_Engine::RunVariablesScript(CXFA\_Node\*) fxjs/xfa/cfxjse\_engine.cpp:522:7  

#5 0x5651b39e9f03 in CFXJSE\_Engine::GetOrCreateJSBindingFromMap(CXFA\_Object\*) fxjs/xfa/cfxjse\_engine.cpp:749:5  

#6 0x5651b3a8f62a in CJX\_Tree::resolveNode(CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_tree.cpp:61:44  

#7 0x5651b3a8edbc in CJX\_Tree::resolveNode\_static(CJX\_Object\*, CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_tree.h:24:3  

#8 0x5651b3a756fd in CJX\_Object::RunMethod(fxcrt::WideString const&, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_object.cpp:177:10  

#9 0x5651b39e5c13 in CFXJSE\_Engine::NormalMethodCall(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, fxcrt::WideString const&) fxjs/xfa/cfxjse\_engine.cpp:459:31  

#10 0x5651b39e11c4 in (anonymous namespace)::DynPropGetterAdapter\_MethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/xfa/cfxjse\_class.cpp:112:7  

#11 0x5651b3bc3998 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#12 0x5651b3bc17bb in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#13 0x5651b3bbf5d4 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#14 0x5651b5857a78 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x37dda78)  

#15 0x5651b57d7803 in Builtins\_InterpreterEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375d803)  

#16 0x5651b57d117b in Builtins\_ArgumentsAdaptorTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375717b)  

#17 0x5651b57d7803 in Builtins\_InterpreterEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375d803)  

#18 0x5651b57d117b in Builtins\_ArgumentsAdaptorTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375717b)  

#19 0x5651b57d51bc in Builtins\_JSEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375b1bc)  

#20 0x5651b57d4f97 in Builtins\_JSEntry (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x375af97)  

#21 0x5651b3e3b959 in Call v8/src/execution/simulator.h:138:12  

#22 0x5651b3e3b959 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:267  

#23 0x5651b3e3af35 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:359:10  

#24 0x5651b3ad13a4 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api/api.cc:4762:7  

#25 0x5651b39e2cdd in CFXJSE\_Context::ExecuteScript(char const\*, CFXJSE\_Value\*, CFXJSE\_Value\*) fxjs/xfa/cfxjse\_context.cpp:300:21  

#26 0x5651b39e9bf1 in CFXJSE\_Engine::RunScript(CXFA\_Script::Type, fxcrt::StringViewTemplate<wchar\_t>, CFXJSE\_Value\*, CXFA\_Object\*) fxjs/xfa/cfxjse\_engine.cpp:153:23  

#27 0x5651b5b8fa0b in CXFA\_Node::ExecuteBoolScript(CXFA\_FFDocView\*, CXFA\_Script\*, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2700:22  

#28 0x5651b5b88d67 in ExecuteScript xfa/fxfa/parser/cxfa\_node.cpp:2660:10  

#29 0x5651b5b88d67 in ProcessEventInternal xfa/fxfa/parser/cxfa\_node.cpp:2360  

#30 0x5651b5b88d67 in CXFA\_Node::ProcessEvent(CXFA\_FFDocView\*, XFA\_AttributeValue, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2337  

#31 0x5651b5c1d15d in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:389:12  

#32 0x5651b5c1cf32 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20  

#33 0x5651b5c1cf32 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20

SUMMARY: AddressSanitizer: heap-buffer-overflow core/fxcrt/tree\_node.h:110:54 in RemoveChild  

Shadow bytes around the buggy address:  

0x0c0e80009f00: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 fa fa  

0x0c0e80009f10: fa fa 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

0x0c0e80009f20: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fd fd  

0x0c0e80009f30: fd fd fd fd fd fd fd fa fa fa fa fa 00 00 00 00  

0x0c0e80009f40: 00 00 00 00 00 fa fa fa fa fa 00 00 00 00 00 00  

=>0x0c0e80009f50: 00 00 00 fa fa fa[fa]fa 00 00 00 00 00 00 00 00  

0x0c0e80009f60: 00 fa fa fa fa fa 00 00 00 00 00 00 00 00 00 fa  

0x0c0e80009f70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e80009f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e80009f90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e80009fa0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==63787==ABORTING

**CREDIT INFORMATION**  

Reporter credit: banananapenguin

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ts...@chromium.org (2019-07-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-07-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-07-11)

Nice find, and thanks for the detailed explanation.

### ts...@chromium.org (2019-07-11)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/57650

### th...@chromium.org (2019-07-11)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-11)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/1eed2010fbb303fadbb183b29afae2cc608aebab

commit 1eed2010fbb303fadbb183b29afae2cc608aebab
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Jul 11 18:30:18 2019

CXFA_ThisProxy is not a CXFA_Node.

Fix type-checking method IsNode() to reflect this fact.

Bug: chromium:983137
Change-Id: I40495cfdcf5a4a357bd5fa02185747b99a872412
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/57650
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/1eed2010fbb303fadbb183b29afae2cc608aebab/testing/resources/pixel/xfa_specific/bug_983137_expected.pdf.0.png
[add] https://pdfium.googlesource.com/pdfium/+/1eed2010fbb303fadbb183b29afae2cc608aebab/testing/resources/pixel/xfa_specific/bug_983137.in
[modify] https://pdfium.googlesource.com/pdfium/+/1eed2010fbb303fadbb183b29afae2cc608aebab/xfa/fxfa/parser/cxfa_object.h


### ts...@chromium.org (2019-07-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/22c8bab51805748354c4f773fe0818aa0c6a5dd4

commit 22c8bab51805748354c4f773fe0818aa0c6a5dd4
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jul 11 23:13:44 2019

Roll src/third_party/pdfium 9231ac5e1c68..3ec47b651aaa (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/9231ac5e1c68..3ec47b651aaa


git log 9231ac5e1c68..3ec47b651aaa --date=short --no-merges --format='%ad %ae %s'
2019-07-11 thestig@chromium.org Roll build/ f52a9d0c5..95a2cff8f (7 commits)
2019-07-11 thestig@chromium.org Roll v8/ c4c480a41..b6dda94d7 (606 commits)
2019-07-11 thestig@chromium.org Remove CPWL_Edit::ReplaceSel().
2019-07-11 tsepez@chromium.org CXFA_ThisProxy is not a CXFA_Node.


Created with:
  gclient setdep -r src/third_party/pdfium@3ec47b651aaa

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:983137
TBR=pdfium-deps-rolls@chromium.org

Change-Id: I660a3e8e78ac9070c73dccf9b8bed994bc8a18a0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1696917
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#676642}

[modify] https://crrev.com/22c8bab51805748354c4f773fe0818aa0c6a5dd4/DEPS


### sh...@chromium.org (2019-07-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $5,000 for this high quality report!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-10-18)

This issue was migrated from crbug.com/chromium/983137?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095672)*
