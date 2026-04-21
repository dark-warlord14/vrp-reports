# uaf in BrowserSwitchHandler::OnLaunchFinished

| Field | Value |
|-------|-------|
| **Issue ID** | [40058583](https://issues.chromium.org/issues/40058583) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise>BrowserSwitcher |
| **Platforms** | Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2022-01-25 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36

Steps to reproduce the problem:
1.
2.
3.a

What is the expected behavior?

What went wrong?
a

Did this work before? N/A 

Chrome version: 97.0.4692.99  Channel: stable
OS Version: 10.0

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.1 KB)
- [0001-uaf-issue-1290700.patch](attachments/0001-uaf-issue-1290700.patch) (text/plain, 2.5 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 20.0 MB)
- [test.png](attachments/test.png) (image/png, 305.9 KB)

## Timeline

### [Deleted User] (2022-01-25)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-01-25)

1. patch chrome to make it easy to trigger uaf
2. open two blank tab, choose one to enter chrome://browser-switch/internals
3.open devtools and enter js 
```
    var arr1 = ["test", "https://www.google.com"];
  chrome.send("launchAlternativeBrowserAndCloseTab", arr1);
```
4. when the browser hang, click the button of close the tab

### wx...@gmail.com (2022-01-25)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-01-26)

Thanks for the report, it seems that the patch introduces a base::Unretained, which might be the source of this UaF. Could you give more details about what the patch does and how this could be triggered from a renderer? Thanks

### ca...@chromium.org (2022-01-26)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-01-26)

HandleLaunchAlternativeBrowserAndCloseTab will enter function BrowserSwitchHandler::OnLaunchFinished, and BrowserSwitchHandler::OnLaunchFinished will use 
base::ThreadTaskRunnerHandle::Get()->PostTask(
+        FROM_HERE,
+        base::BindOnce(&content::WebContents::ClosePage,
+                       base::Unretained(web_ui()->GetWebContents())));

My patch just put it forward  to make us easy to reach this code path

### [Deleted User] (2022-01-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-01-27)

Thanks for the clarification, I believe the patch is still meaningfully changing the code, since normally that call using a base::Unretained is called from AlternativeBrowserDriverImpl::TryLaunch, which posts it using base::TaskPriority::USER_BLOCKING priority and base::TaskShutdownBehavior::BLOCK_SHUTDOWN shutdown behavior, which might prevent this. Can you reproduce while still going through TryLaunch? Basically leaving the Sleep(4000) in, but keeping the call to TryLaunch.

### wx...@gmail.com (2022-01-28)

I try to this patch, and still could reproduce. I use Sleep(4000), because without it, I think it is hard to reproduce.Time is too short. If you don't think it has security influence, you can set it to won't-fix.

### [Deleted User] (2022-01-28)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-01-31)

I was not able to reproduce this myself on Linux, so this might be Windows specific, traging as valid since video proof was included. Triaging as High since this is in the browser process, but requires user interaction by closing the tab.

nicolaso: Passing to you since you've worked with the relevant code before, can you PTAL and reassign as appropriate? Thanks.

[Monorail components: Enterprise>BrowserSwitcher]

### [Deleted User] (2022-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-08)

nicolaso: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@chromium.org (2022-02-09)

This seems _really_ difficult to repro in real environments, and AFAICT there are no crash reports with this signature. So it's probably not too big a deal.

That being said, this code should still use WeakPtr, so we're on the safe side. Fix is out for review, at crrev.com/c/3450459

### gi...@appspot.gserviceaccount.com (2022-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ce87670f70a41beb1a2293582fd5dde70f0092a2

commit ce87670f70a41beb1a2293582fd5dde70f0092a2
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date: Thu Feb 10 12:18:43 2022

[BrowserSwitcher] Use a WeakPtr when closing chrome://browser-switch

After opening a site in the alternative browser, we close the
chrome://browser-switch. This was done by posting a task on a
WebContents's raw pointer. This can theoretically cause a use-after-free
bug; post the task using a WeakPtr so it's safer.

Bug: 1290700
Change-Id: I6bfbaa95b22adb54148616a7971cff1a8ebbcbcc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3450459
Auto-Submit: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Reviewed-by: Julian Pastarmov <pastarmovj@chromium.org>
Commit-Queue: Julian Pastarmov <pastarmovj@chromium.org>
Cr-Commit-Position: refs/heads/main@{#969390}

[modify] https://crrev.com/ce87670f70a41beb1a2293582fd5dde70f0092a2/chrome/browser/ui/webui/browser_switch/browser_switch_ui.cc


### ni...@chromium.org (2022-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-10)

Requesting merge to stable M98 because latest trunk commit (969390) appears to be after stable branch point (950365).

Requesting merge to beta M99 because latest trunk commit (969390) appears to be after beta branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-11)

Merge review required: M99 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-11)

Merge review required: M98 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@chromium.org (2022-02-11)

1. This is a 2-line change. Potential security bug; hard to tell if it's actually meaningful, as this is a hard-to-trigger race condition (how hard?...).
2. crrev.com/c/3450459
3. Released yes, tested no.
4. N/A
5. N/A
6. No

### ni...@chromium.org (2022-02-11)

Also, a bit more context RE: #1 for release TPMs: this entire bug is hidden behind an enterprise policy (with ~8M users total). It also requires the user opening chrome://browser-switch/internals (a debugging page) and closing it manually as part of the race condition.

There's a lot of steps/conditions to repro this bug, and I still can't repro it locally without patching Chrome. As a result, I'm tempted *not* to merge it into Stable/Beta. Unless carlosil@ has a strong opinion on this

### am...@chromium.org (2022-02-11)

Based on the limited amount of bake time this fix has had on canary + the mitigating factors (direct interaction with dev tools + closing tab) and race condition, let's go ahead and hold this back from merge just yet and not include this in M98 respin. 

We should revisit merging to M99 next week as that will become Stable channel with a 1 March release.  But I concur there are significant mitigating factors that backmerging this to M98 for Extended may not be necessary. 

### am...@chromium.org (2022-02-17)

Based on all the assessment above, based on all the mitigations, it's a bit rac-y, and gestures required, I'm bumping this down to medium severity. nicolaso@ and carlosil@ please let me know if you disagree and feel free to readjust accordingly. 

@nicolaso@ -- Also approving for merge to M99. There is another M99 beta release next week (RC cut Tuesday), if you want to get this into next beta, please merge to branch 4844 ASAP/ prior to Tuesday. Based on reservations expressed in https://crbug.com/chromium/1290700#c27 above, I am also okay with withholding merge until after Tuesday so this can just be part of M99 for Stable release instead. Please let me know if there are any concerns or issues with either above. 

### pb...@google.com (2022-02-17)

[Bulk update] Your change has been approved for M99 branch please refer to go/chrome-branches for branch info and merge the CL's to M99 branch manually asap so that they would be part of next week's M99 Beta release.

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Hello, thank you for this report and your efforts. Due to the number of mitigations to triggering this bug, the VRP Panel has decided to award you $2000 for this report. If you can provide an improved POC we would be happy to reassess for a potential change in reward amount. 

### wx...@gmail.com (2022-02-17)

Oh, I will try to make an extension to reproduce it today.

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-21)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@chromium.org (2022-02-22)

M99 merge in flight here: crrev.com/c/3480499

### gi...@appspot.gserviceaccount.com (2022-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9c0616145e98f318bf886bee49a6fa75962c7bd6

commit 9c0616145e98f318bf886bee49a6fa75962c7bd6
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date: Tue Feb 22 16:54:35 2022

M99 merge: [BrowserSwitcher] Use a WeakPtr when closing chrome://browser-switch

After opening a site in the alternative browser, we close the
chrome://browser-switch. This was done by posting a task on a
WebContents's raw pointer. This can theoretically cause a use-after-free
bug; post the task using a WeakPtr so it's safer.

(cherry picked from commit ce87670f70a41beb1a2293582fd5dde70f0092a2)

Bug: 1290700
Change-Id: I6bfbaa95b22adb54148616a7971cff1a8ebbcbcc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3450459
Auto-Submit: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Reviewed-by: Julian Pastarmov <pastarmovj@chromium.org>
Commit-Queue: Julian Pastarmov <pastarmovj@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#969390}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3480499
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4844@{#765}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/9c0616145e98f318bf886bee49a6fa75962c7bd6/chrome/browser/ui/webui/browser_switch/browser_switch_ui.cc


### am...@chromium.org (2022-02-25)

while ordinarily I would strong suggest we backmerge fixes for issues affecting Enterprise features back to Extended given the impact; however, taking impact into consideration and based on this requiring significant and direct user interaction and a somewhat difficult to beat race condition to trigger, I'm going to concur we not merge this back to M98 

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-03-01)

Hello amy,  I would like to change my credit to " raven at KunLun Lab", and hello nicolaso,I submit https://crbug.com/chromium/1301840,I think you are the right owner.

### ni...@chromium.org (2022-03-01)

Unfortunately I don't have access to crbug.com/1301840. amyressler@, can you CC me on it?

### am...@chromium.org (2022-03-01)

thanks, raven. I've updated your acknowledgments/credit info as requested and is reflected in M99 stable release notes for today; nicolaso@ I've cc'ed you on https://crbug.com/chromium/1301840 as requested 

### [Deleted User] (2022-05-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1290700?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058583)*
