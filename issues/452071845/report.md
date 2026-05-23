# Potential out-of-bounds read in Transform::ColMajorF on undersized buffer

| Field | Value |
|-------|-------|
| **Issue ID** | [452071845](https://issues.chromium.org/issues/452071845) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebXR |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ig...@aisle.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2025-10-15 |
| **Bounty** | $2,000.00 |

## Description

**Security Bug**

We have discovered a potential issue in Chromium that lets WebXR content trigger an out-of-bounds read in the renderer by feeding a zero-length buffer into `gfx::Transform::ColMajorF`.

**Vulnerability Details**

- `Transform::ColMajorF` assumes the caller has provided 16 floats and blindly reads indices 0–15; the surrounding UNSAFE\_TODO macros do not add checks.
- When a page detaches the cached matrix buffer on an `XRRigidTransform`, Blink currently hands `XRRay` a fresh zero-length `DOMFloat32Array`, which is then forwarded to `Transform::ColMajorF` without validation.
- This results in a 64-byte read past the view, leaking heap data back to script via `XRRay`'s origin/direction, or crashing on debug builds.

**Code Snippets:**

```
// ui/gfx/geometry/transform.cc (lines 115-130, current HEAD)
Transform Transform::ColMajorF(const float a[16]) {
  if (AllTrue(Float4{UNSAFE_TODO(a[1]), UNSAFE_TODO(a[2]), UNSAFE_TODO(a[3]),
                     UNSAFE_TODO(a[4])} == Float4{0, 0, 0, 0} &
              Float4{UNSAFE_TODO(a[6]), UNSAFE_TODO(a[7]), UNSAFE_TODO(a[8]),
                     UNSAFE_TODO(a[9])} == Float4{0, 0, 0, 0} &
              Float4{UNSAFE_TODO(a[10]), UNSAFE_TODO(a[11]), UNSAFE_TODO(a[14]),
                     UNSAFE_TODO(a[15])} == Float4{1, 0, 0, 1})) {
    return Transform(a[0], UNSAFE_TODO(a[5]), UNSAFE_TODO(a[12]),
                     UNSAFE_TODO(a[13]));
  }
  return Transform(a[0], UNSAFE_TODO(a[1]), UNSAFE_TODO(a[2]),
                   UNSAFE_TODO(a[3]), UNSAFE_TODO(a[4]), UNSAFE_TODO(a[5]),
                   UNSAFE_TODO(a[6]), UNSAFE_TODO(a[7]), UNSAFE_TODO(a[8]),
                   UNSAFE_TODO(a[9]), UNSAFE_TODO(a[10]), UNSAFE_TODO(a[11]),
                   UNSAFE_TODO(a[12]), UNSAFE_TODO(a[13]), UNSAFE_TODO(a[14]),
                   UNSAFE_TODO(a[15]));
}

```
```
// third_party/blink/renderer/modules/xr/xr_rigid_transform.cc (lines 115-120, current HEAD)
if (!matrix_array_ || matrix_array_->IsDetached()) {
  // A page may take the matrix_array_ value and detach it so matrix_array_ is
  // a detached array buffer.  This breaks the inspector, so return an empty
  // array instead.
  return NotShared<DOMFloat32Array>(DOMFloat32Array::Create(0));
}

```
```
// third_party/blink/renderer/modules/xr/xr_ray.cc (lines 38-40, current HEAD)
XRRay::XRRay(XRRigidTransform* transform, ExceptionState& exception_state) {
  NotShared<DOMFloat32Array> m = transform->matrix();
  Set(DOMFloat32ArrayToTransform(m), exception_state);
}

```
```
// third_party/blink/renderer/modules/xr/xr_utils.cc (lines 25-28, current HEAD)
gfx::Transform DOMFloat32ArrayToTransform(NotShared<DOMFloat32Array> m) {
  DCHECK_EQ(m->length(), 16u);
  return gfx::Transform::ColMajorF(m->Data());
}

```

**VERSION**

- Chrome Version: Chromium 143.0.7470.0, Chromium 141.0.7390.65 built on Debian GNU/Linux 13 (trixie)
- Operating System:
  Debian GNU/Linux 13 (trixie)

**REPRODUCTION CASE - DEBUG BUILD**

1. Launch Chromium/Chrome debug
2. In a renderer console:
   ```
   const t = new XRRigidTransform();
   const arr = t.matrix;
   const ch = new MessageChannel();
   ch.port1.postMessage(arr.buffer, [arr.buffer]); // detaches arr
   const ray = new XRRay(t);                       // triggers ColMajorF read
   
   ```
3. Observe `FATAL:third_party/blink/renderer/modules/xr/xr_utils.cc:26] DCHECK failed: m->length() == 16u (0 vs. 16)`

**REPRODUCTION CASE - OOB READ**

1. Launch Chromium/Chrome release
2. Run poc-min-leak.js
3. Observe leaked marked data

**Similar Findings (related patterns in current code)**

- `XRView::projectionMatrix()` returns a zero-length `DOMFloat32Array` when detached, mirroring the `XRRigidTransform::matrix()` behavior. While not currently passed to `Transform::ColMajorF`, this could become exploitable if used in transform code.
  - Location: `third_party/blink/renderer/modules/xr/xr_view.cc` lines 79–85
- `WTFFloatVectorToTransform(const Vector<float>&)` forwards raw `m.data()` to `Transform::ColMajorF` with only a DCHECK on size. This is currently unused but should be hardened to prevent future misuse.
  - Location: `third_party/blink/renderer/modules/xr/xr_utils.cc` lines 30–33

**CREDIT INFORMATION**

**Reporter credit**: Aisle Research

## Attachments

- [poc-min-leak.js](attachments/poc-min-leak.js) (text/javascript, 3.1 KB)

## Timeline

### el...@chromium.org (2025-10-15)

Security shepherd: thanks for the report! I reproduced this locally by:

1. Taking your PoC and wrapping the code at the end in an async function
2. Invoking that async function from devtools

which led to a renderer crash with the described stack trace. In a non-debug build, it instead dumps some nonzero data.

Given that this is an OOB read in the renderer, this is Sev-2 / Pri-2, and I'm sending it to the WebXR team.

### al...@chromium.org (2025-10-15)

It looks like WTFFloatVectorToTransform is unused, and so can be removed. The `projectionMatrix` is not a rigid transform, and so should likely fail due to other reasons; but probably worth figuring out what to do there. I'll likely upgrade the other helper to a CHECK, and then consider whether the constructor should do this validation on hte matrix, or if the matrix should return e.g. identity (or maybe all 0s but the proper length to still highlight the error in dev tools).

### al...@chromium.org (2025-10-15)

Looks like we aren't matching the WebXR spec with the current implementation either, which seems to imply that we should be recalculating the array if it becomes detached.

<https://immersive-web.github.io/webxr/#xrrigidtransform-obtain-the-matrix> (with similar logic for the projection matrix).

Pending CL upgrades the DOMFloat32ArrayToTransform to a check and fixes the two mentioned detached array checks to recalculate the matrix rather than return a short/empty one.

I also filed [Issue 452274003](https://issues.chromium.org/issues/452274003) for the transform owners to update the underlying UNSAFE\_TODOs

### ch...@google.com (2025-10-16)

Setting milestone because of s2 severity.

### dx...@google.com (2025-10-16)

Project: chromium/src  

Branch:  main  

Author:  Alexander Cooper [alcooper@chromium.org](mailto:alcooper@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7046576>

[WebXR] Update detached matrix handling

---


Expand for full commit details
```
     
    Updates a few places that handle an array representation of a matrix 
    being detached by returning a 0-length array to simply recompute the 
    array that should be present, based on the presence of other data. This 
    more closely matches the spec, which for both of these cases essentially 
    state that if the value is not null to check if it's detached, and if it 
    is not detached to return the value. The steps following both of these 
    checks then recompute the matrix, so technically our current impl is 
    not spec-compliant to that. 
     
    Further, we remove one unused array to transform conversion helper and 
    update another to a CHECK from a DCHECK to match best practices for 
    invariants. 
     
    Fixed: 452071845 
    Change-Id: Idf765fe5717d59ae63c71e8253784ff4473dea5f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7046576 
    Commit-Queue: Alexander Cooper <alcooper@chromium.org> 
    Reviewed-by: Brandon Jones <bajones@chromium.org> 
    Auto-Submit: Alexander Cooper <alcooper@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1530947}

```

---

Files:

- M `third_party/blink/renderer/modules/xr/xr_rigid_transform.cc`
- M `third_party/blink/renderer/modules/xr/xr_utils.cc`
- M `third_party/blink/renderer/modules/xr/xr_utils.h`
- M `third_party/blink/renderer/modules/xr/xr_view.cc`
- M `third_party/blink/renderer/modules/xr/xr_view.h`

---

Hash: [6c5963ad6b4541f5fa0812607fd36a979c48c0f1](https://chromiumdash.appspot.com/commit/6c5963ad6b4541f5fa0812607fd36a979c48c0f1)  

Date: Thu Oct 16 17:54:37 2025


---

### ch...@google.com (2025-10-18)

Security Merge Request Consideration: Requesting merge to beta (M142) because latest trunk commit (1530947) appears to be after beta branch point (1522585).
Security Merge Request - Manual Review: Merge review required: M142 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### al...@chromium.org (2025-10-20)

1. <https://chromium-review.googlesource.com/7046576>
2. Yes, seems fine on Canary
3. I don't believe so, the fix is small and basically just adds another path where we go through a path to recalculate a cached value, and otherwise removes dead code.
4. I don't believe so
5. No, it should be fine.
6. I think this is accurate as the actual reported error did not require entering a WebXR session, simply creation of some types we expose as helpers that can be constructed separately from a session.

### al...@chromium.org (2025-10-20)

In the interest of full disclosure, there *does* seem to be a speedometer regression allegedly related to this CL; but I have no idea how my CL could've caused it: [Issue 452701612](https://issues.chromium.org/issues/452701612)

### ya...@chromium.org (2025-10-21)

Please proceed with the merge

### dx...@google.com (2025-10-21)

Project: chromium/src  

Branch:  refs/branch-heads/7444  

Author:  Alexander Cooper [alcooper@chromium.org](mailto:alcooper@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7068658>

[WebXR] Update detached matrix handling

---


Expand for full commit details
```
     
    Updates a few places that handle an array representation of a matrix 
    being detached by returning a 0-length array to simply recompute the 
    array that should be present, based on the presence of other data. This 
    more closely matches the spec, which for both of these cases essentially 
    state that if the value is not null to check if it's detached, and if it 
    is not detached to return the value. The steps following both of these 
    checks then recompute the matrix, so technically our current impl is 
    not spec-compliant to that. 
     
    Further, we remove one unused array to transform conversion helper and 
    update another to a CHECK from a DCHECK to match best practices for 
    invariants. 
     
    (cherry picked from commit 6c5963ad6b4541f5fa0812607fd36a979c48c0f1) 
     
    Fixed: 452071845 
    Change-Id: Idf765fe5717d59ae63c71e8253784ff4473dea5f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7046576 
    Commit-Queue: Alexander Cooper <alcooper@chromium.org> 
    Reviewed-by: Brandon Jones <bajones@chromium.org> 
    Auto-Submit: Alexander Cooper <alcooper@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1530947} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7068658 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7444@{#1683} 
    Cr-Branched-From: 29907d3c18078029695f458b42fb8e6fda3e493d-refs/heads/main@{#1522585}

```

---

Files:

- M `third_party/blink/renderer/modules/xr/xr_rigid_transform.cc`
- M `third_party/blink/renderer/modules/xr/xr_utils.cc`
- M `third_party/blink/renderer/modules/xr/xr_utils.h`
- M `third_party/blink/renderer/modules/xr/xr_view.cc`
- M `third_party/blink/renderer/modules/xr/xr_view.h`

---

Hash: [d2c66e99ce6f42affccf653a0a7d015d6c06d956](https://chromiumdash.appspot.com/commit/d2c66e99ce6f42affccf653a0a7d015d6c06d956)  

Date: Tue Oct 21 18:10:58 2025


---

### pe...@google.com (2025-10-21)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### al...@chromium.org (2025-10-21)

1. No, this is a security issue that has been present for a while
2. No.

### pe...@google.com (2025-10-24)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-10-24)

1. https://chromium-review.googlesource.com/c/chromium/src/+/7077799
2. Low - There was a small conflict in the unit test.
3. 142
4. Yes, the issue has existed for a while according to #13.

### ch...@google.com (2025-10-24)

This V8 bug has been marked as a release blocker. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### sp...@google.com (2025-11-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
baseline user information disclosure i.e. a read in the renderer


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2025-12-23)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Alexander Cooper [alcooper@chromium.org](mailto:alcooper@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7077799>

[M138-LTS][WebXR] Update detached matrix handling

---


Expand for full commit details
```
     
    Updates a few places that handle an array representation of a matrix 
    being detached by returning a 0-length array to simply recompute the 
    array that should be present, based on the presence of other data. This 
    more closely matches the spec, which for both of these cases essentially 
    state that if the value is not null to check if it's detached, and if it 
    is not detached to return the value. The steps following both of these 
    checks then recompute the matrix, so technically our current impl is 
    not spec-compliant to that. 
     
    Further, we remove one unused array to transform conversion helper and 
    update another to a CHECK from a DCHECK to match best practices for 
    invariants. 
     
    (cherry picked from commit 6c5963ad6b4541f5fa0812607fd36a979c48c0f1) 
     
    Fixed: 452071845 
    Change-Id: Idf765fe5717d59ae63c71e8253784ff4473dea5f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7046576 
    Commit-Queue: Alexander Cooper <alcooper@chromium.org> 
    Reviewed-by: Brandon Jones <bajones@chromium.org> 
    Auto-Submit: Alexander Cooper <alcooper@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1530947} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7077799 
    Commit-Queue: Jeremy Roman <jbroman@chromium.org> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
    Reviewed-by: Jeremy Roman <jbroman@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3469} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/modules/xr/xr_rigid_transform.cc`
- M `third_party/blink/renderer/modules/xr/xr_utils.cc`
- M `third_party/blink/renderer/modules/xr/xr_utils.h`
- M `third_party/blink/renderer/modules/xr/xr_view.cc`
- M `third_party/blink/renderer/modules/xr/xr_view.h`

---

Hash: [4e5f8b529d7de813b27d84632b77147d43fbea8a](https://chromiumdash.appspot.com/commit/4e5f8b529d7de813b27d84632b77147d43fbea8a)  

Date: Tue Dec 23 16:00:31 2025


---

### ch...@google.com (2026-01-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline user information disclosure i.e. a read in the renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/452071845)*
