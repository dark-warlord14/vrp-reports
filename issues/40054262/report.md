# Security: UAF in Bookmark OpenAll

| Field | Value |
|-------|-------|
| **Issue ID** | [40054262](https://issues.chromium.org/issues/40054262) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>BookmarksBar |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | co...@chromium.org |
| **Created** | 2020-12-22 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

When the number of user bookmarks reaches 15, open all[1] bookmarks and a confirmation box[2] will pop up. The MessageBox will run a nested message loop[3] to continue running the ui thread. If the web content or other related instances are destroyed, the UAF will be triggered after the nested message loops exit.

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/bookmarks/bookmark_utils_desktop.cc;l=113;drc=b0d21f299ba5fd0c51c26f1f440fb1a006fc4753>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/bookmarks/bookmark_utils_desktop.cc;l=73;drc=b0d21f299ba5fd0c51c26f1f440fb1a006fc4753>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/message_box_dialog.cc;l=85;drc=8b5f6ef28dd93e62fc1a75bc7a812af1b33777ec>

**VERSION**  

Chrome Version: stable  

Operating System: Linux, Windows, ChromeOS

**REPRODUCTION CASE**

1. Ensure that the current user has more than 15 bookmarks.
2. $ python -m SimpleHTTPServer  
   
   $ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>" "about:blank"
3. Show bookmarks bar on "poc.html", click the trigger button, right-click the bookmark bar and click "open all".
4. Click yes after the page "poc.html" is closed.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 297 B)
- [BookmarkOpenAll.asan](attachments/BookmarkOpenAll.asan) (application/octet-stream, 16.2 KB)
- [BookmarkOpenAll.asan.txt](attachments/BookmarkOpenAll.asan.txt) (text/plain, 16.2 KB)

## Timeline

### [Deleted User] (2020-12-22)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-22)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-23)

Thanks for the report.

Assigning as Medium as this requires significant user interaction.

There have been few changes to this code for a long time. Adding some bookmarks and tabstrip folks that might know who best to point this towards.

[Monorail components: UI>Browser UI>Browser>TabStrip]

### [Deleted User] (2020-12-23)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2021-01-15)

pkasting@: Can you please help triage this? It appears to be a use-after-free in the browser process, though with some very specific user interaction to trigger it.

### sk...@chromium.org (2021-01-15)

pkasting->tom as tom is removing the nested message loop, which should fix this ( https://chromium-review.googlesource.com/c/chromium/src/+/2622521 ).

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f6658bc4fcfe269c53f8806e02492c658bedb09f

commit f6658bc4fcfe269c53f8806e02492c658bedb09f
Author: Tom Anderson <thomasanderson@chromium.org>
Date: Sat Jan 16 00:59:21 2021

Avoid spinning a nested message loop for X11 clipboard

BUG=443355,1138143,1161141,1161143,1161144,1161145,1161146,1161147,1161149,1161151,1161152

Change-Id: I5c95a9d066683d18f344d694e517274e3ef7ccb4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2622521
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Thomas Anderson <thomasanderson@chromium.org>
Cr-Commit-Position: refs/heads/master@{#844318}

[modify] https://crrev.com/f6658bc4fcfe269c53f8806e02492c658bedb09f/ui/base/x/selection_requestor_unittest.cc
[modify] https://crrev.com/f6658bc4fcfe269c53f8806e02492c658bedb09f/ui/base/x/selection_requestor.cc


### th...@chromium.org (2021-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-16)

Requesting merge to beta M88 because latest trunk commit (844318) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-16)

This bug requires manual review: We are only 2 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2021-01-18)

It is a very effective patch, but this issue is not related to the clipboard. In this issue, the caller of the nested message is |MessageBoxDialog::Show()=>ShowSync()|, so I think thee patch does not take effect for this issue.

### th...@chromium.org (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-01-22)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser -UI>Browser>TabStrip UI>Browser>TopChrome>BookmarksBar]

### co...@chromium.org (2021-01-22)

This seems fundamentally broken. chrome::OpenAll() takes a pointer to the active WebContents (through the PageNavigator interface) and the active Browser window (its gfx::NativeWindow). It runs a nested RunLoop then assumes these pointers are valid afterward. Clearly this doesn't always hold true.

The best fix I can think of is to make OpenAll() and friends non-synchronous and instead run a callback This may require some untangling.

### sk...@chromium.org (2021-01-23)

While tedious, you can observe both Browser (via BrowserListObserver) and WebContents (through WebContentsObserver) being destroyed. You could then abort the open if either are destroyed.

### co...@chromium.org (2021-01-26)

Potential fix at https://chromium-review.googlesource.com/c/chromium/src/+/2650689

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/58ae65c7f9a276777e611db69633b2ff8ed32cb7

commit 58ae65c7f9a276777e611db69633b2ff8ed32cb7
Author: Collin Baker <collinbaker@chromium.org>
Date: Fri Feb 05 21:12:29 2021

Make "open all bookmarks" safe

chrome::OpenAll may prompt the user before opening many bookmarks. It
uses a nested RunLoop to do so. However, it takes as arguments
pointers that may be invalid at the end of this RunLoop.

This CL replaces chrome::OpenAll with chrome::OpenAllIfAllowed, which
returns immediately and opens the tabs asynchronously if prompting the
user. Instead of taking a content::PageNavigator pointer directly, it
takes a callback to fetch the pointer after the user acknowledges the
prompt. This can ensure a valid PageNavigator is used.

Another function chrome::OpenAllImmediately is added for tests which
shouldn't open a message box.

Fixed: 1161144
Change-Id: I6d0d73ec1d9deaf3cb339dc9646d7fe77a27674e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2650689
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Cr-Commit-Position: refs/heads/master@{#851279}

[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.h
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/media/webrtc/desktop_capture_access_handler.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/bookmarks/bookmark_utils_desktop.h
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/bookmarks/bookmark_context_menu_controller.h
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/bookmarks/bookmark_context_menu_controller.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_bar_view.h
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/simple_message_box.h
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_context_menu_unittest.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/bookmarks/bookmark_context_menu_controller_unittest.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_bar_view.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/process_singleton_win.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/webui/chromeos/cellular_setup/mobile_setup_dialog.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_bar_view_test.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_menu_controller_views.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_menu_controller_views.h
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/toolbar/app_menu.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_menu_delegate_unittest.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/message_box_dialog.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_context_menu.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.cc
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/views/bookmarks/bookmark_context_menu.h
[modify] https://crrev.com/58ae65c7f9a276777e611db69633b2ff8ed32cb7/chrome/browser/ui/bookmarks/bookmark_utils_desktop.cc


### co...@chromium.org (2021-02-05)

I can request a merge to 89 after this is verified

### ad...@chromium.org (2021-02-10)

Sheriffbot made a mistake by requesting merge to M88 but not M89, so I'm filling the gap.

That said, I think this is significantly too complex to meet the bar for an M88 merge (as it's only Medium severity). I'd like to merge to M89 in due course, though.

leecraso@, if you get a chance to confirm that this is fixed, that'd be great.

### [Deleted User] (2021-02-10)

This bug requires manual review: M89's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-10)

[Comment Deleted]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-10)

[Comment Deleted]

### le...@gmail.com (2021-02-11)

About c24: Since I'm on vacation, sorry for not responding in time. The patch works well in my test.

### ad...@chromium.org (2021-02-12)

Thanks leecraso@ for https://crbug.com/chromium/1161144#c28.

The merges in https://crbug.com/chromium/1161144#c26 and https://crbug.com/chromium/1161144#c27 are actually unrelated to this bug so I'm deleting those comments (there was a mistake in the bug list within the CL).

### ad...@chromium.org (2021-02-12)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-02-12)

Approving merge to M89, branch 4389. This should be merged along with https://crbug.com/chromium/1176098 which is a problem in the fix.

### ad...@google.com (2021-02-12)

Rejecting merge to M88. This is too complex a change to merge into M88 at this point in the cycle.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b

commit 4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b
Author: Collin Baker <collinbaker@chromium.org>
Date: Fri Feb 12 23:09:35 2021

Make "open all bookmarks" safe

chrome::OpenAll may prompt the user before opening many bookmarks. It
uses a nested RunLoop to do so. However, it takes as arguments
pointers that may be invalid at the end of this RunLoop.

This CL replaces chrome::OpenAll with chrome::OpenAllIfAllowed, which
returns immediately and opens the tabs asynchronously if prompting the
user. Instead of taking a content::PageNavigator pointer directly, it
takes a callback to fetch the pointer after the user acknowledges the
prompt. This can ensure a valid PageNavigator is used.

Another function chrome::OpenAllImmediately is added for tests which
shouldn't open a message box.

(cherry picked from commit 58ae65c7f9a276777e611db69633b2ff8ed32cb7)

Fixed: 1161144
Change-Id: I6d0d73ec1d9deaf3cb339dc9646d7fe77a27674e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2650689
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#851279}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2693629
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4389@{#994}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.h
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/media/webrtc/desktop_capture_access_handler.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/bookmarks/bookmark_utils_desktop.h
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/bookmarks/bookmark_context_menu_controller.h
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/bookmarks/bookmark_context_menu_controller.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_bar_view.h
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/simple_message_box.h
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_context_menu_unittest.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/bookmarks/bookmark_context_menu_controller_unittest.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_bar_view.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/process_singleton_win.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/webui/chromeos/cellular_setup/mobile_setup_dialog.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_bar_view_test.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_menu_controller_views.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_menu_controller_views.h
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/toolbar/app_menu.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_menu_delegate_unittest.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/message_box_dialog.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_context_menu.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.cc
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/views/bookmarks/bookmark_context_menu.h
[modify] https://crrev.com/4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b/chrome/browser/ui/bookmarks/bookmark_utils_desktop.cc


### am...@google.com (2021-02-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-18)

Hello, Leecraso and Guang Gong! The VRP Panel has decided to award you $10,000 for this report. Thank you for this submission and your engagement with this issue!

### aw...@google.com (2021-02-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/77e9baae36b6bf682eaea96931641d7d31ed0f86

commit 77e9baae36b6bf682eaea96931641d7d31ed0f86
Author: Collin Baker <collinbaker@chromium.org>
Date: Tue Mar 09 14:22:02 2021

Make "open all bookmarks" safe

chrome::OpenAll may prompt the user before opening many bookmarks. It
uses a nested RunLoop to do so. However, it takes as arguments
pointers that may be invalid at the end of this RunLoop.

This CL replaces chrome::OpenAll with chrome::OpenAllIfAllowed, which
returns immediately and opens the tabs asynchronously if prompting the
user. Instead of taking a content::PageNavigator pointer directly, it
takes a callback to fetch the pointer after the user acknowledges the
prompt. This can ensure a valid PageNavigator is used.

Another function chrome::OpenAllImmediately is added for tests which
shouldn't open a message box.

[M86 Merge]: Fixed conflics in bookmark_bar_view.*

(cherry picked from commit 58ae65c7f9a276777e611db69633b2ff8ed32cb7)

(cherry picked from commit 4ff0cb3cded4c5a0203e8cf2712a37ef9090f57b)

Fixed: 1161144
Change-Id: I6d0d73ec1d9deaf3cb339dc9646d7fe77a27674e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2650689
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#851279}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2693629
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/4389@{#994}
Cr-Original-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2731650
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1567}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/media/webrtc/desktop_capture_access_handler.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/process_singleton_win.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/bookmarks/bookmark_context_menu_controller.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/bookmarks/bookmark_context_menu_controller.h
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/bookmarks/bookmark_context_menu_controller_unittest.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/bookmarks/bookmark_utils_desktop.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/bookmarks/bookmark_utils_desktop.h
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/simple_message_box.h
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_bar_view.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_bar_view.h
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_bar_view_test.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_context_menu.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_context_menu.h
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_context_menu_unittest.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_menu_controller_views.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_menu_controller_views.h
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.h
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/bookmarks/bookmark_menu_delegate_unittest.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/message_box_dialog.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/views/toolbar/app_menu.cc
[modify] https://crrev.com/77e9baae36b6bf682eaea96931641d7d31ed0f86/chrome/browser/ui/webui/chromeos/cellular_setup/mobile_setup_dialog.cc


### vs...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1161144?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054262)*
