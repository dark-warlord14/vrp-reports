# V8 Sandbox Bypass: double-free in HandleScope::Extend via concurrent JS stack printing from MainMarkingVisitor and ConcurrentMarkingVisitor

| Field | Value |
|-------|-------|
| **Issue ID** | [501136000](https://issues.chromium.org/issues/501136000) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gu...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2026-04-10 |
| **Bounty** | $5,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

Once major marking observes a corrupted heap-object map pointer and the object is classified as unexpected `FreeSpace` or `Filler`, both the main marker and a background concurrent marker can enter `PushStackTraceAndDie`. That reporting path prints a JS stack and allocates handles. The background marking worker, however, is only under `SetCurrentIsolateScope`, which explicitly does not enter the isolate. As a result, two threads can concurrently mutate `HandleScopeImplementer::blocks_` and race in `DetachableVector::Resize()`, freeing the same backing store twice.

### Root cause analysis

The root cause is that a background GC worker reaches a crash-reporting path that assumes normal isolate/thread state and mutates shared handle-scope storage without synchronization.

The background major-marking worker is not isolate-entered. It only installs a lightweight "current isolate" scope:

```
// src/execution/isolate.h
// Set the current isolate for the thread *without* entering the isolate. Used
// e.g. by background GC threads to be able to access pointer tables.
// This subsumes a `PtrComprCageAccessScope` which is needed in the same
// contexts in order to be able to access on-heap objects.
class V8_NODISCARD SetCurrentIsolateScope final {
 public:
  explicit inline SetCurrentIsolateScope(Isolate* isolate);

  inline ~SetCurrentIsolateScope();

 private:
  V8_NO_UNIQUE_ADDRESS PtrComprCageAccessScope ptr_compr_cage_access_scope_;
  Isolate* const previous_isolate_;
};

```
```
// src/heap/concurrent-marking.cc
class ConcurrentMarking::JobTaskMajor : public v8::JobTask {
 public:
  JobTaskMajor(ConcurrentMarking* concurrent_marking,
               unsigned mark_compact_epoch,
               base::EnumSet<CodeFlushMode> code_flush_mode,
               bool should_keep_ages_unchanged)
      : concurrent_marking_(concurrent_marking),
        mark_compact_epoch_(mark_compact_epoch),
        code_flush_mode_(code_flush_mode),
        should_keep_ages_unchanged_(should_keep_ages_unchanged),
        trace_id_(reinterpret_cast<uint64_t>(concurrent_marking) ^
                  concurrent_marking->heap_->tracer()->CurrentEpoch()) {}

  ~JobTaskMajor() override = default;
  JobTaskMajor(const JobTaskMajor&) = delete;
  JobTaskMajor& operator=(const JobTaskMajor&) = delete;

  // v8::JobTask overrides.
  void Run(JobDelegate* delegate) override {
    // Set the current isolate such that trusted pointer tables etc are
    // available and the cage base is set correctly for multi-cage mode.
    SetCurrentIsolateScope isolate_scope(concurrent_marking_->heap_->isolate());

    if (delegate->IsJoiningThread()) {
      // TRACE_GC is not needed here because the caller opens the right scope.
      concurrent_marking_->RunMajor(delegate, code_flush_mode_,
                                    mark_compact_epoch_,
                                    should_keep_ages_unchanged_);
    } else {
      TRACE_GC_EPOCH_WITH_FLOW(concurrent_marking_->heap_->tracer(),
                               GCTracer::Scope::MC_BACKGROUND_MARKING,
                               ThreadKind::kBackground, trace_id_,
                               TRACE_EVENT_FLAG_FLOW_IN);
      concurrent_marking_->RunMajor(delegate, code_flush_mode_,
                                    mark_compact_epoch_,
                                    should_keep_ages_unchanged_);
    }
  }

  size_t GetMaxConcurrency(size_t worker_count) const override {
    return concurrent_marking_->GetMajorMaxConcurrency(worker_count);
  }

  uint64_t trace_id() const { return trace_id_; }

 private:
  ConcurrentMarking* concurrent_marking_;
  const unsigned mark_compact_epoch_;
  base::EnumSet<CodeFlushMode> code_flush_mode_;
  const bool should_keep_ages_unchanged_;
  const uint64_t trace_id_;
};

```

This scope is enough for pointer-table and cage-base access during background marking, but it is explicitly not a real isolate entry. It makes later code assume it can perform general stack printing and handle allocation from that context.

The corrupted map pointer reaches the diagnostic branch through generic map visitation:

```
// src/heap/marking-visitor.h
void VisitMapPointer(Tagged<HeapObject> host) final {
  Tagged<Map> map = host->map(ObjectVisitorWithCageBases::cage_base());
  ProcessStrongHeapObject(host, host->map_slot(), map);
}

```
```
// src/heap/marking-visitor-inl.h
template <typename THeapObjectSlot>
void MarkingVisitorBase<ConcreteVisitor>::ProcessStrongHeapObject(
    Tagged<HeapObject> host, THeapObjectSlot slot,
    Tagged<HeapObject> heap_object) {
  SynchronizePageAccess(heap_object);
  const auto target_worklist =
      MarkingHelper::ShouldMarkObject(heap_, heap_object);
  if (!target_worklist) {
    return;
  }
  // TODO(chromium:1495151): Remove after diagnosing.
  if (V8_UNLIKELY(!MemoryChunk::FromHeapObject(heap_object)->IsMarking() &&
                  IsFreeSpaceOrFiller(
                      heap_object, ObjectVisitorWithCageBases::cage_base()))) {
    heap_->isolate()->PushStackTraceAndDie(
        reinterpret_cast<void*>(host->map().ptr()),
        reinterpret_cast<void*>(host->address()),
        reinterpret_cast<void*>(slot.address()),
        reinterpret_cast<void*>(
            BasePage::FromHeapObject(heap_->isolate(), heap_object)
                ->owner()
                ->identity()));
  }
  MarkObject(host, heap_object, target_worklist.value());
  concrete_visitor()->RecordSlot(host, slot, heap_object);
}

```

A temporary diagnostic check inside heap marking routes the corruption into `PushStackTraceAndDie`. That reporting helper is not GC-worker-safe, but it is called from both `MainMarkingVisitor` and `ConcurrentMarkingVisitor`.

```
// src/execution/isolate.cc
void Isolate::PushStackTraceAndDie(void* ptr1, void* ptr2, void* ptr3,
                                   void* ptr4, void* ptr5, void* ptr6) {
  StackTraceFailureMessage message(this,
                                   StackTraceFailureMessage::kIncludeStackTrace,
                                   {ptr1, ptr2, ptr3, ptr4, ptr5, ptr6});
  message.Print();
  base::OS::Abort();
}

StackTraceFailureMessage::StackTraceFailureMessage(
    Isolate* isolate, StackTraceFailureMessage::StackTraceMode mode,
    const Address* ptrs, size_t ptrs_count)
    : isolate_(isolate) {
  size_t ptrs_size = std::min(arraysize(ptrs_), ptrs_count);
  std::copy(ptrs, ptrs + ptrs_size, &ptrs_[0]);

  if (mode == kIncludeStackTrace) {
    const size_t buffer_length = arraysize(js_stack_trace_);
    FixedStringAllocator fixed(&js_stack_trace_[0], buffer_length - 1);
    StringStream accumulator(&fixed, StringStream::kPrintObjectConcise);
    isolate_->PrintStack(&accumulator, Isolate::kPrintStackVerbose);
    const size_t code_objects_length = arraysize(code_objects_);
    size_t i = 0;
    StackFrameIterator it(isolate_);
    for (; !it.done() && i < code_objects_length; it.Advance()) {
      code_objects_[i++] = it.frame()->unchecked_code().ptr();
    }
  }
}

```

`PushStackTraceAndDie` constructs a `StackTraceFailureMessage`, which immediately asks the isolate to print a verbose JS stack.

```
// src/handles/handles.cc
Address* HandleScope::Extend(Isolate* isolate) {
  HandleScopeData* current = isolate->handle_scope_data();

  Address* result = current->next;

  DCHECK(result == current->limit);
  // Make sure there's at least one scope on the stack and that the
  // top of the scope stack isn't a barrier.
  if (!Utils::ApiCheck(current->level != current->sealed_level,
                       "v8::HandleScope::CreateHandle()",
                       "Cannot create a handle without a HandleScope")) {
    return nullptr;
  }
  HandleScopeImplementer* impl = isolate->handle_scope_implementer();
  // If there's more room in the last block, we use that. This is used
  // for fast creation of scopes after scope barriers.
  if (!impl->blocks()->empty()) {
    Address* limit = &impl->blocks()->back()[kHandleBlockSize];
    if (current->limit != limit) {
      current->limit = limit;
      DCHECK_LT(limit - current->next, kHandleBlockSize);
    }
  }

  // If we still haven't found a slot for the handle, we extend the
  // current handle scope by allocating a new handle block.
  if (result == current->limit) {
    // If there's a spare block, use it for growing the current scope.
    result = impl->GetSpareOrNewBlock();
    // Add the extension to the global list of blocks, but count the
    // extension as part of the current scope.
    impl->blocks()->push_back(result);
    current->limit = &result[kHandleBlockSize];
  }

  return result;
}

```

Printing the stack allocates handles. That eventually reaches `HandleScope::Extend`, which appends to the isolate-global `HandleScopeImplementer::blocks_` vector.

```
// src/utils/detachable-vector.h
template <typename T>
class DetachableVector : public DetachableVectorBase {
 public:
  void push_back(const T& value) {
    if (size_ == capacity_) {
      size_t new_capacity = std::max(kMinimumCapacity, 2 * capacity_);
      Resize(new_capacity);
    }

    data()[size_] = value;
    ++size_;
  }

 private:
  void Resize(size_t new_capacity) {
    DCHECK_LE(size_, new_capacity);
    T* new_data_ = new T[new_capacity];

    std::copy(data(), data() + size_, new_data_);
    delete[] data();

    data_ = new_data_;
    capacity_ = new_capacity;
  }
};

```

If two threads enter stack printing at the same time, both can call `HandleScope::Extend`, both can append to `blocks_`, and both can race in `DetachableVector::Resize`. Since `Resize` copies the old array and then unconditionally `delete[]`s the previous `data_`, concurrent callers can free the same backing store twice.

So the root cause of the ASan `double-free` is:

1. A corrupted heap-object map pointer is consumed by generic marking code.
2. The temporary diagnostic branch in `ProcessStrongHeapObject` calls `PushStackTraceAndDie`.
3. That reporting path performs JS stack printing and handle allocation.
4. A background GC worker does this while only under `SetCurrentIsolateScope`, not a real isolate entry.
5. Main-thread and background-thread stack printing concurrently mutate the same `HandleScopeImplementer::blocks_` storage.
6. `DetachableVector::Resize` frees the same backing store twice, producing the observed ASan `attempting double-free`.

### VERSION

tested v8 git commit : `4abbe26c5ce6f22783c4f2370ffd2a136c014d97`

v8 git commit that introduces this bug:

- “Introduced the diagnostic path relevant to this ASan”: d2aa2bae7080834052c9fc97ba12ca3bb5923278 (parent of suggesting patch)
- “Introduced the background-major-GC execution context that makes this manifestation more reachable”: 19d1cde7ffe6c6e5c6908496f5b575407c9b49e5

## REPRODUCTION CASE

gn args out/x64.fuzzilli\_sbx:

```
is_debug = false
target_cpu = "x64"
v8_fuzzilli = true
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
dcheck_always_on = false
sanitizer_coverage_flags = "trace-pc-guard"
symbol_level = 1
is_clang = true
is_asan = true

```

Execute:

```
for i in $(seq 1 1000); do                                            
  out/x64.fuzzilli_sbx/d8 \
    --expose-gc \
    --allow-natives-syntax \
    --fuzzing \
    --sandbox-fuzzing \
    min_jstag_bg_gc_asan_v4.js \
    > /tmp/jstag-bg-marker-$i.log 2>&1

  if rg -q 'sandbox violation detected' /tmp/jstag-bg-marker-$i.log; then
    cat /tmp/jstag-bg-marker-$i.log
    break
  fi
done

```

Result:

```
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: anonymous shmem with 1024580 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7eb500000000,0x7fb500000000)
JSTag map word: 0x59f -> 0x59f
=================================================================
==510645==ERROR: AddressSanitizer: attempting double-free on 0x751f64be28a0 in thread T42 (V8 DefaultWorke):
    #0 0x5cc1c283ea3d in operator delete[](void*) (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x149ea3d) (BuildId: 29b1bc3e5e38cafa)
    #1 0x5cc1c3132dbe in v8::internal::HandleScope::Extend(v8::internal::Isolate*) src/utils/detachable-vector.h:94:5
    #2 0x5cc1c305dc9b in v8::internal::JavaScriptFrame::Print(v8::internal::StringStream*, v8::internal::StackFrame::PrintMode, int) const src/handles/handles-inl.h:299:14
    #3 0x5cc1c30712ac in v8::internal::Isolate::PrintStack(v8::internal::StringStream*, v8::internal::Isolate::PrintStackMode) src/execution/isolate.cc:2091:17
    #4 0x5cc1c3072226 in v8::internal::StackTraceFailureMessage::StackTraceFailureMessage(v8::internal::Isolate*, v8::internal::StackTraceFailureMessage::StackTraceMode, unsigned long const*, unsigned long) src/execution/isolate.cc:784:15
    #5 0x5cc1c30717b4 in v8::internal::Isolate::PushStackTraceAndDie(void*, void*, void*, void*, void*, void*) src/execution/isolate.cc:709:28
    #6 0x5cc1c31a893b in void v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor>::ProcessStrongHeapObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) src/heap/marking-visitor-inl.h:87:23
    #7 0x5cc1c315c7e2 in v8::internal::ConcurrentMarking::RunMajor(v8::JobDelegate*, v8::base::EnumSet<v8::internal::CodeFlushMode, int>, unsigned int, bool) src/heap/marking-visitor-inl.h:173:7
    #8 0x5cc1c321581a in v8::internal::ConcurrentMarking::JobTaskMajor::Run(v8::JobDelegate*) src/heap/concurrent-marking.cc:260:28
    #9 0x5cc1c891de14 in v8::platform::DefaultJobWorker::Run() src/libplatform/default-job.h:147:18
    #10 0x5cc1c892f3fa in v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run() src/libplatform/default-worker-threads-task-runner.cc:95:25
    #11 0x5cc1c890f7dc in v8::base::ThreadEntry(void*) src/base/platform/platform-posix.cc:1307:11
    #12 0x5cc1c2802c46 in asan_thread_start(void*) asan_interceptors.cpp

0x751f64be28a0 is located 0 bytes inside of 64-byte region [0x751f64be28a0,0x751f64be28e0)
freed by thread T0 here:
    #0 0x5cc1c283ea3d in operator delete[](void*) (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x149ea3d) (BuildId: 29b1bc3e5e38cafa)
    #1 0x5cc1c3132dbe in v8::internal::HandleScope::Extend(v8::internal::Isolate*) src/utils/detachable-vector.h:94:5
    #2 0x5cc1c305dc9b in v8::internal::JavaScriptFrame::Print(v8::internal::StringStream*, v8::internal::StackFrame::PrintMode, int) const src/handles/handles-inl.h:299:14
    #3 0x5cc1c30712ac in v8::internal::Isolate::PrintStack(v8::internal::StringStream*, v8::internal::Isolate::PrintStackMode) src/execution/isolate.cc:2091:17
    #4 0x5cc1c3072226 in v8::internal::StackTraceFailureMessage::StackTraceFailureMessage(v8::internal::Isolate*, v8::internal::StackTraceFailureMessage::StackTraceMode, unsigned long const*, unsigned long) src/execution/isolate.cc:784:15
    #5 0x5cc1c30717b4 in v8::internal::Isolate::PushStackTraceAndDie(void*, void*, void*, void*, void*, void*) src/execution/isolate.cc:709:28
    #6 0x5cc1c343d78b in void v8::internal::MarkingVisitorBase<v8::internal::MainMarkingVisitor>::ProcessStrongHeapObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) src/heap/marking-visitor-inl.h:87:23
    #7 0x5cc1c342e9c2 in std::__Cr::pair<unsigned long, unsigned long> v8::internal::MarkCompactCollector::ProcessMarkingWorklist<(v8::internal::MarkCompactCollector::MarkingWorklistProcessingMode)0>(v8::base::TimeDelta, unsigned long) src/heap/marking-visitor-inl.h:173:7
    #8 0x5cc1c33e540c in v8::internal::MarkCompactCollector::MarkTransitiveClosureFixpoint()::$_0::operator()() const src/heap/mark-compact.cc:2245:9
    #9 0x5cc1c33e404f in v8::internal::MarkCompactCollector::MarkTransitiveClosureFixpoint() src/heap/mark-compact.cc:2213:35
    #10 0x5cc1c33bd1a3 in v8::internal::MarkCompactCollector::MarkLiveObjects() src/heap/mark-compact.cc:2622:5
    #11 0x5cc1c33ba7f1 in v8::internal::MarkCompactCollector::CollectGarbage() src/heap/mark-compact.cc:526:3
    #12 0x5cc1c33408e3 in v8::internal::Heap::MarkCompact() src/heap/heap.cc:2637:29
    #13 0x5cc1c333e67f in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) src/heap/heap.cc:2369:5
    #14 0x5cc1c3383286 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck)::$_1::operator()() const src/heap/heap.cc:1637:7
    #15 0x5cc1c3382832 in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck)::$_1>(heap::base::Stack*, void*, void const*) src/heap/base/stack.h:182:5
    #16 0x5cc1c5ab9802 in PushAllRegistersAndIterateStack push_registers_asm.cc
    #17 0x5cc1c3332161 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck) src/heap/base/stack.h:78:7
    #18 0x5cc1c30fe2b8 in v8::internal::(anonymous namespace)::InvokeGC(v8::Isolate*, v8::internal::(anonymous namespace)::GCOptions) src/extensions/gc-extension.cc:209:17
    #19 0x5cc1c30fd1ad in v8::internal::GCExtension::GC(v8::FunctionCallbackInfo<v8::Value> const&) src/extensions/gc-extension.cc:304:7
    #20 0x5cc1c8663663 in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc
    #21 0x5cc1c8661901 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #22 0x5cc1c866208e in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #23 0x5cc1c8828797 in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #24 0x5cc1c8661901 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #25 0x5cc1c866208e in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #26 0x5cc1c8828797 in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #27 0x5cc1c8661901 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #28 0x5cc1c866208e in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #29 0x5cc1c8828797 in Builtins_ConstructHandler setup-isolate-deserialize.cc

previously allocated by thread T0 here:
    #0 0x5cc1c283e21d in operator new[](unsigned long) (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x149e21d) (BuildId: 29b1bc3e5e38cafa)
    #1 0x5cc1c3132d4a in v8::internal::HandleScope::Extend(v8::internal::Isolate*) src/utils/detachable-vector.h:91:20
    #2 0x5cc1c46d6a43 in int v8::internal::Deserializer<v8::internal::Isolate>::ReadReadOnlyHeapRef<v8::internal::SlotAccessorForHandle<v8::internal::Isolate>>(unsigned char, v8::internal::SlotAccessorForHandle<v8::internal::Isolate>) src/handles/handles-inl.h:299:14
    #3 0x5cc1c46c0d46 in v8::internal::Deserializer<v8::internal::Isolate>::ReadObject() src/snapshot/deserializer.cc:756:12
    #4 0x5cc1c4717ca8 in v8::internal::SharedHeapDeserializer::DeserializeStringTable() src/snapshot/shared-heap-deserializer.cc:49:51
    #5 0x5cc1c4717895 in v8::internal::SharedHeapDeserializer::DeserializeIntoIsolate() src/snapshot/shared-heap-deserializer.cc:27:3
    #6 0x5cc1c30a65ef in v8::internal::Isolate::Init(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) src/execution/isolate.cc:6322:30
    #7 0x5cc1c30a941c in v8::internal::Isolate::InitWithSnapshot(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) src/execution/isolate.cc:5731:10
    #8 0x5cc1c471df82 in v8::internal::Snapshot::Initialize(v8::internal::Isolate*) src/snapshot/snapshot.cc:198:19
    #9 0x5cc1c2bbd0ba in v8::Isolate::Initialize(v8::Isolate*, v8::Isolate::CreateParams const&) src/api/api.cc:10141:8
    #10 0x5cc1c2bbd5d0 in v8::Isolate::New(v8::Isolate::CreateParams const&) src/api/api.cc:10175:3
    #11 0x5cc1c28cd5b7 in v8::Shell::Main(int, char**) src/d8/d8.cc:7404:22
    #12 0x78bf65a2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #13 0x78bf65a2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #14 0x5cc1c2765029 in _start (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x13c5029) (BuildId: 29b1bc3e5e38cafa)

Thread T42 (V8 DefaultWorke) created by T0 here:
    #0 0x5cc1c27e8a71 in pthread_create (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x1448a71) (BuildId: 29b1bc3e5e38cafa)
    #1 0x5cc1c890f5bf in v8::base::Thread::Start() src/base/platform/platform-posix.cc:1339:14
    #2 0x5cc1c892e3a5 in v8::platform::DefaultWorkerThreadsTaskRunner::DefaultWorkerThreadsTaskRunner(unsigned int, double (*)(), v8::base::Thread::Priority) src/libplatform/default-worker-threads-task-runner.cc:80:9
    #3 0x5cc1c8915ff7 in v8::platform::DefaultPlatform::EnsureBackgroundTaskRunnerInitialized() gen/third_party/libc++/src/include/__memory/construct_at.h:37:49
    #4 0x5cc1c89149f6 in v8::platform::NewDefaultPlatform(int, v8::platform::IdleTaskSupport, v8::platform::InProcessStackDumping, std::__Cr::unique_ptr<v8::TracingController, std::__Cr::default_delete<v8::TracingController>>, v8::platform::PriorityMode) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:30
    #5 0x5cc1c28ccce3 in v8::Shell::Main(int, char**) src/d8/d8.cc:7292:18
    #6 0x78bf65a2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #7 0x78bf65a2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #8 0x5cc1c2765029 in _start (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x13c5029) (BuildId: 29b1bc3e5e38cafa)

SUMMARY: AddressSanitizer: double-free (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x149ea3d) (BuildId: 29b1bc3e5e38cafa) in operator delete[](void*)
==510645==ABORTING

## V8 sandbox violation detected!

```

Type of crash: V8 sandbox violation

## CREDIT INFORMATION

Reporter credit: Hyeonjun Ahn (@\_deayzl)

## Suggesting Fix

suggest.patch:

```
diff --git a/src/heap/marking-visitor-inl.h b/src/heap/marking-visitor-inl.h
index 761f5cc5783..46dcea32cf3 100644
--- a/src/heap/marking-visitor-inl.h
+++ b/src/heap/marking-visitor-inl.h
@@ -84,7 +84,7 @@ void MarkingVisitorBase<ConcreteVisitor>::ProcessStrongHeapObject(
   if (V8_UNLIKELY(!MemoryChunk::FromHeapObject(heap_object)->IsMarking() &&
                   IsFreeSpaceOrFiller(
                       heap_object, ObjectVisitorWithCageBases::cage_base()))) {
-    heap_->isolate()->PushStackTraceAndDie(
+    heap_->isolate()->PushParamsAndDie(
         reinterpret_cast<void*>(host->map().ptr()),
         reinterpret_cast<void*>(host->address()),
         reinterpret_cast<void*>(slot.address()),


```

Result after applying the patch:

```
➜  v8 git:(main) ✗ for i in $(seq 1 1000); do                                            
  out/x64.fuzzilli_sbx/d8 \
    --expose-gc \
    --allow-natives-syntax \
    --fuzzing \
    --sandbox-fuzzing \
    min_jstag_bg_gc_asan_v4.js \
    > /tmp/jstag-bg-marker-$i.log 2>&1

  if rg -q 'sandbox violation detected' /tmp/jstag-bg-marker-$i.log; then
    cat /tmp/jstag-bg-marker-$i.log
    break
  fi
done
➜  v8 git:(main) ✗

```

## Attachments

- [min_jstag_bg_gc_asan_v4.js](attachments/min_jstag_bg_gc_asan_v4.js) (text/javascript, 3.7 KB)
- [double-free.log](attachments/double-free.log) (text/plain, 11.2 KB)
- [suggest.patch](attachments/suggest.patch) (text/x-diff, 712 B)
- [parallel_repro.py](attachments/parallel_repro.py) (text/x-python, 12.3 KB)
- [hit_004228_w01.log](attachments/hit_004228_w01.log) (text/plain, 9.8 KB)

## Timeline

### gu...@gmail.com (2026-04-10)

sandbox violation via heap-buffer-overflow is also reproducible:

```
v8 git:(main) ✗ for i in $(seq 1 10000); do
  /home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8 \
    --expose-gc \
    --allow-natives-syntax \
    --fuzzing \
    --sandbox-fuzzing \
    /home/slave/v8-bug-bounty/findings/2026-04-09_wasm_jstag_map_race_background_gc_double_free_asan/min_jstag_bg_gc_asan_v4.js \
    > /tmp/jstag-bg-marker-$i.log 2>&1

  if rg -q 'sandbox violation detected' /tmp/jstag-bg-marker-$i.log; then
    cat /tmp/jstag-bg-marker-$i.log
    break
  fi
done

[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: anonymous shmem with 1024580 edges
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x782400000000,0x792400000000)
JSTag map word: 0x59f -> 0x59f
=================================================================
==1742696==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7bbcd474f0f0 at pc 0x5bcc012eaed2 bp 0x796c9df62390 sp 0x796c9df62388
WRITE of size 8 at 0x7bbcd474f0f0 thread T46 (V8 DefaultWorke)
    #0 0x5bcc012eaed1 in v8::internal::JavaScriptFrame::Print(v8::internal::StringStream*, v8::internal::StackFrame::PrintMode, int) const src/handles/handles-inl.h:307:11
    #1 0x5bcc012fe2ac in v8::internal::Isolate::PrintStack(v8::internal::StringStream*, v8::internal::Isolate::PrintStackMode) src/execution/isolate.cc:2091:17
    #2 0x5bcc012ff226 in v8::internal::StackTraceFailureMessage::StackTraceFailureMessage(v8::internal::Isolate*, v8::internal::StackTraceFailureMessage::StackTraceMode, unsigned long const*, unsigned long) src/execution/isolate.cc:784:15
    #3 0x5bcc012fe7b4 in v8::internal::Isolate::PushStackTraceAndDie(void*, void*, void*, void*, void*, void*) src/execution/isolate.cc:709:28
    #4 0x5bcc0143593b in void v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor>::ProcessStrongHeapObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) src/heap/marking-visitor-inl.h:87:23
    #5 0x5bcc013e97e2 in v8::internal::ConcurrentMarking::RunMajor(v8::JobDelegate*, v8::base::EnumSet<v8::internal::CodeFlushMode, int>, unsigned int, bool) src/heap/marking-visitor-inl.h:173:7
    #6 0x5bcc014a281a in v8::internal::ConcurrentMarking::JobTaskMajor::Run(v8::JobDelegate*) src/heap/concurrent-marking.cc:260:28
    #7 0x5bcc06baae14 in v8::platform::DefaultJobWorker::Run() src/libplatform/default-job.h:147:18
    #8 0x5bcc06bbc3fa in v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run() src/libplatform/default-worker-threads-task-runner.cc:95:25
    #9 0x5bcc06b9c7dc in v8::base::ThreadEntry(void*) src/base/platform/platform-posix.cc:1307:11
    #10 0x5bcc00a8fc46 in asan_thread_start(void*) asan_interceptors.cpp

0x7bbcd474f0f0 is located 0 bytes after 8176-byte region [0x7bbcd474d100,0x7bbcd474f0f0)
allocated by thread T46 (V8 DefaultWorke) here:
    #0 0x5bcc00acb41d in operator new[](unsigned long, std::nothrow_t const&) (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x149e41d) (BuildId: 29b1bc3e5e38cafa)
    #1 0x5bcc013bfc93 in v8::internal::HandleScope::Extend(v8::internal::Isolate*) src/utils/allocation.h:44:15
    #2 0x5bcc012eac9b in v8::internal::JavaScriptFrame::Print(v8::internal::StringStream*, v8::internal::StackFrame::PrintMode, int) const src/handles/handles-inl.h:299:14
    #3 0x5bcc012fe2ac in v8::internal::Isolate::PrintStack(v8::internal::StringStream*, v8::internal::Isolate::PrintStackMode) src/execution/isolate.cc:2091:17
    #4 0x5bcc012ff226 in v8::internal::StackTraceFailureMessage::StackTraceFailureMessage(v8::internal::Isolate*, v8::internal::StackTraceFailureMessage::StackTraceMode, unsigned long const*, unsigned long) src/execution/isolate.cc:784:15
    #5 0x5bcc012fe7b4 in v8::internal::Isolate::PushStackTraceAndDie(void*, void*, void*, void*, void*, void*) src/execution/isolate.cc:709:28
    #6 0x5bcc0143593b in void v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor>::ProcessStrongHeapObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) src/heap/marking-visitor-inl.h:87:23
    #7 0x5bcc013e97e2 in v8::internal::ConcurrentMarking::RunMajor(v8::JobDelegate*, v8::base::EnumSet<v8::internal::CodeFlushMode, int>, unsigned int, bool) src/heap/marking-visitor-inl.h:173:7
    #8 0x5bcc014a281a in v8::internal::ConcurrentMarking::JobTaskMajor::Run(v8::JobDelegate*) src/heap/concurrent-marking.cc:260:28
    #9 0x5bcc06baae14 in v8::platform::DefaultJobWorker::Run() src/libplatform/default-job.h:147:18
    #10 0x5bcc06bbc3fa in v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run() src/libplatform/default-worker-threads-task-runner.cc:95:25
    #11 0x5bcc06b9c7dc in v8::base::ThreadEntry(void*) src/base/platform/platform-posix.cc:1307:11
    #12 0x5bcc00a8fc46 in asan_thread_start(void*) asan_interceptors.cpp

Thread T46 (V8 DefaultWorke) created by T0 here:
    #0 0x5bcc00a75a71 in pthread_create (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x1448a71) (BuildId: 29b1bc3e5e38cafa)
    #1 0x5bcc06b9c5bf in v8::base::Thread::Start() src/base/platform/platform-posix.cc:1339:14
    #2 0x5bcc06bbb3a5 in v8::platform::DefaultWorkerThreadsTaskRunner::DefaultWorkerThreadsTaskRunner(unsigned int, double (*)(), v8::base::Thread::Priority) src/libplatform/default-worker-threads-task-runner.cc:80:9
    #3 0x5bcc06ba2ff7 in v8::platform::DefaultPlatform::EnsureBackgroundTaskRunnerInitialized() gen/third_party/libc++/src/include/__memory/construct_at.h:37:49
    #4 0x5bcc06ba19f6 in v8::platform::NewDefaultPlatform(int, v8::platform::IdleTaskSupport, v8::platform::InProcessStackDumping, std::__Cr::unique_ptr<v8::TracingController, std::__Cr::default_delete<v8::TracingController>>, v8::platform::PriorityMode) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:30
    #5 0x5bcc00b59ce3 in v8::Shell::Main(int, char**) src/d8/d8.cc:7292:18
    #6 0x7d6cd542a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #7 0x7d6cd542a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #8 0x5bcc009f2029 in _start (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8+0x13c5029) (BuildId: 29b1bc3e5e38cafa)

SUMMARY: AddressSanitizer: heap-buffer-overflow src/handles/handles-inl.h:307:11 in v8::internal::JavaScriptFrame::Print(v8::internal::StringStream*, v8::internal::StackFrame::PrintMode, int) const
Shadow bytes around the buggy address:
  0x7bbcd474ee00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbcd474ee80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbcd474ef00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbcd474ef80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bbcd474f000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bbcd474f080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00[fa]fa
  0x7bbcd474f100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbcd474f180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbcd474f200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbcd474f280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bbcd474f300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1742696==ABORTING

## V8 sandbox violation detected!

```

### gu...@gmail.com (2026-04-10)

Here's python script for easy-reproducing double-free (tested git commit: e31a1338d78fb5bc692fff2607d0142bd84c43f6):

```
➜  fuzzing_v8 python3 /home/slave/v8-bug-bounty/findings/2026-04-09_wasm_jstag_map_race_background_gc_double_free_asan/parallel_repro.py \
    --d8 /home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8 \
    --script /home/slave/v8-bug-bounty/v8_latest/v8/min_jstag_bg_gc_asan_v4.js \
    --jobs 16 \   
    --attempts 5000 --match "double-free"
parallel reproducer
  d8: /home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8
  script: /home/slave/v8-bug-bounty/v8_latest/v8/min_jstag_bg_gc_asan_v4.js
  jobs: 16
  attempts: 5000
  stop_after: 1
  timeout_s: 30.0
  run_dir: /home/slave/v8-bug-bounty/findings/2026-04-09_wasm_jstag_map_race_background_gc_double_free_asan/repro_runs/run_20260410-114312_double-free
  command:
    /home/slave/v8-bug-bounty/v8_latest/v8/out/x64.fuzzilli_sbx/d8 --expose-gc --allow-natives-syntax --fuzzing --sandbox-fuzzing /home/slave/v8-bug-bounty/v8_latest/v8/min_jstag_bg_gc_asan_v4.js
  matchers:
    double-free
[progress] completed=25 hits=0 next_attempt=41
[progress] completed=50 hits=0 next_attempt=66
...
[progress] completed=4200 hits=0 next_attempt=4216
[progress] completed=4225 hits=0 next_attempt=4241
[progress] completed=4250 hits=0 next_attempt=4266
[hit] attempt=4228 worker=1 rc=1 dur=0.28s log=/home/slave/v8-bug-bounty/findings/2026-04-09_wasm_jstag_map_race_background_gc_double_free_asan/repro_runs/run_20260410-114312_double-free/hit_004228_w01.log
  matched: double-free
[progress] completed=4275 hits=1 next_attempt=4289

summary
  elapsed_s: 16.75
  completed: 4288
  hits: 1
  summary: /home/slave/v8-bug-bounty/findings/2026-04-09_wasm_jstag_map_race_background_gc_double_free_asan/repro_runs/run_20260410-114312_double-free/summary.txt
  hit: attempt=4228 worker=1 log=/home/slave/v8-bug-bounty/findings/2026-04-09_wasm_jstag_map_race_background_gc_double_free_asan/repro_runs/run_20260410-114312_double-free/hit_004228_w01.log

```

### ch...@google.com (2026-04-10)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ch...@google.com (2026-04-13)

Setting milestone because of s2 severity.

### is...@chromium.org (2026-04-14)

Thank you for the report.

Dominik, PTAL.

### gu...@gmail.com (2026-04-16)

Hi, I just recognized that this issue is fixed by <https://chromium-review.googlesource.com/c/v8/v8/+/7761973>.

I wonder if my report is duplicate, cause I see that the bug id of the fix is 501268562 and mine is 501136000.

And I wanna be sure about if my report is arrived later that bug report, or it is internally known issue.

Thanks.

### di...@chromium.org (2026-04-16)

Ah sorry, no that is a totally different bug and I simply used the wrong one.. This issue should be fixed now by this [CL](https://crbug.com/c/7761973) here.

### gu...@gmail.com (2026-04-16)

okay.. that was quite freaking me out but thanks for fixing.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
v8 Sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/501136000)*
