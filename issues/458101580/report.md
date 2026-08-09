# Bypass :// Characters in Download Security UI lead to Origin Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [458101580](https://issues.chromium.org/issues/458101580) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 131.0.0.0 |
| **Reporter** | fr...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2025-11-06 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

1. Prepare spoof html files or you can use mine at <https://n13s.site/spoof-2.html>
2. Access the page
3. Download the file
4. You will see that the :// blacklist is getting bypassed and allow attacker to create a fake origin

# Problem Description

By default, Chrome’s Security UI blocks :// from appearing as a filename in the Download UI. One reason Chrome may block these characters is to prevent spoofing techniques in the Download UI. However, in this case, I was able to bypass this restriction using ∶⧸⧸ (Ratio U+2236 + Long Division Slash U+29F8, x2). With this bypass method, an attacker can create a fake origin in the filename, such as creating a different origin source like `From https://google.com` to a malicious file in the Download Origin UI and moreover the MacOS Chrome browser is not showing the Download Origin make it more easier to spoof.

# Summary

iOS Chrome: Bypass :// Characters in Download Security UI lead to Origin Spoofing

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [IMG_4862.MP4](attachments/IMG_4862.MP4) (video/mp4, 5.2 MB)
- [spoof-2.html](attachments/spoof-2.html) (text/html, 2.0 KB)
- Fri Apr 24 2026 17:38:03 GMT+0200 (Central European Summer Time).png (image/png, 170.5 KB)

## Timeline

### ma...@google.com (2025-11-06)

Downloads folks, could you PTAL?

### ma...@google.com (2025-11-06)

Also converting this into a functional bug because I don't think it meets our bar for UI spoofing bugs. Downloading files is one of the examples explicitly called out in <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#What-makes-a-UI-spoof-interesting-to-report>

### pr...@gmail.com (2025-11-06)

Re#3:

Heyyaaa, after my short review there is similar report before this issue ever happened, especially in the Android platform, I believe its not only functionality bugs but also security bugs, the issue reported in https://issues.chromium.org/issues/392818696, and also this issue is giving direct impacts to the end-users... based on those considerations I believe this is vulnerability not only functionality bugs,

thank you 

### ma...@google.com (2025-11-07)

CCing some folks from 392818696. It does seem substantially similar to that issue, though that one too seems borderline. I'll change it back to security for now.

### ch...@google.com (2025-11-08)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pr...@gmail.com (2026-03-03)

heyyaaa any updates?

### sd...@google.com (2026-03-23)

IIUC, on macOS, they fixed this by not displaying the file name. Maybe we should do the same thing on iOS.
As discussed with olivierrobin: qpubert, can you take a look?

### qp...@google.com (2026-04-24)

redacted

### ch...@google.com (2026-04-24)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pr...@gmail.com (2026-05-06)

any reward update?

### sp...@google.com (2026-05-26)

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

### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/458101580)*
