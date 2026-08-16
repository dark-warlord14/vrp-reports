# Service-side UAF due to missing sync token update in C*RP:WillDrawInternal()

| Field | Value |
|-------|-------|
| **Issue ID** | [493708171](https://issues.chromium.org/issues/493708171) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | mj...@chromium.org |
| **Created** | 2026-03-18 |
| **Bounty** | $10,000.00 |

## Description

### Summary

[`CanvasResourceProviderSharedImage::WillDrawInternal`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc;l=584) ends the old source access via the raw `gpu::RasterScopedAccess::EndAccess` helper instead of `CanvasResourceSharedImage::EndAccess`, skipping the `UpdateDestructionSyncToken` call on the source `ClientSharedImage`. This allows the source shared-image backing to be destroyed before the queued `CopySharedImage` and downstream GPU work have completed, resulting in a use-after-free on GPU-backend resources during compositor submit.

### Details

Blink's copy-on-write path in [`CanvasResourceProviderSharedImage::WillDrawInternal`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc;l=608) starts a read access on the old canvas resource, queues a `CopySharedImage()` from the old mailbox to the new mailbox, and then ends the source access through the raw helper:

```
resource_ = NewOrRecycledResource();
DCHECK(IsResourceUsable(resource_.get()));
dst_access = resource_->BeginAccess(/*readonly=*/false);
if (must_preserve_content_on_copy_on_write_) {
  auto old_mailbox =
      old_resource_shared_image->GetClientSharedImage()->mailbox();
  auto mailbox = resource()->GetClientSharedImage()->mailbox();
  auto src_access = old_resource->BeginAccess(/*readonly=*/true);
  RasterInterface()->CopySharedImage(old_mailbox, mailbox, 0, 0, 0, 0,
                                     Size().width(), Size().height());
  gpu::RasterScopedAccess::EndAccess(std::move(src_access));
}

```

The wrapper in [`CanvasResourceSharedImage::EndAccess`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/graphics/canvas_resource.cc;l=509) is what actually feeds the completion sync token back into the shared-image lifetime state:

```
void CanvasResourceSharedImage::EndAccess(
    std::unique_ptr<gpu::RasterScopedAccess> access) {
  CHECK(!GetClientSharedImage()->is_software());
  DCHECK(!is_cross_thread());

  auto sync_token = gpu::RasterScopedAccess::EndAccess(std::move(access));
  SetReleaseSyncToken(sync_token);
  GetClientSharedImage()->UpdateDestructionSyncToken(sync_token);
}

```

The key difference between the two `EndAccess` paths is:

- `gpu::RasterScopedAccess::EndAccess` (line 635, used here) only generates a sync token and returns it, discarding the token at the call site.
- `CanvasResourceSharedImage::EndAccess` (line 509 of `canvas_resource.cc`) calls `gpu::RasterScopedAccess::EndAccess` and then forwards the resulting sync token into both `SetReleaseSyncToken` and `ClientSharedImage::UpdateDestructionSyncToken`.

Because the copy-on-write path uses the raw helper, the source `ClientSharedImage`'s `destruction_sync_token_` is never advanced past its previous value. This means that when the last reference to the old resource is dropped, the GPU-side destruction of the corresponding shared-image backing can be scheduled immediately — without waiting for the `CopySharedImage` command (and any downstream work that depends on the source texels) to retire on the GPU timeline.

When the renderer and compositor operate on separate GPU threads (e.g. with `EnableDrDc`), the compositor thread may still reference the GPU-backend resources (textures, framebuffers, etc.) backed by the old shared image during present/submit, while the old shared image's backing has already been destroyed on the renderer GPU thread due to the stale destruction sync token. This constitutes a use-after-free on the underlying GPU-backend objects.

### Bisection

This issue is introduced by the commit <https://chromium-review.googlesource.com/c/chromium/src/+/7068355>, which rewrite the `WaitSyncToken` into the `BeginAccess()/EndAccess()`.

### Reproduction

Download the chrome from <https://storage.googleapis.com/chromium-browser-asan/win32-release_x64/asan-win32-release_x64-1600354.zip>

On a Windows machine with any dedicated GPU, run the following command

```
./chrome.exe --no-sandbox --enable-skia-graphite --skia-graphite-dawn-backend=opengles --enable-features=EnableDrDc,GraphiteContextIsThreadSafe --enable-unsafe-webgpu --ignore-gpu-blocklist  --enable-experimental-web-platform-features --enable-blink-test-features poc.html

```

You would observe the UAF shown in `asan.txt`

### Suggested Fix

Replace the raw source-access teardown in `CanvasResourceProviderSharedImage::WillDrawInternal` with the wrapper that updates the source resource's destruction sync token, or otherwise explicitly propagate the source completion sync token into the source `ClientSharedImage` before the old resource can be destroyed.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 61.4 KB)
- [poc.html](attachments/poc.html) (text/html, 3.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6003956325056512.

### ts...@google.com (2026-03-18)

Assigning per suspected CL.

### bl...@chromium.org (2026-03-19)

Note: As part of ongoing CanvasResourceProvider decomposition, this method has now been split into two - Canvas{2D, Non2D}ResourceProviderSI::WillDrawInternal() should both get the fix. (We're working toward getting rid of the CoW code from the CanvasNon2D impl after verifying that it's not actually necessary for the use cases there, but we're not quite there yet).

### va...@chromium.org (2026-03-25)

I don't think destruction SyncToken changes anything here. UaF happens inside Angle/D3D11 with calls coming from ganesh (not graphite). I believe Angle's D3D backend is not thread-safe and chrome doesn't turn on Angle's global lock anymore, so turning on DrDc on windows is not really supported.

That being said, nothing wrong with updating destruction SyncToken after CoW to make code base a bit more correct.

### ch...@google.com (2026-03-26)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-03-26)

Project: chromium/src  

Branch:  main  

Author:  Mingjing Zhang [mjzhang@chromium.org](mailto:mjzhang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7686738>

[blink] Fix use-after-free in WillDrawInternal()

---


Expand for full commit details
```
     
    This CL intends to fix an issue where the shared image is freed 
    prematurely by using CanvasResourceSharedImage::EndAccess() instead of 
    the raw RasterScopedAccess::EndAccess(). The former EndAccess() properly 
    updates the destruction sync token. 
     
    Bug: 493708171 
    Change-Id: I3dc864021cd9c834d6f53fe5f114f7c4a84cf135 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686738 
    Commit-Queue: Mingjing Zhang <mjzhang@chromium.org> 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1605684}

```

---

Files:

- M `third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc`

---

Hash: [afb785c7de354846a0cf3524369c39097f4636a9](https://chromiumdash.appspot.com/commit/afb785c7de354846a0cf3524369c39097f4636a9)  

Date: Thu Mar 26 18:37:54 2026


---

### kb...@chromium.org (2026-03-26)

Vasiliy, thanks for pointing out that `--enable-features=EnableDrDc,GraphiteContextIsThreadSafe` is not supported.

@wf...@chromium.org I think this should be downgraded to `Security_Impact-None`. Can you please comment?

### wf...@chromium.org (2026-03-26)

yes, the study I see only has this enabled on Mac but we would prefer if the switch was just not there on unsupported platforms at all (e.g. to avoid accidently turning it on via a rogue config). But yes in this instance I agree this looks like sec impact none.

### he...@gmail.com (2026-04-18)

Hi, thanks for the fix. Could you please mark this issue as fixed. Thank you very much!

### he...@gmail.com (2026-04-30)

friendly ping - could you please mark this as fixed?

### sp...@google.com (2026-05-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Baseline with bisect - Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-08-14)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493708171)*
