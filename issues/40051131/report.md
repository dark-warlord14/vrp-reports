# Use-after-free in DOM Range 

| Field | Value |
|-------|-------|
| **Issue ID** | [40051131](https://issues.chromium.org/issues/40051131) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>DOM |
| **Reporter** | ax...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-11-11 |
| **Bounty** | $1,000.00 |

## Description

Use-after-free bug can be triggered when trying to clone range of removed child element.

**VERSION**  

Win XP SP3 17.0.932.0 dev-m  

Ubuntu 10.10 x64 17.0.937.0 (Developer Build 109620 Linux)  

It does not affects stable, beta not tested.

**REPRODUCTION CASE**  

In attachment.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==10045== ERROR: AddressSanitizer heap-use-after-free on address 0x7fb43f460bb0 at pc 0x7fb458a86824 bp 0x7ffff8a4b740 sp 0x7ffff8a4b738  

READ of size 8 at 0x7fb43f460bb0 thread T0  

#0 0x7fb458a86824 in WebCore::Node::nodeIndex() const asan\_malloc\_linux.cc:0  

#1 0x7fb458ad9386 in WebCore::RangeBoundaryPoint::ensureOffsetIsValid() const /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/RangeBoundaryPoint.h:89  

#2 0x7fb459f8c06b in WTF::PassRefPtr[WebCore::Range](javascript:void(0);)::leakRef() const /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:174  

#3 0x7fb457af7780 in HandleApiCallHelper /home/ams/Desktop/lch/depot\_tools/src/v8/src/builtins.cc:1178  

#4 0x38ff1500428e in  

0x7fb43f460bb0 is located 48 bytes inside of 104-byte region [0x7fb43f460b80,0x7fb43f460be8)  

freed by thread T0 here:  

#0 0x7fb45c3de926 in operator delete(void\*) *asan\_rtl*  

#1 0x7fb4589db234 in WebCore::ContainerNode::removeChild(WebCore::Node\*, int&) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:486  

#2 0x7fb458adc140 in WebCore::Range::surroundContents(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Range.cpp:1559  

#3 0x7fb459f895ad in WebCore::RangeInternal::surroundContentsCallback(v8::Arguments const&) /home/ams/Desktop/lch/depot\_tools/src/out/Release/obj/gen/webcore/bindings/V8Range.cpp:372  

#4 0x7fb457af7780 in HandleApiCallHelper /home/ams/Desktop/lch/depot\_tools/src/v8/src/builtins.cc:1178  

#5 0x38ff1500428e in  

#6 0x38ff1503cf1d in  

#7 0x38ff1503c976 in  

#8 0x38ff1503cbcd in  

#9 0x38ff1501f9a7 in  

#10 0x38ff1500a721 in  

#11 0x7fb457b41343 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /home/ams/Desktop/lch/depot\_tools/src/v8/src/execution.cc:118  

#12 0x7fb457aa68a5 in v8::internal::Isolate::handle\_scope\_implementer() /home/ams/Desktop/lch/depot\_tools/src/v8/src/isolate.h:838  

#13 0x7fb4590cc091 in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Page\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:509  

#14 0x7fb4590cbb71 in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:472  

#15 0x7fb4590be323 in WebCore::V8LazyEventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8LazyEventListener.cpp:72  

#16 0x7fb459894864 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:152  

#17 0x7fb459894549 in v8::Context::Scope::~Scope() /home/ams/Desktop/lch/depot\_tools/src/v8/include/v8.h:3497  

#18 0x7fb458a6fb64 in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:228  

#19 0x7fb458a6f5a0 in WebCore::Event::defaultPrevented() const /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Event.h:133  

#20 0x7fb458a98505 in WebCore::Node::handleLocalEvents(WebCore::Event\*) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2839  

#21 0x7fb458b398f2 in WTF::PassRefPtr[WebCore::Event](javascript:void(0);)::operator->() const /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:83  

#22 0x7fb458b34ce4 in WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher\*) const /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatchMediator.cpp:51  

#23 0x7fb458b36ab4 in WebCore::EventDispatcher::dispatchEvent(WebCore::Node\*, WTF::PassRefPtr[WebCore::EventDispatchMediator](javascript:void(0);)) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:55  

#24 0x7fb458a98b27 in WebCore::Node::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2853  

#25 0x7fb4596c8d1a in WebCore::DOMWindow::dispatchLoadEvent() /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1647  

#26 0x7fb458a01968 in WebCore::Document::dispatchWindowLoadEvent() /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:3469  

#27 0x7fb4595d2486 in WebCore::FrameLoader::checkCompleted() /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:786  

#28 0x7fb4595ce8d8 in WebCore::FrameLoader::finishedParsing() /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:670  

previously allocated by thread T0 here:  

#0 0x7fb45c3deba6 in operator new(unsigned long) *asan\_rtl*  

#1 0x7fb458a4efad in WebCore::Element::create(WebCore::QualifiedName const&, WebCore::Document\*) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:115  

#2 0x7fb4589f166c in WTF::PassRefPtr[WebCore::Element](javascript:void(0);)::leakRef() const /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:174  

#3 0x7fb458a512ce in WebCore::Element::cloneElementWithoutAttributesAndChildren() /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:176  

#4 0x7fb458a50db6 in WTF::PassRefPtr[WebCore::Element](javascript:void(0);)::leakRef() const /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:174  

#5 0x7fb458a50b13 in WTF::PassRefPtr[WebCore::Element](javascript:void(0);)::leakRef() const /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:174  

#6 0x7fb4589e1d77 in WebCore::ContainerNode::cloneChildNodes(WebCore::ContainerNode\*) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:864  

#7 0x7fb458a50b58 in WebCore::Element::cloneElementWithChildren() /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:154  

#8 0x7fb45a3efde2 in WTF::PassRefPtr[WebCore::Node](javascript:void(0);)::get() const /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:78  

#9 0x7fb457af7780 in HandleApiCallHelper /home/ams/Desktop/lch/depot\_tools/src/v8/src/builtins.cc:1178  

#10 0x38ff1500428e in  

#11 0x38ff1503ccf5 in  

#12 0x38ff1503c976 in  

#13 0x38ff1503cbcd in  

#14 0x38ff1501f9a7 in  

#15 0x38ff1500a721 in  

#16 0x7fb457b41343 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /home/ams/Desktop/lch/depot\_tools/src/v8/src/execution.cc:118  

#17 0x7fb457aa68a5 in v8::internal::Isolate::handle\_scope\_implementer() /home/ams/Desktop/lch/depot\_tools/src/v8/src/isolate.h:838  

#18 0x7fb4590cc091 in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Page\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:509  

#19 0x7fb4590cbb71 in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:472  

#20 0x7fb4590be323 in WebCore::V8LazyEventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) /home/ams/Desktop/lch/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8LazyEventListener.cpp:72  

==10045== ABORTING  

HINT: ASan doesn't collect stats. Set ASAN\_OPTIONS=stats=1 or call \_\_asan\_enable\_statistics(true)  

Stats: 0M malloced (0M for red zones) by 0 calls  

Stats: 0M realloced by 0 calls  

Stats: 0M freed by 0 calls  

Stats: 0M really freed by 0 calls  

Stats: 0M (0 full pages) mmaped in 0 calls  

mmaps by size class:  

mallocs by size class:  

frees by size class:  

rfrees by size class:  

Stats: malloc large: 0 small slow: 0  

Shadow byte and word:  

0x1ff687e8c176: fd  

0x1ff687e8c170: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ff687e8c150: 00 00 00 00 fb fb fb fb  

0x1ff687e8c158: fb fb fb fb fb fb fb fb  

0x1ff687e8c160: fa fa fa fa fa fa fa fa  

0x1ff687e8c168: fa fa fa fa fa fa fa fa  

=>0x1ff687e8c170: fd fd fd fd fd fd fd fd  

0x1ff687e8c178: fd fd fd fd fd fd fd fd  

0x1ff687e8c180: fa fa fa fa fa fa fa fa  

0x1ff687e8c188: fa fa fa fa fa fa fa fa  

0x1ff687e8c190: fd fd fd fd fd fd fd fd

## Attachments

- [a.svg](attachments/a.svg) (text/plain; charset=us-ascii, 38 B)
- [poc11-11-11.html](attachments/poc11-11-11.html) (text/html; charset=us-ascii, 717 B)

## Timeline

### ke...@chromium.org (2011-11-11)


Confirmed use-after-free on trunk (both Windows and Mac). I don't see crashes on any of the channels, though.

Is anyone able to verify either way on beta?

### sc...@gmail.com (2011-11-12)

I can do so easily on Monday.

In the mean time, putting our selection / editing ninja, Ryosuke, in the loop. Is this a tricky one or easy, Ryosuke?

### kc...@chromium.org (2011-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2011-11-13)

This is an easy fix.
http://trac.webkit.org/browser/trunk/Source/WebCore/dom/Range.cpp#L1557
1557	    while (Node* n = newParent->firstChild()) {
1558	        toContainerNode(newParent.get())->removeChild(n, ec);
1559	        if (ec)
1560	            return;
1561	    }

inferno & eae have fixed many bugs like this in Range.

### [Deleted User] (2011-11-13)

Oh, wait, this code is fine. Maybe:
http://trac.webkit.org/browser/trunk/Source/WebCore/dom/ContainerNode.cpp#L472
472	    Node* prev = child->previousSibling();
473	    Node* next = child->nextSibling();
474	    removeBetween(prev, next, child.get());
475	
476	    // Dispatch post-removal mutation events
477	    childrenChanged(false, prev, next, -1);
478	    dispatchSubtreeModifiedEvent();
?

### sc...@gmail.com (2011-11-14)

@rniwa: is the suspicion that the nodes are blown away by a synchronously-executed mutation observer? And we failed to RefPtr them?


### [Deleted User] (2011-11-14)

Right.

### sc...@gmail.com (2011-11-15)

Ok, you've inspired me to try and tackle this tomorrow :)

### sc...@gmail.com (2011-11-15)

This does seem to trigger under ASAN on M15, M16 for me. Seems like an old bug. Thanks for finding it, @Ax330d

### [Deleted User] (2011-11-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-18)

@Ax330d: I'm still looking at the best way to fix this bug.
It's an interesting bug, did you find it by fuzzing or code auditing?

### ax...@gmail.com (2011-11-18)

@scarybeasts, this bug was found by fuzzing. I was not digging in much into the problem, so, unfortunately, at the moment can't provide any useful information.

### sc...@gmail.com (2011-11-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-18)

https://bugs.webkit.org/show_bug.cgi?id=72757

### sc...@gmail.com (2011-11-19)

Committed r100827: <http://trac.webkit.org/changeset/100827>

Thank you @Ax330d, we will merge this fix in to the upcoming Chrome 16 release.

### sc...@gmail.com (2011-11-19)

@Ax330d: it probably won't surprise you to learn that this nice bug qualifies for a $1000 Chromium Security Reward!
Keep that fuzzer running, it's obviously doing some interesting things. I'm impressed it found this particular bug, because it requires a very specific node setup and ordering of calls.

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

### sc...@gmail.com (2011-11-23)

Merged to M16
http://trac.webkit.org/changeset/101034

### in...@chromium.org (2011-11-23)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/103921?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>DOM]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051131)*
