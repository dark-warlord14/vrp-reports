# Heap-buffer-overflow in WebCore::SVGAnimatedPointListAnimator::calculateAnimatedValue

| Field | Value |
|-------|-------|
| **Issue ID** | [40057584](https://issues.chromium.org/issues/40057584) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | at...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2012-05-02 |
| **Bounty** | $500.00 |

## Description

Repro-file as attachment.

Chrome Version: ASAN Chromium 20.0.1125.0
Operating System: Ubuntu 11.04

ASAN report:

=================================================================
==453== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f09346d0b00 at pc 0x7f094a61a721 bp 0x7fff582ab430 sp 0x7fff582ab428
READ of size 4 at 0x7f09346d0b00 thread T0
    #0 0x7f094a61a721 in WebCore::SVGAnimatedPointListAnimator::calculateAnimatedValue(float, unsigned int, WebCore::SVGAnimatedType*, WebCore::SVGAnimatedType*, WebCore::SVGAnimatedType*, WebCore::SVGAnimatedType*) ???:0
    #1 0x7f094a358796 in WebCore::SVGAnimateElement::calculateAnimatedValue(float, unsigned int, WTF::String const&, WebCore::SVGSMILElement*) ???:0
    #2 0x7f094a36d09d in WebCore::SVGAnimationElement::updateAnimation(float, unsigned int, WebCore::SVGSMILElement*) ???:0
    #3 0x7f094a5a485e in WebCore::SVGSMILElement::progress(WebCore::SMILTime, WebCore::SVGSMILElement*) ???:0
    #4 0x7f094a58bb35 in WebCore::SMILTimeContainer::updateAnimations(WebCore::SMILTime) ???:0
    #5 0x7f094a58b04a in WebCore::SMILTimeContainer::begin() ???:0
    #6 0x7f094a389bc4 in WebCore::SVGDocumentExtensions::startAnimations() ???:0
    #7 0x7f0947dc62ff in WebCore::Document::implicitClose() ???:0
    #8 0x7f09490391b7 in WebCore::FrameLoader::checkCompleted() ???:0
    #9 0x7f09490358c4 in WebCore::FrameLoader::finishedParsing() ???:0
    #10 0x7f0947de6cd2 in WebCore::Document::finishedParsing() ???:0
    .
    .
    .
0x7f09346d0b00 is located 0 bytes to the right of 128-byte region [0x7f09346d0a80,0x7f09346d0b00)
allocated by thread T0 here:
    #0 0x7f094cc3e122 in malloc ??:0
    #1 0x7f0947f4413b in WTF::fastMalloc(unsigned long) ???:0
    #2 0x7f09487b0fa6 in WTF::Vector<WebCore::FloatPoint, 0ul>::reserveCapacity(unsigned long) ???:0
    #3 0x7f094a4bc812 in WebCore::pointsListFromSVGData(WebCore::SVGPointList&, WTF::String const&) ???:0
    #4 0x7f094a619475 in WebCore::SVGAnimatedPointListAnimator::constructFromString(WTF::String const&) ???:0
    #5 0x7f094a35869d in WebCore::SVGAnimateElement::calculateAnimatedValue(float, unsigned int, WTF::String const&, WebCore::SVGSMILElement*) ???:0
    #6 0x7f094a36d09d in WebCore::SVGAnimationElement::updateAnimation(float, unsigned int, WebCore::SVGSMILElement*) ???:0
    #7 0x7f094a5a485e in WebCore::SVGSMILElement::progress(WebCore::SMILTime, WebCore::SVGSMILElement*) ???:0
    #8 0x7f094a58bb35 in WebCore::SMILTimeContainer::updateAnimations(WebCore::SMILTime) ???:0
    #9 0x7f094a58b04a in WebCore::SMILTimeContainer::begin() ???:0
    #10 0x7f094a389bc4 in WebCore::SVGDocumentExtensions::startAnimations() ???:0
    .
    .
    .
==453== ABORTING
Stats: 4M malloced (7M for red zones) by 21337 calls
Stats: 0M realloced by 37 calls
Stats: 3M freed by 10309 calls
Stats: 0M really freed by 0 calls
Stats: 44M (11270 full pages) mmaped in 11 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32;
  mallocs by size class: 8:18284; 9:1222; 10:1494; 11:174; 12:53; 13:26; 14:18; 15:6; 16:59; 17:1;
  frees   by size class: 8:8077; 9:723; 10:1345; 11:59; 12:25; 13:15; 14:9; 15:3; 16:53;
  rfrees  by size class:
Stats: malloc large: 1 small slow: 106
Shadow byte and word:
  0x1fe1268da160: fa
  0x1fe1268da160: fa fa fa fa fa fa fa fa
More shadow bytes:
  0x1fe1268da140: fa fa fa fa fa fa fa fa
  0x1fe1268da148: fa fa fa fa fa fa fa fa
  0x1fe1268da150: 00 00 00 00 00 00 00 00
  0x1fe1268da158: 00 00 00 00 00 00 00 00
=>0x1fe1268da160: fa fa fa fa fa fa fa fa
  0x1fe1268da168: fa fa fa fa fa fa fa fa
  0x1fe1268da170: fd fd fd fd fd fd fd fd
  0x1fe1268da178: fd fd fd fd fd fd fd fd
  0x1fe1268da180: fa fa fa fa fa fa fa fa






## Attachments

- [cnode0004-heap-buffer-overflow-511-min.svg](attachments/cnode0004-heap-buffer-overflow-511-min.svg) (text/plain; charset=us-ascii, 469 B)

## Timeline

### in...@chromium.org (2012-05-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-02)

[Comment Deleted]

### in...@chromium.org (2012-05-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=42345140

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7f61f5d0f300
Crash State:
  - crash stack -
  WebCore::SVGAnimatedPointListAnimator::calculateAnimatedValue
  WebCore::SVGAnimateElement::calculateAnimatedValue
  WebCore::SVGAnimationElement::updateAnimation
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=134714:134735

Minimized Testcase (0.30 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97VMxXGVYdksie15BlSAbGKUSTpJpePmH85ZJYZCuIdglhXnKH6LjwFk40jk5zBI7sU1vWQsYxnYIpIUuQ-MpGaUTskfJvjG92Qj3PhM_2c6Y6ymN2QN4ZkUO0M27D3S4zXdvZt6D1JJ8etyiKuLxjadpZiGg
<svg xmlns="http://www.w3.org/2000/svg">

 
 <polygon>
    <animate values="
     ;  
     1,1 1,1 1,1 1,1 1,1             
     1,1 1,1 1,1 1,1 1,1              
     1,1 1,1 1,1 1,1 1,1             
     1,1 1,1 1,1 1,1 1,1 
     ;             
     1,1 1,1 1,1 1,1 1,1
     " 
     attributeName="points">

### in...@chromium.org (2012-05-02)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=85382

### dh...@google.com (2012-05-08)

M20 has sailed. If this need to be part of M20, put them back with appropriate release blocker label.

### in...@chromium.org (2012-05-08)

Security bugs don't get moved to next milestone. Please do not update milestone on security bugs.

### in...@chromium.org (2012-05-08)

http://trac.webkit.org/changeset/116458

### cl...@chromium.org (2012-05-09)

ClusterFuzz has detected this issue as fixed in range 135985:135992.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=42345140

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7f61f5d0f300
Crash State:
  - crash stack -
  WebCore::SVGAnimatedPointListAnimator::calculateAnimatedValue
  WebCore::SVGAnimateElement::calculateAnimatedValue
  WebCore::SVGAnimationElement::updateAnimation
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=134714:134735
Fixed: https://cluster-fuzz.appspot.com/revisions?range=135985:135992

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97VMxXGVYdksie15BlSAbGKUSTpJpePmH85ZJYZCuIdglhXnKH6LjwFk40jk5zBI7sU1vWQsYxnYIpIUuQ-MpGaUTskfJvjG92Qj3PhM_2c6Y6ymN2QN4ZkUO0M27D3S4zXdvZt6D1JJ8etyiKuLxjadpZiGg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-05-24)

M20: http://trac.webkit.org/changeset/118295

### sc...@gmail.com (2012-06-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-06-22)

OOB read, recovery likely. $500

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/125919?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057584)*
