# pdfium (XFA): wrong object type in CFXJSE_FormCalcContext::ParseResolveResult

| Field | Value |
|-------|-------|
| **Issue ID** | [40093777](https://issues.chromium.org/issues/40093777) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-01-17 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.71 Safari/537.36

Steps to reproduce the problem:
You can reproduce with pdfium_test by setting is_ubsan_security or is_ubsan_vptr.

fxjs/xfa/cjx_node.cpp:460:7: runtime error: member call on address 0x6070000009c0 which does not point to an object of type 'CJX_Node'
0x6070000009c0: note: object is of type 'CJX_Date'
 05 00 80 7b  90 c0 b6 65 ad 55 00 00  c0 07 00 00 10 61 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CJX_Date'

    #0 0x55ad6371a321 in CJX_Node::model(CFXJSE_Value*, bool, XFA_Attribute) fxjs/xfa/cjx_node.cpp:460:7
    #1 0x55ad635e46ca in CFXJSE_FormCalcContext::ParseResolveResult(CFXJSE_Value*, XFA_RESOLVENODE_RS const&, CFXJSE_Value*, std::__1::vector<std::__1::unique_ptr<CFXJSE_Value, std::__1::default_delete<CFXJSE_Value> >, std::__1::allocator<std::__1::unique_ptr<CFXJSE_Value, std::__1::default_delete<CFXJSE_Value> > > >*, bool*) fxjs/xfa/cfxjse_formcalc_context.cpp:5765:7
    #2 0x55ad635e26bb in CFXJSE_FormCalcContext::dot_accessor(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Arguments&) fxjs/xfa/cfxjse_formcalc_context.cpp:5025:9
    #3 0x55ad63595e89 in (anonymous namespace)::V8FunctionCallback_Wrapper(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:47:3
    #4 0x55ad61e39286 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:146:3
    #5 0x55ad61de5c20 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #6 0x55ad61de49ad in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #7 0x55ad61de4675 in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:127:1
    #8 0x55ad62c1818a in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit
    #9 0x55ad62b78276 in Builtins_InterpreterEntryTrampoline
    #10 0x55ad62b78276 in Builtins_InterpreterEntryTrampoline
    #11 0x55ad62b71c7f in Builtins_ArgumentsAdaptorTrampoline
    #12 0x55ad62b78276 in Builtins_InterpreterEntryTrampoline
    #13 0x55ad62b71c7f in Builtins_ArgumentsAdaptorTrampoline
    #14 0x55ad62b75aa2 in Builtins_JSEntryTrampoline
    #15 0x55ad62b7582c in Builtins_JSEntry
    #16 0x55ad6231ea51 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:293:34
    #17 0x55ad6231e623 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:369:10
    #18 0x55ad61b8c07a in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:4998:7
    #19 0x55ad63598736 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:295:21
    #20 0x55ad635a04a9 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:149:23
    #21 0x55ad63a2a2e8 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2636:22
    #22 0x55ad63a23ff7 in CXFA_Node::ExecuteScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2595:26
    #23 0x55ad63833d78 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:400:11
    #24 0x55ad63833c49 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:388:17
    #25 0x55ad638340f3 in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:84:3
    #26 0x55ad63774273 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:130:22
    #27 0x55ad62daa00a in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #28 0x55ad6186263d in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:794:12
    #29 0x55ad6185edc6 in main samples/pdfium_test.cc:1006:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 70.0.3538.71  Channel: stable
OS Version: 
Flash Version:

## Attachments

- [chromium-922864.pdf](attachments/chromium-922864.pdf) (application/pdf, 418 B)
- [chromium-922864-2.pdf](attachments/chromium-922864-2.pdf) (application/pdf, 421 B)

## Timeline

### pd...@gmail.com (2019-01-17)

[Empty comment from Monorail migration]

### pd...@gmail.com (2019-01-17)

Note that the wrong type can be easily changed.

fxjs/xfa/cjx_node.cpp:460:7: runtime error: member call on address 0x6070000009c0 which does not point to an object of type 'CJX_Node'
0x6070000009c0: note: object is of type 'CJX_Boolean'
 08 00 00 5e  b0 39 8d a6 55 55 00 00  c0 07 00 00 10 61 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CJX_Boolean'


### cl...@chromium.org (2019-01-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5646057975054336.

### jd...@chromium.org (2019-01-17)

This is medium priority as potential memory corruption in a sandboxed process.

tsepez@ (and/or thestig@), can you take a look at this and re-delegate as necessary?

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-01-17)

Testcase 5646057975054336 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5646057975054336.

### jd...@chromium.org (2019-01-17)

Medium *severity*, rather...

### jd...@chromium.org (2019-01-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-01-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-01-18)

Repros locally.  Maybe CF was not using the right sanizier.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-23)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7e786cc978b21d8365dc78e3776bef4082279a30

commit 7e786cc978b21d8365dc78e3776bef4082279a30
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Jan 23 21:57:06 2019

Don't trust CJX_Objects handed back from JavaScript.

Implement our own dynamic typing to ensure we are not making
bad casts since we don't have RTTI. There are too many ways
that JS can apply methods/getter to objects that this provides
another line of defense.

Put all the type information constants into the header so that
they can be easily checked against the actual class hierarchy.
The changes to the .cpp files should all be boilerplate, except
for CJX_Object, which has no superclass.

Apply the check inside the jse_define.h macros before making cast.

Bug: chromium:922864
Change-Id: I4d5faf572949a72168b39d43d33eea22659194b1
Reviewed-on: https://pdfium-review.googlesource.com/c/48650
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_signaturepseudomodel.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_value.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_eventpseudomodel.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_desc.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_handler.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_integer.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_picture.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_packet.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_comb.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_extras.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_date.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_extras.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_manifest.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_date.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_boolean.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_field.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_datetime.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_exdata.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_model.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_encrypt.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_delta.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_datetime.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_text.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_wsdlconnection.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_float.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_xfa.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_model.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_textnode.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_textnode.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_boolean.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_logpseudomodel.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_hostpseudomodel.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_tree.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_source.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_form.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_wsdlconnection.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_subform.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_draw.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_treelist.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_datawindow.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_occur.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_time.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_layoutpseudomodel.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_datavalue.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_occur.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_exdata.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_image.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_template.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_object.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_container.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_float.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_handler.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_instancemanager.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_treelist.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_subformset.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_packet.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_exclgroup.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_instancemanager.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_node.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_exclgroup.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_comb.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_subformset.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_encrypt.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_delta.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_node.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_object.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_integer.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_time.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_subform.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_signaturepseudomodel.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_field.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_source.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_logpseudomodel.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_picture.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_draw.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_desc.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_hostpseudomodel.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_form.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_decimal.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_decimal.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_script.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_image.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_datavalue.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_layoutpseudomodel.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_datawindow.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_xfa.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_script.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_value.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_tree.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_text.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_container.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/jse_define.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_eventpseudomodel.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_manifest.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_list.cpp
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_list.h
[modify] https://crrev.com/7e786cc978b21d8365dc78e3776bef4082279a30/fxjs/xfa/cjx_template.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ca1a001a0c3dbf235e727e0e17f246a14f39b486

commit ca1a001a0c3dbf235e727e0e17f246a14f39b486
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jan 24 07:30:19 2019

Roll src/third_party/pdfium 3e873fa0184f..b2bab1fee534 (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/3e873fa0184f..b2bab1fee534


git log 3e873fa0184f..b2bab1fee534 --date=short --no-merges --format='%ad %ae %s'
2019-01-23 thestig@chromium.org Avoid a crash in CFXJSE_Value::ToString().
2019-01-23 tsepez@chromium.org [XFA] Apply dynamic type checks to JSE method invocation.
2019-01-23 tsepez@chromium.org Don't trust CJX_Objects handed back from JavaScript.
2019-01-23 tsepez@chromium.org Add CFXJSE_Value::IsEmpty() and use it in SetArray()
2019-01-23 thestig@chromium.org Fix some nits in CFXJSE_Engine.


Created with:
  gclient setdep -r src/third_party/pdfium@b2bab1fee534

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:922864
TBR=dsinclair@chromium.org

Change-Id: I15cd1a5e13928f49b3993763667358a1164b0a62
Reviewed-on: https://chromium-review.googlesource.com/c/1432872
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#625546}


### ts...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-25)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-31)

Congrats! The Panel decided to reward $3,000 :) 

### na...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

This bug requires manual review: M73 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pd...@gmail.com (2019-02-09)

I think Impact should actually be None. Although pdfiumers(?) should have the final word on that.

### aw...@chromium.org (2019-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/922864?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093777)*
