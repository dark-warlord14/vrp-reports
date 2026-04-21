# Heap-use-after-free in vk::Buffer::getOffsetPointer

| Field | Value |
|-------|-------|
| **Issue ID** | [40055268](https://issues.chromium.org/issues/40055268) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Vulkan |
| **Platforms** | Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | su...@chromium.org |
| **Created** | 2021-03-20 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5673171727220736

Fuzzer: attekett_dom_fuzzer
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x0001638bce01
Crash State:
  vk::Buffer::getOffsetPointer
  vk::GraphicsPipeline::getIndexBuffers
  CmdDrawIndexed::play
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=mac_asan_chrome&revision=862654

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5673171727220736

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5673171727220736 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2021-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-20)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2021-03-22)

This might affect more platforms than just macOS. If so, please add them. Thanks!

[Monorail components: Internals>GPU>Vulkan]

### cw...@chromium.org (2021-03-23)

This test case is using Canvas on Swiftshader, maybe Alexis you could take a look or find another owner?

### su...@chromium.org (2021-03-23)

Looks like this might be because what's mentioned in the warning:
VkMemoryAllocateInfo->pNext sType = 1000178000 (or VK_STRUCTURE_TYPE_IMPORT_MEMORY_HOST_POINTER_INFO_EXT)

We're not handling it in OpaqueFdAllocateInfo():
https://source.chromium.org/chromium/chromium/src/+/master:third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp;l=235

This had already been reported here, but I haven't had time to look into it yet:
https://bugs.chromium.org/p/chromium/issues/detail?id=1185611

### [Deleted User] (2021-03-23)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2021-03-27)

ClusterFuzz testcase 5673171727220736 is verified as fixed in https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=867019:867020

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-03-27)

[Empty comment from Monorail migration]

### ni...@google.com (2021-03-29)

The fix range only contains one change: "Roll Chrome Win64 PGO Profile"

Since this ClusterFuzz issue is Mac-specific, I'm puzzled about how this can can have fixed things. CC'ing some people might know whether or not Windows PGO data can have an effect here.

### th...@chromium.org (2021-03-29)

it can't

### ni...@google.com (2021-03-30)

I had ClusterFuzz redo whether the issue still reproduces, and it does. I'm not sure why it closed this as fixed.

We're still preoccupied with SwANGLE work for Windows and Linux, but should get around to taking a closer look at this once that's done.

### ge...@chromium.org (2021-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-06)

sugoi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-20)

sugoi: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-05-06)

sugoi@ please could you add an update?

Also, do you have any idea when this bug was introduced? It's marked as Security_Impact-Beta, and technically we should be re-adding ReleaseBlock-Stable because we don't release high severity security regressions - so we should delay M92 release to accommodate a fix. But I'm skeptical that Security_Impact-Beta is correct.

### su...@chromium.org (2021-05-06)

This is a bug using SwiftShader Vulkan on MacOS. This is not a shipped configuration.

### ad...@google.com (2021-05-06)

> This is a bug using SwiftShader Vulkan on MacOS. This is not a shipped configuration.

Great - adjusting labels appropriately.

### [Deleted User] (2021-05-06)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-06-03)

[gpu triage]

Should we downgrade to P2 or P3 if this is for a not-shipped configuration and it's deprioritized per c#12.

### su...@chromium.org (2021-06-03)

I just started working on MacOS failures this week. We need to fix this before we ship on MacOS, but this won't be M91, so I'll at least push it back to M92.

### gi...@appspot.gserviceaccount.com (2021-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4fbb6f436f5b5a1c59c31f7e6b03f6e47fc2cd17

commit 4fbb6f436f5b5a1c59c31f7e6b03f6e47fc2cd17
Author: Alexis Hetu <sugoi@google.com>
Date: Mon Jun 14 22:20:06 2021

Vulkan: Fix accessing index buffer with uninitialized memory

This was discovered by Clusterfuzz on MacOS. The issue was
that is index buffer of a draw indexed call was missing,
causing SwiftShader to access uninitialized memory, leading
to the ASAN crash. The missing index buffer was caused by
DIRTY_BIT_INDEX_BUFFER not being set. This was in turn
caused by ContextVk::flushDirtyGraphicsRenderPass() not
setting dirty bits not included in the dirtyBitMask,
despite needing to be set for future processing.

Bug: chromium:1183068
Bug: chromium:1190493
Change-Id: I65b398d8737b3df5fd51a03a2c8074a774a94a81
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2961690
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/4fbb6f436f5b5a1c59c31f7e6b03f6e47fc2cd17/src/libANGLE/renderer/vulkan/ContextVk.cpp


### gi...@appspot.gserviceaccount.com (2021-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/86d39730f5e696576e7fddc5a91aee173cc273f8

commit 86d39730f5e696576e7fddc5a91aee173cc273f8
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jun 15 10:31:42 2021

Roll ANGLE from 8333d061441e to af1eed2ef4cf (2 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/8333d061441e..af1eed2ef4cf

2021-06-15 syoussefi@chromium.org Vulkan: Generate gl_FragColor/Data declarations in AST
2021-06-15 sugoi@google.com Vulkan: Fix accessing index buffer with uninitialized memory

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ianelliott@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win-asan;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1183068,chromium:1190493
Tbr: ianelliott@google.com
Change-Id: I3cf7d7481da540eaf71b81102cff90e48f53a7af
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2962232
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#892520}

[modify] https://crrev.com/86d39730f5e696576e7fddc5a91aee173cc273f8/DEPS


### gi...@appspot.gserviceaccount.com (2021-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/c51c59c775abd902c3de0e515d906e559fed0f76

commit c51c59c775abd902c3de0e515d906e559fed0f76
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Jun 15 17:43:50 2021

Test for missing index dirty bit bug

Bug fixed in
https://chromium-review.googlesource.com/c/angle/angle/+/2961690
triggers only in the following situation:

- Context 1: draw indexed -> clears index dirty bit
- Context 1: change state in such a way that closing the render pass is
             deferred to dirty bit handling (for example, change FBO)
- Context 1: issue a non-indexed draw call.  This closes the render pass
             and starts a new one -> bug was that the index dirty bit
             was not set
- Context 2: flush the command buffer, which submits the previous render
             pass of context 1 (which contained vkCmdBindIndexBuffer).
             The primary command buffer is now reset.
- Context 1: issue an indexed draw call.  Since the index dirty bit was
             not set, this was missing the vkCmdBindIndexBuffer call.

This change implements a regression test based on the above scenario.

Bug: chromium:1183068
Bug: chromium:1190493
Change-Id: I729bd48cd6df2621ca763f6231023a52ac08b0fb
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2963836
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/c51c59c775abd902c3de0e515d906e559fed0f76/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/c51c59c775abd902c3de0e515d906e559fed0f76/src/tests/angle_end2end_tests_main.cpp
[modify] https://crrev.com/c51c59c775abd902c3de0e515d906e559fed0f76/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/c51c59c775abd902c3de0e515d906e559fed0f76/src/tests/test_expectations/GPUTestExpectationsParser.cpp
[modify] https://crrev.com/c51c59c775abd902c3de0e515d906e559fed0f76/src/tests/test_expectations/GPUTestExpectationsParser.h
[modify] https://crrev.com/c51c59c775abd902c3de0e515d906e559fed0f76/src/tests/test_utils/runner/TestSuite.h


### gi...@appspot.gserviceaccount.com (2021-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e7ff2ae3a73b9d0c8ba15141f5a1351b04b8dd0b

commit e7ff2ae3a73b9d0c8ba15141f5a1351b04b8dd0b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jun 23 15:23:30 2021

Roll ANGLE from 24155b13671f to 95603a5e736c (30 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/24155b13671f..95603a5e736c

2021-06-23 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 685eab2b2e45 to bbc918ca9021 (471 revisions)
2021-06-23 syoussefi@chromium.org Vulkan: Use pipeline statistics query to emulate primitives generated
2021-06-22 syoussefi@chromium.org Test runner: Capture test stderr
2021-06-22 syoussefi@chromium.org Allow capturing process stdout and stderr interleaved
2021-06-22 lexa.knyazev@gmail.com Fix overflow in gl::ValidateES2TexImageParametersBase
2021-06-22 syoussefi@chromium.org Vulkan: SPIR-V Gen: Support most non-texture/image built-ins
2021-06-22 jmadill@chromium.org Trace Tests: Print serialization diff on failure.
2021-06-22 jmadill@chromium.org Test Runner: Add maximum failure count.
2021-06-22 jmadill@chromium.org Better stack traces on Linux.
2021-06-22 syoussefi@chromium.org Add regression test for GL bug w.r.t cached programs
2021-06-22 jmadill@chromium.org Add simple UBSAN ignorelist.
2021-06-22 xiaoxuan.liu@arm.com Update glColorspace(EGL_KHR_gl_colorspace) enable logic
2021-06-22 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 6cbd7212ad42 to 85e758a22b7a (4 revisions)
2021-06-22 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 4a304244dd86 to f0a9f88dd5cb (1 revision)
2021-06-22 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 637b4cdf0c64 to 685eab2b2e45 (109 revisions)
2021-06-22 syoussefi@chromium.org Tests: Add support for --renderdoc
2021-06-22 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 414f62ab7363 to 637b4cdf0c64 (416 revisions)
2021-06-21 jplate@google.com CL: Make CL front end and back end thread-safe
2021-06-21 timvp@google.com Fix roll_aosp.sh 'gn gen' failure
2021-06-21 jplate@google.com CL: Refactor TRY macro and fix more conformance bugs
2021-06-21 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 65149e19efd9 to 6cbd7212ad42 (2 revisions)
2021-06-19 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 4c77f83b612d to 414f62ab7363 (319 revisions)
2021-06-18 ianelliott@google.com Vulkan: Fix AGI hierarchy crash for noop'd clears/queries
2021-06-18 syoussefi@chromium.org Test for missing index dirty bit bug
2021-06-18 jmadill@chromium.org infra: Add symbol_level=1 in Release.
2021-06-18 cnorthrop@google.com Vulkan: Switch viewport and scissor to dynamic state
2021-06-18 doughorn@google.com Ensure GLES1 state is cleared on context switch.
2021-06-18 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 84bc198202e5 to 4a304244dd86 (4 revisions)
2021-06-18 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 7304bd043edc to 65149e19efd9 (8 revisions)
2021-06-18 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 681ec5b77d1d to 4c77f83b612d (360 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jonahr@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win-asan;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1183068,chromium:1190493,chromium:1222516
Tbr: jonahr@google.com
Test: Test: GLES1 applications work with the D3D11 backend in multi-context
Change-Id: I3873dd9080db5ce7ef29c03c666f238e5e5959fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2982637
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#895147}

[modify] https://crrev.com/e7ff2ae3a73b9d0c8ba15141f5a1351b04b8dd0b/DEPS


### su...@chromium.org (2021-07-06)

The issue is marked as fixed in Clusterfuzz, but this issue is still open for some reason. Marking as Fixed.

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congratulations, attekett! The VRP Panel has decided to award you $6000 for this bug, $5000 for the UAF issue + $1000 fuzzer bonus. Nice work and thank you for your contributions to the Chrome Fuzzing effort!

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1190493?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1060139]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055268)*
