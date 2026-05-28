# "File might be harmful" dialog does not have origin

| Field | Value |
|-------|-------|
| **Issue ID** | [415496161](https://issues.chromium.org/issues/415496161) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Chrome Version** | 135.0.0.0 |
| **Reporter** | fr...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2025-05-04 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Access poc.html
2. Click the button
3. The download pop-up will still appear on <https://google.com>

# Problem Description

This vulnerability occurs when there is a condition that a file download pop-up origin can be overlaid on other origin. The file download pop-up should only be appear when user is accessing the real origin where the file download pop-up come from.

For more information you can read on [crbug.com/40055527](https://crbug.com/40055527)

Chrome version: 135.0.7049.111 (Official Build) (64-bit)

# Summary

[crbug.com/40055527](https://crbug.com/40055527) is still reproducible on newest version of Chrome

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: Yes

## Attachments

- [regression - file download pop-up chrome.mp4](attachments/regression - file download pop-up chrome.mp4) (video/mp4, 7.8 MB)
- [poc.html](attachments/poc.html) (text/html, 601 B)

## Timeline

### dc...@chromium.org (2025-05-05)

It's not really the same bug. The origin is correct: in the original, the download was incorrectly attributed to the foreground tab, even in the downloads page.

The origin appears to be correctly displayed in this repro; is there something else that's concretely wrong?

### fr...@gmail.com (2025-05-05)

Yes, the origin is the same, but if we look at [crbug.com/40055527](https://crbug.com/40055527), the main issue is not about the file’s source origin. It’s about the fact that the file download dialog can be overlaid on a different origin or page. The test.apk file comes from the attacker’s site, but in this case, the download dialog can still be overlaid and appear on <https://google.com> as an example of trusted sites. In my opinion, this is the same issue that described in [crbug.com/40055527](https://crbug.com/40055527).

### pe...@google.com (2025-05-05)

Thank you for providing more feedback. Adding the requester to the CC list.

### dc...@chromium.org (2025-05-05)

It's not the same bug as [issue 40055527](https://issues.chromium.org/issues/40055527): that bug is about the downloads UI (accessible via the triple dot menu > Downloads) showing a completely incorrect origin.

I do agree it would be nice if the "file might be harmful" dialog had an origin (but of course, we'll have to be careful about very long origins getting elided in interesting/confusing ways).

### ch...@google.com (2025-05-06)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-06)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-05-20)

chlily: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-06-04)

chlily: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@chromium.org (2025-06-06)

I plan to address this by adding the origin to the DangerousDownloadDialog, which is going to require a custom view, but I'll also need that to address [crbug.com/410721828](https://crbug.com/410721828)

### ch...@google.com (2025-06-21)

chlily: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-07-02)

Project: chromium/src  

Branch: main  

Author: Lily Chen [chlily@chromium.org](mailto:chlily@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6696592>

Improve DangerousDownloadDialog message

---


Expand for full commit details
```
     
    This CL improves the message string shown in DangerousDownloadDialog to 
    more accurately convey security-relevant information to the user. 
     
    * Puts the filename in quotation marks and adds bold font, to make it 
      clearer that the filename portion is site-controlled and delineate it 
      from adjacent Chrome-produced parts of the UI string. The use of bold 
      font is consistent with the iOS download dialog, updated in 
      crrev.com/c/6633364. 
     
    * Adds the domain of the download URL to the string if available, in a 
      colored font. This domain string is currently the download URL, 
      processed through elide_url formatting functions, but we may select a 
      more representative URL or origin in the future. 
     
    Screenshots: 
    https://drive.google.com/drive/folders/10U4_bv9OZxIpCOCR3pPdJE9PC1MIg5Ve 
     
    Bug: 415496161, 410721828 
    Change-Id: I5366c4f95350e0bbabda25f004288b760213da20 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6696592 
    Reviewed-by: Xinghui Lu <xinghuilu@chromium.org> 
    Commit-Queue: Lily Chen <chlily@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1481797}

```

---

Files:

- M `chrome/android/javatests/src/org/chromium/chrome/browser/download/dialogs/DownloadDialogIncognitoTest.java`
- M `chrome/browser/download/android/dangerous_download_dialog_bridge.cc`
- M `chrome/browser/download/android/java/src/org/chromium/chrome/browser/download/DangerousDownloadDialogBridge.java`
- M `chrome/browser/download/android/java/src/org/chromium/chrome/browser/download/dialogs/DangerousDownloadDialog.java`
- M `chrome/browser/ui/android/strings/android_chrome_strings.grd`
- M `chrome/browser/ui/android/strings/android_chrome_strings_grd/IDS_DANGEROUS_DOWNLOAD_DIALOG_TEXT.png.sha1`
- A `chrome/browser/ui/android/strings/android_chrome_strings_grd/IDS_DANGEROUS_DOWNLOAD_DIALOG_TEXT_WITH_DOMAIN.png.sha1`
- M `chrome/browser/ui/android/strings/android_chrome_strings_grd/IDS_DANGEROUS_DOWNLOAD_DIALOG_TEXT_WITH_SIZE.png.sha1`
- A `chrome/browser/ui/android/strings/android_chrome_strings_grd/IDS_DANGEROUS_DOWNLOAD_DIALOG_TEXT_WITH_SIZE_AND_DOMAIN.png.sha1`

---

Hash: b2bf216dc223e333700a470b55df72ffeba66c6d  

Date:  Wed Jul 2 19:17:41 2025


---

### fr...@gmail.com (2025-07-16)

Hi team, is there any update regarding VRP panel meeting results?

### sp...@google.com (2025-07-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI spoof 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### fr...@gmail.com (2025-07-22)

Thanks for the reward

### ch...@google.com (2025-10-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/415496161)*
