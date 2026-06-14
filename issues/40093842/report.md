# pdfium (XFA): double-free in CJX_Node::saveXML

| Field | Value |
|-------|-------|
| **Issue ID** | [40093842](https://issues.chromium.org/issues/40093842) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-01-24 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.71 Safari/537.36

Steps to reproduce the problem:
==1204==ERROR: AddressSanitizer: attempting double-free on 0x631000168800 in thread T0:
SCARINESS: 42 (double-free)

    #1 0x5580e9828012 in CFX_MemoryStream::WriteBlockAtOffset(void const*, long, unsigned long) core/fxcrt/cfx_memorystream.cpp
    #2 0x5580eba9f21d in (anonymous namespace)::RegenerateFormFile_Container(CXFA_Node*, fxcrt::RetainPtr<IFX_SeekableStream> const&, bool) xfa/fxfa/parser/xfa_utils.cpp:355:14
    #3 0x5580eba9dfe7 in XFA_DataExporter_RegenerateFormFile(CXFA_Node*, fxcrt::RetainPtr<IFX_SeekableStream> const&, bool) xfa/fxfa/parser/xfa_utils.cpp:508:5
    #4 0x5580eb653ba5 in CJX_Node::saveXML(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_node.cpp:410:5
    #5 0x5580eb67ae39 in CJS_Result JSEMethod<CJX_Node, &(CJX_Node::saveXML(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(CJX_Node*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/jse_define.h:22:10
    #6 0x5580eb64d3f4 in CJX_Node::saveXML_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_node.h:29:3
    #7 0x5580eb658df8 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:178:10
    #8 0x5580eb4d63e9 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:449:31
    #9 0x5580eb5c1ec7 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #10 0x5580e9d74286 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:146:3
    #11 0x5580e9d20c20 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #12 0x5580e9d1f9ad in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #13 0x5580e9d1f675 in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:127:1
    #14 0x5580eab5318a in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit
    #15 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #16 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #17 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #18 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #19 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #20 0x5580eaaacc7f in Builtins_ArgumentsAdaptorTrampoline
    #21 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #22 0x5580eaaacc7f in Builtins_ArgumentsAdaptorTrampoline
    #23 0x5580eaab0aa2 in Builtins_JSEntryTrampoline
    #24 0x5580eaab082c in Builtins_JSEntry
    #25 0x5580ea259a51 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:293:34
    #26 0x5580ea259623 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:369:10
    #27 0x5580e9ac707a in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:4998:7
    #28 0x5580eb4d36a6 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:295:21
    #29 0x5580eb4db419 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:149:23
    #30 0x5580eb964fa2 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2636:22
    #31 0x5580eb95ecb7 in CXFA_Node::ExecuteScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2595:26
    #32 0x5580eb76ecbd in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:400:11
    #33 0x5580eb76eb99 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:388:17
    #34 0x5580eb76f033 in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:84:3
    #35 0x5580eb6af3a3 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:130:22
    #36 0x5580eace500a in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #37 0x5580e979d63d in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:794:12
    #38 0x5580e9799dc6 in main samples/pdfium_test.cc:1006:5

0x631000168800 is located 0 bytes inside of 65536-byte region [0x631000168800,0x631000178800)
freed by thread T0 here:

    #1 0x5580e9a321ba in pdfium::base::PartitionReallocGenericFlags(pdfium::base::PartitionRootGeneric*, int, void*, unsigned long, char const*) third_party/base/allocator/partition_allocator/partition_alloc.cc:268:18
    #2 0x5580e986295e in FX_SafeRealloc(void*, unsigned long, unsigned long) core/fxcrt/fx_memory.h:59:10
    #3 0x5580e9824ce0 in FX_ReallocOrDie(void*, unsigned long, unsigned long) core/fxcrt/fx_memory.h:84:18
    #4 0x5580e9827f10 in CFX_MemoryStream::WriteBlockAtOffset(void const*, long, unsigned long) core/fxcrt/cfx_memorystream.cpp:92:20
    #5 0x5580eba9f21d in (anonymous namespace)::RegenerateFormFile_Container(CXFA_Node*, fxcrt::RetainPtr<IFX_SeekableStream> const&, bool) xfa/fxfa/parser/xfa_utils.cpp:355:14
    #6 0x5580eba9dfe7 in XFA_DataExporter_RegenerateFormFile(CXFA_Node*, fxcrt::RetainPtr<IFX_SeekableStream> const&, bool) xfa/fxfa/parser/xfa_utils.cpp:508:5
    #7 0x5580eb653ba5 in CJX_Node::saveXML(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_node.cpp:410:5
    #8 0x5580eb67ae39 in CJS_Result JSEMethod<CJX_Node, &(CJX_Node::saveXML(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(CJX_Node*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/jse_define.h:22:10
    #9 0x5580eb64d3f4 in CJX_Node::saveXML_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_node.h:29:3
    #10 0x5580eb658df8 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:178:10
    #11 0x5580eb4d63e9 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:449:31
    #12 0x5580eb5c1ec7 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #13 0x5580e9d74286 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:146:3
    #14 0x5580e9d20c20 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #15 0x5580e9d1f9ad in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #16 0x5580e9d1f675 in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:127:1
    #17 0x5580eab5318a in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit
    #18 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #19 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #20 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #21 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #22 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #23 0x5580eaaacc7f in Builtins_ArgumentsAdaptorTrampoline
    #24 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #25 0x5580eaaacc7f in Builtins_ArgumentsAdaptorTrampoline
    #26 0x5580eaab0aa2 in Builtins_JSEntryTrampoline
    #27 0x5580eaab082c in Builtins_JSEntry
    #28 0x5580ea259a51 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:293:34
    #29 0x5580ea259623 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:369:10

previously allocated by thread T0 here:

    #1 0x5580e983870b in PartitionAllocGenericFlags third_party/base/allocator/partition_allocator/partition_alloc.h:355:30
    #2 0x5580e983870b in FX_SafeAlloc(unsigned long, unsigned long) core/fxcrt/fx_memory.h:48
    #3 0x5580e9824dc0 in FX_AllocOrDie(unsigned long, unsigned long) core/fxcrt/fx_memory.h:67:18
    #4 0x5580e9828006 in CFX_MemoryStream::WriteBlockAtOffset(void const*, long, unsigned long) core/fxcrt/cfx_memorystream.cpp:94:20
    #5 0x5580eb653a3d in CJX_Node::saveXML(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_node.cpp:407:18
    #6 0x5580eb67ae39 in CJS_Result JSEMethod<CJX_Node, &(CJX_Node::saveXML(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(CJX_Node*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/jse_define.h:22:10
    #7 0x5580eb64d3f4 in CJX_Node::saveXML_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_node.h:29:3
    #8 0x5580eb658df8 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:178:10
    #9 0x5580eb4d63e9 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:449:31
    #10 0x5580eb5c1ec7 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #11 0x5580e9d74286 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:146:3
    #12 0x5580e9d20c20 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #13 0x5580e9d1f9ad in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #14 0x5580e9d1f675 in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:127:1
    #15 0x5580eab5318a in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit
    #16 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #17 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #18 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #19 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #20 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #21 0x5580eaaacc7f in Builtins_ArgumentsAdaptorTrampoline
    #22 0x5580eaab3276 in Builtins_InterpreterEntryTrampoline
    #23 0x5580eaaacc7f in Builtins_ArgumentsAdaptorTrampoline
    #24 0x5580eaab0aa2 in Builtins_JSEntryTrampoline
    #25 0x5580eaab082c in Builtins_JSEntry
    #26 0x5580ea259a51 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:293:34
    #27 0x5580ea259623 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:369:10
    #28 0x5580e9ac707a in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:4998:7
    #29 0x5580eb4d36a6 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:295:21
    #30 0x5580eb4db419 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:149:23

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 70.0.3538.71  Channel: stable
OS Version: 
Flash Version:

## Attachments

- [chromium-924928.pdf](attachments/chromium-924928.pdf) (application/pdf, 1.2 KB)

## Timeline

### pd...@gmail.com (2019-01-24)

Note that the fill-bytes are required.

### li...@chromium.org (2019-01-24)

[Comment Deleted]

### ts...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-01-24)

Repro's on ToT with pdfium_test, asan, and XFA.

### ts...@chromium.org (2019-01-24)

offending line is:
   m_data.reset(FX_Realloc(uint8_t, m_data.get(), m_nTotalSize));

should be:
  m_data.release() instead of get() for use with realloc.

### ts...@chromium.org (2019-01-24)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/48830

### ts...@chromium.org (2019-01-24)

Code is compiled into non-xfa builds, there may be a path to trigger it there.  Setting impact stable until we can determine if it can't be hit in non-xfa.

### ts...@chromium.org (2019-01-24)

Broken at https://pdfium-review.googlesource.com/c/pdfium/+/40050/

### pd...@gmail.com (2019-01-24)

When I saw your CL and noticed that it affects non-XFA as well, I searched cs.chromium.org for other ways to trigger. One way is CFX_XMLElement::Save, which does appear to be only used in unit tests. Another is in a few places in core/fpdfapi/edit/cpdf_creator.cpp, which I'm not sure Chromium uses.

### pd...@gmail.com (2019-01-24)

By trigger I merely mean that the function is used, not necessarily that the bug triggers.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-24)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/c30b0a434de9d5e9f2512871cb1395d7c41aaf4f

commit c30b0a434de9d5e9f2512871cb1395d7c41aaf4f
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Jan 24 19:32:30 2019

Release before reallocation in cfx_memorystream.cpp

Bug: chromium:924928
Change-Id: Iad053694d4139414775527dc94fb003b040f51de
Reviewed-on: https://pdfium-review.googlesource.com/c/48830
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/c30b0a434de9d5e9f2512871cb1395d7c41aaf4f/core/fxcrt/cfx_memorystream.cpp


### th...@chromium.org (2019-01-24)

Chromium does use cpdf_creator.cpp code via FPDF_SaveAsCopy(), but cpdf_creator.cpp only uses CPDFSDK_FileWriteAdapter in non-XFA code. The CFX_MemoryStream use is XFA-only.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/29bf1f8c7a9f3d69a62eacb272027ff76b742256

commit 29bf1f8c7a9f3d69a62eacb272027ff76b742256
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jan 24 21:19:36 2019

Roll src/third_party/pdfium 13a5f9e46a5d..c30b0a434de9 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/13a5f9e46a5d..c30b0a434de9


git log 13a5f9e46a5d..c30b0a434de9 --date=short --no-merges --format='%ad %ae %s'
2019-01-24 tsepez@chromium.org Release before reallocation in cfx_memorystream.cpp


Created with:
  gclient setdep -r src/third_party/pdfium@c30b0a434de9

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:924928
TBR=dsinclair@chromium.org

Change-Id: I7e08bb3fe79200b3d1e12bf0680beffaf25b52cc
Reviewed-on: https://chromium-review.googlesource.com/c/1435354
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#625808}


### ts...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-01-24)

XFA Only => Impact none.

### sh...@chromium.org (2019-01-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-31)

Congrats! The Panel decided to reward $3,000 for this report :) 

### na...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-05-03)

This issue was migrated from crbug.com/chromium/924928?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093842)*
