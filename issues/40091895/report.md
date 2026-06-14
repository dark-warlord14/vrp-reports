# Security: Bad cast in JSPropGetter in js_define.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40091895](https://issues.chromium.org/issues/40091895) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-07-10 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

This bug is present in JSPropSetter method in fxjs/js\_define.h file.  

I think JSMethod and JSPropGetter methods in fxjs/js\_define.h also has the same bug.  

But I could not prepare a test case for those methods.

Below is a code section from JSPropSetter method.

template <class C, CJS\_Return (C::\*M)(CJS\_Runtime\*)>  

void JSPropGetter(const char\* prop\_name\_string,  

const char\* class\_name\_string,  

v8::Local[v8::String](javascript:void(0);) property,  

const v8::PropertyCallbackInfo[v8::Value](javascript:void(0);)& info) {  

CJS\_Object\* pJSObj = CFXJS\_Engine::GetObjectPrivate(info.Holder());  

.....  

C\* pObj = static\_cast<C\*>(pJSObj);  

CJS\_Return result = (pObj->\*M)(pRuntime);  

......  

}

Above method uses CFXJS\_Engine::GetObjectPrivate method to get private CJS\_Object from javascript object.  

Then try to cast CJS\_Object to the subclass type of "C"(see template above method signature).  

But does not check wether the actual type of CJS\_Object matches type "C".

This is the code of CFXJS\_Engine::GetObjectPrivate method.

CJS\_Object\* CFXJS\_Engine::GetObjectPrivate(v8::Local[v8::Object](javascript:void(0);) pObj) {  

CFXJS\_PerObjectData\* pData = CFXJS\_PerObjectData::GetFromObject(pObj);  

if (!pData && !pObj.IsEmpty()) {  

// It could be a global proxy object.

```
v8::Local<v8::Value> v = pObj->GetPrototype();   
 /\* Note:  Prototype can be changed with  Object.setPrototypeOf \*/  

if (v->IsObject()) {  
  pData = CFXJS_PerObjectData::GetFromObject(  
      v->ToObject(v8::Isolate::GetCurrent()->GetCurrentContext())  
          .ToLocalChecked());  
}  

```

}  

return pData ? pData->m\_pPrivate.get() : nullptr;  

}

Setting the prototype of javascript object to a diffent type of object makes CFXJS\_Engine::GetObjectPrivate method to return  

incorrect type of CJS\_Object to JSPropGetter method.  

ex. a = new app.constructor;  

Object.setPrototypeOf(a,global);

**VERSION**  

Chrome Version: [67.0.3396.99] + [stable]  

[69.0.3487.0] + [Trunk build]  

Operating System: [Windows 10 , Ubuntu 16.04]

**REPRODUCTION CASE**

1. Open attached cast.pdf with chrome.  
   
   PDF plugin process will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF plugin process]  

Crash State: [Address Sanitizer output]

This is the address sanitizer output produced by test case.  

But it does not show the actual stacktrace for bad cast bug.

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x608000019701 at pc 0x55d70318592e bp 0x7ffcf4828700 sp 0x7ffcf48286f8  

READ of size 8 at 0x608000019701 thread T0 (chrome)  

#0 0x55d70318592d in \_\_insert\_node\_at /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2112:25  

#1 0x55d70318592d in std::\_\_1::pair<std::\_\_1::\_\_tree\_iterator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CJS\_Global::JSGlobalData, std::\_\_1::default\_delete<CJS\_Global::JSGlobalData> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CJS\_Global::JSGlobalData, std::\_\_1::default\_delete<CJS\_Global::JSGlobalData> > >, void\*>\*, long>, bool> std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CJS\_Global::JSGlobalData, std::\_\_1::default\_delete<CJS\_Global::JSGlobalData> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CJS\_Global::JSGlobalData, std::\_\_1::default\_delete<CJS\_Global::JSGlobalData> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CJS\_Global::JSGlobalData, std::\_\_1::default\_delete<CJS\_Global::JSGlobalData> > > > >::\_\_emplace\_unique\_key\_args<fxcrt::ByteString, std::\_\_1::piecewise\_construct\_t const&, std::\_\_1::tuple<fxcrt::ByteString const&>, std::\_\_1::tuple<> >(fxcrt::ByteString const&, std::\_\_1::piecewise\_construct\_t const&&&, std::\_\_1::tuple<fxcrt::ByteString const&>&&, std::\_\_1::tuple<>&&) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2141:0  

#2 0x55d7031843da in operator[] /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/map:1319:20  

#3 0x55d7031843da in CJS\_Global::SetGlobalVariables(fxcrt::ByteString const&, JS\_GlobalDataType, double, bool, fxcrt::ByteString const&, v8::Local[v8::Object](javascript:void(0);), bool) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_global.cpp:563:0  

#4 0x55d703183a99 in CJS\_Global::SetProperty(CJS\_Runtime\*, wchar\_t const\*, v8::Local[v8::Value](javascript:void(0);)) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_global.cpp:278:12  

#5 0x55d703180b89 in JSSpecialPropPut<CJS\_Global> /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_global.cpp:86:50  

#6 0x55d703180b89 in CJS\_Global::putprop\_static(v8::Local[v8::Name](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_global.cpp:170:0  

#7 0x55d6f1ae97cf in v8::internal::PropertyCallbackArguments::CallNamedSetter(v8::internal::Handle[v8::internal::InterceptorInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) /chromium/src/out/asan/../../v8/src/api-arguments-inl.h:168:3  

#8 0x55d6f1cc54c0 in v8::internal::(anonymous namespace)::SetPropertyWithInterceptorInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::InterceptorInfo](javascript:void(0);), v8::internal::ShouldThrow, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) /chromium/src/out/asan/../../v8/src/objects.cc:1845:20  

#9 0x55d6f1cf2bd6 in SetPropertyWithInterceptor /chromium/src/out/asan/../../v8/src/objects.cc:4884:10  

#10 0x55d6f1cf2bd6 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed, bool\*) /chromium/src/out/asan/../../v8/src/objects.cc:4931:0  

#11 0x55d6f1cf279c in v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed) /chromium/src/out/asan/../../v8/src/objects.cc:5014:9  

#12 0x55d6f1ac166a in v8::internal::StoreIC::Store(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Object::StoreFromKeyed) /chromium/src/out/asan/../../v8/src/ic/ic.cc:1429:3  

#13 0x55d6f1ad319c in **RT\_impl\_Runtime\_StoreIC\_Miss /chromium/src/out/asan/../../v8/src/ic/ic.cc:2283:5  

#14 0x55d6f1ad319c in v8::internal::Runtime\_StoreIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) /chromium/src/out/asan/../../v8/src/ic/ic.cc:2269:0  

#15 0x55d6f27b49cd in v8\_Default\_embedded\_blob* embedded.cc:?  

#16 0x55d6f27b49cd in ?? ??:0  

#11 0x7ec7f408675b (<unknown module>)  

#12 0x7ec7f40086a5 (<unknown module>)  

#17 0x55d6f2728502 in v8\_Default\_embedded\_blob* embedded.cc:?  

#18 0x55d6f2728502 in ?? ??:0  

#14 0x7ec7f40041c0 (<unknown module>)  

#19 0x55d6f188e146 in Call /chromium/src/out/asan/../../v8/src/simulator.h:113:12  

#20 0x55d6f188e146 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) /chromium/src/out/asan/../../v8/src/execution.cc:155:0  

#21 0x55d6f188d993 in CallInternal /chromium/src/out/asan/../../v8/src/execution.cc:191:10  

#22 0x55d6f188d993 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) /chromium/src/out/asan/../../v8/src/execution.cc:202:0  

#23 0x55d6f0ea8f9c in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) /chromium/src/out/asan/../../v8/src/api.cc:2209:7  

#24 0x55d7031752cd in CFXJS\_Engine::Execute(fxcrt::WideString const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cfxjs\_engine.cpp:532:25  

#25 0x55d70317c221 in CJS\_Runtime::ExecuteScript(fxcrt::WideString const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_runtime.cpp:182:10  

#26 0x55d70320fcc7 in CJS\_EventContext::RunScript(fxcrt::WideString const&) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_event\_context.cpp:53:23  

#27 0x55d702c7c8d6 in RunScript /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:546:13  

#28 0x55d702c7c8d6 in CPDFSDK\_ActionHandler::RunDocumentOpenJavaScript(CPDFSDK\_FormFillEnvironment\*, fxcrt::WideString const&, fxcrt::WideString const&) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:455:0  

#29 0x55d702c7c58a in CPDFSDK\_ActionHandler::DoAction\_JavaScript(CPDF\_Action const&, fxcrt::WideString, CPDFSDK\_FormFillEnvironment\*) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:37:7  

#30 0x55d702c853ae in CPDFSDK\_FormFillEnvironment::ProcJavascriptFun() /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:563:25  

#31 0x55d702bea77c in chrome\_pdf::PDFiumEngine::FinishLoadingDocument() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:1031:3  

#32 0x55d702c01d8c in chrome\_pdf::PDFiumEngine::ContinueLoadingDocument(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2619:5  

#33 0x55d702be912b in chrome\_pdf::PDFiumEngine::LoadDocument() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2532:5  

#34 0x55d702c11bec in chrome\_pdf::DocumentLoaderImpl::DidRead(int) /chromium/src/out/asan/../../pdf/document\_loader\_impl.cc:0:7  

#35 0x55d702c12acb in operator() /chromium/src/out/asan/../../ppapi/utility/completion\_callback\_factory.h:6......

0x608000019701 is located 31 bytes to the left of 96-byte region [0x608000019720,0x608000019780)  

allocated by thread T0 (chrome) here:  

#0 0x55d6ec253412 in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55d703181740 in MakeUnique<CJS\_Global, v8::Local[v8::Object](javascript:void(0);) &, CJS\_Runtime \*> /chromium/src/out/asan/../../third\_party/pdfium/third\_party/base/ptr\_util.h:56:29  

#2 0x55d703181740 in void JSConstructor<CJS\_Global>(CFXJS\_Engine\*, v8::Local[v8::Object](javascript:void(0);)) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/js\_define.h:54:0  

#3 0x55d7031744e2 in operator() /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/functional:1913:12  

#4 0x55d7031744e2 in CFXJS\_Engine::NewFXJSBoundObject(int, bool) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cfxjs\_engine.cpp:561:0  

#5 0x55d703173af9 in CFXJS\_Engine::InitializeEngine() /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cfxjs\_engine.cpp:468:35  

#6 0x55d70317ab0d in CJS\_Runtime::CJS\_Runtime(CPDFSDK\_FormFillEnvironment\*) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_runtime.cpp:77:3  

#7 0x55d70316e33d in MakeUnique<CJS\_Runtime, CPDFSDK\_FormFillEnvironment \*&> /chromium/src/out/asan/../../third\_party/pdfium/third\_party/base/ptr\_util.h:56:33  

#8 0x55d70316e33d in IJS\_Runtime::Create(CPDFSDK\_FormFillEnvironment\*) /chromium/src/out/asan/../../third\_party/pdfium/fxjs/ijs\_runtime.cpp:35:0  

#9 0x55d702c8368e in CPDFSDK\_FormFillEnvironment::GetIJSRuntime() /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:212:21  

#10 0x55d702c7c7f2 in RunScript /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:544:58  

#11 0x55d702c7c7f2 in CPDFSDK\_ActionHandler::RunDocumentOpenJavaScript(CPDFSDK\_FormFillEnvironment\*, fxcrt::WideString const&, fxcrt::WideString const&) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:455:0  

#12 0x55d702c7c58a in CPDFSDK\_ActionHandler::DoAction\_JavaScript(CPDF\_Action const&, fxcrt::WideString, CPDFSDK\_FormFillEnvironment\*) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_actionhandler.cpp:37:7  

#13 0x55d702c853ae in CPDFSDK\_FormFillEnvironment::ProcJavascriptFun() /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:563:25  

#14 0x55d702bea77c in chrome\_pdf::PDFiumEngine::FinishLoadingDocument() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:1031:3  

#15 0x55d702c01d8c in chrome\_pdf::PDFiumEngine::ContinueLoadingDocument(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2619:5  

#16 0x55d702be912b in chrome\_pdf::PDFiumEngine::LoadDocument() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2532:5  

#17 0x55d702c11bec in chrome\_pdf::DocumentLoaderImpl::DidRead(int) /chromium/src/out/asan/../../pdf/document\_loader\_impl.cc:0:7  

#18 0x55d702c12acb in operator()  

.....

## Attachments

- [cast.pdf](attachments/cast.pdf) (application/pdf, 2.0 KB)
- [cast_global.pdf](attachments/cast_global.pdf) (application/pdf, 2.0 KB)
- [cast_read.pdf](attachments/cast_read.pdf) (application/pdf, 4.0 KB)
- [description.png](attachments/description.png) (image/png, 21.5 KB)
- [cast_read_release.pdf](attachments/cast_read_release.pdf) (application/pdf, 4.1 KB)

## Timeline

### ch...@gmail.com (2018-07-10)

cast.pdf file contains below mentioned Javascript.

Document Javascript section
----------------------------
a = new app.constructor;
Object.setPrototypeOf(a,global);
a.calculate=true;
global.b = "b"; // This line triggers address sanitizer crash. But it is not part of the actual bug.
                // Above 3 lines causes the incorrect cast bug, but they do not trigger a crash.

### cl...@chromium.org (2018-07-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5090372544626688.

### es...@chromium.org (2018-07-10)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### ch...@gmail.com (2018-07-10)

Please set Components:Internals>Plugins>PDF. This is not a blink>javascript bug.

### ms...@chromium.org (2018-07-11)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Internals>Plugins>PDF]

### th...@chromium.org (2018-07-11)

palmer: Can you help us triage?

This can be reproduced with pdfium_test, so you don't need to build the entire browser. In a Chromium checkout, one can turn on UBSAN and get:

Rendering PDF file /tmp/cast.pdf.
../../third_party/pdfium/fxjs/js_define.h:99:13: runtime error: downcast of address 0x117837fc1a20 which does not point to an object of type 'CJS_App'
0x117837fc1a20: note: object is of type 'CJS_Global'
 00 00 00 00  38 fd f9 02 00 00 00 00  00 20 09 38 78 11 00 00  00 b1 b2 38 78 11 00 00  38 fa f9 02
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CJS_Global'
    #0 0x1e66865 in void JSPropSetter<CJS_App, &(CJS_App::set_calculate(CJS_Runtime*, v8::Local<v8::Value>))>(char const*, char const*, v8::Local<v8::String>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<void> const&) third_party/pdfium/fxjs/js_define.h:99:13
    #1 0x11da77b in v8::internal::PropertyCallbackArguments::CallAccessorSetter(v8::internal::Handle<v8::internal::AccessorInfo>, v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::Object>) v8/src/api-arguments-inl.h:297:3
   ...

### th...@chromium.org (2018-07-11)

https://pdfium-review.googlesource.com/c/pdfium/+/37510

### bu...@chromium.org (2018-07-11)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f

commit ad1f7b410cd6885bd22d9ee49d9f80d3017f131f
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Jul 11 13:04:43 2018

Check GetObjDefnID() in various JS functions.

Consolidate all the checks into JSGetObject(), and add GetObjDefnID()
methods for classes that are missing it.

BUG=chromium:862059

Change-Id: I2c2b725a01dcd259ef712d2513fcf740cc410b15
Reviewed-on: https://pdfium-review.googlesource.com/37510
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_app.cpp
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_console.h
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/js_define.h
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_color.h
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_console.cpp
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_event.h
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_app.h
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_util.h
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_report.cpp
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_global.cpp
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_global.h
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_color.cpp
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_report.h
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_util.cpp
[modify] https://crrev.com/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f/fxjs/cjs_event.cpp


### es...@chromium.org (2018-07-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/46629048c53ced6353eb92800761deb10a20ffbc

commit 46629048c53ced6353eb92800761deb10a20ffbc
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Wed Jul 11 16:40:58 2018

Roll src/third_party/pdfium b1a4db5551ca..e7e454da8e38 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/b1a4db5551ca..e7e454da8e38


git log b1a4db5551ca..e7e454da8e38 --date=short --no-merges --format='%ad %ae %s'
2018-07-11 art-snake@yandex-team.ru Do not store cross ref v5 obj within document.
2018-07-11 vmiklos@collabora.co.uk Add FPDFFormObj_CountObjects() API
2018-07-11 thestig@chromium.org Check GetObjDefnID() in various JS functions.


Created with:
  gclient setdep -r src/third_party/pdfium@e7e454da8e38

The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:810768,chromium:862059
TBR=dsinclair@chromium.org

Change-Id: I5cdecfe75e8069f179eca07f9eb873cfa875c756
Reviewed-on: https://chromium-review.googlesource.com/1133338
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#574190}
[modify] https://crrev.com/46629048c53ced6353eb92800761deb10a20ffbc/DEPS


### th...@chromium.org (2018-07-11)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-07-12)

Attached cast_global.pdf file can reproduce same cast bug in JSSpecialPropPut method of cjs_global.cpp. JSSpecialPropDel, JSSpecialPropGet and JSSpecialPropQuery methods also has similar code.

Document Javascript Section of cast_global.pdf
----------------------------------------------
g = new global.constructor;
Object.setPrototypeOf(g,app);
g.cc=true;

### th...@chromium.org (2018-07-12)

I did look through the other CFXJS_Engine::GetObjectPrivate() calls but clearly I did a poor job.

### th...@chromium.org (2018-07-12)

One more round: https://pdfium-review.googlesource.com/37670

### bu...@chromium.org (2018-07-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/6aa2190f70a80b70af7bcfe198041756ed8c803e

commit 6aa2190f70a80b70af7bcfe198041756ed8c803e
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Jul 12 13:15:11 2018

Use JSGetObject() in even more places.

BUG=chromium:862059

Change-Id: Id354a5e6dbc037dbb76f901de8311a4f4a4d8940
Reviewed-on: https://pdfium-review.googlesource.com/37670
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/6aa2190f70a80b70af7bcfe198041756ed8c803e/fxjs/cjs_global.cpp


### bu...@chromium.org (2018-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/df1df391ec8f9534d21219ea753c260c4357588b

commit df1df391ec8f9534d21219ea753c260c4357588b
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Thu Jul 12 14:29:37 2018

Roll src/third_party/pdfium 5ff09fb5ee90..6aa2190f70a8 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/5ff09fb5ee90..6aa2190f70a8


git log 5ff09fb5ee90..6aa2190f70a8 --date=short --no-merges --format='%ad %ae %s'
2018-07-12 thestig@chromium.org Use JSGetObject() in even more places.


Created with:
  gclient setdep -r src/third_party/pdfium@6aa2190f70a8

The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:862059
TBR=dsinclair@chromium.org

Change-Id: I1f8681742658f04204fb7df938c0667e814d84c6
Reviewed-on: https://chromium-review.googlesource.com/1134951
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#574556}
[modify] https://crrev.com/df1df391ec8f9534d21219ea753c260c4357588b/DEPS


### th...@chromium.org (2018-07-12)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-07-13)

Hope I got all the bad casts. I also have 2 more cleanup CLs to consolidate CFXJS_Engine::GetObjectPrivate() calls based on the most common usage patterns. So the code base will be down to only 3 callers soon.

https://pdfium-review.googlesource.com/c/pdfium/+/37513
https://pdfium-review.googlesource.com/c/pdfium/+/37811

### sh...@chromium.org (2018-07-13)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-07-13)

We'll need to merge:

https://pdfium.googlesource.com/pdfium/+/ad1f7b410cd6885bd22d9ee49d9f80d3017f131f
https://pdfium.googlesource.com/pdfium/+/6aa2190f70a80b70af7bcfe198041756ed8c803e

### sh...@chromium.org (2018-07-13)

This bug requires manual review: We are only 10 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2018-07-13)

Probably not going to merge to M67, given it's 10 days until M68 stable.

### aw...@chromium.org (2018-07-16)

[Empty comment from Monorail migration]

### ab...@google.com (2018-07-16)

How safe is this merge overall to M68?

### ts...@chromium.org (2018-07-16)

Might also be nice to not even take the
   // It could be a global proxy object.
path unless we know that the ObjDefnID corresponds to an object definition of type FXJSOBJTYPE_GLOBAL.

### th...@chromium.org (2018-07-16)

re: https://crbug.com/chromium/862059#c24: Should be safe.
re: https://crbug.com/chromium/862059#c25: Care to send a CL for that?

### ab...@google.com (2018-07-16)

Approved- branch:3440

### bu...@chromium.org (2018-07-17)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/ff402c2c4ce8ae8690959262ca731d5cc6bd7015

commit ff402c2c4ce8ae8690959262ca731d5cc6bd7015
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jul 17 00:12:56 2018

Check for global flag on global proxy objects.

Second line of defense for issue in the associated bug.

Bug: chromium:862059
Change-Id: I58ba890dfe02c89dd6bcfa23e2e116e107f9adbc
Reviewed-on: https://pdfium-review.googlesource.com/37991
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/ff402c2c4ce8ae8690959262ca731d5cc6bd7015/fxjs/cfxjs_engine.cpp


### bu...@chromium.org (2018-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2a02c684f8fa69e776995b77e183ce6a597fa6e3

commit 2a02c684f8fa69e776995b77e183ce6a597fa6e3
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Tue Jul 17 02:37:59 2018

Roll src/third_party/pdfium 481749905d44..ff402c2c4ce8 (11 commits)

https://pdfium.googlesource.com/pdfium.git/+log/481749905d44..ff402c2c4ce8


git log 481749905d44..ff402c2c4ce8 --date=short --no-merges --format='%ad %ae %s'
2018-07-17 tsepez@chromium.org Check for global flag on global proxy objects.
2018-07-16 tsepez@chromium.org Make JSGetObject<C>() return UnownedPtr<C>.
2018-07-16 tsepez@chromium.org Use UnownedPtr/Optional in cfxa_layoutcontext.cpp
2018-07-16 tsepez@chromium.org Use UnownedPtr<> to v8::Isolates.
2018-07-16 hnakashima@chromium.org Fix crash when typing letters into an XFA datetime field.
2018-07-16 rharrison@chromium.org Alert embedder when attempting to save XFA form
2018-07-16 thestig@chromium.org Fix some nits in CPDF_Document.
2018-07-16 vmiklos@collabora.co.uk Add FPDFFormObj_GetObject() API
2018-07-16 rharrison@chromium.org Process data changes regardless if they can be formatted
2018-07-16 tsepez@chromium.org Use UnownedPtr in CXFA_LocaleMgr
2018-07-16 tsepez@chromium.org Remove unused member from CPDF_DataAvail.


Created with:
  gclient setdep -r src/third_party/pdfium@ff402c2c4ce8

The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:862059,chromium:857521
TBR=dsinclair@chromium.org

Change-Id: I34c5767262f39734719d87120febf1c2c8193a9a
Reviewed-on: https://chromium-review.googlesource.com/1139006
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#575525}
[modify] https://crrev.com/2a02c684f8fa69e776995b77e183ce6a597fa6e3/DEPS


### bu...@chromium.org (2018-07-17)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019

commit b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Jul 17 21:33:37 2018

M68: Check GetObjDefnID() in various JS functions.

Consolidate all the checks into JSGetObject(), and add GetObjDefnID()
methods for classes that are missing it.

BUG=chromium:862059

Change-Id: I2c2b725a01dcd259ef712d2513fcf740cc410b15
Reviewed-on: https://pdfium-review.googlesource.com/37510
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>
(cherry picked from commit ad1f7b410cd6885bd22d9ee49d9f80d3017f131f)
Reviewed-on: https://pdfium-review.googlesource.com/38030
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_app.cpp
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_console.h
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/JS_Define.h
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_color.h
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_console.cpp
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_event.h
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_app.h
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_util.h
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_report.cpp
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_global.cpp
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_global.h
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_color.cpp
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_report.h
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_util.cpp
[modify] https://crrev.com/b6b5a2dcd7cc4302d5f20e21ab637be1b03d1019/fxjs/cjs_event.cpp


### bu...@chromium.org (2018-07-17)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a1c1c63d3454e51ec321cdaa6e3420db2ed6c957

commit a1c1c63d3454e51ec321cdaa6e3420db2ed6c957
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Jul 17 21:34:27 2018

M68: Use JSGetObject() in even more places.

This is a manual merge of commit 6aa2190.

BUG=chromium:862059

Change-Id: Iae0069f1532adc8aea3ac865a4242b00b84d632b
Reviewed-on: https://pdfium-review.googlesource.com/38050
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/a1c1c63d3454e51ec321cdaa6e3420db2ed6c957/fxjs/cjs_global.cpp


### ch...@gmail.com (2018-07-19)

Exploitablity of this bug
---------------------------
Sometimes it is possible to read some values from memory. But not consistently. I attached a test case to demonstrate this issue.

OS: Linux (Because test case depends a lot on behavior of tcmalloc)
    Windows (Shows memory values on very rare occasions)
Chrome Version: 67.0.3396.99 stable

* If you are testing on a debug build, please build tcmalloc with gn flag 
  enable_debugallocation=false. Also debug build should not contain the fix.
 
Steps:
1. Open cast_read.pdf file with chrome.
2. Click "Show Memory" button.
   Wait for about 6-7 seconds.
   PDF files tries to read memory values through "color.red", "color.green" etc. Javascript property accesses. These properties return a Javascript array. If these returned arrays contain values from memory, PDF file will display an Alert with those values.
  If it cannot find any memory values PDF file will display an Alert with a message.
3. If this test case cannot display any memory values please click "Show Memory" button again.
   Also try to close the browser and start again from step 1.

Attached description.png shows what this test case tries to do.
But I am not sure whether that is what happens exactly because returned data is very inconsistent.

Javascript for Test Case
------------------------
OnClick Handler of btn1(Show Memory) button contains the Javascript.
I have added some comments there too.



   





### ch...@gmail.com (2018-07-21)

[Comment Deleted]

### ch...@gmail.com (2018-07-21)

Correction on https://crbug.com/chromium/862059#c32 (Exploitablity of this bug)
----------------------------------------------------
Test case attached on https://crbug.com/chromium/862059#c32 displays values in memory for stable and release builds. But not for the exact reason I mentioned in description.png. CJS_Icon and ArrayBuffer objects are not allocated on adjacent memory locations on release builds as shown in description.png.

Reason: CJS_Icon takes 48 bytes. On a debug build tcmalloc uses size class 64 for CJS_Icon. But on a release build tcmalloc uses size class 48.

Please try attached cast_read_release.pdf, if above test case does not work on stable build. This test case works, but not for the exact reason mentioned in description.png.

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### mb...@google.com (2018-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-07-30)

Nice one! $5,000 for this report :)

### aw...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/862059?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091895)*
