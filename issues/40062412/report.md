# Security: PWA Installation can be unknowingly installed and launched into by pressing the "Enter" button repeatedly

| Field | Value |
|-------|-------|
| **Issue ID** | [40062412](https://issues.chromium.org/issues/40062412) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2022-12-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

By convincing the user to repeatedly press a button multiple times, it is possible to convince them to install a malicious PWA app and open it at the same time.

Since the PWA app do not show the address bar (only shows the origin which fades after a few seconds), it enables an attacker to spoof convincing UI as the omnibox is not present in the PWA prompt.

**VERSION**  

Chrome Version: 108.0.5359.125 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 Version 21H2 (Build 19044.2364)

**REPRODUCTION CASE**

1. Go to <https://lavender-goose-apple.glitch.me/a2hs-poc.html>
2. Repeatedly click "Enter" in quick succession (I set it to 10 times required)
3. You will install a PWA app which can contain convincing UI (I just put a regular login form) and launch it even.

This is quite similar to the Web browser app mode spoofing attacks discussed in <https://www.bleepingcomputer.com/news/security/web-browser-app-mode-can-be-abused-to-make-desktop-phishing-pages/>. Except now it can be launched from the web. (But you have to convince the user to repeatedly press "Enter" multiple times.)

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [a2hs-poc.html](attachments/a2hs-poc.html) (text/plain, 939 B)
- [app.js](attachments/app.js) (text/plain, 1.8 KB)
- [app.webmanifest](attachments/app.webmanifest) (application/octet-stream, 1.1 KB)
- [dummy-sw.js](attachments/dummy-sw.js) (text/plain, 156 B)
- [phishing.html](attachments/phishing.html) (text/plain, 731 B)
- [style.css](attachments/style.css) (text/plain, 868 B)
- [Untitled_ Dec 28, 2022 2_56 AM.webm](attachments/Untitled_ Dec 28, 2022 2_56 AM.webm) (video/webm, 1015.5 KB)

## Timeline

### [Deleted User] (2022-12-27)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-12-27)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-12-27)

Here is a video of the spoof. Few key points to note:

1) The PWA is launched immediately, and utilises the MS-Teams logo. The logo lends credence that the MS-Teams application being opened
2) The PWA can be launched over the browser line-of-death, which makes it very much more convincing.
3) An origin is shown at the top but it is very very very easy to miss and will fade after 1-2 seconds.

A website should not be able to install a PWA or even launch it without explicit user consent.

### li...@chromium.org (2022-12-27)

I managed to reproduce this on Linux, this does seem particularly useful for phishing. If a user hits enter multiple times and the PWA install prompt appears, the install button is in focus so the next time the user hits enter they install the PWA. 

Setting as medium for now since it seems like a pretty trivial spoof that can be effective for phishing, but this feels borderline low/medium to me. Adding a couple security UX and MWI folks to PTAL and reroute if necessary. 


[Monorail components: UI>Browser>WebAppInstalls]

### [Deleted User] (2022-12-27)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-12-27)

Our typical recommendation for prompts is to make "Cancel" the default selected button, or having no button selected by default. For example, LabelButton can be set to not be the default in order to not take ENTER events (https://source.chromium.org/chromium/chromium/src/+/main:ui/views/controls/button/label_button.cc;l=208;drc=6d35269c83e6cebb41c078dd2697547ae9165337). Or, if this is a Dialog, then you can set ui::DIALOG_BUTTON_NONE as the default button in the DialogDelegate implementation (https://source.chromium.org/chromium/chromium/src/+/main:ui/views/window/dialog_delegate.h;l=124;drc=6e3fe13366e47d7baddbca167c5cdeb87eb063f3).

### ct...@chromium.org (2022-12-27)

Question for the reporter: Does this reproduce if the user instead holds down ENTER instead of pressing it repeatedly?

### ha...@gmail.com (2022-12-28)

Only when pressing repeatedly.

### ei...@chromium.org (2022-12-28)

This is not an Android PWA issue, removing myself from owner.

Adding dmurph@ to triage for dPWA

### [Deleted User] (2022-12-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-11)

dmurph: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-25)

dmurph: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### dm...@chromium.org (2023-05-22)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-05-22)

I just checked the Chrome Canary build and this issue is indeed fixed by https://chromium-review.googlesource.com/c/chromium/src/+/4505003 which references https://crbug.com/chromium/1442018, which is a later reported duplicate of this issue.

### [Deleted User] (2023-05-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-23)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-01)

Congratulations, Axel! The VRP Panel has decided to award you $1,000 for this report. I've added the CVE number to this report as well as updated the security fix notes on the Chrome releases blog to reflect your finding as the primary one. Thank you for your efforts and reporting this issue to us. 

### am...@chromium.org (2023-06-01)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-06-01)

If there aren't any issues, may I have access to https://crbug.com/chromium/1442018?

### am...@google.com (2023-06-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1403836?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1442018]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062412)*
