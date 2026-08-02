# V8 SBX Trap Fuzzing: Container Overflow in src/bigint/bigint.h:163:37

| Field | Value |
|-------|-------|
| **Issue ID** | [504663582](https://issues.chromium.org/issues/504663582) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@goodmanemail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2026-04-20 |
| **Bounty** | $5,000.00 |

## Description

PREAMBLE
I spotted in 5df56c210ed6398cd4ce2f1f37a070a8af9ec175 Samuel Groß has added a new argument in d8: --sandbox-trap-fuzzing.  After attempting (stupidly?) to get this working in Fuzzilli I figured that the results of running this over an existing corpus appear at odds to what you normally want in a fuzzer.  It seems to kinda be its own fuzzer?  Regardless I've rammed my well developed Fuzzilli corpus through it a few dozen times and got some interesting looking sandbox violations.  Sadly I've no idea what to do with the output so I thought I would report some of the unique ones here to test the waters...

VULNERABILITY DETAILS
SUMMARY: AddressSanitizer: container-overflow src/bigint/bigint.h:163:37 in v8::bigint::ProcessorImpl::MultiplyFFT(v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits)

## V8 sandbox violation detected!

VERSION
V8 66e743448ed44d092b179fe2aa544c161e1934a0
Operating System: Ubuntu 24.04

REPRODUCTION CASE
Attached

GN ARGS:
is_debug = false
is_asan = true
is_component_build = false
v8_monolithic = true
target_cpu = "x64"
v8_enable_sandbox = true
v8_enable_sandbox_hardware_support = true
v8_enable_pointer_compression = true
v8_enable_verify_heap = false
v8_enable_object_print = false
v8_static_library = false
v8_use_external_startup_data = false
v8_fuzzilli = true
symbol_level = 1
v8_enable_disassembler = true
v8_enable_backtrace = true
dcheck_always_on = false
v8_enable_code_coverage = true
sanitizer_coverage_flags = "trace-pc-guard"

Command line:

/home/alan/v8/v8/out/v8sandbox/d8 --fuzzing --sandbox-testing --sandbox-fuzzing --sandbox-trap-fuzzing --allow-natives-syntax --expose-gc --expose-gc --expose-externalize-string --omit-quit --allow-natives-syntax --fuzzing --future --harmony --experimental-fuzzing --js-staging --wasm-staging --wasm-fast-api --expose-fast-api

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
=================================================================
==2873400==ERROR: AddressSanitizer: container-overflow on address 0x7bfff6c1f328 at pc 0x55555b27bb6d bp 0x7fffffffc9f0 sp 0x7fffffffc9e8
WRITE of size 8 at 0x7bfff6c1f328 thread T0
    #0 0x55555b27bb6c in v8::bigint::ProcessorImpl::MultiplyFFT(v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits) src/bigint/bigint.h:163:37
    #1 0x55555b245c15 in v8::bigint::ProcessorImpl::MultiplyLarge(v8::bigint::RWDigits&, v8::bigint::Digits&, v8::bigint::Digits&) src/bigint/bigint-internal.cc:57:10
    #2 0x55555b245646 in v8::bigint::ProcessorImpl::Multiply(v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits) src/bigint/bigint-internal.cc:44:10
    #3 0x55555b25a241 in v8::bigint::ProcessorImpl::FromStringLarge(v8::bigint::RWDigits, v8::bigint::FromStringAccumulator*) src/bigint/fromstring.cc:162:7
    #4 0x55555b25e613 in v8::bigint::Processor::FromString(v8::bigint::RWDigits, v8::bigint::FromStringAccumulator*) src/bigint/fromstring.cc:325:9
    #5 0x555558f1b621 in v8::internal::MaybeHandle<v8::internal::BigInt> v8::internal::BigInt::Allocate<v8::internal::Isolate>(v8::internal::Isolate*, v8::bigint::FromStringAccumulator*, bool, v8::internal::AllocationType) src/objects/bigint.cc:1257:36
    #6 0x555558eede11 in v8::internal::StringToBigInt(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>) src/numbers/conversions.cc:1110:17
    #7 0x555558f2aa99 in v8::internal::BigInt::CompareToString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::BigInt>, v8::internal::DirectHandle<v8::internal::String>) src/objects/bigint.cc:695:40
    #8 0x555559a2fb67 in v8::internal::Runtime_BigIntCompareToString(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-bigint.cc:30:7
    #9 0x55555e298bd4 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #10 0x55555e3c4307 in Builtins_TestLessThanHandler setup-isolate-deserialize.cc
    #11 0x55555e1d2a56 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x55555e1cf738 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #13 0x55555e1cf3c9 in Builtins_JSEntry setup-isolate-deserialize.cc
    #14 0x55555846f8c9 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #15 0x555558472609 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:575:10
    #16 0x555557ef31eb in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2042:7
    #17 0x555557be423c in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1043:44
    #18 0x555557c3068d in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5838:32
    #19 0x555557c401b3 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6878:37
    #20 0x555557c3f4c2 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6786:18
    #21 0x555557c44588 in v8::Shell::Main(int, char**) src/d8/d8.cc:7718:18
    #22 0x7ffff7c2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #23 0x7ffff7c2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #24 0x555557ad1029 in _start (/home/alan/v8/v8/out/v8sandbox/d8+0x257d029) (BuildId: ab30bf5b005f9f89)

0x7bfff6c1f328 is located 88872 bytes inside of 131072-byte region [0x7bfff6c09800,0x7bfff6c29800)
allocated by thread T0 here:
    #0 0x555557baa2ad in operator new(unsigned long) (/home/alan/v8/v8/out/v8sandbox/d8+0x26562ad) (BuildId: ab30bf5b005f9f89)
    #1 0x5555583edee0 in unsigned long* std::__Cr::vector<unsigned long, std::__Cr::allocator<unsigned long>>::__emplace_back_slow_path<unsigned long const&>(unsigned long const&) gen/third_party/libc++/src/include/__new/allocate.h:42:28
    #2 0x555558ef71c4 in void v8::internal::StringToBigIntHelper<v8::internal::Isolate>::ParseInternal<unsigned char>(unsigned char const*) gen/third_party/libc++/src/include/__vector/vector.h:1148:21
    #3 0x555558ee7e44 in v8::internal::StringToIntHelper::ParseInt() src/numbers/conversions.cc
    #4 0x555558ee5fd4 in v8::internal::StringToBigIntHelper<v8::internal::Isolate>::GetResult() src/numbers/conversions.cc:1026:5
    #5 0x555558eede11 in v8::internal::StringToBigInt(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>) src/numbers/conversions.cc:1110:17
    #6 0x555558f2aa99 in v8::internal::BigInt::CompareToString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::BigInt>, v8::internal::DirectHandle<v8::internal::String>) src/objects/bigint.cc:695:40
    #7 0x555559a2fb67 in v8::internal::Runtime_BigIntCompareToString(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-bigint.cc:30:7
    #8 0x55555e298bd4 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #9 0x55555e3c4307 in Builtins_TestLessThanHandler setup-isolate-deserialize.cc
    #10 0x55555e1d2a56 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #11 0x55555e1cf738 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #12 0x55555e1cf3c9 in Builtins_JSEntry setup-isolate-deserialize.cc
    #13 0x55555846f8c9 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #14 0x555558472609 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:575:10
    #15 0x555557ef31eb in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2042:7
    #16 0x555557be423c in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1043:44
    #17 0x555557c3068d in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5838:32
    #18 0x555557c401b3 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6878:37
    #19 0x555557c3f4c2 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6786:18
    #20 0x555557c44588 in v8::Shell::Main(int, char**) src/d8/d8.cc:7718:18
    #21 0x7ffff7c2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #22 0x7ffff7c2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #23 0x555557ad1029 in _start (/home/alan/v8/v8/out/v8sandbox/d8+0x257d029) (BuildId: ab30bf5b005f9f89)

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
Or if supported by the container library, pass -D__SANITIZER_DISABLE_CONTAINER_OVERFLOW__ to the compiler to disable  instrumentation.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow src/bigint/bigint.h:163:37 in v8::bigint::ProcessorImpl::MultiplyFFT(v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits)
Shadow bytes around the buggy address:
  0x7bfff6c1f080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfff6c1f100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfff6c1f180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfff6c1f200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bfff6c1f280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bfff6c1f300: 00 00 00 00 00[fc]fc fc fc fc fc fc fc fc fc fc
  0x7bfff6c1f380: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x7bfff6c1f400: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x7bfff6c1f480: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x7bfff6c1f500: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x7bfff6c1f580: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
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
==2873400==ABORTING
Cannot check if faulting address lies inside a know-safe memory region. Falling back to generic checks. Results will be inaccurate

## V8 sandbox violation detected!

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Alan Goodman

## Attachments

- [program_20260324001909_8EFCCC45-5108-4285-9BC1-DEEA07A0D626.js](attachments/program_20260324001909_8EFCCC45-5108-4285-9BC1-DEEA07A0D626.js) (text/javascript, 58 B)
- [program_20260324001909_8EFCCC45-5108-4285-9BC1-DEEA07A0D626.js.log](attachments/program_20260324001909_8EFCCC45-5108-4285-9BC1-DEEA07A0D626.js.log) (text/plain, 23.0 KB)
- [bigint_validation.patch](attachments/bigint_validation.patch) (text/x-diff, 2.6 KB)

## Timeline

### ar...@google.com (2026-04-21)

Delegating to the current V8 security shepherd.

### ml...@google.com (2026-04-21)

Note that we need an actual POC here to consider this bug: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/sandbox/trap-fuzzer.cc;l=140;drc=5df56c210ed6398cd4ce2f1f37a070a8af9ec175>

Reporter: Can you provide one?

### al...@goodmanemail.com (2026-04-21)

PoC is attached and includes the necessary to reproduce the crash. Sadly the process to get from that information back to the crash (eg "replay the steps") isn't publicly documented and I haven't figured it out.. yet. It must be possible to replicate the crashers as the "fuzzer" has generated multiple examples of each crash (I've got half a dozen unique looking ones)

### ml...@google.com (2026-04-21)

The POC requires applying the log in a structured way which is not yet possible. Since you took an unfinished fuzzer and immediately reported an issue: Can you build infrastructure to apply the log?

### sa...@google.com (2026-04-21)

@Reporter yeah you need look at the logs and recover the bug (and then build an actual reproducer testcase) from it as [this message](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/sandbox/trap-fuzzer.cc;l=141;drc=5df56c210ed6398cd4ce2f1f37a070a8af9ec175) tries to explain. That's what I did manually (and/or with gemini) for [these bugs](https://project-zero.issues.chromium.org/issues?q=componentid:1638259%20%22V8%20Sandbox%20Bypass%22) :)

### al...@goodmanemail.com (2026-04-22)

Please be kind to me on this one... This is the first time I've ever tried to do anything like this!! I cant get the memory corruption api to do what I need. So I've replicated the crash with some targeted modification of the code; with an extremely heavy pinch of LLM skill!

```
diff --git a/src/bigint/mul-fft.cc b/src/bigint/mul-fft.cc      
  index c9131da0918..59da4f5c0aa 100644                                                                                                                                                 
  --- a/src/bigint/mul-fft.cc                                                                                                                                                           
  +++ b/src/bigint/mul-fft.cc                                                                                                                                                           
  @@ -620,18 +620,34 @@ void FFTContainer::NormalizeAndRecombine(int omega, int m, RWDigits Z,                                                                                          
     Z.Clear();                                                                                                                                                                         
     uint32_t z_index = 0;                                                                                                                                                              
     const int shift = n_ * omega - m;                                                                                                                                                  
  +                                                                                                                                                                                     
     for (uint32_t i = 0; i < n_; i++, z_index += chunk_size) {                                                                                                                         
       digit_t* part = part_[i];                                                                                                                                                        
       ShiftModFn(temp(), part, shift, K_);                                                                                                                                             
  +                                                                                                                                                                                     
       digit_t carry = 0;                                                                                                                                                               
       uint32_t zi = z_index;                                                                                                                                                           
       uint32_t j = 0;                                                                                                                                                                  
       for (; j < length_ && zi < Z.len(); j++, zi++) {                                                                                                                                 
         Z[zi] = digit_add3(Z[zi], temp_[j], carry, &carry);                                                                                                                            
       }                                                                                                                                                                                
  +                                                                                                                                                                                     
       for (; j < length_; j++) {                                                                                                                                                       
         DCHECK(temp_[j] == 0);                                                                                                                                                         
       }                                                                                                                                                                                
  +                                                                                                                                                                                     
  +    // CORRUPTION INJECTION: Simulate trap-fuzzer causing incorrect computation.                                                                                                     
  +    // The trap-fuzzer mutated FFT intermediate values during execution, causing                                                                                                     
  +    // the computation to produce results larger than expected. When Z buffer is                                                                                                     
  +    // undersized (Z.len() < n_ * chunk_size) and we reach the boundary,                                                                                                             
  +    // this forces a carry that overflows past Z.len().                                                                                                                              
  +    uint32_t expected_total = n_ * chunk_size;                                                                                                                                       
  +    bool undersized = Z.len() < expected_total;                                                                                                                                      
  +    if (undersized && Z.len() > 100 && zi == Z.len()) {                                                                                                                              
  +      carry = 1;  // Force non-zero carry to trigger the overflow bug                                                                                                                
  +    }                                                                                                                                                                                
  +                                                                                                                                                                                     
  +    // BUG: Carry written without bounds checking.                                                                                                                                   
       if (carry != 0) {                                                                                                                                                                
         Z[zi] = carry;                                                                                                                                                                 
       }                                                                                                                                                                                
  @@ -733,6 +749,7 @@ void FFTContainer::DoPointwiseMultiplication(const FFTContainer& other,                                                                                           
     bool use_fft = length_ >= config::kFftInnerThreshold && (K_ & 3) == 0;                                                                                                             
     Parameters params;                                                                                                                                                                 
     if (use_fft) ComputeParameters_Inner(K_, &params);                                                                                                                                 
  +                                                                                                                                                                                     
     RWDigits result(temp, 2 * length_);                                                                                                                                                
     for (uint32_t i = start; i < end; i++) {                                                                                                                                           
       Digits A(part_[i], length_);

```

Root cause analysis:
Root Cause: In FFTContainer::NormalizeAndRecombine(), a carry value is written to the output buffer Z without bounds checking. When memory corruption (via trap-fuzzer or other means) causes FFT computation to produce unexpectedly large results, and the output buffer is undersized (Z.len() < n\_ \* chunk\_size), the carry write overflows past the allocated buffer boundary.

Vulnerable Code Pattern:

```
  for (; j < length_ && zi < Z.len(); j++, zi++) {
    Z[zi] = digit_add3(Z[zi], temp_[j], carry, &carry);                                                                                                                                 
  }                                                                                                                                                                                     
  // BUG: No bounds check before writing carry!                                                                                                                                         
  if (carry != 0) {                                                                                                                                                                     
    Z[zi] = carry;  // Overflows when zi == Z.len()                                                                                                                                     
  }      
                                                                                                                                                                               

```

Attack Vector: The trap-fuzzer's memory mutations corrupt FFT intermediate values, causing the computation to produce results larger than expected. When combined with an undersized output buffer (which can occur during BigInt parsing of large strings), this triggers a container overflow at offset 88,872 bytes into a 131,072-byte region.

Note: there is a heavy hint of LLM going on here and this is the first time I've leaned on an LLM in any of my reporting. Doing so tears me up inside with worry because I think you deserve better from me... But sadly on my own I didnt have the skill to pull this off. I've personally verified the results of the above and I'm reasonably happy it looks correct.

For the avoidance of doubt, I've used a locally hosted LLM for this work which means I've not disclosed any details of this potential issue to anybode else.

I also think there is partial control possible over the write:

```
  Address Control Mechanism

  // Input parameters → String length → FFT params (n, K, s) → Buffer size → Overflow offset
  const arr = new Int32Array(SIZE);  // Controls string length
  arr.join(SEP);                     // Affects digit parsing and FFT chunking

  Demonstrated Control Range

  By varying array.size and separator, we achieved overflow at three different offsets:
  - 88,872 bytes (11,109 digits) - original case
  - 92,632 bytes (11,579 digits) - 55000×150
  - 117,896 bytes (14,737 digits) - 50000×100

```

### ch...@google.com (2026-04-22)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-22)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### jk...@chromium.org (2026-04-22)

I don't think there's anything here.

We used to have a concurrent-modification sandbox escape there, we fixed it with <https://chromium-review.googlesource.com/c/v8/v8/+/7581282>  

Then we switched to a sandbox allocator for temp buffers, so `Z` is now always in-sandbox: <https://chromium-review.googlesource.com/c/v8/v8/+/7713563>  

Which allowed us to clean up the extra bounds checks again: <https://chromium-review.googlesource.com/c/v8/v8/+/7775793>

So if you're claiming that there's still (or again?) a sandbox escape there, I'd like to see stronger evidence than a C++ patch that causes some experimental fuzzer to produce an ASan report that may or may not be spurious.

### al...@goodmanemail.com (2026-04-22)

The experimental fuzzer found the 'crash' depicted in #1 using tip of tree 66e743448ed44d092b179fe2aa544c161e1934a0 which I think includes patches mentioned in #10?

I believe the patched code exactly resembles the corruption detailed in the log attached to #1

I've done my best to replicate the method of demonstration used in example <https://project-zero.issues.chromium.org/issues/478814344> as I dont see any other way to replicate these issues?

I dont even fully understand this sandbox stuff; however I presume you're trying to find situations where in sandbox corruption causes outside sandbox reads or writes...

P.S. my replication does not use the experimental fuzzer thingy because that would go off causing its own random corruptions...

### sa...@google.com (2026-04-22)

I'm wondering if [this](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/numbers/conversions.cc;l=1065;drc=ef40f0628efc7e9c15b6f28edd69aa76480f064d) is maybe a place where we still allocate temp buffers outside of the sandbox? Could we enforce that all `bigint::Digit`s always live inside the sandbox with some strategically-placed DCHECKs?

### sa...@google.com (2026-04-22)

> Could we enforce that all bigint::Digits always live inside the sandbox with some strategically-placed DCHECKs?

I gave that a shot (see attachment) and indeed there are a few tests that fail with that:

```
=== mjsunit/harmony/bigint/regress-tostring-2 ===
../../src/bigint/bigint.h:89: Assertion failed: v8::bigint::ValidateBigIntBuffer(mem, len)
Received signal 6

==== C stack trace ===============================

/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8_libbase.so(_ZN2v84base5debug10StackTraceC2Ev+0x1e) [0x7f7bbc1f458e]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8_libbase.so(+0x4c4d6) [0x7f7bbc1f44d6]
/usr/lib/x86_64-linux-gnu/libc.so.6(+0x40a70) [0x7f7bbb840a70]
/usr/lib/x86_64-linux-gnu/libc.so.6(+0x973dc) [0x7f7bbb8973dc]
/usr/lib/x86_64-linux-gnu/libc.so.6(gsignal+0x12) [0x7f7bbb840942]
/usr/lib/x86_64-linux-gnu/libc.so.6(abort+0x22) [0x7f7bbb8284ac]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8.so(+0x43fe989) [0x7f7bc05fe989]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8.so(_ZN2v86bigint13ProcessorImpl15FromStringLargeENS0_8RWDigitsEPNS0_21FromStringAccumulatorE+0x64) [0x7f7bc1b18984]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8.so(_ZN2v86bigint9Processor10FromStringENS0_8RWDigitsEPNS0_21FromStringAccumulatorE+0xe) [0x7f7bc1b1a0ee]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8.so(_ZN2v88internal6BigInt8AllocateINS0_7IsolateEEENS0_11MaybeHandleIS1_EEPT_PNS_6bigint21FromStringAccumulatorEbNS0_14AllocationTypeE+0x8c) [0x7f7bc0605abc]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8.so(_ZN2v88internal14StringToBigIntEPNS0_7IsolateENS0_12DirectHandleINS0_6StringEEE+0x103) [0x7f7bc05f09d3]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8.so(_ZN2v88internal6BigInt10FromObjectINS0_6HandleEQsr3stdE16is_convertible_vIT_INS0_6ObjectEENS0_12DirectHandleIS5_EEEEENS4_IS1_E9MaybeTypeEPNS0_7IsolateES6_+0x262) [0x7f7bc0605722]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8.so(+0x3af9154) [0x7f7bbfcf9154]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8.so(_ZN2v88internal25Builtin_BigIntConstructorEiPmPNS0_7IsolateE+0x7d) [0x7f7bbfcf8cdd]
/usr/local/google/home/saelo/Workspace/v8/v8/out/x64.optdebug/libv8.so(+0x2dd0dbd) [0x7f7bbefd0dbd]
[end of stack trace]
Command: out/x64.optdebug/d8 --test test/mjsunit/mjsunit.js test/mjsunit/harmony/bigint/regress-tostring-2.js --random-seed=479103188 --nohard-abort --verify-heap
--- FAILED ---

```

So there might be something here. Jakob WDYT about integrating a patch like the one here? It's not super nice as it needs to thread `IsInsideSandbox` through to the low-level bigint constructor, but not sure there's a better way. If we ever get to the point where we can have sandbox enforcement for C++ code (i.e. no writes outside the sandbox + stack, basically) then we won't need this anymore, but that'll probably be a while still.

### jk...@chromium.org (2026-04-23)

OK, this is kind of the opposite of the problem we had before: now that the temporary buffers are allocated inside the sandbox (and hence vulnerable to corruption), the rotating-buffer scheme means we can't operate on out-of-sandbox *inputs* any more.

Fix: <https://chromium-review.googlesource.com/c/v8/v8/+/7790150>

### al...@goodmanemail.com (2026-04-23)

I had a solid go at writing a PoC for this using the memory corruption api; but I couldnt replicate the exact scenario. It seems the big int code computes bounds based upon a corrupted length from within the sandbox however it seems when I corrupt that length I often run into a check; so maybe this situation depends upon the corrupt after N accesses logic, making it potentially impossible to replicate using the tooling we have.

### dx...@google.com (2026-04-24)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7790150>

[sandbox][bigint] Move more storage into the sandbox

---


Expand for full commit details
```
     
    The recent move to in-sandbox buffers missed two cases of digits 
    that are stored in vectors. To consistently confine any possible 
    corruption to the sandbox, these need to be allocated inside the 
    sandbox as well. 
     
    Fixed: 504663582 
    Change-Id: I2dac81e040b427b28e0d6f1c9e8172318679448e 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7790150 
    Reviewed-by: Samuel Groß <saelo@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Samuel Groß <saelo@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106810}

```

---

Files:

- M `src/bigint/bigint-inl.h`
- M `src/bigint/fromstring.cc`
- M `src/numbers/conversions.cc`
- M `test/bigint/bigint-shell.cc`

---

Hash: [286971150a3820ab365bc7937fd8887f0eb4dbd0](https://chromiumdash.appspot.com/commit/286971150a3820ab365bc7937fd8887f0eb4dbd0)  

Date: Thu Apr 23 12:58:22 2026


---

### jk...@chromium.org (2026-04-27)

Note for VRP panel: there is plausible evidence here that in theory in-sandbox corruption could be used to trigger an out-of-sandbox OOB write; however an actual repro has not been produced, and I agree that this seems supremely difficult to actually trigger in practice.

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

### ch...@google.com (2026-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504663582)*
