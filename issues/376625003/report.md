# Local file access restrictions in chrome.devtools can be bypassed through prototype manipulation.

| Field | Value |
|-------|-------|
| **Issue ID** | [376625003](https://issues.chromium.org/issues/376625003) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 130.0.6723.0 |
| **Reporter** | ba...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2024-10-31 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Install the attached extension on macOS, and disable "Allow access to file URLs".
2. Open devtools on the new tab opened by the extension.
3. Edit the /etc/hosts file highlighted in the sources panel, and save the changes.
4. Observe that extension pops up an alert with the new contents of this file.

# Problem Description

Various APIs under chrome.devtools use the canAccessResource function (<https://chromium.googlesource.com/devtools/devtools-frontend/+/refs/heads/main/front_end/models/extensions/ExtensionAPI.ts#1149>) for checking if local resources should be accessible to a given extension.
However, the checks in this function can currently be entirely bypassed by overriding URL.prototype's protocol getter as is done in the attached POC.
Since there are no additional checks on the ExtensionServer side when adding event listeners through chrome.devtools.inspectedWindow.onResourceContentCommitted.addListener, an extension can gain access to local resources this way if the user interacts with such resources in the sources panel.

# Additional Comments

Previous issues relating to this include:

- <https://issues.chromium.org/issues/40060465>
- <https://issues.chromium.org/issues/40063505>
  Notably, the latter of those was fixed by <https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4370246>, which in turn introduced the possibility to modify the URL prototype to bypass this check.

# Summary

Local file access restrictions in chrome.devtools can be bypassed through prototype manipulation.

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [background.js](attachments/background.js) (text/javascript, 227 B)
- [devtools.html](attachments/devtools.html) (text/html, 36 B)
- [devtools.js](attachments/devtools.js) (text/javascript, 283 B)
- [manifest.json](attachments/manifest.json) (application/json, 190 B)

## Timeline

### pg...@google.com (2024-11-01)

Setting Severity to S2 as it requires an extension download  

Setting OSes as I have been able to repro this in Linux  

Setting FoundIn to M128 I've been able to repro this in M128

dsv@ - assigning to you per the other extension bugs! could you take a look and reassign if need be?

### pe...@google.com (2024-11-02)

Setting milestone because of s2 severity.

### pe...@google.com (2024-11-02)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-11-04)

Project: devtools/devtools-frontend  

Branch: main  

Author: Danil Somsikov <[dsv@chromium.org](mailto:dsv@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5987430>

Protect canAccessResource in DevTools API form prototype pollution

---


Expand for full commit details
```
Protect canAccessResource in DevTools API form prototype pollution 
 
Bug: 376625003 
Change-Id: Ib07a65da8f342c4727bceb6afcbd920bcfd07b81 
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5987430 
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org> 
Commit-Queue: Danil Somsikov <dsv@chromium.org>

```

---

Files:

- M `front_end/models/extensions/ExtensionAPI.ts`

---

Hash: b50c1dbc6b709196064bb26ee75b1ed6cee4f974  

Date:  Mon Nov 04 12:09:10 2024


---

### ap...@google.com (2024-11-06)

Project: chromium/src  

Branch: main  

Author: Danil Somsikov <[dsv@chromium.org](mailto:dsv@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6000132>

Test that extensions can't get access to local file via prototype pollution

---


Expand for full commit details
```
Test that extensions can't get access to local file via prototype pollution 
 
Bug: 376625003 
Change-Id: I7fd532c28dc9017380fb364c4af0bbdc7ea2549a 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6000132 
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org> 
Commit-Queue: Danil Somsikov <dsv@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1378983}

```

---

Files:

- M `chrome/browser/devtools/devtools_browsertest.cc`

---

Hash: 2b3332f90019f018bcc3563281f511363451129c  

Date:  Wed Nov 06 14:41:16 2024


---

### pe...@google.com (2024-11-06)

Security Merge Request Consideration: Requesting merge to beta (M131) because latest trunk commit (1378983) appears to be after beta branch point (1368529).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-11-06)

Given the precondition to install a malicious extension and the interaction required in dev tools, this is aptly set as medium severity. M131 Stable RC has already been cut for release next week, so I'm going to decline backmerge approval and this fix can ship in M132 Stable.
If there are any issues or concerns about this please let me know.

### sp...@google.com (2024-11-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-22)

Congratulations! Thank you for your efforts and reporting this issue to us.

### pg...@google.com (2025-01-13)

Hello reporter - how would you like to be credited for this report?

### ba...@gmail.com (2025-01-14)

Credit: Anonymous

### ph...@google.com (2025-02-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/376625003)*
