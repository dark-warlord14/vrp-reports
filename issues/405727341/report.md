# clickjacking (enterjacking) download notification when a window.alert() is closed

| Field | Value |
|-------|-------|
| **Issue ID** | [405727341](https://issues.chromium.org/issues/405727341) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2025-03-24 |
| **Bounty** | $3,000.00 |

## Description

Security Bug

VULNERABILITY DETAILS
when opening a window alert() and at the same time the popup window is downloading a file and  window.alert() is closed the focus changes to the file that has been downloaded (download notification) this causes the file to be opened

VERSION
Chrome Version: Version 136.0.7084.0 (Official Build) canary (64-bit)
Operating System: Windows OS

REPRODUCTION CASE
1. open enterjack3.html
2. do enter 3-4 times fastly



CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- enterjack3.html (text/html, 1.1 KB)
- bandicam 2025-03-24 11-30-17-311.mp4 (video/mp4, 1.4 MB)
- bandicam 2025-10-16 10-02-11-145.mp4 (video/mp4, 1.2 MB)

## Timeline

### sr...@google.com (2025-03-24)

Your text in the video says "this is an evil executable". Can you show an example that actually gets code execution, like open a .bat file that opens the calculator or so?

### sa...@gmail.com (2025-03-24)

Hi  you can check this bug https://issues.chromium.org/issues/40927191 this is same but 40927191 affected on clickjacking. In 40927191 also open txt file if you want to run exe or bat file  just change on href to download exe file

### sa...@gmail.com (2025-03-24)

I think it needs to be run exe because you just change the href to mime exe or bat file and the impact is clear and other bugs also only display txt files. before you ask, have you tracked other bugs?

### pe...@google.com (2025-03-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### ts...@google.com (2025-03-24)

Assinging per owner of linked issue 40927191, probably another case where some delay is warranted before acting on a gesture.

### dx...@google.com (2025-10-14)

Project: chromium/src  

Branch:  main  

Author:  Lily Chen [chlily@chromium.org](mailto:chlily@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7041986>

Protect download bubble from unintended key events

---


Expand for full commit details
```
     
    This change considers key events when protecting the download bubble row 
    view from unintended user input. Clicking (or pressing Enter) on the 
    download bubble row view may result in opening a downloaded file. The 
    existing InputEventActivationProtector prevents clicks too soon after 
    showing the download bubble (500 ms). After this change, key events are 
    subject to the delay as well. 
     
    This is only a partial mitigation for a number of variants of 
    "enterjacking" on the download bubble, because the 500 ms delay may not 
    be sufficient to catch all unintended keypresses. 
     
    Bug: 392375329, 405727341, 421348748, 421877606 
    Change-Id: Ia6252f397966dd1d5cb539bf5c58f348effebadc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7041986 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Auto-Submit: Lily Chen <chlily@chromium.org> 
    Commit-Queue: Lily Chen <chlily@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1529740}

```

---

Files:

- M `chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc`

---

Hash: [8be46d66315fc47df5634d7cface5b62d7673b26](https://chromiumdash.appspot.com/commit/8be46d66315fc47df5634d7cface5b62d7673b26)  

Date: Tue Oct 14 20:12:42 2025


---

### sa...@gmail.com (2025-10-16)

I confirm this bug has been fixed. There was a delay when the file was about to be opened so the user could cancel it. I reproduced it in Version 143.0.7473.0 (Official Build) canary (64-bit)

### ch...@chromium.org (2025-10-16)

Thanks for confirming

### sp...@google.com (2025-10-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Security UI spoofing baseline - lower impact


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Security UI spoofing baseline - lower impact

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/405727341)*
