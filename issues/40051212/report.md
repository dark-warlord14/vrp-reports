# pdfium (XFA): use-of-uninitialized-value in CFWL_DateTimePicker::DrawWidget

| Field | Value |
|-------|-------|
| **Issue ID** | [40051212](https://issues.chromium.org/issues/40051212) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-01-13 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.130 Safari/537.36

Steps to reproduce the problem:
WARNING: MemorySanitizer: use-of-uninitialized-value

    #0 0x5627b80f3de6 in CFX_RectF::IsEmpty() const core/fxcrt/fx_coordinates.h:412:44
    #1 0x5627b82c5ba8 in CFWL_DateTimePicker::DrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_datetimepicker.cpp:118:16
    #2 0x5627b82c9728 in CFWL_DateTimePicker::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_datetimepicker.cpp:381:3
    #3 0x5627b815a72a in CXFA_FFTextEdit::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fftextedit.cpp:377:19
    #4 0x5627b815a77c in non-virtual thunk to CXFA_FFTextEdit::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fftextedit.cpp
    #5 0x5627b832a029 in CFWL_WidgetMgr::OnDrawWidget(CFWL_Widget*, CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_widgetmgr.cpp:332:27
    #6 0x5627b80f2fbe in CXFA_FFField::RenderWidget(CXFA_Graphics*, CFX_Matrix const&, CXFA_FFWidget::HighlightOption) xfa/fxfa/cxfa_fffield.cpp:85:32
    #7 0x5627b8177c69 in CXFA_RenderContext::DoRender(CXFA_Graphics*) xfa/fxfa/cxfa_rendercontext.cpp:29:18
    #8 0x5627b862a570 in CPDFXFA_Page::DrawFocusAnnot(CFX_RenderDevice*, CPDFSDK_Annot*, CFX_Matrix const&, FX_RECT const&) fpdfsdk/fpdfxfa/cpdfxfa_page.cpp:245:17
    #9 0x5627b314c3ac in CPDFSDK_PageView::PageView_OnDraw(CFX_RenderDevice*, CFX_Matrix const&, CPDF_RenderOptions*, FX_RECT const&) fpdfsdk/cpdfsdk_pageview.cpp:78:40
    #10 0x5627b3195d6d in (anonymous namespace)::FFLCommon(fpdf_form_handle_t__*, fpdf_bitmap_t__*, void*, fpdf_page_t__*, int, int, int, int, int, int) fpdfsdk/fpdf_formfill.cpp:220:18
    #11 0x5627b319541c in FPDF_FFLDraw fpdfsdk/fpdf_formfill.cpp:568:3
    #12 0x5627b306b813 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:745:5
    #13 0x5627b305d3fe in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:960:9
    #14 0x5627b3056c4d in main samples/pdfium_test.cc:1179:5

  Uninitialized value was stored to memory at
    #0 0x5627b3000506 in __msan_memcpy /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan_interceptors.cpp:1567:3
    #1 0x5627b82c8d97 in CFWL_DateTimePicker::OnFocusChanged(CFWL_Message*, bool) xfa/fwl/cfwl_datetimepicker.cpp:392:15
    #2 0x5627b82c8827 in CFWL_DateTimePicker::OnProcessMessage(CFWL_Message*) xfa/fwl/cfwl_datetimepicker.cpp
    #3 0x5627b815a3ee in CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp:356:19
    #4 0x5627b815a43c in non-virtual thunk to CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp
    #5 0x5627b830ba21 in CFWL_NoteDriver::DispatchMessage(CFWL_Message*, CFWL_Widget*) xfa/fwl/cfwl_notedriver.cpp:148:16
    #6 0x5627b830b55c in CFWL_NoteDriver::ProcessMessage(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_notedriver.cpp:108:8
    #7 0x5627b8329c8c in CFWL_WidgetMgr::OnProcessMessageToForm(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_widgetmgr.cpp:320:16
    #8 0x5627b80f8852 in CXFA_FFField::SendMessageToFWLWidget(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fxfa/cxfa_fffield.cpp:743:32
    #9 0x5627b815815e in CXFA_FFTextEdit::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fftextedit.cpp:181:3
    #10 0x5627b80e0d10 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:316:25
    #11 0x5627b80dd0ca in CXFA_FFDocView::SetFocusNode(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:334:8
    #12 0x5627b811709c in CXFA_FFNotify::SetFocusWidgetNode(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:320:13
    #13 0x5627b3f193f1 in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:447:12
    #14 0x5627b3f1388f in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #15 0x5627b3f3db86 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:177:10
    #16 0x5627b3e5bcbf in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:483:31
    #17 0x5627b3e4ffa8 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #18 0x5627b421ee58 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #19 0x5627b421a3f5 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36

  Uninitialized value was stored to memory at
    #0 0x5627b32255ef in CFX_RectF::CFX_RectF(float, float, float, float) core/fxcrt/fx_coordinates.h:329:39
    #1 0x5627b82c8d86 in CFWL_DateTimePicker::OnFocusChanged(CFWL_Message*, bool) xfa/fwl/cfwl_datetimepicker.cpp:392:17
    #2 0x5627b82c8827 in CFWL_DateTimePicker::OnProcessMessage(CFWL_Message*) xfa/fwl/cfwl_datetimepicker.cpp
    #3 0x5627b815a3ee in CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp:356:19
    #4 0x5627b815a43c in non-virtual thunk to CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp
    #5 0x5627b830ba21 in CFWL_NoteDriver::DispatchMessage(CFWL_Message*, CFWL_Widget*) xfa/fwl/cfwl_notedriver.cpp:148:16
    #6 0x5627b830b55c in CFWL_NoteDriver::ProcessMessage(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_notedriver.cpp:108:8
    #7 0x5627b8329c8c in CFWL_WidgetMgr::OnProcessMessageToForm(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_widgetmgr.cpp:320:16
    #8 0x5627b80f8852 in CXFA_FFField::SendMessageToFWLWidget(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fxfa/cxfa_fffield.cpp:743:32
    #9 0x5627b815815e in CXFA_FFTextEdit::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fftextedit.cpp:181:3
    #10 0x5627b80e0d10 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:316:25
    #11 0x5627b80dd0ca in CXFA_FFDocView::SetFocusNode(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:334:8
    #12 0x5627b811709c in CXFA_FFNotify::SetFocusWidgetNode(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:320:13
    #13 0x5627b3f193f1 in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:447:12
    #14 0x5627b3f1388f in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #15 0x5627b3f3db86 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:177:10
    #16 0x5627b3e5bcbf in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:483:31
    #17 0x5627b3e4ffa8 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #18 0x5627b421ee58 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #19 0x5627b421a3f5 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36

  Uninitialized value was created by a heap allocation
    #0 0x5627b3054fc9 in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan_new_delete.cpp:45:35
    #1 0x5627b80c92f9 in pdfium::internal::MakeUniqueResult<CFWL_DateTimePicker>::Scalar pdfium::MakeUnique<CFWL_DateTimePicker, CFWL_App const*>(CFWL_App const*&&) third_party/base/ptr_util.h:56:29
    #2 0x5627b80c8a68 in CXFA_FFDateTimeEdit::LoadWidget() xfa/fxfa/cxfa_ffdatetimeedit.cpp:46:21
    #3 0x5627b812df0f in CXFA_FFPageWidgetIterator::GetWidget(CXFA_LayoutItem*) xfa/fxfa/cxfa_ffpageview.cpp:215:19
    #4 0x5627b812e4e6 in CXFA_FFPageWidgetIterator::MoveToNext() xfa/fxfa/cxfa_ffpageview.cpp:178:34
    #5 0x5627b3151668 in CPDFSDK_PageView::LoadFXAnnots() fpdfsdk/cpdfsdk_pageview.cpp:492:55
    #6 0x5627b3114af4 in CPDFSDK_FormFillEnvironment::GetPageView(IPDF_Page*, bool) fpdfsdk/cpdfsdk_formfillenvironment.cpp:581:14
    #7 0x5627b31948b5 in (anonymous namespace)::FormHandleToPageView(fpdf_form_handle_t__*, fpdf_page_t__*) fpdfsdk/fpdf_formfill.cpp:171:39
    #8 0x5627b31963b8 in FORM_OnAfterLoadPage fpdfsdk/fpdf_formfill.cpp:619:37
    #9 0x5627b306a619 in (anonymous namespace)::GetPageForIndex(_FPDF_FORMFILLINFO*, fpdf_document_t__*, int) samples/pdfium_test.cc:674:3
    #10 0x5627b306a986 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:693:20
    #11 0x5627b305d3fe in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:960:9
    #12 0x5627b3056c4d in main samples/pdfium_test.cc:1179:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.130  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1041303.pdf](attachments/chromium-1041303.pdf) (application/pdf, 634 B)

## Timeline

### pd...@gmail.com (2020-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-01-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5164788353138688.

### ts...@chromium.org (2020-01-13)

XFA -> not shipped, float constant used in subsequent size calculation may not leak much information.

### ts...@chromium.org (2020-01-13)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-01-13)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2020-01-13)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/65011

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-13)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b43f594b3900ffe36729d78bfe87e1862badce5a

commit b43f594b3900ffe36729d78bfe87e1862badce5a
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Jan 13 19:12:43 2020

Initialize all scalars in header for CFWL_DateTimePicker.

Avoid potential uninitialized reads.

- Tidy/pack members by size/complexity while at it.

Bug: chromium:1041303
Change-Id: I51f4514809783262b5179553a2e93a5329867e97
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65011
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/b43f594b3900ffe36729d78bfe87e1862badce5a/xfa/fwl/cfwl_datetimepicker.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/b43f594b3900ffe36729d78bfe87e1862badce5a/xfa/fwl/cfwl_datetimepicker.h


### ts...@chromium.org (2020-01-13)

Trivial fix is to stick an initializer in the header.

### cl...@chromium.org (2020-01-13)

Testcase 5164788353138688 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5164788353138688.

### pd...@gmail.com (2020-01-13)

(I forgot the usual XFA note.)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9b6b4f1f4e51dd7d22ac2a121e086fa5ec515df8

commit 9b6b4f1f4e51dd7d22ac2a121e086fa5ec515df8
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jan 14 07:56:40 2020

Roll src/third_party/pdfium 801b95f34349..f12daef7970e (6 commits)

https://pdfium.googlesource.com/pdfium.git/+log/801b95f34349..f12daef7970e

git log 801b95f34349..f12daef7970e --date=short --first-parent --format='%ad %ae %s'
2020-01-13 tsepez@chromium.org Call xfa.host.pageUp(), pageDown(), and resetData() from JS tests.
2020-01-13 thestig@chromium.org Use IsValueInRangeForNumericType() in CPDF_StreamParser.
2020-01-13 thestig@chromium.org Consistently read |CPDF_StreamParser::m_pBuf| values as uint8_t.
2020-01-13 thestig@chromium.org Clean up some CFFL class headers.
2020-01-13 tsepez@chromium.org Initialize all scalars in header for CFWL_DateTimePicker.
2020-01-13 nigi@chromium.org Add string validations in StringToCode() and StringToWideString().

Created with:
  gclient setdep -r src/third_party/pdfium@f12daef7970e

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1041303
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ic7f6d5c6d88b51aa810c7afb5a7b8e9d0c02c07a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1999454
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#731139}

[modify] https://crrev.com/9b6b4f1f4e51dd7d22ac2a121e086fa5ec515df8/DEPS


### sh...@chromium.org (2020-01-14)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-14)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $500 for this report!

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-21)

This issue was migrated from crbug.com/chromium/1041303?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051212)*
