# ASSERTION FAILED: !object || (object->isBox()), UNKNOWN in WebCore::CompositedLayerMapping::updateGraphicsLayerGeometry

| Field | Value |
|-------|-------|
| **Issue ID** | [40079358](https://issues.chromium.org/issues/40079358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Compositing |
| **Reporter** | cl...@chromium.org |
| **Assignee** | vo...@chromium.org |
| **Created** | 2014-04-16 |
| **Bounty** | $3,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4998755537387520

Fuzzer: Miaubiz_css_fuzzer
Job Type: Android_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0xfbadbeef
Crash State:
  - crash stack -
  WebCore::CompositedLayerMapping::updateGraphicsLayerGeometry
  WebCore::GraphicsLayerUpdater::update
  WebCore::GraphicsLayerUpdater::update
  
Regressed: Clank: r208297:208335

Minimized Testcase (0.70 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97vouBGhL3k9pWQKEyoP_C8Hzqvg80Bf7VL-jm7hJU9hHhGmLdJv1nDBUDCZkpzULl5Ny6RFeflIlwu9eb3_lYtsmisrXBQiOAj8Ka7LlRs4cV8gsqOo3TdvxNQSHWFwQW1cT5lKFF7smsvwMbmaq5CAsI0cg

Additional requirements: Requires HTTP

## Timeline

### in...@chromium.org (2014-04-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-16)

[Empty comment from Monorail migration]

### vo...@chromium.org (2014-04-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-04-17)

What is the commit link ? or codereview link ?

### vo...@chromium.org (2014-04-17)

https://codereview.chromium.org/239513010/

### bu...@chromium.org (2014-04-17)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=171832

------------------------------------------------------------------
r171832 | vollick@chromium.org | 2014-04-17T03:00:35.940219Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/compositing/CompositedLayerMapping.cpp?r1=171832&r2=171831&pathrev=171832
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/compositing/child-transform-layer-requires-box-expected.txt?r1=171832&r2=171831&pathrev=171832
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/compositing/child-transform-layer-requires-box.html?r1=171832&r2=171831&pathrev=171832

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
-----------------------------------------------------------------

### cl...@chromium.org (2014-04-18)

ClusterFuzz has detected this issue as fixed in range 208845:208853.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4998755537387520

Fuzzer: Miaubiz_css_fuzzer
Job Type: Android_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0xfbadbeef
Crash State:
  - crash stack -
  WebCore::CompositedLayerMapping::updateGraphicsLayerGeometry
  WebCore::GraphicsLayerUpdater::update
  WebCore::GraphicsLayerUpdater::update
  
Regressed: Clank: r208297:208335
Fixed: Clank: r208845:208853

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97vouBGhL3k9pWQKEyoP_C8Hzqvg80Bf7VL-jm7hJU9hHhGmLdJv1nDBUDCZkpzULl5Ny6RFeflIlwu9eb3_lYtsmisrXBQiOAj8Ka7LlRs4cV8gsqOo3TdvxNQSHWFwQW1cT5lKFF7smsvwMbmaq5CAsI0cg

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-04-22)

Merge Requested for M35

### ka...@google.com (2014-04-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-25)

Vollick@, does this impact m34 ?

### vo...@chromium.org (2014-04-28)

So sorry for the slow response! No, this does not impact m34.

The problem was that I was asking for box-related info to size the "child transform layer" as of blink r171502, and sometimes we weren't a box.

Looking at omaha proxy, M34 was cut at blink r167304, and M35 was cut at blink r170313, so I don't think any merging is necessary as both branches missed the troublesome revision.

### vo...@chromium.org (2014-04-28)

Whoops. Messed up the status.

### ti...@chromium.org (2014-04-28)

Thanks vollick@ - Marking as merge not required and Security_Impact-None (which actually doesn't mean no impact, just not in stable or beta. There's a CL that should land in a few days that will change the label to Security_Impact-Head for clarity).

### ti...@chromium.org (2014-05-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M36 label.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-07-14)

Congrats - $3000 for this one (nice bad cast).

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/363873?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079358)*
