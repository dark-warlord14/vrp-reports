# CCT Clipboard Content Sniffing -  Task Hijacking

| Field | Value |
|-------|-------|
| **Issue ID** | [40068069](https://issues.chromium.org/issues/40068069) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile>CustomTabs |
| **Platforms** | Android |
| **Reporter** | le...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2023-07-25 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

1. Watch attached video
2. See attached source code / install Apk demo to your device and follow the reproduction steps in the video.

PoC Video, Source Code and Apk are attached here <https://drive.google.com/drive/folders/1WcZECOpRIoX34KZ5nK8FCJGxd40IXNjb?usp=sharing>

**Problem Description:**  

A malicious app is capable of hijacking Chrome Custom Tabs task and sniff everything copied by the user in real time while browsing. This exposes user private data such as emails, usernames, passwords, credit card information etc.

**Additional Comments:**

\*\*Chrome version: \*\* 114.0.5735.196 \*\*Channel: \*\* Stable

**OS:** Android

## Attachments

- [InvisibleActivity.java](attachments/InvisibleActivity.java) (text/plain, 1.8 KB)
- [MainActivity.java](attachments/MainActivity.java) (text/plain, 1.3 KB)
- [AndroidManifest.xml](attachments/AndroidManifest.xml) (text/plain, 1.2 KB)
- [activity_main.xml](attachments/activity_main.xml) (text/plain, 778 B)
- [invisible_activity.xml](attachments/invisible_activity.xml) (text/plain, 529 B)
- [themes.xml](attachments/themes.xml) (text/plain, 1.4 KB)
- [CCT Clipboard Sniffing PoC Video Compress.mp4](attachments/CCT Clipboard Sniffing PoC Video Compress.mp4) (video/mp4, 7.3 MB)

## Timeline

### [Deleted User] (2023-07-25)

[Empty comment from Monorail migration]

### ma...@google.com (2023-07-26)

Thank you for your submission. Could you please attach source codes and videos directly to this bug? Also please upload them uncompressed, not as zip files. See https://www.chromium.org/Home/chromium-security/reporting-security-bugs/ for more information

### le...@gmail.com (2023-07-27)

Hi

please see attached PoC video and code implementation. The code is simple but I've included the xml and theme as they play a major role in reproducing the vulnerability.

### ma...@google.com (2023-07-27)

Thank you for the report.

Looking at the sample, the app simply reads the contents that the user chooses to copy to the clipboard. From what I understand that's how the clipboard APIs are supposed to work in Android. There's nothing special about CCT here, an unrelated app could do this with contents copied from Chrome or any other Android app. I don't think there is a bug here.

### le...@gmail.com (2023-07-27)

An app should only read clipboard content when it is in focus. CCT is capable of preventing the malicious app launching it from overlaying by launching the browser activity in a new task as opposed to the same task.

Normally the app should only read clipboard when the user closes CCT and the app regains focus. In my demo, I've shown how the clipboard content is monitored in real time, making it possible to steal copied sensitive information.

### ma...@google.com (2023-07-27)

peconn@, could you PTAL and let me know whether we consider this an issue? Thank you

### ma...@google.com (2023-07-27)

(Speculatively setting security labels.)

[Monorail components: UI>Browser>Mobile>CustomTabs]

### ma...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2023-07-31)

Reporter, do you mind sharing your Android version?

### le...@gmail.com (2023-07-31)

Hi, tested in Android OS versions 11 and 13, both Pixel 4a and non Pixel devices.

### pe...@chromium.org (2023-07-31)

+Kevin FYI

### pe...@chromium.org (2023-08-01)

martinkr - yeah, this goes against Android's security expectations (that only the focused app can read from the Clipboard from Android 10).

Kevin, Theresa, I could do with your thoughts on this. The attack is:

1. Developer launches a Custom Tab.
2. Developer launches an invisible Activity on top of that Custom Tab.
3. That invisible Activity has focus and therefore can read from the clipboard.

We can detect whether there is an activity on top, and we do disable clicks on permissions dialogs in this case, but given that there are legitimate use cases for having an Activity on top (chat bubbles), it seems a bit extreme to disable the clipboard when that happens.

### le...@gmail.com (2023-08-01)

Probably warn users about the risk of leaking their clipboard data when they are about to copy anything and there is an activity on top  of the CCT.

Another approach would be that CCT should securely store all clipboard data separately and clear the clipboard by replacing with empty string. When the user requires to paste anything from the clipboard, CCT could then avail the previously copied data to the fields.

### tw...@chromium.org (2023-08-01)

+Victor as an fyi and Jinsuk (who's look at a similar issue with taps for Activity overlays)

> We can detect whether there is an activity on top, and we do disable clicks on permissions dialogs in this case, ...

We're also looking at disabling taps on Chrome in general this scenario (specifically CCT is not the foreground Activity) on older OS versions to match newer OS behavior.

This might be sufficient to mitigate this issue as well -- if Chrome can't receive taps when its not the foreground Activity, then its content can't be copied to the Clipboard.

Could confirm by testing this on Android 13+, where taps should be prevented from going through the semi-transparent attacker activity automatically due to some Android OS changes aimed at preventing these types of attacks across the broader ecosystem.

> given that there are legitimate use cases for having an Activity on top (chat bubbles), it seems a bit extreme to disable the clipboard when that happens.

Jinsuk, can we find some examples of chat bubbles and confirm whether the CCT is still considered "resumed"? (I'd hope so) 

We're looking at using Activity state to know when the Custom Tab isn't the top activity in the Task. 

> Another approach would be that CCT should securely store all clipboard data separately and clear the clipboard by replacing with empty string. When the user requires to paste anything from the clipboard, CCT could then avail the previously copied data to the fields.

I'm not following how the end portion here would work.... the paste is likely to happen outside of Chrome. I'm not sure how Chrome could know "When the user requires to paste anything".

### le...@gmail.com (2023-08-01)

>>I'm not following how the end portion here would work.... the paste is likely to happen outside of Chrome. I'm not sure how Chrome could know "When the user requires to paste anything".

CCT could securely store copied data separately and clear the clipboard by replacing with empty string when another activity comes on top of it, when CCT regains focus / no activity is on top of CCT, it could restore the clipboard data by simply copying it back from the secure storage. 

Generally, whenever an activity is on top of CCT, there could be a permission prompt on whether to allow the external window to access clipboard content or not. It's a simple hide / unhide solution.

### tw...@chromium.org (2023-08-01)

Re #19 -- I'd expect most of the time users want to copy to other apps (outside of Chrome). This seems like it'd have somewhat similar user impact to disabling copying to clipboard when Chrome isn't the foreground Activity with more complex code.

### le...@gmail.com (2023-08-01)

[Comment Deleted]

### ji...@chromium.org (2023-08-01)

> Jinsuk, can we find some examples of chat bubbles and confirm whether the CCT is still considered "resumed"? (I'd hope so) 

Yes my test shows that chat bubbles/apps running in overlay mode doesn't affect CCT activity state. It remains "resumed". Used gchat/messaging app and a third-party screen recorder to verify that.

### tw...@chromium.org (2023-08-01)

Thanks for confirming, Jinsuk!

I believe in-flight CL should protect against new Chrome/webpage content being copied to the clipboard while a transparent Activity is showing on top.

Which leaves content copied to the clipboard before the transparent Activity is launched per levitnudi@'s earlier comments. When the malicous Activity reads from the clipboard, Android 12+ should display a toast to the user (https://developer.android.com/about/versions/12/behavior-changes-all#clipboard-access-notifications)

martinkr@ -- does that reduced attack surface lower the severity of this security bug?

### ma...@google.com (2023-08-01)

I'm not sure it does, the notification happens after the clipboard content disclosure, so isn't that too late to mitigate anything here? Also the app hypothetically may have accessed clipboard content from another app for different reasons at a different point in time, so the notification doesn't even necessarily show, right?


### tw...@chromium.org (2023-08-01)

I'm more thinking that the user not being able to continue interacting with Chrome and copying potentially sensitive data after the transparent Activity is launched minimizes the attack surface -- it becomes point in time where the malicious app can read whatever's currently in the clipboard -- which they can also do before launching the CCT, so the attack surface is even more minimally read one thing copied while viewing the CCT. Versus the original report that the malicious app could launch a transparent Activity and do ongoing monitoring of the clipboard contents as the user interacts with Chrome.

I suppose they could keep launching a transparent Activity to periodically pull from the clipboard.

I would personally rather lean into "Background Activity Launch" restrictions, which Android is trying to harden at an OS level, than add complex clipboard management logic into Chrome.

> also the app hypothetically may have accessed clipboard content from another app for different reasons at a different point in time,

The documentation says "when an app calls getPrimaryClip() to access clip data from a different app for the first time, a toast message notifies the user of this clipboard access." I'm not sure if that's the first time ever - if so, then you're correct - or the first time per app launch or something else.

### le...@gmail.com (2023-08-02)

#25 relying on system toast messaging may not be reliable for such a serious security notification. For example, a malicious app could toast several empty messages in a loop (or something that would mislead e.g labeled "downloading..."), by that, every other toast notification from the system will become almost invisible (overridden), I could demo this if you need proof.

### [Deleted User] (2023-08-15)

peconn: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### pe...@chromium.org (2023-08-18)

To summarize the current state:

1. Code has landed in Chrome that prevents CCT touches from being processed when there's an invisible Activity on top of it.
  a) It may still be possible for an app to continuously launch and kill the overlay activities.
2. Launching in the same task as the client app is a fundamental part of how CCTs work - changing this would break a lot of existing applications.
3. Android is adding restrictions to launching Activities in this way to fix this problem generally.
4. On Android 12+ there is some user visible effect to accessing clipboard data from another app.
5. This attack does involve getting the user to carry out certain steps - eg, copying their email/personal data.

I can't see a good solution to this problem that wouldn't break CCT functionality, so I'm tempted to just wait until Android fixes the lower level issue.

Martin, Theresa what do you think?

### tw...@chromium.org (2023-08-21)

>  I'm tempted to just wait until Android fixes the lower level issue.

That was my recommendation in #25 as well

### [Deleted User] (2023-09-01)

peconn: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-11)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-21)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-04)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-08)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1467615?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-21)

Thank you for providing more feedback. Adding the requester to the CC list.

### pg...@google.com (2024-05-24)

Hi [peconn@chromium.org](mailto:peconn@chromium.org)! Do you have the tracking bug for Android's work on adding restrictions to launching Activities that would provide a more general fix for this issue (if so can you attach it as a blocker or comment it here)? I've searched for it but couldnt find it, but it would be good to be able to follow the progress on it, as it is the current plan for this bug's solution!

### pe...@chromium.org (2024-06-04)

I'm not sure if there's an Android bug, although https://buganizer.corp.google.com/issues/299126931 has some relevant discussion.

### pe...@google.com (2024-10-26)

peconn: Uh oh! This issue still open and hasn't been updated in the last 143 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

peconn: Uh oh! This issue still open and hasn't been updated in the last 158 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dc...@chromium.org (2026-01-30)

Android V included background activity launch hardening, and Chrome (as of M127) sets V as the target SDK, so I think this is fixed.

### ch...@google.com (2026-01-30)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### le...@gmail.com (2026-01-30)

deleted

### sp...@google.com (2026-02-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Mitigated baseline / low impact user information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### le...@gmail.com (2026-02-20)

Thank you! I appreciate it **Chrome VRP**!

### ch...@google.com (2026-05-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068069)*
