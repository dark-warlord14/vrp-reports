# AddressSanitizer: heap-use-after-free location_bar\permission_request_chip.cc:127 in PermissionReque

| Field | Value |
|-------|-------|
| **Issue ID** | [40059675](https://issues.chromium.org/issues/40059675) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-05-16 |
| **Bounty** | $15,000.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1003503

#Reproduce  

I think the previously reported 1319797 was not fixed correctly,My fuzzer is still reporting similar issues, and the crash stack is basically the same.  

But the reproduction method is different from 1319797, I have not found a stable reproduction method.  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1319797>

**Problem Description:**  

Type of crash  

browser process(SANDBOX ESCAPE)

#Analysis  

same as 1319797

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.3 KB)
- deleted (application/octet-stream, 0 B)
- [poc2.html](attachments/poc2.html) (text/plain, 898 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [Untitled2.mov](attachments/Untitled2.mov) (video/quicktime, 8.6 MB)
- [fuzz-00004.html](attachments/fuzz-00004.html) (text/plain, 351.9 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### dt...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2022-05-16)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-16)

Thanks for your report. It might be hard for us to make progress without a set of reproduction steps.

[Monorail components: UI>Browser>Permissions>Prompts]

### wf...@chromium.org (2022-05-16)

This seems to go via OnHostResized maybe this is related to permission chip appearing, host resizing window, then it being dismissed prematurely? I'm tagging this as High sev given it's a browser bug but it likely requires complex UI interaction. I believe this code has been around for a while, unless the fix to https://crbug.com/chromium/1319797 exacerbated this somehow?

### [Deleted User] (2022-05-16)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-05-16)

Thank you for reporting! Just to clarify, the permission chip is not enabled on stable.

I'm actively working on the permission chip refactoring. 

### m....@gmail.com (2022-05-16)

re https://crbug.com/chromium/1325699#c04
" but it likely requires complex UI interaction" 
This one doesn't require complex user interaction, my fuzzer just clicks the start button.

I think there are some special paths that trigger this problem, which may be related to the timing of OnBackgroundFullscreen, which makes it impossible to trigger stably.

### [Deleted User] (2022-05-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@google.com (2022-05-18)

@m.cooolie is it possible to double-check the build version? The fix for 1319797 landed in 102.0.5005.39. 

### m....@gmail.com (2022-05-18)

I'm sure the version in issue is asan-win32-release_x64-1003503, which I downloaded from the chromium precompiled repository(gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-1003503).
Moreover, the problem of 1319797 cannot be reproduced on the asan-win32-release_x64-1003503 version, so I think it should be that the problem still exists after the fix.

I see that CF also found a case recently, but it cannot be reproduced stably, so it will be deleted soon https://clusterfuzz.com/testcase-detail/5322510958788608

### m....@gmail.com (2022-05-23)

test on windows asan-win32-release_x64-1005131
1. install node,puppeteer-core
2. python -m http.server 8000
3. node ch.test.js chrome.exe's_path http://localhost:8000/poc2.html
4. make sure that the tested chrome ui window is not the frontmost window, for example, open the task manager and let it always be displayed in the frontmost

Through this reproduction, I guess it should be that the patch of #1319797 was bypassed and caused the same issue


### m....@gmail.com (2022-05-23)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-05-23)

Was trying to reproduce it multiple times, without a success. I was asan-win32-release_x64-1005131 and asan-win32-release_x64-1003503. 
In a loop, the script starts the browser, opens fullscreen, and requests permission. 

### el...@chromium.org (2022-05-23)

The chrome window was not the frontmost, I've used always on top another window.

### m....@gmail.com (2022-05-23)

Here is the video I reproduced.

### el...@chromium.org (2022-05-23)

Thank you for the video! In my case when it goes into the fullscreen mode, I see a normal permission prompt and it does not crash. I'll try more on another Windows device. 

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ma...@google.com (2022-06-01)

Friendly security marshal ping. elklm@, did you have any luck in reproducing this?

### el...@chromium.org (2022-06-02)

I was not able to reproduce it on remove and local windows device. (attached video)

But the WIP CL is here https://chromium-review.googlesource.com/c/chromium/src/+/3644569


### el...@chromium.org (2022-06-03)

m.cooolie@ Could you please verify (run through a fuzzer and check via the above script) if there are crashes for the quiet chip as well?

1. Please enable the quiet chip experiment #permission-quiet-chip
2. In chrome://settings/content/notifications enable "Use quieter messaging"

After that any notifications permission request will be shown as a less prominent chip.

The goal is to understand if we have issues only with PermissionRequestChip or with both PermissionRequestChip and PermissionQuietChip.



### en...@chromium.org (2022-06-03)

And just for good measure, in addition to https://crbug.com/chromium/1325699#c21, could you also disable chrome://flags/#permission-chip, so only the quiet chip is enabled?

### m....@gmail.com (2022-06-04)

re#c20
The attachment is the original sample, it may be more likely to reproduce.
I hardcoded the port as 1337, if you change the port you can replace all the values in fuzz-00004.html

1. python -m http.server 1337
2. node ch.test2.js D:\chrome_asan\asan-win32-release_x64-1003503\chrome.exe http://localhost:1337/fuzz-00004.html

### m....@gmail.com (2022-06-04)

Test on asan-win32-release_x64-1010106
re 
https://crbug.com/chromium/1325699#c20 Reproduce

https://crbug.com/chromium/1325699#c21 Unreproduce 


### m....@gmail.com (2022-06-08)

Can you reproduce it using my new testcase?

### el...@chromium.org (2022-06-09)

@m.cooolie thank you for the attachments #23, I was able to reproduce the crash. 

### gi...@appspot.gserviceaccount.com (2022-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f1b476be552f0be02c941669483e0b462bfb9ef9

commit f1b476be552f0be02c941669483e0b462bfb9ef9
Author: Illia Klimov <elklm@google.com>
Date: Fri Jun 10 13:27:50 2022

PermissionChip lifecycle refactoring.

Current state: PermissionChip object dynamically created and removed as a response to the incoming permission request.

This CL: Always keep the PermissionChip object in the LocationBarView and only change its visibility when we need.

Bug: 1324947,1325699
Change-Id: I7276c132c1ec1f0734db3cfb15abdfeda11a6aae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3644569
Reviewed-by: Allen Bauer <kylixrd@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Ravjit Uppal <ravjit@chromium.org>
Reviewed-by: Olesia Marukhno <olesiamarukhno@google.com>
Cr-Commit-Position: refs/heads/main@{#1012907}

[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/intent_chip_button.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/permission_chip_unittest.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/omnibox_chip_button.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/permission_bubble/permission_bubble_interactive_uitest.cc
[add] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/permission_chip_delegate.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/frame/immersive_mode_controller_chromeos_browsertest.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/bubble_anchor_util_views.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/content_settings/content_setting_bubble_model.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/content_setting_bubble_contents.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/permission_quiet_chip.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/content_settings/content_setting_bubble_model.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/components/permissions/features.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/permission_chip.cc
[add] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/omnibox_chip_theme.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/location_bar_view.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/frame/browser_view.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/omnibox_chip_button.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view_browsertest.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/components/permissions/features.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/permission_chip.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/intent_chip_button.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/location_bar_view.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/permission_request_chip.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/permission_quiet_chip.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/permission_request_chip.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/location_bar/permission_request_chip_browsertest.cc
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/content_setting_bubble_contents.h
[modify] https://crrev.com/f1b476be552f0be02c941669483e0b462bfb9ef9/chrome/browser/ui/views/permission_bubble/permission_chip_interactive_test.cc


### el...@chromium.org (2022-06-13)

It seems like the above submitted CL has fixed the crash. The CL landed in 105.0.5113.0

Verified with https://crbug.com/chromium/1325699#c23 on:
1. asan-win32-release_x64-1012228 (104.0.5110.0) - crashing 
2. asan-win32-release_x64-1013361 (105.0.5118.0) - not crashing 

Marking as fixed and requesting a merger into M104 Beta.



### [Deleted User] (2022-06-13)

Merge approved: your change passed merge requirements and is auto-approved for M104. Please go ahead and merge the CL to branch 5112 (refs/branch-heads/5112) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7770dc6980d74292052bcf2017323aecc5fdb0d5

commit 7770dc6980d74292052bcf2017323aecc5fdb0d5
Author: Illia Klimov <elklm@google.com>
Date: Mon Jun 13 16:14:14 2022

PermissionChip lifecycle refactoring.

Current state: PermissionChip object dynamically created and removed as a response to the incoming permission request.

This CL: Always keep the PermissionChip object in the LocationBarView and only change its visibility when we need.

(cherry picked from commit f1b476be552f0be02c941669483e0b462bfb9ef9)

Bug: 1324947,1325699
Change-Id: I7276c132c1ec1f0734db3cfb15abdfeda11a6aae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3644569
Reviewed-by: Allen Bauer <kylixrd@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Ravjit Uppal <ravjit@chromium.org>
Reviewed-by: Olesia Marukhno <olesiamarukhno@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1012907}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3702432
Auto-Submit: Illia Klimov <elklm@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Allen Bauer <kylixrd@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#28}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/intent_chip_button.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/permission_chip_unittest.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/omnibox_chip_button.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/permission_bubble/permission_bubble_interactive_uitest.cc
[add] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/permission_chip_delegate.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/frame/immersive_mode_controller_chromeos_browsertest.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/bubble_anchor_util_views.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/content_settings/content_setting_bubble_model.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/content_setting_bubble_contents.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/permission_quiet_chip.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/content_settings/content_setting_bubble_model.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/components/permissions/features.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/permission_chip.cc
[add] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/omnibox_chip_theme.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/location_bar_view.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/frame/browser_view.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view_browsertest.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/omnibox_chip_button.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/components/permissions/features.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/permission_chip.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/intent_chip_button.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/location_bar_view.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/permission_request_chip.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/permission_quiet_chip.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/permission_request_chip.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/location_bar/permission_request_chip_browsertest.cc
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/content_setting_bubble_contents.h
[modify] https://crrev.com/7770dc6980d74292052bcf2017323aecc5fdb0d5/chrome/browser/ui/views/permission_bubble/permission_chip_interactive_test.cc


### [Deleted User] (2022-06-13)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### vo...@google.com (2022-06-14)

[Empty comment from Monorail migration]

### vo...@google.com (2022-06-20)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-24)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts in reporting this issue to us and nice work! 

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### gm...@google.com (2022-07-11)

@amyressler would this be merged to 102 extended?

### gm...@google.com (2022-07-12)

[Empty comment from Monorail migration]

### vo...@google.com (2022-07-14)

[Empty comment from Monorail migration]

### vo...@google.com (2022-07-15)

Marking as not applicable to M96 because chrome://flags/#permission-chip is disabled on M96.

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-11)

Can we please evaluate for LTC-102?

### el...@google.com (2022-08-11)

The feature is not enabled for M102. 

### rz...@google.com (2022-08-12)

Thanks @elklm, labelling as not applicable for 102.

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1325699?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Omnibox, UI>Browser>Permissions>Prompts]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059675)*
