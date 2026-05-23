# Security: Omnibox Spoofing in MacOS

| Field | Value |
|-------|-------|
| **Issue ID** | [41483793](https://issues.chromium.org/issues/41483793) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Mac |
| **Reporter** | fa...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2023-12-13 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

By leveraging a combination of requestFullscreen(), onmousedown, and select dropdown functions, an attacker could take control of the omnibox in the Chrome browser with content controlled by the attacker.

This issue is caused by a combination of the aforementioned weirdness with the macOS Chrome browser, which delays the fullscreen notification. When the fullscreen notification is shown, it's only a popup for a fraction of a second, making it unnoticeable. Whereas fullscreen typically shows at the start for a few seconds to ensure the user is aware of this transition and to prevent omnibox spoofing.

**VERSION**  

Chrome Version: stable, beta, or dev  

Operating System: macOS Sonoma 14.1.2

**REPRODUCTION CASE**

1. Download poc.html and spoof.png files.
2. Open the poc.html file in the latest Chrome browser.
3. Click on `Click to spoof` area on the site for testing.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- poc.html (text/plain, 889 B)
- [spoof.png](attachments/spoof.png) (image/png, 337.6 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 2.2 MB)
- [spoofing-fixed-test.mp4](attachments/spoofing-fixed-test.mp4) (video/mp4, 1.7 MB)

## Timeline

### [Deleted User] (2023-12-13)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-12-13)

Similar issue: crbug.com/1447237

### th...@chromium.org (2023-12-13)

I can reproduce this on Mac on M120. Setting severity to medium and assigning to the Open Screen team.

[Monorail components: UI>Browser>FullScreen]

### [Deleted User] (2023-12-13)

[Empty comment from Monorail migration]

### mu...@google.com (2023-12-13)

This should be a high priority issue that our team will fix. 

### [Deleted User] (2023-12-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-27)

takumif: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-11)

takumif: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2024-01-24)

Hello, friendly ping.

### is...@google.com (2024-01-24)

This issue was migrated from crbug.com/chromium/1511206?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### fa...@gmail.com (2024-02-05)

Friendly ping.

### fa...@gmail.com (2024-03-05)

Friendly ping.

### fa...@gmail.com (2024-04-23)

Hi, it's been a long time. Can we update on this issue?

### pe...@google.com (2024-11-05)

liberato: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-20)

liberato: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fa...@gmail.com (2025-04-14)

Hi, it seems this issue is fixed. I tested it on the latest version chrome (135) on macOS. Can we confirm this and close the issue as resolved, if so?

### li...@google.com (2025-04-15)

=> muyaoxu@ to confirm that this is expected to be fixed.

### mu...@google.com (2025-04-15)

Yes. The fullscreen toast doesn't disappear immediately now. I haven't made changes to the toast recently, so it might have been fixed a while a go due to other changes.

### ch...@google.com (2025-04-15)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### mu...@google.com (2025-04-15)

Re #21,

We don't know which specific CL fixed the issue.

### aj...@chromium.org (2025-04-17)

135 is Stable so we wouldn't merge anything anyway so setting to NA.

### sp...@google.com (2025-04-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of moderate impact security UI issue


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### fa...@gmail.com (2025-04-30)

Thank you!

### ch...@google.com (2025-04-30)

deleted

### ch...@google.com (2025-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of moderate impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41483793)*
