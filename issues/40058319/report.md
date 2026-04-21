# Security: UAF in BookmarkDragHelper::OnBookmarkIconLoaded

| Field | Value |
|-------|-------|
| **Issue ID** | [40058319](https://issues.chromium.org/issues/40058319) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Views, UI>Browser>Bookmarks |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | pk...@chromium.org |
| **Created** | 2021-12-22 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

BookmarkDragHelper is a self-owned class that takes a bookmark drag request and responsible for deleting itself after drag ends. Its constructor takes a raw pointer to WebContents and stores it as a member [1], and the codes can also observe BookmarkModel events [2].

```
BookmarkDragHelper(Profile\* profile,  
                    const BookmarkDragParams& params,  
                    DoBookmarkDragCallback do_drag_callback)  
    : model_(BookmarkModelFactory::GetForBrowserContext(profile)),  
      count_(params.nodes.size()),  
      web_contents_(params.web_contents),  // ===> [1]  
      source_(params.source),  
      start_point_(params.start_point),  
      do_drag_callback_(std::move(do_drag_callback)),  
      drag_data_(std::make_unique<ui::OSExchangeData>()) {  
  observation_.Observe(model_.get());      // ===> [2]  

```

If the favicon of the bookmark node being dragged changes, OnBookmarkIconLoaded will be invoked and there is a virtual function call on webcontents\_ pointer [3]. However, the WebContents instance can be freed if the web page has already been closed, thus causing UAF in browser process.

```
  void OnBookmarkIconLoaded(const BookmarkNode\* drag_node,  
                            const ui::ImageModel& icon) {  
    auto\* widget =  
        views::Widget::GetWidgetForNativeView(web_contents_->GetNativeView()); // ===> [3]  
    // skip  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc;l=188;drc=9356708a7b47760261c0f895d7fc6a5087f5b55b>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc;l=193;drc=9356708a7b47760261c0f895d7fc6a5087f5b55b>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc;l=230;drc=9356708a7b47760261c0f895d7fc6a5087f5b55b>

**VERSION**  

Chrome Version: stable (96.0.4664.110) + dev

**REPRODUCTION CASE**

1. Unzip the attached poc.zip
2. Setup a HTTP server using nodejs  
   
   node ./server.js
3. Run following command  
   
   chrome --load-extension=<path-to-the-extracted-poc-files>/extension
4. Click the bookmark on the page and start dragging, keep dragging for a few seconds (~5s) and the browser should crash

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log for details

**CREDIT INFORMATION**  

@\_\_R0ng and Guang Gong of 360 Alpha Lab

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 56.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 30.1 KB)

## Timeline

### [Deleted User] (2021-12-22)

[Empty comment from Monorail migration]

### jt...@gmail.com (2021-12-22)

[Comment Deleted]

### wf...@chromium.org (2021-12-22)

Thanks for your report. Triaging as High since this is a UAF in the browser that requires user interaction.

I'm assigning this to pkasting@ based on code changes to the affected files(s) although this doesn't strike me as a recent regression, suspected since m93?

[Monorail components: Internals>Views UI>Browser>Bookmarks]

### [Deleted User] (2021-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-05)

pkasting: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pk...@chromium.org (2022-01-10)

Clearly this code needs to use WebContents::GetWeakPtr, and sanity-check it before calling anything on it.

### pk...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5eaba7cca73cbb6743cc76c7bf1e5935d94110cc

commit 5eaba7cca73cbb6743cc76c7bf1e5935d94110cc
Author: Peter Kasting <pkasting@chromium.org>
Date: Mon Jan 10 20:32:48 2022

Check whether the WebContents has been destroyed before dereffing.

This prevents a UAF if the bookmark icon changes after the web page is
closed.

Bug: 1282118
Change-Id: I9b9f6c323dc00f499f141953363f73fa9bb3d538
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378450
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Auto-Submit: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#957179}

[modify] https://crrev.com/5eaba7cca73cbb6743cc76c7bf1e5935d94110cc/chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc


### pk...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

Requesting merge to extended stable M96 because latest trunk commit (957179) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (957179) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (957179) appears to be after beta branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-12)

Merge review required: M98 is already shipping to beta.

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

### [Deleted User] (2022-01-12)

Merge review required: M97 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-12)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-14)

based on checks and off-bug chat with pkasting@, no stability issues or concerns here, so approving merge to M96 and M97, please merge to branches 4664 and 4692 respectively, ASAP -- NLT tomorrow/Friday, 14 January so this fix can be included in the next Extended and Stable security respins -- thank you! 

### am...@chromium.org (2022-01-14)

merge also approved to m98, please merge to branch 4758 at your earliest convenience 


### sr...@google.com (2022-01-14)

Please complete your merges to M97/M96 branches asap before 1pm PST today as we are cutting RC build for these today.

### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2fa5a30cbee60a79a8f64fa054c31447c568071c

commit 2fa5a30cbee60a79a8f64fa054c31447c568071c
Author: Peter Kasting <pkasting@chromium.org>
Date: Fri Jan 14 20:07:41 2022

Check whether the WebContents has been destroyed before dereffing.

This prevents a UAF if the bookmark icon changes after the web page is
closed.

(cherry picked from commit 5eaba7cca73cbb6743cc76c7bf1e5935d94110cc)

Bug: 1282118
Change-Id: I9b9f6c323dc00f499f141953363f73fa9bb3d538
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378450
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Auto-Submit: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#957179}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389552
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#630}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/2fa5a30cbee60a79a8f64fa054c31447c568071c/chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc


### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9109a3aa18a637f5ecb11abe81654415e8523ac8

commit 9109a3aa18a637f5ecb11abe81654415e8523ac8
Author: Peter Kasting <pkasting@chromium.org>
Date: Fri Jan 14 20:10:51 2022

Check whether the WebContents has been destroyed before dereffing.

This prevents a UAF if the bookmark icon changes after the web page is
closed.

(cherry picked from commit 5eaba7cca73cbb6743cc76c7bf1e5935d94110cc)

Bug: 1282118
Change-Id: I9b9f6c323dc00f499f141953363f73fa9bb3d538
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378450
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Auto-Submit: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#957179}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389554
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1403}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/9109a3aa18a637f5ecb11abe81654415e8523ac8/chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc


### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/08d44f95a8a08ce0e702324589fab34ea7ebd581

commit 08d44f95a8a08ce0e702324589fab34ea7ebd581
Author: Peter Kasting <pkasting@chromium.org>
Date: Fri Jan 14 20:11:36 2022

Check whether the WebContents has been destroyed before dereffing.

This prevents a UAF if the bookmark icon changes after the web page is
closed.

(cherry picked from commit 5eaba7cca73cbb6743cc76c7bf1e5935d94110cc)

Bug: 1282118
Change-Id: I9b9f6c323dc00f499f141953363f73fa9bb3d538
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378450
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Auto-Submit: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#957179}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389553
Cr-Commit-Position: refs/branch-heads/4692@{#1441}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/08d44f95a8a08ce0e702324589fab34ea7ebd581/chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc


### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-20)

And another one -- congratulations! The VRP Panel has decided to award you $10,000 for this report. Thanks for your effort and great work! 

### am...@google.com (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1282118?no_tracker_redirect=1

[Multiple monorail components: Internals>Views, UI>Browser>Bookmarks]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058319)*
