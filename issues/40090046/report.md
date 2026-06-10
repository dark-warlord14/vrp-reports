# Chrome for Android - Window.open combined with the onbeforeunload dialog crashes Chrome's WebView render

| Field | Value |
|-------|-------|
| **Issue ID** | [40090046](https://issues.chromium.org/issues/40090046) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile>CompositedUI, UI>Browser>Mobile>CustomTabs |
| **Platforms** | Android |
| **Reporter** | he...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2018-01-04 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Opening a new window while in Chrome's WebView and redirecting the opener's location to trigger an onbeforeunload dialog crashes the render while still allowing the user to interact with the page in the background.  

This allows the attacker to spoof the URL and also to perform "clickjacking" on any website.

**VERSION**  

I tested on:  

Chrome 63.0.3239.111 / Android 6.0.1

**REPRODUCTION CASE**

WARNING:  

By following through the PoC, you will end up giving permission to the app "OAuth.io" to read your private email on Github.

1. From Chrome's WebView, you should access <https://lbherrera.github.io/lab/render/index.html>
2. Click on the link.
3. A dialog will show up asking if you want to leave the page, click in "Leave".
4. Click in the button "Redeem prize". If no button shows up, try again from Step 1.

\* I made this PoC only having my phone's screen resolution in mind, so the the button's location may be off and you will need to click elsewhere to give permission to the "attacker" on GitHub, but a dedicated attacker could easily fix this, as he knows the users' screen resolution.

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 5.4 MB)

## Timeline

### me...@chromium.org (2018-01-05)

I need to look into this more.

I was able to reproduce the exploit using the Twitter app exactly as you did.

However, I wasn't able to reproduce this using the webview_shell, the crashed renderer was immediately replaced by the page you were trying to clickjack on Github.

I'm unsure if Twitter is doing something weird or the WebView shell is behaving differently than WebView in apps.

### me...@chromium.org (2018-01-05)

As I expected, I was able to reproduce this using another app using WebView.

[Monorail components: Mobile>WebView]

### he...@gmail.com (2018-01-05)

I just tested and was able to reproduce it on Telegram and Facebook apps, so it doesn't seem to be something Twitter is doing specifically.

### me...@chromium.org (2018-01-05)

timvolodine@ Could you please take a look at this?

Thank you

### sh...@chromium.org (2018-01-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-18)

timvolodine: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2018-01-19)

currently no cycles to look at this.. unassigning to allow somebody else pick this up.

### me...@chromium.org (2018-01-26)

eugenebut, wjmaclean: Would either of you be able to take a look at this medium severity bug? Thanks!

### wj...@chromium.org (2018-01-26)

I'm afraid I have *zero* experience with Android WebView (which is quite a separate thing from desktop WebView, which I do work on).

### eu...@chromium.org (2018-01-26)

I don't work on Chrome for Android or Android WebView. From By description it's unclear if the problem is specific to Chrome or WebView. CCing folks from WebView and Chrome for Android to help with triage.

### te...@chromium.org (2018-01-26)

The twitter page looks like a chrome custom tab, so maybe not WebView related at all.  Does this reproduce in the standalone Chrome app?

### he...@gmail.com (2018-01-26)

#12: I believe you are right. I was not aware of Chrome Custom Tab's and mistakenly took it for the WebView. Sorry about that :/

And no, it doesn't reproduce on the standalone app.

### sh...@chromium.org (2018-02-01)

bauerb: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2018-02-01)

Thanks, nagbot! :-D

A few initial notes: 
* I can reproduce this in Stable and Canary. In a local debug build I get a blank page instead of the "Redeem prize" page, but otherwise the same behavior. I'll try a Release build to see if that makes a difference.
* I did not get any indication of an actual crash (either as a crash report or a stack trace on logcat). If there is a process going down, it's doing that very silently.
* The page that is being loaded definitely is https://github.com (as seen in the origin indicator), and it can even be interacted with (I get a keyboard popping up when I tap on the page, presumably because I'm hitting a text input field), but what is _visible_ is the old page.
* chrome://inspect/#devices actually shows two tabs (!) when that happens. By clicking "focus tab" I can switch the active tab.
* If the github authorization tab is active (i.e. not the spoof page), what is visible in the custom tab is ever so slightly blurry, which is what happens if the compositor draws a saved snapshot of the webcontents (which is stored at slightly reduced quality) instead of the "live" webcontents.

[Monorail components: -Mobile>WebView UI>Browser>Mobile>CustomTabs]

### ba...@chromium.org (2018-02-06)

WIP CL is up at https://chromium-review.googlesource.com/c/chromium/src/+/904982.

### ba...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Mobile>CompositedUI]

### bu...@chromium.org (2018-02-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/371ba40daa4b7c34912b02e0288e165ae2043a93

commit 371ba40daa4b7c34912b02e0288e165ae2043a93
Author: Bernhard Bauer <bauerb@chromium.org>
Date: Thu Feb 08 11:06:02 2018

🖿🔬 Move tab observation from LayoutManagerChrome to LayoutManager.

This ensures that all activities using a LayoutManager observe the necessary tab
events (not just ChromeTabbedActivity), and allows removing the
CustomTabLayoutManager, which used to observe only a subset of events.

Bug: 798933
Change-Id: I20242ba89fc058256adeddfdc42260c0220a9fe8
Reviewed-on: https://chromium-review.googlesource.com/904982
Commit-Queue: Bernhard Bauer <bauerb@chromium.org>
Reviewed-by: Matthew Jones <mdjones@chromium.org>
Reviewed-by: Yusuf Ozuysal <yusufo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#535351}
[modify] https://crrev.com/371ba40daa4b7c34912b02e0288e165ae2043a93/chrome/android/java/src/org/chromium/chrome/browser/compositor/layouts/LayoutManager.java
[modify] https://crrev.com/371ba40daa4b7c34912b02e0288e165ae2043a93/chrome/android/java/src/org/chromium/chrome/browser/compositor/layouts/LayoutManagerChrome.java
[modify] https://crrev.com/371ba40daa4b7c34912b02e0288e165ae2043a93/chrome/android/java/src/org/chromium/chrome/browser/compositor/layouts/LayoutManagerChromeTablet.java
[modify] https://crrev.com/371ba40daa4b7c34912b02e0288e165ae2043a93/chrome/android/java/src/org/chromium/chrome/browser/customtabs/CustomTabActivity.java
[delete] https://crrev.com/21a534ef80dc7ab11a42747f2601bdc48a740ba8/chrome/android/java/src/org/chromium/chrome/browser/customtabs/CustomTabLayoutManager.java
[modify] https://crrev.com/371ba40daa4b7c34912b02e0288e165ae2043a93/chrome/android/java/src/org/chromium/chrome/browser/webapps/WebappActivity.java
[modify] https://crrev.com/371ba40daa4b7c34912b02e0288e165ae2043a93/chrome/android/java_sources.gni


### ba...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### ba...@chromium.org (2018-02-08)

+Emily because spoofing

Do I need to do anything special to make the sheriffbot pick this up?

### es...@chromium.org (2018-02-08)

No need to do anything special for sheriffbot, however, I think we may want to try to merge this to M65 per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#medium-severity.

Thanks for the fix!

### ba...@chromium.org (2018-02-08)

Sure! I actually have cherry-pick CLs for 65 (https://chromium-review.googlesource.com/c/chromium/src/+/906777) and 64 (https://chromium-review.googlesource.com/c/chromium/src/+/906934).

### es...@chromium.org (2018-02-08)

Ah, great, thank you!

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-19)

Nice one luan.herrera@! The Chrome VRP panel decided to award $2,000 for this report. Thanks!

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@google.com (2018-03-19)

Please verify the fix in the latest canary

### cm...@google.com (2018-03-23)

Ping!

### wj...@chromium.org (2018-03-23)

[Empty comment from Monorail migration]

### cm...@google.com (2018-03-26)

awhalley@ please can you make ensure this issue is merge into M66? Unless it can wait?

### cm...@google.com (2018-03-30)

I have requested this issue to be merged into M66 since March 19th. We are now only few days away from releasing M66. Can someone on this thread handle this since the owner does not respond? 

awhalley@ do we care about merging this security issue?

### aw...@google.com (2018-03-30)

No merge needed for 66

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/798933?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Mobile>CompositedUI, UI>Browser>Mobile>CustomTabs]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090046)*
