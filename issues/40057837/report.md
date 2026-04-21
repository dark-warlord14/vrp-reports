# Security: webgl heap-buffer-overflow LoadCompressedToNative

| Field | Value |
|-------|-------|
| **Issue ID** | [40057837](https://issues.chromium.org/issues/40057837) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | jo...@google.com |
| **Created** | 2021-11-06 |
| **Bounty** | $2,000.00 |

## Description

Tested on Version asan-linux-release-936833
Full asan log attached.

==96692==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6060001c4d00 at pc 0x55bd11753b67 bp 0x7ffc75b06310 sp 0x7ffc75b05ad8
READ of size 16 at 0x6060001c4d00 thread T0 (chrome)
    #0 0x55bd11753b66 in __asan_memcpy /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:22:3
    #1 0x7f48b9c5dfb5 in void angle::LoadCompressedToNative<4ul, 4ul, 1ul, 16ul>(unsigned long, unsigned long, unsigned long, unsigned char const*, unsigned long, unsigned long, unsigned char*, unsigned long, unsigned long) third_party/angle/src/image_util/loadimage.inc:128:13
    #2 0x7f48ba16e3b2 in rx::vk::ImageHelper::stageSubresourceUpdateImpl(rx::ContextVk*, gl::ImageIndex const&, gl::Extents const&, gl::Offset const&, gl::InternalFormat const&, gl::PixelUnpackState const&, rx::vk::DynamicBuffer*, unsigned int, unsigned char const*, rx::vk::Format const&, rx::vk::ImageAccess, unsigned int, unsigned int, unsigned int) third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:5598:5
    #3 0x7f48ba1713aa in rx::vk::ImageHelper::stageSubresourceUpdate(rx::ContextVk*, gl::ImageIndex const&, gl::Extents const&, gl::Offset const&, gl::InternalFormat const&, gl::PixelUnpackState const&, rx::vk::DynamicBuffer*, unsigned int, unsigned char const*, rx::vk::Format const&, rx::vk::ImageAccess) third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:5949:5
    #4 0x7f48ba087e1f in rx::TextureVk::setSubImageImpl(gl::Context const*, gl::ImageIndex const&, gl::Box const&, gl::InternalFormat const&, unsigned int, gl::PixelUnpackState const&, gl::Buffer*, unsigned char const*, rx::vk::Format const&) third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:552:9
    #5 0x7f48ba0890fd in setImageImpl third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:405:12
    #6 0x7f48ba0890fd in rx::TextureVk::setCompressedImage(gl::Context const*, gl::ImageIndex const&, unsigned int, gl::Extents const&, gl::PixelUnpackState const&, unsigned long, unsigned char const*) third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:358:12
    #7 0x7f48b9b5650e in gl::Texture::setCompressedImage(gl::Context*, gl::PixelUnpackState const&, gl::TextureTarget, int, unsigned int, gl::Extents const&, unsigned long, unsigned char const*) third_party/angle/src/libANGLE/Texture.cpp:1273:5
    #8 0x7f48b99ae90e in gl::Context::compressedTexImage3D(gl::TextureTarget, int, unsigned int, int, int, int, int, int, void const*) third_party/angle/src/libANGLE/Context.cpp:5040:5
    #9 0x7f48b99aea56 in gl::Context::compressedTexImage3DRobust(gl::TextureTarget, int, unsigned int, int, int, int, int, int, int, void const*) third_party/angle/src/libANGLE/Context.cpp:5056:5
    #10 0x7f48b99276a3 in GL_CompressedTexImage3DRobustANGLE third_party/angle/src/libGLESv2/entry_points_gles_ext_autogen.cpp:1974:22
    #11 0x55bd22e4218a in gl::GLApiBase::glCompressedTexImage3DRobustANGLEFn(unsigned int, int, unsigned int, int, int, int, int, int, int, void const*) ui/gl/gl_bindings_autogen_gl.cc:3401:3
    #12 0x55bd250ee7a1 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCompressedTexImage3D(unsigned int, int, unsigned int, int, int, int, int, int, int, void const*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:839:10
    #13 0x55bd25154dc1 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleCompressedTexImage3DBucket(unsigned int, void const volatile*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_handlers.cc:2542:10
    #14 0x55bd250c57ef in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858:20
    #15 0x55bd2553b575 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18

## Attachments

- [LoadCompressedToNative.html](attachments/LoadCompressedToNative.html) (text/plain, 692 B)
- [asan.log](attachments/asan.log) (text/plain, 11.2 KB)

## Timeline

### [Deleted User] (2021-11-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-06)

This has to be launched using --no-sandbox --disable-gpu-sandbox --disable-gpu

### cl...@chromium.org (2021-11-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5734587009138688.

### va...@chromium.org (2021-11-08)

Unable to repro with r920001 (95.0.4638.0)

### va...@chromium.org (2021-11-08)

I'm able to repro this with r929491 (96.0.4664.0) but having trouble getting a symbolized trace.

### va...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE]

### va...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ge...@chromium.org (2021-11-10)

[Empty comment from Monorail migration]

### ge...@chromium.org (2021-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### jo...@google.com (2021-11-18)

Working on the fix here: https://chromium-review.googlesource.com/c/angle/angle/+/3285808

### gi...@appspot.gserviceaccount.com (2021-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/870f458f507ff7ba0f67b28a30a27955ce79dd3e

commit 870f458f507ff7ba0f67b28a30a27955ce79dd3e
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Mon Nov 22 19:30:52 2021

Ignore the pixel unpack state for compressed textures.

From OpenGL ES 3 spec: All pixel storage modes are ignored when decoding
a compressed texture image
This was causing a bad access when calling compressedTexImage3D
with GL_UNPACK_IMAGE_HEIGHT greater than the image height.

Bug: chromium:1267496
Change-Id: I9b1f4c645548af64f2695fd23262225a1ad07cd7
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3296622
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/870f458f507ff7ba0f67b28a30a27955ce79dd3e/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/870f458f507ff7ba0f67b28a30a27955ce79dd3e/src/libANGLE/Context.cpp


### gi...@appspot.gserviceaccount.com (2021-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/70c2cd5a59993d30d0c9f36df12ffacfc4cedb45

commit 70c2cd5a59993d30d0c9f36df12ffacfc4cedb45
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Nov 25 21:32:20 2021

Roll ANGLE from e00ad443296e to 870f458f507f (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/e00ad443296e..870f458f507f

2021-11-25 jonahr@google.com Ignore the pixel unpack state for compressed textures.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC syoussefi@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1267496
Tbr: syoussefi@google.com
Change-Id: Ic66224f480eabce8baa5d35fb4def11b10afc578
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3302847
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#945486}

[modify] https://crrev.com/70c2cd5a59993d30d0c9f36df12ffacfc4cedb45/DEPS


### jo...@google.com (2021-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### su...@google.com (2021-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-29)

Requesting merge to stable M96 because latest trunk commit (945486) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (945486) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-29)

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-29)

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-11-29)

merge tentatively approved to M97; since approving in advance of merge questionnaire completion and this is a textually large fix, please ensure there are no stability issues or other concerns before merging; if there are no concerns, please merge to branch 4692 as soon as possible for this to be in tomorrow's beta cut. 

### am...@chromium.org (2021-11-29)

please ignore my comment about the fix size; sorry, was looking at the wrong commit for this one. Regardless, please ensure there are no stability concerns or other issues. thanks!! 

### jo...@google.com (2021-11-30)

This CL did reveal a new issue: https://bugs.chromium.org/p/angleproject/issues/detail?id=6738
It's in the tests added by this CL, and it looks to be a driver bug that may have always been present.
Given that, I think it's still overall a simple change and should be safe to land.

1. Fixes ASAN failure
2. https://chromium-review.googlesource.com/c/angle/angle/+/3296622
3. Yes
4. No
6. No

### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/0ea1b3451e8b5cba3d4d10a9cb16de072d0e7394

commit 0ea1b3451e8b5cba3d4d10a9cb16de072d0e7394
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Mon Nov 22 19:30:52 2021

[M97] Ignore the pixel unpack state for compressed textures.

From OpenGL ES 3 spec: All pixel storage modes are ignored when decoding
a compressed texture image
This was causing a bad access when calling compressedTexImage3D
with GL_UNPACK_IMAGE_HEIGHT greater than the image height.

Bug: chromium:1267496
Change-Id: I9b1f4c645548af64f2695fd23262225a1ad07cd7
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3296622
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 870f458f507ff7ba0f67b28a30a27955ce79dd3e)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309098
Reviewed-by: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/0ea1b3451e8b5cba3d4d10a9cb16de072d0e7394/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/0ea1b3451e8b5cba3d4d10a9cb16de072d0e7394/src/libANGLE/Context.cpp


### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/891020ed64d418a738b867e5c7e7cb1d0e40c892

commit 891020ed64d418a738b867e5c7e7cb1d0e40c892
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Mon Nov 22 19:30:52 2021

[M96] Ignore the pixel unpack state for compressed textures.

From OpenGL ES 3 spec: All pixel storage modes are ignored when decoding
a compressed texture image
This was causing a bad access when calling compressedTexImage3D
with GL_UNPACK_IMAGE_HEIGHT greater than the image height.

Bug: chromium:1267496
Change-Id: I9b1f4c645548af64f2695fd23262225a1ad07cd7
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3296622
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 870f458f507ff7ba0f67b28a30a27955ce79dd3e)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309097
Reviewed-by: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/891020ed64d418a738b867e5c7e7cb1d0e40c892/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/891020ed64d418a738b867e5c7e7cb1d0e40c892/src/libANGLE/Context.cpp


### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/0ea1b3451e8b5cba3d4d10a9cb16de072d0e7394

commit 0ea1b3451e8b5cba3d4d10a9cb16de072d0e7394
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Mon Nov 22 19:30:52 2021

[M97] Ignore the pixel unpack state for compressed textures.

From OpenGL ES 3 spec: All pixel storage modes are ignored when decoding
a compressed texture image
This was causing a bad access when calling compressedTexImage3D
with GL_UNPACK_IMAGE_HEIGHT greater than the image height.

Bug: chromium:1267496
Change-Id: I9b1f4c645548af64f2695fd23262225a1ad07cd7
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3296622
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 870f458f507ff7ba0f67b28a30a27955ce79dd3e)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309098
Reviewed-by: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/0ea1b3451e8b5cba3d4d10a9cb16de072d0e7394/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/0ea1b3451e8b5cba3d4d10a9cb16de072d0e7394/src/libANGLE/Context.cpp


### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2d41e0f7427b378cbebe23965f31716885c77f14

commit 2d41e0f7427b378cbebe23965f31716885c77f14
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Tue Nov 30 21:14:03 2021

Rework compressed texture pixel unpack state handling.

Compressed images do not use the pixel unpack parameters. Instead of
handling this in Context, move this to formatutils, where it's already
handled for the 2D case. Also, update the test to generate an ASAN error
if not ignored for the 2D case.

Bug: chromium:1267496
Change-Id: Ib93bae00a2b0b75eafd74c267f737da225afd993
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3308825
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/2d41e0f7427b378cbebe23965f31716885c77f14/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/2d41e0f7427b378cbebe23965f31716885c77f14/src/libANGLE/formatutils.cpp


### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/65ec75ce44893103382bc91e5d5d0fb143261fb3

commit 65ec75ce44893103382bc91e5d5d0fb143261fb3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 02 00:20:32 2021

Roll ANGLE from 8f6f5a4bb28d to 2d41e0f7427b (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/8f6f5a4bb28d..2d41e0f7427b

2021-12-01 jonahr@google.com Rework compressed texture pixel unpack state handling.

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
Bug: chromium:1267496
Tbr: ynovikov@google.com
Change-Id: I5673f209e8889f58c6447fda4aae5672db32a871
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3312002
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#947276}

[modify] https://crrev.com/65ec75ce44893103382bc91e5d5d0fb143261fb3/DEPS


### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-06)

ClusterFuzz testcase 5734587009138688 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### am...@google.com (2021-12-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-06)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. Thank you for your continued efforts and nice work! 

### jo...@google.com (2021-12-07)

The clusterfuzz failure on Dec 6 was a bad build, and not an actual test crash. I asked clusterfuzz to repro the task to see if it can get a real run in.

### am...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2022-06-22)

[Empty comment from Monorail migration]

### kb...@chromium.org (2022-06-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1267496?no_tracker_redirect=1

[Monorail blocking: crbug.com/angleproject/6738, crbug.com/angleproject/7457, crbug.com/chromium/1335688]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057837)*
