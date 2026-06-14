# Heap-use-after-free in WebCore::CompositedLayerMapping::~CompositedLayerMapping

| Field | Value |
|-------|-------|
| **Issue ID** | [40079379](https://issues.chromium.org/issues/40079379) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Compositing |
| **Reporter** | cl...@chromium.org |
| **Assignee** | vo...@chromium.org |
| **Created** | 2014-04-19 |
| **Bounty** | $2,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4743489860403200

Fuzzer: Miaubiz_css_fuzzer
Job Type: Android_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x42d10c58
Crash State:
  - crash stack -
  WebCore::CompositedLayerMapping::~CompositedLayerMapping
  WebCore::CompositedLayerMapping::~CompositedLayerMapping
  - free stack -
  WebCore::RenderLayerModelObject::styleDidChange
  WebCore::RenderBox::styleDidChange
  
Regressed: Clank: r209059:209074

Minimized Testcase (2.31 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95RfcozLRGgi02O3C35xgBBiaS2rjWwjlpba92-_1nP9pxp7bur-sW9Weef0fwTqCWbMsRfnZnRZ9MLwCMlWVdPaMIHOaWx6QoRg4H1FfneuIYRL-krB_59MPTrOsy0-W_Nz96Eb2bU-LsECHOzsisjefnvwQ

Additional requirements: Requires HTTP

## Timeline

### in...@chromium.org (2014-04-19)

recent regression that is only showing up on Android.

Revision 171908 - (view) (annotate) - [select for diffs] 
Modified Fri Apr 18 00:08:27 2014 UTC (29 hours, 16 minutes ago) by ajuma@chromium.org 
File length: 91591 byte(s) 
Diff to previous 171899
Suppress layer creation for descendants of GPU-rasterized layers

This suppresses layer creation in descendants (in stacking
order) of layers that are compositing for GPU-rasterization
hints. More specifically, compositing for animations and for
will-change is suppressed in these layers.

BUG=313532

Review URL: https://codereview.chromium.org/233063004
Revision 171899 - (view) (annotate) - [select for diffs] 
Modified Thu Apr 17 23:19:50 2014 UTC (30 hours, 4 minutes ago) by ch.dumez@samsung.com 
File length: 91483 byte(s) 
Diff to previous 171832
Remove some dead code from rendering/ folder

Remove some dead code from rendering/ folder. Several methods were defined but
never used.

R=esprehn@chromium.org, pdr@chromium.org

Review URL: https://codereview.chromium.org/241713002
Revision 171832 - (view) (annotate) - [select for diffs] 
Modified Thu Apr 17 03:00:35 2014 UTC (2 days, 2 hours ago) by vollick@chromium.org 
File length: 91908 byte(s) 
Diff to previous 171805
Only boxes should have child transform layers.

The child transform layer exists to apply a perspective 
transform on its composited descendants. If this were to
be necessary, the renderer housing the transform should
be a box. Without this requirement, we cannot determine
the correct size of the composited layer which will own
the perpective transform.

Rationale,

According to http://www.w3.org/TR/css-transforms-1/

Perspective can apply to "transformable elements."
That is, to

"""
an element whose layout is governed by the CSS box model
which is either a block-level or atomic inline-level
element, or whose display property computes to table-row,
table-row-group, table-header-group, table-footer-group,
table-cell, or table-caption [CSS21] an element in the
SVG namespace and not governed by the CSS box model which
has the attributes transform, ‘patternTransform‘ or
gradientTransform [SVG11].
"""

block-level elements and atomic inline-level elements
are boxes (see http://www.w3.org/TR/CSS2/visuren.html#x13
for more info on atomic inline-level elements), as are
the table-* things.

SVG elements could cause problems if they could be
separately composited, but they cannot be currently and
the SVG root is a box.

BUG=363873

Review URL: https://codereview.chromium.org/239513010

### cl...@chromium.org (2014-04-19)

[Empty comment from Monorail migration]

### aj...@chromium.org (2014-04-19)

This crash involves accessing a RenderLayer that was previously destroyed in RenderLayerModelObject::styleDidChange. This is unlikely to have been caused by 171908, since that shouldn't have changed RenderLayer creation or destruction (and further, the reduced test case doesn't involve GPU rasterization hints).

It'd be helpful to have the full Blink regression change (I'm not sure where to find this from the Clank regression range).

### vo...@chromium.org (2014-04-19)

Hmm. I may have run across this before, but I didn't have a good repro case. I don't have access to a build at the moment to confirm, but IIRC, if you reorder the updateSquashingLayers(false) and updateScrollingLayers(false) calls in ~CompositedLayerMapping it addresses the issue. I'll take a look on Monday. 

### in...@chromium.org (2014-04-19)

We don't have a way to get blink regression range from Clank range yet. it will be available in the next 2-3 weeks. ClusterFuzz on Android just started a few weeks ago.

### cl...@chromium.org (2014-04-19)

ClusterFuzz has detected this issue as fixed in range 209095:209103.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4743489860403200

Fuzzer: Miaubiz_css_fuzzer
Job Type: Android_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x42d10c58
Crash State:
  - crash stack -
  WebCore::CompositedLayerMapping::~CompositedLayerMapping
  WebCore::CompositedLayerMapping::~CompositedLayerMapping
  - free stack -
  WebCore::RenderLayerModelObject::styleDidChange
  WebCore::RenderBox::styleDidChange
  
Regressed: Clank: r209059:209074
Fixed: Clank: r209095:209103

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95RfcozLRGgi02O3C35xgBBiaS2rjWwjlpba92-_1nP9pxp7bur-sW9Weef0fwTqCWbMsRfnZnRZ9MLwCMlWVdPaMIHOaWx6QoRg4H1FfneuIYRL-krB_59MPTrOsy0-W_Nz96Eb2bU-LsECHOzsisjefnvwQ

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-04-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6135418565165056

Fuzzer: Marty_html_twiddler
Job Type: Android_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x8f0370d8
Crash State:
  - crash stack -
  WebCore::CompositedLayerMapping::~CompositedLayerMapping
  WebCore::CompositedLayerMapping::~CompositedLayerMapping
  - free stack -
  WebCore::RenderBox::willBeDestroyed
  WebCore::RenderObject::destroy
  
Regressed: Clank: r209059:209074

Minimized Testcase (5.67 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95G7KMRagqxqVQOtMkhEG2I8Dytj6fUTvV40W0xnULA4wM1hsfnZruQS0fHPv0KIE5Tz6CjgO6ip5jt3d01_IdtFH0XyB8OHeuMdcrT-t_P50bqKY-5g3s-mx4GNX9YKcnYJaXBoMcXq7CBomBV_B3UURzISw

Additional requirements: Requires HTTP



### vo...@chromium.org (2014-04-21)

[Empty comment from Monorail migration]

### vo...@chromium.org (2014-04-21)

It looks like what's happening here is that when we reassign a RenderLayer's grouped mapping, we don't remove it from the old one! Presumably, this fixes itself when we get around to doing a compositing update (though I'm not even convinced that's always going to work), but if you as a CompositedLayerMapping about the squashed layers it owns at the wrong time, you may find yourself with a stale pointer and boom.

I have a trivial CL to fix this up here:
https://codereview.chromium.org/244253006/

I haven't reduced a test case though (and IIUC, I'm not to attach the clusterfuzz repro).

There is one downside to the fix I've added: you'll take a O(n) hit to remove the squashing layer when you do squashing updates. We'll have to keep an eye out for this in traces. If it becomes a bottleneck, we can experiment with fancier data structures for m_squashedLayers.

### in...@chromium.org (2014-04-21)

Does this bug exist in Stable ?

### vo...@chromium.org (2014-04-21)

Yep.

### in...@chromium.org (2014-04-21)

Thanks!

### cl...@chromium.org (2014-04-21)

[Empty comment from Monorail migration]

### vo...@chromium.org (2014-04-23)

As I've investigated this, it appears to be squashing related, and squashing is _not_ enabled in stable (nor M35, in fact). I'm sorry, I think I gave you bad information in #11.

### ke...@chromium.org (2014-04-23)

Thanks Ian.

### cl...@chromium.org (2014-04-23)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-04-23)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=172409

------------------------------------------------------------------
r172409 | vollick@chromium.org | 2014-04-23T21:26:03.264997Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/compositing/squashing/remove-from-grouped-mapping-on-reassignment-expected.txt?r1=172409&r2=172408&pathrev=172409
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/compositing/RenderLayerCompositor.cpp?r1=172409&r2=172408&pathrev=172409
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/compositing/squashing/remove-from-grouped-mapping-on-reassignment.html?r1=172409&r2=172408&pathrev=172409
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderLayer.cpp?r1=172409&r2=172408&pathrev=172409

Setting RL's grouped mapping should remove it from the old one.

Currently, when a RenderLayer is assigned to a new grouped
mapping for squashing, updateGroupedMapping will only mark
the old grouped mapping as needing a graphics layer update.
The old grouped mapping will, however, retain a raw pointer
to the RenderLayer.

It turns out that it is possible to get the old grouped
mapping to use this raw pointer, so it's important that we
clear it when we switch backings so that this never happens.

The attached test case triggers this use of one of these
stale pointers, but it's clunky. It should be possible to
get a better repro.

R=abarth@chromium.org
BUG=365064

Review URL: https://codereview.chromium.org/244253006
-----------------------------------------------------------------

### in...@chromium.org (2014-04-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-24)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M36 label.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-07-14)

Congrats Miaubiz - $2000 for this report (UAF, but in node partition).

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-03)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/365064?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/366135]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079379)*
