# OS X memory corruption in IOAccelSurface2::set_shape_backing_length_ext from KEEN Team

| Field | Value |
|-------|-------|
| **Issue ID** | [40081938](https://issues.chromium.org/issues/40081938) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2015-3706 |
| **Reporter** | sc...@gmail.com |
| **Assignee** | ia...@chromium.org |
| **Created** | 2015-04-25 |
| **Bounty** | $5,000.00 |

## Description

[Chromium bug variant of https://code.google.com/p/google-security-research/issues/detail?id=348 for reward consideration as an OS-level sandbox escape]

---
Vulnerability: Yosemite 10.10.2 IOAccelSurface2::set_shape_backing_length_ext OOB read/write if InputStructLength is larger than 4096

Description:
This vulnerability can be reached via Safari/Chrome sandbox.
In IOKit framework, when inputStructCnt is larger than 4096, in the kext implementation, the code should use structureInputDescriptor::getAddress() to get the correct buffer address. However, set_shape_backing_length_ext still obtains its buffer by referencing inputStruct, which caused unexpected behavior here:

__text:0000000000024989 loc_24989:                              ; CODE XREF: IOAccelSurface2::set_shape_backing_length_ext(eIOAccelSurfaceShapeBits,uint,ulong long,uint,ulong long,IOAccelDeviceRegion *,ulong long)+4E4^Yj
__text:0000000000024989                 mov     eax, ecx
__text:000000000002498B                 mov     rdx, [rbx]
__text:000000000002498E                 mov     rsi, [rdi+rax*8+0Ch] //OOB read
__text:0000000000024993                 mov     [rdx+rax*8+0Ch], rsi //OOB write
__text:0000000000024998                 inc     ecx
__text:000000000002499A                 mov     eax, [rdi]
__text:000000000002499C                 cmp     ecx, eax
__text:000000000002499E                 jb      short loc_24989
__text:00000000000249A0                 cmp     eax, 1
__text:00000000000249A3                 mov     r14d, [rbp+var_74]
__text:00000000000249A7                 jnz     short loc_249CD
__text:00000000000249A9                 cmp     word ptr [rdi+10h], 0
__text:00000000000249AE                 jz      short loc_249BC
__text:00000000000249B0                 mov     ecx, 1
__text:00000000000249B5                 cmp     word ptr [rdi+12h], 0
__text:00000000000249BA                 jnz     short loc_249CF

panic(cpu 4 caller 0xffffff802341a46e): Kernel trap at 0xffffff7fa547f96e, type 14=page fault, registers:
CR0: 0x000000008001003b, CR2: 0xffffff8035746000, CR3: 0x000000010500b06e, CR4: 0x00000000001626e0
RAX: 0x0000000000040ba6, RBX: 0xffffff80354e1060, RCX: 0x0000000000040ba6, RDX: 0xffffff8167d5d000
RSP: 0xffffff812cb8bb20, RBP: 0xffffff812cb8bba0, RSI: 0xdeadbeefdeadbeef, RDI: 0xffffff80355402c4
R8:  0x0000000000000000, R9:  0x0000000000000002, R10: 0x0000000007fc0c00, R11: 0x00000000dbb487f5
R12: 0x000000002fd1000c, R13: 0xffffff80354e0000, R14: 0xffffff80354e1068, R15: 0x0000000000000000
RFL: 0x0000000000010287, RIP: 0xffffff7fa547f96e, CS:  0x0000000000000008, SS:  0x0000000000000010
Fault CR2: 0xffffff8035746000, Error code: 0x0000000000000000, Fault CPU: 0x4

Here the RAX is very large, and caused OOB read. By crafting the memory layout, the vulnerability can be exploited.
---

## Timeline

### in...@chromium.org (2015-11-03)

Reassigning to Ian from PZ. Ian, please update bug if there is any update on PZ tracking bug.

### ia...@chromium.org (2015-11-03)

Fixed in https://support.apple.com/en-us/HT204942 as CVE-2015-3706 

### cl...@chromium.org (2015-11-03)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-11-23)

No merge required - taking to reward panel for sandbox escape consideration. 

### cl...@chromium.org (2016-02-11)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly ClusterFuzz

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

This issue was migrated from crbug.com/chromium/481299?no_tracker_redirect=1

[Auto-CCs applied]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081938)*
