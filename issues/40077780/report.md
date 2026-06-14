# Heap-use-after-free in xsltApplySequenceConstructor

| Field | Value |
|-------|-------|
| **Issue ID** | [40077780](https://issues.chromium.org/issues/40077780) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2013-07-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the asan build of chrome (asan-symbolized-linux-release-211418). The stack backtrace and testcase indicate an issue with object tags being created while XSL is evaluated.

**VERSION**  

Chrome Version: asan build 211418  

Operating System: Linux 64-Bit

**REPRODUCTION CASE**  

The attached zip file contains several files. Loading the crash.html in chrome will lead to the crash. It is a little unreliable and might require several attempts. Reloading the page does not work to make it more reliable (maybe an issue with caching).

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: asan output attached

## Attachments

- [crash.log](attachments/crash.log) (text/plain; charset=us-ascii, 16.8 KB)
- [crash_xsl.zip](attachments/crash_xsl.zip) (application/zip; charset=binary, 13.3 KB)

## Timeline

### in...@chromium.org (2013-07-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-07-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5758226951831552

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61300004c990
Crash State:
  - crash stack -
  xsltApplySequenceConstructor
  xsltApplyXSLTTemplate
  - free stack -
  xsltFreeStylePreComps
  xsltFreeStylesheet
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=193542:193554

Minimized Testcase (2.95 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9753bG910Z6SA5K_eDBwhmTLPiVYNRkcXJqYQyZ-uRbO6pHi3r48qOiqwEyMULJTYkBax1Yfraw1iOVManlrDfxXtTQV6jdTMs078riFJ_sW43jYudc9rVo85DsG--UGnWbPD1K2gwHgajetxmzuNeB8hVFAQ



### in...@chromium.org (2013-07-15)

Daniel, can you please help to take a look.

### in...@chromium.org (2013-07-15)

In the regression range, i only see this that might be related - enabling of the threaded html parser - http://src.chromium.org/viewvc/chrome?view=rev&revision=193554. Adam, do you think it could be related to this xslt issue ?

### ab...@chromium.org (2013-07-15)

That's possible.  You can try --disable-threaded-html-parser to see if that removes the crash.

### in...@chromium.org (2013-07-15)

verified locally that adding --disable-threaded-html-parser fixes the crash. 

To reproduce reliably, we need to start multiple chrome instances at once (i did 10 using a script).

### ve...@gmail.com (2013-07-16)

I can't access the test:

  https://cluster-fuzz.appspot.com/download/AMIfv9753bG910Z6SA5K_eDBwhmTLPiVYNRkcXJqYQyZ-uRbO6pHi3r48qOiqwEyMULJTYkBax1Yfraw1iOVManlrDfxXtTQV6jdTMs078riFJ_sW43jYudc9rVo85DsG--UGnWbPD1K2gwHgajetxmzuNeB8hVFAQ

You (veillard@gmail.com) are not authorized to access this page!

For access, please contact Abhishek Arya (inferno [at] chromium [dot] org).

Daniel

### in...@chromium.org (2013-07-16)

Daniel, it is the same as in https://crbug.com/chromium/260105#c0. You should be able to download that attachment.

READ of size 8 at 0x6170000ad610 thread T0 (chrome)
    #0 0x7fb7133b9b11 in xsltApplySequenceConstructor src/third_party/libxslt/libxslt/transform.c:2588
    #1 0x7fb7133b76ca in xsltApplyXSLTTemplate src/third_party/libxslt/libxslt/transform.c:3044
    #2 0x7fb7133b5568 in xsltProcessOneNode src/third_party/libxslt/libxslt/transform.c:2045
    #3 0x7fb7133c6f35 in xsltApplyStylesheetInternal src/third_party/libxslt/libxslt/transform.c:6049
    #4 0x7fb70f40c978 in WebCore::XSLTProcessor::transformToString(WebCore::Node*, WTF::String&, WTF::String&, WTF::String&) src/third_party/WebKit/Source/core/xml/XSLTProcessorLibxslt.cpp:327
    #5 0x7fb70e087b2f in WebCore::Document::applyXSLTransform(WebCore::ProcessingInstruction*) src/third_party/WebKit/Source/core/dom/Document.cpp:3904
    #6 0x7fb70e198255 in WebCore::StyleSheetCollection::collectStyleSheets(WebCore::DocumentStyleSheetCollection*, WTF::Vector<WTF::RefPtr<WebCore::StyleSheet>, 0ul>&, WTF::Vector<WTF::RefPtr<WebCore::CSSStyleSheet>, 0ul>&) src/third_party/WebKit/Source/core/dom/StyleSheetCollection.cpp:104
    #7 0x7fb70e198fbc in WebCore::StyleSheetCollection::updateActiveStyleSheets(WebCore::DocumentStyleSheetCollection*, WebCore::StyleResolverUpdateMode, WebCore::StyleSheetCollection::StyleResolverUpdateType&) src/third_party/WebKit/Source/core/dom/StyleSheetCollection.cpp:261
    #8 0x7fb70e0d8299 in WebCore::DocumentStyleSheetCollection::updateActiveStyleSheets(WebCore::StyleResolverUpdateMode) src/third_party/WebKit/Source/core/dom/DocumentStyleSheetCollection.cpp:270
    #9 0x7fb70e0788bb in WebCore::Document::styleResolverChanged(WebCore::StyleResolverUpdateType, WebCore::StyleResolverUpdateMode) src/third_party/WebKit/Source/core/dom/Document.cpp:2979
    #10 0x7fb70e07df6f in WebCore::Document::didRemoveAllPendingStylesheet() src/third_party/WebKit/Source/core/dom/Document.cpp:2593
    #11 0x7fb70e16427f in WebCore::ProcessingInstruction::sheetLoaded() src/third_party/WebKit/Source/core/dom/ProcessingInstruction.cpp:192
    #12 0x7fb70f53d066 in WebCore::XSLImportRule::setXSLStyleSheet(WTF::String const&, WebCore::KURL const&, WTF::String const&) src/third_party/WebKit/Source/core/xml/XSLImportRule.cpp:66
    #13 0x7fb70f283bfd in WebCore::CachedXSLStyleSheet::checkNotify() src/third_party/WebKit/Source/core/loader/cache/CachedXSLStyleSheet.cpp:76
    #14 0x7fb70f2637a4 in WebCore::CachedResource::finish(double) src/third_party/WebKit/Source/core/loader/cache/CachedResource.cpp:255
    #15 0x7fb70f23af90 in WebCore::ResourceLoader::didFinishLoading(WebCore::ResourceHandle*, double) src/third_party/WebKit/Source/core/loader/ResourceLoader.cpp:382
    #16 0x7fb712e67003 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(int, bool, std::string const&, base::TimeTicks const&) src/webkit/glue/weburlloader_impl.cc:727
    #17 0x7fb713682968 in content::ResourceDispatcher::OnRequestComplete(int, int, bool, std::string const&, base::TimeTicks const&) src/content/child/resource_dispatcher.cc:513
    #18 0x7fb7136844aa in bool ResourceMsg_RequestComplete::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::*)(int, int, bool, std::string const&, base::TimeTicks const&)>(IPC::Message const*, content::ResourceDispatcher*, content::ResourceDispatcher*, void (content::ResourceDispatcher::*)(int, int, bool, std::string const&, base::TimeTicks const&)) src/content/common/resource_messages.h:263
    #19 0x7fb713680724 in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) src/content/child/resource_dispatcher.cc:615
    #20 0x7fb71367fa88 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) src/content/child/resource_dispatcher.cc:305
    #21 0x7fb71360aa8d in content::ChildThread::OnMessageReceived(IPC::Message const&) src/content/child/child_thread.cc:275
    #22 0x7fb70cf9c86c in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) src/ipc/ipc_channel_proxy.cc:264
    #23 0x7fb70cfa45f4 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) src/base/bind_internal.h:898
    #24 0x7fb71144fd44 in base::MessageLoop::RunTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:497
    #25 0x7fb7114506ab in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:509
    #26 0x7fb711450a11 in base::MessageLoop::DoWork() src/base/message_loop/message_loop.cc:703
    #27 0x7fb71145d96e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) src/base/message_loop/message_pump_default.cc:29
    #28 0x7fb71144f387 in base::MessageLoop::RunInternal() src/base/message_loop/message_loop.cc:451
    #29 0x7fb71149ccb9 in base::RunLoop::Run() src/base/run_loop.cc:45
    #30 0x7fb71144e0cd in base::MessageLoop::Run() src/base/message_loop/message_loop.cc:331
    #31 0x7fb711ee1b8e in content::RendererMain(content::MainFunctionParams const&) src/content/renderer/renderer_main.cc:247
    #32 0x7fb711965816 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:389
    #33 0x7fb711966178 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:445
    #34 0x7fb711967040 in content::ContentMainRunnerImpl::Run() src/content/app/content_main_runner.cc:757
    #35 0x7fb711964ed2 in content::ContentMain(int, char const**, content::ContentMainDelegate*) src/content/app/content_main.cc:35
    #36 0x7fb70bcb4cf6 in ChromeMain src/chrome/app/chrome_main.cc:32
    #37 0x7fb70bcb4c3a in main src/chrome/app/chrome_exe_main_gtk.cc:43
    #38 0x7fb70247176c in ?? ??
    #39 0x7fb70bcb4b5c in _start ??
0x6170000ad610 is located 16 bytes inside of 312-byte region [0x6170000ad600,0x6170000ad738)
freed by thread T0 (chrome) here:
    #0 0x7fb70bca2a25 in __interceptor_free _asan_rtl_
    #1 0x7fb7133aaaf4 in xsltFreeStylePreComps src/third_party/libxslt/libxslt/preproc.c:1947
    #2 0x7fb7133d0ebb in xsltFreeStylesheet src/third_party/libxslt/libxslt/xslt.c:960
    #3 0x7fb7133d6756 in xsltParseStylesheetImportedDoc src/third_party/libxslt/libxslt/xslt.c:6638
    #4 0x7fb7133d6d5b in xsltParseStylesheetDoc src/third_party/libxslt/libxslt/xslt.c:6666
    #5 0x7fb70f40a143 in WebCore::XSLStyleSheet::compileStyleSheet() src/third_party/WebKit/Source/core/xml/XSLStyleSheetLibxslt.cpp:232
    #6 0x7fb70f40d3e8 in WebCore::xsltStylesheetPointer(WTF::RefPtr<WebCore::XSLStyleSheet>&, WebCore::Node*) src/third_party/WebKit/Source/core/xml/XSLTProcessorLibxslt.cpp:241
    #7 0x7fb70f40c743 in WebCore::XSLTProcessor::transformToString(WebCore::Node*, WTF::String&, WTF::String&, WTF::String&) src/third_party/WebKit/Source/core/xml/XSLTProcessorLibxslt.cpp:284
    #8 0x7fb70e087b2f in WebCore::Document::applyXSLTransform(WebCore::ProcessingInstruction*) src/third_party/WebKit/Source/core/dom/Document.cpp:3904
    #9 0x7fb70e198255 in WebCore::StyleSheetCollection::collectStyleSheets(WebCore::DocumentStyleSheetCollection*, WTF::Vector<WTF::RefPtr<WebCore::StyleSheet>, 0ul>&, WTF::Vector<WTF::RefPtr<WebCore::CSSStyleSheet>, 0ul>&) src/third_party/WebKit/Source/core/dom/StyleSheetCollection.cpp:104
    #10 0x7fb70e198fbc in WebCore::StyleSheetCollection::updateActiveStyleSheets(WebCore::DocumentStyleSheetCollection*, WebCore::StyleResolverUpdateMode, WebCore::StyleSheetCollection::StyleResolverUpdateType&) src/third_party/WebKit/Source/core/dom/StyleSheetCollection.cpp:261
    #11 0x7fb70e0d8299 in WebCore::DocumentStyleSheetCollection::updateActiveStyleSheets(WebCore::StyleResolverUpdateMode) src/third_party/WebKit/Source/core/dom/DocumentStyleSheetCollection.cpp:270
    #12 0x7fb70e0788bb in WebCore::Document::styleResolverChanged(WebCore::StyleResolverUpdateType, WebCore::StyleResolverUpdateMode) src/third_party/WebKit/Source/core/dom/Document.cpp:2979
    #13 0x7fb70e07868f in WebCore::Document::updateLayoutIgnorePendingStylesheets() src/third_party/WebKit/Source/core/dom/Document.cpp:1756
    #14 0x7fb70d875075 in WebCore::HTMLObjectElement::renderWidgetForJSBindings() const src/third_party/WebKit/Source/core/html/HTMLObjectElement.cpp:74
    #15 0x7fb70d7e0193 in WebCore::HTMLPlugInElement::pluginWidget() const src/third_party/WebKit/Source/core/html/HTMLPlugInElement.cpp:143
    #16 0x7fb70d7e05a4 in WebCore::HTMLPlugInElement::getInstance() src/third_party/WebKit/Source/core/html/HTMLPlugInElement.cpp:116
    #17 0x7fb70e7f4cfb in void WebCore::npObjectNamedGetter<WebCore::V8HTMLObjectElement>(v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) src/third_party/WebKit/Source/bindings/v8/custom/V8HTMLPlugInElementCustom.cpp:50
    #18 0x7fb70e3d8fb3 in WebCore::HTMLObjectElementV8Internal::namedPropertyGetterCallback(v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) src/out/Release/gen/webkit/bindings/V8HTMLObjectElement.cpp:691
    #19 0x7fb710c36d6e in v8::internal::PropertyCallbackArguments::Call(v8::Handle<v8::Value> (*)(v8::Local<v8::String>, v8::AccessorInfo const&), v8::Local<v8::String>) src/v8/src/arguments.cc:196
    #20 0x7fb710ed37b4 in v8::internal::JSObject::GetPropertyWithInterceptor(v8::internal::Object*, v8::internal::Name*, PropertyAttributes*) src/v8/src/objects.cc:12781
    #21 0x7fb710ece530 in v8::internal::Object::GetProperty(v8::internal::Object*, v8::internal::LookupResult*, v8::internal::Name*, PropertyAttributes*) src/v8/src/objects.cc:875
    #22 0x7fb710ed2c1f in v8::internal::Object::GetProperty(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::LookupResult*, v8::internal::Handle<v8::internal::Name>, PropertyAttributes*) src/v8/src/objects.cc:782
    #23 0x7fb710df10c2 in v8::internal::LoadIC::Load(v8::internal::InlineCacheState, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::String>) src/v8/src/ic.cc:947
    #24 0x7fb710df94c2 in v8::internal::__RT_impl_LoadIC_Miss(v8::internal::Arguments, v8::internal::Isolate*) src/v8/src/ic.cc:2248
    #25 0x7fb710df92e4 in v8::internal::LoadIC_Miss(int, v8::internal::Object**, v8::internal::Isolate*) src/v8/src/ic.cc:2243
    #26 0x260645506aed
    #27 0x260645570cd8
    #28 0x260645570ba6
    #29 0x26064552b623
    #30 0x2606455185b6
    #26 0x7fb710cc4292 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) src/v8/src/execution.cc:119
    #27 0x7fb710c0da8f in v8::Script::Run() src/v8/src/api.cc:2022
    #28 0x7fb70e7bec3f in WebCore::V8ScriptRunner::runCompiledScript(v8::Handle<v8::Script>, WebCore::ScriptExecutionContext*) src/third_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:95
    #29 0x7fb70e76cbd1 in WebCore::ScriptController::compileAndRunScript(WebCore::ScriptSourceCode const&) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:241
    #30 0x7fb70e76fe99 in WebCore::ScriptController::executeScriptInMainWorld(WebCore::ScriptSourceCode const&) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:683
    #31 0x7fb70e76fcf5 in WebCore::ScriptController::executeScript(WebCore::ScriptSourceCode const&) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:624
    #32 0x7fb70e76fbec in WebCore::ScriptController::executeScript(WTF::String const&, bool) src/third_party/WebKit/Source/bindings/v8/ScriptSourceCode.h:47
    #33 0x7fb70e770214 in WebCore::ScriptController::executeScriptIfJavaScriptURL(WebCore::KURL const&) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:646
    #34 0x7fb70f20b78d in WebCore::FrameLoader::loadFrameRequest(WebCore::FrameLoadRequest const&, bool, WTF::PassRefPtr<WebCore::Event>, WTF::PassRefPtr<WebCore::FormState>, WebCore::ShouldSendReferrer) src/third_party/WebKit/Source/core/loader/FrameLoader.cpp:950
    #35 0x7fb70f20b3fc in WebCore::FrameLoader::changeLocation(WebCore::SecurityOrigin*, WebCore::KURL const&, WTF::String const&, bool, bool) src/third_party/WebKit/Source/core/loader/FrameLoader.cpp:224
    #36 0x7fb70f23124a in WebCore::ScheduledURLNavigation::fire(WebCore::Frame*) src/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp:113
    #37 0x7fb70f22e2cf in WebCore::NavigationScheduler::timerFired(WebCore::Timer<WebCore::NavigationScheduler>*) src/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp:407
    #38 0x7fb70d8ddc01 in WebCore::ThreadTimers::sharedTimerFiredInternal() src/third_party/WebKit/Source/core/platform/ThreadTimers.cpp:134
    #39 0x7fb70d8dd624 in WebCore::ThreadTimers::sharedTimerFired() src/third_party/WebKit/Source/core/platform/ThreadTimers.cpp:108
    #40 0x7fb712e5f96a in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, webkit_glue::WebKitPlatformSupportImpl*) src/base/bind_internal.h:871
    #41 0x7fb712e5f743 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*), void (base::internal::UnretainedWrapper<webkit_glue::WebKitPlatformSupportImpl>)>, void (webkit_glue::WebKitPlatformSupportImpl*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1169
    #42 0x7fb7114f4ea2 in base::Timer::RunScheduledTask() src/base/timer/timer.cc:181
    #43 0x7fb7114f54da in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, base::BaseTimerTaskInternal*) src/base/bind_internal.h:871
    #44 0x7fb7114f5383 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*), void (base::internal::OwnedWrapper<base::BaseTimerTaskInternal>)>, void (base::BaseTimerTaskInternal*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1169
    #45 0x7fb71144fd44 in base::MessageLoop::RunTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:497
    #46 0x7fb7114506ab in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:509
    #47 0x7fb711450a11 in base::MessageLoop::DoWork() src/base/message_loop/message_loop.cc:703
    #48 0x7fb71145d96e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) src/base/message_loop/message_pump_default.cc:29
    #49 0x7fb71144f387 in base::MessageLoop::RunInternal() src/base/message_loop/message_loop.cc:451
    #50 0x7fb71149ccb9 in base::RunLoop::Run() src/base/run_loop.cc:45
    #51 0x7fb71144e0cd in base::MessageLoop::Run() src/base/message_loop/message_loop.cc:331
    #52 0x7fb711ee1b8e in content::RendererMain(content::MainFunctionParams const&) src/content/renderer/renderer_main.cc:247
    #53 0x7fb711965816 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:389
    #54 0x7fb711966178 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:445
    #55 0x7fb711967040 in content::ContentMainRunnerImpl::Run() src/content/app/content_main_runner.cc:757
    #56 0x7fb711964ed2 in content::ContentMain(int, char const**, content::ContentMainDelegate*) src/content/app/content_main.cc:35
    #57 0x7fb70bcb4cf6 in ChromeMain src/chrome/app/chrome_main.cc:32
    #58 0x7fb70bcb4c3a in main src/chrome/app/chrome_exe_main_gtk.cc:43
    #59 0x7fb70247176c in ?? ??
previously allocated by thread T0 (chrome) here:
    #0 0x7fb70bca2b65 in __interceptor_malloc _asan_rtl_
    #1 0x7fb7133aa4ed in xsltNewStylePreComp src/third_party/libxslt/libxslt/preproc.c:305
    #2 0x7fb7133acffc in xsltChooseComp src/third_party/libxslt/libxslt/preproc.c:1651
    #3 0x7fb7133aafd6 in xsltStylePreCompute src/third_party/libxslt/libxslt/preproc.c:2215
    #4 0x7fb7133d5361 in xsltPrecomputeStylesheet src/third_party/libxslt/libxslt/xslt.c:3488
    #5 0x7fb7133d3f8e in xsltParseStylesheetProcess src/third_party/libxslt/libxslt/xslt.c:6411
    #6 0x7fb7133d66d7 in xsltParseStylesheetImportedDoc src/third_party/libxslt/libxslt/xslt.c:6627
    #7 0x7fb7133d6d5b in xsltParseStylesheetDoc src/third_party/libxslt/libxslt/xslt.c:6666
    #8 0x7fb70f40a143 in WebCore::XSLStyleSheet::compileStyleSheet() src/third_party/WebKit/Source/core/xml/XSLStyleSheetLibxslt.cpp:232
    #9 0x7fb70f40d3e8 in WebCore::xsltStylesheetPointer(WTF::RefPtr<WebCore::XSLStyleSheet>&, WebCore::Node*) src/third_party/WebKit/Source/core/xml/XSLTProcessorLibxslt.cpp:241
    #10 0x7fb70f40c743 in WebCore::XSLTProcessor::transformToString(WebCore::Node*, WTF::String&, WTF::String&, WTF::String&) src/third_party/WebKit/Source/core/xml/XSLTProcessorLibxslt.cpp:284
    #11 0x7fb70e087b2f in WebCore::Document::applyXSLTransform(WebCore::ProcessingInstruction*) src/third_party/WebKit/Source/core/dom/Document.cpp:3904
    #12 0x7fb70e198255 in WebCore::StyleSheetCollection::collectStyleSheets(WebCore::DocumentStyleSheetCollection*, WTF::Vector<WTF::RefPtr<WebCore::StyleSheet>, 0ul>&, WTF::Vector<WTF::RefPtr<WebCore::CSSStyleSheet>, 0ul>&) src/third_party/WebKit/Source/core/dom/StyleSheetCollection.cpp:104
    #13 0x7fb70e198fbc in WebCore::StyleSheetCollection::updateActiveStyleSheets(WebCore::DocumentStyleSheetCollection*, WebCore::StyleResolverUpdateMode, WebCore::StyleSheetCollection::StyleResolverUpdateType&) src/third_party/WebKit/Source/core/dom/StyleSheetCollection.cpp:261
    #14 0x7fb70e0d8299 in WebCore::DocumentStyleSheetCollection::updateActiveStyleSheets(WebCore::StyleResolverUpdateMode) src/third_party/WebKit/Source/core/dom/DocumentStyleSheetCollection.cpp:270
    #15 0x7fb70e0788bb in WebCore::Document::styleResolverChanged(WebCore::StyleResolverUpdateType, WebCore::StyleResolverUpdateMode) src/third_party/WebKit/Source/core/dom/Document.cpp:2979
    #16 0x7fb70e07868f in WebCore::Document::updateLayoutIgnorePendingStylesheets() src/third_party/WebKit/Source/core/dom/Document.cpp:1756
    #17 0x7fb70d875075 in WebCore::HTMLObjectElement::renderWidgetForJSBindings() const src/third_party/WebKit/Source/core/html/HTMLObjectElement.cpp:74
    #18 0x7fb70d7e0193 in WebCore::HTMLPlugInElement::pluginWidget() const src/third_party/WebKit/Source/core/html/HTMLPlugInElement.cpp:143
    #19 0x7fb70d7e05a4 in WebCore::HTMLPlugInElement::getInstance() src/third_party/WebKit/Source/core/html/HTMLPlugInElement.cpp:116
    #20 0x7fb70e7f4cfb in void WebCore::npObjectNamedGetter<WebCore::V8HTMLObjectElement>(v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) src/third_party/WebKit/Source/bindings/v8/custom/V8HTMLPlugInElementCustom.cpp:50
    #21 0x7fb70e3d8fb3 in WebCore::HTMLObjectElementV8Internal::namedPropertyGetterCallback(v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) src/out/Release/gen/webkit/bindings/V8HTMLObjectElement.cpp:691
    #22 0x7fb710c36d6e in v8::internal::PropertyCallbackArguments::Call(v8::Handle<v8::Value> (*)(v8::Local<v8::String>, v8::AccessorInfo const&), v8::Local<v8::String>) src/v8/src/arguments.cc:196
    #23 0x7fb710ed37b4 in v8::internal::JSObject::GetPropertyWithInterceptor(v8::internal::Object*, v8::internal::Name*, PropertyAttributes*) src/v8/src/objects.cc:12781
    #24 0x7fb710ece530 in v8::internal::Object::GetProperty(v8::internal::Object*, v8::internal::LookupResult*, v8::internal::Name*, PropertyAttributes*) src/v8/src/objects.cc:875
    #25 0x7fb710ed2c1f in v8::internal::Object::GetProperty(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::LookupResult*, v8::internal::Handle<v8::internal::Name>, PropertyAttributes*) src/v8/src/objects.cc:782
    #26 0x7fb710df10c2 in v8::internal::LoadIC::Load(v8::internal::InlineCacheState, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::String>) src/v8/src/ic.cc:947
    #27 0x7fb710df94c2 in v8::internal::__RT_impl_LoadIC_Miss(v8::internal::Arguments, v8::internal::Isolate*) src/v8/src/ic.cc:2248
    #28 0x7fb710df92e4 in v8::internal::LoadIC_Miss(int, v8::internal::Object**, v8::internal::Isolate*) src/v8/src/ic.cc:2243
    #29 0x260645506aed
    #30 0x260645570cd8
    #31 0x260645570ba6
    #32 0x26064552b623
    #33 0x2606455185b6
    #29 0x7fb710cc4292 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) src/v8/src/execution.cc:119
    #30 0x7fb710c0da8f in v8::Script::Run() src/v8/src/api.cc:2022
    #31 0x7fb70e7bec3f in WebCore::V8ScriptRunner::runCompiledScript(v8::Handle<v8::Script>, WebCore::ScriptExecutionContext*) src/third_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:95
    #32 0x7fb70e76cbd1 in WebCore::ScriptController::compileAndRunScript(WebCore::ScriptSourceCode const&) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:241
    #33 0x7fb70e76fe99 in WebCore::ScriptController::executeScriptInMainWorld(WebCore::ScriptSourceCode const&) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:683
    #34 0x7fb70e76fcf5 in WebCore::ScriptController::executeScript(WebCore::ScriptSourceCode const&) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:624
    #35 0x7fb70e76fbec in WebCore::ScriptController::executeScript(WTF::String const&, bool) src/third_party/WebKit/Source/bindings/v8/ScriptSourceCode.h:47
    #36 0x7fb70e770214 in WebCore::ScriptController::executeScriptIfJavaScriptURL(WebCore::KURL const&) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:646
    #37 0x7fb70f20b78d in WebCore::FrameLoader::loadFrameRequest(WebCore::FrameLoadRequest const&, bool, WTF::PassRefPtr<WebCore::Event>, WTF::PassRefPtr<WebCore::FormState>, WebCore::ShouldSendReferrer) src/third_party/WebKit/Source/core/loader/FrameLoader.cpp:950
    #38 0x7fb70f20b3fc in WebCore::FrameLoader::changeLocation(WebCore::SecurityOrigin*, WebCore::KURL const&, WTF::String const&, bool, bool) src/third_party/WebKit/Source/core/loader/FrameLoader.cpp:224
    #39 0x7fb70f23124a in WebCore::ScheduledURLNavigation::fire(WebCore::Frame*) src/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp:113
    #40 0x7fb70f22e2cf in WebCore::NavigationScheduler::timerFired(WebCore::Timer<WebCore::NavigationScheduler>*) src/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp:407
    #41 0x7fb70d8ddc01 in WebCore::ThreadTimers::sharedTimerFiredInternal() src/third_party/WebKit/Source/core/platform/ThreadTimers.cpp:134
    #42 0x7fb70d8dd624 in WebCore::ThreadTimers::sharedTimerFired() src/third_party/WebKit/Source/core/platform/ThreadTimers.cpp:108
    #43 0x7fb712e5f96a in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, webkit_glue::WebKitPlatformSupportImpl*) src/base/bind_internal.h:871
    #44 0x7fb712e5f743 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*), void (base::internal::UnretainedWrapper<webkit_glue::WebKitPlatformSupportImpl>)>, void (webkit_glue::WebKitPlatformSupportImpl*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1169
    #45 0x7fb7114f4ea2 in base::Timer::RunScheduledTask() src/base/timer/timer.cc:181
    #46 0x7fb7114f54da in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, base::BaseTimerTaskInternal*) src/base/bind_internal.h:871
    #47 0x7fb7114f5383 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*), void (base::internal::OwnedWrapper<base::BaseTimerTaskInternal>)>, void (base::BaseTimerTaskInternal*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1169
    #48 0x7fb71144fd44 in base::MessageLoop::RunTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:497
    #49 0x7fb7114506ab in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:509
    #50 0x7fb711450a11 in base::MessageLoop::DoWork() src/base/message_loop/message_loop.cc:703
    #51 0x7fb71145d96e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) src/base/message_loop/message_pump_default.cc:29
    #52 0x7fb71144f387 in base::MessageLoop::RunInternal() src/base/message_loop/message_loop.cc:451
    #53 0x7fb71149ccb9 in base::RunLoop::Run() src/base/run_loop.cc:45
    #54 0x7fb71144e0cd in base::MessageLoop::Run() src/base/message_loop/message_loop.cc:331
    #55 0x7fb711ee1b8e in content::RendererMain(content::MainFunctionParams const&) src/content/renderer/renderer_main.cc:247
    #56 0x7fb711965816 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:389
    #57 0x7fb711966178 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:445
    #58 0x7fb711967040 in content::ContentMainRunnerImpl::Run() src/content/app/content_main_runner.cc:757
    #59 0x7fb711964ed2 in content::ContentMain(int, char const**, content::ContentMainDelegate*) src/content/app/content_main.cc:35
    #60 0x7fb70bcb4cf6 in ChromeMain src/chrome/app/chrome_main.cc:32
    #61 0x7fb70bcb4c3a in main src/chrome/app/chrome_exe_main_gtk.cc:43
    #62 0x7fb70247176c in ?? ??
Shadow bytes around the buggy address:
  0x0c2e8000da70: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8000da80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8000da90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8000daa0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8000dab0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c2e8000dac0: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000dad0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8000dae0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c2e8000daf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8000db00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8000db10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap right redzone:    fb
  Freed heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==6==ABORTING

### ae...@chromium.org (2013-07-17)

I wasn't able to reproduce it. I tried asan 211418 debug and release builds and 210544 release build. Also attempted with 10 instances at a time and with all cores occupied.

From the stack traces, it looks like xsltStylePreComp is used after free, or maybe the whole xsltStylesheet. It's not easy to dig further without reproducing.

### in...@chromium.org (2013-07-17)

i can reproduce reliably with just one instance, try with this command line (i think you just need --allow-file-access-from-files and --js-flags="--expose_gc").

ASAN_OPTIONS=strict_memcmp=0:alloc_dealloc_mismatch=0 ./out/Release/chrome --allow-file-access-from-files --disable-click-to-play --disable-hang-monitor --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-experimental-extension-apis --enable-extension-apps --enable-extension-timeline-api --enable-nacl --enable-native-web-workers --enable-search-provider-api-v2 --enable-video-track --force-internal-pdf --incognito --js-flags="--expose_gc" --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --no-sandbox --enable-shadow-dom --enable-media-stream --enable-css-regions --lang=en-US --enable-data-channels --use-fake-device-for-media-stream --user-data-dir=/tmp/t1

### ae...@chromium.org (2013-07-17)

Ok, reproduces, thanks. --allow-file-access-from-files made the difference.

### [Deleted User] (2013-07-17)

Honestly, I'm not surprised that the threaded parser interacts poorly with XSLT.  XSLT wires into the document lifetime in a strange way.

When we encounter XSLT during a parse, we save off the xmlDoc pointer:
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/xml/parser/XMLDocumentParser.cpp&sq=package:chromium&type=cs&l=1444&rcl=1374049527

Then we force a synchronous style resolve because that's currently the only way to get the "processing instruction" to run.

Which then sends the saved xml document pointer off to libxslt for translation.  When that comes back we parse the result and replace the document with the new result.

It's all a gigantic hack.

### ae...@chromium.org (2013-07-17)

Looks something like:

xsltParseStylesheetImportedDoc(xmlDocPtr doc, ...):
 allocates an xsltStylesheet
 calls xsltParseStylesheetProcess(..., doc), which:
   does some preprocessing, which:
     allocates xsltStylePreComp
     keeps a pointer to xsltStylePreComp inside doc, psvi field of xmlNodePtr
   does some parsing, which fails
 frees the xsltStylesheet along with the xsltStylePreComp because of parse failure
 leaves a dangling pointer at psvi

Later on:
 xsltParseStylesheetImportedDoc is called again with the same doc
 another style sheet is parsed successfully
 xsltApplyStylesheetInternal is called, which accesses the dangling psvi


### ae...@chromium.org (2013-07-22)

veillard, does this look like a possible code path? What do you think should be done differently? I would guess we should NULL the dangling psvi pointers after freeing the xsltStylesheet.

### ve...@gmail.com (2013-07-22)

Yes, it's a bit messy.
Basically when on compile an XML document into a stylesheet, the document is
heavilly modified and links back to the stylesheet.
So I tend to think that if the compilation fails, well the document should probably be freed (otherwise it is freed by freeing the stylesheet).
The fact that the stylesheet may be a part of the initial document makes things
nastier, as one may be tempted to keep that document for further processing.
Removing the psvi links is one sanity , but the process of compiling the stylesheet does modify other things like stripping blanks etc...

Daniel

### [Deleted User] (2013-07-22)

Hi dv.

We need to kill this feature.  It's never been good for stability and only represents an incredibly small fraction of the web.  Obviously that won't happen as part of this bug.  But hopefully this will be the last XSLT-in-blink security bug we'll ever have to fix. :)

### ve...@gmail.com (2013-07-23)

Which feature ? XSLT or embedded XSLT :-) ?
Note that the later is an integral part of the former !

http://www.w3.org/TR/xslt#section-Embedding-Stylesheets

my take is that in the exceptional cases where you find an embedded stylesheet,
duplicate the tree, and process. Nobody expects performances from this anyway !

Daniel

### ab...@chromium.org (2013-07-26)

Reproduced with ASAN build of content_shell:

./out/Release/content_shell http://localhost:8000/run.html --js-flags="--expose_gc"

### ab...@chromium.org (2013-07-26)

The approach suggested in https://crbug.com/chromium/260105#c18 appears to work.  I'll post a patch shortly.

### bu...@chromium.org (2013-07-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=155043

------------------------------------------------------------------------
r155043 | abarth@chromium.org | 2013-07-27T02:45:44.890562Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=155043&r2=155042&pathrev=155043
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ProcessingInstruction.h?r1=155043&r2=155042&pathrev=155043
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/StyleSheetCollection.cpp?r1=155043&r2=155042&pathrev=155043

applyXSLTransform is too eager

There's nothing that stops ProcessingInstruction from applying XSL Transforms
to HTML documents or from applying incompletely loaded XSL Transforms. This CL
adds a couple checks to avoid these cases.

The XSL Transform system is a bundle of insanity. So much of the system makes
so little sense it's hard to know where to start fixing it. Eric Seidel's
opinion is that we shouldn't drive the XSL transform process from style
resolution. Instead, we should kick off the transform either from
DOMContentLoaded or from the XSL sheet's load event. We tried a couple
approaches along those lines, but we didn't finish them for this CL. Maybe
we'll get that working for a future CL.

R=eseidel
BUG=260105

Review URL: https://chromiumcodereview.appspot.com/20856002
------------------------------------------------------------------------

### ab...@chromium.org (2013-07-27)

I ended up using a different approach.  Should be easy to merge to release branches.

### in...@chromium.org (2013-07-27)

Great! Thanks Adam.

### cl...@chromium.org (2013-07-30)

ClusterFuzz has detected this issue as fixed in range 214218:214246.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5758226951831552

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61300004c990
Crash State:
  - crash stack -
  xsltApplySequenceConstructor
  xsltApplyXSLTTemplate
  - free stack -
  xsltFreeStylePreComps
  xsltFreeStylesheet
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=193542:193554
Fixed: https://cluster-fuzz.appspot.com/revisions?range=214218:214246

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv9753bG910Z6SA5K_eDBwhmTLPiVYNRkcXJqYQyZ-uRbO6pHi3r48qOiqwEyMULJTYkBax1Yfraw1iOVManlrDfxXtTQV6jdTMs078riFJ_sW43jYudc9rVo85DsG--UGnWbPD1K2gwHgajetxmzuNeB8hVFAQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-08-06)

M29: http://src.chromium.org/viewvc/blink?view=rev&rev=155640

### bu...@chromium.org (2013-08-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=155640

------------------------------------------------------------------------
r155640 | cevans@chromium.org | 2013-08-06T23:43:05.016664Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1547/Source/core/dom/ProcessingInstruction.h?r1=155640&r2=155639&pathrev=155640
   M http://src.chromium.org/viewvc/blink/branches/chromium/1547/Source/core/dom/DocumentStyleSheetCollection.cpp?r1=155640&r2=155639&pathrev=155640
   M http://src.chromium.org/viewvc/blink/branches/chromium/1547/Source/core/dom/Document.cpp?r1=155640&r2=155639&pathrev=155640

Manual merge of http://src.chromium.org/viewvc/blink?view=revision&revision=155043

BUG=260105
TBR=abarth@chromium.org

Review URL: https://codereview.chromium.org/22392008
------------------------------------------------------------------------

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-08-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### ma...@chromium.org (2014-06-19)

https://crbug.com/chromium/260105#c11 has the repro case.

Thank you.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/260105?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077780)*
