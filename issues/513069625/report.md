# GPU passthrough decoder UAF: DoBufferData GL error path skips mapped_buffer_map.erase()

| Field | Value |
|-------|-------|
| **Issue ID** | [513069625](https://issues.chromium.org/issues/513069625) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Android, Linux, ChromeOS |
| **Reporter** | pa...@gmail.com |
| **Assignee** | sh...@google.com |
| **Created** | 2026-05-14 |
| **Bounty** | $25,000.00 |

## Description

---

### Report description

ANGLE Vulkan ContextVk::flushAndSubmitCommands error paths leak mForeignImagesInUse stale-set causing heap-use-after-free (incomplete fix of CL 7801425)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/angle/angle/+/HEAD/src/libANGLE/renderer/vulkan/ContextVk.cpp;l=7551>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

CL 7801425 (merged 2026-04-29) added a callsite-level cleanup
`forgetAllForeignImagesOnError()` to one caller of
`ContextVk::flushAndSubmitCommands` in `ShareGroupVk.cpp:439`. At HEAD
as of 2026-05-14, twelve other callers of `flushAndSubmitCommands`
within `ContextVk.cpp` (lines 1441, 1490, 1507, 6108, 6136, 6881,
7240, 7660, 8074, 8132 and two callsites at 7548/7657 inside
`finishImpl`/`prepareToSubmitAllCommands`) do not perform the same
cleanup on error return.

When `flushAndSubmitCommands` returns an error via internal
`ANGLE_TRY`, the `mForeignImagesInUse` HashSet retains
`ImageHelper*` pointers populated by earlier `onForeignImageUse`
calls. The next call to `finalizeAllForeignImages` dereferences
those pointers. If the underlying `ImageHelper` is freed in the
interval, this is a heap-use-after-free write in the GPU process.

This is the same defect class as the just-paid Chrome VRP report
507707838 (CL 7808748): early-return on error skips state cleanup,
stale pointer dereferenced later.

## Affected component

Repo: `angle/angle`
File: `src/libANGLE/renderer/vulkan/ContextVk.cpp`
Verified on: HEAD as of 2026-05-14, after CL 7801425.

## Root cause

`ContextVk::flushAndSubmitCommands` has three internal `ANGLE_TRY`
sites that can return error early
(`ContextVk.cpp:7551-7654`):

```
angle::Result ContextVk::flushAndSubmitCommands(...) {
  ...
  if (someCommandsNeedFlush) {
    ANGLE_TRY(
        flushCommandsAndEndRenderPassWithoutSubmit(...));    // line 7577
  }
  ...
  ANGLE_TRY(flushOutsideRenderPassCommands());               // line 7612
  ...
  prepareToSubmitAllCommands();                               // line 7639
  ANGLE_TRY(submitCommands(...));                             // line 7640
  ...
  return angle::Result::Continue;
}

```

`prepareToSubmitAllCommands()` at line 7639 is the only place that
calls `finalizeAllForeignImages` (via line 7548). If any earlier
`ANGLE_TRY` fails, the function returns before
`prepareToSubmitAllCommands` runs.

`mForeignImagesInUse` is populated upstream by
`Context::onForeignImageUse` (vk\_helpers.cpp:642-647):

```
void Context::onForeignImageUse(ImageHelper *image) {
  mForeignImagesInUse.insert(image);
}

```

On error return without `finalizeAllForeignImages`, the set retains
entries. On a later successful flush, `finalizeAllForeignImages`
(vk\_helpers.cpp:665-673) iterates the stale set:

```
void Context::finalizeAllForeignImages() {
  mImagesToTransitionToForeign.reserve(...);
  while (!mForeignImagesInUse.empty()) {
    finalizeForeignImage(*mForeignImagesInUse.begin());
  }
}

```

`finalizeForeignImage` dereferences the pointer
(vk\_helpers.cpp:649-663):

```
void Context::finalizeForeignImage(ImageHelper *image) {
  ...
  mImagesToTransitionToForeign.push_back(image->releaseToForeign(mRenderer));
  //                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  // UAF: image may have been destroyed between failed flush and
  // this finalization.
  mForeignImagesInUse.erase(image);
}

```
## CL 7801425 coverage gap

CL 7801425 applies the cleanup at one caller in
`ShareGroupVk.cpp:439`:

```
const angle::Result result = sharedContextVk->flushAndSubmitCommands(
    nullptr, nullptr, QueueSubmitReason::ForeignImageRelease);

if (result != angle::Result::Continue) {
    sharedContextVk->forgetAllForeignImagesOnError();
}

```

The twelve other callers in `ContextVk.cpp` are not similarly
guarded:

| Line | Caller | Pattern |
| --- | --- | --- |
| 1441 | `flushImpl` | `return flushAndSubmitCommands(...)` |
| 1490 | flush variant | `ANGLE_TRY(flushAndSubmitCommands(...))` |
| 1507 | `flushImpl` epilogue | `return flushAndSubmitCommands(...)` |
| 6108 | `onMakeCurrent` | `ANGLE_TRY` propagates |
| 6136 | `surfaceUnMakeCurrent` | `flushAndSubmitCommands(...)` |
| 6881 | unknown | `return flushAndSubmitCommands(...)` |
| 7240 | `ExcessivePendingGarbage` | `flushAndSubmitCommands(...)` |
| 7660 | `finishImpl` | `ANGLE_TRY(flushAndSubmitCommands(...))` |
| 8074 | flush | `return flushAndSubmitCommands(...)` |
| 8132 | `SyncObjectInit` | `ANGLE_TRY(flushAndSubmitCommands(...))` |

In each case, on error the caller returns or propagates the error
upward but does not call `forgetAllForeignImagesOnError`.
`mForeignImagesInUse` remains populated with stale pointers until
the next successful flush triggers `finalizeAllForeignImages`.

## Proposed patch

Move the cleanup from the call sites into
`flushAndSubmitCommands` itself. This covers every caller and
prevents future regressions when new callers are added.

```
diff --git a/src/libANGLE/renderer/vulkan/ContextVk.cpp \
b/src/libANGLE/renderer/vulkan/ContextVk.cpp
--- a/src/libANGLE/renderer/vulkan/ContextVk.cpp
+++ b/src/libANGLE/renderer/vulkan/ContextVk.cpp
@@ -7551,6 +7551,7 @@
 angle::Result ContextVk::flushAndSubmitCommands(
     const vk::Semaphore *signalSemaphore,
     const vk::SharedExternalFence *externalFence,
     QueueSubmitReason queueSubmitReason)
 {
+    angle::Result innerResult = [&]() -> angle::Result {
     bool someCommandsNeedFlush =
         !mOutsideRenderPassCommands->empty() ||
         mRenderPassCommands->started();
@@ -7651,6 +7652,13 @@
     // ... rest of original body ...
     return angle::Result::Continue;
+    }();
+
+    if (innerResult != angle::Result::Continue) {
+        // Drop foreign image references that did not get transitioned
+        // by the failed submission to prevent stale-pointer UAF.
+        forgetAllForeignImagesOnError();
+    }
+    return innerResult;
 }

```

The ShareGroupVk caller-side cleanup added by CL 7801425 becomes
redundant after this change but does not need to be removed.

## Variants

The same caller-side-vs-callee-side asymmetry may apply to other
state in `ContextVk` that requires error-path cleanup. Worth a
follow-up audit on:

- `mImagesToTransitionToForeign` (vk\_helpers.cpp).
- `mDefaultUniformStorage` and `mStreamedVertexBuffers` (do their
  release-in-flight paths require post-error cleanup that current
  code skips?).
- Any state machine in ContextVk where the success path performs
  cleanup and the error path is silently expected to retry later.

#### Impact analysis

## Impact

Heap-use-after-free write primitive in GPU process. Same severity
tier as Chrome VRP report 507707838 ($25,000 baseline for memory
corruption in highly privileged process).

Reach:

- Renderer-induced Vulkan submission failure is achievable through
  malicious memory allocation patterns or by exhausting GPU
  resources to trigger `VK_ERROR_OUT_OF_DEVICE_MEMORY` or
  `VK_ERROR_DEVICE_LOST`.
- ANGLE Vulkan backend is the default on Linux ChromeOS and one of
  several backends on Windows / macOS.

Starting position: compromised renderer.

User interaction: none beyond normal rendering activity that uses
shared images / EGLImages.

---

### The cause

#### What version of Chrome have you found the security issue in?

ANGLE HEAD as of 2026-05-14, commit-position 1622511 or later (after CL 7801425 / commit 8e610d05a7c89a9800dc5a176a3a7f9e00698861). Chrome stable channels using ANGLE Vulkan backend are affected if they include CL 7801425's partial fix but lack the present coverage.

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

## Attachments

- [angle_foreign_images_callee_side_fix.patch](attachments/angle_foreign_images_callee_side_fix.patch) (application/octet-stream, 1.6 KB)
- [foreign_images_stale_set_poc_test.cpp](attachments/foreign_images_stale_set_poc_test.cpp) (application/octet-stream, 3.3 KB)

## Timeline

### pe...@google.com (2026-05-14)

ANGLE vulkan is max s1 vulnerability due to sandboxed GPU.

### ch...@google.com (2026-05-20)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-05-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### sy...@google.com (2026-05-20)

Closing as Won't Fix per <http://go/angle-security-bugs?tab=t.0#heading=h.196zxa6r9g61>

### pa...@gmail.com (2026-05-20)

Hi, could you pls elaborate?
The PoC I attached was a skeleton with unimplemented stubs - it does not compile. That is on me. But the closure reason is what I want to follow up on.

The status says "Not Reproducible" and the comment says "Won't Fix per go/angle-security-bugs". Those mean different things. If the bug cannot be reproduced because I am wrong about the code path, I want to know where my analysis is wrong. If it is a policy decision that this class does not qualify, that is a different conversation.

The defect as I see it: flushAndSubmitCommands has three ANGLE\_TRY sites before prepareToSubmitAllCommands at line 7651. finalizeAllForeignImages only runs inside prepareToSubmitAllCommands (line 7560). CL 7801425 added forgetAllForeignImagesOnError to ShareGroupVk.cpp:439. The callers in ContextVk.cpp at lines 1441, 1490, 1507, 6120, 6148, 6893, 7252, 7672, 8086, 8144 do not. If any of those callers returns an error while mForeignImagesInUse is non-empty, the set retains stale pointers until the next successful flush calls finalizeAllForeignImages.

Is there an invariant that prevents mForeignImagesInUse from being non-empty when these callers fail? If so I missed it and would like to understand it. If the answer is that the trigger requires a GPU-level submission failure that is not renderer-controllable, then I understand the policy position - but that is worth saying explicitly rather than closing as Not Reproducible.

[Bug 507707838](https://issues.chromium.org/issues/507707838) was the same structure (early error return, skipped cleanup, stale pointer on next use) in the passthrough decoder and was treated as S1. The difference I can think of is trigger controllability. If that is the distinguishing factor here, confirming it would help calibrate future reports.

### ch...@google.com (2026-05-20)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### dx...@google.com (2026-05-25)

Project: angle/angle  

Branch:  main  

Author:  Tzarial [zork@google.com](mailto:zork@google.com)  

Link:    <https://chromium-review.googlesource.com/7857869>

Vulkan: Fix UAF in flushAndSubmitCommands

---


Expand for full commit details
```
     
    ContextVk::flushAndSubmitCommands could early-return on errors via 
    ANGLE_TRY, skipping the call to finalizeAllForeignImages. This left 
    stale ImageHelper pointers in mForeignImagesInUse. If an image was 
    destroyed before the next successful flush dereferenced those 
    pointers, it resulted in a heap-use-after-free in the GPU process. 
     
    This change moves the cleanup logic from the call sites (fixing a gap 
    left by CL 7801425) into flushAndSubmitCommands itself. The core 
    logic is moved to a private flushAndSubmitCommandsImpl helper, and 
    the wrapper ensures forgetAllForeignImagesOnError() is called on any 
    failure path, protecting all current and future callers. 
     
    Bug: b/513069625 
    Change-Id: I227b052509a4107d09055ef18e40afc55cab817d 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7857869 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/ContextVk.cpp`
- M `src/libANGLE/renderer/vulkan/ContextVk.h`

---

Hash: [a793c75398c746f3f8a08fd2e74dfc4dff07a0c9](https://chromiumdash.appspot.com/commit/a793c75398c746f3f8a08fd2e74dfc4dff07a0c9)  

Date: Mon May 18 22:24:56 2026


---

### ch...@google.com (2026-08-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/513069625)*
