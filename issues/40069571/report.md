# chrome.inspectedWindow.eval execution on Web Store with trailing URL dot

| Field | Value |
|-------|-------|
| **Issue ID** | [40069571](https://issues.chromium.org/issues/40069571) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | pf...@google.com |
| **Created** | 2023-08-14 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. Install attached extension
2. Open inspect element on any http/https website
3. Observe alert in Web Store domain with access to privileged APIs

**Problem Description:**  

The issue is simply that the chrome.devtools origin checks and the domains of Web Store pages with privileged methods don't line up.

Web Store URLs with privileges:

- [https://chrome.google.com/webstore\](https://chrome.google.com/webstore%5C)\*
- [https://chrome.google.com./webstore\](https://chrome.google.com./webstore%5C)\* (note trailing dot)

Devtools checks:

- [https://chrome.google.com/webstore\](https://chrome.google.com/webstore%5C)\*

The source of the error is here:

<https://source.chromium.org/chromium/chromium/src/+/main:out/fuchsia-Debug/gen/third_party/devtools-frontend/src/front_end/models/extensions/extensions.js;drc=e2089b5b87f0219bc59c9f965e3dc00d423594d0;l=2544>

```
if (parsedURL.protocol.startsWith("http") && parsedURL.hostname === "chrome.google.com" && parsedURL.pathname.startsWith("/webstore")) {  
[reject access...]  

```

**Additional Comments:**  

Obviously, the check for the new Web Store domain (chromewebstore.google.com) should also be fixed.

\*\*Chrome version: \*\* 116.0.0.0 \*\*Channel: \*\* Beta

**OS:** Chrome OS

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 236 B)
- [devtools.html](attachments/devtools.html) (text/plain, 37 B)
- [devtools.js](attachments/devtools.js) (text/plain, 568 B)
- [trailing_dot_poc.zip](attachments/trailing_dot_poc.zip) (application/octet-stream, 880 B)
- [trailing_dot_poc_vid.mp4](attachments/trailing_dot_poc_vid.mp4) (video/mp4, 818.2 KB)
- [Capture1.PNG](attachments/Capture1.PNG) (image/png, 99.0 KB)
- [may be working poc.zip](attachments/may be working poc.zip) (application/zip, 1.6 KB)

## Timeline

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-08-16)

Assigning to extensions platform team.
Do we need to add the trailing dot URL checks here?
https://crsrc.org/c/third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;drc=1b4c7f814524c8a96499273734b2595338d1d941;l=1320

[Monorail components: Platform>Extensions>API]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-08-16)

[Comment Deleted]

### ma...@gmail.com (2023-10-16)

This looks like an easy fix; is any work being done to fix this?

### tj...@chromium.org (2023-10-16)

dsv@, caseq@: Another small devtools mismatch, could you take a look?

### ds...@chromium.org (2023-10-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/3193420616e941179d2087ea319fc4377df4cd5d

commit 3193420616e941179d2087ea319fc4377df4cd5d
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Thu Oct 26 12:55:37 2023

Match trailing dot in webstore urls

Fixed: 1472898
Change-Id: If84c5f555b41248ab10172f6c094ee5c466def3e
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4979525
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/3193420616e941179d2087ea319fc4377df4cd5d/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/3193420616e941179d2087ea319fc4377df4cd5d/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### [Deleted User] (2023-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-02)

Congratulations, Derin! The Chrome VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### ma...@gmail.com (2023-11-02)

Thanks for the generous bounty :)

### am...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-30)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-02-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-02-01)

This issue was migrated from crbug.com/chromium/1472898?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### si...@gmail.com (2024-03-09)

hi i think i can still execute chrome.inspectedWindow.eval execution on Web Store is it a security issue i have attched the pic
 

### an...@chromium.org (2024-03-11)

This appears to be WAI. From the attached PNG, it looks like the URL you are using includes a quote character after the domain part (i.e. /"webstore) which makes it NOT a webstore URL.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069571)*
