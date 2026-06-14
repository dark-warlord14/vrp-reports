# Security: use-after-free vulnerability in flash player latest version

| Field | Value |
|-------|-------|
| **Issue ID** | [40085170](https://issues.chromium.org/issues/40085170) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2016-7881 |
| **Reporter** | ji...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-08-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a use-after-free vulnerability in flash player. Which could lead to arbitrary code execution.

**VERSION**  

Flash player 22.0.0.209 in Chrome windows 7 x86(chrome 52.0.2743.116 m)

Please drag the test\_uaf.swf into chrome will crash.

Please not public in MAPP and public it in chrome issues list 14 weeks after being marked as Fixed.

Credit is to "JieZeng of Tencent Zhanlu Lab".

Please report it as soon as possible.

CRASH INFORMATION:

chrome crash tate:  

62d21870 8b7508 mov esi,dword ptr [ebp+8]  

62d21873 6874b1a663 push offset pepflashplayer!curl\_getenv+0x6d82cc (63a6b174)  

62d21878 50 push eax  

62d21879 e822db0000 call pepflashplayer!PPP\_ShutdownBroker+0x13e1ad (62d2f3a0)  

62d2187e 8b8790000000 mov eax,dword ptr [edi+90h]  

62d21884 8b8094000000 mov eax,dword ptr [eax+94h] ds:0023:00000094=????????

3:038> r  

eax=00000000 ebx=00000005 ecx=00000002 edx=00000000 esi=02ff6000 edi=02dfa240  

eip=62d21884 esp=001b82c0 ebp=001b8338 iopl=0 nv up ei pl zr na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010246  

pepflashplayer!PPP\_ShutdownBroker+0x130691:  

62d21884 8b8094000000 mov eax,dword ptr [eax+94h] ds:0023:00000094=????????

3:038> dd edi L c0/4  

02dfa240 02dfa2e0 00000000 00000000 00000000  

02dfa250 00000000 00000000 00000000 00000000  

02dfa260 00000000 00000000 00000000 00000000  

02dfa270 00000000 00000000 00000000 00000000  

02dfa280 00000000 00000000 00000000 00000000  

02dfa290 00000000 00000000 00000000 00000000  

02dfa2a0 00000000 00000000 00000000 00000000  

02dfa2b0 00000000 00000000 00000000 00000000  

02dfa2c0 00000000 00000000 00000000 00000000  

02dfa2d0 00000000 00000000 00000000 00000000  

02dfa2e0 02dfa380 00000000 00000000 00000000  

02dfa2f0 00000000 00000000 00000000 00000000

## Attachments

- [test_uaf.swf](attachments/test_uaf.swf) (application/octet-stream, 48.0 KB)

## Timeline

### ji...@gmail.com (2016-08-23)

[Comment Deleted]

### ji...@gmail.com (2016-08-23)

Right after you report it to Adobe, Please tell me the PSIRT number.Thanks!

### in...@chromium.org (2016-08-23)

Natalie, can you please report this to Adobe. Thanks!

### in...@chromium.org (2016-08-23)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### na...@google.com (2016-08-23)

Adding some notes so I remember what bug this is:

This is a UaF in converting a MovieClip to an object. If there is a watch/setter on the __proto__ property of the object, it can delete the MovieClip when the prototype is set, leading to a UaF.

Reported to Adobe, I'll update the PSIRT when I have it.

### na...@google.com (2016-08-23)

This is PSIRT-5760.

### ji...@gmail.com (2016-08-24)

Thanks!

### sh...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-07)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-09-21)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2016-09-22)

Fixed in September update.

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-25)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-26)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### aw...@chromium.org (2016-10-07)

Nothing to merge here.

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

And another $3,000 here!  Thanks for the reports!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### na...@google.com (2016-12-09)

This will be fixed in the next release, and is CVE-2016-7881

### sh...@chromium.org (2016-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-02-25)

This issue was migrated from crbug.com/chromium/640177?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085170)*
