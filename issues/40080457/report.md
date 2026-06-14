# Use-of-uninitialized-value in unsigned int blink::WidthIterator::advanceInternal<blink::SurrogatePairAwareTextIterator>

| Field | Value |
|-------|-------|
| **Issue ID** | [40080457](https://issues.chromium.org/issues/40080457) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ds...@chromium.org |
| **Created** | 2014-09-14 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6192550760153088

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  unsigned int blink::WidthIterator::advanceInternal<blink::SurrogatePairAwar
  blink::WidthIterator::advance
  blink::Font::getGlyphsAndAdvancesForSimpleText
  

Minimized Testcase (3.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96L0scVrYJZvV3RfLsJPVrP2aNX2EsUlqu75uN0p0wvl9SFkgMw19nqLdr8TZg8hlIendPtEzxrDYQm1axwclSMNrz5NHxtJN9-TVERiMF5CoNmERJTJAHxL5IIrYoRrIjYRZgqIOUDEm52IDhOc7yAHPjluw

Filer: inferno

## Attachments

- [reduced_test.html](attachments/reduced_test.html) (text/html, 615 B)

## Timeline

### in...@chromium.org (2014-09-14)

maybe related to

Author: fmalita@chromium.org
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/ae6e22134fc3f8b319205aedc648d4fadd575370
The CL last changed line 197 of file WidthIterator.cpp, which is stack frame 1.

### cl...@chromium.org (2014-09-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-22)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### fm...@chromium.org (2014-09-22)

I'm not convinced that the CL is related, but can't immediately rule it out either: at a quick glance, it appears the uninitialized value is passed in from blink::toArmenian.

Looking.

### fm...@chromium.org (2014-09-22)

Looks like an layout/invalidation problem -- hitting the following on debug builds:

RenderView 0x230cd4204010              	#document	0x144152e04010
  RenderBlock 0x230cd421c010           	HTML	0x144152e10120
    RenderBody 0x230cd421c110          	BODY	0x144152e10010
      RenderBlock 0x230cd421c210       	OPTION	0x144152e34010 CLASS="c4"
      RenderTable 0x230cd4220010
*       RenderBlock 0x230cd421c310     	LI	0x144152e101a8 CLASS="c5"
          RenderBlock (positioned) 0x230cd421c410	<pseudo>	0x144152e54010
            RenderCounter 0x230cd4228010
            RenderTextFragment 0x230cd4238010
ASSERTION FAILED: !needsLayout()
../../third_party/WebKit/Source/core/rendering/RenderObject.h(238) : void blink::RenderObject::assertRendererLaidOut() const
#0 0x7f53b1ba9d5e base::debug::StackTrace::StackTrace()
#1 0x7f53b1ba9893 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#2 0x7f53a4491cb0 <unknown>
#3 0x7f53ac7be54a blink::RenderObject::assertRendererLaidOut()
#4 0x7f53ac7bca9b blink::RenderObject::assertSubtreeIsLaidOut()
#5 0x7f53ac7b2ede blink::FrameView::layout()
#6 0x7f53ac7b61a3 blink::FrameView::scrollbarExistenceDidChange()
#7 0x7f53b32ddeac blink::ScrollView::adjustScrollbarExistence()
#8 0x7f53b32dbf4e blink::ScrollView::updateScrollbars()
#9 0x7f53b32dee58 blink::ScrollView::setFrameRect()
#10 0x7f53ac7af89c blink::FrameView::setFrameRect()
#11 0x7f53aa9d15be blink::Widget::resize()
#12 0x7f53aaaa313e blink::WebViewImpl::performResize()
#13 0x7f53aaaa3e89 blink::WebViewImpl::resize()
#14 0x7f53a7187178 content::RenderWidget::Resize()
#15 0x7f53a718c70b content::RenderWidget::OnResize()
#16 0x7f53a715f586 content::RenderViewImpl::OnResize()
#17 0x7f53a719f6f7 DispatchToMethod<>()
#18 0x7f53a719362f ViewMsg_Resize::Dispatch<>()
...

Reduced test attached.

### es...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### fm...@chromium.org (2014-09-23)

Invalidation state after the last style update:

[needsSimplifiedNormalFlowLayout] RenderView 0x230cd4204010              	#document	0x144152e04010
[needsSimplifiedNormalFlowLayout]   RenderBlock 0x230cd421c010           	HTML	0x144152e10120
[needsSimplifiedNormalFlowLayout]     RenderBody 0x230cd421c110          	BODY	0x144152e10010
[]                                      RenderBlock 0x230cd421c210       	OPTION	0x144152e34010 CLASS="c4"
[needsSimplifiedNormalFlowLayout]       RenderTable 0x230cd4220010
[posChildNeedsLayout]             *       RenderBlock 0x230cd421c310     	LI	0x144152e101a8 CLASS="c5"
                                            ...

The trouble is RenderTable::simplifiedNormalFlowLayout() only looks at table sections -- which apparently don't include this contrived LI block => we don't layout the LI subtree.


This tentative fix appears to work (inhibiting the posChildNeedsLayout-> needsSimplifiedNormalFlowLayout inval optimization for tables):

--- a/Source/core/rendering/RenderObject.cpp
+++ b/Source/core/rendering/RenderObject.cpp
@@ -721,7 +721,7 @@ void RenderObject::markContainingBlocksForLayout(bool scheduleRelayout, RenderOb
             if (willSkipRelativelyPositionedInlines)
                 container = object->container();
             object->setPosChildNeedsLayout(true);
-            simplifiedNormalFlowLayout = true;
+            simplifiedNormalFlowLayout = !(container && container->isTable());
             ASSERT(!object->isSetNeedsLayoutForbidden());
         } else if (simplifiedNormalFlowLayout) {
             if (object->needsSimplifiedNormalFlowLayout())


But since I'm not sure about implications and how all this is supposed to fit together (should the LI block be in a table section instead?), I'm punting to someone who hopefully does.

### in...@chromium.org (2014-09-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-01)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-08)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### oj...@chromium.org (2014-10-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-16)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-24)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-31)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-15)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-22)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-30)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-07)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-07)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4666876171911168

### cl...@chromium.org (2014-12-07)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5631452963143680

### pd...@chromium.org (2014-12-07)

@dsinclair, do you think someone from project warden could take a look at this? Buried in the nags is an almost-patch by fmalita in #8.

In the meantime, knocking this down to P2 since it's clearly not P1. I uploaded fmalita's testcase to clusterfuzz to get a more up-to-date stacktrace.

### cl...@chromium.org (2014-12-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4666876171911168

Uploader: pdr@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: offset + length <= m_length
  blink::InlineTextBoxPainter::paint
  blink::InlineTextBox::paint
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=283013:284047

Minimized Testcase (0.57 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Yv6sxLZgIKHbHUqtWTQmEu3s6ZKFoqSwu2YWYsSUaMU9GVLJ0DbTnA4mZfcieueTD77L0yFi9LKHyNkSMJHYb-ON_HpKkEx8gwS-N3G-ng8to4BiDIY9SaltQTz17z3vOMY1fj0TkMlspRHvJvg-FabngiQ



### pd...@chromium.org (2014-12-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-15)

dsinclair@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ds...@chromium.org (2014-12-15)

I've confirmed that the about patch also fixes the MSAN crash from the test case attached to the clusterfuzz result.

The issue that pdr@ uploaded seems to be different? I don't see hte offset+length <= m_length error locally, I'm getting the original crash in SurrogatePairAwareTextIterator.h.

I'll upload a CL with fmalita@'s change and see what bots and people say in code review.

### ds...@chromium.org (2014-12-16)

CL up for review: https://codereview.chromium.org/804383002/

I ended up not using fmalita@'s patch but, instead, set the tables simplifiedNormalFlowLayout to make sure we layout the table captions which, I think, makes sense.

### ds...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-12-19)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187509

------------------------------------------------------------------
r187509 | dsinclair@chromium.org | 2014-12-19T05:39:24.707639Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/table/display-table-caption-crash-expected.txt?r1=187509&r2=187508&pathrev=187509
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/table/caption-position-expected.html?r1=187509&r2=187508&pathrev=187509
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/table/caption-position.html?r1=187509&r2=187508&pathrev=187509
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/table/display-table-caption-crash.html?r1=187509&r2=187508&pathrev=187509
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderTable.cpp?r1=187509&r2=187508&pathrev=187509

Layout captions in simplifiedNormalFlowLayout for tables.

It is currently possible to get into simplifiedNormalFlowLayout for a table
while the captions need layout. Currently the simplified code will just
iterate over all of the table sections and lay them out if needed.

This CL adds iteration over the table captions as well and makes sure they're
also laid out during simplifedNormalFlowLayout.

BUG=414109

Review URL: https://codereview.chromium.org/804383002
-----------------------------------------------------------------

### in...@chromium.org (2014-12-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

ClusterFuzz has detected this issue as fixed in range 309159:309173.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6192550760153088

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  unsigned int blink::WidthIterator::advanceInternal<blink::SurrogatePairAwar
  blink::WidthIterator::advance
  blink::Font::getGlyphsAndAdvancesForSimpleText
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=309159:309173

Minimized Testcase (3.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96L0scVrYJZvV3RfLsJPVrP2aNX2EsUlqu75uN0p0wvl9SFkgMw19nqLdr8TZg8hlIendPtEzxrDYQm1axwclSMNrz5NHxtJN9-TVERiMF5CoNmERJTJAHxL5IIrYoRrIjYRZgqIOUDEm52IDhOc7yAHPjluw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-19)

ClusterFuzz has detected this issue as fixed in range 309126:309171.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4666876171911168

Uploader: pdr@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: offset + length <= m_length
  blink::InlineTextBoxPainter::paint
  blink::InlineTextBox::paint
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=306834:307048
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=309126:309171

Minimized Testcase (0.57 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Yv6sxLZgIKHbHUqtWTQmEu3s6ZKFoqSwu2YWYsSUaMU9GVLJ0DbTnA4mZfcieueTD77L0yFi9LKHyNkSMJHYb-ON_HpKkEx8gwS-N3G-ng8to4BiDIY9SaltQTz17z3vOMY1fj0TkMlspRHvJvg-FabngiQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-23)

Approved for M40 (branch: 2214)

### in...@chromium.org (2015-01-02)

Please merges these fixes to M40 (branch: 2214) asap. The branch will be cut soon for M40 release.

### bu...@chromium.org (2015-01-05)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187860

------------------------------------------------------------------
r187860 | dsinclair@chromium.org | 2015-01-05T15:30:34.967649Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/table/display-table-caption-crash.html?r1=187860&r2=187859&pathrev=187860
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/rendering/RenderTable.cpp?r1=187860&r2=187859&pathrev=187860
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/table/display-table-caption-crash-expected.txt?r1=187860&r2=187859&pathrev=187860
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/table/caption-position-expected.html?r1=187860&r2=187859&pathrev=187860
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/table/caption-position.html?r1=187860&r2=187859&pathrev=187860

Merge 187509 "Layout captions in simplifiedNormalFlowLayout for ..."

> Layout captions in simplifiedNormalFlowLayout for tables.
> 
> It is currently possible to get into simplifiedNormalFlowLayout for a table
> while the captions need layout. Currently the simplified code will just
> iterate over all of the table sections and lay them out if needed.
> 
> This CL adds iteration over the table captions as well and makes sure they're
> also laid out during simplifedNormalFlowLayout.
> 
> BUG=414109
> 
> Review URL: https://codereview.chromium.org/804383002

TBR=dsinclair@chromium.org

Review URL: https://codereview.chromium.org/807013004
-----------------------------------------------------------------

### in...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

$1000 for this report. Panel notes: "$500 for the bug, +$500 ClusterFuzz bonus".

### ea...@chromium.org (2015-01-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-03-27)

Bulk update: removing view restriction from closed bugs.

### la...@google.com (2015-06-13)

[Empty comment from Monorail migration]

### la...@google.com (2015-06-13)

Attempting to remove dominik.rottsches@intel.com from cc.

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

This issue was migrated from crbug.com/chromium/414109?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/437684]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080457)*
