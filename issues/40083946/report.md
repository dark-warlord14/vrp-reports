# Security: Universal XSS via the interception of |Binding| with Object.prototype.create

| Field | Value |
|-------|-------|
| **Issue ID** | [40083946](https://issues.chromium.org/issues/40083946) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Reporter** | ma...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-03-26 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

The fix for <https://crbug.com/chromium/590118> is insufficient to protect against bindings interception. While they can't be accessed by triggering accessors on the |modules| object anymore, it's still possible to trap the set operation for |Binding.create| using Object.prototype.create. The obtained constructor can then be used to take over the the built-in extensions system and gain access to native functions.

**VERSION**  

Chrome 49.0.2623.108 (Stable)  

Chrome 50.0.2661.49 (Beta)  

Chrome 51.0.2687.0 (Dev)  

Chromium 51.0.2692.0 + Pepper Flash (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 4.0 KB)

## Timeline

### mb...@chromium.org (2016-03-29)

Adding ccs from https://crbug.com/chromium/590118.

[Monorail components: Platform>Extensions]

### rd...@chromium.org (2016-03-29)

I can only get this to repro up to the point of hijacking the extension bindings, not to a full uxss - am I missing something?  (Obviously, hijacking the bindings is still Bad.)

### ma...@gmail.com (2016-03-29)

Do you run it from a HTTP server?

### cl...@chromium.org (2016-03-29)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-03-29)

@3 - a python SimpleHTTPServer running on localhost, which I'd assume would be sufficient?

### ma...@gmail.com (2016-03-29)

Yes, it should. I haven't seen this exploit fail, I get the alert for https://abc.xyz every single time I run it (Windows/Linux/VM/no VM, different versions), no matter how many tries or reloads. It uses a Flash object, so please check that it isn't blocked (console.log('works') inside function f() should do). I'll send you a debug version to figure out what's wrong exactly.

### rd...@chromium.org (2016-03-29)

@6 Just tried it again and got it working - I think I had tried with flash, and with a server, but forgot to try both.  Thanks!

### sh...@chromium.org (2016-03-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cbad917fdd9651eb9afd723a81c9d2ab437ce03d

commit cbad917fdd9651eb9afd723a81c9d2ab437ce03d
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 01 17:14:45 2016

[Extensions] Add an access check before executing native code in the renderer

Sometimes things can intercept bindings. Check access before doing anything.
This is a first step that just adds it for the test API.

BUG=598165

Review URL: https://codereview.chromium.org/1843803002

Cr-Commit-Position: refs/heads/master@{#384614}

[modify] https://crrev.com/cbad917fdd9651eb9afd723a81c9d2ab437ce03d/extensions/renderer/object_backed_native_handler.cc
[modify] https://crrev.com/cbad917fdd9651eb9afd723a81c9d2ab437ce03d/extensions/renderer/object_backed_native_handler.h
[modify] https://crrev.com/cbad917fdd9651eb9afd723a81c9d2ab437ce03d/extensions/renderer/script_context.cc
[modify] https://crrev.com/cbad917fdd9651eb9afd723a81c9d2ab437ce03d/extensions/renderer/user_gestures_native_handler.cc


### bu...@chromium.org (2016-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/14ff9d0cded8ae8032ef027d1f33c6666a695019

commit 14ff9d0cded8ae8032ef027d1f33c6666a695019
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Tue Apr 05 20:56:55 2016

[Extensions] Add more bindings access checks

BUG=598165

Review URL: https://codereview.chromium.org/1854983002

Cr-Commit-Position: refs/heads/master@{#385282}

[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/automation_internal_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/cast_streaming_native_handler.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/file_browser_handler_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/file_browser_handler_custom_bindings.h
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/file_manager_private_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/file_manager_private_custom_bindings.h
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/media_galleries_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/notifications_native_handler.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/page_capture_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/resources/extensions/file_manager_private_custom_bindings.js
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/extensions/renderer/object_backed_native_handler.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/extensions/renderer/object_backed_native_handler.h


### bu...@chromium.org (2016-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/14ff9d0cded8ae8032ef027d1f33c6666a695019

commit 14ff9d0cded8ae8032ef027d1f33c6666a695019
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Tue Apr 05 20:56:55 2016

[Extensions] Add more bindings access checks

BUG=598165

Review URL: https://codereview.chromium.org/1854983002

Cr-Commit-Position: refs/heads/master@{#385282}

[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/automation_internal_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/cast_streaming_native_handler.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/file_browser_handler_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/file_browser_handler_custom_bindings.h
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/file_manager_private_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/file_manager_private_custom_bindings.h
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/media_galleries_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/notifications_native_handler.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/extensions/page_capture_custom_bindings.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/chrome/renderer/resources/extensions/file_manager_private_custom_bindings.js
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/extensions/renderer/object_backed_native_handler.cc
[modify] https://crrev.com/14ff9d0cded8ae8032ef027d1f33c6666a695019/extensions/renderer/object_backed_native_handler.h


### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-14)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 15 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-04-21)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-05-06)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 37 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-05-23)

Marking as Merge-NA as #11 shows landing before M-51 base branch @ 386251

### cl...@chromium.org (2016-05-23)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

I'm going to have to start coming up with more creative things to say when rewarding you thousands of dollars (in this case, $7500). Watch this space.

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/598165?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083946)*
