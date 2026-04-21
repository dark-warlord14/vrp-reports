# Crash in GL_GenerateMipmap method.

| Field | Value |
|-------|-------|
| **Issue ID** | [40056231](https://issues.chromium.org/issues/40056231) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux |
| **Reporter** | sj...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2021-06-16 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36

Steps to reproduce the problem:
1.
2.
3.

What is the expected behavior?

What went wrong?
### Title
Crash in GL_GenerateMipmap method.

### Test Environment

- Ubuntu 20.04 64bit
- angle library commit 222a81cfaaf0be64e64fe1e8ec04753e287532fe with address sanitizer

### Simple analysis

- this issue doesn't reproduce chrome and so, skip detail analysis.

* ./src/libANGLE/renderer/vulkan/vk_helpers.cpp:5265
```
void ImageHelper::removeStagedUpdates(Context *context,
                                      gl::LevelIndex levelGLStart,
                                      gl::LevelIndex levelGLEnd)
{
    ASSERT(validateSubresourceUpdateImageRefsConsistent());

    // Remove all updates to levels [start, end].
    for (gl::LevelIndex level = levelGLStart; level <= levelGLEnd; ++level)
    {
        std::vector<SubresourceUpdate> *levelUpdates = getLevelUpdates(level);
//...
```

* ./src/libANGLE/renderer/vulkan/vk_helpers.cpp:7066
```
std::vector<ImageHelper::SubresourceUpdate> *ImageHelper::getLevelUpdates(gl::LevelIndex level)
{
    return static_cast<size_t>(level.get()) < mSubresourceUpdates.size() //call 'mSubresourceUpdates.size()' got crash.
               ? &mSubresourceUpdates[level.get()]
               : nullptr;
}
```

As a result of simple analysis, the problem is to arise from `prepareForGenerateMipmap`

* ./src/libANGLE/renderer/vulkan/TextureVk.cpp:2359
```
void TextureVk::prepareForGenerateMipmap(ContextVk *contextVk)
{
    // Remove staged updates to the range that's being respecified (which is all the mips except
    // mip 0).
    gl::LevelIndex baseLevel(mState.getEffectiveBaseLevel() + 1);
    gl::LevelIndex maxLevel(mState.getMipmapMaxLevel());

    mImage->removeStagedUpdates(contextVk, baseLevel, maxLevel); //call crash method, at this time contexVk can be invalidate.
    //...
```

the following assembly code is part of prepareForGenerateMipmap method.
```
   0x7ffff2d40c52 <rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*)+146>    mov    rbx, qword ptr [rbp - 0x48]
   0x7ffff2d40c56 <rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*)+150>    lea    edx, [rbx + 1]
 ► 0x7ffff2d40c59 <rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*)+153>    mov    rdi, qword ptr [r13] <--- [r13] is 0.
   0x7ffff2d40c5d <rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*)+157>    lea    rsi, [r15 + 0x28]
   0x7ffff2d40c61 <rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*)+161>    test   r15, r15
   0x7ffff2d40c64 <rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*)+164>    cmove  rsi, r15
   0x7ffff2d40c68 <rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*)+168>    mov    r15d, edx
   0x7ffff2d40c6b <rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*)+171>    mov    ecx, r12d
   0x7ffff2d40c6e <rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*)+174>    call   0x7ffff2def8e0 <0x7ffff2def8e0>
```

### PoC & how to reproduce

- to reproduce this issue, use 'HelloTriangle' in /samples/'
- first, change the original HelloTriangle.cpp to the attached file. (Only the draw method has changed.)
- after that, build angle library with samples. and run HelloTriangle with `--use-angle=vulkan`.

### ASAN backtrace log
```
==740374==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000160 (pc 0x7f36475ef8c2 bp 0x7ffe00d30e30 sp 0x7ffe00d30d60 T0)
==740374==The signal is caused by a READ memory access.
==740374==Hint: address points to the zero page.
    #0 0x7f36475ef8c2 in size build/linux/debian_sid_amd64-sysroot/usr/lib/gcc/x86_64-linux-gnu/10/../../../../include/c++/10/bits/stl_vector.h
    #1 0x7f36475ef8c2 in getLevelUpdates src/libANGLE/renderer/vulkan/vk_helpers.cpp:7066:67
    #2 0x7f36475ef8c2 in rx::vk::ImageHelper::removeStagedUpdates(rx::vk::Context*, gl::LevelIndexWrapper<int>, gl::LevelIndexWrapper<int>) src/libANGLE/renderer/vulkan/vk_helpers.cpp:5265:56
    #3 0x7f3647540bbc in rx::TextureVk::prepareForGenerateMipmap(rx::ContextVk*) src/libANGLE/renderer/vulkan/TextureVk.cpp:2359:13
    #4 0x7f3647541338 in rx::TextureVk::syncState(gl::Context const*, angle::BitSetT<24ul, unsigned long, unsigned long> const&, gl::Command) src/libANGLE/renderer/vulkan/TextureVk.cpp:2452:9
    #5 0x7f3646ca0c03 in syncState src/libANGLE/Texture.cpp:2021:5
    #6 0x7f3646ca0c03 in gl::Texture::generateMipmap(gl::Context*) src/libANGLE/Texture.cpp:1660:5
    #7 0x7f36469ebac6 in GL_GenerateMipmap src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1387:22
    #8 0x55fda80e68e3 in HelloTriangleSample::draw() samples/hello_triangle/HelloTriangle.cpp:58:13
    #9 0x55fda80e7f5f in SampleApplication::run() samples/sample_util/SampleApplication.cpp:268:9
    #10 0x55fda80e6683 in main samples/hello_triangle/HelloTriangle.cpp:88:16
    #11 0x7f364bee20b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV build/linux/debian_sid_amd64-sysroot/usr/lib/gcc/x86_64-linux-gnu/10/../../../../include/c++/10/bits/stl_vector.h in size
```

Did this work before? N/A 

Chrome version: 90.0.4430.212  Channel: n/a
OS Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2021-06-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-06-18)

geofflang - as an Angle OWNER, could you take a look or re-assign as appropriate>

[Monorail components: Internals>GPU>ANGLE]

### ts...@chromium.org (2021-06-19)

[Empty comment from Monorail migration]

### ge...@chromium.org (2021-06-21)

Shabi, want to take a look?

### sy...@chromium.org (2021-06-22)

Will do

### gi...@appspot.gserviceaccount.com (2021-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/977a28f3a2c2e45fcb49731344f549615ee7023c

commit 977a28f3a2c2e45fcb49731344f549615ee7023c
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Jun 22 16:30:07 2021

No-op glGenerateMipmap on zero-sized textures

The spec says:

> Otherwise, ... if any dimension is zero, all mipmap levels are left
> unchanged. This is not an error.

Bug: chromium:1220250
Change-Id: I45e007c1f8e9b80f405d3d096eb896a7246f7c8e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2979853
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/977a28f3a2c2e45fcb49731344f549615ee7023c/src/libANGLE/Texture.cpp
[modify] https://crrev.com/977a28f3a2c2e45fcb49731344f549615ee7023c/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/977a28f3a2c2e45fcb49731344f549615ee7023c/src/tests/gl_tests/MipmapTest.cpp


### sy...@chromium.org (2021-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and Security_Impact labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues Impact guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2021-06-24)

@geoff, please take a look. Not sure anymore what the impact of security bugs in the Vulkan backend is.

### gi...@appspot.gserviceaccount.com (2021-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9b4ba8f7f5151dd0a44c465e80fa224a243d1e06

commit 9b4ba8f7f5151dd0a44c465e80fa224a243d1e06
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jun 24 08:07:27 2021

Roll ANGLE from b6009f64aa5b to 4375d6c732ef (4 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/b6009f64aa5b..4375d6c732ef

2021-06-24 syoussefi@chromium.org Vulkan: Support multiview queries
2021-06-24 syoussefi@chromium.org No-op glGenerateMipmap on zero-sized textures
2021-06-24 syoussefi@chromium.org Vulkan: Support OVR_multiview and OVR_multiview2
2021-06-24 syoussefi@chromium.org Vulkan: Unpack RenderPassDesc

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
Bug: chromium:1220250
Tbr: jonahr@google.com
Change-Id: I7d2e640a3e5824047b33a41cc87cf8506bc03eb8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2982848
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#895499}

[modify] https://crrev.com/9b4ba8f7f5151dd0a44c465e80fa224a243d1e06/DEPS


### ge...@chromium.org (2021-06-29)

Think we're safe, the VK backend isn't shipping anywhere except SwANGLE which has not gone to any release branch yet.

### ge...@chromium.org (2021-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congratulations! The VRP Panel has decided to award you $7,500 for this report. Nice work and thank you for your efforts on this report!

### sj...@gmail.com (2021-07-23)

thank you!

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-10-05)

This issue was migrated from crbug.com/chromium/1220250?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056231)*
