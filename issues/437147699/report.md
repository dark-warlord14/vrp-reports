# Chrome on Android: Spoof issue triggered by bottom address bar

| Field | Value |
|-------|-------|
| **Issue ID** | [437147699](https://issues.chromium.org/issues/437147699) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Chrome Version** | 141.0.7341.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pn...@google.com |
| **Created** | 2025-08-07 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

1. Navigate to <https://lbstyle.github.io/sandbox.html>
2. Tap inside the input field
3. Tap docwrite1

# Problem Description

Note: This is very similar to [issue 379652406](https://issues.chromium.org/issues/379652406) and [issue 40064686](https://issues.chromium.org/issues/40064686).

The omnibox disappears, and the attack can trick the user into thinking they are seeing a fake omnibox of a secure website.

# Summary

Chrome on Android: Spoof issue triggered by bottom address bar

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A \

## Attachments

- js-dialog-origin-spoof-frame.html (text/html, 2.0 KB)
- sandbox.html (text/html, 571 B)
- screen.mp4 (video/mp4, 852.4 KB)

## Timeline

### ch...@gmail.com (2025-08-07)

The issue occurs when Chrome is run with the address bar positioned at the bottom of the screen. 

### za...@google.com (2025-08-08)

[security shepherd]

Thanks for submitting this report. I haven't yet been able to reproduce it on my Android emulator (pixel 6 device).
I think this report shows a functional bug instead of a security vulnerability: the omnibox unexpectedly disappears on Android, triggered by specific interactions with document.write api when using the bottom address bar. This is likely caused by a UI glitch, as the omnibox is not rendered correctly. This can also be exploited by creating a spoofing attack.

I'm converting this to a functional bug and rerouting it to the Android UI team and triaging this bug accordingly. The priority of this bug will be based on the impact on the UI issues and they may change the priority I assigned. The bottom omnibox is relatively new feature and there are some bugs reported related to this issue in the internal bug management system. Thanks for reporting.

Hi pnoland@, we received a bug related to Clank bottom omnibox feature that can be potentially exploited, can you please take a look at my assessment and see if this bug can be addressed by your team? Please feel free to reassign. Thank you.

### ch...@gmail.com (2025-08-08)

This is not a security bug?

### za...@google.com (2025-08-08)

You've raised a very fair point. Thank you for the follow-up. After reconsidering based on your comment and our security guidelines(<https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#what-makes-a-ui-spoof-interesting-to-report>), I agree that this should be classified as a security bug. While the root cause is a functional glitch in the UI, the impact is a UI spoof that can mislead a user into making an incorrect security decision. This meets the bar for a security vulnerability as I double checked.

I have reverted the bug's type to Security and adjusted the priority accordingly. My assignment to the Android UI team and pnoland@ still stands, as they should be the correct team to fix the underlying UI issue. Thank you again for your report.

### pn...@google.com (2025-08-08)

Thank you for finding this.

### ch...@google.com (2025-08-09)

Setting milestone because of s2 severity.

### dx...@google.com (2025-08-12)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/6832030>

[mobar] Handle mid-animation replacement

---


Expand for full commit details
```
     
    Although not explicitly documented, it's possible for a new IME 
    animation to start without the old one finishing, e.g. a "false start" 
    start-showing-then-hide. If we don't update to reflect the state of the 
    new animation we mistakenly perform updates as if the old one is still 
    running which can cause us to e.g. miscalculate the translation. 
     
    Bug: 437147699 
    Change-Id: I56b22c121848acb61410d33b42e82b8c0b05cd1a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6832030 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1500279}

```

---

Files:

- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarController.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarControllerTest.java`

---

Hash: [b583fe9162bd751d0c6bd065b4e7da0c76d66c6a](https://chromiumdash.appspot.com/commit/b583fe9162bd751d0c6bd065b4e7da0c76d66c6a)  

Date: Tue Aug 12 17:46:56 2025


---

### ch...@gmail.com (2025-08-13)

I’ve just verified on Chrome Canary 141.0.7354.0, and the bug no longer reproduces. It appears to be fixed.

### ch...@google.com (2025-08-13)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### pn...@google.com (2025-08-13)

> Why does your merge fit within the merge criteria for these milestones?

Security issue fix

> What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/6832030>

> Have the changes been released and tested on canary?

Yes

> Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

> If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

n/a

### ch...@gmail.com (2025-08-14)

Should this be marked as fixed now?

### pn...@google.com (2025-08-14)

I'm going to leave it open until the merge is addressed if you don't mind

### ch...@gmail.com (2025-08-14)

Thanks for the update! 

As far as I know, this should be marked as Fixed and the CL patch link added to the "Fixed by" label. The merge will follow after that.

### am...@chromium.org (2025-08-15)

merge for <https://crrev.com/c/6832030> approved; please merge to M140 beta / branch 7339 at your earliest convenience

### dx...@google.com (2025-08-15)

Project: chromium/src  

Branch:  refs/branch-heads/7339  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/6854344>

[mobar] Handle mid-animation replacement

---


Expand for full commit details
```
     
    Although not explicitly documented, it's possible for a new IME 
    animation to start without the old one finishing, e.g. a "false start" 
    start-showing-then-hide. If we don't update to reflect the state of the 
    new animation we mistakenly perform updates as if the old one is still 
    running which can cause us to e.g. miscalculate the translation. 
     
    Merge-Approval-Bypass=Merge approved in parent bug without separate merge request bug 
    (cherry picked from commit b583fe9162bd751d0c6bd065b4e7da0c76d66c6a) 
     
    Bug: 437147699 
    Change-Id: I56b22c121848acb61410d33b42e82b8c0b05cd1a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6832030 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1500279} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6854344 
    Cr-Commit-Position: refs/branch-heads/7339@{#672} 
    Cr-Branched-From: 27be8b77710f4405fdfeb4ee946fcabb0f6c92b2-refs/heads/main@{#1496484}

```

---

Files:

- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarController.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarControllerTest.java`

---

Hash: [b3cdbd5d7f6b3a8ad81e09f5fb69c34fb33c76a8](https://chromiumdash.appspot.com/commit/b3cdbd5d7f6b3a8ad81e09f5fb69c34fb33c76a8)  

Date: Fri Aug 15 20:05:00 2025


---

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of moderate impact security UI spoof

It's important to not that future reports related to this specific UI surface, unless demonstrated to be highly and convincingly spoofable with little to no user interaction, may not be eligible for as high of rewards. Given that this report resulted in hardening of a new UI surface, we feel this report warrants this reward.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-11-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of moderate impact security UI spoof
> 
> It's important to not that future reports related to this specific UI surface, unless demonstrated to be highly and convincingly spoofable with little to no user interaction, may not be eligible for as high of rewards. Given that this report resulted in hardening of a new UI surface, we feel this report warrants this reward.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/437147699)*
