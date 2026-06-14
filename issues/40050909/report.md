# pdfium (XFA): oob read in HTMLSTR2Code

| Field | Value |
|-------|-------|
| **Issue ID** | [40050909](https://issues.chromium.org/issues/40050909) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-12-06 |
| **Bounty** | $2,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.101 Safari/537.36

Steps to reproduce the problem:
ERROR: AddressSanitizer: global-buffer-overflow on address 0x55c198b33cc8
READ of size 8 at 0x55c198b33cc8 thread T0
SCARINESS: 33 (8-byte-read-global-buffer-overflow-far-from-bounds)

    #0 0x55c1961b532d in (anonymous namespace)::HTMLSTR2Code(fxcrt::WideString const&, unsigned int*) fxjs/xfa/cfxjse_formcalc_context.cpp:848:37
    #1 0x55c1961b4e3f in (anonymous namespace)::DecodeMLInternal(fxcrt::WideString const&, bool) fxjs/xfa/cfxjse_formcalc_context.cpp:947:11
    #2 0x55c1961a0022 in (anonymous namespace)::DecodeHTML(fxcrt::WideString const&) fxjs/xfa/cfxjse_formcalc_context.cpp:968:10
    #3 0x55c19619fb4d in CFXJSE_FormCalcContext::Decode(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Arguments&) fxjs/xfa/cfxjse_formcalc_context.cpp:3602:15
    #4 0x55c196171d2f in (anonymous namespace)::V8FunctionCallback_Wrapper(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:47:3
    #5 0x55c196381acd in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #6 0x55c19637f76e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #7 0x55c19637c269 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #8 0x55c19637b81e in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:129:1
    #9 0x55c19821d9b8 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit
    #10 0x55c1981a559a in Builtins_InterpreterEntryTrampoline
    #11 0x55c1981a559a in Builtins_InterpreterEntryTrampoline
    #12 0x55c19819f0f8 in Builtins_ArgumentsAdaptorTrampoline
    #13 0x55c1981a559a in Builtins_InterpreterEntryTrampoline
    #14 0x55c19819f0f8 in Builtins_ArgumentsAdaptorTrampoline
    #15 0x55c1981a2e99 in Builtins_JSEntryTrampoline
    #16 0x55c1981a2c77 in Builtins_JSEntry
    #17 0x55c196676cd3 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:266:33
    #18 0x55c1966758ca in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:358:10
    #19 0x55c19625de1c in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:4918:7
    #20 0x55c196175f19 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:301:21
    #21 0x55c19617b8d2 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:153:23
    #22 0x55c1985e1603 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2696:22
    #23 0x55c1985e0dc1 in CXFA_Node::ProcessValidate(CXFA_FFDocView*, int) xfa/fxfa/parser/cxfa_node.cpp:2598:28
    #24 0x55c1983f9175 in XFA_ProcessEvent(CXFA_FFDocView*, CXFA_Node*, CXFA_EventParam*) xfa/fxfa/cxfa_ffdocview.cpp:349:23
    #25 0x55c1983f6cbc in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:413:35
    #26 0x55c1983f6c1d in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:400:20
    #27 0x55c1983f70bc in CXFA_FFDocView::InitValidate(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:581:3
    #28 0x55c1983f6f1e in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:89:3
    #29 0x55c1986a7331 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:123:22
    #30 0x55c195ab7056 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:261:32
    #31 0x55c195a0c7ae in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:899:12
    #32 0x55c195a0953d in main samples/pdfium_test.cc:1145:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.101  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1031523.pdf](attachments/chromium-1031523.pdf) (application/pdf, 456 B)

## Timeline

### pd...@gmail.com (2019-12-06)

[Empty comment from Monorail migration]

### pd...@gmail.com (2019-12-06)

Note: Chrome doesn't use XFA.

### cl...@chromium.org (2019-12-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4798180193337344.

### cl...@chromium.org (2019-12-06)

Automatically adding ccs based on OWNERS file / target commit history.

If this is incorrect, please add the ClusterFuzz-Wrong label.

### pd...@gmail.com (2019-12-06)

A subtle bug.

--- a/fxjs/xfa/cfxjse_formcalc_context.cpp
+++ b/fxjs/xfa/cfxjse_formcalc_context.cpp
@@ -844,7 +863,7 @@ bool HTMLSTR2Code(const WideString& pData, uint32_t* iCode) {
   const XFA_FMHtmlReserveCode* result = std::lower_bound(
       std::begin(kReservesForDecode), std::end(kReservesForDecode),
       temp.AsStringView(), cmpFunc);
-  if (result != std::end(kReservesForEncode) &&
+  if (result != std::end(kReservesForDecode) &&
       !strcmp(temp.c_str(), result->m_htmlReserve)) {
     *iCode = result->m_uCode;
     return true;


### ts...@chromium.org (2019-12-06)

Broken in 573b10a88 (and yes, I reviewed it, and didn't spot the typo).

### ts...@chromium.org (2019-12-06)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/63370

### th...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f3883e32a739dfda868e82a65975adbe23f979d7

commit f3883e32a739dfda868e82a65975adbe23f979d7
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Dec 06 19:40:20 2019

Fix typo in array name in HTMLSTR2Code()

Bug: chromium:1031523
Change-Id: I125655245ebd6c7630a03b7ca2468ebfce75498c
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/63370
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/f3883e32a739dfda868e82a65975adbe23f979d7/fxjs/xfa/cfxjse_formcalc_context.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/f3883e32a739dfda868e82a65975adbe23f979d7/fxjs/xfa/cfxjse_formcalc_context_embeddertest.cpp


### ts...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bb0adca4382c0b1737bf032c2ced6c36931b2b0c

commit bb0adca4382c0b1737bf032c2ced6c36931b2b0c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Dec 06 21:16:06 2019

Roll src/third_party/pdfium 02a82546e547..f3883e32a739 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/02a82546e547..f3883e32a739

git log 02a82546e547..f3883e32a739 --date=short --first-parent --format='%ad %ae %s'
2019-12-06 tsepez@chromium.org Fix typo in array name in HTMLSTR2Code()
2019-12-06 thestig@chromium.org Use more spans with CRYPT_ArcFour code.

Created with:
  gclient setdep -r src/third_party/pdfium@f3883e32a739

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1030583,chromium:1031523
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I3b0cd04114424aba91d9f4baacc29eb16831a31f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1955180
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#722613}

[modify] https://crrev.com/bb0adca4382c0b1737bf032c2ced6c36931b2b0c/DEPS


### cl...@chromium.org (2019-12-06)

Detailed Report: https://clusterfuzz.com/testcase?key=4798180193337344

Fuzzing Engine: libFuzzer
Fuzz Target: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Global-buffer-overflow READ 8
Crash Address: 0x7fa88643eb08
Crash State:
  HTMLSTR2Code
  DecodeMLInternal
  DecodeHTML
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=611512:611543

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4798180193337344

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

### th...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-12-07)

ClusterFuzz testcase 4798180193337344 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=722601:722620

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### aw...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-17)

Congrats! The Panel decided to reward $2,500 for this report

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-03-14)

This issue was migrated from crbug.com/chromium/1031523?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050909)*
