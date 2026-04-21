# Security: Page can obtain autofill data with two consecutive taps with minimal user awareness, bypasses issue 1240472 and issue 1279268 fixes

| Field | Value |
|-------|-------|
| **Issue ID** | [40060134](https://issues.chromium.org/issues/40060134) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Privacy |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | jk...@google.com |
| **Created** | 2022-07-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A page can make a user select an autofill item with two consecutive taps with minimal or no user awareness.

Normally Chrome requires an intentional selection by the user and clear user awareness to select an autofill item.

This bypasses fixes from <https://crbug.com/chromium/1240472> and <https://crbug.com/chromium/1279268>, since those fixes only impact mouse events, not tap events. Those two reports also contain more context.

I've tested this with addresses (which includes name + email) and credit cards. For sample input, see the video recording.

OnGestureEvent() which calls SetSelectedLine() does not have the protections implemented in both issues above:  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc;l=716;drc=bd37e17b610b6113621a2e593f4e90669b47edf2>

**VERSION**  

Chrome Version: 103.0.5060.66 (Official Build) (64-bit) (cohort: Stable Installs & Version Pins), 105.0.5154.2 Canary  

Operating System: Windows 10 Version 21H2 (Build 19044.1706)

**REPRODUCTION CASE**  

PoC for address:  

Prerequisites: Touchscreen device + have at least one address in chrome://settings/addresses

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-two-taps.html>
2. Tap the same place twice in a row, anywhere in the page.

PoC for credit card:  

Prerequisites: Touchscreen device + have at least one credit card in chrome://settings/payments

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-two-taps.html?creditcard>
2. (Same as prior PoC, tap twice in a row)

For all PoCs:  

Observed: Autofilled data is provided to page, because browser does not enforce delay from <https://crbug.com/chromium/1279268> fix on tap events.  

Expected: Autofilled data is \*not\* provided to page, because browser enforces delay from <https://crbug.com/chromium/1279268> fix on tap events.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [autofill-two-taps.mp4](attachments/autofill-two-taps.mp4) (video/mp4, 183.2 KB)
- [autofill-two-taps.html](attachments/autofill-two-taps.html) (text/plain, 3.0 KB)

## Timeline

### [Deleted User] (2022-07-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-05)

Assigning the same things here as https://bugs.chromium.org/p/chromium/issues/detail?id=1279268

[Monorail components: Privacy UI>Browser>Autofill>UI]

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-16)

schwering: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-31)

schwering: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-11-29)

Friendly ping: Any updates on this issue? Still repros in 107.0.5304.107 Stable. No updates since triage in July.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ba...@chromium.org (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### sc...@google.com (2023-02-16)

Vidhan, I think you fixed a similar bug recently. Could you take a look?

### sc...@google.com (2023-02-16)

Vidhan, I think you fixed a similar bug recently. Could you take a look?


### ba...@chromium.org (2023-02-17)

+Jan who worked on something similar.

### jk...@google.com (2023-02-17)

As commented on https://bugs.chromium.org/p/chromium/issues/detail?id=1411524, the current Canary version should enforce this delay. 

### jk...@google.com (2023-02-17)

Confirmed on the other bug - therefore I am marking this one as fixed, too.

### al...@alesandroortiz.com (2023-02-17)

Thanks jkeitel@! Based on code review, seems fixed in commit 142d7061a92787e4f39e9091a396758ef9723177 (https://crbug.com/chromium/1411172, related to linked issue in https://crbug.com/chromium/1341430#c16).

Will re-verify behavior on Canary later today.

### jk...@google.com (2023-02-17)

That's correct - thank you!

### sc...@google.com (2023-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-17)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-02-17)

Verified as fixed on Canary 112.0.5601.0 on Windows 10. Thanks for fixing in the refactor, jkeitel@!

### am...@chromium.org (2023-03-02)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, Alesandro! The VRP Panel has decided to award you $3000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### al...@alesandroortiz.com (2023-03-02)

Thanks for the reward!

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1341430?no_tracker_redirect=1

[Multiple monorail components: Privacy, UI>Browser>Autofill>UI]
[Monorail blocking: crbug.com/chromium/1279268]
[Monorail mergedwith: crbug.com/chromium/1411524]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060134)*
