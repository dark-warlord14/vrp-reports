# A security issue related to jspi stack switching

| Field | Value |
|-------|-------|
| **Issue ID** | [346597059](https://issues.chromium.org/issues/346597059) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | jo...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2024-06-12 |
| **Bounty** | $10,000.00 |

## Description

## TITLE

A security issue related to jspi stack switching

## VULNERABILITY DETAILS

During GC, `TypedFrame::Iterate` may be executed to visit those params on stack.

And when JSPI is used, wasm runs on a secondary stack. But during running js imports, it switches to the central stack.

The flags to decide whether it switches to the central stack are the value of `is_wasm_to_js` and the value at offset `WasmToJSWrapperConstants::kCentralStackSPOffset`.

In `TypedFrame::Iterate`:

```
void TypedFrame::Iterate(RootVisitor* v) const {
  ...
  bool is_wasm_to_js =
      code->is_builtin() && code->builtin_id() == Builtin::kWasmToJsWrapperCSA;
  ...
    #if V8_ENABLE_WEBASSEMBLY
  // Load the central stack SP value from the fixed slot.
  // If it is null, the import wrapper didn't switch and the layout is the same
  // as regular typed frames: the outgoing stack parameters end where the spill
  // area begins.
  // Otherwise, it holds the address in the central stack where the import
  // wrapper switched to before pushing the outgoing stack parameters and
  // calling the target. It marks the limit of the stack param area, and is
  // distinct from the beginning of the spill area.
  Address central_stack_sp =
      Memory<Address>(fp() + WasmToJSWrapperConstants::kCentralStackSPOffset);
  FullObjectSlot parameters_limit(
      is_wasm_to_js && central_stack_sp != kNullAddress
          ? central_stack_sp
          : frame_header_base.address() - spill_slots_size);
#else
  FullObjectSlot parameters_limit(frame_header_base.address() -
                                  spill_slots_size);
#endif
  FullObjectSlot parameters_base(&Memory<Address>(sp()));
  ...
}

```

We calculate the `parameters_limit` in different ways under stack switching, and then the `parameters_base`.

Then, params between `parameters_base` and `parameters_limit` gets visited.

```
  // Visit the rest of the parameters.
  if (HasTaggedOutgoingParams(code)) {
    v->VisitRootPointers(Root::kStackRoots, nullptr, parameters_base,
                         parameters_limit);
  }

```

However, I found that in a specific situation, during running gc in js imports, the `fp()` points to the secondary stack, while `is_wasm_to_js` is false and the value at offset `WasmToJSWrapperConstants::kCentralStackSPOffset` is kNullAddress.

Thus, `parameters_limit` points to the secondary stack, and the `parameters_base` points to the central stack. `VisitRootPointers` will then trigger memory corruptions during the for loop.

```
  void VisitRootPointers(Root root, const char* description,
                         FullObjectSlot start, FullObjectSlot end) override {
    for (FullObjectSlot p = start; p < end; ++p) {
        ClearLeftTrimmedOrForward(root, description, p);
    }
  }

```

Here is the situation:

The `StackFrameIterator` judges the frame type with function `StackFrameIterator::ComputeStackFrameType`. And for wasm wrappers:

```
  // If the {pc} does not point into WebAssembly code we can rely on the
  // returned {wasm_code} to be null and fall back to {GetContainingCode}.
  if (wasm::WasmCode* wasm_code =
          wasm::GetWasmCodeManager()->LookupCode(isolate(), pc)) {
    switch (wasm_code->kind()) {
      case wasm::WasmCode::kWasmFunction:
        return StackFrame::WASM;
      case wasm::WasmCode::kWasmToCapiWrapper:
        return StackFrame::WASM_EXIT;
      case wasm::WasmCode::kWasmToJsWrapper:
        return StackFrame::WASM_TO_JS;
      default:
        UNREACHABLE();
    }
  }

```

However, for `WasmToJSWrapper` with origin of type `WasmFuncRef`, the compiled code will not be added to the code manager of the module.

```
RUNTIME_FUNCTION(Runtime_TierUpWasmToJSWrapper) {
  ...
  if (IsWasmFuncRef(*origin)) {
    ...
    Handle<Code> wasm_to_js_wrapper_code =
        compiler::CompileWasmToJSWrapper(
            isolate, &sig, kind, static_cast<int>(expected_arity),
            static_cast<wasm::Suspend>(ref->suspend()))
            .ToHandleChecked();

    // We have to install the optimized wrapper as `code`, as the generated
    // code may move. `call_target` would become stale then.
    Handle<WasmInternalFunction> internal_function{
        WasmFuncRef::cast(*origin)->internal(isolate), isolate};
    ref->set_code(*wasm_to_js_wrapper_code);
    internal_function->set_call_target(
        Builtins::EntryOf(Builtin::kWasmToOnHeapWasmToJsTrampoline, isolate));
    return ReadOnlyRoots(isolate).undefined_value();
  }

```

Therefore, it does not get the frame type `WASM_TO_JS` and only keeps the `TypedFrame`. However, `TypedFrame::Iterate` dose not work for this situation.

I construct a POC to prove it.

You can run it at the latest version of v8 (commit `0ba42aeb3a431168a13f0a456b8e878d511afde9`)

You should use `python3 tools\dev\gm.py x64.debug` to build v8.

or just use the one from <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/win64-debug%2Fd8-asan-win64-debug-v8-component-94385.zip?generation=1718138752805769&alt=media>

commond line:

```
out\x64.debug\d8.exe --expose-gc --wasm-wrapper-tiering-budget=1 --experimental-wasm-jspi poc.js

```
## VERSION

Chrome Version: V8 12.8.0

Operating System: Windows

## Timeline

### jo...@gmail.com (2024-06-12)

The main root cause is that the `StackFrameIterator` is not suitable for the tier-up wrapper with origin of type `WasmFuncRef`.

You can pass this issue to [thibaudm@chromium.org](mailto:thibaudm@chromium.org). I think he can confirm and fix it.

Here is a simple poc.js for windows:

## poc.js

```
// flags: --expose-gc --wasm-wrapper-tiering-budget=1 --experimental-wasm-jspi
let module = new WebAssembly.Module(new Uint8Array([0,97,115,109,1,0,0,0,1,4,1,96,0,0,2,7,1,1,109,1,102,0,0,7,8,1,4,109,97,105,110,0,0]));
let instance = new WebAssembly.Instance(module, {m: {f: () => {gc();}}});
let main = WebAssembly.promising(instance.exports.main);
main();
main();

```
## Credit

Anonymous.

### jo...@gmail.com (2024-06-12)

I test it on windows x64.debug, and the crash log may be like:

```
#
# Fatal error in ..\..\src\objects\tagged-impl.h, line 147
# Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)).
#
#
#
#FailureMessage Object: 0000008DBDBFBF00
==== C stack trace ===============================

        v8::base::debug::StackTrace::StackTrace [0x00007FFE7CD93105+37]
        v8::platform::`anonymous namespace'::PrintStackTrace [0x00007FFE9D8BA0F9+57]
        V8_Fatal [0x00007FFE7CD66173+323]
        v8::base::`anonymous namespace'::DefaultDcheckHandler [0x00007FFE7CD65B1C+44]
        V8_Dcheck [0x00007FFE7CD66281+81]
        v8::internal::TaggedImpl<1,unsigned long long>::IsStrong [0x00007FFE0E55CE79+105]
        v8::internal::TaggedImpl<1,unsigned long long>::IsHeapObject [0x00007FFE0E55CE03+19]
        v8::internal::IsHeapObject [0x00007FFE0E545E72+34]
        v8::internal::ClearStaleLeftTrimmedPointerVisitor::ClearLeftTrimmedOrForward [0x00007FFE0F07647F+79]
        v8::internal::ClearStaleLeftTrimmedPointerVisitor::VisitRootPointers [0x00007FFE0F07625A+138]
        v8::internal::TypedFrame::Iterate [0x00007FFE0ECD230B+1979]
        v8::internal::Isolate::Iterate [0x00007FFE0ECFCD94+868]
        v8::internal::Isolate::Iterate [0x00007FFE0ECFCE85+69]
        v8::internal::Heap::IterateStackRoots [0x00007FFE0F039FF1+33]
        v8::internal::Heap::IterateRoots [0x00007FFE0F033C1B+971]
        v8::internal::MarkCompactCollector::MarkRoots [0x00007FFE0F0CF543+163]
        v8::internal::MarkCompactCollector::MarkLiveObjects [0x00007FFE0F0C4F1D+2765]
        v8::internal::MarkCompactCollector::CollectGarbage [0x00007FFE0F0C43DF+95]
        v8::internal::Heap::MarkCompact [0x00007FFE0F02A722+162]
        v8::internal::Heap::PerformGarbageCollection [0x00007FFE0F029D3D+2093]

```

There maybe many different crash logs for this bug, such as different SEGVs or different Dchecks, depends on the different stack slots between the wrong pair of `parameters_base` and `parameters_limit`.

Also, you may not directly crash on Linux. But you can add a debugging breakpoint at <https://source.chromium.org/chromium/chromium/src/+/0ba42aeb3a431168a13f0a456b8e878d511afde9:v8/src/execution/frames.cc;l=1809> and watch the value of `parameters_base` and `parameters_limit`. After several executions of `TypedFrame::Iterate`, you can reach that `parameters_limit` points to the secondary stack, and the `parameters_base` points to the central stack.

I think it may be successfully exploited. I will try and upload if success within several weeks.

### jo...@gmail.com (2024-06-12)

## BISECT:

I think the bisect should be the commit where the FrameIterator starts to support stack switching of jspi.

```
commit aef80d12d489b55217b63821ce3b0eaca2b5e2ab
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Thu Nov 16 17:02:58 2023 +0100

    Reland^5 "[wasm][x64] Run JS imports on the central stack"

    This is a reland of commit 3ebc66786099800b9c7170fc6e72eb59298dfb7c
    The last revert also reverted one of the previous fixes, which
    was landed separately so it was not included in the reland...
    Just skip the stack-switching-generic-wrapper test again on
    single_generation.

```

### pg...@google.com (2024-06-12)

Setting FoundIn per [comment #4](https://issues.chromium.org/issues/346597059#comment4) (have not confirmed) and provisional severity of S1 and over to the V8 sheriff!

### is...@chromium.org (2024-06-13)

reporter@, thank you for the report! Handing this issue over to Wasm team.

### pe...@google.com (2024-06-13)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### th...@chromium.org (2024-06-17)

Thank you for the report,
If I'm reading this correctly then there is a related issue that existed before JSPI:

```
  if (is_wasm_to_js) {
    IterateParamsOfWasmToJSWrapper(v);
  }

```

If we misidentify the frame type, then we will not scan the parameters of the wrapper. Actually I just managed to write a repro that does not use JSPI: I pass several reference parameters and a bigint, the bigint allocates and triggers a GC (using %SimulateNewspaceFull()), the references don't get scanned because of the bug described in the report, and using them on the JS side crashes.

### jo...@gmail.com (2024-06-17)

Re [comment #9](https://issues.chromium.org/issues/346597059#comment9): Yes. I agree with you. I also notice that `IterateParamsOfWasmToJSWrapper(v)` is not executed due to the wrong frame type. But I failed to construct a POC using gc() and the common wrapper without jspi before submitting the issue.

### th...@google.com (2024-06-17)

> Therefore, it does not get the frame type WASM\_TO\_JS and only keeps the TypedFrame

Expanding on that after some investigation, because there are a few more steps to fully explain what goes wrong:

- After the quoted switch block, we continue and lookup the Code object and switch again on the code kind
- We handle the WASM\_TO\_JS\_FUNCTION code kind in the switch, return the WASM\_TO\_JS\_FUNCTION frame type, and eventually this maps to the frame class `WasmToJsFunctionFrame` (so far that looks reasonable)
- This frame class does not implement its own `Iterate()` function and inherits from `TypedFrame`, so this is how we end up in `TypedFrame::Iterate()`, which only supports iterating the generic wasm-to-js wrapper, not the optimized ones.

But note that inheriting from `WasmFrame` would also be wrong, because `WasmFrame::Iterate()` expects a valid WasmCode object.

I think this can be fixed by changing the `TypedFrame::Iterate()` code to check the code kind and handle optimized wasm-to-js frames, in addition to generic wasm-to-js frames, I'll give it a try.

### th...@google.com (2024-06-17)

Re [comment #10](https://issues.chromium.org/issues/346597059#comment10): even if we did execute it, that would be wrong because the logic inside of it is specific to the generic wasm-to-js wrapper and does not work for the optimized signature-specific wrappers.

### ap...@google.com (2024-06-21)

Project: v8/v8
Branch: main

commit 901377bb2f3b8ff45fbd077fc425fc2f4e66036a
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Fri Jun 21 16:31:15 2024

    [wasm] Fix scanning of wasm-to-js params
    
    Wasm-to-js wrappers are sometimes compiled as on-heap Code objects, for
    example when tiering-up from a WasmFuncRef call origin. The frames of
    these functions are mapped to a subclass of TypedFrame, however
    TypedFrame::Iterate() only supports iterating the generic wasm-to-js
    wrapper.
    
    Add support for iterating the tagged parameters of optimized wasm-to-js
    wrappers in TypedFrame::Iterate. For this we also add two 16-bit fields
    in the Code object to encode the incoming tagged parameter region, which
    we would normally find in the WasmCode data.
    
    R=jkummerow@chromium.org
    
    Fixed: 346597059
    Change-Id: I425619fca86c38f91f1ca9cbeb70e7b5a7b2d6c1
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5639725
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94589}

M       src/compiler/pipeline.cc
M       src/diagnostics/objects-printer.cc
M       src/execution/frames.cc
M       src/execution/frames.h
M       src/objects/code-inl.h
M       src/objects/code.h

https://chromium-review.googlesource.com/5639725


### pe...@google.com (2024-06-22)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-06-22)

Merge review required: M127 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-06-22)

Merge review required: M126 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### th...@chromium.org (2024-06-24)

Comment #14:
1: https://chromium-review.googlesource.com/c/v8/v8/+/5639725
2: Yes
3: No
4: No
5: No

Comment #15 + comment #16:
1: Fixes an S1 security issue
2: https://chromium-review.googlesource.com/c/v8/v8/+/5639725
3: Yes
4: No
5: No
6: No

### am...@chromium.org (2024-06-25)

merges approved for https://crrev.com/c/5639725 -- please merge this fix to 12.7 at soonest (by 10am Pacific tomorrow) so this fix can be included in this week's M127 Beta update

this week's M126 Stable update has already shipped and we are entering release freeze; please still do merge this fix to 12.6 at your earliest convenience so this fix can be included in the first update of M126 Stable following release freeze

### ap...@google.com (2024-06-26)

Project: v8/v8
Branch: refs/branch-heads/12.7

commit a1076a4fd9fbb3083b23a8c4ade98b2d8a721ba4
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Fri Jun 21 16:31:15 2024

    Merged: [wasm] Fix scanning of wasm-to-js params
    
    Wasm-to-js wrappers are sometimes compiled as on-heap Code objects, for
    example when tiering-up from a WasmFuncRef call origin. The frames of
    these functions are mapped to a subclass of TypedFrame, however
    TypedFrame::Iterate() only supports iterating the generic wasm-to-js
    wrapper.
    
    Add support for iterating the tagged parameters of optimized wasm-to-js
    wrappers in TypedFrame::Iterate. For this we also add two 16-bit fields
    in the Code object to encode the incoming tagged parameter region, which
    we would normally find in the WasmCode data.
    
    R=jkummerow@chromium.org
    
    Fixed: 346597059
    (cherry picked from commit 901377bb2f3b8ff45fbd077fc425fc2f4e66036a)
    
    Change-Id: I26e485242754e430720a68f6a57fec2f8f58ac90
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5656653
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.7@{#18}
    Cr-Branched-From: 35cc908918d3f8083955ed8328506f964e17ae40-refs/heads/12.7.224@{#1}
    Cr-Branched-From: 6d60e6734b32211215c8410db6fe2b84b13abe0e-refs/heads/main@{#94324}

M       src/compiler/pipeline.cc
M       src/diagnostics/objects-printer.cc
M       src/execution/frames.cc
M       src/execution/frames.h
M       src/objects/code-inl.h
M       src/objects/code.h

https://chromium-review.googlesource.com/5656653


### ap...@google.com (2024-06-26)

Project: v8/v8
Branch: refs/branch-heads/12.6

commit 8d6bd5e19f96793b5744b1a84139fbf3bc3883cd
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Wed Jun 26 11:24:07 2024

    Merged: [wasm] Fix scanning of wasm-to-js params
    
    Wasm-to-js wrappers are sometimes compiled as on-heap Code objects, for
    example when tiering-up from a WasmFuncRef call origin. The frames of
    these functions are mapped to a subclass of TypedFrame, however
    TypedFrame::Iterate() only supports iterating the generic wasm-to-js
    wrapper.
    
    Add support for iterating the tagged parameters of optimized wasm-to-js
    wrappers in TypedFrame::Iterate. For this we also add two 16-bit fields
    in the Code object to encode the incoming tagged parameter region, which
    we would normally find in the WasmCode data.
    
    R=jkummerow@chromium.org
    
    Fixed: 346597059
    (cherry picked from commit 901377bb2f3b8ff45fbd077fc425fc2f4e66036a)
    
    Change-Id: I1e3345eee73105f05408fc9c26f069e79c7efe3b
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5658371
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.6@{#42}
    Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2}
    Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

M       src/compiler/pipeline.cc
M       src/diagnostics/objects-printer.cc
M       src/execution/frames.cc
M       src/execution/frames.h
M       src/objects/code-inl.h
M       src/objects/code.h

https://chromium-review.googlesource.com/5658371


### jo...@gmail.com (2024-06-26)

Credit: Anonymous.

### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high quality report of memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-26)

Congratulations! Thank you for your efforts and reporting this issue to us -- great work! 

### ap...@google.com (2024-08-14)

Project: v8/v8
Branch: main

commit ab3bfaa628a5a1c5fb77bec8b7fecf6139d5ce74
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Wed Aug 14 17:27:55 2024

    [wasm] Add missing regression tests
    
    R=jkummerow@chromium.org
    
    Bug: 342522151,342415789,346197738,346597059,
    Change-Id: Iace766d0032d0c3def5877ac86440442b2aea04d
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5788586
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95639}

A       test/mjsunit/regress/wasm/regress-342522151.js
A       test/mjsunit/regress/wasm/regress-346197738.js
A       test/mjsunit/regress/wasm/regress-346597059.js

https://chromium-review.googlesource.com/5788586


### ap...@google.com (2024-08-14)

Project: v8/v8
Branch: main

commit 6876e28371bccf8314d951187e8338ed9dbe19aa
Author: Deepti Gandluri <gdeepti@chromium.org>
Date:   Wed Aug 14 21:44:17 2024

    Revert "[wasm] Add missing regression tests"
    
    This reverts commit ab3bfaa628a5a1c5fb77bec8b7fecf6139d5ce74.
    
    Reason for revert: Regression test fails on the single generation bot - https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64%20-%20debug%20-%20single%20generation/16342/overview
    
    Original change's description:
    > [wasm] Add missing regression tests
    >
    > R=jkummerow@chromium.org
    >
    > Bug: 342522151,342415789,346197738,346597059,
    > Change-Id: Iace766d0032d0c3def5877ac86440442b2aea04d
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5788586
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    > Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#95639}
    
    Bug: 342522151,342415789,346197738,346597059,
    Change-Id: I8bb2b3032437519b4794a08f56314f8f9a3a4b7b
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5788832
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Deepti Gandluri <gdeepti@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95645}

D       test/mjsunit/regress/wasm/regress-342522151.js
D       test/mjsunit/regress/wasm/regress-346197738.js
D       test/mjsunit/regress/wasm/regress-346597059.js

https://chromium-review.googlesource.com/5788832


### ap...@google.com (2024-08-19)

Project: v8/v8
Branch: main

commit c0d69082d25cfdd92557f8f922dc282934a89079
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Mon Aug 19 14:58:10 2024

    Reland "[wasm] Add missing regression tests"
    
    This is a reland of commit ab3bfaa628a5a1c5fb77bec8b7fecf6139d5ce74
    
    Change: Skip test that uses %SimulateNewspaceFull in
    single_generation mode, and skip JSPI test on platforms that
    don't implement JSPI yet.
    
    Original change's description:
    > [wasm] Add missing regression tests
    >
    > R=jkummerow@chromium.org
    >
    > Bug: 342522151,342415789,346197738,346597059,
    > Change-Id: Iace766d0032d0c3def5877ac86440442b2aea04d
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5788586
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    > Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#95639}
    
    Bug: 342522151,342415789,346197738,346597059,
    Change-Id: Ib803b351b1a2b4eb45c549408b7cfc004063d9e7
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5797382
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95690}

M       test/mjsunit/mjsunit.status
A       test/mjsunit/regress/wasm/regress-342522151.js
A       test/mjsunit/regress/wasm/regress-346197738.js
A       test/mjsunit/regress/wasm/regress-346597059.js

https://chromium-review.googlesource.com/5797382


### pe...@google.com (2024-09-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/346597059)*
