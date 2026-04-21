# Security: Bypass about:blank#blocked In Drag & Drop

| Field | Value |
|-------|-------|
| **Issue ID** | [40068570](https://issues.chromium.org/issues/40068570) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>DataTransfer, UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pu...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2023-08-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

In Chrome If Drag Links Such as file:/// , chrome://settings/ etc...

Chrome replaces the file URI , chrome://settings/ with about:blank#blocked.

Attacker Can Bypass about:blank#blocked Now, While using Drag & Drop

**VERSION**  

Chrome Version: [115.0.5790.110] + [stable]  

Operating System: [Microsoft Windows 10]

**REPRODUCTION CASE**

1. Open Pufindex.html
2. Select Lock Emoji
3. Drag to New Tab  
   
   Done

**CREDIT INFORMATION**  

Reporter credit: [P Umar Farooq]

## Attachments

- Chrome File URL.mp4 (video/mp4, 915.9 KB)
- Chrome Links.mp4 (video/mp4, 652.5 KB)
- [PufIndex.html](attachments/PufIndex.html) (text/plain, 578 B)
- Image Drag.mp4 (video/mp4, 398.9 KB)
- PufImgIndex.html (text/plain, 232 B)
- [Latest Reproduce.mp4](attachments/Latest Reproduce.mp4) (video/mp4, 169.6 KB)

## Timeline

### [Deleted User] (2023-08-02)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-08-02)

Repro'd on linux m114 (extended stable) and m117 (ToT). Exact steps are:
1. doubleclick on lock emoji
2. drag lock emoji to omnibox
3. hit enter

Generally, we prevent clicking on such links or pasting of javascript into the omnibox to limit social-engineering, and it feels like we should block this, too, but this might be operating as intended. esp. since it seems I had to hit enter to begin navigation (reporter: let us know if your repro did not require this).

Over to usable security folks for an opinion on whether we should address this.





[Monorail components: Blink>DataTransfer UI>Browser>Omnibox]

### [Deleted User] (2023-08-02)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-08-02)

No Need to Hit Enter 

We Can Just drag This to New Tab 

& We Can Do Same with Image So No Double Click on Emoji too 

### pu...@gmail.com (2023-08-02)

In this New Update We Can Just Directly Drag image to New Tab to Open chrome://settings/ , file:/// etc.

Normally, browsers block certain actions, like navigating to a restricted internal URL (e.g.,  chrome://settings/), if they're initiated by a script or other untrusted methods. The about:blank#blocked page is the browser's way of telling you that an attempted navigation was blocked for security reasons.

 ability to bypass about:blank#blocked could be used to gain unauthorized access to browser-specific URLs like chrome://settings/ or about:downloads. While direct data theft from these pages is unlikely, it could be used to manipulate browser settings or gather information about the user's Browse habits, which can be leveraged for further attacks.

Reproduce:
1. Open PufImg.html
2. Drag Image to New Tab
Done..

Thank you

### pu...@gmail.com (2023-08-02)

Reproduce:
1. Open PufImgindex.html
2. Drag Image to New Tab [ + ]
Execute Done :]

### [Deleted User] (2023-08-03)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-03)

This issue was migrated from crbug.com/chromium/1469599?no_tracker_redirect=1

[Multiple monorail components: Blink>DataTransfer, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

### pu...@gmail.com (2024-09-10)

Friendly ping: any updates

Thanks!

### pu...@gmail.com (2025-07-17)

Hi Team

This Vulnerability Fixed through this bug & CL

<https://chromium-review.googlesource.com/c/chromium/src/+/6428889>

<https://issues.chromium.org/issues/342579972>

### pu...@gmail.com (2025-07-17)

Kindly Update Status to Fixed

### pu...@gmail.com (2025-07-22)

Hi Team

This Vulnerability Fixed through this bug & CL

<https://chromium-review.googlesource.com/c/chromium/src/+/6428889>

<https://issues.chromium.org/issues/342579972>

### pu...@gmail.com (2025-07-29)

Hi Team

This Vulnerability Fixed through this bug & CL

<https://chromium-review.googlesource.com/c/chromium/src/+/6428889>

<https://issues.chromium.org/issues/342579972>

### pu...@gmail.com (2025-08-01)

I have Verified this issue is resolved I have Attached latest reproduce video

Thank you

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### pu...@gmail.com (2025-08-28)

Thank you ❤️

### ch...@google.com (2025-11-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact exploitation mitigation bypass

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068570)*
