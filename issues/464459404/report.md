# V8: OOB memmove in FixedArray::MoveElements triggered via Array.shift leads to negative-size copy

| Field | Value |
|-------|-------|
| **Issue ID** | [464459404](https://issues.chromium.org/issues/464459404) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | V8 version 14.3.0 (candidate) |
| **Reporter** | am...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2025-11-29 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

1. compile d8 with attached args
2. execute the d8 along with the args for some n number of time for crash

# Problem Description

When calling array.shift() with negative length (which we corrupt via sandbox API) it will lead to negative-ength mem copy crash

in the below method uint length is assigned to length of int datatype which cause the integer overflow, finally calling the dst\_elms->MoveElements(isolate, 0, 1, new\_length, mode); cause the ASAN crash

```
 static V8_INLINE Tagged<Object> RemoveElement(Isolate* isolate,
                                                DirectHandle<JSArray> receiver,
                                                Where remove_position) {
    constexpr ElementsKind kind = KindTraits::Kind;
    static_assert(IsFastElementsKind(kind));
    uint32_t length = static_cast<uint32_t>(Smi::ToInt(receiver->length()));
    if (length == 0) return ReadOnlyRoots(isolate).undefined_value();

    if constexpr (IsSmiOrObjectElementsKind(kind)) {
      JSObject::EnsureWritableFastElements(isolate, receiver);
    }

    DCHECK_GT(length, 0);
    int new_length = length - 1;
    int remove_index = remove_position == AT_START ? 0 : new_length;
    Tagged<Object> result;
    Tagged<JSArray> raw_receiver = *receiver;
    if constexpr (IsDoubleElementsKind(kind)) {
      result = *Subclass::GetImpl(isolate, raw_receiver->elements(),
                                  InternalIndex(remove_index));
      raw_receiver = *receiver;
    } else {
      result = Cast<BackingStore>(raw_receiver->elements())->get(remove_index);
    }
    // The result is now unhandlified, so we can't allocate anymore.
    DisallowGarbageCollection no_gc;
    if (V8_UNLIKELY(new_length == 0)) {
      raw_receiver->initialize_elements();
    } else {
      Tagged<BackingStore> dst_elms =
          Cast<BackingStore>(raw_receiver->elements());
      if (remove_position == AT_START) {
        if (V8_UNLIKELY(new_length > JSArray::kMaxCopyElements &&
                        isolate->heap()->CanMoveObjectStart(dst_elms))) {
          dst_elms = Cast<BackingStore>(
              isolate->heap()->LeftTrimFixedArray(dst_elms, 1));
          raw_receiver->set_elements(dst_elms);
        } else {
          WriteBarrierMode mode = IsFastNumberElementsKind(KindTraits::Kind)
                                      ? SKIP_WRITE_BARRIER
                                      : UPDATE_WRITE_BARRIER;
          dst_elms->MoveElements(isolate, 0, 1, new_length, mode);
          dst_elms->FillWithHoles(new_length, new_length + 1);
          Subclass::DecreaseLength(isolate, dst_elms, length, new_length);
        }
      } else {
        dst_elms->FillWithHoles(new_length, new_length + 1);
        Subclass::DecreaseLength(isolate, dst_elms, length, new_length);
      }
    }
    raw_receiver->set_length(Smi::FromInt(new_length));

    if (IsHoleyElementsKind(kind) && IsTheHole(result, isolate)) {
      return ReadOnlyRoots(isolate).undefined_value();
    }
    return result;
  }

```
# Summary

V8: OOB memmove in FixedArray::MoveElements triggered via Array.shift leads to negative-size copy

# Custom Questions

#### Crash state:

```
# Ignoring debug check failure in ../../src/objects/fixed-array-inl.h, line 229: len >= 0 (-2 vs. 0)
# Ignoring debug check failure in ../../src/heap/heap.cc, line 2101: dst_slot < TSlot(dst_slot + len)
# Ignoring debug check failure in ../../src/heap/heap.cc, line 2102: src_slot < src_slot + len
# Ignoring debug check failure in ../../src/heap/heap.cc, line 2066: len > 0 (-2 vs. 0)
=================================================================
==30218==ERROR: AddressSanitizer: negative-size-param: (size=-8)
    #0 0x5555557c7e67 in __asan_memmove (/home/basha/Desktop/v8fuzz/v8/out/d8_symbol_asan_debug_fuzz/d8+0x273e67) (BuildId: 460666f2b7d38937)
    #1 0x7fffecd5edfb in v8::internal::MemMove(void*, void const*, unsigned long) src/utils/memcopy.h:236:7
    #2 0x7fffecd5e5dd in void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int)::operator()(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int) const src/heap/heap.cc:2131:5
    #3 0x7fffecc61d9b in void v8::internal::(anonymous namespace)::CopyOrMoveRangeImpl<v8::internal::CompressedObjectSlot, void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int), void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int)>(v8::internal::Heap*, v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode, void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int), void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int)) src/heap/heap.cc:2073:5
    #4 0x7fffecd18451 in void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode) src/heap/heap.cc:2133:3
    #5 0x7fffedb62baa in v8::internal::TaggedArrayBase<v8::internal::FixedArray, v8::internal::TaggedArrayShape, v8::internal::HeapObjectLayout>::MoveElements(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::FixedArray>, int, v8::internal::Tagged<v8::internal::FixedArray>, int, int, v8::internal::WriteBarrierMode) src/objects/fixed-array-inl.h:238:20
    #6 0x7fffedb6262c in v8::internal::FixedArray::MoveElements(v8::internal::Isolate*, int, int, int, v8::internal::WriteBarrierMode) src/objects/fixed-array-inl.h:424:3
    #7 0x7fffed826153 in v8::internal::(anonymous namespace)::FastElementsAccessor<v8::internal::(anonymous namespace)::FastHoleySmiElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)1>>::RemoveElement(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, v8::internal::(anonymous namespace)::Where) src/objects/elements.cc:2652:21
    #8 0x7fffed826478 in v8::internal::(anonymous namespace)::FastElementsAccessor<v8::internal::(anonymous namespace)::FastHoleySmiElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)1>>::ShiftImpl(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>) src/objects/elements.cc:2389:12
    #9 0x7fffed8198fa in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastHoleySmiElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)1>>::Shift(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>) src/objects/elements.cc:821:12
    #10 0x7fffeba1edb8 in v8::internal::Builtin_Impl_ArrayShift(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-array.cc:700:45
    #11 0x7fffeba1e4cd in v8::internal::Builtin_ArrayShift(int, unsigned long*, v8::internal::Isolate*) src/builtins/builtins-array.cc:694:1
    #12 0x7bffb92ea13c  (<unknown module>)
    #13 0x7bffb8da61b5  (<unknown module>)
    #14 0x7bffb8d988a6  (<unknown module>)
    #15 0x7bffb8d985ea  (<unknown module>)
    #16 0x7fffec417386 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:212:12
    #17 0x7fffec40f934 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #18 0x7fffec410866 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #19 0x7fffeb6b9860 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1953:7
    #20 0x7fffeb6b90cd in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:1917:10
    #21 0x55555589b220 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1044:44
    #22 0x5555558d462b in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5543:10
    #23 0x5555558e05a0 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6503:37
    #24 0x5555558dfe3e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6411:18
    #25 0x5555558e2c7b in v8::Shell::Main(int, char**) src/d8/d8.cc:7301:18
    #26 0x5555558e36d1 in main src/d8/d8.cc:7393:43
    #27 0x7fffde42a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #28 0x7fffde42a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #29 0x555555726309 in _start (/home/basha/Desktop/v8fuzz/v8/out/d8_symbol_asan_debug_fuzz/d8+0x1d2309) (BuildId: 460666f2b7d38937)

Address 0x7abe0088001c is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: negative-size-param (/home/basha/Desktop/v8fuzz/v8/out/d8_symbol_asan_debug_fuzz/d8+0x273e67) (BuildId: 460666f2b7d38937) in __asan_memmove
AddressSanitizer: CHECK failed: asan_poisoning.cpp:249 "((beg)) < ((end))" (0x7abe0088001c, 0x7abe00880014) (tid=30218)
    #0 0x5555557d4cd1 in __asan::CheckUnwind() asan_rtl.cpp
    #1 0x5555557efc22 in __sanitizer::CheckFailed(char const*, int, char const*, unsigned long long, unsigned long long) sanitizer_termination.cpp
    #2 0x5555557cd0cd in __asan_region_is_poisoned (/home/basha/Desktop/v8fuzz/v8/out/d8_symbol_asan_debug_fuzz/d8+0x2790cd) (BuildId: 460666f2b7d38937)
    #3 0x5555557c7fa7 in __asan_memmove (/home/basha/Desktop/v8fuzz/v8/out/d8_symbol_asan_debug_fuzz/d8+0x273fa7) (BuildId: 460666f2b7d38937)
    #4 0x7fffecd5edfb in v8::internal::MemMove(void*, void const*, unsigned long) src/utils/memcopy.h:236:7
    #5 0x7fffecd5e5dd in void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int)::operator()(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int) const src/heap/heap.cc:2131:5
    #6 0x7fffecc61d9b in void v8::internal::(anonymous namespace)::CopyOrMoveRangeImpl<v8::internal::CompressedObjectSlot, void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int), void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int)>(v8::internal::Heap*, v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode, void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int), void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode)::'lambda'(v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int)) src/heap/heap.cc:2073:5
    #7 0x7fffecd18451 in void v8::internal::Heap::MoveRange<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot, int, v8::internal::WriteBarrierMode) src/heap/heap.cc:2133:3
    #8 0x7fffedb62baa in v8::internal::TaggedArrayBase<v8::internal::FixedArray, v8::internal::TaggedArrayShape, v8::internal::HeapObjectLayout>::MoveElements(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::FixedArray>, int, v8::internal::Tagged<v8::internal::FixedArray>, int, int, v8::internal::WriteBarrierMode) src/objects/fixed-array-inl.h:238:20
    #9 0x7fffedb6262c in v8::internal::FixedArray::MoveElements(v8::internal::Isolate*, int, int, int, v8::internal::WriteBarrierMode) src/objects/fixed-array-inl.h:424:3
    #10 0x7fffed826153 in v8::internal::(anonymous namespace)::FastElementsAccessor<v8::internal::(anonymous namespace)::FastHoleySmiElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)1>>::RemoveElement(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, v8::internal::(anonymous namespace)::Where) src/objects/elements.cc:2652:21
    #11 0x7fffed826478 in v8::internal::(anonymous namespace)::FastElementsAccessor<v8::internal::(anonymous namespace)::FastHoleySmiElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)1>>::ShiftImpl(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>) src/objects/elements.cc:2389:12
    #12 0x7fffed8198fa in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastHoleySmiElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)1>>::Shift(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>) src/objects/elements.cc:821:12
    #13 0x7fffeba1edb8 in v8::internal::Builtin_Impl_ArrayShift(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-array.cc:700:45
    #14 0x7fffeba1e4cd in v8::internal::Builtin_ArrayShift(int, unsigned long*, v8::internal::Isolate*) src/builtins/builtins-array.cc:694:1
    #15 0x7bffb92ea13c  (<unknown module>)

```
#### Reporter credit:

Ameen Basha M K

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.2 KB)
- [Sat Nov 29 2025 18:29:55 GMT+0530 (India Standard Time).png](attachments/Sat Nov 29 2025 18_29_55 GMT+0530 (India Standard Time).png) (image/png, 164.9 KB)
- [poc.js](attachments/poc.js) (text/javascript, 1.2 KB)

## Timeline

### am...@gmail.com (2025-11-29)

i have executed the poc some 10 times, in which 6 times i got this crash, have attached the poc proof image

if the issue is not reproduced at your end, kindly re run it in loop of some 10 times

### am...@gmail.com (2025-11-29)

Build gn args:

```
gn gen out/d8_asan_fuzz --args='is_debug=false is_asan=true v8_enable_sandbox=true v8_enable_memory_corruption_api=true dcheck_always_on=false target_cpu="x64" v8_static_library=true v8_fuzzilli=false'

```

D8 Args:

```
d8 --fuzzing --sandbox-fuzzing --single-threaded --allow-natives-syntax --expose-gc poc.js

```

V8 Commit Hash: bc73e539df39434ef6c8ae3f0403b03c9c94c00d

### ar...@chromium.org (2025-12-01)

Thanks!
Assigning to the V8 Shepherd for further triage.

I have set a provisional Severity of High (S1) and a provisional Found In of the current Extended Stable, as this appears to be a V8 memory corruption issue.

### cl...@appspot.gserviceaccount.com (2025-12-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6475760017539072.

### am...@gmail.com (2025-12-01)

Missed to include a v8_enable_memory_corruption_api=true flag in args.gn i have updated the build args in #comment 3 kindly check now


Also in the clusterfuzz seems some other poc is uploaded for reproduce kindly check and update my poc for reproduce

### cl...@appspot.gserviceaccount.com (2025-12-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4865637310464000.

### ar...@google.com (2025-12-01)

Thanks for noticing! I uploaded a new test case for linux\_asan\_chrome\_v8\_sandbox\_testing, so that one can use the `sandbox.MemoryView` API

### ch...@google.com (2025-12-01)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-12-01)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### am...@gmail.com (2025-12-01)

If CF not able to reproduce, kindly try with below args:

```
is_debug = false
is_asan = true
v8_fuzzilli = true
sanitizer_coverage_flags = "trace-pc-guard"
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
v8_enable_pointer_compression = true
is_component_build = false
v8_use_external_startup_data = false
symbol_level = 1
treat_warnings_as_errors = false
dcheck_always_on = false

```

This is the build from which i got the crash by running it some 10 times, out of which 6 is crash, Ref [Comment #2](https://issues.chromium.org/issues/464459404#comment2)

Note: args in comment 3 will also work there is no flag difference that is related to this crash, but for the above flags i got the crash bit quicker for reproduce

### cl...@chromium.org (2025-12-01)

I can reproduce on ToT, but with a much lower rate than 6/10. It's more like 1/20 on my machine. But in any case, this is good enough to run a bisection.

`(for i in $(seq 100); do out/tmp/d8 --fuzzing --sandbox-fuzzing --single-threaded --allow-natives-syntax --expose-gc poc.js&; done; wait) |& grep negative-size`

### cl...@chromium.org (2025-12-01)

This reproduces since at least a year, so bisection is not helpful.

### am...@gmail.com (2025-12-01)

Bisect:

https://chromium.googlesource.com/v8/v8/+/061e2a9b2b1cf70cb1c18ea6425219e8bd592903%5E%21/src/elements.cc
Commit: 061e2a9b2b1cf70cb1c18ea6425219e8bd592903
Done on: 18 Sep 2015

This is the commit that introduce this method with vulnerable snippet of assigning uint32_t to int

### cl...@chromium.org (2025-12-01)

The problem seems to be this read of the in-sandbox `length`, and the conversions between `uint32_t length` and `int new_length` also looks fishy:

```
  static V8_INLINE Tagged<Object> RemoveElement(Isolate* isolate,
                                                DirectHandle<JSArray> receiver,
                                                Where remove_position) {
    constexpr ElementsKind kind = KindTraits::Kind;
    static_assert(IsFastElementsKind(kind));
    uint32_t length = static_cast<uint32_t>(Smi::ToInt(receiver->length()));
    if (length == 0) return ReadOnlyRoots(isolate).undefined_value();

    if constexpr (IsSmiOrObjectElementsKind(kind)) {
      JSObject::EnsureWritableFastElements(isolate, receiver);
    }

    DCHECK_GT(length, 0);
    int new_length = length - 1;

```

(<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/elements.cc;l=2608;drc=1900c13398549f2923fe0f4822c6d695f77af4c6>)

Toon, a lot of this code is from you, can you PTAL or find a better owner?

### cl...@chromium.org (2025-12-01)

Maybe a fix would already be to change this to

```
    int length = Smi::ToInt(receiver->length());
    if (length < 1) return ReadOnlyRoots(isolate).undefined_value();

```

But maybe we should also check for similar patterns in surrounding code.

### cl...@chromium.org (2025-12-01)

Oh, didn't see [comment #14](https://issues.chromium.org/issues/464459404#comment14) yet. +cbruni

### is...@chromium.org (2025-12-01)

Thank you for the report!

I think we should finally address [issue 441221573](https://issues.chromium.org/issues/441221573).

### dx...@google.com (2025-12-03)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7217668>

[elements] Enable sign conversion warnings in elements.cc

---


Expand for full commit details
```
     
    The change is mostly mechanical: 
     - use uint32_t instead of int for FixedArray indices, 
     - change signatures of respective functions to use uint32_t indices, 
       length and capacity, 
     - remove unnecessary static casts (uint32_t -> uint32_t), 
     - add static casts to int/uint32_t where necessary to access code 
       that wasn't migrated yet. 
     
    Fixed: 464459404 
    Bug: 441221573 
    Change-Id: I716d9835147e1c1bb849a1c98d699f4918eac48e 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7217668 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104091}

```

---

Files:

- M `src/builtins/builtins-utils.h`
- M `src/execution/arguments.h`
- M `src/heap/factory-base.cc`
- M `src/heap/factory-base.h`
- M `src/heap/factory.cc`
- M `src/heap/factory.h`
- M `src/heap/heap.cc`
- M `src/heap/heap.h`
- M `src/objects/arguments-inl.h`
- M `src/objects/arguments.h`
- M `src/objects/dictionary-inl.h`
- M `src/objects/elements-kind.h`
- M `src/objects/elements.cc`
- M `src/objects/elements.h`
- M `src/objects/fixed-array-inl.h`
- M `src/objects/fixed-array.cc`
- M `src/objects/fixed-array.h`
- M `src/objects/internal-index.h`
- M `src/objects/intl-objects.cc`
- M `src/objects/js-array.h`
- M `src/objects/js-objects.cc`
- M `src/objects/js-objects.h`
- M `src/objects/objects.cc`
- M `src/objects/slots.h`
- M `src/objects/smi.h`

---

Hash: [07576e5c96c664c421fcf6fb0dfdb940622f8aa3](https://chromiumdash.appspot.com/commit/07576e5c96c664c421fcf6fb0dfdb940622f8aa3)  

Date: Wed Dec 3 15:28:35 2025


---

### dx...@google.com (2025-12-08)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7237994>

[elements] Remove bad DCHECK in CopyDictionaryToDoubleElements(..)

---


Expand for full commit details
```
     
    ... added in a recent CL: https://crrev.com/c/7217668. 
     
    Drive-by: cleanup elements printing: 
     - print NumberDictionary::max_number_key only in full mode (with 
       number of elements, number of deleted element, capacity, etc.), 
     - fix elements backing store detection in JSObject::PrintElements(). 
     
    Fixed: 465843880 
    Bug: 464459404 
    Bug: 441221573 
    Change-Id: I023d650888bde04f5d516ced07941647efb6e9a3 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7237994 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104181}

```

---

Files:

- M `src/diagnostics/objects-printer.cc`
- M `src/objects/elements.cc`

---

Hash: [11ce8e306be20a24806efab04484952a229c1d77](https://chromiumdash.appspot.com/commit/11ce8e306be20a24806efab04484952a229c1d77)  

Date: Mon Dec 8 16:20:15 2025


---

### sp...@google.com (2025-12-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 sandbox escape


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### am...@gmail.com (2025-12-11)

Hi Team, Thanks for the bounty

i have mentioned the bisection details in the comment14
https://issues.chromium.org/issues/464459404#comment14


But the bisection bonus is not included in the bounty,
kindly check on the same

### ch...@google.com (2026-03-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@gmail.com (2026-03-12)

Team Seems the CVE Details are not updated, Kindly share the CVE Details for this issue

## Bounty Award

> V8 sandbox escape

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/464459404)*
