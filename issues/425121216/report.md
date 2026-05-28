# V8 Sandbox Bypass: OOB write in JsonParser due to dangling GC callback

| Field | Value |
|-------|-------|
| **Issue ID** | [425121216](https://issues.chromium.org/issues/425121216) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vs...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2025-06-15 |
| **Bounty** | $1,000.00 |

## Description

#### VULNERABILITY DETAILS

During construction of a `JsonParser`, a [GCEpilogueCallback is registered](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/json/json-parser.cc;drc=feaf4438bcf1f96868820e62254495bfa46d3ea0;l=327) based on the type of the string (depending on whether it is external or not):

```
  if (StringShape(*source_, cage_base).IsExternal()) {
    chars_ =
        static_cast<const Char*>(Cast<SeqExternalString>(*source_)->GetChars());
    chars_may_relocate_ = false;
  } else {
    DisallowGarbageCollection no_gc;
    isolate->main_thread_local_heap()->AddGCEpilogueCallback(
        UpdatePointersCallback, this);
    chars_ = Cast<SeqString>(*source_)->GetChars(no_gc);
    chars_may_relocate_ = true;
  }

```

The registered callback function updates different attributes of the `JsonParser` if executed (including writing some attributes):

```
  void UpdatePointers() {
    DisallowGarbageCollection no_gc;
    const Char* chars = Cast<SeqString>(source_)->GetChars(no_gc);
    if (chars_ != chars) {
      size_t position = cursor_ - chars_;
      size_t length = end_ - chars_;
      chars_ = chars;
      cursor_ = chars_ + position;
      end_ = chars_ + length;
    }
  }

```

When the `JsonParser` goes out of scope, the destructor removes the registered GC callback. This happens again based on the type of the String that is parsed.

```
template <typename Char>
JsonParser<Char>::~JsonParser() {
  if (StringShape(*source_).IsExternal()) {
    // Check that the string shape hasn't changed. Otherwise our GC hooks are
    // broken.
    Cast<SeqExternalString>(*source_);
  } else {
    // Check that the string shape hasn't changed. Otherwise our GC hooks are
    // broken.
    Cast<SeqString>(*source_);
    isolate()->main_thread_local_heap()->RemoveGCEpilogueCallback(
        UpdatePointersCallback, this);
  }
}

```

If an attack constructs a `JsonParser` using a non-externalized string, the GC callback is registered. If the string type is changed to an externalized one during parsing, the GC callback is not removed during the `JsonParser` destruction. During the next gc, the `UpdatePointersCallback` will cause corruption by writing into the stack.

#### VERSION

V8 Git Commit: ef5225097917290af9455f4f39dcc556ff70b343 (2025-06-13T12:42:12+00:00)

#### REPRODUCTION CASE

Currently, I can not provide a working reproducer.

**ASAN Report**

```
==1961079==ERROR: AddressSanitizer: stack-use-after-return on address 0x7bfff5f94b88 at pc 0x5555592f3f55 bp 0x7fffffffd4a0 sp 0x7fffffffd498
WRITE of size 8 at 0x7bfff5f94b88 thread T0
    #0 0x5555592f3f54 in v8::internal::JsonParser<unsigned char>::UpdatePointersCallback(void*) src/json/json-parser.h:395:14
    #1 0x555558bf81c7 in v8::internal::LocalHeap::InvokeGCEpilogueCallbacksInSafepoint(v8::internal::GCCallbacksInSafepoint::GCType) src/heap/gc-callbacks.h:119:9
    #2 0x5555589bb31c in v8::internal::Heap::GarbageCollectionEpilogueInSafepoint(v8::internal::GarbageCollector) src/heap/heap.cc:1093:19
    #3 0x5555589e2309 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) src/heap/heap.cc:2435:3
    #4 0x555558a9a6ea in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck)::$_1::operator()() const src/heap/heap.cc:1720:7
    #5 0x555558a995bb in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck)::$_1>(heap::base::Stack*, void*, void const*) src/heap/base/stack.h:185:5
    #6 0x55555cb14ad2 in PushAllRegistersAndIterateStack push_registers_asm.cc
    #7 0x5555589c37bb in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck) src/heap/base/stack.h:81:7
    #8 0x5555589ddeae in v8::internal::Heap::CollectGarbageWithRetry(v8::internal::AllocationSpace, v8::base::Flags<v8::internal::GCFlag, unsigned char, unsigned char>, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) src/heap/heap.cc:2221:7
    #9 0x555558e394e2 in v8::internal::MinorGCJob::Task::RunInternal() src/heap/minor-gc-job.cc:181:9
    #10 0x555557c90de0 in v8::platform::DefaultPlatform::PumpMessageLoop(v8::Isolate*, v8::platform::MessageLoopBehavior) src/libplatform/default-platform.cc:173:9
    #11 0x555557757bb8 in v8::(anonymous namespace)::ProcessMessages(v8::Isolate*, std::__Cr::function<v8::platform::MessageLoopBehavior ()> const&) src/d8/d8.cc:6269:9
    #12 0x55555773e8cd in v8::Shell::FinishExecuting(v8::Isolate*, v8::Global<v8::Context> const&) src/d8/d8.cc:6325:10
    #13 0x555557757329 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6236:8
    #14 0x55555775617e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6141:18
    #15 0x55555775c8ae in v8::Shell::Main(int, char**) src/d8/d8.cc:7050:18
    #16 0x7ffff79e71c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #17 0x7ffff79e728a in __libc_start_main csu/../csu/libc-start.c:360:3
    #18 0x5555575a6029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x2052029) (BuildId: 6f4524db2ca7e6b2)

Address 0x7bfff5f94b88 is located in stack of thread T0 at offset 904 in frame
    #0 0x5555592ee15f in v8::internal::JsonParser<unsigned char>::Parse(v8::internal::Isolate*, v8::internal::Handle<v8::internal::String>, v8::internal::Handle<v8::internal::Object>) src/json/json-parser.h:167

  This frame has 1 object(s):
    [32, 912) 'parser' (line 173) <== Memory access at offset 904 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return src/json/json-parser.h:395:14 in v8::internal::JsonParser<unsigned char>::UpdatePointersCallback(void*)
Shadow bytes around the buggy address:
  0x7bfff5f94900: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff5f94980: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff5f94a00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff5f94a80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff5f94b00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
=>0x7bfff5f94b80: f5[f5]f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff5f94c00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff5f94c80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff5f94d00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff5f94d80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff5f94e00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
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

==1961079==ABORTING

## V8 sandbox violation detected!

```

## Attachments

- [bug.js](attachments/bug.js) (text/javascript, 1.4 KB)

## Timeline

### pg...@google.com (2025-06-16)

Hi reporter, please let us know as soon as you can get a reproducer!

Over to V8 Sheriff - there is nothing to plug into Clusterfuzz or run so I haven't been able to confirm -  passing over to you in hopes that this makes more sense at a shorter glance to triage!

setting s1 and foundin as extended as placeholders!

### ch...@google.com (2025-06-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-17)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sr...@google.com (2025-06-18)

dinfuehr@ can you take a look? The report doesn't have a reproducer unfortunately, but the bug looks legit to me.

### di...@chromium.org (2025-06-26)

It seems like a sandbox escape to me as well. I believe all we need to do is to change the condition in `~JsonParser` to `chars_may_relocate_` instead.

### dx...@google.com (2025-06-26)

Project: v8/v8  

Branch: main  

Author: Dominik Inführ [dinfuehr@chromium.org](mailto:dinfuehr@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6678331>

[json] Remove callback based on chars\_may\_relocate\_

---


Expand for full commit details
```
     
    The field chars_may_relocate_ is already set to true if a GC epilogue 
    callback is added to this method. So we should use the same field for 
    removing the callback again. 
     
    Bug: 425121216 
    Change-Id: Ifd362ccc29f753e845ee9a1aa18bb08b2147f7ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6678331 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Commit-Queue: Dominik Inführ <dinfuehr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101055}

```

---

Files:

- M `src/json/json-parser.cc`

---

Hash: 8954f5901b75f85fd323c2bab8b7030c90c2fba0  

Date:  Thu Jun 26 10:30:34 2025


---

### di...@chromium.org (2025-06-26)

I believe the CL should fix this but without a repro I can't test it. So please take a look at the CL above to check whether this is indeed fixed.

### vs...@gmail.com (2025-06-26)

Looks good to me. I would have fixed it the same way.

### sp...@google.com (2025-07-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
below baseline / speculative report of V8 sandbox bypass that resulted in a security beneficial change


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### vs...@gmail.com (2025-07-03)

Hello, thanks for the reward! I further investigated the bug and managed to derive a reproducer, demonstrating that the bug is not speculative. I would appreciate it if the VRP panel could reconsider their decision based on this additional information. I will try harder to provide reproducers for all future bugs. Many thanks!

The provided reproducer may need multiple tries to trigger. I tested it on `8eb6cba8e5afc6513042f5ea3da82973da0183c5` using the following gn args:

```
is_debug = false
dcheck_always_on = false
is_asan = true
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
v8_static_library = true
target_cpu = "x64"

```

ASan report:

```
==729348==ERROR: AddressSanitizer: stack-use-after-return on address 0x7bfff62f5048 at pc 0x5555575817cc bp 0x7fffffffd090 sp 0x7fffffffd088
READ of size 8 at 0x7bfff62f5048 thread T0
    #0 0x5555575817cb in UpdatePointers src/json/json-parser.h:393:41
    #1 0x5555575817cb in v8::internal::JsonParser<unsigned char>::UpdatePointersCallback(void*) src/json/json-parser.h:388:50
    #2 0x555557252543 in Invoke src/heap/gc-callbacks.h:119:9
    #3 0x555557252543 in v8::internal::LocalHeap::InvokeGCEpilogueCallbacksInSafepoint(v8::internal::GCCallbacksInSafepoint::GCType) src/heap/local-heap.cc:477:26
    #4 0x555557163f5c in operator() src/heap/heap.cc:1093:19
    #5 0x555557163f5c in IterateLocalHeaps<(lambda at ../../src/heap/heap.cc:1092:36)> src/heap/safepoint.h:41:7
    #6 0x555557163f5c in v8::internal::Heap::GarbageCollectionEpilogueInSafepoint(v8::internal::GarbageCollector) src/heap/heap.cc:1092:18
    #7 0x555557175975 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) src/heap/heap.cc:2440:3
    #8 0x5555571b7e14 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck)::$_1::operator()() const src/heap/heap.cc:1725:7
    #9 0x5555571b7626 in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck)::$_1>(heap::base::Stack*, void*, void const*) src/heap/base/stack.h:185:5
    #10 0x555558ef0132 in PushAllRegistersAndIterateStack push_registers_asm.cc
    #11 0x555557167c64 in SetMarkerIfNeededAndCallback<(lambda at ../../src/heap/heap.cc:1693:40)> src/heap/base/stack.h:81:7
    #12 0x555557167c64 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck) src/heap/heap.cc:1693:11
    #13 0x5555574b2580 in v8::internal::(anonymous namespace)::InvokeGC(v8::Isolate*, v8::internal::(anonymous namespace)::GCOptions) src/extensions/gc-extension.cc:204:17
    #14 0x5555574b1357 in v8::internal::GCExtension::GC(v8::FunctionCallbackInfo<v8::Value> const&) src/extensions/gc-extension.cc:276:5
    #15 0x55555b351583 in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc
    #16 0x55555b34f774 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #17 0x55555b34c51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #18 0x55555b34c26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #19 0x555556f7ed2b in Call src/execution/simulator.h:212:12
    #20 0x555556f7ed2b in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #21 0x555556f802e8 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #22 0x555556bfd1a7 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1968:7
    #23 0x555556857aa2 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1033:44
    #24 0x555556889973 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5329:10
    #25 0x55555689469c in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6281:37
    #26 0x555556893d66 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6189:18
    #27 0x555556896ed8 in v8::Shell::Main(int, char**) src/d8/d8.cc:7056:18
    #28 0x7ffff7c8c1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #29 0x7ffff7c8c28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #30 0x55555674f029 in _start (d8+0x11fb029) (BuildId: 28bbbc7157f38fd2)

Address 0x7bfff62f5048 is located in stack of thread T0 at offset 72 in frame
    #0 0x55555757eb5f in v8::internal::JsonParser<unsigned char>::Parse(v8::internal::Isolate*, v8::internal::Handle<v8::internal::String>, v8::internal::Handle<v8::internal::Object>, std::__Cr::optional<v8::ScriptOriginOptions>) src/json/json-parser.h:168

  This frame has 1 object(s):
    [32, 920) 'parser' (line 174) <== Memory access at offset 72 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return src/json/json-parser.h:393:41 in UpdatePointers
Shadow bytes around the buggy address:
  0x7bfff62f4d80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff62f4e00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff62f4e80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff62f4f00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff62f4f80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
=>0x7bfff62f5000: f5 f5 f5 f5 f5 f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5
  0x7bfff62f5080: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff62f5100: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff62f5180: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff62f5200: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bfff62f5280: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
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

Command: d8 UpdatePointersCallback.original.js 

==729348==ABORTING

## V8 sandbox violation detected!

Received signal 6

```

### am...@chromium.org (2025-07-03)

Hello, thank you for the follow up here. However, we have pretty clear rules regarding reward criteria and expectations for security bug reports in relation to reward decisions.

It is expected that information and demonstration related to the security impact and exploitability, specifically a test case / reproducer, be provided at the time of submission of the bug report or, at the very least, prior to the bug being resolved. This is important as it is information critical for us to validate and investigate the issue, understand the exploitability, and also in testing the fix.
While we appreciate the effort here, we do not provide re-assessments for potential increase reward amounts for information that falls into "expected characteristics of a baseline report" provided after the reward.
Please see our policy about this for more information: <https://g.co/chrome/vrp#report-criteria-for-reward-decisions>

### vs...@gmail.com (2025-07-03)

I see, my bad. Thanks!

### ch...@google.com (2025-10-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/425121216)*
