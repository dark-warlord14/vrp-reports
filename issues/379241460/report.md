# the permission prompt is not in the correct position lead to spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [379241460](https://issues.chromium.org/issues/379241460) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Reporter** | sa...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2024-11-15 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS

when the popup window is displayed on the sidepanel and at the same time the permission prompt is displayed and at the same time window.move is performed, the permission prompt does not move to the window but is in its initial position, this causes to spoofing the permission prompt in a different window

VERSION
Chrome Version 133.0.6838.0 (Official Build) canary (64-bit)
Operating System: Window 10

REPRODUCTION CASE

1. create folder with name : sidepanel then put  the files: index.css,index.js,index.html into sidepanel folder
2  install the extension
3. open the extension
4. click on "open"


CREDIT INFORMATION

Reporter credit: Hafiizh (https://www.linkedin.com/in/hafiizh-7aa6bb31/)

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [bandicam 2024-11-17 05-07-30-993.mp4](attachments/bandicam 2024-11-17 05-07-30-993.mp4) (video/mp4, 3.0 MB)
- [background.js](attachments/background.js) (text/javascript, 115 B)
- [manifest.json](attachments/manifest.json) (application/json, 291 B)
- [index.css](attachments/index.css) (text/css, 1.2 KB)
- [index.html](attachments/index.html) (text/html, 255 B)
- [index.js](attachments/index.js) (text/javascript, 481 B)
- [spoofpermission.html](attachments/spoofpermission.html) (text/html, 292 B)
- [spoofbar.html](attachments/spoofbar.html) (text/html, 142 B)
- [bandicam 2025-03-26 11-40-59-356.mp4](attachments/bandicam 2025-03-26 11-40-59-356.mp4) (video/mp4, 2.8 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### ah...@google.com (2024-11-15)

deleted

### ah...@google.com (2024-11-15)

[Primary Security Shepherd]

Thanks for the report! Could you please upload the files: spoofpermission.html and spoofbar.html?

Thank you!

### sa...@gmail.com (2024-11-15)

sorry i forgot uploaded the files

### pe...@google.com (2024-11-15)

Thank you for providing more feedback. Adding the requester to the CC list.

### sa...@gmail.com (2024-11-16)

I updated the POC:


REPRODUCTION CASE

1. create folder with name : sidepanel then put  the files: index.css,index.js,index.html into sidepanel folder
2  install the extension
3. open the extension
4. click on "open"

### ah...@google.com (2024-11-18)

[Primary Security Shepherd]

Thanks for the report, I wasn't able to reproduce on my device unfortunately.

Provisionally setting the FoundIn to the current extended stable (130)

Setting severity to low since this requires the user to first install the extension.

### ah...@google.com (2024-11-18)

Hello [rdevlin.cronin@chromium.org](mailto:rdevlin.cronin@chromium.org),

Could you please take a look? Feel free to reassign if this is not on your end.

Thanks!

### pe...@google.com (2024-11-18)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2025-03-24)

Hello any updates?

### sa...@gmail.com (2025-03-26)

hello this bug is fixed and cannot be reproduced in Version 136.0.7064.0 (Official Build) dev (64-bit). After the window appears and moves to the bottom corner the permission prompt continues to appear following the window.. Can you set this bug to fixed? 

### sa...@gmail.com (2025-09-23)

pinging to the security team. This bug has not been reproducible since version  Version 136.0.7064.0 (Official Build) dev (64-bit).

### sa...@gmail.com (2025-10-31)

deleted

### dr...@chromium.org (2025-11-04)

Given this was reported fixed in M136, there's no value in identifying the fixing CL. Setting Fixed By Code Changes to NA and closing.

### sp...@google.com (2025-12-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Security UI Spoofing (low impact)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Security UI Spoofing (low impact)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/379241460)*
