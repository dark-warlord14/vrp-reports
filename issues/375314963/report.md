# Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)).

| Field | Value |
|-------|-------|
| **Issue ID** | [375314963](https://issues.chromium.org/issues/375314963) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>Runtime |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jo...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2024-10-24 |
| **Bounty** | $1,000.00 |

## Description

# Title:

Debug check failed: kCanBeWeak || (!IsSmi() == HAS\_STRONG\_HEAP\_OBJECT\_TAG(ptr\_)).

## Component:

Blink>JavaScript>Runtime

## Description:

In some situations, during the gc iteration of `TurbofanJSOptimizedFrame`, the `TaggedOutgoingParams` may be unexpectedly controlled.

```
void CommonFrame::IterateTurbofanJSOptimizedFrame(RootVisitor* v) const {
  ...
  // Find the code and compute the safepoint information.
  const Address inner_pointer = maybe_unauthenticated_pc();
  InnerPointerToCodeCache::InnerPointerToCodeCacheEntry* entry =
      isolate()->inner_pointer_to_code_cache()->GetCacheEntry(inner_pointer);
  CHECK(entry->code.has_value());
  Tagged<GcSafeCode> code = entry->code.value();
  DCHECK(code->is_turbofanned());
  SafepointEntry safepoint_entry =
      GetSafepointEntryFromCodeCache(isolate(), inner_pointer, entry);

#ifdef DEBUG
  // Assert that it is a JS frame and it has a context.
  intptr_t marker =
      Memory<intptr_t>(fp() + CommonFrameConstants::kContextOrFrameTypeOffset);
  DCHECK(!StackFrame::IsTypeMarker(marker));
#endif  // DEBUG

  // Determine the fixed header and spill slot area size.
  int frame_header_size = StandardFrameConstants::kFixedFrameSizeFromFp;
  int spill_slot_count =
      code->stack_slots() - StandardFrameConstants::kFixedSlotCount;

  // Fixed frame slots.
  FullObjectSlot frame_header_base(&Memory<Address>(fp() - frame_header_size));
  FullObjectSlot frame_header_limit(
      &Memory<Address>(fp() - StandardFrameConstants::kCPSlotSize));

  FullObjectSlot parameters_limit = frame_header_base - spill_slot_count;

  if (!InFastCCall()) {
    // Parameters passed to the callee.
    FullObjectSlot parameters_base(&Memory<Address>(sp()));

    // Visit the outgoing parameters if they are tagged.
    if (HasTaggedOutgoingParams(code)) {
      v->VisitRootPointers(Root::kStackRoots, nullptr, parameters_base,                    [1]
                           parameters_limit);
    }
  } else {
    // There are no outgoing parameters to visit for fast C calls.
  }
  ...
}

```

I wrote a testcase to trigger this vulnerability.

Just use the latest d8 build from <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-96792.zip?generation=1729761386387720&alt=media>

run command

```
./d8 poc.js

```

It will crash with decheck `Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_))`.

And in the release version, it may get a SEGV on address related to the controlled value `0xdeadbeaf`.

I believe this vulnerability may be exploited. I will try and update if success.

## Crash Log:

```
#
# Fatal error in ../../src/objects/tagged-impl.h, line 142
# Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)).
#
#
#
#FailureMessage Object: 0x718c9ceb7460
==== C stack trace ===============================

    ./d8(__interceptor_backtrace+0x46) [0x5681b72ddbb6]
    /test/test/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x758cac2d8513]
    /test/test/libv8_libplatform.so(+0x3687a) [0x758ca09e187a]
    /test/test/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x2a0) [0x758cac2a2c20]
    /test/test/libv8_libbase.so(+0x56cdf) [0x758cac2a1cdf]
    /test/test/libv8.so(v8::internal::ClearStaleLeftTrimmedPointerVisitor::VisitRootPointers(v8::internal::Root, char const*, v8::internal::FullObjectSlot, v8::internal::FullObjectSlot)+0x118) [0x758ca5db0bb8]
    /test/test/libv8.so(v8::internal::CommonFrame::IterateTurbofanJSOptimizedFrame(v8::internal::RootVisitor*) const+0x3da) [0x758ca582c0ea]
    /test/test/libv8.so(v8::internal::Isolate::Iterate(v8::internal::RootVisitor*, v8::internal::ThreadLocalTop*)+0x5a8) [0x758ca5864b78]
    /test/test/libv8.so(v8::internal::Heap::IterateRoots(v8::internal::RootVisitor*, v8::base::EnumSet<v8::internal::SkipRoot, int>, v8::internal::Heap::IterateRootsMode)+0x539) [0x758ca5d65529]
    /test/test/libv8.so(v8::internal::ScavengerCollector::CollectGarbage()+0x140c) [0x758ca601221c]
    /test/test/libv8.so(v8::internal::Heap::Scavenge()+0x57a) [0x758ca5d53a4a]
    /test/test/libv8.so(v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*)+0xbc0) [0x758ca5d50360]
    /test/test/libv8.so(+0x53b7ff2) [0x758ca5db7ff2]
    /test/test/libv8.so(+0x53b77d7) [0x758ca5db77d7]
    /test/test/libv8.so(+0x85453a3) [0x758ca8f453a3]
Trace/breakpoint trap

```
## VERSION

Chrome Version: V8 13.2.0

Operating System: Linux

## CREDIT

Anonymous.

## Timeline

### jo...@gmail.com (2024-10-24)

## poc.js

```
let wasm_module = new WebAssembly.Module(new Uint8Array([0,97,115,109,1,0,0,0,1,11,1,96,6,127,127,127,127,127,127,1,127,2,7,1,1,109,1,102,0,0,7,8,1,4,98,111,111,109,0,0]));
let wasm_instance = new WebAssembly.Instance(wasm_module, {m: {f: () => {}}});
while(true) { wasm_instance.exports.boom(0, 0, 0, 0, 0x5deadbea, 0xdeadbeaf);}

```

### za...@google.com (2024-10-24)

Hi clemensb@ can you please take a look at this v8 bug? Thank you! 

### cl...@chromium.org (2024-10-24)

Looking, and also uploading to CF as the testcase is too short to be dangerous.

### cl...@appspot.gserviceaccount.com (2024-10-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6314603487100928.

### cl...@chromium.org (2024-10-24)

In mjsunit syntax:

```
d8.file.execute('test/mjsunit/wasm/wasm-module-builder.js');

const builder = new WasmModuleBuilder();
let $sig0 = builder.addType(makeSig([kWasmI32, kWasmI32, kWasmI32, kWasmI32, kWasmI32, kWasmI32], [kWasmI32]));
let f0 = builder.addImport('m', 'f', $sig0);

builder.addExport('boom', f0);

const instance = builder.instantiate({m: {f: () => {}}});
while (true) { instance.exports.boom(0, 0, 0, 0, 0x5deadbea, 0xdeadbeaf) }

```

### pe...@google.com (2024-10-24)

Setting milestone because of s0/s1 severity.

### cl...@appspot.gserviceaccount.com (2024-10-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5366432632078336.

### cl...@chromium.org (2024-10-24)

I don't know why Clusterfuzz couldn't reproduce on the first try. That was asan, let's see if the second run reproduces.

I'll also run a bisection locally in the meantime.

### cl...@chromium.org (2024-10-24)

Oh, funky, looks like this does not reproduce on ToT any more. I'll run a reverse bisection then. Must have been fixed pretty recently. Maybe it was the `--turboshaft-wasm` flag switch after all? Even though it still does not reproduce with `--no-turboshaft-wasm`...

### cl...@chromium.org (2024-10-24)

I will also re-upload to Clusterfuzz on an older revision where I can reproduce locally.

### cl...@appspot.gserviceaccount.com (2024-10-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4965347564126208.

### cl...@chromium.org (2024-10-24)

This was fixed by:

```
commit 534c66a175cef8102cbe8b5562cc44269eb69048
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Thu Oct 24 12:41:08 2024 +0200

    [wasm][type-reflection] Use shared wrappers for WasmJSFunctions
    
    Now that we have per-process shared WasmToJS wrappers, we can
    and should use them for WasmJSFunctions (from the Type Reflection
    proposal) as well.
    This lets us drop a bunch of custom machinery (WasmToJS wrappers
    as movable Code objects, and the trampoline to call them).
    
    Bug: 42204526
    Change-Id: Ie639982e547380cae6ee703dd501385797b42714
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5952535
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#96809}

```

### 24...@project.gserviceaccount.com (2024-10-24)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-10-24)

Detailed Report: https://clusterfuzz.com/testcase?key=4965347564126208

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)) in tagged-impl.h
  v8::internal::ClearStaleLeftTrimmedPointerVisitor::VisitRootPointers
  v8::internal::CommonFrame::IterateTurbofanJSOptimizedFrame
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96529:96530

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4965347564126208

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### jo...@gmail.com (2024-10-25)

Re #13:

Oh, right.

This vul is mainly about the inlined JS-TO-WASM.

When it happens, the `HasTaggedOutgoingParams` function needs to check if the callee wasm code is in the WasmCodeManager.

```
bool CommonFrame::HasTaggedOutgoingParams(
    Tagged<GcSafeCode> code_lookup) const {
#if V8_ENABLE_WEBASSEMBLY
  // With inlined JS-to-Wasm calls, we can be in an OptimizedJSFrame and
  // directly call a Wasm function from JavaScript. In this case the Wasm frame
  // is responsible for visiting incoming potentially tagged parameters.
  // (This is required for tail-call support: If the direct callee tail-called
  // another function which then caused a GC, the caller would not be able to
  // determine where there might be tagged parameters.)
  wasm::WasmCode* wasm_callee =
      wasm::GetWasmCodeManager()->LookupCode(isolate(), callee_pc());
  if (wasm_callee) return false;

  Tagged<Code> wrapper =
      isolate()->builtins()->code(Builtin::kWasmToJsWrapperCSA);
  if (callee_pc() >= wrapper->instruction_start() &&
      callee_pc() <= wrapper->instruction_end()) {
    return false;
  }
  return code_lookup->has_tagged_outgoing_params();
#else
  return code_lookup->has_tagged_outgoing_params();
#endif  // V8_ENABLE_WEBASSEMBLY
}

```

Before, the tier-up wasm-to-js wrapper code will not be added to the cache.

Thus the result `wasm_callee` will be nullptr.

And also, after inline, the code keeps kind of `TURBOFAN_JS`, so `code_lookup->has_tagged_outgoing_params()` also returns true.

So, `HasTaggedOutgoingParams` returns the wrong result with `true`.

This commit adds the tier-up wrapper code to the cache.

Just a few hours after this report, the commit was landed.

What a coincidence.

### cl...@chromium.org (2024-10-25)

Yes, what a coincidence!

Thanks for the debugging, I didn't come to it yet.

I can confirm that with `--no-turbo-inline-js-wasm-calls`, it does not reproduce (before the CL that fixed it anyway).

The big open question now is whether we can come up with a simple fix which is backmergable to beta and stable.

### cl...@chromium.org (2024-10-25)

The analysis in #16 looks correct. What I see in gdb is a `TURBOFAN_JS` frame which directly calls a `WASM_TO_JS_FUNCTION` frame, so the js-to-wasm frame was inlined. But before the change in [1] the code was not added to the wrapper cache, so `HasTaggedOutgoingParams()` returns true and we then crash when visiting the `0xdeadbeaf` pointer.

### cl...@chromium.org (2024-10-25)

BTW, Clusterfuzz claims that this only fails since `414c594 [wasm] Use CanonicalSig in the compilers by Jakob Kummerow · 2 weeks ago`, which would be nice, but I doubt it. I'll try reproducing earlier.

### jk...@chromium.org (2024-10-25)

Maybe we should try to revive the reverted <https://chromium-review.googlesource.com/c/v8/v8/+/4514337>, to fix these stack walking issues once and for all. I was hoping that Conservative Stack Scanning would make it unnecessary to spend the time, but that seems to have a hard-to-predict timeline...

### cl...@chromium.org (2024-10-25)

That definitely has my +1!

I just checked what happened before the CL in #19, where it does not reproduce any more, and there we don't seem to inline the js-to-wasm wrapper. When iterating the stack, I see `TURBOFAN` -> `TURBOFAN_STUB_WITH_CONTEXT` -> `WASM_TO_JS_FUNCTION`.

I verified that the code for the middle frame is indeed a `JS_TO_WASM_FUNCTION` kind.

Jakob, any idea why your CL would enable inlining of the js-to-wasm wrapper here?

### cl...@chromium.org (2024-10-25)

Setting FoundIn label based on that bisection (which was manually verified, but we don't fully understand it yet).

### jo...@gmail.com (2024-10-25)

Re #21:

I think it's because `IsWasmTrustedInstanceData(implicit_arg)` returns false here.

<https://source.chromium.org/chromium/chromium/src/+/refs/tags/130.0.6723.9:v8/src/compiler/js-call-reducer.cc;l=3841>

```
Reduction JSCallReducer::ReduceCallWasmFunction(Node* node,
                                                SharedFunctionInfoRef shared) {
  DCHECK(flags() & kInlineJSToWasmCalls);

  JSCallNode n(node);
  const CallParameters& p = n.Parameters();

  // Avoid deoptimization loops
  if (p.speculation_mode() == SpeculationMode::kDisallowSpeculation) {
    return NoChange();
  }

  const wasm::FunctionSig* wasm_signature = shared.wasm_function_signature();
  if (!CanInlineJSToWasmCall(wasm_signature)) {
    return NoChange();
  }

  const wasm::WasmModule* wasm_module = shared.wasm_module();
  if (wasm_module_for_inlining_ == nullptr) {
    wasm_module_for_inlining_ = wasm_module;
  }

  wasm::NativeModule* native_module = nullptr;
  if (shared.object()->HasWasmExportedFunctionData()) {
    // TODO(jkummerow): Introduce a pointer from WasmExportedFunctionData
    // to WasmTrustedInstanceData.
    Tagged<TrustedObject> implicit_arg = shared.object()
                                             ->wasm_exported_function_data()
                                             ->internal()
                                             ->implicit_arg();
    if (!IsWasmTrustedInstanceData(implicit_arg)) return NoChange();                               [1]
    native_module =
        Cast<WasmTrustedInstanceData>(implicit_arg)->native_module();
  }

```

And after that, this code is not used.

### cl...@chromium.org (2024-10-25)

Aha, that makes sense. So a backmergable fix for M-131 might be to just re-introduce that check temporarily.

### cl...@chromium.org (2024-10-25)

Bringing back that bailout is trivial:

```
diff --git a/src/compiler/js-call-reducer.cc b/src/compiler/js-call-reducer.cc
index ebb920fab3b..690646ebe2b 100644
--- a/src/compiler/js-call-reducer.cc
+++ b/src/compiler/js-call-reducer.cc
@@ -3843,6 +3843,12 @@ Reduction JSCallReducer::ReduceCallWasmFunction(Node* node,
     wasm_module_for_inlining_ = wasm_module;
   }
 
+  // Bail out if we are not calling an actual Wasm function.
+  // TODO(375314963): Remove this again.
+  Tagged<TrustedObject> implicit_arg =
+      function_data->internal()->implicit_arg();
+  if (!IsWasmTrustedInstanceData(implicit_arg)) return NoChange();
+
   // TODO(mliedtke): We should be able to remove module, signature, native
   // module and function index from the SharedFunctionInfoRef. However, for some
   // reason I may dereference the SharedFunctionInfoRef here but not in

```

I think we should land that, merge it to the 13.1 branch, and then remove it again.
I'll upload a CL for that.

### pe...@google.com (2024-10-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-10-25)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### ap...@google.com (2024-10-28)

Project: v8/v8  

Branch: main  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5965086>

[wasm] Limit inlining of JS-to-Wasm wrappers

---


Expand for full commit details
```
[wasm] Limit inlining of JS-to-Wasm wrappers 
 
We should only inline wrappers that call actual Wasm functions. 
 
R=jkummerow@chromium.org 
 
Fixed: 375314963 
Change-Id: I4e614dcc15396751b6d5438ec9b3f28688e9be3b 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5965086 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#96862}

```

---

Files:

- M `src/compiler/js-call-reducer.cc`
- A `test/mjsunit/regress/wasm/regress-375314963.js`

---

Hash: 6c19fb20cc71ef4cfaab17bab69b96448b94aa53  

Date:  Mon Oct 28 14:36:27 2024


---

### pe...@google.com (2024-10-29)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### cl...@chromium.org (2024-10-29)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://crrev.com/c/5965086>

2. Has this fix been verified on Canary to not pose any stability regressions?

Not yet, but it rolled into chromium this morning (<https://chromiumdash.appspot.com/commit/a43b17d3cb92abe6d587e06eb486f9c46c2a4e72>)

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

No.

6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

Done.

### pe...@google.com (2024-10-29)

Merge review required: M131 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### cl...@chromium.org (2024-10-29)

Huh, a second questionnaire?

1. Why does your merge fit within the merge criteria for these milestones?

Fixes a security issue on beta.

2. What changes specifically would you like to merge? Please link to Gerrit.

<https://crrev.com/c/5965086>

3. Have the changes been released and tested on canary?

Not yet, but it rolled into chromium this morning (<https://chromiumdash.appspot.com/commit/a43b17d3cb92abe6d587e06eb486f9c46c2a4e72>)

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>

n/a

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

no

### pg...@google.com (2024-11-01)

I do not see anything relevant on canary where available!

merge approved for M131 - please merge by Nov 4th Monday EOD MTV time to get this into the M131 stable release!

### jo...@gmail.com (2024-11-04)

Hello, Amy. How about the VRP?

### pe...@google.com (2024-11-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-11-04)

Project: v8/v8  

Branch: refs/branch-heads/13.1  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5988573>

Merged: [wasm] Limit inlining of JS-to-Wasm wrappers

---


Expand for full commit details
```
Merged: [wasm] Limit inlining of JS-to-Wasm wrappers 
 
We should only inline wrappers that call actual Wasm functions. 
 
(cherry picked from commit 6c19fb20cc71ef4cfaab17bab69b96448b94aa53) 
 
Change-Id: Id26d8f5461b4220773acc1251daf1b7a11cfd031 
Fixed: 375314963 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5988573 
Auto-Submit: Matthias Liedtke <mliedtke@chromium.org> 
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.1@{#10} 
Cr-Branched-From: 7998da66cb2883ef9734743857713b1194212d9a-refs/heads/13.1.201@{#1} 
Cr-Branched-From: 5e9af2a913539cf67091def99b62f49afece6f56-refs/heads/main@{#96554}

```

---

Files:

- M `src/compiler/js-call-reducer.cc`
- A `test/mjsunit/regress/wasm/regress-375314963.js`

---

Hash: 53ad46b44bd26f634fdedc182485ceaf8b6c1a2e  

Date:  Mon Oct 28 14:36:27 2024


---

### pe...@google.com (2024-11-04)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### am...@chromium.org (2024-11-04)

re c#34, hello -- since this was just resolved on 29th October (and I have been OOO and we did not have a panel session last week), it missed the cutoff for the previous VRP panel session; this will be assessed at this week's or a future VRP Panel session soon

### jo...@gmail.com (2024-11-05)

deleted

### ap...@google.com (2024-11-06)

Project: v8/v8  

Branch: main  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5998614>

[wasm] Remove unnecessary bailout

---


Expand for full commit details
```
[wasm] Remove unnecessary bailout 
 
The underlying issue was fixed by https://crrev.com/c/5952535 and the 
temporary fix (https://crrev.com/c/5965086) was merged to all relevant 
channels. Hence remove the bailout again. 
 
R=jkummerow@chromium.org 
 
Bug: 375314963 
Change-Id: I8c5003206c378c8de95c88b37e4af36d71d48326 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5998614 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97014}

```

---

Files:

- M `src/compiler/js-call-reducer.cc`

---

Hash: aff79052e818e9d438e39a7dd48b21d614833f3d  

Date:  Wed Nov 06 10:58:05 2024


---

### sp...@google.com (2024-11-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1,000 thank you for your report that lead to the backmerge of the already landed fix for a known bug


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-08)

Thank you for the report. Since the root issue was already known and resolved, we are unable to extend a full reward for this issue. However, we do appreciate this report and that it enabled a backmergeable fix in the meantime of the already landed resolution. Thank you for your efforts -- nice work!

### jo...@gmail.com (2024-11-08)

Get.

### pe...@google.com (2024-12-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-12-10)

1. <https://crrev.com/c/5991853>
2. Low,only a few simple conflicts
3. 131
4. Yes

### rz...@google.com (2024-12-11)

Abandoning merge to 126-LTS, only 131 was affected by the issue.

### pe...@google.com (2025-02-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/375314963)*
