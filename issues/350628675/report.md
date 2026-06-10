# V8 Sandbox Bypass: AAR/W via WASM dispatch table index OOB from `WasmTableObject.uses`

| Field | Value |
|-------|-------|
| **Issue ID** | [350628675](https://issues.chromium.org/issues/350628675) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-07-02 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

V8 sandbox bypass, arbitrary address read/write via WASM dispatch table index OOB where the index is fetched from `WasmTableObject.uses`. This index value can be modified with in-sandbox exploit primitives.

`WasmTableObject` holds `uses`, which is a even-sized FixedArray holding pairs of `<WasmInstanceObject, table_index smi>`. This is used to update the dispatch table linked to this table object. Both the values are modifiable with in-sandbox exploit but the index is not checked to be within bounds of the `ProtectedFixedArray<WasmDispatchTable>` (ex: [`WasmTableObject::Grow()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/wasm-objects.cc;l=249;drc=2fdefb5683cd3e7f7734fb22c9a1cea3d06ece67) -> [`WasmTrustedInstanceData::EnsureMinimumDispatchTableSize()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/wasm-objects.cc;l=1136;drc=2fdefb5683cd3e7f7734fb22c9a1cea3d06ece67)). This allows OOB access within the trusted region. With controlled data sprays on the trusted region, this can be exploited to obtain arbitrary address read/write.

### VERSION

V8 Version: 2fdefb5683cd3e7f7734fb22c9a1cea3d06ece67

### REPRODUCTION CASE

To be uploaded - the problem seems clear, but the PoC is currently WIP :)

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n)

## Attachments

- [crash_poc.js](attachments/crash_poc.js) (text/javascript, 1004 B)
- [dispatch_table_oob.js](attachments/dispatch_table_oob.js) (text/javascript, 6.3 KB)
- [wasm-module-builder.js](attachments/wasm-module-builder.js) (text/javascript, 71.4 KB)

## Timeline

### da...@chromium.org (2024-07-02)

=> v8 gardener

Provisionally setting foundin to extended stable until we learn more.

### se...@gmail.com (2024-07-02)

Update:

This is a PoC that achieves 100% success rate on my environment (`dispatch_table_oob.js`). Each runs take about 5 seconds, but this can be tweaked so that each runs take under 1sec without compromising much exploitability.

The exploit is a bit lengthy contrary to my previous wasm v8sbx submissions, so let me explain how it works:

1. We make a dummy wasm module to pre-allocate canonical indices for types:
   - `$s = struct { i64 }` as canonical index 3
   - `func [i64, ref $s] -> []` as canonical index 4
   - `func [i64, i64] -> []` as canonical index 5
2. We make some dummy wasm modules to fill up canonical indices as desired.
3. We create the target wasm module to exploit.
   - We create a function type `$sig_0` with canonical index "X"
   - We create ~30000 (`DT_SPRAY_CNT`) tables, each sized 0x10 and containing `$sig_0`-typed function `$f0`
   - We create ~70000 (`100000 - DT_SPRAY_CNT`) tables, each sized 0x10 and containing our exploit wasm function to call (typed `[i64, ref $s] -> []`)
4. The wasm module in step 3 is instantiated, which results in the trusted region to have:
   - `ProtectedFixedArray<WasmDispatchTable>` to be located somewhere near `0x40010`, but always aligned to `0x40000` (and add `+0x10`)
   - `WasmDispatchTable` objects for the ~30000 tables, where we can find one in `DT_SPRAY`
   - `WasmDispatchTable` objects for the ~70000 tables, where we can find one in `DT_TARGET`
   - Canonical index "X" in step 3 is set to somewhere near `DT_TARGET` so that a `WasmTableObject::Grow()` overwrites its entries' signature instead of its length
5. Modify a non-function `WasmTableObject` so that it now has a `FixedArray uses`, and set the index out-of-bounds so that we use canonical index "X" in the ~30000 `WasmDispatchTable` as a tagged pointer to a `WasmDispatchTable`
6. Corrupt and grow the `WasmTableObject`:
   - At `WasmTableObject::Grow()` we get the OOB `table_index` from `uses` and passes it down to `WasmTrustedInstanceData::EnsureMinimumDispatchTableSize()`
   - The function loads `old_dispatch_table` from `trusted_instance_data->dispatch_table(table_index)`, which is OOB and uses canonical index "X" in the ~30000 `WasmDispatchTable` entries as a tagged pointer instead. This loads a fake `WasmTableObject` located somewhere near `DT_TARGET` but in a misaligned state
   - `old_dispatch_table->length() >= minimum_size` => does not satisfy, as the object is set such that `length()` fetches the canonical signature of an entry from the ~70000 `WasmDispatchTable`.
   - We call `WasmDispatchTable::Grow()` with fake `WasmDispatchTable`, now checking `new_length < old_table->capacity()` => this satisfies, as `capacity()` is set to fetch the `Map` of the next `WasmDispatchTable` which is constant (by build) and is >0x1000, where `new_length = 5`. Thus we overwrite `length()` field, which is the canonical signature of one of the entries
7. Call each of the table entries, where one of them will have its signature in the dispatch table corrupted to `5` instead of `4`. This results in the rtt subtype check to pass and cause function signature confusion, leading to AAR/W.
   - Note that this is different from [b/350292240](https://issues.chromium.org/issues/350292240) which exploits the fact that we're comparing a trusted signature with data from in-sandbox object. In this bug we have a primitive to corrupt trusted region and modify the trusted data within dispatch table.

Most of the code is heap spraying and other boilerplates to set up data in the trusted region. If what you need is just a PoC showing crash due to an OOB access in trusted region, use the `crash_poc.js` which just crashes with an invalid `table_index` access from `ProtectedFixedArray<WasmDispatchTable>`.

### pe...@google.com (2024-07-03)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cl...@appspot.gserviceaccount.com (2024-07-04)

Detailed Report: https://clusterfuzz.com/testcase?key=5999287395614720

Fuzzer: None
Job Type: linux_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 
Crash State:
  NULL
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&revision=94835

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5999287395614720

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@chromium.org (2024-07-04)

Thanks for the detailed write-up, super cool! I can fairly easily reproduce this locally (`is_debug = false, dcheck_always_on = false, target_cpu = "x64", v8_enable_memory_corruption_api = true`), and now also managed to repro it on CF (seemingly I need to set a higher timeout, but otherwise it seems to work fine).

### se...@gmail.com (2024-07-04)

Great to see it work on CF too! Noticed that I haven't updated debug logs so the second-to-last printed log should instead say something like `Triggering dispatch table entry signature overwrite` :)

### 24...@project.gserviceaccount.com (2024-07-05)

ClusterFuzz testcase 5999287395614720 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2024-07-05)

ClusterFuzz testcase 5999287395614720 appears to be flaky, updating reproducibility hotlist.

### se...@gmail.com (2024-10-21)

FYI, the fix for this would be simple - do a `SBXCHECK_BOUNDS()` on the index before using it. AFAICT some code that relies on `WasmTableObject.uses` already has somewhat of a mitigation added (unintentionally from shared-everything implementation) due to C++ vector indexing which would abort on OOB.

### pe...@google.com (2024-10-28)

jkummerow: Uh oh! This issue still open and hasn't been updated in the last 115 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-12)

jkummerow: Uh oh! This issue still open and hasn't been updated in the last 130 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### jk...@chromium.org (2024-11-13)

#11/#12: The V8 sandbox is WIP, known sandbox escapes were only recently raised to P1.

I've been working on the proper solution for this for months, see changes on [issue 42204526](https://issues.chromium.org/issues/42204526). The plan is:  

(1) Share import wrappers per process - Done.  

(2) Share `WasmDispatchTable` per `WasmTableObject` - currently writing code for this.  

(3) No longer have an on-heap `WasmTableObject.uses` list → no more sandbox escapes by corrupting it \o/

If someone wants to land a bounds check (as suggested in #10) as a temporary mitigation, go for it. I haven't spent much time thinking through how complete of a solution that would be; I have a vague gut feeling that it might still allow more complicated cases of confusion, but no specific theory.

### ap...@google.com (2024-12-02)

Project: v8/v8  

Branch: main  

Author: Jakob Kummerow <[jkummerow@chromium.org](mailto:jkummerow@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6035506>

[wasm][sandbox] One WasmDispatchTable per WasmTableObject

---


Expand for full commit details
```
[wasm][sandbox] One WasmDispatchTable per WasmTableObject 
 
Instead of having a WasmDispatchTable for each instance that uses 
a given table, all these instances now share the same dispatch table. 
This CL includes a few tightly connected changes: 
- store a WasmDispatchTable on each WasmTableObject 
- drop WasmTableObject::uses 
- introduce WasmDispatchTable::uses, because instances have pointers 
  to dispatch tables, which need to be updated when the dispatch 
  table is reallocated in order to grow. This list is weak, to allow 
  old instances to get freed. 
- WasmImportData::call_origin is now a protected field storing either 
  a WasmInternalFunction or a WasmDispatchTable. We no longer need 
  to store Smis or Tuple2s there. 
 
Fixed: 350628675, 42204123 
Change-Id: Ia48ab26ac9d77b21054bae5fd2cea848daab93d0 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6035506 
Reviewed-by: Clemens Backes <clemensb@chromium.org> 
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97495}

```

---

Files:

- M `src/diagnostics/objects-debug.cc`
- M `src/diagnostics/objects-printer.cc`
- M `src/execution/frames.cc`
- M `src/heap/factory.cc`
- M `src/heap/factory.h`
- M `src/objects/objects-body-descriptors-inl.h`
- M `src/runtime/runtime-wasm.cc`
- M `src/wasm/c-api.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/value-type.cc`
- M `src/wasm/value-type.h`
- M `src/wasm/wasm-js.cc`
- M `src/wasm/wasm-module.h`
- M `src/wasm/wasm-objects-inl.h`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.h`
- M `src/wasm/wasm-objects.tq`
- M `test/cctest/wasm/wasm-run-utils.cc`
- M `test/unittests/runtime/runtime-debug-unittest.cc`

---

Hash: 74caf5449508c72236970e5d9e01b7212d609122  

Date:  Mon Dec 02 11:37:24 2024


---

### sp...@google.com (2024-12-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
report of V8 sandbox bypass demonstrating arbitrary write outside of the V8 sandbox 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-05)

Thank you for the high-quality and impactful sandbox bypass report, Seunghyun!

### ch...@google.com (2025-03-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/350628675)*
