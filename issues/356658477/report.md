# Android Chrome External Navigation Bubble Tapjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [356658477](https://issues.chromium.org/issues/356658477) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Intents |
| **Platforms** | Android |
| **Chrome Version** | 127.0.6533.65 |
| **Reporter** | sh...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2024-07-31 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Make sure “com.sec.android.app.sbrowser” is installed on your Android device. (<https://play.google.com/store/apps/details?id=com.sec.android.app.sbrowser>)
2. Open Chrome and visit - <http://bugtest.unaux.com/bubble.html>
3. Click on the red box 3 times
4. Notice, that “Samsung Browser” is triggered accidentally and inside it “[http://evil.com”](http://evil.com%E2%80%9D) is opened.

# Problem Description

Previously I reported [issue 356038470](https://issues.chromium.org/issues/356038470) “Tapjacking on Intent chooser dialog box” which got marked as duplicate, so I got another way to perform browser downgrade attack using the External Navigation bubble tapjacking, which prompts user’s to open any installed apps using INTENT redirects.

If an attacker tricks user’s into clicking 2-3 times on the webpage on a specific point then the user’s will accidentally trigger the INTENT redirect and end up opening any malicious INTENTS.

# Summary

Android Chrome External Navigation Bubble Tapjacking

# Custom Questions

#### Reporter credit:

Mohit Raj (shadow2639)

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [bubble.html](attachments/bubble.html) (text/html, 1.1 KB)
- [Screenrecorder-2024-08-01-00-21-07-701_720x1560.mp4](attachments/Screenrecorder-2024-08-01-00-21-07-701_720x1560.mp4) (video/mp4, 7.2 MB)

## Timeline

### dc...@chromium.org (2024-08-02)

I'm able to reproduce this, and this appears to be a different UX surface for triggering the same behavior. I don't know enough about the underlying implementation to judge if this is something that would have the same root cause (and thus fix) as [issue 40074891](https://issues.chromium.org/issues/40074891). mthiesse@, feel free to "Mark as Duplicate" if you think this is substantially the same.

### mt...@chromium.org (2024-08-02)

lazzzis, have we thought about click-jacking protections at all for Messages UI?

### pe...@google.com (2024-08-02)

Setting milestone because of s2 severity.

### pe...@google.com (2024-08-02)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### la...@google.com (2024-08-02)

> have we thought about click-jacking protections at all for Messages UI?

The primary button is not clickable until the showing animation is done. Do you mean disabling click events for a few milliseconds even after the message has been fully displayed?

### mt...@chromium.org (2024-08-06)

Yes, I believe we would have to disable events for a few milliseconds - I'm not sure what security guidelines say about it.

### pe...@google.com (2024-08-22)

lazzzis: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-09-06)

lazzzis: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ke...@chromium.org (2024-09-25)

Trying to bring some attention back to this: cthomp@, are there general guidelines for how long UI like this should be visible before accepts clicks/taps? (question from comment 7)

### ct...@chromium.org (2024-09-25)

Our general rule of thumb is 500ms for smaller surfaces. We have some guidance at <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-considerations-for-browser-ui.md#introduce-a-short-delay-before-the-ui_s-call_to_action-activates>

### sh...@gmail.com (2024-10-16)

Hi team, just wanted to inform you that the old POC testing link “http://bugtest.unaux.com/bubble.html” has been changed to “https://pocs.iceiy.com/bubble.html”.

### tw...@google.com (2024-12-04)

Thanks for the sharing the updated POC link.

This is still on our team's radar to fix when we have some spare cycles.

### tw...@google.com (2024-12-14)

Hi Lijin,

This could be a great bug to pick up over the quieter holiday period given it's a longer standing S2 security bug and out of P1 fix SLO.

### tw...@google.com (2025-03-28)

Lijin, friendly reminder on this security bug that's been in the backlog for a while

### dx...@google.com (2025-04-03)

Project: chromium/src  

Branch: main  

Author: Lijin Shen [lazzzis@google.com](mailto:lazzzis@google.com)  

Link:      <https://chromium-review.googlesource.com/6411166>

Add tap protection to message ui

---


Expand for full commit details
```
     
    Disallow any touch event as soon as the animation starts. The message should become clickable again once the tap protection period ends. 
     
    Bug: 356658477 
    Change-Id: I3522cb07e0b9a4c6fbe9f88cbe12777ffc41b5d5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6411166 
    Reviewed-by: Aishwarya Rajesh <aishwaryarj@google.com> 
    Commit-Queue: Lijin Shen <lazzzis@google.com> 
    Reviewed-by: Theresa Sullivan <twellington@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1442451}

```

---

Files:

- M `chrome/android/javatests/BUILD.gn`
- A `chrome/android/javatests/src/org/chromium/chrome/browser/messages/MessageTest.java`
- A `chrome/android/javatests/src/org/chromium/chrome/browser/messages/OWNERS`
- M `components/messages/android/internal/java/src/org/chromium/components/messages/MessageBannerMediator.java`
- M `components/messages/android/internal/java/src/org/chromium/components/messages/MessageBannerView.java`
- M `components/messages/android/internal/java/src/org/chromium/components/messages/MessageBannerViewBinder.java`
- M `components/messages/android/java/src/org/chromium/components/messages/MessageBannerProperties.java`
- M `components/messages/android/test/java/src/org/chromium/components/messages/MessagesTestHelper.java`

---

Hash: 95729cec0565596f159af487d0bceeb82a7755b8  

Date:  Thu Apr 3 22:02:33 2025


---

### la...@google.com (2025-04-08)

Please verify

### sp...@google.com (2025-04-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-18)

Congratulations! Thank you for your efforts and reporting this issue to us.

### ch...@google.com (2025-04-30)

deleted

### ch...@google.com (2025-07-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact exploitation mitigation bypass

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/356658477)*
