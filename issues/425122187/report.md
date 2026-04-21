# V8 Sandbox Bypass: UB V8HeapExplorer::GetSystemEntryName leads to OOB write

| Field | Value |
|-------|-------|
| **Issue ID** | [425122187](https://issues.chromium.org/issues/425122187) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vs...@gmail.com |
| **Assignee** | sr...@google.com |
| **Created** | 2025-06-15 |
| **Bounty** | $1,000.00 |

## Description

#### VULNERABILITY DETAILS

In [V8HeapExplorer::GetSystemEntryName](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/profiler/heap-snapshot-generator.cc;drc=feaf4438bcf1f96868820e62254495bfa46d3ea0;l=1052), on-heap data is used as input for a switch statement without a default case (see issue #390568183 for a similar case):

```
  // <---------------- On-heap data is read here
  InstanceType type = object->map()->instance_type();

  // Empty string names are special: TagObject can overwrite them, and devtools
  // will report them as "(internal array)".
  if (InstanceTypeChecker::IsFixedArray(type) ||
      InstanceTypeChecker::IsFixedDoubleArray(type) ||
      InstanceTypeChecker::IsByteArray(type)) {
    return "";
  }

  // <-------------------- switch has no default case,
  // thus switching on a variant not defined in InstanceType causes UB
  switch (type) { 
#define MAKE_TORQUE_CASE(Name, TYPE) \
  case TYPE:                         \
    return "system / " #Name;
    // The following lists include every non-String instance type.
    // This includes a few types that already have non-"system" names assigned
    // by AddEntry, but this is a convenient way to avoid manual upkeep here.
    TORQUE_INSTANCE_CHECKERS_SINGLE_FULLY_DEFINED(MAKE_TORQUE_CASE)
    TORQUE_INSTANCE_CHECKERS_MULTIPLE_FULLY_DEFINED(MAKE_TORQUE_CASE)
    TORQUE_INSTANCE_CHECKERS_SINGLE_ONLY_DECLARED(MAKE_TORQUE_CASE)
    TORQUE_INSTANCE_CHECKERS_MULTIPLE_ONLY_DECLARED(MAKE_TORQUE_CASE)
#undef MAKE_TORQUE_CASE

    // Strings were already handled by AddEntry.
#define MAKE_STRING_CASE(instance_type, size, name, Name) \
  case instance_type:                                     \
    UNREACHABLE();
    STRING_TYPE_LIST(MAKE_STRING_CASE)
#undef MAKE_STRING_CASE
  }
}

```
#### VERSION

V8 Git Commit: ef5225097917290af9455f4f39dcc556ff70b343 (2025-06-13T12:42:12+00:00)

#### REPRODUCTION CASE

Currently, I can not provide a working reproducer; however, the JS file below can trigger the bug (requires `--expose-gc`). By placing a breakpoint at [this line](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/profiler/heap-snapshot-generator.cc;drc=feaf4438bcf1f96868820e62254495bfa46d3ea0;l=1053) and simulating an attacker-controlled type by using `set type = 0xffff`, a segmentation fault can be triggered. The segfault is caused by the `type` value used for indexing a jump table, causing a jump to an unexpected location.

```
const flags = {
    "execution": "sync",
    "type": "major-snapshot",
};
gc(flags);

```

**ASAN Report**

```
## V8 sandbox violation detected!

AddressSanitizer:DEADLYSIGNAL
=================================================================
==2900037==ERROR: AddressSanitizer: SEGV on unknown address 0x5555ca3a1b0e (pc 0x5555ca3a1b0e bp 0x7fffffffcc30 sp 0x7fffffffcc00 T0)
==2900037==The signal is caused by a WRITE memory access.
#0  0x000055555a4caf88 in v8::internal::V8HeapExplorer::GetSystemEntryName (this=<optimized out>, object=...) at ./../../src/profiler/heap-snapshot-generator.cc:1113
#1  0x000055555a4c6fc0 in v8::internal::V8HeapExplorer::AddEntry (this=<optimized out>, object=...) at ./../../src/profiler/heap-snapshot-generator.cc:1063
#2  0x000055555a4e364a in v8::internal::HeapSnapshotGenerator::FindOrAddEntry (ptr=<optimized out>, allocator=<optimized out>, this=<optimized out>) at ../../src/profiler/heap-snapshot-generator.h:698
#3  v8::internal::V8HeapExplorer::GetEntry (this=<optimized out>, obj=...) at ./../../src/profiler/heap-snapshot-generator.cc:2489
#4  0x000055555a4e1e0c in v8::internal::V8HeapExplorer::SetInternalReference (this=<optimized out>, parent_entry=<optimized out>, reference_name=<optimized out>, child_obj=..., field_offset=<optimized out>)
    at ./../../src/profiler/heap-snapshot-generator.cc:2716
#5  0x000055555a4d9b8d in v8::internal::V8HeapExplorer::ExtractContextReferences (this=<optimized out>, entry=<optimized out>, context=...) at ./../../src/profiler/heap-snapshot-generator.cc:1747
#6  0x000055555a4cfb0f in v8::internal::V8HeapExplorer::ExtractReferences (this=<optimized out>, entry=<optimized out>, obj=...) at ./../../src/profiler/heap-snapshot-generator.cc:1450
#7  0x000055555a4e9704 in v8::internal::V8HeapExplorer::IterateAndExtractReferences (this=<optimized out>, generator=<optimized out>) at ./../../src/profiler/heap-snapshot-generator.cc:2610
#8  0x000055555a4f3317 in v8::internal::HeapSnapshotGenerator::FillReferences (this=<optimized out>) at ./../../src/profiler/heap-snapshot-generator.cc:3375
#9  v8::internal::HeapSnapshotGenerator::GenerateSnapshot (this=<optimized out>) at ./../../src/profiler/heap-snapshot-generator.cc:3312
#10 0x000055555a49dd0d in v8::internal::HeapProfiler::TakeSnapshot(v8::HeapProfiler::HeapSnapshotOptions)::$_0::operator()() const (this=<optimized out>) at ./../../src/profiler/heap-profiler.cc:151
#11 0x000055555a49d74c in heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::HeapProfiler::TakeSnapshot(v8::HeapProfiler::HeapSnapshotOptions)::$_0>(heap::base::Stack*, void*, void const*) (stack=<optimized out>, argument=<optimized out>, 
    stack_end=<optimized out>) at ../../src/heap/base/stack.h:185
#12 0x000055555cb14ad3 in PushAllRegistersAndIterateStack ()
#13 0x000055555a492f95 in heap::base::Stack::SetMarkerIfNeededAndCallback<v8::internal::HeapProfiler::TakeSnapshot(v8::HeapProfiler::HeapSnapshotOptions)::$_0>(v8::internal::HeapProfiler::TakeSnapshot(v8::HeapProfiler::HeapSnapshotOptions)::$_0) (
    this=<optimized out>, callback=...) at ../../src/heap/base/stack.h:81
#14 v8::internal::HeapProfiler::TakeSnapshot (this=<optimized out>, options=...) at ./../../src/profiler/heap-profiler.cc:142
#15 0x000055555a4936cb in v8::internal::HeapProfiler::TakeSnapshotToFile (this=<optimized out>, options=..., filename=...) at ./../../src/profiler/heap-profiler.cc:192
#16 0x000055555914086c in v8::internal::(anonymous namespace)::InvokeGC (isolate=<optimized out>, gc_options=...) at ./../../src/extensions/gc-extension.cc:227
#17 0x000055555913ee66 in v8::internal::GCExtension::GC (info=...) at ./../../src/extensions/gc-extension.cc:287
#18 0x0000555561628844 in Builtins_CallApiCallbackGeneric ()

```

## Timeline

### pg...@google.com (2025-06-16)

Over to V8 Sheriff - there is nothing to plug into Clusterfuzz or run so I haven't been able to confirm -  passing over to you in hopes that this makes more sense at a shorter glance to triage! Unsure how much of the exploit is getting to be able to set `set type = 0xffff` patch- 

setting s1 and foundin as extended as placeholders!

### ch...@google.com (2025-06-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-17)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sr...@google.com (2025-06-18)

We also found this in [crbug.com/390617721](https://crbug.com/390617721) but treated it as a non-vulnerability since I thought this is debug only code and doesn't affect any release builds.

@reporter, if you know a way to reach this in a release build, please let me know :). But I'll also check with other folks on the team and leave this as a security bug for now.

### sr...@google.com (2025-06-18)

> But I'll also check with other folks on the team and leave this as a security bug for now.

The verdict is that this code can be reached in release builds through devtools.

### dx...@google.com (2025-06-18)

Project: v8/v8  

Branch: main  

Author: Stephen Roettger [sroettger@google.com](mailto:sroettger@google.com)  

Link:      <https://chromium-review.googlesource.com/6654777>

[sandbox] fix UB in V8HeapExplorer

---


Expand for full commit details
```
     
    There's no return after the switches on the enum values. Even though the 
    switch is exhaustive, the value comes from inside the sandbox and can 
    skip the switch, triggering UB by reaching the end of the function 
    without a return. 
     
    Fixed: 425122187 
    Change-Id: I583cf01186008d89d39a4c554b3c6ed35c7a80aa 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6654777 
    Commit-Queue: Stephen Röttger <sroettger@google.com> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100887}

```

---

Files:

- M `src/profiler/heap-snapshot-generator.cc`

---

Hash: 9544a50a2b762e30746a99ff299822a5c23afa43  

Date:  Wed Jun 18 09:06:51 2025


---

### sp...@google.com (2025-06-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of V8 sandbox bypass issue that does not meet the full conditions of a V8 heap bypass report eligible for a reward, but did result in a security beneficial change 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-26)

Thank you for your efforts and reporting this issue to us!

### ch...@google.com (2025-09-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of V8 sandbox bypass issue that does not meet the full conditions of a V8 heap bypass report eligible for a reward, but did result in a security beneficial change

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/425122187)*
