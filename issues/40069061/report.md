# Security: Cookie for enterprise-policy blocked hosts leaking from the request object in chrome.devtools.network. 

| Field | Value |
|-------|-------|
| **Issue ID** | [40069061](https://issues.chromium.org/issues/40069061) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2023-08-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Request objects from chrome.devtools.network do not clear the cookie values

Chrome Version: 115.0.5790.171 (Official Build) (64-bit) (cohort: Stable) and  

117.0.5936.0 (Official Build) canary (64-bit) (cohort: Clang-64)

Operating System: Windows 10

## **REPRODUCTION CASE** 0. Add runtime\_blocked\_hosts value:

{"\*":{"runtime\_blocked\_hosts":["\*://example.org"]}}

Go to regedit.exe on windows,

Computer\HKEY\_CURRENT\_USER\SOFTWARE\Policies\Google\Chrome

and add a new key

ExtensionSettings

with value

## {"\*":{"runtime\_blocked\_hosts":["\*://example.org"]}}

1. Run document.cookie="a=b" in devtools on <https://example.org>
2. Install extension
3. Open devtools within the first 10 seconds and keep dismissing the alert box until you land on <https://nonexistent> (on the alert box in <https://nonexistent> you will observe the cookie value.)

Side Note: The <https://nonexistent> trick is so that HAR log is not reset when navigating to <https://nonexistent>, for which an extension can then interact with page (to bypass samesite lax).

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [background.js](attachments/background.js) (text/plain, 298 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [devtools.js](attachments/devtools.js) (text/plain, 119 B)
- manifest.json (text/plain, 184 B)

## Timeline

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### bb...@google.com (2023-08-08)

So this seems like once you have added a blocked host, the only way you are leaking the information is by adding it in devtools.

Normally devtools is considered priviledged and we do not consider things you can do with it to be a security issue. 

Can you accomplish this without using devtools? 

### ha...@gmail.com (2023-08-08)

Devtools extension can leak the cookie not devtools

### ha...@gmail.com (2023-08-08)

See also https://bugs.chromium.org/p/chromium/issues/detail?id=1467743 (owners should be same)

### [Deleted User] (2023-08-08)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bb...@google.com (2023-08-09)

Thanks for the clarification on that.   

I'm setting a tentative medium on this, Devtools folks, this one is someone challenging for me to reproduce, but appears similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1467743. Can you possibly assist with triage and tell us if this should be a security bug. 


[Monorail components: Platform>Extensions>API]

### [Deleted User] (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-11)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-23)

dsv: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2023-08-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/90ebdff4cc6efa1c3fbf3026d2be4de268c3afe6

commit 90ebdff4cc6efa1c3fbf3026d2be4de268c3afe6
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Aug 25 08:36:43 2023

Filter out HAR results that are not avaiable to the extensions.

Bug: 1471253
Change-Id: Ief3da4618ae29609d4d730e2c696b2b87ca11046
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4807913
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/90ebdff4cc6efa1c3fbf3026d2be4de268c3afe6/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/90ebdff4cc6efa1c3fbf3026d2be4de268c3afe6/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### ds...@chromium.org (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Thank you for the report, Axel! The Chrome VRP Panel has decided to award you $500 for this report. While we have begun considering bypasses of enterprise policy as security issues, security impact and reward amounts are based on the policy being bypassed and the consequences of the bypass being reporting. The reward amount, therefore, is based on the limited security impact to users. Thank you for your efforts and reporting this issue to us.

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-09)

Setting OSes liberally just for the recor

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-25)

[Empty comment from Monorail migration]

### vo...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### vo...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### vo...@google.com (2023-10-26)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### vo...@google.com (2023-10-30)

Marking as not applicable to M114 after looking at similar bugs and merge conflicts.

### vo...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1471253?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069061)*
