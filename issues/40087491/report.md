# Security: Use-after-poison in blink::FrameView::AdjustMediaTypeForPrinting

| Field | Value |
|-------|-------|
| **Issue ID** | [40087491](https://issues.chromium.org/issues/40087491) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>PrintPreview |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-04-28 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 60.0.3083.0 Canary  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Open the testcase

==4160==ERROR: AddressSanitizer: use-after-poison on address 0x5e17b834 at pc 0x1685c04b bp 0x003ea8  

bc sp 0x003ea8b0  

READ of size 4 at 0x5e17b834 thread T0  

#0 0x1685c04a (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x16b2c04a)  

#1 0x1685bbde (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x16b2bbde)  

#2 0x1685e4c2 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x16b2e4c2)  

#3 0x16f2bdd7 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x171fbdd7)  

#4 0x16f2c091 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x171fc091)  

#5 0x1735ce9a (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x1762ce9a)  

#6 0x1617c236 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x1644c236)  

#7 0x12b29a34 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x12df9a34)  

#8 0x12b320ad (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x12e020ad)  

#9 0x12b2b97d (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x12dfb97d)  

#10 0x12b2c207 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x12dfc207)  

#11 0x12b396ec (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x12e096ec)  

#12 0x12b30dd9 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x12e00dd9)  

#13 0x12b5a88c (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x12e2a88c)  

#14 0x12be32df (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x12eb32df)  

#15 0x1c0b70a2 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x1c3870a2)  

#16 0x1694c2ea (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x16c1c2ea)  

#17 0x169131d6 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x16be31d6)  

#18 0x169141a6 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x16be41a6)  

#19 0x169135b8 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x16be35b8)  

#20 0x174049e6 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x176d49e6)  

#21 0x17404418 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x176d4418)  

#22 0x1737a7fd (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x1764a7fd)  

#23 0x18badf6e (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x18e7df6e)  

#24 0x188425d2 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x18b125d2)  

#25 0x18baaf15 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x18e7af15)  

#26 0x18baa0de (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x18e7a0de)  

#27 0x188e81ff (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x18bb81ff)  

#28 0x18a6204d (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x18d3204d)  

#29 0x15b50fcb (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x15e20fcb)  

#30 0x1a04be1c (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x1a31be1c)  

#31 0x15b89635 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x15e59635)  

#32 0x132a5f26 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x13575f26)  

#33 0x1669d546 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x1696d546)  

#34 0x16698567 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x16968567)  

#35 0x15029b38 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x152f9b38)  

#36 0x132a5f26 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x13575f26)  

#37 0x13142ed0 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x13412ed0)  

#38 0x13143d66 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x13413d66)  

#39 0x131451b6 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x134151b6)  

#40 0x132ac4fa (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x1357c4fa)  

#41 0x13141d6a (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x13411d6a)  

#42 0x131e27e4 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x134b27e4)  

#43 0x1884bea5 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x18b1bea5)  

#44 0x13005790 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x132d5790)  

#45 0x13006d83 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x132d6d83)  

#46 0x13008e46 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x132d8e46)  

#47 0x13005474 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x132d5474)  

#48 0xfd31232 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome\_child.dll+0x10001232)  

#49 0x1219d95 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome.exe+0x409d95)  

#50 0x1211b84 (C:\Users\admin\Desktop\asan-win32-release-467954\chrome.exe+0x401b84)  

#51 0x14808ea (C:\Users\admin\Desktop\asan-win32-release-467954\chrome.exe+0x6708ea)  

#52 0x752b3676 (C:\Windows\syswow64\kernel32.dll+0x7dd73676)  

#53 0x77579d71 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9d71)  

#54 0x77579d44 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9d44)

Address 0x5e17b834 is a wild pointer.  

SUMMARY: AddressSanitizer: use-after-poison (C:\Users\admin\Desktop\asan-win32-release-467954\chrome  

\_child.dll+0x16b2c04a)  

Shadow bytes around the buggy address:  

0x3bc2f6b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3bc2f6c0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3bc2f6d0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3bc2f6e0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3bc2f6f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

=>0x3bc2f700: f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3bc2f710: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3bc2f720: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3bc2f730: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3bc2f740: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3bc2f750: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==4160==ABORTING

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 262 B)
- [rec.mp4](attachments/rec.mp4) (video/mp4, 583.8 KB)

## Timeline

### ch...@gmail.com (2017-04-28)

Note: This is a security regression bug seen after the fix from https://crbug.com/chromium/707549.

### cl...@chromium.org (2017-04-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5091056258646016

### pa...@chromium.org (2017-04-28)

japhet, could you please take a look or re-assign to someone more appropriate? Thanks!

[Monorail components: Blink>Internals>Frames]

### ch...@gmail.com (2017-04-28)

Actually, this is print preview's fault, I suspect this is from Lei Zhang's recent changes per https://crbug.com/chromium/707549.

### th...@chromium.org (2017-04-28)

Checking...

### th...@chromium.org (2017-04-28)

Well, before the https://crbug.com/chromium/707549 fix, the test case here would just trigger that bug instead.

[Monorail components: -Blink>Internals>Frames UI>Browser>PrintPreview]

### ch...@gmail.com (2017-04-28)

hmm... sorry for the assumption :-)

### th...@chromium.org (2017-04-28)

I might have seen this crash once in my own testing for https://crbug.com/chromium/707549, but I could not reproduce it. It took several reloads to repro, but that's still good.

### th...@chromium.org (2017-04-29)

So this crash is happening in Blink and I don't really understand Oilpan. +haraken to help take a look.

### dc...@chromium.org (2017-04-29)

I believe Oilpan poisons object that aren't marked as live, so this may be a UaF.

What line is the use-after-poison happening on?

### th...@chromium.org (2017-04-29)

This is what I have locally:

ERROR: AddressSanitizer: use-after-poison on address 0x7e8706957a48 at pc 0x558af4d54c42 bp 0x7ffe7be47950 sp 0x7ffe7be47948
READ of size 8 at 0x7e8706957a48 thread T0 (chrome)
    #0 0x558af4d54c41 in operator blink::DOMWindow * third_party/WebKit/Source/platform/heap/Member.h:80:32
    #1 0x558af4d54c41 in DomWindow third_party/WebKit/Source/core/frame/LocalFrame.cpp:535
    #2 0x558af4d54c41 in blink::LocalFrame::GetDocument() const third_party/WebKit/Source/core/frame/LocalFrame.cpp:548
    #3 0x558af4d57734 in blink::LocalFrame::SetPrinting(bool, blink::FloatSize const&, blink::FloatSize const&, float) third_party/WebKit/Source/core/frame/LocalFrame.cpp:594:7
    #4 0x558af5503e20 in blink::PrintContext::EndPrintMode() third_party/WebKit/Source/core/page/PrintContext.cpp:197:11
    #5 0x558af550256f in blink::PrintContext::~PrintContext() third_party/WebKit/Source/core/page/PrintContext.cpp:57:5
    #6 0x558aed379c0e in Finalize third_party/WebKit/Source/platform/heap/HeapPage.cpp:103:5
    #7 0x558aed379c0e in blink::NormalPage::Sweep() third_party/WebKit/Source/platform/heap/HeapPage.cpp:1340
    #8 0x558aed372780 in SweepUnsweptPage third_party/WebKit/Source/platform/heap/HeapPage.cpp:284:11
    #9 0x558aed372780 in blink::BaseArena::LazySweepWithDeadline(double) third_party/WebKit/Source/platform/heap/HeapPage.cpp:313
    #10 0x558aed388e75 in blink::ThreadState::PerformIdleLazySweep(double) third_party/WebKit/Source/platform/heap/ThreadState.cpp:636:22
    #11 0x558af48e1d3f in Run base/callback.h:80:12
    #12 0x558af48e1d3f in operator() third_party/WebKit/Source/platform/wtf/Functional.h:221
    #13 0x558af48e1d3f in blink::(anonymous namespace)::IdleTaskRunner::Run(double) third_party/WebKit/Source/platform/WebScheduler.cpp:26

### dc...@chromium.org (2017-04-29)

Oh, that seems pretty dangerous--a GCed object (PrintContext) cannot touch another GCed object (DOMWindow) during finalization, as the finalization order is not guaranteed. So like DOMWindow was already swept, and then PrintContext() tries to touch it in the destructor.

### dc...@chromium.org (2017-04-29)

(Also: the usual solution to this is to perform some sort of explicit cleanup, like FrameView::dispose(), or potentially a pre-finalizer. Usually explicit cleanup is preferred)

### ha...@chromium.org (2017-04-29)

As far as I look at the call sites of PrintContext, it seems easy to explicitly call PrintContext::dispose(). We can call EndPrintCode in PrintContext::dispose().


### th...@chromium.org (2017-04-29)

How about: https://codereview.chromium.org/2848823005

### oc...@chromium.org (2017-05-02)

thestig, any update here?

If possible we'd like to get this fixed as part of the security fixit (see email to chromium-dev) this week. Thanks!

### th...@chromium.org (2017-05-02)

Just waiting for the code review to finish.

### bu...@chromium.org (2017-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/85b7d7b31f25da2481ab2fa569c7b37a42abdeb6

commit 85b7d7b31f25da2481ab2fa569c7b37a42abdeb6
Author: thestig <thestig@chromium.org>
Date: Wed May 03 03:07:13 2017

Clear the PrintContext in WebLocalFrameImpl::Close().

Also explicitly call PrintContext::EndPrintMode(), rather than calling
it in the destructor. Add a ScopedPrintMode helper class to do that
conveniently.

BUG=716474

Review-Url: https://codereview.chromium.org/2848823005
Cr-Commit-Position: refs/heads/master@{#468882}

[modify] https://crrev.com/85b7d7b31f25da2481ab2fa569c7b37a42abdeb6/third_party/WebKit/Source/core/layout/LayoutTreeAsText.cpp
[modify] https://crrev.com/85b7d7b31f25da2481ab2fa569c7b37a42abdeb6/third_party/WebKit/Source/core/page/PrintContext.cpp
[modify] https://crrev.com/85b7d7b31f25da2481ab2fa569c7b37a42abdeb6/third_party/WebKit/Source/core/page/PrintContext.h
[modify] https://crrev.com/85b7d7b31f25da2481ab2fa569c7b37a42abdeb6/third_party/WebKit/Source/core/page/PrintContextTest.cpp
[modify] https://crrev.com/85b7d7b31f25da2481ab2fa569c7b37a42abdeb6/third_party/WebKit/Source/web/WebLocalFrameImpl.cpp


### oc...@chromium.org (2017-05-03)

Thanks!

### sh...@chromium.org (2017-05-03)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-05)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/85199fb739f0c8b8e491cd6f1ac538efb4134ad0

commit 85199fb739f0c8b8e491cd6f1ac538efb4134ad0
Author: Lei Zhang <thestig@chromium.org>
Date: Fri May 05 23:54:38 2017

M59: Clear the PrintContext in WebLocalFrameImpl::Close().

Also explicitly call PrintContext::EndPrintMode(), rather than calling
it in the destructor. Add a ScopedPrintMode helper class to do that
conveniently.

BUG=716474

Review-Url: https://codereview.chromium.org/2848823005
Cr-Commit-Position: refs/heads/master@{#468882}
(cherry picked from commit 85b7d7b31f25da2481ab2fa569c7b37a42abdeb6)

Review-Url: https://codereview.chromium.org/2864753004 .
Cr-Commit-Position: refs/branch-heads/3071@{#429}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}

[modify] https://crrev.com/85199fb739f0c8b8e491cd6f1ac538efb4134ad0/third_party/WebKit/Source/core/layout/LayoutTreeAsText.cpp
[modify] https://crrev.com/85199fb739f0c8b8e491cd6f1ac538efb4134ad0/third_party/WebKit/Source/core/page/PrintContext.cpp
[modify] https://crrev.com/85199fb739f0c8b8e491cd6f1ac538efb4134ad0/third_party/WebKit/Source/core/page/PrintContext.h
[modify] https://crrev.com/85199fb739f0c8b8e491cd6f1ac538efb4134ad0/third_party/WebKit/Source/core/page/PrintContextTest.cpp
[modify] https://crrev.com/85199fb739f0c8b8e491cd6f1ac538efb4134ad0/third_party/WebKit/Source/web/WebLocalFrameImpl.cpp


### aw...@chromium.org (2017-05-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-09)

[Empty comment from Monorail migration]

### aa...@google.com (2017-05-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

Congratulations! The panel decided to award $2,000 for this bug!  Though if you could provide symbolicated stack traces it would be greatly appreciated.

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/716474?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087491)*
