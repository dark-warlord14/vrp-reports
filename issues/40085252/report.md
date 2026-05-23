# Adobe Flash Player NetStream Use-After-Free Remote Code Execution Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40085252](https://issues.chromium.org/issues/40085252) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2016-6981 |
| **Reporter** | be...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-08-31 |
| **Bounty** | $3,000.00 |

## Description

Hello,

There is a UAF Vulnerability in Adobe Flash Player which could lead to Remote Code Execution Vulnerability.

Tested Platforms: 
1) Windows 7 SP1 x86 + Flash Player 23 Beta Standalone(23.0.0.151) with page heap enabled (gflags.exe -I flashplayer_23_sa.exe +ust +hpa)

When using flashplayer_23_sa.exe to load the Poc.swf, it manifests itself in the form of the following crash:

---cut---

0:000> r
eax=0000000c ebx=00000000 ecx=0806b430 edx=00000000 esi=07f92f70 edi=0490c020
eip=001b852b esp=0114daf0 ebp=0114dc44 iopl=0         nv up ei pl nz na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010206
FlashPlayer!WinMainSandboxed+0x159532:
001b852b 8b01            mov     eax,dword ptr [ecx]  ds:0023:0806b430=????????
001b852d 53              push    ebx
001b852e 8d9680000000    lea     edx,[esi+80h]
001b8534 52              push    edx
001b8535 8d5674          lea     edx,[esi+74h]
001b8538 52              push    edx
001b8539 53              push    ebx
001b853a 53              push    ebx
001b853b 53              push    ebx
001b853c ff761c          push    dword ptr [esi+1Ch]
001b853f ff7610          push    dword ptr [esi+10h]
001b8542 ff500c          call    dword ptr [eax+0Ch]

0:000> kb
ChildEBP RetAddr  Args to Child              
0114dc44 006e1c14 00000000 00000004 0114dc6c FlashPlayer!WinMainSandboxed+0x159532
0114dc54 778d4f56 006e20be 00000000 00000004 FlashPlayer!IAEModule_AEModule_PutKernel+0x180164
0114dc6c 778d5083 0114dd2c 0114dcb0 00000024 ntdll!RtlpWalk32BitStack+0x73
0114dccc 7795e531 00000000 081fff80 0115a868 ntdll!RtlWalkFrameChain+0x73
0114dd34 6605c23f 081ef0a4 06c90f70 0989f5e0 ntdll!RtlpStdLockRelease+0xa
0114de04 755abf52 ffffffff 0114d000 0114de54 d3d9!Direct3DCreate9Ex+0xf56a
0114de1c 000946b8 0114d000 0114de54 0000001c KERNELBASE!VirtualQuery+0x15
0114de88 000a910d 0471a280 0490665c 001bb3b7 FlashPlayer!WinMainSandboxed+0x356bf
0114de94 001bb3b7 0114dee8 001bb3be 00000000 FlashPlayer!WinMainSandboxed+0x4a114
0114de9c 001bb3be 00000000 04906000 0490665c FlashPlayer!WinMainSandboxed+0x15c3be
0114dee8 0008969e 04906000 0490665c 0114df2a FlashPlayer!WinMainSandboxed+0x15c3c5
0114dfa0 0008c3cc 00000001 00000001 04906000 FlashPlayer!WinMainSandboxed+0x2a6a5
0114e0e4 00099880 00000001 00000001 00000000 FlashPlayer!WinMainSandboxed+0x2d3d3
0114e100 778d4f56 006e1675 00000000 00000004 FlashPlayer!WinMainSandboxed+0x3a887
0114e118 0114e1a4 00000000 773fc5ab 00c5cd4c ntdll!RtlpWalk32BitStack+0x73
0114e208 00231905 002907de 00000113 00000001 0x114e1a4
00000000 00000000 00000000 00000000 00000000 FlashPlayer!WinMainSandboxed+0x1d290c

0:000> !heap -p -a ecx
    address 0806b430 found in
    _DPH_HEAP_ROOT @ 4591000
    in free-ed allocation (  DPH_HEAP_BLOCK:         VirtAddr         VirtSize)
                                    7eb3a90:          806b000             e000
    6a8e90b2 verifier!AVrfDebugPageHeapFree+0x000000c2
    77967904 ntdll!RtlDebugFreeHeap+0x0000002f
    7792ad81 ntdll!RtlpFreeHeap+0x0000005d
    778f73a6 ntdll!RtlFreeHeap+0x00000142
    773fc584 kernel32!HeapFree+0x00000014

---cut---

This Vulnerability was discovered by 'bo13oy of CloverSec Labs'.

Thank you,

bo13oy
CloverSec Labs

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 1.2 KB)

## Timeline

### va...@chromium.org (2016-09-01)

natashenka@ -- can you please take a look at this? Thanks.

[Monorail components: Internals>Plugins>Flash]

### va...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### na...@google.com (2016-09-01)

Looks good, I'll report it to Adobe

### in...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-09-01)

+awhalley@

### aw...@chromium.org (2016-09-01)

Won't block M53 stable release; will have to wait until next drop from Adobe.

### sh...@chromium.org (2016-09-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-15)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-09-30)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@gmail.com (2016-10-07)

It seems this issue hasn't been updated for a long time. I would like to know whether this case has been properly handled and reported to Adobe. Thanks.

### mm...@chromium.org (2016-10-11)

natashenka@, would you mind giving an update? What did Adobe say?

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-11-28)

natashenka: ping :) Any updates on this? 

### [Deleted User] (2016-11-28)

I believe that this is Adobe PSIRT 5799, which is CVE-2016-6981, and was fixed in the following versions: 23.0.0.185, 18.0.0.382, 11.2.202.637



### na...@google.com (2016-11-28)

Yes, that's the case, this bug is fixed and ready for the rewards panel

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-02-24)

Marking as fixed based on #18. +awhalley: does this need to be tagged for the rewards panel?

### aw...@chromium.org (2017-02-24)

It only hits my VRP queries once marked as fixed.  It's now in the queue for consideration.  Cheers!

### sh...@chromium.org (2017-02-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

Congratulations! The panel decided to award $3,000 for this bug.

### be...@gmail.com (2017-03-14)

Thanks!

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-06-02)

This issue was migrated from crbug.com/chromium/642691?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085252)*
