# SameSite cookie bypass via openWindow

| Field | Value |
|-------|-------|
| **Issue ID** | [40091053](https://issues.chromium.org/issues/40091053) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Internals>Network>Cookies |
| **Platforms** | Windows |
| **Reporter** | s....@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-04-09 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
1. Go to https://shhnjk.azurewebsites.net/SameSite.php (Sets SameSite cookie)
2. Then go to https://vuln.shhnjk.com/openCrossSiteWindow.html
3. Click on the button.
4. Allow notification
5. Click on notification

What is the expected behavior?
SameSite cookie not sent

What went wrong?
URL opened by openWindow is treated as initial navitation, bypassing SameSite cookie

Did this work before? N/A 

Chrome version: 65.0.3325.181  Channel: stable
OS Version: 10 RS3
Flash Version:

## Timeline

### ji...@chromium.org (2018-04-09)

+mkwst@

Similar to https://bugs.chromium.org/p/chromium/issues/detail?id=830091
https://bugs.chromium.org/p/chromium/issues/detail?id=830101

We might consider group them together. 

[Monorail components: Blink>SecurityFeature Internals>Network>Cookies]

### ca...@chromium.org (2018-04-13)

Re #1: IMO, they are fine separate since the trigger is different enough in each of the bugs.

### ts...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-06-21)

Hi folks! Should https://crbug.com/chromium/854429 be treated as dupe of this bug? If so, please mark https://crbug.com/chromium/854429 as dupe of this bug. With https://crbug.com/chromium/854429, attacker doesn't need notification permission anymore.

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### mk...@chromium.org (2019-02-12)

CCing some folks who might have bandwidth.

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### s....@gmail.com (2019-05-23)

This seems to be fixed.

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### bd...@chromium.org (2020-10-15)

Marking this as fixed due to https://crbug.com/chromium/830808#c13 (marhsal). Please reopen if this is actually not fixed.

### [Deleted User] (2020-10-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### s....@gmail.com (2020-10-21)

Double checked and it is fixed :)

### ad...@google.com (2020-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-28)

The VRP panel has decided to award $500 for this report.

### ad...@google.com (2020-10-29)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-30)

I'll credit this in the release notes for M87, even though it was fixed a while ago.

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/830808?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Internals>Network>Cookies]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091053)*
