# Heap-use-after-free in CurrentTabDesktopMediaList::Refresh

| Field | Value |
|-------|-------|
| **Issue ID** | [40055159](https://issues.chromium.org/issues/40055159) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-03-12 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36

Steps to reproduce the problem:
1. download chromium asan build (I use 861451) and unzip
2. python -m SimpleHTTPServer 8605
3. ./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/noexit http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html
4. wait for a moment, crash occurs

What is the expected behavior?

What went wrong?
In file chrome/browser/media/webrtc/desktop_media_list_base.cc:180 function DesktopMediaListBase::ScheduleNextRefreshwill postDelayTask function `Refresh`:
```
void DesktopMediaListBase::ScheduleNextRefresh() {
  DCHECK(!refresh_callback_);
  refresh_callback_ = base::BindOnce(&DesktopMediaListBase::ScheduleNextRefresh,
                                     weak_factory_.GetWeakPtr());
  content::GetUIThreadTaskRunner({})->PostDelayedTask(
      FROM_HERE,
      base::BindOnce(&DesktopMediaListBase::Refresh, weak_factory_.GetWeakPtr(),
                     true),
      update_period_);
}
```

While in file chrome/browser/media/webrtc/current_tab_desktop_media_list.cc:125 , function `Refresh` will use `view_`, it can be destroyed if we close the popup window(shared window). 
So, if we close the popup window(the shared window), when there are still some tasks in queue, it will trigger UAF

```
void CurrentTabDesktopMediaList::Refresh(bool update_thumnails) {
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);
  DCHECK(can_refresh());

  if (refresh_in_progress_ || !update_thumnails || thumbnail_size_.IsEmpty()) {
    return;
  }

  refresh_in_progress_ = true;

  auto reply = base::BindOnce(&CurrentTabDesktopMediaList::OnCaptureHandled,
                              weak_factory_.GetWeakPtr());

  view_->CopyFromSurface(
      gfx::Rect(), gfx::Size(),
      base::BindPostTask(thumbnail_task_runner_,
                         base::BindOnce(&HandleCapturedBitmap, std::move(reply),  // reply is a callback to ScheduleNextRefresh
                                        last_hash_, thumbnail_size_)));
}
```

To make this more stable, I open the poc many many times. If you can not reproduce, open more.

Did this work before? N/A 

Chrome version: 88.0.4324.190  Channel: n/a
OS Version: ubuntu
Flash Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 15.9 KB)
- [video.webm](attachments/video.webm) (video/webm, 4.3 MB)

## Timeline

### [Deleted User] (2021-03-12)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-03-14)

tommi: Could you PTAL? 

This is a UAF in the browser process but it requires significant user interaction (opening a large number of tabs), so I'm marking it as High severity instead of a potential Critical.

[Monorail components: Blink>WebRTC]

### te...@chromium.org (2021-03-15)

Elad, could you take a look at this?

### el...@chromium.org (2021-03-15)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-03-15)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-03-15)

I can reproduce.

### [Deleted User] (2021-03-15)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8854b89b2b774eb0644e58fab328f307c6d45920

commit 8854b89b2b774eb0644e58fab328f307c6d45920
Author: Elad Alon <eladalon@chromium.org>
Date: Mon Mar 15 21:50:30 2021

Fix UAF in CurrentTabDesktopMediaList

Avoid caching RenderWidgetHostView.

Bug: 1187403
Change-Id: Ied433eb2fc1daa9605e650ef1ce227a9caf94d6f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2761137
Commit-Queue: Elad Alon <eladalon@chromium.org>
Auto-Submit: Elad Alon <eladalon@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/master@{#862977}

[modify] https://crrev.com/8854b89b2b774eb0644e58fab328f307c6d45920/chrome/browser/media/webrtc/current_tab_desktop_media_list.cc
[modify] https://crrev.com/8854b89b2b774eb0644e58fab328f307c6d45920/chrome/browser/media/webrtc/current_tab_desktop_media_list.h
[modify] https://crrev.com/8854b89b2b774eb0644e58fab328f307c6d45920/chrome/browser/media/webrtc/current_tab_desktop_media_list_unittest.cc


### el...@chromium.org (2021-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-16)

This bug requires manual review: M90's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2021-03-16)

1. Does your merge fit within the Merge Decision Guidelines?
Yes. This is a high-impact bug (can crash the browser), but the feature is gated behind an origin-trial. User functionality is not changed.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2761137

3. Has the change landed and been verified on ToT?
Yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?
No.

5. Why are these changes required in this milestone after branch?
The browser-crashing regression was only discovered in this milstone (M90).

6. Is this a new feature?
Yes and no. It was behind a flag up to M89, and is OT-gated starting with M90.

7. If it is a new feature, is it behind a flag using finch?
It's is behind an origin-trial. There is also a Finch killswitch - https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/common/features.cc;l=197-200;drc=bbab952d59f344f0e7c458b7e877a24eb38ec15b

### sr...@google.com (2021-03-16)

Merge approved for M90 branch:4430

### gi...@appspot.gserviceaccount.com (2021-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8130f8f14b371080d4dc6ffd082491f5a645386f

commit 8130f8f14b371080d4dc6ffd082491f5a645386f
Author: Elad Alon <eladalon@chromium.org>
Date: Wed Mar 17 00:31:48 2021

Fix UAF in CurrentTabDesktopMediaList

Avoid caching RenderWidgetHostView.

(cherry picked from commit 8854b89b2b774eb0644e58fab328f307c6d45920)

Bug: 1187403
Change-Id: Ied433eb2fc1daa9605e650ef1ce227a9caf94d6f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2761137
Commit-Queue: Elad Alon <eladalon@chromium.org>
Auto-Submit: Elad Alon <eladalon@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#862977}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2764511
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4430@{#531}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/8130f8f14b371080d4dc6ffd082491f5a645386f/chrome/browser/media/webrtc/current_tab_desktop_media_list.cc
[modify] https://crrev.com/8130f8f14b371080d4dc6ffd082491f5a645386f/chrome/browser/media/webrtc/current_tab_desktop_media_list.h
[modify] https://crrev.com/8130f8f14b371080d4dc6ffd082491f5a645386f/chrome/browser/media/webrtc/current_tab_desktop_media_list_unittest.cc


### el...@chromium.org (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-23)

As a high severity security fix, we'd normally merge this back to the current stable branch (M89).

https://crbug.com/chromium/1187403#c11 says this was behind a flag prior to M90, however, the original report gives an M88 user agent and doesn't set any flags. On the other hand, the report says it was asan build 861451 which is M90 territory, so I suspect the user agent is wrong.

It looks to me like:
* this feature was disabled by default prior to M90
* it's checked in the browser process, not the renderer process

As such I'm marking as Security_Impact-Beta and not requesting merge back to M89, but if either of those statements is wrong please let me know.

### el...@chromium.org (2021-03-23)

M89 branched on Jan 14. Up until then, it was behind a command-line flag.
On Feb 24, this CL introduced the origin-trial: https://chromium-review.googlesource.com/c/chromium/src/+/2712823
On Feb 25, this CL changed the kill-switch from default-off to default-on: https://chromium-review.googlesource.com/c/chromium/src/+/2720204

### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-24)

And another one! Congratulations, merc.ouc@ - the VRP Panel has decided to award you $15,000 for this report. Neat find and good reporting! 

### el...@chromium.org (2021-03-24)

Thank you for finding this!

### me...@gmail.com (2021-03-25)

My pleasure:)

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1187403?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055159)*
