# Security: UAF in BookmarkDragHelper

| Field | Value |
|-------|-------|
| **Issue ID** | [40058534](https://issues.chromium.org/issues/40058534) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Bookmarks |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | pk...@chromium.org |
| **Created** | 2022-01-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

BookmarkDragHelper::OnBookmarkIconLoaded could be called from both `Start` and `BookmarkNodeFaviconChanged`, so a re-entrant call to OnBookmarkIconLoaded is made if the favicon changes while the bookmark node is being dragged, and the `delete this` code at [1] would be executed twice, leading to Use-After-Free.

```
  void OnBookmarkIconLoaded(const BookmarkNode\* drag_node,  
                            const ui::ImageModel& icon) {  
    if (web_contents_) {  
      // skip...  
      std::move(do_drag_callback_)  
          .Run(std::move(drag_data_), web_contents_->GetNativeView(), source_,  
               start_point_, operation_);  
    }  
  
    delete this;   // ===> [1]  
  }  
  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc;l=258;drc=5eaba7cca73cbb6743cc76c7bf1e5935d94110cc>

**VERSION**  

Chrome Version: 97.0.4692.99 stable + dev

**REPRODUCTION CASE**

1. Unzip the attached poc.zip
2. Setup a HTTP server using nodejs  
   
   node ./server.js
3. Run following command  
   
   out/Asan/chrome --load-extension=<path-to-the-extracted-poc-files>/extension
4. Click the bookmark on the page and start dragging, keep dragging until the bookmarks ui page is closed, and the browser should crash when drag&drop is ended

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log for details

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 56.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 59 B)
- [server.js](attachments/server.js) (text/plain, 691 B)
- [tree.ico](attachments/tree.ico) (image/x-icon, 179.6 KB)
- [background.js](attachments/background.js) (text/plain, 865 B)
- [manifest.json](attachments/manifest.json) (text/plain, 273 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.6 MB)
- [asan.log](attachments/asan.log) (text/plain, 17.5 KB)

## Timeline

### [Deleted User] (2022-01-20)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-20)

Hi could you upload the poc files individually as well, this makes it easier to take a quick look at the issue.

How does this relate to 1282118?

### aj...@google.com (2022-01-21)

uploading contained files.

### aj...@google.com (2022-01-21)

I'm not currently able to reproduce - it might be helpful to have a short video showing the ui interactions that are required.

### jt...@gmail.com (2022-01-21)

Re #2:
https://crbug.com/chromium/1282118 fixed a UAF results from using raw pointer to `webcontents_` even after the WebContents has gone, and I think this issue is about the re-entrance of function OnBookmarkIconLoaded. While a bookmark is being dragged, it calls `do_drag_callback_` [2] (DoDragImpl) and returns when the drag is complete. However, BookmarkNodeFaviconChanged could be invoked during the dragging process, which calls OnBookmarkIconLoaded again. There are two situations at this time:

1. `webcontents_` is still valid, it will call `do_drag_callback_` again, results in null pointer dereference because `do_drag_callback_` is a OnceCallback.
2. `webcontents_` has been invalidated, it will execute `delete this` directly, and UAF occurs when the first executed `do_drag_callback_` returns and execute `delete this` again.

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc;l=253;drc=5eaba7cca73cbb6743cc76c7bf1e5935d94110cc

Also upload a video for reproducing.

### aj...@google.com (2022-01-21)

Thanks - I'm still not able to repro on HEAD. Can you let me know which asan build you are using?

### [Deleted User] (2022-01-21)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-01-21)

Also cannot repro on Stable.

### jt...@gmail.com (2022-01-22)

Hi, I downloaded and tested on the asan-build chromium from google storage at https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-962180.zip?generation=1642816152519743&alt=media

Metadata:
Commit hash: 933398e9a494e6f1ce272830b610096598ddc228
File: asan-win32-release_x64-962180.zip
Updated: 2022-01-22T01:49:12.596Z

Clearing the browser data (eg. deleting the user data directory) before every new attempt might be helpful, because the favicon may already exist thus OnBookmarkIconLoaded would not be called.

### aj...@google.com (2022-01-25)

Thanks I have finally got this to reproduce:

D:\temp\asan> .\asan-win32-release_x64-962180\chrome.exe --no-sandbox --user-data-dir=d:\temp\asan\user --no-first-run --load-extension=d:/pocs/1289192/extension/
Chrome will open
When the bookmarks page displays, start to drag the bookmark
The extension will then open a new tab
Wiggle the bookmark around and drop it in the tab (i.e. let go of the mouse)

On my asan head build I cannot repro as the chrome://bookmarks page is closed before it gets to displaying anything.

Owner:pkasting as they looked at https://crbug.com/chromium/1282118

Severity=Medium as the requires (a) an extension (b) interaction with (c) chrome://bookmarks
FoundIn=97 based on report

[Monorail components: UI>Browser>Bookmarks]

### [Deleted User] (2022-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

pkasting: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-17)

pkasting: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-02-17)

CC some other people involved with bookmarks for visibility.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### pk...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/29459d6d51286e9d972964abe069a43334919ad6

commit 29459d6d51286e9d972964abe069a43334919ad6
Author: Peter Kasting <pkasting@chromium.org>
Date: Wed Apr 06 18:34:21 2022

Avoid UAF when bookmark icon changes repeatedly while dragging.

Bug: 1289192
Change-Id: I48c1a2bbf0dee7071ebe59c261da47266fd47bf8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3574875
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Auto-Submit: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#989536}

[modify] https://crrev.com/29459d6d51286e9d972964abe069a43334919ad6/chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc


### pk...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-14)

Hello and thank you for this report! The VRP Panel has decided to award you $3,000 for this report due to the mitigation of requiring an extension and the user interaction involved to trigger this issue. Thank you for your efforts and reporting this issue to us.

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-25)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/39acb79d6d841514ac4b19358106bb170ce42a47

commit 39acb79d6d841514ac4b19358106bb170ce42a47
Author: Peter Kasting <pkasting@chromium.org>
Date: Thu May 26 15:28:36 2022

[M96-LTS] Avoid UAF when bookmark icon changes repeatedly while dragging.

(cherry picked from commit 29459d6d51286e9d972964abe069a43334919ad6)

Bug: 1289192
Change-Id: I48c1a2bbf0dee7071ebe59c261da47266fd47bf8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3574875
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Auto-Submit: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#989536}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3669027
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1638}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/39acb79d6d841514ac4b19358106bb170ce42a47/chrome/browser/ui/views/bookmarks/bookmark_drag_drop_views.cc


### rz...@google.com (2022-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1289192?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058534)*
