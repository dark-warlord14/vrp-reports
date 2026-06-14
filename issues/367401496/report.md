# Unable to Uninstall PWA Due to Excessive Emoji in App Name Blocking UI

| Field | Value |
|-------|-------|
| **Issue ID** | [367401496](https://issues.chromium.org/issues/367401496) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | UI>Browser>WebAppInstalls>Desktop |
| **Platforms** | Linux |
| **Reporter** | al...@gmail.com |
| **Assignee** | fi...@google.com |
| **Created** | 2024-09-17 |
| **Bounty** | $1,000.00 |

## Description

When installing a Progressive Web App (PWA) via a custom HTML script, the app name includes a large number of emojis. This causes an issue in Chrome where the uninstall option for the PWA is inaccessible or blocked due to the emojis covering the UI elements. As a result, the user cannot uninstall the app.

Steps to Reproduce:

1. Access the HTML file in Chrome and install the PWA.
2. Attempt to uninstall the PWA by accessing the uninstall option in Chrome’s UI.

Chromium Version : Version 130.0.6701.0 (Developer Build) (64-bit)
OS : Ubuntu 22.04

Expected Result:
The user should be able to uninstall the PWA regardless of the app name length or content.

Actual Result:
The uninstall option is hidden or blocked by the excessive emojis in the app name, making it impossible to remove the PWA through the normal UI.

Impact:
This vulnerability allows a PWA to remain installed on the device without an easy way for users to remove it, which can be exploited by malicious actors.

Recommendation:
Implement validation checks on the app name to restrict the number of emojis or characters allowed, ensuring that UI elements like the uninstall option are always visible and accessible.

## Attachments

- [reproduce.webm](attachments/reproduce.webm) (video/webm, 18.8 MB)
- [icon.png](attachments/icon.png) (image/png, 18.3 KB)
- [index.html](attachments/index.html) (text/html, 1.3 KB)
- [manifest.json](attachments/manifest.json) (application/json, 14.0 KB)
- [sw.js](attachments/sw.js) (text/javascript, 315 B)
- [8e02a2e2728797c3e4a22e967284b5f9bc861a0a (2).png](attachments/8e02a2e2728797c3e4a22e967284b5f9bc861a0a (2).png) (image/png, 76.1 KB)

## Timeline

### ma...@google.com (2024-09-18)

Not convinced the abuse potential is severe enough for us to really consider this a security issue, but triaging as one for now.

dmurph@, could you PTAL?

### pe...@google.com (2024-09-19)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@gmail.com (2024-09-27)

i think this same about issue : https://issues.chromium.org/issues/40063885

### dm...@google.com (2024-09-27)

Hm.... we should attempt to truncate / ellipsis stuff here.

### al...@gmail.com (2024-11-01)

after changing month
any update ?

Thanks

### dm...@google.com (2024-11-06)

Hopefully we can call into a helper function to help us truncate these strings in a way that respects unicode well.

### al...@gmail.com (2024-11-20)

why status changed New ?


### dm...@google.com (2024-11-20)

Strongest candidate for fixing this in our UI is to call `base::TruncateUTF8ToByteSize`.

### dm...@google.com (2024-11-20)

Project is likely

- Find places where name is displayed
- See if views code gives us a good way to know the size of that area? Some of these helpful functions operate directly on pixel size?
- Or - just choose a specific # of characters?
- Or - maybe we can choose an ellide behavior in views? that would be amazing.

### fi...@google.com (2024-12-11)

Here's how this will look like, once the first two CLs are in...

### ap...@google.com (2024-12-11)

Project: chromium/src  

Branch: main  

Author: Finnur Thorarinsson <[finnur@chromium.org](mailto:finnur@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6089150>

[PWA]: Install/Uninstall -- wrap names that are too long.

---


Expand for full commit details
```
[PWA]: Install/Uninstall -- wrap names that are too long. 
 
The dialogs should be resilient to app names that are 
extra long. The decision was to allow app names to wrap 
to the next line, but to elide after that. 
 
This also includes minor UI polish, as directed by the UX 
team. 
 
Bug: 367401496, 383523099 
Change-Id: Ia86ede77bc6beca2991e1fa57e8231216e284bb0 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6089150 
Reviewed-by: Daniel Murphy <dmurph@chromium.org> 
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1395048}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_view.cc`
- M `chrome/browser/ui/views/web_apps/web_app_views_utils.cc`

---

Hash: c7bbe21415591042334587fab29a528ea864de1b  

Date:  Wed Dec 11 12:43:18 2024


---

### al...@gmail.com (2024-12-16)

After fixed this eligable for bounty ?

and if this report get CVE please add Reporter credit: Kang Ali of Punggawa Cybersecurity

Thanks

### fi...@google.com (2024-12-16)

I have submitted a fix. It can be backported, but I'm not sure it is worth doing so. Assigning back to martinkr to resolve that question (and the one in #13).

### ma...@google.com (2024-12-16)

For security issues (type=Vulnerability), we have automation that makes merge decisions for you once the issue Status is set to Fixed, based on the Severity and Found In labels. For low severity/S3 bugs, I think we typically don't merge fixes back.

Re [#comment13](https://issues.chromium.org/issues/367401496#comment13): The Chrome VRP panel will determine bounty eligibility and post a comment to this bug.

### sp...@google.com (2024-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-19)

Congratulations Kang Ali! Thank you for your efforts and reporting this (also amusing) issue to us.

### al...@gmail.com (2024-12-19)

Thank you for the reward and respect to the team for the fix.

This report plan CVE ?

### am...@chromium.org (2024-12-19)

CVEs are issued at the time a fix ships in a Stable channel update. [1] This is a low severity issue so the fix was not backmerged. It was landed on 133. The current release date for the 133 Stable milestone is 4 February, so it we would issue a CVE at that time.

[1] <https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#will-i-receive-a-cve-for-my-bug>

### al...@gmail.com (2024-12-19)

Oke 
Thanks for Bounty and CVE 



### am...@chromium.org (2025-01-09)

This was discovered to be a duplicate of an pre-existing report of this issue.

### ch...@google.com (2025-03-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/367401496)*
