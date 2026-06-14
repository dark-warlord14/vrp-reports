# Security: Adobe Flash TextField.variable property setter Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40086318](https://issues.chromium.org/issues/40086318) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2017-3002 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-12-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Adobe Flash TextField.variable property setter Use After Free

**VERSION**  

Chrome Version: 56.0.2924.28 beta (64-bit)  

Operating System: Windows 7 en 64-bit

**REPRODUCTION CASE**

Open "TestSetVariable.html" with chrome and observe the crash.

This is a use after free bug when setting the "variable" property of a TextField object.

When handling setting the "variable" property of the TextField object, a user-defined callback function could be trigged.  

If we delete the TextField in the callback function, a use-after-free occurs.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

(1e9c.13cc): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.

pepflashplayer!PPP\_ShutdownBroker+0x251640:  

000007fe`d6255dd0 488b81d0000000 mov rax,qword ptr [rcx+0D0h] ds:00000000`000000d0=????????????????  

7:087> k  

Child-SP RetAddr Call Site  

00000000`0031cfd8 000007fe`d62cf912 pepflashplayer!PPP\_ShutdownBroker+0x251640  

00000000`0031cfe0 000007fe`d62d020e pepflashplayer!PPP\_ShutdownBroker+0x2cb182  

00000000`0031d040 000007fe`d62cbd94 pepflashplayer!PPP\_ShutdownBroker+0x2cba7e  

00000000`0031d070 000007fe`d652d06b pepflashplayer!PPP\_ShutdownBroker+0x2c7604  

00000000`0031d0a0 000007fe`d652a417 pepflashplayer!PPP\_ShutdownBroker+0x5288db  

00000000`0031d0e0 000007fe`d6214a53 pepflashplayer!PPP\_ShutdownBroker+0x525c87  

00000000`0031d1d0 000007fe`d6215a38 pepflashplayer!PPP\_ShutdownBroker+0x2102c3  

00000000`0031d3e0 000007fe`d61f2d9e pepflashplayer!PPP\_ShutdownBroker+0x2112a8  

00000000`0031d440 000007fe`d63ec000 pepflashplayer!PPP\_ShutdownBroker+0x1ee60e  

00000000`0031d540 000007fe`d63f1a70 pepflashplayer!PPP\_ShutdownBroker+0x3e7870  

00000000`0031d5b0 000007fe`d61ed547 pepflashplayer!PPP\_ShutdownBroker+0x3ed2e0  

00000000`0031dd60 000007fe`d61ee58e pepflashplayer!PPP\_ShutdownBroker+0x1e8db7  

00000000`0031ddc0 000007fe`d62369f9 pepflashplayer!PPP\_ShutdownBroker+0x1e9dfe  

00000000`0031e080 000007fe`d62369a6 pepflashplayer!PPP\_ShutdownBroker+0x232269  

00000000`0031e0b0 000007fe`d61fcbc1 pepflashplayer!PPP\_ShutdownBroker+0x232216  

00000000`0031e100 000007fe`d601b6bd pepflashplayer!PPP\_ShutdownBroker+0x1f8431  

00000000`0031e190 000007fe`d604114b pepflashplayer!PPP\_ShutdownBroker+0x16f2d  

00000000`0031e3a0 000007fe`d604105e pepflashplayer!PPP\_ShutdownBroker+0x3c9bb  

00000000`0031e3f0 000007fe`d604150c pepflashplayer!PPP\_ShutdownBroker+0x3c8ce  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Program Files (x86)\Google\Chrome\Application\56.0.2924.28\chrome\_child.dll -  

00000000`0031e420 000007fe`d97c7950 pepflashplayer!PPP\_ShutdownBroker+0x3cd7c

Credit:

Please credit "Yuki Chen of Qihoo 360 Vulcan Team" for this bug.

## Attachments

- [TextField_setVariable.zip](attachments/TextField_setVariable.zip) (application/octet-stream, 5.6 KB)

## Timeline

### aa...@google.com (2016-12-24)

Natalie, can you please file these bugs with Adobe. Thanks!

[Monorail components: Internals>Plugins>Flash]

### aa...@google.com (2016-12-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### xi...@gmail.com (2017-02-14)

Hello, 

May i know whether this issue (and other 9 issues) have been reported to Adobe yet? Thank you!

### na...@google.com (2017-02-14)

I'm really sorry, these were filed over the holidays, and I missed them. I am reporting these issues to Adobe now.

I've verified this one still crashes Flash in the current version.

### na...@google.com (2017-02-15)

This is PSIRT-6391

### na...@google.com (2017-03-06)

Yuki, I can't see the PoC anymore, did you delete it? Can you attach it again?

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### na...@google.com (2017-03-10)

This will be fixed as CVE-2017-3002 in the March update.

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### xi...@gmail.com (2017-11-08)

Hello,

Since this vulnerability was fixed in March 2017 as CVE-2017-3002.
Is it possible for this case to go to reward panel now?

### na...@google.com (2017-11-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-11)

This bug requires manual review: M63 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-11-13)

Pls apply appropriate OSs label.

+awhalley@ for M63 merge review.

### aw...@google.com (2017-11-14)

No merge needed for Flash bugs

### aw...@google.com (2017-11-14)

xiong12002@ - now this (and your other reports) have been marked as fixed, we'll pick them up for consideration at the next VRP panel. Sorry for the delay!

### xi...@gmail.com (2017-11-14)

awhalley@

Thank you for the help!

BTW, does this reward program accept bugs in windows system ? For example, bugs in IE, Edge, Kernel EoP?

### aw...@chromium.org (2017-11-14)

Not for IE or Edge, I'm afraid, and kernel EOP should be covered by https://blogs.technet.microsoft.com/msrc/2017/07/26/announcing-the-windows-bounty-program/ now

### aw...@chromium.org (2017-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-11-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-02-25)

This issue was migrated from crbug.com/chromium/676789?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086318)*
