# Security: heap-buffer-overflow in PlatformNotificationServiceImpl::CreateNotificationFromData

| Field | Value |
|-------|-------|
| **Issue ID** | [40055576](https://issues.chromium.org/issues/40055576) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Notifications |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | de...@chromium.org |
| **Created** | 2021-04-17 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/notifications/platform_notification_service_impl.cc;l=453;bpv=0;bpt=1>

if `notification_data.actions.size()` > `notification_resources.action_icons.size()`, access `notification_resources.action_icons[i]` will cause heap overflow.

tigger this bug need Notification permission.

**VERSION**  

Chrome Version: 92.0.4480.0 [x64 dev]  

Operating System: ubuntu20.10

**REPRODUCTION CASE**  

1.python copy\_mojo\_js\_bindings.py path/to/ASAN/gen/  

2.python3 -m http.server  

3../chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/nonexist <http://localhost:8000/test.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

## Attachments

- [test.html](attachments/test.html) (text/plain, 2.0 KB)
- deleted (application/octet-stream, 0 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 1.0 MB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 15.2 KB)

## Timeline

### [Deleted User] (2021-04-17)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-04-17)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-04-17)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-04-19)

Tentatively triaging as High assuming it's not possible to exploit this without a compromised renderer. (Also, even if it were possible, needing to grant notifications permission might still downgrade to High.)

Notifications owners, could you please take a look?

[Monorail components: UI>Notifications]

### es...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### de...@chromium.org (2021-04-19)

After a quick look, I found that Blink normally populates an action icon image for each notification action, so this would require a compromised renderer.

### de...@chromium.org (2021-04-20)

CL in review: https://chromium-review.googlesource.com/c/chromium/src/+/2838205

### [Deleted User] (2021-04-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3b28dc50187b22e080ad9c1e4e6c4f3b08f3136d

commit 3b28dc50187b22e080ad9c1e4e6c4f3b08f3136d
Author: Justin DeWitt <dewittj@chromium.org>
Date: Fri Apr 23 19:15:56 2021

Notifications: crash if improper action icons sent from renderer.

Previously, the code only called DCHECK but as this data is from a
renderer we should probably crash the browser.

Bug: 1200019
Change-Id: If4d9d48c8e18a3ed9c8bb3a50b952591259e0db5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2838205
Commit-Queue: Justin DeWitt <dewittj@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Cr-Commit-Position: refs/heads/master@{#875788}

[modify] https://crrev.com/3b28dc50187b22e080ad9c1e4e6c4f3b08f3136d/chrome/browser/notifications/platform_notification_service_impl.cc
[modify] https://crrev.com/3b28dc50187b22e080ad9c1e4e6c4f3b08f3136d/content/browser/notifications/blink_notification_service_impl.cc
[modify] https://crrev.com/3b28dc50187b22e080ad9c1e4e6c4f3b08f3136d/content/browser/notifications/blink_notification_service_impl.h


### de...@chromium.org (2021-04-23)

Emily, after this is verified on Canary, does security team want to merge to M90 or M91?

### es...@chromium.org (2021-04-24)

This is High severity (memory corruption in browser process triggerable from a compromised renderer; see https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#TOC-High-severity) so it should be merged to current stable milestone M90.

### de...@chromium.org (2021-04-27)

Requesting merge. Canary does not see a spike in crashes in %notification_service% so I think this is safe enough. 

https://crash.corp.google.com/browse?q=expanded_custom_data.ChromeCrashProto.channel%3D%27canary%27+AND+expanded_custom_data.ChromeCrashProto.magic_signature_1.name+LIKE+%27%25notification_service%25%27#productname:1000,productversion:1020,-processtype,+magicsignature:100,magicsignature2:50,stablesignature:50,productversionbyos:20,device:1000,day:110,experiments:10000

### [Deleted User] (2021-04-27)

This bug requires manual review: M91's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-04-28)

dewittj@ please reply to the questions posted in https://crbug.com/chromium/1200019#c13, thank you.

+Adrian(Security TPM)

### ad...@chromium.org (2021-04-28)

Please mark it as fixed if it is: https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#TOC-Merge-labels - then the merge process would have kick in automatically.

Assuming this is deemed a complete fix, approving merge to M91, branch 4472. Merges to M90 will be approved at a later date when we've got a release coming up.


### de...@google.com (2021-04-28)

#15 - Apologies, this is different from the normal merge process.

### ad...@chromium.org (2021-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cdb8756d339fa80f1f7ad12b46ae9651bc4768d8

commit cdb8756d339fa80f1f7ad12b46ae9651bc4768d8
Author: Justin DeWitt <dewittj@chromium.org>
Date: Thu Apr 29 20:47:08 2021

Notifications: crash if improper action icons sent from renderer.

Previously, the code only called DCHECK but as this data is from a
renderer we should probably crash the browser.

(cherry picked from commit 3b28dc50187b22e080ad9c1e4e6c4f3b08f3136d)

Bug: 1200019
Change-Id: If4d9d48c8e18a3ed9c8bb3a50b952591259e0db5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2838205
Commit-Queue: Justin DeWitt <dewittj@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#875788}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2860443
Owners-Override: Justin DeWitt <dewittj@chromium.org>
Auto-Submit: Justin DeWitt <dewittj@chromium.org>
Commit-Queue: Adrian Taylor <adetaylor@chromium.org>
Reviewed-by: Adrian Taylor <adetaylor@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#577}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/cdb8756d339fa80f1f7ad12b46ae9651bc4768d8/chrome/browser/notifications/platform_notification_service_impl.cc
[modify] https://crrev.com/cdb8756d339fa80f1f7ad12b46ae9651bc4768d8/content/browser/notifications/blink_notification_service_impl.cc
[modify] https://crrev.com/cdb8756d339fa80f1f7ad12b46ae9651bc4768d8/content/browser/notifications/blink_notification_service_impl.h


### ad...@google.com (2021-05-04)

Approving merge to M90, branch 4430. Please merge by EOD PST Thursday for inclusion in next week's security refresh.

### go...@chromium.org (2021-05-04)

Please merge your change to M90 branch 4430 ASAP so we can pick it up for next M90 respin. Thank you.

### gi...@appspot.gserviceaccount.com (2021-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4c448c7fa33f21361e816b5fed16ec1e36ec6f5d

commit 4c448c7fa33f21361e816b5fed16ec1e36ec6f5d
Author: Justin DeWitt <dewittj@chromium.org>
Date: Tue May 04 21:46:15 2021

Notifications: crash if improper action icons sent from renderer.

Previously, the code only called DCHECK but as this data is from a
renderer we should probably crash the browser.

(cherry picked from commit 3b28dc50187b22e080ad9c1e4e6c4f3b08f3136d)

Bug: 1200019
Change-Id: If4d9d48c8e18a3ed9c8bb3a50b952591259e0db5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2838205
Commit-Queue: Justin DeWitt <dewittj@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#875788}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2872493
Auto-Submit: Justin DeWitt <dewittj@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Reviewed-by: Adrian Taylor <adetaylor@chromium.org>
Reviewed-by: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1394}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/4c448c7fa33f21361e816b5fed16ec1e36ec6f5d/chrome/browser/notifications/platform_notification_service_impl.cc
[modify] https://crrev.com/4c448c7fa33f21361e816b5fed16ec1e36ec6f5d/content/browser/notifications/blink_notification_service_impl.cc
[modify] https://crrev.com/4c448c7fa33f21361e816b5fed16ec1e36ec6f5d/content/browser/notifications/blink_notification_service_impl.h


### am...@chromium.org (2021-05-07)

[Empty comment from Monorail migration]

### vs...@google.com (2021-05-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/df92940ea80e516cc741bfe19ee23b9687ac43b6

commit df92940ea80e516cc741bfe19ee23b9687ac43b6
Author: Justin DeWitt <dewittj@chromium.org>
Date: Wed May 12 11:51:09 2021

Notifications: crash if improper action icons sent from renderer.

Previously, the code only called DCHECK but as this data is from a
renderer we should probably crash the browser.

(cherry picked from commit 3b28dc50187b22e080ad9c1e4e6c4f3b08f3136d)

(cherry picked from commit 4c448c7fa33f21361e816b5fed16ec1e36ec6f5d)

Bug: 1200019
Change-Id: If4d9d48c8e18a3ed9c8bb3a50b952591259e0db5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2838205
Commit-Queue: Justin DeWitt <dewittj@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#875788}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2872493
Auto-Submit: Justin DeWitt <dewittj@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Reviewed-by: Adrian Taylor <adetaylor@chromium.org>
Reviewed-by: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4430@{#1394}
Cr-Original-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2884075
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430_101@{#27}
Cr-Branched-From: 3e9034a21f4b1f6707146b1309e001c3321ab48a-refs/branch-heads/4430@{#1364}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/df92940ea80e516cc741bfe19ee23b9687ac43b6/chrome/browser/notifications/platform_notification_service_impl.cc
[modify] https://crrev.com/df92940ea80e516cc741bfe19ee23b9687ac43b6/content/browser/notifications/blink_notification_service_impl.cc
[modify] https://crrev.com/df92940ea80e516cc741bfe19ee23b9687ac43b6/content/browser/notifications/blink_notification_service_impl.h


### gi...@google.com (2021-05-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fb27b32078021c3ff911d90428e410c7f2efbafb

commit fb27b32078021c3ff911d90428e410c7f2efbafb
Author: Justin DeWitt <dewittj@chromium.org>
Date: Wed May 12 18:08:04 2021

Notifications: crash if improper action icons sent from renderer.

Previously, the code only called DCHECK but as this data is from a
renderer we should probably crash the browser.

(cherry picked from commit 3b28dc50187b22e080ad9c1e4e6c4f3b08f3136d)

Bug: 1200019
Change-Id: If4d9d48c8e18a3ed9c8bb3a50b952591259e0db5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2838205
Commit-Queue: Justin DeWitt <dewittj@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#875788}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2883723
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1635}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/fb27b32078021c3ff911d90428e410c7f2efbafb/chrome/browser/notifications/platform_notification_service_impl.cc
[modify] https://crrev.com/fb27b32078021c3ff911d90428e410c7f2efbafb/content/browser/notifications/blink_notification_service_impl.cc
[modify] https://crrev.com/fb27b32078021c3ff911d90428e410c7f2efbafb/content/browser/notifications/blink_notification_service_impl.h


### da...@chromium.org (2021-05-12)

It looks like we have a separate list of NotificationActions and icons for those actions. The icons in NotifcationResources should move to be inside each NotificationAction to prevent us from having 2 lists with dependent sizes in a mojom.

I wonder if there's some way to prevent dependent lists like this.

### am...@google.com (2021-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-12)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. Very nice work! 

### dc...@chromium.org (2021-05-12)

Can we make a followup fix here? The current way the IPC is structured violates the Mojo guidelines. See https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/mojo.md#use-structured-types ("avoid parallel arrays of data")

### am...@google.com (2021-05-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1200019?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055576)*
