# Security: Android file picker dialog can be shown over a different tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40063021](https://issues.chromium.org/issues/40063021) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>File, UI>Browser>Navigation |
| **Platforms** | Android, Linux |
| **Reporter** | st...@gmail.com |
| **Assignee** | bo...@chromium.org |
| **Created** | 2023-02-10 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to show a file/image picker dialog over a different tab.

This works regardless if the user has granted the Android system "Photos and videos" permission to Chrome. If not, the Android permission dialog (see [poc-with-system-dialog.webm]) will also be displayed over the opened tab ("google.com").  

As "google.com" is the only origin information shown at this time and there is no further origin information in the dialog itself, this can trick the user into thinking it was opened/requested by the "google.com" tab.

**VERSION**  

Chrome Version: 109.0.5414.118  

Operating System: Android 13

**REPRODUCTION CASE**

1. Open poc.html
2. Tap in the page

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc-with-camera.webm](attachments/poc-with-camera.webm) (video/webm, 1.5 MB)
- [poc-with-system-dialog.webm](attachments/poc-with-system-dialog.webm) (video/webm, 557.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 800 B)

## Timeline

### [Deleted User] (2023-02-10)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-11)

This looks like an Android variant of 1305663. Looping in some folks from that bug. avi@, could you decide whether this is a duplicate or not?


[Monorail components: Blink>Forms>File UI>Browser>Navigation]

### [Deleted User] (2023-02-11)

[Empty comment from Monorail migration]

### av...@chromium.org (2023-02-11)

I don’t know. +some of my favorite Clank folks.

### [Deleted User] (2023-02-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-12)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-02-13)

I don't have much to add except generic things, and I don't have permission for 1305663

Desktop has dialogs that's scoped to a tab (just tried alert()), so switching tabs is safe since it hides the dialog. Desktop also has regular per-window dialogs, like the file select one in poc here; and poc reproduces on desktop as well.

Both of these on android are system dialogs I believe. And especially going to the camera, I don't think chrome even has the ability to cancel that once the camera app is launched.

So I think the general fix is something like:
1) disallow the web page (and user?) from switching tabs when a per-window dialog is showing
2) make sure to treat these android dialogs as per-window

1) sounds like cross-platform change

### st...@gmail.com (2023-02-13)

For the Android system dialog requesting permissions for Chrome, there was a similar bug a few years ago that was fixed [0] by checking if the web contents is visible before showing the dialog. I was thinking the same approach could be used for this, but it would not cover the case when the active tab is changed after the dialog is open (see below).

Generally, programatically opening a new tab after the dialog has been opened and is still showing should not be easy (as that'd require user activation, which should've been consumed by opening the dialog), but is still possible if pop-up blocking is disabled, for example.

The Android system permission dialog itself showing over a different tab is not an issue as it grants a permission to Chrome only (not to a website). But dialogs/pickers showing over a different tab are an issue as the user can make the assumption that the currently opened tab is the one requesting it.

Closing all dialogs/pickers when the currently active tab changes seems like the way this should behave, if that's something Android supports, though.

This does indeed reproduce on desktop as well. I presume that's what 1305663 is about (I can't access it either).

[0]: https://chromium-review.googlesource.com/c/chromium/src/+/3226375

### [Deleted User] (2023-02-26)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-08)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-20)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-30)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-08)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-19)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-29)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2023-07-21)

Quick ping on this P-1 bug, which is (well) outside the 20 day SLO. Any updates? Does this need to be P-1?

### pg...@google.com (2023-07-21)

Chatted with Avi offline -
Bo, reassigning to you in hopes that you might have a clearer picture into the Android world and a way forward (whether that be a fix or a better owner)!

### bo...@chromium.org (2023-07-24)

This reproduces on linux as well, so not android-specific. I don't have machine to test, but I suspect mac and windows are the same. This is more of a UX issue than a bug. I'll send a mail to csa team and see if anyone has opinions..

### bo...@chromium.org (2023-07-24)

Looked at the code a bit. Creating the new window goes through WebContentsImpl::CreateNewWindow. File chooser goes through WebContentsImpl::RunFileChooser. So one fix might be:
* prevent RunFileChooser if WebContents is invisible / background
* prevent creating new windows if there are pending file choosers (or in theory any other kind of dialog)
The events are racy on the browser side, so need to do both of these to avoid user confusion here. Note it's not an option to dismiss file chooser when WebContents becomes hidden, because that's not always possible on android.

This changes web platform behavior. And there's probably other dialogs and whatnot not covered by this particular POC.

+some url spoofing security ux people. thoughts?

### bo...@chromium.org (2023-07-24)

> Note it's not an option to dismiss file chooser when WebContents becomes hidden, because that's not always possible on android.

I suppose it's possible to sever the connection between the file chooser and the page, so that whatever user does select is just dropped and not passed to the page.

### bo...@chromium.org (2023-08-09)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-08-09)

cc reviewer

### gi...@appspot.gserviceaccount.com (2023-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3afe258e082d2f69abdb518c740cbd563d753d4f

commit 3afe258e082d2f69abdb518c740cbd563d753d4f
Author: Bo Liu <boliu@chromium.org>
Date: Fri Aug 11 23:02:56 2023

Reduce file chooser user confusion

Disallow invisible WebContents to create file chooser. Disallow
switching to new tab by opening a new window if there is an active file
chooser. Only allow one file chooser per WebContents at one time.

Add a feature flag to guard new behavior.

Bug: 1414936
Change-Id: Ia4a83da8a7d1dbdcf0eab649175d7ebe5507dc9d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4755412
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Commit-Queue: Bo Liu <boliu@chromium.org>
Reviewed-by: Joe DeBlasio <jdeblasio@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1182835}

[modify] https://crrev.com/3afe258e082d2f69abdb518c740cbd563d753d4f/content/shell/browser/shell.cc
[modify] https://crrev.com/3afe258e082d2f69abdb518c740cbd563d753d4f/content/common/features.h
[modify] https://crrev.com/3afe258e082d2f69abdb518c740cbd563d753d4f/content/browser/web_contents/file_chooser_impl.cc
[modify] https://crrev.com/3afe258e082d2f69abdb518c740cbd563d753d4f/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/3afe258e082d2f69abdb518c740cbd563d753d4f/content/shell/browser/shell.h
[modify] https://crrev.com/3afe258e082d2f69abdb518c740cbd563d753d4f/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/3afe258e082d2f69abdb518c740cbd563d753d4f/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/3afe258e082d2f69abdb518c740cbd563d753d4f/content/common/features.cc


### bo...@chromium.org (2023-08-14)

What's the merge requirement here?

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### ma...@google.com (2023-08-14)

> What's the merge requirement here?
I think sheriffbot will figure that out based on the security triage labels.


### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations on another one Thomas! The Chrome VRP Panel has decided to award you $5,000 for this report, the reward amount given the increased feasibility and plausibility of this spoof beyond baseline expectations. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@navercorp.com (2023-11-24)

Does this patch work in android webview?

### bo...@chromium.org (2023-11-27)

If an app uses webview exactly same way as tabs in chrome (which there is not really anyway to verify) then the fix works same way. In general though, this is a security UX issue, and UX is the concern of the app using webview, not webview itself. And even more generally, it's a really bad idea to build a general-purpose browser with webview, because it's essentially impossible to build good security UX, because the webview API is very limited.

### gi...@appspot.gserviceaccount.com (2023-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8bb2b866e0402d4fa123c383bb9c53b8bcb6339c

commit 8bb2b866e0402d4fa123c383bb9c53b8bcb6339c
Author: Bo Liu <boliu@chromium.org>
Date: Mon Dec 18 19:36:20 2023

Clean up kWindowOpenFileSelectFix

Remove the kill switch.

Bug: 1414936
Change-Id: I163be605868ae04d8f5485d1326dbe5d743fc5c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5123019
Auto-Submit: Bo Liu <boliu@chromium.org>
Commit-Queue: John Abd-El-Malek <jam@chromium.org>
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1238653}

[modify] https://crrev.com/8bb2b866e0402d4fa123c383bb9c53b8bcb6339c/content/common/features.h
[modify] https://crrev.com/8bb2b866e0402d4fa123c383bb9c53b8bcb6339c/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/8bb2b866e0402d4fa123c383bb9c53b8bcb6339c/content/common/features.cc


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1414936?no_tracker_redirect=1

[Multiple monorail components: Blink>Forms>File, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063021)*
