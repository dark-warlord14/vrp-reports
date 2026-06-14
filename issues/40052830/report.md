# Security: Google Chrome DrawElementsInstanced Information Leak Vulnerability (TALOS-2020-1123)

| Field | Value |
|-------|-------|
| **Issue ID** | [40052830](https://issues.chromium.org/issues/40052830) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | vu...@sourcefire.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2020-07-13 |
| **Bounty** | $1,000.00 |

## Description

### Summary

An information disclosure vulnerability exists in the WebGL  functionality of Google Chrome 83.0.4103.116 (Stable) (64-bit) and 86.0.4198.0 (Developer Build) (64-bit). A specially crafted javascript can cause an out-of-bounds read. In order to trigger this vulnerability, victim must visit a malicious web page.


### Tested Versions

Google Chrome 83.0.4103.116 (Stable) (64-bit)   
Google Chrome 86.0.4198.0 (Developer Build) (64-bit)   


### Product URLs

[https://www.google.com/chrome/](https://www.google.com/chrome/)


### CVSSv3 Score

6.8 - CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:L/A:L

## Attachments

- [TALOS-2020-1123.txt](attachments/TALOS-2020-1123.txt) (text/plain, 18.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 3.1 KB)

## Timeline

### cl...@chromium.org (2020-07-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5691815553990656.

### mm...@google.com (2020-07-14)

FYI, ClusterFuzz managed to reproduce this, it's still bisecting the regression range now.

### cl...@chromium.org (2020-07-14)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/angle/angle/+/1e85326695b5150d20d404ed6596f49452bd01ff (Cache common DrawElements states.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2020-07-14)

Detailed Report: https://clusterfuzz.com/testcase?key=5691815553990656

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000041414141
Crash State:
  gl::ComputeIndexRange
  gl::VertexArray::getIndexRangeImpl
  gl::ValidateDrawElementsInstancedBase
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=618729:618730

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5691815553990656

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5691815553990656 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### [Deleted User] (2020-07-14)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2020-07-14)

Reproduced with the attached test and in a standalone test. Can confirm this is a real bug affecting shipping Chrome. Looking into a fix. Should be Windows-only.

[Monorail components: Internals>GPU>ANGLE]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f9e01f1230dc23c867c059ad62482202554d3860

commit f9e01f1230dc23c867c059ad62482202554d3860
Author: Jamie Madill <jmadill@chromium.org>
Date: Wed Jul 15 15:01:23 2020

Fix stale validation cache on buffer deletion.

When we would delete the currently bound element array buffer we
would neglect to invalidate a specific validation cache variable.
This incorrectly would let us skip buffer size validation and lead
to internal invalid memory accesses.

Bug: chromium:1105202
Change-Id: I23ab28ccd3ac6b5d461cb8745b930f4d42d53b35
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2298145
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/f9e01f1230dc23c867c059ad62482202554d3860/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/f9e01f1230dc23c867c059ad62482202554d3860/src/libANGLE/Context.cpp
[modify] https://crrev.com/f9e01f1230dc23c867c059ad62482202554d3860/src/libANGLE/Context.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9e558a911dfbbbc9b88bc61c9558ec8270ce3b4f

commit 9e558a911dfbbbc9b88bc61c9558ec8270ce3b4f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jul 15 19:34:38 2020

Roll ANGLE from c44b2b2567ae to 9277ee741395 (2 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/c44b2b2567ae..9277ee741395

2020-07-15 lehoangq@gmail.com Metal: Implement MSAA default framebuffer.
2020-07-15 jmadill@chromium.org Fix stale validation cache on buffer deletion.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jonahr@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win-asan;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1105202
Tbr: jonahr@google.com
Change-Id: I20ba4fe11548660d3a0203425f1c64fc98ee85f6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2300289
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#788753}

[modify] https://crrev.com/9e558a911dfbbbc9b88bc61c9558ec8270ce3b4f/DEPS


### jm...@chromium.org (2020-07-15)

Marking fixed. Will let this bake for a few days then request merges to 85 and 84.

### jm...@chromium.org (2020-07-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-16)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/88f65ceefdae0dcc05f1dc281354ea34890d795d

commit 88f65ceefdae0dcc05f1dc281354ea34890d795d
Author: skia-autoroll <skia-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jul 16 05:25:04 2020

Roll ANGLE from 4ad0f250a010 to 6fe87f4a226d (14 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/4ad0f250a010..6fe87f4a226d

2020-07-15 cnorthrop@google.com Tests: Change screen orientation for traces on Android
2020-07-15 nguyenmh@google.com Add buffer serialization capability
2020-07-15 jonahr@google.com GL: Fix issue with EXTBlendFuncExtendedES3DrawTest
2020-07-15 jmadill@chromium.org Test Runner: Accept Chromium args.
2020-07-15 kbr@chromium.org Revise documentation on adding EGL extensions.
2020-07-15 cnorthrop@google.com Capture/Replay: More ES 3.1 support
2020-07-15 shrekshao@google.com Fix ANGLE_base_vertex_base_instance baseInstances type
2020-07-15 lehoangq@gmail.com Metal: Compile default shader source files separately.
2020-07-15 lehoangq@gmail.com Metal: Implement MSAA default framebuffer.
2020-07-15 jmadill@chromium.org Fix stale validation cache on buffer deletion.
2020-07-15 angle-autoroll@skia-public.iam.gserviceaccount.com Roll glslang from fe24a54808c2 to b481744aea1e (5 revisions)
2020-07-15 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SPIRV-Tools from 94667fbf66ee to 4c33fb0d3dba (12 revisions)
2020-07-15 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from cd0af6456eb1 to 1de497cc50ab (3 revisions)
2020-07-15 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Vulkan-Loader from 0bc4c2ae7012 to d8f34456c819 (2 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-skia-autoroll
Please CC nifong@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: skia/skia.primary:Build-Debian10-Clang-x86_64-Release-ANGLE;skia/skia.primary:Test-Win10-Clang-AlphaR2-GPU-RadeonR9M470X-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-Golo-GPU-QuadroP400-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-NUC5i7RYH-GPU-IntelIris6100-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-NUC6i5SYK-GPU-IntelIris540-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-NUC8i5BEK-GPU-IntelIris655-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-NUCD34010WYKH-GPU-IntelHD4400-x86_64-Debug-All-ANGLE
Bug: chromium:1099763,chromium:1105202
Tbr: nifong@google.com
Test: Test: Capture from beginning of Asphalt 8 and Aztec Ruins
Change-Id: I42c068c939ac8612f1d68fd545a6b40a1bd55357
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/303196
Reviewed-by: skia-autoroll <skia-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: skia-autoroll <skia-autoroll@skia-public.iam.gserviceaccount.com>

[modify] https://crrev.com/88f65ceefdae0dcc05f1dc281354ea34890d795d/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0ded56a91a748743a9448662ab9cd30f9cbbca76

commit 0ded56a91a748743a9448662ab9cd30f9cbbca76
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jul 16 16:15:20 2020

Roll Skia from 06980dba90a4 to 2b4404b14b04 (29 revisions)

https://skia.googlesource.com/skia.git/+log/06980dba90a4..2b4404b14b04

2020-07-16 mtklein@google.com JIT to_half/from_half
2020-07-16 bsalomon@google.com Revert "Don't avoid disabling subset for planar image draws"
2020-07-16 egdaniel@google.com Using staging buffers for vulkan texture uploads.
2020-07-16 skia-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 4ad0f250a010 to 6fe87f4a226d (14 revisions)
2020-07-16 skia-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 1de497cc50ab to 0a8f44c514ce (1 revision)
2020-07-16 skia-autoroll@skia-public.iam.gserviceaccount.com Roll dawn from b31f5e717e2d to 1b9b53a39576 (9 revisions)
2020-07-16 fmalita@chromium.org [skottie] Fix mask difference
2020-07-15 jvanverth@google.com Change hairline pathrenderer to avoid vertex buffer reads.
2020-07-15 robertphillips@google.com Switch the DDLRecorder over to holding a GrRecordingContext ...
2020-07-15 bsalomon@google.com Rename GrSamplerState::Filter::kBilerp to kLinear
2020-07-15 bungeman@google.com Remove SkFontArguments::Axis.
2020-07-15 mtklein@google.com a bunch of half-related stuff
2020-07-15 elliotevans@google.com Fix experimental_simd CanvasKit build.
2020-07-15 adlai@google.com Remove makeSubset compatibility flag
2020-07-15 egdaniel@google.com Reland "Roll dawn from 0d52f800a1d1 to b31f5e717e2d (4 revisions)"
2020-07-15 bungeman@google.com Implement SkFontMgr::onMakeFromFontData in subclasses.
2020-07-15 michaelludwig@google.com Support releasing blocks while iterating them
2020-07-15 jvanverth@google.com Add new GM to test hairline subdivision.
2020-07-15 jlavrova@google.com add SkParagraph to public headers and fix warnings
2020-07-15 fmalita@chromium.org [skottie] Improved pucker/bloat center heuristic
2020-07-15 michaelludwig@google.com Generalize iterator in GrTAllocator to be useful for other data types
2020-07-15 adlai@google.com Reland "Add a direct context arg to makeColorTypeAndColorSpace"
2020-07-15 mtklein@google.com minor skvm cleanup
2020-07-15 brianosman@google.com Clean up some boilerplate in runtimeshader.cpp
2020-07-15 mtklein@google.com add store(PixelFormat,...)
2020-07-15 mtklein@google.com generalize skvm pixel unpacking
2020-07-15 michaelludwig@google.com QoL improvements to GrTAllocator
2020-07-15 herb@google.com Reland "rename MakePath to Make"
2020-07-15 bsalomon@google.com Don't avoid disabling subset for planar image draws

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC nifong@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Bug: chromium:1070089,chromium:1099763,chromium:1105202
Tbr: nifong@google.com
Test: Test: Test: Capture from beginning of Asphalt 8 and Aztec Ruins
Change-Id: Icdcffce483bc4f282e6a7c9e1b446d75834d37f6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2302220
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#789070}

[modify] https://crrev.com/0ded56a91a748743a9448662ab9cd30f9cbbca76/DEPS


### ge...@chromium.org (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-07-16)

ClusterFuzz testcase 5691815553990656 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=788728:788753

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ad...@chromium.org (2020-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-20)

Requesting merge to beta M84 because latest trunk commit (789070) appears to be after beta branch point (768962).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-20)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vu...@sourcefire.com (2020-07-20)

Is there a planned release/disclosure date for this issue?

### jm...@chromium.org (2020-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-21)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2020-07-21)

1. not sure
2. https://chromium.googlesource.com/angle/angle/+/f9e01f1230dc23c867c059ad62482202554d3860
3. change is verified by clusterfuzz and has baked in Canary for a while
4. closes security hole (information leak according to reporter)
5. no new features
6. n/a

### sr...@google.com (2020-07-21)

Merge approved for M85 branch:4183 please merge asap

### ad...@google.com (2020-07-23)

jmadill@ I'd like to approve merge to M84 per https://crbug.com/chromium/1105202#c10, but please can I have some comments on the risk levels here? As I'm sure you know, to merge things to the current stable release they have to be entirely risk-free as we miss out on much of our usual bake time. Can you confirm this is extremely low-risk?

vulndiscovery@sourcefire.com, thanks for the report. We'll likely be releasing the fix sometime within the next four weeks, at which point there will be a CVE and a mention in the Chrome release notes; the bug will be opened up to public view 14 weeks after the fix date.

### jm...@chromium.org (2020-07-23)

adetaylor@ - please see the effective diff here

https://chromium-review.googlesource.com/c/angle/angle/+/2298145/2/src/libANGLE/Context.cpp

This change invalidates a specific cache that was missing an important refresh. If there were some problem with the change it would have popped up by now. I would say minimal risk that this introduces unexpected bugs.

srinivassista@ Will merge to M85 today.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/034a8b3f3c5c8e7e1629b8ac88cadb72ea68cf23

commit 034a8b3f3c5c8e7e1629b8ac88cadb72ea68cf23
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Jul 23 22:32:44 2020

Fix stale validation cache on buffer deletion.

When we would delete the currently bound element array buffer we
would neglect to invalidate a specific validation cache variable.
This incorrectly would let us skip buffer size validation and lead
to internal invalid memory accesses.

Bug: chromium:1105202
Change-Id: I23ab28ccd3ac6b5d461cb8745b930f4d42d53b35
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2315622
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/034a8b3f3c5c8e7e1629b8ac88cadb72ea68cf23/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/034a8b3f3c5c8e7e1629b8ac88cadb72ea68cf23/src/libANGLE/Context.cpp
[modify] https://crrev.com/034a8b3f3c5c8e7e1629b8ac88cadb72ea68cf23/src/libANGLE/Context.h


### ad...@google.com (2020-07-24)

Thanks. In that case approving merge to M84, branch 4147.

### ad...@google.com (2020-07-24)

Thanks. In that case approving merge to M84, branch 4147.

### [Deleted User] (2020-07-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/af5b008a9546a632ae6dc227e038e3e693b409c6

commit af5b008a9546a632ae6dc227e038e3e693b409c6
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Jul 28 16:45:56 2020

Fix stale validation cache on buffer deletion.

When we would delete the currently bound element array buffer we
would neglect to invalidate a specific validation cache variable.
This incorrectly would let us skip buffer size validation and lead
to internal invalid memory accesses.

Bug: chromium:1105202
Change-Id: I23ab28ccd3ac6b5d461cb8745b930f4d42d53b35
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2323644
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/af5b008a9546a632ae6dc227e038e3e693b409c6/src/libANGLE/Context.cpp
[modify] https://crrev.com/af5b008a9546a632ae6dc227e038e3e693b409c6/src/libANGLE/Context.h


### ad...@google.com (2020-07-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2020-09-14)

Is this issue ready for public disclosure?

### ad...@chromium.org (2020-09-14)

It will be opened to the public 14 weeks after it's fixed, which looks like October 22nd.

### vu...@sourcefire.com (2020-09-14)

The issue reaches 90 days on October 13th. Per our disclosure release policy, it is subject to disclosure when reaches 90 days. Is there a way to move this within the 90 day timeframe?

### ad...@google.com (2020-09-14)

vulndiscovery@ thanks. I'm happy to open up this bug on October 13th. Please feel free to get in touch once you've published your information and I'll remove view restrictions. See https://crbug.com/chromium/1107433 for some general thoughts on how your disclosure policy lines up with ours.

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2020-10-13)

We are publishing the advisory on our end. Please remove view restrictions. Thank you



### ad...@google.com (2020-10-13)

Done. Thanks.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1105202?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052830)*
