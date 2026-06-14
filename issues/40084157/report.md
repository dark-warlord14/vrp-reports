# Chrome for Android - Modal dialog being executed after window.open is called allows for URL Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40084157](https://issues.chromium.org/issues/40084157) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WindowDialog, UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | he...@gmail.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2016-04-23 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability makes it possible to display an arbitrary modal dialog over a window with a spoofed URL by calling a modal dialog after opening a new window. Thus making the victim believe that the modal dialog is from the website he was trying to access, while in reality, it is being controlled by the attacker.

**VERSION**  

I tested on:  

Chrome 49.0.2623.105 / Android 5.1.1  

Chrome 49.0.2623.105 / Android 4.4.2

**REPRODUCTION CASE**

1. Download index.html
2. Open the file and click on the link.
3. A prompt should appear asking for you credentials under the <https://www.google.com> URL.

## Attachments

- [index.html](attachments/index.html) (text/plain, 621 B)
- [spoof.png](attachments/spoof.png) (image/png, 65.6 KB)

## Timeline

### va...@chromium.org (2016-04-25)

meacer@ -- based on some of the other dialog related spoofing bugs, assigning to you. please re-assign as appropriate or assign it back to me.

+CC: felt@

[Monorail components: Security>UX UI>Browser>Navigation]

### cl...@chromium.org (2016-04-26)

[Empty comment from Monorail migration]

### me...@chromium.org (2016-04-26)

I can confirm the bug, although it doesn't always repro.

### dc...@chromium.org (2016-04-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>WindowDialog]

### me...@chromium.org (2016-05-24)

Avi: Does your plan to fix alert include suppressing dialogs coming from background tabs? 

### av...@chromium.org (2016-05-24)

My plan doesn't currently involve Androids. It is possible to bring them into it later, but right now it's desktop-only.

### me...@chromium.org (2016-05-25)

Okay, in that case we'll need to bring alerting tabs to foreground on Androids.

### ra...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX]

### av...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-01-04)

+xisigr who also reported this in https://crbug.com/chromium/677728

### me...@chromium.org (2017-01-04)

Avi, what do you think is the right approach here? Should we suppress the dialog if it's in the background, or should we bring it to the foreground? I believe you had plans to do the former?

### me...@chromium.org (2017-01-04)

Ignore https://crbug.com/chromium/606104#c11, you already answered it in https://crbug.com/chromium/606104#c6 which means I fail at reading :)

### av...@chromium.org (2017-01-04)

NP.

Re https://crbug.com/chromium/606104#c11, either is fine. Either suppress the dialog, or bring the page that spawned it forward. The choice is a design decision (which I'm slowly working on changing on the desktop) but if you don't keep the showing of dialogs in sync with the showing of pages that show them, you essentially get this URL spoof.

### me...@chromium.org (2017-01-04)

Thanks. It seems like suppressing background dialogs is the better solution (both for desktop parity and user experience) but might need an intent-to-deprecate, do you agree? I'm curious how much of a battle that will be versus simply bringing the tab into focus and fixing the immediate issue.

### av...@chromium.org (2017-01-04)

I have that on my list of things to eventually do, but alert() usage is high, and its use to pull webpages to the front is high. I'm collecting UMA stats to make the argument, but I suspect if you file the intent now it will not go well.

I would highly suggest going the other route :)

### me...@chromium.org (2017-01-04)

Sounds good, I'll leave fighting the good fight to you then :) I'll simply bring the tab back to focus.

### me...@chromium.org (2017-01-05)

luan.herrera, xisigr: Are you able to consistently reproduce this? The POCs don't work for me on a tip of tree build -- the tab in the background is already brought forward when it shows a dialog.

### xi...@gmail.com (2017-01-05)

meacer:My POCs work well ,https://bugs.chromium.org/p/chromium/issues/detail?id=677728

### me...@chromium.org (2017-01-05)

Thanks, I tried on a couple of different devices and it looks like it reproduces when the tab strip is not visible (repros on phones but not tablets).

### me...@chromium.org (2017-03-02)

Similar to https://crbug.com/chromium/549724, this also seems to be fixed, possibly by avi's change to suppress dialogs from swapped out frames (https://crbug.com/chromium/634108). I'm unable to reproduce it, the alert gets cancelled when the google.com tab opens.

luan.herrera, xisigr: Are you still able to repro?

### xi...@gmail.com (2017-03-02)

meacer:Which POCs do you run? These two bugs(https://crbug.com/chromium/549724,https://crbug.com/chromium/634108)I can't see. I still can reproduce in https://crbug.com/chromium/677728's POCs.
(Android chrome 56.0.2924.87)

### va...@chromium.org (2017-06-27)

meacer@, any update on this bug?
- your friendly secondary security sheriff.

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### he...@gmail.com (2018-01-06)

I was giving a look at this again and I can reproduce https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=232261 (63.0.3239.111 / Android 6.0.1).

### me...@chromium.org (2018-02-14)

I think I'm actually not the right owner since I don't know how modal dialogs are triggered on Android.

tedchoc: Would you be able to find an appropriate owner? Thanks.

### te...@chromium.org (2018-02-15)

+huayinz@ is making tab modal dialogs work on Android, so sending their way

We already attempt to bring tabs to the foreground when a dialog is shown, so I suspect this is a race condition

TabWebContentsDelegateAndroid#activateContents
https://cs.chromium.org/chromium/src/chrome/android/java/src/org/chromium/chrome/browser/tab/TabWebContentsDelegateAndroid.java?q=bringActivityToForeground&sq=package:chromium&dr=CSs&l=349

Maybe we need to prevent tabs being switched while a dialog is present so we could essentially lock it to this tab (only in the case of modal dailogs)?

I wonder if we turn on modal JS dialogs right now, would this problem go away and thus we should just focus on getting that launched?

### me...@chromium.org (2018-02-15)

On desktop we started hiding dialogs from background tabs until the user brings the tab to the foreground because modal dialogs were being abused -- Avi is the expert on this. It would be nice to have parity and do something similar on mobile.

### av...@chromium.org (2018-02-15)

Yes, this is the removal of activation of alert(), https://www.chromestatus.com/feature/6477774290157568 and prompt(), https://www.chromestatus.com/feature/5637107137642496. Gonna do confirm soon.

We should do something similar with Android.

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### hu...@chromium.org (2018-03-30)

If we turn on tab modal JS dialog, this issue would go away since it brings in Avi's work on removal of activation. So yes, we should just focus on getting that launched.

### hu...@chromium.org (2018-09-26)

JS tab modal dialog is launched (see https://crbug.com/chromium/799334), so this issue won't happen anymore.

### sh...@chromium.org (2018-09-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-04)

Nice one luan.herrera@! The VRP panel decided to award $2,000 for this report.

### aw...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-05)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-12-14)

+ awhalley@ (Security TPM) for M72 merge review. I don't see any CL here.

### aw...@google.com (2018-12-14)

No merge required

### sh...@chromium.org (2019-01-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-01-03)

This issue was migrated from crbug.com/chromium/606104?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WindowDialog, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/677728]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084157)*
