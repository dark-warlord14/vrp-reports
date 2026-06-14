# Heap-use-after-free in WebCore::RenderLayerScrollableArea::updateCompositingLayersAfterScroll

| Field | Value |
|-------|-------|
| **Issue ID** | [40078448](https://issues.chromium.org/issues/40078448) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Compositing |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2013-11-23 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest Chrome ASAN build . Unfortunately it is a little unreliable to reproduce. I had good results with 20 tabs.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-236536  

Operating System: Linux 64-bit

**REPRODUCTION CASE**  

Attached in crash.html, requires svgx.svg.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in stack.txt

## Attachments

- [crash.html](attachments/crash.html) (text/html, 1.0 KB)
- deleted (application/octet-stream, 0 B)
- [svgx.svg](attachments/svgx.svg) (image/svg+xml, 674 B)

## Timeline

### cl...@chromium.org (2013-11-23)

danakj: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### da...@chromium.org (2013-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-23)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5016089394151424

### in...@chromium.org (2013-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5016089394151424

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60f00000fbe0
Crash State:
  - crash stack -
  WebCore::RenderLayerScrollableArea::updateCompositingLayersAfterScroll
  WebCore::RenderLayerScrollableArea::setScrollOffset
  - free stack -
  WebCore::RenderLayer::~RenderLayer
  WebCore::RenderLayerModelObject::willBeDestroyed
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95LijDz9O06DnnP9CQjgeB18XuSxrf6xSUkCv0zMdyfnp_x1RJ_OyKIdzpWZkzNFOGkinqkFv1veIpAff17F76KIZjonHw6hZWGrFTp1xjyNkUaCmP0fudgZE4Hob9WzHSCNTqMTUBMwYhJNXLkP_guXU0mXw

Unreliable crash found using linux_tsan_chrome_mp job type (history_size=5).


### cl...@chromium.org (2013-11-25)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-11-25)

This could be a recent regression, looking at updateCompositingLayersAfterScroll. But changes in setScrollOffset go back to September. Adding jchaffraix and shawnsingh, as they seem to have touched the code most recently.

### ha...@chromium.org (2013-11-26)

I did look into this a bit today, here's what I've found out so far (unfortunately not a whole ton yet, apart from what can be deduced from the stack trace, but here it is).

It looks like sometimes half way through RenderLayerScrollableArea::setScrollOffset(), we trigger a relayout, which determines that some RenderObject indirectly associated with the current RenderLayerScrollableArea is no longer needed. As you'd expect, at that point RenderObject::destroy() is called, which results in the current RenderLayerScrollableArea to be destroyed through its associated RenderLayer. The call stack looks roughly like this:


RenderLayerScrollableArea::setScrollOffset() -> RenderView::updateWidgetPositions() -> FrameView::layout() -> … -> RenderObject::destroy() -> … -> RenderLayer::~RenderLayer() -> RenderLayerScrollableArea::~RenderLayerScrollableArea()


Unfortunately the RenderLayerScrollableArea::setScrollOffset() function isn't done at this point, so once the stack unwinds far enough, we're in the not-too-surprising situation that we're trying to finish a function with a freed "this" pointer. Specifically, RenderLayerScrollableArea::setScrollOffset() calls RenderLayerScrollableArea::updateCompositingLayersAfterScroll(), which crashes while trying to access this->m_box.


Haven't really figured out a good strategy forwards yet, as this goes through some layout and destruction code I'm not too familiar with yet.

### cl...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-11-27)

https://codereview.chromium.org/91743003/

### ha...@chromium.org (2013-11-27)

[Empty comment from Monorail migration]

### ja...@chromium.org (2013-11-27)

The bug here is that RenderMarquee is trying to do a scroll animation by directly poking at the render tree from within the render tree.  That'll never work.  The marquee animation needs to be rewritten in terms of DOM.

There's nothing we can do in the RenderLayer family to correctly handle what RenderMarquee is trying to do - it's just wrong.

### cl...@chromium.org (2013-11-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-01)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-12-02)

Given the insight James provided, I think this is getting a bit far out of my area of expertise, and I am probably not the best owner anymore.

Does anyone on the CC list with more experience in this area have a better idea of how to proceed or triage the issue?

### es...@chromium.org (2013-12-02)

[Empty comment from Monorail migration]

### es...@chromium.org (2013-12-02)

The bug here is much more fundamental than RenderMarquee. Changing RenderMarquee doesn't fix it.

1) RenderLayerScrollableArea::setScrollOffset calls RenderView::updateWidgetPositions,
2) updateWidgetPositions calls FrameView::forceLayoutParentViewIfNeeded,
3) forceLayoutParentViewIfNeeded calls layout()
4) layout() calls updateStyleIfNeeded()
5) updateStyleIfNeeded() deletes the RenderLayerScrollableArea.

Entering layout or recalcStyle from a render tree object is not safe. setScrollOffset _cannot_ call updateWidgetPositions or anything that would trigger a recalcStyle or a layout.

I don't know who's best to fix this, I don't understand the RenderLayer tangle for scrolling very well. We probably need to break this layering violation somehow.

In the short term maybe RenderLayerScrollableArea should be RefCounted and then if it becomes detached from the RenderLayer we return early from setScrollOffset?

### ha...@chromium.org (2013-12-02)

> In the short term maybe RenderLayerScrollableArea should be RefCounted and then if it becomes detached from the RenderLayer we return early from setScrollOffset?

That's more-or-less the approach I was going for in https://codereview.chromium.org/91743003/. Unfortunately there were several other ScrollableArea frames in the stack, so the return value had to be plumbed through a bunch of files, and it seemed a bit contentious.

If it's aggreed that it's an acceptable short-term fix, I can still go ahead and land that for now.

### cl...@chromium.org (2013-12-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-12-09)

Assuming this is a recent regression if cf wasn't able to repro it on a branch.

### sc...@gmail.com (2013-12-13)

Any ideas / progress?

### sc...@gmail.com (2013-12-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-12-13)

See also https://code.google.com/p/chromium/issues/detail?id=327645 which I just marked as a duplicate of this. There's another test case there in case it's useful.

### sc...@gmail.com (2013-12-13)

Assigned to @hartmanng who seems to be making progress on this in https://crbug.com/chromium/322891#c19 (thank you so much!)

### cl...@chromium.org (2013-12-22)

hartmanng@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-12-30)

hartmanng@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ha...@chromium.org (2013-12-30)

Current status is blocked on review (https://codereview.chromium.org/91743003/). The patch seems contentious, reviewers have been reluctant to give it a go-ahead.

jamesr@ and esprehn@, could you give https://codereview.chromium.org/91743003/ another look and see if it's something that could go forward?

### cl...@chromium.org (2014-01-08)

hartmanng@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ha...@chromium.org (2014-01-08)

It looks like my original fix in https://codereview.chromium.org/91743003/ isn't going to work out, the general consensus is that it's too ugly and invasive of a hack.

I've got an alternative solution up for review (https://codereview.chromium.org/128503002/) which involves changing RenderMarquee's timer so that it calls back into HTMLMarqueeElement, where we can safely do a relayout before getting into the Render stack.

### bu...@chromium.org (2014-01-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=164784

------------------------------------------------------------------------
r164784 | hartmanng@chromium.org | 2014-01-09T16:01:46.921290Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderMarquee.cpp?r1=164784&r2=164783&pathrev=164784
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderMarquee.h?r1=164784&r2=164783&pathrev=164784
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLMarqueeElement.cpp?r1=164784&r2=164783&pathrev=164784
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLMarqueeElement.h?r1=164784&r2=164783&pathrev=164784

Prevent RenderMarquee from causing a relayout.

In some circumstances, RenderMarquee can cause a relayout which ends up
deleting the calling RenderMarquee. The underlying problem is that layout
shouldn't be triggered like this through the Render tree.

This CL solves the problem by changing RenderMarquee's timer callback to
HTMLMarqueeElement::timerFired, where we can trigger layout before calling
into the RenderMarquee so that there is no layout to be done in the Render
tree.

This is a cleaner alternative to the fix in
https://codereview.chromium.org/91743003/.

BUG=322891

Review URL: https://codereview.chromium.org/128503002
------------------------------------------------------------------------

### in...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-01-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=165052

------------------------------------------------------------------------
r165052 | esprehn@chromium.org | 2014-01-14T10:19:01.360253Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderView.h?r1=165052&r2=165051&pathrev=165052
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/FrameView.cpp?r1=165052&r2=165051&pathrev=165052
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebViewImpl.cpp?r1=165052&r2=165051&pathrev=165052
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderWidget.cpp?r1=165052&r2=165051&pathrev=165052
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/FrameView.h?r1=165052&r2=165051&pathrev=165052
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderLayerScrollableArea.cpp?r1=165052&r2=165051&pathrev=165052
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderWidget.h?r1=165052&r2=165051&pathrev=165052
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderView.cpp?r1=165052&r2=165051&pathrev=165052

Harden the machinery around updateWidgetPositions()

updateWidgetPositions() can blow away the RenderView by running script or
calling into plugins. This patch moves it from RenderView to FrameView
since having this method on RenderView which might destroy itself is not
safe. It also switches to using normal RefPtr instead of manually managing
the refcount and finally adds RefPtr to callers of updateWidgetPositions()
to avoid use-after-frees.

There's one final call inside RenderLayerScrollableArea::setScrollOffset
which is not safe but is difficult to mitigate since we're way down a
callstack by the time this call is made which can destroy the render tree
and the RenderLayerScrollableArea. This patch adds a RELEASE_ASSERT to
kill the renderer in case we get into a sitaution where this happens.
In the future we should detangle this concept entirely so such an
ASSERT isn't needed and so that the render tree can never destroy itself
from the inside.

It's not clear how to write a test for this since you need to get us to
go into the scrolling code with a dirty tree or have a plugin that does
something nefarious.

BUG=322891

Review URL: https://codereview.chromium.org/132913002
------------------------------------------------------------------------

### ha...@chromium.org (2014-01-14)

http://src.chromium.org/viewvc/blink?view=rev&rev=164784 has been in the m34 Canary for about a day and a half with no negative effects. Requesting merge into m33 branch.

### la...@google.com (2014-01-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-01-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=165138

------------------------------------------------------------------------
r165138 | hartmanng@chromium.org | 2014-01-15T15:53:30.525668Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/core/rendering/RenderMarquee.h?r1=165138&r2=165137&pathrev=165138
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/core/html/HTMLMarqueeElement.cpp?r1=165138&r2=165137&pathrev=165138
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/core/html/HTMLMarqueeElement.h?r1=165138&r2=165137&pathrev=165138
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/core/rendering/RenderMarquee.cpp?r1=165138&r2=165137&pathrev=165138

Merge 164784 "Prevent RenderMarquee from causing a relayout."

> Prevent RenderMarquee from causing a relayout.
> 
> In some circumstances, RenderMarquee can cause a relayout which ends up
> deleting the calling RenderMarquee. The underlying problem is that layout
> shouldn't be triggered like this through the Render tree.
> 
> This CL solves the problem by changing RenderMarquee's timer callback to
> HTMLMarqueeElement::timerFired, where we can trigger layout before calling
> into the RenderMarquee so that there is no layout to be done in the Render
> tree.
> 
> This is a cleaner alternative to the fix in
> https://codereview.chromium.org/91743003/.
> 
> BUG=322891
> 
> Review URL: https://codereview.chromium.org/128503002

TBR=hartmanng@chromium.org

Review URL: https://codereview.chromium.org/137853012
------------------------------------------------------------------------

### dh...@google.com (2014-01-16)

Requesting merge for M32.

### dx...@chromium.org (2014-01-16)

[Empty comment from Monorail migration]

### ka...@google.com (2014-01-17)

this hasn't gone to beta yet. i won't take it to stable yet.

### dh...@google.com (2014-01-28)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-04)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-04)

Thanks for the report! This one qualifies for a $2000 reward. While the freed object is not in a heap partition and there is control between the free and use, this did not qualify at a higher reward level because the crash did not seem to be very reliable.

### ti...@chromium.org (2014-04-15)

Starting payment process.

### cl...@chromium.org (2014-04-17)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-04-18)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you (Req #233621). Thanks again for your help!

### gl...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/322891?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/327645]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078448)*
