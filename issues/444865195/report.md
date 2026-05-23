# V8 Sandbox Bypass: Referencing non-shared heap data across isolates leads to UAF -> AAW/PC control

| Field | Value |
|-------|-------|
| **Issue ID** | [444865195](https://issues.chromium.org/issues/444865195) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kr...@gmail.com |
| **Assignee** | om...@chromium.org |
| **Created** | 2025-09-13 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

#### Details

Normally, [per this document](https://docs.google.com/document/d/18lYuaEsDSudzl2TDu-nc-0sVXW7WTGAs14k64GEhnFg/), data that is shared between Isolates resides in a shared heap so garbage collection can properly account for it. However, with in-sandbox memory corruption, one can construct some data `O` (owned exclusively by some Isolate `A`) that references some data `X` (owned exclusively by some other Isolate `B`). Thus, when garbage collection runs in Isolate `B`, it can make misinformed decisions as it doesn't observe the reference to `X` in Isolate `A`'s non-shared heap. This can lead to a dangling reference that is subject to use-after-free exploits.

Since the isolates can share the same external tables, this can easily lead to AAW/PC control if `X` were some external/trusted information (eg. `Code`, `JSDispatchEntry`, etc.). In the attached PoC, PC control is obtained by making the main thread use a dispatch handle from a worker, which is then UAF'd leading to stale JITed code that imbalances the stack. AAW can be just as easily had though.

**NOTE:** While I chose the same means as [crbug/443772809](https://crbug.com/443772809) to exploit this, these are fundamentally different issues. [crbug/443772809](https://crbug.com/443772809) worked by ["break[ing] the link from JSFunction to
dispatch handle (and thus instruct[i]on stream)"](https://chromium-review.googlesource.com/c/v8/v8/+/6939390) within an isolate's own heap(s). This bug, on the other hand, works by introducing an invisible link across non-shared heaps that is never considered during GC at any point to begin with.

### VERSION

V8 commit: d6579b6d6b712afdb39bfbc4d7d2c831edf34598

#### REPRODUCTION CASE

**NOTE (for the shepherd):** To reproduce in CF, the `linux_d8_sandbox_testing` job type with the below shell args should hopefully do the trick.

**Build args**:

```
is_debug=false
is_asan=true
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true
dcheck_always_on=false
target_cpu="x64"

```

**Shell args**: `--allow-natives-syntax --expose-gc --sandbox-testing`

**Sample output (using `--disable-in-process-stack-traces` to show PC)**:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7e8f00000000,0x7f8f00000000)

## V8 sandbox violation detected!

Access type was read though which is technically not a sandbox violation. This requires manual investigation.
AddressSanitizer:DEADLYSIGNAL
=================================================================
==128433==ERROR: AddressSanitizer: SEGV on unknown address 0x424242424242 (pc 0x424242424242 bp 0x424242424242 sp 0x7fffe9d56880 T0)
==128433==The signal is caused by a READ memory access.
    #0 0x424242424242  (<unknown module>)

==128433==Register values:
rax = 0x00007e8f00000011  rbx = 0x00007e8f00000011  rcx = 0x0000000000000002  rdx = 0x0000424242424242  
rdi = 0x0000000000000000  rsi = 0x0000000000000000  rbp = 0x0000424242424242  rsp = 0x00007fffe9d56880  
 r8 = 0x0000000000000000   r9 = 0x0000000000000000  r10 = 0x00005e356f640107  r11 = 0x00007fffe9d56649  
r12 = 0x00007fffe9d56568  r13 = 0x000071fc07ae1080  r14 = 0x00007e8f00000000  r15 = 0x0000717c07ae0309  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (<unknown module>) 
==128433==ABORTING

```
### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Krishna Ravishankar (@krsh732)

## Attachments

- [cross-isolate-uaf.js](attachments/cross-isolate-uaf.js) (text/javascript, 2.7 KB)

## Timeline

### kr...@gmail.com (2025-09-13)

Oops, sorry actually attached the PoC this time:

### cl...@appspot.gserviceaccount.com (2025-09-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6208849212014592.

### ml...@chromium.org (2025-09-17)

Still trying to grasp what is going on here. The initial sandbox design certainly wanted to have trusted data per Isolate in a non-sharable way.

Few things:

- Shared heap is only collected on the main isolate (first Isolate that is set up)
- Isolates generally don't share tables.
- The dispatch table is global but it has per-Isolate spaces and entries should stay disjoint.
- There's no way to allocate a shared JSFunction in shared space (as of yet).

Fundamentally: If you manage to swap dispatch entries (with different Isolates) with different parameter counts while the function is running then this leads to imbalanced stack and is a corruption.

### ml...@chromium.org (2025-09-17)

I see that the spaces are disjoint but the JSDispatchHandle is just a global index into the overall table. So the swap is easily doable while an invocation is active on the stack and GCs (that are disjoint) are running.

### kr...@gmail.com (2025-09-17)

> I see that the spaces are disjoint but the `JSDispatchHandle` is just a global index into the overall table.

Yeah, sorry, that was what I was trying to say by "the isolates can share the same external tables". Every isolate can read/write to any entry in the table regardless of which isolate it belongs to.

Also, is this just a `JSDispatchTable` problem or do other `ExternalEntityTable` handles (eg. CPT) suffer from the same issue?

### kr...@gmail.com (2025-09-17)

> I see that the spaces are disjoint but the JSDispatchHandle is just a global index into the overall table.

Yeah, sorry, this is what I was trying to say by "the isolates can share the same external tables" as any Isolate can read/write to any entry in the table regardless of which Isolate owns it. Also, is this just a JSDispatchTable problem or do other ExternalEntityTables (eg. CPT) suffer from the same issue?

PS: Not sure what's going on with #6, editing it seemed to have deleted it and trying to restore it results in "Internal Server Error"

### kr...@gmail.com (2025-09-17)

Is there a bug with the issue tracker? The previous comments of mine got deleted immediately upon being sent.

### is...@chromium.org (2025-09-17)

It seems there was something, I can't recover the first deleted comment but I managed to recover the second one.

### kr...@gmail.com (2025-09-17)

Thank you!

### ml...@google.com (2025-09-22)

fyi: We are still discussing how to best address this. The CPT is also global right now and could suffer from these kinds of attacks.

### dx...@google.com (2026-01-26)

Project: v8/v8  

Branch:  main  

Author:  Omer Katz [omerkatz@chromium.org](mailto:omerkatz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7486426>

Convert JSDispatchTable from per-isolate-group to per-isolate

---


Expand for full commit details
```
     
    We currently have a single JSDispatchTable per IsolateGroup, with a 
    space per Isolate and one shared read only space. This splits the 
    table among the Isolates, resulting in one table per Isolate, each containing a space for the Isolate and a read only space. 
     
    This change retains the current JSDispatchTable reservation size of 
    256MB. This may result in number of OOMs increasing. We will mitigate 
    that by reducing the reservation size in followups as/if needed. 
     
    See https://docs.google.com/document/d/1IC6PWCLus_6r-_S44gQIjTpFePoOCTy-MvrVqTSz2p4/edit?usp=sharing 
     
    Bug: 444865195 
    Change-Id: Id1cfb71ec9a856a147b016edbffe1561914f359e 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7486426 
    Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Omer Katz <omerkatz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104918}

```

---

Files:

- M `include/v8-internal.h`
- M `src/codegen/arm/macro-assembler-arm.cc`
- M `src/codegen/arm64/macro-assembler-arm64.cc`
- M `src/codegen/code-stub-assembler.cc`
- M `src/codegen/compiler.cc`
- M `src/codegen/external-reference.cc`
- M `src/codegen/external-reference.h`
- M `src/codegen/loong64/macro-assembler-loong64.cc`
- M `src/codegen/ppc/macro-assembler-ppc.cc`
- M `src/codegen/reloc-info.cc`
- M `src/codegen/riscv/macro-assembler-riscv.cc`
- M `src/codegen/s390/macro-assembler-s390.cc`
- M `src/codegen/x64/macro-assembler-x64.cc`
- M `src/common/segmented-table-inl.h`
- M `src/common/segmented-table.h`
- M `src/compiler/backend/arm/code-generator-arm.cc`
- M `src/compiler/backend/arm64/code-generator-arm64.cc`
- M `src/compiler/backend/loong64/code-generator-loong64.cc`
- M `src/compiler/backend/ppc/code-generator-ppc.cc`
- M `src/compiler/backend/s390/code-generator-s390.cc`
- M `src/compiler/backend/x64/code-generator-x64.cc`
- M `src/deoptimizer/deoptimizer.cc`
- M `src/diagnostics/disassembler.cc`
- M `src/diagnostics/objects-debug.cc`
- M `src/diagnostics/objects-printer.cc`
- M `src/execution/isolate-data-fields.h`
- M `src/execution/isolate-data.h`
- M `src/execution/isolate.cc`
- M `src/execution/isolate.h`
- M `src/execution/local-isolate.h`
- M `src/execution/tiering-manager.cc`
- M `src/heap/factory-base.cc`
- M `src/heap/factory.cc`
- M `src/heap/heap-write-barrier.cc`
- M `src/heap/heap.h`
- M `src/heap/mark-compact.cc`
- M `src/heap/marking-visitor-inl.h`
- M `src/heap/read-only-heap.cc`
- M `src/heap/read-only-heap.h`
- M `src/heap/read-only-promotion.cc`
- M `src/init/isolate-group.cc`
- M `src/init/isolate-group.h`
- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-ir-inl.h`
- M `src/objects/code.cc`
- M `src/objects/js-function-inl.h`
- M `src/objects/js-function.cc`
- M `src/objects/js-function.h`
- M `src/runtime/runtime-compiler.cc`
- M `src/runtime/runtime-test.cc`
- M `src/sandbox/isolate-inl.h`
- M `src/sandbox/isolate.h`
- M `src/sandbox/js-dispatch-table.h`
- M `src/snapshot/serializer.cc`

---

Hash: [4d1e2794e00a1071e774361994ac5ac4b6d3f147](https://chromiumdash.appspot.com/commit/4d1e2794e00a1071e774361994ac5ac4b6d3f147)  

Date: Fri Jan 23 15:42:58 2026


---

### 24...@project.gserviceaccount.com (2026-01-27)

ClusterFuzz testcase 6208849212014592 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&range=104917:104918

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### om...@chromium.org (2026-01-27)

Filed [crbug.com/479054260](https://crbug.com/479054260) for tracking followup work for the CodePointerTable as well.

### sp...@google.com (2026-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
Controlled write outside the V8 sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Controlled write outside the V8 sandbox

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/444865195)*
