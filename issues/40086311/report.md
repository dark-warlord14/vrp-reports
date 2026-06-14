# Security: Adobe Flash MovieClip.createTextField Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40086311](https://issues.chromium.org/issues/40086311) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2017-3001 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-12-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Adobe Flash MovieClip.createTextField Use After Free

**VERSION**  

Chrome Version: 56.0.2924.28 beta (64-bit)  

Operating System: Windows 7 en 64-bit

**REPRODUCTION CASE**

Open "MovieClip\_createTextField.html" with chrome and observe the crash.

This is a use after free bug when in MovieClip.createEmptyMovieClip.  

When create a new TextField to the MovieClip at some depth, it will first try to remove the MovieClip in that depth.  

This will trig a "onKillFocus" event callback, if we remove the parent MovieClip in the callback, a use-after-free occurs.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

(490.d84): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

0000042c`e046b860 3900 cmp dword ptr [rax],eax ds:000004bb`44dd3e78=d56de338  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Users\yuki\AppData\Local\Google\Chrome\User Data\PepperFlash\24.0.0.186\pepflashplayer.dll -  

8:096> k  

Child-SP RetAddr Call Site  

00000000`0019c118 000007fe`d4add00e 0x42c`e046b860 00000000`0019c120 000007fe`d4adcd3e pepflashplayer!PPP_ShutdownBroker+0x98887e 00000000`0019c160 000007fe`d4adc999 pepflashplayer!PPP_ShutdownBroker+0x9885ae 00000000`0019c190 000007fe`d4adaeb5 pepflashplayer!PPP_ShutdownBroker+0x988209 00000000`0019c240 000007fe`d4ae4f84 pepflashplayer!PPP_ShutdownBroker+0x986725 00000000`0019c280 000007fe`d4345d46 pepflashplayer!PPP_ShutdownBroker+0x9907f4 00000000`0019c2c0 000007fe`d434241f pepflashplayer!PPP_ShutdownBroker+0x1f15b6 00000000`0019c300 000007fe`d433b7b9 pepflashplayer!PPP_ShutdownBroker+0x1edc8f 00000000`0019c400 000007fe`d4673046 pepflashplayer!PPP_ShutdownBroker+0x1e7029 00000000`0019c440 000007fe`d4364a53 pepflashplayer!PPP_ShutdownBroker+0x51e8b6 00000000`0019c560 000007fe`d4541c5a pepflashplayer!PPP_ShutdownBroker+0x2102c3 00000000`0019c770 000007fe`d4379a2e pepflashplayer!PPP_ShutdownBroker+0x3ed4ca 00000000`0019cf20 000007fe`d43acb13 pepflashplayer!PPP_ShutdownBroker+0x22529e 00000000`0019d010 000007fe`d4391c01 pepflashplayer!PPP_ShutdownBroker+0x258383 00000000`0019d050 000007fe`d4391dc4 pepflashplayer!PPP_ShutdownBroker+0x23d471 00000000`0019d080 000007fe`d43196c4 pepflashplayer!PPP_ShutdownBroker+0x23d634 00000000`0019d0b0 000007fe`d431e099 pepflashplayer!PPP_ShutdownBroker+0x1c4f34 00000000`0019d110 000007fe`d4679e93 pepflashplayer!PPP_ShutdownBroker+0x1c9909 00000000`0019d160 000007fe`d467a42b pepflashplayer!PPP_ShutdownBroker+0x525703 00000000`0019d480 000007fe`d4364a53 pepflashplayer!PPP\_ShutdownBroker+0x525c9b

Credit:

Please credit "Yuki Chen of Qihoo 360 Vulcan Team" for this bug.

## Attachments

- deleted (application/octet-stream, 0 B)

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

### na...@google.com (2017-02-14)

Just reported this.

### na...@google.com (2017-02-15)

This is PSIRT-6394

### na...@google.com (2017-03-06)

Yuki, I can't see the PoC anymore, did you delete it? Can you attach it again?

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### na...@google.com (2017-03-10)

This will be resolved in the upcoming March update as CVE-2017-3001. 

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

Since this vulnerability was fixed in March 2017 as CVE-2017-3001.
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

No merge needed for Flash bugs.

### go...@chromium.org (2017-11-14)

Removing "Merge-Review-63" label per https://crbug.com/chromium/676773#c23.

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

This issue was migrated from crbug.com/chromium/676773?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/676779, crbug.com/chromium/676780, crbug.com/chromium/676781, crbug.com/chromium/692322, crbug.com/chromium/692325, crbug.com/chromium/692327, crbug.com/chromium/692330, crbug.com/chromium/692333, crbug.com/chromium/692337, crbug.com/chromium/692339, crbug.com/chromium/692340, crbug.com/chromium/692345, crbug.com/chromium/692347, crbug.com/chromium/692349]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086311)*
