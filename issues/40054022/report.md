# Security: UAF in Drag-and-drop

| Field | Value |
|-------|-------|
| **Issue ID** | [40054022](https://issues.chromium.org/issues/40054022) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI |
| **Platforms** | Linux |
| **Reporter** | le...@gmail.com |
| **Assignee** | ad...@igalia.com |
| **Created** | 2020-11-30 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

|source\_client\_|[1] keep a raw pointer of XDragDropClient[2]. And it could be accessed[3] when handling dispatched events even after the source window has been destroyed.

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_context.h;l=78;drc=0c59d7a7073f14e600491fd2eba187f5684c3224;bpv=0;bpt=0>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_drop_client.cc;l=309;drc=2a460ccaa47f04efefa45cc127aa57cc51a999b7>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_context.cc;l=173;drc=d2169dbe1a3c4162e7b25550181ac261e0f26287>

**VERSION**  

Chrome Version: stable  

Operating System: Linux, Chrome OS

**REPRODUCTION CASE**  

$ python -m SimpleHTTPServer  

$ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"  

Drag and drop the picture.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 14.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)
- [render.patch](attachments/render.patch) (text/plain, 4.0 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 377 B)

## Timeline

### [Deleted User] (2020-11-30)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-12-01)

Security sheriff: I can reproduce this with a linux ASAN release build but not a debug build, although it took me a couple tries. Setting some initial labels: This looks like a UAF in the browser process, but it requires user interaction to trigger so it doesn't seem like it would be exploitable in a drive-by fashion, so setting Severity-High. Reporter: I'd be interested if you can think of a way to reduce or remove the user interaction requirement (with our without a compromised renderer), which might make this a Sev-Critical.

thomasanderson@ could you PTAL? Also cc'ing adunaev@ who also appears active in x11_drag_drop_client.cc.

[Monorail components: UI]

### th...@chromium.org (2020-12-01)

Over to adunaev@

### le...@gmail.com (2020-12-02)

@cthomp: 

With a compromised renderer, the bug can be easily triggered through |StartDragging|-IPC[1] without any user interaction. I uploaded a renderer patch and poc to do this. 

Without a compromised renderer, I have no idea how to completely remove the user interaction. But I think the drag-and-drop is a very common operation when users browse the web, it can happen to not only images but also other elements such as text and links.

[1]. https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/public/mojom/page/widget.mojom;l=191;drc=32b38e9faec44c50ad28f9c592e7ca6a0d1ec7e1

### ad...@igalia.com (2020-12-02)

[Empty comment from Monorail migration]

### ad...@igalia.com (2020-12-02)

Thank you for the details.  I am working on a fix.

I wonder if the issue existed before M81, which is the first release that had changes in the DnD on Linux/X11.  At a brief glance, the logic around using the |source_client_| was the same before those changes, so probably the vulnerability was available too.  @cthomp, could you please either try it on M80 or provide some hints how I could do that myself?

### ct...@chromium.org (2020-12-02)

Testing:
- r722276 (roughly M80): Can't reproduce
- r737177 (roughly M81): Can't reproduce
- r775683 (which includes crrev.com/c/2209132): Can't reproduce
- r783262 (which includes crrev.com/c/2265393): Can't reproduce

Bisecting manually a bit further:
- r812852 (M87 Stable): Can reproduce
- r800441: Can reproduce
- r791843: Can't reproduce
- r796142: Can reproduce
- r793992: Can reproduce
- r792933: Can't reproduce
- r793458: Can reproduce
- r793191: Can reproduce
- r793062: Can reproduce
- r792997: Can’t reproduce
- r793029: Can reproduce
- r793013: Can’t reproduce
- r793020: Can’t reproduce

That gives a regression range of https://chromium.googlesource.com/chromium/src/+log/be4c444017c88d95a3ef03cce585ba34b0e78cee..f506af438fbf0913856f9e896732dd0451252f30

Which points to https://chromium.googlesource.com/chromium/src/+/f506af438fbf0913856f9e896732dd0451252f30 (Reland "[ozone/x11] Removed DesktopWindowTreeHostX11 and its DnD client.”), which was in  86.0.4218.0.

(For reference, I generally use a combination of looking up old branch revision numbers and then grabbing ASAN builds from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html to repro bugs that require ASAN builds. Unfortunately I don't think there's an easy way to run bisect-builds.py on ASAN builds, so this was manual bisection. If this didn't require user interaction, then I'd just plug it into Clusterfuzz which would generate a regression range.)

### ad...@igalia.com (2020-12-03)

Thank you!

The fix is at review: https://chromium-review.googlesource.com/c/chromium/src/+/2567229

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9eeb09a73570ffaed6f7caea95912a9ffface755

commit 9eeb09a73570ffaed6f7caea95912a9ffface755
Author: Alexander Dunaev <adunaev@igalia.com>
Date: Fri Dec 04 02:49:22 2020

[x11] Fixed UAF in drag and drop.

To short-cut round trips to the X server when drag and drop happens
between two Chromium windows, XDragContext stored the raw pointer to
XDragDropClient of the source window in its source_client_ attribute.
This made possible to access the deleted object (use after free) if the
source window had been destroyed during the operation.  In short,
although the target context can call the source client directly via the
shortcut, the PropertyNotify event comes from the X server (not using
the shortcut), and apparently it can come to the target context after
the source window and its client had been destroyed but before the
target context is notified.  See the issue for full details.

Here the XDragContext::source_client_ is removed, and all its uses
are replaced with getting the client from the global map of clients
[1]. The client removes itself from the map upon destruction [2] so
this change eliminates the vulnerability.

For the record, there is the test in the interactive_ui_tests suite
(namely BookmarkBarViewTest22.CloseSourceBrowserDuringDrag) that should
emulate this situation but is has some flaws [3].

[1] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_drop_client.cc;l=120
[2] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_drop_client.cc;l=200
[3] https://crbug.com/1106379

Bug: 1153595
Change-Id: Ibb875cb4fa04ddfa8f99b39e4dab654048da86c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567229
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Alexander Dunaev <adunaev@igalia.com>
Cr-Commit-Position: refs/heads/master@{#833577}

[modify] https://crrev.com/9eeb09a73570ffaed6f7caea95912a9ffface755/ui/base/x/x11_drag_context.cc
[modify] https://crrev.com/9eeb09a73570ffaed6f7caea95912a9ffface755/ui/base/x/x11_drag_context.h
[modify] https://crrev.com/9eeb09a73570ffaed6f7caea95912a9ffface755/ui/base/x/x11_drag_drop_client.cc
[modify] https://crrev.com/9eeb09a73570ffaed6f7caea95912a9ffface755/ui/base/x/x11_drag_drop_client.h
[modify] https://crrev.com/9eeb09a73570ffaed6f7caea95912a9ffface755/ui/platform_window/x11/x11_window.cc


### ad...@igalia.com (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

Requesting merge to stable M87 because latest trunk commit (833577) appears to be after stable branch point (812852).

Requesting merge to beta M88 because latest trunk commit (833577) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-05)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-12-07)

Approving merge to M88, branch 4324.

### ad...@google.com (2020-12-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-10)

Congratulations, the VRP panel has awarded $20,000 for this bug.

### ad...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-12-11)

adunaev@igalia.com please answer https://crbug.com/chromium/1153595#c14 or at least more generally comment on any stability risks from this merge.

### ad...@igalia.com (2020-12-14)

My apologies for not commenting right away.

1. This merge partially fits the Merge Decision Guidelines.  It does not introduce regressions, and it is covered by unit tests, but it is known that the test is flawed (an issue for fixing the test does exist: https://bugs.chromium.org/p/chromium/issues/detail?id=1106379).
2. https://chromium-review.googlesource.com/c/chromium/src/+/2567229
3. The patch has been landed on ToT, but it was not yet confirmed by the reporter that the issue is fixed.
4. Yes.
5. This merge fixes the vulnerability.
6. No.
7. No.

### sr...@google.com (2020-12-14)

Please help complete the merges before end of day Monday dec 14, (PST). The final beta release candidate will be cut during tuesday Dec 15 and I would like to include all these merges in. This will be the last beta release for this year ( no releases for 2 weeks)

### ad...@igalia.com (2020-12-14)

The cherry-pick to M88 is here: https://chromium-review.googlesource.com/c/chromium/src/+/2588338

Waiting for thomasanderson@ to approve.

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4609f29534df2ce025a5389ce6b334ad6a5cce46

commit 4609f29534df2ce025a5389ce6b334ad6a5cce46
Author: Alexander Dunaev <adunaev@igalia.com>
Date: Mon Dec 14 18:55:03 2020

[x11] Fixed UAF in drag and drop.

To short-cut round trips to the X server when drag and drop happens
between two Chromium windows, XDragContext stored the raw pointer to
XDragDropClient of the source window in its source_client_ attribute.
This made possible to access the deleted object (use after free) if the
source window had been destroyed during the operation.  In short,
although the target context can call the source client directly via the
shortcut, the PropertyNotify event comes from the X server (not using
the shortcut), and apparently it can come to the target context after
the source window and its client had been destroyed but before the
target context is notified.  See the issue for full details.

Here the XDragContext::source_client_ is removed, and all its uses
are replaced with getting the client from the global map of clients
[1]. The client removes itself from the map upon destruction [2] so
this change eliminates the vulnerability.

For the record, there is the test in the interactive_ui_tests suite
(namely BookmarkBarViewTest22.CloseSourceBrowserDuringDrag) that should
emulate this situation but is has some flaws [3].

[1] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_drop_client.cc;l=120
[2] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_drop_client.cc;l=200
[3] https://crbug.com/1106379

(cherry picked from commit 9eeb09a73570ffaed6f7caea95912a9ffface755)

Bug: 1153595
Change-Id: Ibb875cb4fa04ddfa8f99b39e4dab654048da86c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567229
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Alexander Dunaev <adunaev@igalia.com>
Cr-Original-Commit-Position: refs/heads/master@{#833577}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2588338
Auto-Submit: Alexander Dunaev <adunaev@igalia.com>
Commit-Queue: Thomas Anderson <thomasanderson@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#904}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/4609f29534df2ce025a5389ce6b334ad6a5cce46/ui/base/x/x11_drag_drop_client.cc
[modify] https://crrev.com/4609f29534df2ce025a5389ce6b334ad6a5cce46/ui/platform_window/x11/x11_window.cc
[modify] https://crrev.com/4609f29534df2ce025a5389ce6b334ad6a5cce46/ui/base/x/x11_drag_drop_client.h
[modify] https://crrev.com/4609f29534df2ce025a5389ce6b334ad6a5cce46/ui/base/x/x11_drag_context.cc
[modify] https://crrev.com/4609f29534df2ce025a5389ce6b334ad6a5cce46/ui/base/x/x11_drag_context.h


### ad...@google.com (2020-12-15)

Approving merge to M87, branch 4280.

### ad...@igalia.com (2020-12-16)

The cherry-pick to M87 is here: https://chromium-review.googlesource.com/c/chromium/src/+/2593613

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/36aba5e75bfddda35e8088a9c23e08f8940694f9

commit 36aba5e75bfddda35e8088a9c23e08f8940694f9
Author: Alexander Dunaev <adunaev@igalia.com>
Date: Wed Dec 16 03:51:31 2020

[x11] Fixed UAF in drag and drop.

To short-cut round trips to the X server when drag and drop happens
between two Chromium windows, XDragContext stored the raw pointer to
XDragDropClient of the source window in its source_client_ attribute.
This made possible to access the deleted object (use after free) if the
source window had been destroyed during the operation.  In short,
although the target context can call the source client directly via the
shortcut, the PropertyNotify event comes from the X server (not using
the shortcut), and apparently it can come to the target context after
the source window and its client had been destroyed but before the
target context is notified.  See the issue for full details.

Here the XDragContext::source_client_ is removed, and all its uses
are replaced with getting the client from the global map of clients
[1]. The client removes itself from the map upon destruction [2] so
this change eliminates the vulnerability.

For the record, there is the test in the interactive_ui_tests suite
(namely BookmarkBarViewTest22.CloseSourceBrowserDuringDrag) that should
emulate this situation but is has some flaws [3].

[1] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_drop_client.cc;l=120
[2] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_drop_client.cc;l=200
[3] https://crbug.com/1106379

(cherry picked from commit 9eeb09a73570ffaed6f7caea95912a9ffface755)

Bug: 1153595
Change-Id: Ibb875cb4fa04ddfa8f99b39e4dab654048da86c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567229
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Alexander Dunaev <adunaev@igalia.com>
Cr-Original-Commit-Position: refs/heads/master@{#833577}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2593613
Reviewed-by: Alexander Dunaev <adunaev@igalia.com>
Cr-Commit-Position: refs/branch-heads/4280@{#1890}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/36aba5e75bfddda35e8088a9c23e08f8940694f9/ui/base/x/x11_drag_drop_client.cc
[modify] https://crrev.com/36aba5e75bfddda35e8088a9c23e08f8940694f9/ui/platform_window/x11/x11_window.cc
[modify] https://crrev.com/36aba5e75bfddda35e8088a9c23e08f8940694f9/ui/base/x/x11_drag_drop_client.h
[modify] https://crrev.com/36aba5e75bfddda35e8088a9c23e08f8940694f9/ui/base/x/x11_drag_context.cc
[modify] https://crrev.com/36aba5e75bfddda35e8088a9c23e08f8940694f9/ui/base/x/x11_drag_context.h


### ad...@google.com (2021-01-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1752fe9fd96012e365e03b8ea97b63c247734603

commit 1752fe9fd96012e365e03b8ea97b63c247734603
Author: Alexander Dunaev <adunaev@igalia.com>
Date: Sat Jan 09 19:56:54 2021

[x11] Fixed UAF in drag and drop.

To short-cut round trips to the X server when drag and drop happens
between two Chromium windows, XDragContext stored the raw pointer to
XDragDropClient of the source window in its source_client_ attribute.
This made possible to access the deleted object (use after free) if the
source window had been destroyed during the operation.  In short,
although the target context can call the source client directly via the
shortcut, the PropertyNotify event comes from the X server (not using
the shortcut), and apparently it can come to the target context after
the source window and its client had been destroyed but before the
target context is notified.  See the issue for full details.

Here the XDragContext::source_client_ is removed, and all its uses
are replaced with getting the client from the global map of clients
[1]. The client removes itself from the map upon destruction [2] so
this change eliminates the vulnerability.

For the record, there is the test in the interactive_ui_tests suite
(namely BookmarkBarViewTest22.CloseSourceBrowserDuringDrag) that should
emulate this situation but is has some flaws [3].

[1] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_drop_client.cc;l=120
[2] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/x11_drag_drop_client.cc;l=200
[3] https://crbug.com/1106379

(cherry picked from commit 9eeb09a73570ffaed6f7caea95912a9ffface755)

(cherry picked from commit 36aba5e75bfddda35e8088a9c23e08f8940694f9)

Bug: 1153595
Change-Id: Ibb875cb4fa04ddfa8f99b39e4dab654048da86c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567229
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Alexander Dunaev <adunaev@igalia.com>
Cr-Original-Original-Commit-Position: refs/heads/master@{#833577}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2593613
Reviewed-by: Alexander Dunaev <adunaev@igalia.com>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#1890}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617101
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1502}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/1752fe9fd96012e365e03b8ea97b63c247734603/ui/base/x/x11_drag_drop_client.cc
[modify] https://crrev.com/1752fe9fd96012e365e03b8ea97b63c247734603/ui/platform_window/x11/x11_window.cc
[modify] https://crrev.com/1752fe9fd96012e365e03b8ea97b63c247734603/ui/base/x/x11_drag_drop_client.h
[modify] https://crrev.com/1752fe9fd96012e365e03b8ea97b63c247734603/ui/base/x/x11_drag_context.cc
[modify] https://crrev.com/1752fe9fd96012e365e03b8ea97b63c247734603/ui/base/x/x11_drag_context.h


### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xp...@gmail.com (2022-08-11)

Sorry to bother, but can https://crbug.com/chromium/1153595#c4's attachments be undeleted? Thank you.

### le...@gmail.com (2022-08-12)

c37: Done.

### is...@google.com (2022-08-12)

This issue was migrated from crbug.com/chromium/1153595?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054022)*
