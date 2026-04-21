# Heap-buffer-overflow in SkAnalyticEdge::setLine

| Field | Value |
|-------|-------|
| **Issue ID** | [40054019](https://issues.chromium.org/issues/40054019) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | re...@google.com |
| **Created** | 2020-11-29 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5689989573967872

Fuzzer: jesse_avalanche
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 8
Crash Address: 0x61700005cbb0
Crash State:
  SkAnalyticEdge::setLine
  SkAnalyticEdgeBuilder::addPolyLine
  SkEdgeBuilder::buildPoly
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=826076:826084

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5689989573967872

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5689989573967872 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### cl...@chromium.org (2020-11-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-11-29)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Skia]

### [Deleted User] (2020-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-30)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2020-11-30)

Assigning to reed@: could you PTAL or help assign? From looking at the Skia changelog range from Clusterfuzz [1], it seems possible that this might be related to [2], but I'm not sure.

[1] https://skia.googlesource.com/skia/+log/008d63e23dab8c07f9eeafe99358c912f6c659bf..1fe2b80dc7824fc579451d6f1829c199eb8cd8f6?pretty=fuller&n=10000
[2] https://skia-review.googlesource.com/c/skia/+/331776

### [Deleted User] (2020-12-01)

[Empty comment from Monorail migration]

### sr...@google.com (2020-12-08)

reed@ can you ptal as this is marked RBS for M88 and it would be good to get a fix in early so we get beta coverage.

### sr...@google.com (2020-12-08)

Please help get the fix landed on canary and get the merge ready for beta by monday next week ( Dec 14) so we can include this fix in last beta release for this year. I am trying to get all RBS's fixed by next week beta so we have good beta coverage as we head into no release weeks

### re...@google.com (2020-12-09)

Can reproduce locally -- haven't found a fix yet.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-09)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/0dd0ed6d1e42176935bc3cf3d133df6dc5777358

commit 0dd0ed6d1e42176935bc3cf3d133df6dc5777358
Author: Mike Reed <reed@google.com>
Date: Wed Dec 09 20:27:36 2020

Update our lastmoveindex if addPath ended with a kClose verb

Bug: 1153516
Change-Id: Id6ab162ba3bbf902048009ae2b48b2c67f814b99
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/342616
Reviewed-by: Florin Malita <fmalita@chromium.org>
Commit-Queue: Mike Reed <reed@google.com>

[modify] https://crrev.com/0dd0ed6d1e42176935bc3cf3d133df6dc5777358/tests/PathTest.cpp
[modify] https://crrev.com/0dd0ed6d1e42176935bc3cf3d133df6dc5777358/src/core/SkPath.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8177cfd0766725a2e2a1a86efbe39b39e6a65409

commit 8177cfd0766725a2e2a1a86efbe39b39e6a65409
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 10 00:27:24 2020

Roll Skia from 32c6099d9294 to 201bcee38a94 (11 revisions)

https://skia.googlesource.com/skia.git/+log/32c6099d9294..201bcee38a94

2020-12-09 jvanverth@google.com Use full precision for QuadEdge attributes on iOS.
2020-12-09 tdenniston@google.com [svg] Convert stop-color and stop-opacity to presentation attrs
2020-12-09 tdenniston@google.com [svg] Split out SkSVGColor from paint
2020-12-09 johnstiles@google.com Improve Metal support for out parameters.
2020-12-09 nifong@google.com Reland "Always attempt to flatten images with mskp image ids"
2020-12-09 mtklein@google.com use SkVM_fwd.h in SkColorFilterBase.h
2020-12-09 ethannicholas@google.com Revert "Initial land of SkSL DSL."
2020-12-09 reed@google.com Update our lastmoveindex if addPath ended with a kClose verb
2020-12-09 ethannicholas@google.com Initial land of SkSL DSL.
2020-12-09 fmalita@chromium.org [svg] xml:space support
2020-12-09 adlai@google.com Destroy GrRecordingContext::fAuditTrail last when

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC jmbetancourt@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Cq-Do-Not-Cancel-Tryjobs: true
Bug: chromium:1153516,chromium:1155871
Tbr: jmbetancourt@google.com
Change-Id: I2578a851f6e646c6558afc1c8be97fddbf42e406
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2582875
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#835458}

[modify] https://crrev.com/8177cfd0766725a2e2a1a86efbe39b39e6a65409/DEPS


### cl...@chromium.org (2020-12-10)

ClusterFuzz testcase 5689989573967872 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=835451:835469

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-12)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-12)

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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-12-12)

pls answer https://crbug.com/chromium/1153516#c16 for merge review

### re...@google.com (2020-12-14)

[Empty comment from Monorail migration]

### re...@google.com (2020-12-14)

Here is the only CL: https://skia-review.googlesource.com/c/skia/+/342616

Not a new feature.

### sr...@google.com (2020-12-14)

Merge approved for M88 branch:"4324 pls merge asap

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-14)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/4f9c91ab814e45d10decba2c19a8acdcdd946e9b

commit 4f9c91ab814e45d10decba2c19a8acdcdd946e9b
Author: Mike Reed <reed@google.com>
Date: Mon Dec 14 21:13:30 2020

Update our lastmoveindex if addPath ended with a kClose verb

Bug: 1153516
Change-Id: Id6ab162ba3bbf902048009ae2b48b2c67f814b99
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/342616
Reviewed-by: Florin Malita <fmalita@chromium.org>
Commit-Queue: Mike Reed <reed@google.com>
(cherry picked from commit 0dd0ed6d1e42176935bc3cf3d133df6dc5777358)
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/344159
Reviewed-by: Heather Miller <hcm@google.com>

[modify] https://crrev.com/4f9c91ab814e45d10decba2c19a8acdcdd946e9b/tests/PathTest.cpp
[modify] https://crrev.com/4f9c91ab814e45d10decba2c19a8acdcdd946e9b/src/core/SkPath.cpp


### sr...@google.com (2020-12-15)

per https://crbug.com/chromium/1153516#c21

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations, the VRP panel has decided to award $6000.

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1153516?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054019)*
