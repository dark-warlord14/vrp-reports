# Security: Forced user interaction for Hidden permission prompts by freezing/resizing the browser Bypass of 1371215 

| Field | Value |
|-------|-------|
| **Issue ID** | [40064841](https://issues.chromium.org/issues/40064841) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Windows |
| **Reporter** | el...@gmail.com |
| **Assignee** | fj...@chromium.org |
| **Created** | 2023-05-25 |
| **Bounty** | $3,000.00 |

## Description

# **VULNERABILITY DETAILS**

This issue is straight forward variation of <https://crbug.com/chromium/1371215> that was fixed in old permission prompt Surface at this commit <https://chromium.googlesource.com/chromium/src/+/764cdb906a602c684f70e381e90f964cd0ac78af> , duo to introducing new permission prompt Surface/UI the new variation found as discussed below, could you assign to same folks for better tracking the variations and for best fix , [tungnh@chromium.org](mailto:tungnh@chromium.org) solved the main one before so he might be aware enough about this area(thanks for considering this).

I've Poked around the main POC for making it working in Linux , and Windows chrome versions where new Surface/UI was introduced.

It is possible to trick a user into accepting a permission prompt (eg microphone/webcam) by tricking them into clicking rapidly in a window, and freezing the browser with the window.resizeBy() function, while clicking the cookie icon Resizing function (with high rate) make the prompt have no chance to be shown to the user and that clicks accept the prompt without being shown to the user ,bypassing google security measures for the prompt making the user accept permissions for malicious sites without seeing any prompts referring to Reference[1].

# References:

Docs (docs/security/security-considerations-for-browser-ui.md):  

[1] <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-considerations-for-browser-ui.md#introduce-a-short-delay-before-the-ui_s-call_to_action-activates>

# **VERSION**

## I've tested the Bug after the new surface/UI has been rolled out , also I've tested this with Chrome Canary in MacOS be the feature still not pushed to MacOS yet.

Bug Found-In : 115  

Components: UI>Browser>Permissions>Prompts  

**-------------------------** ----------------  

Bug Tested With the Following Properties:  

**-------------------------** ----------------  

Google Chrome:115.0.5773.4 (Official Build) dev (64-bit)  

Revision:f255fbf1fbd3eceb020c09db1d8e65f381700040-refs/branch-heads/5773@{#8}  

Version:115.0.5773.4  

Milestone:115  

Branch:5773  

Branch Base Position:1143970  

OS: Linux Ubuntu  

**-------------------------** ----------------  

Google Chrome 116.0.5791.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Revision:8b1fd9e623e6f91c0cb5b45a21d248b6f1b7f066-refs/branch-heads/5791@{#1}  

OS: Windows 11 Version 22H2 (Build 22621.1702)  

**-------------------------** ----------------  

MacOS Chrome Canary: Feature Not Introduced till the day of submission for this report, but can update here later.

# **REPRODUCTION CASE**

## I've made two PoCs for Windows and Linux.

1. Host the attached poc files to web server / or You Can try Live PoC's from URLs Below in Steps

[A]- for Windows [poc01-windows.html] ,or Live Poc URL :<https://vrphunt.com/chrome/spoof/poc01-windows.html>

[B]- for Linux [poc01.html],,or Live Poc URL :<https://vrphunt.com/chrome/spoof/poc01.html>

2. Click on 'Click to play!'

3[A].[for Windows] Put your mouse cursor on the Cookie and Rapidly click the cookie as shown in poc video below.  

3[B].[for Linux] Put your mouse cursor on the Cookie and double click the cookie.

4. The window will be resized in x and y quickly and frequently and force user into accepting the microphone permission without seeing the prompt at all.

---

+The POC-video demonstrates the above PoC working perfectly with no prompt showing up at all.

## ++Notes for Developing the Poc:

If the PoC did not work correctly, try to refine the values of times, open the HTML file and edit the "waitPerResize" variable to 2. If it still doesn't work, try values 4 and 6, but I've tuned this well (i think so) to work smoothly.

# Observed:

New Surface/UI permission prompt dialog made hidden which Bypass sensitive Google Security Measures in Chrome UI.

# Expected:

According to References[1] mentioned above

# If multiple clicks/gestures aren't feasible, consider introducing a short delay between when the browser UI is shown and the call-to-action activates. For example, if the user must click a button to grant a permission, introduce a delay before the button becomes active once the permission prompt is shown. Chrome uses short and long delays in various UI:

For large security-sensitive browser surfaces like interstitials, three seconds is typically considered a delay that is long enough to let the user notice that the UI is showing without being too disruptive to the typical user experience.

## For smaller UI surfaces such as dialog boxes, a shorter delay like 500ms can be more practical. InputEventActivationProtector is a helper class that ignores UI events that happen within 500ms of the sensitive UI being displayed.

## also User Should interact with sensitive browser UI ,which also should be Clear visible to the deal with and accept or /reject but not totally hidden .

# Mitigation/Fix:

Add CL to check if the permission prompt is already shown and intersect the Web-content area , then add appropriate time like reference stated between showing the prompt and accepting user input from user {at level of input protector}.

\*\*Poc Video of Windows Tests Directly Attached  

\*\*Local Offline Files (Poc) Directly Attached  

\*\*Poc Video of Linux Test will be provided later once I get back to office(recorded in my laptop).

# =================== **CREDIT INFORMATION**

# Reporter credit: Ahmed ElMasry

Thank you for your attention. with kind Regards.

## Attachments

- [poc01-windows.html](attachments/poc01-windows.html) (text/plain, 2.1 KB)
- [poc01.html](attachments/poc01.html) (text/plain, 2.1 KB)
- [Bypass-1371215-Canary-WIN- 2023-05-25 21-30-28-462.mp4](attachments/Bypass-1371215-Canary-WIN- 2023-05-25 21-30-28-462.mp4) (video/mp4, 3.3 MB)
- [Linux-repro-2023-05-29_12-05-49.mp4](attachments/Linux-repro-2023-05-29_12-05-49.mp4) (video/mp4, 1.4 MB)
- [linux-with moving mouse away-2023-05-29_12-26-21.mp4](attachments/linux-with moving mouse away-2023-05-29_12-26-21.mp4) (video/mp4, 1.4 MB)

## Timeline

### [Deleted User] (2023-05-25)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-05-29)

Hello..,

Poc Repro for Linux  with the above mentioned properties 

Google Chrome: 115.0.5773.4 (Official Build) dev (64-bit) 
Revision: f255fbf1fbd3eceb020c09db1d8e65f381700040-refs/branch-heads/5773@{#8}
OS:Linux
-------------
Note: i've updated the live poc for linux here https://vrphunt.com/chrome/spoof/poc01.html to be more optimized showing that the clicks takes it's place accepting the prompt before it actually be visible to user , also the repro in linux  with only two consecutive clicks (double click)

steps in linux:
1-open linux POC  https://vrphunt.com/chrome/spoof/poc01.html 
2- make the cursor on Cookie icon , and double click the icon 
3- check site permissions ,you will see permissions accepted before the permission bubble shown .

Just check the poc Video attached for the Repro.

Thanks

### el...@gmail.com (2023-05-29)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-06-02)

Thanks for the report. tungnh@ this seems to be a similar bug that was previously reported for the current permission prompt UI, but the same underlying issue can also affect a UI refresh in M115+. Could you take a look?

[Monorail components: UI>Browser>Permissions>Prompts]

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2023-06-07)

[BULK EDIT] This bug is marked as M115 Stable blocker and we are just two weeks away from M115 RC cut i.e., on June 20th, Please evaluate the bug and get the fix asap thank you.

### [Deleted User] (2023-06-09)

tungnh: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tu...@chromium.org (2023-06-12)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-06-12)

I think the new permission UI is not fully protected by input event protector.
@fjacky, you are working on a similar ticket to protect the new UI, is this a duplicate one?

### fj...@chromium.org (2023-06-12)

I assume you're referring to crbug.com/1451322 and crbug.com/1451308. I haven't had sufficient capacity to address them yet. Seems similar but can't confirm yet. Both reports were made a week ago, so if they're the same, this one would be the first report.

### pb...@google.com (2023-06-12)

[BULK EDIT] M115 Stable RC cut is on June 20th. Please evaluate the issue if it's indeed a blocker or not, If it's blocker please consider them as high priority and get them fixed asap.

### fj...@chromium.org (2023-06-12)

I'll remove the ReleaseBlock label because the involved feature flag can be disabled. However, I'll try to find and merge a fix asap so we can avoid doing that.

### [Deleted User] (2023-06-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fj...@chromium.org (2023-06-13)

CCing avi@ for code review context.

### fj...@chromium.org (2023-06-15)

[Empty comment from Monorail migration]

### fj...@chromium.org (2023-06-15)

[Empty comment from Monorail migration]

### en...@chromium.org (2023-06-15)

Setting M116 as target otherwise Sheriffbot keeps marking this as RBS. The new UI is Finch-gated, so it won't go live suddenly when M115 hits Stable.

### be...@google.com (2023-06-15)

Adding Hotlist-RBS-Removed for tracking purposes.

### gi...@appspot.gserviceaccount.com (2023-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2e59e92b7601ffa3b7f55257bb2172d5e204cb43

commit 2e59e92b7601ffa3b7f55257bb2172d5e204cb43
Author: Florian Jacky <fjacky@chromium.org>
Date: Fri Jun 16 14:10:06 2023

Support input protection in new permissions UI

Bug: 1449007,1451308,1451322,1453929
Change-Id: I9266184f5d8de3d030fdc280a12222111eb4b0f5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4604326
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Florian Jacky <fjacky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1158804}

[modify] https://crrev.com/2e59e92b7601ffa3b7f55257bb2172d5e204cb43/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/2e59e92b7601ffa3b7f55257bb2172d5e204cb43/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/2e59e92b7601ffa3b7f55257bb2172d5e204cb43/chrome/browser/ui/views/permissions/permission_prompt_bubble_base_view.cc
[modify] https://crrev.com/2e59e92b7601ffa3b7f55257bb2172d5e204cb43/chrome/browser/ui/views/permissions/permission_prompt_bubble_base_view.h


### fj...@chromium.org (2023-06-16)

[Empty comment from Monorail migration]

### fj...@chromium.org (2023-06-16)

1. Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
This merge fixes a security issue (click jacking)

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/4604326

3. Have the changes been released and tested on canary?
They have not yet landed on canary, but have been manually verified by 2 SWEs on the merged commit.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
This is a new UI that is fully behind a finch flag. There is an active experiment on canary and beta (115 and 116)

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
N/A

### [Deleted User] (2023-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-17)

Merge review required: M115 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-06-18)

Hello Florian  and Avi..,
===========
Thanks for all your great efforts fixing this issue.!

**[From my side i can confirm that issue has been fully fixed tightly by the introduced commit below [1] ] [Tested on> Canary Google Chrome:116.0.5839.0 (Official Build) canary (64-bit) (cohort: Clang-64) at Windows 10 Machine **

[1] https://crbug.com/chromium/1449007#c21 https://chromium-review.googlesource.com/c/chromium/src/+/4604326

and I poked again around this , the fix make it harder to be exploited :) , thanks again for your collab working on that case .

============
Hello amyressler@
Not sure if the panel already took a look at this report, but I would like to highlight that the impact of this bug was in allowing an attacker to fool users to Accept Critical Web Permissions for attacker website and leaking sensitive information (like Clipboard data, voice,video,etc) to  Attacker C&C server .

- As Poc for Linux and Windows shows up , the Attack Only Require 2 Clicks(double click the Cookie icon) in "Linux"  , and the poc in Windows require Only (3 Consecutive Clicks ), Making User Accept the prompt of Permission.

- The prompt not Shown at All (Fully Spoofed) like Shown in Poc Videos Attached to Issue Description.

-As per Rules Stated "https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules" , i made This Report as High Quality report as much as i Can ,hope you too consider this report as high quality report referencing bounty to  table here "https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules " and bounty amount table for (high quality report with functional exploit),with (Security UI Spoofing) impact
,(Mildly mitigated) [New UI /surface Feature] , also i have Followed the Rules of Bisection and Added and verified which active release branches (dev/beta/stable) are impacted at the time of reporting , identifying the specific commit that introduced the bug.

Hope You Consider These Points While Taking Bounty Decision By Panel.

Thank you so much for protecting us.

### fj...@chromium.org (2023-06-19)

Thank you for the detailed report and confirming the fix!

pbommana@: regarding merge review questions, see https://bugs.chromium.org/p/chromium/issues/detail?id=1449007#c23 . In the meantime, these changes have also landed in canary. Thanks!


### fj...@chromium.org (2023-06-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-20)

There does not appear to be any issues on Canary from this fix since it landed; approving merge to 115.
Please merge this fix to M115/branch 5790 at soonest so this fix can be included in the next M115 beta update -- thank you! 

### fj...@chromium.org (2023-06-20)

Thanks for the approval! The cherry-pick is running through the CQ and will land soon.

### gi...@appspot.gserviceaccount.com (2023-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f3c34f8e7b61909e683114ce13c2f1e769027cd4

commit f3c34f8e7b61909e683114ce13c2f1e769027cd4
Author: Florian Jacky <fjacky@chromium.org>
Date: Tue Jun 20 20:40:16 2023

Support input protection in new permissions UI

(cherry picked from commit 2e59e92b7601ffa3b7f55257bb2172d5e204cb43)

Bug: 1449007,1451308,1451322
Change-Id: I9266184f5d8de3d030fdc280a12222111eb4b0f5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4604326
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Florian Jacky <fjacky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1158804}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4624054
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5790@{#972}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/f3c34f8e7b61909e683114ce13c2f1e769027cd4/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/f3c34f8e7b61909e683114ce13c2f1e769027cd4/chrome/browser/ui/views/permissions/permission_prompt_bubble_base_view.cc
[modify] https://crrev.com/f3c34f8e7b61909e683114ce13c2f1e769027cd4/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/f3c34f8e7b61909e683114ce13c2f1e769027cd4/chrome/browser/ui/views/permissions/permission_prompt_bubble_base_view.h


### am...@google.com (2023-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-24)

Congratulations, Ahmed! The VRP Panel has decided to award you $3,000 for this report. The reward amount was decided on since this is not entirely a security UI spool as the permission prompt is displayed and requires to user to knowingly grant permission for access to the microphone. Thank you for your efforts and reporting this issue to us. 

### el...@gmail.com (2023-06-24)

Hello Amy, 
I think https://crbug.com/chromium/1449007#c27 is slipped  ,i'd like to highlight that the permission prompt not shown at all as poc video shows in main description with name "Bypass-1371215-Canary-WIN- 2023-05-25 21-30-28-462.mp4" , and user dont even know what happened underneath. PTAL at https://crbug.com/chromium/1449007#c27 and poc video mentioned at description.
Thanks for the reward,if this will change the reward it will be appreciated .



### el...@gmail.com (2023-06-24)

amyressler@
>as the permission prompt is displayed and requires to user to knowingly grant permission for access to the microphone

Rep:/ User didn't see any prompts,and unknowingly accept the permission he didn't see it's prompt at all.

Hope my reply considered well, maybe something missed  while assessment.
Thanks 

### am...@chromium.org (2023-06-24)

I don't think we missed anything here though perhaps I didn't articulate our assessment as I should have. This isn't a full security UI spoof, but a permission prompt overlay that results in the user being tricked to grant permission to the microphone with a fair amount of user interaction. 
In terms of "high quality security UI spoof with functional exploit" the impact expectation for this category is fully remote and non-mitigated security UI spoofing, such as full spoof / control of the omnibox for example. 

### el...@gmail.com (2023-06-24)

Thanks Amy for getting attention to this and for clarification .!
Actually this msg "as the permission prompt is displayed and requires to user to knowingly grant permission for access to the microphone" made me think something was not clear while assessment, Thanks Again and also for Reward :) , Have a great day!

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1449007?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1451308, crbug.com/chromium/1451322]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064841)*
