# Bad-cast to blink::RenderBox from blink::RenderText;RenderBox.h:769:1

| Field | Value |
|-------|-------|
| **Issue ID** | [40080179](https://issues.chromium.org/issues/40080179) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout>Grid |
| **Reporter** | rh...@partner.samsung.com |
| **Assignee** | jc...@chromium.org |
| **Created** | 2014-08-07 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Security assertion fires since a RenderText is erroneously cast to a RenderBox.

**VERSION**  

Chrome Version: 38.0.2116.0 (Developer Build 287842), Blink @179578  

Operating System: Ubuntu 13.10

**REPRODUCTION CASE**  

Run a debug chromium with --enable-experimental-web-platform-features flag and load the following test case:

<!DOCTYPE html>
<style>
body {
display:inline-grid;
grid-auto-flow:column stack;
}
embed {
display:grid;
position:absolute;
padding-bottom:1vmin;
}
</style>
<dl>
<dt></dt>
</dl>a
<embed></embed>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Backtrace:

ASSERTION FAILED: !object || (object->isBox())  

../../third\_party/WebKit/Source/core/rendering/RenderBox.h(766) : blink::RenderBox\* blink::toRenderBox(blink::RenderObject\*)  

1 0x1f8a613  

2 0x2a8ece4  

3 0x2b252ad  

4 0x2b251cf  

5 0x20fd42b  

6 0x208c3bd  

7 0x232e02f  

8 0x20c9cfd  

9 0x232e838  

10 0x208cd84  

11 0x208d6ab  

12 0x208ce8f  

13 0x208d6ab  

14 0x208ce8f  

15 0x20390ec  

16 0x2038b91  

17 0x1f59a17  

18 0x2718a0a  

19 0x271926c  

20 0x271d294  

21 0x195c6ef  

22 0x195c7b9  

23 0x195b477  

24 0x2717b83  

25 0x2717ef5  

26 0x2719a70  

27 0x2039501  

28 0x20464b4  

29 0x20763af  

30 0x1963bdb  

31 0x19639b5

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffdbd88700 (LWP 13222)]  

0x0000000001f8a61d in blink::toRenderBox (object=0x12e1edc24010) at ../../third\_party/WebKit/Source/core/rendering/RenderBox.h:766  

766 DEFINE\_RENDER\_OBJECT\_TYPE\_CASTS(RenderBox, isBox());  

(gdb) p this  

No symbol "this" in current context.  

(gdb) bt  

#0 0x0000000001f8a61d in blink::toRenderBox (object=0x12e1edc24010) at ../../third\_party/WebKit/Source/core/rendering/RenderBox.h:766  

#1 0x0000000002a8ece4 in blink::RenderBox::previousSiblingBox (this=0x12e1edc340f0) at ../../third\_party/WebKit/Source/core/rendering/RenderBox.h:770  

#2 0x0000000002b252ad in blink::RenderGrid::addChildToIndexesMap (this=0x12e1edc14010, child=0x12e1edc340f0)  

at ../../third\_party/WebKit/Source/core/rendering/RenderGrid.cpp:248  

#3 0x0000000002b251cf in blink::RenderGrid::addChild (this=0x12e1edc14010, newChild=0x12e1edc340f0, beforeChild=0x0)  

at ../../third\_party/WebKit/Source/core/rendering/RenderGrid.cpp:237  

#4 0x00000000020fd42b in blink::RenderTreeBuilder::createRendererForElementIfNeeded (this=0x7fffdbd86570)  

at ../../third\_party/WebKit/Source/core/dom/RenderTreeBuilder.cpp:142  

#5 0x000000000208c3bd in blink::Element::attach (this=0x185a6fe38010, context=...) at ../../third\_party/WebKit/Source/core/dom/Element.cpp:1328  

#6 0x000000000232e02f in blink::HTMLPlugInElement::attach (this=0x185a6fe38010, context=...)  

at ../../third\_party/WebKit/Source/core/html/HTMLPlugInElement.cpp:121  

#7 0x00000000020c9cfd in blink::Node::reattach (this=0x185a6fe38010, context=...) at ../../third\_party/WebKit/Source/core/dom/Node.cpp:951  

#8 0x000000000232e838 in blink::HTMLPlugInElement::willRecalcStyle (this=0x185a6fe38010)  

at ../../third\_party/WebKit/Source/core/html/HTMLPlugInElement.cpp:246  

#9 0x000000000208cd84 in blink::Element::recalcStyle (this=0x185a6fe38010, change=blink::NoChange, nextTextSibling=0x0)  

at ../../third\_party/WebKit/Source/core/dom/Element.cpp:1472  

#10 0x000000000208d6ab in blink::Element::recalcChildStyle (this=0x185a6fe10010, change=blink::NoChange)  

at ../../third\_party/WebKit/Source/core/dom/Element.cpp:1589  

#11 0x000000000208ce8f in blink::Element::recalcStyle (this=0x185a6fe10010, change=blink::NoChange, nextTextSibling=0x0)  

at ../../third\_party/WebKit/Source/core/dom/Element.cpp:1492  

#12 0x000000000208d6ab in blink::Element::recalcChildStyle (this=0x185a6fe10120, change=blink::NoChange)  

at ../../third\_party/WebKit/Source/core/dom/Element.cpp:1589  

#13 0x000000000208ce8f in blink::Element::recalcStyle (this=0x185a6fe10120, change=blink::NoChange, nextTextSibling=0x0)  

at ../../third\_party/WebKit/Source/core/dom/Element.cpp:1492  

#14 0x00000000020390ec in blink::Document::updateStyle (this=0x185a6fe04010, change=blink::NoChange)  

at ../../third\_party/WebKit/Source/core/dom/Document.cpp:1891  

#15 0x0000000002038b91 in blink::Document::updateRenderTree (this=0x185a6fe04010, change=blink::NoChange)  

at ../../third\_party/WebKit/Source/core/dom/Document.cpp:1829  

#16 0x0000000001f59a17 in blink::Document::updateRenderTreeIfNeeded (this=0x185a6fe04010) at ../../third\_party/WebKit/Source/core/dom/Document.h:460  

#17 0x0000000002718a0a in blink::FrameView::performPreLayoutTasks (this=0x2dfd482fc010)  

at ../../third\_party/WebKit/Source/core/frame/FrameView.cpp:754  

#18 0x000000000271926c in blink::FrameView::layout (this=0x2dfd482fc010, allowSubtree=true)  

at ../../third\_party/WebKit/Source/core/frame/FrameView.cpp:845  

#19 0x000000000271d294 in blink::FrameView::scrollbarExistenceDidChange (this=0x2dfd482fc010)  

at ../../third\_party/WebKit/Source/core/frame/FrameView.cpp:1765  

#20 0x000000000195c6ef in blink::ScrollView::adjustScrollbarExistence (this=0x2dfd482fc010, option=blink::ScrollView::FirstPass)  

at ../../third\_party/WebKit/Source/platform/scroll/ScrollView.cpp:465  

#21 0x000000000195c7b9 in blink::ScrollView::updateScrollbars (this=0x2dfd482fc010, desiredOffset=...)  

at ../../third\_party/WebKit/Source/platform/scroll/ScrollView.cpp:480  

#22 0x000000000195b477 in blink::ScrollView::setContentsSize (this=0x2dfd482fc010, newSize=...)  

at ../../third\_party/WebKit/Source/platform/scroll/ScrollView.cpp:217  

#23 0x0000000002717b83 in blink::FrameView::setContentsSize (this=0x2dfd482fc010, size=...)  

at ../../third\_party/WebKit/Source/core/frame/FrameView.cpp:451  

#24 0x0000000002717ef5 in blink::FrameView::adjustViewSize (this=0x2dfd482fc010) at ../../third\_party/WebKit/Source/core/frame/FrameView.cpp:489  

#25 0x0000000002719a70 in blink::FrameView::layout (this=0x2dfd482fc010, allowSubtree=true)  

at ../../third\_party/WebKit/Source/core/frame/FrameView.cpp:944  

#26 0x0000000002039501 in blink::Document::updateLayout (this=0x185a6fe04010) at ../../third\_party/WebKit/Source/core/dom/Document.cpp:1948  

#27 0x00000000020464b4 in blink::Document::pluginLoadingTimerFired (this=0x185a6fe04010) at ../../third\_party/WebKit/Source/core/dom/Document.cpp:5193  

#28 0x00000000020763af in blink::Timer[blink::Document](javascript:void(0);)::fired (this=0x185a6fe047b8) at ../../third\_party/WebKit/Source/platform/Timer.h:127  

#29 0x0000000001963bdb in blink::ThreadTimers::sharedTimerFiredInternal (this=0x2dfd48250010)  

at ../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:139  

#30 0x00000000019639b5 in blink::ThreadTimers::sharedTimerFired () at ../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:109  

#31 0x000000000196c676 in blink::Scheduler::tickSharedTimer (this=0x7802b33ee30)  

at ../../third\_party/WebKit/Source/platform/scheduler/Scheduler.cpp:124  

#32 0x000000000196c695 in blink::Scheduler::sharedTimerAdapter () at ../../third\_party/WebKit/Source/platform/scheduler/Scheduler.cpp:129  

#33 0x000000000439897b in content::BlinkPlatformImpl::DoTimeout (this=0x7802b340c60) at ../../content/child/blink\_platform\_impl.h:165  

---Type <return> to continue, or q <return> to quit---  

#34 0x000000000439a7b5 in base::internal::RunnableAdapter<void (content::BlinkPlatformImpl::\*)()>::Run (this=0x7fffdbd87110, object=0x7802b340c60)  

at ../../base/bind\_internal.h:134  

#35 0x000000000439a61c in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (content::BlinkPlatformImpl::\*)()>, void (content::BlinkPlatformImpl\*)>::MakeItSo(base::internal::RunnableAdapter<void (content::BlinkPlatformImpl::\*)()>, content::BlinkPlatformImpl\*) (  

runnable=..., a1=0x7802b340c60) at ../../base/bind\_internal.h:871  

#36 0x000000000439a29e in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (content::BlinkPlatformImpl::\*)()>, void (content::BlinkPlatformImpl\*), void (base::internal::UnretainedWrapper[content::BlinkPlatformImpl](javascript:void(0);))>, void (content::BlinkPlatformImpl\*)>::Run(base::internal::BindStateBase\*) (base=0x7802b560da0) at ../../base/bind\_internal.h:1169  

#37 0x000000000043a190 in base::Callback<void ()>::Run() const (this=0x7fffdbd871b0) at ../../base/callback.h:401  

#38 0x000000000078b0fb in base::Timer::RunScheduledTask (this=0x7802b340c88) at ../../base/timer/timer.cc:201  

#39 0x000000000078b1f3 in base::BaseTimerTaskInternal::Run (this=0x7802ade1120) at ../../base/timer/timer.cc:49  

#40 0x000000000078b53d in base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>::Run (this=0x7fffdbd87230, object=0x7802ade1120)  

at ../../base/bind\_internal.h:134  

#41 0x000000000078b4b1 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void (base::BaseTimerTaskInternal\*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, base::BaseTimerTaskInternal\*) (  

runnable=..., a1=0x7802ade1120) at ../../base/bind\_internal.h:871  

#42 0x000000000078b456 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void (base::BaseTimerTaskInternal\*), void (base::internal::OwnedWrapper[base::BaseTimerTaskInternal](javascript:void(0);))>, void (base::BaseTimerTaskInternal\*)>::Run(base::internal::BindStateBase\*) (base=0x7802b55f080) at ../../base/bind\_internal.h:1169  

#43 0x000000000043a190 in base::Callback<void ()>::Run() const (this=0x7fffdbd87578) at ../../base/callback.h:401  

#44 0x0000000000701cae in base::MessageLoop::RunTask (this=0x7802adf2460, pending\_task=...) at ../../base/message\_loop/message\_loop.cc:458  

#45 0x0000000000701dec in base::MessageLoop::DeferOrRunPendingTask (this=0x7802adf2460, pending\_task=...)  

at ../../base/message\_loop/message\_loop.cc:470  

#46 0x000000000070233c in base::MessageLoop::DoWork (this=0x7802adf2460) at ../../base/message\_loop/message\_loop.cc:584  

#47 0x0000000000712703 in base::MessagePumpDefault::Run (this=0x7802b331f50, delegate=0x7802adf2460)  

at ../../base/message\_loop/message\_pump\_default.cc:32  

#48 0x0000000000701780 in base::MessageLoop::RunHandler (this=0x7802adf2460) at ../../base/message\_loop/message\_loop.cc:408  

#49 0x000000000073b612 in base::RunLoop::Run (this=0x7fffdbd879a0) at ../../base/run\_loop.cc:49  

#50 0x0000000000700e30 in base::MessageLoop::Run (this=0x7802adf2460) at ../../base/message\_loop/message\_loop.cc:301  

#51 0x0000000004d2ad1c in base::Thread::Run (this=0x7802b3c7020, message\_loop=0x7802adf2460) at ../../base/threading/thread.cc:174  

#52 0x0000000004d2afb9 in base::Thread::ThreadMain (this=0x7802b3c7020) at ../../base/threading/thread.cc:228  

#53 0x0000000000769d78 in base::(anonymous namespace)::ThreadFunc (params=0x7fffffff9f10) at ../../base/threading/platform\_thread\_posix.cc:80  

#54 0x00007ffff3b28f6e in start\_thread (arg=0x7fffdbd88700) at pthread\_create.c:311  

#55 0x00007ffff29da9cd in clone () at ../sysdeps/unix/sysv/linux/x86\_64/clone.S:113

## Attachments

- [crash.html](attachments/crash.html) (text/html, 218 B)

## Timeline

### in...@chromium.org (2014-08-07)

[Empty comment from Monorail migration]

### re...@igalia.com (2014-08-07)

I've been taking a look to this issue.

The problem is basically because of when adding a positioned block after an inline, the positioned block is inserted inside the anonymous block wrapping the inline.
This causes the assert while trying to navigate the sibling boxes, as they're inline and not boxes.

Here's the render tree of this example:

RenderView 0x227c4cc04010              	#document	0x168d90004b10
  RenderBlock 0x227c4cc10010           	HTML	0x168d900101a8
   RenderGrid 0x227c4cc14010          	BODY	0x168d900102b8
      RenderBlock 0x227c4cc10110       	DL	0x168d90010340
        RenderBlock 0x227c4cc10210     	DT	0x168d900103c8
      RenderBlock (anonymous) 0x227c4cc10310
        RenderText 0x227c4cc24010      	#text	0x168d900281d0 "a\n"
        RenderEmbeddedObject 0x227c4cc340f0	EMBED	0x168d90038010

RenderEmbeddedObject is inserted after RenderText in "RenderBlock (anonymous)" that was created when inserting RenderText.
Then, even when RenderEmbeddedObject is a box, when we do previousSiblingBox, we're getting RenderText which is not a box (and we hit the assert).

The solution would be to ignore this item, as "RenderBlock (anonymous)" is already a grid item, and the new child (RenderEmbeddedObject) will be inside it.

This kind of render tree is right, as there's an old explicit test checking exactly this situation:
fast/block/basic/adding-near-anonymous-block.html

I'm adding svillar and jfernandez on CC, as I'll be on holidays the next weeks and they could carry on moving this forward if needed.

### re...@igalia.com (2014-08-07)

I've just uploaded a CL to fix this issue: https://codereview.chromium.org/450783002/

### sv...@igalia.com (2014-09-04)

I think this might be a dup of 401479

### re...@igalia.com (2014-09-04)

@svillar nope, it's not a duplicated.

This is specific issue related with the fact that positioned objects are added reusing the anonymous box created by previous siblings. Check #2 for more information.

The test in the CL was not crashing in current master, but I've just uploaded a new one that crashes.

### cl...@chromium.org (2014-09-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5007038506598400

Fuzzer: Inferno_twister_custom_bundle
Job Type: Linux_ubsan_vptr_content_shell_drt

Crash Type: Bad-cast
Crash Address: 0x2c74b3228180
Crash State:
  Bad-cast to blink::RenderBox from blink::RenderText
  RenderBox.h:769:1
  

Minimized Testcase (2.75 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94JODPiuxjN30O0q71Wwg189-2L3WMC2Hlab-f73ZiIPzChz4FfGGf9WQ8peekohCqpT-PvX7M9Mj0JrqJIZFNkIu75cVioiSWnWwxg0yRfsbQgtT5EXemFXaSH_weTkNo_ifoZoTm2-OCDrcABZqBuK0VKoQ

Filer: inferno

### bu...@chromium.org (2014-09-09)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=181633

------------------------------------------------------------------
r181633 | rego@igalia.com | 2014-09-09T11:17:56.948586Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css-grid-layout/grid-add-positioned-block-item-after-inline-item-expected.txt?r1=181633&r2=181632&pathrev=181633
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css-grid-layout/grid-add-positioned-block-item-after-inline-item.html?r1=181633&r2=181632&pathrev=181633
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderGrid.cpp?r1=181633&r2=181632&pathrev=181633

[CSS Grid Layout] Ignore positioned block item added after inline

Right now if you add a positioned block item after an inline item, the
positioned block item is inserted inside the anonymous block wrapping
the inline item.

This was causing an assert in RenderGrid::addChildToIndexesMap() while
navigating the sibling boxes, as its previous sibling is an inline.

As the positioned block is now not direct child of the grid, we can
ignore it, as it's not considered a grid item. The grid item would
be the anonymous block. So the proper check is added in
RenderGrid::addChild to do it.

BUG=401463
TEST=fast/css-grid-layout/grid-add-positioned-block-item-after-inline-item.html

Review URL: https://codereview.chromium.org/450783002
-----------------------------------------------------------------

### in...@chromium.org (2014-09-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-10)

ClusterFuzz has detected this issue as fixed in range 293914:293939.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5007038506598400

Fuzzer: Inferno_twister_custom_bundle
Job Type: Linux_ubsan_vptr_content_shell_drt

Crash Type: Bad-cast
Crash Address: 0x2c74b3228180
Crash State:
  Bad-cast to blink::RenderBox from blink::RenderText
  RenderBox.h:769:1
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_ubsan_vptr_content_shell_drt&range=293914:293939

Minimized Testcase (2.75 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94JODPiuxjN30O0q71Wwg189-2L3WMC2Hlab-f73ZiIPzChz4FfGGf9WQ8peekohCqpT-PvX7M9Mj0JrqJIZFNkIu75cVioiSWnWwxg0yRfsbQgtT5EXemFXaSH_weTkNo_ifoZoTm2-OCDrcABZqBuK0VKoQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### re...@igalia.com (2014-10-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

Bulk update: removing view restriction from closed bugs.

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering-Grid to Cr-Blink-Layout-Grid

### ti...@google.com (2015-12-17)

This reporter isn't from Samsung as initially thought, so is eligible for consideration under the Chrome Reward Program: https://www.google.com/about/appsecurity/chrome-rewards/

### ti...@google.com (2016-04-22)

Congratulations - $3,000 for this report. I'll add this in with your other payments.



### ti...@google.com (2016-04-25)

Adding in OP's new email address.

### ti...@google.com (2016-04-25)

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

This issue was migrated from crbug.com/chromium/401463?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/79180]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080179)*
