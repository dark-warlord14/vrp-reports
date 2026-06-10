# Security: heap-use-after-free in __tree_next_iter

| Field | Value |
|-------|-------|
| **Issue ID** | [40093192](https://issues.chromium.org/issues/40093192) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-11-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

This issue was found by fuzzing against a 64-bit asan linux build of pdfium\_test.

**VERSION**  

Chrome Version: 70.0.3538.77  

Operating System: Fedora 29 x86\_64

**REPRODUCTION CASE**  

./pdfium\_test tests\_f11fdb5028adb80d3781b8be70d336e521c53768

# Rendering PDF file tests\_f11fdb5028adb80d3781b8be70d336e521c53768.

==3224==ERROR: AddressSanitizer: heap-use-after-free on address 0x604000003c58 at pc 0x000002ff6648 bp 0x7ffe76ccd550 sp 0x7ffe76ccd548  

READ of size 8 at 0x604000003c58 thread T0  

#0 0x2ff6647 in \_\_tree\_next\_iter<std::\_\_1::\_\_tree\_end\_node<std::\_\_1::\_\_tree\_node\_base<void \*> \*> \*, std::\_\_1::\_\_tree\_node\_base<void \*> \*> buildtools/third\_party/libc++/trunk/include/\_\_tree:185:14  

#1 0x2ff6647 in operator++ buildtools/third\_party/libc++/trunk/include/\_\_tree:921  

#2 0x2ff6647 in operator++ buildtools/third\_party/libc++/trunk/include/map:772  

#3 0x2ff6647 in CJS\_Document::get\_info(CJS\_Runtime\*) third\_party/pdfium/fxjs/cjs\_document.cpp:686  

#4 0x3001802 in void JSPropGetter<CJS\_Document, &(CJS\_Document::get\_info(CJS\_Runtime\*))>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&) third\_party/pdfium/fxjs/js\_define.h:86:23  

#5 0x1a88751 in v8::internal::PropertyCallbackArguments::BasicCallNamedGetterCallback(void (\*)(v8::Local[v8::Name](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/api-arguments-inl.h:174:3  

#6 0x1c72fe3 in CallAccessorGetter v8/src/api-arguments-inl.h:306:10  

#7 0x1c72fe3 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator\*) v8/src/objects.cc:1569  

#8 0x1c71280 in v8::internal::Object::GetProperty(v8::internal::LookupIterator\*, v8::internal::OnNonExistent) v8/src/objects.cc:1053:16  

#9 0x1a4c964 in v8::internal::LoadIC::Load(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);)) v8/src/ic/ic.cc:470:5  

#10 0x1a66792 in \_\_RT\_impl\_Runtime\_LoadIC\_Miss v8/src/ic/ic.cc:2175:5  

#11 0x1a66792 in v8::internal::Runtime\_LoadIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/ic/ic.cc:2159  

#12 0x277016d (/home/henices/research/asan-linux-stable-70.0.3538.77/pdfium\_test+0x277016d)  

#13 0x7eafde1063f1 (<unknown module>)  

#14 0x7eafde088557 (<unknown module>)  

#15 0x7eafde088557 (<unknown module>)  

#16 0x26e39a2 (/home/henices/research/asan-linux-stable-70.0.3538.77/pdfium\_test+0x26e39a2)  

#17 0x7eafde085a1d (<unknown module>)  

#18 0x1826c5d in Call v8/src/simulator.h:113:12  

#19 0x1826c5d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:155  

#20 0x1826453 in CallInternal v8/src/execution.cc:191:10  

#21 0x1826453 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:202  

#22 0xe3faed in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:2137:7  

#23 0x2fd952d in CFXJS\_Engine::Execute(fxcrt::WideString const&) third\_party/pdfium/fxjs/cfxjs\_engine.cpp:534:25  

#24 0x2fe0be1 in CJS\_Runtime::ExecuteScript(fxcrt::WideString const&) third\_party/pdfium/fxjs/cjs\_runtime.cpp:176:10  

#25 0x3079ceb in CJS\_EventContext::RunScript(fxcrt::WideString const&) third\_party/pdfium/fxjs/cjs\_event\_context.cpp:53:23  

#26 0x290ed96 in CPDFSDK\_ActionHandler::RunScript(CPDFSDK\_FormFillEnvironment\*, fxcrt::WideString const&, std::\_\_1::function<void (IJS\_EventContext\*)> const&) third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:546:13  

#27 0x290c390 in RunDocumentOpenJavaScript third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:455:3  

#28 0x290c390 in CPDFSDK\_ActionHandler::ExecuteDocumentOpenAction(CPDF\_Action const&, CPDFSDK\_FormFillEnvironment\*, std::\_\_1::set<CPDF\_Dictionary const\*, std::\_\_1::less<CPDF\_Dictionary const\*>, std::\_\_1::allocator<CPDF\_Dictionary const\*> >\*) third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:130  

#29 0x290bd41 in CPDFSDK\_ActionHandler::DoAction\_DocOpen(CPDF\_Action const&, CPDFSDK\_FormFillEnvironment\*) third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:27:10  

#30 0x29157bd in CPDFSDK\_FormFillEnvironment::ProcOpenAction() third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:588:23  

#31 0x28e6ac3 in FORM\_DoDocumentOpenAction third\_party/pdfium/fpdfsdk/fpdf\_formfill.cpp:662:19  

#32 0xb92253 in RenderPdf third\_party/pdfium/samples/pdfium\_test.cc:747:3  

#33 0xb92253 in main third\_party/pdfium/samples/pdfium\_test.cc:948  

#34 0x7effc6448412 in \_\_libc\_start\_main (/lib64/libc.so.6+0x24412)

0x604000003c58 is located 8 bytes inside of 48-byte region [0x604000003c50,0x604000003c80)  

freed by thread T0 here:  

#0 0xb8afa2 in operator delete(void\*) /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:167:3  

#1 0x2bd2194 in \_\_libcpp\_deallocate buildtools/third\_party/libc++/trunk/include/new:279:10  

#2 0x2bd2194 in deallocate buildtools/third\_party/libc++/trunk/include/memory:1802  

#3 0x2bd2194 in deallocate buildtools/third\_party/libc++/trunk/include/memory:1556  

#4 0x2bd2194 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::erase(std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, long>) buildtools/third\_party/libc++/trunk/include/\_\_tree:2370  

#5 0x2bd0070 in erase buildtools/third\_party/libc++/trunk/include/map:1194:56  

#6 0x2bd0070 in CPDF\_Dictionary::RemoveFor(fxcrt::ByteString const&) third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:229  

#7 0x2cad220 in CPDF\_FormField::ResetField(NotificationOption) third\_party/pdfium/core/fpdfdoc/cpdf\_formfield.cpp:236:18  

#8 0x2cb9ec2 in CPDF\_InterForm::ResetForm(NotificationOption) third\_party/pdfium/core/fpdfdoc/cpdf\_interform.cpp:820:13  

#9 0x2ff2c0d in CJS\_Document::resetForm(CJS\_Runtime\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) third\_party/pdfium/fxjs/cjs\_document.cpp:473:15  

#10 0x301824c in void JSMethod<CJS\_Document, &(CJS\_Document::resetForm(CJS\_Runtime\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&))>(char const\*, char const\*, v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) third\_party/pdfium/fxjs/js\_define.h:136:23  

#11 0xf81991 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) v8/src/api-arguments-inl.h:119:3  

#12 0xf7f453 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#13 0xf7d5d8 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#14 0x277016d (/home/henices/research/asan-linux-stable-70.0.3538.77/pdfium\_test+0x277016d)  

#15 0x7eafde088557 (<unknown module>)  

#16 0x26dfea5 (/home/henices/research/asan-linux-stable-70.0.3538.77/pdfium\_test+0x26dfea5)  

#17 0x26e39a2 (/home/henices/research/asan-linux-stable-70.0.3538.77/pdfium\_test+0x26e39a2)  

#18 0x7eafde085a1d (<unknown module>)  

#19 0x1826c5d in Call v8/src/simulator.h:113:12  

#20 0x1826c5d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:155  

#21 0x1826453 in CallInternal v8/src/execution.cc:191:10  

#22 0x1826453 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:202  

#23 0x1c7ace0 in SetPropertyWithDefinedSetter v8/src/objects.cc:1747:3  

#24 0x1c7ace0 in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::ShouldThrow) v8/src/objects.cc:1707  

#25 0x1cab6de in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed, bool\*) v8/src/objects.cc:5058:16  

#26 0x1caafac in v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed) v8/src/objects.cc:5114:9  

#27 0x20fae26 in v8::internal::Runtime::SetObjectProperty(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode) v8/src/runtime/runtime-object.cc:456:3  

#28 0xe51b7d in v8::Object::Set(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);)) v8/src/api.cc:4104:7  

#29 0x2fde71b in CFX\_V8::PutObjectProperty(v8::Local[v8::Object](javascript:void(0);), fxcrt::WideString const&, v8::Local[v8::Value](javascript:void(0);)) third\_party/pdfium/fxjs/cfx\_v8.cpp:52:9  

#30 0x2ff61ca in CJS\_Document::get\_info(CJS\_Runtime\*) third\_party/pdfium/fxjs/cjs\_document.cpp:691:17  

#31 0x3001802 in void JSPropGetter<CJS\_Document, &(CJS\_Document::get\_info(CJS\_Runtime\*))>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&) third\_party/pdfium/fxjs/js\_define.h:86:23  

#32 0x1a88751 in v8::internal::PropertyCallbackArguments::BasicCallNamedGetterCallback(void (\*)(v8::Local[v8::Name](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/api-arguments-inl.h:174:3  

#33 0x1c72fe3 in CallAccessorGetter v8/src/api-arguments-inl.h:306:10  

#34 0x1c72fe3 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator\*) v8/src/objects.cc:1569  

#35 0x1c71280 in v8::internal::Object::GetProperty(v8::internal::LookupIterator\*, v8::internal::OnNonExistent) v8/src/objects.cc:1053:16  

#36 0x1a4c964 in v8::internal::LoadIC::Load(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);)) v8/src/ic/ic.cc:470:5  

#37 0x1a66792 in \_\_RT\_impl\_Runtime\_LoadIC\_Miss v8/src/ic/ic.cc:2175:5  

#38 0x1a66792 in v8::internal::Runtime\_LoadIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/ic/ic.cc:2159

previously allocated by thread T0 here:  

#0 0xb8a362 in operator new(unsigned long) /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:106:3  

#1 0x2bd232b in \_\_libcpp\_allocate buildtools/third\_party/libc++/trunk/include/new:259:10  

#2 0x2bd232b in allocate buildtools/third\_party/libc++/trunk/include/memory:1799  

#3 0x2bd232b in allocate buildtools/third\_party/libc++/trunk/include/memory:1548  

#4 0x2bd232b in \_\_construct\_node<const std::\_\_1::piecewise\_construct\_t &, std::\_\_1::tuple<fxcrt::ByteString &&>, std::\_\_1::tuple<> > buildtools/third\_party/libc++/trunk/include/\_\_tree:2191  

#5 0x2bd232b in std::\_\_1::pair<std::\_\_1::\_\_tree\_iterator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, long>, bool> std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::\_\_emplace\_unique\_key\_args<fxcrt::ByteString, std::\_\_1::piecewise\_construct\_t const&, std::\_\_1::tuple[fxcrt::ByteString&&](javascript:void(0);), std::\_\_1::tuple<> >(fxcrt::ByteString const&, std::\_\_1::piecewise\_construct\_t const&, std::\_\_1::tuple[fxcrt::ByteString&&](javascript:void(0);)&&, std::\_\_1::tuple<>&&) buildtools/third\_party/libc++/trunk/include/\_\_tree:2137  

#6 0x2bcfcff in operator[] buildtools/third\_party/libc++/trunk/include/map:1329:20  

#7 0x2bcfcff in CPDF\_Dictionary::SetFor(fxcrt::ByteString const&, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >) third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:209  

#8 0x2c31d88 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:511:16  

#9 0x2c3444b in CPDF\_SyntaxParser::GetIndirectObject(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:553:7  

#10 0x2c10a8a in CPDF\_Parser::ParseIndirectObjectAt(long, unsigned int) third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:921:28  

#11 0x2c11843 in CPDF\_Parser::ParseIndirectObject(unsigned int) third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:870:12  

#12 0x2be376c in CPDF\_Document::ParseIndirectObject(unsigned int) third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:196:33  

#13 0x2bf38fe in CPDF\_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) third\_party/pdfium/core/fpdfapi/parser/cpdf\_indirect\_object\_holder.cpp:49:42  

#14 0x2bb3595 in GetDirectObjectAt third\_party/pdfium/core/fpdfapi/parser/cpdf\_array.cpp:105:24  

#15 0x2bb3595 in CPDF\_Array::GetDictAt(unsigned long) third\_party/pdfium/core/fpdfapi/parser/cpdf\_array.cpp:139  

#16 0x2cb7fcd in CPDF\_InterForm::CPDF\_InterForm(CPDF\_Document\*) third\_party/pdfium/core/fpdfdoc/cpdf\_interform.cpp:596:24  

#17 0x28e12e4 in ReportUnsupportedFeatures(CPDF\_Document\*) third\_party/pdfium/fpdfsdk/cpdfsdk\_helpers.cpp:242:32  

#18 0x291a774 in (anonymous namespace)::LoadDocumentImpl(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, char const\*) third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:156:3  

#19 0x291a8fb in FPDF\_LoadCustomDocument third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:282:10  

#20 0xb91f92 in RenderPdf third\_party/pdfium/samples/pdfium\_test.cc:691:15  

#21 0xb91f92 in main third\_party/pdfium/samples/pdfium\_test.cc:948  

#22 0x7effc6448412 in \_\_libc\_start\_main (/lib64/libc.so.6+0x24412)

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third\_party/libc++/trunk/include/\_\_tree:185:14 in \_\_tree\_next\_iter<std::\_\_1::\_\_tree\_end\_node<std::\_\_1::\_\_tree\_node\_base<void \*> \*> \*, std::\_\_1::\_\_tree\_node\_base<void \*> \*>  

Shadow bytes around the buggy address:  

0x0c087fff8730: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fa  

0x0c087fff8740: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c087fff8750: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa  

0x0c087fff8760: fa fa fd fd fd fd fd fa fa fa 00 00 00 00 00 00  

0x0c087fff8770: fa fa 00 00 00 00 00 00 fa fa 00 00 00 00 00 00  

=>0x0c087fff8780: fa fa 00 00 00 00 00 00 fa fa fd[fd]fd fd fd fd  

0x0c087fff8790: fa fa 00 00 00 00 00 00 fa fa 00 00 00 00 00 00  

0x0c087fff87a0: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa  

0x0c087fff87b0: fa fa 00 00 00 00 00 00 fa fa 00 00 00 00 00 00  

0x0c087fff87c0: fa fa 00 00 00 00 00 00 fa fa 00 00 00 00 00 00  

0x0c087fff87d0: fa fa 00 00 00 00 00 00 fa fa 00 00 00 00 00 00  

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

==3224==ABORTING

testcase is in the attachment.

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### zh...@gmail.com (2018-11-26)

affects asan-linux-stable-70.0.3538.77

### do...@chromium.org (2018-11-26)

+pdf folks, can you follow up on this please?

[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### rh...@chromium.org (2018-11-26)

Not on the PDFium anymore, sending to someone that is active on the project.

### ts...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### zh...@gmail.com (2018-12-07)

It's not only affects stable 70 but also beta 71.

The last beta 71 (asan-linux-beta-71.0.3578.80.zip) which is refered to 71 stable (asan-linux-stable-71.0.3578.80.zip), this bug is still there.

see https://crbug.com/chromium/912469.

Because I don't have the permission to see https://crbug.com/chromium/895152, so I doubt about if the patch hadn't been merge to beta branch or this is another issue.


### th...@chromium.org (2018-12-07)

awhalley: Looks like we forgot to merge to 71?

### zh...@gmail.com (2018-12-07)

mmoroz@ asked me to create a new issue for the bug, but I have already created a lot of duplicated issues. (-_-)

If you have more details could you please let me know, thank you.

### th...@chromium.org (2018-12-07)

Let's wait for the https://crbug.com/chromium/895152 merge and see if this still reproduces.

### th...@chromium.org (2018-12-07)

Setting a NextAction date for a week from now, so we don't forget.

### th...@chromium.org (2018-12-14)

awhalley@ didn't get back to me on https://crbug.com/chromium/895152, so we are still stuck here.

### aw...@google.com (2018-12-14)

Updated https://crbug.com/chromium/895152, recommending it gets merge approval for 71

### zh...@gmail.com (2018-12-17)

I can't reproduce this bug, after https://crbug.com/chromium/895152 merged to 71.

awhalley@

As this bug affected stable 71, could I request a CVE, thank you.

### zh...@gmail.com (2018-12-20)

Hi Team:

Any update for this issue?

I think marked https://crbug.com/chromium/912469 duplicated is a bit hasty,fortunately I have this old issue to notify the team.

Because this bug affected stable 71, it's eligible for a CVE.





### th...@chromium.org (2018-12-20)

I merged to M71 here: https://pdfium.googlesource.com/pdfium/+/2ebef1487e139dfe1f44998f312ed59f80202c82

That will be in 71.0.3578.100, but the current stable release is 71.0.3578.98.

### aw...@google.com (2018-12-22)

Greetings zhouzhenster@ - unless there's a stable update to M71, this fix will be included in M72, and will be issued a CVE when that goes stable. Are you OK to wait until then or would you like one issued sooner?

### aw...@google.com (2018-12-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-22)

[Empty comment from Monorail migration]

### zh...@gmail.com (2018-12-24)

awhalley@

I'm OK to wait util M72 goes stable.

BTW, the sheriffbot@ rejected to set reward-topanel label, due to the bug status (Duplicated).

Thanks.


### aw...@google.com (2018-12-27)

(moving to fixed from Dupe of 895152 so the VRP panel can take a look)

### sh...@chromium.org (2018-12-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-28)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-12-28)

thestig@ - do we need to merge this to m72?

### aw...@google.com (2019-01-02)

no need to merge per https://crbug.com/chromium/908292#c5 of https://crbug.com/chromium/895152 it's already there

### na...@google.com (2019-01-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-10)

Thanks for your report. The panel has decided to reward $500 :) 

### na...@google.com (2019-01-10)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/908292?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/895152]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093192)*
