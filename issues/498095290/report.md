# V8 sandbox bypass: WasmDispatchTable swapping lead to use of not fully initialized WasmTrustedInstanceData

| Field | Value |
|-------|-------|
| **Issue ID** | [498095290](https://issues.chromium.org/issues/498095290) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pv...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2026-03-31 |
| **Bounty** | $20,000.00 |

## Description

## SUMMARY

- When calling `InstanceBuilder::SetTableInitialValues` it resolves `WasmDispatchTable` from table object which can be swapped due to concurrent modify

```
void InstanceBuilder::SetTableInitialValues() {
  for (int table_index = 0;
       table_index < static_cast<int>(module_->tables.size()); ++table_index) {
      ...     // table object from untrusted space
      DirectHandle<WasmTableObject> table_object(
        Cast<WasmTableObject>(maybe_shared_data->tables()->get(table_index)),
        isolate_);
        ...
      SetFunctionTablePlaceholder(isolate_, maybe_shared_data, table_object,
                                    entry_index, table.initial_value.index());
                                    ...
}


V8_INLINE void SetFunctionTablePlaceholder(
    Isolate* isolate,
    DirectHandle<WasmTrustedInstanceData> trusted_instance_data,
    DirectHandle<WasmTableObject> table_object, uint32_t entry_index,
    uint32_t func_index) {
    ...
    
    WasmTableObject::UpdateDispatchTable(isolate, table_object, entry_index,
                                       function, trusted_instance_data
#if V8_ENABLE_DRUMBRAKE
                                       ,
                                       func_index
#endif  // V8_ENABLE_DRUMBRAKE
  );
}


void WasmTableObject::UpdateDispatchTable(
    Isolate* isolate, DirectHandle<WasmTableObject> table, int entry_index,
    const wasm::WasmFunction* func,
    DirectHandle<WasmTrustedInstanceData> target_instance_data
#if V8_ENABLE_DRUMBRAKE
    ,
    int target_func_index
#endif  // V8_ENABLE_DRUMBRAKE
) {

... // reoslve dispatch table from table object
DirectHandle<WasmDispatchTable> dispatch_table(
      table->trusted_dispatch_table(isolate), isolate);
...
}


```

- This make a dispatch table can contain an entry with a not fully initialized `WasmTrustedInstanceData` if the instantiating fails later and can be called via call indirect opcode

## Exploit

- When the instantiating fails (in the poc it is caused by a fail in const expression with a very large wasm array) the `memory_bases_and_sizes` will not be initilized and its entries are

```
for (uint32_t i = 0; i < num_memories; ++i) {
      memory_bases_and_sizes->set(
          2 * i, reinterpret_cast<Address>(empty_backing_store_buffer));
      memory_bases_and_sizes->set(2 * i + 1, 0);
    }

```

- With the `size = 0` it can make wrong bound check when accessing memory with trap handling disabled

```
Register BoundsCheckMem(FullDecoder* decoder, const WasmMemory* memory,
                          uint32_t access_size, uint64_t offset,
                          LiftoffRegister index, LiftoffRegList pinned,
                          ForceCheck force_check,
                          AlignmentCheck check_alignment) {
...
    LiftoffRegister effective_size_reg = end_offset_reg;
    __ emit_ptrsize_sub(effective_size_reg.gp(), mem_size.gp(),
                        end_offset_reg.gp());

    __ emit_cond_jump(kUnsignedGreaterThanEqual, trap.label(), kIntPtrKind,
                      index_ptrsize, effective_size_reg.gp(), trap.frozen());
    return index_ptrsize;
  }

```

- It takes `mem_size` from `memory_bases_and_sizes` which will be `0` in runtime and subtract to `end_offset_reg` which is `7` in my poc. This make the result be a very large number -> arb write in fully 64bit address
- Note: the poc have to run with `--no-wasm-memory64-trap-handling` to disable trap handling but with arm64 it can be run with default since `kPartialOOBWritesAreNoops = false`

```
#if V8_TARGET_ARCH_ARM64 && !V8_OS_MACOS
constexpr bool kPartialOOBWritesAreNoops = false;
#else
constexpr bool kPartialOOBWritesAreNoops = true;
#endif

```
```
void StoreMem(FullDecoder* decoder, StoreType type,
                const MemoryAccessImmediate& imm, const Value& index_val,
                const Value& value_val) {
    ...
        // arm64 and type size can force it to check bound
    ForceCheck force_check = (kPartialOOBWritesAreNoops || type.size() == 1)
                                   ? kDontForceCheck
                                   : kDoForceCheck;
      index =
          BoundsCheckMem(decoder, imm.memory, type.size(), imm.offset,
                         full_index, pinned, force_check, kDontCheckAlignment);
                         
    ...

```
## REPRODUCE

- Run with `.\d8.exe --no-wasm-memory64-trap-handling --expose-memory-corruption-api uninit_instance.js`
- Or `.\d8.exe --expose-memory-corruption-api uninit_instance.js` on arm64
- It will write `0xdeadbeef` at `0x414141414141`

## Crash state

```
(83b0.5dcc): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
000001c1`b8051a35 4889540108      mov     qword ptr [rcx+rax+8],rdx ds:00004141`41414141=????????????????

```
```
RAX: 00003CD34141413A   RBX: 0000000000000000   RCX: 0000046DFFFFFFFF   
RDX: 00000000DEADBEEF   RSI: 000001C601081679   RDI: 000001C1B8051A08   
RIP: 000001C1B8051A35   RSP: 0000002E7E5FB2E8   RBP: 0000002E7E5FB308   
R8:  0000000000000008   R9:  0000000000000001   R10: 00007FF734E40000   
R11: 0000000000000000   R12: 0000000000000000   R13: 0000183400E68080   
R14: 0000036E00000000   R15: 0000036E01413395   
EFLAGS: 00010203 CF=1 PF=0 AF=0 ZF=0 SF=0 TF=0 IF=1 DF=0 OF=0
LastErrorValue: 0x00000000
LastStatusValue: 0xC0000018

```
```
00 0000002e`7e5fb2e8 000001c1`b7ca1ac5     0x000001c1`b8051a35
01 0000002e`7e5fb318 00007ff7`3a103249     0x000001c1`b7ca1ac5
02 0000002e`7e5fb368 00007ff7`3a1ef19c     d8!Builtins_JSToWasmWrapperAsm+0x89
03 0000002e`7e5fb3a0 00007ff7`3a058683     d8!Builtins_JSToWasmWrapper+0xc5c
04 0000002e`7e5fb598 00007ff7`3a058683     d8!Builtins_InterpreterEntryTrampoline+0x143
05 0000002e`7e5fb610 00007ff7`3a05541c     d8!Builtins_InterpreterEntryTrampoline+0x143
06 0000002e`7e5fb6d0 00007ff7`3a054f7f     d8!Builtins_JSEntryTrampoline+0x5c
07 0000002e`7e5fb6f8 00007ff7`356d812c     d8!Builtins_JSEntry+0xff
08 0000002e`7e5fb820 00007ff7`356d286f     d8!v8::internal::GeneratedCode<unsigned long long,unsigned long long,unsigned long long,unsigned long long,unsigned long long,long long,unsigned long long **>::Call+0x6c [D:\30_3_2026\v8\src\execution\simulator.h @ 216] 
09 0000002e`7e5fb880 00007ff7`356d3210     d8!v8::internal::`anonymous namespace'::Invoke+0x3d8f [D:\30_3_2026\v8\src\execution\execution.cc @ 473] 
0a 0000002e`7e5fd720 00007ff7`34ff6248     d8!v8::internal::Execution::CallScript+0x110 [D:\30_3_2026\v8\src\execution\execution.cc @ 574] 
0b 0000002e`7e5fd830 00007ff7`34ff58ae     d8!v8::Script::Run+0x958 [D:\30_3_2026\v8\src\api\api.cc @ 2041] 
0c 0000002e`7e5fde30 00007ff7`34ea8c60     d8!v8::Script::Run+0x9e [D:\30_3_2026\v8\src\api\api.cc @ 2006] 
0d 0000002e`7e5fdec0 00007ff7`34f071ac     d8!v8::Shell::ExecuteString+0x18f0 [D:\30_3_2026\v8\src\d8\d8.cc @ 1043] 
0e 0000002e`7e5feb90 00007ff7`34f125af     d8!v8::SourceGroup::Execute+0x76c [D:\30_3_2026\v8\src\d8\d8.cc @ 5682] 
0f 0000002e`7e5fee00 00007ff7`34f1145d     d8!v8::Shell::RunMainIsolate+0x94f [D:\30_3_2026\v8\src\d8\d8.cc @ 6703] 
10 0000002e`7e5ff3a0 00007ff7`34f14cee     d8!v8::Shell::RunMain+0xcd [D:\30_3_2026\v8\src\d8\d8.cc @ 6611] 
11 0000002e`7e5ff630 00007ff7`34f158e3     d8!v8::Shell::Main+0xfce [D:\30_3_2026\v8\src\d8\d8.cc @ 7528] 
12 0000002e`7e5ffe70 00007ff7`3a2623c8     d8!main+0x23 [D:\30_3_2026\v8\src\d8\d8.cc @ 7631] 
13 (Inline Function) --------`--------     d8!invoke_main+0x22 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 78] 
14 0000002e`7e5ffeb0 00007ffe`25a0e8d7     d8!__scrt_common_main_seh+0x10c [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
15 0000002e`7e5ffef0 00007ffe`26c4c48c     KERNEL32!BaseThreadInitThunk+0x17
16 0000002e`7e5fff20 00000000`00000000     ntdll!RtlUserThreadStart+0x2c

```
## Credit

- Nao(@natsumikyouno\_\_)

## Attachments

- [uninit_instance.js](attachments/uninit_instance.js) (text/javascript, 3.4 KB)

## Timeline

### ja...@google.com (2026-03-31)

[security triage] following the v8 triage procedure. This looks like it has a poc and a trace and command to reproduce it.

### ch...@google.com (2026-04-01)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-01)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cl...@appspot.gserviceaccount.com (2026-04-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4536519108886528.

### cl...@appspot.gserviceaccount.com (2026-04-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6537555109511168.

### 24...@project.gserviceaccount.com (2026-04-01)

Detailed Report: https://clusterfuzz.com/testcase?key=6537555109511168

Fuzzer: None
Job Type: linux_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 
Crash State:
  NULL
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&range=106221:106222

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6537555109511168

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2026-04-02)

Thanks for this report!

Looks like a legit sandbox escape, but I'll only be able to work on this next week.

### cl...@chromium.org (2026-04-08)

I'll prepare a fix to pass down the dispatch table together with the table object through most methods. We will load it from the trusted instance data then instead of from the table object.

### dx...@google.com (2026-04-09)

Project: v8/v8  

Branch:  main  

Author:  Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7736088>

[wasm] Introduce empty\_wasm\_dispatch\_table root

---


Expand for full commit details
```
     
    Follow-up CLs will change Wasm table objects to always store a dispatch 
    table (for stricter types, avoiding `Union<Smi, WasmDispatchTable>`). 
    This new root avoids repeated allocations of empty dispatch tables. 
     
    Avoid allocating the `TrustedManaged` for that empty table though; it's 
    never used anyway. 
     
    R=jkummerow@chromium.org 
     
    Bug: 498095290 
    Change-Id: I2ea847a54e08ffb7e8bec151582f9e3b9601af02 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7736088 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Clemens Backes <clemensb@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106349}

```

---

Files:

- M `src/heap/factory.cc`
- M `src/heap/setup-heap-internal.cc`
- M `src/roots/roots.h`
- M `src/wasm/wasm-objects-inl.h`
- M `src/wasm/wasm-objects.cc`

---

Hash: [19a0b1da2e8d683e4c2ad8f1520ffbe4502ca2fa](https://chromiumdash.appspot.com/commit/19a0b1da2e8d683e4c2ad8f1520ffbe4502ca2fa)  

Date: Wed Apr 8 15:31:18 2026


---

### dx...@google.com (2026-04-09)

Project: v8/v8  

Branch:  main  

Author:  Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7734899>

[wasm] Always set a dispatch table for all tables

---


Expand for full commit details
```
     
    This allows to use a stricter type, avoiding `Union<Smi, 
    WasmDispatchTable>` and will make the follow-up CL much simpler. 
     
    R=jkummerow@chromium.org 
     
    Bug: 498095290 
    Change-Id: I48d10e3b7e32a13e095636326d492d28d82cd5c4 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7734899 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Clemens Backes <clemensb@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106352}

```

---

Files:

- M `src/diagnostics/objects-debug.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-objects-inl.h`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.h`
- M `src/wasm/wasm-objects.tq`

---

Hash: [aee5dedab9a9a5d39fd68ea981222024a939e7cb](https://chromiumdash.appspot.com/commit/aee5dedab9a9a5d39fd68ea981222024a939e7cb)  

Date: Wed Apr 8 17:02:37 2026


---

### dx...@google.com (2026-04-09)

Project: v8/v8  

Branch:  main  

Author:  Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7739142>

[wasm] Pass dispatch table as parameter for sandbox safety

---


Expand for full commit details
```
     
    Load the dispatch table from the WasmTrustedInstanceData whenever 
    possible instead of from the untrusted WasmTableObject. 
     
    This is particularly important during instantiation where we need to 
    avoid writing a pointer to a partially initialized 
    WasmTrustedInstanceData into an existing WasmDispatchTable associated 
    with another table or instance. 
     
    R=jkummerow@chromium.org 
     
    Bug: 498095290 
    Change-Id: Id5ef447405461c447b60db0113eb81c58b8b3f29 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7739142 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Clemens Backes <clemensb@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106366}

```

---

Files:

- M `src/runtime/runtime-wasm.cc`
- M `src/wasm/c-api.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-js.cc`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.h`

---

Hash: [534f607e8951004e479c246cf30e2c9d5bae1d4f](https://chromiumdash.appspot.com/commit/534f607e8951004e479c246cf30e2c9d5bae1d4f)  

Date: Thu Apr 9 14:25:45 2026


---

### dx...@google.com (2026-04-13)

Project: v8/v8  

Branch:  main  

Author:  Gyuyoung Kim [gyuyoung@igalia.com](mailto:gyuyoung@igalia.com)  

Link:    <https://chromium-review.googlesource.com/7750624>

[wasm-interpreter] Pass a dispatch table as a parameter

---


Expand for full commit details
```
     
    https://crrev.com/c/7739142 missed passing a dispatch table as a 
    parameter for the wasm interpreter. Also it missed renaming 
    `new_dispatch_table` to `dispatch_table`. This CL fixes them. 
     
    Bug: 498095290 
    Change-Id: I0bbf74005963ce24f6de130dfb7cdbc0a3829eee 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7750624 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Paolo Severini <paolosev@microsoft.com> 
    Commit-Queue: Gyuyoung Kim <gyuyoung@igalia.com> 
    Cr-Commit-Position: refs/heads/main@{#106420}

```

---

Files:

- M `src/wasm/interpreter/wasm-interpreter-runtime.cc`
- M `src/wasm/wasm-objects.cc`

---

Hash: [fd54ab6c9446d246b8661ff69fcd14f87566b9c7](https://chromiumdash.appspot.com/commit/fd54ab6c9446d246b8661ff69fcd14f87566b9c7)  

Date: Sat Apr 11 08:52:21 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
v8 Sandbox escape with controlled write


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/498095290)*
