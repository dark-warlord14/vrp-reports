# Security: Fullscreen Confusion Attack in Chrome with Mail Application

| Field | Value |
|-------|-------|
| **Issue ID** | [40063041](https://issues.chromium.org/issues/40063041) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Fullscreen |
| **Platforms** | Windows |
| **Reporter** | fa...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2023-02-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome usually blocks external interactions outside the browser when launching with fullscreen. However, this proof of concept (POC) allows an attacker to deceive the user by launching the mail application through a 'mailto' URI and fullscreen simultaneously. The fullscreen loads behind the default mail application, and a fullscreen notification appears on top of the mail application instead, which can confuse the victim and lure them to a spoofed page.

**VERSION**  

Chrome Version: 110.0.5481.78 (Official Build) (64-bit) (cohort: Stable Installs & Version Pins)

**REPRODUCTION CASE**

1. Download the attached files
2. Open poc.html in a Chrome browser to Begin testing.

When the victim clicks the button, the above proof-of-concept triggers the launch of both default mail application and fullscreen simultaneously, with the mail application positioned between the fullscreen notification and the Chrome browser, thereby confusing/misinforming the user about the notification origin.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 4.4 KB)
- [top.png](attachments/top.png) (image/png, 26.8 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 3.2 MB)

## Timeline

### [Deleted User] (2023-02-12)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-02-13)

Also, it is important to note that the Esc notification for full-screen mode is displayed over the mail application. If the user attempts to escape, the handling of the escape occurs within the mail application itself (A prompt to discard the draft is displayed when Esc).

### ma...@google.com (2023-02-13)

Can repro on Windows. This requires the user to have a non-Chrome default app for email set, and for that mail app to launch in fullscreen. (Otherwise you just see the mail app window on top of Chrome fullscreen, which is a bit less convincing to me.)

avi@, since this is a fullscreen UI spoof, can you take a look at this one?

[Monorail components: Blink>Fullscreen]

### [Deleted User] (2023-02-13)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-02-14)

I have also tried on Ubuntu Linux, in the same manner as Windows, where the Thunderbird mail application opens in full-screen mode, obscuring the Chrome browser if the user previously opened the application in full-screen.

### [Deleted User] (2023-02-14)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2023-04-03)

Friendly ping 

### fa...@gmail.com (2023-04-06)

Hello, this vulnerability affects both Windows and Linux. Even though the fullscreen notification is displayed above the mail application, when the user presses the "Escape" key, it only triggers the "Escape" command for the mail application and when the user returns to the Chrome window, the attacker will display the spoofed window.

### fa...@gmail.com (2023-05-02)

Friendly ping :)

### fa...@gmail.com (2023-05-12)

[Comment Deleted]

### fa...@gmail.com (2023-05-25)

Hello team, this bug has been around for a few months now, and I feel that it is not receiving the attention it deserves. The severity should be considered for an increase because the mail application is overlapped with notifications, pressing the "Esc" key does not work, and when the user files mail, they are left with a fully spoofed website.

### fa...@gmail.com (2023-06-08)

It has been more than 3 months since I reported this bug, and there has been no discussion or update regarding this issue. Team, could you please provide any updates on this matter?

### ar...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-06-21)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-06-22)

Owner, it's been months since I reported this issue, and more people are discovering this vulnerability. Can you please fix this or provide an update on the progress? If you're busy or not the right owner for this issue, could you please transfer it to a developer who is able to fix it? Thank you.

### th...@chromium.org (2023-07-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-24)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-10-29)

Friendly ping

### fa...@gmail.com (2023-12-04)

[Comment Deleted]

### is...@google.com (2023-12-04)

This issue was migrated from crbug.com/chromium/1415138?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1453580]
[Monorail components added to Component Tags custom field.]

### fa...@gmail.com (2024-02-20)

Friendly ping.

### am...@chromium.org (2024-12-09)

I believe this issue should be resolved by <https://crrev.com/c/5560391>.
Please let me know if that is not the case.

### pe...@google.com (2024-12-09)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2024-12-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI spoof / exploit mitigation bypass 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-12)

Thank you for your efforts and reporting this issue to us, Shaheen!

### ch...@google.com (2025-03-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063041)*
