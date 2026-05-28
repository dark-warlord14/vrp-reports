# V8 Sandbox Bypass: MemoryChunk metadata_pointer_table OOB write

| Field | Value |
|-------|-------|
| **Issue ID** | [392938085](https://issues.chromium.org/issues/392938085) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Sandbox |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | v8...@gmail.com |
| **Assignee** | sr...@google.com |
| **Created** | 2025-01-29 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

The function `GetOneByteStringInternal` at `ast/ast-value-factory.cc:317` contains a double fetch bug when converting a on heap string into a `AstRawString`:

```
const AstRawString* AstValueFactory::GetOneByteStringInternal(
    base::Vector<const uint8_t> literal) {
  if (literal.length() == 1 && literal[0] < kMaxOneCharStringValue) { // <---- 1. fetch of literal[0]
    int key = literal[0];  // <---- 2. fetch of literal[0]
    if (V8_UNLIKELY(one_character_strings_[key] == nullptr)) {
      uint32_t raw_hash_field = StringHasher::HashSequentialString<uint8_t>(
          literal.begin(), literal.length(), hash_seed_);
      one_character_strings_[key] = GetString(raw_hash_field, true, literal); // OOB write
    }
    return one_character_strings_[key];
  }
  uint32_t raw_hash_field = StringHasher::HashSequentialString<uint8_t>(
      literal.begin(), literal.length(), hash_seed_);
  return GetString(raw_hash_field, true, literal);
}


```

The `literal[0]` value here is located on the heap and can change between the first and second load. If the second time the loaded value is >= `kMaxOneCharStringValue`, the write into the `one_character_strings_` array is going to be out of bounds. This can potentially be archived by a worker thread running in the background.

The code path can be triggered by constructing an exception (e.g., via `ErrorUtils::NewConstructedNonConstructable`) that parses the context (e.g., the enclosing function name) in which it was raised.

As with [bug 389713719](https://issues.chromium.org/issues/389713719), it's hard to construct a reproducer because, depending on the compiler, `literal[0]` may only be fetched once.

#### VERSION

V8 commit: `69b47d88cb8f3bff0966000cd039b50786bbd891` (2025-01-27T20:39:04+00:00)

##### ASAN Report:

```
=================================================================
==1289300==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x51900001d0e0 at pc 0x55555dd030a5 bp 0x7fffffff6c90 sp 0x7fffffff6c88
WRITE of size 8 at 0x51900001d0e0 thread T0
    #0 0x55555dd030a4 in v8::internal::AstValueFactory::GetOneByteStringInternal(v8::base::Vector<unsigned char const>) src/ast/ast-value-factory.cc:324:35
    #1 0x55555dd069de in v8::internal::AstValueFactory::GetString(v8::internal::Tagged<v8::internal::String>, v8::internal::SharedStringAccessGuardIfNeeded const&) src/ast/ast-value-factory.cc:348:14
    #2 0x55556272d222 in v8::internal::Parser::ParseFunction(v8::internal::Isolate*, v8::internal::ParseInfo*, v8::internal::DirectHandle<v8::internal::SharedFunctionInfo>) src/parsing/parser.cc:991:48
    #3 0x555562833f3b in v8::internal::parsing::ParseFunction(v8::internal::ParseInfo*, v8::internal::DirectHandle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*, v8::internal::parsing::ReportStatisticsMode) src/parsing/parsing.cc:93:10
    #4 0x5555628358d5 in v8::internal::parsing::ParseAny(v8::internal::ParseInfo*, v8::internal::DirectHandle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*, v8::internal::parsing::ReportStatisticsMode) src/parsing/parsing.cc:111:10
    #5 0x55555e75b7dd in v8::internal::(anonymous namespace)::RenderCallSite(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::MessageLocation*, v8::internal::CallPrinter::ErrorHint*) src/execution/messages.cc:894:9
    #6 0x55555e76ae7f in v8::internal::ErrorUtils::NewConstructedNonConstructable(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>) src/execution/messages.cc:1001:7
    #7 0x5555634d67af in v8::internal::Runtime_ThrowConstructedNonConstructable(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-internal.cc:520:8
    #8 0x55556bc2bb35 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #9 0x55556bb7f057 in Builtins_ConstructedNonConstructable setup-isolate-deserialize.cc
    #10 0x55556bd2ceca in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #11 0x55556bb84e34 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x55556bb84e34 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #13 0x55556bb8291b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #14 0x55556bb8266a in Builtins_JSEntry setup-isolate-deserialize.cc
    #15 0x55555e38391d in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:191:12
    #16 0x55555e374fa7 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:437:22
    #17 0x55555e3768fd in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:537:10
    #18 0x55555cd0465c in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2147:7
    #19 0x55555cd02ffc in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:2110:10
    #20 0x55555c06e1ba in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1021:44
    #21 0x55555c12e277 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4885:10
    #22 0x55555c14d906 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5924:37
    #23 0x55555c14b75e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5832:18
    #24 0x55555c154cea in v8::Shell::Main(int, char**) src/d8/d8.cc:6731:18
    #25 0x55555c156c81 in main src/d8/d8.cc:6823:43
    #26 0x7ffff7a1f1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #27 0x7ffff7a1f28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #28 0x55555be30029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x68dc029) (BuildId: 00b75c7fe5a61b3d)

0x51900001d0e0 is located 24 bytes after 1096-byte region [0x51900001cc80,0x51900001d0c8)
allocated by thread T0 here:
    #0 0x55555bf5f538 in operator new(unsigned long) /work/llvm-project/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x5555627025b9 in v8::internal::ReusableUnoptimizedCompileState::ReusableUnoptimizedCompileState(v8::internal::Isolate*) src/parsing/parse-info.cc:170:11
    #2 0x55555e75b701 in v8::internal::(anonymous namespace)::RenderCallSite(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::MessageLocation*, v8::internal::CallPrinter::ErrorHint*) src/execution/messages.cc:892:37
    #3 0x55555e76ae7f in v8::internal::ErrorUtils::NewConstructedNonConstructable(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>) src/execution/messages.cc:1001:7
    #4 0x5555634d67af in v8::internal::Runtime_ThrowConstructedNonConstructable(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-internal.cc:520:8
    #5 0x55556bc2bb35 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #6 0x55556bb7f057 in Builtins_ConstructedNonConstructable setup-isolate-deserialize.cc
    #7 0x55556bd2ceca in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #8 0x55556bb84e34 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #9 0x55556bb84e34 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #10 0x55556bb8291b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #11 0x55556bb8266a in Builtins_JSEntry setup-isolate-deserialize.cc
    #12 0x55555e38391d in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:191:12
    #13 0x55555e374fa7 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:437:22
    #14 0x55555e3768fd in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:537:10
    #15 0x55555cd0465c in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2147:7
    #16 0x55555cd02ffc in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:2110:10
    #17 0x55555c06e1ba in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1021:44
    #18 0x55555c12e277 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4885:10
    #19 0x55555c14d906 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5924:37
    #20 0x55555c14b75e in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5832:18
    #21 0x55555c154cea in v8::Shell::Main(int, char**) src/d8/d8.cc:6731:18
    #22 0x55555c156c81 in main src/d8/d8.cc:6823:43
    #23 0x7ffff7a1f1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #24 0x7ffff7a1f28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #25 0x55555be30029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x68dc029) (BuildId: 00b75c7fe5a61b3d)

SUMMARY: AddressSanitizer: heap-buffer-overflow src/ast/ast-value-factory.cc:324:35 in v8::internal::AstValueFactory::GetOneByteStringInternal(v8::base::Vector<unsigned char const>)
Shadow bytes around the buggy address:
  0x51900001ce00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x51900001ce80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x51900001cf00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x51900001cf80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x51900001d000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x51900001d080: 00 00 00 00 00 00 00 00 00 fa fa fa[fa]fa fa fa
  0x51900001d100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51900001d180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x51900001d200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x51900001d280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x51900001d300: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==1289300==ABORTING

## V8 sandbox violation detected!


```
#### CREDIT INFORMATION

Reporter credit: v8sbxfuzz

## Timeline

### an...@chromium.org (2025-01-29)

Assigning to V8 shepherd.

### ap...@google.com (2025-02-05)

Project: v8/v8  

Branch: main  

Author: Igor Sheludko <[ishell@chromium.org](mailto:ishell@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6233934>

[ast] Avoid double-fetch in AstValueFactory

---


Expand for full commit details
```
[ast] Avoid double-fetch in AstValueFactory 
 
... GetOneByteStringInternal(). 
 
Fixed: 392938085 
Change-Id: If97af2bc89f8317b22834c0f87363ef44a24f3a5 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6233934 
Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
Commit-Queue: Igor Sheludko <ishell@chromium.org> 
Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
Auto-Submit: Igor Sheludko <ishell@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98514}

```

---

Files:

- M `src/ast/ast-value-factory.cc`

---

Hash: 710a7a83c68cd554fb495563ac4870b03b40cc58  

Date:  Wed Feb 05 12:15:01 2025


---

### is...@chromium.org (2025-02-05)

Lowering severity because this double-fetch is most likely not an issue for our production builds (this kind of double load should be optimized into a single load).

Could you please provide the gn args you used?

### v8...@gmail.com (2025-02-05)

I built this with an out-of-tree compiler and `-O0`, thus this may not affect the release build, but I think it's hard to predict what a compiler will do in the end. Here are the gn args:

```
is_debug=false
symbol_level=2
v8_enable_backtrace=true
clang_use_chrome_plugins=false
custom_toolchain=\"//build/toolchain/linux/unbundle:default\"
host_toolchain=\"//build/toolchain/linux/unbundle:default\"
export CFLAGS="-O0 -g"
export CXXFLAGS="$CFLAGS"

```

### am...@chromium.org (2025-02-05)

Since this is a sandbox issue, it's already marked as SI-None, which would also carry over to this issue not impacting release builds (as in, had this issue not already been marked SI-None, we would have wanted to do that now).
I think lowering the severity && priority here is fine since this seems to only impact the debug builds.

### am...@chromium.org (2025-02-10)

Thanks for the report, v8sbxfuzz@. Since this bypass only impacts debug builds, rather than potential future production builds, this report is unfortunately not eligible for a Chrome VRP reward.

### ch...@google.com (2025-05-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/392938085)*
