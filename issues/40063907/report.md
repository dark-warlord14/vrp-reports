# Permission Tapjacking Is Possible In Android Custom Tabs

| Field | Value |
|-------|-------|
| **Issue ID** | [40063907](https://issues.chromium.org/issues/40063907) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile>CustomTabs, UI>Browser>Permissions>Prompts |
| **Platforms** | Android |
| **Reporter** | le...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2023-04-05 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. Install attached demo apk file in your device (Tapjacker.apk)
2. You might want to upload the index.html file to your own url and make changes to the source code to open your own url in custom tabs (This is optional)
3. Follow the instruction on the screen (Watch the attached video for more information)

**Problem Description:**  

Even though there is an existing mitigation for tapjacking in android chrome / custom tabs using View.setFilterTouchesWhenObscured(true), this only applies to a very small area of the window where the permission request dialog is displayed. This attack proves that a fully obscured window still poses a risk for such attacks in Chrome. The attacker is capable requesting any permissions and luring unsuspecting users to tap on specific locations on the screen, thus giving them access.

**Additional Comments:**  

Please watch the quick PoC Video found here: <https://drive.google.com/file/d/1L8_TQbLBqwjb85F33d86R82zNtLdZEI3/view?usp=share_link>

Do let me know if you have any questions.

Thanks!

\*\*Chrome version: \*\* 111.0.5563.116 \*\*Channel: \*\* Stable

**OS:** Android

## Attachments

- [Tapjacker Source Code.zip](attachments/Tapjacker Source Code.zip) (application/octet-stream, 108.9 KB)
- [TapJacking Apk Demo.apk](attachments/TapJacking Apk Demo.apk) (application/octet-stream, 5.9 MB)
- [index.html](attachments/index.html) (text/plain, 4.3 KB)

## Timeline

### le...@gmail.com (2023-04-05)

In case you may need to upload the camera requesting index.html file on your own website, please find it attached here.

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-04-05)

Hello, thanks for the report, PoC and video. In the video, the permissions dialog is hidden from the user by making the website opaque and essentially asking the user to tap into "space". I think its a harder sell to make the user do that than actually on a target they can see - however, the permission dialog button target is protected by View.setFilterTouchesWhenObscured(true) as you point out. So I am not convinced this is an effective attack vector.

CCing some folks to get their take.

[Monorail components: UI>Browser>Permissions>Prompts]

### le...@gmail.com (2023-04-05)

This PoC only uses permission request to show the possibility of this kind of attack. The concept may not be convincing enough for a technical person because of it's simplicity :). This is just a demo, and if it was an elaborate game requiring players to tap various positions on the screen, you wouldn't easily suspect an ongoing attack.

Either way, tap jacking shouldn't be encouraged in custom tabs. There are several components that aren't secured by View.setFilterTouchesWhenObscured(true) that are at risk e.g tricking a user to subscribe to a YouTube channel, thus leaking the web visitor information or tricking users to unknowingly perform sensitive actions on a website like signing in using One Tap auth or Autofill sensitive info like credit card details unknowingly.

A suggested fix is disabling the WebView when a floating window with opacity >= .8f is detected to prevent unintended touches.

### ed...@chromium.org (2023-04-05)

FYI engedy@

### me...@chromium.org (2023-04-05)

I believe this report is using a partial custom tab. Clickjacking concerns were discussed before launch (go/custom-tabs-clickjacking) and "untrusted touches" (go/untrusted-touches) was pointed at as a mitigation. Custom tabs team, can you please take a look? Not sure why these mitigations don't work here.

[Monorail components: UI>Browser>Mobile>CustomTabs]

### me...@chromium.org (2023-04-05)

Actually, it just looks like a normal CCT, but covered with an overlay. The code to create the CCT is:

        String url = "https://evolvedthinkers.blogspot.com/2022/08/bounty.html";
        CustomTabsIntent.Builder builder = new CustomTabsIntent.Builder();
        CustomTabsIntent customTabsIntent = builder.build();
        customTabsIntent.launchUrl(this, Uri.parse(url));

### an...@chromium.org (2023-04-05)

==> This is just a demo, and if it was an elaborate game requiring players to tap various positions on the screen, you wouldn't easily suspect an ongoing attack.

Thanks for pointing out this scenario. Agreed, that it would be more likely for someone to tap in various positions then. I'll wait for some of the people CC'd to chime in with their thoughts.

### tw...@chromium.org (2023-04-05)

anunoy@ -- what Android OS version are you on?

I think on Android 13+, taps should be prevented from going through the semi-transparent attacker activity automatically due to some Android OS changes aimed at preventing these types of attacks across the broader ecosystem.

https://android.googlesource.com/platform/frameworks/base/+/1bc541e8950824f223dc2aba43f09c20f96189a9%5E%21/services/core/java/com/android/server/wm/ActivityRecord.java

### an...@chromium.org (2023-04-06)

I'll pass the question on to the bug reporter: Could you tell us what version of Android are you running?

### le...@gmail.com (2023-04-06)

I reproduced this in Android 11 & 12 but unable to reproduce it in android T.

### tw...@chromium.org (2023-04-06)

[Comment Deleted]

### tw...@chromium.org (2023-04-06)

Thanks for confirming!

Given Android's continued investment in this space, I think we should be leaning into ensuring the OS protections around various types of phishing/tap-jacking attacks work for Custom Tabs.

Chrome security -- could we please get your input on severity level and whether the team needs to investigate whether a Chrome-specific mitigation is possible in Android 12 and below?

### me...@chromium.org (2023-04-06)

This requires a malicious app to be installed for the exploit to work, so it feels like medium severity. twellington, also assigning to you, but please feel free to reassign.

> whether the team needs to investigate whether a Chrome-specific mitigation is possible in Android 12 and below?

Yes, please, that would be great. Generally, the mitigation for these types of attacks is to add a delay to the button so that it can't be clicked for the first N milliseconds. That won't work here though, as the CCT is always visible but dimmed. For example, if detecting dim status is possible without underlying changes from Android, perhaps we could consider disabling CCT input when CCT is dimmed, as suggested by OP?

If a Chrome only mitigation is not possible, we might want to mark this bug as external dependency.

### [Deleted User] (2023-04-06)

[Empty comment from Monorail migration]

### tw...@chromium.org (2023-04-06)

-> Kevin as Connective Tissue TLM for triage/tracking since iiuc this attack is relying on an "activity sandwich", which can be applied to CCT since it is shown in the same Task as other apps, but not ChromeTabbedActivity which is always in its own Task.

Given this isn't a regression, we do protect permission dialogs (would be good to confirm those are still protected in this scenario), and there are OS level solutions for newer versions of Android, I'm inclined to prioritize this lower (i.e. not shuffle around the team's planned roadmap to make a big investment). I also suspect a malicious app that's trying to phish / tap jack web content is more likely to use WebView than CCT (especially as more safeguards get built into CCT) but that's just a suspicion.

> For example, if detecting dim status is possible without underlying changes from Android, perhaps we could consider disabling CCT input when CCT is dimmed, as suggested by OP?

We might be able to detect if a ChromeActivity is the top Activity in the Task and disable clicks on the CCT when its not the top activity to mimic the Android 13+ behavior. 

If that's not possible or catches non-malicious use cases, my recollection from our past foray into similar issues with tap jacking on permission dialogs in Clank is that it was hard to differentiate malicious behavior from non-malicious behavior. For example, after our initial solve for https://bugs.chromium.org/p/chromium/issues/detail?id=902427 we received reports from users who were confused why they couldn't accept permission dialogs  when it was due to e.g. a phone dialer bubble showing the screen. Which led to this exploration to improve the UX: https://docs.google.com/document/d/1JOj-I2ojvZa2DlClqFBUN0NQ1ee1cIsreqNtt3nlRM0/edit#

That said, this was added back in 2018 originally, with the UX improvement in 2020, so it's been a bit since we've looked at this.

Android added "chat bubbles" in Android 11 (2020), so it's possible that at least on Android 11+ the uses of overlay windows for legitimate reasons has declined sufficiently such that we could consider being more aggressive in our restrictions (e.g. not just disabling permission prompt taps but disabling). 

### le...@gmail.com (2023-04-07)

Yes, permission dialogs are protected in this scenario, but that only applies to windows directly on top of the permission dialogs. That's why the popup dialog pointing the location to tap disappears for a few seconds to allow for a tap. WebView is not very ideal for such an attack because it'll first of all require the victim to authenticate (login e.g to Google account) and give the app access to permissions, CCT doesn't require additional auth, making it an ideal target.

Maybe an interesting thing to consider would be to make the permission dialog an activity, this will make it show on top of any malicious overlay :-)

### le...@gmail.com (2023-04-07)

And when the permission dialog is an activity dialog, you can also detect when it loses focus. If another overlay displays on top of the dialog, finish the current dialog task and start a new dialog activity. This will ensure permission dialogs are always visible to users.

### le...@gmail.com (2023-04-07)

Just to clarify https://crbug.com/chromium/1430867#c17 on the WebView, a malicious app doesn't really need to trick users to tap while it can simply inject JavaScript and perform actions on behalf of the user. That's why WebView shouldn't be a concern, at least not for this attack vector.

### tw...@chromium.org (2023-04-07)

> Yes, permission dialogs are protected in this scenario, but that only applies to windows directly on top of the permission dialogs.

We're using FLAG_WINDOW_IS_PARTIALLY_OBSCURED, which I believe protects permission prompts from overlays on any part of the window, not just those directly over the permission dialog.

References: https://developer.android.com/reference/android/view/MotionEvent#FLAG_WINDOW_IS_PARTIALLY_OBSCURED

https://source.chromium.org/chromium/chromium/src/+/main:components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/ModalDialogView.java;l=261?q=FLAG_WINDOW_IS_PARTIALLY_OBSCURED&ss=chromium (filed crbug.com/1431459 to replace the reflection... we could have done that quite some time ago).

> CCT doesn't require additional auth

That's fair.

### le...@gmail.com (2023-04-07)

I agree, nice approach.

### [Deleted User] (2023-04-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-08)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tw...@chromium.org (2023-04-10)

Removing milestone target since this isn't a regression (has existed since the beginning of CCT), see https://crbug.com/chromium/1430867#c16 for rationale

### le...@gmail.com (2023-04-10)

Okay, is there any additional feedback you need from me? Asking because I'm seeing the feedback label.

### tw...@chromium.org (2023-04-10)

I think that was added for the question on OS version, which has been clarified. Removing the label!

### [Deleted User] (2023-04-11)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2023-05-02)

Hello there, isn't this issue fixed yet?

### kg...@google.com (2023-05-03)

Hi @levitnudi, thanks for following up! We have discussed this within the team and as per the rationale provided in https://crbug.com/chromium/1430867#c16 we want to prioritize an investigation for a solution for this during Q3 (July - September timeframe). We will be able to provide a more clear timeframe as we approach Q3 and we will have a clearer idea about the work planned for it and how it will be allocated.

### le...@gmail.com (2023-05-03)

Alright, thank you @kgrosu for the update!

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-07-12)

kgrosu - is there an updated schedule yet? Thanks!

### kg...@google.com (2023-07-12)

Yes, this has been slotted for Q3 so we should be able to look into it sometime in the next 2 months.

### ji...@chromium.org (2023-07-14)

[Empty comment from Monorail migration]

### ji...@chromium.org (2023-07-25)

From https://crbug.com/chromium/1430867#c16 https://crbug.com/chromium/1430867#c20, I think we may go with monitoring MotionEvents in CustomTabActivity#dispatchTouchEvent, block them if the flag FLAG_WINDOW_IS_PARTIALLY_OBSCURED is set. This is extending what we're already doing for permission dialog to the activity level.

Alternatively, we could (dynamically) if CCT is the top activity or not, and block the events accordingly. Haven't figured out how to do it. One way I tried was ActivityManager#getAppTasks which returns AppTask objects.  One of which should contain the TaskInfo for the current task, but AppTask#getTaskInfo is not always a valid one.    

### tw...@chromium.org (2023-07-25)

[Comment Deleted]

### tw...@chromium.org (2023-07-25)

> I think we may go with monitoring MotionEvents in CustomTabActivity#dispatchTouchEvent, block them if the flag FLAG_WINDOW_IS_PARTIALLY_OBSCURED is set. This is extending what we're already doing for permission dialog to the activity level.

I think this is likely too restrictive. iirc, FLAG_WINDOW_IS_PARTIALLY_OBSCURED might be set when e.g. dialer chat bubbles are showing. 

See this doc where we updated the explainer dialog text based on user feedback about being confused why they couldn't interact with permission prompts: https://docs.google.com/document/d/1JOj-I2ojvZa2DlClqFBUN0NQ1ee1cIsreqNtt3nlRM0/edit#heading=h.umrx4eppq67h

We have metrics tracking how often taps are blocked (or at least we used). iirc, while it's a small percent it's not trivial.

> Alternatively, we could (dynamically) if CCT is the top activity or not, and block the events accordingly.

I mentioned something similar up in https://crbug.com/chromium/1430867#c16 above :) not sure if there's a technical path forward but seems worth exploring since this conceptually seems like what we want


As another alternate idea:

Could we tell by Activity lifecycle state? 

There might be a wrinkle on prior OS versions when in multi-window where only one Activity is "resumed" at a time, but on newer OS versions maybe there's a workable solution.

### ji...@chromium.org (2023-07-26)

Thanks for the feedback and suggestions! Will experiment with them and make a summary to share.

### tu...@chromium.org (2023-07-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9

commit a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Thu Aug 03 23:34:03 2023

[CCT] Prevent taps from the overlay activity

Uses the activity state to proceed or discard touch event processing.
This can prevent taps coming down from overlay activity running
on top of the CCT.

Bug: 1430867
Change-Id: I471471dbbebf4528a01f1114e4317f252af7bbc3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4729026
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1179343}

[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/browser/flag_descriptions.cc
[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/browser/flags/android/chrome_feature_list.h
[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/android/java/src/org/chromium/chrome/browser/customtabs/CustomTabActivity.java
[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/browser/about_flags.cc
[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/browser/flag_descriptions.h
[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/browser/flag-metadata.json
[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/android/chrome_junit_test_java_sources.gni
[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/browser/flags/android/java/src/org/chromium/chrome/browser/flags/ChromeFeatureList.java
[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/browser/flags/android/chrome_feature_list.cc
[add] https://crrev.com/a6531d4f20eb5cbd1a2f20d65b7a41986f4febd9/chrome/android/junit/src/org/chromium/chrome/browser/customtabs/CustomTabsFilterTouchUnitTest.java


### ji...@chromium.org (2023-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-05)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-09)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let us know what name/handle you would like us to use in acknowledging you for this finding. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### le...@gmail.com (2023-08-10)

https://crbug.com/chromium/1430867#c45 Thank you so much! Acknowledged as Levit Nudi from Kenya

### le...@gmail.com (2023-08-10)

deleted

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36

commit 68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Tue Dec 12 00:27:29 2023

[CCT] Clean up a feature flag kCCTPreventTouches

Deletes the feature flag which is enabled by default, and the related
code as well.

Bug: 1430867
Change-Id: I73e567967005f552610610c53022fdcb502219db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5111939
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Sinan Sahin <sinansahin@google.com>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1236054}

[modify] https://crrev.com/68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36/chrome/browser/flag_descriptions.cc
[modify] https://crrev.com/68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36/chrome/browser/flags/android/chrome_feature_list.h
[modify] https://crrev.com/68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36/chrome/android/java/src/org/chromium/chrome/browser/customtabs/CustomTabActivity.java
[modify] https://crrev.com/68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36/chrome/browser/about_flags.cc
[modify] https://crrev.com/68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36/chrome/browser/flag_descriptions.h
[modify] https://crrev.com/68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36/chrome/browser/flags/android/java/src/org/chromium/chrome/browser/flags/ChromeFeatureList.java
[modify] https://crrev.com/68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36/chrome/browser/flags/android/chrome_feature_list.cc
[modify] https://crrev.com/68fbc4ce9b4fc50a13860cf199bf5125f9cb8e36/chrome/android/junit/src/org/chromium/chrome/browser/customtabs/CustomTabsFilterTouchUnitTest.java


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1430867?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Mobile>CustomTabs, UI>Browser>Permissions>Prompts]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063907)*
