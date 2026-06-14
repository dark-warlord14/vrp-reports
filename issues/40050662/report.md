# Use-after-free in SVG renderer

| Field | Value |
|-------|-------|
| **Issue ID** | [40050662](https://issues.chromium.org/issues/40050662) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2011-10-31 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

HTML file with loaded SVG file can trigger use-after-free in SVG renderer while changing the order of tree nodes.

**VERSION**  

Ubuntu 10.10, x64 - 17.0.923.0 (Developer Build 107869 Linux)  

Windows 7, x64 - 15.0.874.106 m

**REPRODUCTION CASE**  

PoC file is in attachment.

Here is an ASan log:  

==26413== ERROR: AddressSanitizer heap-use-after-free on address 0x7f7f6e566890 at pc 0x7f7f8a01382f bp 0x7fffeeefafb0 sp 0x7fffeeefafa8  

READ of size 8 at 0x7f7f6e566890 thread T0  

#0 0x7f7f8a01382f in WebCore::RenderObject::document() const asan\_stats.cc:0  

#1 0x7f7f8afcbed9 in WebCore::RenderObject::view() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.cpp:2094  

#2 0x7f7f8b6c1636 in WebCore::RenderSVGResourceContainer::markClientForInvalidation(WebCore::RenderObject\*, WebCore::RenderSVGResourceContainer::InvalidationMode) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/RenderSVGResourceContainer.cpp:134  

#3 0x7f7f8b6c54ea in WebCore::RenderSVGResourceFilter::primitiveAttributeChanged(WebCore::RenderObject\*, WebCore::QualifiedName const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/RenderSVGResourceFilter.cpp:344  

#4 0x7f7f8b5e53c4 in WebCore::SVGFELightElement::svgAttributeChanged(WebCore::QualifiedName const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGFELightElement.cpp:199  

#5 0x7f7f8a32f262 in WebCore::Element::setAttribute(WebCore::QualifiedName const&, WTF::AtomicString const&, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:712  

#6 0x7f7f8b59f316 in WebCore::SVGAnimationElement::setTargetAttributeAnimatedValue(WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGAnimationElement.cpp:359  

#7 0x7f7f8b5955e0 in WTF::RefPtr[WTF::StringImpl](javascript:void(0);)::~RefPtr() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#8 0x7f7f8b68a1ff in WebCore::SMILTimeContainer::updateAnimations(WebCore::SMILTime, double, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/animation/SMILTimeContainer.cpp:297  

#9 0x7f7f8b689059 in WTF::RefPtr[WTF::StringImpl](javascript:void(0);)::~RefPtr() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#10 0x7f7f8a5681b8 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#11 0x7f7f88b81c79 in base::subtle::TaskClosureAdapter::Run() /media/Chromium/chromium/depot\_tools/src/base/task.cc:72  

#12 0x7f7f88b1aa52 in MessageLoop::RunTask(MessageLoop::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:496  

#13 0x7f7f88b1afe4 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:509  

#14 0x7f7f88b1b692 in MessageLoop::DoDelayedWork(base::TimeTicks\*) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:737  

#15 0x7f7f88b2816f in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:33  

#16 0x7f7f88b1a234 in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:454  

#17 0x7f7f88b19198 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:342  

#18 0x7f7f8c2f3061 in RendererMain(MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:230  

#19 0x7f7f889fd0f4 in (anonymous namespace)::RunZygote(MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:230  

addr2line: '': No such file  

#20 0x7f7f889fccab in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:267  

#21 0x7f7f889fc4ce in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:445  

#22 0x7f7f876eed17 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#23 0x7f7f876edf2b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#24 0x7f7f8144ad8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

#25 0x7f7f876ede49 in \_start ??:0  

0x7f7f6e566890 is located 16 bytes inside of 272-byte region [0x7f7f6e566880,0x7f7f6e566990)  

freed by thread T0 here:  

#0 0x7f7f8cc80076 in free /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:29  

#1 0x7f7f8a34fb41 in WebCore::Node::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:1412  

#2 0x7f7f8a333a9a in WebCore::Element::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1029  

#3 0x7f7f8a2cd200 in WebCore::ContainerNode::removeBetween(WebCore::Node\*, WebCore::Node\*, WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:499  

#4 0x7f7f8a2cb33a in WebCore::ContainerNode::removeChild(WebCore::Node\*, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:474  

#5 0x7f7f8a2cab86 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:638  

#6 0x7f7f8a2ca3dc in WebCore::ContainerNode::insertBefore(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::Node\*, int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:123  

#7 0x7f7f8a34c720 in WebCore::Node::insertBefore(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::Node\*, int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:658  

#8 0x7f7f8a7bcada in WebCore::V8Node::insertBeforeCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:70  

#9 0x7f7f8959a480 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1164  

#10 0x3f6e0bb0428e in  

#11 0x3f6e0bb41b7d in  

#12 0x3f6e0bb41416 in  

#13 0x3f6e0bb3fb6d in  

#14 0x3f6e0bb237c7 in  

#15 0x3f6e0bb08a21 in  

#16 0x7f7f895e28ee in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#17 0x7f7f8954be95 in v8::internal::Isolate::handle\_scope\_implementer() /media/Chromium/chromium/depot\_tools/src/v8/src/isolate.h:838  

#18 0x7f7f8a790266 in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Page\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:520  

#19 0x7f7f8a78fe76 in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:483  

#20 0x7f7f8a77f623 in WebCore::V8LazyEventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8LazyEventListener.cpp:69  

#21 0x7f7f8ac86e3d in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:152  

#22 0x7f7f8ac86a22 in WebCore::V8AbstractEventListener::handleEvent(WebCore::ScriptExecutionContext\*, WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:98  

#23 0x7f7f8a33eecd in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:214  

#24 0x7f7f8a33eb87 in WebCore::EventTarget::fireEventListeners(WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:199  

#25 0x7f7f8a356d3e in WebCore::Node::handleLocalEvents(WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2793  

#26 0x7f7f8a3cea2e in WebCore::EventDispatcher::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:319  

#27 0x7f7f8a3cce2d in WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher\*) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatchMediator.cpp:51  

#28 0x7f7f8a3cd881 in WebCore::EventDispatcher::dispatchEvent(WebCore::Node\*, WTF::PassRefPtr[WebCore::EventDispatchMediator](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:55  

previously allocated by thread T0 here:  

#0 0x7f7f8cc7feff in malloc /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:41  

#1 0x7f7f8b665e74 in WebCore::SVGStyledTransformableElement::createRenderer(WebCore::RenderArena\*, WebCore::RenderStyle\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGStyledTransformableElement.cpp:146  

#2 0x7f7f8a36c655 in WebCore::NodeRendererFactory::createRenderer() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:293  

#3 0x7f7f8a36ca2f in WebCore::NodeRendererFactory::createRendererIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:339  

#4 0x7f7f8a34faa6 in WebCore::Node::createRendererIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:1488  

#5 0x7f7f8a333771 in WebCore::Element::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:995  

#6 0x7f7f8b6600c1 in WebCore::SVGStyledElement::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGStyledElement.cpp:363  

#7 0x7f7f8ac353f0 in WebCore::XMLDocumentParser::startElementNs(unsigned char const\*, unsigned char const\*, unsigned char const\*, int, unsigned char const\*\*, int, int, unsigned char const\*\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/xml/parser/XMLDocumentParserLibxml2.cpp:792  

#8 0x7f7f89d28e04 in xmlParseStartTag2 /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:9126  

#9 0x7f7f89d32646 in xmlParseTryOrFinish /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:10847  

#10 0x7f7f89d2eee1 in xmlParseChunk /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:11625  

#11 0x7f7f8ac343bb in WebCore::XMLDocumentParser::doWrite(WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/xml/parser/XMLDocumentParserLibxml2.cpp:657  

#12 0x7f7f8ac318a7 in WTF::RefPtr[WTF::StringImpl](javascript:void(0);)::~RefPtr() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#13 0x7f7f8c8c615e in WebCore::DecodedDataDocumentParser::appendBytes(WebCore::DocumentWriter\*, char const\*, unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/DecodedDataDocumentParser.cpp:50  

#14 0x7f7f8aa67d41 in WTF::RefPtr[WTF::StringImpl](javascript:void(0);)::~RefPtr() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#15 0x7f7f8a06b75a in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader\*, char const\*, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1115  

#16 0x7f7f8aa67c40 in void WTF::derefIfNotNull[WebCore::DocumentLoader](javascript:void(0);)(WebCore::DocumentLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:59  

#17 0x7f7f8aac3ad2 in WebCore::ResourceLoader::didReceiveData(char const\*, int, long long, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:291  

#18 0x7f7f8aaae6cd in void WTF::derefIfNotNull[WebCore::MainResourceLoader](javascript:void(0);)(WebCore::MainResourceLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:59  

#19 0x7f7f8aac4945 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle\*, char const\*, int, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:442  

#20 0x7f7f89f43b02 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:377  

#21 0x7f7f89f44ed8 in bool ResourceMsg\_DataReceived::Dispatch<ResourceDispatcher, ResourceDispatcher, int, base::FileDescriptor, int, int>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(IPC::Message const&, int, base::FileDescriptor, int, int)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:137  

#22 0x7f7f89f433bb in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:523  

==26413== ABORTING  

Shadow byte and word:  

0x1fefedcacd12: fd  

0x1fefedcacd10: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fefedcaccf0: 00 00 fb fb fb fb fb fb  

0x1fefedcaccf8: fb fb fb fb fb fb fb fb  

0x1fefedcacd00: fa fa fa fa fa fa fa fa  

0x1fefedcacd08: fa fa fa fa fa fa fa fa  

=>0x1fefedcacd10: fd fd fd fd fd fd fd fd  

0x1fefedcacd18: fd fd fd fd fd fd fd fd  

0x1fefedcacd20: fd fd fd fd fd fd fd fd  

0x1fefedcacd28: fd fd fd fd fd fd fd fd  

0x1fefedcacd30: fd fd fd fd fd fd fd fd

## Attachments

- [9.zip](attachments/9.zip) (application/zip; charset=binary, 1.0 KB)
- deleted (application/octet-stream, 0 B)
- [crbug102359.html](attachments/crbug102359.html) (text/plain; charset=us-ascii, 432 B)

## Timeline

### ax...@gmail.com (2011-10-31)

Managed to make smaller version:

<!DOCTYPE html>
<html>
    <script type="text/javascript">

        function body_start() {

            q = document.getElementById('root').contentDocument;

            rn = q.getElementById('_g');
            nc = q.getElementById('_title');
            oc = q.getElementById('_svg');
            rn.insertBefore(nc, oc.nextSibling);

            rn = q.getElementById('_animate');
            nc = q.getElementById('_rect');
            oc = q.getElementById('_title');
            rn.insertBefore(nc, oc.nextSibling);

        }
    </script>
    <object data="i.svg" id="root" onload="body_start()"/></object>
</html>

---- i.svg ----

<svg id="_svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <title id="_title"></title>
    <defs>
        <filter id="C"><feDiffuseLighting><feSpotLight><animate id="_animate" attributeName="limitingConeAngle" from="0" to="50" dur="10s"/></feSpotLight></feDiffuseLighting></filter>
    </defs>
    <g id="_g"><rect id="_rect" width="50" height="30" filter="url(#C)"/></g>
</svg>

### js...@chromium.org (2011-11-01)

@inferno - Would you verify this one under ASAN for me? I won't be able to test on Linux until tomorrow, and I can't hit it on my Windows build.

### in...@chromium.org (2011-11-01)

Original testcase in c#0 crashes easily, reduction in c#1 does not seem to work. It crashes m15 on a null and not with a use after free. 

### js...@chromium.org (2011-11-01)

If it's set for m16 then it must affect beta. Flagging for now and I'll verify later.

### js...@chromium.org (2011-11-03)

Here's a simplified repro that triggers on stable and trunk. The problem is in reparenting the rect with the animated filter applied. Probably just need to fix some things up on element removal. I'll dig into it a bit more tomorrow.

### js...@chromium.org (2011-11-03)

[Comment Deleted]

### js...@chromium.org (2011-11-03)

Better repro if you're pausing execution a lot in the debugger.

### sc...@gmail.com (2011-11-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-07)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-11-08)

Upstreamed: https://bugs.webkit.org/show_bug.cgi?id=71741

### js...@chromium.org (2011-11-10)

Patch up for review upstream. Looks like an easy fix and should be a clean merge candidate. 

### js...@chromium.org (2011-11-16)

Landed upstream: http://trac.webkit.org/changeset/100502

### sc...@gmail.com (2011-11-18)

Merged to M16
http://trac.webkit.org/changeset/100711

### sc...@gmail.com (2011-11-18)

@Ax330d: another great bug! Thanks for picking up ASAN and thanks for your efforts to make smaller test cases. Definitely a $1000 Chromium Security Reward.

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

### sc...@gmail.com (2011-12-20)

Payment in system.

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/102359?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050662)*
