# Permission Service Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40050720](https://issues.chromium.org/issues/40050720) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Permissions>Model |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | if...@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2019-11-18 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36

Steps to reproduce the problem:
First of all, apply two patches in the attchments, and then:

1. python copy_binding.py /path/to/out/gen/
2. cp /path/to/permission.html /path/to/permission.js ./
3. python3 -m http.server

Run asan build chromium with ./chromium --enable-blink-features=MojoJS http://localhost:8000/permission.html

What is the expected behavior?

What went wrong?
A use after free occured. In PermissionServiceImpl::AddPermissionObserver -> PermissionServiceContext::CreateSubscription we could find that subscription_id will increase one by one. So we could destruct the PermissionSubscription if we trigger the int overflow.

Se the destructor function, we could find that:

https://cs.chromium.org/chromium/src/content/browser/permissions/permission_service_context.cc?rcl=f6f2afe93d24b8c7823dc281ba5a3f2d33262fa4&l=35

it will call the Unsubscribe, but in the unsubscribe logic: 
https://cs.chromium.org/chromium/src/content/browser/permissions/permission_controller_impl.cc?rcl=f6f2afe93d24b8c7823dc281ba5a3f2d33262fa4&l=430

it will judge if the id is equal to -1, it will not remove the subscription, so the logic error occured.

Asan log in the attachment.

Did this work before? N/A 

Chrome version: 78.0.3904.97  Channel: stable
OS Version: 
Flash Version:

## Attachments

- [permission.html](attachments/permission.html) (text/plain, 231 B)
- [permission.js](attachments/permission.js) (text/plain, 938 B)
- [copy_binding.py](attachments/copy_binding.py) (text/plain, 530 B)
- [asan_log_permission.txt](attachments/asan_log_permission.txt) (text/plain, 20.1 KB)
- [permission_chrome.diff](attachments/permission_chrome.diff) (text/plain, 619 B)
- [permissions_content_browser.diff](attachments/permissions_content_browser.diff) (text/plain, 698 B)

## Timeline

### if...@gmail.com (2019-11-18)

For convenience, the patch modify the IDMap index type to int8_t, so it can be triggered easily.
In reaility, this attack scene could cost hours of time to execute such big loop.

### do...@chromium.org (2019-11-19)

+mlamouri - PTAL

Assigning None impact since this needs the MojoJs flag and some patches to be applied to Chrome.

[Monorail components: Internals>Permissions>Model]

### if...@gmail.com (2019-11-19)

Sorry but the patch is just for you to convenientily trigger the integer overflow, in fact if you don't apply the patch, the problem is also exists, you just need to change the iteration cound to int32_max.

### ml...@google.com (2019-11-19)

Assigning to engedy@ as they own the permissions code now. Please, let me know if I can be of any help.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-02-24)

This appears to be a high severity sandbox escape. Yes, it relies on mojojs but a renderer can just toggle this on. This is mitigated by the time it would take to perform the attack in reality.

engedy can you please take a look at this or find someone who can?

### [Deleted User] (2021-02-26)

engedy: Uh oh! This issue still open and hasn't been updated in the last 466 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-26)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-13)

engedy: Uh oh! This issue still open and hasn't been updated in the last 481 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-03-30)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-03-30)

CC'ing code reviewers on the bug.

### gi...@appspot.gserviceaccount.com (2021-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ad1489b7c3ed705fc623cdffdc292324be9fcbfa

commit ad1489b7c3ed705fc623cdffdc292324be9fcbfa
Author: Balazs Engedy <engedy@chromium.org>
Date: Wed Mar 31 07:47:19 2021

Use IDType for permission change subscriptions.

Bug: 1025683
Change-Id: I3b44ba7833138e8a657a4192e1a36c978695db32
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2791431
Reviewed-by: Richard Coles <torne@chromium.org>
Reviewed-by: Yuchen Liu <yucliu@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Fabrice de Gans-Riberi <fdegans@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Illia Klimov <elklm@google.com>
Auto-Submit: Balazs Engedy <engedy@chromium.org>
Commit-Queue: Balazs Engedy <engedy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#867999}

[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/android_webview/browser/aw_permission_manager.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/android_webview/browser/aw_permission_manager.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/chrome/browser/permissions/permission_manager_browsertest.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/chromecast/browser/cast_permission_manager.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/chromecast/browser/cast_permission_manager.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/components/permissions/permission_manager.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/components/permissions/permission_manager.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/components/permissions/permission_manager_unittest.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/browser/android/nfc_host.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/browser/android/nfc_host.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/browser/android/nfc_host_unittest.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/browser/permissions/permission_controller_impl.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/browser/permissions/permission_controller_impl.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/browser/permissions/permission_service_context.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/browser/permissions/permission_service_context.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/browser/renderer_host/media/media_stream_manager.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/browser/renderer_host/media/media_stream_manager.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/public/browser/permission_controller.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/public/browser/permission_controller_delegate.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/public/test/mock_permission_manager.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/shell/browser/shell_permission_manager.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/shell/browser/shell_permission_manager.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/web_test/browser/web_test_permission_manager.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/content/web_test/browser/web_test_permission_manager.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/fuchsia/engine/browser/web_engine_permission_delegate.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/fuchsia/engine/browser/web_engine_permission_delegate.h
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/headless/lib/browser/headless_permission_manager.cc
[modify] https://crrev.com/ad1489b7c3ed705fc623cdffdc292324be9fcbfa/headless/lib/browser/headless_permission_manager.h


### en...@chromium.org (2021-03-31)

Putting this on the radar for M90 merge review, would like to cherry pick as soon as we get some Canary testing.

### [Deleted User] (2021-03-31)

This bug requires manual review: We are only 12 days from stable.
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

### if...@gmail.com (2021-03-31)

[Comment Deleted]

### en...@chromium.org (2021-03-31)

Merge request questionnaire answers:

1. Does your merge fit within the Merge Decision Guidelines?
Yes.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2791431

3. Has the change landed and been verified on ToT?
Yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?
No.

5. Why are these changes required in this milestone after branch?
Addressing a high-severity security issue.

6. Is this a new feature?
No.

7. If it is a new feature, is it behind a flag using finch?
N/A.

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents
N/A.

### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-31)

engedy@ I love this change. Not only does it fix this bug but it brings type safety to all this code in the future.

That said, it's quite a (textually) big change to be merging to M90 at this fairly late stage. So:

Approving merge to M90 - please merge to branch 4430 - _but_ please wait until this has been in a Canary build for 24 hours first and only merge if there are no signs of trouble.

### en...@chromium.org (2021-03-31)

Fully agreed, I am slightly concerned about this as well, but wanted a fix that's obviously correct.

Just in case we hit any snags, I do have a Plan B as well, namely I also prepared a one-line fix in crrev.com/c/2794363, I just abandoned it because I was not able to convince myself at 100% confidence that it's correct.

### gi...@appspot.gserviceaccount.com (2021-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d

commit b0dc55a9ce8811ffa27d468c6f52f6673283ab4d
Author: Balazs Engedy <engedy@chromium.org>
Date: Mon Apr 05 17:38:22 2021

Use IDType for permission change subscriptions.

(cherry picked from commit ad1489b7c3ed705fc623cdffdc292324be9fcbfa)

Bug: 1025683
Change-Id: I3b44ba7833138e8a657a4192e1a36c978695db32
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2791431
Reviewed-by: Richard Coles <torne@chromium.org>
Reviewed-by: Yuchen Liu <yucliu@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Fabrice de Gans-Riberi <fdegans@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Illia Klimov <elklm@google.com>
Auto-Submit: Balazs Engedy <engedy@chromium.org>
Commit-Queue: Balazs Engedy <engedy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#867999}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2802371
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1056}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/android_webview/browser/aw_permission_manager.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/android_webview/browser/aw_permission_manager.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/chrome/browser/permissions/permission_manager_browsertest.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/chromecast/browser/cast_permission_manager.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/chromecast/browser/cast_permission_manager.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/components/permissions/permission_manager.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/components/permissions/permission_manager.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/components/permissions/permission_manager_unittest.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/browser/android/nfc_host.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/browser/android/nfc_host.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/browser/android/nfc_host_unittest.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/browser/permissions/permission_controller_impl.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/browser/permissions/permission_controller_impl.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/browser/permissions/permission_service_context.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/browser/permissions/permission_service_context.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/browser/renderer_host/media/media_stream_manager.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/browser/renderer_host/media/media_stream_manager.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/public/browser/permission_controller.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/public/browser/permission_controller_delegate.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/public/test/mock_permission_manager.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/shell/browser/shell_permission_manager.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/shell/browser/shell_permission_manager.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/web_test/browser/web_test_permission_manager.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/content/web_test/browser/web_test_permission_manager.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/fuchsia/engine/browser/web_engine_permission_delegate.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/fuchsia/engine/browser/web_engine_permission_delegate.h
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/headless/lib/browser/headless_permission_manager.cc
[modify] https://crrev.com/b0dc55a9ce8811ffa27d468c6f52f6673283ab4d/headless/lib/browser/headless_permission_manager.h


### en...@chromium.org (2021-04-05)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-07)

Congratulations, the VRP Panel has decided to award you $20,000 for this report! A member of our finance team will be in touch with you soon to arrange payment. Nice work and thank you for reporting this issue to us!

### if...@gmail.com (2021-04-09)

Thanks, credit goes to Gengming Liu and Jianyu Chen when working at Tencent KeenLab

### ja...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530

commit 74c9ad9a53568a0dfca89a0877f3a6c66f4fc530
Author: Jana Grill <janagrill@google.com>
Date: Thu Apr 15 19:35:42 2021

Use IDType for permission change subscriptions.

(cherry picked from commit ad1489b7c3ed705fc623cdffdc292324be9fcbfa)

Bug: 1025683
Change-Id: I3b44ba7833138e8a657a4192e1a36c978695db32
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2791431
Reviewed-by: Richard Coles <torne@chromium.org>
Reviewed-by: Yuchen Liu <yucliu@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Fabrice de Gans-Riberi <fdegans@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Illia Klimov <elklm@google.com>
Auto-Submit: Balazs Engedy <engedy@chromium.org>
Commit-Queue: Balazs Engedy <engedy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#867999}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2817980
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1607}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/android_webview/browser/aw_permission_manager.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/android_webview/browser/aw_permission_manager.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/chrome/browser/permissions/permission_manager_browsertest.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/chromecast/browser/cast_permission_manager.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/chromecast/browser/cast_permission_manager.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/components/permissions/permission_manager.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/components/permissions/permission_manager.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/components/permissions/permission_manager_unittest.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/browser/android/nfc_host.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/browser/android/nfc_host.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/browser/android/nfc_host_unittest.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/browser/permissions/permission_controller_impl.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/browser/permissions/permission_controller_impl.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/browser/permissions/permission_service_context.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/browser/permissions/permission_service_context.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/browser/renderer_host/media/media_stream_manager.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/browser/renderer_host/media/media_stream_manager.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/public/browser/permission_controller.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/public/browser/permission_controller_delegate.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/public/test/mock_permission_manager.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/shell/browser/shell_permission_manager.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/shell/browser/shell_permission_manager.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/shell/browser/web_test/web_test_permission_manager.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/content/shell/browser/web_test/web_test_permission_manager.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/fuchsia/engine/browser/web_engine_permission_delegate.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/fuchsia/engine/browser/web_engine_permission_delegate.h
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/headless/lib/browser/headless_permission_manager.cc
[modify] https://crrev.com/74c9ad9a53568a0dfca89a0877f3a6c66f4fc530/headless/lib/browser/headless_permission_manager.h


### ja...@google.com (2021-04-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-07-23)

This issue was migrated from crbug.com/chromium/1025683?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050720)*
