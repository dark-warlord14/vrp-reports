# pyz and pyzw file not in block list

| Field | Value |
|-------|-------|
| **Issue ID** | [333940412](https://issues.chromium.org/issues/333940412) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2024-04-12 |
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
Please provide a brief explanation of the security issue.

VERSION
Chrome Version: 123.0.6312.123
Operating System: windows

REPRODUCTION CASE
The metadata describe file-type download behavior in Chrome stored in download_file_types.asciipb:

https://source.chromium.org/chromium/chromium/src/+/main:components/safe_browsing/content/resources/download_file_types.asciipb

We can see python related file marked as ALLOW_ON_USER_GESTURE : py/pyc/pyd/pyo/pyw. But pyz and pyzw files are also dangerous, they are executable python zip archives:

https://docs.python.org/3.9/library/zipapp.html

I have uploaded app.pyz and app.pyzw, they can pop a calc on windows. And as you can see in screenshot.png, I get a warning when download py file in edge but no warning when download pyzw.


## Attachments

- [app.pyz](attachments/app.pyz) (application/x-zip, 711 B)
- [app.pyzw](attachments/app.pyzw) (application/x-zip, 711 B)
- [screenshot.png](attachments/screenshot.png) (image/png, 27.1 KB)

## Timeline

### bo...@chromium.org (2024-04-12)

Thanks for the report! Confirming no download warning on 123 (stable).

Note, the executables did not run successfully when double-clicked from the file explorer on my Linux environment, but they did on my Windows environment. Perhaps behavior depends on the file extension handler configuration.

Routing to our owner for the Downloader's extension configuration list for an authoritative opinion about whether to add .pyz and .pyzw to the list.

### jd...@chromium.org (2024-04-12)

Ope! I'm not the owner, but over to drubery@ who should be able to help.

### pe...@google.com (2024-04-13)

Setting milestone because of s2 severity.

### pe...@google.com (2024-04-27)

drubery: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-05-03)

Project: chromium/src
Branch: main

commit b2a7ca7e84a2e7bab60387ab01a1d884db2db4e9
Author: Daniel Rubery <drubery@chromium.org>
Date:   Fri May 03 13:26:46 2024

    Add PYZ and PYZW to download_file_types.asciipb
    
    Users with Safe Browsing disabled will now be warned on drive-by
    downloads of these file types. This protects them slightly more than
    previously.
    
    Fixed: 333940412
    Change-Id: Ifaf65e0899654cba11ce6e410996e163866e522a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5510090
    Reviewed-by: thefrog <thefrog@chromium.org>
    Auto-Submit: Daniel Rubery <drubery@chromium.org>
    Commit-Queue: thefrog <thefrog@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1296043}

M       components/safe_browsing/content/resources/download_file_types.asciipb
M       tools/metrics/histograms/enums.xml

https://chromium-review.googlesource.com/5510090


### sp...@google.com (2024-05-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you for the report! The Chrome VRP Panel has decided to award you $500 for this report of a low-impact issue with some pre-existing protection from Safe Browsing.

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### ho...@gmail.com (2024-07-29)

Hello, When will this vulnerability be disclosed?

### am...@chromium.org (2024-07-29)

security bugs are automatically publicly disclosed 14 weeks after the issue is closed as fixed [1]; this issue was closed on 3 May, so it will be opened for public disclosure on 9 August.

[1] <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#when-will-the-bug-i-reported-be-publicly-disclosed>

### dr...@chromium.org (2024-07-29)

deleted

### pe...@google.com (2024-08-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/333940412)*
