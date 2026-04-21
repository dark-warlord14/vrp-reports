# Security: UAF in Screens::UpdateScreenInfos due to iterator invalidation

| Field | Value |
|-------|-------|
| **Issue ID** | [40056781](https://issues.chromium.org/issues/40056781) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2021-08-04 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

Bug is function `Screens::UpdateScreenInfos()`

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/screen_enumeration/screens.cc;drc=fd7836b1b1e2268550c9239c4d3a55f671332d09;l=60>

```
void Screens::UpdateScreenInfos(LocalDOMWindow\* window,  
                                const display::ScreenInfos& new_infos) {  
  
  ...  
  
  // (5) Send change events to individual screens if they have changed.  
  // It's not guaranteed that screen_infos are ordered, so for each screen  
  // find the info that corresponds to it in old_info and new_infos.  
  for (const auto& screen : screens_) {  
    auto id = screen->DisplayId();  
    auto new_it = base::ranges::find(new_infos.screen_infos, id,  
                                     &display::ScreenInfo::display_id);  
    DCHECK(new_it != new_infos.screen_infos.end());  
    auto old_it = base::ranges::find(prev_screen_infos_.screen_infos, id,  
                                     &display::ScreenInfo::display_id);  
    if (old_it != prev_screen_infos_.screen_infos.end() && \*old_it != \*new_it) {  
      // TODO(enne): http://crbug.com/1202981 only send this event when  
      // properties on ScreenAdvanced (vs anything in ScreenInfo) change.  
      screen->DispatchEvent(\*Event::Create(event_type_names::kChange));			// ===> trigger JS user defined callback  
    }  
  }  
  
  ...  
  

```

`screen->DispatchEvent` can synchronously run a user-defined JavaScript function by setting `change` event of screen object.  

If in JS the function we detach the iframe by using `document.body.removeChild(iframe);`, it will call to funcion `Screens::ContextDestroyed()`

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/screen_enumeration/screens.cc;drc=fd7836b1b1e2268550c9239c4d3a55f671332d09;l=50>

```
void Screens::ContextDestroyed() {  
  screens_.clear();						// ==> clear `screens_` in middle of `for` loop  
}  

```

This will clear the `screens_` and invalidate the iterator used in the range-based for loop. The invalidated iterator will  

cause a use-after-free condition in the next iteration of the loop.

The bug has the same pattern with this issue <https://bugs.chromium.org/p/chromium/issues/detail?id=1108518>

**VERSION**

Chromium 93.0.4542.2

## Timeline

### [Deleted User] (2021-08-04)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-08-04)

Thanks for the report.

Have you been able to produce a PoC for this? Your description makes sense but I wonder if the frame destruction is synchronous with the JS removeChild call.

[Monorail components: UI>Browser>WebAppInstalls]

### cm...@chromium.org (2021-08-05)

Mike, could you PTAL / triage further?

### ms...@google.com (2021-08-06)

This does seem like a potential concern; thanks for the report!
Perhaps HeapVector swapping in https://crrev.com/c/2325499 for https://crbug.com/chromium/1108518 will inspire a fix here.

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-08-06)

[Automated comment] This feature blocker is blocking a channel that is not yet enabled and will no longer be considered a binary push blocker (go/chrome-feature-blockers).

### en...@chromium.org (2021-08-06)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-08-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c7e2656e195fc5ac5122e5377d70e9715aba3655

commit c7e2656e195fc5ac5122e5377d70e9715aba3655
Author: Adrienne Walker <enne@chromium.org>
Date: Fri Aug 06 22:53:08 2021

Window Placement: fix event dispatch loop bug

ContextDestroyed can be called in the middle of looping through
screens to dispatch events to.  Rewrite the for loop to handle this.

Bug: 1236701
Change-Id: I2647fa73c5576caad86eebae6b03c906634d3e0c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3078483
Commit-Queue: enne <enne@chromium.org>
Auto-Submit: enne <enne@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#909527}

[modify] https://crrev.com/c7e2656e195fc5ac5122e5377d70e9715aba3655/third_party/blink/renderer/modules/screen_enumeration/screens.cc


### ke...@chromium.org (2021-08-09)

For the sake of getting security flags right, was the invalid iterator state verified as reachable other than by code inspection?

### en...@chromium.org (2021-08-09)

kenrb: this was just code inspection on my part

### en...@chromium.org (2021-08-09)

Requesting merge on this to M93.  This is an extremely minimal change of an iterator loop to an index loop, so feels very safe to merge as a mitigation for a potential UAF.

### [Deleted User] (2021-08-09)

This bug requires manual review: M93's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2021-08-09)

1. Does your merge fit within the Merge Decision Guidelines?

Mostly? I think one could argue that this is not a high priority security fix because there's no proof of concept here, but it's an extremely safe and small fix.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/3078483

3. Has the change landed and been verified on ToT?

It's had time to bake in a canary over the weekend.  It's an extremely safe change (covered by tests) of switching a single for loop from an iterator to an index.

4. Does this change need to be merged into other active release branches (M-1, M+1)?

No.

5. Why are these changes required in this milestone after branch?

This is a potential use-after-free situation with a very easy fix.

6. Is this a new feature?

No.

7. If it is a new feature, is it behind a flag using finch?

No.

### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-10)

merge approved to M93; please go ahead and merge to branch 4577 asap (by EOD today, 10 August) so this can be a part of the 93 beta release tomorrow. Thank you! 

### gi...@appspot.gserviceaccount.com (2021-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/88f777918ce85da2bad088fa23b101009bdace9a

commit 88f777918ce85da2bad088fa23b101009bdace9a
Author: Adrienne Walker <enne@chromium.org>
Date: Tue Aug 10 22:05:29 2021

Window Placement: fix event dispatch loop bug

ContextDestroyed can be called in the middle of looping through
screens to dispatch events to.  Rewrite the for loop to handle this.

(cherry picked from commit c7e2656e195fc5ac5122e5377d70e9715aba3655)

Bug: 1236701
Change-Id: I2647fa73c5576caad86eebae6b03c906634d3e0c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3078483
Commit-Queue: enne <enne@chromium.org>
Auto-Submit: enne <enne@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#909527}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3086411
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4577@{#688}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/88f777918ce85da2bad088fa23b101009bdace9a/third_party/blink/renderer/modules/screen_enumeration/screens.cc


### am...@google.com (2021-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-19)

Congratulations! The VRP Panel has decided to award you $7500 for this report. Nice work! 

### am...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-11-04)

Labelling as not applicable as the changed file isn't present in M90

### [Deleted User] (2021-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-11-16)

This issue was migrated from crbug.com/chromium/1236701?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1169426, crbug.com/chromium/897300]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056781)*
