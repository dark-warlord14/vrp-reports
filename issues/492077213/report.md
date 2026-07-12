# V8 Sandbox Bypass: Fast API overload metadata corruption causes compiler-emitted mixed native call type confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [492077213](https://issues.chromium.org/issues/492077213) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gu...@gmail.com |
| **Assignee** | em...@google.com |
| **Created** | 2026-03-12 |
| **Bounty** | $5,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

In V8, Fast API overload metadata is stored as mutable in-heap `[address, signature]` pairs and later trusted by TurboFan during fast-call optimization.
If an attacker can corrupt `c_function_overloads`, they can mix a native callee address from one overload with the C signature of another overload.
This causes a compiler-emitted mixed native call, leading to JS/native type confusion and attacker-controlled memory access.

### Root cause analysis

```
// src/api/api.cc
void FunctionTemplate::SetCallHandler(
    FunctionCallback callback, v8::Local<Data> data,
    SideEffectType side_effect_type,
    const MemorySpan<const CFunction>& c_function_overloads) {
  ...
  if (!c_function_overloads.empty()) {
    // Stores the data for a sequence of CFunction overloads into a single
    // FixedArray, as [address_0, signature_0, ... address_n-1, signature_n-1].
    i::DirectHandle<i::FixedArray> function_overloads =
        i_isolate->factory()->NewFixedArray(static_cast<int>(
            c_function_overloads.size() *
            i::FunctionTemplateInfo::kFunctionOverloadEntrySize));
    int function_count = static_cast<int>(c_function_overloads.size());
    for (int i = 0; i < function_count; i++) {
      const CFunction& c_function = c_function_overloads.data()[i];
      i::DirectHandle<i::Object> address = FromCData<internal::kCFunctionTag>(
          i_isolate, c_function.GetAddress());
      function_overloads->set(
          i::FunctionTemplateInfo::kFunctionOverloadEntrySize * i, *address);
      i::DirectHandle<i::Object> signature =
          FromCData<internal::kCFunctionInfoTag>(i_isolate,
                                                c_function.GetTypeInfo());
      function_overloads->set(
          i::FunctionTemplateInfo::kFunctionOverloadEntrySize * i + 1,
          *signature);
    }
    i::FunctionTemplateInfo::SetCFunctionOverloads(i_isolate, info,
                                                  function_overloads);
  }
  ...

```

`c_function_overloads` is on in-sandbox heap memory, and it is consist of

- entry 0: native function address
- entry 1: signature / type description
- entry 2: next address
- entry 3: next signature
- and so on

```
// src/compiler/heap-refs.cc
ZoneVector<Address> GetCFunctions(Tagged<FixedArray> function_overloads,
                                  Isolate* isolate, Zone* zone) {
  const uint32_t len = function_overloads->ulength().value() /
                       FunctionTemplateInfo::kFunctionOverloadEntrySize;
  ZoneVector<Address> c_functions = ZoneVector<Address>(len, zone);
  for (uint32_t i = 0; i < len; i++) {
    c_functions[i] = v8::ToCData<kCFunctionTag>(
        isolate, function_overloads->get(
                     FunctionTemplateInfo::kFunctionOverloadEntrySize * i));
  }
  return c_functions;
}

ZoneVector<const CFunctionInfo*> GetCSignatures(
    Tagged<FixedArray> function_overloads, Isolate* isolate, Zone* zone) {
  const uint32_t len = function_overloads->ulength().value() /
                       FunctionTemplateInfo::kFunctionOverloadEntrySize;
  ZoneVector<const CFunctionInfo*> c_signatures =
      ZoneVector<const CFunctionInfo*>(len, zone);
  for (uint32_t i = 0; i < len; i++) {
    c_signatures[i] = v8::ToCData<const CFunctionInfo*, kCFunctionInfoTag>(
        isolate, function_overloads->get(
                     FunctionTemplateInfo::kFunctionOverloadEntrySize * i + 1));
  }
  return c_signatures;
}

ZoneVector<Address> FunctionTemplateInfoRef::c_functions(
    JSHeapBroker* broker) const {
  return GetCFunctions(Cast<FixedArray>(object()->GetCFunctionOverloads()),
                       broker->isolate(), broker->zone());
}

ZoneVector<const CFunctionInfo*> FunctionTemplateInfoRef::c_signatures(
    JSHeapBroker* broker) const {
  return GetCSignatures(Cast<FixedArray>(object()->GetCFunctionOverloads()),
                        broker->isolate(), broker->zone());
}

```
```
// src/compiler/fast-api-calls.cc
FastApiCallFunction GetFastApiCallTarget(
    JSHeapBroker* broker, FunctionTemplateInfoRef function_template_info,
    size_t arg_count) {
  if (!v8_flags.turbo_fast_api_calls) return {0, nullptr};

  static constexpr int kReceiver = 1;

  const ZoneVector<const CFunctionInfo*>& signatures =
      function_template_info.c_signatures(broker);
  const size_t overloads_count = signatures.size();

  // Only considers entries whose type list length matches arg_count.
  for (size_t i = 0; i < overloads_count; i++) {
    const CFunctionInfo* c_signature = signatures[i];
    const size_t len = c_signature->ArgumentCount() - kReceiver;
    bool optimize_to_fast_call =
        (len == arg_count) &&
        fast_api_call::CanOptimizeFastSignature(c_signature);

    if (optimize_to_fast_call) {
      return {function_template_info.c_functions(broker)[i], c_signature};
    }
  }

  return {0, nullptr};
}

```

Later, TurboFan reads the addresses and signatures back separately, then pairs them again by index. That means the compiler is trusting mutable heap data for both:

- the callee target
- the calling convention and conversions

If an attacker already has a sandbox-heap write primitive, the victim overload's address slot can be overwritten with the address value taken from a different overload, while leaving the victim overload's signature slot unchanged.

```
// src/compiler/turboshaft/fast-api-call-lowering-reducer.h
template <typename Next>
class FastApiCallLoweringReducer : public Next {
 public:
  TURBOSHAFT_REDUCER_BOILERPLATE(FastApiCallLowering)

  OpIndex REDUCE(FastApiCall)(
      V<FrameState> frame_state, V<Object> data_argument, V<Context> context,
      base::Vector<const OpIndex> arguments,
      const FastApiCallParameters* parameters,
      base::Vector<const RegisterRepresentation> out_reps) {
    ...
    OpIndex callee = __ ExternalConstant(ExternalReference::Create(
        c_function.address, ExternalReference::FAST_C_CALL));

    base::SmallVector<OpIndex, 16> args;
    for (int i = 0; i < c_arg_count; ++i) {
        CTypeInfo type = c_signature->ArgumentInfo(i);
        args.push_back(AdaptFastCallArgument(arguments[i], type, handle_error));
    }
    ...
      OpIndex c_call_result = WrapFastCall(call_descriptor, callee, frame_state,
                                           context, base::VectorOf(args));
    ...

```
```
  OpIndex WrapFastCall(const TSCallDescriptor* descriptor, OpIndex callee,
                       V<FrameState> frame_state, V<Context> context,
                       base::Vector<const OpIndex> arguments) {
    // CPU profiler support.
    OpIndex target_address =
        __ IsolateField(IsolateFieldId::kFastApiCallTarget);
    __ StoreOffHeap(target_address, __ BitcastHeapObjectToWordPtr(callee),
                    MemoryRepresentation::UintPtr());

    OpIndex context_address = __ IsolateField(IsolateFieldId::kContext);

    __ StoreOffHeap(context_address, __ BitcastHeapObjectToWordPtr(context),
                    MemoryRepresentation::UintPtr());

    // Create the fast call.
    OpIndex result = __ Call(callee, frame_state, arguments, descriptor);

    // Reset the CPU profiler target address.
    __ StoreOffHeap(target_address, __ IntPtrConstant(0),
                    MemoryRepresentation::UintPtr());

#if DEBUG
    // Reset the context again after the call, to make sure nobody is using the
    // leftover context in the isolate.
    __ StoreOffHeap(context_address, __ WordPtrConstant(Context::kNoContext),
                    MemoryRepresentation::UintPtr());
#endif

    return result;
  }

```

After heap corruption, the compiler can emit a raw native call whose target and ABI no longer match.

So the emitted machine code becomes a mixed native call.

And it is how type-confusion is achieved.

```
void HandleScope::Initialize(Isolate* v8_isolate) {
  using I = internal::Internals;
  internal::HandleScopeData* current = I::GetHandleScopeData(v8_isolate);
  isolate_ = v8_isolate;
  prev_next_ = current->next; // fake v8_isolate leads to arbitrary address read
  prev_limit_ = current->limit;
  current->level++; // fake v8_isolate leads to arbitrary address write
#ifdef V8_ENABLE_CHECKS
  DoInitializeAsserts(v8_isolate);
  scope_level_ = current->level;
#endif
}

```

- call\_to\_number <- sum\_int64\_as\_bigint
  - the target callback expects `Local<Object>,` `FastApiCallbackOptions&`
  - but the victim signature gives it two `int64_t` values
  - so one `BigInt` becomes a fake `FastApiCallbackOptions*`
  - inside that struct, the first field is `isolate`
  - `HandleScope(options.isolate)` immediately dereferences that fake isolate
  - in my PoC, `current = isolate + 0x230` becomes `0x414141414141`, and the first fault is the read of current->next
  - Potentially, arbitrary write can be achieved by `current->level++`

### VERSION

tested v8 git commit : 51000ec9355ffb6f974a08995eb76e98e2ec8332

v8 git commit that introduces the root cause of this bug:

```
commit 4f28e6d9a162429cee5ea730fbff449a5df0287f
Author: Mike Stanton <mvstanton@chromium.org>
Date:   Fri Feb 21 15:46:07 2020 +0100

    Reland "[turbofan] Fast API calls from TurboFan"
    
    Relanding the Fast C API code with fix for UBSan undefined behavior
    issue.
    
    Design doc:
    http://doc/1SAHn7d8M7CoazTd1laVF8gduFC_ikZWiYuytrR9c4Oc/
    
    This CL implements basic API with integer and pointer types marshaling.

```

v8 git commit that introduces `c_function_overloads`:

```
commit ad4eab00e7ec96730eb2c1b6ddcef14ba2e4becd
Author: Paolo Severini <paolosev@microsoft.com>
Date:   Fri May 14 16:14:14 2021 -0700

    [fastcall] Store multiple CFunction overloads in FunctionTemplateInfo
    
    In order to support Fast API calls with overloads, store a FixedArray
    of c-function addresses and a FixedArray of the corresponding
    FunctionInfo*. For now keep using only the first function in the array.

```
## REPRODUCTION CASE

gn args out/x64.sbx\_rel\_asan:

```
is_debug = false
target_cpu = "x64"
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
is_clang = true
is_asan = true
symbol_level = 2

```

Execute:

```
./out/x64.sbx_rel_asan/d8 \
  --sandbox-testing \
  --expose-fast-api \
  --allow-natives-syntax \
  repro_handlescope_current_plus_0_read.js

```

Result:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7abe00000000,0x7bbe00000000)
donor: fti=0x1004f2d rare@+32 ov@+36 len=2
  [0] = 0x1041069 FOREIGN_TYPE
  [1] = 0x1041071 FOREIGN_TYPE
victim: fti=0x1005325 rare@+32 ov@+36 len=2
  [0] = 0x104137d FOREIGN_TYPE
  [1] = 0x1041385 FOREIGN_TYPE
targetCurrent=0x414141414141
fakeIsolate=0x414141413f11
fakeOptionsPtr=0x7ac000004000
warm0=3
warm1=3
patched victim[0] from 0x104137d to 0x1041069

## V8 sandbox violation detected!

The sandbox violation was a *read* access which is technically not a sandbox violation. This requires manual investigation.
Received signal 11 SEGV_MAPERR 414141414141

==== C stack trace ===============================

out/x64.sbx_rel_asan/d8(___interceptor_backtrace+0x46)[0x5555568f39f6]
out/x64.sbx_rel_asan/d8(+0x63941f0)[0x55555b8e81f0]
out/x64.sbx_rel_asan/d8(+0x2dd1e1a)[0x555558325e1a]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x7ffff7c45330]
out/x64.sbx_rel_asan/d8(+0x1456694)[0x5555569aa694]
[0x5555bb6401c2]
[end of stack trace]
[1]    2617164 segmentation fault  out/x64.sbx_rel_asan/d8 --sandbox-testing --expose-fast-api    

```

Type of crash: sandbox violation

## CREDIT INFORMATION

Reporter credit: Hyeonjun Ahn (@\_deayzl)

## Attachments

- [repro.js](attachments/repro.js) (text/javascript, 5.7 KB)

## Timeline

### th...@chromium.org (2026-03-12)

[security shepherd] Triaging as v8 bug[1](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/shepherd.md#handling-special_case-bugs):

- Assign it to the current v8 shepherd (bikineev@)
- Set it to High Severity (S1)
- Set the OS field to all platforms we use v8 on (everything except iOS)
- Set FoundIn to the oldest active branch (145)
- Set the component to Chromium > Blink > JavaScript

### cl...@appspot.gserviceaccount.com (2026-03-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5033428940521472.

### gu...@gmail.com (2026-03-16)

any update on this issue?

### cl...@appspot.gserviceaccount.com (2026-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5850885032804352.

### dx...@google.com (2026-03-24)

Project: v8/node-ci  

Branch:  main  

Author:  Andreas Haas [ahaas@chromium.org](mailto:ahaas@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7696992>

Update Deps

---


Expand for full commit details
```
     
    Bug: 492077213 
    Change-Id: I337aa796e14e99fe5750146305b2ddfe342f5b00 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/node-ci/+/7696992 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Andreas Haas <ahaas@chromium.org>

```

---

Files:

- M `DEPS`

---

Hash: [8f3fdc15d67a0f4708f3ecd9f48ee4f101216356](https://chromiumdash.appspot.com/commit/8f3fdc15d67a0f4708f3ecd9f48ee4f101216356)  

Date: Tue Mar 24 11:55:05 2026


---

### dx...@google.com (2026-03-25)

Project: v8/v8  

Branch:  main  

Author:  Andreas Haas [ahaas@chromium.org](mailto:ahaas@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7668829>

[fastapi] Store callback and signature in one C++ object

---


Expand for full commit details
```
     
    For fast API callbacks, callback and signature were stored in two 
    different JS heap objects. With sandbox corruption, it was therefore 
    possible to create invalid callback-signature pairs. 
     
    With this CL, callback and signature are stored together in a C++ 
    object, and only a single JS heap object has a reference to it. Thereby, 
    sandbox corruption cannot create invalid callback-signature pairs. 
     
    Fixed: 492077213 
     
    Change-Id: I7316cbec258d28289dcf7374354dbcb59335f564 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7668829 
    Reviewed-by: Arash Kazemi <arashk@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Andreas Haas <ahaas@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106017}

```

---

Files:

- M `include/v8-internal.h`
- M `src/api/api.cc`
- M `src/compiler/heap-refs.cc`
- M `src/objects/templates.cc`
- M `src/objects/templates.h`

---

Hash: [edc949e7c9785abb81ad25b8da9bb5c03c3593e5](https://chromiumdash.appspot.com/commit/edc949e7c9785abb81ad25b8da9bb5c03c3593e5)  

Date: Tue Mar 24 12:55:29 2026


---

### 24...@project.gserviceaccount.com (2026-03-25)

ClusterFuzz testcase 6385562223149056 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=106016:106017

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-26)

Merge review required: M147 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-26)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ah...@google.com (2026-03-26)

1. This issue is a sandbox escape that allows potentially to execute JavaScript code with a completely attacker-defined isolate.
2. <https://chromium-review.googlesource.com/7668829>
3. In 148.0.7754.0
4. No
5. No
6. No

### em...@google.com (2026-03-27)

Tentatively reopening because higher in the stack (<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/js-call-reducer.cc;l=718-721;drc=0de84cf02a392cdba969d4e16a20c79e0be0f3bf>) there are still separate calls that might end up returning out-of-sync data:

```
  TNode<Object> ReduceFastApiCall() {
    // ...
    ExternalReference function_reference = ExternalReference::Create(
        isolate(), &api_function, ExternalReference::DIRECT_API_CALL,
        function_template_info_.c_functions(broker()).data(),
        function_template_info_.c_signatures(broker()).data(),
        static_cast<unsigned>(
            function_template_info_.c_functions(broker()).size()));

```

### cl...@appspot.gserviceaccount.com (2026-03-27)

Detailed Report: https://clusterfuzz.com/testcase?key=4996093460905984

Fuzzer: big_sleep
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 0x7a576da90058
Crash State:
  v8::internal::compiler::fast_api_call::GetFastApiCallTarget
  v8::internal::compiler::JSCallReducer::ReduceCallApiFunction
  v8::internal::compiler::JSCallReducer::ReduceJSCall
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=106016:106017

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4996093460905984

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### em...@google.com (2026-03-27)

(I've attached this new clusterfuzz report to the issue, since it does seem to be related to my [comment #12](https://issues.chromium.org/issues/492077213#comment12), at least the stack is similar and ahaas@' new in-review CL fixes this POC.)

### em...@google.com (2026-03-27)

CL [crrev.com/c/7708355](https://crrev.com/c/7708355) from ahaas@ should fix the issues at `js-call-reducer.cc` and `js-native-context-specialization.cc`.

I think there's still one more variant of this - in the Wasm code?

```
// [1] wasm-compiler.cc
const Address c_address = api_func_data->GetCFunction(isolate, 0);
const v8::CFunctionInfo* c_signature =
    api_func_data->GetCSignature(isolate, 0);
// ^^^ c_signature may be out of sync with c_address?

// [2] templates.cc
Address FunctionTemplateInfo::GetCFunction(Isolate* isolate, int index) const {
  i::DisallowHeapAllocation no_gc;
  return Cast<Managed<CFunctionWithSignature>>(
             Cast<FixedArray>(GetCFunctionOverloads())->get(index))
      ->raw()
      ->address;
}

const CFunctionInfo* FunctionTemplateInfo::GetCSignature(Isolate* isolate,
                                                         int index) const {
  i::DisallowHeapAllocation no_gc;
  return Cast<Managed<CFunctionWithSignature>>(
             Cast<FixedArray>(GetCFunctionOverloads())->get(index))
      ->raw()
      ->signature;
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/wasm-compiler.cc;l=874-876;drc=e28fa5b90bf167ca4f5edaa753106753e1e59a4e>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/templates.cc;l=177-192;drc=e28fa5b90bf167ca4f5edaa753106753e1e59a4e>

### dx...@google.com (2026-03-28)

Project: v8/v8  

Branch:  main  

Author:  Andreas Haas [ahaas@chromium.org](mailto:ahaas@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7708355>

[fastapi] Read c-function and signature atomically

---


Expand for full commit details
```
     
    For the fast API, c-functions and their signature are stored together in 
    a C++ object referenced brom a FixedArray on the JS heap. So far, 
    however, the c-functions and their signatures were loaded separately 
    from the FixedArray, which made it possible that due to raceful changes 
    to the FixedArray, the c-function and the signature loaded from the 
    FixedArray did not match. With this CL, the C++ object is loaded only 
    once from the FixedArray, so the c-function and the signature always 
    match. 
     
    Bug: 492077213 
    Change-Id: I7cf2842486cc9aa6866e8a61e8cb07072a5719ca 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7708355 
    Reviewed-by: Maksim Ivanov <emaxx@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106121}

```

---

Files:

- M `src/compiler/fast-api-calls.cc`
- M `src/compiler/heap-refs.cc`
- M `src/compiler/heap-refs.h`
- M `src/compiler/js-call-reducer.cc`
- M `src/compiler/js-native-context-specialization.cc`

---

Hash: [f5ac1a82d0cf4da9013f7a36c347d3a17bb2291f](https://chromiumdash.appspot.com/commit/f5ac1a82d0cf4da9013f7a36c347d3a17bb2291f)  

Date: Fri Mar 27 16:44:00 2026


---

### dr...@chromium.org (2026-03-30)

I'm going to remove the merge labels here until we know what we need to merge. Feel free to re-request when this bug is ready.

### dx...@google.com (2026-04-01)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7715581>

[wasm] Read c-function and signature atomically

---


Expand for full commit details
```
     
    Similarly to crrev.com/c/7668829 and crrev.com/c/7708355, update the 
    wasm-related code to read the CFunction's address and signature 
    atomically. 
     
    This removes the possibility for a racy in-sandbox corruption to bring 
    the fastapi function's signature out of sync. 
     
    Bug: 492077213 
    Change-Id: I30b2a74bb94bf28f16a3b0f8c741c384aecda86e 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7715581 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Reviewed-by: Arash Kazemi <arashk@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106225}

```

---

Files:

- M `src/compiler/wasm-compiler.cc`
- M `src/logging/log.cc`
- M `src/objects/templates.cc`
- M `src/objects/templates.h`
- M `src/wasm/module-instantiate.cc`

---

Hash: [ef2143b7e2b93dffec266488ce23e84947c138e5](https://chromiumdash.appspot.com/commit/ef2143b7e2b93dffec266488ce23e84947c138e5)  

Date: Wed Apr 1 15:47:54 2026


---

### em...@google.com (2026-04-01)

Not planning to request merges since the chain of CLs is nontrivial. Please let me know if there's a security necessity in backmerges.

### dx...@google.com (2026-04-02)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7721359>

[fastapi] Use uint32\_t for overload count/index

---


Expand for full commit details
```
     
    Refactor the GetCFunctions getters in FunctionTemplateInfo to use 
    unsigned integers for sizes and indices, following the changes made in 
    other parts of V8. 
     
    Also delete the unused isolate parameter. 
     
    Bug: 492077213, 375937549 
    Change-Id: I92f12a3fc4ee1bb54c2672debbcad982489d97f2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7721359 
    Reviewed-by: Arash Kazemi <arashk@chromium.org> 
    Reviewed-by: Daniel Lehmann <dlehmann@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106246}

```

---

Files:

- M `src/compiler/wasm-compiler.cc`
- M `src/logging/log.cc`
- M `src/objects/templates.cc`
- M `src/objects/templates.h`
- M `src/wasm/module-instantiate.cc`

---

Hash: [94134285c4210c31665d0d71ad575aaf18dc3ed5](https://chromiumdash.appspot.com/commit/94134285c4210c31665d0d71ad575aaf18dc3ed5)  

Date: Thu Apr 2 10:04:05 2026


---

### dx...@google.com (2026-04-07)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7723321>

[wasm] Fix fastapi overload index for simulator

---


Expand for full commit details
```
     
    Use the index of the matched fastapi function overload for the 
    V8_USE_SIMULATOR_WITH_GENERIC_C_CALLS mode instead of always using 
    the zeroth one. 
     
    Bug: 492077213, 41492790 
    Change-Id: I9b5ee1b7b1c1a6a7389e71d5686f2754aa33b642 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7723321 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106282}

```

---

Files:

- M `src/wasm/module-instantiate.cc`

---

Hash: [24d775be616807ddc3f31a11cb89f53470cded42](https://chromiumdash.appspot.com/commit/24d775be616807ddc3f31a11cb89f53470cded42)  

Date: Thu Apr 2 11:40:33 2026


---

### dx...@google.com (2026-04-08)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7735734>

[wasm][fastapi] Refactor FindSupportedWasmFastApiFunction

---


Expand for full commit details
```
     
    Slightly polish FindSupportedWasmFastApiFunction interface. 
     
    Add a comment about sandbox safety for non-Chromium code path. 
     
    Bug: 492077213 
    Change-Id: I20a29cac01c7ef37cb13cf7da5b17725459d4a08 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7735734 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106319}

```

---

Files:

- M `src/compiler/wasm-compiler.cc`
- M `src/wasm/module-instantiate.cc`

---

Hash: [cb087e97855162a967f9009c66768f15054760e8](https://chromiumdash.appspot.com/commit/cb087e97855162a967f9009c66768f15054760e8)  

Date: Wed Apr 8 11:20:38 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. v8 Sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492077213)*
