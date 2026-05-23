# Nearby Share UI incorrectly appears in non-ChromeOS browsers: causes UAF

| Field | Value |
|-------|-------|
| **Issue ID** | [40056709](https://issues.chromium.org/issues/40056709) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | kr...@chromium.org |
| **Created** | 2021-07-28 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36

Steps to reproduce the problem:
1.open two tabs. the first tab open nearby share
2.then close the first tab
3.close the nearby share

My test in chromium linux
versions is 94.0.4578
commit is e7e943012eb6ddb6ab6cae8b97d5c7f7524f4e9a

What is the expected behavior?

What went wrong?
browser crashes

Did this work before? N/A 

Chrome version: 92.0.4515.107  Channel: stable
OS Version: 10.0

## Attachments

- [uaf.txt](attachments/uaf.txt) (text/plain, 24.6 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 9.3 MB)
- [chrome_sharing_hub_bubble_controller_browertest.cc](attachments/chrome_sharing_hub_bubble_controller_browertest.cc) (text/plain, 2.6 KB)
- [0001-fix-browser-crash.patch](attachments/0001-fix-browser-crash.patch) (text/plain, 1.8 KB)

## Timeline

### wx...@gmail.com (2021-07-28)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-07-28)

the fix is simple, add the WebContentObserver to web_contents_.

### [Deleted User] (2021-07-28)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-07-28)

oh..look like the function 'ScreenshotCapturedBubbleController::ShowBubble'   has the same question.

### wx...@gmail.com (2021-07-28)

I will try to file second bug. I must  build the recently source code  and prove it...

### wx...@gmail.com (2021-07-29)

here is the browsertest

### wx...@gmail.com (2021-07-29)

I set a Test function in sharing_hub_bubble_controller.cc and 
```
void SharingHubBubbleController::OnSharesheetClosedTest(
  views::Widget::ClosedReason reason){
  OnSharesheetClosed(reason);
}
```

and set the function OnSharesheetClosedTest to be public in sharing_hub_bubble_controller.h

### me...@chromium.org (2021-07-30)

kmilka: Could you please take a look?

Marking as high severity as this requires significant user interaction even though it's a UAF in the browser process. I think the feature is disabled as well, so there is currently no impact.

[Monorail components: UI>Browser>Sharing>Nearby]

### wx...@gmail.com (2021-07-30)

from the code, this bug just influence OS-Chrome. And in my build version, I don't set any chrome://flags , so Maybe here should set Security_Impact-Stable And OS-Chrome.

### ha...@chromium.org (2021-07-30)

Nearby Share should not be appearing in the sharesheet on any OS besides Chrome OS; this is undefined behavior. And this is not a security issue.

Mel, are you the right person to take a look at this?


[Monorail components: -UI>Browser>Sharing>Nearby OS>Systems>Multidevice>Nearby]

### ha...@chromium.org (2021-07-30)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-07-30)

[Comment Deleted]

### wx...@gmail.com (2021-07-30)

So this is not a  security bug?????

### wx...@gmail.com (2021-07-30)

Feel disappointed about this...

### wx...@gmail.com (2021-07-30)

I use the chromeos- linux build in the video

### wx...@gmail.com (2021-07-31)

Please set the security label

### ha...@chromium.org (2021-08-02)

Hi wxhusst@, what is your security concern of this issue?

### wx...@gmail.com (2021-08-02)

it's a obvious uaf in  chromium （chrome os version)

### wx...@gmail.com (2021-08-02)

If you don't think it is a security bug, you can see the bug https://bugs.chromium.org/p/chromium/issues/detail?id=1212498. It has the similar bug pattern.

### wx...@gmail.com (2021-08-02)

You can also CC security people to get their advices.

### wx...@gmail.com (2021-08-02)

as a developer, I could tell you the bug reason, the class SharingHubBubbleController owns "web_contents_". when we choose to close the tab, the web_contents_. is destoryed, bug the nearby bubble is still alive which means the class SharingHubBubbleController is still alive, but its raw pointer "web_contents_" had been freed and raw pointers whcih related to "web_contents_" had been freed. When we click the "close" button, the "view()" has been destroyed cause uaf, and here make a browser uaf that always means critical to our normal user.

### ha...@chromium.org (2021-08-02)

I apologize, I was incorrect. I was not aware that UAFs needed to be marked as security issues. Reverting to the labels set by meacer@.

Leaving assigned to Mel to determine why this is appearing in a non-Chrome OS operating system.

### wx...@gmail.com (2021-08-03)

I think here should set Security_Impact-Stable or Security_Impact-Head, because I don't set any flags to use the nearby share. 

### me...@chromium.org (2021-08-03)

+kristipark fyi, I'm looking into this.

[Monorail components: Platform>Apps>Foundation>Sharesheet]

### ha...@chromium.org (2021-08-03)

[Empty comment from Monorail migration]

### me...@google.com (2021-08-04)

Assigning to kristipark@. This is crashing in SharingHubBubbleController::OnSharesheetClosed when you go through the steps to reproduce (listed in C1) twice in a row. I suspect there's a lifecycle issue somewhere, something that gets destructed /set to null and isn't passed a new value between the first and second invocation.

wxhusst@'s reasoning in C21 makes sense to me but it's odd to me that it needs to be done twice to crash.

Regardless, in my opinion when the tab closes, the NearbyShare bubble should also close with it (not sure if Nearby Share will have different thoughts on this). But if that's the behaviour we decide to go with, you can call SharesheetService::CloseBubble when SharingHubBubbleController destructs (with the WebContents).

### js...@chromium.org (2021-08-09)

[triage]

### ha...@chromium.org (2021-08-09)

[Empty comment from Monorail migration]

[Monorail components: -OS>Systems>Multidevice>Nearby]

### me...@chromium.org (2021-08-12)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Sharing]

### me...@chromium.org (2021-08-12)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-08-12)

Would you like to set the type to Bug-Security?

### wx...@gmail.com (2021-08-23)

  It will not crash after my patch

### wx...@gmail.com (2021-08-23)

oh, in my patch 
```
       base::BindOnce(&SharingHubBubbleController::OnSharesheetClosed,
-                     base::Unretained(this)));
+                     weak_ptr_factory_.GetWeakPtr());   // here should be weak_ptr_factory_.GetWeakPtr()))
```

### kr...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-09-01)

[Empty comment from Monorail migration]

### bi...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### bi...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### bi...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e0e1b4522a43cfeb146bd2c8f3dea922fcc27509

commit e0e1b4522a43cfeb146bd2c8f3dea922fcc27509
Author: Kristi Park <kristipark@chromium.org>
Date: Thu Sep 09 01:25:45 2021

[CrOSSharingHub] Close sharesheet if tab is closed

Fix issue where sharesheet remains open if the associated tab is closed.

Bug: 1234050
Change-Id: Icf5fb86853f4f4d1889b4b5d52c81f7b47e7aa0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3149505
Commit-Queue: Kristi Park <kristipark@chromium.org>
Reviewed-by: Travis Skare <skare@chromium.org>
Cr-Commit-Position: refs/heads/main@{#919546}

[modify] https://crrev.com/e0e1b4522a43cfeb146bd2c8f3dea922fcc27509/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc
[modify] https://crrev.com/e0e1b4522a43cfeb146bd2c8f3dea922fcc27509/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.h


### kr...@chromium.org (2021-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-09)

This bug requires manual review: We are only 11 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2021-09-09)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-09-09)

1. Yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/3149505
3. Has not landed, verified on local build.
4. No
5. Security fix for new feature
6. Yes
7. Yes
8. N/A

### am...@chromium.org (2021-09-10)

readjusting type to Bug-Security (as this appears to be a UAF in the browser process) so that this fixed issue will be updated with appropriate merge review process labeling and VRP labeling by Sheriffbot.

### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-09-14)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-09-14)

Hello, this bug just influence os-chrome, not linux

### sr...@google.com (2021-09-15)

adjusting label to CrOS only per https://crbug.com/chromium/1234050#c50

### am...@chromium.org (2021-09-15)

merge approved to M94, please go ahead and merge to branch 4606. 

### wx...@gmail.com (2021-09-15)

Can I get a cve in this bug report?

### am...@chromium.org (2021-09-15)

CVEs are issued once a patch is being included in a stable channel release. 

### wx...@gmail.com (2021-09-15)

Thanks sincerely!

### am...@google.com (2021-09-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### wx...@gmail.com (2021-09-15)

:) thank you.

### am...@chromium.org (2021-09-15)

Huzzah! Congratulations - the VRP Panel has decided to award you $15,000 for this report. Nice work!

### am...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-09-17)

Hello, I find a uaf that caused by this fix. I submit it as https://crbug.com/chromium/1249491

### [Deleted User] (2021-09-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2021-09-20)

Unfortunately, this is a messy merge since https://crrev.com/c/3109413 did not make it to 94. Opting to leave this fixed in 95 and address the follow up https://crbug.com/chromium/1249491 at the same time.

### ts...@chromium.org (2021-09-20)

I'm not sure whether we should be avoiding the merge here, my understanding is that this would mean M94 would be impacted on stable channel (where this bug was previously Security_Impact-None). On top of that, M95 is being skipped for CrOS, so it wouldn't be fixed until 96.

Can someone from the security team (amyressler@?) confirm what the right move is here?

### kr...@chromium.org (2021-09-21)

Oh, I was not aware that CrOs is skipping M95. I'll work on the M94 merge, but it won't be very clean.

### am...@chromium.org (2021-09-21)

Thanks, kristipark@ and apologies for the backmerging pains! Yes, we should definitely get this into M94 especially given the ChromeOS release plan. 

### kr...@chromium.org (2021-09-23)

Re-adding the merge approved label that I removed

### [Deleted User] (2021-09-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-09-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5da95385de4f13da4b42a586c6745df1aba624a1

commit 5da95385de4f13da4b42a586c6745df1aba624a1
Author: Kristi Park <kristipark@chromium.org>
Date: Thu Sep 30 01:20:37 2021

[M94][CrOSSharingHub] Close sharesheet if tab is closed

Fix issue where sharesheet remains open if the associated tab is closed.

(cherry picked from commit e0e1b4522a43cfeb146bd2c8f3dea922fcc27509)

Bug: 1234050
Change-Id: Icf5fb86853f4f4d1889b4b5d52c81f7b47e7aa0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3149505
Commit-Queue: Kristi Park <kristipark@chromium.org>
Reviewed-by: Travis Skare <skare@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#919546}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3163104
Cr-Commit-Position: refs/branch-heads/4606@{#1259}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/5da95385de4f13da4b42a586c6745df1aba624a1/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc
[modify] https://crrev.com/5da95385de4f13da4b42a586c6745df1aba624a1/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.h


### rz...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ce...@google.com (2022-09-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1234050?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Apps>Foundation>Sharesheet, UI>Browser>Sharing]
[Monorail mergedwith: crbug.com/chromium/1234059, crbug.com/chromium/1237868, crbug.com/chromium/1244420]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056709)*
