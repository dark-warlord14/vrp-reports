# Heap-use-after-free in ui::SendDamagedRectsRecursive

| Field | Value |
|-------|-------|
| **Issue ID** | [40056968](https://issues.chromium.org/issues/40056968) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Compositing |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | sk...@chromium.org |
| **Created** | 2021-08-23 |
| **Bounty** | $16,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6047035357462528

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x609000c2d328
Crash State:
  ui::SendDamagedRectsRecursive
  cc::LayerTreeHost::RequestMainFrameUpdate
  cc::SingleThreadProxy::BeginMainFrame
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=899178:899187

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6047035357462528

Additional requirements: Requires Gestures

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6047035357462528 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2021-08-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-08-23)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Compositing]

### m....@gmail.com (2021-08-23)

#RCA
1. Function SendDamagedRectsRecursive calls itself in an iterator loop AT[1]
2. SendDamagedRectsRecursive will call SendDamagedRects AT[2] which may invaild iterator(look free stack frame) cause UAF.

ps. This seems to be a UAF problem in the browser process,If so, it may cause the sandbox escape.

```
ui/compositor/compositor.cc:655

static void SendDamagedRectsRecursive(ui::Layer* layer) {
  layer->SendDamagedRects();				<<<[2]
  for (auto* child : layer->children())
    SendDamagedRectsRecursive(child);		<<<[1]
}

void Compositor::UpdateLayerTreeHost() {
  if (!root_layer())
    return;
  SendDamagedRectsRecursive(root_layer());
}

```

#Patch
Maybe clone "std::vector<Layer*> children_;" before iteration.



### [Deleted User] (2021-08-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-08-30)

Assigned owner based on Blame, PTAL asap as this issue seemed to go untriaged and unassigned for a week. As it is foundin-93, it's presently considered a potential release blocker for tomorrow's stable channel release. 

### ad...@google.com (2021-08-30)

There's permissions mentioned in the call stack, so I think this is the most likely commit from the regression range:
https://chromium.googlesource.com/chromium/src/+/df283b07c23c49214afe36e7db83b31269c4b4da



### [Deleted User] (2021-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-01)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-01)

@bsep  I've checked the crash log and I'm lacking an understanding of what is happening and how it is connected to our chip-related work. If it is unclear for you as well, who would be the best person to talk to?

### el...@chromium.org (2021-09-01)

[Empty comment from Monorail migration]

### bs...@chromium.org (2021-09-01)

#11: I can't see the full stack trace as I'm not the owner of the bug. I would ask maybe sky@ if it's related to damage (i.e. SendDamagedRectsRecursive) or someone from cc/OWNERS if it's a compositor issue.

### cl...@chromium.org (2021-09-01)

ClusterFuzz testcase 6047035357462528 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=917149:917151

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### en...@chromium.org (2021-09-01)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-02)

@sky and @enne: The crash is not reproducible and I'm lacking understanding of what is happening. Please check or suggest who I can talk to regarding the SendDamagedRectsRecursive();

Please use your chromium account to see the crash log.

### sk...@chromium.org (2021-09-02)

I see what the issue is. I'll take it.

### gi...@appspot.gserviceaccount.com (2021-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7c0b0577c3ac1060945b7d05ad69f0dec33479b4

commit 7c0b0577c3ac1060945b7d05ad69f0dec33479b4
Author: Scott Violet <sky@chromium.org>
Date: Thu Sep 02 23:53:44 2021

compositor: fix bug in sending damage regions

Specifically if a layer is added when sending damaged regions the
iterator would be invalidated. This converts to iterating over the
size.

BUG=1242257
TEST=CompositorTestWithMessageLoop.AddLayerDuringUpdateVisualState

Change-Id: I09f2bd34afce5d3c9402ef470f14923bbc76b8ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140178
Reviewed-by: Ian Vollick <vollick@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#917886}

[modify] https://crrev.com/7c0b0577c3ac1060945b7d05ad69f0dec33479b4/ui/compositor/compositor.cc
[modify] https://crrev.com/7c0b0577c3ac1060945b7d05ad69f0dec33479b4/ui/compositor/compositor_unittest.cc


### sk...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-09-03)

Thanks for the quick fix!

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

Requesting merge to stable M93 because latest trunk commit (917886) appears to be after stable branch point (902210).

Requesting merge to beta M94 because latest trunk commit (917886) appears to be after beta branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-04)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2021-09-07)

1. Does your merge fit within the Merge Decision Guidelines?

Possible security bug.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/3140178

3. Has the change landed and been verified on ToT?

Yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?

Possibly 93.

5. Why are these changes required in this milestone after branch?

Bug only recently reported.

6. Is this a new feature?

Probably always possible, but perhaps new feature made it easier to trigger.

7. If it is a new feature, is it behind a flag using finch?

### sr...@google.com (2021-09-07)

Merge approved for M94 branch:4606 please merge before 3pm PST today so this can go out in tomorrow beta release

### sr...@google.com (2021-09-07)

re-opening to get engineer's attention

### gi...@appspot.gserviceaccount.com (2021-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/091d66b700aec94848927f46b7a5a4465d62ac16

commit 091d66b700aec94848927f46b7a5a4465d62ac16
Author: Scott Violet <sky@chromium.org>
Date: Tue Sep 07 21:48:36 2021

[M94 merge] compositor: fix bug in sending damage regions

Specifically if a layer is added when sending damaged regions the
iterator would be invalidated. This converts to iterating over the
size.

BUG=1242257
TEST=CompositorTestWithMessageLoop.AddLayerDuringUpdateVisualState

(cherry picked from commit 7c0b0577c3ac1060945b7d05ad69f0dec33479b4)

Change-Id: I09f2bd34afce5d3c9402ef470f14923bbc76b8ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140178
Reviewed-by: Ian Vollick <vollick@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917886}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3144277
Auto-Submit: Scott Violet <sky@chromium.org>
Commit-Queue: enne <enne@chromium.org>
Reviewed-by: enne <enne@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#842}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/091d66b700aec94848927f46b7a5a4465d62ac16/ui/compositor/compositor.cc
[modify] https://crrev.com/091d66b700aec94848927f46b7a5a4465d62ac16/ui/compositor/compositor_unittest.cc


### sk...@chromium.org (2021-09-08)

Moving to fixed to get this off the radar.

### am...@chromium.org (2021-09-08)

Merge approved for M93; please merge to branch 4577 by 2pm PDT Thursday, 9 September so this fix can be included in next week's stable channel security refresh. thank you. 

### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6215793f008fdf98124e695eca738c05db3f13b0

commit 6215793f008fdf98124e695eca738c05db3f13b0
Author: Scott Violet <sky@chromium.org>
Date: Wed Sep 08 18:45:42 2021

[M93 merge] compositor: fix bug in sending damage regions

Specifically if a layer is added when sending damaged regions the
iterator would be invalidated. This converts to iterating over the
size.

BUG=1242257
TEST=CompositorTestWithMessageLoop.AddLayerDuringUpdateVisualState

(cherry picked from commit 7c0b0577c3ac1060945b7d05ad69f0dec33479b4)

Change-Id: I09f2bd34afce5d3c9402ef470f14923bbc76b8ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140178
Reviewed-by: Ian Vollick <vollick@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917886}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3149110
Commit-Queue: enne <enne@chromium.org>
Auto-Submit: Scott Violet <sky@chromium.org>
Reviewed-by: enne <enne@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#1206}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/6215793f008fdf98124e695eca738c05db3f13b0/ui/compositor/compositor.cc
[modify] https://crrev.com/6215793f008fdf98124e695eca738c05db3f13b0/ui/compositor/compositor_unittest.cc


### am...@google.com (2021-09-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-08)

Congratulations - the VRP Panel has decided to award you $15,000 for this report + $1,000 fuzzer bonus. Thank you for your contributions to Chrome Fuzzing! 

### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-14)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-14)

[Empty comment from Monorail migration]

### gi...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/30b6e9bf0a7cfe35ffa70c3377f25cbf13fd158e

commit 30b6e9bf0a7cfe35ffa70c3377f25cbf13fd158e
Author: Scott Violet <sky@chromium.org>
Date: Thu Sep 16 11:34:12 2021

[M90-LTS] compositor: fix bug in sending damage regions

Specifically if a layer is added when sending damaged regions the
iterator would be invalidated. This converts to iterating over the
size.

BUG=1242257
TEST=CompositorTestWithMessageLoop.AddLayerDuringUpdateVisualState

(cherry picked from commit 7c0b0577c3ac1060945b7d05ad69f0dec33479b4)

Change-Id: I09f2bd34afce5d3c9402ef470f14923bbc76b8ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140178
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917886}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3160208
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1607}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/30b6e9bf0a7cfe35ffa70c3377f25cbf13fd158e/ui/compositor/compositor.cc
[modify] https://crrev.com/30b6e9bf0a7cfe35ffa70c3377f25cbf13fd158e/ui/compositor/compositor_unittest.cc


### vo...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1242257?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056968)*
