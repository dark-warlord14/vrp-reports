# Heap-use-after-free in WebCore::HTMLMediaElement::~HTMLMediaElement

| Field | Value |
|-------|-------|
| **Issue ID** | [40077008](https://issues.chromium.org/issues/40077008) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ac...@chromium.org |
| **Created** | 2013-02-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Attached test case crashes with a use after free in WTF::RefCountedBase::derefBase().

**VERSION**  

Chrome Version: [27.0.1419.0 (183684)] + [trunk]  

[24.0.1312.70] + [stable]  

[25.0.1364.84] + [beta]  

[26.0.1410.5] + [dev]  

Operating System: [Ubuntu 12.04 64 bit]

**REPRODUCTION CASE**

## Steps

1. Download parent.html, test.html and out.ogv and copy them to a folder in web server.
2. Open chrome with --js-flags="--expose-gc"
3. Open parent.html
4. Chrome will display an alert box. Press escape.
5. Chrome will display another alert box. Press escape.  
   
   Tab will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: [ASAN output]

==19512== ERROR: AddressSanitizer: heap-use-after-free on address 0x600c000d2b08 at pc 0x7f591f287dcd bp 0x7fffbec831a0 sp 0x7fffbec83198  

READ of size 4 at 0x600c000d2b08 thread T0 (chrome)  

#0 0x7f591f287dcc in WTF::RefCountedBase::derefBase() out/Release/../../third\_party/WebKit/Source/WTF/wtf/RefCounted.h:148  

#1 0x7f591fa392fd in WTF::RefCounted[WebCore::PODArena](javascript:void(0);)::deref() out/Release/../../third\_party/WebKit/Source/WTF/wtf/RefCounted.h:201  

#2 0x7f591fa11070 in ~HTMLMediaElement out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:357  

#3 0x7f591fa10cdd in ~HTMLMediaElement out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:329  

#4 0x7f5921189550 in void WTF::derefIfNotNull[WebCore::EventTarget](javascript:void(0);)(WebCore::EventTarget\*) out/Release/../../third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:53  

#5 0x7f59217bbbea in WebCore::Event::setTarget(WTF::PassRefPtr[WebCore::EventTarget](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/dom/Event.cpp:183  

#6 0x7f59217c2b4d in WebCore::GenericEventQueue::enqueueEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/dom/GenericEventQueue.cpp:57  

#7 0x7f591fa145bd in WebCore::HTMLMediaElement::scheduleEvent(WTF::AtomicString const&) out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:655  

#8 0x7f591fa273d4 in WebCore::HTMLMediaElement::userCancelledLoad() out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:3862  

#9 0x7f591fa27619 in WebCore::HTMLMediaElement::stop() out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:3932  

#10 0x7f592182b3e1 in WebCore::ScriptExecutionContext::stopActiveDOMObjects() out/Release/../../third\_party/WebKit/Source/WebCore/dom/ScriptExecutionContext.cpp:239  

#11 0x7f59210a946a in WebCore::FrameLoader::frameDetached() out/Release/../../third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:2379  

#12 0x7f591fadfada in WebCore::HTMLFrameOwnerElement::disconnectContentFrame() out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLFrameOwnerElement.cpp:84  

#13 0x7f5921728a10 in WebCore::ChildFrameDisconnector::disconnectCollectedFrameOwners() out/Release/../../third\_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:316  

#14 0x7f59217230f8 in WebCore::willRemoveChild(WebCore::Node\*) out/Release/../../third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:455  

#15 0x7f5921722bba in WebCore::ContainerNode::removeChild(WebCore::Node\*, int&) out/Release/../../third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:520  

#16 0x7f59217e8ad1 in WebCore::Node::removeChild(WebCore::Node\*, int&) out/Release/../../third\_party/WebKit/Source/WebCore/dom/Node.cpp:568  

#17 0x7f5920d56b40 in WebCore::V8Node::removeChildCallbackCustom(v8::Arguments const&) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:101  

#18 0x7f5923141ca3 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1335  

#19 0x2e474e0062ed in  

0x600c000d2b08 is located 8 bytes inside of 64-byte region [0x600c000d2b00,0x600c000d2b40)  

freed by thread T0 (chrome) here:  

#0 0x7f591dcf64e2 in free ??:0  

#1 0x7f591fa11070 in ~HTMLMediaElement out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:357  

#2 0x7f59244afd0d in WebCore::HTMLVideoElement::~HTMLVideoElement() out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLVideoElement.h:36  

#3 0x7f59231c5751 in v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing(v8::internal::Isolate\*, v8::internal::GlobalHandles\*) out/Release/../../v8/src/global-handles.cc:274  

#4 0x7f59231c51d4 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector, v8::internal::GCTracer\*) out/Release/../../v8/src/global-handles.cc:656  

#5 0x7f59231db01c in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer\*) out/Release/../../v8/src/heap.cc:989  

#6 0x7f59231da749 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const\*, char const\*) out/Release/../../v8/src/heap.cc:655  

#7 0x7f592319321d in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, char const\*) out/Release/../../v8/src/heap-inl.h:461  

#8 0x7f59231da36e in v8::internal::Heap::CollectAllGarbage(int, char const\*) out/Release/../../v8/src/heap.cc:565  

#9 0x7f5923193145 in v8::internal::GCExtension::GC(v8::Arguments const&) out/Release/../../v8/src/extensions/gc-extension.cc:46  

#10 0x7f5923141ca3 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1335  

#11 0x2e474e0062ed in  

#12 0x2e474e059ce6 in  

#13 0x2e474e00b353 in  

#14 0x2e474e025bdd in  

#15 0x2e474e007176 in  

#16 0x7f592318cf51 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) out/Release/../../v8/src/execution.cc:118  

#17 0x7f592310bd02 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) out/Release/../../v8/src/api.cc:3723  

#18 0x7f5920cea6d7 in WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:234  

#19 0x7f5920cea3f2 in WebCore::ScriptController::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:187  

#20 0x7f59215533b1 in WebCore::V8EventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/V8EventListener.cpp:95  

#21 0x7f592133f6a6 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:143  

#22 0x7f592133f40a in WebCore::V8AbstractEventListener::handleEvent(WebCore::ScriptExecutionContext\*, WebCore::Event\*) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:103  

#23 0x7f59217c00ce in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:256  

#24 0x7f59217bfaad in WebCore::EventTarget::fireEventListeners(WebCore::Event\*) out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:203  

#25 0x7f592187fce3 in WebCore::WindowEventContext::handleLocalEvents(WebCore::Event\*) out/Release/../../third\_party/WebKit/Source/WebCore/dom/WindowEventContext.cpp:60  

#26 0x7f5921877b85 in WebCore::EventDispatcher::dispatchEventAtBubbling(WebCore::WindowEventContext&) out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:190  

#27 0x7f592187741c in WebCore::EventDispatcher::dispatch() out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:123  

#28 0x7f592187610b in WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher\*) const out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventDispatchMediator.cpp:54  

#29 0x7f592187627d in WebCore::EventDispatcher::dispatchEvent(WebCore::Node\*, WTF::PassRefPtr[WebCore::EventDispatchMediator](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:56  

previously allocated by thread T0 (chrome) here:  

#0 0x7f591dcf65c2 in malloc ??:0  

#1 0x7f5923ae2ef8 in WTF::fastMalloc(unsigned long) out/Release/../../third\_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:285  

#2 0x7f591fa39233 in WebCore::PODFreeListArena<WebCore::PODRedBlackTree<WebCore::PODInterval<double, WebCore::TextTrackCue\*> >::Node>::create() out/Release/../../third\_party/WebKit/Source/WebCore/platform/PODFreeListArena.h:40  

#3 0x7f591fa3875a in PODRedBlackTree out/Release/../../third\_party/WebKit/Source/WebCore/platform/PODRedBlackTree.h:125  

#4 0x7f591fa3869d in PODIntervalTree out/Release/../../third\_party/WebKit/Source/WebCore/platform/PODIntervalTree.h:89  

#5 0x7f591fa0fee2 in HTMLMediaElement out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:264  

#6 0x7f59244b0040 in HTMLVideoElement out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLVideoElement.cpp:50  

#7 0x7f59244aea63 in WebCore::HTMLVideoElement::create(WebCore::QualifiedName const&, WebCore::Document\*, bool) out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLVideoElement.cpp:56  

#8 0x7f5922021c31 in WebCore::videoConstructor(WebCore::QualifiedName const&, WebCore::Document\*, WebCore::HTMLFormElement\*, bool) out/Release/gen/webkit/HTMLElementFactory.cpp:576  

#9 0x7f592201c632 in WebCore::HTMLElementFactory::createHTMLElement(WebCore::QualifiedName const&, WebCore::Document\*, WebCore::HTMLFormElement\*, bool) out/Release/gen/webkit/HTMLElementFactory.cpp:782  

#10 0x7f591fb838c2 in WebCore::HTMLConstructionSite::createHTMLElement(WebCore::AtomicHTMLToken\*) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:538  

#11 0x7f591fb84307 in WebCore::HTMLConstructionSite::insertHTMLElement(WebCore::AtomicHTMLToken\*) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:416  

#12 0x7f591fb3c5d3 in WebCore::HTMLTreeBuilder::processStartTagForInBody(WebCore::AtomicHTMLToken\*) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:947  

#13 0x7f591fb38db5 in WebCore::HTMLTreeBuilder::processStartTag(WebCore::AtomicHTMLToken\*) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:1176  

#14 0x7f591fb36efe in WebCore::HTMLTreeBuilder::constructTree(WebCore::AtomicHTMLToken\*) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:369  

#15 0x7f591faf47b4 in WebCore::HTMLDocumentParser::constructTreeFromHTMLToken(WebCore::HTMLToken&) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:482  

#16 0x7f591faf1af7 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:439  

#17 0x7f591faf587b in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:627  

#18 0x7f5921731161 in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter\*) out/Release/../../third\_party/WebKit/Source/WebCore/dom/DecodedDataDocumentParser.cpp:60  

#19 0x7f5921090aaf in WebCore::DocumentWriter::end() out/Release/../../third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:240  

#20 0x7f5921078346 in WebCore::DocumentLoader::finishedLoading() out/Release/../../third\_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:295  

#21 0x7f59210bf9d5 in WebCore::MainResourceLoader::didFinishLoading(double) out/Release/../../third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:563  

#22 0x7f59210fa3b7 in WebCore::CachedResource::checkNotify() out/Release/../../third\_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:378  

#23 0x7f59210f62be in WebCore::CachedRawResource::data(WTF::PassRefPtr[WebCore::ResourceBuffer](javascript:void(0);), bool) out/Release/../../third\_party/WebKit/Source/WebCore/loader/cache/CachedRawResource.cpp:72  

#24 0x7f59210d7e33 in WebCore::SubresourceLoader::didFinishLoading(double) out/Release/../../third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:278  

#25 0x7f5923a5a388 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../webkit/glue/weburlloader\_impl.cc:713  

#26 0x7f5921b68a52 in content::ResourceDispatcher::OnRequestComplete(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../content/common/resource\_dispatcher.cc:501  

#27 0x7f5921b6a47e in bool ResourceMsg\_RequestComplete::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, content::ResourceDispatcher\*, content::ResourceDispatcher\*, void (content::ResourceDispatcher::\*)(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) out/Release/../../content/common/resource\_messages.h:256  

#28 0x7f5921b65d8c in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) out/Release/../../content/common/resource\_dispatcher.cc:601  

#29 0x7f5921b65190 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/resource\_dispatcher.cc:293

## Attachments

- [out.ogv](attachments/out.ogv) (application/ogg; charset=binary, 288.3 KB)
- [test.html](attachments/test.html) (text/html; charset=us-ascii, 495 B)
- [parent.html](attachments/parent.html) (text/plain; charset=us-ascii, 131 B)

## Timeline

### ch...@gmail.com (2013-02-22)

Apply the fix for https://crbug.com/chromium/176882, before reproducing this issue. Otherwise https://crbug.com/chromium/176882 may reproduce before this issue.

### in...@chromium.org (2013-02-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=167007772

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x600c000aff48
Crash State:
  - crash stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement

### in...@chromium.org (2013-02-22)

Actually we are hitting this same stack after the fix went in, so caught it in time. CF report above.

### in...@chromium.org (2013-02-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-02-22)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-02-22)

Upstreamed as https://bugs.webkit.org/show_bug.cgi?id=110623

### sc...@gmail.com (2013-02-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-01)

Oops! We forgot to cc: media people.
Adding them, since it looks to be related to lifetime in the HTMLMediaElement example.

### sc...@gmail.com (2013-03-04)

Moose Drool for @scherkus if he can cajole someone to fix it by EOD Monday :P

### sc...@chromium.org (2013-03-04)

acolwell will take a look

### sc...@chromium.org (2013-03-04)

(FWIW, Moose Drool is one of my favourite beers http://www.bigskybrew.com/Moose%20Drool !!!!)

### cl...@chromium.org (2013-03-04)

ClusterFuzz has detected this issue as fixed in range 183264:183765.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=167007772

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x600c000aff48
Crash State:
  - crash stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=140979:140989
Fixed: https://cluster-fuzz.appspot.com/revisions?range=183264:183765

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@chromium.org (2013-03-04)

hum -- do we believe that's legitimate?

### in...@chromium.org (2013-03-04)

that is false positive, i clicked redo on the testcase and now it completes with fixed:no. this usually happens when testcase is too flaky. 

### ac...@chromium.org (2013-03-05)

So I haven't found the exact cause yet, but I've narrowed down at least some of what is happening.

The stack appears to get blown away on this call to dispatchEvent()(https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/WebCore/dom/Document.cpp&sq=package:chromium&l=1227)

Here is a snapshot of the stack right before the dispatchEvent() call.
 [0x7ffff5734e6e] base::debug::StackTrace::StackTrace()
 [0x7ffff1253f8f] WebCore::Document::setReadyState()
 [0x7ffff222fd1f] WebCore::FrameLoader::checkCompleted()
 [0x7ffff22300d2] WebCore::FrameLoader::loadDone()
 [0x7ffff22ac0ae] WebCore::CachedResourceLoader::loadDone()
 [0x7ffff2271744] WebCore::SubresourceLoader::releaseResources()
 [0x7ffff226b6a3] WebCore::ResourceLoader::cancel()
 [0x7ffff226a553] WebCore::ResourceLoader::cancel()
 [0x7ffff22701f5] WebCore::SubresourceLoader::cancelIfNotFinishing()
 [0x7ffff229742b] WebCore::CachedRawResource::allClientsRemoved()
 [0x7ffff229bdd8] WebCore::CachedResource::removeClient()
 [0x7ffff221caf1] WebCore::DocumentThreadableLoader::clearResource()
 [0x7ffff221c9a6] WebCore::DocumentThreadableLoader::cancel()
 [0x7ffff098578b] WebKit::AssociatedURLLoader::cancel()
 [0x7fffed8c708a] webkit_media::ActiveLoader::~ActiveLoader()
 [0x7fffed8d524e] base::DefaultDeleter<>::operator()()
 [0x7fffed8d520c] base::internal::scoped_ptr_impl<>::reset()
 [0x7fffed8d4a6d] scoped_ptr<>::reset()
 [0x7fffed8d1317] webkit_media::BufferedResourceLoader::Stop()
 [0x7fffed8ca36c] webkit_media::BufferedDataSource::StopLoader()
 [0x7fffed8ca17e] webkit_media::BufferedDataSource::Abort()
 [0x7fffed8ee25c] webkit_media::WebMediaPlayerImpl::Destroy()
 [0x7fffed8ede58] webkit_media::WebMediaPlayerImpl::~WebMediaPlayerImpl()
 [0x7fffed8edd29] webkit_media::WebMediaPlayerImpl::~WebMediaPlayerImpl()
 [0x7ffff0a6bd6e] WTF::deleteOwnedPtr<>()
 [0x7ffff0a6aa77] WTF::OwnPtr<>::clear()
 [0x7ffff0a6698b] WebKit::WebMediaPlayerClientImpl::~WebMediaPlayerClientImpl()
 [0x7ffff0a667f9] WebKit::WebMediaPlayerClientImpl::~WebMediaPlayerClientImpl()
 [0x7ffff194c1ae] WTF::deleteOwnedPtr<>()
 [0x7ffff194c208] WTF::OwnPtr<>::~OwnPtr()
 [0x7ffff194be95] WTF::OwnPtr<>::~OwnPtr()
 [0x7ffff1948eb7] WebCore::MediaPlayer::~MediaPlayer()
 [0x7ffff1948e09] WebCore::MediaPlayer::~MediaPlayer()
 [0x7ffff250487e] WTF::deleteOwnedPtr<>()
 [0x7ffff250aa78] WTF::OwnPtr<>::~OwnPtr()
 [0x7ffff24fa225] WTF::OwnPtr<>::~OwnPtr()
 [0x7ffff24e6fd5] WebCore::HTMLMediaElement::~HTMLMediaElement()
 [0x7ffff25408af] WebCore::HTMLVideoElement::~HTMLVideoElement()
 [0x7ffff2540345] WebCore::HTMLVideoElement::~HTMLVideoElement()
 [0x7ffff2540369] WebCore::HTMLVideoElement::~HTMLVideoElement()
 [0x7ffff1343bf8] WebCore::Node::removedLastRef()
 [0x7ffff0990820] WebCore::TreeShared<>::deref()
 [0x7ffff2d3f20c] WebCore::V8HTMLVideoElement::derefObject()
 [0x7ffff1c63a74] WebCore::WrapperTypeInfo::derefObject()
 [0x7ffff1ce1554] WebCore::ScriptWrappable::weakCallback()
 [0x7ffff704f59e] v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing()
 [0x7ffff704d958] v8::internal::GlobalHandles::PostGarbageCollectionProcessing()
 [0x7ffff7077802] v8::internal::Heap::PerformGarbageCollection()
 [0x7ffff7077166] v8::internal::Heap::CollectGarbage()
 [0x7ffff6fb999f] v8::internal::Heap::CollectGarbage()
 [0x7ffff7076def] v8::internal::Heap::CollectAllGarbage()
 [0x7ffff7012ab6] v8::internal::GCExtension::GC()
 [0x7ffff6fa2ea5] v8::internal::HandleApiCallHelper<>()
 [0x7ffff6fa2a83] v8::internal::Builtin_Impl_HandleApiCall()
 [0x7ffff6f9c2dc] v8::internal::Builtin_HandleApiCall()
 [0x1e9347a062ee] <unknown>

The dispatchEvent() call never appears to return. The crash appears to occur within this call although the original stack seems to get destroyed.

The following stack trace printed out while the code was apparently in dispatchEvent(), but I have no idea what triggered it yet.
 [0x7ffff5734e6e] base::debug::StackTrace::StackTrace()
 [0x7ffff1253e29] WebCore::Document::setReadyState()
 [0x7ffff222e78b] WebCore::FrameLoader::stopLoading()
 [0x7ffff2205bb0] WebCore::DocumentLoader::stopLoading()
 [0x7ffff2235a0a] WebCore::FrameLoader::stopAllLoaders()
 [0x7ffff2238f6e] WebCore::FrameLoader::frameDetached()
 [0x7ffff24cd365] WebCore::HTMLFrameOwnerElement::disconnectContentFrame()
 [0x7ffff1236377] WebCore::ChildFrameDisconnector::disconnectCollectedFrameOwners()
 [0x7ffff1232f51] WebCore::ChildFrameDisconnector::disconnect()
 [0x7ffff122f94d] WebCore::willRemoveChild()
 [0x7ffff122f66e] WebCore::ContainerNode::removeChild()
 [0x7ffff133a8f8] WebCore::Node::removeChild()
 [0x7ffff1d7dea0] WebCore::V8Node::removeChildMethodCustom()
 [0x7ffff2d4df55] WebCore::NodeV8Internal::removeChildMethodCallback()
 [0x7ffff6fa2ea5] v8::internal::HandleApiCallHelper<>()
 [0x7ffff6fa2a83] v8::internal::Builtin_Impl_HandleApiCall()
 [0x7ffff6f9c2dc] v8::internal::Builtin_HandleApiCall()
 [0x1e9347a062ee] <unknown>

Shortly after this the application crashes while trying to schedule an abort event (https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp&q=HTMLMediaElement.cpp&sq=package:chromium&type=cs&l=3838) with the following stack.
 [0x7ffff5734e6e] base::debug::StackTrace::StackTrace()
 [0x7ffff24f75c9] WebCore::HTMLMediaElement::userCancelledLoad()
 [0x7ffff24f7792] WebCore::HTMLMediaElement::stop()
 [0x7ffff24f782c] WebCore::HTMLMediaElement::stop()
 [0x7ffff137cf6f] WebCore::ScriptExecutionContext::stopActiveDOMObjects()
 [0x7ffff2238f8e] WebCore::FrameLoader::frameDetached()
 [0x7ffff24cd365] WebCore::HTMLFrameOwnerElement::disconnectContentFrame()
 [0x7ffff1236377] WebCore::ChildFrameDisconnector::disconnectCollectedFrameOwners()
 [0x7ffff1232f51] WebCore::ChildFrameDisconnector::disconnect()
 [0x7ffff122f94d] WebCore::willRemoveChild()
 [0x7ffff122f66e] WebCore::ContainerNode::removeChild()
 [0x7ffff133a8f8] WebCore::Node::removeChild()
 [0x7ffff1d7dea0] WebCore::V8Node::removeChildMethodCustom()
 [0x7ffff2d4df55] WebCore::NodeV8Internal::removeChildMethodCallback()
 [0x7ffff6fa2ea5] v8::internal::HandleApiCallHelper<>()
 [0x7ffff6fa2a83] v8::internal::Builtin_Impl_HandleApiCall()
 [0x7ffff6f9c2dc] v8::internal::Builtin_HandleApiCall()
 [0x1e9347a062ee] <unknown>

I don't totally understand the magic behind dispatchEvent(), but I'm pretty sure it isn't a good idea to transfer control to JavaScript while inside a destructor. 

I'll continue looking into this tomorrow.

### ac...@chromium.org (2013-03-05)

Ok. I have a WebKit patch to fix this, but I'm unclear what the process is for fixing security bugs in WebKit. 

Should I just file a Security bug in WebKit, link it back to this bug, and upload my patch?

### in...@chromium.org (2013-03-05)

yes acolwell, that is right.

### ts...@chromium.org (2013-03-05)

Except that there is already an upstream bug for this in C6 https://bugs.webkit.org/show_bug.cgi?id=110623.  All else is the same.

### ac...@chromium.org (2013-03-05)

tsepez@, could you CC acolwell@chromium.org on that bug so I can view it please.

### in...@chromium.org (2013-03-05)

acolwell@, done

### ac...@chromium.org (2013-03-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-06)

https://bugs.webkit.org/show_bug.cgi?id=111486
http://trac.webkit.org/changeset/144846
https://bugs.webkit.org/show_bug.cgi?id=111486


### in...@chromium.org (2013-03-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-03-06)

Wrong bug number, but anyway patch in cq and should land soon.

### sc...@gmail.com (2013-03-06)

Committed r144859: <http://trac.webkit.org/changeset/144859>

### ac...@chromium.org (2013-03-07)

The original patch got reverted and a new one is up for review.

### ac...@chromium.org (2013-03-08)

The new patch landed last night and stuck.
http://trac.webkit.org/changeset/145162

### cl...@chromium.org (2013-03-08)

ClusterFuzz has detected this issue as fixed in range 183264:183765.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=167007772

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x600c000aff48
Crash State:
  - crash stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=140979:140989
Fixed: https://cluster-fuzz.appspot.com/revisions?range=183264:183765

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@chromium.org (2013-03-08)

kudos, acolwell. kudos.

### ac...@chromium.org (2013-03-08)

Thanks scherkus@. Sorry I couldn't bring it in by the Moose Drool deadline. :)

### in...@chromium.org (2013-03-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=170399332

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x600c00042b68
Crash State:
  - crash stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  

Minimized Testcase (1.14 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94lgSZ8glSvEW-VtV0haQZJWZMCpxwjSdjYckJvwL9euqYtHOAoAGkk2L8YjTKzipRxnZQ3tdHSUDRkr8Uw3KpGDB0-Xeazyf1_javQZI7BE93vXpXeKpOd8M1iiSiyYGQWgRGVq6HFFunn6rrsPThvNk8CGk3HIjDNisP7ldXwuG0vI5o

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### ac...@chromium.org (2013-03-11)

Hmm.. looks like there is still another issue with this. I'll take a look again today.

### in...@chromium.org (2013-03-12)

Yes, this bug is not fixed, testcases coming.

### in...@chromium.org (2013-03-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=171154605

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x600c00042568
Crash State:
  - crash stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  

Minimized Testcase (0.38 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94hk19KxNU-Uuiqjg5Pkr2oqSHu_yh6XDboJiqoME6xHYs-eoslFXycGprc16lfVjguhz6dLmb_aQ0WfINFSAvOzyU4XPr4CYCVskX4C6CrBLCQ3VsrZf4eSbZ1ogQ6-Wkki5Ge8l4lM_NFb50ziCX3nBet_nTROSMQm_PgZMg-Yu6EEXE

### ac...@chromium.org (2013-03-12)

It might also be quicker to find someone more familiar w/ the ResourceLoader code to look into this.

I'm pretty sure the problem lies in this part of the stack trace I included in a previous comment.

 [0x7ffff5734e6e] base::debug::StackTrace::StackTrace()
 [0x7ffff1253f8f] WebCore::Document::setReadyState()
 [0x7ffff222fd1f] WebCore::FrameLoader::checkCompleted()
 [0x7ffff22300d2] WebCore::FrameLoader::loadDone()
 [0x7ffff22ac0ae] WebCore::CachedResourceLoader::loadDone()
 [0x7ffff2271744] WebCore::SubresourceLoader::releaseResources()
 [0x7ffff226b6a3] WebCore::ResourceLoader::cancel()
 [0x7ffff226a553] WebCore::ResourceLoader::cancel()
 [0x7ffff22701f5] WebCore::SubresourceLoader::cancelIfNotFinishing()
 [0x7ffff229742b] WebCore::CachedRawResource::allClientsRemoved()
 [0x7ffff229bdd8] WebCore::CachedResource::removeClient()
 [0x7ffff221caf1] WebCore::DocumentThreadableLoader::clearResource()
 [0x7ffff221c9a6] WebCore::DocumentThreadableLoader::cancel()
 [0x7ffff098578b] WebKit::AssociatedURLLoader::cancel()
 [0x7fffed8c708a] webkit_media::ActiveLoader::~ActiveLoader()

WebCore::Document::setReadyState() dispatches an event to JavaScript, which I'm pretty sure isn't supposed to happen from within a destructor. I can keep looking around, but you might get quicker results w/ someone more familiar w/ these classes.

### sc...@gmail.com (2013-03-12)

[+tsepez]
Tom, didn't you fix something similar recently?

### cl...@chromium.org (2013-03-13)

ClusterFuzz has detected this issue as fixed in range 187589:187778.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=171154605

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x600c00042568
Crash State:
  - crash stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=187589:187778

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94hk19KxNU-Uuiqjg5Pkr2oqSHu_yh6XDboJiqoME6xHYs-eoslFXycGprc16lfVjguhz6dLmb_aQ0WfINFSAvOzyU4XPr4CYCVskX4C6CrBLCQ3VsrZf4eSbZ1ogQ6-Wkki5Ge8l4lM_NFb50ziCX3nBet_nTROSMQm_PgZMg-Yu6EEXE

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-03-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=171433090

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x600c00054988
Crash State:
  - crash stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  

Minimized Testcase (1.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97OlIfLd2g6v1ZXLL0SBijMcrDVwjnna0dwzmE-XYoTaTRFA_jkoTsz0ef8MQxPrgiYGJTvkuZl8XWOnXPgIS-LQSvN_O62Ky2M6qLotjxzt2U_ensie34YEqnAdxxq4Htv4-viO-_kuWFfx2UyL0uE2mlnUMRSr6nCWBV3Pr9GNOErwdI

### [Deleted User] (2013-03-21)

Bulk Edit

### [Deleted User] (2013-03-21)

Bulk edit

### [Deleted User] (2013-03-21)

Bulk edit

### in...@chromium.org (2013-03-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=173442025

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x600c0005f368
Crash State:
  - crash stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  

Minimized Testcase (0.91 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96xs5zxqc8p5UEg8v0yh8whPA1uVBCoZwLVPDNXK32kSB2g0HVue7EmeprnqRVG8sPr5yGzX8UWE9hBVLAk6IfQm-ccjjUWlbJi9tFl6MZgMi7Lyf8ca0GzLyA8BwBOWmUxxlp7zjOptF3-9an9LcshBibFWB9D26zY2Ot6nimI6Ry5oic

### ch...@gmail.com (2013-03-24)

[Comment Deleted]

### ts...@chromium.org (2013-03-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-04-02)

http://trac.webkit.org/changeset/147370

### cl...@chromium.org (2013-04-04)

ClusterFuzz has detected this issue as fixed in range 190946:191011.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=173442025

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x600c0005f368
Crash State:
  - crash stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=190946:191011

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96xs5zxqc8p5UEg8v0yh8whPA1uVBCoZwLVPDNXK32kSB2g0HVue7EmeprnqRVG8sPr5yGzX8UWE9hBVLAk6IfQm-ccjjUWlbJi9tFl6MZgMi7Lyf8ca0GzLyA8BwBOWmUxxlp7zjOptF3-9an9LcshBibFWB9D26zY2Ot6nimI6Ry5oic

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-04-16)

M27: https://src.chromium.org/viewvc/blink?view=rev&revision=148445

### ac...@chromium.org (2013-04-17)

A new patch was uploaded and landed in WebKit (https://bugs.webkit.org/show_bug.cgi?id=113531#c8) that I believe Blink should also adopt. I'll be uploading a Blink version shortly.

### ac...@chromium.org (2013-04-17)

Actually. I spoke too soon. I don't believe that patch is correct for the problems that we were seeing. I'll come up with a different patch to address the issue mentioned in that bug about configureTextTrackDisplay().

### sc...@gmail.com (2013-05-03)

Thanks Chamal and $1000 !

### ch...@gmail.com (2013-05-04)

Thank you very much for the reward!

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### ja...@chromium.org (2013-05-24)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### tk...@chromium.org (2014-06-20)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/177620?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077008)*
