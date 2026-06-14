# Security: Use-after-free in CPDFSDK_ActionHandler::ExecuteFieldAction

| Field | Value |
|-------|-------|
| **Issue ID** | [40095708](https://issues.chromium.org/issues/40095708) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ba...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-07-14 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Javascript code for validate is stored in dictionary key '/V'.  

And the value of (text) field is stored in dictionary key '/V'.  

By overlapping both dictionary key and remove '/V' key during validate event, can cause dangling CPDF\_Dictionary pointer.

Attached file is minimized PoC file. I used setFocus method to generate validate event and resetForm method to remove dictionary key '/V'.

**VERSION**  

Chrome Version: Mozilla/5.0 (X11; Linux x86\_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3853.0 Safari/537.36  

PDFium: Commit ac011992a88667d2347892e60fe38bf6dde1a056  

Operating System: All

**REPRODUCTION CASE**

1. Build pdfium\_test or chromium with ASAN
2. Load the attached poc pdf file
3. Crash occured

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: PDF plugin process  

Crash State: Address Sanitizer output

==55153==ERROR: AddressSanitizer: heap-use-after-free on address 0x606000000f50 at pc 0x562ce2eed32f bp 0x7ffcb83dbac0 sp 0x7ffcb83dbab8  

READ of size 8 at 0x606000000f50 thread T0  

#0 0x562ce2eed32e in \_\_root buildtools/third\_party/libc++/trunk/include/\_\_tree:1082:59  

#1 0x562ce2eed32e in find[fxcrt::ByteString](javascript:void(0);) buildtools/third\_party/libc++/trunk/include/\_\_tree:2616  

#2 0x562ce2eed32e in find buildtools/third\_party/libc++/trunk/include/map:1380  

#3 0x562ce2eed32e in ContainsKey<std::\_\_1::map<fxcrt::ByteString, fxcrt::RetainPtr<CPDF\_Object>, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), std::\_\_1::allocator<std::\_\_1::pair<const fxcrt::ByteString, fxcrt::RetainPtr<CPDF\_Object> > > >, fxcrt::ByteString> third\_party/base/stl\_util.h:35  

#4 0x562ce2eed32e in CPDF\_Dictionary::KeyExist(fxcrt::ByteString const&) const core/fpdfapi/parser/cpdf\_dictionary.cpp:196  

#5 0x562ce303c5df in CPDF\_Action::GetSubActionsCount() const core/fpdfdoc/cpdf\_action.cpp:128:29  

#6 0x562ce2a90dc1 in CPDFSDK\_ActionHandler::ExecuteFieldAction(CPDF\_Action const&, CPDF\_AAction::AActionType, CPDFSDK\_FormFillEnvironment\*, CPDF\_FormField\*, CPDFSDK\_FieldAction\*, std::\_\_1::set<CPDF\_Dictionary const\*, std::\_\_1::less<CPDF\_Dictionary const\*>, std::\_\_1::allocator<CPDF\_Dictionary const\*> >\*) fpdfsdk/cpdfsdk\_actionhandler.cpp:246:35  

#7 0x562ce2a90818 in CPDFSDK\_ActionHandler::DoAction\_Field(CPDF\_Action const&, CPDF\_AAction::AActionType, CPDFSDK\_FormFillEnvironment\*, CPDF\_FormField\*, CPDFSDK\_FieldAction\*) fpdfsdk/cpdfsdk\_actionhandler.cpp:111:10  

#8 0x562ce2ac313d in CPDFSDK\_Widget::OnAAction(CPDF\_AAction::AActionType, CPDFSDK\_FieldAction\*, CPDFSDK\_PageView\*) fpdfsdk/cpdfsdk\_widget.cpp:845:39  

#9 0x562ce50047a6 in CFFL\_InteractiveFormFiller::OnValidate(fxcrt::ObservedPtr<CPDFSDK\_Annot>\*, CPDFSDK\_PageView\*, unsigned int) fpdfsdk/formfiller/cffl\_interactiveformfiller.cpp:702:12  

#10 0x562ce4ffb068 in CFFL\_FormFiller::CommitData(CPDFSDK\_PageView\*, unsigned int) fpdfsdk/formfiller/cffl\_formfiller.cpp:516:21  

#11 0x562ce4ffa96a in CFFL\_FormFiller::KillFocusForAnnot(unsigned int) fpdfsdk/formfiller/cffl\_formfiller.cpp:302:22  

#12 0x562ce5002e2e in CFFL\_InteractiveFormFiller::OnKillFocus(fxcrt::ObservedPtr<CPDFSDK\_Annot>\*, unsigned int) fpdfsdk/formfiller/cffl\_interactiveformfiller.cpp:436:16  

#13 0x562ce2aac4cc in CPDFSDK\_FormFillEnvironment::KillFocusAnnot(unsigned int) fpdfsdk/cpdfsdk\_formfillenvironment.cpp:696:23  

#14 0x562ce2aadcf5 in CPDFSDK\_FormFillEnvironment::SetFocusAnnot(fxcrt::ObservedPtr<CPDFSDK\_Annot>\*) fpdfsdk/cpdfsdk\_formfillenvironment.cpp:655:25  

#15 0x562ce3147f5c in CJS\_Field::setFocus(CJS\_Runtime\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/cjs\_field.cpp:2530:21  

#16 0x562ce31648a7 in void JSMethod<CJS\_Field, &CJS\_Field::setFocus>(char const\*, char const\*, v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/js\_define.h:128:23  

#17 0x562ce32d5378 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#18 0x562ce32d3067 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36  

#19 0x562ce32d0f54 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:141:5  

#20 0x562ce4f64e18 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x337be18)  

#21 0x562ce4ee61c3 in Builtins\_InterpreterEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x32fd1c3)  

#22 0x562ce4ee3a9c in Builtins\_JSEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x32faa9c)  

#23 0x562ce4ee3877 in Builtins\_JSEntry (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x32fa877)  

#24 0x562ce3548159 in Call v8/src/execution/simulator.h:138:12  

#25 0x562ce3548159 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:265  

#26 0x562ce3547595 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:357:10  

#27 0x562ce31bc617 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api/api.cc:2137:7  

#28 0x562ce30c414b in CFXJS\_Engine::Execute(fxcrt::WideString const&) fxjs/cfxjs\_engine.cpp:571:25  

#29 0x562ce3191731 in CJS\_Runtime::ExecuteScript(fxcrt::WideString const&) fxjs/cjs\_runtime.cpp:168:10  

#30 0x562ce312524c in CJS\_EventContext::RunScript(fxcrt::WideString const&) fxjs/cjs\_event\_context.cpp:54:23  

#31 0x562ce2a8f710 in RunScript fpdfsdk/cpdfsdk\_actionhandler.cpp:552:13  

#32 0x562ce2a8f710 in CPDFSDK\_ActionHandler::RunDocumentOpenJavaScript(CPDFSDK\_FormFillEnvironment\*, fxcrt::WideString const&, fxcrt::WideString const&) fpdfsdk/cpdfsdk\_actionhandler.cpp:461  

#33 0x562ce2a8f152 in CPDFSDK\_ActionHandler::ExecuteDocumentOpenAction(CPDF\_Action const&, CPDFSDK\_FormFillEnvironment\*, std::\_\_1::set<CPDF\_Dictionary const\*, std::\_\_1::less<CPDF\_Dictionary const\*>, std::\_\_1::allocator<CPDF\_Dictionary const\*> >\*) fpdfsdk/cpdfsdk\_actionhandler.cpp:130:9  

#34 0x562ce2a8ec21 in CPDFSDK\_ActionHandler::DoAction\_DocOpen(CPDF\_Action const&, CPDFSDK\_FormFillEnvironment\*) fpdfsdk/cpdfsdk\_actionhandler.cpp:26:10  

#35 0x562ce2aad76d in CPDFSDK\_FormFillEnvironment::ProcOpenAction() fpdfsdk/cpdfsdk\_formfillenvironment.cpp:597:23  

#36 0x562ce2a7ccc5 in RenderPdf samples/pdfium\_test.cc:850:3  

#37 0x562ce2a7ccc5 in main samples/pdfium\_test.cc:1068  

#38 0x7fc7b7f2682f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

0x606000000f50 is located 48 bytes inside of 64-byte region [0x606000000f20,0x606000000f60)  

freed by thread T0 here:  

#0 0x562ce2a75bbd in operator delete(void\*) /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:160:3  

#1 0x562ce3050648 in Release core/fxcrt/retain\_ptr.h:122:7  

#2 0x562ce3050648 in operator() core/fxcrt/retain\_ptr.h:20  

#3 0x562ce3050648 in reset buildtools/third\_party/libc++/trunk/include/memory:2651  

#4 0x562ce3050648 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/memory:2605  

#5 0x562ce3050648 in ~RetainPtr core/fxcrt/retain\_ptr.h:25  

#6 0x562ce3050648 in CPDF\_FormField::ResetField(NotificationOption) core/fpdfdoc/cpdf\_formfield.cpp:249  

#7 0x562ce305d90c in CPDF\_InteractiveForm::ResetForm(NotificationOption) core/fpdfdoc/cpdf\_interactiveform.cpp:829:13  

#8 0x562ce30efd6e in CJS\_Document::resetForm(CJS\_Runtime\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/cjs\_document.cpp:586:15  

#9 0x562ce31169bc in void JSMethod<CJS\_Document, &CJS\_Document::resetForm>(char const\*, char const\*, v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/js\_define.h:128:23  

#10 0x562ce32d5378 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#11 0x562ce32d3067 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36  

#12 0x562ce32d0f54 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:141:5  

#13 0x562ce4f64e18 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x337be18)  

#14 0x562ce4ee61c3 in Builtins\_InterpreterEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x32fd1c3)  

#15 0x562ce4ee3a9c in Builtins\_JSEntryTrampoline (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x32faa9c)  

#16 0x562ce4ee3877 in Builtins\_JSEntry (/home/bananana/pdfium\_latest/pdfium/out/release\_asan/pdfium\_test+0x32fa877)  

#17 0x562ce3548159 in Call v8/src/execution/simulator.h:138:12  

#18 0x562ce3548159 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:265  

#19 0x562ce3547595 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:357:10  

#20 0x562ce31bc617 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api/api.cc:2137:7  

#21 0x562ce30c414b in CFXJS\_Engine::Execute(fxcrt::WideString const&) fxjs/cfxjs\_engine.cpp:571:25  

#22 0x562ce3191731 in CJS\_Runtime::ExecuteScript(fxcrt::WideString const&) fxjs/cjs\_runtime.cpp:168:10  

#23 0x562ce312524c in CJS\_EventContext::RunScript(fxcrt::WideString const&) fxjs/cjs\_event\_context.cpp:54:23  

#24 0x562ce2a8fc3d in RunScript fpdfsdk/cpdfsdk\_actionhandler.cpp:552:13  

#25 0x562ce2a8fc3d in CPDFSDK\_ActionHandler::RunFieldJavaScript(CPDFSDK\_FormFillEnvironment\*, CPDF\_FormField\*, CPDF\_AAction::AActionType, CPDFSDK\_FieldAction\*, fxcrt::WideString const&) fpdfsdk/cpdfsdk\_actionhandler.cpp:410  

#26 0x562ce2a90d3a in CPDFSDK\_ActionHandler::ExecuteFieldAction(CPDF\_Action const&, CPDF\_AAction::AActionType, CPDFSDK\_FormFillEnvironment\*, CPDF\_FormField\*, CPDFSDK\_FieldAction\*, std::\_\_1::set<CPDF\_Dictionary const\*, std::\_\_1::less<CPDF\_Dictionary const\*>, std::\_\_1::allocator<CPDF\_Dictionary const\*> >\*) fpdfsdk/cpdfsdk\_actionhandler.cpp:237:9  

#27 0x562ce2a90818 in CPDFSDK\_ActionHandler::DoAction\_Field(CPDF\_Action const&, CPDF\_AAction::AActionType, CPDFSDK\_FormFillEnvironment\*, CPDF\_FormField\*, CPDFSDK\_FieldAction\*) fpdfsdk/cpdfsdk\_actionhandler.cpp:111:10  

#28 0x562ce2ac313d in CPDFSDK\_Widget::OnAAction(CPDF\_AAction::AActionType, CPDFSDK\_FieldAction\*, CPDFSDK\_PageView\*) fpdfsdk/cpdfsdk\_widget.cpp:845:39  

#29 0x562ce50047a6 in CFFL\_InteractiveFormFiller::OnValidate(fxcrt::ObservedPtr<CPDFSDK\_Annot>\*, CPDFSDK\_PageView\*, unsigned int) fpdfsdk/formfiller/cffl\_interactiveformfiller.cpp:702:12  

#30 0x562ce4ffb068 in CFFL\_FormFiller::CommitData(CPDFSDK\_PageView\*, unsigned int) fpdfsdk/formfiller/cffl\_formfiller.cpp:516:21  

#31 0x562ce4ffa96a in CFFL\_FormFiller::KillFocusForAnnot(unsigned int) fpdfsdk/formfiller/cffl\_formfiller.cpp:302:22  

#32 0x562ce5002e2e in CFFL\_InteractiveFormFiller::OnKillFocus(fxcrt::ObservedPtr<CPDFSDK\_Annot>\*, unsigned int) fpdfsdk/formfiller/cffl\_interactiveformfiller.cpp:436:16  

#33 0x562ce2aac4cc in CPDFSDK\_FormFillEnvironment::KillFocusAnnot(unsigned int) fpdfsdk/cpdfsdk\_formfillenvironment.cpp:696:23  

#34 0x562ce2aadcf5 in CPDFSDK\_FormFillEnvironment::SetFocusAnnot(fxcrt::ObservedPtr<CPDFSDK\_Annot>\*) fpdfsdk/cpdfsdk\_formfillenvironment.cpp:655:25  

#35 0x562ce3147f5c in CJS\_Field::setFocus(CJS\_Runtime\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/cjs\_field.cpp:2530:21  

#36 0x562ce31648a7 in void JSMethod<CJS\_Field, &CJS\_Field::setFocus>(char const\*, char const\*, v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/js\_define.h:128:23

previously allocated by thread T0 here:  

#0 0x562ce2a7535d in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:99:3  

#1 0x562ce2f37243 in MakeRetain<CPDF\_Dictionary, fxcrt::WeakPtr<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);), std::\_\_1::default\_delete<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);) > > &> core/fxcrt/retain\_ptr.h:142:23  

#2 0x562ce2f37243 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:485  

#3 0x562ce2f37587 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:507:11  

#4 0x562ce2f3a035 in CPDF\_SyntaxParser::GetIndirectObject(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:559:33  

#5 0x562ce2f1b412 in CPDF\_Parser::ParseIndirectObjectAt(long, unsigned int) core/fpdfapi/parser/cpdf\_parser.cpp:916:28  

#6 0x562ce2f1c014 in CPDF\_Parser::ParseIndirectObject(unsigned int) core/fpdfapi/parser/cpdf\_parser.cpp:865:12  

#7 0x562ce2ef122c in CPDF\_Document::ParseIndirectObject(unsigned int) core/fpdfapi/parser/cpdf\_document.cpp:76:33  

#8 0x562ce2efc3f2 in CPDF\_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) core/fpdfapi/parser/cpdf\_indirect\_object\_holder.cpp:50:36  

#9 0x562ce2ec6ea5 in GetDirectObjectAt core/fpdfapi/parser/cpdf\_array.cpp:105:24  

#10 0x562ce2ec6ea5 in CPDF\_Array::GetDictAt(unsigned long) core/fpdfapi/parser/cpdf\_array.cpp:139  

#11 0x562ce305b71d in CPDF\_InteractiveForm::CPDF\_InteractiveForm(CPDF\_Document\*) core/fpdfdoc/cpdf\_interactiveform.cpp:600:24  

#12 0x562ce2aafd34 in ReportUnsupportedFeatures(CPDF\_Document\*) fpdfsdk/cpdfsdk\_helpers.cpp:361:32  

#13 0x562ce2ad4ce4 in (anonymous namespace)::LoadDocumentImpl(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, char const\*) fpdfsdk/fpdf\_view.cpp:164:3  

#14 0x562ce2ad53b6 in FPDF\_LoadCustomDocument fpdfsdk/fpdf\_view.cpp:287:10  

#15 0x562ce2a7c93a in RenderPdf samples/pdfium\_test.cc:786:17  

#16 0x562ce2a7c93a in main samples/pdfium\_test.cc:1068  

#17 0x7fc7b7f2682f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third\_party/libc++/trunk/include/\_\_tree:1082:59 in \_\_root  

Shadow bytes around the buggy address:  

0x0c0c7fff8190: 00 00 00 00 00 00 00 00 fa fa fa fa fd fd fd fd  

0x0c0c7fff81a0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0c7fff81b0: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c0c7fff81c0: fd fd fd fd fd fd fd fd fa fa fa fa 00 00 00 00  

0x0c0c7fff81d0: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00  

=>0x0c0c7fff81e0: fa fa fa fa fd fd fd fd fd fd[fd]fd fa fa fa fa  

0x0c0c7fff81f0: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x0c0c7fff8200: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0c7fff8210: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c0c7fff8220: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x0c0c7fff8230: fd fd fd fd fa fa fa fa 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==55153==ABORTING

**CREDIT INFORMATION**  

Reporter credit: banananapenguin

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ba...@gmail.com (2019-07-14)

[Comment Deleted]

### ba...@gmail.com (2019-07-14)

Please note that it works with both XFA-enable/XFA-disabled

### ba...@gmail.com (2019-07-14)

Oops, I miswrote. In 'Javascript code for validate is stored in dictionary key '/V'.' , I meant 'Event action information for validate is ~~'. not javascript code

### ba...@gmail.com (2019-07-15)

Below comment note shows possible flow of remote code execution

bool CPDFSDK_ActionHandler::ExecuteFieldAction(
    const CPDF_Action& action,
    CPDF_AAction::AActionType type,
    CPDFSDK_FormFillEnvironment* pFormFillEnv,
    CPDF_FormField* pFormField,
    CPDFSDK_FieldAction* data,
    std::set<const CPDF_Dictionary*>* visited) {
  const CPDF_Dictionary* pDict = action.GetDict();
  if (pdfium::ContainsKey(*visited, pDict))
    return false;

  visited->insert(pDict);

  ASSERT(pFormFillEnv);
  if (action.GetType() == CPDF_Action::JavaScript) {
    if (pFormFillEnv->IsJSPlatformPresent()) {
      WideString swJS = action.GetJavaScript();
      if (!swJS.IsEmpty()) {
        RunFieldJavaScript(pFormFillEnv, pFormField, type, data, swJS);
        // Note (1) : action.m_pDict is now freed
        if (!IsValidField(pFormFillEnv, pFormField->GetFieldDict()))
          return false;
      }
    }
  } else {
    DoAction_NoJs(action, type, pFormFillEnv);
  }

  for (int32_t i = 0, sz = action.GetSubActionsCount(); i < sz; i++) { // Note (2) : (freed) action.m_pDict is used
    CPDF_Action subaction = action.GetSubAction(i);
    if (!ExecuteFieldAction(subaction, type, pFormFillEnv, pFormField, data,
                            visited))
      return false;
  }

  return true;
}

size_t CPDF_Action::GetSubActionsCount() const {
  if (!m_pDict || !m_pDict->KeyExist("Next"))
    return 0;

  const CPDF_Object* pNext = m_pDict->GetDirectObjectFor("Next"); // Note (3) : fake pNext pointer could be returned
  if (!pNext)
    return 0;
  if (pNext->IsDictionary()) // Note (4) : Virtual function, CPDF_Object::IsDictionary, is called. Control flow could be hijacked
    return 1;
  const CPDF_Array* pArray = pNext->AsArray();
  return pArray ? pArray->size() : 0;
}

### pa...@chromium.org (2019-07-15)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2019-07-15)

https://pdfium-review.googlesource.com/c/pdfium/+/57854

### pa...@chromium.org (2019-07-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@gmail.com (2019-07-17)

[Comment Deleted]

### ba...@gmail.com (2019-07-17)

[Comment Deleted]

### ba...@gmail.com (2019-07-17)

[Comment Deleted]

### ba...@gmail.com (2019-07-17)

[Comment Deleted]

### ba...@gmail.com (2019-07-17)

I've managed this bug works in pdfium of chrome for 75.0.3770.142, the latest stable release.
I used check/radio-button instead of text field to trigger free without getting orphaned, which was introduced in pdfium:1399a22912fa38b0d5af2532cd0b37b0b3951d50.
So I think security impact of this bug should be stable, instead of beta.
I used pdfium standlone with revision 6ce1d132489de5aa420cec9ef83818d5bad81c51 which is used to 75.0.3770.142. (https://chromium.googlesource.com/chromium/src/+/bcaef32a586391a3d5de7e40baa183946bddb10d/DEPS#153)
Tested chrome stable release on linux x64 + windows x64 and both were crashed. 

New PoC is attached and here is the asan log for attached new one.

==18076==ERROR: AddressSanitizer: heap-use-after-free on address 0x606000001908 at pc 0x55bbb47213cf bp 0x7ffd84819700 sp 0x7ffd848196f8
READ of size 8 at 0x606000001908 thread T0
    #0 0x55bbb47213ce in __root buildtools/third_party/libc++/trunk/include/__tree:1082:59
    #1 0x55bbb47213ce in find<fxcrt::ByteString> buildtools/third_party/libc++/trunk/include/__tree:2616
    #2 0x55bbb47213ce in find buildtools/third_party/libc++/trunk/include/map:1376
    #3 0x55bbb47213ce in ContainsKey<std::__1::map<fxcrt::ByteString, std::__1::unique_ptr<CPDF_Object, std::__1::default_delete<CPDF_Object> >, std::__1::less<fxcrt::ByteString>, std::__1::allocator<std::__1::pair<const fxcrt::ByteString, std::__1::unique_ptr<CPDF_Object, std::__1::default_delete<CPDF_Object> > > > >, fxcrt::ByteString> third_party/base/stl_util.h:35
    #4 0x55bbb47213ce in CPDF_Dictionary::KeyExist(fxcrt::ByteString const&) const core/fpdfapi/parser/cpdf_dictionary.cpp:196
    #5 0x55bbb4593f0f in CPDF_Action::GetSubActionsCount() const core/fpdfdoc/cpdf_action.cpp:125:29
    #6 0x55bbb49ff151 in CPDFSDK_ActionHandler::ExecuteFieldAction(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, CPDF_FormField*, CPDFSDK_FieldAction*, std::__1::set<CPDF_Dictionary const*, std::__1::less<CPDF_Dictionary const*>, std::__1::allocator<CPDF_Dictionary const*> >*) fpdfsdk/cpdfsdk_actionhandler.cpp:247:35
    #7 0x55bbb49feb98 in CPDFSDK_ActionHandler::DoAction_Field(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, CPDF_FormField*, CPDFSDK_FieldAction*) fpdfsdk/cpdfsdk_actionhandler.cpp:112:10
    #8 0x55bbb4a2c50d in CPDFSDK_Widget::OnAAction(CPDF_AAction::AActionType, CPDFSDK_FieldAction*, CPDFSDK_PageView*) fpdfsdk/cpdfsdk_widget.cpp:837:39
    #9 0x55bbb6871296 in CFFL_InteractiveFormFiller::OnValidate(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*, CPDFSDK_PageView*, unsigned int) fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:702:12
    #10 0x55bbb6867844 in CFFL_FormFiller::CommitData(CPDFSDK_PageView*, unsigned int) fpdfsdk/formfiller/cffl_formfiller.cpp:516:21
    #11 0x55bbb686714a in CFFL_FormFiller::KillFocusForAnnot(unsigned int) fpdfsdk/formfiller/cffl_formfiller.cpp:302:22
    #12 0x55bbb686f91e in CFFL_InteractiveFormFiller::OnKillFocus(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*, unsigned int) fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:436:16
    #13 0x55bbb4a18818 in CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int) fpdfsdk/cpdfsdk_formfillenvironment.cpp:695:23
    #14 0x55bbb4a1a035 in CPDFSDK_FormFillEnvironment::SetFocusAnnot(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*) fpdfsdk/cpdfsdk_formfillenvironment.cpp:654:25
    #15 0x55bbb4abf99c in CJS_Field::setFocus(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/cjs_field.cpp:2529:21
    #16 0x55bbb4adc2e7 in void JSMethod<CJS_Field, &CJS_Field::setFocus>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) fxjs/js_define.h:128:23
    #17 0x55bbb4c9419d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:157:3
    #18 0x55bbb4c91ec4 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #19 0x55bbb4c8fa54 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #20 0x55bbb67d5b18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit (/home/bananana/pdfium_latest/pdfium/out/stable_asan/pdfium_test+0x3226b18)
    #21 0x55bbb6748a03 in Builtins_InterpreterEntryTrampoline (/home/bananana/pdfium_latest/pdfium/out/stable_asan/pdfium_test+0x3199a03)
    #22 0x55bbb674637c in Builtins_JSEntryTrampoline (/home/bananana/pdfium_latest/pdfium/out/stable_asan/pdfium_test+0x319737c)
    #23 0x55bbb67460f7 in Builtins_JSEntry (/home/bananana/pdfium_latest/pdfium/out/stable_asan/pdfium_test+0x31970f7)
    #24 0x55bbb560b5b5 in Call v8/src/simulator.h:138:12
    #25 0x55bbb560b5b5 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:274
    #26 0x55bbb560ab35 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:366:10
    #27 0x55bbb4b3c5f6 in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:2174:7
    #28 0x55bbb4a3b33b in CFXJS_Engine::Execute(fxcrt::WideString const&) fxjs/cfxjs_engine.cpp:571:25
    #29 0x55bbb4b09801 in CJS_Runtime::ExecuteScript(fxcrt::WideString const&) fxjs/cjs_runtime.cpp:168:10
    #30 0x55bbb4a9cdbc in CJS_EventContext::RunScript(fxcrt::WideString const&) fxjs/cjs_event_context.cpp:53:23
    #31 0x55bbb49fda80 in RunScript fpdfsdk/cpdfsdk_actionhandler.cpp:553:13
    #32 0x55bbb49fda80 in CPDFSDK_ActionHandler::RunDocumentOpenJavaScript(CPDFSDK_FormFillEnvironment*, fxcrt::WideString const&, fxcrt::WideString const&) fpdfsdk/cpdfsdk_actionhandler.cpp:462
    #33 0x55bbb49fd4b2 in CPDFSDK_ActionHandler::ExecuteDocumentOpenAction(CPDF_Action const&, CPDFSDK_FormFillEnvironment*, std::__1::set<CPDF_Dictionary const*, std::__1::less<CPDF_Dictionary const*>, std::__1::allocator<CPDF_Dictionary const*> >*) fpdfsdk/cpdfsdk_actionhandler.cpp:131:9
    #34 0x55bbb49fcf71 in CPDFSDK_ActionHandler::DoAction_DocOpen(CPDF_Action const&, CPDFSDK_FormFillEnvironment*) fpdfsdk/cpdfsdk_actionhandler.cpp:27:10
    #35 0x55bbb4a19aad in CPDFSDK_FormFillEnvironment::ProcOpenAction() fpdfsdk/cpdfsdk_formfillenvironment.cpp:596:23
    #36 0x55bbb4411e7b in RenderPdf samples/pdfium_test.cc:806:3
    #37 0x55bbb4411e7b in main samples/pdfium_test.cc:1012
    #38 0x7fb0b10e882f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

0x606000001908 is located 40 bytes inside of 56-byte region [0x6060000018e0,0x606000001918)
freed by thread T0 here:
    #0 0x55bbb440af6d in operator delete(void*) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:166:3
    #1 0x55bbb472194a in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #2 0x55bbb472194a in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #3 0x55bbb472194a in operator= buildtools/third_party/libc++/trunk/include/memory:2517
    #4 0x55bbb472194a in CPDF_Dictionary::SetFor(fxcrt::ByteString const&, std::__1::unique_ptr<CPDF_Object, std::__1::default_delete<CPDF_Object> >) core/fpdfapi/parser/cpdf_dictionary.cpp:216
    #5 0x55bbb45a43c7 in _ZN15CPDF_Dictionary9SetNewForI9CPDF_NameJRN5fxcrt10ByteStringEEEENSt3__19enable_ifIXsr16CanInternStringsIT_EE5valueEPS7_E4typeERKS3_DpOT0_ core/fpdfapi/parser/cpdf_dictionary.h:93:28
    #6 0x55bbb45a9c8e in CPDF_FormField::CheckControl(int, bool, NotificationOption) core/fpdfdoc/cpdf_formfield.cpp:749:16
    #7 0x55bbb45a83af in CPDF_FormField::ResetField(NotificationOption) core/fpdfdoc/cpdf_formfield.cpp:191:9
    #8 0x55bbb45b6982 in CPDF_InteractiveForm::ResetForm(NotificationOption) core/fpdfdoc/cpdf_interactiveform.cpp:827:13
    #9 0x55bbb4a6735e in CJS_Document::resetForm(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/cjs_document.cpp:581:15
    #10 0x55bbb4a8e2ec in void JSMethod<CJS_Document, &CJS_Document::resetForm>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) fxjs/js_define.h:128:23
    #11 0x55bbb4c9419d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:157:3
    #12 0x55bbb4c91ec4 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #13 0x55bbb4c8fa54 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #14 0x55bbb67d5b18 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit (/home/bananana/pdfium_latest/pdfium/out/stable_asan/pdfium_test+0x3226b18)
    #15 0x55bbb6748a03 in Builtins_InterpreterEntryTrampoline (/home/bananana/pdfium_latest/pdfium/out/stable_asan/pdfium_test+0x3199a03)
    #16 0x55bbb674637c in Builtins_JSEntryTrampoline (/home/bananana/pdfium_latest/pdfium/out/stable_asan/pdfium_test+0x319737c)
    #17 0x55bbb67460f7 in Builtins_JSEntry (/home/bananana/pdfium_latest/pdfium/out/stable_asan/pdfium_test+0x31970f7)
    #18 0x55bbb560b5b5 in Call v8/src/simulator.h:138:12
    #19 0x55bbb560b5b5 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:274
    #20 0x55bbb560ab35 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:366:10
    #21 0x55bbb4b3c5f6 in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:2174:7
    #22 0x55bbb4a3b33b in CFXJS_Engine::Execute(fxcrt::WideString const&) fxjs/cfxjs_engine.cpp:571:25
    #23 0x55bbb4b09801 in CJS_Runtime::ExecuteScript(fxcrt::WideString const&) fxjs/cjs_runtime.cpp:168:10
    #24 0x55bbb4a9cdbc in CJS_EventContext::RunScript(fxcrt::WideString const&) fxjs/cjs_event_context.cpp:53:23
    #25 0x55bbb49fdfad in RunScript fpdfsdk/cpdfsdk_actionhandler.cpp:553:13
    #26 0x55bbb49fdfad in CPDFSDK_ActionHandler::RunFieldJavaScript(CPDFSDK_FormFillEnvironment*, CPDF_FormField*, CPDF_AAction::AActionType, CPDFSDK_FieldAction*, fxcrt::WideString const&) fpdfsdk/cpdfsdk_actionhandler.cpp:411
    #27 0x55bbb49ff0ca in CPDFSDK_ActionHandler::ExecuteFieldAction(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, CPDF_FormField*, CPDFSDK_FieldAction*, std::__1::set<CPDF_Dictionary const*, std::__1::less<CPDF_Dictionary const*>, std::__1::allocator<CPDF_Dictionary const*> >*) fpdfsdk/cpdfsdk_actionhandler.cpp:238:9
    #28 0x55bbb49feb98 in CPDFSDK_ActionHandler::DoAction_Field(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, CPDF_FormField*, CPDFSDK_FieldAction*) fpdfsdk/cpdfsdk_actionhandler.cpp:112:10
    #29 0x55bbb4a2c50d in CPDFSDK_Widget::OnAAction(CPDF_AAction::AActionType, CPDFSDK_FieldAction*, CPDFSDK_PageView*) fpdfsdk/cpdfsdk_widget.cpp:837:39
    #30 0x55bbb6871296 in CFFL_InteractiveFormFiller::OnValidate(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*, CPDFSDK_PageView*, unsigned int) fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:702:12
    #31 0x55bbb6867844 in CFFL_FormFiller::CommitData(CPDFSDK_PageView*, unsigned int) fpdfsdk/formfiller/cffl_formfiller.cpp:516:21
    #32 0x55bbb686714a in CFFL_FormFiller::KillFocusForAnnot(unsigned int) fpdfsdk/formfiller/cffl_formfiller.cpp:302:22
    #33 0x55bbb686f91e in CFFL_InteractiveFormFiller::OnKillFocus(fxcrt::Observable<CPDFSDK_Annot>::ObservedPtr*, unsigned int) fpdfsdk/formfiller/cffl_interactiveformfiller.cpp:436:16
    #34 0x55bbb4a18818 in CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int) fpdfsdk/cpdfsdk_formfillenvironment.cpp:695:23

previously allocated by thread T0 here:
    #0 0x55bbb440a70d in operator new(unsigned long) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:105:3
    #1 0x55bbb477158a in MakeUnique<CPDF_Dictionary, fxcrt::WeakPtr<fxcrt::StringPoolTemplate<fxcrt::ByteString>, std::__1::default_delete<fxcrt::StringPoolTemplate<fxcrt::ByteString> > > &> third_party/base/ptr_util.h:56:29
    #2 0x55bbb477158a in CPDF_SyntaxParser::GetObjectBodyInternal(CPDF_IndirectObjectHolder*, CPDF_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf_syntax_parser.cpp:484
    #3 0x55bbb47718b4 in CPDF_SyntaxParser::GetObjectBodyInternal(CPDF_IndirectObjectHolder*, CPDF_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf_syntax_parser.cpp:506:11
    #4 0x55bbb47740d1 in CPDF_SyntaxParser::GetIndirectObject(CPDF_IndirectObjectHolder*, CPDF_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf_syntax_parser.cpp:559:7
    #5 0x55bbb47550d8 in CPDF_Parser::ParseIndirectObjectAt(long, unsigned int) core/fpdfapi/parser/cpdf_parser.cpp:918:28
    #6 0x55bbb4755df0 in CPDF_Parser::ParseIndirectObject(unsigned int) core/fpdfapi/parser/cpdf_parser.cpp:867:12
    #7 0x55bbb4724bcc in CPDF_Document::ParseIndirectObject(unsigned int) core/fpdfapi/parser/cpdf_document.cpp:196:33
    #8 0x55bbb473652e in CPDF_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) core/fpdfapi/parser/cpdf_indirect_object_holder.cpp:50:42
    #9 0x55bbb46fb2e5 in GetDirectObjectAt core/fpdfapi/parser/cpdf_array.cpp:105:24
    #10 0x55bbb46fb2e5 in CPDF_Array::GetDictAt(unsigned long) core/fpdfapi/parser/cpdf_array.cpp:139
    #11 0x55bbb45b4a4d in CPDF_InteractiveForm::CPDF_InteractiveForm(CPDF_Document*) core/fpdfdoc/cpdf_interactiveform.cpp:599:24
    #12 0x55bbb4a1b9d5 in ReportUnsupportedFeatures(CPDF_Document*) fpdfsdk/cpdfsdk_helpers.cpp:340:32
    #13 0x55bbb6a277e4 in (anonymous namespace)::LoadDocumentImpl(fxcrt::RetainPtr<IFX_SeekableReadStream> const&, char const*) fpdfsdk/fpdf_view.cpp:144:3
    #14 0x55bbb6a27976 in FPDF_LoadCustomDocument fpdfsdk/fpdf_view.cpp:272:10
    #15 0x55bbb4411ae2 in RenderPdf samples/pdfium_test.cc:743:15
    #16 0x55bbb4411ae2 in main samples/pdfium_test.cc:1012
    #17 0x7fb0b10e882f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/__tree:1082:59 in __root
Shadow bytes around the buggy address:
  0x0c0c7fff82d0: fa fa fa fa 00 00 00 00 00 00 00 fa fa fa fa fa
  0x0c0c7fff82e0: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
  0x0c0c7fff82f0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c0c7fff8300: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c0c7fff8310: 00 00 00 00 00 00 00 fa fa fa fa fa fd fd fd fd
=>0x0c0c7fff8320: fd[fd]fd fa fa fa fa fa 00 00 00 00 00 00 00 fa
  0x0c0c7fff8330: fa fa fa fa 00 00 00 00 00 00 00 fa fa fa fa fa
  0x0c0c7fff8340: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
  0x0c0c7fff8350: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c0c7fff8360: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c0c7fff8370: 00 00 00 00 00 00 00 fa fa fa fa fa fd fd fd fd
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
==18076==ABORTING

### ba...@gmail.com (2019-07-17)

Please note that it still works on beta too.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-17)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/9d03368411ccb46b1e39693f9d1723a9b2f34dd7

commit 9d03368411ccb46b1e39693f9d1723a9b2f34dd7
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Jul 17 21:16:36 2019

Replace UnownedPtr with RetainPtr to parser objects in fpdfdoc

Bug: chromium:983867
Change-Id: Ib07bfb48ef85ee7a013f5e1a3d2127648dc950ba
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/57854
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/9d03368411ccb46b1e39693f9d1723a9b2f34dd7/testing/resources/javascript/bug_983867_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/9d03368411ccb46b1e39693f9d1723a9b2f34dd7/core/fpdfdoc/cpdf_action.h
[modify] https://pdfium.googlesource.com/pdfium/+/9d03368411ccb46b1e39693f9d1723a9b2f34dd7/core/fpdfdoc/cpdf_aaction.h
[modify] https://pdfium.googlesource.com/pdfium/+/9d03368411ccb46b1e39693f9d1723a9b2f34dd7/core/fpdfdoc/cpdf_bookmark.h
[add] https://pdfium.googlesource.com/pdfium/+/9d03368411ccb46b1e39693f9d1723a9b2f34dd7/testing/resources/javascript/bug_983867.in
[modify] https://pdfium.googlesource.com/pdfium/+/9d03368411ccb46b1e39693f9d1723a9b2f34dd7/core/fpdfdoc/cpdf_dest.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/277e9e3f8e4d8bef5dfe7b67938fae6957684b56

commit 277e9e3f8e4d8bef5dfe7b67938fae6957684b56
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jul 18 00:17:10 2019

Roll src/third_party/pdfium 68fb145dca2b..9d03368411cc (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/68fb145dca2b..9d03368411cc


git log 68fb145dca2b..9d03368411cc --date=short --no-merges --format='%ad %ae %s'
2019-07-17 tsepez@chromium.org Replace UnownedPtr with RetainPtr to parser objects in fpdfdoc
2019-07-17 thestig@chromium.org Properly check for Windows path names in presubmit checks.
2019-07-17 thestig@chromium.org Properly run Python scripts on Windows in presubmit checks.
2019-07-17 thestig@chromium.org Add click_form.pdf test PDF.


Created with:
  gclient setdep -r src/third_party/pdfium@9d03368411cc

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:983867
TBR=pdfium-deps-rolls@chromium.org

Change-Id: I6369b8090009bbb886506af1eb5d50a9415ef683
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1707378
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#678507}

[modify] https://crrev.com/277e9e3f8e4d8bef5dfe7b67938fae6957684b56/DEPS


### ts...@chromium.org (2019-07-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-07-18)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-76; it appears the fix may have landed after branch point, meaning a merge might be required. The owner of this bug should confirm if a merge is required here. If so, add Merge-Request-76 label and indicate which commits/CLs are to be merged. Otherwise, remove Merge-TBD label. Thanks.

### sh...@chromium.org (2019-07-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-19)

Requesting merge to M76 because latest trunk commit (678507) appears to be after beta branch point (665002).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-19)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-07-19)

tsepez@ can you please confirm if this is something we need to merge toM76?Will this be a fairly safe merge?

### th...@chromium.org (2019-07-19)

BTW, I think we need to merge https://pdfium.googlesource.com/pdfium/+/22923602f40e0fe3cdad7d3ce8828497e5e2a7fb in addition to https://pdfium.googlesource.com/pdfium/+/9d03368411ccb46b1e39693f9d1723a9b2f34dd7, and there may be some minor merge conflicts along the way.

### ab...@google.com (2019-07-22)

How critical is this fix? Since we're so close to M76 stable my preference is that we target M77 for this. 

### na...@google.com (2019-07-22)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-22)

abdulsyed@ I'd like to hear what tsepez@ says about the risk of the fix (and the dependencies noted in https://crbug.com/chromium/983867#c24), but this is externally reported and per https://crbug.com/chromium/983867#c4 plausibly results in remote code execution. I think we'd definitely respin to include this. So it would probably be simplest to include it in the initial M76 release, assuming it's had sufficient bake time for everyone to be comfortable.

That said, per https://crbug.com/chromium/983867#c14 this should be Security_Impact-Stable so it's not actually a regression. I've adjusted that label and removed the RBS label that Sheriffbot added in response.

### wf...@chromium.org (2019-07-26)

re: #25 I agree this should be merged. Removing rejected so this can be reassessed.

### sh...@chromium.org (2019-07-26)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2019-07-29)

Let me take a stab at a merge.

### ts...@chromium.org (2019-07-29)

M76 CL at https://pdfium-review.googlesource.com/c/pdfium/+/58410

### ts...@chromium.org (2019-07-29)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-30)

Congrats the Panel decided to reward $5,000 for this report!

### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-31)

[Empty comment from Monorail migration]

### ab...@google.com (2019-08-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-08-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-08-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/983867?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095708)*
