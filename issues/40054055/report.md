# Security: Skia GPU bug

| Field | Value |
|-------|-------|
| **Issue ID** | [40054055](https://issues.chromium.org/issues/40054055) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ts...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2020-12-03 |
| **Bounty** | $6,000.00 |

## Description

This is a tracking bug to take care of the Chromium merge process for:
https://bugs.chromium.org/p/skia/issues/detail?id=10989

## Timeline

### ad...@google.com (2020-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-03)

robertphilips@ says:

>  The bug has Skia overwriting an arbitrary amount of memory which does seem like it would have security consequences.
> It is a P0 bug in Skia that they would like cherry picked back to both M87 and M88

Setting security impact and severity on that basis.

It's also in buganizer here: https://buganizer.corp.google.com/issues/174268976

### ad...@google.com (2020-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-03)

Fix is here:
https://skia-review.googlesource.com/c/skia/+/339165

This has been approved for M87 and M88 merge by dgagnon@ here: https://buganizer.corp.google.com/issues/174268976 so I am reflecting that status.

### ad...@google.com (2020-12-03)

I don't know what OSs this affects but:

> The Skia-side bug (skbug.com/10989) has a .html that will cause the issue so it isn't limited to ChromeOS.

so I'm assuming all OSs until we're told otherwise.

This is a GPU process buffer overflow triggered directly from HTML content, so I fear this may be Critical, but I'm going to discuss a bit before ringing the alarm bells.

### [Deleted User] (2020-12-03)

It is definitely not limited to ChromeOS. Any platform that supports windows rectangles would be vulnerable.

### ad...@google.com (2020-12-03)

I'm going to stick with High severity because the severity guidelines have more faith in the GPU sandbox than I do :) https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#TOC-High-severity

### la...@google.com (2020-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-03)

re https://crbug.com/chromium/1155178#c5, I believe the bug fix has only received M88 merge approval so far over on https://buganizer.corp.google.com/issues/174268976.

### [Deleted User] (2020-12-03)

Replying to https://crbug.com/chromium/1155178#c5, I believe the bug fix has only received M88 merge approval over on https://buganizer.corp.google.com/issues/174268976.

### ad...@google.com (2020-12-03)

robertphilips reports:

> Typing GL_EXT_window_rectangles into:
> https://opengles.gpuinfo.org/listextensions.php
> yields a coverage of 0.62%. Which indicates it isn't that prevalent.
> This page:
> https://opengles.gpuinfo.org/listreports.php?extension=GL_EXT_window_rectangles

I think that if this only affects a *small* minority of GPUs then that's another reason that we shouldn't rush to release this before the next scheduled security refresh. I'm comfortable with High severity.

### ad...@google.com (2020-12-03)

My mistake - merge was only approved to M88 so far on the buganizer bug.

And that suits me - I would prefer we do not yet merge this fix to M87 whilst we sort out some Android releasing issues.

### ad...@google.com (2020-12-03)

(possibly duplicated comment due to partial Monorail outage)

robertphilips says:
> Typing GL_EXT_window_rectangles into:
> https://opengles.gpuinfo.org/listextensions.php
> yields a coverage of 0.62%. Which indicates it isn't that prevalent.
> This page:
> https://opengles.gpuinfo.org/listreports.php?extension=GL_EXT_window_rectangles

Also, this was in fact only approved on buganizer for M88 merge not M87, and I have adjusted labels appropriately. That suits me because we need to deal with some Android releasing issues on M87.

### [Deleted User] (2020-12-03)

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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

1. I believe this does fit w/in the guidelines for a cherry-pick back to M87 (stable). In ChromeOS it is a P0 bug (https://buganizer.corp.google.com/issues/174268976) and, although I believe it is only labeled a P-1 in this bug, it does have some pretty severe security ramifications. 

2) https://skia-review.googlesource.com/c/skia/+/339165 (Stop overflow of windows rects in GrClipStack). Note that there are only two relevant lines in this CL:
   src/gpu/GrClipStackClip.cpp        1404
   src/gpu/GrWindowRectangles.h       51
All the other changes are either formatting or to allow testing.

3) Yes - the CL landed in Chrome on 11/30 at r831950 in https://chromium-review.googlesource.com/c/chromium/src/+/2565106 

4) No, M87 is as far as it makes sense to cherry-pick the fix.

5) The prior code was very very wrong and could result in a heap overflow.

6) No - this is a bug fix.

7) N/A

8) I have reached out to vsuley@ (who I believe to be the correct owner) for a review but haven't heard back from him yet.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-03)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/fc6759b235c51ecc84f239b70549380da290d6e9

commit fc6759b235c51ecc84f239b70549380da290d6e9
Author: Robert Phillips <robertphillips@google.com>
Date: Thu Dec 03 19:33:40 2020

[M88 Cherrypick] Stop overflow of windows rects in GrClipStack

Bug: skia:10989
Bug: b/174268976
Bug:1155178
Change-Id: Id9af60782dd90ab65a51301a5d6368109f466b9f
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/340716
Reviewed-by: Michael Ludwig <michaelludwig@google.com>
Reviewed-by: Brian Salomon <bsalomon@google.com>
Commit-Queue: Robert Phillips <robertphillips@google.com>

[modify] https://crrev.com/fc6759b235c51ecc84f239b70549380da290d6e9/src/gpu/GrClipStackClip.cpp
[modify] https://crrev.com/fc6759b235c51ecc84f239b70549380da290d6e9/src/gpu/mock/GrMockCaps.h
[modify] https://crrev.com/fc6759b235c51ecc84f239b70549380da290d6e9/include/gpu/mock/GrMockTypes.h
[modify] https://crrev.com/fc6759b235c51ecc84f239b70549380da290d6e9/tests/GrClipStackTest.cpp
[modify] https://crrev.com/fc6759b235c51ecc84f239b70549380da290d6e9/src/gpu/GrClipStack.cpp
[modify] https://crrev.com/fc6759b235c51ecc84f239b70549380da290d6e9/src/gpu/GrWindowRectangles.h


### [Deleted User] (2020-12-03)

[Empty comment from Monorail migration]

### ro...@google.com (2020-12-04)

ChromeOS has okayed the cherry-pick back to M87. Unless we do something special I believe Chrome will also automatically get that cherry-pick. 

Is everyone okay with that?

### ad...@google.com (2020-12-04)

Yes, we are now good to merge to M87. Formally approving merge to M87, branch 4280.

### [Deleted User] (2020-12-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-04)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/73c703c2bdbde9a7602bc017f08376bfb4c79f33

commit 73c703c2bdbde9a7602bc017f08376bfb4c79f33
Author: Robert Phillips <robertphillips@google.com>
Date: Fri Dec 04 18:46:55 2020

[M87 cherry-pick] Stop overflow of windows rects in GrClipStack

Bug: skia:10989
Bug: b/174268976
Bug:1155178
Change-Id: Ida9c7e85de219fc25d2a6cdc1e998f53f1f2309f
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/341006
Reviewed-by: Michael Ludwig <michaelludwig@google.com>
Reviewed-by: Brian Salomon <bsalomon@google.com>
Commit-Queue: Robert Phillips <robertphillips@google.com>

[modify] https://crrev.com/73c703c2bdbde9a7602bc017f08376bfb4c79f33/src/gpu/GrClipStackClip.cpp
[modify] https://crrev.com/73c703c2bdbde9a7602bc017f08376bfb4c79f33/src/gpu/mock/GrMockCaps.h
[modify] https://crrev.com/73c703c2bdbde9a7602bc017f08376bfb4c79f33/include/gpu/mock/GrMockTypes.h
[modify] https://crrev.com/73c703c2bdbde9a7602bc017f08376bfb4c79f33/tests/GrClipStackTest.cpp
[modify] https://crrev.com/73c703c2bdbde9a7602bc017f08376bfb4c79f33/src/gpu/GrClipStack.cpp
[modify] https://crrev.com/73c703c2bdbde9a7602bc017f08376bfb4c79f33/src/gpu/GrWindowRectangles.h


### go...@chromium.org (2020-12-04)

Please merge your change to M88 branch 4324 ASAP. Thank you.

### ro...@google.com (2020-12-04)

Responding to https://crbug.com/chromium/1155178#c26, the M88 cherry pick landed in https://crbug.com/chromium/1155178#c20.

### be...@google.com (2020-12-07)

Removing approved label as this has landed for M87

### [Deleted User] (2020-12-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2020-12-08)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-10)

tsubmunu@ Congratulations, the VRP panel has awarded $5000 for this bug, plus a $1000 patch bonus. Someone from our finance team will be in touch. How would you like to be credited in he Chrome release notes when we release this fix?

### ad...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### as...@google.com (2021-01-28)

Marking as not applicable for M86 LTS since GrClipStack is not present there.

### [Deleted User] (2021-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1155178?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054055)*
