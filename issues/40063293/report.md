# Security: Chrome Vulnerability Leaves Android One UI Users at Risk of Spoofing Attacks

| Field | Value |
|-------|-------|
| **Issue ID** | [40063293](https://issues.chromium.org/issues/40063293) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Fullscreen |
| **Platforms** | Android |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2023-02-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A vulnerability has been discovered in Chrome that affects users of the One UI/Android operating system. Due to certain user settings, the Fullscreen notifications in Chrome are completely hidden from the user. This can leave victims vulnerable to spoofing attacks on Android Chrome users with the following settings.

Settings -> Display -> Camera cutout -> Chrome -> Hide camera cutout  

Settings -> Display -> Navigation bar -> Gesture hint Disabled

Video Demonstration: <https://youtu.be/a48rEInPYBo> (YouTube Unlisted)

**VERSION**  

Chrome Version: Chrome Dev 112.0.5610.0  

Operating System: One UI 5.1 / Android version 13  

Device: Galaxy S23

**REPRODUCTION CASE**  

Settings -> Display -> Camera cutout -> Chrome -> Hide camera cutout  

Settings -> Display -> Navigation bar -> Gesture hint Disabled

1. Download the attached file into a folder
2. Start a Python server on the same folder by running the command `python -m http.server 8080`.
3. Open the Android Chrome browser and navigate to the server at http://{YOUR-SERVER-IP}:8080/poc.html to Begin testing.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.6 KB)
- [spoof.png](attachments/spoof.png) (image/png, 100.1 KB)
- [testpoc.mp4](attachments/testpoc.mp4) (video/mp4, 1.0 MB)

## Timeline

### fa...@gmail.com (2023-02-28)

Similar vulnerability for reference: crbug.com/1259492

### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-02-28)

Similarly, this vulnerability affects the Android Edge Browser, while Android Firefox is unaffected.

### es...@chromium.org (2023-03-01)

I don't have a device or emulator available to test this.

Reporter, would you be able to check if this reproduces on Chrome Stable (110)?

Triaging as Low severity because of the specific settings that the user needs to change.

[Monorail components: Blink>Fullscreen]

### es...@chromium.org (2023-03-01)

(To clarify, a One UI device specifically is needed to reproduce this, AFAIU.)

### fa...@gmail.com (2023-03-01)

I have tested the issue in Chrome Stable (110) and was able to reproduce it.

Application version: Chrome 110.0.5481.154

### [Deleted User] (2023-03-01)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2023-03-01)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-01)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-03-01)

Based on my testing in the Microsoft Edge browser, it appears that users only need to change one setting while leaving the other on default (auto) in order to be vulnerable. If a victim chooses to use this setting alone, which is usually a preferred setting to enable a Fullscreen experience on such devices, it could easily impact most users who use this browser.

Setting:
Settings -> Display -> Navigation bar -> Gesture hint Disabled

Application version:
Edge 110.0.1587.54


### [Deleted User] (2023-03-01)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2023-03-17)

Since Microsoft Edge Chromium is vulnerable with only one setting, which is usually preferred by most users, may I request that the severity level be increased if possible?

### fa...@gmail.com (2023-04-03)

Friendly ping

### an...@chromium.org (2023-04-17)

Hello, checking on this bug. What could be done to help move this bug forward? Thanks.

### fa...@gmail.com (2023-05-02)

Friendly ping :)

### fa...@gmail.com (2023-06-08)

It has been more than 3 months since I reported this bug, and there has been no discussion or update regarding this issue. Team, could you please provide any updates on this matter?

### am...@chromium.org (2023-07-13)

This issue was not assigned to an owner, assigning to jinsukkim@ and cc'ing others involved with fullscreen work on Android 

### tw...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### ji...@chromium.org (2023-08-02)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-10-29)

Friendly ping

### tw...@chromium.org (2023-10-31)

This issue is blocked on longer term discussions around a larger rework to Chrome's fullscreen notifications, tracked in https://crbug.com/chromium/1469626.

### is...@google.com (2023-10-31)

This issue was migrated from crbug.com/chromium/1420249?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1469626]
[Monorail components added to Component Tags custom field.]

### fa...@gmail.com (2024-02-20)

Friendly ping.

### ji...@chromium.org (2024-11-19)

b/40068581 -> jinsukkim@google.com

### bu...@google.com (2024-11-19)

Sorry, Bugjuggler can only be used by users in the @google.com domain.

### ji...@google.com (2024-11-19)

Bugjuggler: b/40068581 -> jinsukkim@google.com

### bu...@google.com (2024-11-19)

Hi. I've received your bug and will wait for b/40068581 to be resolved and then assign the bug to jinsukkim.

### fa...@gmail.com (2025-01-14)

Hi, it seems this issue is fixed — fullscreen toasts now properly show with the above settings that are currently default on the latest Samsung devices.

### fa...@gmail.com (2025-04-30)

Tested on:
Chrome 135 on the latest Android version.

### aj...@chromium.org (2025-06-23)

Hi Fazim - it could be helpful to bisect to a fix.

Marking fixed but we do not know which CL fixed this.

### bu...@google.com (2025-06-23)

Bug is closed; my job here is done.

### ch...@google.com (2025-06-23)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### fa...@gmail.com (2025-06-25)

Hi, I'm not familiar with bisecting Chrome for Android, but I have providing a screenrecording proving that this is fixed in the latest Chrome version.

### sp...@google.com (2025-07-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-10-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI spoof

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063293)*
