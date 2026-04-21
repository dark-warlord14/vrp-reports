# Security:  opens a new window at the same time as the previous window in fullscreen mode, (the window enters fullscreen mode which is closed by another new window) leads to spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40074800](https://issues.chromium.org/issues/40074800) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Fullscreen |
| **Platforms** | Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2023-10-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

I found a bar spoofing vulnerability, when a window opens in fullscreen mode and opens a new window at same time what happens is that it immediately exits fullscreen mode.  

However, this does not happen when opening an open window and redirecting to download files using the "open link in new window" menu. when you open a new window at the same time as fullscreen mode with "open link in new window" what happens is you open a new window and then download the file and a fullscreen notification will appear and the previous window goes into fullscreen mode  

The impact is that the victim thinks that the full screen notification comes from a new open window and not from the previous window because the focus is on the new open window. and this causes address bar spoofing in the previous window

**VERSION**  

Chrome Version: Version 120.0.6051.2 (Official Build) dev (64-bit)  

Operating System: Windows

**REPRODUCTION CASE**

1. open downloadspoofbar.html
2. right click on redirect link and choose "open link in new window"

**CREDIT INFORMATION**  

Reporter credit: Hafiizh (<https://www.linkedin.com/in/hafiizh-7aa6bb31/>)

## Attachments

- [bandicam 2023-10-13 13-19-17-377.mp4](attachments/bandicam 2023-10-13 13-19-17-377.mp4) (video/mp4, 4.0 MB)
- [downloadspoofbar.html](attachments/downloadspoofbar.html) (text/plain, 628 B)
- [bandicam 2023-10-17 07-10-46-335.mp4](attachments/bandicam 2023-10-17 07-10-46-335.mp4) (video/mp4, 2.1 MB)
- [bandicam 2024-12-16 09-34-46-158.mp4](attachments/bandicam 2024-12-16 09-34-46-158.mp4) (video/mp4, 1.5 MB)
- [bandicam 2024-12-16 09-34-46-158.mp4](attachments/bandicam 2024-12-16 09-34-46-158.mp4) (video/mp4, 1.5 MB)

## Timeline

### [Deleted User] (2023-10-13)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-10-16)

if it fails to reproduce the poc just repeat the poc

### ct...@chromium.org (2023-10-16)

msw@ could you take a look for Fullscreen? This seems somewhat similar to https://crbug.com/chromium/1463943. This requires some user interaction but the timing aspect seems automated (and could plausibly be made more robust) as the two actions can be triggered by the page simultaneously. This is a bit noisy, but does fully hide the fullscreen notice, so conservatively marking this as Severity-Medium.

Reporter: Are you able to reproduce this on other channels, such as Stable (M-118)?

[Monorail components: Blink>Fullscreen]

### sa...@gmail.com (2023-10-17)

yes i can reproduce in Stable (M-118)

### sa...@gmail.com (2023-10-17)

[Empty comment from Monorail migration]

### mf...@chromium.org (2023-10-17)

Similar question as the other bug, was multi-screen window placement part of this report?

### ct...@chromium.org (2023-10-17)

No, this is using regular fullscreen, but obscuring the fullscreen notice (like the other report).

### mf...@chromium.org (2023-10-17)

=> takumif@

### ms...@chromium.org (2023-10-17)

Interesting. Some offhand ideas:
(1) Close context menus when fullscreen is triggered. (like Firefox)
(2) Make context-menu triggering input events not grant user activation? (that may break other stuff...)
(3) Do not hide the fullscreen exit bubble until the underlying fullscreen OS window is activated?
(4) Do not z-order the exit bubble over other windows? (like Firefox, that likely causes other issues)
(5) Block fullscreen requests when "requesting element is not in the currently focused tab." (like Firefox, likely breaks valid fullscreen delegation use cases)

### am...@chromium.org (2023-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-27)

takumif: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-10)

takumif: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2023-11-23)

Hello any updates?

### sa...@gmail.com (2023-12-06)

Hello any updates? 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### sa...@gmail.com (2024-02-01)

Helo any updates?

### is...@google.com (2024-02-01)

This issue was migrated from crbug.com/chromium/1492397?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### sa...@gmail.com (2024-03-18)

hello any updates?

### sa...@gmail.com (2024-06-05)

Hello any updates?

### sa...@gmail.com (2024-07-02)

hello any updates?

### sa...@gmail.com (2024-08-02)

hello any updates?

### ta...@google.com (2024-09-09)

=> muyaoxu@

### sa...@gmail.com (2024-10-08)

hello any updates?

### sa...@gmail.com (2024-12-16)

is this bug fixed because i can't reproduce this bug on Version 133.0.6898.1 (Official Build) canary-dcheck (64-bit). when a new window is opened along with the window behind it fullscreen mode auto focus changes to the window behind it (fullscreen mode)

### sa...@gmail.com (2025-03-26)

hello this bug fixed because i can't reproduce this bug on Version 133.0.6898.1 (Official Build) canary-dcheck (64-bit). when a new window is opened along with the window behind it fullscreen mode auto focus changes to the window behind it (fullscreen mode).  Can you set this bug to fixed?

### ch...@google.com (2025-10-30)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dr...@chromium.org (2025-11-04)

Given this was reported fixed in M133, there's no value in identifying the fixing CL. Setting Fixed By Code Changes to NA and closing again.

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Security UI spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Security UI spoofing

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074800)*
