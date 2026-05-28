# Security: Debug check failed: IsSweepingInProgress()

| Field | Value |
|-------|-------|
| **Issue ID** | [40063616](https://issues.chromium.org/issues/40063616) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | om...@chromium.org |
| **Created** | 2023-03-16 |
| **Bounty** | $8,000.00 |

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

Debug check failed: IsSweepingInProgress()

**VERSION**  

tested at current HEAD

**REPRODUCTION CASE**

This bug hard to repro.  

please run

1. build fuzzbuild-d8  
   
   if [ "$(uname)" == "Linux" ]; then
   # See <https://v8.dev/docs/compile-arm64> for instructions on how to build on Arm64
   
   gn gen out/fuzzbuild --args='is\_debug=false dcheck\_always\_on=true v8\_static\_library=true v8\_enable\_slow\_dchecks=true v8\_enable\_v8\_checks=true v8\_enable\_verify\_heap=true v8\_enable\_verify\_csa=true v8\_fuzzilli=true sanitizer\_coverage\_flags="trace-pc-guard" target\_cpu="x64"'  
   
   else  
   
   echo "Unsupported operating system"  
   
   fi

ninja -C ./out/fuzzbuild d8

2. run

for i in {1..999}; do /home/uuu/v8\_src.updated/v8/out/fuzzbuild/d8 --expose-gc --future --harmony --assert-types --maglev-assert --harmony-rab-gsab --harmony-struct --allow-natives-syntax --interrupt-budget=1000 --fuzzing --sparkplug --no-opt --lazy --allow-natives-syntax --no-always-osr --no-always-turbofan --no-force-slow-path --turbo-move-optimization --turbo-jt --no-turbo-loop-peeling --turbo-loop-variable --turbo-loop-rotation --turbo-cf-optimization --turbo-escape --turbo-allocation-folding --turbo-instruction-scheduling --turbo-stress-instruction-scheduling --no-turbo-store-elimination --turbo-rewrite-far-jumps --turbo-optimize-apply --no-enable-ssse3 --turbo-load-elimination --turbo-inlining --turbo-splitting --lazy-feedback-allocation --turbo-filter=match --allow-natives-syntax --shared-string-table poc.js ; echo $?; done

it should need some time to trigger.

then you will see  

// V8 is running with experimental features enabled. Stability and security will suffer.  

// #  

// # Fatal error in ../../src/heap/gc-tracer.cc, line 568  

// # Debug check failed: IsSweepingInProgress().  

// #  

// #  

// #

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 9.8 KB)

## Timeline

### [Deleted User] (2023-03-16)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-03-16)

run with debug d8

    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fb38283d23e]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libplatform.so(+0x4f51d) [0x7fb38279051d]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1ac) [0x7fb38280b46c]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(+0x57ebc) [0x7fb38280aebc]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x27) [0x7fb38280b527]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::GCTracer::NotifyYoungSweepingCompleted()+0x139) [0x7fb3861b83b9]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::GCTracer::NotifyFullSweepingCompleted()+0xac) [0x7fb3861b80fc]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Heap::EnsureSweepingCompleted(v8::internal::Heap::SweepingForcedFinalizationMode)+0x4c4) [0x7fb3861e3e44]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Heap::MakeHeapIterable()+0x2b) [0x7fb3861ec26b]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::MarkCompactCollector::MarkObjectsFromClientHeap(v8::internal::Isolate*)+0xba) [0x7fb38626ea9a]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(+0x3a39fb0) [0x7fb38628bfb0]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(+0x3a1c9c2) [0x7fb38626e9c2]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::MarkCompactCollector::MarkObjectsFromClientHeaps()+0x53) [0x7fb38626e933]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::MarkCompactCollector::MarkLiveObjects()+0xcd8) [0x7fb386265538]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::MarkCompactCollector::CollectGarbage()+0x5b) [0x7fb3862647fb]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Heap::MarkCompact()+0xb3) [0x7fb3861e5253]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*)+0x71a) [0x7fb3861e289a]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)+0x65d) [0x7fb3861e03ad]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Heap::CollectAllGarbage(int, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)+0x39) [0x7fb3861df5e9]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Heap::HandleGCRequest()+0xed) [0x7fb3861df52d]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::StackGuard::HandleInterrupts()+0x410) [0x7fb38606a5e0]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(+0x43e7fb2) [0x7fb386c39fb2]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Runtime_StackGuard(int, unsigned long*, v8::internal::Isolate*)+0x128) [0x7fb386c39b18]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(+0x2bbe67d) [0x7fb38541067d]


### wh...@gmail.com (2023-03-16)

[Comment Deleted]

### wh...@gmail.com (2023-03-16)

bisect 

The bug was introduced in this CL https://chromium-review.googlesource.com/c/v8/v8/+/3934769 [1]

ONLY based that CL 

active release: M113/dev M112/beta M111/stable

[1] https://chromiumdash.appspot.com/commit/8aef1fb204873527dbd8385a9c2ea79182911f1f

### ts...@chromium.org (2023-03-16)

Reporter - have you tried to minimize the PoC? Its not immediately obvious from looking at it what it is trying to do.


### ts...@chromium.org (2023-03-16)

Omer - something to ponder from the report only, but security team has not been able to verify the safety of the test case nor reproduce (redshell acting up today).  Act accordingly.


### ts...@chromium.org (2023-03-16)

Sev High, Impact None because of the flags required - seems like this would not be a shipping configuration. Please confirm.

[Monorail components: Blink>JavaScript]

### om...@chromium.org (2023-03-16)

The line "V8 is running with experimental features enabled. Stability and security will suffer." from the output tells me that the configuration the reporter used is definitely not a shipping/production configuration. However, I can't confirm that the same is not possible in a shipping configuration without reproducing it (which I'm avoiding for now based on c#6).

### sa...@google.com (2023-03-16)

Thanks for the report and bisect! To add some context, the first ~130 LoC of the testcase are this code here: https://github.com/googleprojectzero/fuzzilli/blob/main/Sources/Fuzzilli/Lifting/JavaScriptProbeLifting.swift. The actual fuzzer-generated code starts with the main function.

### om...@chromium.org (2023-03-16)

Thanks Saelo for the context. Since most of it is copied from the link you mentioned and the rest is fuzzer-generated code, I assume it's fine to try and reproduce this crash. I will go ahead and investigate this further. 

### wh...@gmail.com (2023-03-17)

sorry, please use new poc 

function main() {
function V0(v2,v3,v4,v5) {
    if (!new.target) { throw 'must be called with new'; }
    for (let v6 = 0; v6 < 4004; v6++) {
        const v8 = new BigUint64Array(v6);
    }
}
function v10(v11,v12) {
    for (let v13 = 0; v13 < 1150; v13++) {
        const v16 = new Int32Array(14990892);
    }
    return v11;
}
const v17 = "function" || "function";
const v18 = ["function","function","function","function"];
v18.type = v17;
const v20 = new Worker(v10,v18);
const v21 = new V0(v18,v10,v17,"function");
}
main(); 

run following cmd 
for i in {1..999}; do /home/uuu/v8_src.main/v8/out/fuzzbuild/d8  --harmony-struct --future  ./poc.js ; if [ $? -ne 0 ]; then break; fi; done




### sr...@google.com (2023-03-17)

@reporter, on which commit do you run your poc?
I tried the poc from https://crbug.com/chromium/1424955#c11 against 8aef1fb204873527dbd8385a9c2ea79182911f1f and it doesn't crash on my machine with the gn args from https://crbug.com/chromium/1424955#c0.

### om...@chromium.org (2023-03-17)

I am able to reproduce it on ToT. I'm currently investigating it.

### om...@chromium.org (2023-03-20)

The underlying issue is with the order in which the GC signals (to the GCTracer) the starting of an atomic pause and when it enters a global safepoint for shared GCs. To fix we will just need to reorder these steps (that are already happening one right after the other).

Reproduction requires allocating a shared space, which is currently disabled by default, so this issue should not affect any shipping configurations (as per tsepez@'s question from c#7).

[Monorail components: -Blink>JavaScript Blink>JavaScript>GarbageCollection]

### gi...@appspot.gserviceaccount.com (2023-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6136da99d297325475d22ead1854a21b9c4c49fd

commit 6136da99d297325475d22ead1854a21b9c4c49fd
Author: Omer Katz <omerkatz@chromium.org>
Date: Mon Mar 20 13:52:18 2023

[heap] Enter global safepoint before starting a cycle/atomic pause

For shared GCs, the initiator isolate finalizes sweeping for the client
isolates. The GCTracer expects that when sweeping is finalized, the
current cycle is in a sweeping state. Since we were starting a cycle (if
needed) and entering an atomic pause before entering a global safepoint,
it was possible for a client to start a minor GC first. At which point,
the GCTracer would see that the current cycle is in a MARKING/ATOMIC
state rather than a SWEEPING state, and fail the DCHECK in
gc-tracer.cc::568.

Fix by entering the safepoint before updating the GCTracer events.

Bug: chromium:1424955
Change-Id: I344276a8aba5178fb76a0f22acd9eee31a7fcc1f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4353176
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#86588}

[modify] https://crrev.com/6136da99d297325475d22ead1854a21b9c4c49fd/src/heap/safepoint.h
[modify] https://crrev.com/6136da99d297325475d22ead1854a21b9c4c49fd/test/cctest/test-shared-strings.cc
[modify] https://crrev.com/6136da99d297325475d22ead1854a21b9c4c49fd/src/heap/heap.cc
[modify] https://crrev.com/6136da99d297325475d22ead1854a21b9c4c49fd/src/heap/safepoint.cc


### om...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### sa...@google.com (2023-03-28)

For completeness, the report used --harmony-struct for reproducing the issue, which is currently marked as experimental. However, the issue can also be reproduced with for example --shared-string-table (because --harmony-struct implies --shared-string-table) so the issue also affected non-experimental configurations (but not any shipping configurations).
Since the issue appears to have been found with the help of Fuzzilli, I'm adding that label (we use these for some basic statistics), but @Reporter please let me know if that is not the case. Thanks!

### wh...@gmail.com (2023-03-28)

Hi, @saelo
>  --harmony-struct for reproducing the issue, which is currently marked as experimental. 

It seems no marked as experimental, I can't find any about "DEFINE_EXPERIMENTAL_FEATURE(harmony_struct.." in file flag-definitions.h, only this

```
// Features that are still work in progress (behind individual flags).
#define HARMONY_INPROGRESS_BASE(V)                                             \
  V(harmony_weak_refs_with_cleanup_some,                                       \
    "harmony weak references with FinalizationRegistry.prototype.cleanupSome") \
  V(harmony_temporal, "Temporal")                                              \
  V(harmony_shadow_realm, "harmony ShadowRealm")                               \
  V(harmony_struct, "harmony structs, shared structs, and shared arrays")      \              <---
  V(harmony_array_from_async, "harmony Array.fromAsync")                       \
  V(harmony_iterator_helpers, "JavaScript iterator helpers")
```
is it also means marked as experimental? why you say as experimental?

### sa...@google.com (2023-03-28)

Hi!

The easiest way to find out if something is marked as experimental is to enable the flag and look for that "experimental features enabled" message:

```
./out/x64.debug/d8 --harmony-struct
V8 is running with experimental features enabled. Stability and security will suffer.
V8 version 11.4.0 (candidate)
d8> 
```

Or look at the --help entry for that flag and see if it says "experimental": "--harmony-struct (enable "harmony structs, shared structs, and shared arrays" (in progress / experimental))".
In the flag-definitions.h, all HARMONY_INPROGRESS features are marked as experimental here: https://source.chromium.org/chromium/chromium/src/+/main:v8/src/flags/flag-definitions.h;l=294 Hope that helps!

### am...@google.com (2023-03-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-29)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us!  

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-06)

Hello -- we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. 

### is...@google.com (2023-07-06)

This issue was migrated from crbug.com/chromium/1424955?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063616)*
