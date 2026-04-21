# V8 sandbox violation in v8::base::GenerateCountedDigits

| Field | Value |
|-------|-------|
| **Issue ID** | [395029283](https://issues.chromium.org/issues/395029283) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | v8...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2025-02-07 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

During the execution of the `Number.prototype.toPrecision` builtin a heap Number is converted to a double without checking whether it is NaN. This double is then used to check some stack buffer bounds, which pass because comparing to NaN is false. Eventually, the value is cast to int, resulting in -1 being used as size value during a copy later during execution.

```
BUILTIN(NumberPrototypeToPrecision) {
  HandleScope scope(isolate);
  DirectHandle<Object> value = args.at(0);
  Handle<Object> precision = args.atOrUndefined(isolate, 1);

  // Unwrap the receiver {value}.
  if (IsJSPrimitiveWrapper(*value)) {
    value = direct_handle(Cast<JSPrimitiveWrapper>(value)->value(), isolate);
  }
  if (!IsNumber(*value)) {
    THROW_NEW_ERROR_RETURN_FAILURE(
        isolate, NewTypeError(MessageTemplate::kNotGeneric,
                              isolate->factory()->NewStringFromAsciiChecked(
                                  "Number.prototype.toPrecision"),
                              isolate->factory()->Number_string()));
  }
  double const value_number = Object::NumberValue(*value);

  // If no {precision} was specified, just return ToString of {value}.
  if (IsUndefined(*precision, isolate)) {
    return *isolate->factory()->NumberToString(value);
  }

  // Convert the {precision} to an integer first.
  // <<<<<<<<<<< precision is a Number. If precision can not be stored in an SMI,
  // <<<<<<<<<<< this will allocate a new Number heap object.
  ASSIGN_RETURN_FAILURE_ON_EXCEPTION(isolate, precision,
                                     Object::ToInteger(isolate, precision));
  // <<<<<<<<<<< Here, we store NaN through a background thread
  // <<<<<<<<<<< into the heap object from above.
  double const precision_number = Object::NumberValue(*precision);
  // <<<<<<<<<<< precision_number is NaN

  if (std::isnan(value_number)) return ReadOnlyRoots(isolate).NaN_string();
  if (std::isinf(value_number)) {
    return (value_number < 0.0) ? ReadOnlyRoots(isolate).minus_Infinity_string()
                                : ReadOnlyRoots(isolate).Infinity_string();
  }

  // <<<<<<<<<<< This check will not trigger for NaN
  if (precision_number < 1.0 || precision_number > kMaxFractionDigits) {
    THROW_NEW_ERROR_RETURN_FAILURE(
        isolate, NewRangeError(MessageTemplate::kToPrecisionFormatRange));
  }
  char chars[kDoubleToPrecisionMaxChars];
  base::Vector<char> buffer = base::ArrayVector(chars);
  // <<<<<<<<<<< NaN is cast to int, resulting in -1
  std::string_view str = DoubleToPrecisionStringView(
      value_number, static_cast<int>(precision_number), buffer);
  DirectHandle<String> result =
      isolate->factory()->NewStringFromAsciiChecked(str);
  return *result;
}


```
#### VERSION

V8 commit: 932fab3dab1483a16dc10bd0e036df6af564bcab

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
==827218==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7b8a0bd60ca5 at pc 0x55e5e4c5f82c bp 0x7ffe479e00b0 sp 0x7ffe479e00a8
WRITE of size 1 at 0x7b8a0bd60ca5 thread T0
    #0 0x55e5e4c5f82b in v8::base::GenerateCountedDigits(int, int*, v8::base::Bignum*, v8::base::Bignum*, v8::base::Vector<char>, int*) src/base/numbers/bignum-dtoa.cc:242:15
    #1 0x55e5e4c5f45c in v8::base::BignumDtoa(double, v8::base::BignumDtoaMode, int, v8::base::Vector<char>, int*, int*) src/base/numbers/bignum-dtoa.cc
    #2 0x55e5e4c5b892 in v8::base::DoubleToAscii(double, v8::base::DtoaMode, int, v8::base::Vector<char>, int*, int*, int*) src/base/numbers/dtoa.cc:76:3
    #3 0x55e5e4c48869 in v8::internal::DoubleToPrecisionStringView(double, int, v8::base::Vector<char>) src/numbers/conversions.cc:1182:3
    #4 0x55e5e427745c in v8::internal::Builtin_Impl_NumberPrototypeToPrecision(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-number.cc:188:26
    #5 0x55e5e84c7cf5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #6 0x55e5e8420c74 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #7 0x55e5e841e75b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #8 0x55e5e841e4aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #9 0x55e5e457269a in Call src/execution/simulator.h:191:12
    #10 0x55e5e457269a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:437:22
    #11 0x55e5e4574b48 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:537:10
    #12 0x55e5e4154b5b in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2146:7
    #13 0x55e5e3e0de64 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1017:44
    #14 0x55e5e3e38576 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4959:10
    #15 0x55e5e3e43456 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5904:37
    #16 0x55e5e3e42b26 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5812:18
    #17 0x55e5e3e45b3d in v8::Shell::Main(int, char**) src/d8/d8.cc:6680:18
    #18 0x7f8a0db7c1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #19 0x7f8a0db7c28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #20 0x55e5e3d09029 in _start (/work/v8-build/v8/out/Reproduction/d8+0x10e5029) (BuildId: bd5d3ccb721c4315)

Address 0x7b8a0bd60ca5 is located in stack of thread T0 at offset 165 in frame
    #0 0x55e5e4c4872f in v8::internal::DoubleToPrecisionStringView(double, int, v8::base::Vector<char>) src/numbers/conversions.cc:1163

  This frame has 4 object(s):
    [32, 36) 'decimal_point' (line 1175)
    [48, 52) 'sign' (line 1176)
    [64, 165) 'decimal_rep' (line 1179) <== Memory access at offset 165 overflows this variable
    [208, 212) 'decimal_rep_length' (line 1180)
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow src/base/numbers/bignum-dtoa.cc:242:15 in v8::base::GenerateCountedDigits(int, int*, v8::base::Bignum*, v8::base::Bignum*, v8::base::Vector<char>, int*)
Shadow bytes around the buggy address:
  0x7b8a0bd60a00: f1 f1 f1 f1 f8 f8 f2 f2 00 00 00 00 00 00 00 00
  0x7b8a0bd60a80: 00 00 00 00 00 04 f3 f3 f3 f3 f3 f3 00 00 00 00
  0x7b8a0bd60b00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7b8a0bd60b80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7b8a0bd60c00: f1 f1 f1 f1 04 f2 04 f2 00 00 00 00 00 00 00 00
=>0x7b8a0bd60c80: 00 00 00 00[05]f2 f2 f2 f2 f2 04 f3 00 00 00 00
  0x7b8a0bd60d00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7b8a0bd60d80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7b8a0bd60e00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7b8a0bd60e80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7b8a0bd60f00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
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
==827218==ABORTING

## V8 sandbox violation detected!


```
#### CREDIT INFORMATION

Reporter credit: v8sbxfuzz

## Attachments

- bug.js (text/javascript, 1.6 KB)

## Timeline

### ma...@chromium.org (2025-02-07)

assigning per sandbox bypass shepherding instructions: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/shepherd.md#assign:~:text=normally%20be%20necessary.-,V8%20Sandbox%20bypasses,-.%20The%20V8%20Sandbox>

### cl...@appspot.gserviceaccount.com (2025-02-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6140332303384576.

### cl...@appspot.gserviceaccount.com (2025-02-08)

Detailed Report: https://clusterfuzz.com/testcase?key=4634446456094720

Fuzzer: None
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 0x762e3cc687a5
Crash State:
  v8::base::GenerateCountedDigits
  v8::base::BignumDtoa
  v8::base::DoubleToAscii
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&revision=98589

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4634446456094720

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sr...@google.com (2025-02-10)

pthier@ would you be a good person to look at this one?

An easy fix would be to turn the DCHECK in DoubleToPrecisionStringView into a SBXCHECK, but I wonder if it would make sense to refactor a few of the functions so that they take unsigned integers instead of plain int.

### pt...@chromium.org (2025-02-11)

I can take a look.  

I think it makes sense to refactor `base::DoubleToAscii` to take unsigned ints instead of a signed int (Not only for `requested_digits`, but also `length`).  

For some of the `Double.*ToStringView` methods `-1` is used as a sentinel for `undefined`, so I would keep all of them signed for consistency.

`base::DoubleToAscii` is a big rabbit hole down our number library, so I will start with the bandage fix of turning the `DCHECK`s into `SBXCHECK`s.

Besides `Number.prototype.toPrecision`, the following methods are also affected:

- `Number.prototype.toFixed`
- `Number.prototype.toExponential`

### pt...@chromium.org (2025-02-11)

I gave this a second thought and think the best solution is to avoid the double read of the objects value.

I.e. in

```
  ASSIGN_RETURN_FAILURE_ON_EXCEPTION(isolate, precision,
                                     Object::ToInteger(isolate, precision));
  double const precision_number = Object::NumberValue(*precision);

```

the assumption is that `precision` doesn't contain `NaN` or `-0`, which is the case without corruption.

Instead of converting the object and reading the value (assuming it is an integer or infinity), we should do something like this:

```
  double precision_number;
  ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
      isolate, precision_number,
      Object::IntegerValue(isolate, *precision));

```

This a) avoids the double read enabling this exploit and b) avoids allocating a new `HeapNumber`, which is unnecessary in these cases where the `HeapNumber` doesn't escape the current function (not relevant for security, but another nice benefit).

I still have to check all cases where the return value of `Object::ToInteger()` escapes the current function and is later used in `Object::NumberValue`. In this case callers need to ensure they use `DoubleToInteger` on the value returned by `Object::NumberValue` if it's assumed to be an integer or infinity.

### ap...@google.com (2025-02-12)

Project: v8/v8  

Branch: main  

Author: pthier <[pthier@chromium.org](mailto:pthier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6257166>

Introduce Object::IntegerValue

---


Expand for full commit details
```
Introduce Object::IntegerValue 
 
... as a replacement for the sequence Object::ToInteger + 
Object::NumberValue for cases where the HeapObject returned by 
Object::ToInteger doesn't escape the current function. 
This avoids reloading the value (Object::NumberValue) and 
potentially a HeapNumber allocation if the value wasn't a Smi. 
 
Fixed: 395029283 
Change-Id: I50325f39d68f2926d9740b7777fd193b9ec1d45e 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6257166 
Commit-Queue: Patrick Thier <pthier@chromium.org> 
Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98660}

```

---

Files:

- M `src/builtins/builtins-array.cc`
- M `src/builtins/builtins-arraybuffer.cc`
- M `src/builtins/builtins-atomics-synchronization.cc`
- M `src/builtins/builtins-bigint.cc`
- M `src/builtins/builtins-intl.cc`
- M `src/builtins/builtins-number.cc`
- M `src/builtins/builtins-sharedarraybuffer.cc`
- M `src/builtins/builtins-string.cc`
- M `src/builtins/builtins-typed-array.cc`
- M `src/objects/objects-inl.h`
- M `src/objects/objects.h`
- M `src/runtime/runtime-array.cc`

---

Hash: 8bf0d48b23855c14e8f4e4629640e3955ca228f0  

Date:  Wed Feb 12 11:46:34 2025


---

### sp...@google.com (2025-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 sandbox bypass demonstrating memory corruption outside the V8 heap sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-20)

Congratulations on another one! Thanks for all your different efforts fuzzing Chrome and reporting these issues to us!

### ch...@google.com (2025-05-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> V8 sandbox bypass demonstrating memory corruption outside the V8 heap sandbox

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/395029283)*
