# Security: Autofill prompt can be obscured by FedCM bubble dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [415838602](https://issues.chromium.org/issues/415838602) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Windows |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | yi...@chromium.org |
| **Created** | 2025-05-06 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

Similar to [issue 339481295](https://issues.chromium.org/issues/339481295)

1. Go to <https://lbstyle.github.io/autofill.html>
2. Click somewhere
3. Press down arrow, then press enter

# Problem Description

The Autofill prompt might be hidden under the permission dialog, making it non-interactive or invisible.

# Summary

Autofill prompt can be obscured by USB/Bluetooth permission prompt

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [autofill.html](attachments/autofill.html) (text/html, 4.1 KB)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 192.4 KB)

## Timeline

### dc...@chromium.org (2025-05-06)

I was able to reproduce this after a lot of trial and error. The repro instructions do not work for me as-is. In step 3, I need to press <down arrow>, <right arrow>, and then <enter> to repro.

Given the rather involved steps, I think I'd call this medium severity at best. Popping a permission dialog like this should unconditionally switch keyboard focus to the permission dialog.

For whoever ends up working on this, it seems the input focus is all over the place. For example, if I press <up arrow>, <up arrow>, <left arrow>, <enter> in step 3, I switch tabs (assuming the repro tab is the second tab).

### dc...@chromium.org (2025-05-06)

As far as I can tell, this repro is Windows-specific. On CrOS, input focus transitions to the permission dialog as expected. On Mac, input focus does not appear to transition to the permission dialog (pressing <enter> after clicking does not dismiss the dialog), but I was not able to trigger the autofill selector either.

### pe...@google.com (2025-05-06)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### dc...@chromium.org (2025-05-06)

reilly@, I've assigned this to you, but I suspect the fix may be should be in views somewhere to avoid getting a billion variations of these types of things in the future. Feel free to pass along as appropriate.

### re...@chromium.org (2025-05-06)

Assigning to the current device API owner to triage.

### ch...@google.com (2025-05-06)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-06)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@gmail.com (2025-05-12)

Thanks for the detailed repro steps! Just a heads-up — you don’t need to press the left or right arrow. Simply press the down arrow, wait about a second, then press Enter. That should trigger the issue as well.


### ch...@google.com (2025-05-21)

mattreynolds: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@gmail.com (2025-05-23)

Any update on this bug?

### ma...@chromium.org (2025-05-23)

autofill.html creates two chooser dialogs. The second chooser is created when the parent window is not active. In this case we call ShowInactive to show the chooser dialog, which causes the chooser to be shown without focus but still drawn on top of other bubbles (like autofill).

The chooser dialog is designed to always have focus and auto-dismiss when it loses focus. I think it should never be created without activating (always call Show, never ShowInactive). If the parent window isn't active then I think there are two reasonable options. Either use Show to focus the dialog, or skip showing the dialog. <https://crrev.com/c/6580551> implements the first option.

### ch...@gmail.com (2025-06-17)

Any update on the CL? Thanks!

### ch...@google.com (2025-06-18)

mattreynolds: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-07-09)

Project: chromium/src  

Branch: main  

Author: Matt Reynolds [mattreynolds@google.com](mailto:mattreynolds@google.com)  

Link:      <https://chromium-review.googlesource.com/6580551>

Always activate device dialogs when shown

---


Expand for full commit details
```
     
    Bug: 415838602 
    Change-Id: Ibd1c99010a675cce40b1cfb190a5effaba2d6fc8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6580551 
    Reviewed-by: Jack Hsieh <chengweih@chromium.org> 
    Reviewed-by: Florian Jacky <fjacky@chromium.org> 
    Commit-Queue: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1484530}

```

---

Files:

- M `chrome/browser/ui/views/permissions/chooser_bubble_ui.cc`

---

Hash: 40d2e9041e109b70d7b1fe35f3234d2b39584f8a  

Date:  Wed Jul 9 19:32:48 2025


---

### ch...@gmail.com (2025-07-09)

I just verified on Chromium 140.0.7287.0 (Build Revision: 1484632) on Windows 10, and it seems to be fixed.

Thanks for the fix!

### am...@chromium.org (2025-07-21)

Thank you for the report. Upon assessment, this issue does not meet the bar for a convincing UI spoof that could be realistically exploited: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#What-makes-a-UI-spoof-interesting-to-report>

Therefore, this report is unfortunately not eligible for a Chrome VRP reward.

### ch...@gmail.com (2025-07-21)

Thank you for reviewing my report.

I wanted to clarify an important detail:
The USB permission prompt is triggered twice — the first prompt disappears, and the second one stays visible at the exact moment the Autofill popup appears.

This is not just an accidental UI overlap — it seems intentionally timed to hide the Autofill prompt, making it invisible or non-interactive to the user as in issue 339481295. This could mislead users into thinking no Autofill suggestions were available or affect how they fill out sensitive fields.

Could you confirm whether this specific behavior was considered during triage? I’d appreciate any clarification on why it didn’t meet the reward threshold, so I can better understand the bar for future reports.

### ch...@google.com (2025-10-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/415838602)*
