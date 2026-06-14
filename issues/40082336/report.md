# Security: adobe flash NetStream.appendBytes ByteArray data Use-After-Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40082336](https://issues.chromium.org/issues/40082336) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2015-6682 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-06-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

By calling NetStream.appendBytes(ByteArray ba, ...)  

flash will parse the data we passed in the ByteArray, it seems the function will directy pass  

the raw buffer in the ByteArray to lower implementation functions, insteading of copying the data.

So if we can change the ByteArray data while flash is parsing it, we can let the parser to use inconsistent or already freed memory.

We can achieve this by setting an "onSeekPoint" event handler on the NetStream object, it will get called when the parser is parseing our data.  

In our "onSeekPoint" handler, we force the internal buffer of the ByteArray to be freed, so when the execution flow returns to the parser, a use-after-free  

crash will happen.

**VERSION**  

Chrome Version: Version 44.0.2403.52 beta-m (64-bit)  

Operating System: Windows 7 Home Edition 64-bit

**REPRODUCTION CASE**  

Please see the attached PoC

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Crash State:

(1930.177c): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Program Files (x86)\Google\Chrome\Application\44.0.2403.52\PepperFlash\pepflashplayer.dll -  

pepflashplayer!IAEModule\_IAEKernel\_UnloadModule+0x14998f:  

000007fe`e3962c4f 488b040a mov rax,qword ptr [rdx+rcx] ds:000007ff`f20236e1=????????????????  

0:000> k  

Child-SP RetAddr Call Site  

00000000`0030cc58 000007fe`e314a90e pepflashplayer!IAEModule\_IAEKernel\_UnloadModule+0x14998f  

00000000`0030cc60 000007fe`e3145d1b pepflashplayer!PPP\_ShutdownBroker+0x41935e  

00000000`0030ccd0 000007fe`e3150ba8 pepflashplayer!PPP\_ShutdownBroker+0x41476b  

00000000`0030cd00 000007fe`e30289e0 pepflashplayer!PPP\_ShutdownBroker+0x41f5f8  

00000000`0030cd30 000007ff`fbb4b2f7 pepflashplayer!PPP\_ShutdownBroker+0x2f7430  

00000000`0030cd60 00000000`0030cfb0 0x7ff`fbb4b2f7 00000000`0030cd68 000007ff`ff520000 0x30cfb0 \*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Program Files (x86)\Google\Chrome\Application\44.0.2403.52\chrome_child.dll - 00000000`0030cd70 000007fe`dd03d8cf 0x7ff`ff520000  

00000000`0030cd78 000007ff`00000000 chrome\_child!IsSandboxedProcess+0x351187  

00000000`0030cd80 00000000`01e53fc0 0x7ff`00000000 00000000`0030cd88 000007ff`fbb332e0 0x1e53fc0 00000000`0030cd90 000007ff`ff17b0d0 0x7ff`fbb332e0  

00000000`0030cd98 000007ff`fbb33190 0x7ff`ff17b0d0 00000000`0030cda0 000007ff`ff17b0d0 0x7ff`fbb33190  

00000000`0030cda8 000007ff`ff1685d8 0x7ff`ff17b0d0 00000000`0030cdb0 000007ff`ff1730d0 0x7ff`ff1685d8  

00000000`0030cdb8 000007ff`ff16a330 0x7ff`ff1730d0 00000000`0030cdc0 000007ff`fbb2b160 0x7ff`ff16a330  

00000000`0030cdc8 000007ff`fbb33190 0x7ff`fbb2b160 00000000`0030cdd0 000007ff`ff1afa60 0x7ff`fbb33190

## Attachments

- [adobe flash NetStream.appendBytes ByteArray data Use-After-Free.zip](attachments/adobe flash NetStream.appendBytes ByteArray data Use-After-Free.zip) (application/zip, 295.2 KB)
- [poc-leak.zip](attachments/poc-leak.zip) (application/zip, 3.4 KB)

## Timeline

### xi...@gmail.com (2015-06-22)

Sorry I forgot to attach the PoC, here is the PoC

### es...@chromium.org (2015-06-22)

Sorry, I still don't see the PoC. Can you please attach it?

### xi...@gmail.com (2015-06-22)

Re-attach the PoC

### es...@chromium.org (2015-06-22)

wfh@, do you think you could try this out on Windows?

### es...@chromium.org (2015-06-22)

[Empty comment from Monorail migration]

### xi...@gmail.com (2015-06-23)

Add a memory leak poc on 32-bit Flash 

### wf...@chromium.org (2015-06-23)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-06-23)

I can repro on Flash 18.0.0.160. it appears to be crashing inside a memcpy.

### wf...@chromium.org (2015-06-23)

-> cevans to notify Adobe

### wf...@chromium.org (2015-06-23)

also reproduces on flash 18.0.0.194 on Stable.

### sc...@gmail.com (2015-06-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-07-06)

Sorry, dropped the ball a bit on this one. I confirm the PoC in https://crbug.com/chromium/502871#c6 -- nice work!

### sc...@gmail.com (2015-07-06)

@xiong12002: how would you like to be credited?

### sc...@gmail.com (2015-07-06)

[Deadline tracking for P0 is https://code.google.com/p/google-security-research/issues/detail?id=476]

### xi...@gmail.com (2015-07-06)

Please use "Yuki Chen of Qihoo 360 Vulcan Team" for credit, thank you!

### sc...@gmail.com (2015-07-06)

Adobe acknowledged as PSIRT-3893

### xi...@gmail.com (2015-10-14)

Hello, this is fixed as CVE-2015-6682 in September update:
https://helpx.adobe.com/security/products/flash-player/apsb15-23.html

Is there any reward for this one?

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### th...@chromium.org (2016-09-22)

awhalley: Can you help follow up on this bug or reassign it to someone that can?

### aw...@chromium.org (2016-09-22)

Sorry, this hadn't joined the reward panel queue yet since it hadn't been marked as fixed. Doing so now.  There's a bit of a backlog at the moment but I'll make sure it moves along.

### sh...@chromium.org (2016-09-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-24)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-25)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### sh...@chromium.org (2016-09-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2016-10-03)

No merge necessary for Chromium, this was done in Flash Player.

### aw...@google.com (2016-10-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

Congratulations, $3000 for this bug!  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************
 

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-12-29)

This issue was migrated from crbug.com/chromium/502871?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082336)*
