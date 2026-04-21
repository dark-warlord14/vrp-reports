# Security: Locked devices - VPN adding possible

| Field | Value |
|-------|-------|
| **Issue ID** | [40058985](https://issues.chromium.org/issues/40058985) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>VPN |
| **Platforms** | ChromeOS |
| **Reporter** | he...@googlemail.com |
| **Assignee** | ta...@google.com |
| **Created** | 2022-03-05 |
| **Bounty** | $5,000.00 |

## Description

Hello,

Please kindly note that it is obviously possible to add VPNs to a locked user session.

* Chromebook, OS v99.0.4844.57

How?

0.) Be in front of the device, the user has locked his session (not: logged out)
1.) press the menu (clock) in the lower right corner
==> some quick tiles are appearing
2.) Search the "VPN" icon and press its subtext
==> you get a dark menu "Privates Netzwerk" (Private Network), showing two entries with a plus sign at their rights
3.) click the plus sign next to the first entry
==> You get the mask "Mit VPN verbinden" for setting up a VPN
4.) Do add a VPN.
==> Note: As I don't have such data, I sadly cannot do this; but I assume the device will accept a new connection, as it is prompting for the data.

Enclosed a video for demonstration.

Problem/Expectation:
=====================

Should it really be possible to add a VPN to the device while the user's session is locked, this would be a high risk as a local proximate attacker could add a VPN which is controlled by him/her, with all risks for the user: Data manipulation, redirecting traffic etc.

Adding VPNs do not have to be allowed while the user session is locked.

++++++

ATTENTION:

The video is showing two more vulnerabilties in this context; so please add the "embargo" flag until they are fixed too.

++++++

Thank you for checking and fixing on occasion for my an millions of others security.

Best regards 

## Attachments

- [20220305_175206.mp4](attachments/20220305_175206.mp4) (video/mp4, 10.9 MB)

## Timeline

### [Deleted User] (2022-03-05)

[Empty comment from Monorail migration]

### he...@googlemail.com (2022-03-05)

All issues shown in the video, needed to be embargoed:

https://crbug.com/chromium/1303308
https://crbug.com/chromium/1303312
https://crbug.com/chromium/1300710

### dc...@chromium.org (2022-03-05)

Given that it is does not seem possible to configure/change wifi networks at the lock screen, I agree that it should also not be possible to configure VPN networks at the lock screen either.

[Monorail components: UI>Shell>LockScreen]

### [Deleted User] (2022-03-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-06)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2022-03-07)

Pass to lockscreen TL

### an...@chromium.org (2022-03-09)

Per b/144202836 and crbug.com/1167070, it should be possible to set up VPN connection from login screen (and, transitively, lock screen), this is a requested feature from the enterprise customers.
However, that feature should only be available for the managed devices, and exposing it on non-managed devices is actually  a bug.
Assigning to the owners of the feature.

### [Deleted User] (2022-03-20)

kura: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-04)

kura: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@google.com (2022-04-27)

kura@ could you please update this ticket? It is popping up during OAC team's triage, but nobody on that team has access to the issue and therefore they cannot do anything about it. 

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ul...@chromium.org (2022-07-12)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-07-12)

Re-assigning this issue to author of crrev.com/c/2383366 - CL that introduced the VPN feature.

cc pmarko on enterprise networking side.

See https://crbug.com/chromium/1303306#c7 - main issue here is that VPN can be configured on the login/lock screen by consumer users on consumer devices, which (per go/cros-vpn-login) should not happen.


### an...@chromium.org (2022-07-12)

[Empty comment from Monorail migration]

### ta...@google.com (2022-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2022-07-13)

+aghuie@.

Alex, I remember we had a discussion that for the ease of admin debug purpose it could be useful to enable adding VPN through UI before login. Giving the context of this bug I feel that we might be a little bit careless. I think even for managed devices #1 still sounds a valid security concern.

Do you still think it is a good trade-off to continuing allowing configuring VPN manually before login for managed device, or should we just remove it on all devices?

### ta...@google.com (2022-07-13)

I'm double checking the code and notice that we DID decided that manually adding VPN should be disabled on login screen. (https://source.chromium.org/chromium/chromium/src/+/main:ash/system/network/vpn_list_view.cc;drc=bdfd14582d13303693de1248bdabbfae2c251d59;l=160)

So it's simply a bug that we only disable it on login but missed the locked state. I'll upload a patch.

Just to double confirm - I suppose we should disable it on kiosk mode as well, right?

### an...@chromium.org (2022-07-13)

Can we also add a test for login/lock screen that would cover this situation as a part of the fix?

### ta...@google.com (2022-07-14)

[Empty comment from Monorail migration]

### ta...@google.com (2022-07-14)

[Empty comment from Monorail migration]

### ta...@google.com (2022-07-14)

Adding khorimoto@ for information.

> #19
Yes I do plan to add a test covering this.

### ta...@google.com (2022-07-20)

Per discussion in crrev/c/3760105, it is difficult to add automatic test covering this in current architecture.

Adding harpreet@ -

Harpreet, we might need to add a manual test case to cover this:
- Before user login, it is not possible to add a VPN through "Add VPN" UI in right bottom panel.
- After a user logged in and locked the device, it is not possble to add a VPN through  "Add VPN" UI in right bottom panel.

What do you think?

### ha...@chromium.org (2022-07-21)

taoyl@ -

Generally we should have an automated test for P0/P1 scenarios which it seems like the case with this given the bug priority. So we should definitely have a plan with an ETA on when this can be added. From the comment in the CL, I see that it is blocked on a refactor. 

khorimoto@
As the refactor is planned for M105 (crbug.com/1311762), is it still not possible to automate these tests? Can you please help clarify what is pending?
 

----

For now, we'll go ahead and add manual tests since we are trying to patch a bug in a released product with the assumption that the fix can not wait for automation.

### ha...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-07-26)

[Empty comment from Monorail migration]

[Monorail components: -UI>Shell>LockScreen Internals>Network>VPN]

### kh...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### he...@googlemail.com (2022-08-07)

Hello,

just a small side note, because the following issue has no owner: I reported a related behaviour (there: guest mode persistence) over a year ago under https://crbug.com/chromium/1228064, which was merged into a ticket from 04/2015. Unfortunately, the gap there ought to be exploitable for over seven years now (today: v104.0.5112.83)... dupe or not. ;(

That said, just a friendly hint.

Best regards

### gi...@appspot.gserviceaccount.com (2022-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/275e88b8ce0ed04b029c74af9886ca5a4f1ea9d8

commit 275e88b8ce0ed04b029c74af9886ca5a4f1ea9d8
Author: Taoyu Li <taoyl@google.com>
Date: Mon Aug 08 02:13:58 2022

Disable VPN add button on lock and kiosk mode

Bug: 1303306
Change-Id: Ib4eae778c7aa73da3b5cf3c2d09b17e23e069b29
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3760105
Commit-Queue: Taoyu Li <taoyl@chromium.org>
Reviewed-by: Pavol Marko <pmarko@chromium.org>
Reviewed-by: Kyle Horimoto <khorimoto@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1032400}

[modify] https://crrev.com/275e88b8ce0ed04b029c74af9886ca5a4f1ea9d8/ash/system/network/vpn_list_view.cc


### ta...@google.com (2022-08-08)

The fix is current in.
dcheng@ and antrim@ - I suppose the auto-added M104 tag was wrong: it might be too late to pick this into M104. That being said, do you think we should pick this into M105?


### ad...@google.com (2022-09-21)

taoyl@ based on https://crbug.com/chromium/1303306#c32 I am marking this Fixed. Please mark things as Fixed as soon as you deem them fixed - that would have initiated the merge processes you mention in https://crbug.com/chromium/1303306#c32, but Sheriffbot didn't know that you considered this fixed.

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-07)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1303306?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058985)*
