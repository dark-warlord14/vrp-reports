# Security DCHECK failure: IsA<Derived>(from) in casting.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40058651](https://issues.chromium.org/issues/40058651) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2022-02-01 |
| **Bounty** | $5,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5988822684598272

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::InlineStylePropertyMap::SetCustomProperty
  blink::StylePropertyMap::set
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=538991:538995

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5988822684598272

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-02-01)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>CSS]

### [Deleted User] (2022-02-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### ad...@google.com (2022-02-08)

This was likely the 'regression', a long long time ago: https://chromium.googlesource.com/chromium/src/+/1a64819208251a3c8d7f0d508de39cf505bdb884, just by turning on a feature.

So this is a long standing bug. andruud@, please could you work out who should fix this?

### [Deleted User] (2022-02-15)

andruud: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-03-17)

andruud@ 
This's High security issue,if you don't have time to deal with it, please pass it to someone else.

### ad...@google.com (2022-03-24)

furthark@ andruud@ could someone jump on this please? This is really old for a high severity bug.

### fu...@chromium.org (2022-03-25)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/02e4b18febb37de8baea718bc2f62cfb5fe56e23

commit 02e4b18febb37de8baea718bc2f62cfb5fe56e23
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Tue Mar 29 10:11:28 2022

[css-typed-om] Disallow CSS-wide keywords for StylePropertyMap.set

We don't support this properly, and the spec does not handle CSS-keywords
either. Disallow it until we can add proper support for this.

Fixed: 1292905
Bug: 1310761
Change-Id: Ieb3d20edfea72c2ccb0928536fdfd86d10aad1a9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3551609
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/main@{#986411}

[modify] https://crrev.com/02e4b18febb37de8baea718bc2f62cfb5fe56e23/third_party/blink/renderer/build/scripts/core/css/templates/cssom_keywords.cc.tmpl
[add] https://crrev.com/02e4b18febb37de8baea718bc2f62cfb5fe56e23/third_party/blink/web_tests/external/wpt/css/css-typed-om/set-css-wide-in-custom-property-crash.html


### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

Requesting merge to extended stable M98 because latest trunk commit (986411) appears to be after extended stable branch point (950365).

Requesting merge to stable M99 because latest trunk commit (986411) appears to be after stable branch point (961656).

Requesting merge to beta M100 because latest trunk commit (986411) appears to be after beta branch point (972766).

Requesting merge to dev M101 because latest trunk commit (986411) appears to be after dev branch point (982481).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-03-30)

ClusterFuzz testcase 5988822684598272 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=986409:986412

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-03-30)

Merge approved: your change passed merge requirements and is auto-approved for M101. Please go ahead and merge the CL to branch 4951 (refs/branch-heads/4951) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-30)

Merge review required: M100 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-30)

Merge review required: M99 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-31)

M100 merge approved, please merge to branch 4896 at your earliest convenience so this fix can be included in the next M100 security respin 

merge-na 98/99-- M100 is now Stable channel, no further planned releases of 98/99 

### pb...@google.com (2022-04-01)

[Bulk Edit] Your change has been approved for M101 branch,please go ahead and merge the CL's to M101 branch manually asap so that it would be part of next week's M101 Beta release.

### pb...@google.com (2022-04-04)

[Bulk Edit]Your change has been approved for M101 branch,please go ahead and merge the CL's to M101 branch manually asap on or before noon tomorrow so that they would be part of this week's M101 Beta release.

### sr...@google.com (2022-04-05)

I have created the CP to M100 here - https://chromium-review.googlesource.com/c/chromium/src/+/3572186 Please help land it after it completes dry-run CQ.

### gi...@appspot.gserviceaccount.com (2022-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1a31e2110440a507ff75e50490ae50a47fdd2a6c

commit 1a31e2110440a507ff75e50490ae50a47fdd2a6c
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Tue Apr 05 20:44:33 2022

[css-typed-om] Disallow CSS-wide keywords for StylePropertyMap.set

We don't support this properly, and the spec does not handle CSS-keywords
either. Disallow it until we can add proper support for this.

(cherry picked from commit 02e4b18febb37de8baea718bc2f62cfb5fe56e23)

Fixed: 1292905
Bug: 1310761
Change-Id: Ieb3d20edfea72c2ccb0928536fdfd86d10aad1a9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3551609
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#986411}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3572186
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Auto-Submit: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/branch-heads/4896@{#1041}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/1a31e2110440a507ff75e50490ae50a47fdd2a6c/third_party/blink/renderer/build/scripts/core/css/templates/cssom_keywords.cc.tmpl
[add] https://crrev.com/1a31e2110440a507ff75e50490ae50a47fdd2a6c/third_party/blink/web_tests/external/wpt/css/css-typed-om/set-css-wide-in-custom-property-crash.html


### pb...@google.com (2022-04-11)

[Bulk Edit] Your change has been approved for M101 branch,please go ahead and merge the CL's to M101 branch(http://go/chromebranches) manually asap so that they would be part of this week's first M101 Beta release.

Note : I will be cutting M101 Beta RC build tomorrow around Noon PST, please try to get the changes cherry picked asap.


### am...@google.com (2022-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2022-04-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-11)

Congratulations! The VRP Panel has decided to award you $5,000 for this report + a $1,000 fuzzer bonus. Thank you for your contributions to Chrome Fuzzing! 

### an...@chromium.org (2022-04-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/75478fe20d017638bee80e1b5e56982493fb043f

commit 75478fe20d017638bee80e1b5e56982493fb043f
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Wed Apr 13 07:55:24 2022

[css-typed-om] Disallow CSS-wide keywords for StylePropertyMap.set

We don't support this properly, and the spec does not handle CSS-keywords
either. Disallow it until we can add proper support for this.

(cherry picked from commit 02e4b18febb37de8baea718bc2f62cfb5fe56e23)

Fixed: 1292905
Bug: 1310761
Change-Id: Ieb3d20edfea72c2ccb0928536fdfd86d10aad1a9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3551609
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#986411}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3581987
Auto-Submit: Anders Hartvoll Ruud <andruud@chromium.org>
Reviewed-by: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/branch-heads/4951@{#716}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/75478fe20d017638bee80e1b5e56982493fb043f/third_party/blink/renderer/build/scripts/core/css/templates/cssom_keywords.cc.tmpl
[add] https://crrev.com/75478fe20d017638bee80e1b5e56982493fb043f/third_party/blink/web_tests/external/wpt/css/css-typed-om/set-css-wide-in-custom-property-crash.html


### [Deleted User] (2022-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1292905?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058651)*
