# Security: type confusion vulnerability in flash player latest version

| Field | Value |
|-------|-------|
| **Issue ID** | [40085171](https://issues.chromium.org/issues/40085171) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | ji...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-08-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a type confusion vulnerability in flash player. In particular, the vulnerability is caused by BitmapData.draw method checking parameter not strict.

**VERSION**  

Flash player 22.0.0.209 in Chrome windows 7 x86(chrome 52.0.2743.116 m)

Please drag the test\_crash.swf into chrome will crash.

Please not public in MAPP and public it in chrome issues list 14 weeks after being marked as Fixed.

Credit is to "JieZeng of Tencent Zhanlu Lab".

Please report it as soon as possible.And right after you report it to Adobe, Please tell me the PSIRT number.

Thanks!

CRASH INFORMATION:  

chrome crash tate:  

623bf78e 894628 mov dword ptr [esi+28h],eax  

623bf791 8b4718 mov eax,dword ptr [edi+18h]  

623bf794 3b462c cmp eax,dword ptr [esi+2Ch]  

623bf797 7e03 jle pepflashplayer!PPP\_ShutdownBroker+0x28e5a9 (623bf79c)  

623bf799 89462c mov dword ptr [esi+2Ch],eax  

623bf79c 8b4610 mov eax,dword ptr [esi+10h]  

623bf79f 8b0c90 mov ecx,dword ptr [eax+edx\*4] ds:0023:aa38b6dc=????????

3:038> r  

eax=039fce40 ebx=001ec3c0 ecx=1ffffffc edx=69a63a27 esi=001ec3c0 edi=028fa080  

eip=623bf79f esp=001ebc20 ebp=00000002 iopl=0 nv up ei ng nz na po cy  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010283  

pepflashplayer!PPP\_ShutdownBroker+0x28e5ac:  

623bf79f 8b0c90 mov ecx,dword ptr [eax+edx\*4] ds:0023:aa38b6dc=????????

## Attachments

- [test_crash.swf](attachments/test_crash.swf) (application/octet-stream, 880 B)

## Timeline

### in...@chromium.org (2016-08-23)

Natalie, can you please report this to Adobe. Thanks!

### in...@chromium.org (2016-08-23)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### na...@google.com (2016-08-23)

Tested this out, it is a crash in rastering. Reporting to Adobe.

### na...@google.com (2016-08-23)

This is PSIRT-5761.

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

### mm...@chromium.org (2016-10-11)

Just to clarify: we wait until Adobe fixes this, right?

### aw...@chromium.org (2016-10-11)

Correct.

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-22)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@gmail.com (2016-10-28)

This has been fixed!

### es...@chromium.org (2016-11-02)

Natalie, sounds like we can close this bug now?

### na...@google.com (2016-11-02)

Yep, it still needs to go through the rewards panel though.

### na...@google.com (2016-11-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-02)

It can start that journey now it's been marked as fixed.  Keyword added.

### sh...@chromium.org (2016-11-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-05)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-11-06)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### aw...@chromium.org (2016-11-08)

Nothing to merge here

### aw...@chromium.org (2016-11-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-14)

Thanks, the panel awarded $3,000 for this report!

### aw...@google.com (2016-11-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-02-25)

This issue was migrated from crbug.com/chromium/640191?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085171)*
