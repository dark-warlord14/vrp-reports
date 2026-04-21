# Chrome's Reading Mode UAF

| Field | Value |
|-------|-------|
| **Issue ID** | [40073847](https://issues.chromium.org/issues/40073847) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility |
| **Platforms** | Mac |
| **Reporter** | no...@ssd-disclosure.com |
| **Assignee** | jo...@google.com |
| **Created** | 2023-10-01 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

### REPRODUCTION CASE

Use After Free occurs when a page is loaded by directly typing [chrome-untrusted://read-anything-side-panel.top-chrome/](javascript:void(0);) in the address bar of the tab and then moving to another page.

**Problem Description:**

### ROOT CAUSE ANALYSIS

#### Free

```
void RenderFrameImpl::FrameDetached() {  
  // We need to clean up subframes by removing them from the map and deleting  
  // the RenderFrameImpl.  In contrast, the main frame is owned by its  
  // containing RenderViewHost (so that they have the same lifetime), so only  
  // removal from the map is needed and no deletion.  
  auto it = g_frame_map.Get().find(frame_);  
  CHECK(it != g_frame_map.Get().end());  
  CHECK_EQ(it->second, this);  
  g_frame_map.Get().erase(it);  
  
  // RenderAccessibilityManager keeps a reference to the RenderFrame that owns  
  // it, so we need to clear the pointer to prevent invalid access after the  
  // frame gets closed and deleted.  
  render_accessibility_manager_.reset();  
  
  // |frame_| may not be referenced after this, so clear the pointer since  
  // the actual WebLocalFrame may not be deleted immediately and other methods  
  // may try to access it.  
  frame_->Close();  
  frame_ = nullptr;  
  
  if (mhtml_body_loader_client_) {  
    mhtml_body_loader_client_->Detach();  
    mhtml_body_loader_client_.reset();  
  }  
  
  delete this; // [0]  
  // Object is invalid after this point.  
}  

```

[0] Free `RenderFrame` object of the Reading Mode page while navigating from tab to other pages.

#### Use

```
void ReadAnythingAppController::OnActiveAXTreeIDChanged(  
    const ui::AXTreeID& tree_id,  
    ukm::SourceId ukm_source_id,  
    const GURL& url) {  
  if (tree_id == model_.active_tree_id()) {  
    return;  
  }  
  ui::AXTreeID previous_active_tree_id = model_.active_tree_id();  
  model_.SetActiveTreeId(tree_id);  
  model_.SetActiveUkmSourceId(ukm_source_id);  
  model_.SetActiveTreeSelectable(GetSelectable(url));  
  // Delete all pending updates on the formerly active AXTree.  
  // TODO(crbug.com/1266555): If distillation is in progress, cancel the  
  // distillation request.  
  model_.ClearPendingUpdates();  
  model_.set_requires_distillation(false);  
  
  // TODO(b/1266555): Use v8::Function rather than javascript. If possible,  
  // replace this function call with firing an event.  
  std::string script = "chrome.readingMode.showLoading();";  
  render_frame_->ExecuteJavaScript(base::ASCIIToUTF16(script)); // [1]  
  
  // When the UI first constructs, this function may be called before tree_id  
  // has been added to the tree list in AccessibilityEventReceived. In that  
  // case, do not distill.  
  if (model_.active_tree_id() != ui::AXTreeIDUnknown() &&  
      model_.ContainsTree(model_.active_tree_id())) {  
    Distill();  
  }  
}  

```

By moving to another page, the information of the `AXTree` is changed and the above function is called.

[1] UAF occurs while accessing the already freed `RenderFrame` object.

### RECOMMENDED PATCH

```
--- a/renderer/accessibility/read_anything_app_controller.cc  
+++ b/renderer/accessibility/read_anything_app_controller2.cc  
@@ -427,6 +427,7 @@  
   // TODO(b/1266555): Use v8::Function rather than javascript. If possible,  
   // replace this function call with firing an event.  
   std::string script = "chrome.readingMode.showLoading();";  
+  CHECK(render_frame_);  
   render_frame_->ExecuteJavaScript(base::ASCIIToUTF16(script));  
   
   // When the UI first constructs, this function may be called before tree_id  
\ No newline at end of file  

```

---

The above WebUI component can be accessed immediately by the user using the Reading Modefeature.

Later, when the user clicks the Anchor tag in Reading Mode, the attacker can perform malicious actions such as triggering the above vulnerability via Javascript.

Therefore, it seems imporant to solve fundamental vulnerabilities to prevent this.

---

### VERSION

\* Chrome Version: 118.0.5961.0 (Developer Build) (x86\_64), Also Stable.  

\* Operating System: macOS Ventura 13.4.1 (22F770820d)

### CREDIT

parkminchan, working for SSD Labs Korea.

**Additional Comments:**

\*\*Chrome version: \*\* 118.0.5961.0 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 29.0 KB)
- [readme.md](attachments/readme.md) (text/plain, 4.1 KB)
- [proof-reduced.mp4](attachments/proof-reduced.mp4) (video/mp4, 2.3 MB)

## Timeline

### [Deleted User] (2023-10-01)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-10-01)

Thank you for the report!

Hi kristislee@google.com , would you be able to help triage this issue? I see that you have made changes to the file chrome/renderer/accessibility/read_anything_app_controller.cc before which the bug refers to. Thanks!

[Monorail components: UI>Accessibility]

### [Deleted User] (2023-10-01)

[Empty comment from Monorail migration]

### kr...@google.com (2023-10-02)

[Empty comment from Monorail migration]

### kr...@google.com (2023-10-02)

Jocelyn, can you take a look?

### [Deleted User] (2023-10-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-02)

[Empty comment from Monorail migration]

### jo...@google.com (2023-10-02)

Hi parkminchan, thank you for finding this. 

Could you please clarify what you mean by "moving to another page" in the reproduction steps? I tried opening chrome-untrusted://read-anything-side-panel.top-chrome/ in the address bar and then opening another webpage in the same tab. And I also tried opening a new tab and navigating to another webpage in that new tab instead. I was not able to reproduce the UAF in either case.

### jo...@google.com (2023-10-02)

[Empty comment from Monorail migration]

### no...@ssd-disclosure.com (2023-10-03)

Adding a "movie"

### gi...@appspot.gserviceaccount.com (2023-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/30c81dd6746a82c8b8020bbcd3dc0ab50b8b81e5

commit 30c81dd6746a82c8b8020bbcd3dc0ab50b8b81e5
Author: Jocelyn Tran <jocelyntran@google.com>
Date: Wed Oct 04 18:16:07 2023

[Read Anything] Fix render frame uaf

Fixed: 1488268
Change-Id: I5b480f261335dab374b606c3a2672dd05c715100
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4908587
Reviewed-by: Abigail Klein <abigailbklein@google.com>
Commit-Queue: Jocelyn Tran <jocelyntran@google.com>
Cr-Commit-Position: refs/heads/main@{#1205343}

[modify] https://crrev.com/30c81dd6746a82c8b8020bbcd3dc0ab50b8b81e5/chrome/renderer/accessibility/read_anything_app_controller.h
[modify] https://crrev.com/30c81dd6746a82c8b8020bbcd3dc0ab50b8b81e5/chrome/renderer/accessibility/read_anything_app_controller.cc


### [Deleted User] (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-05)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M118, which branched on 2023-09-05 (Chromium branch: 5993, Chromium branch position: 1192594)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-05)

Merge approved: your change passed merge requirements and is auto-approved for M119. Please go ahead and merge the CL to branch 6045 (refs/branch-heads/6045) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-05)

Merge review required: M118 has already been cut for stable release.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2023-10-05)

1. Fix for medium severity security issue
2. https://chromium-review.googlesource.com/c/chromium/src/+/4908587
3. Yes, released on Canary 120.0.6048.0
4. Yes, this is for a new feature. It's not behind a finch flag and experiments are active.

### gi...@appspot.gserviceaccount.com (2023-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fe3bf96259da9bac6d0d809966002baea988face

commit fe3bf96259da9bac6d0d809966002baea988face
Author: Jocelyn Tran <jocelyntran@google.com>
Date: Fri Oct 06 16:44:54 2023

[Merge M119] [Read Anything] Fix render frame uaf

(cherry picked from commit 30c81dd6746a82c8b8020bbcd3dc0ab50b8b81e5)

Fixed: 1488268
Bug: 1488268
Change-Id: I5b480f261335dab374b606c3a2672dd05c715100
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4908587
Reviewed-by: Abigail Klein <abigailbklein@google.com>
Commit-Queue: Jocelyn Tran <jocelyntran@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1205343}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4916396
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6045@{#125}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/fe3bf96259da9bac6d0d809966002baea988face/chrome/renderer/accessibility/read_anything_app_controller.h
[modify] https://crrev.com/fe3bf96259da9bac6d0d809966002baea988face/chrome/renderer/accessibility/read_anything_app_controller.cc


### am...@chromium.org (2023-10-09)

118 merge approved, please merge this fix to branch 5993 at your earliest convenience so this fix can be included in the next M118 Stable update 

### gi...@appspot.gserviceaccount.com (2023-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/86f0cf0295bc1dc3d9877afb7949e1ecbda8a85d

commit 86f0cf0295bc1dc3d9877afb7949e1ecbda8a85d
Author: Jocelyn Tran <jocelyntran@google.com>
Date: Mon Oct 09 21:02:55 2023

[Merge M118][Read Anything] Fix render frame uaf

(cherry picked from commit 30c81dd6746a82c8b8020bbcd3dc0ab50b8b81e5)

Fixed: 1488268
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4908587
Reviewed-by: Abigail Klein <abigailbklein@google.com>
Commit-Queue: Jocelyn Tran <jocelyntran@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1205343}
Change-Id: I040637963a4b7f0736cad228f72092fba5e5b0ce
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4922809
Owners-Override: Daniel Yip <danielyip@google.com>
Reviewed-by: Jocelyn Tran <jocelyntran@google.com>
Cr-Commit-Position: refs/branch-heads/5993@{#1221}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/86f0cf0295bc1dc3d9877afb7949e1ecbda8a85d/chrome/renderer/accessibility/read_anything_app_controller.h
[modify] https://crrev.com/86f0cf0295bc1dc3d9877afb7949e1ecbda8a85d/chrome/renderer/accessibility/read_anything_app_controller.cc


### am...@google.com (2023-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-11)

Congratulations parkminchan! The Chrome VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug. The reward amount was decided upon based on this issue not being remote exploitable and the user interaction required to trigger this issue. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### sr...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-10)

This issue was migrated from crbug.com/chromium/1488268?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ni...@google.com (2024-05-28)

marking verrified per comment 26

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073847)*
