# Security: WriteTexture heap-buffer-overflow in WebGL on macOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40090246](https://issues.chromium.org/issues/40090246) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU |
| **Platforms** | Mac |
| **Reporter** | [Deleted User] |
| **Assignee** | zm...@chromium.org |
| **Created** | 2018-01-20 |
| **Bounty** | $1,000.00 |

## Description

heap overflow in WriteTextureData on macOS, tested on asan-mac-release-529226.zip

==801==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000046a04 at pc 0x000101cc248b bp 0x7ffeedf9f5f0 sp 0x7ffeedf9ed90
READ of size 8 at 0x602000046a04 thread T0
    #0 0x101cc248a  (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x1a48a)
    #1 0x12f6af75b in glrWriteTextureData (AppleIntelBDWGraphicsGLDriver:x86_64+0x1375b)
    #2 0x7fff3858db49 in glTexImage2D_Exec (GLEngine:x86_64+0x19b49)
    #3 0x7fff379fd63e in glTexImage2D (libGL.dylib:x86_64+0x363e)
    #4 0x116a395a8 in gl::GLApiBase::glTexImage2DFn(unsigned int, int, int, int, int, int, unsigned int, unsigned int, void const*) gl_bindings_autogen_gl.cc:4372
    #5 0x116a86e37 in gl::RealGLApi::glTexImage2DFn(unsigned int, int, int, int, int, int, unsigned int, unsigned int, void const*) gl_gl_api_implementation.cc:374
    #6 0x117489714 in gpu::gles2::TextureManager::DoTexImage(gpu::gles2::DecoderTextureState*, gpu::gles2::ContextState*, gpu::gles2::DecoderFramebufferState*, char const*, gpu::gles2::TextureRef*, gpu::gles2::TextureManager::DoTexImageArguments const&) texture_manager.cc:3381
    #7 0x117487a35 in gpu::gles2::TextureManager::DoCubeMapWorkaround(gpu::gles2::DecoderTextureState*, gpu::gles2::ContextState*, gpu::gles2::DecoderFramebufferState*, gpu::gles2::TextureRef*, char const*, gpu::gles2::TextureManager::DoTexImageArguments const&) texture_manager.cc:2694
    #8 0x1172b00bd in gpu::gles2::GLES2DecoderImpl::DoCopyTexImage2D(unsigned int, int, unsigned int, int, int, int, int, int) texture_manager.h:1102

## Attachments

- [writeTexture.html](attachments/writeTexture.html) (text/plain, 1.6 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 9.6 KB)
- [simplied_test_case_for_crbug_804118.html](attachments/simplied_test_case_for_crbug_804118.html) (text/plain, 516 B)

## Timeline

### cl...@chromium.org (2018-01-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5920132118609920.

### cl...@chromium.org (2018-01-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5002286467383296.

### np...@chromium.org (2018-01-22)

Neither of these could be reproduced on CF, either on Mac or Linux. Is there a special setup required?

[Monorail components: Internals>GPU]

### np...@chromium.org (2018-01-22)

Trying a different CF job...

### cl...@chromium.org (2018-01-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6066698078912512.

### [Deleted User] (2018-01-23)

#1 0x12f6af75b in glrWriteTextureData (AppleIntelBDWGraphicsGLDriver:x86_64+0x1375b)

I guess you require a Intel HD Graphics based MacOS for this to reproduce. 

### cl...@chromium.org (2018-01-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5699413012643840.

### me...@chromium.org (2018-01-25)

I can repro with a 2012 Macbook Pro using the integrated graphics. Uploaded another test case with mac_asan_chrome job type.

zmo: Can you please take a look, or reassign? Thanks.

### zm...@chromium.org (2018-01-25)

It seems we fail to reset pixel unpack params in TextureManager::DoCubeMapWorkaround before calling TexImage*(). I will patch this up.

That said, the underlying Intel driver should really generate an INVALID_OPERATION rather than crash.

### me...@chromium.org (2018-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-01-28)

[Empty comment from Monorail migration]

### zm...@chromium.org (2018-01-29)

No need to block release since this has been in many releases.

That said, I will fix this soon.

### zm...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-29)

> No need to block release since this has been in many releases.

Does it mean this impacts stable? Or is beta accurate? (I incorrectly marked it as Security_Impact-Beta based on the asan build in the original report (529226))

### zm...@chromium.org (2018-01-29)

This affects all (date back a couple years). That's why this should not be a blocker because this is not a regression. That said, this should still be fixed in this release.

### me...@chromium.org (2018-01-29)

Thanks for confirming. Not sure why sheriffbot thought it impacts Beta.

### zm...@chromium.org (2018-01-30)

Here is a simplified test case. I deleted unrelated shader/program setup.

### zm...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### zm...@chromium.org (2018-01-30)

Fix is uploaded for review: https://chromium-review.googlesource.com/c/chromium/src/+/892282

### zm...@chromium.org (2018-01-30)

Conformance test is added in https://github.com/KhronosGroup/WebGL/pull/2593 (except it only catch the bug in MSAN bot)

### bu...@chromium.org (2018-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a89aa4642cefb79e312c95ca3c66bbaff5263a22

commit a89aa4642cefb79e312c95ca3c66bbaff5263a22
Author: Zhenyao Mo <zmo@chromium.org>
Date: Tue Jan 30 04:22:34 2018

Fix CopyTexImage behavior when cubemap workaround is involved.

The bug is, we need to reset PIXEL_UNPACK_BUFFER as well as UNPACK params
in order to upload data to textures correctly.

BUG=804118
TEST=tests in the bug
R=piman@chromium.org
NOTRY=true

Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: I743f03cdc98b2c6993449ca615b246eb42ef4dfa
Reviewed-on: https://chromium-review.googlesource.com/892282
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Reviewed-by: Antoine Labour <piman@chromium.org>
Reviewed-by: Kai Ninomiya <kainino@chromium.org>
Cr-Commit-Position: refs/heads/master@{#532749}
[modify] https://crrev.com/a89aa4642cefb79e312c95ca3c66bbaff5263a22/gpu/command_buffer/service/texture_manager.cc


### zm...@chromium.org (2018-01-30)

It's a simple CL, so let's at least merge back to M65.

### sh...@chromium.org (2018-01-31)

Your change meets the bar and is auto-approved for M65. Please go ahead and merge the CL to branch 3325 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-01-31)

Pls merge your change to M65 branch 3325 ASAP so we can pick it up for next M65 dev release. Thank you.

### bu...@chromium.org (2018-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fccae1a6842d24b1fb02b6ea5aa37c887e0a11d3

commit fccae1a6842d24b1fb02b6ea5aa37c887e0a11d3
Author: Zhenyao Mo <zmo@chromium.org>
Date: Wed Jan 31 18:50:12 2018

Fix CopyTexImage behavior when cubemap workaround is involved.

The bug is, we need to reset PIXEL_UNPACK_BUFFER as well as UNPACK params
in order to upload data to textures correctly.

BUG=804118
TEST=tests in the bug
R=piman@chromium.org
TBR=zmo@chromium.org
NOTRY=true

(cherry picked from commit a89aa4642cefb79e312c95ca3c66bbaff5263a22)

Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: I743f03cdc98b2c6993449ca615b246eb42ef4dfa
Reviewed-on: https://chromium-review.googlesource.com/892282
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Reviewed-by: Antoine Labour <piman@chromium.org>
Reviewed-by: Kai Ninomiya <kainino@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#532749}
Reviewed-on: https://chromium-review.googlesource.com/895907
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/branch-heads/3325@{#208}
Cr-Branched-From: bc084a8b5afa3744a74927344e304c02ae54189f-refs/heads/master@{#530369}
[modify] https://crrev.com/fccae1a6842d24b1fb02b6ea5aa37c887e0a11d3/gpu/command_buffer/service/texture_manager.cc


### aw...@google.com (2018-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-09)

Hello! The VRP panel decided to reward $1,000 for this report - cheers!

### aw...@google.com (2018-02-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d5fd79c66c041e669cb7cc0d0a41dbcdac886649

commit d5fd79c66c041e669cb7cc0d0a41dbcdac886649
Author: Kenneth Russell <kbr@chromium.org>
Date: Thu Apr 12 23:23:34 2018

Roll WebGL aef0b3a..7c0541d

https://chromium.googlesource.com/external/khronosgroup/webgl.git/+log/aef0b3a..7c0541d

Bug: 804118, 818336, 828262, angleproject:2381
Tbr: zmo@chromium.org, kainino@chromium.org, jdarpinian@chromium.org
Cq-Include-Trybots: luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_angle_rel_ng;luci.chromium.try:win_angle_rel_ng
Change-Id: I28b3d55e43f5633ffe4c8cd6e7e375dd2fba2b9b
Reviewed-on: https://chromium-review.googlesource.com/1010910
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#550408}
[modify] https://crrev.com/d5fd79c66c041e669cb7cc0d0a41dbcdac886649/DEPS
[modify] https://crrev.com/d5fd79c66c041e669cb7cc0d0a41dbcdac886649/content/test/gpu/gpu_tests/webgl_conformance_revision.txt


### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d5fd79c66c041e669cb7cc0d0a41dbcdac886649

commit d5fd79c66c041e669cb7cc0d0a41dbcdac886649
Author: Kenneth Russell <kbr@chromium.org>
Date: Thu Apr 12 23:23:34 2018

Roll WebGL aef0b3a..7c0541d

https://chromium.googlesource.com/external/khronosgroup/webgl.git/+log/aef0b3a..7c0541d

Bug: 804118, 818336, 828262, angleproject:2381
Tbr: zmo@chromium.org, kainino@chromium.org, jdarpinian@chromium.org
Cq-Include-Trybots: luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_angle_rel_ng;luci.chromium.try:win_angle_rel_ng
Change-Id: I28b3d55e43f5633ffe4c8cd6e7e375dd2fba2b9b
Reviewed-on: https://chromium-review.googlesource.com/1010910
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#550408}
[modify] https://crrev.com/d5fd79c66c041e669cb7cc0d0a41dbcdac886649/DEPS
[modify] https://crrev.com/d5fd79c66c041e669cb7cc0d0a41dbcdac886649/content/test/gpu/gpu_tests/webgl_conformance_revision.txt


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/804118?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090246)*
