# Security: Double-free in libwebp WebPEncode (with alpha) under OOM condition

| Field | Value |
|-------|-------|
| **Issue ID** | [40063285](https://issues.chromium.org/issues/40063285) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | su...@gmail.com |
| **Assignee** | jz...@chromium.org |
| **Created** | 2023-02-28 |
| **Bounty** | $1,337.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

While encoding lossy webp with alpha, trials will be performed with different filtering settings to find the option that compresses the alpha data the best. If a certain stage during the alpha encode fails to allocate memory, the buffer used for a trial encode will be freed [1]. During that failed attempt the trail buffer was not reinitialized and refers to an earlier, successful run. The pointer may have been cached in another variable [2] which will be freed on receipt of the error [3].

See also: <https://crbug.com/webp/603>

[1] <https://chromium.googlesource.com/webm/libwebp/+/refs/tags/v1.3.0/src/enc/alpha_enc.c#260>  

[2] <https://chromium.googlesource.com/webm/libwebp/+/refs/tags/v1.3.0/src/enc/alpha_enc.c#258>  

[3] <https://chromium.googlesource.com/webm/libwebp/+/refs/tags/v1.3.0/src/enc/alpha_enc.c#287>

**VERSION**  

Chrome Version: 110.0.5481.177 stable + beta, dev and tip of tree  

Operating System: All

**REPRODUCTION CASE**  

This requires an OOM condition for a specific allocation to fail while encoding RGBA. This should be reproducible with <canvas>, but given the need for OOM there isn't a reliable reproduction in Chrome. It may be more likely to happen with a large canvas and a 32-bit build.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: N/A  

Client ID (if relevant): N/A

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: From <https://crbug.com/webp/603>, [susah.yak@gmail.com](mailto:susah.yak@gmail.com).

## Timeline

### jz...@chromium.org (2023-02-28)

A fix has been submitted upstream [1]. After cherry-picking to libwebp's release branches, I'll pull this into Chrome from the 1.3.0 branch.

[1] https://chromium-review.googlesource.com/c/webm/libwebp/+/4285643

### jz...@chromium.org (2023-02-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-02-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3808d2e69bf1a3fe3f4d83d607bb25e7b2370732

commit 3808d2e69bf1a3fe3f4d83d607bb25e7b2370732
Author: James Zern <jzern@chromium.org>
Date: Wed Mar 01 21:02:33 2023

Roll src/third_party/libwebp/src/ 603e8d7ad..fd7b5d484 (2 commits)

https://chromium.googlesource.com/webm/libwebp.git/+log/603e8d7adb0c..fd7b5d484644

$ git log 603e8d7ad..fd7b5d484 --date=short --no-merges --format='%ad %ae %s'
2023-02-22 jzern EncodeAlphaInternal: clear result->bw on error
2023-02-23 jzern PaletteSortModifiedZeng: fix leak on error

Created with:
  roll-dep src/third_party/libwebp/src

Bug: 1420107
Bug: webp:603
Change-Id: Ib525d4e248bd04bc7229a1253f6b6292b8cd3ffa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4298413
Commit-Queue: James Zern <jzern@google.com>
Reviewed-by: Leon Scroggins <scroggo@google.com>
Cr-Commit-Position: refs/heads/main@{#1111809}

[modify] https://crrev.com/3808d2e69bf1a3fe3f4d83d607bb25e7b2370732/DEPS


### jz...@chromium.org (2023-03-02)

[Empty comment from Monorail migration]

### jz...@chromium.org (2023-03-02)

Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?

This is marked as medium security with M111 as the target. The crash can occur in low memory conditions / large <canvas> encode. M110 might be valid since it's an extended release.

What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/4298413

Have the changes been released and tested on canary?

Yes

Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

[Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?
If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No

### [Deleted User] (2023-03-02)

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
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-02)

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-02)

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
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

[Empty comment from Monorail migration]

### jz...@chromium.org (2023-03-03)

The merge request questions were answered in https://crbug.com/chromium/1420107#c8.

### am...@chromium.org (2023-03-04)

Thanks James. Holding off on merge approvals for M111 and M110 right now since M111 and M110 are needing to be recut to include two Pri-0 fixes. Keeping this in the review queue until Monday or early next week after M111/Stable RC is finalized. 

M112 merge approved, please merge to branch 5615 so this fix can be included in the next M112/dev and first beta.

### go...@chromium.org (2023-03-06)

Please merge your change to M112 ASAP so we can take fix/merge in for this week's beta.

M112 Branch Details: https://chromiumdash.appspot.com/branches

### gi...@appspot.gserviceaccount.com (2023-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/70ce37d24cb93ee376467e560404aab4a7b2018b

commit 70ce37d24cb93ee376467e560404aab4a7b2018b
Author: James Zern <jzern@chromium.org>
Date: Mon Mar 06 17:11:26 2023

Roll src/third_party/libwebp/src/ 603e8d7ad..fd7b5d484 (2 commits)

https://chromium.googlesource.com/webm/libwebp.git/+log/603e8d7adb0c..fd7b5d484644

$ git log 603e8d7ad..fd7b5d484 --date=short --no-merges --format='%ad %ae %s'
2023-02-22 jzern EncodeAlphaInternal: clear result->bw on error
2023-02-23 jzern PaletteSortModifiedZeng: fix leak on error

Created with:
  roll-dep src/third_party/libwebp/src

(cherry picked from commit 3808d2e69bf1a3fe3f4d83d607bb25e7b2370732)

Bug: 1420107
Bug: webp:603
Change-Id: Ib525d4e248bd04bc7229a1253f6b6292b8cd3ffa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4298413
Commit-Queue: James Zern <jzern@google.com>
Reviewed-by: Leon Scroggins <scroggo@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1111809}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4310757
Auto-Submit: James Zern <jzern@google.com>
Commit-Queue: Leon Scroggins <scroggo@google.com>
Cr-Commit-Position: refs/branch-heads/5615@{#230}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/70ce37d24cb93ee376467e560404aab4a7b2018b/third_party/libwebp/README.chromium
[modify] https://crrev.com/70ce37d24cb93ee376467e560404aab4a7b2018b/DEPS


### gi...@appspot.gserviceaccount.com (2023-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8ee8edb5aa6b081685c155084442c535405da721

commit 8ee8edb5aa6b081685c155084442c535405da721
Author: James Zern <jzern@chromium.org>
Date: Mon Mar 06 18:28:44 2023

third_party/libwebp,README.chromium: update Revision

missed in:
http://crrev.com/3808d2e69bf1a
(Roll src/third_party/libwebp/src/ 603e8d7ad..fd7b5d484 (2 commits))

Bug: 1420107
Change-Id: I5e140c5f896f9a7e2c499eea2970b468756095b5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4310758
Auto-Submit: James Zern <jzern@google.com>
Reviewed-by: Leon Scroggins <scroggo@google.com>
Commit-Queue: James Zern <jzern@google.com>
Cr-Commit-Position: refs/heads/main@{#1113468}

[modify] https://crrev.com/8ee8edb5aa6b081685c155084442c535405da721/third_party/libwebp/README.chromium


### am...@chromium.org (2023-03-08)

M111 and M110 merges approved, please merge this libwebp update to branches 5563 and 5481 respectively at your earliest convenience so it can be included in the next M111/Stable and M110/Extended updates. Thank you! 

### gi...@appspot.gserviceaccount.com (2023-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d9424afd93ace9729e57fb7cf84286b1da579145

commit d9424afd93ace9729e57fb7cf84286b1da579145
Author: James Zern <jzern@chromium.org>
Date: Thu Mar 09 19:23:45 2023

Roll src/third_party/libwebp/src/ 603e8d7ad..fd7b5d484 (2 commits)

https://chromium.googlesource.com/webm/libwebp.git/+log/603e8d7adb0c..fd7b5d484644

$ git log 603e8d7ad..fd7b5d484 --date=short --no-merges --format='%ad %ae %s'
2023-02-22 jzern EncodeAlphaInternal: clear result->bw on error
2023-02-23 jzern PaletteSortModifiedZeng: fix leak on error

Created with:
  roll-dep src/third_party/libwebp/src

(cherry picked from commit 70ce37d24cb93ee376467e560404aab4a7b2018b)

Bug: 1420107
Bug: webp:603
Change-Id: I1b3096ad8696079f8736d3e1f4533962a24a24ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4322697
Commit-Queue: Leon Scroggins <scroggo@google.com>
Auto-Submit: James Zern <jzern@google.com>
Reviewed-by: Leon Scroggins <scroggo@google.com>
Cr-Commit-Position: refs/branch-heads/5563@{#1113}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/d9424afd93ace9729e57fb7cf84286b1da579145/third_party/libwebp/README.chromium
[modify] https://crrev.com/d9424afd93ace9729e57fb7cf84286b1da579145/DEPS


### gi...@appspot.gserviceaccount.com (2023-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4621a191a76b536be7c5d0c22a1f56ef57fc9ac9

commit 4621a191a76b536be7c5d0c22a1f56ef57fc9ac9
Author: James Zern <jzern@chromium.org>
Date: Thu Mar 09 21:42:02 2023

Roll src/third_party/libwebp/src/ 7366f7f39..0aa5f755c (9 commits)

https://chromium.googlesource.com/webm/libwebp.git/+log/7366f7f394af..0aa5f755c601

$ git log 7366f7f39..0aa5f755c --date=short --no-merges --format='%ad %ae %s'
2023-02-23 jzern PaletteSortModifiedZeng: fix leak on error
2023-02-22 jzern EncodeAlphaInternal: clear result->bw on error
2022-10-04 jzern WebPConfig.cmake.in: add find_dependency(Threads)
2022-08-05 jzern update ChangeLog
2022-08-04 jzern update NEWS
2022-08-04 jzern bump version to 1.2.4
2022-07-20 jzern lossless: fix crunch mode w/WEBP_REDUCE_SIZE
2022-07-21 jzern CMakeLists.txt: correct libwebpmux name in WebPConfig.cmake
2022-07-21 jzern Revert "cmake: fix webpmux lib name for cmake linking"

Created with:
  roll-dep src/third_party/libwebp/src

Bug: 1420107
Bug: webp:603
Change-Id: I8d5f1212e54d98e0df28e82a3574b48505bfa978
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4326427
Commit-Queue: Leon Scroggins <scroggo@google.com>
Reviewed-by: Leon Scroggins <scroggo@google.com>
Auto-Submit: James Zern <jzern@google.com>
Cr-Commit-Position: refs/branch-heads/5481@{#1343}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/4621a191a76b536be7c5d0c22a1f56ef57fc9ac9/third_party/libwebp/README.chromium
[modify] https://crrev.com/4621a191a76b536be7c5d0c22a1f56ef57fc9ac9/DEPS


### am...@chromium.org (2023-03-17)

hank you for the report. As it is not evident that this issue would manifest or be exploitable though Chrome, we must unfortunately decline to extend a VRP reward.  

### am...@chromium.org (2023-04-11)

[Empty comment from Monorail migration]

### ko...@google.com (2023-04-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-12)

Google OSS CNA has issued a CVE for this security bug

### ko...@google.com (2023-04-17)

Hello,

Google Open Source Software Vulnerability Reward Program panel has decided to issue a reward of $1337 for your report. Congratulations!

Rationale for this decision:
Target is in "Standard OSS projects" tier.
Issue category is "Product vulnerabilities".
We applied 1 downgrade from the base amount, since the exploitation requires an OOM condition.

### am...@chromium.org (2023-04-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
******************************

### am...@chromium.org (2023-04-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1420107?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063285)*
