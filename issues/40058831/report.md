# Use After Free in TextureVk::releaseAndDeleteImageAndViews

| Field | Value |
|-------|-------|
| **Issue ID** | [40058831](https://issues.chromium.org/issues/40058831) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sj...@gmail.com |
| **Assignee** | yu...@google.com |
| **Created** | 2022-02-19 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36

Steps to reproduce the problem:
1. run poc.html with '--no-sandbox --disable-gpu' option on Linux Chromium Dev Channel.
2.
3.

What is the expected behavior?

What went wrong?
## Title

- Use After Free in TextureVk::releaseAndDeleteImageAndViews

## Test environment

- Chromium Version

  - Chromium 100.0.4867.0 (Developer Build, 966488)
  - Chromium 100.0.4892.0 (Developer Build, 971463)

- OS : Ubuntu 20.04.3 LTS 64bit

- ** Run Option **

  - ./chrome --disable-gpu --no-sandbox http://localhost:8000/poc.html

## Credit
	- Jeonghoon Shin(@singi21a) at Theori

## Analysis

- https://source.chromium.org/chromium/chromium/src/+/f996d4d879434de5056e3210c8d41d28d0f15ae2:third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp;l=1481

  ```C++
  void TextureVk::releaseAndDeleteImageAndViews(ContextVk *contextVk)
  {
      if (mImage)
      {
          releaseStagedUpdates(contextVk); //[1]
          releaseImage(contextVk);
          mImageObserverBinding.bind(nullptr);
          mRequiresMutableStorage = false;
          mRequiredImageAccess    = vk::ImageAccess::SampleOnly;
          mImageCreateFlags       = 0;
          SafeDelete(mImage);
      }
      mBufferViews.release(contextVk);
      mRedefinedLevels.reset();
  }
  ```

  The above method is called when the texture is destroyed. In the `[1]`, call the `releaseStagedUpdates` method.

- https://source.chromium.org/chromium/chromium/src/+/f996d4d879434de5056e3210c8d41d28d0f15ae2:third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp;l=4737;bpv=1

```c++
void ImageHelper::releaseStagedUpdates(RendererVk *renderer)
{
    ASSERT(validateSubresourceUpdateRefCountsConsistent());

    // Remove updates that never made it to the texture.
    for (std::vector<SubresourceUpdate> &levelUpdates : mSubresourceUpdates)
    {
        for (SubresourceUpdate &update : levelUpdates)
        {
            update.release(renderer); //[2]
        }
    }

    ASSERT(validateSubresourceUpdateRefCountsConsistent());

    mSubresourceUpdates.clear();
    mCurrentSingleClearValue.reset();
}
```

In the above code,  `ImageHelper::SubresourceUpdate::release` is called `[2]`. When calling this method, Passes the already freed `renderer` object as a method argument. 

The following is the `SubresourceUpdate::release` method.

* https://source.chromium.org/chromium/chromium/src/+/f996d4d879434de5056e3210c8d41d28d0f15ae2:third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp;l=8329

  ```c++
  void ImageHelper::SubresourceUpdate::release(RendererVk *renderer)
  {
      if (updateSource == UpdateSource::Image)
      {
          refCounted.image->releaseRef();

          if (!refCounted.image->isReferenced())
          {
              // Staging images won't be used in render pass attachments.
              refCounted.image->get().releaseImage(renderer);
              refCounted.image->get().releaseStagedUpdates(renderer);
              SafeDelete(refCounted.image);
          }

          refCounted.image = nullptr;
      }
      else if (updateSource == UpdateSource::Buffer && refCounted.buffer != nullptr)
      {
          refCounted.buffer->releaseRef();

          if (!refCounted.buffer->isReferenced())
          {
              refCounted.buffer->get().release(renderer); //[3] UAF occur
              SafeDelete(refCounted.buffer);
          }

          refCounted.buffer = nullptr;
      }
  }
  ```

  In the comment `[3]`, Use After Free occurs when accessing a `renderer` object that has already been freed.

## PoC

- please refer to attached files.

## ASan log
- please refer to attached files.

Did this work before? N/A 

Chrome version: 100.0.4892.0  Channel: dev
OS Version: 20.04

## Attachments

- [report.md](attachments/report.md) (text/plain, 3.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 2.1 KB)
- [asan_log.txt](attachments/asan_log.txt) (text/plain, 14.6 KB)
- [asan-log-with-line_number.txt](attachments/asan-log-with-line_number.txt) (text/plain, 24.3 KB)

## Timeline

### [Deleted User] (2022-02-19)

[Empty comment from Monorail migration]

### sj...@gmail.com (2022-02-20)

Attaching an ASAN log file with additional line numbers. 

Those logs were gets from chromium build commit c89b9b4b8396352f855bc8ee4e26add967c15d6b.

### sj...@gmail.com (2022-02-22)

Hello? 


### da...@chromium.org (2022-02-22)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE]

### da...@chromium.org (2022-02-22)

On M96 I am just getting OOM:

[23484:23484:0222/215620.943840:ERROR:gl_utils.cc(314)] [.WebGL-0x61b000008580] GL_OUT_OF_MEMORY: Internal Vulkan error (-2): A device memory allocation has failed.
[23484:23484:0222/215620.966062:ERROR:gl_utils.cc(318)] [.WebGL-0x61b000008580]GL Driver Message (OpenGL, Performance, GL_CLOSE_PATH_NV, High): GPU stall due to ReadPixels


### da...@chromium.org (2022-02-22)

On M98 I get the same. So I am unable to reproduce. Any suggestions?

### sj...@gmail.com (2022-02-22)

Hi, 

As I wrote in test environment, it only works with the current dev version of chromium.

Finally, it crashes on commit 102bfe9f38a5d0239f58db09ce0375a60e2f01a9.

### [Deleted User] (2022-02-22)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-02-23)

Ah I saw only this: UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36

Thanks, will give it a go.

### da...@chromium.org (2022-02-23)

I can repro in dev (M100) but not M99, with --disable-gpu. I believe this is Angle not swiftshader tho?

### [Deleted User] (2022-02-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-24)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-24)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2022-02-24)

[Empty comment from Monorail migration]

### sr...@google.com (2022-02-24)

M100 branched last week and beta promotion is coming up next week, this bug is marked as beta blocker so please help get a change landed on trunk asap and ready to merge to M100 before next week monday ( Feb 28) so we can include in beta RC build

if this is not critical enough to block beta, please drop the RBB label

### jm...@chromium.org (2022-02-24)

Can anyone advise if this is critical enough to warrant RBB label, or if RBS would be sufficient? I'm not as familiar with the severity of this type of UAF.

### sr...@google.com (2022-02-24)

[Empty comment from Monorail migration]

### sr...@google.com (2022-02-24)

see https://crbug.com/chromium/1299211#c17

### da...@chromium.org (2022-02-24)

Shipping a known security vuln that is accessibly to the open web to our beta population is not great. As this won't get disclosed before stable, and the beta population is smaller, I could see this as an argument to not block Beta. Are high value targets running Beta? Depends who you want to compromise.

I don't see anything in the FAQ, maybe we have a policy for this.

### ad...@chromium.org (2022-02-24)

Yep this was labelled RBB because it was deemed Critical. Now this has been regraded as High, we won't block beta. Removing label. Obviously it would be better to fix it!

### jm...@chromium.org (2022-02-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2022-02-28)

JFYI comment https://crbug.com/chromium/1299211#c23 is correct according to our standards and per https://crbug.com/chromium/1299211#c10. As a High severity bug recently introduced, this will block M100 stable release pending a fix.

ANGLE folks: if you believe that this was introduced earlier (there seems to be some uncertainty) such that this isn't a recent regression, let us know so we can adjust labels.

### go...@chromium.org (2022-03-01)

Reminder M100 is already branched and Stable promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### [Deleted User] (2022-03-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-07)

hi ANGLE folks, friendly ping  and follow-up from comments 24 and 35, this issue is still labeled and considered as a stable release blocker for M100 Stable; Stable cut for M100 is Tuesday, 22 March. If this issue is indeed a recent regression, please ensure there is a fix landed with sufficient canary time in advance of this deadline. If this is not a recent regression, please let us know so we can update accordingly (and stop pinging y'all). TY! 


### yu...@google.com (2022-03-07)

I am not sure if this is a bug is introduced by a recent CL, maybe Jamie can add on more details. But I am working on a fix and aim to land it by end of this week (Mar 11th).

### jm...@chromium.org (2022-03-07)

I'm not sure if it's a regression from a recent CL. It might be because of the switch to Vulkan SwiftShader which exposed a new API exploit surface compared the the prior implementation. Amy, we should have it done by 22 March.

### am...@chromium.org (2022-03-07)

 Yuxin and Jamie, thank you both so much for the insight and update. Much appreciated! 

### jm...@chromium.org (2022-03-09)

[Empty comment from Monorail migration]

### sr...@google.com (2022-03-14)

we need to land before March 22, so we can get verification and ready to merge to M100 on March 22.

### gi...@appspot.gserviceaccount.com (2022-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/5c29d795d1625f71ac6999f157b6f3bba79d5256

commit 5c29d795d1625f71ac6999f157b6f3bba79d5256
Author: Yuxin Hu <yuxinhu@google.com>
Date: Mon Feb 28 23:56:46 2022

Flush the texture staged updates when destroying context share group

If we are using the extension EGL_ANGLE_display_texture_share_group,
flush the texture staged updates upon destroying the context. With the
extension enabled, the texture could still be alive when both context
and its' EGL::ShareGroup are destroyed. If we have staged updates not
yet flushed, the updates will keep the ShareGroupVk bufferpool occupied,
causing an error upon ShareGroupVk::onDestroy().

Bug: chromium:1299211
Change-Id: I260de93c3a3099e023e31acbe017803e824459ad
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3495879
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Yuxin Hu <yuxinhu@google.com>

[modify] https://crrev.com/5c29d795d1625f71ac6999f157b6f3bba79d5256/src/tests/egl_tests/EGLContextSharingTest.cpp
[modify] https://crrev.com/5c29d795d1625f71ac6999f157b6f3bba79d5256/src/libANGLE/Texture.cpp
[modify] https://crrev.com/5c29d795d1625f71ac6999f157b6f3bba79d5256/src/libANGLE/renderer/metal/TextureMtl.mm
[modify] https://crrev.com/5c29d795d1625f71ac6999f157b6f3bba79d5256/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/5c29d795d1625f71ac6999f157b6f3bba79d5256/src/libANGLE/angletypes.h
[modify] https://crrev.com/5c29d795d1625f71ac6999f157b6f3bba79d5256/src/libANGLE/Context.cpp


### am...@chromium.org (2022-03-16)

as per yuxinhu@, fix has been validated in ANGLE 

### [Deleted User] (2022-03-16)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M100. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-16)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/1dc9f1267830308d60221febe342b239c79105da

commit 1dc9f1267830308d60221febe342b239c79105da
Author: Yuxin Hu <yuxinhu@google.com>
Date: Wed Mar 16 19:29:26 2022

Revert "Flush the texture staged updates when destroying context share group"

This reverts commit 5c29d795d1625f71ac6999f157b6f3bba79d5256.

Reason for revert: this is causing some test failures on chromium and blocking the angle-chromium auto roller job: https://chromium-review.googlesource.com/c/chromium/src/+/3529771/

Original change's description:
> Flush the texture staged updates when destroying context share group
>
> If we are using the extension EGL_ANGLE_display_texture_share_group,
> flush the texture staged updates upon destroying the context. With the
> extension enabled, the texture could still be alive when both context
> and its' EGL::ShareGroup are destroyed. If we have staged updates not
> yet flushed, the updates will keep the ShareGroupVk bufferpool occupied,
> causing an error upon ShareGroupVk::onDestroy().
>
> Bug: chromium:1299211
> Change-Id: I260de93c3a3099e023e31acbe017803e824459ad
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3495879
> Reviewed-by: Charlie Lao <cclao@google.com>
> Reviewed-by: Jamie Madill <jmadill@chromium.org>
> Commit-Queue: Yuxin Hu <yuxinhu@google.com>

Bug: chromium:1299211
Change-Id: I214161d6a8aec834e1efc5fc9d2479e62e3bfae0
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3530505
Auto-Submit: Yuxin Hu <yuxinhu@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/1dc9f1267830308d60221febe342b239c79105da/src/tests/egl_tests/EGLContextSharingTest.cpp
[modify] https://crrev.com/1dc9f1267830308d60221febe342b239c79105da/src/libANGLE/Texture.cpp
[modify] https://crrev.com/1dc9f1267830308d60221febe342b239c79105da/src/libANGLE/renderer/metal/TextureMtl.mm
[modify] https://crrev.com/1dc9f1267830308d60221febe342b239c79105da/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/1dc9f1267830308d60221febe342b239c79105da/src/libANGLE/angletypes.h
[modify] https://crrev.com/1dc9f1267830308d60221febe342b239c79105da/src/libANGLE/Context.cpp


### jm...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9b1219a869bd9b469bac758bc9f8463b1361b52e

commit 9b1219a869bd9b469bac758bc9f8463b1361b52e
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Mar 17 00:45:04 2022

Roll ANGLE from 3739a195c2df to d867ddbbb1b8 (26 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/3739a195c2df..d867ddbbb1b8

2022-03-16 m.maiya@samsung.com Doc: Update supported EGL minor version
2022-03-16 yuxinhu@google.com Revert "Flush the texture staged updates when destroying context share group"
2022-03-16 lubosz.sarnecki@collabora.com FrameCapture: Add override for Glsizei* types.
2022-03-16 antonio.caggiano@collabora.com Vulkan: VkFormat/DrmFourCC
2022-03-16 romanl@google.com angle_system_info_test also exports androidSdkLevel
2022-03-16 romanl@google.com angle_system_info_test passes json via file
2022-03-16 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from a11411926c31 to 51988dcdccbf (9 revisions)
2022-03-16 yahan@google.com Do not copy parent layer frame position
2022-03-15 cclao@google.com Vulkan: Update mCurrentElementArrayBuffersync based on dirty bit
2022-03-15 yuxinhu@google.com Flush the texture staged updates when destroying context share group
2022-03-15 b.schade@samsung.com Remove invalid validation check on compressed texture formats
2022-03-15 cclao@google.com Vulkan: Handle the case where the bound buffer is empty
2022-03-15 lubosz.sarnecki@collabora.com FrameCapture: Skip invalid VertexAttribPointer calls in MEC.
2022-03-15 antonio.caggiano@collabora.com Vulkan: VkFormat/DrmFourCC
2022-03-15 jmadill@chromium.org Vulkan: Temporarily suppress 3 perf counter tests on P6.
2022-03-15 jmadill@chromium.org Revert "Vulkan: VkFormat/DrmFourCC"
2022-03-15 lexa.knyazev@gmail.com Skip no-op base instance draw calls
2022-03-15 lexa.knyazev@gmail.com Fix typo in DrawElementsInstancedBaseVertexBaseInstanceANGLE
2022-03-15 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from ffa866a5ae9e to 45902868a797 (562 revisions)
2022-03-15 b.schade@samsung.com Add usage of Spirv through glslang build flag
2022-03-14 kkinnunen@apple.com Add device id as a part of the key in EGLDisplay cache
2022-03-14 antonio.caggiano@collabora.com Vulkan: VkFormat/DrmFourCC
2022-03-14 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 2d9abfbddc1b to a11411926c31 (18 revisions)
2022-03-14 jmadill@chromium.org Fix crash when pausing XFB then deleting a buffer.
2022-03-14 cclao@google.com Vulkan: Fix another corner case of mCurrentElementArrayBuffer
2022-03-14 angle-autoroll@skia-public.iam.gserviceaccount.com Roll VK-GL-CTS from f7e842466e0a to 8252a3d3cdd3 (8 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jmadill@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1296467,chromium:1299211,chromium:1299261,chromium:1305190
Tbr: jmadill@google.com
Test: Test: angle_end2end_tests --gtest_filter="VertexAttributeTestES3.InvalidAttribPointer/*"
Test: Test: capture_replay_tests.py --gtest_filter=FenceSyncTest.NullLength/*
Test: Test: gtest_filter=*DXT1CompressedTextureTest.NonBlockSizesMipLevels*
Test: Test: when using ANGLE (with metal or swiftshader backend) with
Change-Id: I52ffe787d20dd083af8efe1bdef05616ac611f55
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3530116
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#981945}

[modify] https://crrev.com/9b1219a869bd9b469bac758bc9f8463b1361b52e/DEPS


### am...@chromium.org (2022-03-21)

cc'ing Srinivas for M100 Desktop, Krishna for M100 Android (as this is in ANGLE, not Swiftshader and would impact Android) 

### [Deleted User] (2022-03-22)

yuxinhu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/1099b5ef2279cfe1988a39c8e011aada59c650f1

commit 1099b5ef2279cfe1988a39c8e011aada59c650f1
Author: Yuxin Hu <yuxinhu@google.com>
Date: Thu Mar 17 17:20:44 2022

Vulkan: Fix invalid access with display texture share group.

Create bufferpool that owns by RendererVk.
If we are using EGL_ANGLE_display_texture_share_group
extension, use the bufferpool owned RendererVk,
otherwise, use the bufferpool owned by EGL::ShareGroup.
The bufferpool lifetime will remain consistent with
texture lifetime.

Bug: chromium:1299211
Change-Id: Ie4e87cea1dfd20dabab24e2afed6ddd92e469888
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3531155
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/renderer/vulkan/DisplayVk.h
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/renderer/vulkan/RendererVk.cpp
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/renderer/vulkan/RendererVk.h
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/renderer/vulkan/vk_utils.h
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/renderer/vulkan/vk_utils.cpp
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/State.cpp
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/tests/egl_tests/EGLContextSharingTest.cpp
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/renderer/vulkan/DisplayVk.cpp
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/1099b5ef2279cfe1988a39c8e011aada59c650f1/src/libANGLE/State.h


### gi...@appspot.gserviceaccount.com (2022-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0a90b3298e9e0bccaca7b84e0bd8166765da2a1f

commit 0a90b3298e9e0bccaca7b84e0bd8166765da2a1f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Mar 22 22:58:25 2022

Roll ANGLE from e7f29440f025 to 1099b5ef2279 (4 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/e7f29440f025..1099b5ef2279

2022-03-22 yuxinhu@google.com Vulkan: Fix invalid access with display texture share group.
2022-03-22 ynovikov@chromium.org Roll chromium_revision 3e4963702e..384f873e09 (982601:983904)
2022-03-22 ianelliott@google.com Add back Pixel 6-specific dEQP FAIL suppression
2022-03-22 syoussefi@chromium.org Vulkan: Fix invalidate of attachments with emulated format

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1299211
Tbr: ynovikov@google.com
Change-Id: I6c98a6e045f55a2af96857bee69ba447208c9a9f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3543677
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#984072}

[modify] https://crrev.com/0a90b3298e9e0bccaca7b84e0bd8166765da2a1f/DEPS


### go...@chromium.org (2022-03-23)

Looks like this will need a merge to M101 as well. 


### [Deleted User] (2022-03-23)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2022-03-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/73ec28af7ab9cef5624474ea975daa2c2c10cb5c

commit 73ec28af7ab9cef5624474ea975daa2c2c10cb5c
Author: Shrek Shao <shrekshao@google.com>
Date: Wed Mar 23 21:13:45 2022

Revert "Vulkan: Fix invalid access with display texture share group."

This reverts commit 1099b5ef2279cfe1988a39c8e011aada59c650f1.

Reason for revert: suspect culprit of 1309304

Original change's description:
> Vulkan: Fix invalid access with display texture share group.
>
> Create bufferpool that owns by RendererVk.
> If we are using EGL_ANGLE_display_texture_share_group
> extension, use the bufferpool owned RendererVk,
> otherwise, use the bufferpool owned by EGL::ShareGroup.
> The bufferpool lifetime will remain consistent with
> texture lifetime.
>
> Bug: chromium:1299211
> Change-Id: Ie4e87cea1dfd20dabab24e2afed6ddd92e469888
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3531155
> Reviewed-by: Charlie Lao <cclao@google.com>
> Reviewed-by: Geoff Lang <geofflang@chromium.org>
> Commit-Queue: Geoff Lang <geofflang@chromium.org>

Bug: chromium:1299211, 1309304
Change-Id: Ibdc119ef6bb52352858114d72a0f1c0edcd4da5e
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3546288
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Shrek Shao <shrekshao@google.com>
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>

[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/renderer/vulkan/RendererVk.cpp
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/renderer/vulkan/DisplayVk.h
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/renderer/vulkan/vk_utils.h
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/renderer/vulkan/RendererVk.h
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/renderer/vulkan/vk_utils.cpp
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/State.cpp
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/tests/egl_tests/EGLContextSharingTest.cpp
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/renderer/vulkan/DisplayVk.cpp
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/73ec28af7ab9cef5624474ea975daa2c2c10cb5c/src/libANGLE/State.h


### gi...@appspot.gserviceaccount.com (2022-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca2b632ae54d5203242b70c98bdc08789c7bac3d

commit ca2b632ae54d5203242b70c98bdc08789c7bac3d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Mar 23 23:55:16 2022

Roll ANGLE from 09f55382dac4 to 73ec28af7ab9 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/09f55382dac4..73ec28af7ab9

2022-03-23 shrekshao@google.com Revert "Vulkan: Fix invalid access with display texture share group."

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1299211,chromium:1309304
Tbr: ynovikov@google.com
Change-Id: I959926f7ed4ffd24b31615c115d36a59e413f906
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3547440
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#984603}

[modify] https://crrev.com/ca2b632ae54d5203242b70c98bdc08789c7bac3d/DEPS


### jm...@chromium.org (2022-03-24)

[Empty comment from Monorail migration]

### ad...@google.com (2022-03-24)

Approving merge of https://crbug.com/chromium/1299211#c43 to M100 (branch 4896) and M101 (branch 4951). The revert was due to a test which relates to a pre-existing (separate) security bug which was just made more visible by the CL, but is not new. A CL is going to land which is going to disable the problematic test.

### gi...@appspot.gserviceaccount.com (2022-03-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced

commit cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced
Author: Yuxin Hu <yuxinhu@google.com>
Date: Thu Mar 24 20:19:16 2022

[M100] Vulkan: Fix invalid access with display texture share group.

Create bufferpool that owns by RendererVk.
If we are using EGL_ANGLE_display_texture_share_group
extension, use the bufferpool owned RendererVk,
otherwise, use the bufferpool owned by EGL::ShareGroup.
The bufferpool lifetime will remain consistent with
texture lifetime.

Bug: chromium:1299211
Change-Id: Ie4e87cea1dfd20dabab24e2afed6ddd92e469888
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3531155
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>

Bug: chromium:1299211
Change-Id: I4b8f5bcb30297f2c5f24e02404fd96011f9d843b
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3550041
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Yuxin Hu <yuxinhu@google.com>

[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/renderer/vulkan/DisplayVk.h
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/renderer/vulkan/RendererVk.cpp
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/renderer/vulkan/vk_utils.h
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/renderer/vulkan/RendererVk.h
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/renderer/vulkan/vk_utils.cpp
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/State.cpp
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/tests/egl_tests/EGLContextSharingTest.cpp
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/renderer/vulkan/DisplayVk.cpp
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/cc8b741c6ba4cf3cd56d6bc1173b029c816f8ced/src/libANGLE/State.h


### gi...@appspot.gserviceaccount.com (2022-03-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001

commit cdd97fb81b29fe34cb09fba70b2c4f212fd3c001
Author: Yuxin Hu <yuxinhu@google.com>
Date: Thu Mar 24 17:41:30 2022

Reland "Vulkan: Fix invalid access with display texture share group."

This is a reland of 1099b5ef2279cfe1988a39c8e011aada59c650f1.

Original change's description:
> Vulkan: Fix invalid access with display texture share group.

> Create bufferpool that owns by RendererVk.
> If we are using EGL_ANGLE_display_texture_share_group
> extension, use the bufferpool owned RendererVk,
> otherwise, use the bufferpool owned by EGL::ShareGroup.
> The bufferpool lifetime will remain consistent with
> texture lifetime.

> Bug: chromium:1299211
> Change-Id: Ie4e87cea1dfd20dabab24e2afed6ddd92e469888
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3531155
> Reviewed-by: Charlie Lao <cclao@google.com>
> Reviewed-by: Geoff Lang <geofflang@chromium.org>
> Commit-Queue: Geoff Lang <geofflang@chromium.org>

Bug: chromium:1299211
Change-Id: I4b8f5bcb30297f2c5f24e02404fd96011f9d843b
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3550038
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/renderer/vulkan/DisplayVk.h
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/renderer/vulkan/RendererVk.cpp
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/renderer/vulkan/RendererVk.h
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/renderer/vulkan/vk_utils.h
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/renderer/vulkan/vk_utils.cpp
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/State.cpp
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/tests/egl_tests/EGLContextSharingTest.cpp
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/renderer/vulkan/DisplayVk.cpp
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/cdd97fb81b29fe34cb09fba70b2c4f212fd3c001/src/libANGLE/State.h


### gi...@appspot.gserviceaccount.com (2022-03-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2ab7f399a56659d5e45c9a1cbe55841e95c97407

commit 2ab7f399a56659d5e45c9a1cbe55841e95c97407
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Mar 25 05:26:58 2022

Roll ANGLE from dd4b2c2164a8 to cdd97fb81b29 (2 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/dd4b2c2164a8..cdd97fb81b29

2022-03-25 yuxinhu@google.com Reland "Vulkan: Fix invalid access with display texture share group."
2022-03-25 ianelliott@google.com Remove unnecessary suppressions for Pixel6 dEQP tests

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1299211
Tbr: ynovikov@google.com
Change-Id: I5281eef2b257696c50fbb1d2f5d29bfa4964a784
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3551863
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#985181}

[modify] https://crrev.com/2ab7f399a56659d5e45c9a1cbe55841e95c97407/DEPS


### yu...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-25)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-27)

[Empty comment from Monorail migration]

### pb...@google.com (2022-03-28)

[Bulk Edit] Your change has been approved for M101 branch,please go ahead and merge the CL's to M101 branch manually asap(Refer to go/chrome-branches for branch info) so that they would be part of this week's first M101 Dev/Beta release.

### [Deleted User] (2022-03-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346

commit a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346
Author: Yuxin Hu <yuxinhu@google.com>
Date: Thu Mar 24 17:41:30 2022

[M101] Vulkan: Fix invalid access with DisplayTextureShareGroup.

Create bufferpool that owns by RendererVk.
If we are using EGL_ANGLE_display_texture_share_group
extension, use the bufferpool owned RendererVk,
otherwise, use the bufferpool owned by EGL::ShareGroup.
The bufferpool lifetime will remain consistent with
texture lifetime.

Bug: chromium:1299211
Change-Id: I4b8f5bcb30297f2c5f24e02404fd96011f9d843b
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3550038
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3554362
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Yuxin Hu <yuxinhu@google.com>

[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/renderer/vulkan/RendererVk.cpp
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/renderer/vulkan/DisplayVk.h
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/renderer/vulkan/vk_utils.h
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/renderer/vulkan/RendererVk.h
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/renderer/vulkan/vk_utils.cpp
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/State.cpp
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/tests/egl_tests/EGLContextSharingTest.cpp
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/renderer/vulkan/DisplayVk.cpp
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/a3d35e42c9cdc2ebc40d1e960fd5f69baeeb0346/src/libANGLE/State.h


### am...@chromium.org (2022-03-29)

[Comment Deleted]

### [Deleted User] (2022-03-29)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-03-29)

[Comment Deleted]

### kb...@chromium.org (2022-03-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-29)

the bot was correct as this was a regression and did not impact stable 


### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Congratulations, Jeonghoon! The VRP Panel has decided to award you $10000 for this report. Thank you for your efforts in finding and reporting ANGLE security bugs and nice work! 

### sj...@gmail.com (2022-04-01)

Thanks a lot :)

### vo...@google.com (2022-04-01)

Not applicable to LTS-96 based on the https://crbug.com/chromium/1299211#c66.

### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1299211?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1309304]
[Monorail blocking: crbug.com/chromium/1311208]
[Monorail mergedwith: crbug.com/chromium/1302693, crbug.com/chromium/1305836]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058831)*
