# Security: website is able to draw over protected UI elements (URL, padlock, tab list, titlebar) using 3D CSS transforms

| Field | Value |
|-------|-------|
| **Issue ID** | [40054357](https://issues.chromium.org/issues/40054357) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Compositing, Internals>Compositing>Animation |
| **Platforms** | Android, Linux, Windows |
| **Reporter** | rs...@gmail.com |
| **Assignee** | bs...@google.com |
| **Created** | 2021-01-04 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The UI elements outside of the content area are security-sensitive and a website being able to paint on top of them would allow critical security-sensitive information to be faked.

The attached repro case was built to demonstrate 3D CSS capabilities, but it inadvertently triggers a bug that makes this possible. The bug may be in third party drivers but Chrome still needs to mitigate it due to the consequences of a successful exploit.

The repro case is not a complete attack, nor a proof of concept. It merely demonstrates that *some* painting is possible, and it is clear that some of that painting is using website-supplied textures.

It is unclear whether it's possible to trigger the overpaint consistently enough to construct a viable attack.

**VERSION**  

Version 87.0.4280.88 (Official Build) (64-bit) (stable)  

Operating System: Windows 10 Pro 1909 (build 18363.1198)

**REPRODUCTION CASE**

1. Open the repro website
2. Click to capture the mouse (this appears to be a crucial requirement)
3. Press W/A/S/D and rotate the mouse until one of the CSS surfaces is clipped incorrectly (it becomes see through or overlaid on top of another surface)
4. At this point the UI may already have been painted over, but un-capturing the mouse with Esc often triggers extra overpainting.

See screenshot.png.

**CREDIT INFORMATION**  

3D CSS credit: Keith Clark <https://keithclark.co.uk/labs/css-fps/desktop/>  

Reporter credit: Roman Starkov

## Attachments

- [repro.html](attachments/repro.html) (text/plain, 55.7 KB)
- [ceil.jpg](attachments/ceil.jpg) (image/jpeg, 60.5 KB)
- [crate.jpg](attachments/crate.jpg) (image/jpeg, 3.3 KB)
- [drum2.png](attachments/drum2.png) (image/png, 52.2 KB)
- [floor.jpg](attachments/floor.jpg) (image/jpeg, 76.5 KB)
- [map.png](attachments/map.png) (image/png, 452 B)
- [pipe2.jpg](attachments/pipe2.jpg) (image/jpeg, 7.6 KB)
- [wall.jpg](attachments/wall.jpg) (image/jpeg, 56.2 KB)
- screenshot.png (image/png, 802.0 KB)
- [Screenshot 2021-01-04 at 1.08.18 PM.png](attachments/Screenshot 2021-01-04 at 1.08.18 PM.png) (image/png, 1.1 MB)
- [about_gpu_linux.txt](attachments/about_gpu_linux.txt) (text/plain, 21.6 KB)
- [about_gpu_chromeos.txt](attachments/about_gpu_chromeos.txt) (text/plain, 64.4 KB)
- [about_gpu_windows.txt](attachments/about_gpu_windows.txt) (text/plain, 23.4 KB)
- [quad_over_ui.html](attachments/quad_over_ui.html) (text/plain, 6.7 KB)
- [quad_over_ui.png](attachments/quad_over_ui.png) (image/png, 26.9 KB)
- [white_highlight.png](attachments/white_highlight.png) (image/png, 31.3 KB)
- [crbug1162942-repro.jpg](attachments/crbug1162942-repro.jpg) (image/jpeg, 85.7 KB)

## Timeline

### [Deleted User] (2021-01-04)

[Empty comment from Monorail migration]

### rs...@gmail.com (2021-01-04)

Screenshot demonstrating the overpaint

### mp...@google.com (2021-01-04)

Thanks for the report! I was able to reproduce this on Linux (screenshot attached), but I wasn't able to reproduce this on ChromeOS. I attached my about:gpu dumps for both.

rstarkov, could you post the contents of your about:gpu page so we can investigate?

kylechar@ would you mind helping triage this?

I'm not sure how possible it is to reliably control the overpainting so for now I'm marking this as medium severity.

[Monorail components: Internals>Compositing Internals>Compositing>Animation]

### rs...@gmail.com (2021-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-04)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-05)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-05)

[Empty comment from Monorail migration]

### ky...@chromium.org (2021-01-13)

I can reproduce the quads drawing over top of UI on Linux when I'm walking around in https://keithclark.co.uk/labs/css-fps/desktop/. Loading repo.html doesn't work for me but it seems like this is dependent on what UI elements are being drawn.

Since this only reproduces on Linux and not CrOS I tested SkiaRenderer vs GLRenderer. I can't reproduce with GLRenderer so I think it's a SkiaRenderer issue. Maybe a bug in SkiaRenderer clipping for 3D CSS transforms.

I saved the DOM from when I reproduced it on Linux and removed all the planes that weren't required to reproduce the bug. I've attached an HTML and screenshot of it. In order for me to reproduce I have to maximize the Chrome window. It seems drawing the side/bottom borders breaks the repro I have. I'll do some more investigation to see if I can figure out what is going on, but I think Skia handles the 3D transforms and clipping internally so the issue will be internal to Skia.

### mi...@google.com (2021-01-13)

I noticed that the perspective matrix has a distance of 600.644 px and some of the divs have transforms of 600.64px, putting them very close to the near plane and w = 0 (in terms of perspective clipping). This, and the visual character, are enough for me to say it's blocked on https://bugs.chromium.org/p/skia/issues/detail?id=9906 being fixed in Skia (at least for rectangle drawing).

However, I would have thought that skia_renderer's scissor would have prevented the perspective issues from bleeding out to the UI elements. I wonder if it's not being enabled so there's no clipRect call to Skia? Or if there's a bug or overflow in bounds calculations within Skia that decides the scissor is a no-op and then is skipped on the GPU.  I'll try and debug into it if I'm able to reproduce, otherwise @kylechar, it'll be similar to the debugging you did for https://bugs.chromium.org/p/chromium/issues/detail?id=1128636

### ky...@chromium.org (2021-01-14)

I tried the quad_over_ui.html sample on Windows. As long I'm using software rasterization and the Chrome window is maximized the quad draws over the UI on Windows too. I think the example should be portable across any Linux/Windows machine with a recent Chrome version as a result.

I looked a bit closer and there are 8 quads with 3D transforms. Drawing any of those quads on their own doesn't trigger the glitch, it's a combination of two or more than does it.

michaelludwidg@ is on leave I think. bsalomon@ can you triage this to someone on the Skia team who might be able to take a look?

### ky...@chromium.org (2021-01-14)

Oh also I tried changing kW0PlaneDistance [1] back to 0.05 to clip things that are closer again but it had no impact.

[1] https://source.chromium.org/chromium/chromium/src/+/master:third_party/skia/src/core/SkPathPriv.h;l=28;drc=71f12666647b40c6d0a95ab75a5c77095a171e54

### bs...@google.com (2021-01-14)

I can investigate this. I have a repro on linux using quad_over_ui.html. So far I've figured out that we bail on clipping the draw here:
https://source.chromium.org/chromium/chromium/src/+/master:third_party/skia/src/gpu/GrClipStack.cpp;l=1310;drc=7ccffaf0933ccc647c744bf66971bcf5f33a676a

If I skip that return and make the code starting here:
https://source.chromium.org/chromium/chromium/src/+/master:third_party/skia/src/gpu/GrClipStack.cpp;l=1439;drc=7ccffaf0933ccc647c744bf66971bcf5f33a676a;bpv=1;bpt=1

always apply a scissor then we no longer draw over the UI

### mi...@google.com (2021-01-15)

I did a little more digging and dropping the scissor and the code in GrClipStack is sort of a red herring. The bounds that are being calculated are correct, I believe, and it's properly detecting that the scissor isn't needed.

However, later on, when we calculate the inset and outset for the anti-aliased "picture frame", the interior vertices get messed up. At least when I've reproduced the issue of over-draw, one of the inset vertices Y coordinate flips sign and becomes a coordinate that is no longer within the original bounds of the quadrilateral.  The w values are actually not very close to 0, but appears to project to an exceptional thin quadrilateral.  This is likely causing some of the math to become numerically unstable and it's just a matter of tracking it down.

[1] Inset calculations begin: https://source.chromium.org/chromium/chromium/src/+/master:third_party/skia/src/gpu/ops/GrQuadPerEdgeAA.cpp;drc=f124108e23259cd309dcafea1efbd22460b4ee84;l=361
[2] Perspective insets are always done here: https://source.chromium.org/chromium/chromium/src/+/master:third_party/skia/src/gpu/geometry/GrQuadUtils.cpp;drc=290d6df49be966a9947eca757693ed03147aece8;l=934
[3] This is a semi-hack that scales by -1 when w flips behind w = 0, but I'm not sure that's applicable here, but should be ruled out: https://source.chromium.org/chromium/chromium/src/+/master:third_party/skia/src/gpu/geometry/GrQuadUtils.cpp;drc=290d6df49be966a9947eca757693ed03147aece8;l=1010



### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-19)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/7656c4b7e89b4ff00480a6d7a8a19e3fd0e5c86e

commit 7656c4b7e89b4ff00480a6d7a8a19e3fd0e5c86e
Author: Brian Salomon <bsalomon@google.com>
Date: Tue Jan 19 17:33:45 2021

Fix DrawEdgeAAQuad degenerate issue where 3D points don't correctly project to 2D points.


Bug: chromium:1162942

Change-Id: Idc1dcb725ff9eae651b84de2fe792b188dcd1c1b
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/354671
Commit-Queue: Brian Salomon <bsalomon@google.com>
Reviewed-by: Michael Ludwig <michaelludwig@google.com>

[modify] https://crrev.com/7656c4b7e89b4ff00480a6d7a8a19e3fd0e5c86e/gn/gm.gni
[modify] https://crrev.com/7656c4b7e89b4ff00480a6d7a8a19e3fd0e5c86e/src/gpu/geometry/GrQuadUtils.h
[modify] https://crrev.com/7656c4b7e89b4ff00480a6d7a8a19e3fd0e5c86e/src/gpu/geometry/GrQuadUtils.cpp
[add] https://crrev.com/7656c4b7e89b4ff00480a6d7a8a19e3fd0e5c86e/gm/crbug_1162942.cpp


### ky...@chromium.org (2021-01-19)

Add Peng/Peter for https://crbug.com/1167277 since this is marked as a security bug.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/825955c808f5bd2125a6b83bfb5fdf12bc1b9b56

commit 825955c808f5bd2125a6b83bfb5fdf12bc1b9b56
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jan 19 22:31:16 2021

Roll Skia from f8dfc3b51883 to f3087d8297fe (5 revisions)

https://skia.googlesource.com/skia.git/+log/f8dfc3b51883..f3087d8297fe

2021-01-19 mtklein@google.com allow a fourth Val/Reg arg per op
2021-01-19 fmalita@chromium.org [svg] Cleanup: use FP alpha for opacity
2021-01-19 mtklein@google.com remove reg/imm unions
2021-01-19 scroggo@google.com Fix decoding gifs with too-big-bounds
2021-01-19 bsalomon@google.com Fix DrawEdgeAAQuad degenerate issue where 3D points don't correctly project to 2D points.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC scroggo@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Cq-Do-Not-Cancel-Tryjobs: true
Bug: chromium:1162942
Tbr: scroggo@google.com
Change-Id: I7ed0b74cc37c0b75d0305d3f0cbcce5d2a66013f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2638354
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#844934}

[modify] https://crrev.com/825955c808f5bd2125a6b83bfb5fdf12bc1b9b56/DEPS


### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### bs...@google.com (2021-01-21)

Fix on ToT. I assume we'll want this cherry-picked back to 88 once it bakes a bit on canary?

### ky...@chromium.org (2021-01-21)

Yes I think so.

### [Deleted User] (2021-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-21)

Requesting merge to beta M88 because latest trunk commit (844934) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-21)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bs...@google.com (2021-01-25)

1) yes
2) https://skia-review.googlesource.com/c/skia/+/354671
3) yes
4) yes, M89
5) P1 Security bug
6) No
7) N/A

### ad...@google.com (2021-01-26)

Landed after M89 branch point. Adding merge request which was omitted due to Sheriffbot bug (https://crbug.com/chromium/991615)

### [Deleted User] (2021-01-26)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bs...@google.com (2021-01-26)

1) yes
2) https://skia-review.googlesource.com/c/skia/+/354671
3) yes
4) yes, M88 (according to Target label)
5) P1 Security bug
6) No
7) N/A

### ad...@google.com (2021-01-27)

Approving merge to M89, branch 4389. M88 merge approvals will likely happen on Thursday after a bit more bake time.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-27)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/b0d3d3e85fa6b9eba987796d410ea3ea5cbeb18f

commit b0d3d3e85fa6b9eba987796d410ea3ea5cbeb18f
Author: Brian Salomon <bsalomon@google.com>
Date: Wed Jan 27 15:20:59 2021

Fix DrawEdgeAAQuad degenerate issue where 3D points don't correctly project to 2D points.


Bug: chromium:1162942

Change-Id: Idc1dcb725ff9eae651b84de2fe792b188dcd1c1b
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/354671
Commit-Queue: Brian Salomon <bsalomon@google.com>
Reviewed-by: Michael Ludwig <michaelludwig@google.com>
(cherry picked from commit 7656c4b7e89b4ff00480a6d7a8a19e3fd0e5c86e)
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/360376
Reviewed-by: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/b0d3d3e85fa6b9eba987796d410ea3ea5cbeb18f/gn/gm.gni
[modify] https://crrev.com/b0d3d3e85fa6b9eba987796d410ea3ea5cbeb18f/src/gpu/geometry/GrQuadUtils.h
[modify] https://crrev.com/b0d3d3e85fa6b9eba987796d410ea3ea5cbeb18f/src/gpu/geometry/GrQuadUtils.cpp
[add] https://crrev.com/b0d3d3e85fa6b9eba987796d410ea3ea5cbeb18f/gm/crbug_1162942.cpp


### ad...@google.com (2021-01-27)

Approving merge to M88, branch 4324, assuming no problems have shown up on Canary or elsewhere.

### am...@google.com (2021-01-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-28)

Congratulations rstarkov@! The VRP Panel has decided to award you $5000 for this report. A member of our finance team will be in touch shortly to arrange payment. In the interim, please let me know the name and/or handle by which you would like to be credited in release notes. Thank you and nice work! 

### go...@google.com (2021-01-28)

Already merged to M89 at #30.

Please merge to M88 ASAP so it can be included in next week M88 Stable respin. We're cutting RC tomorrow, Friday morning. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-28)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/433b2a55a5fbc9e3f5a6b457526ad99d73ba6117

commit 433b2a55a5fbc9e3f5a6b457526ad99d73ba6117
Author: Brian Salomon <bsalomon@google.com>
Date: Thu Jan 28 19:38:29 2021

Fix DrawEdgeAAQuad degenerate issue where 3D points don't correctly project to 2D points.

Bug: chromium:1162942

Change-Id: Idc1dcb725ff9eae651b84de2fe792b188dcd1c1b
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/354671
Commit-Queue: Brian Salomon <bsalomon@google.com>
Reviewed-by: Michael Ludwig <michaelludwig@google.com>
(cherry picked from commit 7656c4b7e89b4ff00480a6d7a8a19e3fd0e5c86e)
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/361518
Reviewed-by: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/433b2a55a5fbc9e3f5a6b457526ad99d73ba6117/gn/gm.gni
[modify] https://crrev.com/433b2a55a5fbc9e3f5a6b457526ad99d73ba6117/src/gpu/geometry/GrQuadUtils.h
[modify] https://crrev.com/433b2a55a5fbc9e3f5a6b457526ad99d73ba6117/src/gpu/geometry/GrQuadUtils.cpp
[add] https://crrev.com/433b2a55a5fbc9e3f5a6b457526ad99d73ba6117/gm/crbug_1162942.cpp


### am...@google.com (2021-01-28)

[Empty comment from Monorail migration]

### sr...@google.com (2021-01-29)

removing approved label per https://crbug.com/chromium/1162942#c35

### ad...@google.com (2021-01-29)

[Empty comment from Monorail migration]

### rs...@gmail.com (2021-01-31)

Thank you all for fixing this so quickly. You can use my full name (Roman Starkov) in the release notes.

### am...@google.com (2021-01-31)

Thanks, Roman! Release notes will be posted later this week. 

### am...@google.com (2021-01-31)

[Empty comment from Monorail migration]

### as...@google.com (2021-02-02)

Adding LTS labels and marking as NotApplicable as per https://crbug.com/chromium/1162942#c3.

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2021-04-29)

I'm still able to partially repro on 90.0.4430.93 Stable but doesn't seem to repro on 91.0.4467.0 or later on local+Beta+Canary builds.
Were there any additional fixes other than these commits?

My repro most of the time is a flickering area, but if two flickering areas overlap, it results in a solid area (similar to original reporter's screenshots). I'm trying to take good photos with my phone, since taking screenshots clears the effect.

https://chromiumdash.appspot.com/commit/825955c808f5bd2125a6b83bfb5fdf12bc1b9b56 shows fix landed on 90.0.4430.72 Stable so unsure why I'm able to partially repro on .93

### bs...@google.com (2021-04-29)

There was another related bug, https://crbug.com/chromium/1177833. It wasn't fixed in until this change:

https://chromiumdash.appspot.com/commits?commit=6b432e8e5f37052d00cd57831cb95febc2a1eee0&platform=Windows

which first made it into M91. I'm guessing this page is triggering it too and that is the source of the partial repro.

### al...@alesandroortiz.com (2021-04-29)

Got it, thanks. FWIW, I'm not able to repro https://crbug.com/chromium/1177833 on the same Stable version, but maybe I'm not trying enough or wrong environment. Since neither repros on Beta or Canary, I'll assume that this bug will stop reproducing on 91 Stable onwards.

For this bug, I was able to get a better repro on Stable after a few more tries (with artifacts similar to reporter's screenshots). Highly-cropped dusty photo attached.

### bs...@google.com (2021-04-29)

I could be mixing up the various issues now but I'm pretty sure when I reproduced 1177033 I had to modify the molecule page to spin much more slowly and then wait a bit to spot the glitch, which was pretty subtle.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1162942?no_tracker_redirect=1

[Multiple monorail components: Internals>Compositing, Internals>Compositing>Animation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054357)*
