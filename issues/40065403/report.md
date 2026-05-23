# Security: Tapjacking Android Chrome APK Warning

| Field | Value |
|-------|-------|
| **Issue ID** | [40065403](https://issues.chromium.org/issues/40065403) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | fa...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2023-06-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The site requires permission from the user to download APK files, but an attacker can lure victims into unknowingly allowing the download of a file using an engaging game via the tapjacking method.

Usually, Chrome prevents Tapjacking in permission dialogues by require two taps to grant access when spoofed (Possible Fix), but this safeguard is not implemented in Android Chrome's untrusted apk download permission.

**VERSION**  

Chrome Version: Chrome Dev 116.0.5803.0  

Operating System: Android 13

**REPRODUCTION CASE**

1. Host the poc.html file on a web server.
2. Access the web server using the Chrome browser on Android device.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.9 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 2.8 MB)
- [poc.html](attachments/poc.html) (text/plain, 2.4 KB)
- [test.apk](attachments/test.apk) (application/octet-stream, 1.9 KB)
- exp.mp4 (video/mp4, 5.3 MB)
- [chrome permission.mp4](attachments/chrome permission.mp4) (video/mp4, 909.8 KB)

## Timeline

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-06-06)

For further exploitation, the "open" option after downloading is also vulnerable to Tapjacking. Therefore, this can be further exploited to open the app installer. Safeguarding dialogues by requiring two taps to allow download may solve both of this issue.

### fa...@gmail.com (2023-06-06)

Above method, I have used the Google Assistant intent to hide the downloading notification, which displays 'detail' instead of 'open'.

### aj...@google.com (2023-06-06)

Low as this needs several things to happen to confuse a user.

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-06-06)

I understand the second exploitation requires several conditions to be met. However, staying to the original report, considering alone the tapjacking of the download warning as a significant vulnerability in itself should be deemed impactful, similar to https://crbug.com/1301180 

### qi...@chromium.org (2023-06-06)

Requiring user to have 2 taps will have a negative impact on user experience. Given the set up needed to bait the user, not sure if we need a fix here.  Probably someone with UX experience would need to comment on this.

### fa...@gmail.com (2023-06-06)

A different solution would be to introduce a delay after taps between the DOM and the download button. On desktop, a similar safeguard is implemented to protect against Clickjacking, but it is missing on Android.

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-06-07)

The Chrome permission dialogue has protection against tapjacking, whereas the download warning lacks this safeguard against tapjacking.

### [Deleted User] (2023-06-07)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### tw...@chromium.org (2023-07-11)

I think we have multiples of these and should choose one as the canonical bug and mark the rest as duplicates

### am...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-11)

This is the first report of the three reports of this issue that I am aware of at this time, and should be considered the canonical one. So, I have merged the other issue into this one. 

### fa...@gmail.com (2023-07-12)

Hi, thanks for reviewing this issue. In the second comment (#2), the PoC demonstrates tapjacking on both harmful file dialogue and open file dialogues. Both of these dialogues on Android Chrome are vulnerable. This can be chained (as demonstrated in https://crbug.com/chromium/1451726#c2 proof-of-concept video) or used to tapjack downloads alone for opening other extension. I hope the new fix includes security measures for both of these dialogues. Thanks.

### dt...@chromium.org (2023-07-20)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-10-29)

Friendly ping

### fa...@gmail.com (2024-01-24)

Hello, Friendly ping

### is...@google.com (2024-01-24)

This issue was migrated from crbug.com/chromium/1451726?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1461991, crbug.com/chromium/1464262]
[Monorail components added to Component Tags custom field.]

### fa...@gmail.com (2024-02-05)

Hi, it seems that there's been no progress on this issue for a long time. Is there any way to make changes to move the issue processing forward for a fix?

### fa...@gmail.com (2024-02-05)

I would suggest a possible fix would be to implement clickjacking protection similar to other UI prompts on Chromium. I believe this is a straightforward fix.

### aj...@google.com (2024-02-07)

The report I duped ([issue 41497269](https://issues.chromium.org/issues/41497269)) in covers both:

1. Tapjacking Download Malicious File Popup
2. Tapjacking Download Again Popup

I have a feeling these are all the same root cause.

### fa...@gmail.com (2024-02-20)

Friendly ping.

### fa...@gmail.com (2024-03-05)

Friendly ping.

### fa...@gmail.com (2024-03-19)

Friendly ping.

### la...@chromium.org (2024-03-19)

Hi [qimmin@google.com](mailto:qimmin@google.com), could you take a look at this issue? We can add [UiUtils.PROMPT\_INPUT\_PROTECTION\_SHORT\_DELAY\_MS](https://source.chromium.org/chromium/chromium/src/+/main:ui/android/java/src/org/chromium/ui/UiUtils.java;drc=fdf78013a9f355f91da2c4ac8bf78932886ce444;l=67) for download dialogs in this case.

### fa...@gmail.com (2024-04-02)

Hi, it's been a long time. Can we update on this issue?

### fa...@gmail.com (2024-04-12)

Friendly ping.

### ap...@google.com (2024-04-12)

Project: chromium/src
Branch: main

commit 60cdb219a3cc5d0d901a6c51bb5ed1534184be12
Author: Lijin Shen <lazzzis@google.com>
Date:   Fri Apr 12 17:32:41 2024

    Add button tap protection duration to download dialogs
    
    Bug: 40065403
    Change-Id: I9dc99ea93824d616a542c9e7e72fa96d9d1a1340
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5416053
    Reviewed-by: Min Qin <qinmin@chromium.org>
    Commit-Queue: Lijin Shen <lazzzis@google.com>
    Cr-Commit-Position: refs/heads/main@{#1286581}

M       chrome/browser/download/android/java/src/org/chromium/chrome/browser/download/dialogs/DangerousDownloadDialog.java
M       chrome/browser/download/android/java/src/org/chromium/chrome/browser/download/dialogs/DownloadLocationDialogCoordinator.java

https://chromium-review.googlesource.com/5416053


### am...@chromium.org (2024-04-18)

This looks to have missed the M124 release notes / CVE process. It should get picked up in the orphans process. Thank you! Apologies for the inconvenience, Shaheen.

### am...@google.com (2024-04-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-25)

Congratulations Shaheen! The Chrome VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us.

### am...@chromium.org (2024-04-25)

While I'm here, I removed relnotes\_update label since I'm realizing my c#32 was in error. This fix landed in M125, not M124. Because low severity fixes are not backmerged, this fix has not yet shipped and will be reflected in the M125 Stable channel release.

### fa...@gmail.com (2024-04-26)

Thank you,

I have demonstrated two clickjacking bugs here:
1. Tapjacking Download Malicious File Popup
2. Tapjacking Open Downloads Popup
I believe the issue has been fixed for both of these issues: https://chromium-review.googlesource.com/c/chromium/src/+/5416053

A $1k reward may be sufficient for the first issue, but I believe the VRP didn't consider the second issue. Can we reevaluate the reward decision again, considering the demonstration of the second issue as well? Thank you.

### am...@chromium.org (2024-04-26)

Hi Shaheen, both examples were considered in VRP reward assessment. These are low severity and low impact clickjacking issues, requiring many preconditions to result in a user being tricked by these scenarios. Additionally, there is a single root cause here, which was resolved by this CL. As such, the VRP Panel has considerer this to be a sufficient reward for this report.
We're happy to take another look, but I did want to level-set expectations to explain how this report was reviewed and assessed already.

### fa...@gmail.com (2024-04-26)

Thank you Amy,
The precondition is clickjacking to bypass the APK warning with two taps, which allows bypassing the warning. Additionally, with another two taps, the opening of this APK file is also bypassed, which is the second issue. Furthermore, other files besides APKs do not open automatically after download; the user needs to click again, which can also be clickjacked with two taps, allowing any files to be downloaded and opened without the prompt request to open a downloaded file. I am hoping this issue is also fixed in the CL.

> As such, the VRP Panel has considerer this to be a sufficient reward for this report. We're happy to take another look, but I did want to level-set expectations to explain how this report was reviewed and assessed already

Thank you again, but it would be greatly appreciated if you could take another look at this bug. Probably nothing will change, but for me, I would like to remain hopeful and try again.

### am...@chromium.org (2024-05-01)

Thank you for again for the report, Shaheen. Upon reassessment, the Chrome VRP Panel has decided that the reward amount is sufficient for the report based on these being low severity and low impact clickjacking issues. There are specific preconditions and a fairly high amount of user interaction required here. There was no change in the reward decision upon consideration of your input above during the reassessment.

### fa...@gmail.com (2024-05-06)

Ok, Thank you.

### pe...@google.com (2024-07-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065403)*
