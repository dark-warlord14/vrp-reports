# V8 Sandbox Bypass: AAW/PC control via dispatch entry UAF during InstantiateAsmJs by hijacking start

| Field | Value |
|-------|-------|
| **Issue ID** | [462217236](https://issues.chromium.org/issues/462217236) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>GarbageCollection, Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kr...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2025-11-20 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

The js-to-wasm wrapper for the start function used for asm.js instantiation exists inside the sandbox and so can be corrupted to run user code during instantiation. Since nothing besides in-sandbox data retains the dispatch entry of the instantiator at this point, said references can be removed to free and reclaim it with a higher formal parameter count. Following which, the hijacked start can throw an error to get `Builtins_InstantiateAsmJs` to tail using the reclaimed entry to imbalance the stack for AAW/PC control as in the past.

#### Details

asm.js uses a [start function to copy globals](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/asmjs/asm-parser.cc;l=365-377;drc=e3f4a72847c1d1dcc38ad8834bf9b6b5d8b7c956):

```
void AsmJsParser::ValidateModule() {
  // ... snipped...

  // Add start function to initialize things.
  WasmFunctionBuilder* start = module_builder_->AddFunction();
  module_builder_->MarkStartFunction(start);
  for (auto& global_import : global_imports_) {
    uint32_t import_index = module_builder_->AddGlobalImport(
        global_import.import_name, global_import.value_type,
        false /* mutability */);
    start->EmitWithU32V(kExprGlobalGet, import_index);
    start->EmitWithU32V(kExprGlobalSet, VarIndex(global_import.var_info));
  }
  start->Emit(kExprEnd);
  FunctionSig::Builder b(zone(), 0, 0);
  start->SetSignature(b.Get());
}

```

For which a [JSFunction js-to-wasm wrapper is made in InstanceBuilder::Build\_Phase1](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;l=1477-1488;drc=e1bbad0f24864aead83224b08f5cb000bac8fa32):

```
    if (start_function_.is_null()) {
      // TODO(clemensb): Don't generate an exported function for the start
      // function. Use CWasmEntry instead.
      bool function_is_shared = module_->type(function.sig_index).is_shared;
      DirectHandle<WasmFuncRef> func_ref =
          WasmTrustedInstanceData::GetOrCreateFuncRef(
              isolate_, trusted_data(function_is_shared), start_index,
              kPrecreateExternal);
      DirectHandle<WasmInternalFunction> internal{func_ref->internal(isolate_),
                                                  isolate_};
      start_function_ = WasmInternalFunction::GetOrCreateExternal(internal);
    }

```

This JSFunction resides in-sandbox. Moreover, the code cache for the wrappers also does. So start can be hijacked with sandbox corruption by:

- Swapping the dispatch handle of the JSFunction (via some race?) to another one
- Or corrupting the cache to install some custom compatible code on the JSFunction (this was chosen for the PoC)

Start is called during instantiation in [InstanceBuilder::ExecuteStartFunction](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;l=1561-1587;drc=e1bbad0f24864aead83224b08f5cb000bac8fa32) like so:

```
bool InstanceBuilder::ExecuteStartFunction() {
  // ... snipped...

  // Call the JS function.
  DirectHandle<Object> undefined = isolate_->factory()->undefined_value();
  MaybeDirectHandle<Object> retval =
      Execution::Call(isolate_, start_function_, undefined, {});
  hsi->LeaveContext();
  // {start_function_} has to be called only once.
  start_function_ = {};

  if (retval.is_null()) {
    DCHECK(isolate_->has_exception());
    return false;
  }
  return true;
}

```

At this point, nothing besides in-sandbox data is retaining the instantiator's dispatch entry, so the hijacked start can be leveraged to free and reclaim it with a greater formal parameter count.

Furthermore, notice if the start function throws an exception it returns false which eventually cascades to fail the instantiation and tail back to JS using the dispatch entry it came in with:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/runtime/runtime-compiler.cc;l=305-308;drc=f27e813c120e8114d73f609f98f9414b761eab06
RUNTIME_FUNCTION(Runtime_InstantiateAsmJs) {
  // ... snipped ...
  DCHECK_EQ(function->code(isolate), *BUILTIN_CODE(isolate, InstantiateAsmJs));
  function->UpdateCode(isolate, *BUILTIN_CODE(isolate, CompileLazy));
  DCHECK(!isolate->has_exception());
  return Smi::zero();
}
**Note:** While `CompileLazy` is seemingly being installed on the instantiator here, this code is subject to TOCTOU. The dispatch handle is being retrieved from the JSFunction rather than the stack/register, so user code could have just corrupted the dispatch handle of the JSFunction to some other thing.

// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/builtins/builtins-internal-gen.cc;l=1659-1669;drc=98bde8d7cbfda1946837ae1cc257646d057ebd56
TF_BUILTIN(InstantiateAsmJs, JSTrampolineAssembler) {
  // ... snipped ...

  // Call runtime, on success just pass the result to the caller and pop all
  // arguments. A smi 0 is returned on failure, an object on success.
  TNode<JSAny> maybe_result_or_smi_zero = CallRuntime<JSAny>(
      Runtime::kInstantiateAsmJs, context, function, stdlib, foreign, heap);
  GotoIf(TaggedIsSmi(maybe_result_or_smi_zero), &tailcall_to_function);
  args.PopAndReturn(maybe_result_or_smi_zero);

  BIND(&tailcall_to_function);
  // On failure, tail call back to regular JavaScript by re-calling the given
  // function which has been reset to the compile lazy builtin.
  TailCallJSFunction(function);
}

```

Since the hijacked start can reclaim the dispatch entry with a higher formal parameter count, the stack can be imbalanced during the tail to lead to AAW/PC control as in the past.

#### Some Thoughts

AFAICT, `Builtins_InstantiateAsmJs` is the only trampoline at present which can be abused like this. So, to stop this issue perhaps it suffices to prevent the start function for asm.js from being tampered with. Maybe [this TODO](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;l=1478-1479;drc=e1bbad0f24864aead83224b08f5cb000bac8fa32) to not use an exported function is relevant.

Also, maybe the following should eventually be addressed at some point to prevent future issues like this:

- Unless there is an invariant that user-code cannot execute during trampolines, GC might have to account for dispatch entries that are part of the current execution stack, eg:
  - Track the stack of currently used dispatch entries or traverse the actual stack for spilled handles to prevent freeing or deopting related functions if freeing.
  - Or defer/disallow freeing dispatch entries during such user-code.
- Move the js-to-wasm wrapper cache outside of the sandbox similar to wasm-to-js wrappers(?) if possible or add checks upon retrieving values from it to ensure it's not some corrupted value.

### VERSION

V8 commit: 9421e58f431a7c2f7792cbef49fa5c3baf4b84d3

#### REPRODUCTION CASE

**NOTE (for the shepherd):** To reproduce in CF, the `linux_d8_sandbox_testing` job type with the below shell args should hopefully do the trick.

**Shell args**: `--allow-natives-syntax --sandbox-testing --expose-gc`

**Build args**:

```
is_debug=false
is_asan=true
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true
dcheck_always_on=false
target_cpu="x64"

```

**Sample output (`--disable-in-process-stack-traces` used to show PC)**:

```
$ ./d8 --allow-natives-syntax  --sandbox-testing --expose-gc --disable-in-process-stack-traces ./tail-dispatch-uaf-poc.js
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7ea300000000,0x7fa300000000)
undefined:1: Linking failure in asm.js: Internal wasm failure

## V8 sandbox violation detected!

The sandbox violation was a *read* access which is technically not a sandbox violation. This requires manual investigation.
AddressSanitizer:DEADLYSIGNAL
=================================================================
==1015178==ERROR: AddressSanitizer: SEGV on unknown address 0x424242424242 (pc 0x424242424242 bp 0x424242424242 sp 0x7ffe85ad0530 T0)
==1015178==The signal is caused by a READ memory access.
    #0 0x424242424242  (<unknown module>)

==1015178==Register values:
rax = 0x00007ea300000011  rbx = 0x00007ffe85ad0471  rcx = 0x0000000000000000  rdx = 0x00007ea300000011  
rdi = 0x00007ea30101f459  rsi = 0x0000000000000000  rbp = 0x0000424242424242  rsp = 0x00007ffe85ad0530  
 r8 = 0x0000000000000017   r9 = 0x0000000000000000  r10 = 0x000074af0a8f19f0  r11 = 0x00007ffe85ad0551  
r12 = 0x00007ffe85ad0470  r13 = 0x0000779f0a8e1080  r14 = 0x00007ea300000000  r15 = 0x0000771f0a8e0309  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (<unknown module>) 
==1015178==ABORTING

```
### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Krishna Ravishankar (@krsh732)

## Attachments

- [tail-dispatch-uaf-poc.js](attachments/tail-dispatch-uaf-poc.js) (text/javascript, 3.8 KB)

## Timeline

### za...@google.com (2025-11-20)

Triaging this v8 sandbox bug based on guideline, assigning it to v8 shepherd for further triage.

### ch...@google.com (2025-11-20)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### cl...@appspot.gserviceaccount.com (2025-11-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4553483382358016.

### cl...@appspot.gserviceaccount.com (2025-11-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5820120777555968.

### bi...@google.com (2025-11-26)

This appears to be different from [b/430960844](https://issues.chromium.org/issues/430960844). Clemens, could you ptal?

### cl...@chromium.org (2025-11-26)

Didn't have time to look into this today; CCing a few folks for visibility.

I'll need to understand first which checks the JSDispatchHandle has (I thought each handle knows the expected formal parameter count?), and why we can confuse them without tripping over some check...

### kr...@gmail.com (2025-11-26)

Here's some info in case it helps!

> I thought each handle knows the expected formal parameter count

Yes, as the JSDispatchHandle refers to a JSDispatchEntry which contains the entrypoint and formal parameter count.

> and why we can confuse them without tripping over some check

The handle itself isn't being confused as the double fetch for the handle while tailing was fixed as part of [crbug/430960844](https://crbug.com/430960844). So instead of changing the dispatch handle[0], this bypass changes the contents of the JSDispatchEntry that the JSDispatchHandle refers to.

To change the contents of the JSDispatchEntry, the garbage collector was abused similar to [crbug/443772809](https://crbug.com/443772809). This bypass hijacks the asm.js start function which runs during the Builtins\_InstantiateAsmJs trampoline to do the following:

1. Orphan the instantiator's JSDispatchEntry by removing all references of its JSDispatchHandle (all the references happen to be inside the sandbox).
2. Trigger garbage collection to free the JSDispatchEntry.
3. Reclaim the target JSDispatchEntry for some another function with a higher formal parameter count.

So when Builtins\_InstantiateAsmJs tails, it's still going to tail using the dispatch handle it entered with like it should be. It's just that now when it tails, the actual dispatch entry that the dispatch handle refers to has changed to contain some other entrypoint and formal parameter count to cause under-application once again.

[0] For convenience, the PoC does actually change the dispatch handle on the instantiator's JSFunction, to get CompileLazy installed elsewhere. This has nothing to do with the tailing and underapplication, as the tail still uses the original dispatch handle as it should be. It's possible to write the bypass without abusing this TOCTOU by corrupting the exports to return an smi (similar to [crbug/430960844](https://crbug.com/430960844)) to trigger tailing without CompileLazy getting installed anywhere.

### cl...@chromium.org (2025-12-02)

Thanks, I'll look into this now.

### cl...@chromium.org (2025-12-02)

I see two ways to fix this.

The simplest would be a targeted fix to the `InstantiateAsmJs` builtin. Just before the tail call, it should check that the parameter count on the dispatch handle is still the expected value. This is a fix we could land immediately.

A much better fix would be to make the GC visit dispatch handles which are held alive via the stack (the dispatch handle is passed to JS functions for leaptiering, IIUC). That value should be visited when visiting the stack. This sounds like a much more complicated solution, but more robust as it would prevent the UAF.

Oli / Michael: Opinions?

I'll prepare the simple fix in the meantime.

### cl...@chromium.org (2025-12-02)

This adds a `CSA_SBXCHECK` to catch the parameter count mismatch on the dispatch handle (the simple fix): <https://crrev.com/c/7210825>

### ml...@chromium.org (2025-12-02)

There's still an open GC issue where unrelated threads (Isolates) all share the same table. I hope this isn't used as proxy here.

> A much better fix would be to make the GC visit dispatch handles which are held alive via the stack (the dispatch handle is passed to JS functions for leaptiering, IIUC). That value should be visited when visiting the stack. This sounds like a much more complicated solution, but more robust as it would prevent the UAF.

Yeah, having the dispatch handle as first class primitive would be best. Can we put it on a trusted object as a proxy ?

### cl...@chromium.org (2025-12-02)

> There's still an open GC issue where unrelated threads (Isolates) all share the same table. I hope this isn't used as proxy here.

No, the reproducer uses a single isolate, fully single-threaded.

> Yeah, having the dispatch handle as first class primitive would be best. Can we put it on a trusted object as a proxy ?

It's currently stored on the `JSFunction` directly. Are you proposing to (additionally?) store it in a trusted object which is linked from the `JSFunction`, and then keeping that trusted object live while we are using the dispatch handle? Or would we allocate the trusted object on demand and only keep it alive via the frame?
Both sounds a bit fragile. We would need to be careful that optimizations don't drop the reference to the trusted object if it's not used otherwise.

### ml...@chromium.org (2025-12-02)

> It's currently stored on the JSFunction directly. Are you proposing to (additionally?) store it in a trusted object which is linked from the JSFunction, and then keeping that trusted object live while we are using the dispatch handle? Or would we allocate the trusted object on demand and only keep it alive via the frame? Both sounds a bit fragile. We would need to be careful that optimizations don't drop the reference to the trusted object if it's not used otherwise.

I am aware that those are fragile. Stack support would obviously be best.

### dx...@google.com (2025-12-02)

Project: v8/v8  

Branch:  main  

Author:  Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7210825>

[sandbox] Prevent UAF of dispatch handle

---


Expand for full commit details
```
     
    The `InstantiateAsmJs` builtin calls out to JS code and afterwards uses 
    the passed-in dispatch handle for a tail call. 
    Nothing (except for in-sandbox objects) keeps the dispatch handle alive 
    though. So the dispatch handle could be freed and re-allocated by the JS 
    code and the tail-call would call code with a different parameter count, 
    corrupting the stack. 
     
    This CL adds a check for the expected parameter count just before the 
    tail call. 
     
    See the linked issue for a discussion on a more complete mitigation of 
    the problem. 
     
    R=olivf@chromium.org 
    CC=mlippautz@chromium.org 
     
    Bug: 462217236 
    Change-Id: I3a91b7b70253fd31ed2bb507feeb130e0959df36 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7210825 
    Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Clemens Backes <clemensb@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104059}

```

---

Files:

- M `src/builtins/builtins-internal-gen.cc`
- M `src/codegen/code-stub-assembler.cc`
- A `test/mjsunit/sandbox/regress/regress-462217236.js`

---

Hash: [1f64f8ec5d55233b184c277a611c9bade0441c6b](https://chromiumdash.appspot.com/commit/1f64f8ec5d55233b184c277a611c9bade0441c6b)  

Date: Tue Dec 2 14:32:18 2025


---

### cl...@chromium.org (2025-12-03)

I created a tracking bug for keeping dispatch handles alive on the stack: <https://crbug.com/465487205>

I'll close this one as fixed then.

CF confirmed the fix: `[2025-12-03 07:31:22 UTC] clusterfuzz-tworker-35dz: Progression task finished: fixed in range r104058:104059.`

### sp...@google.com (2025-12-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
V8 sandbox bypass with control of PC


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> V8 sandbox bypass with control of PC

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/462217236)*
