# Security: Chrome desktop on MacOS allows websites to access a folder contains system files

| Field | Value |
|-------|-------|
| **Issue ID** | [40910758](https://issues.chromium.org/issues/40910758) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Mac |
| **Reporter** | du...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2023-05-05 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

Chrome desktop on MacOS allows websites to access a folder contains system files.

**VERSION**  

Chrome Version: 112.0.5615.137 (Official Build) (arm64) + [stable]  

Operating System: macOS Ventura 13.3.1 (a)

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

Load the demo website:

<https://web.dev/patterns/files/open-a-directory/demo.html>

Pick Downloads, Desktop, Document folders on Mac: the website is blocked by Chrome to access these folders as they are restricted folders on the OS (described at: <https://support.apple.com/en-vn/guide/security/secddd1d86a6/web>).

Pick iCloud Drive: the website is allowed by Chrome to access iCloud Drive while this also is a restricted storage on macOS (described at: <https://support.apple.com/en-vn/guide/security/secddd1d86a6/web>).

A short video of demonstration: <https://drive.google.com/file/d/18IUlIkrjlmBma4RVCo5SEAht8IdmmV39/view?usp=sharing>.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Khiem Tran (@duckhiem)

## Timeline

### [Deleted User] (2023-05-05)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-05-05)

I think this is just a logical bug so fixing it or not depends on your plan for Chrome on macOS. 

Best,

Khiem Tran

### do...@chromium.org (2023-05-05)

I'm not sure this is a security bug - it's Apple's call as to whether the directory is restricted or not. cc filesystem folks to follow up.

[Monorail components: Blink>Storage>FileSystem]

### do...@chromium.org (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-05-05)

There is a line in the link: https://support.apple.com/en-vn/guide/security/secddd1d86a6/web:

"... this model is enforced by the system to help ensure that all apps must obtain user consent before accessing files in Documents, Downloads, Desktop, iCloud Drive, ..."

But it is Chrome's decision to consider it or not as Chrome is currently not an app from the App Store.

### as...@chromium.org (2023-05-05)

Our intention is to allow access to iCloud Drive in the same way that we give access to Documents and Downloads; i.e. we should avoid giving access to the directory itself, but allow access to sub-files and -folders

That being said, we're currently expecting iCloud Drive to live at "~/Library/Mobile Documents" whereas the video shows the picker at what I believe is "~/Library/Mobile Documents/com~apple~CloudDocs/". So that should be fixed, but it's still not a security issue IMHO

https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc;l=312-314;drc=e0e0d24aaa54727dc0a8bc4b159ccdf80d3f5d8d



### do...@chromium.org (2023-05-08)

I think I concur with #7 that this isn't a security bug. I'll remove this from the security queue.

### as...@chromium.org (2023-05-08)

FWIW I have a WIP CL to block direct access to "~/Library/Mobile Documents/com~apple~CloudDocs/" as well https://crrev.com/c/4509234

### gi...@appspot.gserviceaccount.com (2023-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f93a19c2db0f8c4227d478a997bdd6dcc38710dc

commit f93a19c2db0f8c4227d478a997bdd6dcc38710dc
Author: Austin Sullivan <asully@chromium.org>
Date: Mon May 08 19:18:29 2023

FSA: Update iCloud Drive blocklist rule

We should block direct access to not just ~/Library/Mobile Documents
but also ~/Library/Mobile Documents/com~apple~CloudDocs/

Accessing children of these directories is okay

Bug: 1442789
Change-Id: Iadfddcee18c2bf613d164c46584870f68cb102f6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4509234
Auto-Submit: Austin Sullivan <asully@chromium.org>
Commit-Queue: Daseul Lee <dslee@chromium.org>
Reviewed-by: Daseul Lee <dslee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1141002}

[modify] https://crrev.com/f93a19c2db0f8c4227d478a997bdd6dcc38710dc/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/f93a19c2db0f8c4227d478a997bdd6dcc38710dc/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc


### as...@chromium.org (2023-05-08)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-05-09)

Despite the title of this report "Chrome desktop on MacOS allows websites to access a folder contains system files", the description of the revision "We should block direct access to not just ~/Library/Mobile Documents
but also ~/Library/Mobile Documents/com~apple~CloudDocs/" lets me know that this report should have a tiny reward :), as it helped add one item in the blocklist ;).

Just my 2 cents :">.

Best regards,

Khiem Tran

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-19)

Hello Khiem! Thank you for this report. As mentioned, we do not considerer this to be a security bug, but since this did allow us to land a change to block unnecessary directory access, we would like to extend a thank you reward to show our appreciating for taking the time to find and report this issue to us! 

### du...@gmail.com (2023-05-19)

Hello Amy, thank you for that!

I will contribute more.

Best,

Khiem

### am...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-05-30)

A friendly ping as the finance team doesn't contact me yet :">.

### am...@chromium.org (2023-05-30)

Thanks reaching out. You were already enrolled in the Google payments system, so they did not need to contact you directly. Your reward payment has already been processed by finance and approved. You should payment sometime within the next week or so, depending on your financial institution. 

### du...@gmail.com (2023-05-31)

Thank you very much for your time and your kindness!

### [Deleted User] (2023-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-15)

This issue was migrated from crbug.com/chromium/1442789?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### du...@gmail.com (2025-01-20)

deleted

### am...@chromium.org (2025-01-20)

It has come to our attention that your are spamming report comments, such as with your email address or other comments unrelated to the bug. We must kindly remind request you please stop this behavior as comments should be used only to make relevant technical updates to a bug or its resolution.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40910758)*
