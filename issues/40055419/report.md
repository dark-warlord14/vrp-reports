# UAF in bookmark

| Field | Value |
|-------|-------|
| **Issue ID** | [40055419](https://issues.chromium.org/issues/40055419) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Bookmarks |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | su...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2021-04-02 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36

Steps to reproduce the problem:
1.load the extension
2.do the step as my follows .mp4 will trigger the uaf

What is the expected behavior?

What went wrong?
BookmarkEditorView::ExecuteCommand will run a message loop,
and node[1] will be destroyed in the message loop.Then uaf will be trigger when access the node.
void BookmarkEditorView::ExecuteCommand(int command_id, int event_flags) {
  DCHECK(tree_view_->GetActiveNode());
    LOG(ERROR)<<"in BookmarkEditorView::ExecuteCommand";

  if (command_id == IDS_EDIT) {
    tree_view_->StartEditing(tree_view_->GetActiveNode());
  } else if (command_id == IDS_DELETE) {
      LOG(ERROR)<<"in BookmarkEditorView::ExecuteCommand delete";
    EditorNode* node = tree_model_->AsNode(tree_view_->GetActiveNode()); [1]
    if (!node)
      return;
      LOG(ERROR)<<"bypass 1";
    if (node->value != 0) {
        LOG(ERROR)<<"bypass 2";
      const BookmarkNode* b_node =
          bookmarks::GetBookmarkNodeByID(bb_model_, node->value);
      if (!b_node->children().empty() &&
          !chrome::ConfirmDeleteBookmarkNode(b_node,
                                             GetWidget()->GetNativeWindow())) {
        // The folder is not empty and the user didn't confirm.
        return;
      }
      deletes_.push_back(node->value);
    }
    tree_model_->Remove(node->parent(), node);
  } else {
    DCHECK_EQ(IDS_BOOKMARK_EDITOR_NEW_FOLDER_MENU_ITEM, command_id);
    NewFolder(tree_model_->AsNode(tree_view_->GetActiveNode()));
  }
}

I will upload the poc soon

Did this work before? N/A 

Chrome version: 89.0.4389.114  Channel: stable
OS Version: OS X 11.2.3
Flash Version:

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 18.2 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [extension.js](attachments/extension.js) (text/plain, 644 B)
- [manifest.json](attachments/manifest.json) (text/plain, 356 B)
- deleted (application/octet-stream, 0 B)
- [Screencast 2021-04-02 15_03_46.mp4](attachments/Screencast 2021-04-02 15_03_46.mp4) (video/mp4, 3.0 MB)

## Timeline

### [Deleted User] (2021-04-02)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-04-02)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-04-02)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-04-02)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-04-05)

[Comment Deleted]

### dr...@chromium.org (2021-04-05)

Thanks for the report, this reproduced for me. Triaging as medium severity due to the need for a specific malicious extension. Forwarding to bookmarks owners.

mastiz@, sky@ - can you take a look?

[Monorail components: UI>Browser>Bookmarks]

### dr...@chromium.org (2021-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-05)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2021-04-06)

The right thing is likely to convert ConfirmDeleteBookmarkNode to be async.

### su...@gmail.com (2021-04-09)

Hello, could you change the impact OS more widely? I think it's not just impact mac. Thank you!

### ma...@chromium.org (2021-04-09)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-04-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a453de0ca590f4341a6d8d32bb5f6525705676de

commit a453de0ca590f4341a6d8d32bb5f6525705676de
Author: Mikel Astiz <mastiz@chromium.org>
Date: Fri Apr 09 18:45:35 2021

[bookmarks] Fix UAF if bookmark deleted during modal confirmation dialog

BookmarkEditorView shows a modal dialog when the user requests to delete
a bookmark folder that is non-empty, for the user to confirm. This
involves a nested message loop, which means that additional changes can
take place, including extensions modifying the bookmark tree.

If the bookmark folder being modified by the user happens to be deleted
(e.g. by an extension) while the confirmation dialog is open, prior to
this patch, the code could dereference freed memory.

In this patch, a safeguard is introduced to fix the issue, which is
achieved by detecting problematic changes based on bookmark IDs (which
are integers and never reused during the lifetime of the browser).

Change-Id: Ife1d005f1b3d8d17b5b5d7c07b538732cd377e13
Bug: 1195278
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2818022
Commit-Queue: Mikel Astiz <mastiz@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/master@{#871053}

[modify] https://crrev.com/a453de0ca590f4341a6d8d32bb5f6525705676de/chrome/browser/ui/bookmarks/bookmark_utils_desktop.cc
[modify] https://crrev.com/a453de0ca590f4341a6d8d32bb5f6525705676de/chrome/browser/ui/bookmarks/bookmark_utils_desktop.h
[modify] https://crrev.com/a453de0ca590f4341a6d8d32bb5f6525705676de/chrome/browser/ui/views/bookmarks/bookmark_editor_view.cc
[modify] https://crrev.com/a453de0ca590f4341a6d8d32bb5f6525705676de/chrome/browser/ui/views/bookmarks/bookmark_editor_view.h
[modify] https://crrev.com/a453de0ca590f4341a6d8d32bb5f6525705676de/chrome/browser/ui/views/bookmarks/bookmark_editor_view_unittest.cc


### ma...@chromium.org (2021-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-12)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-04-13)

report credit: koocola(@alo_cook) and Nan Wang(@eternalsakura13) of 360 Alpha Lab.
Thank you!


### [Deleted User] (2021-04-13)

Your change meets the bar and is auto-approved for M91. Please go ahead and merge the CL to branch 4472 (refs/branch-heads/4472) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e4ac01f0725366234305fdd841e87a371c3d3ae3

commit e4ac01f0725366234305fdd841e87a371c3d3ae3
Author: Mikel Astiz <mastiz@chromium.org>
Date: Tue Apr 13 20:52:01 2021

[bookmarks] Fix UAF if bookmark deleted during modal confirmation dialog

BookmarkEditorView shows a modal dialog when the user requests to delete
a bookmark folder that is non-empty, for the user to confirm. This
involves a nested message loop, which means that additional changes can
take place, including extensions modifying the bookmark tree.

If the bookmark folder being modified by the user happens to be deleted
(e.g. by an extension) while the confirmation dialog is open, prior to
this patch, the code could dereference freed memory.

In this patch, a safeguard is introduced to fix the issue, which is
achieved by detecting problematic changes based on bookmark IDs (which
are integers and never reused during the lifetime of the browser).

(cherry picked from commit a453de0ca590f4341a6d8d32bb5f6525705676de)

Change-Id: Ife1d005f1b3d8d17b5b5d7c07b538732cd377e13
Bug: 1195278
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2818022
Commit-Queue: Mikel Astiz <mastiz@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#871053}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2822158
Reviewed-by: Mikel Astiz <mastiz@chromium.org>
Reviewed-by: Prudhvi Kumar Bommana <pbommana@google.com>
Auto-Submit: Mikel Astiz <mastiz@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Prudhvi Kumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/4472@{#43}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/e4ac01f0725366234305fdd841e87a371c3d3ae3/chrome/browser/ui/bookmarks/bookmark_utils_desktop.cc
[modify] https://crrev.com/e4ac01f0725366234305fdd841e87a371c3d3ae3/chrome/browser/ui/bookmarks/bookmark_utils_desktop.h
[modify] https://crrev.com/e4ac01f0725366234305fdd841e87a371c3d3ae3/chrome/browser/ui/views/bookmarks/bookmark_editor_view.cc
[modify] https://crrev.com/e4ac01f0725366234305fdd841e87a371c3d3ae3/chrome/browser/ui/views/bookmarks/bookmark_editor_view.h
[modify] https://crrev.com/e4ac01f0725366234305fdd841e87a371c3d3ae3/chrome/browser/ui/views/bookmarks/bookmark_editor_view_unittest.cc


### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Congratulations, superjoe@! The VRP Panel has decided to award you $7500 for this report. Nice work and thanks for reporting this! 

### su...@gmail.com (2021-04-24)

Thank you very much!

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### ja...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### gi...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/10bd177a4b078b47636c3894daf0f3b5af348733

commit 10bd177a4b078b47636c3894daf0f3b5af348733
Author: Mikel Astiz <mastiz@chromium.org>
Date: Thu May 27 15:27:22 2021

[86-LTS][bookmarks] Fix UAF if bookmark deleted during modal confirmation dialog

BookmarkEditorView shows a modal dialog when the user requests to delete
a bookmark folder that is non-empty, for the user to confirm. This
involves a nested message loop, which means that additional changes can
take place, including extensions modifying the bookmark tree.

If the bookmark folder being modified by the user happens to be deleted
(e.g. by an extension) while the confirmation dialog is open, prior to
this patch, the code could dereference freed memory.

In this patch, a safeguard is introduced to fix the issue, which is
achieved by detecting problematic changes based on bookmark IDs (which
are integers and never reused during the lifetime of the browser).

(cherry picked from commit a453de0ca590f4341a6d8d32bb5f6525705676de)

Change-Id: Ife1d005f1b3d8d17b5b5d7c07b538732cd377e13
Bug: 1195278
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2818022
Commit-Queue: Mikel Astiz <mastiz@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#871053}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2919850
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1651}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/10bd177a4b078b47636c3894daf0f3b5af348733/chrome/browser/ui/bookmarks/bookmark_utils_desktop.cc
[modify] https://crrev.com/10bd177a4b078b47636c3894daf0f3b5af348733/chrome/browser/ui/bookmarks/bookmark_utils_desktop.h
[modify] https://crrev.com/10bd177a4b078b47636c3894daf0f3b5af348733/chrome/browser/ui/views/bookmarks/bookmark_editor_view.cc
[modify] https://crrev.com/10bd177a4b078b47636c3894daf0f3b5af348733/chrome/browser/ui/views/bookmarks/bookmark_editor_view.h
[modify] https://crrev.com/10bd177a4b078b47636c3894daf0f3b5af348733/chrome/browser/ui/views/bookmarks/bookmark_editor_view_unittest.cc


### ja...@google.com (2021-05-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0b4f280e4578b5e185ffc2a3e6d4aebb98869d87

commit 0b4f280e4578b5e185ffc2a3e6d4aebb98869d87
Author: Mikel Astiz <mastiz@chromium.org>
Date: Wed Jun 16 13:02:07 2021

[M90-LTS][bookmarks] Fix UAF if bookmark deleted during modal confirmation dialog

BookmarkEditorView shows a modal dialog when the user requests to delete
a bookmark folder that is non-empty, for the user to confirm. This
involves a nested message loop, which means that additional changes can
take place, including extensions modifying the bookmark tree.

If the bookmark folder being modified by the user happens to be deleted
(e.g. by an extension) while the confirmation dialog is open, prior to
this patch, the code could dereference freed memory.

In this patch, a safeguard is introduced to fix the issue, which is
achieved by detecting problematic changes based on bookmark IDs (which
are integers and never reused during the lifetime of the browser).

(cherry picked from commit a453de0ca590f4341a6d8d32bb5f6525705676de)

Change-Id: Ife1d005f1b3d8d17b5b5d7c07b538732cd377e13
Bug: 1195278
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2818022
Commit-Queue: Mikel Astiz <mastiz@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#871053}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2961090
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1526}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/0b4f280e4578b5e185ffc2a3e6d4aebb98869d87/chrome/browser/ui/bookmarks/bookmark_utils_desktop.cc
[modify] https://crrev.com/0b4f280e4578b5e185ffc2a3e6d4aebb98869d87/chrome/browser/ui/bookmarks/bookmark_utils_desktop.h
[modify] https://crrev.com/0b4f280e4578b5e185ffc2a3e6d4aebb98869d87/chrome/browser/ui/views/bookmarks/bookmark_editor_view.cc
[modify] https://crrev.com/0b4f280e4578b5e185ffc2a3e6d4aebb98869d87/chrome/browser/ui/views/bookmarks/bookmark_editor_view.h
[modify] https://crrev.com/0b4f280e4578b5e185ffc2a3e6d4aebb98869d87/chrome/browser/ui/views/bookmarks/bookmark_editor_view_unittest.cc


### vs...@google.com (2021-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1195278?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055419)*
