# Security: Crash in Adobe Flash Player (24.0.0.154)

| Field | Value |
|-------|-------|
| **Issue ID** | [40085952](https://issues.chromium.org/issues/40085952) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Linux, Mac, Windows |
| **CVE IDs** | CVE-2017-2928 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-11-12 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 56.0.2917.0 canary (64-bit)
Operating System: Windows 7
Flash:	24.0.0.154

Crash ID 7b15927c-76e5-4b6e-a6b9-8d772d95fdcf


rax=0000000000000001 rbx=000002b1bfbdd660 rcx=000002b1bfc60001
rdx=000002b1bfc60000 rsi=000000000021d1d8 rdi=000000000021d350
rip=000007fed1d9408a rsp=000000000021d150 rbp=000000000021d260
 r8=000000000021d1d8  r9=000002b1bfc60001 r10=000002b1bfc60001
r11=000002df136d9000 r12=000000000021d600 r13=0000000000000000
r14=0000000000000000 r15=000002b1bfbf8508
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=0000  ds=0000  es=0000  fs=0053  gs=002b             efl=00010202
*** WARNING: Unable to verify checksum for pepflashplayer.dll
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for pepflashplayer.dll - 
pepflashplayer!PPP_ShutdownBroker+0x2af8fa:
000007fe`d1d9408a f20f1002        movsd   xmm0,mmword ptr [rdx] ds:000002b1`bfc60000=????????????????
0:000> k
  *** Stack trace for last set context - .thread/.cxr resets it
Child-SP          RetAddr           Call Site
00000000`0021d150 000007fe`d1d20fe2 pepflashplayer!PPP_ShutdownBroker+0x2af8fa
00000000`0021d1a0 000007fe`d1d7f3f9 pepflashplayer!PPP_ShutdownBroker+0x23c852
00000000`0021d1d0 000007fe`d1cf3a83 pepflashplayer!PPP_ShutdownBroker+0x29ac69
00000000`0021d210 000007fe`d1cf4a68 pepflashplayer!PPP_ShutdownBroker+0x20f2f3
00000000`0021d410 000007fe`d1d7fce8 pepflashplayer!PPP_ShutdownBroker+0x2102d8
00000000`0021d470 000007fe`d1cf3a83 pepflashplayer!PPP_ShutdownBroker+0x29b558
00000000`0021d540 000007fe`d1ed0a6a pepflashplayer!PPP_ShutdownBroker+0x20f2f3
00000000`0021d750 000007fe`d1ccc5a7 pepflashplayer!PPP_ShutdownBroker+0x3ec2da
00000000`0021df00 000007fe`d1ccd5ee pepflashplayer!PPP_ShutdownBroker+0x1e7e17
00000000`0021df60 000007fe`d1d15a29 pepflashplayer!PPP_ShutdownBroker+0x1e8e5e
00000000`0021e220 000007fe`d1d159d6 pepflashplayer!PPP_ShutdownBroker+0x231299
00000000`0021e250 000007fe`d1cdbc01 pepflashplayer!PPP_ShutdownBroker+0x231246
00000000`0021e2a0 000007fe`d1afb61d pepflashplayer!PPP_ShutdownBroker+0x1f7471
00000000`0021e330 000007fe`d1b211d6 pepflashplayer!PPP_ShutdownBroker+0x16e8d
00000000`0021e540 000007fe`d1b2146c pepflashplayer!PPP_ShutdownBroker+0x3ca46
*** WARNING: Unable to verify checksum for chrome_child.dll
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for chrome_child.dll - 
00000000`0021e5e0 000007fe`d528fd30 pepflashplayer!PPP_ShutdownBroker+0x3ccdc
00000000`0021e610 000007fe`d52d617d chrome_child!IsSandboxedProcess+0x2063c
00000000`0021e640 000007fe`d52aafe2 chrome_child!IsSandboxedProcess+0x66a89
00000000`0021e6b0 000007fe`d52aab0c chrome_child!IsSandboxedProcess+0x3b8ee
00000000`0021e6e0 000007fe`d52aac56 chrome_child!IsSandboxedProcess+0x3b418

## Attachments

- [TestButton.swf](attachments/TestButton.swf) (application/octet-stream, 27.3 KB)
- [7b15927c-76e5-4b6e-a6b9-8d772d95fdcf.dmp](attachments/7b15927c-76e5-4b6e-a6b9-8d772d95fdcf.dmp) (application/octet-stream, 273.8 KB)

## Timeline

### ri...@chromium.org (2016-11-14)

Forwarding flash bugs to natashenka@.

### ch...@gmail.com (2016-11-18)

Any updates on this bug?

### ke...@chromium.org (2016-11-18)

Any update on triaging this? Thanks.

### na...@google.com (2016-11-18)

This appears to be an out-of-bounds read in getting the blend mode of a display object. I've reported it to Adobe.

### na...@google.com (2016-11-18)

Also, how do you want to be credited on Adobe's bulletin?

### ch...@gmail.com (2016-11-18)

Khalil Zhani. Thank you.

### me...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### sh...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-21)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### bu...@google.com (2016-12-07)

Removing ReleaseBlock-Beta since this will be fixed and updated with Flash separate from M56.

### sh...@chromium.org (2016-12-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-12-29)

Tested on 57.0.2965.1 (Canary) with 24.0.0.186 (Flash), seems like fixed.

### aw...@chromium.org (2017-01-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-03)

[Empty comment from Monorail migration]

### aw...@google.com (2017-01-10)

[Empty comment from Monorail migration]

### na...@google.com (2017-01-10)

This was fixed today as CVE-2017-2928. It is ready for Rewards Panel.

### wf...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-04)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-06)

Please merge your change to M57 branch 2987 before 5:00 PM PT, Monday (02/06/) so we can pick it up for next Beta release. Thank you.

### sh...@chromium.org (2017-02-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-07)

If possible, please merge your change to M57 branch 2987 before 5:00 PM PT today, Tuesday (02/07/17) so we can pick it up for tomorrow's Beta release. Thank you.

### go...@chromium.org (2017-02-09)

Please merge your change to M57 branch 2987 before 5:00 PM PT, Friday 02/10 (sooner the better please) so we can take it in for next week beta release. Thank you.

### go...@chromium.org (2017-02-09)

+awhalley@, could you please check if M57 merge is needed here. If not, please remove "Merge-Approved-57" label. Thank you.

### sh...@chromium.org (2017-02-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-02-10)

[Empty comment from Monorail migration]

### mb...@chromium.org (2017-02-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

Thanks for the report!  The panel decided to award $500 for this one.

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-04-19)

This issue was migrated from crbug.com/chromium/664756?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085952)*
