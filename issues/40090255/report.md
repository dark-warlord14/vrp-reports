# Security: Adobe Flash NetStream Object Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40090255](https://issues.chromium.org/issues/40090255) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2018-4919 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2018-01-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This is a use after free vulnerability. A NetStream object could be used after it is freed.

This vulnerability exists because we can set a callback function in the middle of other object’s constructor function (e.g. a PrintJob object). When our callback function gets called, we can call the NetStream constructor function on the “this” object, which makes the “this” object become a NetStream object. Then we use the NetStream object to connect to a remote server. In this way, the flash runtime will keeps a reference to the NetStream object.

Then we return from our callback function and the PrintJob constructor function continues to execute, and the object becomes a PrintJob object again.

This will finally results in a dangling pointer to the NetStream object.

**VERSION**  

Chrome Version: Version 64.0.3282.100 (Official Build) beta (64-bit)  

Operating System: Windows 7 64-bits

**REPRODUCTION CASE**

1. Start a command line, cd to the "poc" folder
2. Start a server using the "poc" folder as the root directory by executing:  
   
   python -m SimpleHTTPServer
3. Start chrome, visit  
   
   <http://127.0.0.1:8000/index.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: Tab

0:016> g  

(5a8.1be8): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

pepflashplayer!PPP\_ShutdownBroker+0x1e1368:  

000007fe`d7b15678 48395038 cmp qword ptr [rax+38h],rdx ds:00000000`00000038=????????????????  

0:000> k  

Child-SP RetAddr Call Site  

00000000`003ee480 000007fe`d7dfa2d3 pepflashplayer!PPP\_ShutdownBroker+0x1e1368  

00000000`003ee4b0 000007fe`d7df5dbc pepflashplayer!PPP\_ShutdownBroker+0x4c5fc3  

00000000`003ee4e0 000007fe`d7df64b4 pepflashplayer!PPP\_ShutdownBroker+0x4c1aac  

00000000`003ee510 000007fe`d7dfa043 pepflashplayer!PPP\_ShutdownBroker+0x4c21a4  

00000000`003ee540 000007fe`d7dc6610 pepflashplayer!PPP\_ShutdownBroker+0x4c5d33  

00000000`003ee570 000007fe`d7b2d944 pepflashplayer!PPP\_ShutdownBroker+0x492300  

00000000`003ee5a0 000007fe`d79436aa pepflashplayer!PPP\_ShutdownBroker+0x1f9634  

00000000`003ee620 000007fe`d794238e pepflashplayer!PPP\_ShutdownBroker+0xf39a  

00000000`003ee680 000007fe`d7942724 pepflashplayer!PPP\_ShutdownBroker+0xe07e  

00000000`003ee6b0 000007fe`d7aca1d1 pepflashplayer!PPP\_ShutdownBroker+0xe414  

00000000`003ee6e0 000007fe`d7938f6c pepflashplayer!PPP\_ShutdownBroker+0x195ec1  

00000000`003ee710 000007fe`d7939044 pepflashplayer!PPP\_ShutdownBroker+0x4c5c  

00000000`003ee8c0 000007fe`e17df7a5 pepflashplayer!PPP\_ShutdownBroker+0x4d34  

00000000`003ee8f0 000007fe`e17de9b6 chrome\_child!IsSandboxedProcess+0x4f9f4d  

00000000`003ee920 000007fe`e17df460 chrome\_child!IsSandboxedProcess+0x4f915e  

00000000`003ee9c0 000007fe`e17d3a1f chrome\_child!IsSandboxedProcess+0x4f9c08  

00000000`003eea10 000007fe`dfcffb4c chrome\_child!IsSandboxedProcess+0x4ee1c7  

00000000`003eeae0 000007fe`df8cf476 chrome\_child!ChromeMain+0x10a294  

00000000`003eeb10 000007fe`df7c42e4 chrome\_child!ovly\_debug\_event+0x11d1f6  

00000000`003eec20 000007fe`df8cf882 chrome\_child!ovly\_debug\_event+0x12064

0:000> dq rcx <= RCX points to the freed object  

000005d0`56d72508 000005d0`56d72570 00000000`00000000 000005d0`56d72518 00000000`00000000 00000000`00000000  

000005d0`56d72528 00000000`00000000 00000000`00000000 000005d0`56d72538 00000000`00000000 00000000`00000000  

000005d0`56d72548 00000000`00000000 00000000`00000000 000005d0`56d72558 00000000`00000000 00000000`00000000  

000005d0`56d72568 00000000`00000000 000005d0`56d725d8 000005d0`56d72578 00000000`00000000 00000000`00000000

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### np...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ds...@chromium.org (2018-01-22)

Looks like this is Flash, not PDF.

[Monorail components: -Internals>Plugins>PDF Internals>Plugins>Flash]

### el...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### xi...@gmail.com (2018-01-23)

Please credit "Yuki Chen of Qihoo 360 Vulcan Team", thank you!

### na...@google.com (2018-01-25)

This is PSIRT-7807

### me...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-03-12)

[Empty comment from Monorail migration]

### na...@google.com (2018-03-13)

This was resolved today as CVE-2018-4919

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

What's the fix that needs to be merged?

### aw...@chromium.org (2018-03-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-19)

The VRP panel decided to award $3,000 for this report, thank you!

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### ab...@google.com (2018-03-20)

no merge needed

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/804198?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090255)*
