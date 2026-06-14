# Heap-use-after-free in WebCore::RootInlineBox::closestLeafChildForPoint

| Field | Value |
|-------|-------|
| **Issue ID** | [40077822](https://issues.chromium.org/issues/40077822) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | [Deleted User] |
| **Created** | 2013-07-21 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4722518136979456

Fuzzer: Miaubiz_css_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e00003dfc0
Crash State:
  - crash stack -
  WebCore::RootInlineBox::closestLeafChildForPoint
  WebCore::previousLinePosition
  - free stack -
  WebCore::RenderBlock::layoutRunsAndFloats
  WebCore::RenderBlock::layoutInlineChildren
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=210180:210182

Minimized Testcase (2.63 Kb): https://cluster-fuzz.appspot.com/download/AMIfv959E5oSibRNRtsZhfjm-RTAtsDG3TbE2kIqzRxnS6EvM9RbgjQftfqOh8zi7u9yCBqyRXrrVNbCIsrPEG0aTy_TCXg4DUMymHz0zxgIVnML805qfZ7owWmwniUEtyY5V-T4ep0A9FJc6mjReDT8MtxiuAxu5g

## Attachments

- [stack](attachments/stack) (text/plain; charset=us-ascii, 18.1 KB)
- [test.html](attachments/test.html) (text/html; charset=us-ascii, 2.7 KB)

## Timeline

### in...@chromium.org (2013-07-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-26)

Looks like a regression from http://src.chromium.org/viewvc/blink?view=rev&revision=153532. Levi, can you please help to take a look.

### le...@chromium.org (2013-07-29)

This isn't repro-ing for me with ASAN on Linux... is there more to this that I'm missing?

### in...@chromium.org (2013-07-29)

i think you need --allow-file-access-from-files or --disable-web-security :)

### le...@chromium.org (2013-07-31)

I believe I have a fix for this.

### le...@chromium.org (2013-08-01)

This is actually a problem with filters. During Style Recalc in this test, we end up queueing up another style recalc via scheduleLayerUpdate. Here's the stack:

#0  WebCore::Element::scheduleLayerUpdate (this=0x2b22592181c8) at ../../third_party/WebKit/Source/core/dom/Element.cpp:2893
#1  0x0000000002d9e00c in WebCore::RenderLayerFilterInfo::notifyFinished (this=0x2e73c406d40) at ../../third_party/WebKit/Source/core/rendering/RenderLayerFilterInfo.cpp:110
#2  0x00000000031a941e in WebCore::Resource::didAddClient (this=0x2e73c447220, c=0x2e73c406d48) at ../../third_party/WebKit/Source/core/loader/cache/Resource.cpp:364
#3  0x00000000031a9353 in WebCore::Resource::addClient (this=0x2e73c447220, client=0x2e73c406d48) at ../../third_party/WebKit/Source/core/loader/cache/Resource.cpp:354
#4  0x0000000002d9e0f7 in WebCore::RenderLayerFilterInfo::updateReferenceFilterClients (this=0x2e73c406d40, operations=...) at ../../third_party/WebKit/Source/core/rendering/RenderLayerFilterInfo.cpp:127
#5  0x0000000002d78e17 in WebCore::RenderLayer::updateOrRemoveFilterClients (this=0x2e73c424038) at ../../third_party/WebKit/Source/core/rendering/RenderLayer.cpp:6311
#6  0x0000000002d77239 in WebCore::RenderLayer::updateFilters (this=0x2e73c424038, oldStyle=0x2e73c3fdc80, newStyle=0x2e73c3fde90) at ../../third_party/WebKit/Source/core/rendering/RenderLayer.cpp:6036
#7  0x0000000002d77510 in WebCore::RenderLayer::styleChanged (this=0x2e73c424038, oldStyle=0x2e73c3fdc80) at ../../third_party/WebKit/Source/core/rendering/RenderLayer.cpp:6087
#8  0x0000000002da2ce4 in WebCore::RenderLayerModelObject::styleDidChange (this=0x2e73c3fea58, diff=WebCore::StyleDifferenceEqual, oldStyle=0x2e73c3fdc80) at ../../third_party/WebKit/Source/core/rendering/RenderLayerModelObject.cpp:168
#9  0x0000000002ce35e5 in WebCore::RenderBox::styleDidChange (this=0x2e73c3fea58, diff=WebCore::StyleDifferenceEqual, oldStyle=0x2e73c3fdc80) at ../../third_party/WebKit/Source/core/rendering/RenderBox.cpp:239
#10 0x0000000002c74678 in WebCore::RenderBlock::styleDidChange (this=0x2e73c3fea58, diff=WebCore::StyleDifferenceEqual, oldStyle=0x2e73c3fdc80) at ../../third_party/WebKit/Source/core/rendering/RenderBlock.cpp:389
#11 0x0000000002e94ed1 in WebCore::RenderListItem::styleDidChange (this=0x2e73c3fea58, diff=WebCore::StyleDifferenceEqual, oldStyle=0x2e73c3fdc80) at ../../third_party/WebKit/Source/core/rendering/RenderListItem.cpp:53
#12 0x0000000002dca860 in WebCore::RenderObject::setStyle (this=0x2e73c3fea58, style=...) at ../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:1857
#13 0x0000000002dc9f1a in WebCore::RenderObject::setAnimatableStyle (this=0x2e73c3fea58, style=...) at ../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:1729
#14 0x00000000023565fe in WebCore::Element::recalcStyle (this=0x2b22592181c8, change=WebCore::Node::NoChange) at ../../third_party/WebKit/Source/core/dom/Element.cpp:1478
#15 0x0000000002356a2b in WebCore::Element::recalcStyle (this=0x2b2259218028, change=WebCore::Node::NoChange) at ../../third_party/WebKit/Source/core/dom/Element.cpp:1542
#16 0x0000000002356a2b in WebCore::Element::recalcStyle (this=0x2b22592180f8, change=WebCore::Node::NoChange) at ../../third_party/WebKit/Source/core/dom/Element.cpp:1542
#17 0x00000000023143f7 in WebCore::Document::recalcStyle (this=0x2b2259214ad8, change=WebCore::Node::NoChange) at ../../third_party/WebKit/Source/core/dom/Document.cpp:1632
#18 0x00000000023147b3 in WebCore::Document::updateStyleIfNeeded (this=0x2b2259214ad8) at ../../third_party/WebKit/Source/core/dom/Document.cpp:1687
#19 0x000000000231497f in WebCore::Document::updateLayout (this=0x2b2259214ad8) at ../../third_party/WebKit/Source/core/dom/Document.cpp:1716
#20 0x0000000002314b64 in WebCore::Document::updateLayoutIgnorePendingStylesheets (this=0x2b2259214ad8) at ../../third_party/WebKit/Source/core/dom/Document.cpp:1760
#21 0x000000000305a43d in WebCore::previousLinePosition (visiblePosition=..., lineDirectionPoint=7, editableType=WebCore::ContentIsEditable) at ../../third_party/WebKit/Source/core/editing/VisibleUnits.cpp:931
#22 0x000000000301e9cc in WebCore::FrameSelection::modifyExtendingBackward (this=0x2e73c1aa700, granularity=WebCore::LineGranularity) at ../../third_party/WebKit/Source/core/editing/FrameSelection.cpp:845

Any advice?

### in...@chromium.org (2013-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-08-01)

The filter stuff i see in the regression range is http://src.chromium.org/viewvc/blink?view=rev&revision=153537.

### se...@chromium.org (2013-08-01)

I reverted r153537 locally (as well as r153589 and r154031 on which it depends), and it still repros.

Hot potato, hot potato.. esprehn seems to have added the scheduleLayerUpdate stuff, maybe he knows what's up.

### se...@chromium.org (2013-08-01)

Verified by manually bisecting:  r153539 is good, r153540 is bad.

### le...@chromium.org (2013-08-01)

Thanks for the manual bisect!

### es...@chromium.org (2013-08-01)

Weird, I'll see if I can figure this out today. r153540 was fixing a regression I had introduced, I wonder if this bug was there before and then disappeared when I broke stuff and then came back when I fixed it.

### es...@chromium.org (2013-08-02)

Okay so this postAttachCallback thing came from https://trac.webkit.org/changeset/62687 and was generalized in https://trac.webkit.org/changeset/88570 so it looks like it was intentionally for scheduling style recalcs in the middle of style recalcs for hooking together compositor layers across frame boundaries.

We were already doing this in a bunch of places but I expanded the logic to do it in more places and now we have a heap use after free from it, but I can't imagine why this wouldn't have been triggered in all those other places you could cause a style recalc inside a style recalc before.

I think this is a layout bug, something is leaving behind free'd line boxes in the tree after the ::destroy(). I can switch the call sites back to hide this bug, but I don't think that means the bug is really fixed.

Someone who understands the line box tree needs to look at this.

### in...@chromium.org (2013-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2013-09-03)

Mostly we just need to reduce the test case.

### cl...@chromium.org (2013-09-11)

ClusterFuzz has detected this issue as fixed in range 212598:212679.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4722518136979456

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e00003dfc0
Crash State:
  - crash stack -
  WebCore::RootInlineBox::closestLeafChildForPoint
  WebCore::previousLinePosition
  - free stack -
  WebCore::RenderBlock::layoutRunsAndFloats
  WebCore::RenderBlock::layoutInlineChildren
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=210180:210182
Fixed: https://cluster-fuzz.appspot.com/revisions?range=212598:212679

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv959E5oSibRNRtsZhfjm-RTAtsDG3TbE2kIqzRxnS6EvM9RbgjQftfqOh8zi7u9yCBqyRXrrVNbCIsrPEG0aTy_TCXg4DUMymHz0zxgIVnML805qfZ7owWmwniUEtyY5V-T4ep0A9FJc6mjReDT8MtxiuAxu5g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-12)

This is not fixed. I clicked redo and it still reproduces.

### cl...@chromium.org (2013-09-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mi...@gmail.com (2013-09-26)

can I have the repro case please?

### in...@chromium.org (2013-09-26)

if you login using miaubiz@gmail.com, then you can access any clusterfuzz reports for your fuzzers. e.g. try detailed report link from c#0 https://cluster-fuzz.appspot.com/testcase?key=4722518136979456 and click download testcase.

### mi...@gmail.com (2013-09-26)

thank you inferno

### cl...@chromium.org (2013-09-27)

eseidel@: you haven't provided any bug update or come up with a fix for this issue in the last 7 days. Please note that this is a medium+ severity security vulnerability that needs your immediate response. If you have a patch in progress and don't want future nags, please add a codereview link and a WIP label. If the issue is already fixed or you can't reproduce it, please close the bug.

### [Deleted User] (2013-09-27)

I built with asan=1:

GYP_GENERATORS=ninja GYP_DEFINES='asan=1 linux_use_tcmalloc=0 ' gclient runhooks
ninja -C $CHROME_BASE/out/Debug -j 1000 content_shell

And then ran the attached test case:
$CHROME_BASE/out/Debug/content_shell file://$PWD/test.html

And it didn't crash?

[27741:27773:0927/153449:358467645694:WARNING:proxy_service.cc(886)] PAC support disabled because there is no system implementation
[27741:27741:0927/153449:358468166495:INFO:CONSOLE(0)] "Unsafe attempt to load URL file:///src/chromium/src/third_party/WebKit/LayoutTests/0.5276760736014694 from frame with URL file:///src/chromium/src/third_party/WebKit/LayoutTests/test.html. Domains, protocols and ports must match.
", source: file:///src/chromium/src/third_party/WebKit/LayoutTests/test.html (0)


### aa...@google.com (2013-09-27)

the testcase originally reproduced in chrome with these command line flags

chrome --allow-file-access-from-files --js-flags="--expose-gc" --no-first-run --use-gl=any --user-data-dir=/mnt/scratch0/tmp/user_profile_chrome_0

it might or might not reproduce in content_shell. and you will need to add testRunner.waitUntilDone() if it has any setTimeouts.

### aa...@google.com (2013-09-27)

adding testRunner.waitUntilDone() crashed in content_shell

### [Deleted User] (2013-09-27)

Looking at the clusterfuzz stacks was more helpful. :)

isEditablePositionIs a gigantic foot-gun.

bool isEditablePosition(const Position& p, EditableType editableType, EUpdateStyle updateStyle)
{
    Node* node = p.deprecatedNode();
    if (!node)
        return false;
    if (updateStyle == UpdateStyle)
        node->document().updateLayoutIgnorePendingStylesheets();
    else
        ASSERT(updateStyle == DoNotUpdateStyle);

    if (node->renderer() && node->renderer()->isTable())
        node = node->parentNode();

    return node->rendererIsEditable(editableType);
}

By default it updates layout and style for you.

It's called all over the place where we're holding on to raw LineBox or RenderObject pointers!

### [Deleted User] (2013-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2013-09-27)

In this specific case:
        RenderObject* renderer = root->closestLeafChildForPoint(pointInLine, isEditablePosition(p))->renderer();


isEditablePosition() is called to produce an argument for closestLeafChildForPoint, but because it causes a layout, root may not be valid by the time closestLeafChildForPoint is actually called.

I think the fix for all of these types of bugs would be to have a LayoutLock() which you hold, which makes layout() calls ASSERT (unless you called them through the lock for instance).

### in...@chromium.org (2013-09-27)

VisiblePosition previousLinePosition(const VisiblePosition &visiblePosition, int lineDirectionPoint, EditableType editableType)
{
.......
    node->document().updateLayoutIgnorePendingStylesheets();

.......

    if (root) {
        // FIXME: Can be wrong for multi-column layout and with transforms.
        IntPoint pointInLine = absoluteLineDirectionPointToLocalPointInBlock(root, lineDirectionPoint);
        RenderObject* renderer = root->closestLeafChildForPoint(pointInLine, isEditablePosition(p))->renderer()

We already did layout at start of function, what caused for need to do layout again. LayoutLock will be helpful here.

### [Deleted User] (2013-09-27)

Near the top of previousLinePosition we try to update layout, but we only do a updateLayoutIgnorePendingStylesheets.

recalcStyleForLayoutIgnoringPendingStylesheets is unfortunate in that if you call it twice it will do something different the second time.

We should really just fix recalcStyleForLayoutIgnoringPendingStylesheets to be idempotent.

### es...@chromium.org (2013-09-27)

Both recalcStyle (resource loads, plugins, focus, ...) and updateLayout (overflowchanged, plugins) can run JS at the end that invalidates layout a second time.

Doing updateLayoutIgnorePendingStyleSheets() doesn't mean the tree doesn't need layout anymore! Similarly doing updateStyleIfNeeded() doesn't mean the tree doesn't needStyleRecalc() after it runs.

We could add a loop in there that does the operation in a loop until script stops invalidating stuff? That would let you get into an infinite loop, but it'd probably be more correct and safer.

### [Deleted User] (2013-09-27)

The code would suggest we should remove this concept entirely:

// FIXME: This is a bad idea and needs to be removed eventually.
// Other browsers load stylesheets before they continue parsing the web page.
// Since we don't, we can run JavaScript code that needs answers before the
// stylesheets are loaded. Doing a layout ignoring the pending stylesheets
// lets us get reasonable answers. The long term solution to this problem is
// to instead suspend JavaScript execution.
void Document::updateLayoutIgnorePendingStylesheets()
{
    recalcStyleForLayoutIgnoringPendingStylesheets();
    updateLayout();
}


### [Deleted User] (2013-09-27)

Code like this wants a function which means "Layout me until I don't need layout anymore".

rendering.transitionTo(LayoutIsDoneDammit);

### pd...@chromium.org (2013-09-28)

@esprehn, can you expand a bit on how calling updateLayoutIgnorePendingStyleSheets does not imply the tree is now laid out?

### es...@chromium.org (2013-09-28)

@pdr: updateLayout() runs script synchronously inside it in the form of overflowchanged events (and also plugins) and updateStyleIfNeeded() runs script internally in the form of autofocus and plugins. Any of those things can invalidate layout:

ex.

// ... setup div so that an overflowchanged event fires  ...
// then:
div.addEventListener('overflowchanged', function() {
  div.style.width = '10px';
  getComputedStyle(div).color; // cause a recalcStyle but not a layout.
});
div.offsetTop; // layout is still needed after this returns.

or

input.setAttribute('autofocus', 'autofocus');
input.onfocus = function() {
  input.remove();
};
dovument.body.appendChild(input);
getComputedStyle(input).color; // recalcStyle but not layout
// tree still needs recalcStyle after this returns since onfocus invalidated it.

Plugins get to do all this too, anywhere you see an updateWidgets thing (ex. SuspensionScope in recalcStyle, updateWidgets in FrameView) the plugin can reach in and invalidate layout.

We do all this work upon returning from recalcStyle() and updateLayout() so calling updateLayoutIgnorePendingStyleSheets() does not mean all the bits have been cleared and the state is updated.

### es...@chromium.org (2013-09-28)

The onfocus one we can fix btw, we should just postTask() or use a SharedTimer for that. The fact that it fires inside recalcStyle is crazy and I got the HTML5 spec fixed so it doesn't need to happen at a specific time now.

### sc...@gmail.com (2013-09-28)

Hmm, looks like the rewards panel voted on this even though it's not fixed. Still, I can't imagine the fix changing the result so it's probably safest to tag the reward so it doesn't get lost: $1000.

### pd...@chromium.org (2013-09-28)

@esprehn, painting with a tree still needing layout has been a source of many security bugs so I thought it was generally a security no-no to synchronously set layout bits in layout.

I created a simple testcase from your example using overflowchanged and we do not leave updateLayoutIgnorePendingStylesheets needing layout because the event is fired asynchronously. If we just have a handful of synchronous events, is it feasible to switch them all to be asynchronous?

### in...@chromium.org (2013-09-28)

looks like this line in repro is invalidating tree during layout.
el0.addEventListener('blur', function(){ el0.setAttribute('X', 'Z') }, false)

pdr@, what problems do we see in taking up esprehn@ idea of retrying updateLayoutIgnorePendingStyleSheets in a loop until it completes (for the short term). And we can add an assert that we can use to determine what synchronous events are left and keep converting them one by one ?



### pd...@chromium.org (2013-09-29)

@inferno, I'd like to avoid looping until layout completes because it complicates the layout algorithm even further and makes partial layout hard to implement. Certainly security is more important than these cases though.

Not all layouts go through updateLayoutIgnorePendingStyleSheets. If we do this, shouldn't we do it in FrameView::layout?

### mi...@gmail.com (2013-09-30)

I haven't been able to trigger any of the six issues :(

### cl...@chromium.org (2013-10-01)

Fixing impact labels.

### cl...@chromium.org (2013-10-06)

eseidel@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-10-06)

Sorry for the multiple nag comments in the last 24 hrs. It was supposed to be just one per week :), but a bug in sheriffbot caused it to generate multiple ones. Sorry for the inconvenience.

### cl...@chromium.org (2013-10-14)

eseidel@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-19)

ClusterFuzz has detected this issue as fixed in range 229274:229345.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4722518136979456

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e00003dfc0
Crash State:
  - crash stack -
  WebCore::RootInlineBox::closestLeafChildForPoint
  WebCore::previousLinePosition
  - free stack -
  WebCore::RenderBlock::layoutRunsAndFloats
  WebCore::RenderBlock::layoutInlineChildren
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=210180:210182
Fixed: https://cluster-fuzz.appspot.com/revisions?range=229274:229345

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv959E5oSibRNRtsZhfjm-RTAtsDG3TbE2kIqzRxnS6EvM9RbgjQftfqOh8zi7u9yCBqyRXrrVNbCIsrPEG0aTy_TCXg4DUMymHz0zxgIVnML805qfZ7owWmwniUEtyY5V-T4ep0A9FJc6mjReDT8MtxiuAxu5g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-10-19)

ClusterFuzz has detected this issue as fixed in range 229274:229345.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4722518136979456

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e00003dfc0
Crash State:
  - crash stack -
  WebCore::RootInlineBox::closestLeafChildForPoint
  WebCore::previousLinePosition
  - free stack -
  WebCore::RenderBlock::layoutRunsAndFloats
  WebCore::RenderBlock::layoutInlineChildren
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=210180:210182
Fixed: https://cluster-fuzz.appspot.com/revisions?range=229274:229345

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv959E5oSibRNRtsZhfjm-RTAtsDG3TbE2kIqzRxnS6EvM9RbgjQftfqOh8zi7u9yCBqyRXrrVNbCIsrPEG0aTy_TCXg4DUMymHz0zxgIVnML805qfZ7owWmwniUEtyY5V-T4ep0A9FJc6mjReDT8MtxiuAxu5g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### le...@chromium.org (2013-10-22)

Is Cluster Fuzz right that this is fixed? Nothing in the Blink range stands out as fixing this issue to me.

### in...@chromium.org (2013-10-22)

I tried it twice, and it points at the same fixed range (c#48, c#49), so something did fix this.

### cl...@chromium.org (2013-10-22)

eseidel@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-10-24)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-10-24)

This does not reproduce anymore on CF. Closing.

### [Deleted User] (2013-10-24)

We have systemic bugs here.  I'm glad this particular issue is fixed.  We need to solve the question of providing programming guarantees of the state of the rendering tree separately.

### cl...@chromium.org (2013-10-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-11-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/262653?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077822)*
