# Extensions can open chrome-untrusted:// URLs with identity.launchWebAuthFlow

| Field | Value |
|-------|-------|
| **Issue ID** | [40067152](https://issues.chromium.org/issues/40067152) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-10 |
| **Bounty** | $750.00 |

## Description

**Steps to reproduce the problem:**

1. Try the following code from an extension with the "identity" permission:

chrome.windows.create({url:"chrome-untrusted://crosh/html/crosh.html"})

chrome.identity.launchWebAuthFlow({  

url:"chrome-untrusted://crosh/html/crosh.html",  

interactive:true  

})

2. Note how windows.create fails but identity.launchWebAuthFlow does not.

**Problem Description:**  

Using the bug from <https://crbug.com/1461895> (now fixed but not in stable yet), I can gain root access on a Chromebook with dev mode on. All the user has to do is open inspect on a certain page and I can use `history.back()` to get back to crosh and execute my commands. The extension I used to do this is attached below.

**Additional Comments:**  

I've also attached a video of the root POC below.

\*\*Chrome version: \*\* 117.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Chrome OS

## Attachments

- [crosh_root_extension_poc.zip](attachments/crosh_root_extension_poc.zip) (application/octet-stream, 1.4 KB)
- [getting_root_from_extension.mp4](attachments/getting_root_from_extension.mp4) (video/mp4, 924.9 KB)
- [basicbug.mp4](attachments/basicbug.mp4) (video/mp4, 487.2 KB)

## Timeline

### [Deleted User] (2023-07-10)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-10)

And here's a video of the basic POC:

### ma...@gmail.com (2023-07-10)

[Comment Deleted]

### pa...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-11)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/290733700). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/290733700]

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-11)

[Comment Deleted]

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-01)

Project: chromium/src
Branch: main

commit 66224c5ed5bd62d598ff40f2abacf21191b035e2
Author: Ryan Sultanem <rsult@google.com>
Date:   Thu Jul 20 12:14:18 2023

    [LaunchWebAuthFlow] Restrict auth urls to have an http/s:// scheme
   
    Bug: b/290733700
    Change-Id: I76cfa73d8109036fbaeca2897aeaacc40cdb5334
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4700767
    Reviewed-by: Alex Ilin <alexilin@chromium.org>
    Commit-Queue: Ryan Sultanem <rsult@google.com>
    Cr-Commit-Position: refs/heads/main@{#1172902}

M       chrome/browser/extensions/api/identity/identity_apitest.cc
M       chrome/browser/extensions/api/identity/identity_constants.cc
M       chrome/browser/extensions/api/identity/identity_constants.h
M       chrome/browser/extensions/api/identity/identity_launch_web_auth_flow_function.cc
M       chrome/browser/extensions/api/identity/identity_launch_web_auth_flow_function.h
M       tools/metrics/histograms/enums.xml

https://chromium-review.googlesource.com/4700767
14:15
14:15
CLs: Merged:​<none>      crrev/c/4700767
CLs: Pending:​crrev/c/4700767      <none>

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-08-05)

Reporter credit for this bug is "Derin Eryilmaz" by the way.

### st...@google.com (2023-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-23)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-26)

Congratulations! 
The VRP Panel has decided to award you $750 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### ch...@google.com (2023-10-26)

Dear Reporter,

Can you please tell us your desired credit-name? --> e.g. mathia.is.fun

### ma...@gmail.com (2023-10-26)

"Derin Eryilmaz" is my desired credit name. Thanks you

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-07)

This issue was migrated from crbug.com/chromium/1463447?no_tracker_redirect=1

[Monorail blocking: b/290733700]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067152)*
