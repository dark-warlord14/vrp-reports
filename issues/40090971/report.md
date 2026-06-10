# Security: ANGLE LoadToNative memory corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40090971](https://issues.chromium.org/issues/40090971) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | cw...@google.com |
| **Created** | 2018-03-30 |
| **Bounty** | $1,000.00 |

## Description

I have tested this on asan-win32-release_x64-547242 and a few older builds. The crash happens in ANGLE.

==11492==ERROR: AddressSanitizer: access-violation on unknown address 0x250082219f00 (pc 0x7ff618f89575 bp 0x00a6bd1f9be0 sp 0x00a6bd1f9b58 T0)
==11492==The signal is caused by a READ memory access.
    #0 0x7ff618f89574 in memcpy f:\dd\vctools\crt\vcruntime\src\string\amd64\memcpy.asm:228
    #1 0x7ff618c7ad2b in __asan_memcpy C:\b\rr\tmp7g7qqx\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cc:23
    #2 0x7ffb67d67102 in angle::LoadToNative<signed char,1>(unsigned __int64,unsigned __int64,unsigned __int64,unsigned char const *,unsigned __int64,unsigned __int64,unsigned char *,unsigned __int64,unsigned __int64) C:\b\c\b\win_asan_release\src\third_party\angle\src\image_util\loadimage.inl:63:17
    #3 0x7ffb67b758a5 in rx::Image11::loadData(class gl::Context const *,struct gl::Box const &,struct gl::PixelUnpackState const &,unsigned int,void const *,bool) C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:310:5
    #4 0x7ffb67b445cf in rx::TextureD3D::setImageImpl(class gl::Context const *,struct gl::ImageIndex const &,unsigned int,struct gl::PixelUnpackState const &,unsigned char const *,__int64) 



## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 7.4 KB)
- [LoadToNative.html](attachments/LoadToNative.html) (text/plain, 906 B)

## Timeline

### mm...@chromium.org (2018-03-30)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE]

### cl...@chromium.org (2018-03-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5087786793959424.

### cl...@chromium.org (2018-03-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5375538462720000.

### mm...@chromium.org (2018-03-30)

Thanks for your report. Do you know whether it's possible to manipulate the address being passed to the memcpy call?

### mm...@chromium.org (2018-03-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-03-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-03-30)

This crash occurs very frequently on windows platform and is likely preventing the fuzzer  from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### cl...@chromium.org (2018-03-30)

Detailed report: https://clusterfuzz.com/testcase?key=5375538462720000

Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: UNKNOWN
Crash Address: 0x7ffff9462ce4
Crash State:
  RtlProcessFlsData
  LdrShutdownProcess
  RtlExitUserProcess
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=532379:532386

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5375538462720000

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### cl...@chromium.org (2018-03-31)

Detailed report: https://clusterfuzz.com/testcase?key=5087786793959424

Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: UNKNOWN READ
Crash Address: 0x24236b728c50
Crash State:
  angle::LoadToNative<signed
  rx::Image11::loadData
  rx::TextureD3D::setImageImpl
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=541484:541517

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5087786793959424

See https://github.com/google/clusterfuzz-tools for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### mm...@chromium.org (2018-03-31)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-04-02)

A friendly reminder that M67 branch is coming soon on 04/12! Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix ASAP to trunk. This way we branch M67 from a high quality trunk. Thank you.

### ge...@chromium.org (2018-04-05)

Luc or Corentin, would you mind taking a look at this crash?  I may not get a chance this week.

### cw...@chromium.org (2018-04-05)

I don't have a Windows machine right now. We'll look at it with Luc once the Chrome build finishes on his machine.

### cw...@chromium.org (2018-04-06)

We root caused the issue, the fix will be in review shortly.

### go...@chromium.org (2018-04-11)

A friendly reminder that M67 branch is tomorrow, Thursday 04/12! Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix ASAP to trunk. This way we branch M67 from a high quality trunk. Thank you.

### bu...@chromium.org (2018-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/56c8577b4dbf2239780e38090dadbeb06f4b8563

commit 56c8577b4dbf2239780e38090dadbeb06f4b8563
Author: Corentin Wallez <cwallez@chromium.org>
Date: Thu Apr 12 18:03:57 2018

TextureD3D_2D::CopyImage clear using initializeContents

When using glCopyTexImage2D clearing of the mip level needs to happen
when running in WebGL or robust resource init mode and any pixel would
be sampled outside of the framebuffer. Previously the code was using
"setImage" for this purpose, causing issues when a PIXEL_UNPACK_BUFFER
was bound.

Also add a regression test.

BUG=chromium:827667

Change-Id: I03be20d8272730ab30afdab2f8919be853e729b6
Reviewed-on: https://chromium-review.googlesource.com/1000182
Commit-Queue: Corentin Wallez <cwallez@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/56c8577b4dbf2239780e38090dadbeb06f4b8563/src/libANGLE/renderer/d3d/TextureD3D.cpp
[modify] https://crrev.com/56c8577b4dbf2239780e38090dadbeb06f4b8563/src/tests/gl_tests/RobustResourceInitTest.cpp


### go...@chromium.org (2018-04-12)

Any update on this bug as M67 is branching today (04/12) and this bug is marked as M67 Beta Blocker?

### cw...@chromium.org (2018-04-12)

The fix is rolling in Chrome right now.

### bu...@chromium.org (2018-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eadee7e04b9af790c389881b27453a3a240b84fa

commit eadee7e04b9af790c389881b27453a3a240b84fa
Author: angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Fri Apr 13 01:01:52 2018

Roll src/third_party/angle/ 14f4817c4..56c8577b4 (6 commits)

https://chromium.googlesource.com/angle/angle.git/+log/14f4817c4dad..56c8577b4dbf

$ git log 14f4817c4..56c8577b4 --date=short --no-merges --format='%ad %ae %s'
2018-04-06 cwallez TextureD3D_2D::CopyImage clear using initializeContents
2018-04-12 lucferron Vulkan: Suppress flaky test in GLSLTest on Windows
2018-04-10 brandon1.jones Autogenerate ANGLE extension entry points
2018-04-11 lucferron Vulkan: drawArrays followed by drawElements bugfix
2018-04-11 jmadill VertexArray: Use switch macro for faster iteration.
2018-04-09 lucferron Vulkan: Enable GLSLTest tests for Vulkan

Created with:
  roll-dep src/third_party/angle
BUG=chromium:827667


The AutoRoll server is located here: https://angle-chromium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
TBR=ynovikov@chromium.org

No-try: True
Change-Id: Ib121297476e16cae32b5198cdf8d54861a048841
Reviewed-on: https://chromium-review.googlesource.com/1011228
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>
Reviewed-by: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Cr-Commit-Position: refs/heads/master@{#550450}
[modify] https://crrev.com/eadee7e04b9af790c389881b27453a3a240b84fa/DEPS


### cw...@chromium.org (2018-04-13)

I will close this as fixed once I have checked the fix was rolled in beta M67

### cw...@chromium.org (2018-04-13)

The roll didn't make it into beta M67, can we merge the ANGLE change in M67?

### go...@chromium.org (2018-04-13)

M67 Beta promotion is coming VERY soon. Pls make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### sh...@chromium.org (2018-04-14)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-04-14)

+awhalley@ (Security TPM) for M67 merge review

### sh...@chromium.org (2018-04-14)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2018-04-15)

ClusterFuzz has detected this issue as fixed in range 550440:550450.

Detailed report: https://clusterfuzz.com/testcase?key=5087786793959424

Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: UNKNOWN READ
Crash Address: 0x24236b728c50
Crash State:
  angle::LoadToNative<signed
  rx::Image11::loadData
  rx::TextureD3D::setImageImpl
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=541484:541517
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=550440:550450

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5087786793959424

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-04-15)

ClusterFuzz testcase 5087786793959424 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-04-15)

[Empty comment from Monorail migration]

### cw...@chromium.org (2018-04-16)

We still need to merge this in M67, re-opening until it is done.

### go...@chromium.org (2018-04-16)

Which Cl you're requesting a merge for? And is the change well baked/verified in canary?

awhalley@ (Security TPM) for merge review.

### cw...@chromium.org (2018-04-16)

I am requesting a merge for https://chromium-review.googlesource.com/1000182

The change is low risk, and verified by clusterfuzz. It has been in Canary for ~3 days.

### aw...@google.com (2018-04-17)

govind@ - good for 67

### go...@chromium.org (2018-04-17)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/827667#c32. Please merge before 1:00 PM PT, Tuesday (04/17) so we can pick it up for this week dev release. Thank you.

### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d915203fe3b63092a5c6a8b31bd06ad01da683cc

commit d915203fe3b63092a5c6a8b31bd06ad01da683cc
Author: Corentin Wallez <cwallez@chromium.org>
Date: Tue Apr 17 15:40:03 2018

TextureD3D_2D::CopyImage clear using initializeContents

When using glCopyTexImage2D clearing of the mip level needs to happen
when running in WebGL or robust resource init mode and any pixel would
be sampled outside of the framebuffer. Previously the code was using
"setImage" for this purpose, causing issues when a PIXEL_UNPACK_BUFFER
was bound.

Also add a regression test.

BUG=chromium:827667

Change-Id: I03be20d8272730ab30afdab2f8919be853e729b6
Reviewed-on: https://chromium-review.googlesource.com/1000182
Commit-Queue: Corentin Wallez <cwallez@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit 56c8577b4dbf2239780e38090dadbeb06f4b8563)
Reviewed-on: https://chromium-review.googlesource.com/1014425
Reviewed-by: Corentin Wallez <cwallez@chromium.org>

[modify] https://crrev.com/d915203fe3b63092a5c6a8b31bd06ad01da683cc/src/libANGLE/renderer/d3d/TextureD3D.cpp
[modify] https://crrev.com/d915203fe3b63092a5c6a8b31bd06ad01da683cc/src/tests/gl_tests/RobustResourceInitTest.cpp


### cw...@chromium.org (2018-04-17)

Merged the change in the ANGLE chromium/3396 branch that should be picked up automatically on the next release.

### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eadee7e04b9af790c389881b27453a3a240b84fa

commit eadee7e04b9af790c389881b27453a3a240b84fa
Author: angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Fri Apr 13 01:01:52 2018

Roll src/third_party/angle/ 14f4817c4..56c8577b4 (6 commits)

https://chromium.googlesource.com/angle/angle.git/+log/14f4817c4dad..56c8577b4dbf

$ git log 14f4817c4..56c8577b4 --date=short --no-merges --format='%ad %ae %s'
2018-04-06 cwallez TextureD3D_2D::CopyImage clear using initializeContents
2018-04-12 lucferron Vulkan: Suppress flaky test in GLSLTest on Windows
2018-04-10 brandon1.jones Autogenerate ANGLE extension entry points
2018-04-11 lucferron Vulkan: drawArrays followed by drawElements bugfix
2018-04-11 jmadill VertexArray: Use switch macro for faster iteration.
2018-04-09 lucferron Vulkan: Enable GLSLTest tests for Vulkan

Created with:
  roll-dep src/third_party/angle
BUG=chromium:827667


The AutoRoll server is located here: https://angle-chromium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
TBR=ynovikov@chromium.org

No-try: True
Change-Id: Ib121297476e16cae32b5198cdf8d54861a048841
Reviewed-on: https://chromium-review.googlesource.com/1011228
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>
Reviewed-by: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Cr-Commit-Position: refs/heads/master@{#550450}
[modify] https://crrev.com/eadee7e04b9af790c389881b27453a3a240b84fa/DEPS


### aw...@google.com (2018-04-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-27)

Thanks for the report, omair@! The Chrome VRP panel decided to award $1,000 for this report. Cheers!

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-07-25)

This issue was migrated from crbug.com/chromium/827667?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/834534, crbug.com/chromium/836131]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090971)*
