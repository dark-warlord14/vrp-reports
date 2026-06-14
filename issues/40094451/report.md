# pdfium (XFA): oob read in CFXJSE_FormCalcContext::WordNum

| Field | Value |
|-------|-------|
| **Issue ID** | [40094451](https://issues.chromium.org/issues/40094451) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-03-31 |
| **Bounty** | $2,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36

Steps to reproduce the problem:
AddressSanitizer: global-buffer-overflow on address 0x561dc72a0a88 at pc 0x561dc37953ea bp 0x7ffc5a14bb10 sp 0x7ffc5a14b2d8
READ of size 16 at 0x561dc72a0a88 thread T0
SCARINESS: 26 (multi-byte-read-global-buffer-overflow)

    #1 0x561dc5cbbf17 in (anonymous namespace)::TrillionUS(fxcrt::StringViewTemplate<char>) fxjs/xfa/cfxjse_formcalc_context.cpp:1222:17
    #2 0x561dc5c4f638 in (anonymous namespace)::WordUS(fxcrt::ByteString const&, int) fxjs/xfa/cfxjse_formcalc_context.cpp:1311:15
    #3 0x561dc5c4f2bc in CFXJSE_FormCalcContext::WordNum(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Arguments&) fxjs/xfa/cfxjse_formcalc_context.cpp:4407:7
    #4 0x561dc5c236a7 in (anonymous namespace)::V8FunctionCallback_Wrapper(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:47:3
    #5 0x561dc3eeb605 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:157:3
    #6 0x561dc3e0c1b8 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #7 0x561dc3e08a1a in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #8 0x561dc3e0800e in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:127:1
    #9 0x561dc568dfb8 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit
    #10 0x561dc5600ea3 in Builtins_InterpreterEntryTrampoline
    #11 0x561dc5600ea3 in Builtins_InterpreterEntryTrampoline
    #12 0x561dc55fa39b in Builtins_ArgumentsAdaptorTrampoline
    #13 0x561dc5600ea3 in Builtins_InterpreterEntryTrampoline
    #14 0x561dc55fa39b in Builtins_ArgumentsAdaptorTrampoline
    #15 0x561dc55fe81c in Builtins_JSEntryTrampoline
    #16 0x561dc55fe597 in Builtins_JSEntry
    #17 0x561dc4642ce3 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:274:33
    #18 0x561dc4641d2a in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:366:10
    #19 0x561dc396e266 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:4985:7
    #20 0x561dc5c255b9 in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:293:21
    #21 0x561dc5c28cf7 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:149:23
    #22 0x561dc5e60843 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2788:22
    #23 0x561dc5e5fff1 in CXFA_Node::ProcessValidate(CXFA_FFDocView*, int) xfa/fxfa/parser/cxfa_node.cpp:2684:28
    #24 0x561dc5d8ae15 in XFA_ProcessEvent(CXFA_FFDocView*, CXFA_Node*, CXFA_EventParam*) xfa/fxfa/cxfa_ffdocview.cpp:345:23
    #25 0x561dc5d88991 in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:406:11
    #26 0x561dc5d888ed in CXFA_FFDocView::ExecEventActivityByDeepFirst(CXFA_Node*, XFA_EVENTTYPE, bool, bool) xfa/fxfa/cxfa_ffdocview.cpp:394:17
    #27 0x561dc5d88cfc in CXFA_FFDocView::InitValidate(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:570:3
    #28 0x561dc5d88b5e in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:87:3
    #29 0x561dc5d2f251 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:125:22
    #30 0x561dc57c3196 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #31 0x561dc37c7d92 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:800:12
    #32 0x561dc37c52b0 in main samples/pdfium_test.cc:1015:5

Shadow bytes around the buggy address:
  0x0ac438e4c100: 00 00 00 00 00 00 00 00 f9 f9 f9 f9 00 f9 f9 f9
  0x0ac438e4c110: f9 f9 f9 f9 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac438e4c120: 00 00 00 00 f9 f9 f9 f9 00 f9 f9 f9 f9 f9 f9 f9
  0x0ac438e4c130: 00 00 00 00 00 00 00 00 00 00 f9 f9 f9 f9 f9 f9
  0x0ac438e4c140: 00 f9 f9 f9 f9 f9 f9 f9 00 f9 f9 f9 f9 f9 f9 f9
=>0x0ac438e4c150: 00[f9]f9 f9 f9 f9 f9 f9 00 f9 f9 f9 f9 f9 f9 f9
  0x0ac438e4c160: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac438e4c170: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f9 f9
  0x0ac438e4c180: f9 f9 f9 f9 00 f9 f9 f9 f9 f9 f9 f9 00 f9 f9 f9
  0x0ac438e4c190: f9 f9 f9 f9 00 f9 f9 f9 f9 f9 f9 f9 00 f9 f9 f9
  0x0ac438e4c1a0: f9 f9 f9 f9 00 f9 f9 f9 f9 f9 f9 f9 00 f9 f9 f9
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

What is the expected behavior?

What went wrong?
^

Did this work before? No 

Chrome version: 70.0.3538.124  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-947876.pdf](attachments/chromium-947876.pdf) (application/pdf, 450 B)

## Timeline

### pd...@gmail.com (2019-03-31)

And by UBSAN.

fxjs/xfa/cfxjse_formcalc_context.cpp:1222:17: runtime error: index 62 out of bounds for type 'const ByteStringView [10]'
    #0 0x55723c6f354a in (anonymous namespace)::TrillionUS(fxcrt::StringViewTemplate<char>) fxjs/xfa/cfxjse_formcalc_context.cpp:1222:17


### pd...@gmail.com (2019-03-31)

[Comment Deleted]

### pd...@gmail.com (2019-03-31)

In WordNum, the following code.

https://cs.chromium.org/chromium/src/third_party/pdfium/fxjs/xfa/cfxjse_formcalc_context.cpp?l=4401&rcl=21d000094adeb6be3b97f3758523c6117f334e82

  if (fNumber < 0.0f || fNumber > 922337203685477550.0f) {
    args.GetReturnValue()->SetString("*");
    return;
  }

  args.GetReturnValue()->SetString(
      WordUS(ByteString::Format("%.2f", fNumber), iIdentifier).AsStringView());

With the attached PDF, fNumber is NaN, which is passed as string "nan" to WordUS. That function only expects dots and numbers. At some point it calls TrillionUS, which triggers the bug on this line.

https://cs.chromium.org/chromium/src/third_party/pdfium/fxjs/xfa/cfxjse_formcalc_context.cpp?l=1222&rcl=21d000094adeb6be3b97f3758523c6117f334e82

      strBuf << pCapUnits[pData[iIndex] - '0'];

With 'n' - '0' == 62. That's the first location reported by ASAN, but more follow with similar reports.

The fix is simple.

diff --git a/fxjs/xfa/cfxjse_formcalc_context.cpp b/fxjs/xfa/cfxjse_formcalc_context.cpp
index 879ba02..27a9d8c 100644
--- a/fxjs/xfa/cfxjse_formcalc_context.cpp
+++ b/fxjs/xfa/cfxjse_formcalc_context.cpp
@@ -4398,7 +4398,7 @@ void CFXJSE_FormCalcContext::WordNum(CFXJSE_Value* pThis,
     bsLocale = ValueToUTF8String(localeValue.get());
   }
 
-  if (fNumber < 0.0f || fNumber > 922337203685477550.0f) {
+  if (fNumber < 0.0f || fNumber > 922337203685477550.0f || std::isnan(fNumber)) {
     args.GetReturnValue()->SetString("*");
     return;
   }


### dr...@chromium.org (2019-04-01)

This reproduces with an XFA-enabled build of pdfium_test. Assigning impact None, since Chrome doesn't ship with XFA-enabled. Assigning to thestig@, who appears to have been doing work on XFA lately.

[Monorail components: Internals>Plugins>PDF]

### pd...@gmail.com (2019-09-05)

Just confirmation: still reproduces.

### pd...@gmail.com (2019-09-11)

Relevant snippet from the specs.

> If n1 is not numeric or the integral value of n1 is negative or greater than 922,337,203,685,477,550 the
function returns "*" (asterisk) characters to indicate an error condition.

### ts...@chromium.org (2019-11-04)

Thanks, I finally cobbled together a CL with the suggested fix at https://pdfium-review.googlesource.com/c/pdfium/+/61910

### ts...@chromium.org (2019-11-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-04)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/69dd6b02511ca608412a1501cdbd692e8a406ada

commit 69dd6b02511ca608412a1501cdbd692e8a406ada
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Nov 04 22:46:47 2019

Check for NaN in CFXJSE_FormCalcContext::WordNum()

Bug: chromium:947876
Change-Id: Ic37f077cddcfcb12e8b6fa66e93e2ab2cd1038e7
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/61910
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/69dd6b02511ca608412a1501cdbd692e8a406ada/fxjs/xfa/cfxjse_formcalc_context.cpp


### ts...@chromium.org (2019-11-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/174e5e8bcbcad223e9553ed0c7d3e1eed6f5bd8a

commit 174e5e8bcbcad223e9553ed0c7d3e1eed6f5bd8a
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Nov 05 10:18:28 2019

Roll src/third_party/pdfium c3a91730e33e..69dd6b02511c (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c3a91730e33e..69dd6b02511c

git log c3a91730e33e..69dd6b02511c --date=short --no-merges --format='%ad %ae %s'
2019-11-04 tsepez@chromium.org Check for NaN in CFXJSE_FormCalcContext::WordNum()
2019-11-04 dhoss@chromium.org Change variable target_type to static_component_type in //:pdfium

Created with:
  gclient setdep -r src/third_party/pdfium@69dd6b02511c

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:947876
Change-Id: I43ade48f66c0b64a4e8199dc77e404af1dd49659
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1899286
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#712509}

[modify] https://crrev.com/174e5e8bcbcad223e9553ed0c7d3e1eed6f5bd8a/DEPS


### sh...@chromium.org (2019-11-05)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-07)

Nice one! The Panel decided to reward $2,000 + $500 patching bonus for this report! 

### na...@google.com (2019-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-02-15)

This issue was migrated from crbug.com/chromium/947876?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094451)*
