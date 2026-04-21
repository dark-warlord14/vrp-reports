# Security: Use after free in PDFium's Field::page

| Field | Value |
|-------|-------|
| **Issue ID** | [40086454](https://issues.chromium.org/issues/40086454) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | [Deleted User] |
| **Assignee** | ts...@chromium.org |
| **Created** | 2017-01-10 |
| **Bounty** | $3,000.00 |

## Description

*No description available.*

## Timeline

### ts...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-01-10)

Is the main.pdf a complete example in and of itself?  Or does it need to be combined somehow with your main.itx?  If it is the later, can we get a single file that reproduces the issue?

Also, what are the flags you are using? There's got to be an expose-gc set somewhere for the gc() call to have effect? 

### ts...@chromium.org (2017-01-10)

Ah, nevermind, you've provided your own gc() implementation, which co-incidentally is the name of function v8 exposes for us given the flag.

### ts...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-01-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6353787523694592

### ts...@chromium.org (2017-01-10)

Yes, I'm working on putting together a non-xfa example, since I didn't see anything XFA-specific, and its easy enough to get into JS without XFA.  

### ts...@chromium.org (2017-01-10)

[Comment Deleted]

### ts...@chromium.org (2017-01-10)

[Comment Deleted]

### ts...@chromium.org (2017-01-10)

[Comment Deleted]

### ts...@chromium.org (2017-01-10)

Ok, finally have a repro.  Not present in any chrome version, hence sev-none, but an XFA blocker. 

==10127==ERROR: AddressSanitizer: heap-use-after-free on address 0x6080000020c0 at pc 0x0000023c978a bp 0x7ffddcfb1f50 sp 0x7ffddcfb1f48
READ of size 8 at 0x6080000020c0 thread T0
    #0 0x23c9789 in GetPageView fpdfsdk/cpdfsdk_annot.h:55:50
    #1 0x23c9789 in Field::page(IJS_Context*, CJS_PropValue&, CFX_WideString&) fpdfsdk/javascript/Field.cpp:1828
    #2 0x23e2bcd in void JSPropGetter<Field, &Field::page>(char const*, char const*, v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) fpdfsdk/javascript/JS_Define.h:88:8
    #3 0x126a5f7 in v8::internal::PropertyCallbackArguments::Call(void (*)(v8::Local<v8::Name>, v8::PropertyCallbackInfo<v8::Value> const&), v8::internal::Handle<v8::internal::Name>) v8/src/api-arguments-inl.h:32:1
    #4 0x1416d95 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator*) v8/src/objects.cc:1353:34
    #5 0x141488a in v8::internal::Object::GetProperty(v8::internal::LookupIterator*) v8/src/objects.cc:999:16
    #6 0x122987c in v8::internal::LoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>) v8/src/ic/ic.cc:644:5
    #7 0x124887d in __RT_impl_Runtime_LoadIC_Miss v8/src/ic/ic.cc:2623:5
    #8 0x124887d in v8::internal::Runtime_LoadIC_Miss(int, v8::internal::Object**, v8::internal::Isolate*) v8/src/ic/ic.cc:2606
    #9 0x7f022c1043a6  (<unknown module>)
    #10 0x7f022c1847ec  (<unknown module>)
    #11 0x7f022c172c37  (<unknown module>)
    #12 0x7f022c205dc0  (<unknown module>)
    #13 0x7f022c172302  (<unknown module>)
    #14 0x7f022c136e20  (<unknown module>)
    #15 0xff7a3b in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>) v8/src/execution.cc:139:13
    #16 0xff7262 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:176:10
    #17 0x527c71 in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:1946:7
    #18 0x243c2cc in CFXJS_Engine::Execute(CFX_WideString const&, FXJSErr*) fxjs/fxjs_v8.cpp:469:25
    #19 0x23665dc in CJS_Runtime::ExecuteScript(CFX_WideString const&, CFX_WideString*) fpdfsdk/javascript/cjs_runtime.cpp:206:14
    #20 0x2436e54 in CJS_Context::RunScript(CFX_WideString const&, CFX_WideString*) fpdfsdk/javascript/cjs_context.cpp:48:24
    #21 0x1e6a14a in RunDocumentOpenJavaScript fpdfsdk/fsdk_actionhandler.cpp:537:25
    #22 0x1e6a14a in CPDFSDK_ActionHandler::ExecuteDocumentOpenAction(CPDF_Action const&, CPDFSDK_FormFillEnvironment*, std::__1::set<CPDF_Dictionary*, std::__1::less<CPDF_Dictionary*>, std::__1::allocator<CPDF_Dictionary*> >*) fpdfsdk/fsdk_actionhandler.cpp:128
    #23 0x1e69d17 in CPDFSDK_ActionHandler::DoAction_DocOpen(CPDF_Action const&, CPDFSDK_FormFillEnvironment*) fpdfsdk/fsdk_actionhandler.cpp:25:10
    #24 0x1e73227 in CPDFSDK_FormFillEnvironment::ProcOpenAction() fpdfsdk/cpdfsdk_formfillenvironment.cpp:643:26
    #25 0x1e65d33 in FORM_DoDocumentOpenAction fpdfsdk/fpdfformfill.cpp:695:19
    #26 0x4fa46a in RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:841:3
    #27 0x4fb6a2 in main samples/pdfium_test.cc:998:5
    #28 0x7f0254722f44 in __libc_start_main /build/eglibc-oGUzwX/eglibc-2.19/csu/libc-start.c:287

0x6080000020c0 is located 32 bytes inside of 96-byte region [0x6080000020a0,0x608000002100)
freed by thread T0 here:
    #0 0x4ef30b in operator delete(void*) (/usr/local/google/tsepez/master/pdfium/out/Asan/pdfium_test+0x4ef30b)
    #1 0x1e7dacb in CPDFSDK_PageView::DeleteAnnot(CPDFSDK_Annot*) fpdfsdk/cpdfsdk_pageview.cpp:202:20
    #2 0x2391e6f in Document::removeField(IJS_Context*, std::__1::vector<CJS_Value, std::__1::allocator<CJS_Value> > const&, CJS_Value&, CFX_WideString&) fpdfsdk/javascript/Document.cpp:531:18
    #3 0x23b5fa0 in void JSMethod<Document, &Document::removeField>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) fpdfsdk/javascript/JS_Define.h:153:8
    #4 0x510fce in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:19:3
    #5 0x65d9c6 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:106:36
    #6 0x65af8e in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:135:5
    #7 0x7f022c1043a6  (<unknown module>)
    #8 0x7f022c205f79  (<unknown module>)
    #9 0x7f022c172302  (<unknown module>)
    #10 0x7f022c136e20  (<unknown module>)
    #11 0xff7a3b in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>) v8/src/execution.cc:139:13
    #12 0xff7262 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:176:10
    #13 0x141ebce in SetPropertyWithDefinedSetter v8/src/objects.cc:1519:3
    #14 0x141ebce in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::internal::Object::ShouldThrow) v8/src/objects.cc:1479
    #15 0x14575b8 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed, bool*) v8/src/objects.cc:4718:16
    #16 0x14566a0 in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed) v8/src/objects.cc:4750:9
    #17 0x53539d in SetElement v8/src/objects-inl.h:1131:3
    #18 0x53539d in v8::Object::Set(v8::Local<v8::Context>, unsigned int, v8::Local<v8::Value>) v8/src/api.cc:3981
    #19 0x243de70 in CFXJS_Engine::PutArrayElement(v8::Local<v8::Array>, unsigned int, v8::Local<v8::Value>) fxjs/fxjs_v8.cpp:682:15
    #20 0x23c9509 in Field::page(IJS_Context*, CJS_PropValue&, CFX_WideString&) fpdfsdk/javascript/Field.cpp:1832:15
    #21 0x23e2bcd in void JSPropGetter<Field, &Field::page>(char const*, char const*, v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) fpdfsdk/javascript/JS_Define.h:88:8
    #22 0x126a5f7 in v8::internal::PropertyCallbackArguments::Call(void (*)(v8::Local<v8::Name>, v8::PropertyCallbackInfo<v8::Value> const&), v8::internal::Handle<v8::internal::Name>) v8/src/api-arguments-inl.h:32:1
    #23 0x1416d95 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator*) v8/src/objects.cc:1353:34
    #24 0x141488a in v8::internal::Object::GetProperty(v8::internal::LookupIterator*) v8/src/objects.cc:999:16
    #25 0x122987c in v8::internal::LoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>) v8/src/ic/ic.cc:644:5
    #26 0x124887d in __RT_impl_Runtime_LoadIC_Miss v8/src/ic/ic.cc:2623:5
    #27 0x124887d in v8::internal::Runtime_LoadIC_Miss(int, v8::internal::Object**, v8::internal::Isolate*) v8/src/ic/ic.cc:2606
    #28 0x7f022c1043a6  (<unknown module>)
    #29 0x7f022c1847ec  (<unknown module>)
    #30 0x7f022c172c37  (<unknown module>)
    #31 0x7f022c205dc0  (<unknown module>)
    #32 0x7f022c172302  (<unknown module>)

previously allocated by thread T0 here:
    #0 0x4ee6cb in operator new(unsigned long) (/usr/local/google/tsepez/master/pdfium/out/Asan/pdfium_test+0x4ee6cb)
    #1 0x1eaca5f in CPDFSDK_WidgetHandler::NewAnnot(CPDF_Annot*, CPDFSDK_PageView*) fpdfsdk/cpdfsdk_widgethandler.cpp:63:29
    #2 0x1e80029 in CPDFSDK_PageView::LoadFXAnnots() fpdfsdk/cpdfsdk_pageview.cpp:436:47
    #3 0x1e723fc in CPDFSDK_FormFillEnvironment::GetPageView(CPDFXFA_Page*, bool) fpdfsdk/cpdfsdk_formfillenvironment.cpp:586:14
    #4 0x1e65be7 in FormHandleToPageView fpdfsdk/fpdfformfill.cpp:58:39
    #5 0x1e65be7 in FORM_OnAfterLoadPage fpdfsdk/fpdfformfill.cpp:658
    #6 0x4f7935 in GetPageForIndex(_FPDF_FORMFILLINFO*, void*, int) samples/pdfium_test.cc:623:3
    #7 0x1e72a7a in GetPage fpdfsdk/cpdfsdk_formfillenvironment.cpp:307:12
    #8 0x1e72a7a in CPDFSDK_FormFillEnvironment::GetPageView(int) fpdfsdk/cpdfsdk_formfillenvironment.cpp:598
    #9 0x1e74b6c in CPDFSDK_InterForm::GetWidget(CPDF_FormControl*) const fpdfsdk/cpdfsdk_interform.cpp:109:31
    #10 0x1e7507a in CPDFSDK_InterForm::GetWidgets(CPDF_FormField*, std::__1::vector<CPDFSDK_Widget*, std::__1::allocator<CPDFSDK_Widget*> >*) const fpdfsdk/cpdfsdk_interform.cpp:134:31
    #11 0x23c9399 in Field::page(IJS_Context*, CJS_PropValue&, CFX_WideString&) fpdfsdk/javascript/Field.cpp:1818:35
    #12 0x23e2bcd in void JSPropGetter<Field, &Field::page>(char const*, char const*, v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) fpdfsdk/javascript/JS_Define.h:88:8
    #13 0x126a5f7 in v8::internal::PropertyCallbackArguments::Call(void (*)(v8::Local<v8::Name>, v8::PropertyCallbackInfo<v8::Value> const&), v8::internal::Handle<v8::internal::Name>) v8/src/api-arguments-inl.h:32:1
    #14 0x1416d95 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator*) v8/src/objects.cc:1353:34
    #15 0x141488a in v8::internal::Object::GetProperty(v8::internal::LookupIterator*) v8/src/objects.cc:999:16
    #16 0x122987c in v8::internal::LoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>) v8/src/ic/ic.cc:644:5
    #17 0x124887d in __RT_impl_Runtime_LoadIC_Miss v8/src/ic/ic.cc:2623:5
    #18 0x124887d in v8::internal::Runtime_LoadIC_Miss(int, v8::internal::Object**, v8::internal::Isolate*) v8/src/ic/ic.cc:2606
    #19 0x7f022c1043a6  (<unknown module>)
    #20 0x7f022c1847ec  (<unknown module>)
    #21 0x7f022c172c37  (<unknown module>)
    #22 0x7f022c205dc0  (<unknown module>)
    #23 0x7f022c172302  (<unknown module>)
    #24 0x7f022c136e20  (<unknown module>)
    #25 0xff7a3b in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>) v8/src/execution.cc:139:13
    #26 0xff7262 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:176:10
    #27 0x527c71 in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:1946:7
    #28 0x243c2cc in CFXJS_Engine::Execute(CFX_WideString const&, FXJSErr*) fxjs/fxjs_v8.cpp:469:25
    #29 0x23665dc in CJS_Runtime::ExecuteScript(CFX_WideString const&, CFX_WideString*) fpdfsdk/javascript/cjs_runtime.cpp:206:14
    #30 0x2436e54 in CJS_Context::RunScript(CFX_WideString const&, CFX_WideString*) fpdfsdk/javascript/cjs_context.cpp:48:24
    #31 0x1e6a14a in RunDocumentOpenJavaScript fpdfsdk/fsdk_actionhandler.cpp:537:25
    #32 0x1e6a14a in CPDFSDK_ActionHandler::ExecuteDocumentOpenAction(CPDF_Action const&, CPDFSDK_FormFillEnvironment*, std::__1::set<CPDF_Dictionary*, std::__1::less<CPDF_Dictionary*>, std::__1::allocator<CPDF_Dictionary*> >*) fpdfsdk/fsdk_actionhandler.cpp:128
    #33 0x1e69d17 in CPDFSDK_ActionHandler::DoAction_DocOpen(CPDF_Action const&, CPDFSDK_FormFillEnvironment*) fpdfsdk/fsdk_actionha

### ts...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2017-01-11)

https://pdfium.googlesource.com/pdfium/+/8fa82794ffc2763e9fa1fc9d401c8e9a14d7c67f



### ts...@chromium.org (2017-01-11)

VRP: athough this instance was not in chromium's production code, it highlighted a few other places where this might have been possible.

### bu...@chromium.org (2017-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/631e11cb3b19a9641d1b9cb1d75c7cd065c76ee7

commit 631e11cb3b19a9641d1b9cb1d75c7cd065c76ee7
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Wed Jan 11 18:51:51 2017

Roll src/third_party/pdfium/ 76a44dea3..8fa82794f (1 commit).

https://pdfium.googlesource.com/pdfium.git/+log/76a44dea3180..8fa82794ffc2

$ git log 76a44dea3..8fa82794f --date=short --no-merges --format='%ad %ae %s'
2017-01-11 tsepez Annotation deleted while retrieving it in JS

BUG=679642

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2623263002
Cr-Commit-Position: refs/heads/master@{#442968}

[modify] https://crrev.com/631e11cb3b19a9641d1b9cb1d75c7cd065c76ee7/DEPS


### sh...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

Nice one! The VRP panel has decided to award $3,000 for this bug.  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-04-20)

This issue was migrated from crbug.com/chromium/679642?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086454)*
