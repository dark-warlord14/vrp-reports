# Chrome ANGLE Out-of-Bound in texStorage3D

| Field | Value |
|-------|-------|
| **Issue ID** | [40056920](https://issues.chromium.org/issues/40056920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | sj...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2021-08-18 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36

Steps to reproduce the problem:
1. run poc.html with chrome stable on win10 64
2.
3.

What is the expected behavior?

What went wrong?
# Title
    - Chrome ANGLE Out-of-Bound in texStorage3D

# Test Environment
    - window 10 64bit chrome 92.0.4515.131 Official Build (latest)

# Root Cause

crash occur to below method
```c++
inline void Initialize4ComponentData(size_t width, size_t height, size_t depth,
                                     uint8_t *output, size_t outputRowPitch, size_t outputDepthPitch)
{
    type writeValues[4] =
    {
        gl::bitCast<type>(firstBits),
        gl::bitCast<type>(secondBits),
        gl::bitCast<type>(thirdBits),
        gl::bitCast<type>(fourthBits),
    };

    for (size_t z = 0; z < depth; z++)
    {
        for (size_t y = 0; y < height; y++)
        {
            type *destRow = priv::OffsetDataPointer<type>(output, y, z, outputRowPitch, outputDepthPitch);
            for (size_t x = 0; x < width; x++)
            {
                type* destPixel = destRow + x * 4;

                // This could potentially be optimized by generating an entire row of initialization
                // data and copying row by row instead of pixel by pixel.
                memcpy(destPixel, writeValues, sizeof(type) * 4); //[1] crash here.
            }
        }
    }
}
```

this method called by texStorage3D of WebGL2 API.

the `destRow` is return by `priv::OffsetDataPointer` method using `y`, `z`.
and invalid memory (`destPixel` + `x`) access by memcpy method.

# windbg log

attached `windbg_log.txt`

# PoC

attached `poc.html`

Did this work before? N/A 

Chrome version: 92.0.4515.131  Channel: stable
OS Version: 10.0

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 552 B)
- [windbg_log.txt](attachments/windbg_log.txt) (text/plain, 5.9 KB)
- [windbg_log_with_symbol.txt](attachments/windbg_log_with_symbol.txt) (text/plain, 19.3 KB)
- [detail-angle-report.md](attachments/detail-angle-report.md) (text/plain, 3.0 KB)

## Timeline

### [Deleted User] (2021-08-18)

[Empty comment from Monorail migration]

### sj...@gmail.com (2021-08-18)

attached windbg log with symbol.

### sj...@gmail.com (2021-08-18)

Also, tested on chrome 92.0.4515.159 official build. Same crash with this version.

### sj...@gmail.com (2021-08-19)

In addition, a detail analysis report is attached.

### cl...@chromium.org (2021-08-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5069036038455296.

### pa...@chromium.org (2021-08-20)

Thank you for this well-written report and analysis!

This might? turn out to work on other platforms too, not sure.

It seems ClusterFuzz can't reproduce it, but the code looks vulnerable to me. cwallez, any chance you or a colleague could take a look? ANGLE should filter the unknown opcode, right? And/or the arithmetic could be checked or constrained?

If we can reproduce this, it's High (memory corruption in a sandboxed process, as usual).

Thanks!

[Monorail components: Blink>WebGL Blink>WebGPU]

### [Deleted User] (2021-08-20)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-08-20)

Probably best if someone on the ANGLE team looks at this. CCing folks

Removing WebGPU component since it's unrelated

[Monorail components: -Blink>WebGPU Internals>GPU>ANGLE]

### jm...@chromium.org (2021-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sj...@gmail.com (2021-09-01)

hello :) 

Any updates on this issue? I confirmed that it is also applied to chrome 93 Stable update today.

thanks!

### jm...@chromium.org (2021-09-01)

Looking now.

### gi...@appspot.gserviceaccount.com (2021-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/794b13ce9f874d472729ebd69897bc7ab9340a4b

commit 794b13ce9f874d472729ebd69897bc7ab9340a4b
Author: Jamie Madill <jmadill@chromium.org>
Date: Wed Sep 01 16:17:26 2021

D3D11: Fix overflow in GenerateInitialTextureData.

Our use of unchecked math was causing OOB accesses with very large
textures. Unfortunately it's not easy to make a passing test that
reproduces this OOB access.

Bug: chromium:1241036
Change-Id: Icd2749f5b3116bb51390ce769fef22c49a11f307
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3136733
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/794b13ce9f874d472729ebd69897bc7ab9340a4b/src/libANGLE/renderer/d3d/d3d11/renderer11_utils.cpp


### gi...@appspot.gserviceaccount.com (2021-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aa6d266ecd709a83d707a2212fa52135f7d02de4

commit aa6d266ecd709a83d707a2212fa52135f7d02de4
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Sep 02 21:59:24 2021

Roll ANGLE from 78e0ae81d924 to de09f8db317d (65 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/78e0ae81d924..de09f8db317d

2021-09-02 geofflang@chromium.org Revert "GL: Update StateManagerGL binding funcs to use ANGLE_GL_TRY"
2021-09-02 cclao@google.com Vulkan: Change TextureVk's vk::FormatID usage to angle::FormatID
2021-09-02 lubosz.sarnecki@collabora.com RendererVk: Skip VK_KHR_image_format_list on SwiftShader.
2021-09-02 jmadill@chromium.org D3D11: Fix overflow in GenerateInitialTextureData.
2021-09-02 cclao@google.com Vulkan: Store actualFormatID (not intendedFormat) in RenderPassDesc
2021-09-02 cclao@google.com Vulkan: Keep track of data format for staged updates for ImageHelper
2021-09-02 syoussefi@chromium.org Vulkan: Remove the forceCPUPathForCubeMapCopy workaround
2021-09-02 gert.wollny@collabora.com Capture/Replay: Change workdir for debug runs and annotation
2021-09-02 syoussefi@chromium.org Vulkan: SPIR-V Gen: Re-fix precision of constructors
2021-09-02 gert.wollny@collabora.com Capture/Replay: Update expectation for fixed test
2021-09-02 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from b75ca3758a80 to c82c59307208 (2 revisions)
2021-09-02 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from a5102f13fe96 to b5237d627f0d (446 revisions)
2021-09-02 gman@chromium.org Convert constructors to function calls where needed.
2021-09-02 gert.wollny@collabora.com Capture/Replay: Handle glInvalidateSubFramebuffer
2021-09-02 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from d54279d797f8 to 84f860ef94ee (1 revision)
2021-09-02 syoussefi@chromium.org Avoid redundant blend state dirty bit setting
2021-09-01 syoussefi@chromium.org Fix SeparateDeclarations vs struct specifiers
2021-09-01 jmadill@chromium.org Capture/Replay: Add uniforms to program serialization.
2021-09-01 jmadill@chromium.org Support syncing traces to experimental CIPD prefix.
2021-09-01 adkushwa@microsoft.com Implement onLabelUpdate method.
2021-09-01 jmadill@chromium.org Style cleanups in JsonSerializer.
2021-09-01 jmadill@chromium.org Traces: Move skia gold Python scripts.
2021-09-01 gert.wollny@collabora.com Capture/Replay: Update expectation bugs, remove passing test
2021-09-01 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 562b4d73eae2 to d54279d797f8 (4 revisions)
2021-09-01 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from a6ca3d4c0ccd to b75ca3758a80 (3 revisions)
2021-09-01 gert.wollny@collabora.com Capture/Replay: Clean up tests that pass and add new failures
2021-09-01 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from abe7c480d95d to a5102f13fe96 (417 revisions)
2021-09-01 cclao@google.com Vulkan: Remove mFormat from ImageHelper
2021-08-31 cclao@google.com Vulkan: Pass actualFormatID directly into ImageHelper::initExternal
2021-08-31 syoussefi@chromium.org Vulkan: SPIR-V Gen: Fix precision of constructors
2021-08-31 timvp@google.com Vulkan: Don't defer clear for read render target
2021-08-31 syoussefi@chromium.org Vulkan: SPIR-V Gen: Fix precision of imageLoad
2021-08-31 b.schade@samsung.com Allow image uniforms to be used in separable programs
2021-08-31 yuxinhu@google.com Improve Error Messaging
2021-08-31 geofflang@chromium.org GL: Update StateManagerGL binding funcs to use ANGLE_GL_TRY
2021-08-31 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 4c030a49cdb9 to 562b4d73eae2 (11 revisions)
2021-08-31 jmadill@chromium.org GetTexImage: Remove syncState calls & add early error exit.
2021-08-31 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from ca199aff3bc7 to abe7c480d95d (1237 revisions)
2021-08-31 cnorthrop@google.com Tests: Add Words With Friends 2 trace
2021-08-31 cnorthrop@google.com Capture/Replay: Set texture buffer offset alignment
2021-08-30 cnorthrop@google.com Tests: Add World of Kings trace
2021-08-30 ianelliott@google.com Split OWNERS by domain
2021-08-30 cnorthrop@google.com Vulkan: Fix VVL error regarding geometryStreams
2021-08-30 cclao@google.com Vulkan: Use angle::Format for ImageViewHelper class
2021-08-30 geofflang@google.com Roll third_party/vulkan_memory_allocator
2021-08-30 cclao@google.com Vulkan: Add ImageHelper::getIntendedFormatID()
2021-08-30 gert.wollny@collabora.com Capture/Replay: Show some expectation when skipped tests are run
2021-08-30 jmadill@chromium.org InitializeVariables: Init shader IO block outputs.
2021-08-30 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 3e5496ec4fdf to 4c030a49cdb9 (6 revisions)
2021-08-29 gert.wollny@collabora.com Capture/Replay: honor base level when serializing textures
2021-08-27 timvp@google.com Capture/Replay: Multi-Context Support
2021-08-27 gman@chromium.org Include globals when defering global initializers
2021-08-27 lexa.knyazev@gmail.com Cleanup ValidateES2TexImageParametersBase; update tests
2021-08-27 kbr@chromium.org Deduplicate autoroller docs.
2021-08-27 jmadill@chromium.org Capture/Replay: Allow serializing cube map array data.
2021-08-27 jmadill@chromium.org Capture/Replay: Serialize buffer texture buffer IDs.
2021-08-27 syoussefi@chromium.org Vulkan: SPIR-V Gen: Fix gl_PerVertex without clip/cull support
2021-08-27 lexa.knyazev@gmail.com Cleanup ValidateES2CopyTexImageParameters; add test
2021-08-27 jmadill@chromium.org infra: Disable perf tests on Win/Intel.
2021-08-27 jmadill@chromium.org Capture/Replay: Skip one additional ES3 test.
2021-08-27 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 518056981519 to a6ca3d4c0ccd (2 revisions)
2021-08-27 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 5e51e6f8ccd4 to 3e5496ec4fdf (6 revisions)
2021-08-27 lubosz.sarnecki@collabora.com SRGBFramebufferTest: Add test that used to fail on Vulkan.
2021-08-27 lubosz.sarnecki@collabora.com Reland "VulkanExternalHelper: Use VK_KHR_image_format_list extension."
2021-08-27 gert.wollny@collabora.com Capture/Replay: Handle glCopyTexture3DANGLE

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC geofflang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win-asan;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1164111,chromium:1216276,chromium:1233561,chromium:1237696,chromium:1241036,chromium:1245774
Tbr: geofflang@google.com
Test: Test: Fortnite MEC
Test: Test: World of Kings MEC
Test: Test: angle_perftests --gtest_filter="*words_with_friends_2*"
Test: Test: angle_perftests --gtest_filter="*world_of_kings*"
Change-Id: I3f22bed9c41278ede4d227d1bcaddc9271a0c83f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3139981
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#917844}

[modify] https://crrev.com/aa6d266ecd709a83d707a2212fa52135f7d02de4/DEPS


### jm...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

Requesting merge to extended stable M92 because latest trunk commit (917844) appears to be after extended stable branch point (885287).

Requesting merge to stable M93 because latest trunk commit (917844) appears to be after stable branch point (902210).

Requesting merge to beta M94 because latest trunk commit (917844) appears to be after beta branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-04)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-09-07)

1. yes
2. https://chromium-review.googlesource.com/c/angle/angle/+/3136733
3. yes
4. yes, M93
5. OOB access in GPU process from javascript WebGL API
6. no
7. n/a

### sr...@google.com (2021-09-07)

Merge approved for M94 branch:4606 please merge before 3pm PST today so this can go out in tomorrow beta release

### gi...@appspot.gserviceaccount.com (2021-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d64ef0c965c6bf943a10b71b751bf8d6411538c3

commit d64ef0c965c6bf943a10b71b751bf8d6411538c3
Author: Jamie Madill <jmadill@chromium.org>
Date: Wed Sep 01 16:17:26 2021

D3D11: Fix overflow in GenerateInitialTextureData.

Our use of unchecked math was causing OOB accesses with very large
textures. Unfortunately it's not easy to make a passing test that
reproduces this OOB access.

Bug: chromium:1241036
Change-Id: Icd2749f5b3116bb51390ce769fef22c49a11f307
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3136733
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 794b13ce9f874d472729ebd69897bc7ab9340a4b)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3145612
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/d64ef0c965c6bf943a10b71b751bf8d6411538c3/src/libANGLE/renderer/d3d/d3d11/renderer11_utils.cpp


### am...@chromium.org (2021-09-08)

merge approved for M93, please merge to branch 4577 by 2pm PDT tomorrow (Thursday) 9 September, so that this fix can be included in next week's stable security refresh; 
also, please go ahead and merge to M92 (branch 4515) as it is presently the Extended Stable channel as we transition to the 4W stable channel release cycle. Thanks! 

### am...@google.com (2021-09-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-08)

Congratulations! The VRP Panel has decided to award you $7500 for this report. Thank you for this report!

### sj...@gmail.com (2021-09-09)

thanks for reward :)

Credit : Jeonghoon Shin of Theori

thanks!


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4d7fd82c5d2b01aae414a0f3f6e7bf9f2f7a05a4

commit 4d7fd82c5d2b01aae414a0f3f6e7bf9f2f7a05a4
Author: Jamie Madill <jmadill@chromium.org>
Date: Wed Sep 01 16:17:26 2021

D3D11: Fix overflow in GenerateInitialTextureData.

Our use of unchecked math was causing OOB accesses with very large
textures. Unfortunately it's not easy to make a passing test that
reproduces this OOB access.

Bug: chromium:1241036
Change-Id: Icd2749f5b3116bb51390ce769fef22c49a11f307
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3136733
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 794b13ce9f874d472729ebd69897bc7ab9340a4b)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3149276
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/4d7fd82c5d2b01aae414a0f3f6e7bf9f2f7a05a4/src/libANGLE/renderer/d3d/d3d11/renderer11_utils.cpp


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/72473550f6ff98af986371f01820fefb2d6e164b

commit 72473550f6ff98af986371f01820fefb2d6e164b
Author: Jamie Madill <jmadill@chromium.org>
Date: Wed Sep 01 16:17:26 2021

D3D11: Fix overflow in GenerateInitialTextureData.

Our use of unchecked math was causing OOB accesses with very large
textures. Unfortunately it's not easy to make a passing test that
reproduces this OOB access.

Bug: chromium:1241036
Change-Id: Icd2749f5b3116bb51390ce769fef22c49a11f307
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3136733
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 794b13ce9f874d472729ebd69897bc7ab9340a4b)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3149277
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/72473550f6ff98af986371f01820fefb2d6e164b/src/libANGLE/renderer/d3d/d3d11/renderer11_utils.cpp


### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### sj...@gmail.com (2021-09-10)

Hi,
Is it possible to set embargo for this issue?

### am...@chromium.org (2021-09-10)

Hello, we can, but I'm presuming you no longer wish to be credited/attributed for this issue publicly despite your credit info in https://crbug.com/chromium/1241036#c26? 

### sj...@gmail.com (2021-09-10)

Ah sorry, i confused to another issue.

Please proceed to information #26. Thank you.

Regards

### am...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-13)

[Empty comment from Monorail migration]

### rz...@google.com (2021-09-16)

Marked as non applicable for M90-LTS because it affects only windows

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-12-20)

hi, OP- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1241036?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056920)*
