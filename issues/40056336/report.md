# Security: HeapOverflow in BookmarkBarView

| Field | Value |
|-------|-------|
| **Issue ID** | [40056336](https://issues.chromium.org/issues/40056336) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Bookmarks |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2021-06-25 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

When dragging a bookmark in the bookmark bar, the index of drop position will be stored in |drop\_info\_|[1]. If you delete a bookmark or folder while dragging, the index info in |drop\_info\_| will not be updated, but the size of |bookmark\_buttons\_|[2] will change. So if the size of |bookmark\_buttons\_| becomes littler than the index, the OOB will be triggered.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/bookmark_bar_view.cc;l=911;drc=5e62be9524a33b05cd6349fcb1b050b47a3a8fbc;bpv=0;bpt=0>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/bookmark_bar_view.cc;l=926;drc=5e62be9524a33b05cd6349fcb1b050b47a3a8fbc;bpv=0;bpt=0>

**VERSION**  

Chrome Version: stable  

Operating System: All

**REPRODUCTION CASE**

1. Install the extension.
2. Drag the bookmark in the folder out of the folder, and drop it after the folder is deleted.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 15.1 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 172 B)
- [poc.js](attachments/poc.js) (text/plain, 366 B)
- [Demo.mp4](attachments/Demo.mp4) (video/mp4, 2.4 MB)

## Timeline

### [Deleted User] (2021-06-25)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-06-25)

Thank you for the poc, video, asan report, and diagnosis! ellyjones@ can you take a look at this one?

Marking as Low severity since extension memory corruption is medium severity and the poc requires the extension to delete a bookmark while the icon is being dragged.

[Monorail components: UI>Browser>Bookmarks]

### [Deleted User] (2021-06-25)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-06-25)

-> sky@ from //c/b/ui/views/bookmarks OWNERS :)

### sk...@chromium.org (2021-06-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f338ed52643716938d2bdb2c8c6e2699cd8789c5

commit f338ed52643716938d2bdb2c8c6e2699cd8789c5
Author: Scott Violet <sky@chromium.org>
Date: Wed Jun 30 17:10:23 2021

bookmarks: reset drop info if model changes during drag

This makes BookmarkBarView invalidate drop information if
the model changes during the drag. This is necessary as
BookmarkBarView caches model information during the drag that
is likely incorrect if the model changes. As model changes during a
drop are infrequent, I did not try to validate the old index, and
instead drop the information. If the mouse/touch moves again, the drop
data will be validated again.

BUG=1223667
TEST=BookmarkBarViewTest.MutateModelDuringDrag

Change-Id: I1489a6baf9b46092213ac371e7b30e37db31b0bf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2993159
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/master@{#897422}

[modify] https://crrev.com/f338ed52643716938d2bdb2c8c6e2699cd8789c5/chrome/browser/ui/views/bookmarks/bookmark_bar_view.cc
[modify] https://crrev.com/f338ed52643716938d2bdb2c8c6e2699cd8789c5/chrome/browser/ui/views/bookmarks/bookmark_bar_view.h
[modify] https://crrev.com/f338ed52643716938d2bdb2c8c6e2699cd8789c5/chrome/browser/ui/views/bookmarks/bookmark_bar_view_test_helper.h
[modify] https://crrev.com/f338ed52643716938d2bdb2c8c6e2699cd8789c5/chrome/browser/ui/views/bookmarks/bookmark_bar_view_unittest.cc


### sk...@chromium.org (2021-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-01)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-19)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $10,000 for this report. Nice work! 

### am...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-10-07)

This issue was migrated from crbug.com/chromium/1223667?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056336)*
