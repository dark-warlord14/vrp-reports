# pdfium (XFA): invalid vptr / uaf in CXFA_FFDocView::RunBindItems

| Field | Value |
|-------|-------|
| **Issue ID** | [40094506](https://issues.chromium.org/issues/40094506) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-04-04 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36

Steps to reproduce the problem:
(UBSAN)

xfa/fxfa/cxfa_ffdocview.cpp:600:15: runtime error: member call on address 0x55e7e795b150 which does not point to an object of type 'CXFA_Node'
0x55e7e795b150: note: object has a possibly invalid vptr: abs(offset to top) too big
 00 00 00 00  f1 54 33 9f e7 0c 00 00  00 00 53 21 ad de ad 1b  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              possibly invalid vptr
    #0 0x55e7e4eb3c7f in CXFA_FFDocView::RunBindItems() xfa/fxfa/cxfa_ffdocview.cpp:600:15
    #1 0x55e7e4eb3b89 in CXFA_FFDocView::InitLayout(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:65:3
    #2 0x55e7e4eb50ad in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:85:3
    #3 0x55e7e4e30b2e in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:125:22
    #4 0x55e7e4824a4a in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #5 0x55e7e37143d1 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:800:12
    #6 0x55e7e37124c8 in main samples/pdfium_test.cc:1015:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 70.0.3538.124  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-949425.pdf](attachments/chromium-949425.pdf) (application/pdf, 454 B)

## Timeline

### pd...@gmail.com (2019-04-04)

(ASAN)

AddressSanitizer: heap-use-after-free on address 0x60200001eb98 at pc 0x563c8fd006a4 bp 0x7ffea24867b0 sp 0x7ffea24867a8
READ of size 8 at 0x60200001eb98 thread T0
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x563c8fd006a3 in CXFA_FFDocView::RunBindItems() xfa/fxfa/cxfa_ffdocview.cpp:599:19
    #1 0x563c8fcffe01 in CXFA_FFDocView::InitLayout(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:65:3
    #2 0x563c8fd00b48 in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:85:3
    #3 0x563c8fca7251 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:125:22
    #4 0x563c8f73b196 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #5 0x563c8d73fd92 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:800:12
    #6 0x563c8d73d2b0 in main samples/pdfium_test.cc:1015:5
    #7 0x7f46434bd82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

0x60200001eb98 is located 8 bytes inside of 16-byte region [0x60200001eb90,0x60200001eba0)
freed by thread T0 here:
    #0 0x563c8d73ad1d in operator delete(void*) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:166:3
    #1 0x563c8d744838 in std::__1::_DeallocateCaller::__do_call(void*) buildtools/third_party/libc++/trunk/include/new:319:12
    #2 0x563c8d744828 in std::__1::_DeallocateCaller::__do_deallocate_handle_size(void*, unsigned long) buildtools/third_party/libc++/trunk/include/new:277:12
    #3 0x563c8d744818 in std::__1::_DeallocateCaller::__do_deallocate_handle_size_align(void*, unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:247:12
    #4 0x563c8d744808 in std::__1::__libcpp_deallocate(void*, unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:325:3
    #5 0x563c8fd3ade8 in std::__1::allocator<CXFA_BindItems*>::deallocate(CXFA_BindItems**, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1816:10
    #6 0x563c8fd3ac98 in std::__1::allocator_traits<std::__1::allocator<CXFA_BindItems*> >::deallocate(std::__1::allocator<CXFA_BindItems*>&, CXFA_BindItems**, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1554:14
    #7 0x563c8fd3a557 in std::__1::__split_buffer<CXFA_BindItems*, std::__1::allocator<CXFA_BindItems*>&>::~__split_buffer() buildtools/third_party/libc++/trunk/include/__split_buffer:343:9
    #8 0x563c8fd39c7b in void std::__1::vector<CXFA_BindItems*, std::__1::allocator<CXFA_BindItems*> >::__push_back_slow_path<CXFA_BindItems* const&>(CXFA_BindItems* const&) buildtools/third_party/libc++/trunk/include/vector:1622:1
    #9 0x563c8fd398c5 in std::__1::vector<CXFA_BindItems*, std::__1::allocator<CXFA_BindItems*> >::push_back(CXFA_BindItems* const&) buildtools/third_party/libc++/trunk/include/vector:1638:9
    #10 0x563c8fd12dd2 in CXFA_FFDocView::AddBindItem(CXFA_BindItems*) xfa/fxfa/cxfa_ffdocview.h:93:56
    #11 0x563c8fd12cc8 in CXFA_FFNotify::OnNodeReady(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:322:17
    #12 0x563c8fdcb166 in CXFA_Node::SetFlagAndNotify(unsigned int) xfa/fxfa/parser/cxfa_node.cpp:1794:16
    #13 0x563c8fdcad74 in CXFA_Node::Clone(bool) xfa/fxfa/parser/cxfa_node.cpp:1011:11
    #14 0x563c8fc86aaa in CJX_Node::clone(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_node.cpp:184:41
    #15 0x563c8fc8638c in CJX_Node::clone_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_node.h:26:3
    #16 0x563c8fc8a824 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:177:10
    #17 0x563c8fb9e704 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:454:31
    #18 0x563c8fc3035c in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #19 0x563c8de63605 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:157:3
    #20 0x563c8dd841b8 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #21 0x563c8dd80a1a in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #22 0x563c8dd8000e in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:127:1
    #23 0x563c8f605fb8 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit
    #24 0x563c8f578ea3 in Builtins_InterpreterEntryTrampoline
    #25 0x563c8f578ea3 in Builtins_InterpreterEntryTrampoline
    #26 0x563c8f578ea3 in Builtins_InterpreterEntryTrampoline
    #27 0x563c8f578ea3 in Builtins_InterpreterEntryTrampoline
    #28 0x563c8f578ea3 in Builtins_InterpreterEntryTrampoline
    #29 0x563c8f57239b in Builtins_ArgumentsAdaptorTrampoline

previously allocated by thread T0 here:
    #0 0x563c8d73a4bd in operator new(unsigned long) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:105:3
    #1 0x563c8d741108 in std::__1::__libcpp_allocate(unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:238:10
    #2 0x563c8fd3a8b3 in std::__1::allocator<CXFA_BindItems*>::allocate(unsigned long, void const*) buildtools/third_party/libc++/trunk/include/memory:1813:37
    #3 0x563c8fd3a7da in std::__1::allocator_traits<std::__1::allocator<CXFA_BindItems*> >::allocate(std::__1::allocator<CXFA_BindItems*>&, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1546:21
    #4 0x563c8fd3a2ed in std::__1::__split_buffer<CXFA_BindItems*, std::__1::allocator<CXFA_BindItems*>&>::__split_buffer(unsigned long, unsigned long, std::__1::allocator<CXFA_BindItems*>&) buildtools/third_party/libc++/trunk/include/__split_buffer:311:29
    #5 0x563c8fd39c0e in void std::__1::vector<CXFA_BindItems*, std::__1::allocator<CXFA_BindItems*> >::__push_back_slow_path<CXFA_BindItems* const&>(CXFA_BindItems* const&) buildtools/third_party/libc++/trunk/include/vector:1617:49
    #6 0x563c8fd398c5 in std::__1::vector<CXFA_BindItems*, std::__1::allocator<CXFA_BindItems*> >::push_back(CXFA_BindItems* const&) buildtools/third_party/libc++/trunk/include/vector:1638:9
    #7 0x563c8fd12dd2 in CXFA_FFDocView::AddBindItem(CXFA_BindItems*) xfa/fxfa/cxfa_ffdocview.h:93:56
    #8 0x563c8fd12cc8 in CXFA_FFNotify::OnNodeReady(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:322:17
    #9 0x563c8fdcb166 in CXFA_Node::SetFlagAndNotify(unsigned int) xfa/fxfa/parser/cxfa_node.cpp:1794:16
    #10 0x563c8fdcc0c4 in CXFA_Node::CloneTemplateToForm(bool) xfa/fxfa/parser/cxfa_node.cpp:1197:11
    #11 0x563c8fe90e0d in XFA_NodeMerge_CloneOrMergeContainer(CXFA_Document*, CXFA_Node*, CXFA_Node*, bool, std::__1::vector<CXFA_Node*, std::__1::allocator<CXFA_Node*> >*) xfa/fxfa/parser/xfa_document_datamerger_imp.cpp:84:48
    #12 0x563c8fd90978 in CXFA_Document::DoDataMerge() xfa/fxfa/parser/cxfa_document.cpp:1758:7
    #13 0x563c8fd00ae0 in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:73:24
    #14 0x563c8fca7251 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:125:22
    #15 0x563c8f73b196 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #16 0x563c8d73fd92 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:800:12
    #17 0x563c8d73d2b0 in main samples/pdfium_test.cc:1015:5
    #18 0x7f46434bd82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-use-after-free xfa/fxfa/cxfa_ffdocview.cpp:599:19 in CXFA_FFDocView::RunBindItems()
Shadow bytes around the buggy address:
  0x0c047fffbd20: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c047fffbd30: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fa
  0x0c047fffbd40: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c047fffbd50: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd
  0x0c047fffbd60: fa fa fd fd fa fa 00 fa fa fa 00 fa fa fa fd fa
=>0x0c047fffbd70: fa fa fd[fd]fa fa 00 fa fa fa 00 fa fa fa fd fa
  0x0c047fffbd80: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c047fffbd90: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd
  0x0c047fffbda0: fa fa 00 00 fa fa fd fa fa fa fd fd fa fa fd fa
  0x0c047fffbdb0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c047fffbdc0: fa fa fd fd fa fa 00 00 fa fa fd fa fa fa fd fd
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


### pd...@gmail.com (2019-04-04)

[Empty comment from Monorail migration]

### pd...@gmail.com (2019-04-04)

Relevant snippet from XFA spec.

> The syntax " .[formcalc_expression] " can be used to select all sibling nodes that match the given
> expression. The contained expression must yield a Boolean value.

Although that's probably a red herring I think. It's just an opportunity to run a formcalc script.

### pd...@gmail.com (2019-04-04)

[Comment Deleted]

### cl...@chromium.org (2019-04-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6014088479113216.

### cl...@chromium.org (2019-04-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-04-04)

Automatically assigning owner based on suspected regression changelist https://pdfium.googlesource.com/pdfium/+/70180648ffd01dd3716871758411d2031aaaebbe (Add a CFX_XMLDocument class.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-04-04)

Detailed report: https://clusterfuzz.com/testcase?key=6014088479113216

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x609000113c38
Crash State:
  CXFA_FFDocView::RunBindItems
  CXFA_FFDocView::InitLayout
  CXFA_FFDocView::StartLayout
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=555504:555559

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6014088479113216

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### th...@chromium.org (2019-04-04)

Thanks for continuing to report XFA bogs. I'm a bit behind on them, since they don't have security impact as is, but I will get to them sooner or later.

### oc...@google.com (2019-05-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-24)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a6ab0ba17520745b10a1f7b2a7990be5bca0478d

commit a6ab0ba17520745b10a1f7b2a7990be5bca0478d
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Jun 24 17:32:00 2019

Switch from vector to deque for another CXFA_FFDocView members.

This make it easier to iterate through them safely.

BUG=chromium:949425

Change-Id: I14dd051f0ba5b25dd6e0fbcbae8d3afb42a243a9
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/56770
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/a6ab0ba17520745b10a1f7b2a7990be5bca0478d/xfa/fxfa/cxfa_ffdocview.cpp
[modify] https://crrev.com/a6ab0ba17520745b10a1f7b2a7990be5bca0478d/xfa/fxfa/cxfa_ffdocview.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7916e23f916e0a63a2ae72114a3fbcf9a27c44a7

commit 7916e23f916e0a63a2ae72114a3fbcf9a27c44a7
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jun 24 18:53:31 2019

Roll src/third_party/pdfium 9d1193b591c5..ad6de6a08a66 (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/9d1193b591c5..ad6de6a08a66


git log 9d1193b591c5..ad6de6a08a66 --date=short --no-merges --format='%ad %ae %s'
2019-06-24 asweintraub@google.com Fix ClangTidy-Readability/Naming findings in core/fpdfapi.
2019-06-24 thestig@chromium.org Switch from vector to deque for another CXFA_FFDocView members.
2019-06-24 chinsenj@google.com Fix Heap-buffer-overflow caused by PDF_DataDecode() refactor
2019-06-24 asweintraub@google.com Fix 22 ClangTidy - Readability/Naming findings in fpdfsdk.
2019-06-24 asweintraub@google.com Fix 2 ClangTidy - Readability/Naming findings in core/fdrm


Created with:
  gclient setdep -r src/third_party/pdfium@ad6de6a08a66

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:949425,chromium:977832
TBR=pdfium-deps-rolls@chromium.org

Change-Id: Ibae0cc2eab33d9fc235328820b0b550c81857887
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1674217
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#671731}

[modify] https://crrev.com/7916e23f916e0a63a2ae72114a3fbcf9a27c44a7/DEPS


### cl...@chromium.org (2019-06-25)

Detailed report: https://clusterfuzz.com/testcase?key=6014088479113216

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x609000113c38
Crash State:
  CXFA_FFDocView::RunBindItems
  CXFA_FFDocView::InitLayout
  CXFA_FFDocView::StartLayout
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=555504:555559

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6014088479113216

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### cl...@chromium.org (2019-06-25)

ClusterFuzz testcase 6014088479113216 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=671725:671734

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### th...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report! 

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-10-01)

This issue was migrated from crbug.com/chromium/949425?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/962802, crbug.com/chromium/977463]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094506)*
