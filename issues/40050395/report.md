# Security: Debug check failed: Smi::IsValid(value)

| Field | Value |
|-------|-------|
| **Issue ID** | [40050395](https://issues.chromium.org/issues/40050395) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2019-10-10 |
| **Bounty** | $5,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

The following testcase crashes an ASAN debug build of d8.

**VERSION**  

Chrome Version: asan-linux-debug-704309  

Operating System: Linux 64bit

**REPRODUCTION CASE**

o14=[1.1,2.2,3.3];  

o18=o14['constructor'];  

o42=o18.bind(undefined);  

o190=o42(undefined);  

Object.defineProperty(o190,134217725,{get:()=>{},writeable: false,configurable: false,enumerable: true,});  

o592=(function asm(stdlib, foreign, heap) {"use asm";var std = stdlib.Math.imul; var heap32 = new stdlib.Uint32Array(heap);function f(arg) {arg=arg|0;var x =0;x= arg | 0;heap32[x>>2] = x | 0;heap32[x>>2] = std(x|0,arg|0) | 0;return x | 0;}return {f:f};});  

o592'apply';

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Crash State:

# 

# Fatal error in ../../v8/src/objects/smi.h, line 51

# Debug check failed: Smi::IsValid(value).

# 

# 

# 

#FailureMessage Object: 0x7f4f6e3de460  

==== C stack trace ===============================

```
asan-linux-debug-704309/d8(backtrace+0x5b) [0x56151f33a43b]  
asan-linux-debug-704309/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f4f77b910f3]  
asan-linux-debug-704309/libv8_libplatform.so(+0x2140a) [0x7f4f77b2e40a]  
asan-linux-debug-704309/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x27b) [0x7f4f77b7876b]  
asan-linux-debug-704309/libv8_libbase.so(+0x2f0af) [0x7f4f77b780af]  
asan-linux-debug-704309/libv8.so(v8::internal::Heap::CreateFillerObjectAt(unsigned long, int, v8::internal::ClearRecordedSlots, v8::internal::ClearFreedMemoryMode)+0x3c5) [0x7f4f74de4485]  
asan-linux-debug-704309/libv8.so(+0x18a7b3d) [0x7f4f74f8db3d]  
asan-linux-debug-704309/libv8.so(v8::internal::NewLargeObjectSpace::AllocateRaw(int)+0x178) [0x7f4f74f927b8]  
asan-linux-debug-704309/libv8.so(+0x1666f23) [0x7f4f74d4cf23]  
asan-linux-debug-704309/libv8.so(+0x1724e7a) [0x7f4f74e0ae7a]  
asan-linux-debug-704309/libv8.so(+0x172523b) [0x7f4f74e0b23b]  
asan-linux-debug-704309/libv8.so(v8::internal::Factory::NewFixedArrayWithFiller(v8::internal::RootIndex, int, v8::internal::Object, v8::internal::AllocationType)+0x62) [0x7f4f74d421e2]  
asan-linux-debug-704309/libv8.so(+0x1f5f905) [0x7f4f75645905]  
asan-linux-debug-704309/libv8.so(+0x2426d93) [0x7f4f75b0cd93]  
asan-linux-debug-704309/libv8.so(+0x24263d1) [0x7f4f75b0c3d1]  
asan-linux-debug-704309/libv8.so(+0x3a050e0) [0x7f4f770eb0e0]  

```

## Timeline

### aj...@google.com (2019-10-10)

Assigning to v8 clusterfuzz sheriff. Thanks fellow sheriff!

[Monorail components: Blink>JavaScript]

### ms...@chromium.org (2019-10-11)

This is independent of asm.js, here is a reduced repro ...

var a = [];
Object.defineProperty(a, 134217725, {get: () => {}});
function f(x, y, z) {}
f.apply(undefined, a);

### cl...@chromium.org (2019-10-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4939863731077120.

### ms...@chromium.org (2019-10-11)

Bisects to the change of Smi's from 32 to 31 bit payloads. Best to use repro in https://crbug.com/chromium/1013042#c2. Bisects to the following ...

commit d68bf369cb8f2cdd2068dd8c31c2418b2b974c60
Author: Igor Sheludko <ishell@chromium.org>
Date:   Tue Sep 24 11:19:57 2019 +0200

    Reland "[ptr-compr] Switch to 31 bit Smis on 64-bit architectures"
    
    This is a reland of 12a9ee3a5bfde926e0bcfcd2aac3bcdb5a411497
    
    Fixed arm64 disasm test.
    
    Original change's description:
    > [ptr-compr] Switch to 31 bit Smis on 64-bit architectures
    >
    > 32 bit Smis are incompatible with pointer compression so we land disable
    > them before enabling pointer compression in order to separate memory and
    > performance regressions caused by 31 bit Smis from pointer compression
    > change.
    >
    > Bug: v8:9767
    > Change-Id: I3d4a675df4208f808b1ba6e7816be545eae0dc24
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1815249
    > Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    > Commit-Queue: Igor Sheludko <ishell@chromium.org>
    > Cr-Commit-Position: refs/heads/master@{#63934}
    
    Bug: v8:9767
    Change-Id: Ife46a4240141dd89d841eac152032ad6ca471810
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1820939
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Igor Sheludko <ishell@chromium.org>
    Cr-Commit-Position: refs/heads/master@{#63940}


### cl...@chromium.org (2019-10-11)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>GC]

### cl...@chromium.org (2019-10-11)

Detailed Report: https://clusterfuzz.com/testcase?key=4939863731077120

Fuzzer: 
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  Smi::IsValid(value) in smi.h
  v8::internal::Heap::CreateFillerObjectAt
  v8::internal::LargeObjectSpace::AllocateLargePage
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=63939:63940

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4939863731077120

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/4939863731077120 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### is...@chromium.org (2019-10-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1ce9b553b58e8f5759cfd3550e021c9b5b7d991b

commit 1ce9b553b58e8f5759cfd3550e021c9b5b7d991b
Author: Igor Sheludko <ishell@chromium.org>
Date: Fri Oct 11 14:56:14 2019

[ptr-compr] Update FixedArrayBase::kMaxSize for 31-bit Smi and ptr-compr

When we allocate a large page we write a free space filler of the object's
size which is encoded as a Smi. Previously the 1Gb didn't fit into 31-bit
Smi. In addition, when pointer compression is enabled we should use the
same limitation as we had for 32 bit architectures.

Bug: v8:9767, chromium:1013042
Change-Id: I6e372324417f03977943f18816eaaf49540184ab
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1856007
Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#64246}

[modify] https://crrev.com/1ce9b553b58e8f5759cfd3550e021c9b5b7d991b/src/objects/fixed-array.h


### is...@chromium.org (2019-10-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-10-12)

ClusterFuzz testcase 4939863731077120 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=64245:64246

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-01-29)

ishell@ please would you set an appropriate Security_Severity label here. It may be that I need to retrospectively get this into some release notes. Thanks!

### ad...@google.com (2020-01-29)

(probably not on the release notes as it was Security_Impact-Head. TBD).

### is...@chromium.org (2020-01-30)

This issue does not affect any releases because it was caused by changing Smi size which wanted to ship (and shipped) only in M-80 with pointer compression and the fix in #8 was landed before the M-80 branch.

### ad...@google.com (2020-02-05)

ishell@ please could you set Security_Severity to something reasonable here. We do need Security_Severity to be set on all security bugs, because lots of downstream things happen based on that - notably merge decisions.

### is...@chromium.org (2020-02-06)

I don't see how it can be exploitable directly but without the fix GC may be confused in unpredictable ways. Let's leave the severity High.

### is...@chromium.org (2020-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-06)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-11)

Congrats! The Panel decided to award $5,000 for this report!

### na...@google.com (2020-02-11)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-11)

This issue was migrated from crbug.com/chromium/1013042?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>GarbageCollection]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050395)*
