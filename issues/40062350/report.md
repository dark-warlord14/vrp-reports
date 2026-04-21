# Security: Heap-use-after-free in ExtensionViewHost::OnDidStopFirstLoad

| Field | Value |
|-------|-------|
| **Issue ID** | [40062350](https://issues.chromium.org/issues/40062350) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2022-12-22 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1086198.zip and unzip
2. put `default_path.html` and `manifest.json` in the folder `/path/to/extension` AND run `./chrome --user-data-dir=/tmp/noexist --enable-features=ExtensionSidePanelIntegration --load-extension=/path/to/extension`
3. open the side panel, switch the combobox to `Extension` then close the side panel
4. open and close the side panel again, UAF occurs

**Problem Description:**

1. Analysis

In `ExtensionViewHost`, there is a raw\_ptr `view_`[1]. This `view_` can be created by `ExtensionSidePanelCoordinator`[2]

```
void ExtensionViewHost::OnDidStopFirstLoad() {  
  view_->OnLoaded();  
}  

```
```
std::unique_ptr<views::View> ExtensionSidePanelCoordinator::CreateView(  
    const GURL& side_panel_url) {  
  host_ =  
      ExtensionViewHostFactory::CreateSidePanelHost(side_panel_url, browser_);  
  
  auto extension_view = std::make_unique<ExtensionViewViews>(host_.get());  
  extension_view->SetVisible(true);  
  
  return extension_view;  
}  

```

When we close the side panel, this view will be removed, and therefore destruct the `view_`[3]. However, when we close the side panel, WebContents will call this function `LoadingStateChanged`[4], which will notify `ExtensionViewHost::OnDidStopFirstLoad`[1], the use of freed `view_` causes UAF.

```
void SidePanelCoordinator::Close() {  
[...]  
  // `OnEntryWillDeregister` (triggered by calling `OnEntryHidden`) may already  
  // have deleted the content view, so check that it still exists.  
  if (views::View\* content_view = GetContentView())  
    browser_view_->unified_side_panel()->RemoveChildViewT(content_view);  // this will remove the view  
[...]  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/extension_view_host.cc;l=99;drc=72e47001946d247e7e38c91c1c64f226e1766a92;bpv=1;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/extensions/extension_side_panel_coordinator.cc;l=80;drc=5c59552006a1431d22fd927b370782683a9a1602;bpv=0;bpt=0>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/side_panel_coordinator.cc;l=297;drc=3818a71e195ac2ff46729c4428127ef23b4de43b;bpv=0;bpt=0>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=6861;drc=23e90a11b9094fe2682083445f14abbaea9bef48;bpv=1;bpt=0>

2. Affected versions  
   
   This new creation of `ExtensionViewViews` is introduced in this commit: 5c59552006a1431d22fd927b370782683a9a1602  
   
   The change of `ExtensionViewHost::view_` from `unique_ptr` to `raw_ptr` is introduced in this commit: 48ca044350b60cf785693f36cc25a279fe0b3492
3. Suggested Patch  
   
   Maybe you could use a weak\_ptr to check whether `view_` has been freed before use it.

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 187 B)
- [default_path.html](attachments/default_path.html) (text/plain, 23 B)
- [asan.txt](attachments/asan.txt) (text/plain, 21.6 KB)
- [video.webm](attachments/video.webm) (video/webm, 365.5 KB)

## Timeline

### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-22)

Thanks for the report! I'm able to reproduce. +kelvinjiang@ to take a look.

Setting severity to high since it is a UaF in the browser process that requires UI interaction. https://crrev.com/c/4118630 was landed in 111 so setting FoundIn to M111 (https://chromiumdash.appspot.com/commits?commit=5c59552006a1431d22fd927b370782683a9a1602&platform=Windows).

[Monorail components: Platform>Extensions]

### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-12-22)

I've encountered this UAF as well while working on another related CL in tests, which caused the test to flake. I was able to come up with a fix and I will add it individually in a CL.

### [Deleted User] (2022-12-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-12-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/15551a2cd53d3f56f16bd137bea728c802273024

commit 15551a2cd53d3f56f16bd137bea728c802273024
Author: Kelvin Jiang <kelvinjiang@chromium.org>
Date: Wed Dec 28 16:20:02 2022

[Extensions] Fix UAF in side panel if closed quickly

This CL fixes a use after free if the extension's side panel is open by
selecting the extension's side panel entry, then closing the side panel
quickly before the extension's page has finished loading. Here, the
ExtensionViewHost still gets notified when the load finishes even
though the side panel is closed and its associated view is destroyed.
At this time, attempting to use the host's view triggers the UAF.

The fix was to listen for the destruction the extension's side panel
view. When this happens, reset the ExtensionViewHost so it can't
notify its associated view (which no longer exists) when events come
in.

Bug: 1403168
Change-Id: Id300d16ba2a9cbcb1efdbb97234a95c285491276
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4120250
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1087345}

[modify] https://crrev.com/15551a2cd53d3f56f16bd137bea728c802273024/chrome/browser/ui/views/side_panel/extensions/extension_side_panel_browsertest.cc
[modify] https://crrev.com/15551a2cd53d3f56f16bd137bea728c802273024/chrome/browser/ui/views/extensions/extension_view_views.cc
[modify] https://crrev.com/15551a2cd53d3f56f16bd137bea728c802273024/chrome/browser/ui/views/extensions/extension_view_views.h
[modify] https://crrev.com/15551a2cd53d3f56f16bd137bea728c802273024/chrome/browser/ui/views/side_panel/extensions/extension_side_panel_coordinator.h
[modify] https://crrev.com/15551a2cd53d3f56f16bd137bea728c802273024/chrome/browser/ui/views/side_panel/extensions/extension_side_panel_coordinator.cc


### ke...@chromium.org (2022-12-28)

Fix has been merged into origin/main, should be landing in Canary by tonight

### [Deleted User] (2022-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-04)

Congratulations Krace! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

Not requesting merge to dev (M111) because latest trunk commit (1087345) appears to be prior to dev branch point (1097615). If this is incorrect, please replace the Merge-NA-111 label with Merge-Request-111. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M111. Please go ahead and merge the CL to branch 5563 (refs/branch-heads/5563) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-27)

this fix landed on M111, no merge needed here

### [Deleted User] (2023-04-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1403168?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062350)*
