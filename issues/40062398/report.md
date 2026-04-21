# Security: Improper origin elision in downloads prompt initiated in Chrome Custom Tab (Android)

| Field | Value |
|-------|-------|
| **Issue ID** | [40062398](https://issues.chromium.org/issues/40062398) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-12-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The origin in the download prompt at the bottom (not the top popup) in Chrome Custom Tab on Android are back-elided instead of front-elided.

The origin at the prompt may be used in a user's security decision whether to open the file from the bottom prompt or not.

**VERSION**  

Chrome Version: [108.0.5359.128 Stable]  

Operating System: [Android 11]

**REPRODUCTION CASE**

1. Go to Gmail app and paste this link in an email draft -- <https://the-actual-real-not-fake-google-com-haha-notrlly-lol.glitch.me/>
2. Click on link in Gmail, this opens a Chrome Custom Tab to the site which initiates a download.
3. The origin shown in the download prompt at the bottom is not elided properly according to <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/url_display_guidelines/url_display_guidelines.md#eliding-urls>

See attached screenshot.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [Screenshot_20221227-022515_Chrome.jpg](attachments/Screenshot_20221227-022515_Chrome.jpg) (image/jpeg, 111.8 KB)

## Timeline

### [Deleted User] (2022-12-26)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-26)

Thanks for the report. I understand that this report is for CCT and https://crbug.com/1389289 is for Chrome App, but the underlying implementation should be shared between the two, so keeping track of one bug should be sufficient.

### ha...@gmail.com (2022-12-27)

Thanks for the reply @xinghuilu. I think they are probably different. This talka about download prompt that appear at bottom which should only be present in CCT while the previous report talk about the downloads history.

Furthermore, in comparing screenshots you can see that in 1389289 we stop at ...real-google-com... while here we stpp at ...-real-google... so just by this alone I think they are different UI.

### xi...@chromium.org (2023-01-03)

Thanks for the explaining the differences. I'll let the owner decide if this is a duplicate.

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2023-09-25)

Assigning to alexmitra@ to take a quick look.

Alex, do you remember where in the code we set this text? For referecne, we fixed a similar bug recently in download home https://chromium-review.googlesource.com/c/chromium/src/+/4706260 and this fix looks very similar.

### ha...@gmail.com (2023-09-25)

Reporter here, i verified the fix in canary. It should also be fixed along with https://chromium-review.googlesource.com/c/chromium/src/+/4706260. You have to set canary as default browssr and restart the phone to observe the changes.

### sh...@chromium.org (2023-09-25)

Awesome. In that case, we can close this bug.

### [Deleted User] (2023-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Congratulations Axel! The Chrome VRP Panel has decided to award you $1,000 for this report. Though it was resolved by a CL for two previously reported issues, your report did report a different aspect of the elision issue that was not surfaced in the other reports. As such, we did want to show our appreciation for that finding. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-03)

This issue was migrated from crbug.com/chromium/1403716?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1389289]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062398)*
