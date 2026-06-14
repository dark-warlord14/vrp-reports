# UAF in BrowserView

| Field | Value |
|-------|-------|
| **Issue ID** | [325697537](https://issues.chromium.org/issues/325697537) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | xi...@google.com |
| **Created** | 2024-02-17 |
| **Bounty** | $4,000.00 |

## Description

VULNERABILITY DETAILS

This is a UAF in view. Root cause analysis coming soon.

## Bisect

By analyzing the required feature and the manual reproduction bisect, this UAF is introduced in the commit 

https://chromium-review.googlesource.com/c/chromium/src/+/5241404


VERSION
Chrome Version: [122.0.6260.0] + [canary]
Operating System: [macOS]

REPRODUCTION CASE

Load the attached extension to reproduce:

./Chromium.app/Contents/MacOS/Chromium --enable-features=DataCollectionModeForScreen2x --load-extension=/path/to/ext



FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [browser]
Crash State: [UAF]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [ret2happy]

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 25.8 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [325697537.mp4](attachments/325697537.mp4) (video/mp4, 10.5 MB)
- [poc.html](attachments/poc.html) (text/html, 309 B)
- [asan2.txt](attachments/asan2.txt) (text/plain, 24.7 KB)
- [manifest.json](attachments/manifest.json) (application/json, 191 B)
- [background.js](attachments/background.js) (text/javascript, 221 B)

## Timeline

### he...@gmail.com (2024-02-17)

redacted

### he...@gmail.com (2024-02-17)

redacted

### dr...@chromium.org (2024-02-19)

[security shepherd] I'm not able to reproduce this, but based on the PoC I'm guessing it's quite racy. I'm triaging assuming everything reproduces exactly as claimed. Hopefully the DataCollectionModeForScreen2x owners are able to make more progress here.

A UAF with no gestures would normally be a Critical, but based on the current raciness I'm going to mark it High.

### dr...@chromium.org (2024-02-19)

mschillaci@ - can you take a look?

### ms...@google.com (2024-02-20)

-me

Adding original CL author/reviewers, and some Mac folks.

### pe...@google.com (2024-02-20)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-02-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### he...@gmail.com (2024-02-22)

Attach the reproduction video on the 124.0.6315.0 chroimum. Both original attached PoC do not need raciness and is stable for me to reproduce it with 100% success rate.

### ap...@google.com (2024-02-22)

Project: chromium/src
Branch: main

commit b1630471ef8cf06f96172cce9fd2ee0d80eb9c5b
Author: Xiang Xiao <xiangxiao@google.com>
Date:   Thu Feb 22 21:59:54 2024

    Address an UAF issue potentially caused by the loader pointer.
    
    Bug: 325697537
    Change-Id: I11991152a644a099831de73ba356b3330da07ae8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5318584
    Reviewed-by: Abigail Klein <abigailbklein@google.com>
    Commit-Queue: Xiang Xiao <xiangxiao@google.com>
    Cr-Commit-Position: refs/heads/main@{#1264250}

M       chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.cc

https://chromium-review.googlesource.com/5318584


### he...@gmail.com (2024-02-28)

Thanks for the fix. I could verify that this is fixed.

Feel free to mark this as fixed. Thank you.

### am...@chromium.org (2024-03-05)

re-uploading the content in [comment #3](https://issues.chromium.org/issues/325697537#comment3) that is marked as restricted

### am...@chromium.org (2024-03-05)

This issue looks like it has a requirement of a command line flag to trigger so I've updated SI- from Extended to None, please let me know (or feel free to change) if that is incorrect

### am...@google.com (2024-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-07)

Congratulations! The Chrome VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug, mitigated by race (and in this presentation of the issue to open the tabs necessary to trigger this issue -- an extension), + $1,000 bisect bonus. Thank you for your efforts in reporting this issue to us!

### he...@gmail.com (2024-03-07)

Hello, I see that the baseline for issue requied for extension is $5000 or $7000, I'm not sure why this is below that baseline so much.

Moreover, the race is negligent for triggering it. The attached PoC achieve 100% success rate to trigger this UAF. You could cc other devs to reproduce it. Besides, I attached a renderer PoC which demonstrate that using a web page could directly trigger this UAF,  which should be a critical issue and is the additional renderer bonus  for browser UAF considered? (by opening the tab using the js code and trigger the UAF **STABLY**, this is not mitigated in the realworld exploitation).

Thank you very much.

### am...@chromium.org (2024-03-07)

Hi, thanks for reaching out with your questions.
Reward amounts are based on bug class and impact, mitigation, and report quality. Considering that this issue is mitigated by either fairly significant race condition or extension, and is a baseline quality report. We are happy to take another look, but we were also fairly certain this issue would have been discovered before this feature was launched.

Issues that are mitigated are not considered for the renderer RCE bonus.
The requirement of an extension to reliably reproduce and trigger this issue is considered a mitigation.

### he...@gmail.com (2024-03-08)

deleted

### pe...@google.com (2024-06-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/325697537)*
