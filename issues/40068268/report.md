# Security:  Debug check failed: page->area_size() >= static_cast<size_t>(page->live_bytes())

| Field | Value |
|-------|-------|
| **Issue ID** | [40068268](https://issues.chromium.org/issues/40068268) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | dd...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2023-07-28 |
| **Bounty** | $10,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

// #  

// # Fatal error in ../../src/heap/sweeper.cc, line 1164  

// # Debug check failed: page->area\_size() >= static\_cast<size\_t>(page->live\_bytes()) (253656 vs. 267828).  

// #  

// #  

// #  

// #FailureMessage Object: 0x7ffefaa0c0e0  

// ==== C stack trace ===============================  

//  

// Targets/V8/v8/out/fuzzbuild/d8(+0x7ea6f2) [0x562bf468d6f2]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x7e8e87) [0x562bf468be87]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x7db3ff) [0x562bf467e3ff]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x7dad85) [0x562bf467dd85]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x108d692) [0x562bf4f30692]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x108cead) [0x562bf4f2fead]  

// Targets/V8/v8/out/fuzzbuild/d8(+0xf759a7) [0x562bf4e189a7]  

// Targets/V8/v8/out/fuzzbuild/d8(+0xf596b0) [0x562bf4dfc6b0]  

// Targets/V8/v8/out/fuzzbuild/d8(+0xf549b5) [0x562bf4df79b5]  

// Targets/V8/v8/out/fuzzbuild/d8(+0xea8816) [0x562bf4d4b816]  

// Targets/V8/v8/out/fuzzbuild/d8(+0xea491b) [0x562bf4d4791b]  

// Targets/V8/v8/out/fuzzbuild/d8(+0xea0b51) [0x562bf4d43b51]  

// Targets/V8/v8/out/fuzzbuild/d8(+0xea016f) [0x562bf4d4316f]  

// Targets/V8/v8/out/fuzzbuild/d8(+0xdbd32c) [0x562bf4c6032c]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x11db5de) [0x562bf507e5de]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x11d6681) [0x562bf5079681]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x11d512f) [0x562bf507812f]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x11d8b86) [0x562bf507bb86]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x11d9f2e) [0x562bf507cf2e]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x11d0ec8) [0x562bf5073ec8]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x11d0c56) [0x562bf5073c56]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x92bdc4) [0x562bf47cedc4]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x92b7a5) [0x562bf47ce7a5]  

// Targets/V8/v8/out/fuzzbuild/d8(+0x34f37b6) [0x562bf73967b6]  

// Received signal 6

commit cbb53f647400b97e6923b3f8706bbae6a4403d43 (HEAD, origin/main)  

Author: Manos Koukoutos [manoskouk@chromium.org](mailto:manoskouk@chromium.org)  

Date: Mon Jul 24 11:56:55 2023 +0200

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

build as debug and run with  

--expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --always-turbofan --turbofan --shared-string-table

it not stable, need run multi time

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 773 B)

## Timeline

### [Deleted User] (2023-07-28)

[Empty comment from Monorail migration]

### dd...@gmail.com (2023-07-28)

```
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:51
#1  0x00007fd4ce0b28cb in __GI_abort () at abort.c:100
#2  0x000055a8573e2b8a in v8::base::OS::Abort() ()
#3  0x000055a8573d940d in V8_Fatal(char const*, int, char const*, ...) ()
#4  0x000055a8573d8d85 in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) ()
#5  0x000055a857c9a852 in v8::internal::Sweeper::PrepareToBeSweptPage(v8::internal::AllocationSpace, v8::internal::Page*) ()
#6  0x000055a857c9a06d in v8::internal::Sweeper::AddPageImpl(v8::internal::AllocationSpace, v8::internal::Page*) ()
#7  0x000055a857b7e617 in v8::internal::MarkCompactCollector::StartSweepSpace(v8::internal::PagedSpace*) ()
#8  0x000055a857b6073a in v8::internal::MarkCompactCollector::Sweep() ()
#9  0x000055a857b59dc5 in v8::internal::MarkCompactCollector::CollectGarbage() ()
#10 0x000055a857aab326 in v8::internal::Heap::MarkCompact() ()
#11 0x000055a857aa709b in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) ()
#12 0x000055a857aa31b1 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ()
#13 0x000055a857aa27cf in v8::internal::Heap::HandleGCRequest() ()
#14 0x000055a8579bec6c in v8::internal::StackGuard::HandleInterrupts(v8::internal::StackGuard::InterruptLevel) ()
#15 0x000055a8586c8af1 in v8::internal::__RT_impl_Runtime_StackGuard(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) ()
#16 0x000055a8586c839b in v8::internal::Runtime_StackGuard(int, unsigned long*, v8::internal::Isolate*) ()
#17 0x000055a85a1099b6 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
#18 0x000055a85a189c56 in Builtins_ObjectPrototypeValueOf ()
#19 0x000055a85a165f8c in Builtins_OrdinaryToPrimitive_Number_Inline ()
#20 0x000055a85a16583a in Builtins_NonPrimitiveToPrimitive_Default ()
#21 0x00007ffdeebfd9e0 in ?? ()
#22 0x0000000000000006 in ?? ()
#23 0x0000000000000022 in ?? ()
#24 0x00007ffdeebfda30 in ?? ()
#25 0x000055a85a17fabf in Builtins_Add ()
```

### th...@chromium.org (2023-07-28)

Per these instructions[1], I am assigning this bug to the V8 sheriff (clemensb@). I don't understand everything the POC is doing, so I am not uploading it to Clusterfuzz. However, I found a duplicate Clusterfuzz bug[2] that got automatically closed out shortly after it was filed. The regression range[3] in that bug had only one CL in it which was reverted and later relanded[4]. I am not sure if that is related or not.

I'm provisionally setting high severity and extended stable FoundIn.

clemensb@: Please triage this as appropriate, including updating the severity and FoundIn.

[1]: https://chromium.googlesource.com/chromium/src/+/main/docs/security/shepherd.md#step-1_reproduce-legitimate_sounding-issues
[2]: https://crbug.com/1465342
[3]: https://chromium.googlesource.com/v8/v8/+log/c0a5e28905056ca12af50493fcfd7762178dfcf1..543b7377cd079ec5f4054edee64c7f59ad96863a?pretty=fuller&n=10000
[4]: https://crrev.com/c/4684143

### [Deleted User] (2023-07-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-28)

I am already out for the weekend, and don't work on Monday, so assigning this to next week's sheriff.

### cl...@chromium.org (2023-07-28)

[Empty comment from Monorail migration]

[Monorail components: Blink>GarbageCollection]

### [Deleted User] (2023-07-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### di...@chromium.org (2023-07-31)

I wasn't able to reproduce this crash so far with this specific commit. Which args.gn flags are you using? Without being able to repro this issue is likely not actionable for us.

Does your POC also reproduce without `--shared-string-table`?

### dd...@gmail.com (2023-07-31)

[Comment Deleted]

### dd...@gmail.com (2023-07-31)

Hi, I can not reproduce it without --shared-string-table

### di...@chromium.org (2023-07-31)

Decreasing security impact since --shared-string-table is disabled by default.

### di...@chromium.org (2023-08-01)

I am still not able to reproduce this locally with those gn args. Could you please check whether that crash reproduces with https://chromium-review.googlesource.com/c/v8/v8/+/4738814 as well?

### dd...@gmail.com (2023-08-01)

Ok, I will try it

### dd...@gmail.com (2023-08-01)

Hi, @dinfuehr@chromium.org I apply this patch and run for fifty minute. And with no crash.
Your patch can solve this bug.

### di...@chromium.org (2023-08-01)

Thanks for testing! I still can't reproduce so I might have to use you for remote debugging... From the crash stack trace above in https://crbug.com/chromium/1468458#c2 [0], could you please check where MarkSweepCollector::StartSweepSpace is called from. So whether it is old/code/shared space. Can you also shared the bottom of the stack trace to see on which thread we are on?

0: https://bugs.chromium.org/p/chromium/issues/detail?id=1468458#c2

### dd...@gmail.com (2023-08-01)

Hi, I can not find that poc (I have multi poc), by the way, I don't know which poc cause this backtrace. and this backtrace is a little different with https://crbug.com/chromium/1468458#c2. I will build a debug one to get more info
```
#3  0x000055d7cf68540d in V8_Fatal(char const*, int, char const*, ...) ()
#4  0x000055d7cf684d85 in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) ()
#5  0x000055d7cff46852 in v8::internal::Sweeper::PrepareToBeSweptPage(v8::internal::AllocationSpace, v8::internal::Page*) ()
#6  0x000055d7cff4606d in v8::internal::Sweeper::AddPageImpl(v8::internal::AllocationSpace, v8::internal::Page*) ()
#7  0x000055d7cfe2a617 in v8::internal::MarkCompactCollector::StartSweepSpace(v8::internal::PagedSpace*) ()
#8  0x000055d7cfe0c73a in v8::internal::MarkCompactCollector::Sweep() ()
#9  0x000055d7cfe05dc5 in v8::internal::MarkCompactCollector::CollectGarbage() ()
#10 0x000055d7cfd57326 in v8::internal::Heap::MarkCompact() ()
#11 0x000055d7cfd5309b in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) ()
#12 0x000055d7cfd4f1b1 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ()
#13 0x000055d7cfd51f58 in v8::internal::Heap::FinalizeIncrementalMarkingAtomically(v8::internal::GarbageCollectionReason) ()
#14 0x000055d7cfded9a4 in v8::internal::IncrementalMarkingJob::Task::RunInternal() ()
#15 0x000055d7cf6919cc in v8::platform::DefaultPlatform::PumpMessageLoop(v8::Isolate*, v8::platform::MessageLoopBehavior) ()
#16 0x000055d7cf5d7d6b in v8::(anonymous namespace)::ProcessMessages(v8::Isolate*, std::__Cr::function<v8::platform::MessageLoopBehavior ()> const&) ()
#17 0x000055d7cf5d76aa in v8::Shell::RunMainIsolate(v8::Isolate*, bool) ()
#18 0x000055d7cf5d6ee5 in v8::Shell::RunMain(v8::Isolate*, bool) ()
#19 0x000055d7cf5d9a49 in v8::Shell::Main(int, char**) ()
#20 0x00007f4c606ffc87 in __libc_start_main (main=0x55d7cf5da830 <main>, argc=10, argv=0x7ffefac0a7f8, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7ffefac0a7e8) at ../csu/libc-start.c:310
#21 0x000055d7cf58102a in _start ()
```

### dd...@gmail.com (2023-08-02)

[Comment Deleted]

### dd...@gmail.com (2023-08-02)

called in StartSweepSpace(heap_->shared_space());

### di...@chromium.org (2023-08-02)

Thanks, that helps! Can you please check whether this CL fixes this issues as well: https://chromium-review.googlesource.com/c/v8/v8/+/4738817?

### gi...@appspot.gserviceaccount.com (2023-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b8abd0e17fe38ee9f0a7c822827b06a54dd2c07c

commit b8abd0e17fe38ee9f0a7c822827b06a54dd2c07c
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Wed Aug 02 10:59:43 2023

[heap] Free LABs on incremental marking start

Free LABs in the safepoint for starting incremental marking. This
avoids having LABs on allocation candidates. While this isn't
necessary for correctness, it avoids corner cases when giving back
unused memory of a LAB to the free list.

It also helps with not creating more additional work for evacuators
due to allocations. So far we did not consider pages with main thread
LABs as evacuation candidates. However, we didn't handle background
threads. Freeing all LABs means that not even background threads can
have LABs on evacuation candidates anymore.

Bug: chromium:1468458
Change-Id: Ib16389157eaf14b1bb7d897242bafa559bbc964b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4738817
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89315}

[modify] https://crrev.com/b8abd0e17fe38ee9f0a7c822827b06a54dd2c07c/src/heap/incremental-marking.cc
[modify] https://crrev.com/b8abd0e17fe38ee9f0a7c822827b06a54dd2c07c/src/heap/concurrent-allocator.cc
[modify] https://crrev.com/b8abd0e17fe38ee9f0a7c822827b06a54dd2c07c/src/heap/mark-compact.cc


### dd...@gmail.com (2023-08-02)

I apply this patch and run 30 minute, no crash

### di...@chromium.org (2023-08-03)

Great! Thanks for testing, the bug seems to be closed now.

### di...@chromium.org (2023-08-03)

*fixed

### sa...@google.com (2023-08-03)

I guess you're the more appropriate owner, Dominik :)

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-09)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and input in the reproduction and verification process --appreciate your efforts here and in reporting this issue to us. 

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1468458?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068268)*
