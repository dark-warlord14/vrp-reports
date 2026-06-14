# Security: Heap-use-after-free in WebRTCInternals::EnableLocalEventLogRecordings

| Field | Value |
|-------|-------|
| **Issue ID** | [40059367](https://issues.chromium.org/issues/40059367) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>WebRTC |
| **Platforms** | ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-04-13 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

1. download and unzip chromeos: asan-linux-release-991857.zip
2. ./chrome and open 'chrome://webrtc-internals'
3. open devtools and input chrome.send('enableEventLogRecordings');chrome.send('enableEventLogRecordings');
4. click save

**Problem Description:**  

This is similar to <https://chromium-review.googlesource.com/c/chromium/src/+/3546821/> and <https://chromium-review.googlesource.com/c/chromium/src/+/3577755>  

You should check whether the dialog is already shown.

**Additional Comments:**

\*\*Chrome version: \*\* 99.0.4844.74 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 21.4 KB)

## Timeline

### dt...@chromium.org (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-04-13)

This is presumably the exact same as https://crbug.com/1315863. ashleydp@ PTAL at this one as well?

[Monorail components: OS>Systems>Diagnostics]

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### as...@google.com (2022-04-13)

Does look like a duplicate.

eladalon@/hbos@ - Can you PTAL at this one as well? Thanks.

[Monorail components: -OS>Systems>Diagnostics Blink>WebRTC]

### hb...@chromium.org (2022-04-14)

Logs and recordings? Can you take a look Elad?

### me...@gmail.com (2022-05-03)

Any updates?

### el...@chromium.org (2022-05-03)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-05-03)

I've uploaded this CL for it:
https://chromium-review.googlesource.com/c/chromium/src/+/3623662

I don't see how it's exploitable, though. Applications cannot call `chrome.send()`. Is the idea that a hijacked render process could initiate this message?

### el...@chromium.org (2022-05-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/67ac27bc42cb9084c52dcf203c19a936375a0324

commit 67ac27bc42cb9084c52dcf203c19a936375a0324
Author: Elad Alon <eladalon@chromium.org>
Date: Tue May 03 15:30:26 2022

Soft-fail if WebRTCInternals::select_file_dialog_ set

Instead of DCHECKing that it's not set, soft-fail if it's
already set.

Bug: 1315863, 1315864
Change-Id: I65d54a7a01a41f8dbf0fbc7061cd10f8d6057ab3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3623662
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Elad Alon <eladalon@chromium.org>
Auto-Submit: Elad Alon <eladalon@chromium.org>
Cr-Commit-Position: refs/heads/main@{#998876}

[modify] https://crrev.com/67ac27bc42cb9084c52dcf203c19a936375a0324/content/browser/webrtc/webrtc_internals.cc


### el...@chromium.org (2022-05-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-05)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-06-01)

[Comment Deleted]

### am...@chromium.org (2022-06-21)

Hello, this issue does not appear to be exploitable, and would not be considered a security bug, therefore, unfortunately cannot be issued a CVE and is not eligible for a VRP reward. If you are able to explain or demonstrate exploitability, we would happily reassess this issue as a security bug. 

In the meantime, removing security labels. Will leave this issue as RV-SN in the interim keep this view restricted to provide the researcher time to respond with feedback or new information. 

### me...@gmail.com (2022-06-22)

[Comment Deleted]

### me...@gmail.com (2022-06-22)

[Comment Deleted]

### me...@gmail.com (2022-06-23)

[Comment Deleted]

### me...@gmail.com (2022-06-23)

[Comment Deleted]

### me...@gmail.com (2022-06-23)

[Comment Deleted]

### me...@gmail.com (2022-06-24)

[Comment Deleted]

### am...@chromium.org (2022-06-27)

Hello, apologies as I was out of office the latter half of last week. This does not appear to be exploitable based on reachability by applications as per https://crbug.com/chromium/1315864#c9. If you can figure out a way to exploit this issue, we would appreciate that information and this could be reassessed as a potential security issue. 

### me...@gmail.com (2022-06-28)

[Comment Deleted]

### me...@gmail.com (2022-07-07)

[Comment Deleted]

### me...@gmail.com (2022-07-07)

[Comment Deleted]

### am...@chromium.org (2022-07-08)

Hello, thanks for the additional information and your patience. I responded again in https://crbug.com/chromium/1315864#c23, so I don't understand your the question about "any reply" in https://crbug.com/chromium/1315864#c25. The reward-topanel label is on this bug, it will still be evaluated as a potential security issue and VRP reward during VRP Panel. 

>>>My poc and video has proved that this is reachable. 
I do not see a POC or video in this report. If you would be kind enough to point me to that, I'd be happy to evaluate. Please understand, I cannot immediately respond. There are many security bugs to evaluate and address, and I cannot always respond immediately to each response. :) 
Also, it is Friday, so I'm not likely to respond over the weekend. 

This does not mean that all WebUI bugs are not considered security bugs; however, bugs that are not remote exploitable or web accessible, such as these that require direct user interaction, are considered some mitigated and with a lower exploitability potential. If a security bug requires implausible user interaction, it may not be eligible for a VRP reward or considered a security bug. This had not been evaluated for a potential VRP reward as of yet. 

At the time of my https://crbug.com/chromium/1315864#c19, your report solely consisted of repro steps requiring direct user interaction with DevTools and directly inputting JS, including a call to `chrome.send()` which, based on https://crbug.com/chromium/1315864#c9 should not be reachable by applications. I'm not webRTC expert so I'm included to trust the dev on this one with quick evaluation. 

Since such you're provided additional information and we have yet to evaluate this as a panel. This will happen in the near future.
In the meantime, if you can point us to your POC and video for this issue, that would be greatly appreciated. 



### me...@gmail.com (2022-07-09)

[Comment Deleted]

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. The reward amount was decided based on this issue being not web accessible and very heavily mitigated with a low potential for exploitation. Thank you for your efforts in reporting this issue to us and your patience with communications and getting to it in a VRP Panel session. 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-10)

This issue was migrated from crbug.com/chromium/1315864?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1315863]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059367)*
