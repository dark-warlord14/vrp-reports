# Android APK Spoof in Chrome Download Menu 

| Field | Value |
|-------|-------|
| **Issue ID** | [345688415](https://issues.chromium.org/issues/345688415) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | pu...@gmail.com |
| **Assignee** | sh...@chromium.org |
| **Created** | 2024-06-07 |
| **Bounty** | Confirmed (amount unknown) |

## Description

VULNERABILITY DETAILS

Android APK Spoof in Chrome Download Menu 

the APK file extension is not visible in Chrome Download Menu Due to Long Extension  

`imagefilepuf.puf.puf.puf.jpg.jpg.jpg.jpg.jpg.jpg.jpg.jpg.jpg.jpg.jpg`

Attacker Can Change to any extension jpg,png,mp4,pdf,doc etc... due to long extension this will hide the real APK extension file in Android
 
VERSION
Chrome Version: [125.0.6422.14] + [beta]
Operating System: [Android 14]

REPRODUCTION CASE
1. Upload POC File into your Local Server
2. Open Page and Click On [ open ] Button 
3. the apk file will download 
4. Now goto [ : ] In Chrome
5. Tap On Downloads 
6. You will See apk File Spoofed `imagefilepuf.puf.puf.puf.jpg`

CREDIT INFORMATION
Reporter credit: [Puf]

## Attachments

- [PUFSS.jpg](attachments/PUFSS.jpg) (image/jpeg, 105.5 KB)
- [PUF File Explorer.jpg](attachments/PUF File Explorer.jpg) (image/jpeg, 129.8 KB)
- [ChromeMenuAPK.jpg](attachments/ChromeMenuAPK.jpg) (image/jpeg, 89.7 KB)
- [POC.html](attachments/POC.html) (text/html, 45.9 KB)
- [Longname POC.html](attachments/Longname POC.html) (text/html, 45.8 KB)
- [Reprdoce Video.mp4](attachments/Reprdoce Video.mp4) (video/mp4, 561.5 KB)
- [POC.html](attachments/POC.html) (text/html, 47.2 KB)
- [Screenshot.jpg](attachments/Screenshot.jpg) (image/jpeg, 40.9 KB)
- [Latest Screenshot .jpg](attachments/Latest Screenshot .jpg) (image/jpeg, 18.7 KB)

## Timeline

### pu...@gmail.com (2024-06-07)

Operating System: [Android 14]

Device Name: [Vivo V27]

Chrome Version: [126.0.6478.26]

### pu...@gmail.com (2024-06-07)

Ref: <https://issues.chromium.org/issues/40918159>

### li...@chromium.org (2024-06-07)

Hello,

Your example PoC is actually a jpeg file, not an apk, so the file explorer is properly showing a jpeg extension. Do you have an example with an APK?

### pu...@gmail.com (2024-06-07)

Sorry! Forgot to Attach POC

I Have Attached POC file here

REPRODUCTION CASE

1. Upload POC File into your Local Server
2. Open Page and Click On [ open ] Button
3. the apk file will download
4. Now goto [ : ] In Chrome
5. Tap On Downloads
6. You will See apk File Spoofed `imagefilepuf.puf.puf.puf.jpg`

### pe...@google.com (2024-06-07)

Thank you for providing more feedback. Adding the requester to the CC list.

### li...@chromium.org (2024-06-07)

Adding some relevant folks to help triage.
So I do now see that this file downloads and you can't see the .apk extension at the end. However I get a warning about an unsafe application when trying to install the downloaded APK, and that to me feels like a pretty decent mitigation. I'd like some other folks to weigh in on whether we should do more, though.

### pu...@gmail.com (2024-06-08)

<https://issues.chromium.org/issues/40918159>

This Issue is Still Reproducing in Latest Version of Chrome Bata
file download with long name cannot show the APK extension

I have tried to reproduce in Chromium Based Browser, and this Issue is not reproducing in Edge browser I can see APK extension in Download Menu in Edge Browser

REPRODUCTION CASE

- 1.Upload POC File into your Local Server
- 2.Open Page and Click On [ open ] Button
- 3.the apk file will download
- 4.Now goto [ : ] In Chrome
- 5.Tap On Downloads

You will See File `imagefilepuf................` No APK Extension is visible

### pe...@google.com (2024-06-10)

The NextAction date has arrived: 2024-06-10
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### li...@chromium.org (2024-06-11)

Hmm I do think this is low sev similar to [crbug.com/40918159](https://crbug.com/40918159) so I marked it appropriately. Assigning to owner of the prior bug to take a look.

### pu...@gmail.com (2024-06-28)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### pu...@gmail.com (2024-07-11)

Hello, any updates here?

### pu...@gmail.com (2024-10-27)

deleted

### pu...@gmail.com (2024-11-04)

this vulnerability is fixed! in latest Android Chrome Version 131.0.6778.14 (Official Build) Beta (64-bit)

Please kindly Verify and Change Status to fixed

Thank you!

### pu...@gmail.com (2024-11-05)

hello, any updates regarding status?

Thanks

### pu...@gmail.com (2024-11-12)

Friendly ping

### pu...@gmail.com (2024-11-21)

deleted

### pu...@gmail.com (2024-11-23)

Improved Report

- When a user clicks on attacker's page it is possible to Spoof APK Extension & Hide the Dangerous APK Extension in Chrome Download Page Malicious file can be spoofed with legit extension
  due to this Vulnerability, the user is not capable to know exact file information in Chrome Download Page,
- Long File Name can cause the real extension to hide APK File and leads to spoof

Note: This issue was not fixed in <https://issues.chromium.org/issues/40918159>

- Attached a video reproducing the attack I have also attached the files used in the PoC

REPRODUCTION CASE

1.Upload POC File into your Local Server

2.Open Page and Click On [ open ] Button

3.the apk file will download

4.Now goto [ : ] In Chrome

5.Tap On Downloads

Result You will See File imagefilepuf..@@@@@@@@@@@ Without APK Extension

### sh...@chromium.org (2024-11-28)

Marking as fixed based on comment 14

### pu...@gmail.com (2024-11-28)

The first poc I have submitted I have verified it is fixed

I have retested updated and attached new poc

due to long length of filename, it does not show the real APK extension which leads to Spoof

I have to submit new report. regarding this?

Thank you :)

### am...@chromium.org (2024-12-04)

Thank you for the additional information. Reopening this issue as it does not appear to be resolved.

### pu...@gmail.com (2024-12-04)

Thank you [am...@chromium.org](mailto:am...@chromium.org) I thought I have to submit a new report

Can you please assign someone to verify this issue <https://issues.chromium.org/issues/40076292> it has been fixed on oct, but the status has not been changed

Thank you so much. :)

### am...@google.com (2024-12-05)

re c#22, no new report needed here. This one has been re-opened and is already triaged and assigned.

WRT to the other question, please refrain from questions about other, unrelated issues. It's confusing and disruptive to the thread.
Comments should be used only for information and questions related to this bug toward the investigation and resolution of the issue.
If you have questions about the status of another issue, please reach out to security-vrp@.
Thank you.

### pu...@gmail.com (2024-12-05)

Sorry for the confusion caused here

Thank you so much for your time.

### pu...@gmail.com (2025-03-18)

Would you kindly give me an update?

Thank you!

### pu...@gmail.com (2025-08-26)

I've successfully verified the fix on my Android and confirmed that the issue is resolved.

Verified On Chrome Canary 141.0.7375.0

Verified on Chrome Beta 140.0.7339.25

Verified On Chrome 139.0.7258.143

Thanks,

### aj...@chromium.org (2025-09-30)

Marking Fixed based on earlier comments.

### sp...@google.com (2025-10-21)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

This is mitigated by the APK installation prompt

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### pu...@gmail.com (2025-10-22)

similar Vulnerability <https://issues.chromium.org/issues/40918159>

Thank you very much for the thorough and prompt review of my submission, and for providing a clear rationale for your decision. I understand and appreciate the panel's assessment that the immediate security impact is mitigated by the standard Android APK installation prompt, which requires explicit user action.

I am requesting a reconsideration of this decision based on established reward precedent. In past assessment periods, the panel has rewarded submissions for this specific class of vulnerability, even though those issues were mitigated by the exact same user confirmation prompt.

I kindly request the panel to :

Re-evaluate this submission against the clear historical record of similar, compensated reports.

### ch...@google.com (2026-01-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> This is mitigated by the APK installation prompt
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/345688415)*
