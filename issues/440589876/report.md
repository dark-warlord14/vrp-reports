# V8 Intl::Normalize – Corrupted string length triggers unbounded allocation

| Field | Value |
|-------|-------|
| **Issue ID** | [440589876](https://issues.chromium.org/issues/440589876) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Linux |
| **Reporter** | am...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2025-08-23 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

1. compile d8 with attached args
2. execute the d8 along with the args for some n number of time, because the poc randomly assigns the value from the hardcoded array (because so)
3. d8 --fuzzing --sandbox-fuzzing --single-threaded --allow-natives-syntax --expose-gc poc.js (run for some n number of times)

# Problem Description

While fuzzing V8 with sandbox enabled, I observed a crash in the Intl-backed String.prototype.localeCompare implementation.

The crash occurs when a JS string’s internal metadata is corrupted. When passed to localeCompare, V8’s Intl::ToICUUnicodeString misinterprets the string length as 0xffffffffffffffff, causing ICU to attempt an impossible allocation:

Note: This indicates V8 is not validating string metadata before passing it to ICU.

In non-sandbox builds, this could manifest as a memory corruption / OOM crash, potentially leading to OOB access depending on allocator behavior.
Repro involves string corruption + call to String.prototype.localeCompare.

Build args:
is\_debug=false
is\_asan=true
v8\_enable\_sandbox=true
v8\_enable\_memory\_corruption\_api=true
dcheck\_always\_on=false
v8\_static\_library=true
v8\_fuzzilli=false
target\_cpu="x64"

Shell args:
d8 --fuzzing --sandbox-fuzzing --single-threaded --allow-natives-syntax --expose-gc poc.js

# Summary

V8 Intl String.localeCompare memory corruption leads to out-of-bounds allocation (ASan crash)

# Custom Questions

#### Crash state:

```
>116.js - 02:59 PM 23/08/2025<
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
=================================================================
==66560==ERROR: AddressSanitizer: requested allocation size 0xffffffffffffffff (0x800 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000 (thread T0)
    #0 0x61c2c9f3462d in operator new[](unsigned long, std::nothrow_t const&) (/home/basha/Desktop/chromefuzz/chromium/src/out/d8_asan_fuzz/d8+0x1bb62d) (BuildId: b51fa30873ae9dbc)
    #1 0x7323a4fa8d95 in NewArray<unsigned short> v8/src/utils/allocation.h:44:15
    #2 0x7323a4fa8d95 in v8::internal::(anonymous namespace)::GetUCharBufferFromFlat(v8::internal::String::FlatContent const&, std::__Cr::unique_ptr<unsigned short [], std::__Cr::default_delete<unsigned short []>>*, int) v8/src/objects/intl-objects.cc:195:19
    #3 0x7323a4fa4da7 in v8::internal::Intl::ToICUUnicodeString(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>, int) v8/src/objects/intl-objects.cc:246:20
    #4 0x7323a4fb2b46 in v8::internal::Intl::CompareStrings(v8::internal::Isolate*, icu_74::Collator const&, v8::internal::DirectHandle<v8::internal::String>, v8::internal::DirectHandle<v8::internal::String>, v8::internal::Intl::CompareStringsOptions) v8/src/objects/intl-objects.cc:1475:7
    #5 0x7323a4fb1895 in v8::internal::Intl::StringLocaleCompare(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::String>, v8::internal::DirectHandle<v8::internal::String>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, char const*) v8/src/objects/intl-objects.cc
    #6 0x7323a3b129f9 in v8::internal::Builtin_Impl_StringPrototypeLocaleCompareIntl(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-intl.cc:74:31
    #7 0x7323a3b1200f in v8::internal::Builtin_StringPrototypeLocaleCompareIntl(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-intl.cc:64:1
    #8 0x7323a2e772bc in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x7323a2a2b7a2 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #10 0x7323a2a1f6a6 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #11 0x7323a2a1f3ea in Builtins_JSEntry setup-isolate-deserialize.cc
    #12 0x7323a4071e9d in Call v8/src/execution/simulator.h:212:12
    #13 0x7323a4071e9d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:442:22
    #14 0x7323a40750db in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #15 0x7323a37eed73 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:1985:7
    #16 0x61c2c9f7a489 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1033:44
    #17 0x61c2c9fb447f in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:5331:10
    #18 0x61c2c9fc08fe in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:6289:37
    #19 0x61c2c9fbf895 in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:6197:18
    #20 0x61c2c9fc3853 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:7071:18
    #21 0x73239ca2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #22 0x73239ca2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #23 0x61c2c9e599d9 in _start (/home/basha/Desktop/chromefuzz/chromium/src/out/d8_asan_fuzz/d8+0xe09d9) (BuildId: b51fa30873ae9dbc)

==66560==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big (/home/basha/Desktop/chromefuzz/chromium/src/out/d8_asan_fuzz/d8+0x1bb62d) (BuildId: b51fa30873ae9dbc) in operator new[](unsigned long, std::nothrow_t const&)
==66560==ABORTING
Caught ASan fault without a fault address. Ignoring it as we cannot check if it is a sandbox violation. Exiting process...
>End of 116.js<

```
#### Reporter credit:

Ameen Basha M K

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [116.js](attachments/116.js) (text/javascript, 4.3 KB)
- [crash.txt](attachments/crash.txt) (text/plain, 4.3 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-08-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5772490848534528.

### an...@chromium.org (2025-08-24)

Clusterfuzz seems unable to repro. Setting provisional severity to S1, FoundIn to extended stable and assigning to V8 shepherd.
I wasn't sure if this is a sandbox bypass bug, so didn't set the component to that. PTAL. Thanks!

### am...@gmail.com (2025-08-24)

clusterfuzz didnt capture this due to the sandbox api missing

Kindly use the mentioned build args and shell args for running

also run the js in loop(running it multiple time will give you the crash)

### ch...@google.com (2025-08-25)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-08-25)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### is...@chromium.org (2025-08-25)

Thank you for the report!

This is not a vulnerability issue, this is ASAN build reporting an error that it can't allocate array of 0xffffffffffffffff size because ASAN builds need 0x800 bytes more. As written in the error message setting `ASAN_OPTIONS=allocator_may_return_null=1` lets the memory allocation fail and return a `nullptr` as expected (as happens in non-ASAN builds too) which makes V8 report a fatal OOM error.

What we can do better here is to avoid sign-extending corrupted string length `0xffffffff` to `size_t`.

### am...@gmail.com (2025-08-25)

Team my another issue https://issues.chromium.org/issues/440589880 was marked as duplicate of this. which was in Vulnerability  Category


but this issue was in Bug Category, kindly check and update this case

### dx...@google.com (2025-08-27)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6884672>

[sandbox] Fix implicit signed-unsigned conversions in Intl code

---


Expand for full commit details
```
     
    This CL introduces START_PROHIBIT_SIGN_CONVERSION and 
    END_PROHIBIT_SIGN_CONVERSION for prohibiting implicit conversions 
    between signed and unsigned integer types. 
     
    Drive-by: fix flags for regress-379418918.js which started to fail 
    because of enabled heap verification. 
     
    Fixed: 440589876 
    Bug: 440589880 
    Bug: 441221573 
    Change-Id: Iafa1476b0a28925c086eafc3c4eed1dde9aca9eb 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6884672 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102058}

```

---

Files:

- M `src/base/macros.h`
- M `src/heap/factory-base.cc`
- M `src/heap/factory-base.h`
- M `src/objects/intl-objects.cc`
- M `src/objects/intl-objects.h`
- M `src/strings/char-predicates-inl.h`
- M `src/strings/char-predicates.h`
- M `test/mjsunit/sandbox/regress/regress-379418918.js`
- A `test/mjsunit/sandbox/regress/regress-440589876.js`
- A `test/mjsunit/sandbox/regress/regress-440589880.js`

---

Hash: [895622033e626d2de9348421670b173e87e265db](https://chromiumdash.appspot.com/commit/895622033e626d2de9348421670b173e87e265db)  

Date: Tue Aug 26 15:56:48 2025


---

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. As there are no security implications resulting from this issue, this report is unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-12-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. As there are no security implications resulting from this issue, this report is unfortunately not eligible for a Chrome VRP reward.
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.
> 
> Regards,
> Google Security Bot
> 
> 
> --
> How did we do? Please fill out a s

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/440589876)*
