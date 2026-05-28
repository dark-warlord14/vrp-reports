# V8 Sandbox Bypass: StringToBigIntHelper stack-buffer-overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [389970331](https://issues.chromium.org/issues/389970331) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | v8...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2025-01-15 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

Converting a very long string to a `BigInt` overflows the stack buffer used during conversion. I guess some of the checks in `FromStringAccumulator::Parse` do not deal correctly with very long input arguments.

**Please note that ASAN would terminate on the read on line `bigint.h:571` before hitting the write at `bigint.h:576`, which, eventually causes memory corruption.**

#### VERSION

V8 commit: `14cbf9bdbb97057a9c1f609ace381bd086fcfd56` (2025-01-14T12:35:57+00:00)

#### REPRODUCTION CASE

Build args:

```
is_debug=false
is_asan=true
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true
dcheck_always_on=false
v8_static_library=true
v8_fuzzilli=false
target_cpu="x64"

```

Shell args: `d8 --fuzzing --sandbox-fuzzing --single-threaded --allow-natives-syntax --expose-gc bug.js`

##### ASAN Report:

```
=================================================================
==3320411==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffbde5bc00 at pc 0x55555fb58803 bp 0x7fffffff71d0 sp 0x7fffffff71c8
WRITE of size 8 at 0x7fffbde5bc00 thread T0
    #0 0x55555fb58802 in void v8::internal::StringToBigIntHelper<v8::internal::Isolate>::ParseInternal<unsigned char>(unsigned char const*) src/bigint/bigint.h:576:23
    #1 0x55555fb5742c in v8::internal::StringToBigIntHelper<v8::internal::Isolate>::ParseOneByte(unsigned char const*) src/numbers/conversions.cc:833:58
    #2 0x55555fb3b44c in v8::internal::StringToIntHelper::ParseInt() src/numbers/conversions.cc:400:5
    #3 0x55555fb39d46 in v8::internal::StringToBigIntHelper<v8::internal::Isolate>::GetResult() src/numbers/conversions.cc:839:5
    #4 0x55555fb49884 in v8::internal::StringToBigInt(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>) src/numbers/conversions.cc:923:17
    #5 0x55555fbd6070 in T<v8::internal::BigInt>::MaybeType v8::internal::BigInt::FromObject<v8::internal::Handle>(v8::internal::Isolate*, T<v8::internal::Object>) src/objects/bigint.cc:987:10
    #6 0x55555cac42c4 in v8::internal::Builtin_Impl_BigIntConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:37:5
    #7 0x55555cac0240 in v8::internal::Builtin_BigIntConstructor(int, unsigned long*, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:17:1
    #8 0x55556aee7bf5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x55556ae40e40 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #10 0x55556ae3e91b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #11 0x55556ae3e66a in Builtins_JSEntry setup-isolate-deserialize.cc
    #12 0x55555daf3de3 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:191:12
    #13 0x55555dae5d40 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:437:22
    #14 0x55555dae762d in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:537:10
    #15 0x55555c52ce34 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2156:7
    #16 0x55555c52b84c in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:2119:10
    #17 0x55555bf77bea in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1018:44
    #18 0x55555c034266 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4963:10
    #19 0x55555c051a4a in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5907:37
    #20 0x55555c04f964 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5816:18
    #21 0x55555c058cdb in v8::Shell::Main(int, char**) src/d8/d8.cc:6713:18
    #22 0x55555c05abd1 in main src/d8/d8.cc:6805:43
    #23 0x7fffbf9211c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #24 0x7fffbf92128a in __libc_start_main csu/../csu/libc-start.c:360:3
    #25 0x55555bd44029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x67f0029) (BuildId: 5715b1152b23f173)

Address 0x7fffbde5bc00 is located in stack of thread T0 at offset 1024 in frame
    #0 0x55555fb4826f in v8::internal::StringToBigInt(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>) src/numbers/conversions.cc:920

  This frame has 25 object(s):
    [32, 40) 'object.i145'
    [64, 72) 'ref.tmp.i102'
    [96, 104) 'retval.i81'
    [128, 136) 'retval.i56'
    [160, 168) 'retval.i50'
    [192, 200) 'retval.i40'
    [224, 232) 'retval.i36'
    [256, 264) 'str.i23'
    [288, 296) 'ref.tmp.i25'
    [320, 328) 'ref.tmp4.i26'
    [352, 360) 'str.i'
    [384, 392) 'ref.tmp.i19'
    [416, 424) 'ref.tmp4.i'
    [448, 456) 'retval.i'
    [480, 488) 'string.i'
    [512, 513) 'no_gc.i'
    [528, 532) 'shape.i'
    [544, 552) 'cons.i'
    [576, 600) 'ref.tmp.i'
    [640, 641) 'yes_gc.i'
    [656, 680) 'ref.tmp26.i'
    [720, 724) 'ref.tmp48.i'
    [736, 744) 'ref.tmp57.i'
    [768, 792) 'ref.tmp59.i'
    [832, 1024) 'helper' (line 922) <== Memory access at offset 1024 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow src/bigint/bigint.h:576:23 in void v8::internal::StringToBigIntHelper<v8::internal::Isolate>::ParseInternal<unsigned char>(unsigned char const*)
Shadow bytes around the buggy address:
  0x7fffbde5b980: f8 f2 f2 f2 f8 f2 f2 f2 00 f2 f2 f2 00 f2 f2 f2
  0x7fffbde5ba00: f8 f2 f8 f2 f8 f2 f2 f2 f8 f8 f8 f2 f2 f2 f2 f2
  0x7fffbde5ba80: f8 f2 f8 f8 f8 f2 f2 f2 f2 f2 f8 f2 f8 f2 f2 f2
  0x7fffbde5bb00: f8 f8 f8 f2 f2 f2 f2 f2 00 00 00 00 00 00 00 00
  0x7fffbde5bb80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7fffbde5bc00:[f3]f3 f3 f3 f3 f3 f3 f3 00 00 00 00 00 00 00 00
  0x7fffbde5bc80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fffbde5bd00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fffbde5bd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fffbde5be00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fffbde5be80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==3320411==ABORTING

## V8 sandbox violation detected!

```
#### CREDIT INFORMATION

Reporter credit: v8sbxfuzz

## Attachments

- [bug.js](attachments/bug.js) (text/javascript, 368 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-01-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5700359678787584.

### ti...@chromium.org (2025-01-15)

(primary shepherd)

I was able to reproduce this on head and stable. Thanks for the report! Assigning to the v8 shepherd sroettger@

### cl...@appspot.gserviceaccount.com (2025-01-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5570237638311936.

### jk...@chromium.org (2025-01-16)

I think the problem is that while `String`s themselves have a `uint32_t length_` as of <https://crrev.com/c/5332375>, the `StringToIntHelper` still has an `int length_`. So when in-sandbox corruption sets a string's length field to `0xFFFFFFFF`, parts of the code will think that means `-1`. In particular, `const Char* end = start + length();` (`conversions.cc:894`) won't behave as expected, which in turn causes `inline_everything_ = (end - start) <= kInlineThreshold;` (`bigint.h:525`) to make the wrong decision. The whole code path with that exceeded stack buffer (`bigint.h` around lines 571 through 576) is only meant to be used for *tiny* inputs, not for huge inputs.

Fix coming up.

### ap...@google.com (2025-01-17)

Project: v8/v8  

Branch: main  

Author: Jakob Kummerow <[jkummerow@chromium.org](mailto:jkummerow@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6179688>

[sandbox] Unsigned string lengths in conversions.cc

---


Expand for full commit details
```
[sandbox] Unsigned string lengths in conversions.cc 
 
This CL continues the work of crrev.com/c/5332375 in conversions.cc: 
it replaces most of the `int` values used there for string lengths, 
buffer lengths, and positions in strings and buffers with `size_t`. 
 
Fixed: 389970331 
Change-Id: Ie96548ebd6e491888bfc283346d7757f6d717508 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6179688 
Reviewed-by: Patrick Thier <pthier@chromium.org> 
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Patrick Thier <pthier@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98170}

```

---

Files:

- M `src/bigint/bigint.h`
- M `src/numbers/conversions.cc`

---

Hash: 7891f0516e52549b05c0d880f6b4f6b8c1ea6011  

Date:  Thu Jan 16 20:24:55 2025


---

### sp...@google.com (2025-01-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 sandbox bypass demonstrating memory corruption outside the sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-23)

Thanks for your efforts in fuzzing the V8 heap sandbox -- great work!

### ch...@google.com (2025-04-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/389970331)*
