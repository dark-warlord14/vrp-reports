# v8 crash on regexp length check

| Field | Value |
|-------|-------|
| **Issue ID** | [40095436](https://issues.chromium.org/issues/40095436) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | yn...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2019-06-19 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36

Steps to reproduce the problem:
1.
2.
3.

What is the expected behavior?

What went wrong?
pco:
function main() {
function v2() {
    const v8 = Symbol || 9007199254740991;
    function v9(v10,v11,v12) {
    }
    const v16 = String();
    const v17 = Int32Array();
    const v18 = Map();
    const v19 = [];
    const v20 = v18.values();
    function v21(v22,v23,v24,v25,v26) {
    }
    function v28(v29,v30,v31) {
        function v32(v33,v34,v35,v36) {
        }
        let v39 = 0;
        do {
            const v40 = v32();
            %OptimizeFunctionOnNextCall(v32)
        } while (v39 < 8);
    }
    const v41 = Promise();
}
const v46 = ["has",13.37,-9007199254740991,Reflect];
for (let v50 = 64; v50 <= 1337; v50++) {
    let v51 = v46;
    const v52 = v51.push(v50,v2);
}
const v54 = RegExp(v46);
const v55 = v54.exec();
}
main();

windbg backtrace:
00 000000b6`321fe188 00007ffc`a1fdd2a8 v8_libbase!v8::base::OS::DebugBreak 
*** WARNING: Unable to verify checksum for F:\Browser\Chrome\yngwei_v8\v8\out.gn\x64.debug\v8.dll
01 000000b6`321fe190 00007ffc`6c14ff0e v8_libbase!v8::base::OS::Abort+0x18 
02 000000b6`321fe1d0 00007ffc`6c14f9d2 v8!v8::internal::__RT_impl_Runtime_AbortJS+0x31e 
03 000000b6`321fe2d0 00007ffc`6cfa13c4 v8!v8::internal::Runtime_AbortJS+0x152  
04 000000b6`321fe370 00007274`94a365da v8!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit+0x44
05 000000b6`321fe378 00007ffc`6cd37f01 0x00007274`94a365da
06 000000b6`321fe380 000000b6`321fe388 v8!Builtins_AbortJS+0x61
07 000000b6`321fe388 00000000`00000018 0x000000b6`321fe388
08 000000b6`321fe390 00007274`94a365fa 0x18
09 000000b6`321fe398 00007ffc`6ceb16f7 0x00007274`94a365fa
0a 000000b6`321fe3a0 000000b6`321fe3b0 v8!Builtins_RegExpPrototypeExec+0x2737
0b 000000b6`321fe3a8 000000b6`321fe370 0x000000b6`321fe3b0
0c 000000b6`321fe3b0 00000000`00000006 0x000000b6`321fe370
0d 000000b6`321fe3b8 000000b6`321fe458 0x6
0e 000000b6`321fe3c0 00007ffc`6ceb60be 0x000000b6`321fe458
0f 000000b6`321fe3c8 000003ea`53328a79 v8!Builtins_RegExpPrototypeExec+0x70fe
10 000000b6`321fe3d0 00000000`000804d4 0x000003ea`53328a79
11 000000b6`321fe3d8 000002c1`eab81509 0x804d4
12 000000b6`321fe3e0 0000036c`a8900139 0x000002c1`eab81509
13 000000b6`321fe3e8 00000000`00000000 0x0000036c`a8900139

v8 output:
abort: CSA_ASSERT failed: SmiLessThanOrEqual(length, max_length) [../../src/builtins/builtins-regexp-gen.cc:41]

==== JS stack trace =========================================

    0: ExitFrame [pc: 00007FFC6CFA13C4]
Security context: 0x02c1eab9a6b9 <JSObject>#0#
    1: exec [000002C1EAB88F39](this=0x02a1bfc40181 <JSRegExp <Very long string[701045]>>#1#,0x03ea533004d1 <undefined>)
    2: arguments adaptor frame: 0->1
    3: main [000002C1EAB9F429] [I:\edd\crash.js:30] [bytecode=000002C1EAB9F5C9 offset=84](this=0x02a1bfc40219 <JSGlobal Object>#2#)
    4: /* anonymous */ [000002C1EAB9F379] [I:\edd\crash.js:32] [bytecode=000002C1EAB9F2E9 offset=24](this=0x02a1bfc40219 <JSGlobal Object>#2#)
    5: InternalFrame [pc: 00007FFC6CC56EC1]
    6: EntryFrame [pc: 00007FFC6CC56AAC]

==== Details ================================================

[0]: ExitFrame [pc: 00007FFC6CFA13C4]
[1]: exec [000002C1EAB88F39](this=0x02a1bfc40181 <JSRegExp <Very long string[701045]>>#1#,0x03ea533004d1 <undefined>) {
// optimized frame
--------- s o u r c e   c o d e ---------
<No Source>
-----------------------------------------
}
[2]: arguments adaptor frame: 0->1 {
}

[3]: main [000002C1EAB9F429] [I:\edd\crash.js:30] [bytecode=000002C1EAB9F5C9 offset=84](this=0x02a1bfc40219 <JSGlobal Object>#2#) {
  // expression stack (top to bottom)
  [09] : 0x02a1bfc40181 <JSRegExp <Very long string[701045]>>#1#
  [08] : 0x02a1bfc401b9 <JSArray[2552]>#3#
  [07] : 0x02c1eab88f39 <JSFunction exec (sfi = 0000029F20BCE191)>#4#
  [06] : 2552
  [05] : 0x02a1bfc401b9 <JSArray[2552]>#3#
  [04] : 1338
  [03] : 0x03ea533004d1 <undefined>
  [02] : 0x02a1bfc40181 <JSRegExp <Very long string[701045]>>#1#
  [01] : 0x02a1bfc401b9 <JSArray[2552]>#3#
  [00] : 0x02a1bfc401d9 <JSFunction v2 (sfi = 000002C1EAB9F4E1)>#5#
--------- s o u r c e   c o d e ---------
function main() {\x0afunction v2() {\x0a    const v8 = Symbol || 9007199254740991;\x0a    function v9(v10,v11,v12) {\x0a    }\x0a    const v16 = String();\x0a    const v17 = Int32Array();\x0a    const v18 = Map();\x0a    const v19 = [];\x0a    const v20 = v18.values();\x0a    function v21(v22,v23,v24,v25,v26) {\x0a    }\x0a    function v28(v29,v30...

-----------------------------------------
}

[4]: /* anonymous */ [000002C1EAB9F379] [I:\edd\crash.js:32] [bytecode=000002C1EAB9F2E9 offset=24](this=0x02a1bfc40219 <JSGlobal Object>#2#) {
  // expression stack (top to bottom)
  [04] : 0x02a1bfc40219 <JSGlobal Object>#2#
  [03] : 0x02c1eab9f379 <JSFunction (sfi = 000002C1EAB9EF09)>#6#
  [02] : 0x03ea533004d1 <undefined>
  [01] : 0x02c1eab9f429 <JSFunction main (sfi = 000002C1EAB9EF71)>#7#
  [00] : 0x03ea533004d1 <undefined>
--------- s o u r c e   c o d e ---------
function main() {\x0afunction v2() {\x0a    const v8 = Symbol || 9007199254740991;\x0a    function v9(v10,v11,v12) {\x0a    }\x0a    const v16 = String();\x0a    const v17 = Int32Array();\x0a    const v18 = Map();\x0a    const v19 = [];\x0a    const v20 = v18.values();\x0a    function v21(v22,v23,v24,v25,v26) {\x0a    }\x0a    functio...

-----------------------------------------
}

[5]: InternalFrame [pc: 00007FFC6CC56EC1]
[6]: EntryFrame [pc: 00007FFC6CC56AAC]
==== Key         ============================================

 #0# 000002C1EAB9A6B9: 0x02c1eab9a6b9 <JSObject>
 #1# 000002A1BFC40181: 0x02a1bfc40181 <JSRegExp <Very long string[701045]>>
         lastIndex: 0
 #2# 000002A1BFC40219: 0x02a1bfc40219 <JSGlobal Object>
 #3# 000002A1BFC401B9: 0x02a1bfc401b9 <JSArray[2552]>
                 0: 0x03ea53303e39 <String[#3]: has>
                 1: 0x02c1eab9f541 <HeapNumber 13.37>
                 2: 0x02c1eab9f551 <HeapNumber -9.0072e+15>
                 3: 0x02c1eab8ed41 <Object map = 00000241365C2529>#8#
                 4: 64
                 5: 0x02a1bfc401d9 <JSFunction v2 (sfi = 000002C1EAB9F4E1)>#5#
                 6: 65
                 7: 0x02a1bfc401d9 <JSFunction v2 (sfi = 000002C1EAB9F4E1)>#5#
                 8: 66
                 9: 0x02a1bfc401d9 <JSFunction v2 (sfi = 000002C1EAB9F4E1)>#5#
                  ...
 #4# 000002C1EAB88F39: 0x02c1eab88f39 <JSFunction exec (sfi = 0000029F20BCE191)>
 #5# 000002A1BFC401D9: 0x02a1bfc401d9 <JSFunction v2 (sfi = 000002C1EAB9F4E1)>
 #6# 000002C1EAB9F379: 0x02c1eab9f379 <JSFunction (sfi = 000002C1EAB9EF09)>
 #7# 000002C1EAB9F429: 0x02c1eab9f429 <JSFunction main (sfi = 000002C1EAB9EF71)>
 #8# 000002C1EAB8ED41: 0x02c1eab8ed41 <Object map = 00000241365C2529>
    defineProperty: 0x02c1eab8f119 <JSFunction defineProperty (sfi = 0000029F20BD37C9)>#9#
    deleteProperty: 0x02c1eab8f151 <JSFunction deleteProperty (sfi = 0000029F20BD3801)>#10#
             apply: 0x02c1eab8f189 <JSFunction apply (sfi = 0000029F20BD3839)>#11#
         construct: 0x02c1eab8f1c1 <JSFunction construct (sfi = 0000029F20BD3871)>#12#
               get: 0x02c1eab8ef21 <JSFunction get (sfi = 0000029F20BD38A9)>#13#
getOwnPropertyDescriptor: 0x02c1eab8ef59 <JSFunction getOwnPropertyDescriptor (sfi = 0000029F20BD38E1)>#14#
    getPrototypeOf: 0x02c1eab8ef91 <JSFunction getPrototypeOf (sfi = 0000029F20BD3919)>#15#
               has: 0x02c1eab8efc9 <JSFunction has (sfi = 0000029F20BD3951)>#16#
      isExtensible: 0x02c1eab8f001 <JSFunction isExtensible (sfi = 0000029F20BD3989)>#17#
           ownKeys: 0x02c1eab8f039 <JSFunction ownKeys (sfi = 0000029F20BD39C1)>#18#
 preventExtensions: 0x02c1eab8f071 <JSFunction preventExtensions (sfi = 0000029F20BD39F9)>#19#
               set: 0x02c1eab8f0a9 <JSFunction set (sfi = 0000029F20BD3A31)>#20#
    setPrototypeOf: 0x02c1eab8f0e1 <JSFunction setPrototypeOf (sfi = 0000029F20BD3A69)>#21#
 #9# 000002C1EAB8F119: 0x02c1eab8f119 <JSFunction defineProperty (sfi = 0000029F20BD37C9)>
 #10# 000002C1EAB8F151: 0x02c1eab8f151 <JSFunction deleteProperty (sfi = 0000029F20BD3801)>
 #11# 000002C1EAB8F189: 0x02c1eab8f189 <JSFunction apply (sfi = 0000029F20BD3839)>
 #12# 000002C1EAB8F1C1: 0x02c1eab8f1c1 <JSFunction construct (sfi = 0000029F20BD3871)>
 #13# 000002C1EAB8EF21: 0x02c1eab8ef21 <JSFunction get (sfi = 0000029F20BD38A9)>
 #14# 000002C1EAB8EF59: 0x02c1eab8ef59 <JSFunction getOwnPropertyDescriptor (sfi = 0000029F20BD38E1)>
 #15# 000002C1EAB8EF91: 0x02c1eab8ef91 <JSFunction getPrototypeOf (sfi = 0000029F20BD3919)>
 #16# 000002C1EAB8EFC9: 0x02c1eab8efc9 <JSFunction has (sfi = 0000029F20BD3951)>
 #17# 000002C1EAB8F001: 0x02c1eab8f001 <JSFunction isExtensible (sfi = 0000029F20BD3989)>
 #18# 000002C1EAB8F039: 0x02c1eab8f039 <JSFunction ownKeys (sfi = 0000029F20BD39C1)>
 #19# 000002C1EAB8F071: 0x02c1eab8f071 <JSFunction preventExtensions (sfi = 0000029F20BD39F9)>
 #20# 000002C1EAB8F0A9: 0x02c1eab8f0a9 <JSFunction set (sfi = 0000029F20BD3A31)>
 #21# 000002C1EAB8F0E1: 0x02c1eab8f0e1 <JSFunction setPrototypeOf (sfi = 0000029F20BD3A69)>

Did this work before? N/A 

Chrome version: 75.0.3770.100  Channel: n/a
OS Version: 10.0
Flash Version:

## Timeline

### cl...@chromium.org (2019-06-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-19)

Testcase 5372799446810624 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5372799446810624.

### yn...@gmail.com (2019-06-19)

[Comment Deleted]

### yn...@gmail.com (2019-06-19)

It can reproduce on v8 debug version, and the call chain is (RegExpBuiltinsAssembler::RegExpPrototypeExecBody ---->RegExpBuiltinsAssembler::ConstructNewResultFromMatchInfo  -----> RegExpBuiltinsAssembler::AllocateRegExpResult  ----> CSA), and the CSA code is: 

TNode<Smi> max_length = SmiConstant(JSArray::kInitialMaxFastElementArray);
  CSA_ASSERT(this, SmiLessThanOrEqual(length, max_length));

### me...@chromium.org (2019-06-19)

Thanks, trying again without ASAN.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2019-06-19)

Testcase 5724902358908928 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5724902358908928.

### cl...@chromium.org (2019-06-19)

Testcase 6262659074359296 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6262659074359296.

### is...@chromium.org (2019-06-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-19)

The output from CF (https://clusterfuzz.com/testcase-detail/5724902358908928) is:
[disabled] abort: CSA_ASSERT failed: SmiLessThanOrEqual(length, max_length) [src/builtins/builtins-regexp-gen.cc:41]
Do we know why CF is ignoring this crash?
(adding more people who might know).

### yn...@gmail.com (2019-06-20)

[Comment Deleted]

### yn...@gmail.com (2019-06-20)

TNode<JSRegExpResult> RegExpBuiltinsAssembler::AllocateRegExpResult(
    TNode<Context> context, TNode<Smi> length, TNode<Smi> index,
    TNode<String> input) {
#ifdef DEBUG
     TNode<Smi> max_length = SmiConstant(JSArray::kInitialMaxFastElementArray);
    // CSA_ASSERT(this, SmiLessThanOrEqual(length, max_length));//---> crash here, now comment it
    Print(max_length);//--> DebugPrint: Smi: 0x3ff8 (16376)
    Print(length);//--> DebugPrint: Smi: 0x40b3 (16563)
...
...
  // Initialize the elements.

  DCHECK(!IsDoubleElementsKind(elements_kind));
  const RootIndex map_index = RootIndex::kFixedArrayMap;
  DCHECK(RootsTable::IsImmortalImmovable(map_index));
  StoreMapNoWriteBarrier(elements, map_index);
  StoreObjectFieldNoWriteBarrier(elements, FixedArray::kLengthOffset, length);

  FillFixedArrayWithValue(elements_kind, elements, IntPtrZero(), length_intptr,
                          RootIndex::kUndefinedValue);
    Print(elements);//-->[1]
    Print(result);//-->[2]
  return CAST(result);
}

[1]
DebugPrint: 0x3932d80c1a11: [FixedArray]
 - map: 0x3932b48007b1 <Map>
 - length: 16563
     0-16562: 0x3932b48004d1 <undefined>
0x3932b48007b1: [Map]
 - type: FIXED_ARRAY_TYPE
 - instance size: variable
 - elements kind: HOLEY_ELEMENTS
 - unused property fields: 0
 - enum length: invalid
 - stable_map
 - non-extensible
 - back pointer: 0x3932b48004d1 <undefined>
 - prototype_validity cell: 0
 - instance descriptors (own) #0: 0x3932b4800259 <DescriptorArray[0]>
 - layout descriptor: 0x0
 - prototype: 0x3932b48001d9 <null>
 - constructor: 0x3932b48001d9 <null>
 - dependent code: 0x3932b48002c1 <Other heap object (WEAK_FIXED_ARRAY_TYPE)>
 - construction counter: 0

[2]
DebugPrint: 0x3932d80c19d9: [JSArray]
 - map: 0x393293d84009 <Map(HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x39324cad1109 <JSArray[0]>
 - elements: 0x3932d80c1a11 <FixedArray[16563]> [HOLEY_ELEMENTS]
 - length: 16563
 - properties: 0x3932b4800c21 <FixedArray[0]> {
    #length: 0x3932696001a9 <AccessorInfo> (const accessor descriptor)
    #index: 0 (data field 0)
    #input: 0x3932b48004b1 <String[#9]: undefined> (data field 1)
    #groups: 0x3932b48004d1 <undefined> (data field 2)
 }
 - elements: 0x3932d80c1a11 <FixedArray[16563]> {
     0-16562: 0x3932b48004d1 <undefined>
 }
0x393293d84009: [Map]
 - type: JS_ARRAY_TYPE
 - instance size: 56
 - inobject properties: 3
 - elements kind: HOLEY_ELEMENTS
 - unused property fields: 0
 - enum length: invalid
 - stable_map
 - back pointer: 0x3932b48004d1 <undefined>
 - prototype_validity cell: 0x393269600609 <Cell value= 1>
 - instance descriptors (own) #4: 0x39324cad7341 <DescriptorArray[4]>
 - layout descriptor: 0x0
 - prototype: 0x39324cad1109 <JSArray[0]>
 - constructor: 0x39324cad0eb9 <JSFunction Array (sfi = 0x39326960a991)>
 - dependent code: 0x3932b48002c1 <Other heap object (WEAK_FIXED_ARRAY_TYPE)>
 - construction counter: 0


I think HOLEY_ELEMENTS is "fast" because


enum ElementsKind : uint8_t {
...
...
  // The "fast" kind for tagged values. Must be second to make it possible to
  // efficiently check maps for this and the PACKED_SMI_ELEMENTS kind
  // together at once.
  PACKED_ELEMENTS,
  HOLEY_ELEMENTS,



And The elements length is 16563 more than the kInitialMaxFastElementArray，whether it can cause type confuse?
Why check **CSA_ASSERT(this, SmiLessThanOrEqual(length, max_length))**？Is it possible to exploit it by Type confuse?

And we can increase the length by adding code to function v2,example:

function v2() {
    const v8 = Symbol || 9007199254740991;
    function v9(v10,v11,v12) {
    }
    const v16 = String();
    const v100 = String();//add 
    const v106 = String();// add
    const v116 = String();// add
    const v17 = Int32Array();
    const v18 = Map();
    const v19 = [];
    const v20 = v18.values();
    function v21(v22,v23,v24,v25,v26) {
    }
    function v28(v29,v30,v31) {
        function v32(v33,v34,v35,v36) {
        }
        let v39 = 0;
        do {
            const v40 = v32();
            function v99() {
            }
        } while (v39 < 8);
    }
    const v41 = Promise();
}
const v46 = ["has",13.37,-9007199254740991,Reflect];
for (let v50 = 64; v50 <= 1337; v50++) {
    v46.push(v50,v2);
}
const v54 = RegExp(v46);
const v55 = v54.exec();

length from 16563 to 0x4fa1 (20385).

### ma...@chromium.org (2019-06-24)

Tebbi, Sigurd regarding CSA assert.

### si...@chromium.org (2019-06-24)

Jakob, you are hacking on this, maybe this is interesting to you?

### jg...@chromium.org (2019-06-24)

I did some digging and I think the CSA_ASSERT may be too conservative. We can probably relax it to check `max_length <= JSArray::kMaxFastArrayLength`, if we're careful to also allow large-object allocations in the following `Allocate` call (which we currently don't).

Findings:

- The meaning of kInitialMaxFastElementArray is still not 100% clear to me. Is it just a fast length check to determine which arrays are guaranteed to fit into new space, or is there more behind it?
- AllocateRegExpResult currently requires new-space allocation since it calls Allocate without the kAllowLargeObjectAllocation flag, and it uses manual allocation folding (which doesn't work with LO space allocs). This means very large regexp results (i.e. with many capture groups) will fail the CSA_ASSERT 
 in debug mode. I was expecting the allocation to also fail in release mode, but for some reason it does not. We'll need to investigate more here. See the next point:
- In release mode, for some reason the allocation of elements in new space does not fail, even though the requested size should be too large for new space.
- I think we should be able to replace the manual code with one of the CSA array allocation functions instead.

What we should look at:

1. Investigate current behavior in release mode. Why does new space allocation succeed even though the requested size is too large?
2. Large-ish regexp results should work, even if elements go into LO space.

### jg...@chromium.org (2019-06-24)

[Empty comment from Monorail migration]

### jg...@chromium.org (2019-06-24)

+ulan we are allocating an object in new space that exceeds kMaxRegularHeapObjectSize.

isolate->heap()->new_space()->Contains(ho): true
isolate->heap()->new_lo_space()->Contains(ho): false
ho.elements().Size(): 247960
kMaxRegularHeapObjectSize: 131072

This happens only when we go through the memory optimizer (which happens when we generate the OptimizedAllocate node in CodeStubAssembler::Allocate). Unlike in other spots, e.g. Heap::AllocateRaw, we don't check against kMaxRegularHeapObjectSize here [0], instead we only ensure that bump pointer allocation succeeds. 

Since kMaxRegularHeapObjectSize is half kPageSize, it's possible for an object to exceed the former yet still fit in the latter. I don't think this bug has security implications since the allocated object still fits in the new space page; but according to ulan@ performance will suffer. Lowering priority.

I will fix AllocateRegExpResult to properly handle large objects, and I opened https://crbug.com/v8/9388 for stricter checks in the memory optimizer.

[0] https://cs.chromium.org/chromium/src/v8/src/compiler/memory-optimizer.cc?l=432&rcl=fe77d58a6a3cd9385454aa0bc29330ec668e293a

### jg...@chromium.org (2019-06-24)

Fix in flight: https://crrev.com/c/1674027

### yn...@gmail.com (2019-06-24)

[Comment Deleted]

### sh...@chromium.org (2019-06-24)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jg...@chromium.org (2019-06-24)

Ulan, please confirm security implications from unintentionally allocating multiple objects in a single LO space page. Feel free to assign back after.

### jd...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/4c156936e8929ae3ba546dcd290987985de925c8

commit 4c156936e8929ae3ba546dcd290987985de925c8
Author: Jakob Gruber <jgruber@chromium.org>
Date: Wed Jun 26 07:50:33 2019

[regexp] Allow JSRegExpResult allocations in large object space

Large regexp results may exceed kMaxRegularHeapObjectSize and must
thus be allocated in large object space.

Drive-by: Rename '%InNewSpace' to '%InYoungGeneration'.

Bug: chromium:976627
Change-Id: I38b5aecb95a95cf2fdbb24d19550cec34361a09d
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1674027
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#62368}

[modify] https://crrev.com/4c156936e8929ae3ba546dcd290987985de925c8/src/builtins/builtins-regexp-gen.cc
[modify] https://crrev.com/4c156936e8929ae3ba546dcd290987985de925c8/src/codegen/code-stub-assembler.cc
[modify] https://crrev.com/4c156936e8929ae3ba546dcd290987985de925c8/src/codegen/code-stub-assembler.h
[modify] https://crrev.com/4c156936e8929ae3ba546dcd290987985de925c8/src/runtime/runtime-test.cc
[modify] https://crrev.com/4c156936e8929ae3ba546dcd290987985de925c8/src/runtime/runtime.h
[modify] https://crrev.com/4c156936e8929ae3ba546dcd290987985de925c8/test/cctest/heap/test-heap.cc
[modify] https://crrev.com/4c156936e8929ae3ba546dcd290987985de925c8/test/mjsunit/mjsunit.status
[add] https://crrev.com/4c156936e8929ae3ba546dcd290987985de925c8/test/mjsunit/regress/regress-976627.js


### jg...@chromium.org (2019-06-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-26)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ul...@chromium.org (2019-06-26)

Re https://crbug.com/chromium/976627#c20: allocating multiple objects in a large page can result in memory corruption, e.g. freeing live objects.
Security_Severity-High seems about right if that can happen.

### sh...@chromium.org (2019-06-26)

[Empty comment from Monorail migration]

### ab...@google.com (2019-06-26)

We should wait until this has been verified in canary first, before reviewing merge.

### jg...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### ab...@google.com (2019-06-27)

jgruber@ - can you confirm if things look good in canary?

### ab...@google.com (2019-06-27)

Is this a fairly safe merge?

### jg...@chromium.org (2019-07-01)

#29: Canary seems to look good: https://crash.corp.google.com/browse?q=product_name%3D%27Chrome_Android%27+AND+product.version%3D%2777.0.3836.3%27+AND+expanded_custom_data.ChromeCrashProto.channel%3D%27canary%27+AND+expanded_custom_data.ChromeCrashProto.ptype%3D%27renderer%27#productname:1000,actionablemagicsignature:100,+magicsignature:100,magicsignature2:50,stablesignature:50,magicsignaturesorted:50.

#30: As far as I know yes.

### ab...@google.com (2019-07-01)

Thanks! Approved for M76, branch:3809

### jg...@chromium.org (2019-07-02)

Merged in https://crrev.com/c/1684176.

### jg...@chromium.org (2019-07-02)

[Empty comment from Monorail migration]

### yn...@gmail.com (2019-07-10)

Can I get a CVE for this issue?

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### yn...@gmail.com (2019-07-16)

This is found with Fuzzilli @sealo

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report!

### yn...@gmail.com (2019-07-18)

Thank you very much, and if this issue can be assigned CVE, please credit yngwei(@yngweijw) of IIE Varas and sakura(@eternalsakura13) of Tecent Xuanwu Lab

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-22)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/976627?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/v8/9388]
[Monorail mergedwith: crbug.com/chromium/969421]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095436)*
