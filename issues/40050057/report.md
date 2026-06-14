# Security: Regression : 'Press Esc to exit fullscreen' warning doesn't display 

| Field | Value |
|-------|-------|
| **Issue ID** | [40050057](https://issues.chromium.org/issues/40050057) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen, UI>Browser>FullScreen |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | sd...@chromium.org |
| **Created** | 2019-09-04 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version: 78.0.3903.0 (Developer Build) (64-bit)  

Operating System: Mac

**REPRODUCTION CASE**

1. Go to <https://permission.site/>
2. Click on Fullscreen

Actual:  

The 'Press Esc to exit fullscreen' warning doesn't display.

Expected:  

The 'Press Esc to exit fullscreen' warning should be displayed when you click on Fullscreen

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 831.4 KB)

## Timeline

### ch...@gmail.com (2019-09-04)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-09-04)

Does this reproduce in a fresh profile? I can reproduce only after visiting the site before in fullscreen, which might be intentional/non-regression.

[Monorail components: Blink>Fullscreen]

### es...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-09-05)

I can repro this on a fresh profile as well, but sometimes the fullscreen-warning doesn't disappear.

### sh...@chromium.org (2019-09-05)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2019-09-05)

On Windows the fullscreen-warning doesn't disappear. This is definitely a regression issue seen Canaray on Mac. 

### es...@chromium.org (2019-09-05)

Ok, yes, I can repro in 78.0.3903.0. I couldn't repro in 78.0.3902.0 I think so this is probably a recent regression.

[Monorail components: UI>Browser>FullScreen]

### ch...@gmail.com (2019-09-05)

Thanks for the update!

Shouldn't be Sev-Medium like in https://crbug.com/chromium/623862?

### es...@chromium.org (2019-09-06)

Hmm, it looks like we've triaged these inconsistently in the past. e.g. https://crbug.com/chromium/927150 and 812769 were triaged as Low severity.

Based on https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md, not showing the fullscreen warning would seem to be Medium ("allows web content to tamper with trusted browser UI"), so I'll go with that.

Doing a bisect now.

### es...@chromium.org (2019-09-06)

This bisected to https://chromium.googlesource.com/chromium/src/+/d78d971064ef0c1b4418a3fecf9c20fed2a84411, which looks like it could possibly be related, but not an obvious culprit. magchen, could please take a look and see if this looks at all related? also cc'ing some people who have worked on fullscreen notification before

### es...@chromium.org (2019-09-06)

By the way, I noticed during the bisect that the warning does actually appear after a few seconds (maybe around the time that the warning would normally fade away?), but just momentarily.

### ma...@chromium.org (2019-09-06)

https://chromium.googlesource.com/chromium/src/+/d78d971064ef0c1b4418a3fecf9c20fed2a84411 - Fix the GPU watchdog restart on Linux.

This CL only affects Linux and ChromeOS that the GPU process will be killed and restarted if the GPU hangs. Mac and WIndows has this code running for long time.
If this bug also happens in Mac and Windows, then my CL has nothing to do with this bug. Also this piece of code is only enabled by Finch. It's disabled by default. If your system didn't have this GPUWatchdogV2 feature enabled, it's not caused by my CL.

Hi estark@, Could you please confirm it?

### ma...@chromium.org (2019-09-06)

Sorry, I take it back. The second information is wrong. The change also runs on the systems without Finch. Please ignore it.
(But it's still correct that it won't affect Mac and Windows.)

### es...@chromium.org (2019-09-06)

Ok, thanks for the extra info, magchen. Reassigning to avi: are you still working in this area, Avi? Also cc estade who touched this code recently.

### sh...@chromium.org (2019-09-07)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-07)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-09-09)

I can't reproduce this on tip of tree (r694425) on Chrome OS or Linux. estark@, were you actually able to repro on the other desktop platforms? My interpretation of c#6 is that the bug doesn't occur on Windows, and we only have a confirmed report on Mac.

I touched fullscreen here[1] but it was at the end of June, so I don't think the timing aligns with a regression in the 78.0.3902.0 => 78.0.3903.0 range; also there was no mac specific code there.

Back to Avi.

(p.s. also seems worth it to try to bisect again as the result of the last bisect seems unlikely to be right. Maybe the bug is flaky?)

[1] https://chromium-review.googlesource.com/c/chromium/src/+/1666148

### sd...@chromium.org (2019-09-09)

I’m going to grab this for the moment because it might be a change of mine (r691184).

### sd...@chromium.org (2019-09-09)

CL is up: https://chromium-review.googlesource.com/c/chromium/src/+/1790378

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/079facd978d5c3a745281bcd885f48159244d7c9

commit 079facd978d5c3a745281bcd885f48159244d7c9
Author: Sidney San Martín <sdy@chromium.org>
Date: Mon Sep 09 19:57:57 2019

Mac: Fix fullscreen warning bubble only displaying intermittently.

Sometimes, a browser window isn't considered "on the current space"
during the fullscreen transition at the moment the exclusive access
bubble is displayed. Fix by checking again at the end of the transition.

Bug: 1000882
Change-Id: Ia2ef081098ca84f975dd26dfa6bf2615a3094af7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1790378
Auto-Submit: Sidney San Martín <sdy@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#694863}

[modify] https://crrev.com/079facd978d5c3a745281bcd885f48159244d7c9/components/remote_cocoa/app_shim/native_widget_ns_window_bridge.mm


### sd...@chromium.org (2019-09-09)

This should be fixed, please verify in an upcoming Canary. A merge will also be needed.

### bu...@chromium.org (2019-09-09)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-78; it appears the fix may have landed after branch point, meaning a merge might be required. The owner of this bug should confirm if a merge is required here. If so, add Merge-Request-78 label and indicate which commits/CLs are to be merged. Otherwise, remove Merge-TBD label. Thanks.

### sh...@chromium.org (2019-09-10)

[Empty comment from Monorail migration]

### sd...@chromium.org (2019-09-10)

[Empty comment from Monorail migration]

### sr...@google.com (2019-09-11)

sdy@ pls add a merge request label for M78 and remove merge-tbd 

### sd...@chromium.org (2019-09-11)

I was waiting to hear from someone else on whether their original issue is fixed. But, it seems to be better for me, so I’ll request a merge.

### sh...@chromium.org (2019-09-11)

This bug requires manual review: We don't branch M78 until 2019-09-05.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sd...@chromium.org (2019-09-11)

1. Yes
2. r694863
3. Yes
4. Security regression
5. No
6. n/a

### sr...@google.com (2019-09-12)

Approved for merge to M78, branch:3904

### sr...@google.com (2019-09-13)

Please get your merge to M78 branch 3904 complete by EOD today friday sept 13 PST. 

I would like to include all the merges into dev RC build which will be triggered on monday

### sd...@chromium.org (2019-09-13)

FYI: I merged this (7650a8bdeefc341a72146aa6b202aa4e25ebbdac), but it looks like bugdroid hasn't shown up yet.

### sr...@google.com (2019-09-16)

Please help complete your merges to branch 3904 by 12pm PST today, ( Sept 16).  If . the merge is already complete, pls help remove the merge-approved-78 label from the bug. 

### sd...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $3,000 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1000882?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fullscreen, UI>Browser>FullScreen]
[Monorail mergedwith: crbug.com/chromium/1002454]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050057)*
