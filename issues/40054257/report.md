# Heap-buffer-overflow in WebCore::SVGDocumentExtensions::removeAnimationElementFromTarget

| Field | Value |
|-------|-------|
| **Issue ID** | [40054257](https://issues.chromium.org/issues/40054257) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | ax...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-02-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap buffer overflow occurs when removing animation element from document.

**VERSION**  

Version 19.0.1050.0 (123195) - Developer Build on Ubuntu 10.10  

17.0.963.56 m, Win7 x64

**REPRODUCTION CASE**  

In attachment.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==2709== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f36c2fa8c88 at pc 0x5bed0de bp 0x7fffe0e074f0 sp 0x7fffe0e074e8  

READ of size 8 at 0x7f36c2fa8c88 thread T0  

#0 0x5bed0de in WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >::remove(WebCore::SVGSMILElement\* const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/HashTable.h:826  

#1 0x5e25232 in WebCore::SVGSMILElement::~SVGSMILElement() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/animation/SVGSMILElement.cpp:146  

#2 0x5d9b7ee in WebCore::SVGSetElement::~SVGSetElement() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGSetElement.h:30  

#3 0x3d5ce34 in void WebCore::removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode>(WebCore::ContainerNode\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:51  

#4 0x3d5df52 in ~ContainerNode /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:110  

#5 0x5bf8d3e in WebCore::SVGElement::~SVGElement() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGElement.cpp:89  

#6 0x5d8a05c in non-virtual thunk to WebCore::SVGSVGElement::~SVGSVGElement() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGSVGElement.cpp:103  

#7 0x2c6b589 in v8::internal::RuntimeProfiler::IsEnabled() /media/Chromium/chromium/depot\_tools/src/v8/src/runtime-profiler.h:50  

0x7f36c2fa8c88 is located 8 bytes to the right of 1024-byte region [0x7f36c2fa8880,0x7f36c2fa8c80)  

allocated by thread T0 here:  

#0 0x80137e2 in malloc ??:0  

#1 0x38e1cbf in WTF::fastMalloc(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:268  

#2 0x5bf52e2 in WTF::HashTable<WebCore::SVGElement\*, std::pair<WebCore::SVGElement\*, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*>, WTF::PairFirstExtractor<std::pair<WebCore::SVGElement\*, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*> >, WTF::PtrHash[WebCore::SVGElement\\*](javascript:void(0);), WTF::PairHashTraits<WTF::HashTraits[WebCore::SVGElement\\*](javascript:void(0);), WTF::HashTraits<WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*> >, WTF::HashTraits[WebCore::SVGElement\\*](javascript:void(0);) >::rehash(int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/HashTable.h:965  

#3 0x5bf4b8f in std::pair<WTF::HashTableIterator<WebCore::SVGElement\*, std::pair<WebCore::SVGElement\*, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*>, WTF::PairFirstExtractor<std::pair<WebCore::SVGElement\*, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*> >, WTF::PtrHash[WebCore::SVGElement\\*](javascript:void(0);), WTF::PairHashTraits<WTF::HashTraits[WebCore::SVGElement\\*](javascript:void(0);), WTF::HashTraits<WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*> >, WTF::HashTraits[WebCore::SVGElement\\*](javascript:void(0);) >, bool> WTF::HashTable<WebCore::SVGElement\*, std::pair<WebCore::SVGElement\*, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*>, WTF::PairFirstExtractor<std::pair<WebCore::SVGElement\*, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*> >, WTF::PtrHash[WebCore::SVGElement\\*](javascript:void(0);), WTF::PairHashTraits<WTF::HashTraits[WebCore::SVGElement\\*](javascript:void(0);), WTF::HashTraits<WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*> >, WTF::HashTraits[WebCore::SVGElement\\*](javascript:void(0);) >::add<WTF::HashMapTranslator<WTF::PairHashTraits<WTF::HashTraits[WebCore::SVGElement\\*](javascript:void(0);), WTF::HashTraits<WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*> >, WTF::PtrHash[WebCore::SVGElement\\*](javascript:void(0);) >, WebCore::SVGElement\*, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*>(WebCore::SVGElement\* const&, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\* const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/HashTable.h:674  

#4 0x5becc06 in WTF::HashMap<WebCore::SVGElement\*, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*, WTF::PtrHash[WebCore::SVGElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGElement\\*](javascript:void(0);), WTF::HashTraits<WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\*> >::inlineAdd(WebCore::SVGElement\* const&, WTF::HashSet<WebCore::SVGSMILElement\*, WTF::PtrHash[WebCore::SVGSMILElement\\*](javascript:void(0);), WTF::HashTraits[WebCore::SVGSMILElement\\*](javascript:void(0);) >\* const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/HashMap.h:325  

#5 0x5e2f96b in WebCore::SVGSMILElement::targetElement() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/animation/SVGSMILElement.cpp:527  

#6 0x5e198ae in WebCore::SMILTimeContainer::updateAnimations(WebCore::SMILTime) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/animation/SMILTimeContainer.cpp:249  

#7 0x5e181ea in WebCore::SMILTimeContainer::begin() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/animation/SMILTimeContainer.cpp:97  

#8 0x5bec154 in WebCore::SVGDocumentExtensions::startAnimations() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGDocumentExtensions.cpp:103  

#9 0x3d8f7d5 in WebCore::Document::implicitClose() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:2361  

#10 0x4a85c26 in WebCore::FrameLoader::checkCompleted() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:796  

#11 0x4a824e8 in WebCore::FrameLoader::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:678  

#12 0x3daddea in WebCore::Frame::page() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/Frame.h:346  

#13 0x4a677b4 in WebCore::DocumentWriter::endIfNotLoadingMainResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:233  

#14 0x4a9ece9 in WebCore::ResourceErrorBase::isNull() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/network/ResourceErrorBase.h:42  

#15 0x4ac5e81 in WebCore::MainResourceLoader::didFinishLoading(double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:485  

#16 0x620173d in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:659  

#17 0x36c337a in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:489  

#18 0x36c45ab in void DispatchToMethod<ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks>(ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), Tuple4<int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks> const&) /media/Chromium/chromium/depot\_tools/src/./base/tuple.h:566  

#19 0x36c0afc in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:559  

#20 0x36be9d0 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

#21 0x35c121f in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:171  

#22 0x3753853 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:268  

#23 0x1e98086 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot\_tools/src/./base/callback.h:272  

==2709== ABORTING  

Stats: 27M malloced (25M for red zones) by 52703 calls  

Stats: 0M realloced by 1151 calls  

Stats: 24M freed by 41242 calls  

Stats: 0M really freed by 0 calls  

Stats: 84M (21518 full pages) mmaped in 21 calls  

mmaps by size class: 8:49149; 9:8191; 10:8190; 11:2047; 12:1024; 13:1536; 14:256; 15:256; 16:64; 17:32; 18:16; 19:8; 20:4; 22:2;  

mallocs by size class: 8:40104; 9:5891; 10:3894; 11:1156; 12:282; 13:1049; 14:127; 15:132; 16:21; 17:31; 18:10; 19:2; 20:2; 22:2;  

frees by size class: 8:30131; 9:5257; 10:3509; 11:851; 12:197; 13:1014; 14:111; 15:125; 16:14; 17:17; 18:10; 19:2; 20:2; 22:2;  

rfrees by size class:  

Stats: malloc large: 47 small slow: 298  

Shadow byte and word:  

0x1fe6d85f5191: fa  

0x1fe6d85f5190: fa fa fa fa fa fa fa fa  

More shadow bytes:  

0x1fe6d85f5170: 00 00 00 00 00 00 00 00  

0x1fe6d85f5178: 00 00 00 00 00 00 00 00  

0x1fe6d85f5180: 00 00 00 00 00 00 00 00  

0x1fe6d85f5188: 00 00 00 00 00 00 00 00  

=>0x1fe6d85f5190: fa fa fa fa fa fa fa fa  

0x1fe6d85f5198: fa fa fa fa fa fa fa fa  

0x1fe6d85f51a0: fa fa fa fa fa fa fa fa  

0x1fe6d85f51a8: fa fa fa fa fa fa fa fa  

0x1fe6d85f51b0: fa fa fa fa fa fa fa fa

## Attachments

- [tc-28-02-12-hbo.zip](attachments/tc-28-02-12-hbo.zip) (application/zip; charset=binary, 602 B)

## Timeline

### in...@chromium.org (2012-02-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-28)

Schenney@, can you please triage and see if it is a dup of the existing svg bugs ?

### in...@chromium.org (2012-02-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=22760351

Uploader: aarya@google.com

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x7f51180c4c88
Crash State:
  - crash stack -
  WebCore::SVGDocumentExtensions::removeAnimationElementFromTarget
  WebCore::SVGSMILElement::~SVGSMILElement
  WebCore::SVGSetElement::~SVGSetElement
  

Minimized Testcase (0.48 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96-N2T8BxfGFBudPF8n_mgnW50wHujnbSHDRvmWawcS1D6hfnpBlpZ22uEmUsx-l-Pf9t9Zf-fL-i_cQ9gEILJ2jIUBogfuDJPrh01OENQX1vTGszpNNY4ug5GxxM9rqOuioaWwmf8hHEpn_q-W03VNndRQGw

### in...@chromium.org (2012-02-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-28)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-28)

Will investigate.

### in...@chromium.org (2012-02-28)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-28)

Upstreamed to https://bugs.webkit.org/show_bug.cgi?id=79831

This is not fixed by the other recent fixes.

### in...@chromium.org (2012-03-01)

in r+, cq+, should land today.

### sc...@chromium.org (2012-03-01)

Committed upstream r109345: <http://trac.webkit.org/changeset/109345>

This patch should merge directly into earlier branches. I'm relying on the security team to look after that. Let me know if it does not.

Merge requested for m17 and m18.

### in...@chromium.org (2012-03-01)

We will merge it in our merge fest today.

### sc...@gmail.com (2012-03-01)

M17: http://trac.webkit.org/changeset/109390
M18: http://trac.webkit.org/changeset/109391

### sc...@gmail.com (2012-03-03)

Different to the other SVG issues.
Therefore $1000

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

### sc...@gmail.com (2012-03-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-21)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/116093?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054257)*
