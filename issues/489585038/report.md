# UAF in APICopyTextureToTexture of Dawn

| Field | Value |
|-------|-------|
| **Issue ID** | [489585038](https://issues.chromium.org/issues/489585038) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2026-03-04 |
| **Bounty** | $11,000.00 |

## Description

### Summary

A depth-only `copyTextureToTexture` with `copySize.depthOrArrayLayers == 0` can take a no-op blit path in [`CommandEncoder::APICopyTextureToTexture`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/CommandEncoder.cpp;l=1922) where no `CopyTextureToTextureCmd` is recorded. If we destroy the textures and drops JS references before submit, submit-time validation in [`QueueBase::ValidateSubmit`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/Queue.cpp;l=486) will trigger UAF when dereferences stale pointers from `topLevelTextures`.

### Details

`copySize.depthOrArrayLayers == 0` is accepted on this T2T path because [`ValidateTextureCopyRange`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/CommandValidation.cpp;l=473) checks only out-of-bounds arithmetic and has no non-zero depth/layer guard.

```
MaybeError ValidateTextureCopyRange(DeviceBase const* device,
                                    const TexelCopyTextureInfo& textureCopy,
                                    const Extent3D& copySize) {
    ...
    DAWN_INVALID_IF(
        static_cast<uint64_t>(textureCopy.origin.x) + static_cast<uint64_t>(copySize.width) >
                static_cast<uint64_t>(mipSize.width) ||
            static_cast<uint64_t>(textureCopy.origin.y) + static_cast<uint64_t>(copySize.height) >
                static_cast<uint64_t>(mipSize.height) ||
            static_cast<uint64_t>(textureCopy.origin.z) +
                    static_cast<uint64_t>(copySize.depthOrArrayLayers) >
                static_cast<uint64_t>(mipSize.depthOrArrayLayers),
        ...);
    ...
}

```

The vulnerable state transition occurs in [`CommandEncoder::APICopyTextureToTexture`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/CommandEncoder.cpp;l=1922). Therefore, the raw top-level tracking is always populated first, then the copy command is conditionally skipped when depth blit is selected.

```
mTopLevelTextures.insert(source.texture);
mTopLevelTextures.insert(destination.texture);

const bool blitDepth =
    (aspect & Aspect::Depth) &&
    GetDevice()->IsToggleEnabled(
        Toggle::UseBlitForDepthTextureToTextureCopyToNonzeroSubresource) &&
    (dst.mipLevel > 0 || dst.origin.z > TexelCount{0} ||
     copySize->depthOrArrayLayers > 1);

if (!blitDepth || aspect != Aspect::Depth) {
    CopyTextureToTextureCmd* copy =
        allocator->Allocate<CopyTextureToTextureCmd>(Command::CopyTextureToTexture);
    copy->source = src;
    copy->destination = dst;
    copy->copySize = *copySize;
}

if (blitDepth) {
    DAWN_TRY_CONTEXT(BlitDepthToDepth(GetDevice(), this, src, dst, *copySize), ...);
}

```

When `depthOrArrayLayers == 0`, the blit helper emits no per-layer work, as both loops in [`BlitDepthToDepth`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/BlitDepthToDepth.cpp;l=108) are bounded by `copyExtent.depthOrArrayLayers`.

```
srcViews.reserve(copyExtent.depthOrArrayLayers);
for (TexelCount z = TexelCount{0}; z < copyExtent.depthOrArrayLayers; ++z) {
    ...
}

for (TexelCount z = TexelCount{0}; z < copyExtent.depthOrArrayLayers; ++z) {
    ...
    pass->APIDraw(3, 1, 0, 0);
    pass->End();
}

```

Moreover, while command objects hold strong refs, the CommandBufferResourceUsage does not. In [`Commands.h`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/Commands.h;l=203), `TextureCopy` owns `Ref<TextureBase>`, and `CopyTextureToTextureCmd` embeds two `TextureCopy` objects:

```
struct TextureCopy {
    Ref<TextureBase> texture;
    uint32_t mipLevel;
    TexelOrigin3D origin;
    Aspect aspect;
};

struct CopyTextureToTextureCmd {
    TextureCopy source;
    TextureCopy destination;
    TexelExtent3D copySize;
};

```

Finally, the CommandBufferResourceUsage [`CommandBufferResourceUsage`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/PassResourceUsage.h;l=112) dereference the raw pointer in [`QueueBase::ValidateSubmit`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/Queue.cpp;l=548). These pointers can be corrupted at the time of usage, thus leading to the UAF.

```
for (const TextureBase* texture : usages.topLevelTextures) {
    DAWN_TRY(texture->ValidateCanUseInSubmitNow());
}

```
### Bisection

This issue is introduced by the commit `e60a579c19581f9bffc8ce23a376c0de847a200a`, which change the `APICopyTextureToTexture` from always encoding `CopyTextureToTextureCmd` to a conditional `blitDepth` path that can skip command encoding and call `BlitDepthToDepth` directly.

### Reproduction

Download the chrome from `https://storage.googleapis.com/chromium-browser-asan/mac-release-arm64/asan-mac-release-1592006.zip`.

Run with the following command line on the arm mac.

```
./Chromium.app/Contents/MacOS/Chromium --enable-unsafe-webgpu --no-sandbox --enable-dawn-features=use_blit_for_depth_texture_to_texture_copy_to_nonzero_subresource --js-flags=--expose-gc poc.html

```

This would trigger the UAF shown in the `asan.txt`.

### Suggested Fix

We may tighten `blitDepth` so zero-layer copies never enter the blit-only path, forcing the normal copy-command path.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 34.6 KB)
- [poc.html](attachments/poc.html) (text/html, 1.1 KB)

## Timeline

### me...@google.com (2026-03-07)

Reproed locally.

cwallez@, another one, PTAL?

### cw...@chromium.org (2026-03-09)

Antonio PTAL, I'm confident that this is a valid issue that could happen, basically Dawn always encode commands even if noop, because the Ref<> in `Commands.h` is necessary to keep objects alive until submission (for example to check they can be used in submits). However a workaround path is taken, that on noop encodes nothing, causing a possible UAF. We could fix by skipping the workaround on noop, but should also audit all other workarounds in command encoding to see if there is the same problem that can happen. (plus regression tests, and a TODO to move the Ref<> out of the command stream and on the side in the CommandEncoder, so that we don't need to walk the commands to free the refs, that's something we've wanted to do for perf for a while).

### dx...@google.com (2026-03-12)

Project: dawn  

Branch:  main  

Author:  Antonio Maiorano [amaiorano@google.com](mailto:amaiorano@google.com)  

Link:    <https://dawn-review.googlesource.com/296675>

[native] Fix UAF in CopyTextureToTexture

---


Expand for full commit details
```
     
    This was happening with 
    use_blit_for_depth_texture_to_texture_copy_to_nonzero_subresource 
    enabled, and doing a 0-depth (no-op) copy, then making sure that the src 
    and dst texture refs go to 0 so they are deleted, and then submitting. 
    The bug was that the raw texture pointers were being added 
    CommandEncoder::mTopLevelTextures but without the texture refs being 
    also stored in a command 
     
    Fixed by ensuring we only take the BlitDepthToDepth path if 
    depthOrArrayLayers > 1. 
     
    Added a validation test that reproduced the UAF with ASAN before my fix, 
    and no longer with my fix. 
     
    Bug: 489585038 
    Change-Id: I390b09bbb69ed0ceffbec2017ec7556a05a023e3 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/296675 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>

```

---

Files:

- M `src/dawn/native/BlitDepthToDepth.cpp`
- M `src/dawn/native/CommandAllocator.h`
- M `src/dawn/native/CommandEncoder.cpp`
- M `src/dawn/tests/unittests/validation/CopyCommandsValidationTests.cpp`

---

Hash: 6ec9bf51b0952b13848c8c7c16c54780e74e2a42  

Date: Thu Mar 12 17:23:54 2026


---

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7662818>

Roll Dawn from c4a63a567b25 to 6ec9bf51b095 (3 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/c4a63a567b25..6ec9bf51b095 
     
    2026-03-12 amaiorano@google.com [native] Fix UAF in CopyTextureToTexture 
    2026-03-12 jrprice@google.com [ir] Change bitcast to a builtin function 
    2026-03-12 jrprice@google.com [ir] Add explicit template to bitcast disassembly 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,gman@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:489585038 
    Tbr: gman@google.com 
    Change-Id: I6a40f944049a082499e78591ff9975d36cc858ce 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7662818 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1598706}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [47b03c3fcb97d5d8cec3a53f72740df47e7921b7](https://chromiumdash.appspot.com/commit/47b03c3fcb97d5d8cec3a53f72740df47e7921b7)  

Date: Thu Mar 12 21:53:27 2026


---

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489585038)*
