# WebGL glCompressedTexImage3D Heap-Based Buffer Overflow Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40059929](https://issues.chromium.org/issues/40059929) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | no...@ssd-disclosure.com |
| **Assignee** | kb...@chromium.org |
| **Created** | 2022-06-12 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

## Summary

- A Heap-Based Buffer Overflow vulnerability exists in the WebGL glCompressedTexImage3D.
- An attacker must open a arbitrary generated html file to exploit this vulnerability.

## Test environment

- OS : macOS Monterey 12.4(21F79)
- iMac GPU : AMD Radeon Pro Vega 48
- asan-mac-release-1004761
- Download link: <https://alesandroortiz.com/articles/latest-chromium-asan-builds/>  
  
  \*\* The latest Chrome (not stable) version is uploaded from the link, and you can download the asan build for macOS. \*\*

\*\* As of my testing, this vulnerability only works on macOS. \*\*

## Reproduce

- /asan-mac-release-1004761/Chromium.app/Contents/MacOS/Chromium --no-sandbox poc.html

**Problem Description:**

## Address Sanitizer (ASan)

```
=================================================================  
==17802==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6060001791c0 at pc 0x00010c19221d bp 0x7ff7b413eba0 sp 0x7ff7b413e368  
READ of size 16 at 0x6060001791c0 thread T0  
==17802==WARNING: failed to spawn external symbolizer (errno: 9)  
==17802==WARNING: failed to spawn external symbolizer (errno: 9)  
==17802==WARNING: failed to spawn external symbolizer (errno: 9)  
==17802==WARNING: failed to spawn external symbolizer (errno: 9)  
==17802==WARNING: failed to spawn external symbolizer (errno: 9)  
==17802==WARNING: Failed to use and restart external symbolizer!  
  #0 0x10c19221c in __sanitizer_weak_hook_memmem+0x179c (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Helpers/Chromium Helper (GPU).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x1f21c) (BuildId: 90dc47a9652a34e4841ca1b86bd256c0240000001000000000070a0000010b00)  
  #1 0x7ffa1df34acc in glgCopyRowsWithMemCopy(GLGOperationRec const\*, unsigned long, GLDPixelModeRec const\*)+0x64 (/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGLImage.dylib:x86_64+0x6acc) (BuildId: 56aed9f26e8235e9bd65a2c81c31dec232000000200000000100000000040c00)  
  #2 0x7ffa1df33db9 in glgProcessPixelsWithProcessor+0x92a (/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGLImage.dylib:x86_64+0x5db9) (BuildId: 56aed9f26e8235e9bd65a2c81c31dec232000000200000000100000000040c00)  
  #3 0x112d607ad in glrATIModifyTexSubImageCPU+0x586 (/System/Library/Extensions/AMDRadeonX5000GLDriver.bundle/Contents/MacOS/AMDRadeonX5000GLDriver:x86_64+0x1f7ad) (BuildId: c30348bb999e396085f7000000fb775232000000200000000100000000040c00)  
  #4 0x112d9a650 in glrWriteTextureData+0x23f (/System/Library/Extensions/AMDRadeonX5000GLDriver.bundle/Contents/MacOS/AMDRadeonX5000GLDriver:x86_64+0x59650) (BuildId: c30348bb999e396085f7000000fb775232000000200000000100000000040c00)  
  #5 0x7ffa1e1bf6e1 in glCompressedTexImage3D_Exec+0x435 (/System/Library/Frameworks/OpenGL.framework/Versions/A/Resources/GLEngine.bundle/GLEngine:x86_64+0x866e1) (BuildId: a72561b77972305a8f850366b47b7a8f32000000200000000100000000040c00)  
  #6 0x7ffa1e13209c in glCompressedTexImage3D+0x36 (/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:x86_64+0x409c) (BuildId: 7a5491db1b1337bfa174112d53bf903132000000200000000100000000040c00)  
  #7 0x1223b1242 in rx::TextureGL::setCompressedImage(gl::Context const\*, gl::ImageIndex const&, unsigned int, gl::Extents const&, gl::PixelUnpackState const&, unsigned long, unsigned char const\*)+0x2a2 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0x955242) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)  
  #8 0x121d0611c in gl::Texture::setCompressedImage(gl::Context\*, gl::PixelUnpackState const&, gl::TextureTarget, int, unsigned int, gl::Extents const&, unsigned long, unsigned char const\*)+0x1fc (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0x2aa11c) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)  
  #9 0x121b3fecb in gl::Context::compressedTexImage3D(gl::TextureTarget, int, unsigned int, int, int, int, int, int, void const\*)+0x3eb (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0xe3ecb) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)  
  #10 0x121b40056 in gl::Context::compressedTexImage3DRobust(gl::TextureTarget, int, unsigned int, int, int, int, int, int, int, void const\*)+0x26 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0xe4056) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)  
  #11 0x121aae57f in GL_CompressedTexImage3DRobustANGLE+0x13f (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0x5257f) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)  
  #12 0x1629d4b02 in gl::GLApiBase::glCompressedTexImage3DRobustANGLEFn(unsigned int, int, unsigned int, int, int, int, int, int, int, void const\*)+0x62  

**Additional Comments:**   


**Chrome version: ** 102.0.5005.61 **Channel: ** Stable  

**OS:** Mac OS

```

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 598 B)
- [report.md](attachments/report.md) (text/plain, 29.9 KB)

## Timeline

### no...@ssd-disclosure.com (2022-06-12)

Dohyun Lee (@l33d0hyun) of SSD-Disclosure Labs & DNSLab, Korea Univ

### dt...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGL]

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4512612922621952.

### cl...@chromium.org (2022-06-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6215335325925376.

### xi...@chromium.org (2022-06-15)

Thanks for the report. kbr@, could you take a look? Thanks!

Marking FoundIn-104 for now. Reporter, could you verify whether it can be reproduced for earlier versions?

### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### kb...@chromium.org (2022-06-15)

Is this reproducible in top-of-tree builds? Our colleague Alexey Knyazev just fixed a bug in this area in https://crbug.com/angleproject/4056 .


[Monorail components: Internals>GPU>ANGLE]

### le...@gmail.com (2022-06-16)

That bug was related only to sub-uploads and its code paths are not used by this example.

### le...@gmail.com (2022-06-16)

The first compressedTexImage3D call is rejected by Chromium early, before even reaching ANGLE. The second compressedTexImage3D call looks correct.

It seems that the OpenGL driver does not ignore UNPACK_IMAGE_HEIGHT value.

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2022-06-22)

Working on a fix in ANGLE now.


### ad...@google.com (2022-06-22)

(auto-cc on security bug)

### kb...@chromium.org (2022-06-22)

It turns out that this was essentially fixed in https://crbug.com/chromium/1267496, but ANGLE's OpenGL backend neglected to set the pixel unpack state before calling glCompressedTexImage3D.


### kb...@chromium.org (2022-06-23)

[Empty comment from Monorail migration]

### kb...@chromium.org (2022-06-23)

[Empty comment from Monorail migration]

### kb...@chromium.org (2022-06-23)

Fixes in progress:

Set pixel unpack state in GL backend's CompressedTexImage3D.
https://chromium-review.googlesource.com/c/angle/angle/+/3715717

Add test of UNPACK_IMAGE_HEIGHT with CompressedTexImage3D.
https://chromium-review.googlesource.com/c/chromium/src/+/3715383

and a follow-on:

Please add Mac ASAN bot(s) to ANGLE waterfall
https://bugs.chromium.org/p/angleproject/issues/detail?id=7457


### gi...@appspot.gserviceaccount.com (2022-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/338c65393073a627297e0f21eb1b4375a87631e1

commit 338c65393073a627297e0f21eb1b4375a87631e1
Author: Kenneth Russell <kbr@chromium.org>
Date: Wed Jun 22 17:22:22 2022

Set pixel unpack state in GL backend's CompressedTexImage3D.

A workaround added earlier wasn't applying to the GL backend because
of this missing call.

Covered by existing angle_end2end_test, but only reproduces on ASAN
build. A Chromium-side test is being added separately.

Bug: chromium:1335688
Change-Id: Ia33648054dfa647159ecfc62ca53415de04f625d
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3715717
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/338c65393073a627297e0f21eb1b4375a87631e1/src/libANGLE/renderer/gl/TextureGL.cpp


### [Deleted User] (2022-06-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b977e6794a65ccd2e3b0695bb9ba2d07103a5dd9

commit b977e6794a65ccd2e3b0695bb9ba2d07103a5dd9
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jun 27 15:09:11 2022

Roll ANGLE from 32cb575032ee to 669d7b756e79 (4 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/32cb575032ee..669d7b756e79

2022-06-23 b.schade@samsung.com Fix validation checks in glCompressedTexSubImage3D
2022-06-23 kbr@chromium.org Set pixel unpack state in GL backend's CompressedTexImage3D.
2022-06-23 fwang@igalia.com Fix compilation errors with deprecated sprintf function
2022-06-23 lehoangquyen@chromium.org Metal: Fix invalid iosurface texture after base/max lvl changed

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ianelliott@google.com,ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1335688,chromium:1337324
Tbr: ianelliott@google.com,ynovikov@google.com
Test: Test: *CompressedTexture*Test*
Test: Test: *ETC2RGB8_CubeMapValidation*
Test: Test: KHR-GLES32.core.compressed_format.api.invalid_format_array
Test: Test: KHR-GLES32.core.compressed_format.api.invalid_offset_or_size
Change-Id: I1f0199f4275346707dc4fa91898fb6a68e26b41f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3725717
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1018236}

[modify] https://crrev.com/b977e6794a65ccd2e3b0695bb9ba2d07103a5dd9/DEPS


### kb...@chromium.org (2022-06-28)

With the ANGLE roll-forward into Chrome, this bug is officially fixed. The Chromium-side test is still in the process of landing.


### gi...@appspot.gserviceaccount.com (2022-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4381afbf13a2664f2cd3699095c7e1c12041b244

commit 4381afbf13a2664f2cd3699095c7e1c12041b244
Author: Kenneth Russell <kbr@chromium.org>
Date: Tue Jun 28 04:45:29 2022

Add test of UNPACK_IMAGE_HEIGHT with CompressedTexImage3D.

Catches the associated error on Mac ASAN bots.

Bug: 1335688
Change-Id: I1264db98a7db3b92183eff528a091f92e2951ac6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715383
Reviewed-by: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1018537}

[add] https://crrev.com/4381afbf13a2664f2cd3699095c7e1c12041b244/content/test/data/gpu/webgl2-unpack-image-height.html
[modify] https://crrev.com/4381afbf13a2664f2cd3699095c7e1c12041b244/content/test/gpu/gpu_tests/context_lost_integration_test.py


### [Deleted User] (2022-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-28)

Requesting merge to beta M104 because latest trunk commit (1018537) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-28)

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2022-06-29)

Note to the security team and PMs: I'm not sure whether this warrants a merge-back. The original report, https://crbug.com/chromium/1267496, was merged back at the time; this is the same problem. If it does, then here are the questionnaire answers:

1. Out-of-bounds read in the GPU process reliably triggerable from a web page.
2. https://chromium-review.googlesource.com/c/angle/angle/+/3715717
3. Yes.
4. No.
5. N/A
6. No - this may crash the GPU process or seemingly have no effect. Only reliably reproducible in Mac ASAN builds.


### kb...@chromium.org (2022-06-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-06)

Congratulations, Dohyun Lee! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and reporting this issue to us - nice work! 

### am...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

M104 merge approved, please go ahead and merge this fix to branch 5112 at your earliest convenience. 

Since this is an OOB read, I don't think this is necessary to merge this back to M102/ES and M103/Stable. It's a pretty minimal fix and seems safe to backmerge, but I do not think actual impact warrants such. 

### kb...@chromium.org (2022-07-08)

Thanks. M104 merge is up for review in https://chromium-review.googlesource.com/c/angle/angle/+/3753285 .


### kb...@chromium.org (2022-07-09)

Submitted https://chromium-review.googlesource.com/c/angle/angle/+/3753285 .


### gi...@appspot.gserviceaccount.com (2022-07-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2693b03eba82a424a19febaacaab4115a45b7682

commit 2693b03eba82a424a19febaacaab4115a45b7682
Author: Kenneth Russell <kbr@chromium.org>
Date: Wed Jun 22 17:22:22 2022

[M104] Set pixel unpack state in GL backend's CompressedTexImage3D.

A workaround added earlier wasn't applying to the GL backend because
of this missing call.

Covered by existing angle_end2end_test, but only reproduces on ASAN
build. A Chromium-side test is being added separately.

Bug: chromium:1335688
Change-Id: Ia33648054dfa647159ecfc62ca53415de04f625d
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3715717
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit 338c65393073a627297e0f21eb1b4375a87631e1)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3753285
Reviewed-by: Gregg Tavares <gman@chromium.org>

[modify] https://crrev.com/2693b03eba82a424a19febaacaab4115a45b7682/src/libANGLE/renderer/gl/TextureGL.cpp


### [Deleted User] (2022-10-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1335688?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail blocked-on: crbug.com/chromium/1267496]
[Monorail blocking: crbug.com/angleproject/7457, crbug.com/chromium/1340755]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059929)*
