# Security: Lockscreen - phone options available

| Field | Value |
|-------|-------|
| **Issue ID** | [40060864](https://issues.chromium.org/issues/40060864) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | ChromeOS |
| **Reporter** | he...@googlemail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-09-07 |
| **Bounty** | $1,000.00 |

## Description

Hello together,

Today my device received

* chromeOS Version 105.0.5195.112 (Official Build) (32-bit)

In that version https://crbug.com/chromium/1303308 (open webpages via the lockscreen) is fixed - a thousand thanks again for that.

Unfortunately, the behaviour regarding entered phone numbers is still available:

Steps:
=======

0.) Be in front of the device, the user has locked his session (not: logged out). Feel like that you are the attacker.
1.) press the menu (clock) in the lower right corner
==> some quick tiles are appearing
2.) Search the "VPN" icon and press its subtext
==> you get a dark menu "Privates Netzwerk" (Private Network), showing two entries with a plus sign at their rights
3.) click the plus sign next to the first entry
==> You get the mask "Mit VPN verbinden" for setting up a VPN
4.) Type a phone number, e.g. "+49123456789" or "2125551234"
5.) Triple-click the text
==> the whole line is marked
==> the context menu is appearing, showing three dots at its end
6.) Click them
7.) Click "Call from Samsung phone"
==> A push notification is sent to the smartphone

Variant:

Instead of #5/6 just right-click the number.

Problem:
=========

A bad actor may use my Chromebook and send several phone numbers via the context menu to my smartphone. While I (= synonym for the common user) am in a meeting, the kitchen or on the toilet I can get a push notification on my smartphone telling me to call e.g. +1-212-555-55555 or expensive premium numbers/subscriptions, alternatively the boss or criminals (yes, the number would be then in the call history for other purposes ...).

That said, in my case I just get one single command for "Samsung phone". This implies that other commands are available for other brands/devices too, which may have even worse effects, such as calls being made directly and without a security query, or non-numbers being sent to connected devices (= commands doing whatever).

Perhaps calls can also be started directly via the context menu if the Chromebook itself has a SIM card installed and activated? Unfortunately, I don't know because I don't have a SIM card. But I can imagine.

Expectation:
=============

Thanks again in advance for checking and plugging the gap: The context menü does not have to offer options of the described kind while the user session is locked.

Best regards


## Timeline

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-09-07)

Was able to repro (chromeos 104.0.5112.10 platform 14909.132.0).

Copying FoundIn, Severity, Priority, Component, assignee from https://crbug.com/chromium/1303308 


[Monorail components: UI>Shell>LockScreen]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-22)

djacobo: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-07)

djacobo: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ce...@google.com (2022-11-03)

This issue is currently tagged to M106, which is no longer active.

Please add an active target milestone (M107 or later).

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### dj...@google.com (2023-01-12)

[Empty comment from Monorail migration]

### dj...@google.com (2023-01-13)

Question, I'm trying the suggested repro steps but I cannot access step 3 "3.) click the plus sign next to the first entry"
is there any other surface that is allowing you to perform this exploit?

thanks for reporting

details on my test device: Chrome 111.0.5535.0, Chromeos: 15312.0.0

### he...@googlemail.com (2023-01-13)

 Currently I don't know one; I assume that button was removed with https://crbug.com/chromium/1303306 on my very own device.

But, in my sight, that doesn't mean that somewhere else some textboxes may be left/accessible, like lockscreen notepads, or on corporate configurations (wasn't the VPN button not just removed on non-corporate configurations?!?)

Best regards.

### dj...@google.com (2023-01-19)

I fully agree with you, but I'd like to be able to reproduce this locally to discard some potential causes.

now I'm a bit puzzled because the CL we landed before (ie crrev.com/c/3759500)  was expected to gate arc apps being triggered via the touch menu (chrome/browser/ui/ash/touch_selection_menu_runner_chromeos.cc[1]) which should include apps installed for telephony apps, 
I'm guessing this is a different feature, maybe click to call?

I gave it a try and 1) locally reverted the cl you kindly linked in https://crbug.com/chromium/1361042#c11 to artificially repro your steps, 2) applied a similar session gate to click-to-call  crrev.com/c/4179372, this fixes the issue but DEPS need to be sorted out, asking feature owners to have a look.

hey mvanouwerkerk@, could you have a look at this? I was not fully sure this is something you own but my previous point of contact no longer works on Chrome stuff :S

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/ash/touch_selection_menu_runner_chromeos.cc

### mv...@chromium.org (2023-01-19)

Hi  djacobo, I see you have a CL out to address this already. If you have layering violations, perhaps a delegate interface can be injected and implemented in a place where you can depend on the necessary code. Note I have not worked on this for years at this point. I think perhaps ellyjones@ is effectively an owner now.

[Monorail components: UI>Browser>Sharing]

### el...@chromium.org (2023-01-19)

Oh yikes. I don't know anything about the ash stuff or the cros lock screen, but maybe I can try to help?

### dj...@google.com (2023-01-20)

Thanks folks, I'm gonna pass ownership of this bug to ellyjones@ then,

I agree w/ https://crbug.com/chromium/1361042#c13, however I'm failing to see a good place to set said auxiliary code without having better knowledge on click-to-call,

update: ok I updated my proposed solution by basically getting rid of the SessionState check (that's the portion that introduced the dependency conflict)
on the basis that [1] i'm not really sure its needed here, for instance nearby share uses IsScreenLocked() [2] as well in a similar capacity without having to
check for SessionState, probably something worth exploring with lockscreen peps? 

Anyways the updated CL shouldn't be controversial as it does the bare minimum protection against access to click to call within the Lock screen, 
I'd rather land this and later explore how to complement with SessionState and/or refactoring this code, but I defer to owners.

[1] crsrc.org/c/components/session_manager/session_manager_types.h;drc=00e7ff081d84b492e90a6557eef862ade4a49bdc;l=32
[2] crsrc.org/c/chrome/browser/nearby_sharing/nearby_sharing_service_impl.cc;l=333?q=IsScreenLocked%20nearby%20share&ss=chromium
 

### el...@chromium.org (2023-01-25)

#15: Does that mean you want ownership of the bug back?

### dg...@google.com (2023-01-27)

This issue is currently tagged to M-107 and/or M-108, which is no longer active.

Please add an active target milestone (M-109 or later) or close the bug if it is no longer an issue.

### el...@chromium.org (2023-02-01)

Sharing triage: back to djacobo@ :)

### el...@chromium.org (2023-03-01)

Sharing triage: -> Pri-2

### dj...@google.com (2023-03-01)

hey peeps,

I meant to say that I'm not really the best owner as I'm unfamiliar with the feature and I don't have bandwidth to learn this rn, 
I abandoned the proposed CL long ago as it was incomplete :/ 

sorry for the misunderstanding.
ps: adding myself as cc: in case I can help with reviews

### [Deleted User] (2023-03-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-03-13)

[Empty comment from Monorail migration]

### el...@chromium.org (2023-03-20)

Fixed (by disabling click-to-call)

### [Deleted User] (2023-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-29)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1361042?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Sharing, UI>Shell>LockScreen]
[Monorail components added to Component Tags custom field.]

### he...@googlemail.com (2024-02-24)

Hi together,

Out of interest: Has an CVE been issued? Unfortunately, I cannot find any publication about this issue.

Thanks a lot for a short reply.

Best regards

### am...@chromium.org (2024-02-27)

I don't believe ChromeOS is monitoring issues in this tracker and ChromeOS is a separate CNA, so we cannot issue CVEs for issues within their scope. You'll need to reach out to [chromeos-security@chromium.org](mailto:chromeos-security@chromium.org) to ask about a CVE for this issue.

### he...@googlemail.com (2024-02-27)

I just have access to this Issuetracker

Saying that it was obviously categorised wrongly ([comment #36](https://issues.chromium.org/issues/40060864#comment36)) after migrating from Monorail to Issuetracker, wasn't it?

### am...@chromium.org (2024-02-27)

It was not wrongly categorized. This issue was only reported in the legacy tracker and was resolved before ChromeOS migrated to the Google issue tracker, so it was migrated to this one. ChromeOS is still working through pulling over their groups of issues migrated from the legacy tracker into this tracker into their components in the Google issue tracker.
So it's unlikely they are actively monitoring these issues while that additional migration work takes place.
You will need to reach out to them directly via [chromeos-security@chromium.org](mailto:chromeos-security@chromium.org) in order to ask / request if CVE will be assigned for this issue.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060864)*
