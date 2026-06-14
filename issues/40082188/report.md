# Heap-use-after-free in blink::Frame::deprecatedLocalOwner

| Field | Value |
|-------|-------|
| **Issue ID** | [40082188](https://issues.chromium.org/issues/40082188) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Reporter** | at...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2015-05-28 |
| **Bounty** | $2,000.00 |

## Description


Tested on:

OS: Ubuntu 14.04

Chromium	45.0.2415.0 (Developer Build) (64-bit)
Revision	2bd661311e3192357d72532c87b575bb0f37ae7b-refs/heads/master@{#331701}


Note: The crash is reliable and without timing issues but it takes some time to trigger, so ClusterFuzz might have problems when reproducing this issue. The free-stack has some GC frames, so manually set gc sweeps in right positions could speed up the crash.

ASAN-trace:

==7702==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110000407e8 at pc 0x7f3b8885633e bp 0x7fff5651f8c0 sp 0x7fff5651f8b8
READ of size 8 at 0x6110000407e8 thread T0 (chrome)
    #0 0x7f3b8885633d in blink::Frame::deprecatedLocalOwner() const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/frame/Frame.cpp:147:23
    #1 0x7f3b8885711e in blink::Frame::ownerLayoutObject() const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/frame/Frame.cpp:274:10
    #2 0x7f3b86dce066 in blink::frameContentAsPlainText(unsigned long, blink::LocalFrame*, WTF::StringBuilder&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/web/WebLocalFrameImpl.cpp:276:41
    #3 0x7f3b86dcd91a in blink::WebLocalFrameImpl::contentAsText(unsigned long) const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/web/WebLocalFrameImpl.cpp:1527:5
    #4 0x7f3b82f69689 in ChromeRenderViewObserver::CaptureText(blink::WebFrame*, std::__1::basic_string<unsigned short, base::string16_char_traits, std::__1::allocator<unsigned short> >*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../chrome/renderer/chrome_render_view_observer.cc:442:15
    #5 0x7f3b82f68d1c in ChromeRenderViewObserver::CapturePageInfo(bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../chrome/renderer/chrome_render_view_observer.cc:416:3
.
.
.
0x6110000407e8 is located 104 bytes inside of 200-byte region [0x611000040780,0x611000040848)
freed by thread T0 (chrome) here:
    #0 0x7f3b81c83dab in __interceptor_free ??:0:0
    #1 0x7f3b87ca9ac4 in blink::Node::removedLastRef() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:2313:5
    #2 0x7f3b86dac743 in blink::TreeShared<blink::Node>::deref() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/TreeShared.h:82:13
    #3 0x7f3b861b0bb5 in v8::internal::GlobalHandles::PendingPhantomCallback::Invoke(v8::internal::Isolate*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/global-handles.cc:832:3
    #4 0x7f3b861b076e in v8::internal::GlobalHandles::DispatchPendingPhantomCallbacks() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/global-handles.cc:814:5
    #5 0x7f3b861b0e90 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/global-handles.cc:848:18
.
.
.
previously allocated by thread T0 (chrome) here:
    #0 0x7f3b81c8408b in __interceptor_malloc ??:0:0
    #1 0x7f3b87c9011a in partitionAlloc /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:541:20
    #2 0x7f3b87c9011a in blink::Node::operator new(unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:118:0
    #3 0x7f3b9207ead3 in blink::HTMLIFrameElement::create(blink::Document&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLIFrameElement.cpp:47:1
    #4 0x7f3b89fe61d0 in blink::iframeConstructor(blink::Document&, blink::HTMLFormElement*, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/gen/blink/core/HTMLElementFactory.cpp:613:12
    #5 0x7f3b89fdf093 in blink::HTMLElementFactory::createHTMLElement(WTF::AtomicString const&, blink::Document&, blink::HTMLFormElement*, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/gen/blink/core/HTMLElementFactory.cpp:1248:16
    #6 0x7f3b87b442d7 in blink::Document::createElement(blink::QualifiedName const&, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1053:13
.
.
.

## Attachments

- [chrome-heap-use-after-free-blinkFramedeprecatedLocalOwner.html](attachments/chrome-heap-use-after-free-blinkFramedeprecatedLocalOwner.html) (text/html, 693 B)

## Timeline

### in...@chromium.org (2015-05-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-05-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-05-28)

Adding reward-topanel since our repro in c#1 was junk, we never got it to reproduce.

### cl...@chromium.org (2015-05-30)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5296726806626304

### cl...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-04)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### oc...@chromium.org (2015-06-04)

japhet@, dcheng@, could you please take a look or assign to someone else when you have time? The testcase appears to be a very reliable repro.

### oc...@chromium.org (2015-06-04)

Changing impact since this seems to repro on stable as well.

### cl...@chromium.org (2015-06-04)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-06-06)

I'll take a look on Monday... why does ClusterFuzz say "Status	Unreproducible (trunk)" though?

### mb...@chromium.org (2015-06-06)

When it was uploaded, it didn't crash in ClusterFuzz. Based on c#0, it's probably timing out.

### mb...@chromium.org (2015-06-06)

When it was uploaded, it didn't crash in ClusterFuzz. Based on c#0, it's probably timing out.

### ja...@chromium.org (2015-06-10)

This is some weird behavior in ChildFrameDisconnector when the page contains over 1000 frames (i.e, the max we actually allow to load). In debug builds, the test case reliably asserts inside checkConnectedSubframeCountIsConsistent() in ChildFrameDisconnector.cpp.

### bu...@chromium.org (2015-06-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=197139

------------------------------------------------------------------
r197139 | japhet@chromium.org | 2015-06-15T21:26:44.261946Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/NodeRareData.cpp?r1=197139&r2=197138&pathrev=197139
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLFrameOwnerElement.cpp?r1=197139&r2=197138&pathrev=197139
   A http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/data/max-frames-detach.html?r1=197139&r2=197138&pathrev=197139
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/NodeRareData.h?r1=197139&r2=197138&pathrev=197139
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/LocalFrame.cpp?r1=197139&r2=197138&pathrev=197139
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/WebFrameTest.cpp?r1=197139&r2=197138&pathrev=197139

Fix the logic that limits the number of frames in a page.

This check apparently doesn't run soon enough, and we can create more than the
intended limit of 1000 frames. Once we hit 1024,
NodeRareData::m_connecetedFrameCount can overflow and we no longer fully detach
Frames from their owners at teardown.

BUG=493243
TEST=WebFrameTest.MaxFramesDetach

Review URL: https://codereview.chromium.org/1180603002
-----------------------------------------------------------------

### in...@chromium.org (2015-06-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2015-07-08)

Merge-Requested for M44 (branch 2403).

### pe...@google.com (2015-07-08)

[Automated comment] Less than 2 weeks to go before stable on M44, manual review required.

### pe...@google.com (2015-07-10)

Approved for merge to m44 branch 2403.  Please get the merge done before end of business PST Monday.

### bu...@chromium.org (2015-07-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=198702

------------------------------------------------------------------
r198702 | japhet@chromium.org | 2015-07-10T18:18:26.821649Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/core/dom/NodeRareData.h?r1=198702&r2=198701&pathrev=198702
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/core/frame/LocalFrame.cpp?r1=198702&r2=198701&pathrev=198702
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/web/tests/WebFrameTest.cpp?r1=198702&r2=198701&pathrev=198702
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/core/dom/NodeRareData.cpp?r1=198702&r2=198701&pathrev=198702
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/core/html/HTMLFrameOwnerElement.cpp?r1=198702&r2=198701&pathrev=198702
   A http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/web/tests/data/max-frames-detach.html?r1=198702&r2=198701&pathrev=198702

Merge 197139 "Fix the logic that limits the number of frames in ..."

> Fix the logic that limits the number of frames in a page.
> 
> This check apparently doesn't run soon enough, and we can create more than the
> intended limit of 1000 frames. Once we hit 1024,
> NodeRareData::m_connecetedFrameCount can overflow and we no longer fully detach
> Frames from their owners at teardown.
> 
> BUG=493243
> TEST=WebFrameTest.MaxFramesDetach
> 
> Review URL: https://codereview.chromium.org/1180603002

TBR=japhet@chromium.org

Review URL: https://codereview.chromium.org/1233453006
-----------------------------------------------------------------

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-07-18)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### la...@google.com (2015-08-04)

Manually move from Cr-Blink-GarbageCollection to Cr-Blink-MemoryAllocator-GarbageCollection

### ti...@google.com (2015-08-17)

Congrats: $2000 for this report.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-09-27)

Bulk update: removing view restriction from closed bugs.

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

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### is...@google.com (2021-09-16)

This issue was migrated from crbug.com/chromium/493243?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/486390, crbug.com/chromium/510704]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082188)*
