# Security: Heap-use-after-free in SearchCompanionSidePanelCoordinator::CreateCompanionEntry

| Field | Value |
|-------|-------|
| **Issue ID** | [40064189](https://issues.chromium.org/issues/40064189) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>SidePanel |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | co...@chromium.org |
| **Created** | 2023-04-24 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1134408.zip and unzip
2. run `./chrome --user-data-dir=/tmp/noexist --load-extension=/path/to/extension --enable-features=SidePanelCompanion`
3. Open SidePanel and choose `Google`

**Problem Description:**

1. Analysis

In the function `SearchCompanionSidePanelCoordinator::CreateCompanionEntry`, `Unretained(this)` is posted to callback[1], and the callback is managed by a unique\_ptr `SidePanelEntry`. However, the lifetime of this unique\_ptr may outlive `Unretained(this)`, which means the callback could run after `Unretained(this)` is freed, causing UAF.  

This can be done by merging the tab in different windows, as I showed in the extension. After moving tabs, the `SearchCompanionSidePanelCoordinator` is destructed but the unique\_ptr `SidePanelEntry` could still invoke the callback, causing UAF.

```
std::unique_ptr<SidePanelEntry>  
SearchCompanionSidePanelCoordinator::CreateCompanionEntry() {  
  return std::make_unique<SidePanelEntry>(  
      SidePanelEntry::Id::kSearchCompanion, name(),  
      ui::ImageModel::FromVectorIcon(icon(), ui::kColorIcon,  
                                     /\*icon_size=\*/16),  
      base::BindRepeating(  
          &SearchCompanionSidePanelCoordinator::CreateCompanionWebView,  
          base::Unretained(this)),  // Use of Unretained this  
      base::BindRepeating(  
          &SearchCompanionSidePanelCoordinator::GetOpenInNewTabUrl,  
          base::Unretained(this)));  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/search_companion/search_companion_side_panel_coordinator.cc;l=149;bpv=1;bpt=0;drc=69240a75289021b90fce66e994996c83706b02d0>

2. Bisect

This problem is introduced in this commit: 7c7a9038af332842527150a497ba17f916d2c5a1  

<https://chromium-review.googlesource.com/c/chromium/src/+/4319965>

This commit has been released on Beta 113.0.5672.24 and Dev 113.0.5653.0, so this UAF affects Beta between 113.0.5672.24 to 113.0.5672.53 AND Dev between 113.0.5653.0 to 114.0.5720.4

See attached beta.webm for repro.

3. Suggested Patch

Please pass a WeakPtr rather than an `Unretained` to ensure the lifetime of `this`

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.5672.24 \*\*Channel: \*\* Beta

**OS:** Linux

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 210 B)
- [background.js](attachments/background.js) (text/plain, 370 B)
- [asan.txt](attachments/asan.txt) (text/plain, 29.4 KB)
- [video.webm](attachments/video.webm) (video/webm, 465.6 KB)

## Timeline

### me...@gmail.com (2023-04-24)

[Comment Deleted]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-24)

Hi apalanki@ can you please take a look at this side panel UAF issue? Thanks! 

[Monorail components: UI>Browser>TopChrome>SidePanel]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### ad...@google.com (2023-04-24)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-04-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-25)

This issue requires --SidePanelCompanion (a component of Side Panel / Side Panel journeys) which is not yet enabled / launched, updating as SI-None accordingly; removing RBS as this is not a release blocking issue for M113

### ap...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### ap...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### mc...@google.com (2023-04-25)

shaktisahu@ do you have time for working on this?

If not, I'll bounce around. This is a launch blocker for the feature so we have to land a fix before branch.

### be...@google.com (2023-04-25)

Adding Hotlist-RBS-Removed for tracking purposes.

### me...@gmail.com (2023-05-04)

ping~

### sh...@chromium.org (2023-05-04)

Looked at this. Seems like SearchCompanionSidePanelCoordinator is a Browser scoped object, so I guess it dies when the browser window closes (merging tab from one window to another as the reporter says). The SidePanelEntry keeps a pointer to this coordinator which is invalid. We cannot use a weak ptr as the callback returns a value. Weak ptrs can only be used for void functions.

corising@ might have more idea on how to deal with this.

### mc...@google.com (2023-05-04)

[Empty comment from Monorail migration]

### co...@chromium.org (2023-05-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2e816abc7cd3e2fa496c27764caf646ecb467e26

commit 2e816abc7cd3e2fa496c27764caf646ecb467e26
Author: Caroline Rising <corising@chromium.org>
Date: Tue May 09 16:03:28 2023

Move csc entry and view creation into class attached to the web contents lifetime.

This fixes issues where crashes could happen if the tab was moved to a
different window since entry callbacks were attached to the
SearchCompanionSidePanelCoordinator (a BrowserUserData class) while csc
was a contextual (tab specific) entry.

Bug: 1438400
Change-Id: I87162dbf3456df353ed5d5f37be65230d873718a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4512818
Commit-Queue: Caroline Rising <corising@chromium.org>
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Reviewed-by: Ali Stanfield <stanfield@google.com>
Cr-Commit-Position: refs/heads/main@{#1141418}

[modify] https://crrev.com/2e816abc7cd3e2fa496c27764caf646ecb467e26/chrome/browser/ui/webui/side_panel/companion/companion_page_handler.cc
[modify] https://crrev.com/2e816abc7cd3e2fa496c27764caf646ecb467e26/chrome/browser/ui/side_panel/companion/companion_tab_helper.cc
[modify] https://crrev.com/2e816abc7cd3e2fa496c27764caf646ecb467e26/chrome/browser/ui/webui/side_panel/companion/companion_page_handler.h
[modify] https://crrev.com/2e816abc7cd3e2fa496c27764caf646ecb467e26/chrome/browser/ui/views/side_panel/search_companion/companion_side_panel_controller.cc
[modify] https://crrev.com/2e816abc7cd3e2fa496c27764caf646ecb467e26/chrome/browser/ui/views/side_panel/search_companion/companion_side_panel_controller.h
[modify] https://crrev.com/2e816abc7cd3e2fa496c27764caf646ecb467e26/chrome/browser/ui/side_panel/companion/companion_tab_helper.h
[modify] https://crrev.com/2e816abc7cd3e2fa496c27764caf646ecb467e26/chrome/browser/ui/views/side_panel/search_companion/companion_page_browsertest.cc
[modify] https://crrev.com/2e816abc7cd3e2fa496c27764caf646ecb467e26/chrome/browser/ui/views/side_panel/search_companion/search_companion_side_panel_coordinator.cc
[modify] https://crrev.com/2e816abc7cd3e2fa496c27764caf646ecb467e26/chrome/browser/ui/views/side_panel/search_companion/search_companion_side_panel_coordinator.h


### co...@chromium.org (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-19)

Congratulations, Krace! The VRP Panel has decided to award you $4,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-11)

Hi Krace, please remember we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Thanks! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1438400?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064189)*
