# Security: Adobe Flash MemoryProtector Heap Buffer Overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40084604](https://issues.chromium.org/issues/40084604) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2016-4249 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-06-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This is a heap buffer overflow vulnerability in flash MemoryProtector. The Memory Protector is introduced in flash 22.0.0.192 to mitigate use after free exploits.

The MemoryProtector contains a fixed array (0x400 items) to store memory blocks.  

Each time a new memory block is going to be freed, it will check the current size of the memory block array. If the array is full, it will try to reclaim the memory blocks in the array who do not have any reference on the stack. After the reclaim, the new memory block will be added to the end of the array.

However, if fails to handle the condition when the reclaim function does not free any memory block. That is, when all 0x400 items in the array have references on the stack. In such case, the memory block array will be overflowed when appending the new memory block to the end of it.

To trig this vulnerability, we need to free at least 0x400 items while all of these items have references on the stack. In 32-bit process, we can achieve this by spraying the memory and guess the addresses of these items. Then we put the address on the stack and free the items.

The attached PoC works on 32-bit windows 7 with 32-bit chrome. Please test the poc with the same environment.

**VERSION**  

Chrome Version: 51.0.2704.103 m (32-bit)  

Operating System: windows 7 en 32-bit

**REPRODUCTION CASE**

Please see the attachment for details.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

0:007> g  

Critical error detected c0000374  

(ca8.970): Break instruction exception - code 80000003 (first chance)  

eax=00000000 ebx=00000000 ecx=77861787 edx=002cdf59 esi=02090000 edi=02a17c40  

eip=77903789 esp=002ce1ac ebp=002ce224 iopl=0 nv up ei pl nz na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00000206  

ntdll!RtlReportCriticalFailure+0x29:  

77903789 cc int 3  

0:000> k  

ChildEBP RetAddr  

002ce224 779046e7 ntdll!RtlReportCriticalFailure+0x29  

002ce234 779047c7 ntdll!RtlpReportHeapFailure+0x21  

002ce268 778c9cf2 ntdll!RtlpLogHeapFailure+0xa1  

002ce2b0 77896287 ntdll!RtlpCoalesceFreeBlocks+0x84c  

002ce3a8 778965a6 ntdll!RtlpFreeHeap+0x1f4  

002ce3c8 763fc3d4 ntdll!RtlFreeHeap+0x142  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Program Files\Google\Chrome\Application\51.0.2704.103\PepperFlash\pepflashplayer.dll -  

002ce3dc 628650b0 kernel32!HeapFree+0x14  

WARNING: Stack unwind information not available. Following frames may be wrong.  

002ce3f0 6262503e pepflashplayer!curl\_getenv+0x98020  

002ce468 62044e12 pepflashplayer!PPP\_ShutdownBroker+0x5f3e4b  

002ce47c 763fc3d4 pepflashplayer!PPP\_ShutdownBroker+0x13c1f  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Program Files\Google\Chrome\Application\51.0.2704.103\chrome\_child.dll -  

002ce490 631f4eb7 kernel32!HeapFree+0x14  

002ce4b4 6206a1f8 chrome\_child!ovly\_debug\_event+0x3588  

00000000 00000000 pepflashplayer!PPP\_ShutdownBroker+0x39005

## Attachments

- [MemoryProtectorBOF.zip](attachments/MemoryProtectorBOF.zip) (application/octet-stream, 1.6 KB)

## Timeline

### es...@chromium.org (2016-06-17)

Thanks for the report.

natashenka, can you please take a look?

[Monorail components: Internals>Plugins>Flash]

### cl...@chromium.org (2016-06-18)

[Empty comment from Monorail migration]

### na...@google.com (2016-06-21)

Sorry, was away for a few days, taking look now, will report in a few minutes. Xiong, how do you want to be credited for this issue on the Adobe bulletin?

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

### xi...@gmail.com (2016-07-15)

Hi,

It seemed to be patched this month as CVE-2016-4249:
https://helpx.adobe.com/security/products/flash-player/apsb16-25.html

Is this report qualified for any bonus reward ?


### sh...@chromium.org (2016-07-21)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@gmail.com (2016-07-26)

Hello,

It seems I did not get any update after the submitted bug was patched.
So could anyone help to ask my question please:
Is this chrome reward program still accepting flash submissions?
If this program does not reward flash submissions any more, please cancel all my other submissions. And I think it is better to remove the flash target in your reward program page. 

Thank you!

### ra...@chromium.org (2016-08-02)

xiong12002@gmail.com: sorry for the delay! awhalley: can you help answer the questions in #13? Thanks!

natashenka: any updates on this? jschuh: what's the process for flash security bugs these days?

### aw...@chromium.org (2016-08-02)

xiong12002@gmail.com: Yep, flash bugs are still eligible for consideration under the Chrome VRP at this time. Bugs only start the reward process after they have been marked as fixed, which is why there are no reward- labels on this one yet.

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

### sh...@chromium.org (2017-02-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

Hello!  The panel decided to award $3000 for this bug, and an additional $133.7 because it's pretty neat you were exploiting code in an exploit mitigation :-)

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

This issue was migrated from crbug.com/chromium/620966?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084604)*
