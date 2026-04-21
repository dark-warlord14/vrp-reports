# Security: Fatal error in ../../src/heap/mark-compact.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40062345](https://issues.chromium.org/issues/40062345) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | wh...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-12-22 |
| **Bounty** | $7,000.00 |

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

v8 main branch  

commit: 90eeb55fc7c297f7de263fb0f0e72d97a26cb52a

# 

# Fatal error in ../../src/heap/mark-compact.cc, line 2606

# Debug check failed: heap()->Contains(object).

# 

# 

# 

#FailureMessage Object: 0x7ffd529a1eb0  

==== C stack trace ===============================

```
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0x6fa332) [0x56018e886332]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0x6f8e47) [0x56018e884e47]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0x6ebaba) [0x56018e877aba]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0x6eb415) [0x56018e877415]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xdd9703) [0x56018ef65703]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xdd79c4) [0x56018ef639c4]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xdd7109) [0x56018ef63109]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xdcd402) [0x56018ef59402]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xdcc622) [0x56018ef58622]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xd360ff) [0x56018eec20ff]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xd31ed2) [0x56018eebded2]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xd2e5c4) [0x56018eeba5c4]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xd2d153) [0x56018eeb9153]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0xc623a9) [0x56018edee3a9]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0x1860d6c) [0x56018f9ecd6c]  
/home/uuu/v8_src.main/v8/out/fuzzbuild/d8(+0x186069c) [0x56018f9ec69c]  
[0x56011feafeb8]  

```

Received signal 6  

[1] 115046 abort (core dumped) /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8 --expose-gc --future --harmony

## Attachments

- [program_20221217124453_B70784F2-F324-4DA7-8623-0BC8C3DB8386_flaky.js](attachments/program_20221217124453_B70784F2-F324-4DA7-8623-0BC8C3DB8386_flaky.js) (text/plain, 8.8 KB)
- [1.js](attachments/1.js) (text/plain, 7.2 KB)

## Timeline

### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6326918904479744.

### xi...@chromium.org (2022-12-22)

Looks like ClusterFuzz is not able to reproduce. It encounters the following error:

fuzzilli('FUZZILLI_PRINT', 'PROBING_RESULTS: ' + stringify(results));
        ^
ReferenceError: fuzzilli is not defined

Reporter, could you share another PoC or a symbolized stack trace for us to identify the root cause? Thanks!

### wh...@gmail.com (2022-12-23)

[Comment Deleted]

### [Deleted User] (2022-12-23)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wh...@gmail.com (2022-12-23)

use new PoC

pwndbg> k
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
#1  0x00007f0686bf9859 in __GI_abort () at abort.c:79
#2  0x00007f068745a9f8 in v8::base::OS::Abort () at ../../src/base/platform/platform-posix.cc:677
#3  0x00007f068742c3f6 in V8_Fatal (file=0x7f0688b3b104 "../../src/heap/mark-compact.cc", line=2606, format=0x7f06873ffef7 "Debug check failed: %s.") at ../../src/base/logging.cc:167
#4  0x00007f068742be1c in v8::base::(anonymous namespace)::DefaultDcheckHandler (file=0x7f0688b3b104 "../../src/heap/mark-compact.cc", line=2606, message=0x7f0688c5569d "heap()->Contains(object)") at ../../src/base/logging.cc:57
#5  0x00007f068742c487 in V8_Dcheck (file=0x7f0688b3b104 "../../src/heap/mark-compact.cc", line=2606, message=0x7f0688c5569d "heap()->Contains(object)") at ../../src/base/logging.cc:171
#6  0x00007f068a9a92ef in v8::internal::MarkCompactCollector::ProcessMarkingWorklist (this=0x56279b2695d0, bytes_to_process=0, mode=v8::internal::MarkCompactCollector::MarkingWorklistProcessingMode::kDefault) at ../../src/heap/mark-compact.cc:2606
#7  0x00007f068a9a810f in v8::internal::MarkCompactCollector::ProcessMarkingWorklist (this=0x56279b2695d0, bytes_to_process=0) at ../../src/heap/mark-compact.cc:2570
#8  0x00007f068a9a7f03 in v8::internal::MarkCompactCollector::ProcessEphemerons (this=0x56279b2695d0) at ../../src/heap/mark-compact.cc:2433
#9  0x00007f068a9a7858 in v8::internal::MarkCompactCollector::MarkTransitiveClosureUntilFixpoint (this=0x56279b2695d0) at ../../src/heap/mark-compact.cc:2400
#10 0x00007f068a9a978e in v8::internal::MarkCompactCollector::MarkTransitiveClosure (this=0x56279b2695d0) at ../../src/heap/mark-compact.cc:2666
#11 0x00007f068a99e66a in v8::internal::MarkCompactCollector::MarkLiveObjects (this=0x56279b2695d0) at ../../src/heap/mark-compact.cc:2831
#12 0x00007f068a99d37b in v8::internal::MarkCompactCollector::CollectGarbage (this=0x56279b2695d0) at ../../src/heap/mark-compact.cc:611
#13 0x00007f068a922a5b in v8::internal::Heap::MarkCompact (this=0x56279b1cf048) at ../../src/heap/heap.cc:2563
#14 0x00007f068a91f822 in v8::internal::Heap::PerformGarbageCollection (this=0x56279b1cf048, collector=v8::internal::GarbageCollector::MARK_COMPACTOR, gc_reason=v8::internal::GarbageCollectionReason::kFinalizeMarkingViaStackGuard, collector_reason=0x7f0688b2586f "GC in old space requested") at ../../src/heap/heap.cc:2252
#15 0x00007f068a91ca96 in v8::internal::Heap::CollectGarbage (this=0x56279b1cf048, space=v8::internal::OLD_SPACE, gc_reason=v8::internal::GarbageCollectionReason::kFinalizeMarkingViaStackGuard, gc_callback_flags=v8::kGCCallbackScheduleIdleGarbageCollection) at ../../src/heap/heap.cc:1714
#16 0x00007f068a91b849 in v8::internal::Heap::CollectAllGarbage (this=0x56279b1cf048, flags=0, gc_reason=v8::internal::GarbageCollectionReason::kFinalizeMarkingViaStackGuard, gc_callback_flags=v8::kGCCallbackScheduleIdleGarbageCollection) at ../../src/heap/heap.cc:1431
#17 0x00007f068a91b78d in v8::internal::Heap::HandleGCRequest (this=0x56279b1cf048) at ../../src/heap/heap.cc:1399
#18 0x00007f068a7a9b30 in v8::internal::StackGuard::HandleInterrupts (this=0x56279b1c1f48) at ../../src/execution/stack-guard.cc:293
#19 0x00007f068b343d82 in v8::internal::__RT_impl_Runtime_StackGuard (args=..., isolate=0x56279b1c1f40) at ../../src/runtime/runtime-internal.cc:335
#20 0x00007f068b3438e8 in v8::internal::Runtime_StackGuard (args_length=0, args_object=0x7ffda5021370, isolate=0x56279b1c1f40) at ../../src/runtime/runtime-internal.cc:324
#21 0x00007f061f96eaff in ?? ()
#22 0x00007ffda50213f0 in ?? ()

### cl...@chromium.org (2022-12-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5147071255609344.

### xi...@chromium.org (2022-12-24)

Looks like ClusterFuzz is still not able to reproduce. Over to the current V8 security sheriff for triage. Thanks!

### wh...@gmail.com (2022-12-24)

at my local ubuntu 20.04, 
I run 
➜  x64.debug git:(main) ./d8 --expose-gc --future --harmony --assert-types --harmony-rab-gsab --harmony-struct --allow-natives-syntax --interrupt-budget=1000 --fuzzing ~/1.js


#
# Fatal error in ../../src/heap/mark-compact.cc, line 2606
# Debug check failed: heap()->Contains(object).
#
#
#
#FailureMessage Object: 0x7ffe03789068
==== C stack trace ===============================

    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fc3da134bce]
...

at latest commit 692503619570838e251c3a241057a07cb9e32c6b still can reproduce

sometimes, it just output "{}", you should run many times.
➜  x64.debug git:(main) ./d8 --expose-gc --future --harmony --assert-types --harmony-rab-gsab --harmony-struct --allow-natives-syntax --interrupt-budget=1000 --fuzzing ~/1.js
{}




### [Deleted User] (2022-12-25)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-01-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4856155269693440.

### cl...@chromium.org (2023-01-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5143620289232896.

### cl...@chromium.org (2023-01-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6244882854379520.

### cl...@chromium.org (2023-01-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4780083888979968.

### th...@google.com (2023-01-04)

ClusterFuzz is having trouble bisecting because of the flakiness.
The object in the DCHECK line is a string, and only the --shared-string-table flag is needed to reproduce, so this is probably related to this flag. syg@, can you take a look?

### sy...@chromium.org (2023-01-05)

The root cause is in ephemeron marking around strings promoted into the shared heap:

1. An ephemeron obj -> "string" where "string" is in seq string young generation.
2. A scavenge happens, and "string" is promoted into the shared heap with --shared-string-table.
3. A mark-compact happens that shouldn't be marking objects in the shared heap, and crashes when it encounters an unexpected string in the shared heap in the ephemeron worklist.

I'm not yet sure what the best fix is, cc'ing dinfuehr@.

### cl...@chromium.org (2023-01-10)

ClusterFuzz testcase 4780083888979968 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-01-10)

ClusterFuzz testcase 4856155269693440 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=85174:85175

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c57a13dc3bde8d70396d15e897125376a0fe7c52

commit c57a13dc3bde8d70396d15e897125376a0fe7c52
Author: Shu-yu Guo <syg@chromium.org>
Date: Thu Jan 12 19:26:42 2023

[heap] Skip ephemeron values that shouldn't be marked

Bug: chromium:1403129
Change-Id: Ic26583be78e4e16a5bc18d8d8ce2bfb79ec70dad
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4136976
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85270}

[modify] https://crrev.com/c57a13dc3bde8d70396d15e897125376a0fe7c52/src/heap/marking-visitor-inl.h
[modify] https://crrev.com/c57a13dc3bde8d70396d15e897125376a0fe7c52/src/heap/mark-compact.cc


### am...@chromium.org (2023-01-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### am...@chromium.org (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-18)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M108. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M109. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: M108 is already shipping to stable.

Merge review required: M109 is already shipping to stable.

Merge review required: M110 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [108, 109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-01-18)

This bug depends on the shared string table, which is off by default, so it doesn't impact head or needs back merges. Do I just remove the Merge-Review-* labels or should I add other labels?

### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-18)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@chromium.org (2023-01-18)

thanks syg@ for updating with SI-None and that's correct - no backmerges needed; I've just removed all the merge review labels. 

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-25)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. Thank you.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1403129?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062345)*
