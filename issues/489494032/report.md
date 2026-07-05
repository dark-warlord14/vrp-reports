# V8 Sandbox Bypass: Use-After-Free in JSLocale::Language

| Field | Value |
|-------|-------|
| **Issue ID** | [489494032](https://issues.chromium.org/issues/489494032) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gu...@gmail.com |
| **Assignee** | em...@google.com |
| **Created** | 2026-03-04 |
| **Bounty** | $3,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

`JSLocale::Language` funciton gets raw pointer of `icu_locale`. If the raw pointer becomes unreachable, major gc can free the raw old pointer when allocation triggers gc in `NewStringFromAsciiChecked` then use-after-free occurs when the raw old pointer is used.

### Root cause analysis

```
DirectHandle<Object> JSLocale::Language(Isolate* isolate,
                                        DirectHandle<JSLocale> locale) {
  Factory* factory = isolate->factory();
  const char* language = locale->icu_locale()->raw()->getLanguage();
  // race window that concurrent sandbox api overwrites icu_locale's slot so that the raw language pointer becomes unreachable
  constexpr const char kUnd[] = "und";
  if (strlen(language) == 0) {
    language = kUnd;
  }
  return factory->NewStringFromAsciiChecked(language); // calls gc if allocation slow path is executed -> frees old unreachable raw pointers -> use-after-free
}

```

`JSLocale::Language` gets a raw pointer from `locale`.

Using Concurrent usage of Sandbox api, overwrite `locale+12` with other tagged heap pointer before `NewStringFromAsciiChecked` is executed.

If `NewStringFromAsciiChecked` function leads to allocation slow path, then it can eventually call `CollectGarbageAndRetryAllocation`.

(`NewStringFromAsciiChecked` -> ... -> `HeapAllocator::AllocateRawSlowPath` -> .. -> `HeapAllocator::RetryCustomAllocate` -> `HeapAllocator::CollectGarbageAndRetryAllocation` -> `CollectGarbage`)

Then `ClearNonLiveReferences` sees dead old pointer (`icu_locale`, `language`) then `ManagedObjectFinalizerSecondPass` function calls its `Destructor`.

`factory->NewStringFromAsciiChecked(language);` uses freed `language`.

## VERSION

git commit : 2acd56ce93233d544ca40002ef5da871722940c8

commit that introduces this bug:

```
commit 12f04d8179574ea7c60d3465a73bfad8ec09f348
Author: Frank Tang <ftang@chromium.org>
Date:   Wed Dec 19 21:52:22 2018 -0800

    [Intl] Use icu::Locale as storage in JSLocale
    
    Remove flags and all string in JSLocale
    This does not change the logic of Intl.Locale constructor
    but only the way we store the information.
    Preparation for logic rewrite that sync with latest spec.

```
## REPRODUCTION CASE

gn args out/x64.sbx\_rel.instrumented\_asan:

```
is_asan=true
is_debug = false
target_cpu = "x64"
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
is_clang = true
symbol_level = 2

```

Apply poc.patch:

```
diff --git a/src/heap/heap-allocator.cc b/src/heap/heap-allocator.cc
index b96f67ab34a..d612c466d4e 100644
--- a/src/heap/heap-allocator.cc
+++ b/src/heap/heap-allocator.cc
@@ -536,7 +536,7 @@ bool HeapAllocator::CollectGarbageAndRetryAllocation(
   const auto perform_heap_limit_check = v8_flags.late_heap_limit_check
                                             ? PerformHeapLimitCheck::kNo
                                             : PerformHeapLimitCheck::kYes;
-
+  std::fprintf(stderr, "[CollectGarbageAndRetryAllocation] allocation=%d\n", static_cast<int>(allocation));
   for (int i = 0; i < 2; i++) {
     if (v8_flags.ineffective_gcs_forces_last_resort &&
         allocation != AllocationType::kYoung &&
diff --git a/src/objects/js-locale.cc b/src/objects/js-locale.cc
index 2b38646ec7e..2e0d8199062 100644
--- a/src/objects/js-locale.cc
+++ b/src/objects/js-locale.cc
@@ -859,10 +859,16 @@ DirectHandle<Object> JSLocale::Language(Isolate* isolate,
                                         DirectHandle<JSLocale> locale) {
   Factory* factory = isolate->factory();
   const char* language = locale->icu_locale()->raw()->getLanguage();
+  std::fprintf(stderr, "icu_locale: %p\n", locale->icu_locale()->raw());
+  std::fprintf(stderr, "[Language] race window start\n");
+  base::OS::Sleep(base::TimeDelta::FromMilliseconds(1));
+  std::fprintf(stderr, "[Language] race window end\n");
+  std::fprintf(stderr, "icu_locale(raw): %p\n", locale->icu_locale()->raw());
   constexpr const char kUnd[] = "und";
   if (strlen(language) == 0) {
     language = kUnd;
   }
+  std::fprintf(stderr, "[Language] before NewStringFromAsciiChecked\n");
   return factory->NewStringFromAsciiChecked(language);
 }
 


```

Execute command:

```
python3 /home/slave/v8-bug-bounty/sandbox/jslocale-language-uaf-sandbox/run_repro_icu_locale_until_spc.py \
    --tries 100 --timeout 1.2

```

Crash:

```
[HIT] attempt=19
[cmd]
/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.sbx_rel.instrumented_asan/d8 --sandbox-testing --expose-gc --predictable --gc-global --max-old-space-size=12 --max-semi-space-size=1 /home/slave/v8-bug-bounty/sandbox/jslocale-language-uaf-sandbox/repro_icu_locale_language_slot_race_gc_tunable.js -- 1 0 0 24 3 17849 8 1 0 500 0 en-US fr-FR en
[output]
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7abe00000000,0x7bbe00000000)
[cfg] attempts=1 oldRounds=0 oldPerRound=0 baseCount=24 tailCount=3 microCount=17849 microLen=8 workerMode=1 workerDelaySpins=0 workerBurst=500 preCallDelayMs=0 victimTag=en-US altTag=fr-FR expectedLanguage=en
[setup] victim=0x104f7c0 alt=0x104f7f4
[setup] offIcuLocale=12 oldIcuLocaleSlot=0x104f7b9 altIcuLocaleSlot=0x104f7ed
[worker] ready
[phase] pre-language
icu_locale: 0x7d0ff6fe2840
[Language] race window start
[Language] race window end
icu_locale(raw): 0x7d0ff6fe2c00
[Language] before NewStringFromAsciiChecked
[CollectGarbageAndRetryAllocation] allocation=0
=================================================================
==918026==ERROR: AddressSanitizer: heap-use-after-free on address 0x7d0ff6fe2848 at pc 0x55555721959e bp 0x7fffffffcce0 sp 0x7fffffffccd8
READ of size 2 at 0x7d0ff6fe2848 thread T0
    #0 0x55555721959d in v8::internal::FactoryBase<v8::internal::Factory>::NewStringFromOneByte(v8::base::Vector<unsigned char const>, v8::internal::AllocationType) src/base/memcopy.h:125:7
    #1 0x555557ba4ee6 in v8::internal::JSLocale::Language(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSLocale>) src/heap/factory-base.h:334:12
    #2 0x555556e02a48 in v8::internal::Builtin_Impl_LocalePrototypeLanguage(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:901:11
    #3 0x55555b6e6bf5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #4 0x55555b648015 in Builtins_LoadIC_NoFeedback setup-isolate-deserialize.cc
    #5 0x55555b804d24 in Builtins_GetNamedPropertyWideHandler setup-isolate-deserialize.cc
    #6 0x55555b6358bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #7 0x55555b63265b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #8 0x55555b6323aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #9 0x555557067d66 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #10 0x5555570692d8 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #11 0x555556c7003b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2033:7
    #12 0x5555569ade87 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1039:44
    #13 0x5555569e6799 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5661:10
    #14 0x5555569f2c9d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6680:37
    #15 0x5555569f20d5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6588:18
    #16 0x5555569f583b in v8::Shell::Main(int, char**) src/d8/d8.cc:7502:18
    #17 0x7ffff7c2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #18 0x7ffff7c2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #19 0x5555568a5029 in _start (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.sbx_rel.instrumented_asan/d8+0x1351029) (BuildId: 3583fd7f37b13b28)

0x7d0ff6fe2848 is located 8 bytes inside of 224-byte region [0x7d0ff6fe2840,0x7d0ff6fe2920)
freed by thread T0 here:
    #0 0x555556945086 in free (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.sbx_rel.instrumented_asan/d8+0x13f1086) (BuildId: 3583fd7f37b13b28)
    #1 0x555557b6b41f in void v8::internal::detail::Destructor<icu_77::Locale>(void*) gen/third_party/libc++/src/include/__memory/shared_count.h:65:7
    #2 0x555557c656eb in v8::internal::(anonymous namespace)::ManagedObjectFinalizerSecondPass(v8::WeakCallbackInfo<void> const&) src/objects/managed.cc:21:3
    #3 0x55555712fc52 in v8::internal::GlobalHandles::InvokeSecondPassPhantomCallbacks() src/handles/global-handles.cc:867:3
    #4 0x555557131693 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::GCCallbackFlags) src/handles/global-handles.cc:886:5
    #5 0x5555572ce40b in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck) src/heap/heap.cc:1764:34
    #6 0x5555572acb2a in v8::internal::HeapAllocator::CollectGarbageAndRetryAllocation(v8::base::FunctionRef<bool ()>, v8::internal::AllocationType, v8::internal::GarbageCollectionReason) src/heap/heap-allocator.cc:550:5
    #7 0x5555572ac971 in v8::internal::HeapAllocator::RetryCustomAllocate(v8::base::FunctionRef<bool ()>, v8::internal::AllocationType, v8::internal::GarbageCollectionReason) src/heap/heap-allocator.cc:490:7
    #8 0x5555572abb5e in v8::internal::HeapAllocator::RetryCustomAllocateOrFail(v8::base::FunctionRef<bool ()>, v8::internal::AllocationType, v8::internal::GarbageCollectionReason) src/heap/heap-allocator.cc:513:7
    #9 0x5555572ab9fc in v8::internal::HeapAllocator::AllocateRawSlowPath(v8::internal::HeapAllocator::AllocationRetryMode, int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment, v8::internal::AllocationHint) src/heap/heap-allocator.cc:218:5
    #10 0x55555723e2d3 in v8::internal::Factory::AllocateRaw(int, v8::internal::AllocationType, v8::internal::AllocationAlignment, v8::internal::AllocationHint) src/heap/heap-allocator-inl.h:248:10
    #11 0x55555721974b in v8::internal::FactoryBase<v8::internal::Factory>::NewRawOneByteString(unsigned int, v8::internal::AllocationType, v8::internal::AllocationHint) src/heap/factory-base.cc:1398:18
    #12 0x555557219340 in v8::internal::FactoryBase<v8::internal::Factory>::NewStringFromOneByte(v8::base::Vector<unsigned char const>, v8::internal::AllocationType) src/heap/factory-base.cc:1036:30
    #13 0x555557ba4ee6 in v8::internal::JSLocale::Language(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSLocale>) src/heap/factory-base.h:334:12
    #14 0x555556e02a48 in v8::internal::Builtin_Impl_LocalePrototypeLanguage(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:901:11
    #15 0x55555b6e6bf5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #16 0x55555b648015 in Builtins_LoadIC_NoFeedback setup-isolate-deserialize.cc
    #17 0x55555b804d24 in Builtins_GetNamedPropertyWideHandler setup-isolate-deserialize.cc
    #18 0x55555b6358bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #19 0x55555b63265b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #20 0x55555b6323aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #21 0x555557067d66 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #22 0x5555570692d8 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #23 0x555556c7003b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2033:7
    #24 0x5555569ade87 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1039:44
    #25 0x5555569e6799 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5661:10
    #26 0x5555569f2c9d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6680:37
    #27 0x5555569f20d5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6588:18
    #28 0x5555569f583b in v8::Shell::Main(int, char**) src/d8/d8.cc:7502:18
    #29 0x7ffff7c2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

previously allocated by thread T0 here:
    #0 0x555556945324 in malloc (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.sbx_rel.instrumented_asan/d8+0x13f1324) (BuildId: 3583fd7f37b13b28)
    #1 0x55555bbb6b93 in icu_77::Locale::clone() const third_party/icu/source/common/locid.cpp:474:12
    #2 0x555557b9fd59 in v8::internal::JSLocale::New(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::String>, v8::internal::DirectHandle<v8::internal::JSReceiver>) src/objects/js-locale.cc:480:63
    #3 0x555556dfa27b in v8::internal::Builtin_Impl_LocaleConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:775:16
    #4 0x55555b6e6bf5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #5 0x55555b6361e9 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #6 0x55555b7f3217 in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #7 0x55555b6358bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #8 0x55555b63265b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #9 0x55555b6323aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #10 0x555557067d66 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #11 0x5555570692d8 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #12 0x555556c7003b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2033:7
    #13 0x5555569ade87 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1039:44
    #14 0x5555569e6799 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5661:10
    #15 0x5555569f2c9d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6680:37
    #16 0x5555569f20d5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6588:18
    #17 0x5555569f583b in v8::Shell::Main(int, char**) src/d8/d8.cc:7502:18
    #18 0x7ffff7c2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #19 0x7ffff7c2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #20 0x5555568a5029 in _start (/home/slave/v8-bug-bounty/v8_latest/v8/out/x64.sbx_rel.instrumented_asan/d8+0x1351029) (BuildId: 3583fd7f37b13b28)

SUMMARY: AddressSanitizer: heap-use-after-free src/base/memcopy.h:125:7 in v8::internal::FactoryBase<v8::internal::Factory>::NewStringFromOneByte(v8::base::Vector<unsigned char const>, v8::internal::AllocationType)
Shadow bytes around the buggy address:
  0x7d0ff6fe2580: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x7d0ff6fe2600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0ff6fe2680: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d0ff6fe2700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0ff6fe2780: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
=>0x7d0ff6fe2800: fa fa fa fa fa fa fa fa fd[fd]fd fd fd fd fd fd
  0x7d0ff6fe2880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0ff6fe2900: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d0ff6fe2980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d0ff6fe2a00: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x7d0ff6fe2a80: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
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
==918026==ABORTING

## V8 sandbox violation detected!


```
## CREDIT INFORMATION

Ahn Hyeonjun (@\_deayzl)

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 12.5 KB)
- [poc.patch](attachments/poc.patch) (text/x-diff, 1.7 KB)
- [repro_icu_locale_language_slot_race_gc_tunable.js](attachments/repro_icu_locale_language_slot_race_gc_tunable.js) (text/javascript, 7.7 KB)
- [run_repro_icu_locale_until_spc.py](attachments/run_repro_icu_locale_until_spc.py) (text/x-python, 3.2 KB)

## Timeline

### em...@google.com (2026-03-06)

There was an earlier report [crbug/485286897](https://crbug.com/485286897) that made us aware of the broad problem with raw() callsites. I'll clarify internally whether duping would be appropriate (technically, that bug's reporter didn't mention the `js-locale.cc` file themselves, although it became obvious that we need to inspect all callsites).

### me...@google.com (2026-03-06)

emaxx: Setting provisional labels, please adjust as appropriate.

### ch...@google.com (2026-03-06)

Setting milestone because of s0/s1 severity.

### dc...@chromium.org (2026-03-06)

I'm going to dupe several other bugs into this, because they seem like the same underlying problem. If a fix is needed here, we should make sure it addresses the other duped issues too.

### dx...@google.com (2026-03-09)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@chromium.org](mailto:emaxx@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7635219>

Stop exposing raw ptrs from Managed<>

---


Expand for full commit details
```
     
    Make Managed::raw() temporarily an alias to get(), returning 
    std::shared_ptr (by value, not by a const-ref) instead of a raw pointer. 
     
    The purpose is to provide better lifetime guarantees: with a raw pointer 
    or const-ref-to-shared_ptr, it was easy to make a mistake of keeping a 
    pointer beyond a GC; especially in the presence of sandbox corruptions 
    any such pointer dereference might result in a use-after-free. 
     
    In a follow-up commit, we'll migrate away callsites from raw() to get(). 
    The raw() accessor might be considered for removal, or alternatively 
    requiring a DisallowHeapAllocation witness. 
     
    Bug: 485286897, 489159859, 489482617, 489494032, 489522223 
    Change-Id: I604c6272a27693bb52d79e4653a7856a69c1b1ab 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7635219 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105671}

```

---

Files:

- M `src/api/api.cc`
- M `src/builtins/builtins-intl.cc`
- M `src/compiler/js-call-reducer.cc`
- M `src/compiler/turbofan-graph-visualizer.cc`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- M `src/d8/d8.cc`
- M `src/debug/debug-coverage.cc`
- M `src/debug/debug-interface.cc`
- M `src/debug/debug-wasm-objects.cc`
- M `src/debug/debug.cc`
- M `src/debug/wasm/gdb-server/wasm-module-debug.cc`
- M `src/execution/frames.cc`
- M `src/execution/frames.h`
- M `src/objects/intl-objects.cc`
- M `src/objects/js-collator.cc`
- M `src/objects/js-date-time-format.cc`
- M `src/objects/js-display-names.cc`
- M `src/objects/js-list-format.cc`
- M `src/objects/js-locale.cc`
- M `src/objects/js-number-format.cc`
- M `src/objects/js-plural-rules.cc`
- M `src/objects/js-relative-time-format.cc`
- M `src/objects/js-segments.cc`
- M `src/objects/managed.h`
- M `src/objects/script-inl.h`
- M `src/objects/script.cc`
- M `src/objects/script.h`
- M `src/runtime/runtime-test-wasm.cc`
- M `src/runtime/runtime-wasm.cc`
- M `src/wasm/c-api.cc`
- M `src/wasm/interpreter/wasm-interpreter-runtime.cc`
- M `src/wasm/module-compiler.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-debug.cc`
- M `src/wasm/wasm-module.cc`
- M `src/wasm/wasm-objects-inl.h`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.h`
- M `test/cctest/wasm/test-liftoff-inspection.cc`
- M `test/cctest/wasm/test-streaming-compilation.cc`
- M `test/cctest/wasm/test-wasm-breakpoints.cc`
- M `test/cctest/wasm/test-wasm-serialization.cc`
- M `test/common/wasm/fuzzer-common.cc`
- M `test/common/wasm/wasm-run-utils.cc`
- M `test/unittests/wasm/compilation-hints-unittest.cc`
- M `test/unittests/wasm/wasm-tracing-unittest.cc`

---

Hash: [9bc50dbd7a574ac448f05ff293dd94fba4fe3745](https://chromiumdash.appspot.com/commit/9bc50dbd7a574ac448f05ff293dd94fba4fe3745)  

Date: Fri Mar 6 23:36:02 2026


---

### dx...@google.com (2026-03-11)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@chromium.org](mailto:emaxx@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7653848>

Revert "Stop exposing raw ptrs from Managed<>"

---


Expand for full commit details
```
     
    This reverts commit 9bc50dbd7a574ac448f05ff293dd94fba4fe3745. 
     
    Reason for revert: perf regressions (crbug.com/491028578, crbug.com/491521117). 
     
    Original change's description: 
    > Stop exposing raw ptrs from Managed<> 
    > 
    > Make Managed::raw() temporarily an alias to get(), returning 
    > std::shared_ptr (by value, not by a const-ref) instead of a raw pointer. 
    > 
    > The purpose is to provide better lifetime guarantees: with a raw pointer 
    > or const-ref-to-shared_ptr, it was easy to make a mistake of keeping a 
    > pointer beyond a GC; especially in the presence of sandbox corruptions 
    > any such pointer dereference might result in a use-after-free. 
    > 
    > In a follow-up commit, we'll migrate away callsites from raw() to get(). 
    > The raw() accessor might be considered for removal, or alternatively 
    > requiring a DisallowHeapAllocation witness. 
    > 
    > Bug: 485286897, 489159859, 489482617, 489494032, 489522223 
    > Change-Id: I604c6272a27693bb52d79e4653a7856a69c1b1ab 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7635219 
    > Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#105671} 
     
    Bug: 485286897, 489159859, 489482617, 489494032, 489522223, 491028578, 491521117 
    Bug: 485286897, 489159859, 489482617, 489494032, 489522223 
    Change-Id: Ifb96295c081b36894ce4ddf8f3d0a49c51948fbb 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7653848 
    Auto-Submit: Maksim Ivanov <emaxx@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105724}

```

---

Files:

- M `src/api/api.cc`
- M `src/builtins/builtins-intl.cc`
- M `src/compiler/js-call-reducer.cc`
- M `src/compiler/turbofan-graph-visualizer.cc`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- M `src/d8/d8.cc`
- M `src/debug/debug-coverage.cc`
- M `src/debug/debug-interface.cc`
- M `src/debug/debug-wasm-objects.cc`
- M `src/debug/debug.cc`
- M `src/debug/wasm/gdb-server/wasm-module-debug.cc`
- M `src/execution/frames.cc`
- M `src/execution/frames.h`
- M `src/objects/intl-objects.cc`
- M `src/objects/js-collator.cc`
- M `src/objects/js-date-time-format.cc`
- M `src/objects/js-display-names.cc`
- M `src/objects/js-list-format.cc`
- M `src/objects/js-locale.cc`
- M `src/objects/js-number-format.cc`
- M `src/objects/js-plural-rules.cc`
- M `src/objects/js-relative-time-format.cc`
- M `src/objects/js-segments.cc`
- M `src/objects/managed.h`
- M `src/objects/script-inl.h`
- M `src/objects/script.cc`
- M `src/objects/script.h`
- M `src/runtime/runtime-test-wasm.cc`
- M `src/runtime/runtime-wasm.cc`
- M `src/wasm/c-api.cc`
- M `src/wasm/interpreter/wasm-interpreter-runtime.cc`
- M `src/wasm/module-compiler.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-debug.cc`
- M `src/wasm/wasm-module.cc`
- M `src/wasm/wasm-objects-inl.h`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.h`
- M `test/cctest/wasm/test-liftoff-inspection.cc`
- M `test/cctest/wasm/test-streaming-compilation.cc`
- M `test/cctest/wasm/test-wasm-breakpoints.cc`
- M `test/cctest/wasm/test-wasm-serialization.cc`
- M `test/common/wasm/fuzzer-common.cc`
- M `test/common/wasm/wasm-run-utils.cc`
- M `test/unittests/wasm/compilation-hints-unittest.cc`
- M `test/unittests/wasm/wasm-tracing-unittest.cc`

---

Hash: [0d823bd414136d9167b89c5a92271b8f54f93f8e](https://chromiumdash.appspot.com/commit/0d823bd414136d9167b89c5a92271b8f54f93f8e)  

Date: Wed Mar 11 10:59:43 2026


---

### gu...@gmail.com (2026-03-16)

any update on this issue?

### dx...@google.com (2026-03-20)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7687810>

[intl] Fix Managed ptr lifetime in js-locale

---


Expand for full commit details
```
     
    Fix usages of raw pointers to the Managed<> underlying storage in 
    js-locale.cc. To guarantee they're safe in the sandbox attacker model, 
    we use the ptr() getter and keep the ref counter incremented for the 
    duration of the operation. 
     
    Bug: 485286897, 489494032 
    Change-Id: I99ed40687d1879c0c0741ca8190c41fe7d75a19b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7687810 
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105939}

```

---

Files:

- M `src/objects/js-locale.cc`

---

Hash: [c736e1378c9bb0d94b3e7aca006e667ca6615141](https://chromiumdash.appspot.com/commit/c736e1378c9bb0d94b3e7aca006e667ca6615141)  

Date: Fri Mar 20 13:53:57 2026


---

### gu...@gmail.com (2026-04-01)

If a CVE is going to be assigned to this issue, could you please update the credit information as follows?

```
CREDIT INFORMATION
Reporter credit: Hyeonjun Ahn (@_deayzl)

```

Thanks.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489494032)*
