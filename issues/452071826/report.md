# HTTP-Auth Passwords are not secured on MacOS

| Field | Value |
|-------|-------|
| **Issue ID** | [452071826](https://issues.chromium.org/issues/452071826) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Passwords |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bu...@gmail.com |
| **Assignee** | vs...@google.com |
| **Created** | 2025-10-14 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
"Use your screen lock when filling passwords" on MacOS does not work for HTTP Authentication.

VERSION
Chrome Version: 141.0.7390.77 stable
Operating System: MacOS Tahoe 26.0 (25A354)

REPRODUCTION CASE
1. Install Chrome freshly
2. Open Chrome
3. Open the URL chrome://password-manager/settings
4. Enable the Setting "Use your screen lock when filling passwords"
5. Open the URL https://authenticationtest.com/HTTPAuth/
6. Enter "user" and "pass" as credentials
7. Save the credentials as supposed by Chrome
8. Clear website data to log out, close and reopen Chrome
9. Open again the URL https://authenticationtest.com/HTTPAuth/

At this point, the passwords are already filled in and we can log in without the need to authenticate via screen lock (e.g. fingerprint)

Conversely, the screen lock to access passwords works on other authentication methods such as the one on this site: https://authenticationtest.com/simpleFormAuth/

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Anonymous

## Timeline

### el...@chromium.org (2025-10-14)

Security shepherd: thanks for the report.

I don't know what the conditions are for that toggle to show up, but it doesn't show up for me in 143.0.7471.0 on macOS 15.7.1. Maybe this is macOS 26 specific?

-> vasilii@ for password manager triage; setting provisional Pri-3 / Sev-3.

### bu...@gmail.com (2025-10-14)

Hey, thanks for the ultra fast assessment!

Maybe some more information helps - sorry for not providing it initially
- I downloaded the Chrome binary via https://www.google.com/intl/de/chrome/ and not via the Mac App Store
- it is a MacBook Pro M4 Max 14″, Nov. 2024
- the toggle was for sure available in older versions of MacOS as well - though I cannot test it any more
- in German, the toggle is named "Die Displaysperre zum Ausfüllen von Passwörtern verwenden
Wenn du dieses Gerät gemeinsam mit anderen nutzt, kannst du die Displaysperre verwenden, um deine Identität zu bestätigen, wenn du ein gespeichertes Passwort verwendest"


### va...@chromium.org (2025-10-16)

Yeah, looks like we forgot to implement this toggle for non HTML types of login because they are rare.

### dx...@google.com (2025-10-23)

Project: chromium/src  

Branch:  main  

Author:  Viktor Semeniuk [vsemeniuk@google.com](mailto:vsemeniuk@google.com)  

Link:    <https://chromium-review.googlesource.com/7046232>

Prompt biometric reauth before filling password for basic auth

---


Expand for full commit details
```
     
    Fixed: 452071826 
    Change-Id: I3b91a14f3ef5ace86de024d54178356c14d04dfc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7046232 
    Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com> 
    Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1534201}

```

---

Files:

- M `chrome/browser/password_manager/chrome_password_manager_client.cc`
- M `components/password_manager/core/browser/http_auth_manager_impl.cc`
- M `components/password_manager/core/browser/http_auth_manager_impl.h`
- M `components/password_manager/core/browser/http_auth_manager_unittest.cc`

---

Hash: [98adca1518214906f219902deb50aa01073db37f](https://chromiumdash.appspot.com/commit/98adca1518214906f219902deb50aa01073db37f)  

Date: Thu Oct 23 10:17:47 2025


---

### bu...@gmail.com (2025-10-25)

Hi, thanks for fixing this so fast:)

May I ask for a bug bounty?

### sp...@google.com (2025-12-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Security Improvement


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Security Improvement

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/452071826)*
