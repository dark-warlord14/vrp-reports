# uaf in PermissionStatus::OnPermissionStatusChange

| Field | Value |
|-------|-------|
| **Issue ID** | [40060951](https://issues.chromium.org/issues/40060951) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>PermissionsAPI |
| **Platforms** | Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2022-09-13 |
| **Bounty** | $2,500.00 |

## Description

**Steps to reproduce the problem:**  

1.

```
void PermissionStatus::OnPermissionStatusChange(MojoPermissionStatus status) {  
  DispatchEvent(\*Event::Create(event_type_names::kChange));  here can execute user's js  
}  

```

2.then we can see the function

```
void PermissionStatusListener::OnPermissionStatusChange(  
    MojoPermissionStatus status) {  
  if (status_ == status)  
    return;  
  
  status_ = status;  
  
  for (const auto& observer : observers_) {  
    if (observer)  
      observer->OnPermissionStatusChange(status);  // here will execute user's js  
    else  
      RemoveObserver(observer);  
  }  
}  

```

3.and from the observers\_.insert(observer) I didn't see any check

```
void PermissionStatusListener::AddObserver(Observer\* observer) {  
  if (observers_.IsEmpty())  
    StartListening();  
  
  observers_.insert(observer);  
}  

```

**Problem Description:**  

above all, haven't try to create poc, but I think my analysis is right.

**Additional Comments:**

\*\*Chrome version: \*\* 105.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 14.4 KB)
- [test.html](attachments/test.html) (text/plain, 619 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 2.8 MB)
- [0001-issue-1363040-fix-patch.patch](attachments/0001-issue-1363040-fix-patch.patch) (text/plain, 1.0 KB)
- [0001-fix-issue-1363040.patch](attachments/0001-fix-issue-1363040.patch) (text/plain, 1.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 553.8 KB)
- [0001-fix-issue-1363040.patch](attachments/0001-fix-issue-1363040.patch) (text/plain, 998 B)

## Timeline

### [Deleted User] (2022-09-13)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-13)

Assigning out of an abundance of caution, though generally, without a PoC I'm reluctant to have developers take a look ...

[Monorail components: Blink>PermissionsAPI]

### ts...@chromium.org (2022-09-13)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-09-14)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-09-14)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-09-14)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-09-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-15)

wxhusst, what steps are required to trigger the issue?  I couldn't quite infer them from the video. Thanks!

### wx...@gmail.com (2022-09-16)

You need to change the tab of geolocation permission twice

### wx...@gmail.com (2022-09-16)

use this one

### wx...@gmail.com (2022-09-16)

my command line
" chrome --no-sandbox --enable-experimental-web-platform-features"

### an...@chromium.org (2022-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2022-09-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4df595127d95d4b0bf115be1ab4604d95b75273c

commit 4df595127d95d4b0bf115be1ab4604d95b75273c
Author: Andy Paicu <andypaicu@chromium.org>
Date: Tue Sep 20 13:28:34 2022

Fix UAF issue around permission status observer list

Bug: 1363040
Change-Id: I1f64a901b83aa834ae652c8041456e9b7d253c1f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3907744
Reviewed-by: Kamila Hasanbega <hkamila@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1049058}

[modify] https://crrev.com/4df595127d95d4b0bf115be1ab4604d95b75273c/third_party/blink/renderer/modules/permissions/permission_status_listener.cc


### an...@chromium.org (2022-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-21)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-09-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-09-21)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-09-21)

Andy, do we know if this regressed in M105 or earlier? Note that the `FoundIn` label refers to the earliest version in which the bug can be found in, not where we found it.

### [Deleted User] (2022-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-09-22)

It would be when the initial CL landed (https://chromium-review.googlesource.com/c/chromium/src/+/3359620), so M103. Updating the foundin label.

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-09-30)

this patch also can work..

### wx...@gmail.com (2022-09-30)

I think you can set the status to fixed

### am...@chromium.org (2022-09-30)

Setting this back to Fixed comments #14, #21, and #24 so the bot can add the appropriate merge labels and this fix can go into the security merge review queue 

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-30)

Requesting merge to stable M106 because latest trunk commit (1049058) appears to be after stable branch point (1036826).

Requesting merge to beta M107 because latest trunk commit (1049058) appears to be after beta branch point (1047731).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-30)

Merge review required: M107 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-30)

Merge review required: M106 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-10-03)

upon my initial review, https://crbug.com/chromium/1363040#c12 was deleted so I didn't see that POC / repro steps. 
Is this correct that enable-experimental-web-platform-features flag would need to be set to trigger this? Experimental web platform features flag is disabled by default in stable at present. Backmerge decisions would be made based on if/what channel field experiments would be enabled by default. If that is not planned in any active release channels, this should be set to SI-None. 

### wx...@gmail.com (2022-10-04)

If we don't have the enable-experimental-web-platform-features flag , we need complex ui steps to trigger bug

### am...@chromium.org (2022-10-05)

Since this can be triggered via user gesture, I'm going to err on the side of caution and keep this as SI-Extended and approve backmerging; 
merge approved for M107, please merge to branch 5304 
merge approved for M106, please merge to branch 5249 at your earliest convenience (NLT 12p PST Friday, 7 October) so this fix can be included in next week's Stable respin -- thank you! 

### gi...@appspot.gserviceaccount.com (2022-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1dc5dda6112bdd811c923520cc728a474583409e

commit 1dc5dda6112bdd811c923520cc728a474583409e
Author: Andy Paicu <andypaicu@chromium.org>
Date: Thu Oct 06 11:02:29 2022

Fix UAF issue around permission status observer list

(cherry picked from commit 4df595127d95d4b0bf115be1ab4604d95b75273c)

Bug: 1363040
Change-Id: I1f64a901b83aa834ae652c8041456e9b7d253c1f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3907744
Reviewed-by: Kamila Hasanbega <hkamila@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1049058}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3929034
Reviewed-by: Illia Klimov <elklm@chromium.org>
Cr-Commit-Position: refs/branch-heads/5304@{#483}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/1dc5dda6112bdd811c923520cc728a474583409e/third_party/blink/renderer/modules/permissions/permission_status_listener.cc


### gi...@appspot.gserviceaccount.com (2022-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/65f0ef609c005a16fe38e8f004a6ee3a38181135

commit 65f0ef609c005a16fe38e8f004a6ee3a38181135
Author: Andy Paicu <andypaicu@chromium.org>
Date: Thu Oct 06 21:04:23 2022

Fix UAF issue around permission status observer list

(cherry picked from commit 4df595127d95d4b0bf115be1ab4604d95b75273c)

(cherry picked from commit 1dc5dda6112bdd811c923520cc728a474583409e)

Bug: 1363040
Change-Id: I1f64a901b83aa834ae652c8041456e9b7d253c1f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3907744
Reviewed-by: Kamila Hasanbega <hkamila@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1049058}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3929034
Reviewed-by: Illia Klimov <elklm@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5304@{#483}
Cr-Original-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3936291
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5249@{#764}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/65f0ef609c005a16fe38e8f004a6ee3a38181135/third_party/blink/renderer/modules/permissions/permission_status_listener.cc


### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-06)

Congratulations! The VRP Panel has decided to award you $1,500 for this report of a moderately mitigated security bug and $1,000 patch bonus, for a total of $2500. Thank you for your efforts and reporting this issue to us! 

### wx...@gmail.com (2022-10-07)

I think my bug is similar as https://crbug.com/chromium/1366813, and https://crbug.com/chromium/1366813 can get $7000....

### am...@chromium.org (2022-10-07)

This issue is not remote exploitable and is heavily mitigated by series of user interaction required to trigger this issue. The other report you note (https://crbug.com/chromium/1366813) is remote exploitable and can be triggered by remote content. 

### wx...@gmail.com (2022-10-07)

Ok, thanks 

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1363040?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060951)*
