# Security: scrollTop of ListBox autofill preview discloses sensitive information

| Field | Value |
|-------|-------|
| **Issue ID** | [40057661](https://issues.chromium.org/issues/40057661) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ym...@ym.kim |
| **Assignee** | ba...@chromium.org |
| **Created** | 2021-10-20 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

When previewing the suggested value of autofill in ListBox (<select> with size > 2), it is scrolled to the suggested value: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/forms/select_type.cc;l=983;drc=5cc43d26e76ee462b6224ec447cef2bc5a41a25e>

This can be used to infer the previewed option, disclosing sensitive information:  

select.options[Math.round(select.scrollTop \* select.options.length / select.scrollHeight) + 1]

\* Proposed fix: scrollTop should return 0 if the autofill is being previewed

**VERSION**  

Reproducible on:

- 94.0.4606.61 stable, Windows 10 Version 21H1 (Build 19043.1288)
- 97.0.4674.2 canary, Windows 10 Version 21H1 (Build 19043.1288)
- 94.0.4606.61 stable, Linux 5.11.0-34-generic #40~20.04.1-Ubuntu SMP

**REPRODUCTION CASE**

1. Add at least one credit card entry in chrome://settings/payments and/or one address entry in chrome://settings/addresses
2. Serve the attached poc.html over a secure origin and navigate to the page (an online version is available in <https://me94bk1usdv8c8tfybvy.netlify.app/xyo0vvbwwizlnbpwjp15.html>)
3. Click on any input and hover the mouse over an autofill entry OR press the up or down arrow key on focused input to preview autofill.
4. The inferred content will appear below.

**CREDIT INFORMATION**  

Reporter credit: Young Min Kim (@ylemkimon), CompSec Lab at Seoul National University

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 4.0 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 228.4 KB)
- [issue-1261689.patch](attachments/issue-1261689.patch) (text/plain, 1.8 KB)
- [poc-2.html](attachments/poc-2.html) (text/plain, 4.2 KB)
- [issue-1261689-2.patch](attachments/issue-1261689-2.patch) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2021-10-20)

[Empty comment from Monorail migration]

### ym...@ym.kim (2021-10-20)

Furthermore, the scroll should be reset if the preview is finished.

### ym...@ym.kim (2021-10-20)

Real-world scenarios and related bugs are identical to sections 4 and 5 in the https://crbug.com/chromium/1253101, respectively.

Please find attached a suggested patch

### es...@chromium.org (2021-10-20)

Thanks for the report and the patch! Autofill owners, can you please take a look?

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2021-10-20)

[Empty comment from Monorail migration]

### ba...@chromium.org (2021-10-20)

Thank you for the report and the patch!

### ba...@chromium.org (2021-10-20)

Could you explain to me why you made the changes to ListBoxSelectType::DidSetSuggestedOption in your patch?

### ym...@ym.kim (2021-10-20)

See c#2. The scroll remains after the preview is finished but not applied (selected), so it should be reset to prevent leak. I've chosen `FirstSelectableOption()` because it's available, but it could be scrolled to the top, the first option, or previous saved location.

### [Deleted User] (2021-10-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-20)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-04)

battre: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/55b07dc54220200313366ec821d2303cd847187a

commit 55b07dc54220200313366ec821d2303cd847187a
Author: Dominic Battre <battre@chromium.org>
Date: Mon Nov 15 20:58:16 2021

Pin scrollTop to 0 during autofill preview

This CL forces scrollTop of a ListBox to be 0 during autofill preview
state. After autofill preview ends, it attempts to scroll the ListBox
back so that a previously selected element becomes visible.

Fixed: 1261689
Change-Id: I8593544577cf054cca40e7a487d3248acdcfdaa7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3279960
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Cr-Commit-Position: refs/heads/main@{#941822}

[modify] https://crrev.com/55b07dc54220200313366ec821d2303cd847187a/third_party/blink/renderer/core/html/forms/select_type.cc
[modify] https://crrev.com/55b07dc54220200313366ec821d2303cd847187a/third_party/blink/web_tests/fast/forms/text/input-appearance-autocomplete-suggested-value-over-placeholder-value-expected.html
[modify] https://crrev.com/55b07dc54220200313366ec821d2303cd847187a/third_party/blink/renderer/core/testing/internals.cc
[modify] https://crrev.com/55b07dc54220200313366ec821d2303cd847187a/third_party/blink/web_tests/fast/forms/text/input-appearance-autocomplete-suggested-value-when-underlying-placeholder-is-removed-expected.html
[modify] https://crrev.com/55b07dc54220200313366ec821d2303cd847187a/third_party/blink/renderer/core/dom/element.cc


### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### ym...@ym.kim (2021-11-22)

I wonder why the Sheriffbot is not requesting merges, even if this is Medium severity.

### ba...@chromium.org (2021-11-23)

+adetaylor regarding https://crbug.com/chromium/1261689#c16. Shall we merge?

### am...@chromium.org (2021-11-23)

this is a known https://crbug.com/chromium/1262390; a potential fix has been landed so this shouldn't be an issue soon 

### am...@chromium.org (2021-11-23)

removing ade from cc so he doesn't get pinged on merge review updates; I've added merge review labels so this will add to my review queue - thanks 

### am...@google.com (2021-11-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-24)

Congratulations! The VRP Panel has decided to award you $4000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for your report and nice work!! 

### am...@google.com (2021-11-24)

[Empty comment from Monorail migration]

### ym...@ym.kim (2021-11-27)

It turns out that pinning scrollTop to 0 when the suggested value is empty also leaks the suggested option, as the suggested value becomes empty when the suggested option is removed (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/forms/html_select_element.cc;l=784-785;drc=66f8666257dd5d2687c37c155f40cc72e0176270). Instead, it should check for the autofill state, which doesn't change even after the suggested option is removed. Please find attached the new PoC and patch. The reproduction steps are identical, and the online version is available in https://me94bk1usdv8c8tfybvy.netlify.app/xyo0vvbwwizlnbpwjp15-2.html.

### am...@chromium.org (2021-11-29)

I've re-opened this based on the new POC in https://crbug.com/chromium/1261689#c23 and verifying this does indeed reproduce with the new POC. battre@ would you mind taking a look at this? 

### am...@chromium.org (2021-11-29)

based on the above, going to not approve merge of the earlier landed fix for now until this is reassessed 

### ad...@google.com (2021-12-13)

[Empty comment from Monorail migration]

### ba...@chromium.org (2021-12-13)

Thanks for the reminder, Adrian. I have submitted a CL for review here: https://chromium-review.googlesource.com/c/chromium/src/+/3335637

Thank you for the followup and patch.

I would prefer to merge both CLs together.

### ad...@chromium.org (2021-12-13)

Great. Thank you for following up. When that follow up CL lands, please mark this as Fixed and it will go into the queue for merge approval.

### gi...@appspot.gserviceaccount.com (2021-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e3aeadcf584ebb5d7f61cd141f9af317cb60cf21

commit e3aeadcf584ebb5d7f61cd141f9af317cb60cf21
Author: Dominic Battre <battre@chromium.org>
Date: Tue Dec 14 02:07:29 2021

Fix preview state detection

This CL fixes the preview state detection in some edge cases. See
crbug.com/1261689#c23.

Fixed: 1261689
Change-Id: Iefe27e2748acb4b524e8a0811973bdceda46089a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3335637
Reviewed-by: Mason Freed <masonf@chromium.org>
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Commit-Position: refs/heads/main@{#951313}

[modify] https://crrev.com/e3aeadcf584ebb5d7f61cd141f9af317cb60cf21/third_party/blink/renderer/core/dom/element.cc


### ad...@google.com (2021-12-15)

Approving merge to M96, branch 4664, and M97, branch 4692, but please wait until the CL in https://crbug.com/chromium/1261689#c29 has had 48 hours in Canary and confirm that there are no unexpected crashes from the relevant code. We're not imminently about to cut a release RC so it's OK if this doesn't land in those branches for a couple of days, but it would be great to get it in before the holiday break on the assumption that we might make a release immediately after the holidays (no such release is planned, but it would be surprising if no events necessitated it!)

Also approving merge of https://crbug.com/chromium/1261689#c29 to M98, branch 4758, because it landed after M98 branch point.

### ad...@google.com (2021-12-15)

[Empty comment from Monorail migration]

### ba...@chromium.org (2021-12-20)

Adding jarhar@ because I will request a merge review.

### gi...@appspot.gserviceaccount.com (2021-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9817ab616338df9cf1dbbbec6e589c4abfcacffb

commit 9817ab616338df9cf1dbbbec6e589c4abfcacffb
Author: Dominic Battre <battre@chromium.org>
Date: Mon Dec 20 16:41:52 2021

Pin scrollTop to 0 during autofill preview

This CL forces scrollTop of a ListBox to be 0 during autofill preview
state. After autofill preview ends, it attempts to scroll the ListBox
back so that a previously selected element becomes visible.

(cherry picked from commit 55b07dc54220200313366ec821d2303cd847187a)

Fixed: 1261689
Change-Id: I8593544577cf054cca40e7a487d3248acdcfdaa7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3279960
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#941822}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3347569
Auto-Submit: Dominic Battré <battre@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#1097}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/9817ab616338df9cf1dbbbec6e589c4abfcacffb/third_party/blink/renderer/core/html/forms/select_type.cc
[modify] https://crrev.com/9817ab616338df9cf1dbbbec6e589c4abfcacffb/third_party/blink/web_tests/fast/forms/text/input-appearance-autocomplete-suggested-value-over-placeholder-value-expected.html
[modify] https://crrev.com/9817ab616338df9cf1dbbbec6e589c4abfcacffb/third_party/blink/renderer/core/testing/internals.cc
[modify] https://crrev.com/9817ab616338df9cf1dbbbec6e589c4abfcacffb/third_party/blink/web_tests/fast/forms/text/input-appearance-autocomplete-suggested-value-when-underlying-placeholder-is-removed-expected.html
[modify] https://crrev.com/9817ab616338df9cf1dbbbec6e589c4abfcacffb/third_party/blink/renderer/core/dom/element.cc


### [Deleted User] (2021-12-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cff03c22c54b3bbdb0642b9062855f5f77f9d12a

commit cff03c22c54b3bbdb0642b9062855f5f77f9d12a
Author: Dominic Battre <battre@chromium.org>
Date: Mon Dec 20 18:53:00 2021

Pin scrollTop to 0 during autofill preview

This CL forces scrollTop of a ListBox to be 0 during autofill preview
state. After autofill preview ends, it attempts to scroll the ListBox
back so that a previously selected element becomes visible.

(cherry picked from commit 55b07dc54220200313366ec821d2303cd847187a)

Fixed: 1261689
Change-Id: I8593544577cf054cca40e7a487d3248acdcfdaa7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3279960
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#941822}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3347570
Auto-Submit: Dominic Battré <battre@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1330}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/cff03c22c54b3bbdb0642b9062855f5f77f9d12a/third_party/blink/renderer/core/html/forms/select_type.cc
[modify] https://crrev.com/cff03c22c54b3bbdb0642b9062855f5f77f9d12a/third_party/blink/web_tests/fast/forms/text/input-appearance-autocomplete-suggested-value-over-placeholder-value-expected.html
[modify] https://crrev.com/cff03c22c54b3bbdb0642b9062855f5f77f9d12a/third_party/blink/renderer/core/testing/internals.cc
[modify] https://crrev.com/cff03c22c54b3bbdb0642b9062855f5f77f9d12a/third_party/blink/web_tests/fast/forms/text/input-appearance-autocomplete-suggested-value-when-underlying-placeholder-is-removed-expected.html
[modify] https://crrev.com/cff03c22c54b3bbdb0642b9062855f5f77f9d12a/third_party/blink/renderer/core/dom/element.cc


### gi...@appspot.gserviceaccount.com (2021-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/76ee5ef9198eeb8185bfa6a90b12495ae891c563

commit 76ee5ef9198eeb8185bfa6a90b12495ae891c563
Author: Dominic Battre <battre@chromium.org>
Date: Mon Dec 20 22:37:51 2021

Fix preview state detection

This CL fixes the preview state detection in some edge cases. See
crbug.com/1261689#c23.

(cherry picked from commit e3aeadcf584ebb5d7f61cd141f9af317cb60cf21)

Fixed: 1261689
Change-Id: Iefe27e2748acb4b524e8a0811973bdceda46089a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3335637
Reviewed-by: Mason Freed <masonf@chromium.org>
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#951313}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3350770
Auto-Submit: Dominic Battré <battre@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1332}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/76ee5ef9198eeb8185bfa6a90b12495ae891c563/third_party/blink/renderer/core/dom/element.cc


### gi...@appspot.gserviceaccount.com (2021-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/896620bfe9d405cde104d74347e300d1ddb03c21

commit 896620bfe9d405cde104d74347e300d1ddb03c21
Author: Dominic Battre <battre@chromium.org>
Date: Tue Dec 21 18:01:14 2021

Fix preview state detection

This CL fixes the preview state detection in some edge cases. See
crbug.com/1261689#c23.

(cherry picked from commit e3aeadcf584ebb5d7f61cd141f9af317cb60cf21)

Fixed: 1261689
Change-Id: Iefe27e2748acb4b524e8a0811973bdceda46089a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3335637
Reviewed-by: Mason Freed <masonf@chromium.org>
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#951313}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3350768
Auto-Submit: Dominic Battré <battre@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#1117}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/896620bfe9d405cde104d74347e300d1ddb03c21/third_party/blink/renderer/core/dom/element.cc


### ba...@chromium.org (2021-12-22)

All merging should be done.

### ym...@ym.kim (2021-12-22)

Sorry for chiming in, but it seems it's not merged to M98 (4758). Thank you for your hard work.

### ba...@chromium.org (2021-12-22)

Oh... Thanks for catching this! I have created https://chromium-review.googlesource.com/c/chromium/src/+/3348406.

### gi...@appspot.gserviceaccount.com (2021-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/91fbf179875be529f32f4ad2ba83186f9c072641

commit 91fbf179875be529f32f4ad2ba83186f9c072641
Author: Dominic Battre <battre@chromium.org>
Date: Wed Dec 22 16:25:16 2021

Fix preview state detection

This CL fixes the preview state detection in some edge cases. See
crbug.com/1261689#c23.

(cherry picked from commit e3aeadcf584ebb5d7f61cd141f9af317cb60cf21)

Fixed: 1261689
Change-Id: Iefe27e2748acb4b524e8a0811973bdceda46089a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3335637
Reviewed-by: Mason Freed <masonf@chromium.org>
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#951313}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3348406
Auto-Submit: Dominic Battré <battre@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#186}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/91fbf179875be529f32f4ad2ba83186f9c072641/third_party/blink/renderer/core/dom/element.cc


### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1261689?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057661)*
