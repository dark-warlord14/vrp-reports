# Heap-buffer-overflow in blink::SVGFilterGraphNodeMap::addPrimitive

| Field | Value |
|-------|-------|
| **Issue ID** | [40083011](https://issues.chromium.org/issues/40083011) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SVG |
| **Platforms** | Linux |
| **Reporter** | mi...@gmail.com |
| **Assignee** | fs...@opera.com |
| **Created** | 2015-10-09 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4572849078009856

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x61200006ac88
Crash State:
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  blink::SVGFilterPainter::prepareEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=353033:353139

Minimized Testcase (1.89 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97GoKG955C3fUHodwpkOaHeGwFOZavKnWmSuDX7AttxXD6vqhPZQkT9V_vZZWG0eRHb3EQlACBtGus1SmgTKJe6CLHFzVNK28_8vdyV23waeMsU14HMhMZ6AHin6Ney8TJQmfI42HbsyL4FpGlAM5FeWlc7bg

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2015-10-09)

The result is a list of CLs that change the crashed files.

Author: fs
Component: chromium
Changelist: https://chromium.googlesource.com/chromium/src//+/e795c33a0120bf58d20fc324111c9108b3fc815e
Time: Thu Oct 08 20:21:27 2015
Lines 56-65, 131-141 of file SVGFilterBuilder.cpp which potentially caused crash are changed in this cl (frame #3, "blink::SVGFilterGraphNodeMap::addPrimitive"; frame #4, "blink::SVGFilterBuilder::buildGraph").

Lines 142-145 of file SVGFilterPainter.cpp which potentially caused crash are changed in this cl (frame #5, "blink::SVGFilterPainter::prepareEffect").
Minimum distance from crash line to modified line: 0. (file: SVGFilterBuilder.cpp, crashed on: 131, modified: 131).

Suspected component: chromium

### fs...@opera.com (2015-10-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-10)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5016624761929728

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xb8c24ce4
Crash State:
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  blink::SVGFilterPainter::prepareEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=353013:353144

Minimized Testcase (2.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv963d2iMLMXjTFQwZztfztFB_niNlSaYeNsi2p_A-vGVCDENpcG71JY-u3isclhn0OGWmeq6Q6P_zqNsQBfVTLAxt4iow4VR0I6RbOPGlnBIRsfFvITjzAGxUcNTMNwUHP41IiutepMtkcCRqGMzJxZJJnulPg

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2015-10-10)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6197885522149376

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_syzyasan_chrome
Platform Id: windows

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x0572d1af
Crash State:
  WTF::HashTable<blink::ThreadState *,blink::ThreadState *,WTF::IdentityExtractor,
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_syzyasan_chrome&range=353235:353267

Minimized Testcase (1.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94-wPJBNw6mqy1guTGz44XHDT0BlGszEITPDVTUagxEeU4Y5gDS3pqPOx5ucKwnpI8ugOGkAvBV-AAqTd5FVR9ktY-9_k_QSywk_k-3kraM9zF7GskT-PuIi_NxwkTR0Kz57JOttIWkMDDKUmlIVCXWESDDZw

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2015-10-10)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4547854247395328

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  blink::SVGFilterPainter::prepareEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=353124:353144

Minimized Testcase (10.64 Kb): https://cluster-fuzz.appspot.com/download/AMIfv946G06g4NwkC21SMzoQIXKWqgchSYrGo8Co4fGxUgeQUF9ch3Sx_AqGHGBTFiaaldVq4S25QG5pwAAWOyLjY5gRj7JYvMEKCTrxrJDfiDiO20jXGiXCVURMdIVXZ7zA4wcsGZ8x_yfPByAE6lAplrfMfNfs6Q

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### fe...@chromium.org (2015-10-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-11)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-10-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-10-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5409123905044480

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_syzyasan_chrome
Platform Id: windows

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x055380e7
Crash State:
  WTF::HashTable<blink::IdTargetObserver *,blink::IdTargetObserver *,WTF::Identity
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_syzyasan_chrome&range=353464:353465

Minimized Testcase (9.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97T_woXHfsJnu7cbJ_9AGkQ6uRsnkOGi1ZhK0T7Qz3myeK4VvBeefd0LND9HcY7bykSqFGdMViwQqLbujd3P2eetbSW9JDgWSKAR7x42CywvmFn08h43GZkxY9W38kcHC2TYffuO7VaJB3W88PvTdNYroI8WA

Filer: mbarbella

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### bu...@chromium.org (2015-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fb79f7fc46552d45127acd2959a23662ad8f271e

commit fb79f7fc46552d45127acd2959a23662ad8f271e
Author: fs <fs@opera.com>
Date: Mon Oct 12 23:15:51 2015

Always populate the node map in SVGFilterBuilder if one exists

Since the node map is essentially a "reverse DAG" we cannot have holes
in it, so always add the FilterEffects even we cannot provide the
LayoutObject -> FilterEffect mapping (like in the case of a non-attached
element.)

BUG=541593, 533457

Review URL: https://codereview.chromium.org/1393633007

Cr-Commit-Position: refs/heads/master@{#353620}

[add] http://crrev.com/fb79f7fc46552d45127acd2959a23662ad8f271e/third_party/WebKit/LayoutTests/svg/filters/display-none-filter-primitive-expected.txt
[add] http://crrev.com/fb79f7fc46552d45127acd2959a23662ad8f271e/third_party/WebKit/LayoutTests/svg/filters/display-none-filter-primitive.html
[modify] http://crrev.com/fb79f7fc46552d45127acd2959a23662ad8f271e/third_party/WebKit/Source/core/svg/graphics/filters/SVGFilterBuilder.cpp


### fs...@opera.com (2015-10-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-13)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5409123905044480

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_syzyasan_chrome
Platform Id: windows

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x055380e7
Crash State:
  WTF::HashTable<blink::IdTargetObserver *,blink::IdTargetObserver *,WTF::Identity
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_syzyasan_chrome&range=353464:353465

Minimized Testcase (9.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97T_woXHfsJnu7cbJ_9AGkQ6uRsnkOGi1ZhK0T7Qz3myeK4VvBeefd0LND9HcY7bykSqFGdMViwQqLbujd3P2eetbSW9JDgWSKAR7x42CywvmFn08h43GZkxY9W38kcHC2TYffuO7VaJB3W88PvTdNYroI8WA

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-10-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-13)

ClusterFuzz has detected this issue as fixed in range 353571:353649.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4572849078009856

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x61200006ac88
Crash State:
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  blink::SVGFilterPainter::prepareEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=353033:353139
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=353571:353649

Minimized Testcase (1.89 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97GoKG955C3fUHodwpkOaHeGwFOZavKnWmSuDX7AttxXD6vqhPZQkT9V_vZZWG0eRHb3EQlACBtGus1SmgTKJe6CLHFzVNK28_8vdyV23waeMsU14HMhMZ6AHin6Ney8TJQmfI42HbsyL4FpGlAM5FeWlc7bg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-10-13)

ClusterFuzz has detected this issue as fixed in range 353571:353648.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5016624761929728

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xb8c24ce4
Crash State:
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  blink::SVGFilterPainter::prepareEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=353013:353144
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=353571:353648

Minimized Testcase (2.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv963d2iMLMXjTFQwZztfztFB_niNlSaYeNsi2p_A-vGVCDENpcG71JY-u3isclhn0OGWmeq6Q6P_zqNsQBfVTLAxt4iow4VR0I6RbOPGlnBIRsfFvITjzAGxUcNTMNwUHP41IiutepMtkcCRqGMzJxZJJnulPg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-10-13)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6197885522149376

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_syzyasan_chrome
Platform Id: windows

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x0572d1af
Crash State:
  WTF::HashTable<blink::ThreadState *,blink::ThreadState *,WTF::IdentityExtractor,
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_syzyasan_chrome&range=353235:353267

Minimized Testcase (1.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94-wPJBNw6mqy1guTGz44XHDT0BlGszEITPDVTUagxEeU4Y5gDS3pqPOx5ucKwnpI8ugOGkAvBV-AAqTd5FVR9ktY-9_k_QSywk_k-3kraM9zF7GskT-PuIi_NxwkTR0Kz57JOttIWkMDDKUmlIVCXWESDDZw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-10-14)

ClusterFuzz has detected this issue as fixed in range 353571:353648.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4547854247395328

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGFilterBuilder::buildGraph
  blink::SVGFilterPainter::prepareEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=353124:353144
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=353571:353648

Minimized Testcase (10.64 Kb): https://cluster-fuzz.appspot.com/download/AMIfv946G06g4NwkC21SMzoQIXKWqgchSYrGo8Co4fGxUgeQUF9ch3Sx_AqGHGBTFiaaldVq4S25QG5pwAAWOyLjY5gRj7JYvMEKCTrxrJDfiDiO20jXGiXCVURMdIVXZ7zA4wcsGZ8x_yfPByAE6lAplrfMfNfs6Q

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2016-01-19)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-30)

Miaubiz - $1,500 here ($1,000 for the report, $500 fuzzer bonus).

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

This issue was migrated from crbug.com/chromium/541593?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/542089]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083011)*
