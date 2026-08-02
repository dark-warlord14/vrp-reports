# CanvasRenderingContext2D::drawFocusIfNeeded dangling `Path` use-after-free

| Field | Value |
|-------|-------|
| **Issue ID** | [501646327](https://issues.chromium.org/issues/501646327) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qw...@gmail.com |
| **Assignee** | fm...@chromium.org |
| **Created** | 2026-04-11 |
| **Bounty** | $7,000.00 |

## Description

---

### Report description

CanvasRenderingContext2D::drawFocusIfNeeded dangling `Path` use-after-free

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src>

---

### The problem

#### Please describe the technical details of the vulnerability

## The problem

### Summary

`CanvasRenderingContext2D::drawFocusIfNeeded(Element*)` passes the current canvas path into `DrawFocusIfNeededInternal()` by `const Path&`. If `DrawFocusRing()` loses the 2D context because the canvas size is invalid, the cached current path is destroyed before `DrawFocusIfNeededInternal()` returns. The same stale reference is then used by `UpdateElementAccessibility(path, element)`.

In the tested trigger, the freed object is the `SkPathData` behind the cached current path. The ASAN report shows the first invalid access as `WRITE of size 4` to the freed region.

### Chrome Version

The crash was reproduced on a downloadable Chromium 149 ASAN build on Linux x86\_64. The downloaded ASAN package was requested with `--version 149.0.7779.3`, and the extracted browser used for the run reported `Chromium 149.0.7779.0`. I also checked the corresponding Chromium 149 source tree, including Skia, to verify the code path shown below.

### Root Cause

The vulnerable path starts here in `third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc`:

```
void CanvasRenderingContext2D::drawFocusIfNeeded(Element* element) {
  DrawFocusIfNeededInternal(GetPath(), element);
}

void CanvasRenderingContext2D::DrawFocusIfNeededInternal(const Path& path,
                                                         Element* element) {
  if (!FocusRingCallIsValid(path, element))
    return;

  if (element->GetDocument().FocusedElement() == element) {
    ScrollPathIntoViewInternal(path);
    DrawFocusRing(path, element);
  }

  UpdateElementAccessibility(path, element);
}

```

`GetPath()` returns a reference backed by `PathBuilder::CurrentPath()`. The cached object is stored in `mutable std::optional<Path> current_path_`.

The same call then reaches the context-loss path:

```
void CanvasRenderingContext2D::DrawFocusRing(const Path& path,
                                             Element* element) {
  if (!GetOrCreatePaintCanvas())
    return;

  ...
}

CanvasResourceProvider*
CanvasRenderingContext2D::GetOrCreateResourceProvider() {
  ...

  if (!canvas()->IsValidImageSize()) {
    did_fail_to_create_resource_provider_ = true;
    if (!canvas()->Size().IsEmpty()) {
      LoseContext(CanvasRenderingContext::kInvalidCanvasSize);
    }
    return nullptr;
  }

  ...
}

```

`LoseContext()` clears the cached path through the normal reset path:

```
void CanvasRenderingContext2D::LoseContext(LostContextMode lost_mode) {
  if (context_lost_mode_ != kNotLostContext)
    return;
  context_lost_mode_ = lost_mode;
  ResetInternal();
  ...
}

```
```
void Canvas2DRecorderContext::ResetInternal() {
  ...
  CanvasPath::Clear();
  ...
}

void Clear() {
  line_builder_.Clear();
  arc_builder_.Clear();
  path_builder_.Reset();
}

void PathBuilder::ClearCachedData() {
  current_path_.reset();
  current_bounds_.reset();
}

```

Execution then continues in the same stack frame and reuses the stale reference:

```
void CanvasRenderingContext2D::UpdateElementAccessibility(const Path& path,
                                                          Element* element) {
  ...
  AXObjectCache* ax_object_cache =
      element->GetDocument().ExistingAXObjectCache();
  if (!ax_object_cache) {
    return;
  }
  ax_object_cache->UpdateAXForAllDocuments();

  const AffineTransform& transform = GetState().GetTransform();
  const Path transformed_path =
      transform.IsIdentity()
          ? path
          : PathBuilder(path).Transform(transform).Finalize();

  PhysicalRect element_rect =
      PhysicalRect::EnclosingRect(transformed_path.BoundingRect());
  ...
}

```

In the attached PoC, `transform.IsIdentity()` is true. The dangling `path` is copied into `transformed_path`, `BoundingRect()` is called, and the temporary is then destroyed. The observed ASAN `WRITE of size 4` matches the `sk_sp<SkPathData>` copy path incrementing the freed reference count.

### Trigger Sequence

The trigger uses only standard web APIs.

1. Create a `<canvas>` and get a 2D rendering context.
2. Resize the canvas to `20000 x 20000`.
3. Build a non-empty current path with `beginPath()` and `rect()`.
4. Focus a descendant fallback element inside the canvas.
5. Call `ctx.drawFocusIfNeeded(btn)`.

The trigger does not call drawing or transform APIs after the resize. Calls such as `fillRect()`, `stroke()`, `isPointInPath()`, `scale()`, `rotate()`, or `setTransform()` would reach `GetOrCreatePaintCanvas()` before `drawFocusIfNeeded()` and would lose the context too early.

### Reproduction

#### Test Builds

The following public builds were used for this report.

1. ASAN build used for the crash reproduction:

```
Downloaded with get_asan_chrome.py --version 149.0.7779.3
Executed browser version: Chromium 149.0.7779.0
Linux x86_64

```

2. Release build used as a public Chrome 149 reference binary:

```
Google Chrome for Testing 149.0.7784.0, Linux x86_64

```
#### How the test environment was prepared

The ASAN build can be downloaded with Chromium's helper script:

```
python3 chromium-149/tools/get_asan_chrome/get_asan_chrome.py \
  --version 149.0.7779.3 \
  --os linux \
  --download_directory /home/qwerty/chrome-agent/chromium-149.0.7779.3-linux-asan-download

```

For the runs in this report, the extracted browser was stored at:

```
/home/qwerty/chrome-agent/chromium-149.0.7779.3-linux-asan/chrome

```

The public release build can be downloaded from Chrome for Testing:

```
wget https://storage.googleapis.com/chrome-for-testing-public/149.0.7784.0/linux64/chrome-linux64.zip
unzip chrome-linux64.zip

```

For the runs in this report, the release browser was stored at:

```
/home/qwerty/chrome-agent/chrome-linux64/chrome

```

The source tree used for code verification was a local Chromium 149 checkout. The Skia submodule was initialized with:

```
git -C chromium-149 submodule update --init --depth=1 third_party/skia

```

The trigger itself uses only the attached files. No external media files or additional test corpus are required.

#### How to Run

Place the attached files in one directory and start the ASAN run script with the downloaded browser path:

```
cd pocs/AUD-BLINK_MODULES-130ee005
./run.sh /home/qwerty/chrome-agent/chromium-149.0.7779.3-linux-asan/chrome

```

The `--force-renderer-accessibility` flag is required because `UpdateElementAccessibility()` returns early if `ExistingAXObjectCache()` is null.

The second attached trigger runs the same code with ASAN quarantine disabled:

```
cd pocs/AUD-BLINK_MODULES-130ee005
./run_bof.sh /home/qwerty/chrome-agent/chromium-149.0.7779.3-linux-asan/chrome

```

The same `run.sh` launcher was also used with the public release binary:

```
cd pocs/AUD-BLINK_MODULES-130ee005
./run.sh /home/qwerty/chrome-agent/chrome-linux64/chrome

```
#### Crash Logs

ASAN run with `poc.html`:

```
==122148==ERROR: AddressSanitizer: heap-use-after-free on address 0x7261c71a5200
WRITE of size 4 at 0x7261c71a5200 thread T35 (Chrome_InProcRe)
...
0x7261c71a5200 is located 0 bytes inside of 173-byte region [0x7261c71a5200,0x7261c71a52ad)
...
SUMMARY: AddressSanitizer: heap-use-after-free

```

ASAN run with `poc_bof.html` and `quarantine_size_mb=0`:

```
==122155==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7792f77bf060
WRITE of size 4 at 0x7792f77bf060 thread T35 (Chrome_InProcRe)
...
0x7792f77bf060 is located 72 bytes after 168-byte region [0x7792f77bef70,0x7792f77bf018)
...
SUMMARY: AddressSanitizer: heap-buffer-overflow

```

Public release run with `poc.html`:

```
Received signal 11 SI_KERNEL000000000000
Possibly a General Protection Fault, can be due to a non-canonical address dereference.
...
r14: badbad00badbad00
bx:  badbad00badbad00

```
### Suggested Fix

One straightforward fix is to stop passing the cached current path by reference across a call that may reset the context:

```
diff --git a/third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc b/third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc
index 000000000000..000000000000 100644
--- a/third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc
+++ b/third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc
@@ -930,7 +930,8 @@ cc::Layer* CanvasRenderingContext2D::CcLayer() const {
 }
 
 void CanvasRenderingContext2D::drawFocusIfNeeded(Element* element) {
-  DrawFocusIfNeededInternal(GetPath(), element);
+  const Path path = GetPath();
+  DrawFocusIfNeededInternal(path, element);
 }
 
 void CanvasRenderingContext2D::drawFocusIfNeeded(Path2D* path2d,
                                                  Element* element) {

```
#### Impact analysis

A web page can trigger a use-after-free in the renderer process through the Canvas2D API. The issue is reachable from JavaScript and reproduces as renderer memory corruption without additional user interaction beyond visiting the page.

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7779.0, 148.0.6613.0

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Jungwoo Lee (@physicube) and Wongi Lee (@\_qwerty\_po)

## Attachments

- [poc_bof.html](attachments/poc_bof.html) (text/html, 749 B)
- [run.sh](attachments/run.sh) (text/x-sh, 1.5 KB)
- [poc.html](attachments/poc.html) (text/html, 807 B)
- [asan_report_bof.txt](attachments/asan_report_bof.txt) (text/plain, 18.3 KB)
- [run_bof.sh](attachments/run_bof.sh) (text/x-sh, 1.6 KB)
- [asan_report.txt](attachments/asan_report.txt) (text/plain, 23.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-04-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5767778791358464.

### cl...@appspot.gserviceaccount.com (2026-04-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5094033445650432.

### ma...@google.com (2026-04-16)

Renderer UAF, not protected by MiraclePtr, but mitigated by a11y support needing to be enabled -> S3.

### qw...@gmail.com (2026-04-16)

Could you please add [jwlee2217@gmail.com](mailto:jwlee2217@gmail.com) to the CC list so that both accounts can access the issue?

### 24...@project.gserviceaccount.com (2026-04-16)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/821a6917718c93d1facc4571c549ff6eb18290d8 (Update CanvasPath to use PathBuilder instead of Path

In the previous CL, Florin created a PathBuilder class that serves as
the building phase to create a path
(https://chromium-review.googlesource.com/c/chromium/src/+/6330705),
This CL, updates the CanvasPath to use the new PathBuilder.

Bug: 378688986

Change-Id: I30a3b7e76870f7f72c29a59e9efea94f7bb4254d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6414094
Commit-Queue: Yi Xu <yiyix@chromium.org>
Reviewed-by: Florin Malita <fmalita@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1443319}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2026-04-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5767778791358464

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x7692c1086240
Crash State:
  blink::CanvasRenderingContext2D::UpdateElementAccessibility
  blink::v8_canvas_rendering_context_2d::DrawFocusIfNeededOperationCallback
  Builtins_CallApiCallbackGeneric
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1443313:1443321

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5767778791358464

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ma...@google.com (2026-04-16)

A renderer UAF should be at most ~~S2~~S1, despite what CF thinks. But S2 here is probably adequate, due to the additional accessibility requirement.

### ch...@google.com (2026-04-17)

Setting milestone because of s2 severity.

### ch...@google.com (2026-04-17)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### qw...@gmail.com (2026-04-22)

Could you please add [jwlee2217@gmail.com](mailto:jwlee2217@gmail.com) to the CC list so that both accounts can access the issue?

### fm...@chromium.org (2026-04-22)

Done.

### qw...@gmail.com (2026-04-22)

Thanks!

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  main  

Author:  Florin Malita [fmalita@chromium.org](mailto:fmalita@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7785233>

[path builder] Return current path snapshot by value

---


Expand for full commit details
```
     
    Returning a reference to a std::optional-stored value is fragile, as 
    complex clients can end up inadvertently destroying the Path (e.g. via a 
    canvas 2d context loss in the linked bug) while the stale reference is 
    still in use. 
     
    Instead of attempting to locate and fix all vulnerable code paths, 
    change GetPath() to return a Path value. This is a shallow copy (the 
    underlying SkPathData is shared), and should not have major perf 
    repercussions. 
     
    Bug: 501646327 
    Change-Id: I7917086979b2544f3792f266811728fda8928c7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7785233 
    Reviewed-by: Fredrik Söderquist <fs@opera.com> 
    Commit-Queue: Florin Malita <fmalita@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1618987}

```

---

Files:

- M `third_party/blink/renderer/modules/canvas/canvas2d/canvas_path.h`
- M `third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d_test.cc`
- M `third_party/blink/renderer/platform/geometry/path_builder.cc`
- M `third_party/blink/renderer/platform/geometry/path_builder.h`

---

Hash: [f3b97ba13cd3890ae3369617f9dc6e4caccb22c0](https://chromiumdash.appspot.com/commit/f3b97ba13cd3890ae3369617f9dc6e4caccb22c0)  

Date: Wed Apr 22 18:29:57 2026


---

### 24...@project.gserviceaccount.com (2026-04-23)

ClusterFuzz testcase 5767778791358464 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1618984:1618989

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### aj...@google.com (2026-06-17)

-> High as accessibility flags are not considered a mitigating factor

### ch...@google.com (2026-06-18)

Requesting merge to M148 because latest trunk commit is in 149.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-06-18)

**M148** merge request created. **Please update [crbug/525281657](https://crbug.com/525281657) to have this merge reviewed.**

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Baseline. Renderer


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-31)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/501646327)*
