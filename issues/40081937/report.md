# OS X memory corruption in IGFence::release from KEEN Team

| Field | Value |
|-------|-------|
| **Issue ID** | [40081937](https://issues.chromium.org/issues/40081937) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2015-3702 |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-04-25 |
| **Bounty** | $5,000.00 |

## Description

[Chromium bug variant of https://code.google.com/p/google-security-research/issues/detail?id=347 for reward consideration as an OS-level sandbox escape]

---
Credit is to KEEN Team.

Vulnerability: Yosemite 10.10.2 IGFence::release memory corruption

Description:
This vulnerability can be triggered via Safari/Chrome sandbox.
When calling the PoC attached, the following function could be reached:
__text:000000000002C316 ; __int64 __fastcall IGFence::release(IGFence *__hidden this, unsigned int *)
__text:000000000002C316                 public __ZN7IGFence7releaseERj
__text:000000000002C316 __ZN7IGFence7releaseERj proc near       ; CODE XREF: IGAccelDisplayPipe::startScaledMode(IntelScaledModeData *)+E2^Xp
__text:000000000002C316                                         ; IGAccelDisplayPipe::stopScaledMode(IntelScaledModeData *)+4C^Xp ...
__text:000000000002C316                 push    rbp
__text:000000000002C317                 mov     rbp, rsp
__text:000000000002C31A                 bsf     eax, [rsi]
__text:000000000002C31D                 dec     dword ptr [rdi+rax*4+8]
__text:000000000002C321                 jz      short loc_2C325
__text:000000000002C323                 pop     rbp
__text:000000000002C324                 retn
At that time RAX and RDI can be the value bellow:
RAX: 0xffffff7fa8d51ab0, RBX: 0xffffff8047bff000, RCX: 0x0000000001000000, RDX: 0xffffff8037a11420
RSP: 0xffffff812fcbbb90, RBP: 0xffffff812fcbbb90, RSI: 0xffffff8047bfff90, RDI: 0xffffff803a6def98
R8:  0x0000000000000367, R9:  0x000000011e774000, R10: 0xffffff8043c293c0, R11: 0xffffff8047f96a30
By executing "dec     dword ptr [rdi+rax*4+8]" instruction, it could cause arbitrary memory decreasing, and it is possible to exploit this vulnerability.
---


## Attachments

- [main.c](attachments/main.c) (application/octet-stream, 3.6 KB)

## Timeline

### mb...@google.com (2015-12-14)

Fixed in https://support.apple.com/en-us/HT204942 (CVE-2015-3702)

### cl...@chromium.org (2015-12-15)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-01-09)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-03-22)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-24)

Found this old bug in a cleanup before I jump ship (our old script had -reporter:scaryb...@gmail.com in it). $5,000 for this report.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@google.com (2016-11-18)

[Empty comment from Monorail migration]

### is...@google.com (2016-11-18)

This issue was migrated from crbug.com/chromium/481298?no_tracker_redirect=1

[Auto-CCs applied]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081937)*
