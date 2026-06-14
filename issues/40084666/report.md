# Security: use-after-free vulnerability in flash player 22.0.0.192

| Field | Value |
|-------|-------|
| **Issue ID** | [40084666](https://issues.chromium.org/issues/40084666) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | ji...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-06-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

There is a use-after-free vulnerability in flash player. Which could lead to code execution.

In chrome the crash as follow:  

3:039> r  

eax=031b5b30 ebx=0309a348 ecx=0309a348 edx=00000000 esi=03201000 edi=00000000  

eip=00000000 esp=00222d60 ebp=00222e18 iopl=0 nv up ei pl zr na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010246  

00000000 ?? ???

ub esp:  

5864fe0f 8bd9 mov ebx,ecx  

5864fe11 33ff xor edi,edi  

5864fe13 897c2428 mov dword ptr [esp+28h],edi  

5864fe17 8b03 mov eax,dword ptr [ebx]  

5864fe19 8b500c mov edx,dword ptr [eax+0Ch]  

5864fe1c 8d8c24ac000000 lea ecx,[esp+0ACh]  

5864fe23 51 push ecx  

5864fe24 8bcb mov ecx,ebx  

5864fe26 895c2428 mov dword ptr [esp+28h],ebx  

5864fe2a 897c243c mov dword ptr [esp+3Ch],edi  

5864fe2e ffd2 call edx

dd ecx:  

0309a348 031b5b30 00000000 00000000 00000000  

0309a358 00000000 00000000 00000000 00000000  

0309a368 00000000 00000000 00000000 00000000  

0309a378 00000000 00000000 00000000 00000000  

0309a388 00000000 00000000 00000000 00000000

so this vulnerability can control the EIP.

**VERSION**  

Flash player 22.0.0.192 in Chrome windows 7 x86(other platform should be trigger also)

Please drag the uaftest.swf into chrome will crash.

Please not public in MAPP and public it in chrome issues list 14 weeks after being marked as Fixed.

Credit is to "JieZeng of Tencent Zhanlu Lab".

Please report is as soon as possible.

## Attachments

- [uaftest.swf](attachments/uaftest.swf) (application/octet-stream, 486 B)

## Timeline

### ji...@gmail.com (2016-06-23)

why can't I change the contents of the above?

### do...@chromium.org (2016-06-23)

+natashenka, can you please have a look?

[Monorail components: Internals>Plugins>Flash]

### na...@google.com (2016-06-23)

Thanks, I've reported it!

### na...@google.com (2016-06-23)

This is PSIRT-5526.

### do...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### ji...@gmail.com (2016-06-24)

@natashenka Thanks!

### sh...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-08)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@gmail.com (2016-07-10)

Please let me know the progress of this issue!

Thanks!

### na...@google.com (2016-07-11)

Adobe is still working on this issue, it will not be fixed in the next update, maybe in August instead.

### ji...@gmail.com (2016-07-12)

@natashenka Thanks!  Let's keep in touch.

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ji...@gmail.com (2016-07-21)

Is it eligible for reward?

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-07-21)

Once the fix is released the reward panel will take a look. I don't see any reason to think it wouldn't be, but it's up to the panel to decide.

### ji...@gmail.com (2016-07-22)

[Comment Deleted]

### ji...@gmail.com (2016-07-22)

Thanks for letting me know. 

### sh...@chromium.org (2016-07-26)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-08-02)

[Comment Deleted]

### aw...@chromium.org (2016-08-02)

[Comment Deleted]

### oc...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### na...@google.com (2016-09-22)

Fixed in September update

### sh...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-25)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-26)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### aw...@chromium.org (2016-10-07)

Nothing to merge here.

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

Very nice - $3,000 for this bug.

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### ji...@gmail.com (2016-10-12)

Thanks!then what do I need?

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-12-30)

This issue was migrated from crbug.com/chromium/622634?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084666)*
