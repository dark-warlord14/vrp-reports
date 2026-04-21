# User can still unknowingly allow Permission Prompt Hidden behind PiP during Interaction

| Field | Value |
|-------|-------|
| **Issue ID** | [373794472](https://issues.chromium.org/issues/373794472) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Permissions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | bk...@google.com |
| **Created** | 2024-10-16 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS
This issue is opened based on a previous issue, Bug 364508693, which does not seem to have been properly fixed. I hope the fix has landed, but when testing on the latest Chromium build 1369320, this issue is still reproducible, indicating that the fix did not completely address the problem.

VERSION
Chrome Version: 132.0.6780.0 (Developer Build) (64-bit)
Operating System: Windows 11

REPRODUCTION CASE
The steps to reproduce this issue are the same as those in Bug 364508693.

1. Download the attachment poc.html and permission.html files.
2. Host the page on a local server or open poc.html directly from the same folder.
3. Visit the webpage using the latest Chrome browser.
4. Click "Verify" and then "Start," press Tab three times, and confirm.
5. Press Enter twice and observe that the camera permission is unknowingly approved without the user's awareness.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/html, 5.1 KB)
- [permission.html](attachments/permission.html) (text/html, 1.5 KB)
- [new.mp4](attachments/new.mp4) (video/mp4, 1.7 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### fa...@gmail.com (2024-10-16)

Based on fixed issue: https://issues.chromium.org/issues/364508693

### pe...@google.com (2024-10-17)

Setting milestone because of s2 severity.

### pe...@google.com (2024-10-17)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-10-31)

steimel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-15)

steimel: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ja...@chromium.org (2025-02-06)

[secondary shepherd]

Hi steimel@, can you take a look and provide an update?

Thanks!

### dx...@google.com (2025-06-10)

Project: chromium/src  

Branch: main  

Author: Benjamin Keen [bkeen@google.com](mailto:bkeen@google.com)  

Link:      <https://chromium-review.googlesource.com/6614637>

Extend input protector to cover key events for permission prompts

---


Expand for full commit details
```
     
    This change extends input protector to also cover key events 
    (EventType::kKeyPressed and EventType::kKeyReleased) for permission 
    relevant prompts, in order to prevent unintentional key event actions. 
     
    Also disable input event protection for affected interactive tests that 
    perform automated button press. This is done to prevent the tests from 
    having to wait for the input protector timeout interval. 
     
    Bug: 364508693, 373794472, 416364499 
    Change-Id: I590074221366930c5af653554ae3d21d8191f883 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6614637 
    Reviewed-by: Mitsuru Oshima <oshima@chromium.org> 
    Reviewed-by: Keren Zhu <kerenzhu@chromium.org> 
    Reviewed-by: Florian Jacky <fjacky@chromium.org> 
    Reviewed-by: Lily Chen <chlily@chromium.org> 
    Commit-Queue: Benjamin Keen <bkeen@google.com> 
    Reviewed-by: Zachary Tan <tanzachary@chromium.org> 
    Reviewed-by: Luke Klimek <zgroza@chromium.org> 
    Reviewed-by: Slobodan Pejic <slobodan@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1472055}

```

---

Files:

- M `chrome/browser/smart_card/smart_card_permission_uitest.cc`
- M `chrome/browser/ui/ash/privacy_hub/geolocation_switch_interactive_uitest.cc`
- M `chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc`
- M `chrome/browser/ui/views/download/bubble/download_bubble_row_view_unittest.cc`
- M `chrome/browser/ui/views/payments/payment_sheet_view_controller.cc`
- M `chrome/browser/ui/views/permissions/embedded_permission_prompt_interactive_uitest.cc`
- M `chrome/browser/ui/views/permissions/exclusive_access_permission_prompt_interactive_uitest.cc`
- M `chrome/browser/ui/views/permissions/permission_prompt_base_view.cc`
- M `chrome/browser/ui/views/permissions/permission_rhs_indicators_interactive_uitest.cc`
- M `chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc`
- M `ui/views/bubble/bubble_frame_view.cc`
- M `ui/views/input_event_activation_protector.cc`
- M `ui/views/input_event_activation_protector.h`
- M `ui/views/test/mock_input_event_activation_protector.h`
- M `ui/views/window/dialog_client_view.cc`
- M `ui/views/window/dialog_client_view.h`
- M `ui/views/window/dialog_client_view_unittest.cc`

---

Hash: 08e1033b8bb5fe55f3147f116552bdcd5569fa50  

Date:  Tue Jun 10 21:08:05 2025


---

### bk...@google.com (2025-06-17)

<https://chromium-review.googlesource.com/6614637> landed on 139.0.7232.0 Canary. Issue should be fixed.

### ch...@google.com (2025-06-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### fa...@gmail.com (2025-06-17)

Hi, thank you for the CL. Could you please close this with Gerrit link to the CL that resolved the issue in the 'Fixed by code changes' field.

### sp...@google.com (2025-06-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
report of a lower impact UI spoofing issue that resulted in a beneficial change in Chrome


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-26)

Thank you for the report and your efforts reporting this to us. While we appreciate the effort, this is definitely a borderline issue that may not be considered a security issue in the future given the amount of user interaction preconditions. 
We recommend reviewing our considerations related to UI spoofs when researching future UI issues: https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#What-makes-a-UI-spoof-interesting-to-report

### ch...@google.com (2025-09-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of a lower impact UI spoofing issue that resulted in a beneficial change in Chrome

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/373794472)*
