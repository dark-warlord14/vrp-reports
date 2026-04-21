# Security: Heap-use-after-free in WebContentsImpl::OpenURL

| Field | Value |
|-------|-------|
| **Issue ID** | [40060480](https://issues.chromium.org/issues/40060480) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Pogo, UI>Browser>TopChrome>SidePanel |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2022-08-03 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1030370.zip and unzip
2. run `./chrome --enable-features=SideSearch,UnifiedSidePanel,SideSearchDSESupport --user-data-dir=/tmp/noexist`
3. search anything with google.com and then navigate to any other search engine (such as bing.com)
4. click `Open Search in Side Panel` to open side search in side panel
5. select any text in side search and right click to choose 'Search Google for XXX'

PS: In step 3 you must use `google.com`. `google.com.xx` cannot trigger the Side Search

**Problem Description:**

# Root Cause

In `WebContentsImpl::OpenURL`[1], when `delelage_->OpenURLFromTab(this, params)` is called(1), the `source_render_frame_host`(2) could be freed in some conditions, the following use of `source_render_frame_host`(3) will cause UAF.

```
WebContents\* WebContentsImpl::OpenURL(const OpenURLParams& params) {  
  TRACE_EVENT1("content", "WebContentsImpl::OpenURL", "url", params.url);  
#if DCHECK_IS_ON()  
  DCHECK(params.Valid());  
#endif  
  
  if (!delegate_) {  
    // Embedder can delay setting a delegate on new WebContents with  
    // WebContentsDelegate::ShouldResumeRequestsForCreatedWindow. In the mean  
    // time, navigations, including the initial one, that goes through OpenURL  
    // should be delayed until embedder is ready to resume loading.  
    delayed_open_url_params_ = std::make_unique<OpenURLParams>(params);  
  
    // If there was a navigation deferred when creating the window through  
    // CreateNewWindow, drop it in favor of this navigation.  
    delayed_load_url_params_.reset();  
  
    return nullptr;  
  }  
  
  RenderFrameHost\* source_render_frame_host = RenderFrameHost::FromID(  // (2)  
      params.source_render_process_id, params.source_render_frame_id);  
  
  // Prevent frames that are not active (e.g. a prerendering page) from opening  
  // new windows, tabs, popups, etc.  
  if (params.disposition != WindowOpenDisposition::CURRENT_TAB &&  
      source_render_frame_host && !source_render_frame_host->IsActive()) {  
    return nullptr;  
  }  
  
  if (params.frame_tree_node_id != FrameTreeNode::kFrameTreeNodeInvalidId) {  
    if (auto\* frame_tree_node =  
            FrameTreeNode::GloballyFindByID(params.frame_tree_node_id)) {  
      // If a frame tree node ID is specified and it exists, ensure it is for a  
      // node within this WebContents. Note: this WebContents could be hosting  
      // multiple frame trees (e.g. prerendering) so it's not enough to check  
      // against this->primary_frame_tree_. Check against page_delegate(), which  
      // is always a WebContentsImpl, while delegate() may be implemented by  
      // something else such as for prerendered frame trees.  
      FrameTree\* frame_tree = frame_tree_node->frame_tree();  
      CHECK_EQ(frame_tree->page_delegate(), this);  
  
      // Prerendering and fenced frame navigations are hidden from embedders.  
      // If the navigation is targeting a frame in a prerendering or fenced  
      // frame tree, we shouldn't run that navigation through the embedder  
      // delegate. Embedder implementations of  
      // `WebContentsDelegate::OpenURLFromTab` assume that the primary  
      // frame tree Navigation controller should be used for navigating.  
      // Instead, we just navigate directly on the relevant frame  
      // tree.  
      if (frame_tree->type() == FrameTree::Type::kPrerender ||  
          frame_tree->type() == FrameTree::Type::kFencedFrame) {  
        DCHECK_EQ(params.disposition, WindowOpenDisposition::CURRENT_TAB);  
        frame_tree->controller().LoadURLWithParams(  
            NavigationController::LoadURLParams(params));  
        return this;  
      }  
    } else {  
      // If the node doesn't exist it was probably removed from its frame tree.  
      // In that case, abort since continuing would navigate the root frame.  
      return nullptr;  
    }  
  }  
  
  WebContents\* new_contents = delegate_->OpenURLFromTab(this, params);  //(1)  
  
  if (source_render_frame_host && params.source_site_instance) {  
    CHECK_EQ(source_render_frame_host->GetSiteInstance(),   // (3)  
             params.source_site_instance.get());  
  }  
  if (new_contents && source_render_frame_host && new_contents != this) {  
    observers_.NotifyObservers(  
        &WebContentsObserver::DidOpenRequestedURL, new_contents,  
        source_render_frame_host, params.url, params.referrer,  
        params.disposition, params.transition, params.started_from_context_menu,  
        params.is_renderer_initiated);  
  }  
  
  return new_contents;  
}  

```

When calling `OpenURLFromTab`, SideSearch will actually call `UnifiedSideSearchController::OpenURLFromTab`[2], it will use SideSearch's `browser_view` to call `OpenURL`. According to the ASAN log[3], `OpenURL` will change to a new Tab, so the SidePanel will Close and destroy the corresponding FrameTree and RenderFrameHost.

```
content::WebContents\* UnifiedSideSearchController::OpenURLFromTab(  
    content::WebContents\* source,  
    const content::OpenURLParams& params) {  
  auto\* browser_view = GetBrowserView();  
  return browser_view ? browser_view->browser()->OpenURL(params) : nullptr;  
}  

```
```
#18 0x562c75138396 in SidePanelCoordinator::Close() chrome/browser/ui/views/side_panel/side_panel_coordinator.cc:270:5  
#19 0x562c74598ae2 in TabStripModel::OnChange(TabStripModelChange const&, TabStripSelectionChange const&) chrome/browser/ui/tabs/tab_strip_model.cc:461:14  
#20 0x562c745975c5 in TabStripModel::InsertWebContentsAtImpl(int, std::Cr::unique_ptr<content::WebContents, std::Cr::default_delete<content::WebContents>>, int, absl::optional<tab_groups::Tab  
  
**Additional Comments:**   
  
  
**Chrome version: ** 103.0.0.0 **Channel: ** Not sure  
  
**OS:** Linux

```

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.4 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 1.2 MB)

## Timeline

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### ma...@google.com (2022-08-04)

I can reproduce this in 1030430 (which is M106), but not 1012727 (104) or 1002919 (103). From what I can tell `--enable-features=SideSearch,SideSearchDSESupport` actually suffices for this (i.e. UnifiedSidePanel isn't required).

@Reporter: You seem to have tested with 1030370 (M106), but also say "Chrome version: 103.0.0.0". Could you confirm that you're only seeing this in M106?

FoundIn-M106 for now. 

This is browser process memory corruption, but the interaction required to trigger it is pretty specific, hence Security_Severity-High rather than Critical.

From what I can tell, at least SideSearchDSESupport isn't yet enabled in Stable, so this should probably be Security_Impact-Dev or something like that. But I'll wait for the feature team to confirm which channels this actually impacts currently.

[Monorail components: UI>Browser>Pogo UI>Browser>TopChrome>SidePanel]

### ma...@google.com (2022-08-04)

Also reproduces in 1027018 (M105)

### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-08-05)

>@Reporter: You seem to have tested with 1030370 (M106), but also say "Chrome version: 103.0.0.0". Could you confirm that you're only seeing this in M106?
Sorry, I only test it in 1030370, 103.0.0.0 is the Version of chrome that I submit this issue, not the affected Version.

### [Deleted User] (2022-08-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2022-08-05)

Routing to yuhengh@ for Side Search.

### tl...@chromium.org (2022-08-05)

Currently this will only repro in versions M105+.

This requires Side Search and the Unified Side Panel to both be enabled (i.e. --enable-features=SideSearch,UnifiedSidePanel,SideSearchDSESupport ) - and for Side Search to be running the code that integrates it with the Unified Side Panel. The integration was added in Chrome M105.

To trigger the crash the user needs to explicitly enable the UnifiedSidePanel flag on M105 since the UnifiedSidePanel flag is currently only at 50% Canary / Dev. This likely still warrants a RBS label however so we'll want the fix to land by stable cut later this month.

Yuheng is working on a fix and we should have this ready for a merge soon.

### tl...@chromium.org (2022-08-05)

(re-adding the dropped label)

### yu...@chromium.org (2022-08-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d633877e387532422e93ec9ff61778b1676654c2

commit d633877e387532422e93ec9ff61778b1676654c2
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Sun Aug 07 23:40:07 2022

Side search v2: fix uaf with right click search

When right click context menu and search Google for ... from the side
search side panel, a new foreground will be created to trigger closing the side panel. When side panel is closed, it destroys the side panel WebView, which destroys side search side panel WebContents and cause a UaF inside WebContentsImpl::OpenURL.

This CL prevents WebView from destroying side search side panel WebContents when side search entry is still active in this particular case. A possibly better approach in the future may be have the side panel framework not destroy the view when the side panel entry is still active.

Bug: 1349687
Change-Id: I74a5cc9cc353e108e4300db9a05dbad1267613c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3812004
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1032391}

[modify] https://crrev.com/d633877e387532422e93ec9ff61778b1676654c2/chrome/browser/ui/views/side_search/unified_side_search_controller.cc
[modify] https://crrev.com/d633877e387532422e93ec9ff61778b1676654c2/chrome/browser/ui/views/side_search/unified_side_search_controller_interactive_uitest.cc


### pb...@google.com (2022-08-08)

[Bulk Edit] M105 is already promoted to Beta and we are just 2 weeks away from Stable RC cut this bug has been marked as Stable blocker, Please take a look asap. thank you.

### yu...@chromium.org (2022-08-08)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-08-08)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-08-08)

@pbommana the issue should be fixed, could you verify it? Thanks.

### [Deleted User] (2022-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-08)

Merge review required: M105 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2022-08-09)

1. It's a stable release blocker.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3812004
3. Yes.
4. Yes, it's behind UnifiedSidePanel flag, which is aimed to launch in M105.
5. It's a Chrome feature.
6. I manually verified the issue is fixed. The test added in the CL also can verify the fix.

### am...@chromium.org (2022-08-09)

There appear to be no stability issues or other concerns from this relatively small fix -- M105 merge approved, please merge this fix to branch 5195 asap so this fix can be included in tomorrow's M105 beta release since this feature scheduled to be launched in M105 when promoted to stable. 

### gi...@appspot.gserviceaccount.com (2022-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e1dcdf0a35d65864f51bf6d38e8c9e7a9df29214

commit e1dcdf0a35d65864f51bf6d38e8c9e7a9df29214
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Tue Aug 09 19:20:02 2022

[M105 Merge] Side search v2: fix uaf with right click search

When right click context menu and search Google for ... from the side
search side panel, a new foreground will be created to trigger closing the side panel. When side panel is closed, it destroys the side panel WebView, which destroys side search side panel WebContents and cause a UaF inside WebContentsImpl::OpenURL.

This CL prevents WebView from destroying side search side panel WebContents when side search entry is still active in this particular case. A possibly better approach in the future may be have the side panel framework not destroy the view when the side panel entry is still active.

(cherry picked from commit d633877e387532422e93ec9ff61778b1676654c2)

Bug: 1349687
Change-Id: I74a5cc9cc353e108e4300db9a05dbad1267613c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3812004
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1032391}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3818641
Reviewed-by: Allen Bauer <kylixrd@chromium.org>
Cr-Commit-Position: refs/branch-heads/5195@{#383}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/e1dcdf0a35d65864f51bf6d38e8c9e7a9df29214/chrome/browser/ui/views/side_search/unified_side_search_controller.cc
[modify] https://crrev.com/e1dcdf0a35d65864f51bf6d38e8c9e7a9df29214/chrome/browser/ui/views/side_search/unified_side_search_controller_interactive_uitest.cc


### [Deleted User] (2022-08-09)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2022-08-09)

No need to merge to LTS Milestone M102 since it's a new feature that's not available then.


### rz...@google.com (2022-08-10)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-10)

Changed files aren't present in 96 and 102 branches

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. The reward amount was based on this issue being significantly mitigated by not being remote exploitable and the significant user interaction required. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-21)

Hello OP, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1349687?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Pogo, UI>Browser>TopChrome>SidePanel]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060480)*
