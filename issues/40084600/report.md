# Security: Adobe Flash PSDK.Object Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40084600](https://issues.chromium.org/issues/40084600) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-06-17 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

**VERSION**  

Chrome Version: 52.0.2743.41 beta-m (64-bit)  

Operating System: Windows 7 en 64-bit

**REPRODUCTION CASE**

This is a use after free vulnerability on an inner object of the PSDK object.  

When you call the getter property PSDK.pSDK, you can get an instance of PSDK object. And if you do this:

var o1 = PSDK.pSDK;  

var o2 = PSDK.pSDK;

o1 and o2 will be different objects, while they share a same inner object. And if you call

o1.release();

The inner object will be freed while o2 still has a reference to it. This causes the use after free issue. This bug is highly exploitable. I attached a poc to demonstrate eip-control in chrome 64-bit windows. To test this poc, just visit the index.html with chrome.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: Tab (Flash Content Process)

Crash State:

(15e0.1594): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Program Files (x86)\Google\Chrome\Application\52.0.2743.41\PepperFlash\pepflashplayer.dll -  

pepflashplayer!PPP\_ShutdownBroker+0x6430be:  

000007fe`d83e466e ff5018 call qword ptr [rax+18h] ds:88888888`888888a0=????????????????  

0:000> k  

Child-SP RetAddr Call Site  

00000000`001ebc90 000007fe`d8106ffc pepflashplayer!PPP\_ShutdownBroker+0x6430be  

00000000`001ebdd0 0000048d`cbec5d0c pepflashplayer!PPP\_ShutdownBroker+0x365a4c  

00000000`001ebe00 00000000`001ebec0 0x48d`cbec5d0c 00000000`001ebe08 000007fe`d7f77890 0x1ebec0 00000000`001ebe10 0000048d`cbed7a5a pepflashplayer!PPP_ShutdownBroker+0x1d62e0 00000000`001ebe40 00000000`00000000 0x48d`cbed7a5a

0:000> lmvm pepflashplayer  

start end module name  

000007fe`d7da0000 000007fe`d9ca7000 pepflashplayer (export symbols) C:\Program Files  

Image name: pepflashplayer.dll  

Timestamp: Tue Jun 14 06:26:14 2016 (575F3306)  

CheckSum: 01E1E3D1  

ImageSize: 01F07000  

File version: 22.0.0.192  

Product version: 22.0.0.192  

File flags: 0 (Mask 3F)  

File OS: 4 Unknown Win32  

File type: 2.0 Dll  

File date: 00000000.00000000  

Translations: 0409.04b0

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### es...@chromium.org (2016-06-17)

Thanks for the report.

natashenka, can you please take a look?

[Monorail components: Internals>Plugins>Flash]

### cl...@chromium.org (2016-06-18)

[Empty comment from Monorail migration]

### na...@google.com (2016-06-21)

I believe this is a duplicate of https://crbug.com/chromium/594004, which was reported in March. 

### do...@chromium.org (2016-06-22)

Merging into 594004 as per https://crbug.com/chromium/620949#c3

### xi...@gmail.com (2016-06-22)

Hi, Natashenka,

I believe this is a failed to patch case.

I think the case you reported in March (reported by Wen Guanxing?) was supposed to be fixed in May. The May patch tried to fix the PSDK.release issue by simply disabled this function call from AS3. However in this month's update the PSDK.release function was enabled again with some check to address the UAF issue, but could be bypassed.

Could you please check whether the case you reported in March was already marked as "fixed" by Adobe? And if this is a failed to patch case, will this submission be a valid submission?


### na...@google.com (2016-06-22)

You're right, this bug regressed. I'll let Adobe know.

### na...@google.com (2016-06-23)

This is PSIRT-5523

### na...@google.com (2016-09-22)

Fixed in the September update

### sh...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-11-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-01)

Nice one, the VRP panel decided to reward $5,000 for this - many thanks!

### aw...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/620949?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/594004]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084600)*
