# Security: Heap-use-after-free in LocalTabGroupListener::AddWebContents 

| Field | Value |
|-------|-------|
| **Issue ID** | [40063633](https://issues.chromium.org/issues/40063633) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2023-03-17 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1118297.zip and unzip
2. start a http server at the folder of poc.html
3. run `./asan-linux-release-1118297/chrome --user-data-dir=/tmp/noexist --enable-features=TabGroupsSave http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html`
4. add the first tab to TabGroup and then save it. Drag the TabGroup.

**Problem Description:**

1. Analysis

When dragging the whole TabGroup, `SavedTabGroup` will be removed and call `RemoveImpl`[1] to delete the `SavedTabGroup`.

```
std::unique_ptr<SavedTabGroup> SavedTabGroupModel::RemoveImpl(int index) {  
  CHECK_GE(index, 0);  
  std::unique_ptr<SavedTabGroup> removed_group =  
      std::make_unique<SavedTabGroup>(std::move(saved_tab_groups_[index]));  
  saved_tab_groups_.erase(saved_tab_groups_.begin() + index);  
  return removed_group;  
}  

```

However, there is a raw\_ref ptr of `SavedTabGroup` saved in `LocalTabGroupListener`[2], after dragging, `LocalTabGroupListener::AddWebContents`[3] is called and the freed `SavedTabGroup` will be used.

```
void LocalTabGroupListener::AddWebContents(content::WebContents\* web_contents,  
                                           TabStripModel\* tab_strip_model,  
                                           int index) {  
  const absl::optional<int> first_tab_in_group_index_in_tabstrip =  
      tab_strip_model->group_model()  
          ->GetTabGroup(saved_group_->local_group_id().value())  
          ->GetFirstTab();  
  CHECK(first_tab_in_group_index_in_tabstrip.has_value());  
  
  const int relative_index_of_tab_in_group =  
      tab_strip_model->GetIndexOfWebContents(web_contents) -  
      first_tab_in_group_index_in_tabstrip.value();  
  
  base::Token token = base::Token::CreateRandom();  
  
  // Create a new SavedTabGroupTab linked to `token`.  
  SavedTabGroupTab tab =  
      SavedTabGroupUtils::CreateSavedTabGroupTabFromWebContents(  
          web_contents, saved_group_->saved_guid());  
  tab.SetLocalTabID(token);  
  model_->AddTabToGroup(saved_group_->saved_guid(), std::move(tab),  
                        relative_index_of_tab_in_group);  
  
  // Link `web_contents` to `token`.  
  web_contents_to_tab_id_map_.try_emplace(web_contents, web_contents, token,  
                                          model_);  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/saved_tab_groups/saved_tab_group_model.cc;l=488;drc=598cedadf796088adb940c9cf2d0d1c2a1dee813;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/saved_tab_groups/local_tab_group_listener.h;l=47;drc=598cedadf796088adb940c9cf2d0d1c2a1dee813;bpv=0;bpt=0>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/saved_tab_groups/local_tab_group_listener.cc;l=52;drc=598cedadf796088adb940c9cf2d0d1c2a1dee813;bpv=0;bpt=0>

2. Bisect

This problem is introduced in this commit: 598cedadf796088adb940c9cf2d0d1c2a1dee813  

<https://chromium-review.googlesource.com/c/chromium/src/+/4321680>

3. Suggested Patch

Use a weakPtr to enture the lifetime of `SavedTabGroup`.

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 12 B)
- [asan.txt](attachments/asan.txt) (text/plain, 22.7 KB)
- [video.webm](attachments/video.webm) (video/webm, 524.6 KB)

## Timeline

### [Deleted User] (2023-03-17)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-03-17)

Appears to be more trunk churn on a feature behind a flag.

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### dl...@chromium.org (2023-03-17)

@tbergquist - When you get a chance, can you look into this? Thank you!

### ad...@google.com (2023-03-17)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-03-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1ad505b825eb44b1a733f1aedd554f04556266c4

commit 1ad505b825eb44b1a733f1aedd554f04556266c4
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Mon Mar 20 20:22:53 2023

Fix UAF dereferencing a stale SavedTabGroup.

Switches to keeping a local_id and a saved_guid by value, separately, and looking up the SavedTabGroup each time it's accessed.

Bug: 1425339
Change-Id: Iada8b31606094eaf95ed8ebdd3e54322ae85b93f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4351210
Reviewed-by: Darryl James <dljames@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1119556}

[modify] https://crrev.com/1ad505b825eb44b1a733f1aedd554f04556266c4/chrome/browser/ui/tabs/saved_tab_groups/local_tab_group_listener.cc
[modify] https://crrev.com/1ad505b825eb44b1a733f1aedd554f04556266c4/chrome/browser/ui/tabs/saved_tab_groups/local_tab_group_listener.h
[modify] https://crrev.com/1ad505b825eb44b1a733f1aedd554f04556266c4/chrome/browser/ui/tabs/saved_tab_groups/saved_tab_group_model_listener.cc


### [Deleted User] (2023-03-21)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dl...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-29)

Congratulations, Weipeng Jiang! The VRP Panel has decided to award you $4,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Because this bug was reported based on a commit resulting in a newly introduced bug just hours (< 24 hours old) it would ordinarily not be eligible for a VRP reward. This report was of very high quality, resulting in a fairly quick triage and fix, and was an issue that may not have been discovered by a fuzzer or other means, therefore, we have extended an exception and considering this issue as eligible for a reward. 
Thank you for your effort in discovering and reporting this issue -- nice work! 

### me...@gmail.com (2023-03-30)

Thank you!

### [Deleted User] (2023-03-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-30)

Not requesting merge to dev (M113) because latest trunk commit (1119556) appears to be prior to dev branch point (1121455). If this is incorrect, please replace the Merge-NA-113 label with Merge-Request-113. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M113. Please go ahead and merge the CL to branch 5672 (refs/branch-heads/5672) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-30)

Fix landed on M113, no merge needed here 

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-31)

cc'ing xrosado for UI fuzzing knowledge

### pg...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-06)

Hello Krace -- we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), so I've undeleted them. Please refrain from deleting these attachments and other pertinent data from reports -- thank you! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1425339?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063633)*
