# V8 Sandbox Bypass: OOB write in JsonParser::DecodeString (double fetch)

| Field | Value |
|-------|-------|
| **Issue ID** | [396446145](https://issues.chromium.org/issues/396446145) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | v8...@gmail.com |
| **Assignee** | sr...@google.com |
| **Created** | 2025-02-14 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

In `JsonParser<Char>::MakeString` (`src/json/json-parser.cc:2115`), there is a special case for strings of length one.

```
  if (string.length() == 0) return factory()->empty_string();
  if (string.length() == 1) {
    uint16_t first_char;
    if (!string.has_escape()) {
      first_char = chars_[string.start()];
    } else {
      DecodeString(&first_char, string.start(), 1); <------ This path is taken
    }
    return factory()->LookupSingleCharacterStringFromCode(first_char);
  }

```

In that case, `DecodeString` is called with a buffer of size 2 (`first_char`). I guess if we change the on-heap string concurrently when `DecodeString` is executing, we may break the `!string.has_escape()` assumption, which causes an OOB write.

#### VERSION

V8 commit: a03d7c345e44f41236748e056e5fc6bb4cbe6025

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

Shell args: `d8 --single-threaded --sandbox-fuzzing --allow-natives-syntax --expose-gc bug.js`

##### ASAN Report:

```
==2401856==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7bad7d418863 at pc 0x563427fc9724 bp 0x7fff3b867cd0 sp 0x7fff3b867cc8
WRITE of size 4 at 0x7bad7d418863 thread T0
    #0 0x563427fc9723 in void v8::internal::JsonParser<unsigned char>::DecodeString<unsigned short>(unsigned short*, unsigned int, unsigned int) src/json/json-parser.cc:2206:19
    #1 0x563427fc1541 in v8::internal::JsonParser<unsigned char>::MakeString(v8::internal::JsonString const&, v8::internal::Handle<v8::internal::String>) src/json/json-parser.cc:2123:7
    #2 0x563427fc03c3 in ParseJsonValueRecursive src/json/json-parser.cc:1447:14
    #3 0x563427fc03c3 in v8::internal::JsonParser<unsigned char>::ParseJson(v8::internal::DirectHandle<v8::internal::Object>) src/json/json-parser.cc:540:5
    #4 0x563427fbfd81 in v8::internal::JsonParser<unsigned char>::Parse(v8::internal::Isolate*, v8::internal::Handle<v8::internal::String>, v8::internal::Handle<v8::internal::Object>) src/json/json-parser.h:173:7
    #5 0x5634276cb450 in v8::internal::Builtin_Impl_JsonParse(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-json.cc:25:3
    #6 0x56342bbef135 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #7 0x56342bb47c74 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #8 0x56342bb4575b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #9 0x56342bb454aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #10 0x563427a061c4 in Call src/execution/simulator.h:191:12
    #11 0x563427a061c4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:437:22
    #12 0x563427a07768 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:537:10
    #13 0x5634275acfc7 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2146:7
    #14 0x563427209247 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1018:44
    #15 0x563427234f03 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4999:10
    #16 0x56342723fe0e in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5953:37
    #17 0x56342723f4e6 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5861:18
    #18 0x563427242548 in v8::Shell::Main(int, char**) src/d8/d8.cc:6731:18
    #19 0x7fad7f3d01c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #20 0x7fad7f3d028a in __libc_start_main csu/../csu/libc-start.c:360:3
    #21 0x563427103029 in _start (/work/v8-build/v8/out/Reproduction/d8+0x113f029) (BuildId: 01c98ec35922344c)

Address 0x7bad7d418863 is located in stack of thread T0 at offset 35 in frame
    #0 0x563427fc122f in v8::internal::JsonParser<unsigned char>::MakeString(v8::internal::JsonString const&, v8::internal::Handle<v8::internal::String>) src/json/json-parser.cc:2116

  This frame has 1 object(s):
    [32, 34) 'first_char' (line 2119) <== Memory access at offset 35 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow src/json/json-parser.cc:2206:19 in void v8::internal::JsonParser<unsigned char>::DecodeString<unsigned short>(unsigned short*, unsigned int, unsigned int)
Shadow bytes around the buggy address:
  0x7bad7d418580: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bad7d418600: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bad7d418680: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bad7d418700: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bad7d418780: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
=>0x7bad7d418800: f5 f5 f5 f5 f5 f5 f5 f5 f1 f1 f1 f1[02]f3 f3 f3
  0x7bad7d418880: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bad7d418900: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bad7d418980: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bad7d418a00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7bad7d418a80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
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
==2401856==ABORTING

## V8 sandbox violation detected!


```
#### CREDIT INFORMATION

Reporter credit: v8sbxfuzz

## Attachments

- bug.js (text/javascript, 926 B)

## Timeline

### dx...@google.com (2025-04-17)

Project: v8/v8  

Branch: main  

Author: Stephen Roettger [sroettger@google.com](mailto:sroettger@google.com)  

Link:      <https://chromium-review.googlesource.com/6448401>

[sbx] check length in JsonParser::DecodeString

---


Expand for full commit details
```
     
    Fixed: 396446145 
    Change-Id: I773ffb6cfeade346f8f03cb3cf544f6390b03fd9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6448401 
    Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
    Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#99825}

```

---

Files:

- M `src/json/json-parser.cc`

---

Hash: 281cd945b242b2c32aef0b2c79dbe84e9d098f0c  

Date:  Tue Apr 15 08:39:30 2025


---

### sp...@google.com (2025-05-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 sandbox bypass demonstrating memory corruption outside of the heap sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> V8 sandbox bypass demonstrating memory corruption outside of the heap sandbox

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/396446145)*
