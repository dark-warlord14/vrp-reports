# Crash in SkArenaAllocWithReset::reset

| Field | Value |
|-------|-------|
| **Issue ID** | [40058054](https://issues.chromium.org/issues/40058054) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mi...@google.com |
| **Created** | 2021-11-28 |
| **Bounty** | $5,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5684140533678080

Fuzzer: jesse_avalanche
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: UNKNOWN READ
Crash Address: 0x0005d90be808
Crash State:
  SkArenaAllocWithReset::reset
  GrOpFlushState::reset
  GrDrawingManager::executeRenderTasks
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=943236:943259

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5684140533678080

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5684140533678080 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2021-11-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-28)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Skia]

### [Deleted User] (2021-11-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-12-07)

Hi, ClusterFuzz has spotted a bug where the repro case appears to involve a massively large line width.

CF has identified four possibly relevant Skia commits. One of them is https://skia.googlesource.com/skia/+/32071c3f14a74c35c042804a359b2703014a53e5, so perhaps you could verify if this commit introduced the problem, and if not, pass it on appropriately? Thanks!

### ad...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-12)

csmartdalton: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-12-13)

[Empty comment from Monorail migration]

### bs...@google.com (2021-12-13)

Chris is on leave. Sending this over to the weekly Skia GPU gardener.

### jv...@google.com (2021-12-14)

[Empty comment from Monorail migration]

### jv...@google.com (2021-12-15)

Update: I have not been able to reproduce this. The reproduce.sh script doesn't run well on MacOS (after a long set of brew installs it's failing with some python setup), and running Chromium directly with the given gn args, ASAN_OPTIONS, and runtime flags doesn't duplicate it. I tried to duplicate the webpage and run it in Skia with ASAN and still no issues.

Reverting either of the candidate CLs doesn't seem wise, as they fix another Clusterfuzz issue.



### jv...@google.com (2021-12-16)

Reassigning to next week's GPU Gardener, as I'm on leave.

### mi...@google.com (2021-12-20)

I have made some progress debugging this.

I can reproduce on linux if I manually enable oop-canvas. This appears to be a path made from 4 cubics and very large magnitude control point coordinates, and a very large stroke width (33 million-ish).  After the identified "cause" CLs, the stroke path renderer no longer accepts the path as-is (removing them actually causes a stack-overflow in chopping, so this bug would have triggered the same issue that the fuzzer bugs that Jim mentioned in c11).  However, since it isn't accepted as-is, we use the CPU stroker to turn it into a filled path with about 10,000 verbs and very large bounds.  

This filled path is acceptable to the filled tessellation renderer in the same family of HW tessellating renderers, albeit that renderer "pre-chops" the path to meet the fixed tessellation requirements. This produces a path with about 40k verbs in it. With the current logic in renderer sub-selection, it estimates that the cpu work of triangulating the inner control points outweighs the gpu fragment work (possibly a bug because it uses the unclipped draw bounds, which are massively larger than the viewport's actual fragment work).  Using the inner triangulating path renderer + stenciling just the curves appears to lead to memory corruption in the flush state's arena, so that when it's reset it accesses an invalid destructor function pointer.

Tweaking the sub-selection choice to stencil the entire path and not just its curves allows it to render successfully.  I believe there are several underlying issues:
1. The cpu work vs. gpu work function needs work -> should it be based on the clipped draw bounds? should gpu work also be based on the number of verbs?
2. Is it the number of stencil curve ops that corrupts the arena?
3. Or is it the triangulation of such a large path that corrupts the arena?

Regardless of #1, we should be able to choose the inner triangulating path renderer and not corrupt the flush state arena, that suggests a memory over-run somewhere. I'm going to try and investigate #2/3 a little bit, but worst case, given RBS we can disable the inner triangulation and just rely on the stencil+cover op to avoid this particular crash in the short term.

### mi...@google.com (2021-12-22)

Recording more investigation progress:
1. Having the inner triangulator use its own arena separate from the flush state arena does not seem to have memory corruption
2. Having the inner triangulator skip recording bread crumb triangles lets it complete without crashing
3. Drawing the GPU tessellated hulls does not seem to affect the crash, it is coupled with the GrInnerTriangulator's use of the arena
4. The specific corruption is in a footer of an allocated object in the arena. The footers track per-allocation destructors, skip over POD, or form the linked list between blocks of byte arrays. Specifically, it stores a function pointer and that appears to be corrupted with a value that points to high address space. I confirmed that such an address was never written into the arena.
5. Using manual ASAN poisoning has not uncovered where the corruption originated from, unfortunately. The SkArenaAlloc uses unaligned memory to pack the footers as tightly as possible, so simply marking and unmarking those ranges may not actually let asan detect failures. This is because asan uses 8-byte aligned shadow memory for tracking, so detectable poison ranges need to be 8 byte aligned.
    - Running the fuzz test case with this modification crashes as before.
6. Modifying SkArenaAlloc so that every allocation is at least 8 byte aligned and all footer data fits into 8 byte aligned region bypasses the corruption
    - Running the fuzz test case with this modification seems to avoid or hide the underlying issue so there's no crash at all.
7. The arena gets very large, up to about 10GB in total storage, but the largest blocks are still valid sizes (just over 4GB, such that their size/offsets/etc. fit into the uint32_t limits imposed by SkArenaAlloc so we don't seem to be running into overflow issues).
8. The specific geometry of the path being processed is a pathological case for triggering self intersections, which leads to a huge number of "breadcrumb" triangles needing to be created by the GrInnerTriangulator. It's not obvious to me if it's an issue with the breadcrumb triangle list data type being stored in the arena, the quantity of breadcrumbs, or some other fluke.
9. The triangulator's code that deals with the self intersections makes reproducing this in Skia or ASAN directly somewhat tricky. On Windows debug builds, the collinear edge detection hits a stack overflow before it can resolve all the self intersections (there are 10s of thousands to do, which turns into a very deep stack...).  On linux debug builds, it can complete successfully in skia without crashing although it does consum 10GB of data (and no asserts were tripped). Switching to linux+asan for skia directly re-encounters the stack limit issue so we never get to the resetting of the arena that crashes in chrome.  It would seem that chrome's asan build has a higher stack limit than the skia asan build, so if we can figure out how to adjust that, maybe we can debug more easily.
   - that being said, this does repro in content_shell with --single-process and --in-process-gpu so it's not so far off something that be wired to a debugger easily.

At this point, I think I'm going to apply option #1 from c13 to avoid the pathological case for the triangulator and avoid the crash.

### mi...@google.com (2021-12-23)

I've been able to identify the cause, and it was an int overflow in the SkArenaAlloc:
1. The arena stores cleanup actions in unaligned footers after allocations that need it. These handle invoking destructors for non-POD types, as well as deleting the blocks of arena data as well.
2. Starting with the last recorded footer location, each previous footer location can be reconstructed based on its associated allocation size.
3. There is a special "skip" footer that is recorded when switching from a POD allocation to a non-POD allocation, since POD types do not have any footer at all.
4. This skip is recorded as a uint32_t offset from the current cursor in the arena to the previous real footer so that the implicit linked list of footer locations is maintained.
5. I hacked up SkArenaAlloc to also explicitly store all footer locations and detect if the data was corrupted after allocations, which it was not. I was also able to compare the expected sequence of footer locations from the explicit list and implicit embedded list during the destructor of the arena, and that identified an inconsistency.
6. Because the inner triangulator required a substantial amount of breadcrumb triangles, which were POD types, the arena ended up allocating greater than int32::max of POD. Since this was recorded in the flush state arena, subsequent ops and programs were allocated as well, but these were nonPOD so a skip had to be recorded with a value greater than int32::max.
7. The skip is written as uint32_t, but in the SkipPOD footer action it was being read back into a plain int32_t and then overflowed. This caused the next footer location to be at a completely wrong address, meaning the footer action function pointer that it read was entirely arbitrary (ending up being something with high bits and trapped by ASAN).

On the one hand, this is serious, since it leads to invoking a function pointer read from incorrect memory location. On the other hand, it's only encountered if the arena allocates POD > 2gb in a row, followed by non-POD data.  The regular triangulating path renderer and the inner triangulating variant of the tessellation path renderer are the most capable of this, since they can consume lots of memory when analyzing pathological paths, but in practice, those paths will likely cause OOM, stack overflow, or the triangulator will detect an edge explosion and just stop.  Given that, I think it'd be pretty difficult to apply on a non-ASAN build, certainly was the case when debugging at least...

The fix for the arena is here: https://skia-review.googlesource.com/c/skia/+/488527 and I confirmed that it renders successfully without crashing. While that fixes the crash, it does still lead to a canvas2d draw operation requiring multiple gigs of ram to render, so https://skia-review.googlesource.com/c/skia/+/488528 adds the heuristic change to the tessellating path renderer to use the non-triangulating variant that is much faster for this path case.

### mi...@google.com (2021-12-23)

Going back to the scenarios from c14 and the results of c15, the reason that using a separate arena to store the triangulator's vertices and breadcrumbs never crashed was because it ended up only storing POD. Even though the recorded POD data would have been sufficiently large to create a bad skip footer, there were no subsequent non-POD allocations to trigger that. The non-POD allocations all remained in the flush state arena, which never had that degree of POD data allocated in one block.

### gi...@appspot.gserviceaccount.com (2021-12-23)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/c2b31fb04a80bfcc9125ce9184c4d7808f72a5d6

commit c2b31fb04a80bfcc9125ce9184c4d7808f72a5d6
Author: Michael Ludwig <michaelludwig@google.com>
Date: Thu Dec 23 19:51:43 2021

Use unsigned int to track POD skip

Bug: chromium:1274323
Change-Id: I5d2a25c381ddfa21e56b630139fa61a0bdd8d4e0
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/488527
Reviewed-by: Kevin Lubick <kjlubick@google.com>
Commit-Queue: Michael Ludwig <michaelludwig@google.com>

[modify] https://crrev.com/c2b31fb04a80bfcc9125ce9184c4d7808f72a5d6/src/core/SkArenaAlloc.cpp


### kj...@chromium.org (2021-12-23)

Looks like we'll need to cherry-pick at least back to M98?

### kj...@chromium.org (2021-12-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0cb469f0f8ddc1870fbe0dc4981a138f4c608fb3

commit 0cb469f0f8ddc1870fbe0dc4981a138f4c608fb3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 23 23:10:08 2021

Roll Skia from a7cb849eca4e to c2b31fb04a80 (1 revision)

https://skia.googlesource.com/skia.git/+log/a7cb849eca4e..c2b31fb04a80

2021-12-23 michaelludwig@google.com Use unsigned int to track POD skip

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC egdaniel@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Cq-Do-Not-Cancel-Tryjobs: true
Bug: chromium:1274323
Tbr: egdaniel@google.com
Change-Id: I37e83013980bf6c9d2243399e391dd99eaf16533
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3355366
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#953956}

[modify] https://crrev.com/0cb469f0f8ddc1870fbe0dc4981a138f4c608fb3/DEPS


### mi...@google.com (2021-12-24)

Fixed, waiting on security assessment for merge request. The code with the bug has been around since 2017, it just wasn't tickled until now, so we may also want to cherry pick to m97 since it's having a stable cut soon as well.

### cl...@chromium.org (2021-12-24)

ClusterFuzz testcase 5684140533678080 is verified as fixed in https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=953950:953959

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-12-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-24)

Requesting merge to dev M98 because latest trunk commit (953956) appears to be after dev branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-24)

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mi...@google.com (2021-12-26)

1. It is marked RBS, and is marked medium severity security bug - can read incorrect memory and treat as a function pointer that is executed
2. https://skia-review.googlesource.com/c/skia/+/488529
3. Yes, and verified by fuzzer
4. No
5. N/A
6. No

### am...@chromium.org (2021-12-27)

approved for merge to M98, please merge to branch 4758 at your earliest availability -- thank you

### gi...@appspot.gserviceaccount.com (2021-12-28)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/1beb36334931f6a5b55a8576d73120d38f92d1a8

commit 1beb36334931f6a5b55a8576d73120d38f92d1a8
Author: Michael Ludwig <michaelludwig@google.com>
Date: Thu Dec 23 19:51:43 2021

Use unsigned int to track POD skip

Bug: chromium:1274323
Change-Id: I5d2a25c381ddfa21e56b630139fa61a0bdd8d4e0
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/488527
Reviewed-by: Kevin Lubick <kjlubick@google.com>
Commit-Queue: Michael Ludwig <michaelludwig@google.com>
(cherry picked from commit c2b31fb04a80bfcc9125ce9184c4d7808f72a5d6)
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/488529
Reviewed-by: Brian Salomon <bsalomon@google.com>
Commit-Queue: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/1beb36334931f6a5b55a8576d73120d38f92d1a8/src/core/SkArenaAlloc.cpp


### mi...@google.com (2021-12-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-04)

Congratulations! The VRP Panel has decided to award you $5000 for this report from your fuzzer + $1,000 fuzzer bonus. Thank you for your contributions to Chrome Fuzzing! 

### am...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1274323?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058054)*
