# **Does this work in other browsers? **  Yes - This is just a Chrome problem

| Field | Value |
|-------|-------|
| **Issue ID** | [40062804](https://issues.chromium.org/issues/40062804) |
| **Status** | Unknown |
| **Severity** | Unknown |
| **Priority** | Unknown |
| **Component** | Unknown |
| **Reporter** | Unknown |
| **Created** | 2023-01-27 |
| **Bounty** | $2,000.00 |

## Description

\*\*Does this work in other browsers? \*\* Yes - This is just a Chrome problem

**Steps to reproduce the problem:**

1. go to <https://jsgist.org/?src=dbb12ec6674cfca052f5040f89c118fe>

**Problem Description:**  

ImageBitmapRenderingContext is typically made in the main page and then some other canvas, like an offscreencanvas, transfers its bitmap to the imagebitmaprenderingcontext. That works but if you instead create the imagebitmaprenderingcontext in the worker it doesn't work. It seems like it should

To try to be more clear

This works

```
+---- Main Page ---------------------+   +---- Worker ----------------------------+  
|                                    |   | const ctx = new Offscreen()            |  
| ibctx = canvas.getContext(         |   |    .getContext('2d');                  |  
|    'bitmaprenderer')               |   | function render() {                    |  
| worker = new Worker(...');         |   |    ...draw...                          |  
| worker.onmessage(e => {            |   |    ib = ctx.canvas.transferToBitmap(); |  
|   ibCtx.tranfserFromBitmap(e.data);|   |    postMessage(ib, [ib]);              |  
| });                                |   |    requestAnimationFrame(render);      |  
|                                    |   | }                                      |  
|                                    |   | requestAnimationFrame(render);         |  
+------------------------------------+   +----------------------------------------+  

```

This does NOT work (but seems like it should)

```
+---- Main Page ---------------------+   +---- Worker ----------------------------+  
|                                    |   | onmessage = (e) => {                   |  
| offscreen = canvas                     |   const canvas = e.data;               |  
|    .transferControlToOffscreen()   |   |   const ibctx = canvas.getContext(     |  
| worker = new Worker(...');         |   |     'bitmaprenderer');                 |  
| worker.postMessage(                |   |   const ctx = new Offscreen()          |  
|   offscreen, [offscreen]           |   |      getContext('2d')                  |  
| });                                |   |   function render() {                  |  
|                                    |   |     ...draw...                         |  
|                                    |   |     ib = ctx.canvas.transferToBitmap();|  
|                                    |   |     ibctx.transferFromBitmap(ib);      |  
|                                    |   |     requestAnimationFrame(render);     |  
|                                    |   |   }                                    |  
|                                    |   |   requestAnimationFrame(render);       |  
|                                    |   | };                                     |  
+------------------------------------+   +----------------------------------------+  

```

**Additional Comments:**  

Works in Firefox  

Safari doesn't implement the needed APIs

\*\*Chrome version: \*\* 109.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [Screen Recording 2023-07-28 at 09.41.00.mp4](attachments/Screen Recording 2023-07-28 at 09.41.00.mp4) (video/mp4, 641.6 KB)

## Timeline

### gm...@greggman.com (2023-01-27)

Actually this works in Safari Technology Preview but not in Safari 16.3

### gm...@chromium.org (2023-01-30)

[Empty comment from Monorail migration]

### gm...@chromium.org (2023-01-30)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-01-30)

[Empty comment from Monorail migration]

### gm...@chromium.org (2023-07-27)

Just pointing out there is garbage on the screen with this path.

### kb...@chromium.org (2023-08-01)

That's concerning. Could someone from the Canvas team please investigate? Marking P1 because garbage should never show up on screen.


### kb...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### gm...@chromium.org (2023-08-01)

video on M1, moving the cursor across the omnibar and toolbar

### ju...@chromium.org (2023-08-01)

Marking as a security bug since this could potentially leak private data.

### ju...@chromium.org (2023-08-01)

Marking security severity as medium for now because exploitability is unknown and probably unreliable.

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### ju...@chromium.org (2023-08-01)

In order to reproduce the bug in a developer build on an M1 MacBook Pro, I had to switch ANGLE to use the OpenGL backend.
It seems the Metal backend completely fixes the issue.

Since this appears to be an issue with the legacy ANGLE backend, I'm passing the bug to Geoff to decide what to do about this.

### ju...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-08-01)

While we're working on shipping ANGLE's Metal backend, the OpenGL backend is still what Chrome Stable is using. There is still at least one serious issue to be resolved, https://crbug.com/chromium/1468346. I think this should be investigated from the ImageBitmapRenderingContext side given that. Were some clears recently removed which might not be redundant on ANGLE's OpenGL backend?


### ju...@chromium.org (2023-08-02)

Okay, I will check whether this can be mitigated on the blink side.  I don't think it's just a missing clear though because the rendered content is completely absent. It looks more like a resource id or mailbox mix-up, or something like that.

### ju...@chromium.org (2023-08-02)

Fix is in the pipe, and it's a good thing we're fixing this on the blink side because it turns out that we were triggering an unnecessary GPU readback.

CL pending review: https://chromium-review.googlesource.com/c/chromium/src/+/4743222

### [Deleted User] (2023-08-17)

junov: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@chromium.org (2023-08-17)

Whoops, I forgot about this CR.  It is now in the CQ.

### gi...@appspot.gserviceaccount.com (2023-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5377c7bd91a3779c52f7dc1814c1f3bb4513cc7b

commit 5377c7bd91a3779c52f7dc1814c1f3bb4513cc7b
Author: Justin Novosad <junov@chromium.org>
Date: Sat Aug 19 07:31:44 2023

Fix ImageBitmapRenderingContext compositing in Workers

When we have an ImageBitmapRenderingContext associated with an
OffscreenCanvas in a worker, with a placeholder on the main thread,
animation frames need to be dispatched to both the main thread and
the compositor. The problem was that the OffscreenCanvas was
setting up a non-GPU-accelerated CanvasResourceProvider in cases where
its context was an ImageBitmapRenderingContext. This was causing
an undesirable GPU readback for the purpose of preparing the GPU
resource to be dispatched to the main thread.  The readback is not
just an issue for performance, it also had the side-effect of
consuming then deleting the mailboxed texture on the worker thread,
when it is intended to be consumed by the compositor. This resulted
in compositing failures due to attempts to access deleted resources.
The fix is to ensure that ImageBitmapRenderingContext always uses
gpu-accelerated resources whenever gpu-accelerated compositing is
enabled.

Bug: 1410696
Change-Id: I22603641e94379e8dcca236a532db1219a007e68
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4743222
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1185510}

[modify] https://crrev.com/5377c7bd91a3779c52f7dc1814c1f3bb4513cc7b/content/test/content_test_bundle_data.filelist
[modify] https://crrev.com/5377c7bd91a3779c52f7dc1814c1f3bb4513cc7b/content/test/gpu/gpu_tests/pixel_test_pages.py
[modify] https://crrev.com/5377c7bd91a3779c52f7dc1814c1f3bb4513cc7b/third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc
[add] https://crrev.com/5377c7bd91a3779c52f7dc1814c1f3bb4513cc7b/content/test/data/gpu/pixel_offscreenCanvas_ibrc_worker.html


### kb...@chromium.org (2023-08-24)

[Empty comment from Monorail migration]

### zi...@chromium.org (2023-08-24)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-08-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-01)

junov: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-10-09)

zmo@ (as the reviewer of the last cl here) kbr@ () the blocker 1475455 is closed - can this bug also be marked as fixed?
if there is more work to be done, might you be able to find a new owner for this bug?

thank you! (:

### is...@google.com (2023-10-09)

This issue was migrated from crbug.com/chromium/1410696?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1475455]
[Monorail components added to Component Tags custom field.]

### ar...@chromium.org (2024-03-11)

**[secondary security shepherd]**

This hasn't been updated in 153 days. I am looking what are the next step for this "vulnerability".

@zmo => See comment 24. Can close this?

### pe...@google.com (2024-10-26)

zmo: Uh oh! This issue still open and hasn't been updated in the last 382 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

zmo: Uh oh! This issue still open and hasn't been updated in the last 397 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ar...@chromium.org (2024-12-13)

**[secondary security shepherd]**

@zmo => See [comment #24](https://issues.chromium.org/issues/40062804#comment24) and [comment #25](https://issues.chromium.org/issues/40062804#comment25). Can close this?

(I am going to ping on chat)

### ch...@google.com (2026-01-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### aj...@chromium.org (2026-03-12)

Reporter has alerted us that they are not eligible for rewards at this time.

### ch...@google.com (2026-05-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. User information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062804)*
