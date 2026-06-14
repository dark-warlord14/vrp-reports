# Security: UaF in controller of color chooser 

| Field | Value |
|-------|-------|
| **Issue ID** | [40078892](https://issues.chromium.org/issues/40078892) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2014-02-11 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 34.0.1833.4 canary  

32.0.1700.107 stable

Steps to repro:

1. Open Index.htm
2. Click on Step 1 button then you can see navigate.htm is opened and click on Step 2
3. In the end you'll see Index.htm is crashed

Crash ID : 63ba5dbda0797f00, f08ea60e1a972619

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State:  

eax=5fcb0066 ebx=00000000 ecx=04355d50 edx=5f34d8ff esi=043f1114 edi=0441e5a8  

eip=20030000 esp=0019ef38 ebp=0019ef54 iopl=0 nv up ei pl nz na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010206  

20030000 ?? ???  

\*\*\* WARNING: Unable to verify checksum for chrome\_child.dll  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it  

ChildEBP RetAddr  

WARNING: Frame IP not in any known module. Following frames may be wrong.  

0019ef34 5f34d90e 0x20030000  

0019ef3c 5e7f1fcf chrome\_child!blink::ColorChooserPopupUIController::endChooser+0xf [c:\b\build\slave\win-asan\build\src\third\_party\webkit\source\web\colorchooserpopupuicontroller.cpp @ 74]  

0019ef48 5e7f1e6b chrome\_child!WebCore::ColorInputType::~ColorInputType+0x1f [c:\b\build\slave\win-asan\build\src\third\_party\webkit\source\core\html\forms\colorinputtype.cpp @ 83]  

0019ef54 5e749544 chrome\_child!WebCore::ColorInputType::`scalar deleting destructor'+0xb 0019ef68 5e7491eb chrome_child!WebCore::HTMLInputElement::~HTMLInputElement+0x114 [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\core\html\htmlinputelement.cpp @ 172] 0019ef74 5e4a658e chrome_child!WebCore::HTMLInputElement::`scalar deleting destructor'+0xb  

0019ef98 5e4a2f45 chrome\_child!WebCore::removeDetachedChildrenInContainer[WebCore::Node,WebCore::ContainerNode](javascript:void(0);)+0x8e [c:\b\build\slave\win-asan\build\src\third\_party\webkit\source\core\dom\containernodealgorithms.h @ 102]  

0019efa8 5e7a398b chrome\_child!WebCore::ContainerNode::~ContainerNode+0x45 [c:\b\build\slave\win-asan\build\src\third\_party\webkit\source\core\dom\containernode.cpp @ 99]  

0019efb4 5e49d0b3 chrome\_child!WebCore::HTMLBRElement::`scalar deleting destructor'+0xb 0019efc8 5e4a8aaa chrome_child!WTF::VectorDestructor<1,WTF::RefPtr<WebCore::Element> >::destruct+0x63 [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\wtf\vector.h @ 60] 0019efd8 5e4a7711 chrome_child!WTF::Vector<WTF::RefPtr<WebCore::Element>,0,WTF::DefaultAllocator>::shrinkCapacity+0x1a [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\wtf\vector.h @ 934] 0019efe0 5e48a089 chrome_child!WebCore::FullscreenElementStack::documentWasDisposed+0x21 [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\core\dom\fullscreenelementstack.cpp @ 130] 0019f008 5e48d7e7 chrome_child!WebCore::DocumentLifecycleNotifier::notifyDocumentWasDisposed+0x49 [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\core\dom\documentlifecyclenotifier.h @ 70] 0019f024 5e47792a chrome_child!WebCore::Document::dispose+0x277 [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\core\dom\document.cpp @ 621] 0019f028 5e477e80 chrome_child!WebCore::TreeScope::removedLastRefToScope+0x3a [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\core\dom\node.cpp @ 2404] 0019f030 5e83f1ac chrome_child!WebCore::TreeShared<WebCore::Node>::deref+0x40 [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\core\dom\treeshared.h @ 81] 0019f048 5e83f922 chrome_child!WebCore::DOMWindow::clearDocument+0x6c [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\core\frame\domwindow.cpp @ 362] 0019f058 5e83f11b chrome_child!WebCore::DOMWindow::~DOMWindow+0x32 [c:\b\build\slave\win-asan\build\src\third_party\webkit\source\core\frame\domwindow.cpp @ 515] 0019f064 5ed4a331 chrome_child!WebCore::DOMWindow::`scalar deleting destructor'+0xb  

0019f074 5ebad711 chrome\_child!WebCore::V8IDBDatabase::derefObject+0x41 [c:\b\build\slave\win-asan\build\src\out\release\gen\blink\bindings\v8idbdatabase.cpp @ 478]

## Attachments

- [index.htm](attachments/index.htm) (text/html, 149 B)
- [navigate.htm](attachments/navigate.htm) (text/html, 330 B)
- [repro.html](attachments/repro.html) (text/html, 487 B)

## Timeline

### jl...@chromium.org (2014-02-12)

Reproduced on tip of tree:

=================================================================
==7==ERROR: AddressSanitizer: heap-use-after-free on address 0x6040001ed510 at pc 0x7fbd6d4b27d2 bp 0x7fff4df5a750 sp 0x7fff4df5a748
READ of size 8 at 0x6040001ed510 thread T0 (chrome)
    #0 0x7fbd6d4b27d1 in endChooser /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/web/ColorChooserPopupUIController.cpp:73
    #1 0x7fbd6d4b2bef in _ZThn8_N5blink29ColorChooserPopupUIController10endChooserEv /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/web/ColorChooserPopupUIController.cpp:76
    #2 0x7fbd78e6149f in endColorChooser /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/html/forms/ColorInputType.cpp:200
    #3 0x7fbd78e610fd in ~ColorInputType /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/html/forms/ColorInputType.cpp:82
    #4 0x7fbd78e6160d in ~ColorInputType /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/html/forms/ColorInputType.cpp:81
    #5 0x7fbd7893138f in deref /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/wtf/RefCounted.h:181
    #6 0x7fbd78931913 in derefIfNotNull<WebCore::InputType> /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/wtf/PassRefPtr.h:57
    #7 0x7fbd78928980 in ~RefPtr /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/wtf/RefPtr.h:51
    #8 0x7fbd788fa13e in ~HTMLInputElement /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/html/HTMLInputElement.cpp:172
    #9 0x7fbd788fa63d in ~HTMLInputElement /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/html/HTMLInputElement.cpp:162
    #10 0x7fbd7721328c in removeDetachedChildrenInContainer<WebCore::Node, WebCore::ContainerNode> /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:102
    #11 0x7fbd771ff4fb in removeDetachedChildren /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:83
    #12 0x7fbd77200a14 in ~ContainerNode /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:98
    #13 0x7fbd7750f8c8 in ~Element /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:218


0x6040001ed510 is located 0 bytes inside of 48-byte region [0x6040001ed510,0x6040001ed540)
freed by thread T0 (chrome) here:
    #0 0x7fbda5db4e61 in operator delete _asan_rtl_
    #1 0x7fbd5fcd297e in ~RendererWebColorChooserImpl /home/julien/sources/chrome/src/out/Debug/../../content/renderer/renderer_webcolorchooser_impl.cc:25
    #2 0x7fbd5fcd2b13 in _ZThn8_N7content27RendererWebColorChooserImplD0Ev /home/julien/sources/chrome/src/out/Debug/../../content/renderer/renderer_webcolorchooser_impl.cc:26
    #3 0x7fbd5e68595c in _ZN7content18RenderViewObserver10OnDestructEv /home/julien/sources/chrome/src/out/Debug/../../content/public/renderer/render_view_observer.cc:32
    #4 0x7fbd5f9c3799 in ~RenderViewImpl /home/julien/sources/chrome/src/out/Debug/../../content/renderer/render_view_impl.cc:1027
    #5 0x7fbd5f9c3d48 in ~RenderViewImpl /home/julien/sources/chrome/src/out/Debug/../../content/renderer/render_view_impl.cc:995
    #6 0x7fbd5f9c4531 in ~RenderViewImpl /home/julien/sources/chrome/src/out/Debug/../../content/renderer/render_view_impl.cc:995
    #7 0x7fbd5fc12f53 in _ZNK4base10RefCountedIN7content12RenderWidgetEE7ReleaseEv /home/julien/sources/chrome/src/out/Debug/../../base/memory/ref_counted.h:131
    #8 0x7fbd5fc5aa33 in _ZN4base8internal13MaybeRefcountILb1EPN7content12RenderWidgetEE7ReleaseES4_ /home/julien/sources/chrome/src/out/Debug/../../base/bind_helpers.h:462
    #9 0x7fbd5fc5a6ef in ~BindState /home/julien/sources/chrome/src/out/Debug/../../base/bind_internal.h:2565
    #10 0x7fbd5fc5a891 in ~BindState /home/julien/sources/chrome/src/out/Debug/../../base/bind_internal.h:2565
    #11 0x7fbd9854231c in _ZN4base20RefCountedThreadSafeINS_8internal13BindStateBaseENS_33DefaultRefCountedThreadSafeTraitsIS2_EEE14DeleteInternalEPKS2_ /home/julien/sources/chrome/src/out/Debug/../../base/memory/ref_counted.h:190
    #12 0x7fbd98542119 in _ZN4base33DefaultRefCountedThreadSafeTraitsINS_8internal13BindStateBaseEE8DestructEPKS2_ /home/julien/sources/chrome/src/out/Debug/../../base/memory/ref_counted.h:153
    #13 0x7fbd98541f94 in _ZNK4base20RefCountedThreadSafeINS_8internal13BindStateBaseENS_33DefaultRefCountedThreadSafeTraitsIS2_EEE7ReleaseEv /home/julien/sources/chrome/src/out/Debug/../../base/memory/ref_counted.h:181
    #14 0x7fbd9874b3a0 in ~scoped_refptr /home/julien/sources/chrome/src/out/Debug/../../base/memory/ref_counted.h:289
    #15 0x7fbd9874aa99 in ~CallbackBase /home/julien/sources/chrome/src/out/Debug/../../base/callback_internal.cc:35
    #16 0x7fbd9864ec3c in ~Callback /home/julien/sources/chrome/src/out/Debug/../../base/callback_forward.h:11
    #17 0x7fbd98f44a9b in ~PendingTask /home/julien/sources/chrome/src/out/Debug/../../base/pending_task.cc:38


previously allocated by thread T0 (chrome) here:
    #0 0x7fbda5db4a21 in operator new _asan_rtl_
    #1 0x7fbd5fa0b763 in _ZN7content14RenderViewImpl18createColorChooserEPN5blink21WebColorChooserClientERKjRKNS1_9WebVectorINS1_18WebColorSuggestionEEE /home/julien/sources/chrome/src/out/Debug/../../content/renderer/render_view_impl.cc:2507
    #2 0x7fbd5fa0be2b in _ZThn1304_N7content14RenderViewImpl18createColorChooserEPN5blink21WebColorChooserClientERKjRKNS1_9WebVectorINS1_18WebColorSuggestionEEE /home/julien/sources/chrome/src/out/Debug/../../content/renderer/render_view_impl.cc:2515
    #3 0x7fbd6d4bd386 in openColorChooser /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/web/ColorChooserUIController.cpp:89
    #4 0x7fbd6d4b21bc in openUI /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/web/ColorChooserPopupUIController.cpp:67
    #5 0x7fbd6d47732b in createColorChooser /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/web/ChromeClientImpl.cpp:588
    #6 0x7fbd7b072897 in createColorChooser /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/page/Chrome.cpp:337
    #7 0x7fbd78e63b02 in handleDOMActivateEvent /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/html/forms/ColorInputType.cpp:163
    #8 0x7fbd78916221 in defaultEventHandler /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/html/HTMLInputElement.cpp:1139
    #9 0x7fbd77b160fa in dispatchEventPostProcess /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/events/EventDispatcher.cpp:201
    #10 0x7fbd77b12c8c in dispatch /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/events/EventDispatcher.cpp:119
    #11 0x7fbd77b1b990 in dispatchEvent /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/events/EventDispatchMediator.cpp:52
    #12 0x7fbd77b10fb9 in dispatchEvent /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/events/EventDispatcher.cpp:48
    #13 0x7fbd77bb8f9c in dispatchEvent /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/events/ScopedEventQueue.cpp:83
    #14 0x7fbd77bb8c6b in enqueueEventDispatchMediator /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/events/ScopedEventQueue.cpp:67
    #15 0x7fbd77b11803 in dispatchScopedEvent /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/events/EventDispatcher.cpp:69
    #16 0x7fbd77713d14 in dispatchScopedEventDispatchMediator /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/dom/Node.cpp:2197
    #17 0x7fbd77713b49 in dispatchScopedEvent /home/julien/sources/chrome/src/out/Debug/../../third_party/WebKit/Source/core/dom/Node.cpp:2192

### jl...@chromium.org (2014-02-12)

Leishi, could you please take a look or assign to someone else?

### jl...@chromium.org (2014-02-12)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-02-12)

chromium.khalil: if you manage to create a repro that triggers automatically, please add it here, it'll make it a lot easier for us to use our automated systems to track regression ranges.

### cl...@chromium.org (2014-02-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2014-02-12)

jln: I'll try that today.

### ch...@gmail.com (2014-02-13)

Seems like impossible to create a repro that triggers automatically, because of window.close().

### cl...@chromium.org (2014-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-20)

keishi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ch...@gmail.com (2014-02-20)

keishi@ you fixed a very similar bug to this before, could you please take a look?

### cl...@chromium.org (2014-03-01)

keishi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ch...@gmail.com (2014-03-04)

keishi@ any updates on this bug?


### ke...@chromium.org (2014-03-04)

I think this is a duplicate of 331790.
I'm sorry this took so long. This looked identical to the other one.

### ch...@gmail.com (2014-03-04)

keishi, thanks for the reply, actually I'm still able to repro this bug on the latest version of stable 33.0.1750.146 and canary, and https://crbug.com/chromium/331790 it's already fixed in 33.0.1750.117

### pa...@chromium.org (2014-03-04)

I am also able to get an Aw, Snap on ToT for Linux. I don't think this bug is fixed.

That is potentially separate to the issue of whether or not this bug is a duplicate of 331790. The repros and the stacks seem different enough that I suspect 2 distinct bugs. But I could be wrong, I'm no Blink expert.

keishi, can you please take another look, or let us know who can? Thank you!

### ke...@chromium.org (2014-03-05)

Sorry. This is a new bug. I will fix this.

### ke...@chromium.org (2014-03-05)

CL in review. https://codereview.chromium.org/181233006/

### bu...@chromium.org (2014-03-06)

------------------------------------------------------------------------
r255276 | keishi@chromium.org | 2014-03-06T06:08:23.776110Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/renderer_webcolorchooser_impl.h?r1=255276&r2=255275&pathrev=255276

RendererWebColorChooserImpl shouldn't be destroyed by RenderViewObserver::OnDestruct

RenderWebColorChooserImpl is owned by blink::ColorChooserUIController so it should not be destroyed in RenderViewObserver::OnDestruct

BUG=342735

Review URL: https://codereview.chromium.org/181233006
------------------------------------------------------------------------

### in...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-03-07)

Adding label for consideration of reward.

### ti...@chromium.org (2014-03-07)

Removing label - we'll add it again when the fix is merged.

### ke...@chromium.org (2014-03-11)

Confirmed fix in 35.0.1882.0 canary
Requesting merge to M34

### dx...@chromium.org (2014-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-03-12)

------------------------------------------------------------------------
r256408 | keishi@chromium.org | 2014-03-12T02:23:09.841742Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/content/renderer/renderer_webcolorchooser_impl.h?r1=256408&r2=256407&pathrev=256408

Merge 255276 "RendererWebColorChooserImpl shouldn't be destroyed..."

> RendererWebColorChooserImpl shouldn't be destroyed by RenderViewObserver::OnDestruct
> 
> RenderWebColorChooserImpl is owned by blink::ColorChooserUIController so it should not be destroyed in RenderViewObserver::OnDestruct
> 
> BUG=342735
> 
> Review URL: https://codereview.chromium.org/181233006

TBR=keishi@chromium.org

Review URL: https://codereview.chromium.org/196413003
------------------------------------------------------------------------

### ti...@chromium.org (2014-03-28)

keishi@ - looks like this was merged into M33 (branch 1750)? Was this also merged to M34 (branch 1847)? If not, please merge into M34 as well.

### ke...@chromium.org (2014-03-31)

Sorry, merged to M34.

### bu...@chromium.org (2014-03-31)

------------------------------------------------------------------
r260483 | keishi@chromium.org | 2014-03-31T02:16:58.142256Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/renderer/renderer_webcolorchooser_impl.h?r1=260483&r2=260482&pathrev=260483

Merge 255276 "RendererWebColorChooserImpl shouldn't be destroyed..."

> RendererWebColorChooserImpl shouldn't be destroyed by RenderViewObserver::OnDestruct
> 
> RenderWebColorChooserImpl is owned by blink::ColorChooserUIController so it should not be destroyed in RenderViewObserver::OnDestruct
> 
> BUG=342735
> 
> Review URL: https://codereview.chromium.org/181233006

TBR=keishi@chromium.org

Review URL: https://codereview.chromium.org/218893002
-----------------------------------------------------------------

### ch...@gmail.com (2014-03-31)

[Comment Deleted]

### ch...@gmail.com (2014-03-31)

Is this report qualified for a reward?

### in...@chromium.org (2014-03-31)

Yes it is.

### ti...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-04)

Needs interaction, lowering severity.

### ch...@gmail.com (2014-04-04)

I created a new repro to make the interaction more easy.

### in...@chromium.org (2014-04-04)

Any interaction lowers the severity, and this one needs full screen(which is significant).

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### ch...@gmail.com (2014-04-05)

[Comment Deleted]

### ch...@gmail.com (2014-04-05)

inferno@ Thank you for the explain :), But I'm able to repro this crash without webkitRequestFullScreen() if I change the 40 ms timeout to 01 seconds:  

    window.onclick = function() {
      window.close();
      setTimeout('t.click();', 01);
    }

### ti...@chromium.org (2014-04-14)

Thanks for the report - $1000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-12)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-06-17)

Processing via our e-payment system can take up to 6-8 weeks, but the reward should be on its way to you. Thanks again for your help!


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

This issue was migrated from crbug.com/chromium/342735?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078892)*
