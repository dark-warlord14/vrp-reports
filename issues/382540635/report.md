# Extension popup can appear over WebUSB permission prompt

| Field | Value |
|-------|-------|
| **Issue ID** | [382540635](https://issues.chromium.org/issues/382540635) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 133.0.6879.0 (Official Build) canary (64-bit) (cohort: Clang-64)  |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2024-12-06 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Install attached extension
2. Click anywhere, then Press Ctrl+A

# Problem Description

Similar to [issue 361711121](https://issues.chromium.org/issues/361711121)

# Summary

Extension popup can appear over WebUSB permission prompt

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [bg-keyboard.js](attachments/bg-keyboard.js) (text/javascript, 1.4 KB)
- [manifest.json](attachments/manifest.json) (application/json, 494 B)
- [popup.html](attachments/popup.html) (text/html, 1.5 KB)
- [popup-screenshare.html](attachments/popup-screenshare.html) (text/html, 430 B)
- [screen-capture.webm](attachments/screen-capture.webm) (video/webm, 2.7 MB)

## Timeline

### dr...@chromium.org (2024-12-06)

[security triage] My test machine doesn't have any WebUSB-accessible devices, but this looks very plausible. kerenzhu@ - can you take a look at this one too?

### ch...@gmail.com (2024-12-06)

Note: I don't repro this on Linux. 

### pe...@google.com (2024-12-07)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@gmail.com (2025-01-28)

The problem here is that WebUSB permission prompt displays twice.

### ke...@chromium.org (2025-01-28)

The WebUSB permission prompt should always stays above the extension bubble. This was already done for location permission prompt bubble and others via [Widget::SetZOrderSublevel()](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permissions/permission_prompt_bubble_base_view.cc;l=194;drc=27d34700b83f381c62e3a348de2e6dfdc08364b8).

### ap...@google.com (2025-01-28)

Project: chromium/src  

Branch: main  

Author: Keren Zhu <[kerenzhu@chromium.org](mailto:kerenzhu@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6204583>

Set a higher z-order sublevel for the permission chooser bubble

---


Expand for full commit details
```
Set a higher z-order sublevel for the permission chooser bubble 
 
This change prevents the permission chooser bubble from being occluded 
by the extension bubble. This permission bubble is used to choose WebUSB 
device, etc. 
 
Bug: 382540635 
Change-Id: Ib6aa62e7342fa475cc89d12fe3e9abe1439b47ef 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6204583 
Reviewed-by: Caroline Rising <corising@chromium.org> 
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com> 
Auto-Submit: Keren Zhu <kerenzhu@chromium.org> 
Commit-Queue: Caroline Rising <corising@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1412341}

```

---

Files:

- M `chrome/browser/ui/views/permissions/chooser_bubble_ui.cc`

---

Hash: 59f1d4281a72b19732f63b3232d7c31340ba857d  

Date:  Tue Jan 28 09:13:13 2025


---

### sp...@google.com (2025-02-20)

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

### am...@chromium.org (2025-02-20)

Congratulations Khalil! Thank you for your efforts and reporting this issue to us.

### ch...@google.com (2025-05-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/382540635)*
