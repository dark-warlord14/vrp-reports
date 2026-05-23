# Security: Use-after-free in CPDFSDK_PageView::DeleteAnnot (XFA)

| Field | Value |
|-------|-------|
| **Issue ID** | [40088160](https://issues.chromium.org/issues/40088160) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Mac |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2017-06-22 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36

Steps to reproduce the problem:
Pdfium with XFA enabled.
./pdfium_test ./poc.pdf

What is the expected behavior?

What went wrong?
This bug is related to: 732039 732051 732322

Document JS Action:
    this.getField("MyField").setFocus();
    // to let it be FocusAnnot

Closing Page 0 AAction:
    this.removeField("MyField");

"MyField" LoseFocus AAction:
    this.removeField("MyField");
    // to delete the annot while |DeleteAnnot| processing.

-------------------------------------------------------------------------------------

At |CPDFSDK_PageView::DeleteAnnot|
(
https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/cpdfsdk_pageview.cpp?sq=package:chromium&l=185
)

It's killing the focusing annot.

|CPDFSDK_FormFillEnvironment::KillFocusAnnot| ->|Annot_OnKillFocus| which ends up at |CFFL_InteractiveFormFiller::OnKillFocus| (https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp?sq=package:chromium&l=449)

which calling |AAction::LoseFocus|

Notice 451th line, it returns |false| if pAnnot was killed while getting in AAction. It seems okay, but... later when the program returns back to |CPDFSDK_PageView::DeleteAnnot|

https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/cpdfsdk_pageview.cpp?sq=package:chromium&l=186

--> Root cause = there is no checking whether pAnnot is still alive or not after calling |KillFocusAnnot(0)|

then it calls |pAnnotHandler->ReleaseAnnot(pAnnot)| with |pAnnot| as parameter which is already been freed before.

At 
https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/cpdfsdk_annothandlermgr.cpp?sq=package:chromium&l=61

it's looking for handler like vtable) for this annot (BAnnot or Widget), so it's possible to let attacker control instruction pointer.

Did this work before? N/A 

Chrome version: 58.0.3029.110  Channel: n/a
OS Version: OS X 10.12.5
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [poc.in](attachments/poc.in) (application/octet-stream, 1.5 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 2.4 KB)
- [asan](attachments/asan) (text/plain, 17.7 KB)

## Timeline

### ma...@gmail.com (2017-06-22)

I attached wrong files.

Please download poc/asan here.

### el...@chromium.org (2017-06-22)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ds...@chromium.org (2017-06-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-06-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5515968527990784.

### ts...@chromium.org (2017-06-22)

Dan, Lei, these keep showing up as (xfa-only) not because of some xfa-specific thing, but some ifdef'd code to allow deletion when xfa is present.  Maybe we should just never allow deletion, since the code doesn't appear to handle it properly?

### ds...@chromium.org (2017-06-22)

We're going to be supporting regular annotation deletion, I'm not sure how that will end up when we turn on XFA. (It has been requested to have annotation deletion as an API call)

### cl...@chromium.org (2017-06-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4958676254457856.

### mm...@chromium.org (2017-06-22)

I've managed to reproduce it locally with the following build flags:

is_debug = false
pdf_enable_xfa = true
is_asan = true
enable_nacl = false
proprietary_codecs = true
ffmpeg_branding = "ChromeOS"


$ src/out/asan/pdfium_test ./poc.pdf 
Rendering PDF file ./poc.pdf.
LoadXFA unsuccessful, continuing anyway.
=================================================================
==72596==ERROR: AddressSanitizer: heap-use-after-free on address 0x608000002620 at pc 0x000001f81001 bp 0x7ffca3541050 sp 0x7ffca3541048
READ of size 8 at 0x608000002620 thread T0
    #0 0x1f81000 in GetAnnotHandler third_party/pdfium/fpdfsdk/cpdfsdk_annothandlermgr.cpp:86:34
    #1 0x1f81000 in CPDFSDK_AnnotHandlerMgr::ReleaseAnnot(CPDFSDK_Annot*) third_party/pdfium/fpdfsdk/cpdfsdk_annothandlermgr.cpp:61
    #2 0x1f5be33 in CPDFSDK_PageView::DeleteAnnot(CPDFSDK_Annot*) third_party/pdfium/fpdfsdk/cpdfsdk_pageview.cpp:188:20
    #3 0x35ab95e in Document::removeField(CJS_Runtime*, std::__1::vector<CJS_Value, std::__1::allocator<CJS_Value> > const&, CJS_Value&, CFX_WideString&) third_party/pdfium/fpdfsdk/javascript/Document.cpp:511:18
    #4 0x35d08ce in void JSMethod<Document, &Document::removeField>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) third_party/pdfium/fpdfsdk/javascript/JS_Define.h:123:8
    #5 0x57e53d in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:25:3
    #6 0x70bca7 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:112:36
    #7 0x709627 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:142:5
    #8 0x7f902988463c  (<unknown module>)
    #9 0x7f9029970d7b  (<unknown module>)
    #10 0x7f902993c90d  (<unknown module>)
    #11 0x7f902993b398  (<unknown module>)
    #12 0x7f902988410c  (<unknown module>)
    #13 0xf8747d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling) v8/src/execution.cc:145:13
    #14 0xf86c82 in CallInternal v8/src/execution.cc:181:10
    #15 0xf86c82 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:191
    #16 0x5952f9 in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:2060:7
    #17 0x3650d5e in CFXJS_Engine::Execute(CFX_WideString const&, FXJSErr*) third_party/pdfium/fxjs/fxjs_v8.cpp:473:25
    #18 0x357c730 in CJS_Runtime::ExecuteScript(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_runtime.cpp:199:14
    #19 0x364afca in CJS_EventContext::RunScript(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_event_context.cpp:52:24
    #20 0x1f490e1 in CPDFSDK_ActionHandler::RunDocumentPageJavaScript(CPDFSDK_FormFillEnvironment*, CPDF_AAction::AActionType, CFX_WideString const&) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:576:25
    #21 0x1f47dba in CPDFSDK_ActionHandler::ExecuteDocumentPageAction(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, std::__1::set<CPDF_Dictionary*, std::__1::less<CPDF_Dictionary*>, std::__1::allocator<CPDF_Dictionary*> >*) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:202:9
    #22 0x1f47890 in CPDFSDK_ActionHandler::DoAction_Page(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:68:10
    #23 0x1f42114 in FORM_DoPageAAction third_party/pdfium/fpdfsdk/fpdfformfill.cpp:744:21
    #24 0x4ff090 in RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, void*, void*, FPDF_FORMFILLINFO_PDFiumTest&, int, Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) third_party/pdfium/samples/pdfium_test.cc:1009:3
    #25 0x5000a2 in RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) third_party/pdfium/samples/pdfium_test.cc:1170:9
    #26 0x501866 in main third_party/pdfium/samples/pdfium_test.cc:1311:5
    #27 0x7f9055646f44 in __libc_start_main /build/eglibc-MjiXCM/eglibc-2.19/csu/libc-start.c:287

0x608000002620 is located 0 bytes inside of 88-byte region [0x608000002620,0x608000002678)
freed by thread T0 here:
    #0 0x4f0502 in operator delete(void*) (/usr/local/google/home/mmoroz/Projects/new/chromium/src/out/asan/pdfium_test+0x4f0502)
    #1 0x1f5be33 in CPDFSDK_PageView::DeleteAnnot(CPDFSDK_Annot*) third_party/pdfium/fpdfsdk/cpdfsdk_pageview.cpp:188:20
    #2 0x35ab95e in Document::removeField(CJS_Runtime*, std::__1::vector<CJS_Value, std::__1::allocator<CJS_Value> > const&, CJS_Value&, CFX_WideString&) third_party/pdfium/fpdfsdk/javascript/Document.cpp:511:18
    #3 0x35d08ce in void JSMethod<Document, &Document::removeField>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) third_party/pdfium/fpdfsdk/javascript/JS_Define.h:123:8
    #4 0x57e53d in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:25:3
    #5 0x70bca7 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:112:36
    #6 0x709627 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:142:5
    #7 0x7f902988463c  (<unknown module>)
    #8 0x7f9029970d7b  (<unknown module>)
    #9 0x7f902993c90d  (<unknown module>)
    #10 0x7f902993b398  (<unknown module>)
    #11 0x7f902988410c  (<unknown module>)
    #12 0xf8747d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling) v8/src/execution.cc:145:13
    #13 0xf86c82 in CallInternal v8/src/execution.cc:181:10
    #14 0xf86c82 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:191
    #15 0x5952f9 in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:2060:7
    #16 0x3650d5e in CFXJS_Engine::Execute(CFX_WideString const&, FXJSErr*) third_party/pdfium/fxjs/fxjs_v8.cpp:473:25
    #17 0x357c730 in CJS_Runtime::ExecuteScript(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_runtime.cpp:199:14
    #18 0x364afca in CJS_EventContext::RunScript(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_event_context.cpp:52:24
    #19 0x1f474fe in CPDFSDK_ActionHandler::RunFieldJavaScript(CPDFSDK_FormFillEnvironment*, CPDF_FormField*, CPDF_AAction::AActionType, PDFSDK_FieldAction&, CFX_WideString const&) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:513:25
    #20 0x1f487c2 in CPDFSDK_ActionHandler::ExecuteFieldAction(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, CPDF_FormField*, PDFSDK_FieldAction&, std::__1::set<CPDF_Dictionary*, std::__1::less<CPDF_Dictionary*>, std::__1::allocator<CPDF_Dictionary*> >*) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:249:9
    #21 0x1f48287 in CPDFSDK_ActionHandler::DoAction_Field(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, CPDF_FormField*, PDFSDK_FieldAction&) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:111:10
    #22 0x1f798d6 in CPDFSDK_Widget::OnAAction(CPDF_AAction::AActionType, PDFSDK_FieldAction&, CPDFSDK_PageView*) third_party/pdfium/fpdfsdk/cpdfsdk_widget.cpp:1869:28
    #23 0x2e6b480 in CFFL_InteractiveFormFiller::OnKillFocus(CFX_Observable<CPDFSDK_Annot>::ObservedPtr*, unsigned int) third_party/pdfium/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:449:12
    #24 0x1f4f558 in CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int) third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:732:23
    #25 0x1f5be09 in CPDFSDK_PageView::DeleteAnnot(CPDFSDK_Annot*) third_party/pdfium/fpdfsdk/cpdfsdk_pageview.cpp:185:21
    #26 0x35ab95e in Document::removeField(CJS_Runtime*, std::__1::vector<CJS_Value, std::__1::allocator<CJS_Value> > const&, CJS_Value&, CFX_WideString&) third_party/pdfium/fpdfsdk/javascript/Document.cpp:511:18
    #27 0x35d08ce in void JSMethod<Document, &Document::removeField>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) third_party/pdfium/fpdfsdk/javascript/JS_Define.h:123:8
    #28 0x57e53d in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:25:3
    #29 0x70bca7 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:112:36
    #30 0x709627 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:142:5

previously allocated by thread T0 here:
    #0 0x4ef902 in operator new(unsigned long) (/usr/local/google/home/mmoroz/Projects/new/chromium/src/out/asan/pdfium_test+0x4ef902)
    #1 0x1f90cef in CPDFSDK_WidgetHandler::NewAnnot(CPDF_Annot*, CPDFSDK_PageView*) third_party/pdfium/fpdfsdk/cpdfsdk_widgethandler.cpp:62:29
    #2 0x1f5f124 in CPDFSDK_PageView::LoadFXAnnots() third_party/pdfium/fpdfsdk/cpdfsdk_pageview.cpp:428:47
    #3 0x1f4ff5a in CPDFSDK_FormFillEnvironment::GetPageView(CPDFXFA_Page*, bool) third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:581:14
    #4 0x1f41bb7 in FormHandleToPageView third_party/pdfium/fpdfsdk/fpdfformfill.cpp:65:39
    #5 0x1f41bb7 in FORM_OnAfterLoadPage third_party/pdfium/fpdfsdk/fpdfformfill.cpp:661
    #6 0x4fca65 in GetPageForIndex(_FPDF_FORMFILLINFO*, void*, int) third_party/pdfium/samples/pdfium_test.cc:846:3
    #7 0x1f5012a in GetPage third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:307:12
    #8 0x1f5012a in CPDFSDK_FormFillEnvironment::GetPageView(int) third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:593
    #9 0x1f52647 in CPDFSDK_InterForm::GetWidget(CPDF_FormControl*) const third_party/pdfium/fpdfsdk/cpdfsdk_interform.cpp:110:31
    #10 0x35eef89 in Field::setFocus(CJS_Runtime*, std::__1::vector<CJS_Value, std::__1::allocator<CJS_Value> > const&, CJS_Value&, CFX_WideString&) third_party/pdfium/fpdfsdk/javascript/Field.cpp:3104:27
    #11 0x360bbee in void JSMethod<Field, &Field::setFocus>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) third_party/pdfium/fpdfsdk/javascript/JS_Define.h:123:8
    #12 0x57e53d in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:25:3
    #13 0x70bca7 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:112:36
    #14 0x709627 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:142:5
    #15 0x7f902988463c  (<unknown module>)
    #16 0x7f9029970c48  (<unknown module>)
    #17 0x7f902993c90d  (<unknown module>)
    #18 0x7f902993b398  (<unknown module>)
    #19 0x7f902988410c  (<unknown module>)
    #20 0xf8747d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling) v8/src/execution.cc:145:13
    #21 0xf86c82 in CallInternal v8/src/execution.cc:181:10
    #22 0xf86c82 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:191
    #23 0x5952f9 in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:2060:7
    #24 0x3650d5e in CFXJS_Engine::Execute(CFX_WideString const&, FXJSErr*) third_party/pdfium/fxjs/fxjs_v8.cpp:473:25
    #25 0x357c730 in CJS_Runtime::ExecuteScript(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_runtime.cpp:199:14
    #26 0x364afca in CJS_EventContext::RunScript(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_event_context.cpp:52:24
    #27 0x1f4672a in RunDocumentOpenJavaScript third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:529:25
    #28 0x1f4672a in CPDFSDK_ActionHandler::ExecuteDocumentOpenAction(CPDF_Action const&, CPDFSDK_FormFillEnvironment*, std::__1::set<CPDF_Dictionary*, std::__1::less<CPDF_Dictionary*>, std::__1::allocator<CPDF_Dictionary*> >*) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:130
    #29 0x1f4610c in CPDFSDK_ActionHandler::DoAction_DocOpen(CPDF_Action const&, CPDFSDK_FormFillEnvironment*) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:27:10
    #30 0x1f5099f in CPDFSDK_FormFillEnvironment::ProcOpenAction() third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:635:23
    #31 0x1f41d03 in FORM_DoDocumentOpenAction third_party/pdfium/fpdfsdk/fpdfformfill.cpp:695:19
    #32 0x4fffcf in RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) third_party/pdfium/samples/pdfium_test.cc:1144:3
    #33 0x501866 in main third_party/pdfium/samples/pdfium_test.cc:1311:5

SUMMARY: AddressSanitizer: heap-use-after-free third_party/pdfium/fpdfsdk/cpdfsdk_annothandlermgr.cpp:86:34 in GetAnnotHandler
Shadow bytes around the buggy address:
  0x0c107fff8470: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c107fff8480: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c107fff8490: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c107fff84a0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c107fff84b0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
=>0x0c107fff84c0: fa fa fa fa[fd]fd fd fd fd fd fd fd fd fd fd fa
  0x0c107fff84d0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c107fff84e0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c107fff84f0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c107fff8500: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c107fff8510: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
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
==72596==ABORTING


### mm...@chromium.org (2017-06-22)

Setting Security_Impact-None since XFA is disabled by default.

### ma...@gmail.com (2017-06-23)

Cool, btw Would you mind reapplying Severity for these one ?
https://bugs.chromium.org/p/chromium/issues/detail?id=732039
https://bugs.chromium.org/p/chromium/issues/detail?id=732322

as we discussed at https://bugs.chromium.org/p/chromium/issues/detail?id=732051#c20


### ds...@chromium.org (2017-06-26)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-07-20)

I'll take a shot at this in the absence of thestig.

### ts...@chromium.org (2017-07-20)

Repros locally as of 77417ec9e1 this morning.  Not sure why CF didn't see it.

### ts...@chromium.org (2017-07-20)

CL at https://pdfium-review.googlesource.com/c/8510

### ma...@gmail.com (2017-07-20)

Great! The patch seems fine, since observeptr is used.

Would you mind taking a look at
https://bugs.chromium.org/p/chromium/issues/detail?id=732039
and
https://bugs.chromium.org/p/chromium/issues/detail?id=732322

As me and awhalley discussed at https://bugs.chromium.org/p/chromium/issues/detail?id=732051#c20

Those are should be reapplied Serverity flags, shouldn't ?

Thank you.

### ts...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-08-02)

tsepez: Thanks for taking care of this one.

### aw...@chromium.org (2017-08-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-28)

Congratulations! The VRP panel decided to award $3,000 for this report. Thank you.

### aw...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-10-31)

This issue was migrated from crbug.com/chromium/735912?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088160)*
