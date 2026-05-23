# Security: Form validation UI dialog can cover whole page

| Field | Value |
|-------|-------|
| **Issue ID** | [40057645](https://issues.chromium.org/issues/40057645) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Validation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-10-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A custom form input validation message in an iframe can cover the parent page.

**VERSION**  

Chrome Version: 97.0.4673.2 + all channels  

Operating System: Windows 10

**REPRODUCTION CASE**  

An iframe can cause the validation message of a form input set using `setCustomValidity` to appear over the iframe's parent page and cover a large portion of the parent page with custom text.  

If the validation message is too long (200k characters), it will also overflow the dialog.  

The validation message dialog will be hidden when it's dismissed (clicked/loses focus), but the iframe can keep reopening it.

The iframe needs to be at least 1x1px to open the dialog. This could be exploited for example by `sandbox`ed ad frames to render text over the top-level browsing context.

Demo: <https://vuln-validation-popup-overflow.websec.blog/poc.html>

FIX  

I don't think there is a use case for overly long validation messages, so the message could be constrained to some length limit. This is how Firefox does it.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 164 B)
- [frame.html](attachments/frame.html) (text/plain, 340 B)
- [cross-origin.png](attachments/cross-origin.png) (image/png, 66.7 KB)

## Timeline

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-10-18)

[Comment Deleted]

[Monorail components: Blink>CSS]

### bd...@chromium.org (2021-10-18)

[Empty comment from Monorail migration]

[Monorail components: -Blink>CSS]

### bd...@chromium.org (2021-10-18)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-10-18)

@jarhar can you take a look at this? I was able to see this done in stable

[Monorail components: Blink>Forms>Validation]

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-11-01)

I can't reproduce this with a cross-origin iframe. It only seems to happen when the iframe is same-origin, which leads me to believe that this isn't a security issue.

### st...@gmail.com (2021-11-02)

https://crbug.com/chromium/1261191#c8: I can reproduce this with a cross-origin iframe (Chrome 95.0.4638.69 & 97.0.4689.0, Windows 10)

https://vuln-validation-popup-overflow.websec.blog/crossorigin.html

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-01)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-12-07)

Maybe someone on the paint team knows how to make the form validation popup not paint outside of an oopif's designated rendering area...?

[Monorail components: -Blink>Forms>Validation Blink>Paint]

### sc...@chromium.org (2021-12-07)

Over to szager@ as the resident iframe expert. Clipping the overlay tot he iframe size does seem like the right idea, though that may not be technically feasible. Otherwise I would support limiting the validation message to 200 or 300 characters (assuming they can't control the font size).

### [Deleted User] (2021-12-08)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@gmail.com (2021-12-14)

https://crbug.com/chromium/1261191#c15: `setCustomValidity` only supports a string as the message, so I don't think custom formatting is possible.
Truncating the message seems easier to implement and would reflect the behaviour of other browsers such as Firefox, which truncates the message to 256 chars. [0]

[0]: https://searchfox.org/mozilla-central/source/dom/html/ConstraintValidation.cpp#22

### ja...@chromium.org (2021-12-14)

I guess I can just limit the message length

[Monorail components: -Blink>Paint Blink>Forms>Validation]

### ja...@chromium.org (2021-12-15)

I was just doing some archeology and found an issue which seems quite contrary to my initial suggestion in https://crbug.com/chromium/1261191#c14: https://crbug.com/chromium/910979
I'm still going to limit the message length.

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### st...@gmail.com (2022-03-11)

I can confirm this has been fixed (for OOPIFs), so I think it can be closed now.

### ja...@chromium.org (2022-03-14)

Yeah this was fixed here: https://chromium-review.googlesource.com/c/chromium/src/+/3340071
For some reason gitwatcher didn't kick in and close this bug.

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-23)

Hi Thomas, thank you for this report. The VRP Panel has decided to award you $1,000 for this report given the limitations to impact if an attacker were to leverage this bug as presented in the report. We appreciate you efforts and reporting this issue to us. 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-13)

 Hi Thomas, it looks this issue was not tagged by our automation for inclusion in release notes and CVE processing when the fix shipped in a Stable channel release (probably for whatever reason gitwatcher didn't kick in on https://crbug.com/chromium/1261191#c22) -- sincere apologies for that! It appears this fix shipped in M99/Stable (v99.0.4844.51) am updating labels accordingly so this can get adjusted soon! 

### am...@chromium.org (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1261191?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057645)*
