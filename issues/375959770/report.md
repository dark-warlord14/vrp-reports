# Arbitrary WASM type confusion due to module confusion in wasm-to-js tier-up

| Field | Value |
|-------|-------|
| **Issue ID** | [375959770](https://issues.chromium.org/issues/375959770) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2024-10230 |
| **Reporter** | se...@gmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2024-10-28 |
| **Bounty** | $11,000.00 |

## Description

## VULNERABILITY DETAILS

The poc trigger here[0]: Debug check failed: IsSubtypeOf(value.type(), global.type, module\_).

It should be a variant case of CVE-2024-10230[1][2], which has been used in v8ctf M129, I don't know how to exp temporarily, but it should be exploitable.

I will try to analyze RCA ASAP.

[0]. <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;l=1748>  

[1]. <https://issues.chromium.org/issues/371565065>  

[2]. <https://chromium-review.googlesource.com/c/v8/v8/+/5921410>

## VERSION

Version: I use latest d8 binary from: `gs://v8-asan/linux-debug/d8-asan-linux-debug-v8-component-96845.zip`  

Operating System: ubuntu2204 in wsl

## REPRODUCTION CASE

Please set line1 to your own `wasm-module-builder.js` path located in v8 source code.

```
d8.file.execute("/path/to/v8/test/mjsunit/wasm/wasm-module-builder.js");

function func(obj) {
    return obj;
}

// builder 0: export []->[ref 1]
let builder_0 = new WasmModuleBuilder();
let $s0_0 = builder_0.addStruct([makeField(kWasmI32, true)]);
let $s1_0 = builder_0.addStruct([makeField(kWasmI32, true), makeField(wasmRefType($s0_0), true)]);
let $sig_s1_ar_0 = builder_0.addType(makeSig([kWasmAnyRef], [wasmRefType($s1_0)]));
let $i_0 = builder_0.addImport('import', 'func', $sig_s1_ar_0);
let $t_0 = builder_0.addGlobal(wasmRefType($sig_s1_ar_0), 0, 0, [kExprRefFunc, $i_0]).exportAs('global11');

let instance_0 = builder_0.instantiate({ import: { func } });

let { global11 } = instance_0.exports;

%DebugPrint(global11);

// builder 1: export [ref 1]->[ref 2]
let builder_1 = new WasmModuleBuilder();
let $s0_1 = builder_1.addStruct([makeField(kWasmI32, true)]);
let $s1_1 = builder_1.addStruct([makeField(kWasmExternRef, true), makeField(kWasmI32, true)]);      // src type
let $s2_1 = builder_1.addStruct([makeField(kWasmI32, true), makeField(wasmRefType($s0_1), true)]);  // tgt type, equiv. $s1_0
let $sig_s2_ar_1 = builder_1.addType(makeSig([kWasmAnyRef], [wasmRefType($s2_1)]));                 // equiv. $sig_s1_ar_0
let $sig_v_v_1 = builder_1.addType(kSig_v_v);
let $sig_i_r_1 = builder_1.addType(kSig_i_r);
let $sig_i_i_1 = builder_1.addType(kSig_i_i);
let $sig_v_ii_1 = builder_1.addType(kSig_v_ii);

let $g_1 = builder_1.addImportedGlobal("import", "global11", wasmRefType($sig_s2_ar_1));

let instance_1 = builder_1.instantiate({ import: { global11 } });


```
## dcheck log

```
#
# Fatal error in ../../src/wasm/module-instantiate.cc, line 1733
# Debug check failed: IsSubtypeOf(value.type(), global.type, module_).
#
#
#
#FailureMessage Object: 0x7ffe5a0236b0
==== C stack trace ===============================

    ./d8(v8::base::debug::StackTrace::StackTrace()+0x13) [0x555f8dc61c43]
    ./d8(+0x3f404bb) [0x555f8dc614bb]
    ./d8(V8_Fatal(char const*, int, char const*, ...)+0x183) [0x555f8dc46883]
    ./d8(+0x3f25415) [0x555f8dc46415]
    ./d8(v8::internal::wasm::InstanceBuilder::WriteGlobalValue(v8::internal::wasm::WasmGlobal const&, v8::internal::wasm::WasmValue const&)+0x1ef) [0x555f8c992f6f]
    ./d8(v8::internal::wasm::InstanceBuilder::ProcessImportedWasmGlobalObject(v8::internal::Handle<v8::internal::WasmTrustedInstanceData>, int, v8::internal::wasm::WasmGlobal const&, v8::internal::Handle<v8::internal::WasmGlobalObject>)+0x687) [0x555f8c996857]
    ./d8(v8::internal::wasm::InstanceBuilder::ProcessImportedGlobal(v8::internal::Handle<v8::internal::WasmTrustedInstanceData>, int, int, v8::internal::Handle<v8::internal::Object>)+0x868) [0x555f8c997bb8]
    ./d8(v8::internal::wasm::InstanceBuilder::ProcessImports(v8::internal::Handle<v8::internal::WasmTrustedInstanceData>, v8::internal::Handle<v8::internal::WasmTrustedInstanceData>)+0x35a) [0x555f8c98d44a]
    ./d8(v8::internal::wasm::InstanceBuilder::Build()+0xd67) [0x555f8c989827]
    ./d8(v8::internal::wasm::InstantiateToInstanceObject(v8::internal::Isolate*, v8::internal::wasm::ErrorThrower*, v8::internal::Handle<v8::internal::WasmModuleObject>, v8::internal::MaybeHandle<v8::internal::JSReceiver>, v8::internal::MaybeHandle<v8::internal::JSArrayBuffer>)+0x5d) [0x555f8c98898d]
    ./d8(v8::internal::wasm::WasmEngine::SyncInstantiate(v8::internal::Isolate*, v8::internal::wasm::ErrorThrower*, v8::internal::Handle<v8::internal::WasmModuleObject>, v8::internal::MaybeHandle<v8::internal::JSReceiver>, v8::internal::MaybeHandle<v8::internal::JSArrayBuffer>)+0x128) [0x555f8ca8ff18]
    ./d8(v8::internal::wasm::WebAssemblyInstance(v8::FunctionCallbackInfo<v8::Value> const&)+0x1bf) [0x555f8caab3df]
    ./d8(v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool)+0x1ef) [0x555f8b7c65df]
    ./d8(+0x1aa4484) [0x555f8b7c5484]
    ./d8(v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*)+0x1e9) [0x555f8b7c3f59]
    ./d8(+0x3d4e4b6) [0x555f8da6f4b6]
Trace/breakpoint trap

```
## CREDIT INFORMATION

Reporter credit: tt

## Timeline

### ke...@chromium.org (2024-10-28)

Thanks for the report.

Assigning to current v8 sheriff. Severity and FoundIn are tentative.


### ti...@gmail.com (2024-10-29)

## RCA

When processing the imported gloabl object, if it's a WasmGlobalObject, the code path is

> ProcessImports -> ProcessImportedGlobal -> ProcessImportedWasmGlobalObject - WriteGlobalValue

See the code in [1], use IsSubtypeOf to check valid type, here

- global\_type\_module is global\_object's module, from `instance_0` in poc code.
- trusted\_instance\_data is current module, from `instance_1`
- logic here looks like correct

So in [2], call WriteGlobalValue without global\_object's module info, and in [3], `global` and `value` directly considered to come from the same module, but the value is encoded with `global_object->type()` in [4], which is from another module, so trigger dcheck.

```
bool InstanceBuilder::ProcessImportedWasmGlobalObject(
    DirectHandle<WasmTrustedInstanceData> trusted_instance_data,
    int import_index, const WasmGlobal& global,
    DirectHandle<WasmGlobalObject> global_object) {
  [...]
  const WasmModule* global_type_module =
      global_object->has_trusted_data()
          ? global_object->trusted_data(isolate_)->module()
          : trusted_instance_data->module();

  bool valid_type =
      global.mutability
          ? EquivalentTypes(global_object->type(), global.type,
                            global_type_module, trusted_instance_data->module())
          : IsSubtypeOf(global_object->type(), global.type, global_type_module, // <----- [1]
                        trusted_instance_data->module()); 

  if (!valid_type) {
    thrower_->LinkError("%s: imported global does not match the expected type",
                        ImportName(import_index).c_str());
    return false;
  }
  [...]

  WasmValue value;
  switch (global_object->type().kind()) {
    [...]
    case kRef:
    case kRefNull:
      value = WasmValue(global_object->GetRef(), global_object->type()); // <----- [4]
      break;
    [...]
  }

  WriteGlobalValue(global, value); // <----- [2]
  return true;
}

void InstanceBuilder::WriteGlobalValue(const WasmGlobal& global,
                                       const WasmValue& value) {
  TRACE("init [globals_start=%p + %u] = %s, type = %s\n",
        global.type.is_reference()
            ? reinterpret_cast<uint8_t*>(tagged_globals_->address())
            : raw_buffer_ptr(untagged_globals_, 0),
        global.offset, value.to_string().c_str(), global.type.name().c_str());
  DCHECK(IsSubtypeOf(value.type(), global.type, module_));  // <----- [3]
  if (global.type.is_numeric()) {
    value.CopyTo(GetRawUntaggedGlobalPtr<uint8_t>(global));
  } else {
    tagged_globals_->set(global.offset, *value.to_ref());
  }
}


```
## bisect:

Implement WriteGlobalValue but ignore the case where the global\_object from other module.

[[wasm] Merge WriteGlobal\* functions (2948664) · Gerrit Code Review (googlesource.com)](https://chromium-review.googlesource.com/c/v8/v8/+/2948664)

## suggest patch:

use the current module's global type for ref type

```
diff --git a/src/wasm/module-instantiate.cc b/src/wasm/module-instantiate.cc
index fb94d5e1488..5f336ea9b18 100644
--- a/src/wasm/module-instantiate.cc
+++ b/src/wasm/module-instantiate.cc
@@ -2250,7 +2250,7 @@ bool InstanceBuilder::ProcessImportedWasmGlobalObject(
       break;
     case kRef:
     case kRefNull:
-      value = WasmValue(global_object->GetRef(), global_object->type());
+      value = WasmValue(global_object->GetRef(), global.type);
       break;
     case kVoid:
     case kTop:

```

### cl...@appspot.gserviceaccount.com (2024-10-29)

Detailed Report: https://clusterfuzz.com/testcase?key=5437995377164288

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  IsSubtypeOf(value.type(), global.type, module_) in module-instantiate.cc
  v8::internal::wasm::InstanceBuilder::WriteGlobalValue
  v8::internal::wasm::InstanceBuilder::ProcessImportedWasmGlobalObject
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=96864

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5437995377164288

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-10-29)

Thanks for the report! This just bisects to <https://chromium.googlesource.com/v8/v8/+/50f8643de79d1c0db4efb41c24ed7c283a97bb7b> "[wasm-gc] Ship it!", so Matthias or Jakob, could one of you take a look?

### pe...@google.com (2024-10-29)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-10-29)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ml...@chromium.org (2024-10-29)

Manos, this seems to be related to non-mutable imported globals and it might be some issue with type canonicalization, could you take a look, please?

### ma...@chromium.org (2024-11-04)

Thanks for the report!
This does not seem to be a security vulnerability: The type taken from the exporting module is only used in a DCHECK and to determine if the global is tagged or not, which does not change depending on the type's index.
A more principled fix in my opinion would be to include the module in WasmValue. An indexed ValueType by itself has no meaning if it is not accompanied by the module it defined it.
A CL to fix this is coming up.

### ap...@google.com (2024-11-04)

Project: v8/v8  

Branch: main  

Author: Manos Koukoutos <[manoskouk@chromium.org](mailto:manoskouk@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5987673>

[wasm] Add WasmModule to WasmValue

---


Expand for full commit details
```
[wasm] Add WasmModule to WasmValue 
 
An indexed ValueType is meaningless without the WasmModule that 
defined it. We therefore add a WasmModule to WasmValue. 
This fixes a DCHECK during module instantiation. 
 
Bug: chromium:375959770 
Change-Id: Iccee0fc4c35e8f571a961f2c907289963fa4616e 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5987673 
Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#96961}

```

---

Files:

- M `src/debug/debug-wasm-objects.cc`
- M `src/wasm/baseline/liftoff-compiler.cc`
- M `src/wasm/constant-expression-interface.cc`
- M `src/wasm/constant-expression.cc`
- M `src/wasm/constant-expression.h`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-debug.cc`
- M `src/wasm/wasm-debug.h`
- M `src/wasm/wasm-objects-inl.h`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.h`
- M `src/wasm/wasm-value.h`
- M `test/fuzzer/wasm-init-expr.cc`
- A `test/mjsunit/regress/wasm/regress-375959770.js`

---

Hash: 24e752306cc0cd03cafb9695672741d0737bd0e8  

Date:  Mon Nov 04 14:05:20 2024


---

### 24...@project.gserviceaccount.com (2024-11-05)

ClusterFuzz testcase 5437995377164288 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96960:96961

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-11-05)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M130 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M131 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130, 131].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-11-06)

As per c#9, this does not appear to be an exploitable security issue. Updating status, and removing security merge tags.

### am...@chromium.org (2024-11-06)

Thank you for the report. This doesn't not appear to be an exploitable issue that would result in security consequences for a user, therefore, this report is unfortunately not eligible for a Chrome VRP reward.

### pe...@google.com (2025-02-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/375959770)*
