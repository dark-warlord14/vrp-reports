# Heap-use-after-free in libvk_swiftshader.dylib

| Field | Value |
|-------|-------|
| **Issue ID** | [40055096](https://issues.chromium.org/issues/40055096) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | su...@chromium.org |
| **Created** | 2021-03-07 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5666461394468864

Fuzzer: attekett_dom_fuzzer
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x0001649ac588
Crash State:
  libvk_swiftshader.dylib
  vk::GraphicsPipeline::getIndexBuffers
  CmdDrawIndexed::play
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=mac_asan_chrome&revision=860575

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5666461394468864

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5666461394468864 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2021-03-07)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-03-08)

Poking ClusterFuzz to see if we can get a better regression range.

### [Deleted User] (2021-03-08)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2021-03-08)

Mac triage: -> SwiftShader for triage. +cc a couple of owners.

[Monorail components: Internals>GPU>SwiftShader]

### cw...@chromium.org (2021-03-08)

Assigning Nicolas for triage.

### ca...@chromium.org (2021-03-08)

I see this produces "src/Vulkan/VkDeviceMemory.cpp:235 WARNING: VkMemoryAllocateInfo->pNext sType = 1000178000".

https://issuetracker.google.com/178039602 tracks that issue, and might fix the heap-use-after-free too.

We're not enabling SwANGLE for Mac just yet, so this isn't a priority at this point. Alexis can you make this a blocker of the Mac enablement?

### su...@chromium.org (2021-03-08)

This isn't a release blocker, this code isn't shipped with Chromium yet.

### [Deleted User] (2021-03-09)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-03-20)

ClusterFuzz testcase 5666461394468864 is verified as fixed in https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=864944:864945

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-20)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M90. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-20)

This bug requires manual review: M90's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-03-22)

pls help answer https://crbug.com/chromium/1185611#c17 for review. 

### su...@chromium.org (2021-03-22)

As per https://crbug.com/chromium/1185611#c8, this code does not ship with Chrome. There's nothing to merge.

### ad...@google.com (2021-03-22)

Per https://crbug.com/chromium/1185611#c8 this is not shipped, so Security_Impact-None and no need to merge.

### [Deleted User] (2021-03-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-24)

Congratulations attekett! The VRP Panel has awarded you $6000 for this report. Thank you for your contributions to Chrome Fuzzing! 

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-01)

ClusterFuzz testcase 5666461394468864 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### gi...@appspot.gserviceaccount.com (2021-04-28)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader/+/484a3e15893c769304509bf1607a42f205a7002d

commit 484a3e15893c769304509bf1607a42f205a7002d
Author: Alexis Hetu <sugoi@google.com>
Date: Wed Apr 28 14:34:07 2021

Silence warning for MacOS

MacOS tests have been spamming a lot of lines of this warning from
SwiftShader, sometimes hiding the actual cause of an issue:

../../third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:235 WARNING: VkMemoryAllocateInfo->pNext sType = 1000178000

This CL properly silences this warning.

Bug: chromium:1185611
Change-Id: Ic9c84c0d57dc142904626bbb3c8a0af5c3cff40d
Reviewed-on: https://swiftshader-review.googlesource.com/c/SwiftShader/+/54008
Presubmit-Ready: Alexis Hétu <sugoi@google.com>
Kokoro-Result: kokoro <noreply+kokoro@google.com>
Reviewed-by: Antonio Maiorano <amaiorano@google.com>
Tested-by: Alexis Hétu <sugoi@google.com>
Commit-Queue: Alexis Hétu <sugoi@google.com>

[modify] https://swiftshader.googlesource.com/SwiftShader/+/484a3e15893c769304509bf1607a42f205a7002d/src/Vulkan/VkDeviceMemory.cpp


### gi...@appspot.gserviceaccount.com (2021-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8fb36beb601f99a64dd7c2b6532c6e07c87d0352

commit 8fb36beb601f99a64dd7c2b6532c6e07c87d0352
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Apr 28 20:29:00 2021

Roll SwiftShader from 112faf441539 to 484a3e15893c (1 revision)

https://swiftshader.googlesource.com/SwiftShader.git/+log/112faf441539..484a3e15893c

2021-04-28 sugoi@google.com Silence warning for MacOS

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/swiftshader-chromium-autoroll
Please CC swiftshader-team+autoroll@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_chromium_msan_rel_ng;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1185611
Tbr: swiftshader-team+autoroll@google.com
Change-Id: Iae5dbf2447b9a4399cfd68e6b83f29e9dd963ec2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2856897
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#877206}

[modify] https://crrev.com/8fb36beb601f99a64dd7c2b6532c6e07c87d0352/DEPS


### [Deleted User] (2021-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1185611?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055096)*
