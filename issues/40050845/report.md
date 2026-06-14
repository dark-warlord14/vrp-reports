# pdfium (XFA): oob read in EncodeXML

| Field | Value |
|-------|-------|
| **Issue ID** | [40050845](https://issues.chromium.org/issues/40050845) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-11-30 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.101 Safari/537.36

Steps to reproduce the problem:
(UBSAN)

fxjs/xfa/cfxjse_formcalc_context.cpp:1169:25: runtime error: index 227 out of bounds for type 'const wchar_t [17]'
    #0 0x55bc8d3ef429 in (anonymous namespace)::EncodeXML(fxcrt::ByteString const&) fxjs/xfa/cfxjse_formcalc_context.cpp:1169:25

(ASAN)

AddressSanitizer: global-buffer-overflow on address 0x55af3737430c
READ of size 4 at 0x55af3737430c thread T0
SCARINESS: 17 (4-byte-read-global-buffer-overflow)

    #0 0x55af388f696e in (anonymous namespace)::EncodeXML(fxcrt::ByteString const&) fxjs/xfa/cfxjse_formcalc_context.cpp:1169:25
    #1 0x55af388f4c3a in CFXJSE_FormCalcContext::Encode(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Arguments&) fxjs/xfa/cfxjse_formcalc_context.cpp:3653:15
    #2 0x55af388c648f in (anonymous namespace)::V8FunctionCallback_Wrapper(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:47:3
    #3 0x55af38ad627d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #4 0x55af38ad3f1e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #5 0x55af38ad0a19 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #6 0x55af38acffce in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:129:1
    #7 0x55af3a972158 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit
    #8 0x55af3a8f9d3a in Builtins_InterpreterEntryTrampoline
    #9 0x55af3a8f9d3a in Builtins_InterpreterEntryTrampoline
    #10 0x55af3a8f3898 in Builtins_ArgumentsAdaptorTrampoline
    #11 0x55af3a8f9d3a in Builtins_InterpreterEntryTrampoline
    #12 0x55af3a8f3898 in Builtins_ArgumentsAdaptorTrampoline
    #13 0x55af3a8f7639 in Builtins_JSEntryTrampoline
    #14 0x55af3a8f7417 in Builtins_JSEntry
    #15 0x55af38dcb483 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:266:33
    #16 0x55af38dca07a in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:358:10
    #17 0x55af389b25cc in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:4918:7
    #18 0x55af388ca679 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:301:21
    #19 0x55af388d0032 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:153:23
    #20 0x55af38915ba3 in (anonymous namespace)::DoPredicateFilter(fxcrt::WideString, unsigned long, CFXJSE_ResolveNodeData*) fxjs/xfa/cfxjse_resolveprocessor.cpp:48:22
    #21 0x55af389116ac in CFXJSE_ResolveProcessor::FilterCondition(fxcrt::WideString, CFXJSE_ResolveNodeData*) fxjs/xfa/cfxjse_resolveprocessor.cpp:696:9
    #22 0x55af38912408 in CFXJSE_ResolveProcessor::ResolveNormal(CFXJSE_ResolveNodeData&) fxjs/xfa/cfxjse_resolveprocessor.cpp
    #23 0x55af3890f3f6 in CFXJSE_ResolveProcessor::Resolve(CFXJSE_ResolveNodeData&) fxjs/xfa/cfxjse_resolveprocessor.cpp:115:8
    #24 0x55af388d132d in CFXJSE_Engine::ResolveObjects(CXFA_Object*, fxcrt::StringViewTemplate<wchar_t>, XFA_RESOLVENODE_RS*, unsigned int, CXFA_Node*) fxjs/xfa/cfxjse_engine.cpp:685:32
    #25 0x55af3ace7f8a in CXFA_Document::DoProtoMerge() xfa/fxfa/parser/cxfa_document.cpp:1543:29
    #26 0x55af3ab4b628 in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:74:24
    #27 0x55af3adfbe11 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:123:22
    #28 0x55af3820a6d6 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:261:32
    #29 0x55af381618ae in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:899:12
    #30 0x55af3815e63d in main samples/pdfium_test.cc:1145:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.101  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1029565.pdf](attachments/chromium-1029565.pdf) (application/pdf, 450 B)

## Timeline

### pd...@gmail.com (2019-11-30)

WideString::FromUTF8 returns 0x000e31fd whereas the function apparently only expects <= 0xFFFF. The same bug is also in EncodeHTML.

### pd...@gmail.com (2019-11-30)

Note: Chrome doesn't use XFA.

### pa...@chromium.org (2019-12-02)

Thank you!

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2019-12-02)

Not windows, where wchar_t is uint16_t ... but the rest, yes.

### ts...@chromium.org (2019-12-03)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/63010

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-03)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/8a8437b89797565e9147435b86e1e886b4b34110

commit 8a8437b89797565e9147435b86e1e886b4b34110
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Dec 03 22:28:58 2019

Handle codepoints outside BMP in CFXJSE_FormCalcContext::Encode().

On non-windows platforms, wchar_t is wide enough to represent chars
outside of the Basic Multilingual Plane (chars less than than 65535),
and hence so is WideString. In any case, widen |ch| to 32 bit unsigned
as we step through the loops for consistency, and only output BMP
characters.

- Tidy some local array initializations that are overwritten.

Bug: chromium:1029565
Change-Id: I13b1e65f2d050fd44573bee351fb7e268aa3f40d
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/63010
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/8a8437b89797565e9147435b86e1e886b4b34110/fxjs/xfa/cfxjse_formcalc_context.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/8a8437b89797565e9147435b86e1e886b4b34110/fxjs/xfa/cfxjse_formcalc_context_embeddertest.cpp


### ts...@chromium.org (2019-12-03)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d65f899590b5f400a651436c3ad11a2703e5b1ea

commit d65f899590b5f400a651436c3ad11a2703e5b1ea
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Dec 04 01:00:59 2019

Roll src/third_party/pdfium 8a0f76d3749e..3d7ad5ed37c1 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/8a0f76d3749e..3d7ad5ed37c1

git log 8a0f76d3749e..3d7ad5ed37c1 --date=short --first-parent --format='%ad %ae %s'
2019-12-03 thestig@chromium.org Roll third_party/freetype/src/ 3aaae716b..551bd3a90 (10 commits)
2019-12-03 tsepez@chromium.org Handle codepoints outside BMP in CFXJSE_FormCalcContext::Encode().

Created with:
  gclient setdep -r src/third_party/pdfium@3d7ad5ed37c1

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1029565
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I153d55e7f0fbe843537e21f2e824f6eeb37343ba
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1949584
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#721275}

[modify] https://crrev.com/d65f899590b5f400a651436c3ad11a2703e5b1ea/DEPS


### sh...@chromium.org (2019-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-17)

Congrats! The Panel decided to reward $2,000 for this report

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-03-11)

This issue was migrated from crbug.com/chromium/1029565?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050845)*
