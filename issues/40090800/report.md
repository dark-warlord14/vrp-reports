# Heap-use-after-free in PDFiumEngine::GetVisiblePageIndex

| Field | Value |
|-------|-------|
| **Issue ID** | [40090800](https://issues.chromium.org/issues/40090800) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | hn...@chromium.org |
| **Created** | 2018-03-15 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

## Cause of Bug

Bug is present in below mentioned code in PDFiumEngine::GetVisiblePageIndex(FPDF\_PAGE page) method in pdfium\_engine.cc file.

for (int page\_index : visible\_pages\_) {  

if (pages\_[page\_index]->GetPage() == page)  

return page\_index  

}

It is possible to trigger Format event handler of a Text Field through "pages\_[page\_index]->GetPage()" call.  

Format event handler will execute "a = this.pageNum;" Javascript code.  

That will call PDFiumEngine::CalculateVisiblePages() method in pdfium\_engine.cc file.  

PDFiumEngine::CalculateVisiblePages() method contains below mentioned lines.  

...........  

std::vector<int> formerly\_visible\_pages;  

std::swap(visible\_pages\_, formerly\_visible\_pages);  

...........  

Above lines will invalidate visible\_pages\_ vector which is used in earlier for loop.  

So the next iteration of for loop will crash with a use after free.

## Javascript in visible\_pages.pdf file

## Document Javascript

app.setTimeOut('this.pageNum = 4',1000);  

app.setTimeOut('this.pageNum = 1;',2000);

## Page Close event of First Page

this.getField('txt2').setFocus();

## Format event of "txt1" Text Field on First Page

a = this.pageNum;

**VERSION**  

Chrome Version: [67.0.3371.0] + [Trunk build]  

[65.0.3325.162] + [stable]  

Operating System: [Windows 10, Ubuntu 16.04]

**REPRODUCTION CASE**

## Steps

1. Save test.html and visible\_pages.pdf to same folder.
2. Open chrome
3. Open visible\_pages.pdf.
4. Wait 2 seconds.  
   
   \* Do not click anywhere on PDF file.
5. If above steps did not crash PDF plugin, then open test.html.
6. Wait for 2 seconds.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF plugin process]  

Crash State: Address Sanitizer output

=2852==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000017954 at pc 0x55b1930c134b bp 0x7ffedd59f3b0 sp 0x7ffedd59f3a8  

READ of size 4 at 0x602000017954 thread T0 (chrome)  

#0 0x55b1930c134a in GetVisiblePageIndex /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:3745:23  

#1 0x55b1930c134a in chrome\_pdf::PDFiumEngine::Form\_Invalidate(\_FPDF\_FORMFILLINFO\*, void\*, double, double, double, double) /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:4046:0  

#2 0x55b1931671c9 in CFX\_SystemHandler::InvalidateRect(CPDFSDK\_Widget\*, CFX\_FloatRect const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cfx\_systemhandler.cpp:62:19  

#3 0x55b19376404f in CPWL\_Wnd::InvalidateRect(CFX\_FloatRect\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_wnd.cpp:300:12  

#4 0x55b19372b61e in CPWL\_Caret::InvalidateRect(CFX\_FloatRect\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_caret.cpp:119:22  

#5 0x55b19376b4de in CPWL\_Wnd::SetVisible(bool) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_wnd.cpp:577:10  

#6 0x55b19372b0b8 in CPWL\_Caret::SetCaret(bool, CFX\_PTemplate<float> const&, CFX\_PTemplate<float> const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_caret.cpp:84:15  

#7 0x55b19372a0e0 in CPWL\_EditCtrl::SetCaret(bool, CFX\_PTemplate<float> const&, CFX\_PTemplate<float> const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_edit\_ctrl.cpp:342:17  

#8 0x55b193723043 in CPWL\_Edit::OnKillFocus() /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_edit.cpp:367:8  

#9 0x55b19376a690 in CPWL\_MsgControl::KillFocus() /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_wnd.cpp:89:15  

#10 0x55b19319d505 in CFFL\_FormFiller::KillFocusForAnnot(CPDFSDK\_Annot\*, unsigned int) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/formfiller/cffl\_formfiller.cpp:267:11  

#11 0x55b1931a5c9a in CFFL\_InteractiveFormFiller::OnKillFocus(fxcrt::Observable<CPDFSDK\_Annot>::ObservedPtr\*, unsigned int) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/formfiller/cffl\_interactiveformfiller.cpp:422:16  

#12 0x55b193164cd6 in CPDFSDK\_FormFillEnvironment::KillFocusAnnot(unsigned int) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:714:23  

#13 0x55b1931660e8 in CPDFSDK\_FormFillEnvironment::RemovePageView(CPDF\_Page\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:638:5  

#14 0x55b193115fd2 in chrome\_pdf::PDFiumPage::Unload() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_page.cc:116:7  

#15 0x55b1930c6075 in chrome\_pdf::PDFiumEngine::CalculateVisiblePages() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:3204:20  

#16 0x55b1930c6c88 in chrome\_pdf::PDFiumEngine::ScrolledToYPosition(int) /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:1074:3  

#17 0x55b19309822b in chrome\_pdf::OutOfProcessInstance::HandleMessage(pp::Var const&) /home/chamal/chromium/src/out/asan/../../pdf/out\_of\_process\_instance.cc:582:14  

#18 0x55b183c99693 in pp::Messaging\_HandleMessage(int, PP\_Var) /home/chamal/chromium/src/out/asan/../../ppapi/cpp/module.cc:141:13  

#19 0x55b190800e32 in CallWhileUnlocked<void, int, PP\_Var, int, PP\_Var> /home/chamal/chromium/src/out/asan/../../ppapi/shared\_impl/proxy\_lock.h:135:10  

#20 0x55b190800e32 in ppapi::proxy::PPP\_Messaging\_Proxy::OnMsgHandleMessage(int, ppapi::proxy::SerializedVarReceiveInput) /home/chamal/chromium/src/out/asan/../../ppapi/proxy/ppp\_messaging\_proxy.cc:110:0  

#21 0x55b1908007a3 in DispatchToMethodImpl<ppapi::proxy::PPP\_Messaging\_Proxy \*, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput), std::\_\_1::tuple<int, ppapi::proxy::SerializedVar>, 0, 1> /home/chamal/chromium/src/out/asan/../../base/tuple.h:52:3  

#22 0x55b1908007a3 in DispatchToMethod<ppapi::proxy::PPP\_Messaging\_Proxy \*, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput), std::\_\_1::tuple<int, ppapi::proxy::SerializedVar> > /home/chamal/chromium/src/out/asan/../../base/tuple.h:60:0  

#23 0x55b1908007a3 in DispatchToMethod<ppapi::proxy::PPP\_Messaging\_Proxy, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput), void, std::\_\_1::tuple<int, ppapi::proxy::SerializedVar> > /home/chamal/chromium/src/out/asan/../../ipc/ipc\_message\_templates.h:51:0  

#24 0x55b1908007a3 in bool IPC::MessageT<PpapiMsg\_PPPMessaging\_HandleMessage\_Meta, std::\_\_1::tuple<int, ppapi::proxy::SerializedVar>, void>::Dispatch<ppapi::proxy::PPP\_Messaging\_Proxy, ppapi::proxy::PPP\_Messaging\_Proxy, void, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput)>(IPC::Message const\*, ppapi::proxy::PPP\_Messaging\_Proxy\*, ppapi::proxy::PPP\_Messaging\_Proxy\*, void\*, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput)) /home/chamal/chromium/src/out/asan/../../ipc/ipc\_message\_templates.h:146:0  

#25 0x55b1908004de in ppapi::proxy::PPP\_Messaging\_Proxy::OnMessageReceived(IPC::Message const&) /home/chamal/chromium/src/out/asan/../../ppapi/proxy/ppp\_messaging\_proxy.cc:77:5  

#26 0x55b190767194 in ppapi::proxy::PluginDispatcher::OnMessageReceived(IPC::Message const&) /home/chamal/chromium/src/out/asan/../../ppapi/proxy/plugin\_dispatcher.cc:273:22  

#27 0x55b185d51eda in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /home/chamal/chromium/src/out/asan/../../ipc/ipc\_channel\_proxy.cc:320:14  

#28 0x55b1848f9f50 in Run /home/chamal/chromium/src/out/asan/../../base/callback.h:95:12  

#29 0x55b1848f9f50 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) /home/chamal/chromium/src/out/asan/../../base/debug/task\_annotator.cc:61:0  

#30 0x55b18495c2c5 in base::MessageLoop::RunTask(base::PendingTask\*) /home/chamal/chromium/src/out/asan/../../base/message\_loop/message\_loop.cc:395:25  

#31 0x55b18495d574 in DeferOrRunPendingTask /home/chamal/chromium/src/out/asan/../../base/message\_loop/message\_loop.cc:407:5  

#32 0x55b18495d574 in base::MessageLoop::DoWork() /home/chamal/chromium/src/out/asan/../../base/message\_loop/message\_loop.cc:451:0  

#33 0x55b184964caf in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /home/chamal/chromium/src/out/asan/../../base/message\_loop/message\_pump\_default.cc:37:31  

#34 0x55b1849de8a1 in base::RunLoop::Run() /home/chamal/chromium/src/out/asan/../../base/run\_loop.cc:133:14  

#35 0x55b183c3f221 in content::PpapiPluginMain(content::MainFunctionParams const&) /home/chamal/chromium/src/out/asan/../../content/ppapi\_plugin/ppapi\_plugin\_main.cc:161:19  

#36 0x55b183f04488 in content::RunZygote(content::ContentMainDelegate\*) /home/chamal/chromium/src/out/asan/../../content/app/content\_main\_runner.cc:352:14  

#37 0x55b183f07322 in content::ContentMainRunnerImpl::Run() /home/chamal/chromium/src/out/asan/../../content/app/content\_main\_runner.cc:703:12  

#38 0x55b183f2bbab in service\_manager::Main(service\_manager::MainParams const&) /home/chamal/chromium/src/out/asan/../../services/service\_manager/embedder/main.cc:453:29  

#39 0x55b183f03d48 in content::ContentMain(content::ContentMainParams const&) /home/chamal/chromium/src/out/asan/../../content/app/content\_main.cc:19:10  

#40 0x55b17da7a4a6 in ChromeMain /home/chamal/chromium/src/out/asan/../../chrome/app/chrome\_main.cc:101:12  

#41 0x7f380911482f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

0x602000017954 is located 4 bytes inside of 16-byte region [0x602000017950,0x602000017960)  

freed by thread T0 (chrome) here:  

#0 0x55b17da78022 in operator delete(void\*) *asan\_rtl*:3  

#1 0x55b1930c6678 in \_\_libcpp\_deallocate /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/new:236:3  

#2 0x55b1930c6678 in deallocate /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1796:0  

#3 0x55b1930c6678 in deallocate /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1555:0  

#4 0x55b1930c6678 in ~\_\_vector\_base /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/vector:442:0  

#5 0x55b1930c6678 in chrome\_pdf::PDFiumEngine::CalculateVisiblePages() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:3232:0  

#6 0x55b1930e5909 in chrome\_pdf::PDFiumEngine::GetMostVisiblePage() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2782:3  

#7 0x55b1930c24e4 in chrome\_pdf::PDFiumEngine::Form\_GetCurrentPage(\_FPDF\_FORMFILLINFO\*, void\*) /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:4140:21  

#8 0x55b19316579a in GetCurrentPage /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:295:12  

#9 0x55b19316579a in CPDFSDK\_FormFillEnvironment::GetCurrentView() /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:568:0  

#10 0x55b193639731 in CJS\_Document::get\_page\_num(CJS\_Runtime\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_document.cpp:184:49  

#11 0x55b19364ee0c in void JSPropGetter<CJS\_Document, &CJS\_Document::get\_page\_num>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fxjs/JS\_Define.h:76:23  

#12 0x55b182a4712d in v8::internal::PropertyCallbackArguments::BasicCallNamedGetterCallback(void (\*)(v8::Local[v8::Name](javascript:void(0);), v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) /home/chamal/chromium/src/out/asan/../../v8/src/api-arguments-inl.h:115:3  

#13 0x55b182c07f73 in CallAccessorGetter /home/chamal/chromium/src/out/asan/../../v8/src/api-arguments-inl.h:258:10  

#14 0x55b182c07f73 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator\*) /home/chamal/chromium/src/out/asan/../../v8/src/objects.cc:1502:0  

#15 0x55b182c05bee in v8::internal::Object::GetProperty(v8::internal::LookupIterator\*) /home/chamal/chromium/src/out/asan/../../v8/src/objects.cc:1022:16  

#16 0x55b182a111a2 in v8::internal::LoadIC::Load(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);)) /home/chamal/chromium/src/out/asan/../../v8/src/ic/ic.cc:476:5  

#17 0x55b182a29fe6 in \_\_RT\_impl\_Runtime\_LoadIC\_Miss /home/chamal/chromium/src/out/asan/../../v8/src/ic/ic.cc:2178:5  

#18 0x55b182a29fe6 in v8::internal::Runtime\_LoadIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) /home/chamal/chromium/src/out/asan/../../v8/src/ic/ic.cc:2162:0  

#12 0x7e955d2858bc (<unknown module>)  

#13 0x7e955d305061 (<unknown module>)  

#14 0x7e955d295677 (<unknown module>)  

#15 0x7e955d292794 (<unknown module>)  

#16 0x7e955d2866c0 (<unknown module>)  

#19 0x55b1827d8239 in Call /home/chamal/chromium/src/out/asan/../../v8/src/simulator.h:110:12  

#20 0x55b1827d8239 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) /home/chamal/chromium/src/out/asan/../../v8/src/execution.cc:153:0  

#21 0x55b1827d79d3 in CallInternal /home/chamal/chromium/src/out/asan/../../v8/src/execution.cc:189:10  

#22 0x55b1827d79d3 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) /home/chamal/chromium/src/out/asan/../../v8/src/execution.cc:200:0  

#23 0x55b181e047e1 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) /home/chamal/chromium/src/out/asan/../../v8/src/api.cc:2132:7  

#24 0x55b193625f6e in CFXJS\_Engine::Execute(fxcrt::WideString const&, FXJSErr\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fxjs/cfxjs\_engine.cpp:520:25  

#25 0x55b19361e767 in CJS\_Runtime::ExecuteScript(fxcrt::WideString const&, fxcrt::WideString\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_runtime.cpp:207:14  

#26 0x55b1936beec7 in CJS\_EventContext::RunScript(fxcrt::WideString const&, fxcrt::WideString\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_event\_context.cpp:53:24  

#27 0x55b19315c3c7 in CPDFSDK\_InterForm::OnFormat(CPDF\_FormField\*, bool&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_interform.cpp:330:31  

#28 0x55b193154019 in CPDFSDK\_Widget::OnFormat(bool&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widget.cpp:663:24  

#29 0x55b1931510fa in CPDFSDK\_WidgetHandler::OnLoad(CPDFSDK\_Annot\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widgethandler.cpp:235:34  

#30 0x55b19314164d in CPDFSDK\_PageView::LoadFXAnnots() /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:467:23  

#31 0x55b193165688 in CPDFSDK\_FormFillEnvironment::GetPageView(CPDF\_Page\*, bool) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:562:14  

#32 0x55b19313d337 in FormHandleToPageView /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:120:39  

#33 0x55b19313d337 in FORM\_OnAfterLoadPage /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:749:0  

#34 0x55b193116261 in chrome\_pdf::PDFiumPage::GetPage() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_page.cc:132:7

previously allocated by thread T0 (chrome) here:  

#0 0x55b17da77442 in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55b17e3910b2 in \_\_allocate /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/new:228:10  

#2 0x55b17e3910b2 in allocate /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1793:0  

#3 0x55b17e3910b2 in allocate /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1547:0  

#4 0x55b17e3910b2 in \_\_split\_buffer /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:311:0  

#5 0x55b17e3910b2 in void std::\_\_1::vector<int, std::\_\_1::allocator<int> >::\_\_push\_back\_slow\_path<int const&>(int const&) /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/vector:1578:0  

#6 0x55b1930c608c in push\_back /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/vector:1599:9  

#7 0x55b1930c608c in chrome\_pdf::PDFiumEngine::CalculateVisiblePages() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:3191:0  

#8 0x55b1930c6c88 in chrome\_pdf::PDFiumEngine::ScrolledToYPosition(int) /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:1074:3  

#9 0x55b19309822b in chrome\_pdf::OutOfProcessInstance::HandleMessage(pp::Var const&) /home/chamal/chromium/src/out/asan/../../pdf/out\_of\_process\_instance.cc:582:14  

#10 0x55b183c99693 in pp::Messaging\_HandleMessage(int, PP\_Var) /home/chamal/chromium/src/out/asan/../../ppapi/cpp/module.cc:141:13  

#11 0x55b190800e32 in CallWhileUnlocked<void, int, PP\_Var, int, PP\_Var> /home/chamal/chromium/src/out/asan/../../ppapi/shared\_impl/proxy\_lock.h:135:10  

#12 0x55b190800e32 in ppapi::proxy::PPP\_Messaging\_Proxy::OnMsgHandleMessage(int, ppapi::proxy::SerializedVarReceiveInput) /home/chamal/chromium/src/out/asan/../../ppapi/proxy/ppp\_messaging\_proxy.cc:110:0  

#13 0x55b1908007a3 in DispatchToMethodImpl<ppapi::proxy::PPP\_Messaging\_Proxy \*, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput), std::\_\_1::tuple<int, ppapi::proxy::SerializedVar>, 0, 1> /home/chamal/chromium/src/out/asan/../../base/tuple.h:52:3  

#14 0x55b1908007a3 in DispatchToMethod<ppapi::proxy::PPP\_Messaging\_Proxy \*, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput), std::\_\_1::tuple<int, ppapi::proxy::SerializedVar> > /home/chamal/chromium/src/out/asan/../../base/tuple.h:60:0  

#15 0x55b1908007a3 in DispatchToMethod<ppapi::proxy::PPP\_Messaging\_Proxy, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput), void, std::\_\_1::tuple<int, ppapi::proxy::SerializedVar> > /home/chamal/chromium/src/out/asan/../../ipc/ipc\_message\_templates.h:51:0  

#16 0x55b1908007a3 in bool IPC::MessageT<PpapiMsg\_PPPMessaging\_HandleMessage\_Meta, std::\_\_1::tuple<int, ppapi::proxy::SerializedVar>, void>::Dispatch<ppapi::proxy::PPP\_Messaging\_Proxy, ppapi::proxy::PPP\_Messaging\_Proxy, void, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput)>(IPC::Message const\*, ppapi::proxy::PPP\_Messaging\_Proxy\*, ppapi::proxy::PPP\_Messaging\_Proxy\*, void\*, void (ppapi::proxy::PPP\_Messaging\_Proxy::\*)(int, ppapi::proxy::SerializedVarReceiveInput)) /home/chamal/chromium/src/out/asan/../../ipc/ipc\_message\_templates.h:146:0  

#17 0x55b1908004de in ppapi::proxy::PPP\_Messaging\_Proxy::OnMessageReceived(IPC::Message const&) /home/chamal/chromium/src/out/asan/../../ppapi/proxy/ppp\_messaging\_proxy.cc:77:5  

#18 0x55b190767194 in ppapi::proxy::PluginDispatcher::OnMessageReceived(IPC::Message const&) /home/chamal/chromium/src/out/asan/../../ppapi/proxy/plugin\_dispatcher.cc:273:22  

#19 0x55b185d51eda in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /home/chamal/chromium/src/out/asan/../../ipc/ipc\_channel\_proxy.cc:320:14  

#20 0x55b1848f9f50 in Run /home/chamal/chromium/src/out/asan/../../base/callback.h:95:12  

#21 0x55b1848f9f50 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) /home/chamal/chromium/src/out/asan/../../base/debug/task\_annotator.cc:61:0  

#22 0x55b18495c2c5 in base::MessageLoop::RunTask(base::PendingTask\*) /home/chamal/chromium/src/out/asan/../../base/message\_loop/message\_loop.cc:395:25  

#23 0x55b18495d574 in DeferOrRunPendingTask /home/chamal/chromium/src/out/asan/../../base/message\_loop/message\_loop.cc:407:5  

#24 0x55b18495d574 in base::MessageLoop::DoWork() /home/chamal/chromium/src/out/asan/../../base/message\_loop/message\_loop.cc:451:0  

#25 0x55b184964caf in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /home/chamal/chromium/src/out/asan/../../base/message\_loop/message\_pump\_default.cc:37:31  

#26 0x55b1849de8a1 in base::RunLoop::Run() /home/chamal/chromium/src/out/asan/../../base/run\_loop.cc:133:14  

#27 0x55b183c3f221 in content::PpapiPluginMain(content::MainFunctionParams const&) /home/chamal/chromium/src/out/asan/../../content/ppapi\_plugin/ppapi\_plugin\_main.cc:161:19  

#28 0x55b183f04488 in content::RunZygote(content::ContentMainDelegate\*) /home/chamal/chromium/src/out/asan/../../content/app/content\_main\_runner.cc:352:14  

#29 0x55b183f07322 in content::ContentMainRunnerImpl::Run() /home/chamal/chromium/src/out/asan/../../content/app/content\_main\_runner.cc:703:12  

#30 0x55b183f2bbab in service\_manager::Main(service\_manager::MainParams const&) /home/chamal/chromium/src/out/asan/../../services/service\_manager/embedder/main.cc:453:29  

#31 0x55b183f03d48 in content::ContentMain(content::ContentMainParams const&) /home/chamal/chromium/src/out/asan/../../content/app/content\_main.cc:19:10  

#32 0x55b17da7a4a6 in ChromeMain /home/chamal/chromium/src/out/asan/../../chrome/app/chrome\_main.cc:101:12  

#33 0x7f380911482f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

## Attachments

- [test.html](attachments/test.html) (text/plain, 96 B)
- [visible_pages.pdf](attachments/visible_pages.pdf) (application/pdf, 3.2 KB)
- [visible_pages_2.pdf](attachments/visible_pages_2.pdf) (application/pdf, 3.1 KB)

## Timeline

### do...@chromium.org (2018-03-15)

Thanks for the report.

+PDF folks, do you mind following up here? Seems like a case where we need to avoid mutating the container that's being iterated over. Thanks!

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2018-03-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5506232815976448.

### ch...@gmail.com (2018-03-15)

Please try this test case ,if ClusterFuzz can't reproduce the test case attached with issue report.
I removed "setTimeOut" calls in Document JavaScript section from this test case.

### sh...@chromium.org (2018-03-15)

[Empty comment from Monorail migration]

### ds...@chromium.org (2018-03-15)

hnakashima@ can you please take a look? I'd guess this needs one of those pointer wrappers to make sure the thing we're checking against doesn't go away.

### hn...@chromium.org (2018-03-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-03-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6300062695817216.

### bu...@chromium.org (2018-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/94b3728a2836da335a10085d4089c9d8e1c9d225

commit 94b3728a2836da335a10085d4089c9d8e1c9d225
Author: Henrique Nakashima <hnakashima@chromium.org>
Date: Thu Mar 15 21:11:33 2018

Copy visible_pages_ when iterating over it.

On this case, a call inside the loop may cause visible_pages_ to
change.

Bug: 822091
Change-Id: I41b0715faa6fe3e39203cd9142cf5ea38e59aefb
Reviewed-on: https://chromium-review.googlesource.com/964592
Reviewed-by: dsinclair <dsinclair@chromium.org>
Commit-Queue: Henrique Nakashima <hnakashima@chromium.org>
Cr-Commit-Position: refs/heads/master@{#543494}
[modify] https://crrev.com/94b3728a2836da335a10085d4089c9d8e1c9d225/pdf/pdfium/pdfium_engine.cc


### hn...@chromium.org (2018-03-15)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-03-16)

Is security_severity-medium correct for this issue?

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-20)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-20)

Approved for 66. Branch:3359

### bu...@chromium.org (2018-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b2ecebcb4b84e7bedc44661cd3bfde5acf62bcad

commit b2ecebcb4b84e7bedc44661cd3bfde5acf62bcad
Author: Henrique Nakashima <hnakashima@chromium.org>
Date: Tue Mar 20 16:39:01 2018

Copy visible_pages_ when iterating over it.

On this case, a call inside the loop may cause visible_pages_ to
change.

Bug: 822091
Change-Id: I41b0715faa6fe3e39203cd9142cf5ea38e59aefb
Reviewed-on: https://chromium-review.googlesource.com/964592
Reviewed-by: dsinclair <dsinclair@chromium.org>
Commit-Queue: Henrique Nakashima <hnakashima@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#543494}(cherry picked from commit 94b3728a2836da335a10085d4089c9d8e1c9d225)
Reviewed-on: https://chromium-review.googlesource.com/971121
Cr-Commit-Position: refs/branch-heads/3359@{#343}
Cr-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}
[modify] https://crrev.com/b2ecebcb4b84e7bedc44661cd3bfde5acf62bcad/pdf/pdfium/pdfium_engine.cc


### aw...@chromium.org (2018-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-26)

Thanks Chamal! The VRP panel decided to award $5,000 for this report.  Cheers!

### aw...@chromium.org (2018-03-26)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/822091?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090800)*
