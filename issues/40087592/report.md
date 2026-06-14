# Heap-use-after-free in blink::VisualRectForDisplayItem

| Field | Value |
|-------|-------|
| **Issue ID** | [40087592](https://issues.chromium.org/issues/40087592) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ch...@chromium.org |
| **Created** | 2017-05-09 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=4917785875709952

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x07689a80
Crash State:
  blink::VisualRectForDisplayItem
  blink::PaintController::CommitNewDisplayItems
  blink::GraphicsLayer::Paint
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4917785875709952


Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Attachments

- [minimized.html](attachments/minimized.html) (text/plain, 305 B)
- [test.html](attachments/test.html) (text/plain, 288 B)

## Timeline

### sh...@chromium.org (2017-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-05-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6486232434737152

### cl...@chromium.org (2017-05-10)

Detailed report: https://clusterfuzz.com/testcase?key=6486232434737152

Job Type: linux_asan_chrome_mp
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e000078c80
Crash State:
  blink::VisualRectForDisplayItem
  blink::PaintController::CommitNewDisplayItems
  blink::GraphicsLayer::Paint
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=436273:436323

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6486232434737152


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### aa...@google.com (2017-05-10)

Looks like regression from https://chromium.googlesource.com/chromium/src/+/af2c8d1e6a537c356b4cf931bb5aca1e5f09f119 based on range in c#4.

[Monorail components: Blink>Paint]

### cl...@chromium.org (2017-05-10)

[Empty comment from Monorail migration]

### aa...@google.com (2017-05-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-05-10)

[Empty comment from Monorail migration]

### pd...@chromium.org (2017-05-11)

Minimized the testcase.

### pd...@chromium.org (2017-05-11)

I manually tried the entire range (https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=436273:436323) using the minimized repro but we UAF for all revs in the range.

@Abhishek, can you upload my minimized testcase to clusterfuzz and kick off a regression bisect?

### cl...@chromium.org (2017-05-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4595245575831552

### aa...@google.com (2017-05-11)

Just did it, in future, you can upload it using https://clusterfuzz.com/?noredirect=1#uploadusertestcase

### pd...@chromium.org (2017-05-11)

Thanks!

While that goes, I found we can bisect with --enable-blink-features=PaintUnderInvalidationChecking

Range:
https://chromium.googlesource.com/chromium/src/+log/29bb3301df59c321abee8d9d226bf38e3877a5fb..60e845bca3f291f751495b1ae9f119acd1bccae7
I think this is https://chromium.googlesource.com/chromium/src/+/a77dfb5865c1fc52c2094acba37fea629e26ccf5

We're failing to invalidate pseudo-content on foreign object. One fix is to disable pseudo content (:after, :before) on foreign object entirely.

### cl...@chromium.org (2017-05-12)

Detailed report: https://clusterfuzz.com/testcase?key=4595245575831552

Job Type: linux_asan_chrome_mp
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e000047e40
Crash State:
  blink::VisualRectForDisplayItem
  blink::PaintController::CommitNewDisplayItems
  blink::GraphicsLayer::Paint
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=459626:459636

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4595245575831552


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ch...@chromium.org (2017-05-16)

The problem is that the containing stacking context for an absolutely-positioned
element child of the foreign object is the HTML element. Thus
PaintLayer::SetNeedsRepaint, which sets bits on the stacking ancestor chain,
skips the foreign object and goes straight to the HTML element, and therefore
fails to invalidate subsequence caching on the SVG root.

### ch...@chromium.org (2017-05-16)

Just realized that the problem here is more pedestrian. It's that we fail
to invalidate the previous subsequence location before allocating a PaintLayer
for the child.

Reduced testcase that doesn't use any pseudo elements attached. This one
doesn't cause a use-after-free, but is otherwise the same flavor of under-
invalidation.

### ch...@chromium.org (2017-05-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c17fd462aca8510e9dc38bda911efa2b12d09d4e

commit c17fd462aca8510e9dc38bda911efa2b12d09d4e
Author: chrishtr <chrishtr@chromium.org>
Date: Thu May 18 06:21:07 2017

Only allow subsequence caching for SVG documents, not inline SVG.

Once SVGRoots induce stacking contexts, we can do all SVG. See https://crbug.com/chromium/723076.

BUG=723076,719835
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_layout_tests_slimming_paint_v2

Review-Url: https://codereview.chromium.org/2889783003
Cr-Commit-Position: refs/heads/master@{#472704}

[modify] https://crrev.com/c17fd462aca8510e9dc38bda911efa2b12d09d4e/third_party/WebKit/Source/core/paint/PaintLayer.cpp
[modify] https://crrev.com/c17fd462aca8510e9dc38bda911efa2b12d09d4e/third_party/WebKit/Source/core/paint/PaintLayerPainterTest.cpp
[modify] https://crrev.com/c17fd462aca8510e9dc38bda911efa2b12d09d4e/third_party/WebKit/Source/core/paint/PaintLayerTest.cpp
[modify] https://crrev.com/c17fd462aca8510e9dc38bda911efa2b12d09d4e/third_party/WebKit/Source/core/svg/graphics/SVGImage.h
[modify] https://crrev.com/c17fd462aca8510e9dc38bda911efa2b12d09d4e/third_party/WebKit/Source/core/svg/graphics/SVGImageTest.cpp


### ch...@chromium.org (2017-05-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-05-19)

ClusterFuzz has detected this issue as fixed in range 472667:472720.

Detailed report: https://clusterfuzz.com/testcase?key=4917785875709952

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x07689a80
Crash State:
  blink::VisualRectForDisplayItem
  blink::PaintController::CommitNewDisplayItems
  blink::GraphicsLayer::Paint
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=472667:472720

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4917785875709952


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-05-19)

ClusterFuzz has detected this issue as fixed in range 472665:472720.

Detailed report: https://clusterfuzz.com/testcase?key=6486232434737152

Job Type: linux_asan_chrome_mp
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e000078c80
Crash State:
  blink::VisualRectForDisplayItem
  blink::PaintController::CommitNewDisplayItems
  blink::GraphicsLayer::Paint
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=436273:436323
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=472665:472720

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6486232434737152


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-05-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

Nice! $2,000 for this, and $500 as the fuzzer bonus.

### aw...@chromium.org (2017-05-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-07-14)

ClusterFuzz testcase 4595245575831552 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add ClusterFuzz-Wrong label.

### sc...@chromium.org (2017-07-17)

[Empty comment from Monorail migration]

### sc...@chromium.org (2017-07-17)

chrisht@, could you re-verify the test case?

### sh...@chromium.org (2017-07-18)

chrishtr: Uh oh! This issue still open and hasn't been updated in the last 60 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-07-18)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@chromium.org (2017-07-19)

The testcase for this bug does not reproduce under an ASAN build.

### ch...@chromium.org (2017-07-19)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-07-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5c301712a67bbe70026048a224b4608628199e12

commit 5c301712a67bbe70026048a224b4608628199e12
Author: Chris Harrelson <chrishtr@chromium.org>
Date: Wed Jul 04 01:20:53 2018

Fix CompositingContainer for replaced normal-flow stacking contexts.

For such PaintLayers, the CompositingContainer is the parent, not the
containing stacking context. This is because such stacking contexts
paint during the normal-flow of the ancestor layout object.

This also allows us to enable subsequence caching; the previous attempt
last week was still suffering from the under-invalidation reported
in https://crbug.com/chromium/859520.

The testcases that crash on ASAN from the referenced bugs are fixed;
one such example is included in this CL.

Bug:859294,719835,723076,859520

Cq-Include-Trybots: luci.chromium.try:linux_layout_tests_slimming_paint_v2;master.tryserver.blink:linux_trusty_blink_rel
Change-Id: I6ab5271d70bd834482c22b89f09b93907788ed0c
Reviewed-on: https://chromium-review.googlesource.com/1125269
Commit-Queue: Chris Harrelson <chrishtr@chromium.org>
Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#572428}
[add] https://crrev.com/5c301712a67bbe70026048a224b4608628199e12/third_party/WebKit/LayoutTests/svg/foreignObject/foreignObject-position-crash.html
[modify] https://crrev.com/5c301712a67bbe70026048a224b4608628199e12/third_party/blink/renderer/core/paint/compositing/graphics_layer_updater.cc
[modify] https://crrev.com/5c301712a67bbe70026048a224b4608628199e12/third_party/blink/renderer/core/paint/paint_invalidator.cc
[modify] https://crrev.com/5c301712a67bbe70026048a224b4608628199e12/third_party/blink/renderer/core/paint/paint_layer.cc
[modify] https://crrev.com/5c301712a67bbe70026048a224b4608628199e12/third_party/blink/renderer/core/paint/paint_layer.h
[modify] https://crrev.com/5c301712a67bbe70026048a224b4608628199e12/third_party/blink/renderer/core/paint/paint_layer_test.cc


### is...@google.com (2018-07-04)

This issue was migrated from crbug.com/chromium/719835?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087592)*
