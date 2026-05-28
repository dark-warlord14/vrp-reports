# V8 Turboshaft Late Load Elimination Aliasing bug leads to Memory Corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [417169470](https://issues.chromium.org/issues/417169470) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 135.0.0.0 |
| **Reporter** | pw...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2025-05-12 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. ./d8 --expose-externalize-string --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --wasm-staging --wasm-fast-api --expose-fast-api --turbolev --shared-string-table poc.js

# Problem Description

I'll analyze it and upload it soon.

poc.js

```
function opt(){
        function v3() {
                const v4 = {"B":42};
        }
        const v2 = {};
        const v6 = {"C":42.42};
        function v10(v11) {
                function v13() {
                        v6.e = 41.414;
                        for (let v19 = 0; v19 < 100; v19++) {
                                //const v4 = {"B":42};
                                v3();
                        }
                }
                v6.d = 42;
                v11.b = 42;
                v11.f = v2;
                for (let v26 = 0; v26 < 100; v26++) {
                        v13();
                }
        }
        v6.c = 42;
        v6.d = v2;
        for (let v36 = 0; v36 < 1000; v36++) {
                v10(v6);
        }
}
opt();
opt();
opt();

```
# Summary

V8 Turbolev Memory Corruption

# Custom Questions

#### Crash state:

./d8 --expose-externalize-string --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --wasm-staging --wasm-fast-api --expose-fast-api --turbolev --shared-string-table test3.js
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1520960 edges
V8 is running with experimental features enabled. Stability and security will suffer.
Received signal 11 SEGV\_ACCERR 7e8a00000014

==== C stack trace ===============================

./d8(\_\_\_interceptor\_backtrace+0x46)[0x5a98942fd856]
./d8(+0x26e5959)[0x5a98947a5959]
/lib/x86\_64-linux-gnu/libc.so.6(+0x42520)[0x78df3e842520]
[0x5a98e0002849]
[end of stack trace]
Segmentation fault

#### Reporter credit:

un3xploitable

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Timeline

### cl...@appspot.gserviceaccount.com (2025-05-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6621165535559680.

### 24...@project.gserviceaccount.com (2025-05-12)

ClusterFuzz testcase 6621165535559680 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2025-05-12)

Detailed Report: https://clusterfuzz.com/testcase?key=6621165535559680

Fuzzer: None
Job Type: linux32_asan_d8
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x1e44000c
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux32_asan_d8&revision=100226

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6621165535559680

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

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### 24...@project.gserviceaccount.com (2025-05-12)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-05-12)

Detailed Report: https://clusterfuzz.com/testcase?key=6621165535559680

Fuzzer: None
Job Type: linux32_asan_d8
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x1e44000c
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux32_asan_d8&revision=100226

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6621165535559680

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

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### 24...@project.gserviceaccount.com (2025-05-13)

Detailed Report: https://clusterfuzz.com/testcase?key=6621165535559680

Fuzzer: None
Job Type: linux32_asan_d8
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x1e44000c
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux32_asan_d8&revision=100226

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6621165535559680

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

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### jd...@chromium.org (2025-05-13)

Over to the current v8 sheriff for further triage.

### sr...@google.com (2025-05-13)

Hey, thanks for the report!
I wasn't able to reproduce this yet, can you share:

1. the commit hash
2. the gn.args
   you're testing with?
   Thanks!

### pw...@gmail.com (2025-05-13)

1. 53868098b8c0773aa361fb71b029fc3c11ac93e3
2. args.gn

```
is_debug = false
dcheck_always_on = true
v8_static_library = true
v8_enable_verify_heap = true
v8_fuzzilli = true
sanitizer_coverage_flags = "trace-pc-guard"
target_cpu = "x64"

```

Thanks!

### pe...@google.com (2025-05-13)

Thank you for providing more feedback. Adding the requester to the CC list.

### cl...@appspot.gserviceaccount.com (2025-05-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6388043434885120.

### ch...@google.com (2025-05-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-05-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2025-05-13)

Detailed Report: https://clusterfuzz.com/testcase?key=6388043434885120

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x77cb00000014
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98073:98074

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6388043434885120

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### cl...@appspot.gserviceaccount.com (2025-05-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6230816795328512.

### cl...@appspot.gserviceaccount.com (2025-05-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4670730960568320.

### cl...@appspot.gserviceaccount.com (2025-05-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4629365593669632.

### sr...@google.com (2025-05-14)

The first clusterfuzz run just bisected to the CL that renamed the --turbolev flag.

In the second run, it bisected to enabling --maglev-extend-properties-backing-store.
<https://chromium.googlesource.com/v8/v8/+/e12c1d220ce3e6e406b290f17ee8711bbdc2e77c>

Marking as impact=none since I don't think we're shipping the turbolev code yet.

marja@ can you take a look?

### ma...@chromium.org (2025-05-15)

Yea, it's a def about extending properties backing store; if I forcefully disable it, the bug doesn't repro.

### ma...@chromium.org (2025-05-16)

Debugging notes:

This is the most minimal repro so far:

```
function opt(){
  function v3() {
  }
  const v2 = {};
  const v6 = {"C": 42.42};
  function v10(v11) {
    function v13() {
      v6.e = 41.414;
      for (let v19 = 0; v19 < 100; v19++) {
        v3();
      }
    }
    v6.d = 42;
    v11.b = 42;
    v11.f = v2;
    for (let v26 = 0; v26 < 100; v26++) {
      v13();
    }
  }
  v6.c = 42;
  v6.d = v2;
  for (let v36 = 0; v36 < 1000; v36++) {
    v10(v6);
  }
}
opt();
opt();
opt();

```

with flags `--allow-natives-syntax --fuzzing --jit-fuzzing --turbolev`.

The crash is in generated code for v10, in here:

```
0x7f5e98000a66    66  0f85bf020000         jnz 0x7f5e98000d2b  <+0x32b> << rdi is the v6 object
0x7f5e98000a6c    6c  8b7f03               movl rdi,[rdi+0x3] << rdi is the property array
0x7f5e98000a6f    6f  418b7c3e17           movl rdi,[r14+rdi*1+0x17] << rdi is undefined
0x7f5e98000a74    74  4903fe               REX.W addq rdi,r14
0x7f5e98000a77    77  49baa245b6f3fdb44440 REX.W movq r10,0x4044b4fdf3b645a2
0x7f5e98000a81    81  c4c1f96ec2           vmovq xmm0,r10
0x7f5e98000a86    86  c5fb114703           vmovsd [rdi+0x3],xmm0 <<< crash here

```

### ma...@chromium.org (2025-05-16)

I was lucky to get a smaller repro case in rr. This is inside v13 and the machine code is so small we can just read it:

```
--- Optimized code ---
optimization_id = 4
source_position = 120
kind = TURBOFAN_JS
name = v13
compiler = turbofan
address = 0x2c1000100bd5

Instructions (size = 852)
0x7f5e98000a00     0  55                   push rbp
0x7f5e98000a01     1  4889e5               REX.W movq rbp,rsp
0x7f5e98000a04     4  56                   push rsi
0x7f5e98000a05     5  57                   push rdi
0x7f5e98000a06     6  50                   push rax
0x7f5e98000a07     7  4883ec20             REX.W subq rsp,0x20
0x7f5e98000a0b     b  488975d8             REX.W movq [rbp-0x28],rsi
0x7f5e98000a0f     f  48897de0             REX.W movq [rbp-0x20],rdi
0x7f5e98000a13    13  493b65a0             REX.W cmpq rsp,[r13-0x60] (external value (StackGuard::address_of_jslimit()))
0x7f5e98000a17    17  0f86de010000         jna 0x7f5e98000bfb  <+0x1fb>
0x7f5e98000a1d    1d  488b4dd8             REX.W movq rcx,[rbp-0x28]

(rr) job $rcx
0x54900191045: [Context]
 - map: 0x05490005b309 <Map(FUNCTION_CONTEXT_TYPE)>
 - type: FUNCTION_CONTEXT_TYPE
 - scope_info: 0x054900063b01 <ScopeInfo FUNCTION_SCOPE>
 - previous: 0x05490004b52d <NativeContext[303]>
 - native_context: 0x05490004b52d <NativeContext[303]>
 - length: 5
 - elements:
           0: 0x054900063b01 <ScopeInfo FUNCTION_SCOPE>
           1: 0x05490004b52d <NativeContext[303]>
           2: 0x054900191061 <JSFunction v3 (sfi = 0x54900063c35)>
           3: 0x0549001910a1 <Object map = 0x5490004c265>
           4: 0x0549001910c9 <Object map = 0x5490006402d>


0x7f5e98000a21    21  8b7917               movl rdi,[rcx+0x17]

(rr) job $rdi
0x549001910c9: [JS_OBJECT_TYPE]
 - map: 0x05490006402d <Map[16](HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x05490004c441 <Object map = 0x5490004ba49>
 - elements: 0x054900000745 <FixedArray[0]> [HOLEY_ELEMENTS]
 - properties: 0x054900191169 <PropertyArray[6]>
 - All own properties (excluding elements): {
    0x54900003295: [String] in ReadOnlySpace: #C: 0x0549001910e1 <HeapNumber 42.42> (const data field 0, attrs: [WEC]) @ Any, location: in-object
    0x54900003495: [String] in ReadOnlySpace: #c: 42 (const data field 1, attrs: [WEC]) @ Any, location: properties[0]
    0x549000034a5: [String] in ReadOnlySpace: #d: 42 (data field 2, attrs: [WEC]) @ Any, location: properties[1]
    0x54900003485: [String] in ReadOnlySpace: #b: 42 (data field 3, attrs: [WEC]) @ Any, location: properties[2]
    0x549000034c5: [String] in ReadOnlySpace: #f: 0x0549001910a1 <Object map = 0x5490004c265> (data field 4, attrs: [WEC]) @ Any, location: properties[3]
    0x549000034b5: [String] in ReadOnlySpace: #e: 0x054900000011 <undefined> (data field 5, attrs: [WEC]) @ Any, location: properties[4]
 }
 
0x7f5e98000a24    24  4903fe               REX.W addq rdi,r14
0x7f5e98000a27    27  81ff61070000         cmpl rdi,0x761 << check against the hole
0x7f5e98000a2d    2d  0f8465020000         jz 0x7f5e98000c98  <+0x298>
0x7f5e98000a33    33  660f1f840000000000   nop
0x7f5e98000a3c    3c  0f1f4000             nop
0x7f5e98000a40    40  40f6c701             testb rdi,0x1
0x7f5e98000a44    44  0f84dd020000         jz 0x7f5e98000d27  <+0x327>
0x7f5e98000a4a    4a  448b47ff             movl r8,[rdi-0x1]
0x7f5e98000a4e    4e  41b9cd3f0600         movl r9,0x63fcd    ;; (compressed) object: 0x054900063fcd <Map[16](HOLEY_ELEMENTS)>

(rr) job 0x63fcd
0x54900063fcd: [Map] in OldSpace
 - map: 0x05490004b4dd <MetaMap (0x05490004b52d <NativeContext[303]>)>
 - type: JS_OBJECT_TYPE
 - instance size: 16
 - inobject properties: 1
 - unused property fields: 2
 - elements kind: HOLEY_ELEMENTS
 - enum length: invalid
 - back pointer: 0x054900063fa5 <Map[16](HOLEY_ELEMENTS)>
 - prototype_validity cell: 0x054900063f1d <Cell value= 0>
 - instance descriptors #5: 0x054900188eed <DescriptorArray[6]>
 - transitions #1: 0x05490006402d <Map[16](HOLEY_ELEMENTS)>
     0x549000034b5: [String] in ReadOnlySpace: #e: (transition to (data field, attrs: [WEC]) @ Any) -> 0x05490006402d <Map[16](HOLEY_ELEMENTS)>
 - prototype: 0x05490004c441 <Object map = 0x5490004ba49>
 - constructor: 0x05490004bf59 <JSFunction Object (sfi = 0x549001c33a1)>
 - dependent code: 0x05490018a0b1 <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0

-> this is the map of the object before the property "e" was added

0x7f5e98000a54    54  453bc8               cmpl r9,r8
0x7f5e98000a57    57  0f8433000000         jz 0x7f5e98000a90  <+0x90>
0x7f5e98000a5d    5d  41b92d400600         movl r9,0x6402d    ;; (compressed) object: 0x05490006402d <Map[16](HOLEY_ELEMENTS)>

(rr) job 0x6402d 
0x5490006402d: [Map] in OldSpace
 - map: 0x05490004b4dd <MetaMap (0x05490004b52d <NativeContext[303]>)>
 - type: JS_OBJECT_TYPE
 - instance size: 16
 - inobject properties: 1
 - unused property fields: 1
 - elements kind: HOLEY_ELEMENTS
 - enum length: invalid
 - stable_map
 - back pointer: 0x054900063fcd <Map[16](HOLEY_ELEMENTS)>
 - prototype_validity cell: 0x054900063f1d <Cell value= 0>
 - instance descriptors (own) #6: 0x054900188eed <DescriptorArray[6]>
 - prototype: 0x05490004c441 <Object map = 0x5490004ba49>
 - constructor: 0x05490004bf59 <JSFunction Object (sfi = 0x549001c33a1)>
 - dependent code: 0x05490018a0e1 <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0


0x7f5e98000a63    63  453bc8               cmpl r9,r8
0x7f5e98000a66    66  0f85bf020000         jnz 0x7f5e98000d2b  <+0x32b> << not taking this jump

0x7f5e98000a6c    6c  8b7f03               movl rdi,[rdi+0x3] << rdi is the property array
0x7f5e98000a6f    6f  418b7c3e17           movl rdi,[r14+rdi*1+0x17] << rdi is undefined
0x7f5e98000a74    74  4903fe               REX.W addq rdi,r14
0x7f5e98000a77    77  49baa245b6f3fdb44440 REX.W movq r10,0x4044b4fdf3b645a2 << is this now the double 41.414?
0x7f5e98000a81    81  c4c1f96ec2           vmovq xmm0,r10
0x7f5e98000a86    86  c5fb114703           vmovsd [rdi+0x3],xmm0 << crash here
0x7f5e98000a8b    8b  e980000000           jmp 0x7f5e98000b10  <+0x110>

0x7f5e98000a90    90  448b4703             movl r8,[rdi+0x3] << here's where we jump if the object doesn't yet have the "e" property

```

I'm wondering if the instruction `vmovsd [rdi+0x3],xmm0` is trying to write a new value to a HeapNumber, but fails because rdi is not a HeapNumber but undefined.

### ma...@chromium.org (2025-05-16)

When compiling v13, this is the feedback we have for SetProperty:

```
 - slot #0 SetNamedSloppy POLYMORPHIC
   [weak] 0x10b500064b2d <Map[16](HOLEY_ELEMENTS)>: StoreHandler(Smi)(kind = kField, descriptor = 5, is in object = 0, representation = d, field index = 6)

   [weak] 0x10b500064ab5 <Map[16](HOLEY_ELEMENTS)>: StoreHandler(field transition to 0x10b500064b2d <Map[16](HOLEY_ELEMENTS)>)
 {
     [0]: 0x10b500192085 <WeakFixedArray[4]>
     [1]: 0x10b500000e4d <Symbol: (uninitialized_symbol)>
  }

```

and it looks like we now get an object whose map is 0x10b500064b2d, but which has an `undefined` as the `e` property.

Maybe something goes wrong when trying to figure out which map an object should have after we've extended its property backing store.

Curiously, I don't get this to crash with Maglev only. It should crash there too, since the problem seems to be that we assume something is a HeapNumber and it isn't.

### ma...@chromium.org (2025-05-16)

Trying to debug where we manage to generated such a botched object; which has the map 0x6402d saying the property "e" is a double, but then the corresponding slot in the PropertyArray is undefined. Since this is somehow related to extending the property backing store, maybe it's coming from a place where we are extending a property backing store and somehow fail to set that property. (Or it's a red herring.)

Here's one place in generated code which obviously sets that map:

```
0x7f5e98000a90    90  448b4703             movl r8,[rdi+0x3]
0x7f5e98000a94    94  4d03c6               REX.W addq r8,r14

^ this loads the PropertyArray from rdi

0x7f5e98000a97    97  4d8b4d50             REX.W movq r9,[r13+0x50] (external value (Heap::NewSpaceAllocationTopAddress()))
0x7f5e98000a9b    9b  4d8d590c             REX.W leaq r11,[r9+0xc]
0x7f5e98000a9f    9f  90                   nop
0x7f5e98000aa0    a0  4d395d58             REX.W cmpq [r13+0x58] (external value (Heap::NewSpaceAllocationLimitAddress())),r11
0x7f5e98000aa4    a4  0f867a010000         jna 0x7f5e98000c24  <+0x224>

^ this allocates the HeapNumber

0x7f5e98000aaa    aa  4d8d590c             REX.W leaq r11,[r9+0xc]
0x7f5e98000aae    ae  4d895d50             REX.W movq [r13+0x50] (external value (Heap::NewSpaceAllocationTopAddress())),r11
0x7f5e98000ab2    b2  4983c101             REX.W addq r9,0x1
0x7f5e98000ab6    b6  41c741ff15050000     movl [r9-0x1],0x515

0x515 is the heap number map

0x7f5e98000abe    be  4c8b15b4ffffff       REX.W movq r10,[rip+0xffffffb4]
0x7f5e98000ac5    c5  c4c1f96ec2           vmovq xmm0,r10
0x7f5e98000aca    ca  c4c17b114103         vmovsd [r9+0x3],xmm0

^ this writes the double value into the HeapNumber object

0x7f5e98000ad0    d0  45894817             movl [r8+0x17],r9

^ this writes the heap number object into the property array

0x7f5e98000ad4    d4  41f6c101             testb r9,0x1
0x7f5e98000ad8    d8  0f8414000000         jz 0x7f5e98000af2  <+0xf2>
0x7f5e98000ade    de  49c7c30000fcff       REX.W movq r11,0xfffc0000
0x7f5e98000ae5    e5  4d23d8               REX.W andq r11,r8
0x7f5e98000ae8    e8  41f60304             testb [r11],0x4
0x7f5e98000aec    ec  0f8502020000         jnz 0x7f5e98000cf4  <+0x2f4>
0x7f5e98000af2    f2  41b82d400600         movl r8,0x6402d    ;; (compressed) object: 0x05490006402d <Map[16](HOLEY_ELEMENTS)>
0x7f5e98000af8    f8  448947ff             movl [rdi-0x1],r8

```

but this looks okay (assuming that [rip+0xffffffb4] is something reasonable). Also this place is not extending the PropertyArray.

### ma...@chromium.org (2025-05-16)

With a new rr recording (so registers and addresses differ) I'm now watching the botched object and going backwards from the crash. This is the place which writes the map into the object:

```
0x7bffb000a6f6   236  448b49ff             movl r9,[rcx-0x1]
0x7bffb000a6fa   23a  660f1f440000         nop
0x7bffb000a700   240  4539e1               cmpl r9,r12
0x7bffb000a703   243  0f8489000000         jz 0x7bffb000a792  <+0x2d2>
0x7bffb000a709   249  41bf6d400600         movl r15,0x6406d    ;; (compressed) object: 0x71f40006406d <Map[16](HOLEY_ELEMENTS)>
0x7bffb000a70f   24f  453bf9               cmpl r15,r9
0x7bffb000a712   252  0f857a080000         jnz 0x7bffb000af92  <+0xad2>
0x7bffb000a718   258  4d8b4d50             REX.W movq r9,[r13+0x50] (external value (Heap::NewSpaceAllocationTopAddress()))
0x7bffb000a71c   25c  4d8d790c             REX.W leaq r15,[r9+0xc]
0x7bffb000a720   260  4d397d58             REX.W cmpq [r13+0x58] (external value (Heap::NewSpaceAllocationLimitAddress())),r15
0x7bffb000a724   264  0f86ff040000         jna 0x7bffb000ac29  <+0x769>
0x7bffb000a72a   26a  4d8d790c             REX.W leaq r15,[r9+0xc]
0x7bffb000a72e   26e  4d897d50             REX.W movq [r13+0x50] (external value (Heap::NewSpaceAllocationTopAddress())),r15
0x7bffb000a732   272  4983c101             REX.W addq r9,0x1
0x7bffb000a736   276  41c741ff15050000     movl [r9-0x1],0x515
0x7bffb000a73e   27e  49baa245b6f3fdb44440 REX.W movq r10,0x4044b4fdf3b645a2
0x7bffb000a748   288  c4c1f96ec2           vmovq xmm0,r10
0x7bffb000a74d   28d  c4c17b114103         vmovsd [r9+0x3],xmm0
0x7bffb000a753   293  45894817             movl [r8+0x17],r9
0x7bffb000a757   297  41f6c101             testb r9,0x1
0x7bffb000a75b   29b  0f8414000000         jz 0x7bffb000a775  <+0x2b5>
0x7bffb000a761   2a1  49c7c70000fcff       REX.W movq r15,0xfffc0000
0x7bffb000a768   2a8  4d23f8               REX.W andq r15,r8
0x7bffb000a76b   2ab  41f60704             testb [r15],0x4
0x7bffb000a76f   2af  0f8509070000         jnz 0x7bffb000ae7e  <+0x9be>
0x7bffb000a775   2b5  448961ff             movl [rcx-0x1],r12 << write new map

```

rcx is now the object we're going to mess up:

```
(rr) job $rcx
0x71f4001994c5: [JS_OBJECT_TYPE]
 - map: 0x71f40006406d <Map[16](HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x71f40004c441 <Object map = 0x71f40004ba49>
 - elements: 0x71f400000745 <FixedArray[0]> [HOLEY_ELEMENTS]
 - properties: 0x71f40019951d <PropertyArray[6]>
 - All own properties (excluding elements): {
    0x71f400003295: [String] in ReadOnlySpace: #C: 0x71f4001994dd <HeapNumber 42.42> (const data field 0, attrs: [WEC]) @ Any, location: in-object
    0x71f400003495: [String] in ReadOnlySpace: #c: 42 (const data field 1, attrs: [WEC]) @ Any, location: properties[0]
    0x71f4000034a5: [String] in ReadOnlySpace: #d: 42 (data field 2, attrs: [WEC]) @ Any, location: properties[1]
    0x71f400003485: [String] in ReadOnlySpace: #b: 42 (data field 3, attrs: [WEC]) @ Any, location: properties[2]
    0x71f4000034c5: [String] in ReadOnlySpace: #f: 0x71f4001994a9 <Object map = 0x71f40004c265> (data field 4, attrs: [WEC]) @ Any, location: properties[3]
 }

```

and r9 is the HeapNumber we've successfully allocated:

```
(rr) job $r9
0x71f40019953d: [HeapNumber]
 - map: 0x71f400000515 <Map[12](HEAP_NUMBER_TYPE)>
 - value: 41.414

```

However, the PropertyArray we now have is:

```
(rr) job 0x71f40019951d
0x71f40019951d: [PropertyArray]
 - map: 0x71f400000995 <Map(PROPERTY_ARRAY_TYPE)>
 - length: 6
 - hash: 0
         0-2: 42
           3: 0x71f4001994a9 <Object map = 0x71f40004c265>
         4-5: 0x71f400000011 <undefined>

```

so we haven't written the HeapNumber there.

There's another PropertyArray in r8:

```
(rr) job $r8
0x71f4001994e9: [PropertyArray]
 - map: 0x71f400000995 <Map(PROPERTY_ARRAY_TYPE)>
 - length: 3
 - hash: 0
         0-2: 42

```

### ma...@chromium.org (2025-05-16)

Looks like we tried to write the HeapNumber into a PropertyArray:

```
0x7bffb000a753   293  45894817             movl [r8+0x17],r9

```

but this is not the right PropertyArray...

### ma...@chromium.org (2025-05-16)

Theory: we're writing to a wrong PropertyArray, since some part is hoisting the PropertyArray loading and doesn't take into account that extending the property backing store can change it.

### dm...@chromium.org (2025-05-16)

This looks like a bug in Turboshaft's Late Load Elimination.

Slightly shorter repro:

```
function opt() {
  const nop = 0;
  const empty = {};
  const a = {p1: 42.42};

  function foo(b) {
    nop;

    a.p4 = 42;
    b.p2 = 42;
    b.p5 = empty;
    a.p6 = 41.414;
  }

  a.p3 = 42;
  a.p4 = 42;

  for (let i = 0; i < 300; i++) {
    foo(a);
  }
}

opt();
opt();
opt();

```

Which needs flags `--jit-fuzzing --turbolev --no-maglev` (and it's a bit flaky, but not too much).

It's not entirely clear what the bug in Turboshaft's Late Load Elimination is, but it seems that it's getting mixed up with aliases. I'm worried that this bug could also happen in the regular Turbofan/Turboshaft pipeline, so I'm increasing the priority to P1 (and we'll adapt the impact flag accordingly if it's confirmed). I'll investigate more on Monday.

### dm...@chromium.org (2025-05-19)

Quick update: as I was suspecting, this is also an issue in Turbofan's regular pipeline.

Much simpler repro that doesn't require any flags beyond --allow-natives-syntax:

```
function foo(a, b, c) {
  a.x = 42;
  b.y = 99; // Transitioning store
  c.x = 17;
  return a.x;
}

let o1 = { x : 27 };
let o2 = { x : 27 };

%PrepareFunctionForOptimization(foo);
assertEquals(17, foo(o1, o1, o1));

%OptimizeFunctionOnNextCall(foo);
assertEquals(17, foo(o2, o2, o2)); // Currently fails because foo returns 42

```

Fix incoming...

### dm...@chromium.org (2025-05-19)

It seems hard to exploit, and all repros that we have so far either lead to correctness issues or to writing in read-only space (which will always segfault).

However, one way that we think (credit to Leszek for this idea) this could be exploited: with 2 consecutive stores to the same object through aliasing pointers where the 1st one extends the property backing store, and the second store operates on the outdated backing store, then we could return an object where one field is "undefined" instead of an object. And if we have field-type tracking for this field that tells us that it's an object, then in another optimized function, we could try to load a field from "undefined" instead of from an object, which would treat NaN as a pointer in the sandbox (since the property backing store is at offset 4, and in "undefined", there is NaN at offset 4), which could still be a valid address in the sandbox that contains attacker-controlled memory. I haven't tested this, but it sounds doable. (and even if this specific scenario isn't doable, the bug is so huge that I expect that a motivated attacker could find a way to exploit it, so it makes sense to treat this as a security issue).

### dx...@google.com (2025-05-19)

Project: v8/v8  

Branch: main  

Author: Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6564404>

[turboshaft] Fix map-based alias analysis in Late Load Elimination

---


Expand for full commit details
```
     
    Fixed: 417169470 
    Change-Id: I589f6667ce3b26b07a4dffa707ee78f9d642d409 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6564404 
    Reviewed-by: Marja Hölttä <marja@chromium.org> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100349}

```

---

Files:

- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`
- M `src/compiler/turboshaft/snapshot-table-opindex.h`
- M `src/compiler/turboshaft/store-store-elimination-phase.cc`
- M `src/flags/flag-definitions.h`
- A `test/mjsunit/turboshaft/regress-417169470-1.js`
- A `test/mjsunit/turboshaft/regress-417169470-2.js`
- A `test/mjsunit/turboshaft/regress-417169470-3.js`
- A `test/mjsunit/turboshaft/regress-417169470-4.js`

---

Hash: 37d6fa3f39e17bf46d1cdf340e666cbd3ff976b3  

Date:  Mon May 19 12:48:48 2025


---

### 24...@project.gserviceaccount.com (2025-05-20)

ClusterFuzz testcase 6230816795328512 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=100348:100349

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2025-05-20)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dm...@chromium.org (2025-05-20)

Replies to [Comment #33](https://issues.chromium.org/issues/417169470#comment33):

1. <https://chromium-review.googlesource.com/c/v8/v8/+/6564404>
2. It landed yesterday in V8 and is in Chrome 138.0.7190.2, so canary coverage might still be a bit light.
3. no
4. no
5. no

### am...@chromium.org (2025-05-21)

No issues in Canary data; M137 merge approved for <https://crrev.com/c/6564404>; please merge this fix to 13.7 at your earliest convenience so that this fix can be included in M137 Stable if recut before release and Stable promotion next week.

Please hold off merging to M136 for now to ensure that fix is not included in Extended Stable before Stable.

### dx...@google.com (2025-05-22)

Project: v8/v8  

Branch: refs/branch-heads/13.7  

Author: Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6574467>

Merged: [turboshaft] Fix map-based alias analysis in Late Load Elimination

---


Expand for full commit details
```
     
    Bug: 417169470 
    (cherry picked from commit 37d6fa3f39e17bf46d1cdf340e666cbd3ff976b3) 
     
    Change-Id: Ib1b83f19f4a8ce52b844771e6bec1cefa31cfeb6 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6574467 
    Reviewed-by: Marja Hölttä <marja@chromium.org> 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.7@{#18} 
    Cr-Branched-From: dd5370d3d251320f6a5bed609ff8e1b71c767d97-refs/heads/13.7.152@{#1} 
    Cr-Branched-From: fa9b75303b0b5d2940a67096dca3babd14aa1fd2-refs/heads/main@{#99927}

```

---

Files:

- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`
- M `src/compiler/turboshaft/snapshot-table-opindex.h`
- M `src/compiler/turboshaft/store-store-elimination-phase.cc`
- M `src/flags/flag-definitions.h`
- A `test/mjsunit/turboshaft/regress-417169470-1.js`
- A `test/mjsunit/turboshaft/regress-417169470-2.js`
- A `test/mjsunit/turboshaft/regress-417169470-3.js`
- A `test/mjsunit/turboshaft/regress-417169470-4.js`

---

Hash: 96d88f5f25963997c603e2fe0ec7c971e1af5245  

Date:  Mon May 19 12:48:48 2025


---

### pe...@google.com (2025-05-22)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dm...@chromium.org (2025-05-22)

[Comment #37](https://issues.chromium.org/issues/417169470#comment37):

This bug has been around since <https://crrev.com/c/5522500>, which landed in 126 (and it even existed before, but the code was disabled by default).
So yea, makes sense to backmerge to LTS M132.

### pe...@google.com (2025-05-23)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-05-23)

1. https://chromium-review.googlesource.com/c/v8/v8/+/6579090
2. Medium - There were some conflicts.
3. 137
4. Yes, the suspected CL landed in M126 according to the comment #38.

### sp...@google.com (2025-05-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
below baseline report of memory corruption in a sandboxed process, as presented this issue was specific to the experimental configuration of V8 and would not have been considered a security issue or eligible for VRP reward


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-28)

Thank you for the report. We did want to extend a reward since we were able to land a fix for a security relevant issue. Since a lot of the work here was done by the V8 engineering team to parse your report and test case to determine this as a potentially exploitable security security issue in V8 and, as presented was specific to the experimental configuration of Chrome, we extended a reduced reward to reflect that, but also to still show our appreciation for reporting it to us.

### am...@chromium.org (2025-05-29)

M136 extended stable has been released, please feel free to merge this fix to 13.6 at your earliest convenience

### gm...@google.com (2025-05-29)

Delaying approval to LTS-132 because it hasn't been out in Stable 136 yet.

### dx...@google.com (2025-05-30)

Project: v8/v8  

Branch: refs/branch-heads/13.6  

Author: Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6607080>

[M136][turboshaft] Fix map-based alias analysis in Late Load Elimination

---


Expand for full commit details
```
     
    (cherry picked from commit 37d6fa3f39e17bf46d1cdf340e666cbd3ff976b3) 
     
    Fixed: 417169470 
    Merged: 13.6 
    Change-Id: I589f6667ce3b26b07a4dffa707ee78f9d642d409 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6607080 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.6@{#28} 
    Cr-Branched-From: 04fa9cbe26525ab96ab3ff2a18b5d25e443e12fa-refs/heads/13.6.233@{#1} 
    Cr-Branched-From: f6be4827a049a8c3ea9218934c7bb5728369a3e7-refs/heads/main@{#99571}

```

---

Files:

- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`
- M `src/compiler/turboshaft/snapshot-table-opindex.h`
- M `src/compiler/turboshaft/store-store-elimination-phase.cc`
- M `src/flags/flag-definitions.h`
- A `test/mjsunit/turboshaft/regress-417169470-1.js`
- A `test/mjsunit/turboshaft/regress-417169470-2.js`
- A `test/mjsunit/turboshaft/regress-417169470-3.js`
- A `test/mjsunit/turboshaft/regress-417169470-4.js`

---

Hash: 447c1445c9805e0e9109d077cc43493f37e17b5a  

Date:  Mon May 19 12:48:48 2025


---

### dx...@google.com (2025-06-12)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6579090>

[M132-LTS][turboshaft] Fix map-based alias analysis in Late Load Elimination

---


Expand for full commit details
```
     
    (cherry picked from commit 37d6fa3f39e17bf46d1cdf340e666cbd3ff976b3) 
     
    Fixed: 417169470 
    Change-Id: I589f6667ce3b26b07a4dffa707ee78f9d642d409 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6564404 
    Reviewed-by: Marja Hölttä <marja@chromium.org> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#100349} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6579090 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.2@{#92} 
    Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
    Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`
- M `src/compiler/turboshaft/snapshot-table-opindex.h`
- M `src/compiler/turboshaft/store-store-elimination-phase.cc`
- M `src/flags/flag-definitions.h`
- A `test/mjsunit/turboshaft/regress-417169470-1.js`
- A `test/mjsunit/turboshaft/regress-417169470-2.js`
- A `test/mjsunit/turboshaft/regress-417169470-3.js`
- A `test/mjsunit/turboshaft/regress-417169470-4.js`

---

Hash: 5cf18d038fd472cd3d6d8bbdcdba4edde7cee3c3  

Date:  Mon May 19 12:48:48 2025


---

### ch...@google.com (2025-08-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/417169470)*
