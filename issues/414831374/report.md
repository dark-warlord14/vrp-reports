# V8 Sandbox Bypass: OOB writ in Module::GetModuleNamespace

| Field | Value |
|-------|-------|
| **Issue ID** | [414831374](https://issues.chromium.org/issues/414831374) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | v8...@gmail.com |
| **Assignee** | sa...@google.com |
| **Created** | 2025-04-30 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

I have not yet managed to build a reproducer for this bug. Therefore, I will explain the bug in the following. The problem arises when a dynamic import (via the `import()` function) happens.

```
ns = await import('data:text/javascript,export function v4(){print("v4");}');
ns.v4();

```

During the import, the `Module::GetModuleNamespace` function is executed. Here, we have the following code:

```
  names.reserve(exports->NumberOfElements()); <---- attacker controlled
  for (InternalIndex i : exports->IterateEntries()) {
    Tagged<Object> key;
    if (!exports->ToKey(roots, i, &key)) continue;
    names.push_back(handle(Cast<String>(key), isolate));
  }

```

Here, `reserve()` is called with an attack-controlled input (since `NumberOfElements()` reads from an on-heap object of type `ObjectHashTable`)

The function `reserve(new_cap)` calls [here](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/zone/zone-containers.h;drc=e16e0a9cfaaaec3c25134167b34d57c07ec737a5;l=241) the function `EnsureCapacity(new_cap)`. In turn, this function calls `Grow` [here](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/zone/zone-containers.h;drc=e16e0a9cfaaaec3c25134167b34d57c07ec737a5;l=471), which uses `AllocateArray` to allocate an array of the requested size. The function looks like this:

```
  template <typename T, typename TypeTag = T[]>
  T* AllocateArray(size_t length) {
    static_assert(alignof(T) <= kAlignmentInBytes);
    DCHECK_IMPLIES(is_compressed_pointer<T>::value, supports_compression());
    DCHECK_LT(length, std::numeric_limits<size_t>::max() / sizeof(T));
    return static_cast<T*>(Allocate<TypeTag>(length * sizeof(T)));
  }

```

The problem is that the attacker may pass a value for `length` that violates the `DCHECK_LT` check, consequently causing the multiplication `length * sizeof(T)` to overflow (e.g., for `length=-1`). Thus, the buffer is considerably smaller than anticipated.

Now, returning to the callee `Grow()`, the allocated `data_` array and the `capacity_` array disagree about the correct size of the backing allocation.

```
  V8_NOINLINE V8_PRESERVE_MOST void Grow(size_t minimum) {
    T* old_data = data_;
    T* old_end = end_;
    size_t old_size = size();
    size_t new_capacity = NewCapacity(minimum);
    data_ = zone_->AllocateArray<T>(new_capacity); <----- array that is too small
    end_ = data_ + old_size;
    if (old_data) {
      MoveToNewStorage(data_, old_data, old_end);
      zone_->DeleteArray(old_data, capacity_ - old_data);
    }
    // <---- capacity_ is no longer in sync with the actual size.
    capacity_ = data_ + new_capacity;
  }

```

Returning to the `Module::GetModuleNamespace` function, we use `push_back` on `names`, which relies on the corrupted `capacity_` for bound checking. Thus, depending on the number of exports, we can overwrite an arbitrary amount of memory, eventually resulting in a sandbox bypass.

```
  // <---- `NumberOfElements` is attacker controlled, `names` is corrupted now.
  names.reserve(exports->NumberOfElements());
  for (InternalIndex i : exports->IterateEntries()) {
    Tagged<Object> key;
    if (!exports->ToKey(roots, i, &key)) continue;
    // <---- The backing array is too small and `push_back` will cause OOB write
    names.push_back(handle(Cast<String>(key), isolate)); 
  }

```

If you need any further clarification, please let me know. I would also be happy about any tips on why this might not be straightforward to reproduce.

#### VERSION

V8 commit: 56f9ec26f228aea249900dfe4bcb9cb664a3c8d8

##### ASAN Report:

```
==1738891==ERROR: AddressSanitizer: use-after-poison on address 0x7e4ff75d49a8 at pc 0x5555594c8bc2 bp 0x7fffffffd230 sp 0x7fffffffd228
WRITE of size 8 at 0x7e4ff75d49a8 thread T0
[Detaching after fork from child process 1753641]
    #0 0x5555594c8bc1 in v8::internal::Module::GetModuleNamespace(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Module>) src/zone/zone-containers.h:318:15
    #1 0x555557553c07 in v8::Shell::DoHostImportModuleDynamically(void*) src/d8/d8.cc:1692:57
    #2 0x555559d2ccaa in v8::internal::Runtime_RunMicrotaskCallback(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-promise.cc:93:3
    #3 0x55555ecd28f5 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #4 0x55555eb5a8be in Builtins_RunMicrotasks setup-isolate-deserialize.cc
    #5 0x55555eac558c in Builtins_JSRunMicrotasksEntry setup-isolate-deserialize.cc
    #6 0x55555819ec77 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:212:12
    #7 0x5555581a2f2c in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:500:18
    #8 0x5555581a369c in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*) src/execution/execution.cc:604:10
    #9 0x55555830619f in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) src/execution/microtask-queue.cc:185:22
    #10 0x555558305610 in v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate*) src/execution/microtask-queue.cc:129:3
    #11 0x555558249a02 in v8::internal::Isolate::FireCallCompletedCallbackInternal(v8::internal::MicrotaskQueue*) src/execution/microtask-queue.h:48:5
    #12 0x555557a8ac26 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/execution/isolate.h:1791:5
    #13 0x5555575484ad in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1031:44
    #14 0x55555758e606 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5104:10
    #15 0x55555759fe14 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6058:37
    #16 0x55555759f2a7 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5966:18
    #17 0x5555575a495e in v8::Shell::Main(int, char**) src/d8/d8.cc:6874:18
    #18 0x7ffff7a191c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #19 0x7ffff7a1928a in __libc_start_main csu/../csu/libc-start.c:360:3
    #20 0x555557435029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x1ee1029) (BuildId: ebd42531ac7cf1fd)

0x7e4ff75d49a8 is located 168 bytes inside of 8192-byte region [0x7e4ff75d4900,0x7e4ff75d6900)
allocated by thread T0 here:
    #0 0x5555574c67c0 in malloc /work/llvm-project/compiler-rt/lib/asan/asan_malloc_linux.cpp:67:3
    #1 0x555559f74e05 in v8::internal::AllocAtLeastWithRetry(unsigned long) src/base/platform/memory.h:44:10
    #2 0x555559f899fb in v8::internal::AccountingAllocator::AllocateSegment(unsigned long, bool) src/zone/accounting-allocator.cc:89:19
    #3 0x555559f8ac87 in v8::internal::Zone::Expand(unsigned long) src/zone/zone.cc:179:19
    #4 0x555559f8aacb in v8::internal::Zone::AsanNew(unsigned long) src/zone/zone.cc:55:5
    #5 0x5555594caea5 in void std::__Cr::__hash_table<v8::internal::Handle<v8::internal::Module>, v8::internal::ModuleHandleHash, v8::internal::ModuleHandleEqual, v8::internal::ZoneAllocator<v8::internal::Handle<v8::internal::Module>>>::__do_rehash<true>(unsigned long) src/zone/zone.h:63:12
    #6 0x5555594c7935 in v8::internal::Module::GetModuleNamespace(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Module>) third_party/libc++/src/include/__hash_table:884:63
    #7 0x555557553c07 in v8::Shell::DoHostImportModuleDynamically(void*) src/d8/d8.cc:1692:57
    #8 0x555559d2ccaa in v8::internal::Runtime_RunMicrotaskCallback(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-promise.cc:93:3
    #9 0x55555ecd28f5 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #10 0x55555eb5a8be in Builtins_RunMicrotasks setup-isolate-deserialize.cc
    #11 0x55555eac558c in Builtins_JSRunMicrotasksEntry setup-isolate-deserialize.cc
    #12 0x55555819ec77 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:212:12
    #13 0x5555581a2f2c in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:500:18
    #14 0x5555581a369c in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*) src/execution/execution.cc:604:10
    #15 0x55555830619f in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) src/execution/microtask-queue.cc:185:22
    #16 0x555558305610 in v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate*) src/execution/microtask-queue.cc:129:3
    #17 0x555558249a02 in v8::internal::Isolate::FireCallCompletedCallbackInternal(v8::internal::MicrotaskQueue*) src/execution/microtask-queue.h:48:5
    #18 0x555557a8ac26 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/execution/isolate.h:1791:5
    #19 0x5555575484ad in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1031:44
    #20 0x55555758e606 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5104:10
    #21 0x55555759fe14 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6058:37
    #22 0x55555759f2a7 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5966:18
    #23 0x5555575a495e in v8::Shell::Main(int, char**) src/d8/d8.cc:6874:18
    #24 0x7ffff7a191c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #25 0x7ffff7a1928a in __libc_start_main csu/../csu/libc-start.c:360:3
    #26 0x555557435029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x1ee1029) (BuildId: ebd42531ac7cf1fd)

SUMMARY: AddressSanitizer: use-after-poison src/zone/zone-containers.h:318:15 in v8::internal::Module::GetModuleNamespace(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Module>)
Shadow bytes around the buggy address:
  0x7e4ff75d4700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e4ff75d4780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e4ff75d4800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e4ff75d4880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e4ff75d4900: 00 00 00 00 00 f7 f7 f7 00 00 00 f7 f7 f7 00 00
=>0x7e4ff75d4980: f7 f7 f7 f7 f7[f7]00 00 00 00 00 00 00 00 00 00
  0x7e4ff75d4a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e4ff75d4a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e4ff75d4b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e4ff75d4b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e4ff75d4c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==1738891==ABORTING

## V8 sandbox violation detected!


```
#### CREDIT INFORMATION

Reporter credit: v8sbxfuzz

## Timeline

### ja...@chromium.org (2025-04-30)

Hi, thanks for the detailed explanation. I'm sending it back to you to see if you can provide a working proof of concept (POC) that we could use to verify the bug.

I'm going to treat this as speculatively true for the time being because the description seems plausible.

### ja...@chromium.org (2025-04-30)

Following the security shepherding guide:

- adding provisional severity of Medium (S2)
- provisional priority P1
- assigned to current V8 sheriff
- setting security impact - none
- adding to v8 sandbox hotlist.

### sa...@google.com (2025-05-02)

Thanks for the report! I agree that this looks like a valid issue, but a reproducer would be nice for sure. I suspect one issue for a reproducer is that there is no JS code execution between the allocation of the Module object (which must be corrupted) and the execution of the vulnerable code? Have you run into such an issue? Maybe it would be possible to get a hold of the Module object (and corrupt it) from inside the imported code, but I'm not familiar enough with the module logic to be sure.

In any case, from a brief look at the code I see three potential improvements/fixes:

1. AllocateArray() should probably have an overflow check as a defense-in-depth measure. It'd be great to have more robust out-of-sandbox containers, and this is a step in that direction.
2. HashTableBase::NumberOfElements() should probably not return a signed int but an unsigned int. I think this is the reason why the size\_t can even become large enough to overflow: if we promote a negative int to a size\_t, it will become a huge value.
3. I'm not sure there's a need to allocate any out-of-sandbox memory for this use-case. Potentially that C++ code could just allocate an in-sandbox buffer. This might be a target for code refactoring if we want to sandbox C++ code in the future (so that it only writes to in-sandbox memory).

Igor, what do you think of these options? I'm happy to give (1) and (2) a try. (3) would probably be something for the future if we start looking into sandboxing of C++ code.

### dx...@google.com (2025-05-13)

Project: v8/v8  

Branch: main  

Author: Samuel Groß [saelo@chromium.org](mailto:saelo@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6540007>

[zone] Harden Zone::AllocateArray

---


Expand for full commit details
```
     
    This CL adds an overflow check to ensure that the multiplication of the 
    requested length with the element size does not overflow. This is a 
    defense-in-depth measure to avoid potential memory corruption since we 
    would return a too-small allocation in case of an integer overflow. 
     
    Bug: 414831374 
    Change-Id: I84e3470d7a59b393c6f3631efad9ff181f06c34b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6540007 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Samuel Groß <saelo@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100233}

```

---

Files:

- M `src/zone/zone.h`

---

Hash: 7f7c238b9e20fa74b16d93c2300aa212f6540ec1  

Date:  Tue May 13 07:55:07 2025


---

### dx...@google.com (2025-05-14)

Project: v8/v8  

Branch: main  

Author: Samuel Groß [saelo@chromium.org](mailto:saelo@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6540830>

Use unsigned integers for HashTable size and capacity

---


Expand for full commit details
```
     
    Until now, we used a (signed) int for the NumberOfElements() and 
    Capacity() of a HashTable. Using signed integers for things like sizes 
    is generally somewhat dangerous as it can for example lead to seemingly 
    impossible integer overflows if the (32-bit) int is first promoted to a 
    (64-bit) size_t, which is then increased further (e.g. through a 
    multiplication with an element size). This is particularly problematic 
    for the sandbox as the on-heap integer value is fully 
    attacker-controlled. To avoid these problems, unsigned integer types 
    should be used for values that represent object sizes or similar. This 
    CL therefore switches HashTableBase to use uint32_t instead. 
     
    Bug: 414831374 
    Change-Id: Iba3a8034b124a4452cb843f9b46b41def8dced7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6540830 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Samuel Groß <saelo@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100269}

```

---

Files:

- M `src/objects/hash-table-inl.h`
- M `src/objects/hash-table.h`
- M `src/objects/js-collection.h`
- M `src/objects/js-struct.cc`
- M `src/objects/objects.cc`
- M `test/cctest/test-code-stub-assembler.cc`

---

Hash: 9a99c108f6763fa125930e86981707caca68102f  

Date:  Wed May 14 11:18:38 2025


---

### sa...@google.com (2025-05-14)

I've landed the two fixes discussed in [comment #4](https://issues.chromium.org/issues/414831374#comment4) now. @Reporter are you able to confirm that this issues has been fixed properly and that you're no longer seeing these crashes in your fuzzer? Thanks!

### v8...@gmail.com (2025-05-14)

This is looking good now. I can not reproduce the bug anymore. Thanks!

### pe...@google.com (2025-05-14)

Thank you for providing more feedback. Adding the requester to the CC list.

### sa...@google.com (2025-05-15)

Excellent thank you very much! Then I will mark this as fixed now

### sp...@google.com (2025-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of V8 sandbox bypass demonstrating memory corruption outside the V8 heap sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-22)

Congratulations and thank you for your continued work fuzzing the V8 sandbox!

### ch...@google.com (2025-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of V8 sandbox bypass demonstrating memory corruption outside the V8 heap sandbox

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/414831374)*
