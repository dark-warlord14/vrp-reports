# Security: Adobe Flash AdBannerAsset Object Type Confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [40090261](https://issues.chromium.org/issues/40090261) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2018-4920 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2018-01-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This is a type confusion vulnerability. This vulnerability is caused by an Exception thrown in a middle of a parent class’s constructor function.

**VERSION**  

Chrome Version: Version 64.0.3282.100 (Official Build) beta (64-bit)  

Operating System: Winows 7 64-bits

**REPRODUCTION CASE**

Visit poc.swf with chrome to observe the crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: tab

0:017> g  

(6e8.4cc): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Users\yuki\AppData\Local\Google\Chrome\User Data\PepperFlash\28.0.0.137\pepflashplayer.dll -  

pepflashplayer!PPP\_ShutdownBroker+0xb2920:  

000007fe`d26f6c30 440fb609 movzx r9d,byte ptr [rcx] ds:00000000`0016c000=??  

0:000> k  

Child-SP RetAddr Call Site  

00000000`003bd818 000007fe`d26f8131 pepflashplayer!PPP\_ShutdownBroker+0xb2920  

00000000`003bd820 000007fe`d26f4517 pepflashplayer!PPP\_ShutdownBroker+0xb3e21  

00000000`003bd8a0 00000355`389b8fac pepflashplayer!PPP\_ShutdownBroker+0xb0207  

00000000`003bd8e0 00000000`00000000 0x355`389b8fac

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### xi...@gmail.com (2018-01-23)

Please credit "Yuki Chen of Qihoo 360 Vulcan Team" for this bug, thank you!

### el...@chromium.org (2018-01-23)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### na...@google.com (2018-01-25)

Thanks, I've reported this to Adobe

### na...@google.com (2018-01-25)

[Empty comment from Monorail migration]

### na...@google.com (2018-01-25)

This is PSIRT-7808

### mb...@chromium.org (2018-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-03-12)

[Empty comment from Monorail migration]

### na...@google.com (2018-03-13)

This was resolved today as CVE-2018-4920

### aw...@google.com (2018-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-19)

What's the fix that needs to be merged to M66?

### aw...@chromium.org (2018-03-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-19)

The VRP panel decided to award $3,000 for this report, thanks!

### aw...@google.com (2018-03-19)

btw xiong12002@, how would you like to be credited if this is included in Chrome release notes?

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### ab...@google.com (2018-03-20)

no merge needed. 

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/804636?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090261)*
