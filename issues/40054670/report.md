# CSS 3D transform intersection glitch in Chrome / Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40054670](https://issues.chromium.org/issues/40054670) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Compositing |
| **Platforms** | Linux, Windows |
| **Reporter** | ja...@gmail.com |
| **Assignee** | bs...@google.com |
| **Created** | 2021-02-03 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 88.0.4324.104 (Official Build) (64-bit) (cohort: Stable)  

**URLs (if applicable) :** <https://codepen.io/japongnet/pen/YzpyxJQ>  

**Other browsers tested:**  

Add OK or FAIL, along with the version, after other browsers where you  

**have tested this issue:**  

Safari: OK (14.0.2)  

Firefox: OK (85.0)  

Edge: FAIL (Version 88.0.705.56 (Official build) (64-bit)

**What steps will reproduce the problem?**  

**(1)** Create 3D transforms that cause HTML elements to intersect each other while animated: <https://codepen.io/japongnet/pen/YzpyxJQ> (view in Chrome on Windows / Linux)

**(2)**  

**(3)**

**What is the expected result?**  

These elements should intersect each other with no graphical anomalies.

**What happens instead?**  

These elements instead cause graphical artifacts and glitches that can paint over the UI of the browser, obscuring browser tabs and menus.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

Stack overflow topic here: <https://stackoverflow.com/questions/66033729/css-3d-transform-intersection-glitch-in-chrome-windows>  

Codepen example here: <https://codepen.io/japongnet/pen/YzpyxJQ>

## Attachments

- [Screenshot 2021-02-03 132258.png](attachments/Screenshot 2021-02-03 132258.png) (image/png, 88.2 KB)

## Timeline

### dt...@chromium.org (2021-02-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>Paint]

### pd...@chromium.org (2021-02-03)

Wow that is a wild screenshot! I can't reproduce on 88.0.4324.96/MacOS but this is likely to be related to the specific hardware. Test team, can you reproduce?

This seems similar to crbug.com/1174187.

[Monorail components: -Blink>Paint Internals>Compositing]

### pd...@chromium.org (2021-02-03)

[Empty comment from Monorail migration]

### jh...@chromium.org (2021-02-04)

[Empty comment from Monorail migration]

### pe...@chromium.org (2021-02-04)

[Empty comment from Monorail migration]

### br...@gmail.com (2021-02-04)

This happened to me too on Windows.

### jh...@chromium.org (2021-02-04)

Able to reproduce the issue on reported chrome version #88.0.4324.96 using windows 10, Linux 16.04 as per https://crbug.com/chromium/1174186#c0.
Note: Not reproducible on mac 10.15.7.

Reproducible:
---------------------
Stable : 88.0.4324.146.
Beta: 89.0.4389.40
Dev: 90.0.4400.10
Canary: 90.0.4398.0

Bisect information
--------------------------
Good Build: 87.0.4251.0.
Bad Build: 87.0.4252.0.

The script might not always return single CL as suspect as some perf builds might get missing due to failure.
  https://chromium.googlesource.com/chromium/src/+log/a857108e4452b0dc2254df29a87befe8af408fdf..60789cdca25a8eb8534d0c5fccfb87c04c0f66d3
Change-Id: I32c23ceb39fc63f93a0dc8fbd3a8a787bc1a45e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2368505

kylechar @Please help us in reassigning the issue if it is not related to your change.

Thanks..     

### ky...@chromium.org (2021-02-04)

It reproduces on Linux/Windows due to SkiaRenderer being enabled there by default. This looks like the same type of Skia numerical instability issue as https://crbug.com/1162942 and https://crbug.com/1167277. Unfortunate it's not fixed as this still reproduces at ToT on Linux for me.

+bsalamon/michaelludwig for triage.

### pd...@chromium.org (2021-02-04)

Can we not use Restrict-View-Google so users can track the progress?

### bs...@google.com (2021-02-05)

Here is a non-animating, more minimized repro derived from the original code pen: https://codepen.io/bsalomon/pen/NWbxONE

### ky...@chromium.org (2021-02-05)

I marked this RVG since drawing over the omnibox has potential security implications. It kinda looks like the graphics glitches are all lines that cross through renderer pixels, so you can't draw arbitrary pixels over the omnibox, but until we have a better idea what this allows it probably shouldn't be public.

pdr@ any idea if there is a more appropriate label? RV-SecurityNotify maybe?

### pd...@chromium.org (2021-02-05)

Kyle, I see you were right to use RVG. Sorry for the noise!

+cc srinivassista, this is a regression with potential security implications (probably low severity). Can you set the right labels for that?

### ch...@google.com (2021-02-05)

Marking as RBS because of the security implications.

### sr...@google.com (2021-02-05)

adetaylor@ for his inputs on this, yes marking as RBS is fine for now. 

Regarding the fix for this, we have security re-spin planned week of Feb 15 so if a fix can be ready for merge to M88 by thursday next week we can get it included in the re-spin

### bs...@google.com (2021-02-05)

Still debugging but I think that is plenty of time.

### ad...@chromium.org (2021-02-05)

I'm moving this to be type=Bug-Security and cc'ing everyone who wasn't cc'd for visibility. Hope that's OK. That way this will go through our CVE, release notes and VRP processes automatically. Our security sheriff will assess for severity.

From the security team point of view, we don't need to mark this as RBS unless this is believed to be a recent regression. It would still be great to fix it urgently of course!

### [Deleted User] (2021-02-05)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-02-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-08)

[Empty comment from Monorail migration]

### bs...@google.com (2021-02-08)

I think the general problem here is that the inset/outset code for AA will determine when the process creates degenerecies (i.e. insets erase the interior, collapse to a triangle, etc), but doesn't handle inputs well where the input quad before inset/outset is already nearly a line. I've added some detection for that locally, but it isn't robust enough as there are still occasional artifacts. Working on isolating an example of that....

### sr...@google.com (2021-02-09)

is this a recent regression ( checking if this warrants RBS)? if not please remove it and we will take it to the next release once the fix is ready. 

M88 last re-spin is next week so we need to get fix ready to merge to M88 branch before friday this week

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-10)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/ec04e062f3f5b6d79715572d9b55cd132d9f5945

commit ec04e062f3f5b6d79715572d9b55cd132d9f5945
Author: Brian Salomon <bsalomon@google.com>
Date: Wed Feb 10 02:43:35 2021

Drop AA on quads that are extremely thin before AA insetting/outsetting.

Bug: chromium:1174186
Change-Id: I91a88d2d57150dee37f08bc4270d399abfd0d60d
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/368497
Commit-Queue: Brian Salomon <bsalomon@google.com>
Reviewed-by: Michael Ludwig <michaelludwig@google.com>

[modify] https://crrev.com/ec04e062f3f5b6d79715572d9b55cd132d9f5945/gn/gm.gni
[add] https://crrev.com/ec04e062f3f5b6d79715572d9b55cd132d9f5945/gm/crbug_1174186.cpp
[modify] https://crrev.com/ec04e062f3f5b6d79715572d9b55cd132d9f5945/src/gpu/geometry/GrQuadUtils.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9a64708d9ea0c9f7922772752b3e361235b92a36

commit 9a64708d9ea0c9f7922772752b3e361235b92a36
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Feb 10 09:06:02 2021

Roll Skia from e89b50ae054c to 7f942e46fda2 (4 revisions)

https://skia.googlesource.com/skia.git/+log/e89b50ae054c..7f942e46fda2

2021-02-10 skia-autoroll@skia-public.iam.gserviceaccount.com Roll Dawn from e7e42ebbed90 to 02fd17c75403 (10 revisions)
2021-02-10 skia-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 983950b467bc to 8cbe693bd2e0 (368 revisions)
2021-02-10 skia-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 9d35d544ce96 to 9677c6d28278 (5 revisions)
2021-02-10 bsalomon@google.com Drop AA on quads that are extremely thin before AA insetting/outsetting.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC borenet@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Cq-Do-Not-Cancel-Tryjobs: true
Bug: chromium:1174186
Tbr: borenet@google.com
Change-Id: I8ef34fb27ef9ecc173c22e79fabad9885d5975e7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2686736
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#852555}

[modify] https://crrev.com/9a64708d9ea0c9f7922772752b3e361235b92a36/DEPS


### bs...@google.com (2021-02-10)

It's not a recent regression. Removing RBS. Fix is very simple and safe.

### bs...@google.com (2021-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-11)

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

### bs...@google.com (2021-02-12)

1) yes
2) https://skia.googlesource.com/skia/+/ec04e062f3f5b6d79715572d9b55cd132d9f5945
3) yes
4) Probably too late for earlier branches
5) Fixes bad rendering glitch, possible security issue
6) No
7) N/A

### bs...@google.com (2021-02-12)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-12)

Approving merge to M89, branch 4389, assuming no problems have shown up in Canary.

### [Deleted User] (2021-02-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-14)

[Empty comment from Monorail migration]

### sc...@chromium.org (2021-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-16)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/25f6bc42d7d6a25d0701f7c7ce479d8672e854b8

commit 25f6bc42d7d6a25d0701f7c7ce479d8672e854b8
Author: Brian Salomon <bsalomon@google.com>
Date: Tue Feb 16 19:27:13 2021

Drop AA on quads that are extremely thin before AA insetting/outsetting.

Bug: chromium:1174186
Change-Id: I91a88d2d57150dee37f08bc4270d399abfd0d60d
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/368497
Commit-Queue: Brian Salomon <bsalomon@google.com>
Reviewed-by: Michael Ludwig <michaelludwig@google.com>
(cherry picked from commit ec04e062f3f5b6d79715572d9b55cd132d9f5945)
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/370837
Reviewed-by: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/25f6bc42d7d6a25d0701f7c7ce479d8672e854b8/gn/gm.gni
[add] https://crrev.com/25f6bc42d7d6a25d0701f7c7ce479d8672e854b8/gm/crbug_1174186.cpp
[modify] https://crrev.com/25f6bc42d7d6a25d0701f7c7ce479d8672e854b8/src/gpu/geometry/GrQuadUtils.cpp


### pb...@google.com (2021-02-18)

bsalomon@ please let me know if all required merges are merged to M89 Branch, If so I will manually drop the "Merge-Approed-89" label not sure why it wasn't removed.

### bs...@google.com (2021-02-18)

Yes, everything is merged to 89.

### pb...@google.com (2021-02-18)

Had confirmed that all the required changes have been merged to M89 branch by Brian. 

The Merge-Approved-89 isn't removed as part of merges is due to missing "Merge-Merged-4389" as the changes were merged to M89 SKIA branch  is "chrome/m89"

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

japong@ do you have a preference for how you'd like to be credited in the Chrome release notes? Thanks for the report!

### ja...@gmail.com (2021-03-02)

You can just put me in as Japong, thanks!

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-04)

hello, japong@! The VRP Panel has decided to award you $500 for this submission. A member of our finance team will be in touch soon to arrange payment. Thank you for reporting this issue to us!  

### am...@google.com (2021-03-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1174186?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1174187, crbug.com/chromium/1178372]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054670)*
