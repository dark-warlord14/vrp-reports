# File Might Be Harmful Warning Missing for HTTP-Only Sites on Android

| Field | Value |
|-------|-------|
| **Issue ID** | [353244363](https://issues.chromium.org/issues/353244363) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Services (Use Subcomponents)>Safebrowsing, UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2024-07-15 |
| **Bounty** | $500.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
When an Android .apk file is downloaded using the Chrome browser on an Android device, a warning dialog usually appears indicating that the file may be harmful (see harmful-file-warning.jpg). This warning differentiates .apk files from other types of files during the download process.

However, if the website is served over HTTP rather than HTTPS, the specific harmful file warning for .apk files is no longer displayed. Instead, only HTTP insecure warning appears for all downloads, regardless of the file type (see test.jpg). This general warning does not specifically highlight the potential risks associated with .apk files, with other types of files downloaded from an HTTP site.

VERSION
Chrome Version: 126.0.6478.122 + [stable]
Operating System: Android 14

REPRODUCTION CASE
1. Download the `test.html` file below.
2. Host the file on a simple Python HTTP server by running `python3 -m http.server 8080` in the same folder (to simulate an HTTP-only scenario).
3. Access the site on the Android device using the latest version of the Chrome browser with the URL `http://YOUR_SERVER_IP:8080/test.html`.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Shaheen Fazim

## Attachments

- [test.html](attachments/test.html) (text/html, 114 B)
- [test.jpg](attachments/test.jpg) (image/jpeg, 45.9 KB)
- [harmful-file-warning.jpg](attachments/harmful-file-warning.jpg) (image/jpeg, 25.4 KB)
- [screencapture.mp4](attachments/screencapture.mp4) (video/mp4, 1.5 MB)

## Timeline

### ja...@chromium.org (2024-07-15)

Thanks for the bug report. I think this sounds like a Downloads bug on Android but not like a vulnerability that can be exploited by an attacker -- the user will still be warned that something is wrong by the note that the download can't be retrieved securely.

I'm thinking there's a UX issue that can be solved here, where Chrome needs to decide how to convey both pieces of information to the user.

### fa...@gmail.com (2024-07-16)

Previous issues like <https://issues.chromium.org/issues/40058914>, where the lack of a "file might be harmful" warning was considered a security issue, similarly, using the method above, we are able to evade this warning. Yes, it shows another dialogue warning, "insecure download," but this warning can be for any insecure download, even images, and there is no extra warning for .apk downloads, which is usually present.

### dr...@chromium.org (2024-07-16)

[security triage] I can reproduce this in M126 and am the right owner. Easy triage.

### pe...@google.com (2024-07-17)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### fa...@gmail.com (2024-09-18)

Hi Assignee, any updates on this issue?

### fa...@gmail.com (2024-10-15)

Hello Assignee, may I get an update on this issue?

### fa...@gmail.com (2024-10-16)

deleted

### dr...@chromium.org (2025-03-21)

chlily@ - this is going to be addressed by your planned work on APK downloads, right?

Given that this is S3, I think it's reasonable to let the more comprehensive work complete as planned and make this obsolete.

### ch...@chromium.org (2025-03-21)

Oh hm, I am fairly certain I spotted some code that should have dealt with the "insecure download + generic APK file type warning" combo. I can't find it at the moment, but yes this is likely to be obsoleted by MaliciousApkDownloadCheck so I'll follow up here after that lands.

### fa...@gmail.com (2025-04-09)

Friendly ping.

### fa...@gmail.com (2025-12-16)

Hi, tested on the latest Chrome version `143.0.7499.109` on Android and can confirm that the issue is now fixed. The APK warning is now shown for HTTP download requests. This issue can be closed as resolved. Thank you.

### ch...@chromium.org (2025-12-16)

Hm strange, MaliciousApkDownloadCheck never landed and I'm not aware of any work here that would have fixed this bug.

Joe, did anything change about InsecureDownloadWarnings on Android, that might have affected whether the insecure dialog interferes with the dangerous dialog?

### fa...@gmail.com (2025-12-19)

Hi, I forgot to add the screen recording. It seems that it was fixed, and both dialogs are now properly shown.

### ch...@chromium.org (2025-12-19)

Ok, thanks for confirming.

It's possible this was previously hitting another bug, maybe [crbug.com/419363698](https://crbug.com/419363698), that was causing the DangerousDownloadDialog to not be displayed.

### sp...@google.com (2026-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
the panel determined this was low impact exploitation mitigation bypass and thanks you for suggesting improvements here


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/353244363)*
