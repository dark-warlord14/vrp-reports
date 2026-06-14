# Heap-use-after-free in blink::DeprecatedPaintLayer::setGroupedMapping

| Field | Value |
|-------|-------|
| **Issue ID** | [40082450](https://issues.chromium.org/issues/40082450) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | mi...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2015-07-08 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4874486313123840

Fuzzer: Miaubiz_css_fuzzer
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x048701e4
Crash State:
  blink::DeprecatedPaintLayer::setGroupedMapping
  blink::CompositedDeprecatedPaintLayerMapping::updateSquashingLayerAssignment
  blink::CompositingLayerAssigner::updateSquashingAssignment
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=337409:337474

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96bzAymeich9264_PWc63_jBLi8Z841e8T2qKDFXFjo6tXswtHwLwXN4M9pbBTGy2klJmpS2NdnjNmfyTxfmysbjkmzkVIE_RpKK65kdFJxyxhS65wbdf9TteYC92Ux3-RBunU8B3z25fW45_2DNWlEqnGlssuuZHVkaZ1cD_UAFNtEcDg


Filer: inferno

## Timeline

### in...@chromium.org (2015-07-08)

Author: schenney@chromium.org 
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/4ed403f935e469766ff5d86096c3b0cb94cc5808
Time: Mon Jul 06 18:57:01 2015
Lines 2278 of file CompositedDeprecatedPaintLayerMapping.cpp which potentially caused crash are changed in this cl (frame #1, "blink::CompositedDeprecatedPaintLayerMapping::updateSquashingLayerAssignment").

Lines 2355 of file DeprecatedPaintLayer.cpp which potentially caused crash are changed in this cl (frame #0, "blink::DeprecatedPaintLayer::setGroupedMapping").

File CompositingLayerAssigner.cpp is changed in this cl (and is part of stack frame #2, "blink::CompositingLayerAssigner::updateSquashingAssignment"; frame #3, "blink::CompositingLayerAssigner::assignLayersToBackingsInternal"; frame #4, "blink::CompositingLayerAssigner::assignLayersToBackingsInternal"; frame #5, "blink::CompositingLayerAssigner::assignLayersToBackingsInternal"; frame #6, "blink::CompositingLayerAssigner::assign")
Minimum distance from crash line to modified line: 0. (file: CompositedDeprecatedPaintLayerMapping.cpp, crashed on: 2275, modified: 2275).

Suspected component: blink

### cl...@chromium.org (2015-07-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4755618999566336

Fuzzer: Marty_html_twiddler
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-use-after-free READ 4
Crash Address: 0xbba446e4
Crash State:
  blink::CompositedDeprecatedPaintLayerMapping::~CompositedDeprecatedPaintLayerMap
  blink::CompositedDeprecatedPaintLayerMapping::~CompositedDeprecatedPaintLayerMap
  blink::DeprecatedPaintLayer::~DeprecatedPaintLayer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=337438:337555

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97dsO1JeDZdW8Q28A5tg_h7jnftbFkZwCmmYSMLWUl2G2lGVSr0FB_7fWi7LgfUB4hLNCUY6ai-kMLuev1wvDMUd_BBomFBw3oIva813XzL44zXDYEz1Xrr5RkQaiMSUhhcV0pJhWiGIkOSmViHs_v1Z6igTZwXdL1kUMWMb6krotmO6GM


Filer: inferno

### cl...@chromium.org (2015-07-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-08)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### sc...@chromium.org (2015-07-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-07-08)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=198534

------------------------------------------------------------------
r198534 | schenney@chromium.org | 2015-07-08T20:38:26.941130Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/layout/compositing/CompositedDeprecatedPaintLayerMapping.cpp?r1=198534&r2=198533&pathrev=198534

Avoid clearing pointers on layers still in the mapping's vector of layers.

When adjusting layers, a particular layer may be added to a grouped
mapping at a location earlier than where it already appears in the
layer vector. When we then clear the unused entries in the list, we
remove the layer and null its group mapping, despite it still being
present earlier in the vector.

R=vollick
BUG=507988

Review URL: https://codereview.chromium.org/1227763002
-----------------------------------------------------------------

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### sc...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2015-07-10)

Is there a merge required here?

### sc...@chromium.org (2015-07-10)

No. We never merged the patch that caused this to break, so I think it's simpler to just leave them both unmerged.

### cl...@chromium.org (2015-07-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-07-16)

ClusterFuzz has detected this issue as potentially fixed, but it appears to be flaky.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4874486313123840

Fuzzer: Miaubiz_css_fuzzer
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x048701e4
Crash State:
  blink::DeprecatedPaintLayer::setGroupedMapping
  blink::CompositedDeprecatedPaintLayerMapping::updateSquashingLayerAssignment
  blink::CompositingLayerAssigner::updateSquashingAssignment
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=337409:337474

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96bzAymeich9264_PWc63_jBLi8Z841e8T2qKDFXFjo6tXswtHwLwXN4M9pbBTGy2klJmpS2NdnjNmfyTxfmysbjkmzkVIE_RpKK65kdFJxyxhS65wbdf9TteYC92Ux3-RBunU8B3z25fW45_2DNWlEqnGlssuuZHVkaZ1cD_UAFNtEcDg

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-07-23)

ClusterFuzz has detected this issue as fixed in range 339832:339843.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4755618999566336

Fuzzer: Marty_html_twiddler
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-use-after-free READ 4
Crash Address: 0xbba446e4
Crash State:
  blink::CompositedDeprecatedPaintLayerMapping::~CompositedDeprecatedPaintLayerMap
  blink::CompositedDeprecatedPaintLayerMapping::~CompositedDeprecatedPaintLayerMap
  blink::DeprecatedPaintLayer::~DeprecatedPaintLayer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=337438:337555
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=339832:339843

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97dsO1JeDZdW8Q28A5tg_h7jnftbFkZwCmmYSMLWUl2G2lGVSr0FB_7fWi7LgfUB4hLNCUY6ai-kMLuev1wvDMUd_BBomFBw3oIva813XzL44zXDYEz1Xrr5RkQaiMSUhhcV0pJhWiGIkOSmViHs_v1Z6igTZwXdL1kUMWMb6krotmO6GM

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### am...@google.com (2015-07-24)

Just to be 100% sure, note that the CFuzz regression listed here started 7/8, which was ahead of 7/10 branch date.  CC'ing timwillis@ from security team for explicit review, removing Merge-TBD in the meantime.

### am...@google.com (2015-07-24)

Actually CC'ing Tim this time - Tim, review if you get a chance please.

### aa...@google.com (2015-07-24)

Based on c#11, marking Merge-NA

### cl...@chromium.org (2015-10-16)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-30)

Miaubiz - surprise $3,500 for this report. (We're going through a non-stable bug reward panel backlog). 

Panel notes: $3,000 for the bug, +$500 for Fuzzer bonus

We'll start payment shortly.

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

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

This issue was migrated from crbug.com/chromium/507988?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082450)*
