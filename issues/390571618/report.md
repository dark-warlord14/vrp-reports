# Misuse of Permission Dialog Dismiss to Deceive Users About Fullscreen Status

| Field | Value |
|-------|-------|
| **Issue ID** | [390571618](https://issues.chromium.org/issues/390571618) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Mac |
| **Chrome Version** | 132.0.6834.84 |
| **Reporter** | sy...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2025-01-18 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Victim visit: <https://syarifmsajjad.github.io/test-spoofing/fs-escape.html> and click to enter fullscreen
2. Press "Esc". "Insert omnibox here" text should appear. An attacker can use this opportunity to trick the user into thinking that they have exited fullscreen and draw a fake omnibox once the user pressed "Esc"

# Problem Description

In Chrome, the permission dialog can be closed using the “Esc” key, which also serves to exit fullscreen mode. When the permission dialog appears after a website takes the user into fullscreen mode, if the user presses “Esc” afterwards, the input will be redirected to the permission dialog instead of exiting fullscreen. This allows attackers to insert a fake omnibox and trick users into thinking that they have exited fullscreen mode. With this fake omnibox, the attacker can perform URL spoofing of other websites.

Expected result
Pressing the “Esc” key while in fullscreen mode with a permission dialog open should exit fullscreen mode without redirecting input to the permission dialog. The browser should prioritize exiting fullscreen mode to ensure consistent and secure user experience, preventing potential UI spoofing vulnerabilities.

Actual result
When the victim presses the “Esc” key while the permission dialog is displayed in fullscreen mode, instead of exiting fullscreen, the input is redirected to the permission dialog. This allows the attacker to insert a fake omnibox, tricking the user into believing they have exited fullscreen mode.

# Summary

Misuse of Permission Dialog Dismiss to Deceive Users About Fullscreen Status

# Custom Questions

#### Type of crash:

1

#### Crash state:

1

#### Reporter credit:

syrf

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [Screen Recording 2025-01-18 at 10.35.42.mov](attachments/Screen Recording 2025-01-18 at 10.35.42.mov) (video/quicktime, 2.5 MB)
- [fs-c.html](attachments/fs-c.html) (text/html, 29.4 KB)

## Timeline

### ad...@google.com (2025-01-18)

Please attach all the files required to reproduce this.

### sy...@gmail.com (2025-01-18)

Ok, please check my attachment

### ad...@google.com (2025-01-19)

Thanks for the report - I've reproduced it just as you say, on Mac on 132.0.6834.83.

I agree that, in principle, the Esc keypress should be directed to the full screen code rather than closing the permission prompt.

However, I can't see an opportunity for an attacker to exploit this. As our [severity guidelines say](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md), "Bugs that require implausible interaction, interactions a user would not realistically be convinced to perform, will generally be downgraded to a functional bug and not considered a security bug.".

I don't see a way that an attacker could rely on a user pressing Esc at this point, so I'm going to change this to a functional bug.

### ad...@google.com (2025-01-19)

Balazs, as full screen isn't owned, I'm sending this your way for consideration.

### sy...@gmail.com (2025-01-19)

Hi team, I honestly disagree with you. This is not a “nonsensical interaction” because when the victim clicks on the page he/she will automatically go to fullscreen mode and naturally the victim will press the Esc key to exit fullscreen mode. But when pressing Esc the victim does not actually exit fullscreen mode. I think this is a similar case with <https://issues.chromium.org/issues/40071026>.

### en...@chromium.org (2025-01-22)

syarifsajjad07@, could you please elaborate on how you see this issue as different from [Issue 40071026](https://issues.chromium.org/issues/40071026)? The POC you included seems to be virtually the same. Did Chromium's implementation regress here between M129 and M132?

### sy...@gmail.com (2025-01-22)

The simple fact is that the problem with <https://issues.chromium.org/issues/40071026> is that it can be reproduced in the latest version.

### en...@chromium.org (2025-01-22)

With Chrome version 132.0.6834.83 and macOS version 14.7.2, I am able to reproduce this on every odd-numbered try (1st, 3rd, ...), but not on every even-numbered try (2nd, 4th...). I wonder if there is no regression, but we closed the previous bug due to having the misfortune of verifying it in the latter state?

### sy...@gmail.com (2025-01-22)

Thanks for the feedback. I was also able to reproduce this behavior on Version 132.0.6834.84 (Official Build) on macOS 15.2. The pattern remains consistent: the bug appears on odd-numbered attempts (1st, 3rd, ...) but not on even-numbered attempts (2nd, 4th, ...).

Regarding the possibility of regression, this pattern may indicate that certain internal conditions in Chrome affect whether the bug occurs or not. If the bug was previously verified only under circumstances equivalent to even attempts (when the bug did not appear), it is possible that the regression had actually already occurred but was not detected.

### sy...@gmail.com (2025-01-25)

Hi team any update?

### sy...@gmail.com (2025-02-05)

Hi team any update? can you move this report to `Vulnerability` issue?

### en...@chromium.org (2025-02-05)

Apologies for the delay, I have upped the priority/severity to P2/S3 (low severity) and marked it as a Vulnerability. Also reached out to macOS experts to form a hypothesis as to what is keeping state here. Alternatively, syarifsajjad07@, maybe you have reviewed the relevant code and have a patch ready at hand?

### en...@chromium.org (2025-02-05)

Routing to Leonard to take a look, as this might be another manifestation of the fullscreen state desync issue he is already looking into.

### lg...@chromium.org (2025-02-05)

Poked around a bit and it doesn't seem to be related to fullscreen state. I think maybe focus related? Handing off to kerenzhu@ since he has a better grasp of how focus routing is supposed to work and has context from [bug 40071026](https://issues.chromium.org/issues/40071026)

### en...@chromium.org (2025-02-11)

Keren, are there any focus management edge cases that might explain this?

### ke...@chromium.org (2025-02-12)

Yes, in general keyboard event goes to the focused widget. In this case, that's the permission bubble.

I actually think that **any permission request should force exit of content fullscreen**. This is already what would happen if the page opens a screen sharing dialog. In content fullscreen, there is no top-chrome UI and therefore any dialog or bubble can be easily spoofed.

@security, what do you think of the idea of exiting content fullscreen when showing permission prompt? Note that this does not affect user-initiated fullscreen.

### sy...@gmail.com (2025-02-20)

Hi team any update?

### sy...@gmail.com (2025-02-28)

Hi team any update?

### lg...@chromium.org (2025-02-28)

ellyjones@ can you weigh in on c#17?

### el...@chromium.org (2025-03-03)

I personally would be totally fine with that. In general I ask avi@ this kind of stuff :)

### ke...@chromium.org (2025-03-03)

Avi, let me know if my proposal in [comment #17](https://issues.chromium.org/issues/390571618#comment17) makes sense to you. If so, I can implement it.

### av...@chromium.org (2025-03-03)

SGTM.

In general, any appearance of dialogs is meant to kick you out of fullscreen. It would make sense to do so for bubbles too, especially permission requests.

### sy...@gmail.com (2025-03-25)

Hi team any update?

### sy...@gmail.com (2025-04-05)

Hi team any update?

### sy...@gmail.com (2025-04-13)

Hi team any update?

### sy...@gmail.com (2025-04-17)

Hi team any update?

### sy...@gmail.com (2025-04-21)

Hi team any update?

### sy...@gmail.com (2025-05-02)

Hi team any update?

### sy...@gmail.com (2025-05-06)

Hi team any update?

### sy...@gmail.com (2025-05-16)

Any apdet sir?

### sy...@gmail.com (2025-05-26)

eni apdet sir?

### sy...@gmail.com (2025-05-31)

Hi team any update?

### sy...@gmail.com (2025-06-30)

Hi team any update?

### sy...@gmail.com (2025-07-03)

Hi team any update?

### sy...@gmail.com (2025-07-04)

Hi team any update?

### sy...@gmail.com (2025-07-19)

Hi team any update?

### sy...@gmail.com (2025-07-22)

Hi team any update? Why i don't get any response???

### sy...@gmail.com (2025-08-29)

Bang? ada update nggak bang?
Perlu bounty, belom makan ni :)

### sy...@gmail.com (2025-09-06)

Any update?

### dx...@google.com (2025-09-08)

Project: chromium/src  

Branch:  main  

Author:  Keren Zhu [kerenzhu@chromium.org](mailto:kerenzhu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6921231>

Exit content fullscreen when a permission prompt bubble is shown.

---


Expand for full commit details
```
     
    In content fullscreen there is almost no browser UI. Showing a 
    permission prompt bubble is therefore prone to spoofing attacks. This CL 
    exits the content fullscreen on showing a permission bubble. It also 
    prevents re-entering content fullscreen while the permission prompt 
    bubble is visible. 
     
    Fixed: 390571618 
    Change-Id: I87c1a58ebd68a39d0beda8a5cf056de89f92d679 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6921231 
    Reviewed-by: Tom Lukaszewicz <tluk@chromium.org> 
    Commit-Queue: Keren Zhu <kerenzhu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1512541}

```

---

Files:

- M `chrome/browser/ui/exclusive_access/fullscreen_controller_interactive_browsertest.cc`
- M `chrome/browser/ui/views/permissions/permission_prompt_bubble.cc`
- M `chrome/browser/ui/views/permissions/permission_prompt_bubble.h`

---

Hash: [5eb4b823dced000b8d61678f1c885f38c2dc4fbe](https://chromiumdash.appspot.com/commit/5eb4b823dced000b8d61678f1c885f38c2dc4fbe)  

Date: Mon Sep 8 17:57:48 2025


---

### sy...@gmail.com (2025-09-09)

How about bounty?

### sy...@gmail.com (2025-09-18)

Any update?

### sp...@google.com (2025-09-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline / Lower Impact Security UI spoofing


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sy...@gmail.com (2025-09-20)

Thanks for bounty :')

### ch...@google.com (2025-12-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline / Lower Impact Security UI spoofing

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/390571618)*
