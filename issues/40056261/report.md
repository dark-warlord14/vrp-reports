# OpenXR VR session exits with Samsung mixed reality controllers

| Field | Value |
|-------|-------|
| **Issue ID** | [40056261](https://issues.chromium.org/issues/40056261) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebXR |
| **Platforms** | Windows |
| **Reporter** | al...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2021-06-17 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36

Steps to reproduce the problem:
1. Connect Samsung Odyssey HMD and controllers
2. Make sure headset is on but both controllers are off
3. Go to https://immersive-web.github.io/webxr-input-profiles/packages/viewer/dist/index.html
4. Enter VR works correctly. You will enter VR experience 
5. Turn on controllers. VR session will exit.

What is the expected behavior?
Controller should be visible and buttons working.

What went wrong?
VR session will immediately exit to Windows Mixed Reality Portal when one or both controllers are on

Did this work before? Yes Chrome 90

Chrome version: 91.0.4472.106  Channel: stable
OS Version: 10.0

Other controllers from HP and Acer are working with the Samsung HMD. The issue only occurs with Samsung Odyssey controllers.

## Timeline

### dt...@chromium.org (2021-06-17)

[Empty comment from Monorail migration]

### dt...@chromium.org (2021-06-17)

[Empty comment from Monorail migration]

### dt...@chromium.org (2021-06-17)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebXR]

### gi...@appspot.gserviceaccount.com (2021-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/673ab2da69084391ec1f6812f620ed096dbbd25f

commit 673ab2da69084391ec1f6812f620ed096dbbd25f
Author: Alexander Cooper <alcooper@chromium.org>
Date: Fri Jun 18 01:15:29 2021

Fix Samsung Odyssey Input Profile Mismatch

There is a mismatch in the size of the Samsung Odyssey input profiles
which causes XR Sessions to be terminated when a controller is on.
This change fixes that mismatch.

Bug: 1221309
Change-Id: Ia265786a985c07ccd1a1e135c8404294caa18016
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2971885
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Commit-Queue: Piotr Bialecki <bialpio@chromium.org>
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Reviewed-by: Piotr Bialecki <bialpio@chromium.org>
Cr-Commit-Position: refs/heads/master@{#893644}

[modify] https://crrev.com/673ab2da69084391ec1f6812f620ed096dbbd25f/device/vr/openxr/openxr_interaction_profiles.h


### kr...@chromium.org (2021-06-18)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-06-18)

As per https://crbug.com/chromium/1221309#c0, the issue needs to be tested using Samsung Odyssey HMD, as we don't have the device to test the issue from our end. Hence, adding label TE-Hardware-Dependency. 
Also cl has already been landed at https://crbug.com/chromium/1221309#c4. Hence, marking it as untriaged.

Thanks...!!

### al...@gmail.com (2021-06-18)

We can triage and test it. Please let me know how we can assist. Is the fix available in the nightly build of Canary?

### al...@chromium.org (2021-06-18)

It looks like it missed the cut off for today's canary.  This link should tell you which version of canary it makes it in to: https://chromiumdash.appspot.com/commit/673ab2da69084391ec1f6812f620ed096dbbd25f

### al...@chromium.org (2021-06-18)

[Empty comment from Monorail migration]

### aj...@google.com (2021-06-18)

[Empty comment from Monorail migration]

### aj...@google.com (2021-06-18)

[Empty comment from Monorail migration]

### aj...@google.com (2021-06-18)

I've added security labels - please mark as Fixed once you're sure this is Fixed and that will kick off the merge request process.

### aj...@google.com (2021-06-18)

(also CC'ed bialpio as they were on the CL).

### [Deleted User] (2021-06-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-18)

[Empty comment from Monorail migration]

### al...@chromium.org (2021-06-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-20)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2021-06-21)

I was able to verify this was fixed in 93.0.4549

### [Deleted User] (2021-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-22)

Requesting merge to beta M92 because latest trunk commit (893644) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-22)

This bug requires manual review: M92's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2021-06-22)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Yes, per the Security team this is a Medium Severity Bug, and from a product standpoint (and the descriptions here: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/release_blockers.md), I think this also meets the bar for ReleaseBlock-Stable, as though it impacts few users (only Desktop VR users with a specific brand of headset), the impact is that WebXR is mostly unusable for those users because it crashes as soon as controllers are connected.

2. Links to the CLs you are requesting to merge.
https://crbug.com/chromium/1221309#c4: https://crrev.com/c/2971885

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
Yes, I would like to Merge this to M-1 (M91) as well. Please let me know if I need to add the additional request label

5. Why are these changes required in this milestone after branch?
This is a late-caught crash bug with a security impact and has a high impact to the WebXR feature for users with the particular headset model.

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
N/a

### am...@chromium.org (2021-06-23)

Approved for M92, please merge to branch 4515 at your earliest convenience. Thanks! 

### al...@chromium.org (2021-06-23)

Merge for 92 out, requesting merge to 91 as well; See justification in https://crbug.com/chromium/1221309#c23

### gi...@appspot.gserviceaccount.com (2021-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/73f769d913fb74ca2e7b48103b69203ee1e57cca

commit 73f769d913fb74ca2e7b48103b69203ee1e57cca
Author: Alexander Cooper <alcooper@chromium.org>
Date: Wed Jun 23 17:58:43 2021

Fix Samsung Odyssey Input Profile Mismatch

There is a mismatch in the size of the Samsung Odyssey input profiles
which causes XR Sessions to be terminated when a controller is on.
This change fixes that mismatch.

(cherry picked from commit 673ab2da69084391ec1f6812f620ed096dbbd25f)

Bug: 1221309
Change-Id: Ia265786a985c07ccd1a1e135c8404294caa18016
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2971885
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Commit-Queue: Piotr Bialecki <bialpio@chromium.org>
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Reviewed-by: Piotr Bialecki <bialpio@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#893644}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2982585
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rafael Cintron <rafael.cintron@microsoft.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Rafael Cintron <rafael.cintron@microsoft.com>
Cr-Commit-Position: refs/branch-heads/4515@{#954}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/73f769d913fb74ca2e7b48103b69203ee1e57cca/device/vr/openxr/openxr_interaction_profiles.h


### am...@chromium.org (2021-06-28)

Approving merge to M91; please merge to branch 4472 at your convenience. At this time there isn't another security refreshed planned for M91. Merging approved to M91 to prepare for any potential unplanned security refresh scenarios before M92. Thanks! 

### gi...@appspot.gserviceaccount.com (2021-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6f7e7bca53c6eef25fdf57d566d7b6ce0bc28145

commit 6f7e7bca53c6eef25fdf57d566d7b6ce0bc28145
Author: Alexander Cooper <alcooper@chromium.org>
Date: Mon Jun 28 19:58:23 2021

Fix Samsung Odyssey Input Profile Mismatch

There is a mismatch in the size of the Samsung Odyssey input profiles
which causes XR Sessions to be terminated when a controller is on.
This change fixes that mismatch.

(cherry picked from commit 673ab2da69084391ec1f6812f620ed096dbbd25f)

Bug: 1221309
Change-Id: Ia265786a985c07ccd1a1e135c8404294caa18016
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2971885
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Commit-Queue: Piotr Bialecki <bialpio@chromium.org>
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Reviewed-by: Piotr Bialecki <bialpio@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#893644}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2993149
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4472@{#1528}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/6f7e7bca53c6eef25fdf57d566d7b6ce0bc28145/device/vr/openxr/openxr_interaction_profiles.h


### [Deleted User] (2021-07-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2021-07-01)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-14)

alimerchant1999@gmail.com - thanks for this report; we'll be crediting you in the Chrome release notes. How would you like to be credited?

### al...@gmail.com (2021-07-14)

I appreciate the quick response on this fix. It was business critical for us. 

You can credit: Ali Merchant, iQ3Connect VR Platform 

### ad...@google.com (2021-07-14)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-21)

OpenXrSystemInputProfiles isn't used on M90-LTS, the parameter change that fixes the issue can' t be applied

### al...@chromium.org (2021-07-21)

As best as I can tell the original regression which caused this landed in  91.0.4434.0, so verifying that it shouldn't be needed for M90.

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congratulations -- the VRP Panel has decided to award you $500 for this report. A member of our finance team will be in touch soon to arrange payment. In the meantime, please let us know how (the name or handle) you would like to be credited for this issue. Thank you again for this report!

### al...@gmail.com (2021-07-22)

Name for credit: Ali Merchant (iQ3Connect)

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1221309?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1221310, crbug.com/chromium/1221311]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056261)*
