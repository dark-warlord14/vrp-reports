# Security: adb wireless debugging bugfix bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40064420](https://issues.chromium.org/issues/40064420) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | sm...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-05-08 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

We found the M110 fix for [https://crbug.com/chromium/1401666: Security: sideload APKs on ChromeOS without enabling developer mode nor ADB](https://bugs.chromium.org/p/chromium/issues/detail?id=1401666) was insufficient for preventing the use of wireless debugging to obtain remote adb access to arcvm.

`uname` for  

ChromeOS: `Linux localhost 4.14.306-20290-g9799d3cf8bba #1 SMP PREEMPT x86_64 (CPU vendor here) GNU/Linux`  

android via termux `Linux localhost 5.10.162-987869-g93fc1d636189 #1 SMP PREEMPT x86_64 Android`

**VERSION**

Chrome + ChromeOS: 112.0.5615.134 (Official Build) (64-bit) (Stable)  

Arc: 9891653 SDK Version: 30

CONTEXT

The original context statement about heavily restricted managed environments still applies here.

Similarly, by policy, we have developer mode disabled, chrome extensions, and apps on a whitelist system. Google play store is enabled, but a whitelist of installable apps is enforced. In addition, network-level content restrictions are applied. However, since they do not work in home networks, there is a Chrome extension for filtering.

A user can take advantage of this to:

1. Install a sufficiently capable VPN like 1.1.1.1 (Cloudflare Warp) or Mullvad to bypass network restrictions
2. Install another browser in the Android subsystem, like Firefox, Brave, or Opera, to bypass browser restrictions.

**REPRODUCTION CASE**

To obtain adb access to archive, use the following steps similar to the original exploit. Pictures are attached for reference.

1. Enable developer options in "Manage Android Preferences" since this launches settings. (In Android, NOT Chrome OS)
2. Return to the first activity of settings and scroll to the top.
3. Use the search tool for the term "pair."
4. Tap any devices with "Wireless Debugging" under them. This bypasses the developer options activity and goes directly to the activity dedicated to Wireless Debugging.
5. Don't pair anything. Instead, use the highlighted toggle at the top to turn on wireless debugging.
6. Enjoy unrestricted adb access.

Here's an additional interesting bit I uncovered later: If you install the open source AppManager or termux with the adb package, you can adb your own device through localhost and install apps to the same device without the need for a separate computer afterwards. For some reason, android thinks it is being debugged via USB (it seems like multiple connections can cause this).

As I understand it, this happens because what the patch disabled was the toggle on the main activity for developer options. The developer options toggle is not the only way to get to the activity dedicated to just wireless debugging. As shown, we were able to abuse the search feature to visit that activity directly.

Referenced:  

[AppManager](https://github.com/MuntashirAkon/AppManager) app.  

[Android Activities](https://developer.android.com/guide/components/activities/intro-activities)

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

this bug is included; how would you like to be credited?  

Reporter credit: Les Amateurs Team

## Attachments

- [step1_outside_of_developer_options.png](attachments/step1_outside_of_developer_options.png) (image/png, 24.4 KB)
- [step1_verify_developer_options.png](attachments/step1_verify_developer_options.png) (image/png, 48.2 KB)
- [step2_scroll_up_in_first_activity.png](attachments/step2_scroll_up_in_first_activity.png) (image/png, 45.0 KB)
- [step3_search_pair.png](attachments/step3_search_pair.png) (image/png, 30.4 KB)
- [step4_arrive_directly_at_wireless_debug_activity.png](attachments/step4_arrive_directly_at_wireless_debug_activity.png) (image/png, 15.3 KB)
- [step5_verify_adb_shell.png](attachments/step5_verify_adb_shell.png) (image/png, 27.8 KB)
- [step5_wireless_debug_activity_postenable.png](attachments/step5_wireless_debug_activity_postenable.png) (image/png, 32.0 KB)
- [step5_wireless_debug_confirm_network.png](attachments/step5_wireless_debug_confirm_network.png) (image/png, 39.0 KB)
- [extra_appmanager_detected_adb_mode.png](attachments/extra_appmanager_detected_adb_mode.png) (image/png, 57.1 KB)
- [extra_appmanager_first_activity.png](attachments/extra_appmanager_first_activity.png) (image/png, 136.6 KB)
- [extra_appmanager_supplement_confirm_debugging.png](attachments/extra_appmanager_supplement_confirm_debugging.png) (image/png, 25.4 KB)
- [extra_termux_next_to_settings.png](attachments/extra_termux_next_to_settings.png) (image/png, 237.5 KB)
- [extra_termux_next_to_settings_with_cmd.png](attachments/extra_termux_next_to_settings_with_cmd.png) (image/png, 246.7 KB)

## Timeline

### sm...@gmail.com (2023-05-08)

Remaining two attachments: these show termux side by side with the developer section of settings (this is a minor ui glitch allowing me to see this part)

### [Deleted User] (2023-05-08)

[Empty comment from Monorail migration]

### nh...@google.com (2023-05-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-08)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/281468454). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/281468454]

### [Deleted User] (2023-05-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### st...@google.com (2023-06-05)

[Empty comment from Monorail migration]

### st...@google.com (2023-06-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-07)

chmiel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@gmail.com (2023-06-13)

Some additional information I forgot to initially provide, if you look in all of the images that have an android modal/dialog displayed, you'll notice that there's a checkbox for either "Always allow on this network" (shows up first), and then "Always allow from this computer" when a computer tries to connect (the one with the RSA fingerprint). It looks like in some cases, with setup beforehand using these checkboxes it is possible to not need to open settings for wireless debugging to be enabled, so it looks like fixing this ui side may not entirely block this method if the user sets things up before they receive the update. From my testing, if arcvm is force restarted (simulating this through a reboot request reboot), one of the first things it does on startup is ask if you want to enable wireless debugging on the network through the exact same prompt seen before if the checkbox was not checked. 

### sm...@gmail.com (2023-06-13)

I also have thought of another bypass but I think your new patch may cover it, will update when I produce a poc as I'm waiting for hardware to test on. 

### sm...@gmail.com (2023-06-14)

Here is my potential bypass: According to these sources, if a user is on a vulnerable version of chromeos, it appears they can setup a "backdoor" for themselves by creating their own app to enable wireless debugging because apparently android has a permission to modify the adb settings which are called "secure settings". 
https://web.archive.org/web/20230614013905/https://old.reddit.com/r/androiddev/comments/j6p8q4/wireless_debugging_in_android_11_off/gte71jd/
https://web.archive.org/web/20230613110323/https://tasker.joaoapps.com/userguide/en/help/ah_secure_setting_grant.html
As I've said before, unfortunately I don't have access to a ChromeOS device with arcvm any more installed (flex is usable in a vm but lacks arcvm), so my ability to test these is limited for now. 

A probably better mitigation would be perhaps to block port 5555 at a firewall level until adb is enabled via the developer mode toggle.


### sm...@gmail.com (2023-06-15)

By the way, may this issue be potentially considered for bug bounty by the VRP panel? 
Thanks!

### jo...@chromium.org (2023-06-15)

[Empty comment from Monorail migration]

### vr...@chromium.org (2023-06-15)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-16)

Marked as fixed.

19:45
+Hotlist:​Merge-Merged
19:45
-Hotlist:​Merge-Approved-115
19:45
-Hotlist:​Merge-Approved-114
19:46
+Hotlist:​LTS-Merge-Merged-108
19:46
-Hotlist:​LTS-Merge-Approved-108
19:47
Status:​In Progress (Accepted)      Fixed



The posted solution patches will

NOT allow users to gain new : ADB over Wi-Fi capability
NOT allow users to continue to have: ADB over Wi-Fi capability for users that had it before.
From now on, to enable or continue to use ADB over Wi-Fi, the user will first have to give either of the 2 explicit permissions:

Enable ADB Sideloading, or
Put the whole device in Developer mode.
I don't think the possible loophole scenarios will work now.

### [Deleted User] (2023-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-16)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-17)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-18)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-19)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vr...@chromium.org (2023-06-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-20)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vr...@chromium.org (2023-06-20)

The required patches have successfully landed in branches - 108(LTS), 114 (also LTS), 115, and trunk.

**Build numbers** 

1. rvc-115 : R115/15474.6.0
2. rvc-114 : R114/15437.38.0
3. rvc-108 :  R108/15183.98.0
4. tm-115 : R115/15474.11.0
5. tm-114 :  R114/15474.39.0

### am...@google.com (2023-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-24)

Congratulations! The VRP Panel has decided to award you $3,000 for this exploit mitigation bypass of sideloading android apps without restrictions. A member of our finance team will reach out to you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-12-20)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1443292?no_tracker_redirect=1

[Monorail blocking: b/281468454]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064420)*
