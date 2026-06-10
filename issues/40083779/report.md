# Heap-use-after-free in blink::FrameView::performLayout

| Field | Value |
|-------|-------|
| **Issue ID** | [40083779](https://issues.chromium.org/issues/40083779) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2016-1644 |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ko...@chromium.org |
| **Created** | 2016-02-29 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5304655887728640

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6030000fd040
Crash State:
  blink::FrameView::performLayout
  blink::FrameView::layout
  blink::FrameView::updateStyleAndLayoutIfNeededRecursive
  
Recommended Security Severity: Medium


Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96frxd4QqejYvrhWUZHdWaEuLi5IRAA1imRemRvaRyJc3qh0JBgfBpIvC-643BQAKrwK27fZokgYjVj2Io-gBz9By0NBn_O-317HsGgfB0l2U90E0m7c1NegWN_3zgKFBzXOYbgu5a2lZp7rHc9MkFwOssQow


Additional requirements: Requires Gestures

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-02-29)

This may be the cause of https://crbug.com/chromium/589773.

It hits an assertion:
ASSERTION FAILED: !extraRowSpanningHeight
../../third_party/WebKit/Source/core/layout/LayoutTableSection.cpp(663) : void blink::LayoutTableSection::distributeRowSpanHeightToRows(SpanningLayoutTableCells &)

If I ignore this, it hits:
ASSERTION FAILED: !object.frameView()->isInPerformLayout()
../../third_party/WebKit/Source/core/layout/DepthOrderedLayoutObjectList.cpp(15) : void blink::DepthOrderedLayoutObjectList::add(blink::LayoutObject &)

#2 0x7f3e1517452e blink::DepthOrderedLayoutObjectList::add()
#3 0x7f3e14f2db64 blink::FrameView::scheduleRelayoutOfSubtree()
#4 0x7f3e1518f782 blink::LayoutBlock::dirtyForLayoutFromPercentageHeightDescendants()
#5 0x7f3e151a130d blink::LayoutBlockFlow::layoutBlockChildren()
#6 0x7f3e1519c8e1 blink::LayoutBlockFlow::layoutBlockFlow()
#7 0x7f3e1519c290 blink::LayoutBlockFlow::layoutBlock()
#8 0x7f3e1518c429 blink::LayoutBlock::layout()
#9 0x7f3e1519da53 blink::LayoutBlockFlow::positionAndLayoutOnceIfNeeded()
#10 0x7f3e1519dbb9 blink::LayoutBlockFlow::layoutBlockChild()
#11 0x7f3e151a1662 blink::LayoutBlockFlow::layoutBlockChildren()
#12 0x7f3e1519c8e1 blink::LayoutBlockFlow::layoutBlockFlow()
#13 0x7f3e1519c290 blink::LayoutBlockFlow::layoutBlock()
#14 0x7f3e1518c429 blink::LayoutBlock::layout()
#15 0x7f3e152ddefe blink::LayoutSVGForeignObject::layout()
#16 0x7f3e152f7711 blink::SVGLayoutSupport::layoutChildren()
#17 0x7f3e152eff2b blink::LayoutSVGRoot::layout()
#18 0x7f3e14f28552 blink::FrameView::performLayout()

Now I'm not sure whether the issue is in subtree layout or in LayoutSVGForeignObject.

leviw@, fs@, any idea whether:
1. we should allow adding m_layoutSubtreeRootList during layout, or
2. LayoutSVGForeignObject should not dirty layout subtree root
?

### oc...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>Layout]

### cl...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### le...@chromium.org (2016-02-29)

In this particular case, dirtyForLayoutFromPercentageHeightDescendants shouldn't lead to a call to markContainerChainForLayout with scheduleRelayout = true. We're in layout and we're marking a descendant as needing layout with the intention of visiting it during this layout. We shouldn't be scheduling it to be laid out later.

### bu...@chromium.org (2016-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1

commit 6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1
Author: kojii <kojii@chromium.org>
Date: Wed Mar 02 01:04:55 2016

Fix SubtreeLayoutScope not to schedule relayout

This patch fixes SubtreeLayoutScope::setNeedsLayout() and
setChildNeedsLayout() not to schedule relayout when they call
markContainerChainForLayout().

The signature of markContainerChainForLayout() allows to schedule
relayout even when SubtreeLayoutScope exists. To not allow scheduling
relayout while we're in layout, this patch changes the signature.

BUG=590620

Review URL: https://codereview.chromium.org/1755543002

Cr-Commit-Position: refs/heads/master@{#378639}

[add] https://crrev.com/6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1/third_party/WebKit/LayoutTests/fast/layout/subtree-layout-percent-height-assert-expected.txt
[add] https://crrev.com/6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1/third_party/WebKit/LayoutTests/fast/layout/subtree-layout-percent-height-assert.html
[modify] https://crrev.com/6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1/third_party/WebKit/Source/core/layout/LayoutObject.cpp
[modify] https://crrev.com/6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1/third_party/WebKit/Source/core/layout/LayoutObject.h


### ko...@chromium.org (2016-03-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-03-02)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1

commit 6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1
Author: kojii <kojii@chromium.org>
Date: Wed Mar 02 01:04:55 2016


### cl...@chromium.org (2016-03-02)

ClusterFuzz has detected this issue as fixed in range 378578:378682.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5304655887728640

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6030000b96f0
Crash State:
  blink::FrameView::performLayout
  blink::FrameView::layout
  blink::FrameView::updateStyleAndLayoutIfNeededRecursive
  
Recommended Security Severity: Medium

Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=378578:378682

Minimized Testcase (1.72 Kb): https://cluster-fuzz.appspot.com/download/AMIfv959W1srKEy4e9LArEkDmv5QHi0lDCmb1Sf0bnVeNY-XndezSz3cI35iywuuwTne_JKbxbQl-m1907HYrOXT_pdQTWgT8JdyeAhdMujVuV1fibHerpDVTf1yd3rqDfbzpiwrDDKaOoeHAbAzammHb3WRMk12-A

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ea...@chromium.org (2016-03-03)

Yay, the fix works. Thank you Koji!

### cb...@chromium.org (2016-03-03)

Should this be merged to M50? Probably not 49, I guess.

### ko...@chromium.org (2016-03-04)

Yeah, right, requesting.

### ti...@google.com (2016-03-04)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### bu...@chromium.org (2016-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1fb49bb47cbcb17f44198fc2a906928adf4dbaff

commit 1fb49bb47cbcb17f44198fc2a906928adf4dbaff
Author: Koji Ishii <kojii@chromium.org>
Date: Fri Mar 04 05:16:31 2016

Fix SubtreeLayoutScope not to schedule relayout

This patch fixes SubtreeLayoutScope::setNeedsLayout() and
setChildNeedsLayout() not to schedule relayout when they call
markContainerChainForLayout().

The signature of markContainerChainForLayout() allows to schedule
relayout even when SubtreeLayoutScope exists. To not allow scheduling
relayout while we're in layout, this patch changes the signature.

BUG=590620

Review URL: https://codereview.chromium.org/1755543002

Cr-Commit-Position: refs/heads/master@{#378639}
(cherry picked from commit 6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1)

Review URL: https://codereview.chromium.org/1768493002 .

Cr-Commit-Position: refs/branch-heads/2661@{#76}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[add] https://crrev.com/1fb49bb47cbcb17f44198fc2a906928adf4dbaff/third_party/WebKit/LayoutTests/fast/layout/subtree-layout-percent-height-assert-expected.txt
[add] https://crrev.com/1fb49bb47cbcb17f44198fc2a906928adf4dbaff/third_party/WebKit/LayoutTests/fast/layout/subtree-layout-percent-height-assert.html
[modify] https://crrev.com/1fb49bb47cbcb17f44198fc2a906928adf4dbaff/third_party/WebKit/Source/core/layout/LayoutObject.cpp
[modify] https://crrev.com/1fb49bb47cbcb17f44198fc2a906928adf4dbaff/third_party/WebKit/Source/core/layout/LayoutObject.h


### ko...@chromium.org (2016-03-04)

> Probably not 49, I guess.

I think so too, adding the label to make sure people who can make the decision can have a look. Please feel free to reject if this does not meet the bar.

### cl...@chromium.org (2016-03-04)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-05)

Merge approved for M49 (branch 2623). Please note that this will probably not be in next week's stable release (we already have a candidate build on its way). Based on comments (#15 and #11), seems like this is not essential in M49. So, if we have a refresh, this change will be in that cut.

### bu...@chromium.org (2016-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/402601f6de1e6ff85d404bcbfd059573c36c0562

commit 402601f6de1e6ff85d404bcbfd059573c36c0562
Author: Koji Ishii <kojii@chromium.org>
Date: Sat Mar 05 15:25:34 2016

Fix SubtreeLayoutScope not to schedule relayout

This patch fixes SubtreeLayoutScope::setNeedsLayout() and
setChildNeedsLayout() not to schedule relayout when they call
markContainerChainForLayout().

The signature of markContainerChainForLayout() allows to schedule
relayout even when SubtreeLayoutScope exists. To not allow scheduling
relayout while we're in layout, this patch changes the signature.

BUG=590620

Review URL: https://codereview.chromium.org/1755543002

Cr-Commit-Position: refs/heads/master@{#378639}
(cherry picked from commit 6e396c50a4630c1bd065aaf19244cf8c1fdcd6d1)

Review URL: https://codereview.chromium.org/1763343002 .

Cr-Commit-Position: refs/branch-heads/2623@{#586}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[add] https://crrev.com/402601f6de1e6ff85d404bcbfd059573c36c0562/third_party/WebKit/LayoutTests/fast/layout/subtree-layout-percent-height-assert-expected.txt
[add] https://crrev.com/402601f6de1e6ff85d404bcbfd059573c36c0562/third_party/WebKit/LayoutTests/fast/layout/subtree-layout-percent-height-assert.html
[modify] https://crrev.com/402601f6de1e6ff85d404bcbfd059573c36c0562/third_party/WebKit/Source/core/layout/LayoutObject.cpp
[modify] https://crrev.com/402601f6de1e6ff85d404bcbfd059573c36c0562/third_party/WebKit/Source/core/layout/LayoutObject.h


### bu...@chromium.org (2016-03-05)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/402601f6de1e6ff85d404bcbfd059573c36c0562

commit 402601f6de1e6ff85d404bcbfd059573c36c0562
Author: Koji Ishii <kojii@chromium.org>
Date: Sat Mar 05 15:25:34 2016


### go...@chromium.org (2016-03-08)

Stable RC in progress 49.0.2623.87 includes this changes. If all goes well with the build, this change will go to stable tomorrow.

### ti...@google.com (2016-03-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-08)

Congrats Atte - $3500 for this bug ($3000 for the bug, +$500 ClusterFuzz bonus).

CVE-ID is CVE-2016-1644 and this should be listed in the release notes for the M-49 patch release today.

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sc...@chromium.org (2016-03-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### no...@google.com (2020-12-12)

[Empty comment from Monorail migration]

### is...@google.com (2020-12-12)

This issue was migrated from crbug.com/chromium/590620?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/588558, crbug.com/chromium/589773]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083779)*
