# heap-use-after-free in Read Anything

| Field | Value |
|-------|-------|
| **Issue ID** | [40062849](https://issues.chromium.org/issues/40062849) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Accessibility |
| **Platforms** | Linux, Windows |
| **Reporter** | xp...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2023-01-31 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

1. Enable #read-anything in flags (chrome://flags/#read-anything).
2. Inspect any page and undock devtools.
3. Right click devtools console and press menu option "Open in Reader"
4. Dock devtools => UAF

**Problem Description:**  

heap-use-after-free in Read Anything

**Additional Comments:**

\*\*Chrome version: \*\* 112.0.5572.0 (Developer Build) (64-bit) \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.6 KB)
- [WindowsTerminal_xXCzTIcLjY.mp4](attachments/WindowsTerminal_xXCzTIcLjY.mp4) (video/mp4, 7.4 MB)

## Timeline

### [Deleted User] (2023-01-31)

[Empty comment from Monorail migration]

### xp...@gmail.com (2023-01-31)

[Empty comment from Monorail migration]

### fl...@google.com (2023-02-01)

Thank you for the clear, detailed report!

Setting Security_Severity-High due to memory corruption in the browser process, partially mitigated by the complexity of hitting this code path (opening devtools, docking/undocking, etc).

Setting Security_Impact-None because this is an experimental feature gated behind a flag.

Assigning to abigailbklein@ who kindly offered to take this on.

[Monorail components: UI>Accessibility]

### xp...@gmail.com (2023-02-01)

Hi, I appreciate the quick response, triage and assignment!

Bisect: "You are probably looking for a change made after 1091513 (known good), but no later than 1091586 (first known bad).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/a69d2c206905b1c0787b116cc7d75296c16cee5a..40afafa78c964221eface74dbe0e0af8482ae226"

Confirmed the UAF does not reproduce before: https://chromium.googlesource.com/chromium/src/+/08b7c5ae101637173aa505fdb1b1c07d810455df

### ab...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### xp...@gmail.com (2023-03-08)

No longer can reproduce on latest Chromium/Chrome Canary 113.0.5637.2 branch-heads/5637@{#4} Windows 11

I think this issue was fixed with: https://chromium-review.googlesource.com/c/chromium/src/+/4283457 by abigailbklein@google.com.

Could you please resolve/verify this issue? Thank you!

### th...@chromium.org (2023-03-10)

Security marshal here. abigailbklein@, if this issue is resolved, could you please mark it as fixed?

### ab...@google.com (2023-03-10)

The CL identified in https://crbug.com/chromium/1411862#c6 did a number of things related to reducing memory usage and web contents observers, so it very well could have fixed this UAF, but it wasn't specifically targetting the UAF. I'll mark this bug as fixed given that it's no longer reproduceable, and we can reopen if we find it again.

### th...@chromium.org (2023-03-10)

I can confirm I can't reproduce the UAF on a recent ASAN build (1115000 from March 9th) while I can reproduce it on a 1109244 ASAN build (from Feb 23rd). I agree this seems fixed.

### [Deleted User] (2023-03-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations, Sven! The VRP Panel has decided to award you $1,000 for this report of a very highly mitigated security bug. Thank you for your efforts and reporting this issue to us. 

### xp...@gmail.com (2023-03-17)

Thank you

### xp...@gmail.com (2023-03-17)

@amy Question: When is a bisect bonus factored into security reports? I assume it's only factored in when it's used in the fix?

### am...@chromium.org (2023-03-17)

Hi Sven, the issue with bisect bonus here is that this feature is not yet launched / enabled by default (therefore, is security_impact-none) and does not impact any active release channels. 

### xp...@gmail.com (2023-03-17)

Gotcha, thanks.

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-17)

This issue was migrated from crbug.com/chromium/1411862?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062849)*
