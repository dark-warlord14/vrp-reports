# V8 Sandbox Bypass: BigInt CachedMod Heap-Buffer-Overflow on C++ Heap

| Field | Value |
|-------|-------|
| **Issue ID** | [490769268](https://issues.chromium.org/issues/490769268) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2026-03-08 |
| **Bounty** | $20,000.00 |

## Description

## VULNERABILITY DETAILS

A heap-buffer-overflow in V8's BigInt `CachedMod()` [1] function allows **arbitrary write (AAW) to the C++ heap outside the V8 sandbox**. By corrupting a BigInt's `bitfield_` [2] (an in-sandbox write), an attacker can inflate the divisor's reported digit-length while the cached Barrett inverse retains its genuine (small) size. The runtime guard `X.len() <= 2 * Y.len()` [3] reads the corrupted length and passes. This mismatch causes `CachedMod` to compute an oversized scratch space requirement and call `MultiplySchoolbook` [4] with a length that overflows the fixed 800-byte `small_scratch_` buffer [5] allocated on the C++ heap via `std::make_unique` [6]. The four `DCHECK` guards [7] that would catch this invariant violation are stripped in production builds.

We can control both the **values** written (via the dividend's digit contents) and the **distance** of the OOB write (via the corrupted divisor length). The adjacent PartitionAlloc slot contains a `DateCache` object [8] whose vtable pointer can be overwritten with an attacker-chosen address, redirecting virtual dispatch outside the sandbox.

[1] <https://source.chromium.org/chromium/chromium/src/+/95dc352b79cc7f77adc1a824d6a9e8ed6f619ad6:v8/src/bigint/bigint-inl.h;l=941-986>

[2] <https://source.chromium.org/chromium/chromium/src/+/95dc352b79cc7f77adc1a824d6a9e8ed6f619ad6:v8/src/objects/bigint.h;l=114-155>

[3] <https://source.chromium.org/chromium/chromium/src/+/95dc352b79cc7f77adc1a824d6a9e8ed6f619ad6:v8/src/objects/bigint.cc;l=1655>

[4] <https://source.chromium.org/chromium/chromium/src/+/95dc352b79cc7f77adc1a824d6a9e8ed6f619ad6:v8/src/bigint/bigint-inl.h;l=726-773>

[5] <https://source.chromium.org/chromium/chromium/src/+/95dc352b79cc7f77adc1a824d6a9e8ed6f619ad6:v8/src/bigint/bigint.h;l=346-358>

[6] <https://source.chromium.org/chromium/chromium/src/+/95dc352b79cc7f77adc1a824d6a9e8ed6f619ad6:v8/src/bigint/bigint.h;l=350-352>

[7] <https://source.chromium.org/chromium/chromium/src/+/95dc352b79cc7f77adc1a824d6a9e8ed6f619ad6:v8/src/bigint/bigint-inl.h;l=944-947>

[8] <https://source.chromium.org/chromium/chromium/src/+/95dc352b79cc7f77adc1a824d6a9e8ed6f619ad6:v8/src/date/date.h;l=18-45>

## VERSION

- V8 version: 14.7.0 ([d8-release-105658](https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-release%2Fd8-asan-sandbox-testing-linux-release-v8-component-105658.zip?generation=1772995989259638&alt=media) and `7cb7e0e4ae1d6a858f4922aa9399c1c307740e78` commit of V8)
- OS: All (tested on Linux x86-64)

## REPRODUCTION CASE

The attached PoC can trigger the V8 sandbox violation in both ASan and release modes. Only `--sandbox-testing` and `--expose-gc` flags are required for the testing.

### Release

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7b6500000000,0x7c6500000000)
[*] triggering OOB write: scratch[112] = 0x414141414000
[+] OOB write survived — DateCache vtable overwritten with 0x414141414000
[*] triggering DateCache virtual call...

## V8 sandbox violation detected!

The sandbox violation was a *read* access which is technically not a sandbox violation. This requires manual investigation.
Received signal 11 SEGV_MAPERR 414141414010

==== C stack trace ===============================

./out/x64.release/d8(+0x1c1cf2f)[0x63b0b7029f2f]
./out/x64.release/d8(+0xd32215)[0x63b0b613f215]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7ca6c2a42520]
./out/x64.release/d8(+0x77bcab)[0x63b0b5b88cab]
./out/x64.release/d8(+0x6e384e)[0x63b0b5af084e]
./out/x64.release/d8(+0x1ab9bf6)[0x63b0b6ec6bf6]
[end of stack trace]
[1]    3855637 segmentation fault (core dumped)  ./out/x64.release/d8 --sandbox-testing --expose-gc audit/v8-kzww/poc_aaw2.js

```
### ASan-enabled

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x776c00000000,0x786c00000000)
[*] triggering OOB write: scratch[112] = 0x414141414000
=================================================================
==3856597==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7a2db65e0ba0 at pc 0x61dcea041bae bp 0x7ffec7ed1020 sp 0x7ffec7ed1018
WRITE of size 8 at 0x7a2db65e0ba0 thread T0
    #0 0x61dcea041bad in v8::bigint::MultiplySchoolbook(v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits) src/bigint/bigint.h:162:37
    #1 0x61dcea03382d in v8::internal::MutableBigInt_AbsoluteModAndCanonicalize(unsigned long, unsigned long, unsigned long) src/bigint/bigint-inl.h
    #2 0x61dcedf2ad65 in Builtins_BigIntModulusNoThrow setup-isolate-deserialize.cc
    #3 0x61dcedfde5c1 in Builtins_ModHandler setup-isolate-deserialize.cc
    #4 0x61dcede2a8bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #5 0x61dcede2765b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #6 0x61dcede273aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #7 0x61dce9859dc6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #8 0x61dce985b338 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #9 0x61dce94616ab in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2033:7
    #10 0x61dce919efc7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1039:44
    #11 0x61dce91d78a9 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5661:10
    #12 0x61dce91e3dad in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6680:37
    #13 0x61dce91e31e5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6588:18
    #14 0x61dce91e694b in v8::Shell::Main(int, char**) src/d8/d8.cc:7502:18
    #15 0x7cadb7429d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x7a2db65e0ba0 is located 0 bytes after 800-byte region [0x7a2db65e0880,0x7a2db65e0ba0)
allocated by thread T0 here:
    #0 0x61dce916f50d in operator new[](unsigned long) (/home/inthewild/chromium/260306/v8/out/x64.asan/d8+0x142950d) (BuildId: 586cf5bea52f3013)
    #1 0x61dcebb5d0a4 in v8::bigint::ProcessorImpl::DivideSchoolbook(v8::bigint::RWDigits&, v8::bigint::RWDigits&, v8::bigint::Digits&, v8::bigint::Digits&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:780:55
    #2 0x61dcebb522ff in v8::bigint::Processor::ModuloLarge(v8::bigint::RWDigits&, v8::bigint::Digits&, v8::bigint::Digits&) src/bigint/bigint-internal.cc:107:11
    #3 0x61dcea035279 in v8::internal::MutableBigInt_AbsoluteModAndCanonicalize(unsigned long, unsigned long, unsigned long) src/objects/bigint.cc:1692:56
    #4 0x61dcedf2ad65 in Builtins_BigIntModulusNoThrow setup-isolate-deserialize.cc
    #5 0x61dcedfde5c1 in Builtins_ModHandler setup-isolate-deserialize.cc
    #6 0x61dcede2a8bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #7 0x61dcede2765b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #8 0x61dcede273aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #9 0x61dce9859dc6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:216:12
    #10 0x61dce985b338 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #11 0x61dce94616ab in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2033:7
    #12 0x61dce919efc7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1039:44
    #13 0x61dce91d78a9 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5661:10
    #14 0x61dce91e3dad in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6680:37
    #15 0x61dce91e31e5 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6588:18
    #16 0x61dce91e694b in v8::Shell::Main(int, char**) src/d8/d8.cc:7502:18
    #17 0x7cadb7429d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-buffer-overflow src/bigint/bigint.h:162:37 in v8::bigint::MultiplySchoolbook(v8::bigint::RWDigits, v8::bigint::Digits, v8::bigint::Digits)
Shadow bytes around the buggy address:
  0x7a2db65e0900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a2db65e0980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a2db65e0a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a2db65e0a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a2db65e0b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a2db65e0b80: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x7a2db65e0c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a2db65e0c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a2db65e0d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a2db65e0d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7a2db65e0e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==3856597==ABORTING

## V8 sandbox violation detected!

```

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 3.2 KB)
- [poc_write_violation.js](attachments/poc_write_violation.js) (text/javascript, 1.2 KB)
- [poc_rip_control.js](attachments/poc_rip_control.js) (text/javascript, 7.2 KB)

## Timeline

### de...@gmail.com (2026-03-09)

Sorry, the initial bug report contained incorrect information. The originally attached PoC is technically a read access violation with a controlled address. I have attached a simplified PoC that triggers a write access violation of the V8 sandbox. I will share additional details if AAW is confirmed.

### jd...@chromium.org (2026-03-09)

Adding TENTATIVE severity to aid in triage.

### jd...@chromium.org (2026-03-09)

Forwarding to v8 security shepherd

### ch...@google.com (2026-03-10)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-03-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-10)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### de...@gmail.com (2026-03-10)

I attached an improved PoC that controls RIP. You can still use `--sandbox-testing --expose-gc` flags for the reproduction. Note that the attached PoC is a bit unstable, meaning it requires multiple attempts to trigger the sandbox violation.

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x167400000000,0x177400000000)
=== BigInt CachedMod: Vtable Hijack Chain ===

Chain: OOB write -> DateCache vtable corruption -> fake vtable in sandbox
       -> virtual dispatch -> code execution at attacker-chosen address

Sandbox base:  0x167400000000
TARGET_ADDR:   0x414141414141 (attacker-chosen)

[*] Step 1: Warming up CachedMod (110 iterations)...
    y @ sandbox+0x1026420, length=2

[*] Step 2: Creating fake vtable in sandbox...
    Fake vtable at full addr: 0x1674010800d8
    All 32 slots contain:     0x414141414141

[*] Step 3: Setting up x digits for OOB...
    X[112] = 0xffffe98bfef7ff28
    -> Z[112] = 0x1674010800d8 (DateCache vtable overwrite)

[*] Step 4: Corrupting y.bitfield_ and setting shield digits...
    y.bitfield_ corrupted: length=58 (was 2)

[*] Step 5: Triggering OOB (x % y)...
[+] OOB survived! DateCache vtable now points to fake vtable in sandbox.

=======================================================================
 CHAIN SUMMARY

 1. OOB write to DateCache vtable (scratch_ptr + 0x380):
    VALUE written: 0x1674010800d8
    (attacker-chosen sandbox address of fake vtable)

 2. Fake vtable in sandbox memory:
    Every slot = 0x414141414141
    (attacker-chosen code execution target)

 3. Virtual dispatch reads TARGET_ADDR from fake vtable -> jumps there
    Expected crash: RIP = 0x414141414141

 VALUE CONTROL: OOB carry chain writes any 64-bit value to any
   position in the ~1.6MB range (here: FAKE_VTABLE_FULL to pos 112)
 ADDRESS CONTROL: fake vtable redirects execution to TARGET_ADDR
   (here: 0x414141414141, can be any canonical addr)
=======================================================================

[!] Triggering new Date().toString()...
[!] Expected: V8 sandbox violation at 0x414141414141


## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 414141414141
[1]    2340440 segmentation fault (core dumped)  ./out/x64.release/d8 --sandbox-testing --expose-gc 

```

### cl...@appspot.gserviceaccount.com (2026-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6059941089443840.

### 24...@project.gserviceaccount.com (2026-03-11)

Detailed Report: https://clusterfuzz.com/testcase?key=6059941089443840

Fuzzer: None
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 0x773534ee0ba0
Crash State:
  v8::bigint::MultiplySchoolbook
  v8::internal::MutableBigInt_AbsoluteModAndCanonicalize
  Builtins_BigIntModulusNoThrow
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=105566:105567

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6059941089443840

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### bi...@chromium.org (2026-03-11)

Jakob, could you ptal?

### jk...@chromium.org (2026-03-11)

FWIW, the repro in #2 does not reproduce anything for me. The repro in #8 is successful though. Fix coming up.

### dx...@google.com (2026-03-12)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7657784>

[sandbox][bigint] Harden CachedMod against corruption

---


Expand for full commit details
```
     
    by caching the divisor along with its inverse. 
     
    Fixed: 490769268 
    Change-Id: Iceb5cd0be9188dfd6f727f2f4bffe3810d236f31 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7657784 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105752}

```

---

Files:

- M `src/bigint/bigint-inl.h`
- M `src/bigint/bigint-internal.cc`
- M `src/bigint/bigint.h`
- M `src/objects/bigint.cc`
- M `test/bigint/bigint-shell.cc`
- A `test/mjsunit/sandbox/regress-490769268.js`

---

Hash: [f875f0bb18961935cb76c2b204acef7bd30048e0](https://chromiumdash.appspot.com/commit/f875f0bb18961935cb76c2b204acef7bd30048e0)  

Date: Wed Mar 11 18:26:06 2026


---

### 24...@project.gserviceaccount.com (2026-03-12)

ClusterFuzz testcase 6059941089443840 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=105751:105752

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### de...@gmail.com (2026-05-19)

Hi, I wanted to follow up on the VRP status for this report. Are there any updates or an estimated timeline? Thanks!

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
High Quality. v8 sandbox. Nice!


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490769268)*
