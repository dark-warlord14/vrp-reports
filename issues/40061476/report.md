# Out of bound write in GPU

| Field | Value |
|-------|-------|
| **Issue ID** | [40061476](https://issues.chromium.org/issues/40061476) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>SwiftShader, Internals>GPU>Testing |
| **Platforms** | Mac, Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2022-10-26 |
| **Bounty** | $15,000.00 |

## Description

**Steps to reproduce the problem:**  

Attached asan log, will attach details soon.

**Problem Description:**  

GPU oob write

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.5383.0 \*\*Channel: \*\* Canary

**OS:** Mac OS

## Attachments

- [asan_log.txt](attachments/asan_log.txt) (text/plain, 29.6 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 13.9 KB)
- [mini.html](attachments/mini.html) (text/plain, 250 B)
- [asan.txt](attachments/asan.txt) (text/plain, 14.3 KB)

## Timeline

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-10-26)

[Comment Deleted]

### ha...@gmail.com (2022-10-26)

Seems that the asan log stack is not stable, attached another occured stack.

### ha...@gmail.com (2022-10-26)

update with the new minimized poc

### me...@chromium.org (2022-10-26)

sugoi, could you PTAL?

[Monorail components: Internals>GPU>SwiftShader]

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### su...@chromium.org (2022-10-26)

Hi, I just did a fresh ASAN Chromium build, version: 109.0.5384.0 (Developer Build) (x86_64)
I tried both:
- mini.html
- poc_1378476.html

I did not encounter an ASAN error.

I used the following GN args:
dcheck_always_on = true
enable_nacl = false
is_asan = true
is_component_build = false
is_debug = false
symbol_level = 1

happyercat@, what GN args did you use to build Chromium ASAN?

### ha...@gmail.com (2022-10-27)

[Comment Deleted]

### ha...@gmail.com (2022-10-27)

Helo, the GN args I'm using:

is_asan=true
is_component_build=true
dcheck_always_on=false
is_debug=false

Moreover, I reproduce it on 109.0.5383.0 Arm Chromium with m1pro chip, not sure if it matters. Seems that the 109.0.5384.0 version hasn't been roll out yet.

### ha...@gmail.com (2022-10-27)

[Comment Deleted]

### su...@chromium.org (2022-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-27)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2022-10-27)

I'm able to reproduce this on my M1 Macbook Pro


### su...@chromium.org (2022-10-28)

I'll try to help Jonah debug this early next week. I'm mostly suspecting that this is an ASAN instrumentation error on M1, but I haven't ruled out that this could be a real memory problem yet.

### su...@chromium.org (2022-11-03)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-11-03)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-09)

hello your friendly security sheriff here, have you determined whether this is a real issue or not yet?

### jo...@google.com (2022-11-10)

Hi, we put some work into this last week but weren't able to make progress, and have some other high priority work going on. @sugoi what do you suggest we do?

### jo...@google.com (2022-11-10)

[Empty comment from Monorail migration]

### jo...@google.com (2022-11-10)

The way I've managed to avoid this crash is in VertexRoutine::writeCache: https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/src/Pipeline/VertexRoutine.cpp;l=570;drc=76ee012c8192bdfd62f59e451cc5ecd8aaf6e3c1?q=VertexRoutine::writeCa&sq=&ss=chromium%2Fchromium%2Fsrc

By commenting out the output builtins for spv::BuiltInPosition and spv::BuiltInPointSize, it doesn't hit the oob write.

### su...@chromium.org (2022-11-15)

[Empty comment from Monorail migration]

### su...@chromium.org (2022-11-15)

Yuly pointed out that ASAN on MacOS ARM isn't explicitly supported. See:
https://github.com/google/sanitizers/wiki/AddressSanitizer

### jo...@google.com (2022-11-17)

In that case I'll close this out.

### ha...@gmail.com (2022-11-22)

[Comment Deleted]

### jo...@google.com (2022-11-22)

Okay, I'l reopen this. Thanks for looking into this more!

### ha...@gmail.com (2022-11-23)

[Comment Deleted]

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### ni...@google.com (2022-11-23)

Thanks for the deeper look! We're still using LLVM 10 as the JIT-compiler for ARMv8, which I suspect doesn't properly support the M1 CPU.

[Monorail blocked-on: b/165000222]

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

jonahr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-12-07)

[security marshal] Hi nicolascapens@! Just following up on the status of the LLVM upgrade status. b/165000222 hasn't been updated since Sep 7, 2022. Can you provide any update? 

Also, is jonahr@ the correct owner for this bug? Thanks!

### pb...@google.com (2022-12-07)

[BULK EDIT] M109 Stable RC cut  date is fast approaching(Jan 03rd), we need to start resolving this issue as it is marked as a Stable blocker. Please update with a plan for resolution.

### an...@chromium.org (2022-12-07)

Chatted offline with sugoi@. It looks like an LLVM upgrade is unlikely to happen in the near term due to staffing & priority issues. Instead, should we consider disabling SwiftShader on all ARM devices? These are the first ones we ship SwiftShader to and apparently there may not be enough test coverage from Chromium on those devices.

Adding kbr@ and geofflang@ to CC list as well to help converge on a plan-of-action soon since this is a Stable blocker.

### an...@chromium.org (2022-12-07)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-12-07)

Victor, would the switch to a V8-based shader stack address this issue?

### jm...@chromium.org (2022-12-07)

Jonahr is probably not the right owner.

### vm...@chromium.org (2022-12-07)

@jmadill - it seems likely that it could, if we're having problems with LLVM.

Have we confirmed that the generated IR is correct?

### jo...@google.com (2022-12-07)

I have this CL up if we want to disable SwiftShader on ARM: https://chromium-review.googlesource.com/c/chromium/src/+/4086205

### jm...@chromium.org (2022-12-07)

My bad, thought it was a SwS-specific task. Sending back to you for the disable.

### jo...@google.com (2022-12-07)

Are we okay with landing the CL in https://crbug.com/chromium/1378476#c40, or is it better to go with the solution proposed in https://crbug.com/chromium/1378476#c37?

### su...@chromium.org (2022-12-07)

Doing https://crbug.com/chromium/1378476#c37 would take months of development, so go with the CL in https://crbug.com/chromium/1378476#c40.

### gi...@appspot.gserviceaccount.com (2022-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/96a4a5a1fde16180ecf60218cd232416df331764

commit 96a4a5a1fde16180ecf60218cd232416df331764
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Wed Dec 07 22:33:26 2022

Disable SwiftShader on ARM Macs

SwiftShader uses LLVM 10 as its JIT, which is not supported on ARM.
Disable SwiftShader on ARM Macs until LLVM is updated.

Bug: chromium:1378476
Change-Id: I477de747d11f2a3675905fa035ab3f47dcf55571
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4086205
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Alexis Hétu <sugoi@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1080607}

[modify] https://crrev.com/96a4a5a1fde16180ecf60218cd232416df331764/ui/gl/init/gl_factory_mac.cc


### jo...@google.com (2022-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-08)

Merge review required: M109 is already shipping to beta.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### jo...@google.com (2022-12-12)

1. Release blocker
2. https://chromium-review.googlesource.com/c/chromium/src/+/4086205
3. Yes, landed on Dec 7
4. No
5. -
6. No

### am...@chromium.org (2022-12-12)

M109 merge approved, please merge this CL to branch 5414 as soon as possible before 3pm Pacific tomorrow/ Tuesday, 13 December so this fix can be included in the next M109 Stable -- thank you! 

### ha...@gmail.com (2022-12-13)

Hello, I found that this could still be reproduced on the ToT chromium.

After digging it deeper, seems that only remove `gl::ANGLEImplementation::kSwiftShader` in `GetAllowedGLImplementations` function is not enough to disable swiftshader.

The swiftshader (e.g., swiftshader-webgl here) could be added automatically if we doesn't specify the angle implementation name in `use-gl` switch in [1][2][3]. Seems that the automatically added swiftshader name could then be fetched in [5] and selected in [4], since the `GLImplementationParts::IsAllowed` function only checks if the matched implementation is ANGLE.

Hence maybe we could add additional check in `GLImplementationParts GetRequestedGLImplementation` (i.e., skip the code [4] on Arm Mac), or we could set additional condition to `enable_swiftshader` flag (turn off `enable_swiftshader` on arm Mac) in [7]. 

Thank you very much.

[1]https://source.chromium.org/chromium/chromium/src/+/main:gpu/ipc/service/gpu_init.cc;l=431-435;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29

[2]https://source.chromium.org/chromium/chromium/src/+/main:gpu/config/gpu_util.cc;l=813;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29

[3]https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/gl_implementation.cc;l=278-280;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29

[4]https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/init/gl_factory.cc;l=111-112;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29

[5]https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/gl_implementation.cc;l=310-326;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29

[6]https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/gl_implementation.cc;l=39;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29

[7]https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/features.gni;l=30-37;drc=cdd8b38358066d4f9ea3c1cc442c29dc70010fc0

### pb...@google.com (2022-12-13)

Your merge has been approved for M109, please help complete your merges asap (before 2pm PST) today, so the change can be included in this week's RC build for beta releases.

We would like to get the changes as much beta time as possible, so please complete your merges asap to M109 branch(go/chrome-branches).

### jo...@google.com (2022-12-13)

Working on a fix that will affect this issue as well as https://crbug.com/chromium/1231934

### gi...@appspot.gserviceaccount.com (2022-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/63a75619ae2c6c59c1e98135b19231d2ff2fd1e8

commit 63a75619ae2c6c59c1e98135b19231d2ff2fd1e8
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Tue Dec 13 16:18:53 2022

[M109] Disable SwiftShader on ARM Macs

SwiftShader uses LLVM 10 as its JIT, which is not supported on ARM.
Disable SwiftShader on ARM Macs until LLVM is updated.

(cherry picked from commit 96a4a5a1fde16180ecf60218cd232416df331764)

Bug: chromium:1378476
Change-Id: I477de747d11f2a3675905fa035ab3f47dcf55571
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4086205
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Alexis Hétu <sugoi@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1080607}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4098247
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#689}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/63a75619ae2c6c59c1e98135b19231d2ff2fd1e8/ui/gl/init/gl_factory_mac.cc


### jo...@google.com (2022-12-13)

The CL is up here: https://chromium-review.googlesource.com/c/chromium/src/+/4102520
I'm currently testing on multiple platforms, I believe this should fix this issue and fully disable swiftshader.

### am...@chromium.org (2022-12-14)

reopening as it does not appear this issue was resolved 

### gi...@appspot.gserviceaccount.com (2022-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/25a6dc248bc0f4bc91adb4a313bba2988437cf13

commit 25a6dc248bc0f4bc91adb4a313bba2988437cf13
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Tue Dec 20 20:16:56 2022

Fix bugs in ANGLE backend selection

This CL does the following:
1. Fixes the unexpected behavior where in order to omit the --use-angle
flag, it's necessary to have ANGLEImplementation::kDefault explicitly
added to the allowed_impls list.
2. Fixes the case where ANGLE is allowed to select an explicitly
prohibited backend via omitting the --use-angle flag and choosing
its default backend.
3. Removes kDefault as an option from lists of allowed_impls that are
expected to explicitly prohibit certain ANGLE backends.
4. Cleans up allowed_impls lists that add kDefault explicitly or
implicitly via GLImplementationEGLANGLE, and also add unnecessary
redundant explicit ANGLE backend implementations to the same list.
5. In cases where the GLImplementation was set programmatically on
init (mostly tests) and it's not specified in the command-line, use
whichever ANGLE implementation was already set.
6. Fix a missing case where OpenGL-EGL and OpenGLES-EGL backends
were not setting the correct GLImplementation.

The effects should make ANGLE backend selection work as follows:
- If no ANGLE backend is chosen via explicit request (ie --use-angle),
then the allowed default backend will be chosen.
- If an invalid ANGLE backend is chosen via explicit request, then
we will fall back to either the default backend, or swiftshader,
depending on the failure mechanism.
- If a valid ANGLE backend is chosen, it will be used.
- If either of the two following options are added to the
allowed_impls list, then all ANGLE backends are considered valid:
  - gl::kGLImplementationEGLANGLE
  - gl::ANGLEImplementation::kDefault

One noted edge case I found was the case where both ANGLE's internal
default backend was explicitly disallowed, and the swiftshader
backend was explicitly disallowed, then by specifying an invalid
backend, ANGLE would fallback to initializing with the ANGLE display
type DEFAULT, which would initialize the default backend that was
supposed to be explicitly disallowed. Currently there aren't any
platforms that use this setup, so this isn't an issue right now. If we
ever need to add a platform which can only be initialized with a
secondary backend (like vulkan or metal), we will need to change this
behavior.

Bug: chromium:1378476
Bug: chromium:1231934
Bug: chromium:1400043
Change-Id: Idca3efc512494e1f7725187c58a7ea2508778df8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4102520
Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: ccameron chromium <ccameron@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1085609}

[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/egl_api_unittest.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/gl_initializer_win.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/chrome/browser/vr/test/gl_test_environment_unittest.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/ozone/platform/scenic/scenic_surface_factory.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/ozone/platform/flatland/flatland_surface_factory.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/gl_factory_mac.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/gl_factory_android.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/gl_initializer_mac.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/ozone/platform/x11/x11_surface_factory.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/test/egl_initialization_displays_unittest.cc
[add] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/gl_display_initializer.h
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/BUILD.gn
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/gl_factory_win.cc
[add] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/gl_display_initializer.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/gl_initializer_android.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/ozone/common/gl_ozone_egl.h
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/gl_implementation.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/init/gl_initializer_ozone.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/gl_display.h
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/gl/gl_display.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/chrome/browser/vr/ui_pixeltest.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/ozone/platform/headless/headless_surface_factory.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/ozone/common/gl_ozone_egl.cc
[modify] https://crrev.com/25a6dc248bc0f4bc91adb4a313bba2988437cf13/ui/ozone/public/gl_ozone.h


### gi...@appspot.gserviceaccount.com (2022-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0

commit f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0
Author: Shrek Shao <shrekshao@google.com>
Date: Tue Dec 20 22:39:33 2022

Revert "Fix bugs in ANGLE backend selection"

This reverts commit 25a6dc248bc0f4bc91adb4a313bba2988437cf13.

Reason for revert: Failing Lacros FYI x64 Release (Intel)

Original change's description:
> Fix bugs in ANGLE backend selection
>
> This CL does the following:
> 1. Fixes the unexpected behavior where in order to omit the --use-angle
> flag, it's necessary to have ANGLEImplementation::kDefault explicitly
> added to the allowed_impls list.
> 2. Fixes the case where ANGLE is allowed to select an explicitly
> prohibited backend via omitting the --use-angle flag and choosing
> its default backend.
> 3. Removes kDefault as an option from lists of allowed_impls that are
> expected to explicitly prohibit certain ANGLE backends.
> 4. Cleans up allowed_impls lists that add kDefault explicitly or
> implicitly via GLImplementationEGLANGLE, and also add unnecessary
> redundant explicit ANGLE backend implementations to the same list.
> 5. In cases where the GLImplementation was set programmatically on
> init (mostly tests) and it's not specified in the command-line, use
> whichever ANGLE implementation was already set.
> 6. Fix a missing case where OpenGL-EGL and OpenGLES-EGL backends
> were not setting the correct GLImplementation.
>
> The effects should make ANGLE backend selection work as follows:
> - If no ANGLE backend is chosen via explicit request (ie --use-angle),
> then the allowed default backend will be chosen.
> - If an invalid ANGLE backend is chosen via explicit request, then
> we will fall back to either the default backend, or swiftshader,
> depending on the failure mechanism.
> - If a valid ANGLE backend is chosen, it will be used.
> - If either of the two following options are added to the
> allowed_impls list, then all ANGLE backends are considered valid:
>   - gl::kGLImplementationEGLANGLE
>   - gl::ANGLEImplementation::kDefault
>
> One noted edge case I found was the case where both ANGLE's internal
> default backend was explicitly disallowed, and the swiftshader
> backend was explicitly disallowed, then by specifying an invalid
> backend, ANGLE would fallback to initializing with the ANGLE display
> type DEFAULT, which would initialize the default backend that was
> supposed to be explicitly disallowed. Currently there aren't any
> platforms that use this setup, so this isn't an issue right now. If we
> ever need to add a platform which can only be initialized with a
> secondary backend (like vulkan or metal), we will need to change this
> behavior.
>
> Bug: chromium:1378476
> Bug: chromium:1231934
> Bug: chromium:1400043
> Change-Id: Idca3efc512494e1f7725187c58a7ea2508778df8
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4102520
> Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
> Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
> Reviewed-by: ccameron chromium <ccameron@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1085609}

Bug: chromium:1378476
Bug: chromium:1231934
Bug: chromium:1400043
Change-Id: I4384f263fc742f01c2dfa26a3c62495be5fb4603
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4117441
Owners-Override: Shrek Shao <shrekshao@google.com>
Commit-Queue: Shrek Shao <shrekshao@google.com>
Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Shrek Shao <shrekshao@google.com>
Cr-Commit-Position: refs/heads/main@{#1085671}

[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/egl_api_unittest.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/init/gl_initializer_win.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/chrome/browser/vr/test/gl_test_environment_unittest.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/ozone/platform/scenic/scenic_surface_factory.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/ozone/platform/flatland/flatland_surface_factory.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/init/gl_factory_mac.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/init/gl_factory_android.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/init/gl_initializer_mac.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/test/egl_initialization_displays_unittest.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/ozone/platform/x11/x11_surface_factory.cc
[delete] https://crrev.com/406e0a01358ae58e5b902ab0fb6066908b688558/ui/gl/init/gl_display_initializer.h
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/init/BUILD.gn
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/init/gl_factory_win.cc
[delete] https://crrev.com/406e0a01358ae58e5b902ab0fb6066908b688558/ui/gl/init/gl_display_initializer.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/init/gl_initializer_android.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/gl_implementation.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/ozone/common/gl_ozone_egl.h
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/gl_display.h
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/init/gl_initializer_ozone.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/gl/gl_display.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/chrome/browser/vr/ui_pixeltest.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/ozone/platform/headless/headless_surface_factory.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/ozone/common/gl_ozone_egl.cc
[modify] https://crrev.com/f44fc861ab51332d4c55de8039cc0f3f8b3a2ab0/ui/ozone/public/gl_ozone.h


### kb...@chromium.org (2022-12-21)

For the record, the first failing build:
https://ci.chromium.org/ui/p/chromium/builders/ci/Lacros%20FYI%20x64%20Release%20(Intel)/21607/overview

and the first passing build after the revert:
https://ci.chromium.org/ui/p/chromium/builders/ci/Lacros%20FYI%20x64%20Release%20(Intel)/21611/overview

Tests running the validating command decoder (no ANGLE, at least theoretically) were failing. Here's one shard:
https://chromium-swarm.appspot.com/task?id=5f4a351fb624de10

The browser was started with --use-cmd-decoder=validating, but once started it was actually using ANGLE and the passthrough command decoder:
  gl_renderer         : ANGLE (Intel Open Source Technology Center, Mesa DRI Intel(R) UHD Graphics 630 (CML GT2), OpenGL ES 3.2 Mesa 20.0.8)
  passthrough_cmd_decoder: True

and all tests failed for this reason:
  Traceback (most recent call last):
    File "/b/s/w/ir/third_party/catapult/telemetry/telemetry/testing/serially_executed_browser_test_case.py", line 318, in <lambda>
      return lambda self: based_method(self, *args)
    File "/b/s/w/ir/content/test/gpu/gpu_tests/gpu_integration_test.py", line 494, in _RunGpuTest
      self.RunActualGpuTest(url, args)
    File "/b/s/w/ir/content/test/gpu/gpu_tests/webgl_conformance_integration_test_base.py", line 211, in RunActualGpuTest
      getattr(self, test_name)(test_path, test_args)
    File "/b/s/w/ir/content/test/gpu/gpu_tests/webgl_conformance_integration_test_base.py", line 310, in _RunExtensionTest
      self._NavigateTo(test_path, _GetExtensionHarnessScript())
    File "/b/s/w/ir/content/test/gpu/gpu_tests/webgl_conformance_integration_test_base.py", line 274, in _NavigateTo
      and self._VerifyCommandDecoder(gpu_info)):
    File "/b/s/w/ir/content/test/gpu/gpu_tests/webgl_conformance_integration_test_base.py", line 261, in _VerifyCommandDecoder
      self.fail('requested command decoder (' + self._command_decoder + ')' +
  AssertionError: requested command decoder (validating) had no effect on the browser: primary gpu=ANGLE (Intel Open Source Technology Center, Mesa DRI Intel(R) UHD Graphics 630 (CML GT2), OpenGL ES 3.2 Mesa 20.0.8), gl_renderer=ANGLE (Intel Open Source Technology Center, Mesa DRI Intel(R) UHD Graphics 630 (CML GT2), OpenGL ES 3.2 Mesa 20.0.8)

after the revert, the validating command decoder was used as expected:
https://chromium-swarm.appspot.com/task?id=5f4aad6e0d6ba610
  gl_renderer         : Mesa DRI Intel(R) UHD Graphics 630 (CML GT2)
  passthrough_cmd_decoder: False


[Monorail components: Internals>GPU>ANGLE Internals>GPU>Testing]

### gi...@appspot.gserviceaccount.com (2022-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9620c12777040b697cd8d3c5927c1e40edf1094b

commit 9620c12777040b697cd8d3c5927c1e40edf1094b
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Wed Dec 21 19:44:22 2022

Reland: "Fix bugs in ANGLE backend selection"

This is a reland of 25a6dc248bc0f4bc91adb4a313bba2988437cf13

The failure was related to enabling ANGLE on Lacros. I've split this
up into a separate change now.

Original change's description:
> This CL does the following:
> 1. Fixes the unexpected behavior where in order to omit the --use-angle
> flag, it's necessary to have ANGLEImplementation::kDefault explicitly
> added to the allowed_impls list.
> 2. Fixes the case where ANGLE is allowed to select an explicitly
> prohibited backend via omitting the --use-angle flag and choosing
> its default backend.
> 3. Removes kDefault as an option from lists of allowed_impls that are
> expected to explicitly prohibit certain ANGLE backends.
> 4. Cleans up allowed_impls lists that add kDefault explicitly or
> implicitly via GLImplementationEGLANGLE, and also add unnecessary
> redundant explicit ANGLE backend implementations to the same list.
> 5. In cases where the GLImplementation was set programmatically on
> init (mostly tests) and it's not specified in the command-line, use
> whichever ANGLE implementation was already set.
> 6. Fix a missing case where OpenGL-EGL and OpenGLES-EGL backends
> were not setting the correct GLImplementation.
>
> The effects should make ANGLE backend selection work as follows:
> - If no ANGLE backend is chosen via explicit request (ie --use-angle),
> then the allowed default backend will be chosen.
> - If an invalid ANGLE backend is chosen via explicit request, then
> we will fall back to either the default backend, or swiftshader,
> depending on the failure mechanism.
> - If a valid ANGLE backend is chosen, it will be used.
> - If either of the two following options are added to the
> allowed_impls list, then all ANGLE backends are considered valid:
>   - gl::kGLImplementationEGLANGLE
>   - gl::ANGLEImplementation::kDefault
>
> One noted edge case I found was the case where both ANGLE's internal
> default backend was explicitly disallowed, and the swiftshader
> backend was explicitly disallowed, then by specifying an invalid
> backend, ANGLE would fallback to initializing with the ANGLE display
> type DEFAULT, which would initialize the default backend that was
> supposed to be explicitly disallowed. Currently there aren't any
> platforms that use this setup, so this isn't an issue right now. If we
> ever need to add a platform which can only be initialized with a
> secondary backend (like vulkan or metal), we will need to change this
> behavior.
>
> Bug: chromium:1378476
> Bug: chromium:1231934
> Bug: chromium:1400043
> Change-Id: Idca3efc512494e1f7725187c58a7ea2508778df8
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4102520
> Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
> Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
> Reviewed-by: ccameron chromium <ccameron@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1085609}

Bug: chromium:1378476
Bug: chromium:1231934
Bug: chromium:1400043
Change-Id: I185f2819dfda19ac2779c328f39068357c6ff0aa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4119407
Reviewed-by: ccameron chromium <ccameron@chromium.org>
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1086028}

[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/egl_api_unittest.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/gl_initializer_win.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/chrome/browser/vr/test/gl_test_environment_unittest.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/ozone/platform/scenic/scenic_surface_factory.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/ozone/platform/flatland/flatland_surface_factory.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/gl_factory_mac.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/gl_initializer_mac.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/gl_factory_android.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/test/egl_initialization_displays_unittest.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/ozone/platform/x11/x11_surface_factory.cc
[add] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/gl_display_initializer.h
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/gl_factory_win.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/BUILD.gn
[add] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/gl_display_initializer.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/gl_initializer_android.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/gl_implementation.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/ozone/common/gl_ozone_egl.h
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/init/gl_initializer_ozone.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/gl_display.h
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/gl/gl_display.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/chrome/browser/vr/ui_pixeltest.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/ozone/platform/headless/headless_surface_factory.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/ozone/common/gl_ozone_egl.cc
[modify] https://crrev.com/9620c12777040b697cd8d3c5927c1e40edf1094b/ui/ozone/public/gl_ozone.h


### gi...@appspot.gserviceaccount.com (2022-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3

commit c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3
Author: Peter Williamson <petewil@chromium.org>
Date: Wed Dec 21 22:57:15 2022

Revert "Reland: "Fix bugs in ANGLE backend selection""

This reverts commit 9620c12777040b697cd8d3c5927c1e40edf1094b.

Reason for revert: Lots and lots of image diff tests are failing on lots of builders.  Here is one example.  https://ci.chromium.org/ui/p/chromium/builders/ci/mac11-arm64-rel-tests/11718/test-results?sortby=&groupby=

According to dbaron, this change in its original form caused something similar, so reverting this change on suspicion of causing it again.

Original change's description:
> Reland: "Fix bugs in ANGLE backend selection"
>
> This is a reland of 25a6dc248bc0f4bc91adb4a313bba2988437cf13
>
> The failure was related to enabling ANGLE on Lacros. I've split this
> up into a separate change now.
>
> Original change's description:
> > This CL does the following:
> > 1. Fixes the unexpected behavior where in order to omit the --use-angle
> > flag, it's necessary to have ANGLEImplementation::kDefault explicitly
> > added to the allowed_impls list.
> > 2. Fixes the case where ANGLE is allowed to select an explicitly
> > prohibited backend via omitting the --use-angle flag and choosing
> > its default backend.
> > 3. Removes kDefault as an option from lists of allowed_impls that are
> > expected to explicitly prohibit certain ANGLE backends.
> > 4. Cleans up allowed_impls lists that add kDefault explicitly or
> > implicitly via GLImplementationEGLANGLE, and also add unnecessary
> > redundant explicit ANGLE backend implementations to the same list.
> > 5. In cases where the GLImplementation was set programmatically on
> > init (mostly tests) and it's not specified in the command-line, use
> > whichever ANGLE implementation was already set.
> > 6. Fix a missing case where OpenGL-EGL and OpenGLES-EGL backends
> > were not setting the correct GLImplementation.
> >
> > The effects should make ANGLE backend selection work as follows:
> > - If no ANGLE backend is chosen via explicit request (ie --use-angle),
> > then the allowed default backend will be chosen.
> > - If an invalid ANGLE backend is chosen via explicit request, then
> > we will fall back to either the default backend, or swiftshader,
> > depending on the failure mechanism.
> > - If a valid ANGLE backend is chosen, it will be used.
> > - If either of the two following options are added to the
> > allowed_impls list, then all ANGLE backends are considered valid:
> >   - gl::kGLImplementationEGLANGLE
> >   - gl::ANGLEImplementation::kDefault
> >
> > One noted edge case I found was the case where both ANGLE's internal
> > default backend was explicitly disallowed, and the swiftshader
> > backend was explicitly disallowed, then by specifying an invalid
> > backend, ANGLE would fallback to initializing with the ANGLE display
> > type DEFAULT, which would initialize the default backend that was
> > supposed to be explicitly disallowed. Currently there aren't any
> > platforms that use this setup, so this isn't an issue right now. If we
> > ever need to add a platform which can only be initialized with a
> > secondary backend (like vulkan or metal), we will need to change this
> > behavior.
> >
> > Bug: chromium:1378476
> > Bug: chromium:1231934
> > Bug: chromium:1400043
> > Change-Id: Idca3efc512494e1f7725187c58a7ea2508778df8
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4102520
> > Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
> > Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
> > Reviewed-by: ccameron chromium <ccameron@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#1085609}
>
> Bug: chromium:1378476
> Bug: chromium:1231934
> Bug: chromium:1400043
> Change-Id: I185f2819dfda19ac2779c328f39068357c6ff0aa
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4119407
> Reviewed-by: ccameron chromium <ccameron@chromium.org>
> Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
> Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1086028}

Bug: chromium:1378476
Bug: chromium:1231934
Bug: chromium:1400043
Change-Id: If2f3cc25f5ddc37613c8f42356ca6e5a358c988f
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4119374
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Peter Williamson <petewil@chromium.org>
Quick-Run: Peter Williamson <petewil@chromium.org>
Auto-Submit: Peter Williamson <petewil@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1086126}

[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/egl_api_unittest.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/init/gl_initializer_win.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/chrome/browser/vr/test/gl_test_environment_unittest.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/ozone/platform/scenic/scenic_surface_factory.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/ozone/platform/flatland/flatland_surface_factory.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/init/gl_factory_mac.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/init/gl_initializer_mac.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/init/gl_factory_android.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/test/egl_initialization_displays_unittest.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/ozone/platform/x11/x11_surface_factory.cc
[delete] https://crrev.com/5360f4589947ae5ff13a8a1360b5c3801b0cf6cb/ui/gl/init/gl_display_initializer.h
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/init/BUILD.gn
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/init/gl_factory_win.cc
[delete] https://crrev.com/5360f4589947ae5ff13a8a1360b5c3801b0cf6cb/ui/gl/init/gl_display_initializer.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/init/gl_initializer_android.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/ozone/common/gl_ozone_egl.h
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/gl_implementation.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/init/gl_initializer_ozone.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/gl_display.h
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/gl/gl_display.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/chrome/browser/vr/ui_pixeltest.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/ozone/platform/headless/headless_surface_factory.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/ozone/common/gl_ozone_egl.cc
[modify] https://crrev.com/c7575854b2e0fc7e765b330d58f7f0a0f1dbd7f3/ui/ozone/public/gl_ozone.h


### [Deleted User] (2022-12-25)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-03)

following up from off-bug conversation with geofflang@ who is working on this issue and plans on spending more time on it tomorrow; plan / hope is to land a more targeted patch than than the refactor patch in order to have a fix this week 

release team has been made aware of the status and have cut RC for M109 Stable for all Desktop platforms with the exception of Mac; Mac Desktop RC will be cut once this fix has been landed and can be backmerged 

### gi...@appspot.gserviceaccount.com (2023-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ceef12f4c335512a2599bc796574505d32215f61

commit ceef12f4c335512a2599bc796574505d32215f61
Author: Geoff Lang <geofflang@google.com>
Date: Wed Jan 04 19:32:01 2023

Disable SwiftShader for WebGL on M1 Macs.

SwiftShader's LLVM 10 doesn't fully support code generation on ARM.
Continue to support SwiftShader for rasterization which is used in
testing and explicitly requested through flags.

Bug: chromium:1378476
Change-Id: If452edabb9ca385cb40dbb33c9591814bd862396
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4133390
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1088867}

[modify] https://crrev.com/ceef12f4c335512a2599bc796574505d32215f61/ui/gl/gl_context_egl.cc


### ge...@chromium.org (2023-01-04)

I'll be owner of this for now.

### gi...@appspot.gserviceaccount.com (2023-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/51798ee1eef1f08f13705d7b06737b9e8cbeadab

commit 51798ee1eef1f08f13705d7b06737b9e8cbeadab
Author: kylechar <kylechar@chromium.org>
Date: Thu Jan 05 00:12:05 2023

Skip SwiftShader GPU tests on Mac M1

Swiftshader was disabled so skip the failing tests that try and use it
on Mac M1. These should be reenabled with SwiftShader.

Bug: 1378476
Change-Id: I1d069835d2db1099c5c994227119358f0a0e919e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4137056
Auto-Submit: Kyle Charbonneau <kylechar@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1089032}

[modify] https://crrev.com/51798ee1eef1f08f13705d7b06737b9e8cbeadab/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt
[modify] https://crrev.com/51798ee1eef1f08f13705d7b06737b9e8cbeadab/content/test/gpu/gpu_tests/test_expectations/gpu_process_expectations.txt


### gi...@appspot.gserviceaccount.com (2023-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7080f631d28bf4500cd8bd2e7e9012173cf72f84

commit 7080f631d28bf4500cd8bd2e7e9012173cf72f84
Author: Ioana Pandele <ioanap@chromium.org>
Date: Thu Jan 05 09:22:43 2023

Revert "Disable SwiftShader for WebGL on M1 Macs."

This reverts commit ceef12f4c335512a2599bc796574505d32215f61.

Reason for revert: Speculative revert for blink_web_tests failures on https://ci.chromium.org/ui/p/chromium/builders/ci/mac12-arm64-rel-tests/4985/overview

Original change's description:
> Disable SwiftShader for WebGL on M1 Macs.
>
> SwiftShader's LLVM 10 doesn't fully support code generation on ARM.
> Continue to support SwiftShader for rasterization which is used in
> testing and explicitly requested through flags.
>
> Bug: chromium:1378476
> Change-Id: If452edabb9ca385cb40dbb33c9591814bd862396
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4133390
> Reviewed-by: Kenneth Russell <kbr@chromium.org>
> Commit-Queue: Geoff Lang <geofflang@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1088867}

Bug: chromium:1378476
Change-Id: Ia973715141f300d00508c9cdb347914b6e6d839d
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4136812
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Ioana Pandele <ioanap@chromium.org>
Owners-Override: Ioana Pandele <ioanap@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1089160}

[modify] https://crrev.com/7080f631d28bf4500cd8bd2e7e9012173cf72f84/ui/gl/gl_context_egl.cc


### kb...@chromium.org (2023-01-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2a045be858e3be8ce8fc76939e3a978f61e6b7db

commit 2a045be858e3be8ce8fc76939e3a978f61e6b7db
Author: Geoff Lang <geofflang@google.com>
Date: Thu Jan 05 22:09:29 2023

Disable SwiftShader for WebGL on M1 Macs.

SwiftShader's LLVM 10 doesn't fully support code generation on ARM.
Continue to support SwiftShader for rasterization which is used in
testing and explicitly requested through flags.

Update web_test expectations for tests that use WebGL.

Bug: chromium:1378476
Change-Id: If63e6102dd42d7211c8c8cde3954d2442fd9c95d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4138403
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1089453}

[modify] https://crrev.com/2a045be858e3be8ce8fc76939e3a978f61e6b7db/headless/test/headless_browser_browsertest.cc
[modify] https://crrev.com/2a045be858e3be8ce8fc76939e3a978f61e6b7db/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/2a045be858e3be8ce8fc76939e3a978f61e6b7db/ui/gl/gl_context_egl.cc


### gi...@appspot.gserviceaccount.com (2023-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d1be68fc205c1713ab83f796a7151cdbdcd599e0

commit d1be68fc205c1713ab83f796a7151cdbdcd599e0
Author: kylechar <kylechar@chromium.org>
Date: Fri Jan 06 16:56:45 2023

Fix mac M1 suppression

The angle-swiftshader tag is only present when Chrome is restrarted for
the failing test, not the first test in the test suite, so the test
wasn't being skipped. Remove the angle-swiftshader tag.

Bug: 1378476
Change-Id: I6e89e6fc3ee177816188f5821c8cecfc5289aa44
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4141602
Reviewed-by: Saifuddin Hitawala <hitawala@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1089757}

[modify] https://crrev.com/d1be68fc205c1713ab83f796a7151cdbdcd599e0/content/test/gpu/gpu_tests/test_expectations/gpu_process_expectations.txt


### ge...@chromium.org (2023-01-06)

Requesting merge for M109 for https://crrev.com/2a045be858e3be8ce8fc76939e3a978f61e6b7db

### pb...@google.com (2023-01-06)

Merge approved for M109 Branch:Refer to go/chrome-branches for branch info, Please goahead and get the changes cherrypick asap.

### kb...@chromium.org (2023-01-06)

[Empty comment from Monorail migration]

### pb...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### pb...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1f3a37c9050965fb958d3602b6602c89f5e4ccb3

commit 1f3a37c9050965fb958d3602b6602c89f5e4ccb3
Author: Geoff Lang <geofflang@google.com>
Date: Fri Jan 06 21:02:26 2023

Duplicate Mac12 M1 SwiftShader WebGL suppressions to Mac11.

Bug: chromium:1378476
Change-Id: I9562d40f333d544674af64f609a4fe1d2d0ce4dd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4143498
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1089884}

[modify] https://crrev.com/1f3a37c9050965fb958d3602b6602c89f5e4ccb3/third_party/blink/web_tests/TestExpectations


### pb...@google.com (2023-01-06)

Merge approved for M110 Branch:Refer to go/chrome-branches for branch info, Please goahead and get the changes cherrypick asap.

### gi...@appspot.gserviceaccount.com (2023-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d799555f367dcc09c0fa050c0a635bc54c07ce5c

commit d799555f367dcc09c0fa050c0a635bc54c07ce5c
Author: Geoff Lang <geofflang@google.com>
Date: Fri Jan 06 21:31:29 2023

[109] Disable SwiftShader for WebGL on M1 Macs.

SwiftShader's LLVM 10 doesn't fully support code generation on ARM.
Continue to support SwiftShader for rasterization which is used in
testing and explicitly requested through flags.

(cherry picked from commit ceef12f4c335512a2599bc796574505d32215f61)

Bug: chromium:1378476
Change-Id: If452edabb9ca385cb40dbb33c9591814bd862396
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4133390
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1088867}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4142361
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5414@{#1240}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/d799555f367dcc09c0fa050c0a635bc54c07ce5c/ui/gl/gl_context_egl.cc


### vi...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### pb...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2a352cd43d3ee8db4543ff76093774874a14d6f9

commit 2a352cd43d3ee8db4543ff76093774874a14d6f9
Author: Geoff Lang <geofflang@google.com>
Date: Fri Jan 06 23:42:12 2023

[110] Disable SwiftShader for WebGL on M1 Macs.

SwiftShader's LLVM 10 doesn't fully support code generation on ARM.
Continue to support SwiftShader for rasterization which is used in
testing and explicitly requested through flags.

(cherry picked from commit ceef12f4c335512a2599bc796574505d32215f61)

Bug: chromium:1378476
Change-Id: If452edabb9ca385cb40dbb33c9591814bd862396
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4133390
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1088867}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4143761
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5481@{#159}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/2a352cd43d3ee8db4543ff76093774874a14d6f9/ui/gl/gl_context_egl.cc


### gi...@appspot.gserviceaccount.com (2023-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1e3d1c6fd5b876f8b5bbf6a813e75ecf541bd16e

commit 1e3d1c6fd5b876f8b5bbf6a813e75ecf541bd16e
Author: Jeevan Shikaram <jshikaram@chromium.org>
Date: Mon Jan 09 02:55:58 2023

[Sheriff] Disable Mac11/12 tests due to feature not being available.

Bug: 1378476
Change-Id: I7f1e378499915542a111f96fb2baa847ab0cb7fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4145220
Auto-Submit: Jeevan Shikaram <jshikaram@chromium.org>
Reviewed-by: Tim Sergeant <tsergeant@chromium.org>
Commit-Queue: Tim Sergeant <tsergeant@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1090190}

[modify] https://crrev.com/1e3d1c6fd5b876f8b5bbf6a813e75ecf541bd16e/third_party/blink/web_tests/TestExpectations


### gi...@appspot.gserviceaccount.com (2023-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b6290f3e1b717e62dff4e954b78217caa0eb5016

commit b6290f3e1b717e62dff4e954b78217caa0eb5016
Author: Geoff Lang <geofflang@google.com>
Date: Mon Jan 09 17:52:59 2023

Skip WebGL web_tests tests on M1 Macs.

Marking these tests as crashing was not enough to suppress the tests
in all cases.

Bug: chromium:1405468, chromium:1378476
Change-Id: Ibb07d4dd5591ae608e6522423183d6e0f053424b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4145926
Auto-Submit: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1090395}

[modify] https://crrev.com/b6290f3e1b717e62dff4e954b78217caa0eb5016/third_party/blink/web_tests/TestExpectations


### kb...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a8009d7dc5dab141f80d38b162225528acaeb887

commit a8009d7dc5dab141f80d38b162225528acaeb887
Author: Dominic Battre <battre@chromium.org>
Date: Tue Jan 10 15:34:29 2023

Skip tests that are suspected to be failing due to SwiftShader

This CL skips a couple of tests that are suspected to be failing
due to SwiftShader for WebGL not being available for ARM Macs.
These tests were re-enabled in
https://chromium-review.googlesource.com/c/chromium/src/+/4143837.
The tests are timing out consistently.

Bug: 1378476
Change-Id: I393633ac1f3f79f6ded72f7aaca7ad46a45ac4a9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4151713
Auto-Submit: Dominic Battré <battre@chromium.org>
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1090836}

[modify] https://crrev.com/a8009d7dc5dab141f80d38b162225528acaeb887/third_party/blink/web_tests/TestExpectations


### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### ge...@chromium.org (2023-01-10)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-01-10)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-01-11)

Thank you for the fix. I could verify that those patches indeed fix this issue.

### gi...@appspot.gserviceaccount.com (2023-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b8bc8ef25ac2fdaa3b40bce9767db6e8631fce6e

commit b8bc8ef25ac2fdaa3b40bce9767db6e8631fce6e
Author: Kenneth Russell <kbr@chromium.org>
Date: Wed Jan 11 09:06:24 2023

Skip virtual webgl-oversized-printing test on two configurations.

1) SwiftShader is not currently supported on ARM Macs, so skip this
test there.

2) The test causes a 1 GB allocation in the GPU process on Windows
which often fails. Skip the test there.

Bug: 1378476
Bug: 1393294
Change-Id: Ie220850053a125cbed0373f5c42714d939d39c88
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4149722
Auto-Submit: Kenneth Russell <kbr@chromium.org>
Reviewed-by: Roman Sorokin <rsorokin@google.com>
Commit-Queue: Roman Sorokin <rsorokin@google.com>
Cr-Commit-Position: refs/heads/main@{#1091226}

[modify] https://crrev.com/b8bc8ef25ac2fdaa3b40bce9767db6e8631fce6e/third_party/blink/web_tests/NeverFixTests


### jo...@google.com (2023-01-11)

Filed https://buganizer.corp.google.com/issues/265194429 to track ARM support longterm

### ka...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### ka...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### ka...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/494cf94306dba49b6cb379e15d2f810a5b7abd40

commit 494cf94306dba49b6cb379e15d2f810a5b7abd40
Author: Expectation File Editor <chromium-automated-expectation@chops-service-accounts.iam.gserviceaccount.com>
Date: Sat Jan 14 11:59:24 2023

Remove stale Blink expectations

Autogenerated CL from running:

//third_party/blink/tools/remove_stale_expectations.py --project chrome-unexpected-pass-data --no-include-internal-builders --remove-stale-expectations --narrow-semi-stale-expectation-scope --large-query-mode --num-samples 200 --jobs 2

Affected bugs for CL description:

R=rubber-stamper@appspot.gserviceaccount.com

Bug: 1046784, 1299948, 1311128, 1378476, 626703
Bug: 874695
Change-Id: I8f149c86054f359bd3ce13b2a3578da1beb1df3e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4166199
Auto-Submit: chromium-automated-expectation@chops-service-accounts.iam.gserviceaccount.com <chromium-automated-expectation@chops-service-accounts.iam.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1092768}

[modify] https://crrev.com/494cf94306dba49b6cb379e15d2f810a5b7abd40/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/494cf94306dba49b6cb379e15d2f810a5b7abd40/third_party/blink/web_tests/SlowTests


### jo...@google.com (2023-01-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5f6721beecd15354c7245ac38d44e808f272e67c

commit 5f6721beecd15354c7245ac38d44e808f272e67c
Author: Jonah Ryan-Davis <jonahr@google.com>
Date: Tue Jan 17 23:13:46 2023

Reland: "Fix bugs in ANGLE backend selection"

This is a reland of 25a6dc248bc0f4bc91adb4a313bba2988437cf13

The failures were related to enabling ANGLE on Lacros, and disabling
SwANGLE on ARM Mac.
These changes can be done in a follow-up CL. This CL should be a no-op
besides the behavioural changes documented below.

Original change's description:
> This CL does the following:
> 1. Fixes the unexpected behavior where in order to omit the --use-angle
> flag, it's necessary to have ANGLEImplementation::kDefault explicitly
> added to the allowed_impls list.
> 2. Fixes the case where ANGLE is allowed to select an explicitly
> prohibited backend via omitting the --use-angle flag and choosing
> its default backend.
> 3. Removes kDefault as an option from lists of allowed_impls that are
> expected to explicitly prohibit certain ANGLE backends.
> 4. Cleans up allowed_impls lists that add kDefault explicitly or
> implicitly via GLImplementationEGLANGLE, and also add unnecessary
> redundant explicit ANGLE backend implementations to the same list.
> 5. In cases where the GLImplementation was set programmatically on
> init (mostly tests) and it's not specified in the command-line, use
> whichever ANGLE implementation was already set.
> 6. Fix a missing case where OpenGL-EGL and OpenGLES-EGL backends
> were not setting the correct GLImplementation.
>
> The effects should make ANGLE backend selection work as follows:
> - If no ANGLE backend is chosen via explicit request (ie --use-angle),
> then the allowed default backend will be chosen.
> - If an invalid ANGLE backend is chosen via explicit request, then
> we will fall back to either the default backend, or swiftshader,
> depending on the failure mechanism.
> - If a valid ANGLE backend is chosen, it will be used.
> - If either of the two following options are added to the
> allowed_impls list, then all ANGLE backends are considered valid:
>   - gl::kGLImplementationEGLANGLE
>   - gl::ANGLEImplementation::kDefault
>
> One noted edge case I found was the case where both ANGLE's internal
> default backend was explicitly disallowed, and the swiftshader
> backend was explicitly disallowed, then by specifying an invalid
> backend, ANGLE would fallback to initializing with the ANGLE display
> type DEFAULT, which would initialize the default backend that was
> supposed to be explicitly disallowed. Currently there aren't any
> platforms that use this setup, so this isn't an issue right now. If we
> ever need to add a platform which can only be initialized with a
> secondary backend (like vulkan or metal), we will need to change this
> behavior.
>
> Bug: chromium:1378476
> Bug: chromium:1231934
> Bug: chromium:1400043
> Change-Id: Idca3efc512494e1f7725187c58a7ea2508778df8
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4102520
> Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
> Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
> Reviewed-by: ccameron chromium <ccameron@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1085609}

Bug: chromium:1378476
Bug: chromium:1231934
Bug: chromium:1400043
Change-Id: I9cb57ed4850e9ee783fe28b9567932d0dd1c4a51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4117698
Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
Reviewed-by: ccameron chromium <ccameron@chromium.org>
Commit-Queue: Jonah Ryan-Davis <jonahr@google.com>
Cr-Commit-Position: refs/heads/main@{#1093580}

[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/gl_initializer_win.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/egl_api_unittest.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/chrome/browser/vr/test/gl_test_environment_unittest.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/ozone/platform/scenic/scenic_surface_factory.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/ozone/platform/flatland/flatland_surface_factory.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/gl_factory_mac.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/gl_factory_android.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/gl_initializer_mac.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/ozone/platform/x11/x11_surface_factory.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/test/egl_initialization_displays_unittest.cc
[add] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/gl_display_initializer.h
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/gl_factory_win.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/BUILD.gn
[add] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/gl_display_initializer.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/gl_initializer_android.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/ozone/common/gl_ozone_egl.h
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/gl_implementation.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/init/gl_initializer_ozone.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/gl_display.h
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/gl/gl_display.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/chrome/browser/vr/ui_pixeltest.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/ozone/platform/headless/headless_surface_factory.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/ozone/common/gl_ozone_egl.cc
[modify] https://crrev.com/5f6721beecd15354c7245ac38d44e808f272e67c/ui/ozone/public/gl_ozone.h


### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-18)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-01-31)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-02-22)

Looks like this issue is still happening on M110 - we probably need another merge?
This bot has a whole host of issues, and so does the Mac12 bot. https://ci.chromium.org/p/chromium-m110/builders/ci/mac11-arm64-rel-tests

geofflang@chromium.org can you advise on how to address some of these failures?


- Branch sheriff

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### jo...@google.com (2023-02-22)

donnd, can you explain where this issue is happening on M110? Are you able to reproduce the issue in the OP?

I think it should be expected that WebGL is broken on the ARM Mac blink web tests, as swiftshader is disabled. We should skip all tests that use a WebGL context on those bots. (Or is it possible to run the web tests on the GPU?)

### ge...@chromium.org (2023-02-22)

We didn't merge the test expectations updates to the M110 branch because at the time there was no branch tester AFAIK and we wanted to keep the merge small.

We can merge the test changes too if needed.

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### ge...@chromium.org (2023-02-27)

Re-marking this as fixed.

### gi...@appspot.gserviceaccount.com (2023-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ebb9afb51c828c4a5ff55e43125a58b6d841e31c

commit ebb9afb51c828c4a5ff55e43125a58b6d841e31c
Author: Geoff Lang <geofflang@google.com>
Date: Thu Mar 02 00:13:38 2023

Disable SwiftShader for WebGL on M1 Macs.

SwiftShader's LLVM 10 doesn't fully support code generation on ARM.
Continue to support SwiftShader for rasterization which is used in
testing and explicitly requested through flags.

Update web_test expectations for tests that use WebGL.

(cherry picked from commit 2a045be858e3be8ce8fc76939e3a978f61e6b7db)

Bug: chromium:1378476
Change-Id: If63e6102dd42d7211c8c8cde3954d2442fd9c95d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4138403
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1089453}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4273873
Commit-Queue: Tomasz Wiszkowski <ender@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Owners-Override: Tomasz Wiszkowski <ender@google.com>
Reviewed-by: Caroline Rising <corising@chromium.org>
Reviewed-by: Tomasz Wiszkowski <ender@google.com>
Cr-Commit-Position: refs/branch-heads/5481@{#1308}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/ebb9afb51c828c4a5ff55e43125a58b6d841e31c/headless/test/headless_browser_browsertest.cc
[modify] https://crrev.com/ebb9afb51c828c4a5ff55e43125a58b6d841e31c/third_party/blink/web_tests/TestExpectations


### la...@chromium.org (2023-03-04)

Branch sheriff note:
I see lots of failures on these Mac arm64 branch builders:
https://ci.chromium.org/p/chromium-m110/builders/ci/mac11-arm64-rel-tests
https://ci.chromium.org/p/chromium-m110/builders/ci/mac12-arm64-rel-tests

Examples:
https://ci.chromium.org/ui/p/chromium-m110/builders/ci/mac11-arm64-rel-tests/996/overview
https://ci.chromium.org/ui/p/chromium-m110/builders/ci/mac12-arm64-rel-tests/851/overview

A common error message is something like:
ERROR:gles2_command_buffer_stub.cc(352)] ContextResult::kFatalFailure: Failed to create context.
CONSOLE ERROR: Uncaught Unable to fetch WebGL rendering context for Canvas


### gi...@appspot.gserviceaccount.com (2023-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f98313ae8c45ba23fa4bfe150aba737dbd1806f7

commit f98313ae8c45ba23fa4bfe150aba737dbd1806f7
Author: Justin Novosad <junov@chromium.org>
Date: Mon Mar 20 17:17:03 2023

Cleanup TestExpectations related to SwiftShader on arm64 MacOS

Moving expectations to NeverFixTests and setting all expectations to
"Skip" since we have no plans to resolve this. Bug associated with
the failures was closed.

Bug: 1378476
Change-Id: Idbdcdd8f6ce02720dc3012e27cd8f76778a89d19
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4351285
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Auto-Submit: Justin Novosad <junov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1119419}

[modify] https://crrev.com/f98313ae8c45ba23fa4bfe150aba737dbd1806f7/third_party/blink/web_tests/NeverFixTests
[modify] https://crrev.com/f98313ae8c45ba23fa4bfe150aba737dbd1806f7/third_party/blink/web_tests/TestExpectations


### kb...@chromium.org (2023-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2023-06-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e2241b497985cce79f0a064f9daebf77cebb05da

commit e2241b497985cce79f0a064f9daebf77cebb05da
Author: Justin Novosad <junov@chromium.org>
Date: Tue Jun 20 20:04:16 2023

Skip web test using WebGL on arm64 Mac

Affected test:
fast/canvas-api/offscreencanvas.transferrable-webgl-exception.html

Bug: 1378476, 1422685
Change-Id: I6fb2e003a6626901442b1b691f8c476614410efd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4630048
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Commit-Queue: Justin Novosad <junov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1160222}

[modify] https://crrev.com/e2241b497985cce79f0a064f9daebf77cebb05da/third_party/blink/web_tests/NeverFixTests
[modify] https://crrev.com/e2241b497985cce79f0a064f9daebf77cebb05da/third_party/blink/web_tests/TestExpectations


### da...@chromium.org (2023-07-13)

WinARM is being brought up now, and this key part of our graphics stack is broken on ARM. (Linux ARM is a thing too but maybe not for Chrome yet.)

The disable in the CL here is behind IS_APPLE so this exploit is currently open and available on WinARM.



### br...@chromium.org (2023-07-13)

It looks like we need these three CLs updated to reference Windows ARM:

crrev.com/c/4138403 - Disable SwiftShader for WebGL on M1 Macs.
crrev.com/c/4351285 - Cleanup TestExpectations related to SwiftShader on arm64 MacOS
crrev.com/c/4630048 - Skip web test using WebGL on arm64 Mac

The first one is the most important. The other two just deal with test failures. Does this look right?

Reopening and tagging with Windows


### [Deleted User] (2023-07-14)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 136 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2023-07-20)

hi geofflang@ Seems it was fixed for Mac. Is this a release blocker on Windows?

### ge...@chromium.org (2023-07-20)

Yea, not a release blocker anymore.

### br...@chromium.org (2023-07-20)

geofflang@, can you clarify? "not a release blocker anymore" doesn't quite make sense because ARM64 Windows is a new (soon) platform so it is just now becoming a potential release blocker on Windows. Is there some reason to believe that it will not be a release blocker for ARM64 Windows Chrome?


### be...@google.com (2023-07-20)

Adding Hotlist-RBS-Removed for tracking purposes.

### gi...@appspot.gserviceaccount.com (2023-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c94b5aaedf4aad05b4f76c170bc7fe3a50961dfc

commit c94b5aaedf4aad05b4f76c170bc7fe3a50961dfc
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Jul 21 17:55:49 2023

Disable SwiftShader for WebGL on ARM Windows.

The same issues with ARM Macs apply to Windows. The version of LLVM
that SwiftShader uses has incomplete ARM code generation.

Bug: chromium:1378476
Change-Id: I010ee2ee8938072ba0f320e2037ae34cbc193f01
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4698353
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Peng Huang <penghuang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1173615}

[modify] https://crrev.com/c94b5aaedf4aad05b4f76c170bc7fe3a50961dfc/third_party/blink/web_tests/NeverFixTests
[modify] https://crrev.com/c94b5aaedf4aad05b4f76c170bc7fe3a50961dfc/ui/gl/gl_context_egl.cc


### ke...@chromium.org (2023-07-28)

It looks like we can mark this fixed?

### ge...@chromium.org (2023-08-14)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-09-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-24)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-10-31)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1378476?no_tracker_redirect=1

[Multiple monorail components: Internals>GPU>ANGLE, Internals>GPU>SwiftShader, Internals>GPU>Testing]
[Monorail blocked-on: b/165000222]
[Monorail blocking: crbug.com/chromium/1393294, crbug.com/chromium/1405378, crbug.com/chromium/1405470, crbug.com/chromium/1407025, crbug.com/chromium/1407288, crbug.com/chromium/1409689, crbug.com/chromium/1422685, crbug.com/chromium/1453965, crbug.com/chromium/1487585, crbug.com/chromium/1498181]
[Monorail mergedwith: crbug.com/chromium/1405128, crbug.com/chromium/1405276, crbug.com/chromium/1405375, crbug.com/chromium/1407165]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061476)*
