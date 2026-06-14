# Security: ASAN heap-use-after-free in SVGElement::propertyFromAttribute

| Field | Value |
|-------|-------|
| **Issue ID** | [40079497](https://issues.chromium.org/issues/40079497) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2014-05-04 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest chromium ASAN build. ASAN output attached in asan.txt

**VERSION**  

Chrome Version: asan-symbolized-linux-release-267662  

Operating System: Linux

**REPRODUCTION CASE**  

Requires multiple files, attached in crash.zip. Opening the testcase in multiple tabs helps if it doesn't reproduce reliably.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: attached in ASAN.txt

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip, 1.4 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 20.0 KB)

## Timeline

### cl...@chromium.org (2014-05-04)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6753359954444288

### in...@chromium.org (2014-05-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-13)

schenney@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-05-14)

definitely looks like regression from Kouhei@ recent changes. [http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGAnimatedTypeAnimator.cpp?annotate=HEAD]

This should be impacting upcoming m35 stable.

### cl...@chromium.org (2014-05-14)

[Empty comment from Monorail migration]

### ko...@chromium.org (2014-05-14)

I'm looking into this bug but I'm attending BlinkOn atm so I'll be slow.

### ko...@chromium.org (2014-05-14)

Hmm. I haven't succeeded to repro this. It hits ASSERT when I load the page, which seems to be another bug.

progress dump...:

Looking at the asan trace, |SVGAnimateElement::m_animatedElements| seems to be holding stale references to old use shadow tree elements.
This is weird. SVGAnimateElement is calling addElementReferencingTarget to be notified when the target change.
The SVGAnimateElement should have been notified |svgAttributeChanged(hrefAttr)| from the destructed element's d-tor.
The asan stack trace does show that the svgAttributeChanged notification is received by SVGAnimateElement, but it is either too late (notification wasn't fired for the element somehow) or the destructed element is captured again when |findElementInstances|.

### in...@chromium.org (2014-05-14)

Did you try with c#0 and an ASAN build - "Opening the testcase in multiple tabs helps if it doesn't reproduce reliably.". It is ok, we understand everyone is occupied with BlinkOn atm, but please do look at it after that.

### ko...@chromium.org (2014-05-14)

Sorry I'm out of time, I don't have network connection from now on.

I'll continue this investigation on next Monday, but please reassign this bug if you can't wait.

### in...@chromium.org (2014-05-14)

next Monday is fine.

### ko...@chromium.org (2014-05-19)

https://codereview.chromium.org/290353002/ deals with ASSERT failure. Doesn't resolve this bug but allows me to repro this bug.

### ko...@chromium.org (2014-05-19)

OK. I tracked down this is from elementInstances() map carrying stale ptr. The map becomes inconsistent when running the testcase, but I don't know what is exactly what op is making the map inconsistent.

I minimized/annotated the repro case to below, but this is still big:
<script>
window.setTimeout("location.reload()",50);
var done=0;
function start() {
animate_iframe=document.createElement('iframe');
animate_iframe.src='animate.svg';
animate_iframe.onload=animate_onload;
document.documentElement.appendChild(animate_iframe);
o14=document.createElement('div');
}
function animate_onload() {
animate_document=animate_iframe.contentWindow.document.documentElement;
o14.appendChild(animate_document);
svgid_iframe=document.createElement('iframe');
svgid_iframe.src='svgid.svg';
svgid_iframe.onload=svgid_onload;
document.documentElement.appendChild(svgid_iframe);
}
function svgid_onload() {
document.body.appendChild(svgid_iframe);
document.body.appendChild(o14);
document.body.appendChild(animate_document.cloneNode(true));
}
</script>
<body onload="start()">
</body>


### ko...@chromium.org (2014-05-19)

pdr@ : Given that SVGElementInstance tree is going away anyway, do you think it is reasonable to rewrite the SVGAnimateElement to not rely on SVGElementInstance tree instead of fixing this bug?

### ko...@chromium.org (2014-05-19)

According to tasak@, CSSStyleResolver is also using SVGElementInstance tree, so deprecating SVGElementInstance tree will take more time than I thought.

Given that this also affects M35, I'll continue trying to fix elementInstances() map inconsistency.

### bu...@chromium.org (2014-05-20)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=174338

------------------------------------------------------------------
r174338 | kouhei@chromium.org | 2014-05-20T02:13:08.413273Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/dom/resources/import-other-svg.svg?r1=174338&r2=174337&pathrev=174338
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/animation/SMILTimeContainer.cpp?r1=174338&r2=174337&pathrev=174338
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/dom/move-animating-svg-to-other-frame.html?r1=174338&r2=174337&pathrev=174338
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGDocumentExtensions.cpp?r1=174338&r2=174337&pathrev=174338
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/dom/move-animating-svg-to-other-frame-expected.txt?r1=174338&r2=174337&pathrev=174338
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/dom/resources/svg-with-animate.svg?r1=174338&r2=174337&pathrev=174338

SVG: Moving animating <svg> to other iframe should not crash.

Moving SVGSVGElement with its SMILTimeContainer already started caused crash before this patch.
|SVGDocumentExtentions::startAnimations()| calls begin() against all SMILTimeContainers in the document, but the SMILTimeContainer for <svg> moved from other document may be already started.

BUG=369860

Review URL: https://codereview.chromium.org/290353002
-----------------------------------------------------------------

### ko...@chromium.org (2014-05-20)

The above CL only fixes part of the bug. Work still in progress.

### ko...@chromium.org (2014-05-22)

Ok. Just locally fixed one of the issue caused by the repro case, and this seems to have been causing UAF.

This "if (inDocument()) return;" is wrong, as |SVGElement::invalidateInstances()| is also triggered from |SVGElement::removedFrom| to invalidate past instances.
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/svg/SVGElement.cpp&q=svgelement.cpp&sq=package:chromium&type=cs&l=1045

However, with above issue resolved, there are still inconsistency in |elementInstances()|, which triggers SMILAnimation asserts. I'm looking into it.

### ko...@chromium.org (2014-05-22)

Applying this CL fixes the problem : https://codereview.chromium.org/298873003

I'm now splitting CLs and trying to adding a unittest to each.

### ko...@chromium.org (2014-05-22)

I wrote a unit test for the CL but it lead to a new crash. :/
The 4th bug originating from the original repro case.

Continuing this work tomorrow.

### ti...@chromium.org (2014-05-22)

Thanks for the update kouhei@ - please remember to mark as fixed when you're finished.

### ko...@chromium.org (2014-05-23)

+esprehn
 
from your recent CL on <use>.

### ko...@chromium.org (2014-05-23)

[Comment Deleted]

### ko...@chromium.org (2014-05-23)

[Comment Deleted]

### ko...@chromium.org (2014-05-23)

[Comment Deleted]

### es...@chromium.org (2014-05-23)

Indeed the inDocument() check is wrong, I had a fix in a different patch I didn't land. I didn't have a test at the time.

### es...@chromium.org (2014-05-23)

Specifically I was trying to fix this issue in https://codereview.chromium.org/234633004

### ko...@chromium.org (2014-05-23)

esprehn: I posted the fix CL on https://codereview.chromium.org/298873003/

However, I think this conflicts with your async <use> approach. Do you have an idea how to resolve it?

### jl...@chromium.org (2014-05-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-05-28)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=174923

------------------------------------------------------------------
r174923 | kouhei@chromium.org | 2014-05-28T02:40:15.407037Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGAnimatedTypeAnimator.h?r1=174923&r2=174922&pathrev=174923
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGAnimateElement.cpp?r1=174923&r2=174922&pathrev=174923
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/properties/SVGAnimatedProperty.h?r1=174923&r2=174922&pathrev=174923
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/dom/remove-use-target-element-indirectly-expected.txt?r1=174923&r2=174922&pathrev=174923
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGAnimatedAngle.cpp?r1=174923&r2=174922&pathrev=174923
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGStaticStringList.cpp?r1=174923&r2=174922&pathrev=174923
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGAnimatedNumber.cpp?r1=174923&r2=174922&pathrev=174923
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/dom/resources/svg-with-animate-use.svg?r1=174923&r2=174922&pathrev=174923
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGAnimateElement.h?r1=174923&r2=174922&pathrev=174923
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/dom/remove-use-target-element-indirectly.html?r1=174923&r2=174922&pathrev=174923
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGStaticStringList.h?r1=174923&r2=174922&pathrev=174923
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGAnimatedInteger.cpp?r1=174923&r2=174922&pathrev=174923
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/properties/SVGAnimatedProperty.cpp?r1=174923&r2=174922&pathrev=174923

SVG: SVGAnimateElement should not cache |m_animatedElements|

Before this change, SVGAnimateElement cached resolved element instances in 
|m_animatedElements|. However, this is not updated synchronously when <use> 
shadow dom/instance tree is torn down or new instances are added.

The patch changes SVGAnimateElement to resolve its target instances on the fly 
when needed.

As |m_animatedElements| are no longer kept, we do not guarantee that 
animationStarted hook is called before each animation. animationEnded
hook is guaranteed to be called for elements stayed in the tree 
when the animation ended, but it may not be called for the animated element 
|removedFrom| the document tree while animation.

BUG=369860

Review URL: https://codereview.chromium.org/298873003
-----------------------------------------------------------------

### in...@chromium.org (2014-05-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-28)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-05-30)

kouhei@ - once this hits the next dev release and spends a few days baking, please nominate this bug for M36 (branch 1985).

### ti...@chromium.org (2014-06-03)

removing M-35 (not going to make patch 1)

### ti...@chromium.org (2014-06-06)

Still waiting for this to land in a dev release before nominating for M36.

### ti...@chromium.org (2014-06-17)

Merge Requested for M36 (branch 1985)

### [Deleted User] (2014-06-17)

Rejected, nontrivial code change that is not fixing a critical security, stability or regression.

### in...@chromium.org (2014-06-17)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-14)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-07-24)

This is a high severity security vulnerability found by external reporter. This needs to go in m37.

### in...@chromium.org (2014-08-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-08-05)

removing merge request label - i don't see anything here that needs to be merged to m37, as all revisions referenced above would have been included as they were landed pre-cut.

### in...@chromium.org (2014-08-05)

yes merge is not required.

### mb...@chromium.org (2014-08-28)

Thanks for the report! This qualifies for a $2000 reward.

### cl...@chromium.org (2014-09-03)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@google.com (2014-10-07)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/369860?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079497)*
