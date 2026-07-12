# V8 Sandbox Bypass: BigInt DivideBarrett Double Fetch causing Native Heap oob read/write

| Field | Value |
|-------|-------|
| **Issue ID** | [496629079](https://issues.chromium.org/issues/496629079) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2026-03-27 |
| **Bounty** | $5,000.00 |

## Description

## Vulnerability Details

### Summary

When `toString()` enters `ToStringFormatter::Fast()`, the top-level `ProcessLevel()` directly reuses the original BigInt heap memory (that is, `digits`) under certain parameter combinations (such as `radix=21`) instead of copying it first. At that point, if an attacker uses an arbitrary sandbox write primitive to concurrently modify those heap digits, `DivideBarrett()` can observe two contradictory snapshots during the same division: the first half of the reads computes the quotient `Q` as 0, while the second half of the reads judges the remainder as "negative and requiring correction." Eventually, the correction logic `Subtract(Q, q_sub)` subtracts from an all-zero native buffer of only 2 digits, causing the borrow chain to cross the buffer boundary and resulting in native heap OOB reads and writes.

### Details

BigInt inside V8 is not a simple number. It is an array containing multiple 64-bit chunks (called `digit`). When `toString(radix)` handles a radix that is not a power of 2, it enters `ToStringFormatter::Fast()`. This is a divide-and-conquer algorithm: it first computes a huge internal divisor `B`, then uses `DivideBarrett()` to split the current large integer `A` into quotient `Q` and remainder `R`, and then processes them recursively.

The root cause of the vulnerability is: the input BigInt data lives in the V8 sandbox heap and can be modified concurrently, while the intermediate result `Q` is allocated in a temporary buffer on the native heap.

In `src/objects/bigint.cc`, `BigInt::ToString` directly hands the digits view on the heap to the bigint library:

```
// src/objects/bigint.cc
bigint::Digits digits = bigint->digits();
bigint::Status status = isolate->bigint_processor()->ToString(
    characters, &chars_written, digits, radix, sign);

```

When `radix=21` and the BigInt length is `124`, the automatically generated top-level divisor `B` has length `123`. Under this parameter combination, the top-level `leading_zero_shift_` happens to be 0, which means `ShiftedDigits` **does not copy the original digits**, but directly aliases the original heap memory:

```
// src/bigint/div-helpers-inl.h
if (shift == 0) {
  inplace_ = true;
  return;
}

```

Therefore, the dividend `A` seen by `DivideBarrett()` is heap memory that can be modified concurrently.

At the same time, the size of the native buffer allocated by `ProcessLevel()` for the quotient `Q` is:

```
// src/bigint/tostring.cc
ScratchDigits left(chunk.len() - level->divisor_.len() + 1);

```

At this point, `chunk.len() == 124` and `level->divisor_.len() == 123`, so `Q.len() = 2`. In other words, `Q` is only a **16-byte native heap buffer**.

Inside `DivideBarrett()`, it reads `A` multiple times:

```
// src/bigint/div-barrett.cc
RWDigits K(scratch, 0, 2 * I.len());
Multiply(K, A1, I);   // <--- first read of A's high part A1
// ...
Add(Q, K + I.len(), A1);
// ...
digit_t r_high = A[B.len()] - P[B.len()] - borrow; // <--- second read of A[B.len()]
// ...
if (r_high >> (kDigitBits - 1) == 1) { // negative remainder correction
  digit_t q_sub = 0;
  do {
    r_high += InplaceAddAndReturnCarry(R, B);
    q_sub++;
  } while (r_high != 0);
  Subtract(Q, q_sub);
}

```

If an attacker tampers `A[B.len()]` from `0` to `~0` (that is, all 1s) between the two reads, the following logical inconsistency occurs:

1. In the first half, `Multiply` and `Add` see `A1` as 0, so the computed quotient `Q = 0`.
2. In the second half, when computing `r_high`, the code sees `A[B.len()] == ~0`, which makes the highest bit of `r_high` become 1.
3. The code mistakenly concludes that the remainder is negative and enters the correction loop.
4. The correction loop eventually executes `Subtract(Q, q_sub)`.

At this point, `Q` is an all-zero array of length 2. The internal implementation of subtracting from an all-zero array is as follows:

```
// src/bigint/bigint-inl.h
inline void Subtract(RWDigits X, digit_t y) {
  digit_t borrow = y;
  uint32_t i = 0;
  do {
    X[i] = digit_sub(X[i], borrow, &borrow);
    i++;
  } while (borrow != 0);
}

```

Because `Q` is all zero, `0 - 1` generates a borrow. The borrow propagates from `Q[0]` to `Q[1]`, and then to `Q[2]`. But `Q` has length 2, and the loop continues because `borrow != 0`, crossing the boundary of the 16-byte native buffer and causing OOB reads and writes.

## Bisect

The commit that introduced the core vulnerable logic is perhaps `40b20c9401e [bigint] Faster .toString()`. This is the first commit that simultaneously introduced the divide-and-conquer `ToStringFormatter::Fast()` path, level construction based on `BitLength(digits_)`, a top-level `ProcessLevel(..., digits_, ...)` that later re-reads the same heap digits, and `ShiftedDigits` directly aliasing the original digits when `shift == 0`.

## Version

Test on V8 14.8.99:

```
git checkout 14.8.99

```
## Reproduction

In the PoC, we fix `radix = 21`, construct a 124-digit BigInt, and pre-arrange its lower 123 digits as `2^(64*123) - B` (so that the correction loop only needs to execute once, i.e. `q_sub = 1`). Then a worker thread continuously flips digit 123 (between `0` and `~0`), while the main thread repeatedly calls `toString(21)` to trigger the race.

Build `d8` with ASan + sandbox + `v8_enable_memory_corruption_api` and run (this may need a lot of tries to trigger):

```
ASAN_OPTIONS=halt_on_error=1 ./d8 --sandbox-testing ./poc.js

```
```
for i in $(seq 1 100); do   echo "=== run $i ===";   ASAN_OPTIONS=halt_on_error=1 ./d8 --sandbox-testing ./poc.js && continue;   break; done

```

In the original code, `X[i] = digit_sub(X[i], ...)` is a read-modify-write operation. It must first read the old value of `X[i]` and then write it back. Therefore, ASAN first catches the out-of-bounds read:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a2500000000,0x7b2500000000)
=================================================================
==1580251==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b8defffc660 at pc 0x555f81445f2c bp 0x7fff211bdaf0 sp 0x7fff211bdae8
READ of size 8 at 0x7b8defffc660 thread T0
    #0 0x555f81445f2b in v8::bigint::ProcessorImpl::DivideBarrett(v8::bigint::RWDigits, v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::RWDigits) src/bigint/bigint.h:171:7
    #1 0x555f8143e589 in v8::bigint::(anonymous namespace)::ToStringFormatter::ProcessLevel(v8::bigint::(anonymous namespace)::RecursionLevel*, v8::bigint::Digits, char*, bool) src/bigint/tostring.cc:530:17
    #2 0x555f8143bc02 in v8::bigint::ProcessorImpl::ToStringImpl(char*, unsigned int*, v8::bigint::Digits&, int, bool, bool) src/bigint/tostring.cc:434:10
    #3 0x555f8143c28b in v8::bigint::Processor::ToString(char*, unsigned int*, v8::bigint::Digits&, int, bool) src/bigint/tostring.cc:561:3
    #4 0x555f7ec839d9 in v8::internal::BigInt::ToString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::BigInt>, int, v8::internal::ShouldThrow) src/objects/bigint.cc:964:58
    #5 0x555f7de74253 in v8::internal::Builtin_Impl_BigIntPrototypeToString(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:120:37
    #6 0x555f84108eb5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #7 0x555f840548bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #8 0x555f8405165b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #9 0x555f840513aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #10 0x555f7e25ec07 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #11 0x555f7e26154c in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #12 0x555f7dda8fbd in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2034:7
    #13 0x555f7d8b8e2e in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #14 0x555f7d8fe243 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5670:10
    #15 0x555f7d90cfbf in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6691:37
    #16 0x555f7d90c14e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6599:18
    #17 0x555f7d911418 in v8::Shell::Main(int, char**) src/d8/d8.cc:7516:18
    #18 0x7f6df0c9fd79 in __libc_start_main csu/../csu/libc-start.c:308:16

0x7b8defffc660 is located 0 bytes after 16-byte region [0x7b8defffc650,0x7b8defffc660)
allocated by thread T0 here:
    #0 0x555f7d87f21d in operator new[](unsigned long) (/home/user/v8_build/v8/out/release_asan_14_4_201/d8+0x14bb21d) (BuildId: 0fd4e37526f252c9)
    #1 0x555f8143d1ae in v8::bigint::(anonymous namespace)::ToStringFormatter::ProcessLevel(v8::bigint::(anonymous namespace)::RecursionLevel*, v8::bigint::Digits, char*, bool) src/bigint/bigint-internal.h:97:43
    #2 0x555f8143bc02 in v8::bigint::ProcessorImpl::ToStringImpl(char*, unsigned int*, v8::bigint::Digits&, int, bool, bool) src/bigint/tostring.cc:434:10
    #3 0x555f8143c28b in v8::bigint::Processor::ToString(char*, unsigned int*, v8::bigint::Digits&, int, bool) src/bigint/tostring.cc:561:3
    #4 0x555f7ec839d9 in v8::internal::BigInt::ToString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::BigInt>, int, v8::internal::ShouldThrow) src/objects/bigint.cc:964:58
    #5 0x555f7de74253 in v8::internal::Builtin_Impl_BigIntPrototypeToString(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:120:37
    #6 0x555f84108eb5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #7 0x555f840548bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #8 0x555f8405165b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #9 0x555f840513aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #10 0x555f7e25ec07 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #11 0x555f7e26154c in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #12 0x555f7dda8fbd in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2034:7
    #13 0x555f7d8b8e2e in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #14 0x555f7d8fe243 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5670:10
    #15 0x555f7d90cfbf in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6691:37
    #16 0x555f7d90c14e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6599:18
    #17 0x555f7d911418 in v8::Shell::Main(int, char**) src/d8/d8.cc:7516:18
    #18 0x7f6df0c9fd79 in __libc_start_main csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow src/bigint/bigint.h:171:7 in v8::bigint::ProcessorImpl::DivideBarrett(v8::bigint::RWDigits, v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::RWDigits)
Shadow bytes around the buggy address:
  0x7b8defffc380: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa
  0x7b8defffc400: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd
  0x7b8defffc480: fa fa fd fa fa fa fd fd fa fa 00 fa fa fa 00 fa
  0x7b8defffc500: fa fa 00 00 fa fa fd fd fa fa 00 fa fa fa 00 00
  0x7b8defffc580: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa
=>0x7b8defffc600: fa fa 00 fa fa fa 00 fa fa fa 00 00[fa]fa fd fd
  0x7b8defffc680: fa fa 00 fa fa fa 00 00 fa fa fa fa fa fa fa fa
  0x7b8defffc700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8defffc780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8defffc800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b8defffc880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1580251==ABORTING

## V8 sandbox violation detected!

```

After patching out the read behavior, an OOB write is observed:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a0300000000,0x7b0300000000)
=================================================================
==1575279==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b6bc02035a0 at pc 0x55af8abb1194 bp 0x7ffe90feec30 sp 0x7ffe90feec28
WRITE of size 8 at 0x7b6bc02035a0 thread T0
    #0 0x55af8abb1193 in v8::bigint::ProcessorImpl::DivideBarrett(v8::bigint::RWDigits, v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::RWDigits) src/bigint/bigint.h:162:37
    #1 0x55af8aba9689 in v8::bigint::(anonymous namespace)::ToStringFormatter::ProcessLevel(v8::bigint::(anonymous namespace)::RecursionLevel*, v8::bigint::Digits, char*, bool) src/bigint/tostring.cc:530:17
    #2 0x55af8aba6d02 in v8::bigint::ProcessorImpl::ToStringImpl(char*, unsigned int*, v8::bigint::Digits&, int, bool, bool) src/bigint/tostring.cc:434:10
    #3 0x55af8aba738b in v8::bigint::Processor::ToString(char*, unsigned int*, v8::bigint::Digits&, int, bool) src/bigint/tostring.cc:561:3
    #4 0x55af883ee9d9 in v8::internal::BigInt::ToString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::BigInt>, int, v8::internal::ShouldThrow) src/objects/bigint.cc:964:58
    #5 0x55af875df253 in v8::internal::Builtin_Impl_BigIntPrototypeToString(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:120:37
    #6 0x55af8d874eb5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #7 0x55af8d7c08bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #8 0x55af8d7bd65b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #9 0x55af8d7bd3aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #10 0x55af879c9c07 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #11 0x55af879cc54c in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #12 0x55af87513fbd in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2034:7
    #13 0x55af87023e2e in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #14 0x55af87069243 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5670:10
    #15 0x55af87077fbf in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6691:37
    #16 0x55af8707714e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6599:18
    #17 0x55af8707c418 in v8::Shell::Main(int, char**) src/d8/d8.cc:7516:18
    #18 0x7f4bc0f30d79 in __libc_start_main csu/../csu/libc-start.c:308:16

0x7b6bc02035a0 is located 0 bytes after 16-byte region [0x7b6bc0203590,0x7b6bc02035a0)
allocated by thread T0 here:
    #0 0x55af86fea21d in operator new[](unsigned long) (/home/user/v8_build/v8/out/release_asan_14_4_201/d8+0x14bb21d) (BuildId: 65df69b9e8b92939)
    #1 0x55af8aba82ae in v8::bigint::(anonymous namespace)::ToStringFormatter::ProcessLevel(v8::bigint::(anonymous namespace)::RecursionLevel*, v8::bigint::Digits, char*, bool) src/bigint/bigint-internal.h:97:43
    #2 0x55af8aba6d02 in v8::bigint::ProcessorImpl::ToStringImpl(char*, unsigned int*, v8::bigint::Digits&, int, bool, bool) src/bigint/tostring.cc:434:10
    #3 0x55af8aba738b in v8::bigint::Processor::ToString(char*, unsigned int*, v8::bigint::Digits&, int, bool) src/bigint/tostring.cc:561:3
    #4 0x55af883ee9d9 in v8::internal::BigInt::ToString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::BigInt>, int, v8::internal::ShouldThrow) src/objects/bigint.cc:964:58
    #5 0x55af875df253 in v8::internal::Builtin_Impl_BigIntPrototypeToString(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:120:37
    #6 0x55af8d874eb5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #7 0x55af8d7c08bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #8 0x55af8d7bd65b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #9 0x55af8d7bd3aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #10 0x55af879c9c07 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #11 0x55af879cc54c in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #12 0x55af87513fbd in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2034:7
    #13 0x55af87023e2e in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #14 0x55af87069243 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5670:10
    #15 0x55af87077fbf in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6691:37
    #16 0x55af8707714e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6599:18
    #17 0x55af8707c418 in v8::Shell::Main(int, char**) src/d8/d8.cc:7516:18
    #18 0x7f4bc0f30d79 in __libc_start_main csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow src/bigint/bigint.h:162:37 in v8::bigint::ProcessorImpl::DivideBarrett(v8::bigint::RWDigits, v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::RWDigits)
Shadow bytes around the buggy address:
  0x7b6bc0203300: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x7b6bc0203380: fa fa fd fa fa fa fd fa fa fa fd fd fa fa 00 00
  0x7b6bc0203400: fa fa 00 00 fa fa 00 fa fa fa 00 00 fa fa fd fd
  0x7b6bc0203480: fa fa 00 fa fa fa 00 00 fa fa 00 fa fa fa 00 fa
  0x7b6bc0203500: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa
=>0x7b6bc0203580: fa fa 00 00[fa]fa fd fd fa fa 00 fa fa fa 00 00
  0x7b6bc0203600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6bc0203680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6bc0203700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6bc0203780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b6bc0203800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1575279==ABORTING

## V8 sandbox violation detected!

```
## Additional Crash Information

**Type of crash**: v8 sandbox violation

## CREDIT INFORMATION

Reporter credit: Picasso from Dawn Security Lab, JD.com

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 2.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6199846025330688.

### ar...@google.com (2026-03-27)

I am trying to reproduce locally on commit `e6c5b6cb3a656b95eb8849d2c274f92bfd29ef32` but I always hit a CHECK:

```
./out/asan/d8 --sandbox-testing poc.js
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a7d00000000,0x7b7d00000000)
../../src/bigint/tostring.cc:421: Assertion failed: inverse_len <= inverse_.len()
Caught harmless signal (SIGABRT). Exiting process...

```

### 24...@project.gserviceaccount.com (2026-03-27)

Detailed Report: https://clusterfuzz.com/testcase?key=6199846025330688

Fuzzer: None
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  inverse_len <= inverse_.len()
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=98383:98384

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6199846025330688

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pi...@gmail.com (2026-03-28)

Yes, this may need a lot of tries as [comment3](https://issuetracker.google.com/issues/496629079#comment3) says.

Maybe run this (also need try few times):

```
for i in $(seq 1 100); do   echo "=== run $i ===";   ASAN_OPTIONS=halt_on_error=1 ./d8 --sandbox-testing ./poc.js && continue;   break; done

```

### ar...@google.com (2026-03-30)

Thanks, I confirm I was able to reproduce the sandbox violation after running it many times. In almost every run it crashes in a safe assertion, Jakob CYPTAL?

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x79b800000000,0x7ab800000000)
=================================================================
==1858484==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b209b40ccc0 at pc 0x7f00a1a20210 bp 0x7ffc19901ad0 sp 0x7ffc19901ac8
READ of size 8 at 0x7b209b40ccc0 thread T0
    #0 0x7f00a1a2020f in v8::bigint::ProcessorImpl::DivideBarrett(v8::bigint::RWDigits, v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::RWDigits) src/bigint/bigint.h:171:7
    #1 0x7f00a1a199ac in v8::bigint::(anonymous namespace)::ToStringFormatter::ProcessLevel(v8::bigint::(anonymous namespace)::RecursionLevel*, v8::bigint::Digits, char*, bool) src/bigint/tostring.cc:530:17
    #2 0x7f00a1a17d0a in v8::bigint::ProcessorImpl::ToStringImpl(char*, unsigned int*, v8::bigint::Digits&, int, bool, bool) src/bigint/tostring.cc:434:10
    #3 0x7f00a1a18626 in v8::bigint::Processor::ToString(char*, unsigned int*, v8::bigint::Digits&, int, bool) src/bigint/tostring.cc:561:3
    #4 0x7f009fc0e500 in v8::internal::BigInt::ToString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::BigInt>, int, v8::internal::ShouldThrow) src/objects/bigint.cc:964:58
    #5 0x7f009f07ea45 in v8::internal::Builtin_Impl_BigIntPrototypeToString(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:120:37
    #6 0x7f009edaadb5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #7 0x7f009ecf68c2 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #8 0x7f009ecf365b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #9 0x7f009ecf33aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #10 0x7f009f38892f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #11 0x7f009f389f38 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #12 0x7f009ef1c9ed in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2042:7
    #13 0x55583e1f864c in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #14 0x55583e2309a9 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5682:10
    #15 0x55583e23cead in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6703:37
    #16 0x55583e23c2e5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6611:18
    #17 0x55583e23fa5b in v8::Shell::Main(int, char**) src/d8/d8.cc:7528:18
    #18 0x7f009c029f74 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #19 0x7ffc1990379f  (<unknown module>)
    #20 0x2d2d0038642f6e60  (<unknown module>)

0x7b209b40ccc0 is located 0 bytes after 16-byte region [0x7b209b40ccb0,0x7b209b40ccc0)
allocated by thread T0 here:
    #0 0x55583e1c8bed in operator new[](unsigned long) (/usr/local/google/home/arashk/Code/v8/v8/out/asan/d8+0x1a1bed) (BuildId: 227eb363faf71ac2)
    #1 0x7f00a1a1907d in v8::bigint::(anonymous namespace)::ToStringFormatter::ProcessLevel(v8::bigint::(anonymous namespace)::RecursionLevel*, v8::bigint::Digits, char*, bool) src/bigint/bigint-internal.h:97:43
    #2 0x7f00a1a17d0a in v8::bigint::ProcessorImpl::ToStringImpl(char*, unsigned int*, v8::bigint::Digits&, int, bool, bool) src/bigint/tostring.cc:434:10
    #3 0x7f00a1a18626 in v8::bigint::Processor::ToString(char*, unsigned int*, v8::bigint::Digits&, int, bool) src/bigint/tostring.cc:561:3
    #4 0x7f009fc0e500 in v8::internal::BigInt::ToString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::BigInt>, int, v8::internal::ShouldThrow) src/objects/bigint.cc:964:58
    #5 0x7f009f07ea45 in v8::internal::Builtin_Impl_BigIntPrototypeToString(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:120:37
    #6 0x7f009edaadb5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #7 0x7f009ecf68c2 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #8 0x7f009ecf365b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #9 0x7f009ecf33aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #10 0x7f009f38892f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #11 0x7f009f389f38 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #12 0x7f009ef1c9ed in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2042:7
    #13 0x55583e1f864c in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #14 0x55583e2309a9 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5682:10
    #15 0x55583e23cead in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6703:37
    #16 0x55583e23c2e5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6611:18
    #17 0x55583e23fa5b in v8::Shell::Main(int, char**) src/d8/d8.cc:7528:18
    #18 0x7f009c029f74 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #19 0x7ffc1990379f  (<unknown module>)
    #20 0x2d2d0038642f6e60  (<unknown module>)

SUMMARY: AddressSanitizer: heap-buffer-overflow src/bigint/bigint.h:171:7 in v8::bigint::ProcessorImpl::DivideBarrett(v8::bigint::RWDigits, v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::Digits, v8::bigint::RWDigits)
Shadow bytes around the buggy address:
  0x7b209b40ca00: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x7b209b40ca80: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fd
  0x7b209b40cb00: fa fa 00 00 fa fa 00 00 fa fa 00 fa fa fa 00 00
  0x7b209b40cb80: fa fa fd fd fa fa 00 fa fa fa 00 00 fa fa 00 fa
  0x7b209b40cc00: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa
=>0x7b209b40cc80: fa fa 00 fa fa fa 00 00[fa]fa fd fd fa fa 00 fa
  0x7b209b40cd00: fa fa 00 00 fa fa fd fd fa fa fd fd fa fa fd fd
  0x7b209b40cd80: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x7b209b40ce00: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x7b209b40ce80: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x7b209b40cf00: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
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
==1858484==ABORTING

## V8 sandbox violation detected!

```

### dx...@google.com (2026-03-30)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705547>

[sandbox][bigint] Harden ShiftedDigits against concurrent corruption

---


Expand for full commit details
```
     
    When division algorithms left-shift a divisor or dividend, always 
    make a copy of in-sandbox values, so that subsequent operations can 
    enjoy a consistent view even under concurrent in-sandbox corruption. 
     
    Fixed: 496629079 
    Change-Id: I9e51a95df7b704a87ab42b5f89230414e5ca0062 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7705547 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Arash Kazemi <arashk@chromium.org> 
    Commit-Queue: Arash Kazemi <arashk@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106150}

```

---

Files:

- M `src/bigint/div-helpers-inl.h`

---

Hash: [bbc425dc25012f4ef2f317a79179b87cd3d750ec](https://chromiumdash.appspot.com/commit/bbc425dc25012f4ef2f317a79179b87cd3d750ec)  

Date: Mon Mar 30 15:13:17 2026


---

### 24...@project.gserviceaccount.com (2026-03-31)

ClusterFuzz testcase 6199846025330688 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=106162:106163

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pi...@gmail.com (2026-05-14)

Hello, is there any reward update?

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
v8 Sandbox


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496629079)*
