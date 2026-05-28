# Security: use-after-poison libANGLE\renderer\d3d\d3d11\VertexBuffer11.cpp:129 in rx::VertexBuffer11::storeVertexAttributes

| Field | Value |
|-------|-------|
| **Issue ID** | [40064044](https://issues.chromium.org/issues/40064044) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2023-04-14 |
| **Bounty** | $11,000.00 |

## Description

#Version
asan-win32-release_x64-1129101

#Reproduce
chrome --no-sandbox --user-data-dir=test poc.html

#Type of crash
gpu process

#Analysis
coming soon

#Note
*.js is part of the KhronosGroup/WebGL,the files can be found here
https://github.com/KhronosGroup/WebGL/tree/main/sdk/tests/js

#Asan


## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 13.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 8.3 KB)
- [desktop-gl-constants.js](attachments/desktop-gl-constants.js) (text/plain, 88.2 KB)
- [js-test-post.js](attachments/js-test-post.js) (text/plain, 1.3 KB)
- [js-test-pre.js](attachments/js-test-pre.js) (text/plain, 21.0 KB)
- [webgl-test-utils.js](attachments/webgl-test-utils.js) (text/plain, 118.8 KB)
- [pocmini.html](attachments/pocmini.html) (text/plain, 1.5 KB)
- [webgl-test-utils.js](attachments/webgl-test-utils.js) (text/plain, 118.8 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-04-14)

Update the minimum poc

### m....@gmail.com (2023-04-14)

#RCA
We can bind a smaller buffer with the bufferData and ask to draw a large buffer, causing OOBR

var colorData = new Float32Array([1,0,0,1,0,1,0,1]);
gl.bufferData(gl.ARRAY_BUFFER, colorData, gl.DYNAMIC_DRAW);

gl.vertexAttribPointer(2, 4, gl.FLOAT, false, 0, 0);
gl.drawArrays(gl.TRIANGLES, 0, 6);

https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/copyvertex.inc.h;drc=11ff9071e6112d0b830036e7c5bc2b00560649c0;l=61

### m....@gmail.com (2023-04-14)

bisect
https://chromium-review.googlesource.com/c/angle/angle/+/4375138

### m....@gmail.com (2023-04-14)

My fix is revert the CL https://chromium-review.googlesource.com/c/angle/angle/+/4375138

### jd...@chromium.org (2023-04-14)

I can't reproduce this, but it's possible that that's an artifact of my test environment.

geofflang@ would you mind taking a look? If it doesn't look valid to you, it's OK to close it as such. Thanks!

Tentatively labeling assuming it's valid.

[Monorail components: Blink>WebGL]

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2023-04-18)

re https://crbug.com/chromium/1433180#c06 Did you do the test in the windows environment? 
I can reproduce it stably on several local machines, and the root cause of the issue is also very clear.

### ge...@chromium.org (2023-04-19)

Going to debug this this week.

### ge...@chromium.org (2023-04-19)

Will revert if the fix isn't simple

### gi...@appspot.gserviceaccount.com (2023-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f1b8a29adb6142e17a116722d5bd5ed850e68bf8

commit f1b8a29adb6142e17a116722d5bd5ed850e68bf8
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Apr 21 18:37:23 2023

D3D11: Fix instanced vertex streaming data copies.

Fix the other usage of ComputeVertexBindingElementCount in the D3D11
vertex streaming code. It is possible to try to copy too much source
data due to incorrect instanced count calculations.

Bug: chromium:1425606, chromium:1433180
Change-Id: Ie393b1c0b1291cf2b5087341c9fba8c98343d7bf
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4459152
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/f1b8a29adb6142e17a116722d5bd5ed850e68bf8/src/libANGLE/renderer/d3d/VertexDataManager.cpp
[modify] https://crrev.com/f1b8a29adb6142e17a116722d5bd5ed850e68bf8/src/tests/gl_tests/InstancingTest.cpp


### gi...@appspot.gserviceaccount.com (2023-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/291c1427a82d0af02136923943ab3513386cb69f

commit 291c1427a82d0af02136923943ab3513386cb69f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Apr 25 19:03:58 2023

Roll ANGLE from 7ec05fb8dcf0 to a2fceac2feb2 (5 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/7ec05fb8dcf0..a2fceac2feb2

2023-04-25 geofflang@chromium.org Prefer Metal over CGL for querying device registry IDs.
2023-04-25 lexa.knyazev@gmail.com GL: Enable NV_shader_noperspective_interpolation on ES
2023-04-25 lexa.knyazev@gmail.com GL: Fix readPixels for snorm color buffers
2023-04-25 geofflang@chromium.org D3D11: Fix instanced vertex streaming data copies.
2023-04-25 syoussefi@chromium.org Vulkan: Use Android TLS for *valid* global context

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,ianelliott@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1425606,chromium:1433180,chromium:1433697
Tbr: ianelliott@google.com
Change-Id: Ib48895150500e632a673114061a0509a1236fa7b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4475647
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1135445}

[modify] https://crrev.com/291c1427a82d0af02136923943ab3513386cb69f/DEPS


### ge...@chromium.org (2023-04-26)

This fix landed in the same version as the regression (114) so no merge is necessary. 

### [Deleted User] (2023-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

Not requesting merge to dev (M114) because latest trunk commit (1135445) appears to be prior to dev branch point (1135570). If this is incorrect, please replace the Merge-NA-114 label with Merge-Request-114. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-05)

Congratulations! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1433180?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064044)*
