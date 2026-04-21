# heap-use-after-free ui/views/view.cc:1898:7 in views::View::HandleAccessibleAction

| Field | Value |
|-------|-------|
| **Issue ID** | [40060647](https://issues.chromium.org/issues/40060647) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility, UI>Accessibility>Compatibility |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2022-08-22 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. Enable touch screen & chromevox
2. Open NTP
3. alt+tab then double click on views (please refer to screencast)

**Problem Description:**  

This heap UaF occurs when chromevox is enabled. Holding alt+tab then releasing the onEvent state get freed and then re-pick the views triggers UaF.

```
bool View::HandleAccessibleAction(const ui::AXActionData& action_data) {  
  switch (action_data.action) {  
    case ax::mojom::Action::kBlur:  
      if (HasFocus()) {  
        GetFocusManager()->ClearFocus();  
        return true;  
      }  
      break;  
    case ax::mojom::Action::kDoDefault: {  
      const gfx::Point center = GetLocalBounds().CenterPoint();  
      ui::MouseEvent press(ui::ET_MOUSE_PRESSED, center, center,  
                           ui::EventTimeForNow(), ui::EF_LEFT_MOUSE_BUTTON,  
                           ui::EF_LEFT_MOUSE_BUTTON);  
      OnEvent(&press);  
      ui::MouseEvent release(ui::ET_MOUSE_RELEASED, center, center,  
                             ui::EventTimeForNow(), ui::EF_LEFT_MOUSE_BUTTON,  
                             ui::EF_LEFT_MOUSE_BUTTON);  
      OnEvent(&release); <------[1]  
      return true;  
    }  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/view.cc;l=1881-1900?q=ui%2Fviews%2Fview.cc&ss=chromium%2Fchromium%2Fsrc>

**Additional Comments:**  

This UaF probably affect into stable channel. Tested following version, lower than 107.0.5252.0

Chromium 106.0.5210.0 -- r1029999 -- can reproduce  

Chromium 105.0.5154.0 -- r1020005 -- can reproduce  

Chromium 104.0.5099.0 -- r1010000 -- can reproduce

\*\*Chrome version: \*\* 107.0.5252.0 \*\*Channel: \*\* Dev

**OS:** Chrome OS

## Attachments

- [chromevox_onEvent_uaf.log](attachments/chromevox_onEvent_uaf.log) (text/plain, 18.0 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [1355560-M109.log](attachments/1355560-M109.log) (text/plain, 18.8 KB)

## Timeline

### [Deleted User] (2022-08-22)

[Empty comment from Monorail migration]

### lz...@google.com (2022-08-22)

[Empty comment from Monorail migration]

[Monorail components: UI>Accessibility UI>Accessibility>Compatibility]

### [Deleted User] (2022-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-08-30)

friendly ping, anyone can help me with this issue?

### ro...@chromium.org (2022-08-30)

Routing to dtseng@ for a11y triage.

### [Deleted User] (2022-09-07)

dtseng: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@gmail.com (2022-09-07)

friendly ping: any chance to get an simple update? or next action reminder for this issue?

### gi...@appspot.gserviceaccount.com (2022-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/82eb0c8e83f8dc133cbd348361a3cf09d115cde4

commit 82eb0c8e83f8dc133cbd348361a3cf09d115cde4
Author: David Tseng <dtseng@google.com>
Date: Wed Sep 14 23:42:08 2022

Instrument View::~View to ascertain recreation of AXViewObjWrapper

This change adds additional nuance to View::Lifecycle, makes it public,
and uses it to DCHECK calls to AXAuraObjCache::GetOrCreate.

Specifically, accessibility never expects GetOrCreate on a view which is
destroying or destroyed.

The change also adds an early return to GetOrCreate, if the view is
detached. This occurs in ~View, when the view is removed as a child of
its parent.

Thus, the added DCHECK in AXAuraObjCache::GetOrCreate triggers narrowly
for any codepaths from the start of ~View up to almost all of
parent_->RemoveChildView(this) where view's parent_ is nullified in
DoRemoveChildView.

Bug: 1355560
Change-Id: If8817f88b90a0633898d6a6e073b85ab91fbbe26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3868127
Reviewed-by: Robert Liao <robliao@chromium.org>
Commit-Queue: David Tseng <dtseng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1047200}

[modify] https://crrev.com/82eb0c8e83f8dc133cbd348361a3cf09d115cde4/ui/views/view.cc
[modify] https://crrev.com/82eb0c8e83f8dc133cbd348361a3cf09d115cde4/ui/views/accessibility/ax_aura_obj_cache_unittest.cc
[modify] https://crrev.com/82eb0c8e83f8dc133cbd348361a3cf09d115cde4/ui/views/accessibility/ax_aura_obj_cache.cc
[modify] https://crrev.com/82eb0c8e83f8dc133cbd348361a3cf09d115cde4/ui/views/accessibility/ax_widget_obj_wrapper.cc
[modify] https://crrev.com/82eb0c8e83f8dc133cbd348361a3cf09d115cde4/ui/views/view.h
[modify] https://crrev.com/82eb0c8e83f8dc133cbd348361a3cf09d115cde4/ui/views/accessibility/ax_widget_obj_wrapper.h


### rh...@gmail.com (2022-09-20)

dtseng@, thanks for fixing this issue. I've tested on latest linux-chromeOS and see no longer crash. 

### [Deleted User] (2022-09-22)

dtseng: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@gmail.com (2022-09-26)

Hello,

Can this issue mark as fixed based on https://crbug.com/chromium/1355560#c12?

Thanks

### am...@chromium.org (2022-09-28)

Updating as Fixed based on fix CL and https://crbug.com/chromium/1355560#c12 verification of fix

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug. Thank you for efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### dt...@chromium.org (2022-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-24)

Merge review required: M107 has already been cut for stable release.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-10-24)

[Comment Deleted]

### rh...@gmail.com (2022-10-24)

Hello,

I think the CL on https://crbug.com/chromium/1355560#c11 is not complete to fix UaF. I see there still UaF exist on M109. Please refer to the screencast

### rh...@gmail.com (2022-10-24)

uploaded asan log

### rh...@gmail.com (2022-10-26)

[Comment Deleted]

### rh...@gmail.com (2022-10-26)

deleted https://crbug.com/chromium/1355560#c27, the UaF still exists on latest chromium dev.

### am...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1355560?no_tracker_redirect=1

[Multiple monorail components: UI>Accessibility, UI>Accessibility>Compatibility]
[Monorail components added to Component Tags custom field.]

### ni...@google.com (2024-06-18)

marking verified per comment 19

### ni...@google.com (2024-06-18)

Marking verified per comment 20

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060647)*
