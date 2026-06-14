# Heap-buffer-overflow in SkOpSegment::blindCoincident

| Field | Value |
|-------|-------|
| **Issue ID** | [40080620](https://issues.chromium.org/issues/40080620) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | fm...@chromium.org |
| **Created** | 2014-10-10 |
| **Bounty** | $1,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 40.0.2184.0 (Developer Build) 

ASAN-trace:

==10714==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61500003b138 at pc 0x7fe2492c2eec bp 0x7fff49846bc0 sp 0x7fff49846bb8
READ of size 8 at 0x61500003b138 thread T0 (chrome)
    #0 0x7fe2492c2eeb in SkOpSegment::blindCoincident(SkCoincidence const&, SkOpSegment*) ??:0:0
    #1 0x7fe2492b32d1 in SkOpContour::resolveNearCoincidence() ??:0:0
    #2 0x7fe24928b195 in CoincidenceCheck(SkTArray<SkOpContour*, true>*, int) ??:0:0
    #3 0x7fe2492d996c in HandleCoincidence(SkTArray<SkOpContour*, true>*, int) ??:0:0
    #4 0x7fe2491098f2 in Op(SkPath const&, SkPath const&, SkPathOp, SkPath*) ??:0:0
    #5 0x7fe24c146a28 in blink::RenderSVGResourceClipper::tryPathOnlyClipping(blink::GraphicsContext*, blink::AffineTransform const&, blink::FloatRect const&) ??:0:0
    #6 0x7fe24c1462a6 in blink::RenderSVGResourceClipper::applyClippingToContext(blink::RenderObject*, blink::FloatRect const&, blink::FloatRect const&, blink::GraphicsContext*, blink::RenderSVGResourceClipper::ClipperState&) ??:0:0
.
.
.
0x61500003b138 is located 72 bytes to the left of 480-byte region [0x61500003b180,0x61500003b360)
allocated by thread T0 (chrome) here:
    #0 0x7fe24720bdbe in __interceptor_realloc ??:0:0
    #1 0x7fe2494d02c1 in sk_realloc_throw(void*, unsigned long) ??:0:0
    #2 0x7fe2492d4c0b in SkTDArray<SkOpSpan>::resizeStorageToAtLeast(int) ??:0:0
    #3 0x7fe2492d4b3b in SkTDArray<SkOpSpan>::setCount(int) ??:0:0
    #4 0x7fe2492d49f5 in SkTDArray<SkOpSpan>::append(int, SkOpSpan const*) ??:0:0
    #5 0x7fe2492bea8c in SkOpSegment::addT(SkOpSegment*, SkPoint const&, double) ??:0:0
    #6 0x7fe249287a52 in AddIntersectTs(SkOpContour*, SkOpContour*) ??:0:0
.
.
.

## Attachments

- [chrome-heap-buffer-overflow-SkOpSegmentblindCoincident8.svg](attachments/chrome-heap-buffer-overflow-SkOpSegmentblindCoincident8.svg) (image/svg+xml, 529 B)

## Timeline

### cl...@chromium.org (2014-10-10)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4798377094021120

### mb...@chromium.org (2014-10-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-10)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4798377094021120

Uploader: mbarbella@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x615000012738
Crash State:
  SkOpSegment::blindCoincident
  SkOpContour::resolveNearCoincidence
  CoincidenceCheck
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=287661:287842

Minimized Testcase (0.41 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97-JDIpCy__xqrtoJaSY1tjTiLpKqyGXHHjNV5QaWco6xEgJso8G9XRw8fqtf7o5VUTWJ8j4k-XWbQGWVQkSFkGSre1tPo5Nf0V8JzY_P1urHrB46ANPzNnPvt7M6YJN3Z5fuyvKCLBiOULGY9Rbhtovnfcqg
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
    <path id="star" d="m 100,0 60,170 -160,-110 200,0 -170,110 z" transform="translate(40,40)"/>
    <clipPath id="clip">
        <use xlink:href="#star"/>
        <use xlink:href="#star" transform="translate(444444440,40)"/>
    </clipPath>
</defs>

<rect height="300" width="300" style="fill:green;clip-path:url(#clip);"/>




### cl...@chromium.org (2014-10-11)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-10-12)

reed: Could you help find an owner for this one?

### mb...@chromium.org (2014-10-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-10-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-17)

ClusterFuzz has detected this issue as fixed in range 300119:300141.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4798377094021120

Uploader: mbarbella@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x615000012738
Crash State:
  SkOpSegment::blindCoincident
  SkOpContour::resolveNearCoincidence
  CoincidenceCheck
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=287661:287842
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=300119:300141

Minimized Testcase (0.41 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97-JDIpCy__xqrtoJaSY1tjTiLpKqyGXHHjNV5QaWco6xEgJso8G9XRw8fqtf7o5VUTWJ8j4k-XWbQGWVQkSFkGSre1tPo5Nf0V8JzY_P1urHrB46ANPzNnPvt7M6YJN3Z5fuyvKCLBiOULGY9Rbhtovnfcqg
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
    <path id="star" d="m 100,0 60,170 -160,-110 200,0 -170,110 z" transform="translate(40,40)"/>
    <clipPath id="clip">
        <use xlink:href="#star"/>
        <use xlink:href="#star" transform="translate(444444440,40)"/>
    </clipPath>
</defs>

<rect height="300" width="300" style="fill:green;clip-path:url(#clip);"/>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-10-19)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-26)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-03)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-10)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-18)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-25)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-03)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-10)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-17)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-12-18)

this looks fixed after revert in https://chromium.googlesource.com/chromium/blink/+/55f7e5d4da95b0d89c4e1030396ffbb49e0c68b8%5E%21/#F0

fmalita@, if you plan to reenable, please fix the bug.

### cl...@chromium.org (2014-12-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

ClusterFuzz has detected this issue as fixed in range 300119:300141.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4798377094021120

Uploader: mbarbella@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x615000012738
Crash State:
  SkOpSegment::blindCoincident
  SkOpContour::resolveNearCoincidence
  CoincidenceCheck
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=287661:287842
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=300119:300141

Minimized Testcase (0.41 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97-JDIpCy__xqrtoJaSY1tjTiLpKqyGXHHjNV5QaWco6xEgJso8G9XRw8fqtf7o5VUTWJ8j4k-XWbQGWVQkSFkGSre1tPo5Nf0V8JzY_P1urHrB46ANPzNnPvt7M6YJN3Z5fuyvKCLBiOULGY9Rbhtovnfcqg
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
    <path id="star" d="m 100,0 60,170 -160,-110 200,0 -170,110 z" transform="translate(40,40)"/>
    <clipPath id="clip">
        <use xlink:href="#star"/>
        <use xlink:href="#star" transform="translate(444444440,40)"/>
    </clipPath>
</defs>

<rect height="300" width="300" style="fill:green;clip-path:url(#clip);"/>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-23)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### [Deleted User] (2014-12-29)

Per https://crbug.com/chromium/422492#c20, approving revert.

### fm...@chromium.org (2014-12-29)

AFAICT the revert (183894) is already in M40 (base_webkit: 184994).

### in...@chromium.org (2014-12-29)

[Empty comment from Monorail migration]

### aa...@google.com (2014-12-31)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

$1000 here. Panel notes: "unclear if this OOB read is a pointer or not. $500 for bug,  +$500 ClusterFuzz bonus".

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-27)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/422492?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080620)*
