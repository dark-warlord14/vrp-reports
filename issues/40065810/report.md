# Security: Users cannot escape the full screen mode in this offline .html file

| Field | Value |
|-------|-------|
| **Issue ID** | [40065810](https://issues.chromium.org/issues/40065810) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Android |
| **Reporter** | du...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2023-06-14 |
| **Bounty** | $3,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

Security: Users cannot escape the full screen mode in this offline .html file.

**VERSION**  

Chrome Version: 114.0.5735.61 + [stable]  

Operating System: Android 12

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

Open the .html file, click on the body of the web page to go to full screen, and then cannot escape the full screen mode.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Khiem Tran (@duckhiem)

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 544 B)
- [testcase.html](attachments/testcase.html) (text/plain, 544 B)

## Timeline

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-06-15)

I am able to escape fullscreen mode by going to the home screen, but the normal back gesture does appear to be broken.

[Monorail components: UI>Browser>FullScreen]

### [Deleted User] (2023-06-15)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-06-16)

I guess using the home screen, it means exit the browser, not exit the full screen, literally. 

### [Deleted User] (2023-06-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bb...@google.com (2023-06-19)

[Empty comment from Monorail migration]

### bb...@google.com (2023-06-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-28)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-10)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-20)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2023-07-20)

I can repro this - back button press (or any click event) invokes floating action bar, thus prevents the event from exiting fullscreen.  

The html/js code traps users into an inescapable hole, rendering the page basically useless. I think there are many ways to something similar, such as holding the main thread forever, or not allowing users to do anything else. I'm not sure if this could be viewed as a security hole - it seems like just one way to render the page useless.

dcheng@ could you help assess the severity? I'd like to understand if there are ways to use this trick to make the page vulnerable to security attack. Feel free to assign it back to me if you believe so.
 

### du...@gmail.com (2023-07-20)

Firstly, this disables the function of the fullscreen notification, and then, it can make people think they are escaping the fullscreen to fake the UI.

### dc...@chromium.org (2023-07-20)

I triaged this bug as the primary, and the severity labels and priority labels have already been set accordingly :) These severity guidelines are outlined at https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md

Triage-wise, this one was a bit tricky, because fullscreen has the potential for URL spoofing ("Complete control over the apparent origin in the omnibox"), especially on Android. This would normally mean High severity; however there are also mitigating factors here (going home breaks out, IIRC, the fullscreen notification is still displayed), thus the Medium rating.

Note that this is distinct from a browser DoS, because with this bug, the browser itself is still usable. Tying up the main thread means the user wouldn't be able to interact with the browser.

### ji...@chromium.org (2023-07-20)

[Empty comment from Monorail migration]

### tw...@chromium.org (2023-07-24)

> I can repro this - back button press (or any click event) invokes floating action bar, thus prevents the event from exiting fullscreen.  

Jinsuk, do you know what code is responsible for this? A demo video would also be helpful if it's easy to capture.

Users getting stuck in fullscreen certainly isn't great.

cc Kevin for visibility

### ji...@chromium.org (2023-07-24)

What happens is that the javascript keeps opening the floating action bar whenever the user presses the back button. The back button event is consumed to dismiss the action bar first, and the next back button press is supposed to exit the fullscreen. But the very action of the back button press opens the action bar again, so the code got itself into an inescapable loop.

I'm not certain if this can turn into a valid security threat. It may fool users into believing that he's out of fullscreen, but there's nothing he can do, such as typing in his credential; the float action bar is always on the screen, preventing any valid user input.

### tw...@chromium.org (2023-07-24)

> The back button event is consumed to dismiss the action bar first, and the next back button press is supposed to exit the fullscreen.

Is this Android backpress handling determining action bar dismissal is higher priority than exiting OS fullscreen mode or Chrome?

If it's Chrome, let's think how to mitigate (cc'ing lijin who's done a lot of backpress handling work recently)

### du...@gmail.com (2023-07-25)

So often, I see the fullscreen mode is used to fake the web address, and then, when users escape the fullscreen mode, the real address bar appears. In this case, the malicious website goes to fullscreen to show a fake address bar with a fake content, and then users escape the fullscreen but can't, and will believe the the fake address bar, and copy or translate the fake content via the floating action bar and use the fake content as a content from the trusted web address. At the first look, I see that, I will think more, deeper 

### ji...@chromium.org (2023-07-25)

Lijin may confirm - backpress handling on action mode is handled by OS and takes precedence over Chrome, on the ground that it is a general dismissal mechanism for action mode, and I don't see the backpress handler for action mode in Chrome [1]
 

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java;l=2261;drc=167158158bee37e5f6c4bd74059ac9fe514b0eee

### tw...@chromium.org (2023-07-25)

Lijin's OOO today. 

Could we do a simple / quick test to see if ChromeActivity#handleOnBackPressed is called?

There is some code relevant to clearing selection in that method...

```
       SelectionPopupController controller = getSelectionPopupController();
        if (controller != null && controller.isSelectActionBarShowing()) {
            controller.clearSelection();
            BackPressManager.record(Type.SELECTION_POPUP);
            return true;
        }
```

And it's ordered higher than our code to exit full screen, so that might be where things are getting snagged.

### ji...@chromium.org (2023-07-25)

Sorry my logic was hasty - you were right that it is SelectionPopupController that handles the floating action mode as well. Thought it was for selection dialog only. Verified that, by switching the order of the type code, we can exit fullscreen.

Let me hand this over to Lijin as it has more to do with BackPressManager than Fullscreen itself.

### tw...@chromium.org (2023-07-27)

[Empty comment from Monorail migration]

### la...@chromium.org (2023-07-27)

Thanks for investigating!

### gi...@appspot.gserviceaccount.com (2023-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8bbb9ffaaaed8b2e4759bfb626ed83232c47a731

commit 8bbb9ffaaaed8b2e4759bfb626ed83232c47a731
Author: Lijin Shen <lazzzis@google.com>
Date: Fri Jul 28 23:32:10 2023

Exit fullscreen before dismissing selection popup via back press.

Adjust the priority of fullscreen and selection popup back press
handlers such that back press event exits fullscreen first before
dismissing the selection popup.

Bug: 1454817
Change-Id: I21432a2468418a26e05240bbc00ca9823b36da0e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4730397
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Lijin Shen <lazzzis@google.com>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1176867}

[modify] https://crrev.com/8bbb9ffaaaed8b2e4759bfb626ed83232c47a731/chrome/android/javatests/src/org/chromium/chrome/browser/fullscreen/FullscreenManagerTest.java
[modify] https://crrev.com/8bbb9ffaaaed8b2e4759bfb626ed83232c47a731/chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java
[modify] https://crrev.com/8bbb9ffaaaed8b2e4759bfb626ed83232c47a731/components/browser_ui/widget/android/java/src/org/chromium/components/browser_ui/widget/gesture/BackPressHandler.java


### la...@chromium.org (2023-07-31)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-08-01)

Hi there,

I would ask the status Fixed means you landed the revision/changes/updates/fixing to Chrome on Android 115.0.5790.138?

Because I still can reproduce the report on Chrome on Android 115.0.5790.138.

https://drive.google.com/file/d/1Durkdzuu8Zk0swz_JKrZoR8adUemt8XQ/view?usp=drivesdk.

(The video of demonstration)

I hope for a double/bigger reward for this bypassing after the fixing :D.

### du...@gmail.com (2023-08-01)

I guess the bypassing can happen because I am using Android 12?

### la...@chromium.org (2023-08-01)

The fix landed on canary  117.0.5918.0. Please test using the latest canary.

### du...@gmail.com (2023-08-01)

I confirm the behavior is fixed on Canary 117.0.5918.0. Is this considered as a security-related bug for a reward? As I said, the behavior bases on three Google's Chrome's trusted products: the Back function on Android OS, the fullscreen notification and the floating action bar to trick users using/believing the content of the faked-URL website as the trusted content of the trusted website.

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

Requesting merge to stable M115 because latest trunk commit (1176867) appears to be after stable branch point (1148114).

Requesting merge to beta M116 because latest trunk commit (1176867) appears to be after beta branch point (1160321).

Merge review required: M115 is already shipping to stable.

Merge review required: M116 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-08-01)

116 merge approved, please merge https://crrev.com/c/4730397 to branch 5845 at your availability / by EOD tomorrow Wednesday 2 August, so this fix can be included in the next M116/Beta update on Thursday 

M115/Stable update RC was already recut for (delayed) release tomorrow, there are no further planned releases of M115/Stable 


### gi...@appspot.gserviceaccount.com (2023-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c439e21e2a8321105df6fd7f981d620513231f02

commit c439e21e2a8321105df6fd7f981d620513231f02
Author: Lijin Shen <lazzzis@google.com>
Date: Tue Aug 01 20:48:24 2023

[M116] Exit fullscreen before dismissing selection popup via back press.

Adjust the priority of fullscreen and selection popup back press
handlers such that back press event exits fullscreen first before
dismissing the selection popup.

(cherry picked from commit 8bbb9ffaaaed8b2e4759bfb626ed83232c47a731)

Bug: 1454817
Change-Id: I21432a2468418a26e05240bbc00ca9823b36da0e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4730397
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Lijin Shen <lazzzis@google.com>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1176867}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4738748
Cr-Commit-Position: refs/branch-heads/5845@{#1032}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/c439e21e2a8321105df6fd7f981d620513231f02/chrome/android/javatests/src/org/chromium/chrome/browser/fullscreen/FullscreenManagerTest.java
[modify] https://crrev.com/c439e21e2a8321105df6fd7f981d620513231f02/chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java
[modify] https://crrev.com/c439e21e2a8321105df6fd7f981d620513231f02/components/browser_ui/widget/android/java/src/org/chromium/components/browser_ui/widget/gesture/BackPressHandler.java


### du...@gmail.com (2023-08-02)

I hope for a bigger reward for this report :).

As usually if there is a function which can hide the notification about fullscreen, that behavior will be rewarded at least 3000 USD. This report is about the trusted Google/Chrome-owned Back button, the notification about fullscreen and the floating action bar are used to trick users believe the malicious content is from the the trusted domain while this is a fake domain as it is in fullscreen mode.


### du...@gmail.com (2023-08-08)

A friendly eager-to-know ping.

### am...@google.com (2023-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-09)

Congratulations, Khiem! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### du...@gmail.com (2023-08-09)

Thanks, Amy. Please help me process the payment with the Finance team (I am already in their system for paying). Personally, I hope I can get the bounty in the next two weeks ;).

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1454817?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1455291, crbug.com/chromium/1455777]
[Monorail components added to Component Tags custom field.]

### du...@gmail.com (2024-12-28)

deleted

### du...@gmail.com (2025-01-10)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065810)*
