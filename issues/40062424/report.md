# Security: PWA Install prompt can be overlaid over other origins.

| Field | Value |
|-------|-------|
| **Issue ID** | [40062424](https://issues.chromium.org/issues/40062424) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2022-12-28 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

The PWA installation prompt can be overlaid over other origins by first initiating the prompt and then calling window.open.

**VERSION**  

Chrome Version: 108.0.5359.125 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 Version 21H2 (Build 19044.2364)

**REPRODUCTION CASE**

1. Go to <https://jewel-chip-panama.glitch.me/a2hs-poc.html>
2. Click on the page once the tick is ready.
3. The PWA installation prompt is overlaid on <https://microsoft.com>. The origin of the installer still shows though.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [a2hs-poc.html](attachments/a2hs-poc.html) (text/plain, 939 B)
- [app.js](attachments/app.js) (text/plain, 1.7 KB)
- [app.webmanifest](attachments/app.webmanifest) (application/octet-stream, 1.2 KB)
- [dummy-sw.js](attachments/dummy-sw.js) (text/plain, 156 B)
- [phishing.html](attachments/phishing.html) (text/plain, 731 B)
- [style.css](attachments/style.css) (text/plain, 868 B)
- [Untitled_ Dec 30, 2022 2_28 AM.webm](attachments/Untitled_ Dec 30, 2022 2_28 AM.webm) (video/webm, 1.3 MB)

## Timeline

### [Deleted User] (2022-12-28)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-12-28)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-12-29)

Expected behaviour: The prompt is closed when on another origin just like with permission prompts. etc.

### li...@chromium.org (2022-12-29)

Hmm, I can't repro this on Windows or Linux. On Windows the install prompt shows up on the original page, not on microsoft.com, and on Linux there's no prompt it just links to microsoft.com. Can you add a video to show what the poc should look like?

### ha...@gmail.com (2022-12-29)

weird that you can't reproduce... are you using the same version (108.0.5359.125 (Official Build) (64-bit) (cohort: Stable)) and also using to https://jewel-chip-panama.glitch.me/a2hs-poc.html? 

### [Deleted User] (2022-12-29)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2022-12-29)

Did you also install from jewel-chip-panama before? In that case you need to delete previous app install from the prompt to show again. 

### ha...@gmail.com (2022-12-29)

Did you also click on the page once, not multiple times?

### li...@chromium.org (2022-12-29)

I made sure to uninstall it on both devices before testing this again, not super sure why I still can't repro it. Tentatively setting OS for desktops because this looks like it should repro on Linux and Mac as well.

Assigning to a dPWA owner to triage, and CCing some mobile folks because this might be a mobile issue as well.
Reporter: have you tried this PoC on Android?

Setting severity to medium since this seems like another UX issue that can be trivial to spoof for phishing campaigns.

[Monorail components: UI>Browser>WebAppInstalls]

### ha...@gmail.com (2022-12-29)

just checked. doesnt repro on Android even with popup blocker off

### [Deleted User] (2022-12-29)

[Empty comment from Monorail migration]

### li...@chromium.org (2022-12-29)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-12-30)

Just an update to the PoC website: I just changed the PoC to use location.href instead of window.open so that popup-blocker disabled is not required.(It still works.)

### [Deleted User] (2022-12-31)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2023-01-03)

https://bugs.chromium.org/p/chromium/issues/detail?id=1404230 for Android version of this bug.

### [Deleted User] (2023-01-12)

dmurph: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-27)

dmurph: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2023-02-03)

This is scheduled in our backlog. adding Disable-Nags

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### dm...@chromium.org (2023-06-23)

[Empty comment from Monorail migration]

### dm...@chromium.org (2023-06-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-23)

Unmerging this bug as it was the earlier reported version of this issue. Cannot merge https://crbug.com/chromium/1450203 into this report as the fix was landed on that bug and that will need to be the canonical report. When that fix ships in 115, the CVE should be applied to this report. 

### [Deleted User] (2023-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-27)

Congratulations, Axel! The VRP Panel has decided to award you $4,000 for this report. The reward amount was determined based on the display / presence of the correct origin on the install prompt. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-08)

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1404001?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1450203]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062424)*
