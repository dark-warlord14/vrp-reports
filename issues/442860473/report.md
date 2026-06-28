# File Source Origin Spoofing via Extension Name

| Field | Value |
|-------|-------|
| **Issue ID** | [442860473](https://issues.chromium.org/issues/442860473) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 139.0.0.0 |
| **Reporter** | fr...@gmail.com |
| **Assignee** | ya...@google.com |
| **Created** | 2025-09-04 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Load the extension
2. Go to chrome://extensions
3. Reload the extension
4. Go to chrome://downloads and you will see the google.apk origin is pointing to <https://google.com>

# Problem Description

This vulnerability occurs when the chrome://downloads source origin can be spoofed via the extension name. By default, if we install an extension that downloads a file, Chrome will set the downloaded file’s origin to the extension’s name. For example, if a file is downloaded by an extension named “Frozzipies Extension”, Chrome will display the origin as “Downloaded by Frozzipies Extension”.

However, in this case, we can use any valid URL (like <https://google.com>) as the extension name, which causes Chrome to display the file origin as “Downloaded by [https://google.com”](https://google.com%E2%80%9D), leading to an origin spoofing issue.

# Summary

File Source Origin Spoofing via Extension Name

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 221 B)
- [background.js](attachments/background.js) (text/javascript, 601 B)
- [file origin spoofing via extension name.mov](attachments/file origin spoofing via extension name.mov) (video/quicktime, 6.7 MB)
- [PoC origin spoofing via extension name.zip](attachments/PoC origin spoofing via extension name.zip) (application/zip, 2.4 KB)
- [Screenshot 2025-09-04 at 1.46.51 PM.png](attachments/Screenshot 2025-09-04 at 1.46.51 PM.png) (image/png, 81.5 KB)
- [IDS_DOWNLOAD_BY_EXTENSION_URL.png](attachments/IDS_DOWNLOAD_BY_EXTENSION_URL.png) (image/png, 58.1 KB)
- [IDS_DOWNLOAD_BY_EXTENSION_URL.png](attachments/IDS_DOWNLOAD_BY_EXTENSION_URL_74524550.png) (image/png, 58.7 KB)

## Timeline

### [Deleted User] (2025-09-04)

For reference, I've attached a screenshot of what the UI looks like. The only indications that this came from an extension named "<https://google.com>" are that it says "Downloaded by" instead of "From" and the name is hyperlinked to go to the extension.

### ch...@google.com (2025-09-05)

Setting milestone because of s2 severity.

### ch...@google.com (2025-09-05)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-09-19)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-04)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-19)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-03)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-19)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 75 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-04)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 90 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-19)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 105 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-03)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 120 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fr...@gmail.com (2026-01-15)

Hi team, any update on this?

### ch...@google.com (2026-01-18)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 135 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-02)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 150 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-17)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 165 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-03-04)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 180 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ya...@google.com (2026-03-18)

Hi @ch...@google.com, should bugs like this be marked as "Won't Fix" until there is an implementation for go/chrome-ui-download-origins?

cc: @qi...@google.com @li...@google.com

### ya...@google.com (2026-03-19)

Synced with @ch...@google.com offline. Recommendation was to change the text from `Downloaded by` to `Downloaded by Chrome extension:`  to make spoofing attempts more obvious to the user. I attached a screenshot of the updated text after the code change.

### ch...@google.com (2026-03-19)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 195 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ya...@google.com (2026-03-19)

I have attached an updated screenshot after the text change from `Downloaded by` to `Downloaded by extension:`  based on [CL](https://chromium-review.git.corp.google.com/c/chromium/src/+/7681374/comment/cdb3e9f6_915cda5c/) feedback.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Yaw Frempong [yawfrempong@google.com](mailto:yawfrempong@google.com)  

Link:    <https://chromium-review.googlesource.com/7681374>

[Downloads Origin] Update String for Download by Extension URL

---


Expand for full commit details
```
     
    Details: Update the text for downloads triggered by an extension URL to 
    make spoofing attempts more obvious to the end-user. 
     
    Screenshot: https://crbug.com/442860473#attachment74524550 
     
    Bug: 442860473 
    Change-Id: Ibb900e954a2d4cb1ba9b0852846a9634d842db7a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7681374 
    Reviewed-by: Lily Chen <chlily@chromium.org> 
    Reviewed-by: Andrew Liu <liu@chromium.org> 
    Commit-Queue: Yaw Frempong <yawfrempong@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1602119}

```

---

Files:

- M `chrome/app/generated_resources.grd`
- A `chrome/app/generated_resources_grd/IDS_DOWNLOAD_BY_EXTENSION_URL.png.sha1`

---

Hash: [69626ea817c67a6450bf47627483671e030fa5d5](https://chromiumdash.appspot.com/commit/69626ea817c67a6450bf47627483671e030fa5d5)  

Date: Thu Mar 19 18:23:03 2026


---

### wf...@chromium.org (2026-06-09)

Hi re: [comment#21](https://issues.chromium.org/issues/442860473#comment21) can you confirm where the link in your screenshot goes to -> does it go to google.com or does it go to the extension page?

### fr...@gmail.com (2026-06-09)

When we click the link, it will go to the extension page.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Security UI Spoofing


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/442860473)*
