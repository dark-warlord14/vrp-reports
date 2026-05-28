# Extensions without file URL access can open UNC paths through chrome.debugger

| Field | Value |
|-------|-------|
| **Issue ID** | [391114799](https://issues.chromium.org/issues/391114799) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Windows |
| **Chrome Version** | 132.0.6834.84 |
| **Reporter** | ba...@gmail.com |
| **Assignee** | pf...@google.com |
| **Created** | 2025-01-20 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

On a server that the target can access:

1. Clone the following repository: <https://github.com/lgandx/Responder>
2. Inside the repository, run sudo ./Responder.py -I <INTERFACE> -w, where INTERFACE is the public facing network interface of the server

On the target:

1. Download the attached extension
2. In background.js, replace SERVER\_IP with the address of the server running responder.py
3. Install the extension, and make sure to disable "Allow access to file URLs"

Note that the NTLM hash is leaked twice, once after the initial install with access to file URLs enabled (as expected), but also when the extension reloads after disabling that option.

# Problem Description

DevTool's TargetHandler::CreateTarget does not check if the current extension should be allowed to access local files, which allows extensions with the debugger permission to open arbitrary file URLs. On Windows, this can be exploited by opening a UNC path, which will then lead to the current user's NTLM hash getting leaked, as in bugs such as <https://issues.chromium.org/issues/40060207>

In addition to the extension that can be used to reproduce this, I've also attached a suggested fix, which should disallow creating targets with file URLs if the appropriate permissions aren't given.

# Summary

Extensions without file URL access can open UNC paths through chrome.debugger

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: No

## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 157 B)
- [patch.patch](attachments/patch.patch) (text/x-diff, 2.4 KB)
- [background.js](attachments/background.js) (text/javascript, 640 B)

## Timeline

### ad...@google.com (2025-01-20)

Security shepherd: I don't have the required setup to reproduce this, but it sounds like it's probably a valid bug. The [extensions security FAQ](https://chromium.googlesource.com/chromium/src/+/main/extensions/docs/security_faq.md#what-privileges-does-the-debugger-permission-grant-an-extension_what-privileges-should-it-lack) makes no suggestion that debugger permission should grant this sort of privilege.

I'm rating it as S2 because it is a significant information leak but has the prerequisite of an extension being installed. Assuming this impacts stable onwards.

### pe...@google.com (2025-01-21)

Setting milestone because of s2 severity.

### pe...@google.com (2025-01-21)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### rd...@chromium.org (2025-01-21)

triage: debugger API -> dsv@

### pf...@google.com (2025-01-22)

The attached patch looks reasonable. Reporter: Would you like to send the CL yourself?

### ba...@gmail.com (2025-01-22)

Sorry, I'd prefer the patch to be committed on my behalf, as I haven't sent any prior CLs so far.

### pf...@google.com (2025-01-30)

Unfortunately we can't accept contributions in the form of patch files. Please see <https://chromium.googlesource.com/chromium/src/+/main/docs/contributing.md> to learn how to submit changes!

### ba...@gmail.com (2025-01-31)

Alright, I've sent a CL: https://chromium-review.googlesource.com/c/chromium/src/+/6218796

### ap...@google.com (2025-02-03)

Project: chromium/src  

Branch: main  

Author: Topi Lassila <[tolassila@gmail.com](mailto:tolassila@gmail.com)>  

Link:      <https://chromium-review.googlesource.com/6218796>

Check whether devtools clients should be allowed to target local files

---


Expand for full commit details
```
Check whether devtools clients should be allowed to target local files 
 
Bug: 391114799 
Change-Id: I1ab514ebe7b4a00c740bb1943dcf3c3401d931b8 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6218796 
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
Reviewed-by: Simon Zünd <szuend@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1414781}

```

---

Files:

- M `AUTHORS`
- M `chrome/browser/devtools/chrome_devtools_session.cc`
- M `chrome/browser/devtools/protocol/target_handler.cc`
- M `chrome/browser/devtools/protocol/target_handler.h`
- M `chrome/test/data/extensions/api_test/debugger_file_access/background.js`

---

Hash: e166400fa4c632c5150d75bf587e8a34285fb783  

Date:  Mon Feb 03 00:09:25 2025


---

### pf...@google.com (2025-02-07)

Alex did you verify if the CL fixed the issue? Let's close this

### al...@google.com (2025-02-07)

pfaffe@ I left that part for you as the issue assignee

### pf...@google.com (2025-02-07)

Verified that the attached extension now fails to create a target when a file:// url is used!

### sp...@google.com (2025-02-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$2,000 for report of lower impact user information disclosure + $2,000 patch bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-14)

Congratulations! Thank you for your efforts and reporting this issue to us. Please let us know what name/handle/tag you would like us to use in publicly acknowledging you for this finding.

### ba...@gmail.com (2025-02-15)

Thanks for the reward! You may credit me as "Topi Lassila".

### am...@chromium.org (2025-04-04)

In review of this issue, I believe this should have been assessed at low severity based on the requirement of the debugger API and is a pretty hefty precondition for extensions based vulnerabilities. That being said, this issue does demonstrate a good user information disclosure so it is definitely considered a security issue.

### ch...@google.com (2025-05-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/391114799)*
