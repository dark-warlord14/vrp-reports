# V8 Sandbox Bypass: BigInt DivideSchoolbook Native Heap OOB Write via Signed Scratch-Length Overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [496807861](https://issues.chromium.org/issues/496807861) |
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

## VULNERABILITY DETAILS

### Summary

`DivideSchoolbook` computes its temporary scratch size with signed `int` locals even though the driving operand lengths come from attacker-corruptible BigInt heap metadata. By corrupting the dividend length to `0x7fffffff` and then executing `%` with a small multi-digit divisor, the signed scratch-size calculation wraps negative, the function selects a 100-digit native scratch buffer as if it were sufficient, and `LeftShift` immediately writes past that allocation using the corrupted `A.len()` as its loop bound.

### Details

The stable entry point is `BigInt::Remainder(...)`. The remainder result allocation depends only on `y`, not on the corrupted `x` length:

```
// src/objects/bigint.cc
MaybeHandle<BigInt> BigInt::Remainder(Isolate* isolate, DirectHandle<BigInt> x,
                                     DirectHandle<BigInt> y) {
  if (bigint::Compare(x->digits(), y->digits()) < 0) {
    return indirect_handle(x, isolate);
  }
  if (y->length() == 1 && y->digit(0) == 1) return Zero(isolate);
  Handle<MutableBigInt> remainder;
  uint32_t result_length = bigint::ModuloResultLength(y->digits());
  if (!MutableBigInt::New(isolate, result_length).ToHandle(&remainder)) {
    return {};
  }
  DisallowGarbageCollection no_gc;
  bigint::Digits X = x->digits();
  bigint::Digits Y = y->digits();
  bigint::RWDigits Z = remainder->rw_digits();
  auto [success, top_digit] = bigint::ModuloSmall(Z, X, Y);
  if (success) [[likely]] {
    ...
  }
  bigint::Status status = isolate->bigint_processor()->ModuloLarge(Z, X, Y);
  ...
}

```

With a 2-digit divisor, `ModuloLarge(...)` takes the schoolbook path and skips the large-length release check:

```
// src/bigint/bigint-internal.cc
Status Processor::ModuloLarge(RWDigits& R, Digits& A, Digits& B) {
  ProcessorImpl* impl = static_cast<ProcessorImpl*>(this);
  DCHECK(IsDigitNormalized(A));
  DCHECK(IsDigitNormalized(B));
  DCHECK(B.len() > 1);
  if (B.len() < config::kBurnikelThreshold) {
    RWDigits Q(nullptr, 0);
    impl->DivideSchoolbook(Q, R, A, B);
    return impl->get_and_clear_status();
  }
  CHECK(A.len() < kMaxNumDigits);
  ...
}

```

Inside `DivideSchoolbook`, the scratch requirement is computed with signed `int` temporaries:

```
// src/bigint/div-schoolbook.cc
const uint32_t n = B.len();
const uint32_t m = A.len() - n;

int qhatv_len = n + 1;
int b_normalized_storage_len = n;
int U_len = A.len() + 1;
int needed_scratch_space = qhatv_len + b_normalized_storage_len + U_len;
std::optional<ScratchDigits> allocated_scratch;
RWDigits scratch(nullptr, 0);
if (needed_scratch_space <= kSmallScratchSize) {
  scratch = GetSmallScratch();
} else {
  allocated_scratch = ScratchDigits(needed_scratch_space);
  scratch = allocated_scratch.value();
}

```

For the trigger used below:

1. `x` is a real 128-digit BigInt.
2. The attacker corrupts `x`'s length bitfield to `0x7fffffff` .
3. `y` is a 2-digit divisor, so `ModuloLarge(...)` dispatches to `DivideSchoolbook`.

That produces:

- `n = 2`
- `qhatv_len = 3`
- `b_normalized_storage_len = 2`
- `U_len = A.len() + 1 = 0x80000000`, which becomes `-2147483648` as signed `int`
- `needed_scratch_space = 3 + 2 + (-2147483648) = -2147483643`

Because the comparison is signed, `needed_scratch_space <= kSmallScratchSize` evaluates true and V8 uses a 100-digit native heap buffer.

The `U` view is then created from that scratch buffer. The slice constructor clamps the logical length to the remaining backing capacity:

```
// src/bigint/bigint.h
Digits(Digits src, uint32_t offset, uint32_t len)
    : digits_(src.digits_ + offset),
      len_(std::min(len, src.len_ > offset ? src.len_ - offset : 0)) {}

```

So with a 100-digit scratch buffer and `U` starting at offset `5`, `U.len()` becomes only `95` digits. But `LeftShift` ignores `Z.len()` for its main loop and uses the corrupted source length instead:

```
// src/bigint/div-helpers-inl.h
inline void LeftShift(RWDigits Z, Digits X, int shift) {
  DCHECK(Z.len() >= X.len());
  if (shift == 0) return Copy(Z, X);
  digit_t carry = 0;
  uint32_t i = 0;
  for (; i < X.len(); i++) {
    digit_t d = X[i];
    Z[i] = (d << shift) | carry;
    carry = d >> (kDigitBits - shift);
  }
  ...
}

```

On 64-bit builds, `RWDigits::operator[]` only has a debug check and then performs a raw `memcpy`-based write:

```
// src/bigint/bigint.h
WritableDigitReference operator[](uint32_t i) {
  BIGINT_H_DCHECK(i < len_);
  return WritableDigitReference(digits_ + i);
}

```

This means the first out-of-bounds write occurs as soon as `i == 95`, which targets `scratch[100]`, i.e. exactly the first `digit_t` past the 800-byte native allocation.

A stable trigger is therefore:

1. Create `x` as a normal 128-digit BigInt.
2. Create `y` as a normal 2-digit BigInt.
3. Corrupt `x`'s length field from `128` to `0x7fffffff`.
4. Execute `x % y` once.

## INTRODUCING COMMIT

### Bisect Result

`git blame -L 137,140 src/bigint/div-schoolbook.cc` shows that the vulnerable signed scratch-size computation was perhaps introduced by:

- `69f7a37bd6376d72ebb6cf2bbab49f88ce3a944a`
- **Date:** 2026-02-11 12:20:04 +0100
- **Subject:** `[bigint] Avoid temp allocations in DivideSchoolbook`

That commit introduced the `kSmallScratchSize` fast path and the signed locals:

- `int qhatv_len = n + 1;`
- `int b_normalized_storage_len = n;`
- `int U_len = A.len() + 1;`
- `int needed_scratch_space = ...;`

Earlier code did not contain this exact signed scratch-size fast path. In the current ancestry, `69f7a37bd637` is the effective introducing commit for this bug.

## Version

Test on V8 14.8.99:

```
git checkout 14.8.99

```
## REPRODUCTION CASE

Build `d8` with ASan + sandbox + `v8_enable_memory_corruption_api` and run:

```
ASAN_OPTIONS=halt_on_error=1 ./d8 --sandbox-testing poc.js

```

Observed crash on the current ASan build:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a1600000000,0x7b1600000000)
=================================================================
==1437907==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7cdec2be0ba0 at pc 0x55cda29160de bp 0x7ffc46b544d0 sp 0x7ffc46b544c8
WRITE of size 8 at 0x7cdec2be0ba0 thread T0
    #0 0x55cda29160dd in v8::bigint::ProcessorImpl::DivideSchoolbook(v8::bigint::RWDigits&, v8::bigint::RWDigits&, v8::bigint::Digits&, v8::bigint::Digits&) src/bigint/bigint.h:162:37
    #1 0x55cda290655f in v8::bigint::Processor::ModuloLarge(v8::bigint::RWDigits&, v8::bigint::Digits&, v8::bigint::Digits&) src/bigint/bigint-internal.cc:107:11
    #2 0x55cda017d854 in v8::internal::MutableBigInt_AbsoluteModAndCanonicalize(unsigned long, unsigned long, unsigned long, unsigned long) src/objects/bigint.cc:1694:56
    #3 0x55cda56450e8 in Builtins_BigIntModulusNoThrow setup-isolate-deserialize.cc
    #4 0x55cda56fc501 in Builtins_ModHandler setup-isolate-deserialize.cc
    #5 0x55cda55418bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #6 0x55cda553e65b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #7 0x55cda553e3aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #8 0x55cd9f74bc07 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #9 0x55cd9f74e54c in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #10 0x55cd9f295fbd in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2034:7
    #11 0x55cd9eda5e2e in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #12 0x55cd9edeb243 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5670:10
    #13 0x55cd9edf9fbf in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6691:37
    #14 0x55cd9edf914e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6599:18
    #15 0x55cd9edfe418 in v8::Shell::Main(int, char**) src/d8/d8.cc:7516:18
    #16 0x7f5ec386bd79 in __libc_start_main csu/../csu/libc-start.c:308:16

0x7cdec2be0ba0 is located 0 bytes after 800-byte region [0x7cdec2be0880,0x7cdec2be0ba0)
allocated by thread T0 here:
    #0 0x55cd9ed6c21d in operator new[](unsigned long) (/home/user/v8_build/v8/out/release_asan_14_4_201/d8+0x14bb21d) (BuildId: 0fd4e37526f252c9)
    #1 0x55cda29156f9 in v8::bigint::ProcessorImpl::DivideSchoolbook(v8::bigint::RWDigits&, v8::bigint::RWDigits&, v8::bigint::Digits&, v8::bigint::Digits&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:780:55
    #2 0x55cda290655f in v8::bigint::Processor::ModuloLarge(v8::bigint::RWDigits&, v8::bigint::Digits&, v8::bigint::Digits&) src/bigint/bigint-internal.cc:107:11
    #3 0x55cda017d854 in v8::internal::MutableBigInt_AbsoluteModAndCanonicalize(unsigned long, unsigned long, unsigned long, unsigned long) src/objects/bigint.cc:1694:56
    #4 0x55cda56450e8 in Builtins_BigIntModulusNoThrow setup-isolate-deserialize.cc
    #5 0x55cda56fc501 in Builtins_ModHandler setup-isolate-deserialize.cc
    #6 0x55cda55418bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #7 0x55cda553e65b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #8 0x55cda553e3aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #9 0x55cd9f74bc07 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #10 0x55cd9f74e54c in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #11 0x55cd9f295fbd in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2034:7
    #12 0x55cd9eda5e2e in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #13 0x55cd9edeb243 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5670:10
    #14 0x55cd9edf9fbf in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6691:37
    #15 0x55cd9edf914e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6599:18
    #16 0x55cd9edfe418 in v8::Shell::Main(int, char**) src/d8/d8.cc:7516:18
    #17 0x7f5ec386bd79 in __libc_start_main csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow src/bigint/bigint.h:162:37 in v8::bigint::ProcessorImpl::DivideSchoolbook(v8::bigint::RWDigits&, v8::bigint::RWDigits&, v8::bigint::Digits&, v8::bigint::Digits&)
Shadow bytes around the buggy address:
  0x7cdec2be0900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7cdec2be0980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7cdec2be0a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7cdec2be0a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7cdec2be0b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7cdec2be0b80: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x7cdec2be0c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7cdec2be0c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7cdec2be0d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7cdec2be0d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7cdec2be0e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1437907==ABORTING

## V8 sandbox violation detected!

```
## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

**Type of crash**: v8 sandbox violation

## CREDIT INFORMATION

Reporter credit: Picasso from Dawn Security Lab, JD.com

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 416 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6594761255321600.

### 24...@project.gserviceaccount.com (2026-03-28)

Detailed Report: https://clusterfuzz.com/testcase?key=6594761255321600

Fuzzer: None
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 0x7bd1316e0ba0
Crash State:
  v8::bigint::ProcessorImpl::DivideSchoolbook
  v8::bigint::Processor::ModuloLarge
  v8::internal::MutableBigInt_AbsoluteModAndCanonicalize
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=105238:105239

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6594761255321600

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ar...@google.com (2026-03-30)

Thanks for report. This reproduces locally and on CF, I also tried with the fix from [crrev.com/c/7706644](https://crrev.com/c/7706644) and it's not a duplicate, Jakob CYPTAL?

### dx...@google.com (2026-03-30)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7706198>

[sandbox][bigint] Harden against int overflow

---


Expand for full commit details
```
     
    Recent optimizations in crrev.com/c/7566485 introduced a sandbox 
    escape via signed int overflow on length computations. This patch 
    fixes that by switching to unsigned ints, and also adds a general 
    protective measure against possible similar bugs: we can store a 
    BigInt's length left-shifted such that decoding the field limits 
    the range, similar to how ArrayBuffer lengths are made sandbox-safe. 
     
    Fixed: 496807861 
    Change-Id: I080543010b9bf548b95743c4084ca606701212d2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7706198 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106152}

```

---

Files:

- M `src/bigint/bigint.h`
- M `src/bigint/div-schoolbook.cc`
- M `src/builtins/base.tq`
- M `src/builtins/builtins-bigint.tq`
- M `src/objects/bigint.cc`
- M `src/objects/bigint.h`
- M `src/parsing/scanner.cc`
- M `src/runtime/runtime-test.cc`
- M `src/runtime/runtime.h`
- M `test/js-perf-test/BigInt/bigint-util.js`
- M `test/mjsunit/compiler/bigint-add-no-deopt-loop.js`
- M `test/mjsunit/regress/regress-crbug-909614.js`
- M `test/mjsunit/sandbox/regress-496618662.js`
- A `test/mjsunit/sandbox/regress-496807861.js`
- M `test/mjsunit/sandbox/regress/regress-392180065.js`
- M `test/mjsunit/wasm/bigint-opt.js`

---

Hash: [3f5013f6fd674862a1293400555768e9b9006182](https://chromiumdash.appspot.com/commit/3f5013f6fd674862a1293400555768e9b9006182)  

Date: Mon Mar 30 15:01:51 2026


---

### 24...@project.gserviceaccount.com (2026-03-31)

ClusterFuzz testcase 6594761255321600 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=106151:106152

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
v8 Sanbox


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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496807861)*
