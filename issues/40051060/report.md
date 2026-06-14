# Security: Full screen notification overlap on Windows and Linux

| Field | Value |
|-------|-------|
| **Issue ID** | [40051060](https://issues.chromium.org/issues/40051060) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2019-12-24 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 81.0.4005.0 (Official Build) canary (64-bit)  

Operating System: Windows and Linux

**REPRODUCTION CASE**  

Similar to <https://crbug.com/chromium/752003>.

- Please allow pop-ups from index.html

1. Lunch index.html
2. Click on the button
3. Click on the button

A popup can show up over fullscreen mode and hide the fullscreen notification.

## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 587.8 KB)
- [index.html](attachments/index.html) (text/plain, 171 B)
- [fullscreen.html](attachments/fullscreen.html) (text/plain, 102 B)

## Timeline

### ad...@google.com (2019-12-26)

chromium.khalil@, is this different from https://crbug.com/chromium/1020026? Do you have reason to believe it's a different root cause or wouldn't be covered by the fix for that issue? If so, why? Thanks!

### ch...@gmail.com (2019-12-26)

https://crbug.com/chromium/1020026 doesn't repro on Linux, while this issue does repro on both Linux and Windows, I'm actually not sure if https://crbug.com/chromium/1020026 will fix this bug.

### sh...@chromium.org (2019-12-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-12-27)

Thanks. I'll send it in the same direction and avi@ can determine if it's a duplicate.

I had difficulty reproducing this, but eventually succeeded. I used a dev build on Linux (81.0.4000.3) and the latest stable build on OS X (79.0.3945.88).

I did this:
1. Saved both HTML files to my download location
2. Opened index.html
3. Clicked the button(s) a couple of times, I can't remember if it was one or both
4. Closed tabs until I saw the "pop-up blocked" notification and then allowed popups
5. Started again
6. The key thing it took me a while to figure out: you have to click both buttons IN QUICK SUCCESSION or it doesn't work. Click the first button, do not wait for the second page obviously to load, just immediately click again.
7. On Linux I found that the full-screen notification was only partially masked but that's just a screen geometry thing.

I'm tentatively marking this as Medium like https://crbug.com/chromium/10200026 but, if the two clicks and the pop-up unblocking are both necessary parts of the attack, then I'd rate this as Low. Marking as impact stable since I could reproduce a problem on 79.

[Monorail components: UI>Browser>FullScreen]

### ad...@google.com (2019-12-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-27)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-07)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-21)

avi: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d1d25656154f09c4c7a689aaa2df0044d5e02f93

commit d1d25656154f09c4c7a689aaa2df0044d5e02f93
Author: Avi Drissman <avi@chromium.org>
Date: Fri Mar 06 21:28:58 2020

Prevent fullscreen while dialogs are up (1/2)

Chromium already drops fullscreen when a dialog is first displayed.
Extend that behavior so that a WebContents may not enter fullscreen
for the duration of a dialog's display.

This is part 1: Extend the fullscreen IPC so that the browser can
decline a renderer's request to enter fullscreen.

Bug: 1042210, 1020026, 1037730
Change-Id: Iafba087b22c51bf3c8fb6f9a4ce02921d51f0044
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2041871
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#747870}

[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/frame_host/render_frame_host_delegate.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/frame_host/render_frame_host_delegate.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/frame_host/render_frame_host_impl.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/screen_orientation/screen_orientation_provider_unittest.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/web_contents/web_contents_impl_unittest.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/public/mojom/frame/frame.mojom
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/frame/fullscreen_controller.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/frame/fullscreen_controller.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/fullscreen/fullscreen.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/fullscreen/fullscreen.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/html/media/html_media_element_event_listeners_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/html/media/html_video_element_persistent_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/html/media/video_auto_fullscreen_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/testing/fake_local_frame_host.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/testing/fake_local_frame_host.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/modules/media_controls/elements/media_control_display_cutout_fullscreen_button_element_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/modules/media_controls/media_controls_display_cutout_delegate_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/modules/media_controls/media_controls_orientation_lock_delegate_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/modules/media_controls/media_controls_rotate_to_fullscreen_delegate_test.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee

commit 1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee
Author: Avi Drissman <avi@chromium.org>
Date: Tue Mar 10 18:56:45 2020

Prevent fullscreen while dialogs are up (2/2)

Chromium already drops fullscreen when a dialog is first displayed.
Extend that behavior so that a WebContents may not enter fullscreen
for the duration of a dialog's display.

This is part 2: Modify WebContents::ForSecurityDropFullscreen() to
support a span of time that fullscreen is prohibited and modify all
callers to correctly request that span.

Bug: 1042210, 1020026, 1037730
Change-Id: I9d2ccc1e459cf37bfbf3499063d87d93ef9910e8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2044658
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#748808}

[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/custom_handlers/register_protocol_handler_permission_request.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/custom_handlers/register_protocol_handler_permission_request.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/chrome_native_file_system_permission_context.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/native_file_system_permission_request_manager.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/native_file_system_permission_request_manager.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/origin_scoped_native_file_system_permission_context.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/tab_scoped_native_file_system_permission_context.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/permissions/permission_request_manager_browsertest.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/browser.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/native_file_system_dialogs.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/native_file_system_dialogs.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/views/native_file_system/native_file_system_directory_access_confirmation_view.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/views/native_file_system/native_file_system_directory_access_confirmation_view.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/views/native_file_system/native_file_system_directory_access_confirmation_view_browsertest.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/BUILD.gn
[add] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/file_chooser_impl.cc
[add] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/file_chooser_impl.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/render_frame_host_delegate.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/render_frame_host_delegate.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/native_file_system/file_system_chooser.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/native_file_system/file_system_chooser.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/native_file_system/file_system_chooser_unittest.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/native_file_system/native_file_system_manager_impl.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/public/browser/web_contents.h


### av...@chromium.org (2020-03-10)

I believe these changes should fix this. PTAL and let me know.

### av...@chromium.org (2020-03-19)

Let me know if it doesn’t fix it.

### [Deleted User] (2020-03-19)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-23)

Requesting merge to beta M81 because latest trunk commit (748808) appears to be after beta branch point (737173).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-23)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2020-03-23)

No, sheriffbot. This is too complicated to merge.

### na...@google.com (2020-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-26)

Congrats! The Panel decided to award $500 for this report! 

### na...@google.com (2020-03-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-06-03)

This seems like still repro Canary 85.0.4163.0.

### ad...@google.com (2020-06-03)

Raised https://crbug.com/chromium/1090835 for the new recurrence of this.

### av...@chromium.org (2020-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1037730?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051060)*
