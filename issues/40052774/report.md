# Security: Information disclosure through screenshare with clickjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [40052774](https://issues.chromium.org/issues/40052774) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ga...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2020-07-05 |
| **Bounty** | $2,000.00 |

## Description

Hello Security Team,

Before the screen transmission starts, a dialog box appears. This dialog window is displayed in the middle of the browser and only 2 clicks are enough to start the screen transmission. This can be used by attackers who want to get important information. I have created a video demonstration where you can see how theoretically attackers can get private Google information (The video is attached).

In the example I have created a cookie clicker website where you have to click on a cookie as fast as possible. To make the user press the cookie faster, the counter gets smaller every 200 milliseconds. 

From the 12th click the dialog window with the screen Transfer appears. Many users would click at least twice more from Reflex and transfer their screen contents. Once this is done, a callback is performed, where a tab with account information is opened. Meanwhile, the screen content is sent to the attacker. The victim has little time to close the screen transmission and will not understand what is going on. In the end the attacker has the information. 

Theoretically you could also get the phone number for the 2 factor authentication this way, but unfortunately I have not linked one to this account, so it is not visible in the demonstration.

There are many websites that forget to censor sensitive information and in the same way criminals could get information.

I have the following solutions for this problem:
- Screen contents can only be transmitted in 5 seconds. (Add delay)
- Move the window to a different position where the user cannot misunderstandably click on it.

I wrote the PoC code in NodeJS, so you can reproduce it.

In my opinion, this is a simple but critical thing. Personally, I would have fallen for that trick.

Best Regards
David Albert

## Attachments

- [2020-07-05 01-52-07.mp4](attachments/2020-07-05 01-52-07.mp4) (video/mp4, 5.0 MB)
- [PoC.zip](attachments/PoC.zip) (application/octet-stream, 4.0 KB)
- [Bildschirmfoto 2020-07-05 um 02.57.42.png](attachments/Bildschirmfoto 2020-07-05 um 02.57.42.png) (image/png, 237.7 KB)
- [Bildschirmfoto 2020-07-05 um 16.49.24.png](attachments/Bildschirmfoto 2020-07-05 um 16.49.24.png) (image/png, 96.2 KB)

## Timeline

### ga...@gmail.com (2020-07-05)

Here is an example with a phone number

### ga...@gmail.com (2020-07-05)

Visited links can be marked accordingly by CSS. Thus the attacker knows whether and which pages were visited. Now you can create such a page and open it in the new tab as well. There are a variety of things you can do with it. To find out the user's privacy or profile. Attackers could read out private ones of porn visitors (for example) and blackmail them later. But this is only one example. I just want to prove the importance of the vector. 

### ga...@gmail.com (2020-07-05)

For example, in Firefox you should select the screen from the drop-down list and press the button. Because only then it will become clickable. Maybe you can find a similar solution.

### ca...@chromium.org (2020-07-06)

Assigning high severity to be on the safe side since this seems easy to clickjack due to the large click target.



[Monorail components: Internals>Media>ScreenCapture]

### ca...@chromium.org (2020-07-06)

[Comment Deleted]

### ca...@chromium.org (2020-07-06)

miu: Can you PTAL and help further triage this (and reassign as appropriate)? Thanks.

### ga...@gmail.com (2020-07-07)

This is my first time here. does this page belong to the Google Bug Bounty program? Best Regards

### ga...@gmail.com (2020-07-07)

In my opinion, the vulnerability is really of great value.  You can build a project from the PoC and use it en masse.  If 100 victims fall into it, you have 100 folders with screenshots.  Spammers could also take advantage of this by generating links that have the victim's email in the parameter.  The email is then the folder name, for example

### mi...@chromium.org (2020-07-07)

Seeking a more-appropriate owner. marinaciocea@: Is that you?

[Monorail components: -Internals>Media>ScreenCapture Blink>GetUserMedia>Desktop]

### gu...@chromium.org (2020-07-07)

ellyjones@: provisionally assigning to you, since you owns this UI flow.
cc adetaylor@ to help assess the security aspect of this issue.

### [Deleted User] (2020-07-07)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-07)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-07-07)

Re https://crbug.com/chromium/1102153#c10, I'm happy with Carlos' assessment of High in https://crbug.com/chromium/1102153#c4 especially as he's an expert on UI spoofs and I'm not :)

garkolym@ thanks for the report and welcome to the community of Chrome bug submitters. If this is deemed to be a valid bug and is fixed, we would normally credit you in the Chrome release notes. How would you like to be credited? "David Albert"?


### ga...@gmail.com (2020-07-07)

Yes, it would be great. Is this report enough to get a reward?

### ad...@chromium.org (2020-07-07)

The process is this: first of all it will go through initial triage ('sheriffing') which has been done. From that initial triage, this does look like a valid bug. The relevant engineering teams will then set about fixing it. At any point they might discover it's not a valid bug, or is a duplicate of some previously-reported or known issue. In such a case it would not be rewardable. If it survives as far as actually being fixed, then you'll be credited in the Chrome release notes and it will get a CVE assigned. Finally, it will go to the VRP panel who will decide whether it merits a reward. That usually happens 1-4 weeks after the fix is made.

So... TL;DR: maybe :)

### ga...@gmail.com (2020-07-07)

I can't wait to hear the results. :) I'm really looking forward to it. This will be my first CVE. I'd like to take this opportunity to thank you for the quick answers. With the amount of work you have to do, this cannot be taken for granted.

### ga...@gmail.com (2020-07-14)

[Comment Deleted]

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-19)

ellyjones: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2020-07-22)

Fix CL: https://chromium-review.googlesource.com/c/chromium/src/+/2313156

### ga...@gmail.com (2020-07-23)

Nice commits, that should solve the problem.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5020f8a4e75234b09d800815b4e4b320c463e293

commit 5020f8a4e75234b09d800815b4e4b320c463e293
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Thu Jul 23 17:40:20 2020

cbuiv desktopmedia: disallow selecting sources by double-click

See the bug for details about why.

Bug: 1102153
Change-Id: I71423c13405cfd57a1eee024205c48145af18009
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2313156
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/master@{#791283}

[modify] https://crrev.com/5020f8a4e75234b09d800815b4e4b320c463e293/chrome/browser/ui/views/desktop_capture/desktop_media_list_view.cc
[modify] https://crrev.com/5020f8a4e75234b09d800815b4e4b320c463e293/chrome/browser/ui/views/desktop_capture/desktop_media_list_view.h
[modify] https://crrev.com/5020f8a4e75234b09d800815b4e4b320c463e293/chrome/browser/ui/views/desktop_capture/desktop_media_picker_views_test_api.cc
[modify] https://crrev.com/5020f8a4e75234b09d800815b4e4b320c463e293/chrome/browser/ui/views/desktop_capture/desktop_media_picker_views_unittest.cc
[modify] https://crrev.com/5020f8a4e75234b09d800815b4e4b320c463e293/chrome/browser/ui/views/desktop_capture/desktop_media_source_view.cc


### el...@chromium.org (2020-07-24)

Given the SecImpact from #4 I'm going to request a merge to 85.

### ad...@chromium.org (2020-07-24)

Please mark this as Fixed if it is. I'll add a merge request for 84 as well which would be normal for high severity security bugs. Could you comment on stability risks here Elly? To merge back to M84 we have to regard it as almost entirely risk-free since it loses out on a lot of bake time. (Sheriffbot will also give you a formal questionnaire when this is marked as fixed).

### [Deleted User] (2020-07-24)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-07-27)

adetaylor@ please approve this for M85 beta if you think this is good for merge to M85 as well

### el...@chromium.org (2020-07-27)

#25:
1. Yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/2313156
3. Yes
4. To fix a Severity-High security bug
5. No
6. N/A

### ad...@chromium.org (2020-07-27)

Approving merge to M85, branch 4183, assuming no related problems have shown up in Canary. I'll go through and approve M84 merges when we're a bit closer to making another M84 release.

### ga...@gmail.com (2020-07-27)

On Chrome Canary version 86.0.4214.0 its fixed!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2ebdbed786d629308beec2e7836db558d6682925

commit 2ebdbed786d629308beec2e7836db558d6682925
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Tue Jul 28 15:36:20 2020

cbuiv desktopmedia: disallow selecting sources by double-click

See the bug for details about why.

(cherry picked from commit 5020f8a4e75234b09d800815b4e4b320c463e293)

Bug: 1102153
Change-Id: I71423c13405cfd57a1eee024205c48145af18009
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2313156
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#791283}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2323134
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#996}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/2ebdbed786d629308beec2e7836db558d6682925/chrome/browser/ui/views/desktop_capture/desktop_media_list_view.cc
[modify] https://crrev.com/2ebdbed786d629308beec2e7836db558d6682925/chrome/browser/ui/views/desktop_capture/desktop_media_list_view.h
[modify] https://crrev.com/2ebdbed786d629308beec2e7836db558d6682925/chrome/browser/ui/views/desktop_capture/desktop_media_picker_views_test_api.cc
[modify] https://crrev.com/2ebdbed786d629308beec2e7836db558d6682925/chrome/browser/ui/views/desktop_capture/desktop_media_picker_views_unittest.cc
[modify] https://crrev.com/2ebdbed786d629308beec2e7836db558d6682925/chrome/browser/ui/views/desktop_capture/desktop_media_source_view.cc


### ga...@gmail.com (2020-08-02)

Statusupdate?

### el...@chromium.org (2020-08-03)

Bug is fixed on 85 and 86. I'm awaiting a decision from adetaylor@ on an 84 merge. I won't mark this Fixed until we've conclusively decided whether to land the fix on 84 or not.

### ad...@google.com (2020-08-03)

OK, if no problems have shown up, please merge to M84, branch 4147.

ellyjones@, for security bugs, we normally mark them as Fixed *then* do all the merging stuff, otherwise Sheriffbot gets confused. I appreciate this is the opposite practice to some teams; I can't explain that anomaly; one day I'll look into it...

### el...@chromium.org (2020-08-04)

#33: Merge to 84: https://chromium-review.googlesource.com/c/chromium/src/+/2333680

If the bugs are marked Fixed before they are merged, how does one tell which bugs might need further merges?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1857273a028472f72de817a6752ce07d10a46487

commit 1857273a028472f72de817a6752ce07d10a46487
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Tue Aug 04 14:56:02 2020

cbuiv desktopmedia: disallow selecting sources by double-click

See the bug for details about why.

(cherry picked from commit 5020f8a4e75234b09d800815b4e4b320c463e293)

Bug: 1102153
Change-Id: I71423c13405cfd57a1eee024205c48145af18009
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2313156
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#791283}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2333680
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#1017}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/1857273a028472f72de817a6752ce07d10a46487/chrome/browser/ui/views/desktop_capture/desktop_media_list_view.cc
[modify] https://crrev.com/1857273a028472f72de817a6752ce07d10a46487/chrome/browser/ui/views/desktop_capture/desktop_media_list_view.h
[modify] https://crrev.com/1857273a028472f72de817a6752ce07d10a46487/chrome/browser/ui/views/desktop_capture/desktop_media_picker_views_test_api.cc
[modify] https://crrev.com/1857273a028472f72de817a6752ce07d10a46487/chrome/browser/ui/views/desktop_capture/desktop_media_picker_views_unittest.cc
[modify] https://crrev.com/1857273a028472f72de817a6752ce07d10a46487/chrome/browser/ui/views/desktop_capture/desktop_media_source_view.cc


### el...@chromium.org (2020-08-04)

84 merge is complete.

### ad...@chromium.org (2020-08-04)

> If the bugs are marked Fixed before they are merged, how does one tell which bugs might need further merges?

Because the release TPMs and me ruthlessly nag people who have outstanding merges :)

To look at it the other way, if bugs _aren't_ marked Fixed when they're fixed, how should sheriffbot and the release TPMs know to request merges? It's not reasonable to expect every Chrome engineer to understand our esoteric merge rules for security bugs.

### [Deleted User] (2020-08-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-13)

Congratulations! The VRP panel decided to award $2000 for this report. Thanks!

### ad...@google.com (2020-08-13)

(Someone from our finance team will be in touch to arrange payment.)

### ad...@google.com (2020-08-13)

[Empty comment from Monorail migration]

### ga...@gmail.com (2020-08-14)

Thanks a lot guys! Where will I be contacted, by email? Best Regards

### ad...@chromium.org (2020-08-14)

Yes, you should expect an e-mail. Thanks!

### ga...@gmail.com (2020-08-14)

Thank you

### el...@chromium.org (2020-09-11)

[Empty comment from Monorail migration]

### el...@chromium.org (2020-09-11)

Reopening this bug to issue another fix. Currently starting screen share from "Chromium Tab" works with double clicking as that is created as a TableView rather than a DesktopMediaSourceView which is used for "Your Entire Screen" and "Application Window". 

### [Deleted User] (2020-09-11)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-09-11)

elainec@ - sorry - it'll mess with merging, release notes, VRP and CVE systems if you re-use this bug for another fix. I took the liberty of raising https://crbug.com/chromium/1127496 for the new issue you've identified.

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### ga...@gmail.com (2020-09-29)

I have given my bank details and all other details and I am not getting the money. Are there things I still have to do? Best Regards

### ad...@chromium.org (2020-09-29)

Unfortunately the first payment for a given recipient can take a little while. Sorry for the delay. I have confirmed that things are in process, but it looks like it may still be another few weeks before all the stages of our complicated finance process have actually completed.

### ga...@gmail.com (2020-12-15)

I know it doesn't belong here right now, but I don't know what to do. I can't get into my email account anymore and the only 2 factor option I have is the backup codes. I don't have them anymore. I had a lot more options, like restoring via this email. When I click on help, I immediately get to a page that I could not be confirmed. I would be very grateful if you could help me. I use this account to manage my Adsense revenue.

Email: bufinoclown@gmail.com

I don't see any other way to fix the problem. Because the restore options are completely gone and only the backup codes are left. I have set my email that I use here as the recovery email (garkolym@gmail.com)
Again, I'm sorry to put this in here, I don't know what to do. I've had this problem for months.

### el...@chromium.org (2020-12-15)

#56: That's unfortunate but I don't have anything to do with Google accounts. :(

### [Deleted User] (2020-12-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1102153?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052774)*
