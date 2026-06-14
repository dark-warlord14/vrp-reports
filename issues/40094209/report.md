# pdfium (XFA): oob read in CFGAS_FormatString::FormatStrNum

| Field | Value |
|-------|-------|
| **Issue ID** | [40094209](https://issues.chromium.org/issues/40094209) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-03-06 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36

Steps to reproduce the problem:
==27206==WARNING: MemorySanitizer: use-of-uninitialized-value

    #0 0x55e31c992104 in CFGAS_FormatString::FormatStrNum(fxcrt::StringViewTemplate<wchar_t>, fxcrt::WideString const&, fxcrt::WideString*) const xfa/fgas/crt/cfgas_formatstring.cpp:2096:7
    #1 0x55e31c992aed in CFGAS_FormatString::FormatNum(fxcrt::WideString const&, fxcrt::WideString const&, fxcrt::WideString*) const xfa/fgas/crt/cfgas_formatstring.cpp:2217:10
    #2 0x55e31c0064c3 in CXFA_LocaleValue::FormatSinglePattern(fxcrt::WideString&, fxcrt::WideString const&, LocaleIface*, XFA_VALUEPICTURE) const xfa/fxfa/parser/cxfa_localevalue.cpp:301:23
    #3 0x55e31c005d1a in CXFA_LocaleValue::FormatPatterns(fxcrt::WideString&, fxcrt::WideString const&, LocaleIface*, XFA_VALUEPICTURE) const xfa/fxfa/parser/cxfa_localevalue.cpp:271:9
    #4 0x55e31bc22e47 in CFXJSE_FormCalcContext::Format(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Arguments&) fxjs/xfa/cfxjse_formcalc_context.cpp:3740:20
    #5 0x55e31bbd7f78 in (anonymous namespace)::V8FunctionCallback_Wrapper(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:47:3
    #6 0x55e31870e239 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:146:3
    #7 0x55e318558411 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #8 0x55e31855059b in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #9 0x55e31854f23c in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:127:1
    #10 0x55e31ab89ba2 in v8::internal::Simulator::DoRuntimeCall(v8::internal::Instruction*) v8/src/arm64/simulator-arm64.cc:537:11
    #11 0x55e31ab89153 in v8::internal::Simulator::ExecuteInstruction() v8/src/arm64/simulator-arm64.h:781:5
    #12 0x55e31ab88fd1 in v8::internal::Simulator::Run() v8/src/arm64/simulator-arm64.cc:388:5
    #13 0x55e31ab86ab9 in v8::internal::Simulator::CallImpl(unsigned long, v8::internal::Simulator::CallArgument*) v8/src/arm64/simulator-arm64.cc:155:3
    #14 0x55e3196682e3 in unsigned long v8::internal::Simulator::Call<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/arm64/simulator-arm64.h:727:5
    #15 0x55e319667bfc in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/simulator.h:118:51
    #16 0x55e3195e5f3e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:265:33
    #17 0x55e3195e40fb in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:357:10
    #18 0x55e317cd233e in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:5017:7
    #19 0x55e31bbdbe89 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:295:21
    #20 0x55e31bbe3cfa in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:149:23
    #21 0x55e31c03461c in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2605:22
    #22 0x55e31c033358 in CXFA_Node::ProcessValidate(CXFA_FFDocView*, int) xfa/fxfa/parser/cxfa_node.cpp:2501:28
    #23 0x55e31be9b68b in XFA_ProcessEvent(CXFA_FFDocView*, CXFA_Node*, CXFA_EventParam*) xfa/fxfa/cxfa_ffdocview.cpp:345:23
    #24 0x55e31be95ed7 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:406:11
    #25 0x55e31be95bb2 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:394:17
    #26 0x55e31be9686f in CXFA_FFDocView::InitValidate(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:570:3
    #27 0x55e31be96412 in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:87:3
    #28 0x55e31bde1295 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:129:22
    #29 0x55e31b377a71 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #30 0x55e317a01fc8 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:798:12
    #31 0x55e3179fcbe6 in main samples/pdfium_test.cc:1013:5

  Uninitialized value was created by a heap allocation

    #1 0x55e317a8f91e in PartitionAllocGenericFlags third_party/base/allocator/partition_allocator/partition_alloc.h:363:48
    #2 0x55e317a8f91e in Alloc third_party/base/allocator/partition_allocator/partition_alloc.h:384
    #3 0x55e317a8f91e in fxcrt::StringDataTemplate<wchar_t>::Create(unsigned long) core/fxcrt/string_data_template.h:39
    #4 0x55e317a97225 in fxcrt::WideString::Concat(wchar_t const*, unsigned long) core/fxcrt/widestring.cpp:628:7
    #5 0x55e317a978c8 in fxcrt::WideString::operator+=(fxcrt::WideString const&) core/fxcrt/widestring.cpp:434:5
    #6 0x55e31c97beb8 in CFGAS_FormatString::GetNumericFormat(fxcrt::WideString const&, int*, unsigned int*, fxcrt::WideString*) const xfa/fgas/crt/cfgas_formatstring.cpp:1042:27
    #7 0x55e31c98de7e in CFGAS_FormatString::FormatStrNum(fxcrt::StringViewTemplate<wchar_t>, fxcrt::WideString const&, fxcrt::WideString*) const xfa/fgas/crt/cfgas_formatstring.cpp:1866:7
    #8 0x55e31c992aed in CFGAS_FormatString::FormatNum(fxcrt::WideString const&, fxcrt::WideString const&, fxcrt::WideString*) const xfa/fgas/crt/cfgas_formatstring.cpp:2217:10
    #9 0x55e31c0064c3 in CXFA_LocaleValue::FormatSinglePattern(fxcrt::WideString&, fxcrt::WideString const&, LocaleIface*, XFA_VALUEPICTURE) const xfa/fxfa/parser/cxfa_localevalue.cpp:301:23
    #10 0x55e31c005d1a in CXFA_LocaleValue::FormatPatterns(fxcrt::WideString&, fxcrt::WideString const&, LocaleIface*, XFA_VALUEPICTURE) const xfa/fxfa/parser/cxfa_localevalue.cpp:271:9
    #11 0x55e31bc22e47 in CFXJSE_FormCalcContext::Format(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Arguments&) fxjs/xfa/cfxjse_formcalc_context.cpp:3740:20

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 70.0.3538.124  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-938724.pdf](attachments/chromium-938724.pdf) (application/pdf, 499 B)

## Timeline

### pd...@gmail.com (2019-03-06)

This is a 4-byte (wchar_t) READ, but for some reason ASAN doesn't report this. Nor does UBSAN.

You can verify manually that strf (set in line 1871) has length 76 (plus null) and dot_index_f is 77, so it reads just past it.



### cl...@chromium.org (2019-03-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5931221533196288.

### cl...@chromium.org (2019-03-06)

Detailed report: <https://clusterfuzz.com/testcase?key=5931221533196288>

Fuzzer: libFuzzer\_pdfium\_xfa\_fuzzer  

Fuzz target binary: pdfium\_xfa\_fuzzer  

Job Type: libfuzzer\_chrome\_msan  

Platform Id: linux

Crash Type: Use-of-uninitialized-value  

Crash Address:  

Crash State:  

CFGAS\_FormatString::FormatStrNum  

CFGAS\_FormatString::FormatNum  

CXFA\_LocaleValue::FormatSinglePattern

Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=5931221533196288>

See <https://www.chromium.org/developers/testing/memorysanitizer#TOC-Reproducing-ClusterFuzz-Bugs> for instructions to reproduce this bug locally.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### oc...@chromium.org (2019-03-06)

Tom, could you please take a look at this one too?

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2019-03-07)

Another way to repro is to pull the patch at https://pdfium-review.googlesource.com/c/pdfium/+/51610 which converts this bad indexing into a hard CHECK() in CFGAS_FormatString::ParseNum() earlier on.

### ts...@chromium.org (2019-03-07)

Oh, as to why ASAN doesn't catch it, its because we round-up slightly the capacity of a widestring buffer so that we can append to it without always incurring a reallocation ...

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-11)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f234dde95a5472cfc34f858bee3ef7d81c23f279

commit f234dde95a5472cfc34f858bee3ef7d81c23f279
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Mar 11 21:43:21 2019

Make CFGAS_FormatString::GetNumericFormat() handle multiple dots.

The existing code only happens to work on single-dot input because
dot_index_f is set to -1 by its caller, so that the += operation
computes the same thing the first time around as the new code does
in all cases.

Bug: chromium:938724
Change-Id: I7057e92f94b92e079bf295c6c95c2c4681fc41ad
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/51630
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/f234dde95a5472cfc34f858bee3ef7d81c23f279/xfa/fgas/crt/cfgas_formatstring.cpp
[modify] https://crrev.com/f234dde95a5472cfc34f858bee3ef7d81c23f279/xfa/fgas/crt/cfgas_formatstring_unittest.cpp


### ts...@chromium.org (2019-03-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d64e2dc8eb9f921bced221b4fa8e518d37c81205

commit d64e2dc8eb9f921bced221b4fa8e518d37c81205
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Mar 12 02:37:56 2019

Roll src/third_party/pdfium c6f50282a2af..c924d0027a7d (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c6f50282a2af..c924d0027a7d


git log c6f50282a2af..c924d0027a7d --date=short --no-merges --format='%ad %ae %s'
2019-03-11 tsepez@chromium.org Use spans in CFGAS_FormatString, part 3
2019-03-11 tsepez@chromium.org Use spans in CFGAS_FormatString, part 2
2019-03-11 rycsmith@google.com Update parameter name in declaration to match definition.
2019-03-11 tsepez@chromium.org Make CFGAS_FormatString::GetNumericFormat() handle multiple dots.


Created with:
  gclient setdep -r src/third_party/pdfium@c924d0027a7d

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:938724
TBR=dsinclair@chromium.org

Change-Id: If1cd1dc1a4be27ce1e6d651fef68126f6a806ec4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1516359
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#639779}
[modify] https://crrev.com/d64e2dc8eb9f921bced221b4fa8e518d37c81205/DEPS


### sh...@chromium.org (2019-03-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-20)

Congrats the Panel decided to reward $1,000 for this report! 

### aw...@google.com (2019-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-06-18)

This issue was migrated from crbug.com/chromium/938724?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094209)*
