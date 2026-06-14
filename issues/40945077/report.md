# Security: Fullscreen Quickly Hide "Press and hold Esc to exit fullscreen and see download" Notification

| Field | Value |
|-------|-------|
| **Issue ID** | [40945077](https://issues.chromium.org/issues/40945077) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Linux, Windows |
| **Reporter** | pu...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2023-11-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

In Fullscreen Mode We Can Hide "Press and hold Esc to exit Fullscreen and see download" Using navigator.keyboard.lock & Timeout

First the Page Enters into Fullscreen Mode & Then File Start Downloading Immediately navigator.keyboard.lock Activates. Due to "Esc" Lock Quickly Hides "Press and hold Esc to exit Fullscreen and see download". Notification

**VERSION**  

120.0.6099.28 (Official Build) beta (64-bit)  

Operating System: [Windows 10 (64-bit)]

**REPRODUCTION CASE**

1. Open PufIndex.html
2. Click On [ Click Me! ] Button
3. Done

**CREDIT INFORMATION**  

Reporter credit: [Puf]

## Attachments

- [Puf POC.mp4](attachments/Puf POC.mp4) (video/mp4, 125.5 KB)
- [PufIndex.html](attachments/PufIndex.html) (text/plain, 819 B)
- [New Update POC.mp4](attachments/New Update POC.mp4) (video/mp4, 169.9 KB)
- [Index.html](attachments/Index.html) (text/plain, 874 B)
- [Screenshot.PNG](attachments/Screenshot.PNG) (image/png, 5.2 KB)
- [Repro canary .mp4](attachments/Repro canary .mp4) (video/mp4, 85.6 KB)
- [Repro Beta.mp4](attachments/Repro Beta.mp4) (video/mp4, 140.1 KB)

## Timeline

### pu...@gmail.com (2023-11-22)

There is One More Issue Here on Exit Fullscreen it Does not Show Download List Panel.

### [Deleted User] (2023-11-22)

[Empty comment from Monorail migration]

### pm...@chromium.org (2023-11-22)

reproduced in stable - linux 119

There's a notification quickly displayed and hidden by the default "press est to exit full screen". I reckon the impact for the users is fairly low to non-existent.



[Monorail components: UI>Browser>FullScreen]

### [Deleted User] (2023-11-22)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-11-22)

Here it is a New Update Code & POC Please Check it out.

### [Deleted User] (2023-11-22)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-12-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-12-18)

CC'ing the reporter of bug https://crbug.com/chromium/1512418.

### is...@google.com (2023-12-18)

This issue was migrated from crbug.com/chromium/1504537?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1512418]
[Monorail components added to Component Tags custom field.]

### pu...@gmail.com (2025-01-19)

This Issue has been Fixed I Have Verified in Latest Chrome Version 134.0.6961.0

### pu...@gmail.com (2025-01-22)

This Issue Has Been Fixed
Attached the Screenshot
Thanks

### am...@chromium.org (2025-01-22)

Bugs closed as fixed require the entry of a gerrit CL in the `fixed by code changes` field.
Additionally your screenshot (in c#13) is only that of a fullscreen notification, not proof it has been resolved in relation to this root cause.
A fix for a similar issue is in Mac specific code so it cannot be the fix for this issue.
We'll need to identify the change that resulted in the resolution of this issue as a precondition to closing it.

### pu...@gmail.com (2025-01-22)

Thank you for quick response and explaining I appreciate it

Before posting comment about fix, I always reproduce many times in All the Versions in Chrome from Beta to canary to find out behaviour changes of the Vulnerability

When I reported this Vulnerability Fullscreen Download Message/Notification `Press and hold Esc to exit Fullscreen and see download` Does not show the Message to Users as you can see in (C #1)

The Download Message/notification hides quickly due to navigator.keyboard.lock Message/Notification interference and the user does not know the file is getting downloaded

While I was trying to reproduce this Issue in canary and Beta

- In Latest Version Canary 134.0.6973.0 the Download Message/notification is Showing me ☑ when I have tried to Download the file in Fullscreen mode I get the notification `file is Downloaded` I Have Attached reproduce Video on this
- In Beta Version the Fullscreen Download Message/Notification `Press and hold Esc to exit Fullscreen and see download` is not showing me and the file is Downloading without knowing User I Have Attached reproduce Video too

Thank you and Sorry for Attaching the screenshot

### pu...@gmail.com (2025-04-24)

Hi amy,

This Vulnerability fixed though this bug <https://issues.chromium.org/issues/363640098>

<https://chromium-review.googlesource.com/c/chromium/src/+/6161794>

### am...@chromium.org (2025-04-24)

This is an issue with very low potential for user harm, in that it strictly hides the filename being downloaded from the user and obfuscates a file is being downloaded, so I have converted it to type=bug, same as in [issue 363640098](https://issues.chromium.org/issues/363640098).

### sp...@google.com (2025-05-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
While we do not consider the potential exploitability or user impact to be such that this can be considered a security issue, we were able to make a security-beneficial change based on this report (and issue 363640098, the bug the fix is linked to), therefore we are issuing as small thank you reward.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945077)*
