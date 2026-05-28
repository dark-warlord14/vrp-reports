# V8 Sandbox Bypass: UB in WebAssemblyMemoryGrow because AddressType is constructed from on-heap data

| Field | Value |
|-------|-------|
| **Issue ID** | [390453039](https://issues.chromium.org/issues/390453039) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | v8...@gmail.com |
| **Assignee** | sr...@google.com |
| **Created** | 2025-01-17 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

During the growth of a WASM heap memory object, `WebAssemblyMemoryGrow` constructs an `AddressType` enum variant from on-heap data and passes it to a `switch` instruction, causing undefined behavior.

#### VERSION

V8 commit: `ab875b6ed878b0b1934ab935366224ee4c761985` (2025-01-15T14:21:08+00:00)

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

The value is read here from the heap:

```
    #2 0x555561c28b52 in v8::internal::wasm::AddressType v8::internal::ReadMaybeUnalignedValue<v8::internal::wasm::AddressType>(unsigned long) src/common/ptr-compr.h:192:12
    #3 0x555561c28ac4 in v8::internal::wasm::AddressType v8::internal::HeapObject::ReadField<v8::internal::wasm::AddressType>(unsigned long) const requires std::is_arithmetic_v<v8::internal::wasm::AddressType> || std::is_enum_v<v8::internal::wasm::AddressType> || std::is_pointer_v<v8::internal::wasm::AddressType> src/objects/heap-object.h:241:12
    #4 0x555561c28a59 in v8::internal::TorqueGeneratedWasmMemoryObject<v8::internal::WasmMemoryObject, v8::internal::JSObject>::address_type() const gen/torque-generated/src/wasm/wasm-objects-tq-inl.inc:986:44
    #5 0x555564abae0d in v8::(anonymous namespace)::WebAssemblyMemoryGrowImpl(v8::FunctionCallbackInfo<v8::Value> const&) src/wasm/wasm-js.cc:2768:59
    #6 0x555564ab9144 in v8::internal::wasm::WebAssemblyMemoryGrow(v8::FunctionCallbackInfo<v8::Value> const&) src/wasm/wasm-js.cc:3151:1
    #7 0x55556ae44c4b in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc
    #8 0x55556ae42e40 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #9 0x55556ae4091b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #10 0x55556ae4066a in Builtins_JSEntry setup-isolate-deserialize.cc
    #11 0x55555daf5283 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:191:12
    #12 0x55555dae71e0 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:437:22
    #13 0x55555dae8acd in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:537:10
    #14 0x55555c52c654 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2156:7
    #15 0x55555c52b06c in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:2119:10
    #16 0x55555bf7679a in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1018:44
    #17 0x55555c031e53 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4869:10
    #18 0x55555c0505fa in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5907:37
    #19 0x55555c04e514 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5816:18
    #20 0x55555c05788b in v8::Shell::Main(int, char**) src/d8/d8.cc:6714:18
    #21 0x55555c059781 in main src/d8/d8.cc:6806:43
    #22 0x7ffff7a211c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #23 0x7ffff7a2128a in __libc_start_main csu/../csu/libc-start.c:360:3
    #24 0x55555bd43029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x67ef029) (BuildId: cbaa25b471887c0f)

```

and causes undefined behavior here:

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==1131878==ERROR: AddressSanitizer: ILL on unknown address 0x555564b560bd (pc 0x555564b560bd bp 0x7fffffff8fd0 sp 0x7fffffff8ec0 T0)
    #0 0x555564b560bd in std::__Cr::optional<unsigned long> v8::(anonymous namespace)::(anonymous namespace)::AddressValueToU64<char const*>(v8::internal::wasm::ErrorThrower*, v8::Local<v8::Context>, v8::Local<v8::Value>, char const*, v8::internal::wasm::AddressType) src/wasm/wasm-js.cc:1302:3
    #1 0x555564abae32 in v8::(anonymous namespace)::WebAssemblyMemoryGrowImpl(v8::FunctionCallbackInfo<v8::Value> const&) src/wasm/wasm-js.cc:2767:47
    #2 0x555564ab9144 in v8::internal::wasm::WebAssemblyMemoryGrow(v8::FunctionCallbackInfo<v8::Value> const&) src/wasm/wasm-js.cc:3151:1
    #3 0x55556ae44c4b in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc
    #4 0x55556ae42e40 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #5 0x55556ae4091b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #6 0x55556ae4066a in Builtins_JSEntry setup-isolate-deserialize.cc
    #7 0x55555daf5283 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:191:12
    #8 0x55555dae71e0 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:437:22
    #9 0x55555dae8acd in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:537:10
    #10 0x55555c52c654 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2156:7
    #11 0x55555c52b06c in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:2119:10
    #12 0x55555bf7679a in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1018:44
    #13 0x55555c031e53 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4869:10
    #14 0x55555c0505fa in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5907:37
    #15 0x55555c04e514 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5816:18
    #16 0x55555c05788b in v8::Shell::Main(int, char**) src/d8/d8.cc:6714:18
    #17 0x55555c059781 in main src/d8/d8.cc:6806:43
    #18 0x7ffff7a211c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #19 0x7ffff7a2128a in __libc_start_main csu/../csu/libc-start.c:360:3
    #20 0x55555bd43029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x67ef029) (BuildId: cbaa25b471887c0f)


## V8 sandbox violation detected!

```
#### CREDIT INFORMATION

Reporter credit: v8sbxfuzz

## Attachments

- [bug.js](attachments/bug.js) (text/javascript, 3.7 KB)

## Timeline

### ad...@google.com (2025-01-17)

Security shepherd: adding provisional triage labels as is normal for V8 sandbox bypasses.

### ap...@google.com (2025-01-20)

Project: v8/v8  

Branch: main  

Author: Stephen Roettger <[sroettger@google.com](mailto:sroettger@google.com)>  

Link:      <https://chromium-review.googlesource.com/6179825>

[sandbox] fix UB after switch on AddressType enum

---


Expand for full commit details
```
[sandbox] fix UB after switch on AddressType enum 
 
AddressValueToU64 doesn't have a return after the exhaustive switch on 
the AddressType enum. This is UB if the enum value can be outside of the 
range of the declared enum values. 
 
Fixed: 390453039 
Bug: 390617721 
Change-Id: I199190ea7ad2fd31a15819e8f54acd8cd5274775 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6179825 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Stephen Röttger <sroettger@google.com> 
Cr-Commit-Position: refs/heads/main@{#98207}

```

---

Files:

- M `src/wasm/wasm-js.cc`

---

Hash: c67b420e4fba9a69bb1f81b10eb79910067f943e  

Date:  Mon Jan 20 18:01:59 2025


---

### sp...@google.com (2025-01-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 sandbox bypass demonstrating memory corruption outside the V8 sandbox 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-29)

Congratulations on another one this week! Thank you for your efforts fuzzing the V8 sandbox and reporting this issue to us -- great work!

### ch...@google.com (2025-04-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/390453039)*
