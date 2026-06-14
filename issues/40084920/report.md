# Security: use-after-free vulnerability in Adobe flash player 

| Field | Value |
|-------|-------|
| **Issue ID** | [40084920](https://issues.chromium.org/issues/40084920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ji...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-07-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a use-after-free vulnerability in flash player. Which could lead to code execution.

**VERSION**  

Flash player 22.0.0.209 in Chrome windows 7 x86(other platform should be trigger also)

Please drag the TEST.swf into chrome will crash.

Please not public in MAPP and public it in chrome issues list 14 weeks after being marked as Fixed.

Credit is to "JieZeng of Tencent Zhanlu Lab".

Please report it as soon as possible.

CRASH INFORMATION:

chrome crash tate:  

59e593ba 55 push ebp  

59e593bb e870e2faff call pepflashplayer!PPP\_ShutdownBroker+0x16643d (59e07630)  

59e593c0 8b451c mov eax,dword ptr [ebp+1Ch]  

59e593c3 8b80fc000000 mov eax,dword ptr [eax+0FCh] ds:0023:000000fc=????????

3:041> r  

eax=00000000 ebx=0220a100 ecx=0220a240 edx=022090a0 esi=022090a0 edi=0220a1a0  

eip=59e593c3 esp=0014dfa8 ebp=0220a240 iopl=0 nv up ei pl nz na po nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010202  

pepflashplayer!PPP\_ShutdownBroker+0x1b81d0:  

59e593c3 8b80fc000000 mov eax,dword ptr [eax+0FCh] ds:0023:000000fc=????????

3:041> dd ebp  

0220a240 0220a4c0 00000000 00000000 00000000  

0220a250 00000000 00000000 00000000 00000000  

0220a260 00000000 00000800 00000000 00000000  

0220a270 00000000 00000000 00000000 00000000  

0220a280 00000000 00000000 00000000 00000000

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### ke...@chromium.org (2016-07-22)

Natalie, can you please triage this and file a bug with Adobe?

### na...@google.com (2016-07-23)

Thanks for reporting this! I'll report it to Adobe soon.

Some quick notes on this bug, to differentiate it from the other bug.

This seems to be a bug in the AS2 onUnload event, where a MovieClip is getting freed before the event is called on it. It appears the onUnload handler on a child is deleting its own parent, so that when the handler gets called on the parent, it is already freed.

### sh...@chromium.org (2016-07-23)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### ke...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### ji...@gmail.com (2016-07-26)

what is the PSIRT number?

### ji...@gmail.com (2016-07-26)

[Comment Deleted]

### ji...@gmail.com (2016-07-26)

@natashenka Thanks for your reply above!

### sh...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### ji...@gmail.com (2016-07-29)

@natashenka: I want to know this issue whether have a PSIRT number? And if this issue submitted by others,please let me know as soon as possible. Thanks!

### na...@google.com (2016-07-29)

Sorry, forgot to update this issue. This is PSIRT-5644.

### ji...@gmail.com (2016-07-30)

@natashenka That's OK!

### oc...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### na...@google.com (2016-09-22)

Fixed in September Update

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-25)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-26)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### sh...@chromium.org (2016-09-29)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-10-07)

Nothing to merge here.

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

Congratulations, the panel decided to award $3,000 for this bug.  A member of our finance team should be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-12-30)

This issue was migrated from crbug.com/chromium/630547?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084920)*
