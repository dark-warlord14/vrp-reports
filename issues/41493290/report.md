# Security: UAF IN BaseRenderingContext2D::ResetInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [41493290](https://issues.chromium.org/issues/41493290) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Canvas |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2024-01-21 |
| **Bounty** | $4,000.00 |

## Description


##Reproduce
The issue was found by code review, and I will provide a POC later.

##RCA
Similar to the issue(1511567) I previously reported.

1. ResetInternal calls GetPaintCanvas to get the PaintCanvas object pointer c[1], which is valid at this time. 
2. Then WillDraw[2] is called, and WillDraw will call CheckForGpuContextLost, which may cause the "canvas resource provider" to be destroyed.
3. Ultimately, c->drawRect()[3] uses the PaintCanvas object pointer c obtained in step 1, resulting in an UAF.

```
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc;drc=3cc22c22d7637bc5604e8fef3b0882b51a762901;l=437
void BaseRenderingContext2D::ResetInternal() {
  if (UNLIKELY(identifiability_study_helper_.ShouldUpdateBuilder())) {
    identifiability_study_helper_.UpdateBuilder(CanvasOps::kReset);
  }
  ValidateStateStack();
  state_stack_.resize(1);
  state_stack_.front() = MakeGarbageCollected<CanvasRenderingContext2DState>();
  layer_count_ = 0;
  SetIsTransformInvertible(true);
  CanvasPath::Clear();
  RestartRecording();

  // Clear the frame in case a flush previously drew to the canvas surface.
  if (cc::PaintCanvas* c = GetPaintCanvas()) {                                      << [1]
    int width = Width();  // Keeping results to avoid repetitive virtual calls.
    int height = Height();
    WillDraw(SkIRect::MakeXYWH(0, 0, width, height),                                << [2]
             CanvasPerformanceMonitor::DrawType::kOther);
    c->drawRect(SkRect::MakeXYWH(0.0f, 0.0f, width, height), GetClearFlags());      << [3]
  }

  ValidateStateStack();
  origin_tainted_by_content_ = false;
}

//CALL HIERARCHY
third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc (1 result)
    590: CheckForGpuContextLost() {... ResourceProvider()->IsGpuContextLost()) { ...}
        third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc (1 result)
            193: GetOrCreateCanvasResourceProvider() {... host->CheckForGpuContextLost(); ...}
                third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc (9 results)
                155: FinalizeFrame( reason) {... if (!GetOrCreateCanvasResourceProvider()) ...}
                    third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc (4 results)
                        231: PushFrame() {... FinalizeFrame(FlushReason::kOffscreenCanvasPushFrame); ...}
                            third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc (1 result)
                                536: PushFrameIfNeeded() {... return context_->PushFrame(); ...}
                                    third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc (1 result)
                                        536: PushFrameIfNeeded() {... return context_->PushFrame(); ...}
                                        third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc (1 result, 18 displayed)
                                            521: BeginFrame() {... return PushFrameIfNeeded(); ...}
                                            third_party/blink/renderer/platform/graphics/canvas_resource_dispatcher.cc (2 results, 18 displayed)
                                                344: SetNeedsBeginFrame( needs_begin_frame) {... Client()->BeginFrame(); ...}
                                                    third_party/blink/renderer/core/html/canvas/html_canvas_element.cc (1 result)
                                                    third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc (2 results, 4 displayed)
                                                        514: DidDraw(const rect) {... GetOrCreateResourceDispatcher()->SetNeedsBeginFrame(true); ...}
                                                            third_party/blink/renderer/core/html/canvas/canvas_rendering_context.cc (1 result)
                                                            third_party/blink/renderer/core/html/canvas/canvas_rendering_context_host.h (1 result)
                                                            third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc (1 result)
                                                                333: WillDraw(const dirty_rect, draw_type) {... Host()->DidDraw(dirty_rect_for_commit_); ...}
                                                                    third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc (5 results)
                                                                        453: ResetInternal() {... WillDraw(SkIRect::MakeXYWH(0, 0, width, height), ...}

```

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 7.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 380 B)
- [rep.patch.diff](attachments/rep.patch.diff) (text/plain, 6.9 KB)

## Timeline

### [Deleted User] (2024-01-21)

[Empty comment from Monorail migration]

### m....@gmail.com (2024-01-23)

To reproduce the issue, I modified the code to simulate the situation where the GPU is invalid when calling the blink::BaseRenderingContext2D::ResetInternal
Reproduction steps:
1. apply rep.patch.diff and compile chromium
2. chrome --no-sandbox --user-data-dir=test --enable-logging=stderr poc.html

### ke...@chromium.org (2024-01-23)

Thanks for the report and the repro.

This would require the GPU to crash with a certain precision of timing, so this might be difficult to exploit in practice, but it is valid. Assigning Severity-Medium on that basis.

jpgravel@: Can you PTAL?

[Monorail components: Blink>Canvas]

### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-24)

[Empty comment from Monorail migration]

### m....@gmail.com (2024-01-25)

Bisect:
https://chromium-review.googlesource.com/c/chromium/src/+/4953275

Canary 122 122.0.6186.0
Dev 122 122.0.6226.2
Beta 122 122.0.6261.6

### jp...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### jp...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### an...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### jp...@chromium.org (2024-01-26)

This bug has the same root-cause as https://crbug.com/1511567, they were both caused by https://crrev.com/c/4982911 which first landed in M121. Updating the FoundIn label accordingly.

### [Deleted User] (2024-01-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/812dd783e5e140e555b6a8b8b31cdb8bdcd8988d

commit 812dd783e5e140e555b6a8b8b31cdb8bdcd8988d
Author: Andres Ricardo Perez <andresrperez@chromium.org>
Date: Fri Jan 26 18:49:48 2024

Remove destruction of the resource provider in CheckForGpuContextLost

When `CheckForGpuContextLost` is called, if it is detected that the GPU
process has crashed, the resource provider is destroyed. This seems to
be causing use-after-free issues since `CheckForGpuContextLost` is
called from `GetOrCreateResourceProvider`, resulting in unexpected uses
of a now null resource provider.

Since `CheckForGpuContextLost` also sets a flag to indicate that the
context has been lost and should be recovered, it is not necessary to
set the resource provider to nullptr at this point. Therefore, the
destruction of the resource provider has been removed.

Fixed: 1520316
Change-Id: I7c2659e874284223622753fe2b4a39806362bfb2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5238385
Commit-Queue: Andres Ricardo Perez Rojas <andresrperez@chromium.org>
Reviewed-by: Jean-Philippe Gravel <jpgravel@chromium.org>
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1252769}

[modify] https://crrev.com/812dd783e5e140e555b6a8b8b31cdb8bdcd8988d/third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc


### [Deleted User] (2024-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations! The Chrome VRP Panel has decided to award you $3,000 for this report of a mildly mitigated security bug in the renderer, mitigated by race condition and precondition to crash the GPU process, + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1520316?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-05-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493290)*
