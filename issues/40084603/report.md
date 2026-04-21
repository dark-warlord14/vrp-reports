# Security: Adobe Flash MediaPlayerItemLoader.addEventListener Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40084603](https://issues.chromium.org/issues/40084603) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2016-4180 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-06-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This is a use after free vulnerability in MediaPlayerItemLoader.addEventListener.  

I believe this is a use after free because when I tested the poc in IE with page heap enabled, I got crash immediately when it tries to access freed memory.

**VERSION**  

Chrome Version: 52.0.2743.41 beta-m (64-bit)  

Operating System: Windows 7 en 64-bit

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

0:012> g  

(a68.19b0): Invalid handle - code c0000008 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

ntdll!RtlRaiseStatus+0x18:  

00000000`77c27ef8 488b8424b8010000 mov rax,qword ptr [rsp+1B8h] ss:00000000`001cccd8=0000000077c27ef8  

0:000> k  

Child-SP RetAddr Call Site  

00000000`001ccb20 00000000`77be5d95 ntdll!RtlRaiseStatus+0x18  

00000000`001cd0c0 000007fe`d8824624 ntdll! ?? ::FNODOBFM::`string'+0x8b8e 00000000`001cd0f0 000007fe`d8234f2f pepflashplayer!IAEModule_IAEKernel_UnloadModule+0x45944 00000000`001cd130 000007fe`d801ebd4 pepflashplayer!PPP_ShutdownBroker+0x63397f 00000000`001cd190 000007fe`d867bf32 pepflashplayer!PPP_ShutdownBroker+0x41d624 00000000`001cd1c0 000007fe`d866ef7c pepflashplayer!PPP_ShutdownBroker+0xa7a982 00000000`001cd210 000007fe`d8670baa pepflashplayer!PPP_ShutdownBroker+0xa6d9cc 00000000`001cd250 000007fe`d8671731 pepflashplayer!PPP_ShutdownBroker+0xa6f5fa 00000000`001cd310 000007fe`d7e5c826 pepflashplayer!PPP_ShutdownBroker+0xa70181 00000000`001cd340 000007fe`d7c0f90a pepflashplayer!PPP_ShutdownBroker+0x25b276 00000000`001cd3d0 000007fe`d7c145fe pepflashplayer!PPP_ShutdownBroker+0xe35a 00000000`001cd430 000007fe`d7c14bd4 pepflashplayer!PPP_ShutdownBroker+0x1304e 00000000`001cd460 000007fe`d7e11fa6 pepflashplayer!PPP_ShutdownBroker+0x13624 00000000`001cd490 000007fe`d7c074d0 pepflashplayer!PPP_ShutdownBroker+0x2109f6 00000000`001cd4c0 000007fe`d7c07d74 pepflashplayer!PPP_ShutdownBroker+0x5f20 00000000`001cd670 000007fe`d89a71dc pepflashplayer!PPP_ShutdownBroker+0x67c4 - 00000000`001cd6a0 000007fe`dfedbd35 pepflashplayer!IAEModule_IAEKernel_UnloadModule+0x1c84fc 00000000`001cd6d0 000007fe`df6c7acd chrome_child!ChromeMain+0x13673d9 00000000`001cd700 000007fe`df6c6dab chrome_child!ChromeMain+0xb53171 00000000`001cd730 000007fe`df6c76b8 chrome\_child!ChromeMain+0xb5244f

## Attachments

- [MediaPlayerItemLoader_addEventListener_UAF.zip](attachments/MediaPlayerItemLoader_addEventListener_UAF.zip) (application/octet-stream, 1.7 KB)

## Timeline

### es...@chromium.org (2016-06-17)

Thanks for the report.

natashenka, can you please take a look?

### es...@chromium.org (2016-06-17)

Er, actually adding natashenka now, can you please take a look?

[Monorail components: Internals>Plugins>Flash]

### cl...@chromium.org (2016-06-18)

[Empty comment from Monorail migration]

### na...@google.com (2016-06-21)

Reported to Adobe. Can you let me know how you want to be credited?

### xi...@gmail.com (2016-06-22)

Please use "Yuki Chen of Qihoo 360 Vulcan Team" for credit, thank you!

### do...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-06)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2016-08-02)

natashenka: any updates on this from Adobe?

### oc...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-15)

[Empty comment from Monorail migration]

### na...@google.com (2017-02-15)

This is CVE-2016-4180

### sh...@chromium.org (2017-02-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

Congratulations! The panel decided to award $3,000 for this report. Thanks!

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-19)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-02-20)

No merge needed.

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-25)

This issue was migrated from crbug.com/chromium/620961?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084603)*
