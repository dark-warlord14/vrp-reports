# Security: heap-use-after-free in Blink

| Field | Value |
|-------|-------|
| **Issue ID** | [40055132](https://issues.chromium.org/issues/40055132) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | li...@gmail.com |
| **Assignee** | yi...@chromium.org |
| **Created** | 2021-03-10 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

UAF bug in blink, it affects chromium from version 85 to 89.  

The problem is:  

On CanvasRenderingContext2D constuctor, which hold a raw pointer ukm\_recorder\_ which will be freed on the Document destruct.  

<https://source.chromium.org/chromium/chromium/src/+/refs/tags/89.0.4389.88:third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc;l=155>

<https://source.chromium.org/chromium/chromium/src/+/refs/tags/89.0.4389.88:third_party/blink/renderer/core/dom/document.h;l=2081>;

```
#0 0x555fc9a02dbd in operator delete(void\*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3  
#1 0x555fe0ea44ae in std::__1::default_delete<ukm::UkmRecorder>::operator()(ukm::UkmRecorder\*) const buildtools/third_party/libc++/trunk/include/memory:2378:5  
#2 0x555fe0ea44ae in std::__1::unique_ptr<ukm::UkmRecorder, std::__1::default_delete<ukm::UkmRecorder> >::reset(ukm::UkmRecorder\*) buildtools/third_party/libc++/trunk/include/memory:2633:7  
#3 0x555fe0ea44ae in std::__1::unique_ptr<ukm::UkmRecorder, std::__1::default_delete<ukm::UkmRecorder> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19  
#4 0x555fe0ea44ae in blink::Document::~Document() third_party/blink/renderer/core/dom/document.cc:908:1  
#5 0x555fd3e35a9f in blink::HeapObjectHeader::Finalize(unsigned char\*, unsigned long) third_party/blink/renderer/platform/heap/impl/heap_page.cc:95:5  

```

After document is free, CanvasRenderingContext2D object will hold a wild pointer(ukm\_recorder\_) which can be call from getImageInternal.

<https://source.chromium.org/chromium/chromium/src/+/refs/tags/85.0.4183.99:third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc;l=688>

In master branch and version 90, the call of ukm\_recorder\_ is removed, but CanvasRenderingContext2D object still hold the pointer ukm\_recorder\_.  

<https://github.com/chromium/chromium/commit/809231f0c9fdc6180b6a99cf067d0a32db053034>

By Search the sources, ukm\_recoder\_ not only hold by CanvasRenderingContext2D, but also any other objects. So problems will not only here:  

<https://source.chromium.org/chromium/chromium/src/+/refs/tags/89.0.4389.88:third_party/blink/renderer/core/loader/interactive_detector.cc;l=79>;

**VERSION**  

Chrome Version: 89.0.4389.86 + stable  

Operating System: Ubuntu

**REPRODUCTION CASE**  

browse the attached file: uaf.html

**CREDIT INFORMATION**  

Reporter credit: Liang Dong

## Attachments

- [asan](attachments/asan) (text/plain, 26.0 KB)
- [asan2](attachments/asan2) (text/plain, 40.5 KB)
- [uaf.html](attachments/uaf.html) (text/plain, 810 B)

## Timeline

### [Deleted User] (2021-03-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-03-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5769050916192256.

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-03-11)

CF couldn't repro this issue.

aaronhk: Could you PTAL? (though I'm not sure if this is particularly canvas related)

[Monorail components: Blink Blink>Canvas]

### ch...@chromium.org (2021-03-13)

[Empty comment from Monorail migration]

[Monorail components: -Blink]

### me...@chromium.org (2021-03-14)

Assigning tentative labels.

### [Deleted User] (2021-03-15)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@chromium.org (2021-03-17)

[Empty comment from Monorail migration]

### aa...@chromium.org (2021-03-17)

Throwing this to canvas bug rotation.

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### yi...@chromium.org (2021-03-19)

Thank you so much for such a detailed report! You have a a really nice analysis!

I think the reason we can no longer reproduce it is because this memory violation has already been fixed. 

The link you share for getImageData is from M85 (https://source.chromium.org/chromium/chromium/src/+/refs/tags/85.0.4183.99:third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc;l=688) 

The new version is here:  https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc;l=691;bpv=1;bpt=1 

I also checked the other violation you pointed to in interactive_detector.cc, that one is also fixed. 

I believe someone else reported it as it's impact many places and it's fixed with a different cl. 







### yi...@chromium.org (2021-03-19)

I did some quick search. I think this is the fix https://chromium-review.googlesource.com/c/chromium/src/+/2600386

### yi...@chromium.org (2021-03-19)

I can also confirm that I can reproduce the issue without that patch! 

I try to merge that patch to earlier chrome version

### yi...@chromium.org (2021-03-19)

[Empty comment from Monorail migration]

### yi...@chromium.org (2021-03-19)

[Empty comment from Monorail migration]

### yi...@chromium.org (2021-03-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-19)

[Empty comment from Monorail migration]

### yi...@chromium.org (2021-03-19)

Since the fix is landed in Jan 26 before the feature freeze for M90 (feb 12), the reported issue is fixed for all chrome version >= M90.

Check if it is possible to merge to M89.

### [Deleted User] (2021-03-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-22)

yiyix@, would it be possible for you to remove the CanvasRenderingContext2D::ukm_recorder_ member entirely? To make sure other code doesn't come along and use it in future by accident, given that there's this known risk of UaF here in the face of future code changes?

Meanwhile the UaF was fixed in https://crbug.com/chromium/1161379. I'm going to turn *that* into a security bug and request merge back to M89.


### ad...@google.com (2021-03-22)

[Empty comment from Monorail migration]

### yi...@chromium.org (2021-03-24)

Totally agree, I already created a cl to do that: https://chromium-review.googlesource.com/c/chromium/src/+/2774667
Fixing the failed bot now.... once fixed, will land it.

### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-24)

Congratulations, Liang Dong! The VRP Panel has decided to award you $7500 for this report. Excellent work!

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### yi...@chromium.org (2021-03-30)

cl is Landed: https://chromium-review.googlesource.com/c/chromium/src/+/2774667

### gi...@appspot.gserviceaccount.com (2021-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5745eaf16077dc12b31252ab1904f2e1f6344e2d

commit 5745eaf16077dc12b31252ab1904f2e1f6344e2d
Author: Asanka Herath <asanka@chromium.org>
Date: Wed Mar 31 16:33:46 2021

[privacy_budget] Remove unnecessary kCanvasReadback metrics.

The identifiability metrics recorded under kCanvasReadback surface type
used two conflicting sources as inputs: the CanvasRenderingContext
type, and the paint-op digest.

There are known collisions between resulting IdentifiableSurface values
from the two sources, which makes it impossible to losslessly separate
the two during analysis.

While the fact that a canvas readback happened is interesting, it
doesn't help determine the observed diversity of clients. Hence this
change removes one of those sources: the CanvasRenderingContext type.

M86 merge conflicts and resolution:
* third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc
  M86 does not have the code removed in original CL.
* third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc
  third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc
  Removed corresponding code, kept old API.

(cherry picked from commit 809231f0c9fdc6180b6a99cf067d0a32db053034)

(cherry picked from commit b206b57b96985713ad167738f6839a8d32db78f2)

Bug: 1161379, 1186641
Change-Id: I770cb631c9c4afe4c36d1b129aaf61410db25d43
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2600386
Commit-Queue: Asanka Herath <asanka@chromium.org>
Reviewed-by: Caleb Raitto <caraitto@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#847480}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2785145
Reviewed-by: Justin Novosad <junov@chromium.org>
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Reviewed-by: Asanka Herath <asanka@chromium.org>
Commit-Queue: Yi Xu <yiyix@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4389@{#1599}
Cr-Original-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2794506
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Auto-Submit: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1586}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/5745eaf16077dc12b31252ab1904f2e1f6344e2d/third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc
[modify] https://crrev.com/5745eaf16077dc12b31252ab1904f2e1f6344e2d/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### [Deleted User] (2021-07-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-07-14)

Hello, liangdong- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1186641?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055132)*
