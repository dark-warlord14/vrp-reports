# Crash in Maglev due to Stale ScopeInfo Cache with Async Generators

| Field | Value |
|-------|-------|
| **Issue ID** | [470831166](https://issues.chromium.org/issues/470831166) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2025-12-22 |
| **Bounty** | $10,000.00 |

## Description

## Details

### Context Node

For `opt_me`, since it is an async generator function, its execution will be suspended (`SuspendGenerator`) and resumed (`ResumeGenerator`) multiple times. Each time it resumes, the context and the Ignition register file are restored based on the `generator_state`.

Therefore, before Maglev optimizes the function body, the `BuildRegisterFrameInitialization()` method adds an `n5` node to represent the `generator_state`. Since the context is obtained from the `generator_state`, the Current Context is loaded as a field from `n5`.

```
    // generator_state
  0xa1c00f41310  n5: RegisterInput(rdx), 0 uses 🪦
    ...
    // Current Context
  0xa1c00f44020  n12: LoadTaggedField(0x10, compressed, Context) [n5], 0 uses 🪦

```
### insert cache into `scope_infos`

When processing the IIFE, a closure must first be created. This calls `GetContext()` to retrieve the current context for creating the closure, and `GetContext()` returns the `n12` node.

Afterward, `BuildCallWithFeedback()` is called to generate the node for the closure call. It's important to note that after getting the closure's context node, `graph()->record_scope_info(context, scope_info)` is called to record the `ScopeInfo` corresponding to the `Context`. This **adds the mapping `n12 => Scope_dummy0` to the `scope_infos_` cache.**

```
ReduceResult MaglevGraphBuilder::BuildCallWithFeedback(
    ValueNode* target_node, CallArguments& args,
    const compiler::FeedbackSource& feedback_source) {
  ...

  if (call_feedback.target().has_value()) {    // Has feedback
    if (call_feedback.target()->IsJSFunction()) {    // The called JSFunction is saved in the feedback
      ...
    } else if (call_feedback.target()->IsFeedbackCell() && args.mode() == CallArguments::kDefault) { // Ploy IC
      compiler::FeedbackCellRef feedback_cell = call_feedback.target()->AsFeedbackCell();
      compiler::OptionalSharedFunctionInfoRef shared = feedback_cell.shared_function_info(broker());

      if (shared.has_value() && !shared->HasBreakInfo(broker())) {
        RETURN_IF_ABORT(BuildCheckJSFunction(target_node));
        ValueNode* target_feedback_cell;
        GET_VALUE_OR_ABORT(target_feedback_cell, BuildLoadJSFunctionFeedbackCell(target_node));
        RETURN_IF_ABORT(
            BuildCheckValueByReference(target_feedback_cell, feedback_cell, DeoptimizeReason::kWrongFeedbackCell));
        if (IsClassConstructor(shared->kind())) {
          ...
        }

        // context: n12
        ValueNode* context;
        GET_VALUE_OR_ABORT(context, BuildLoadJSFunctionContext(target_node));
        // scope_info: Scope_dummy0
        compiler::ScopeInfoRef scope_info = shared->scope_info(broker());
        if (scope_info.HasOuterScopeInfo()) {
          scope_info = scope_info.OuterScopeInfo(broker());
          CHECK(scope_info.HasContext());
          graph()->record_scope_info(context, scope_info); // <===
        }
        ...
      }
    }
  }
  ...
}

```
### Context Load And Store

Subsequently, when processing `i++`, following nodes will be generated:

```
  0xa1c00f410f0  n2: InitialValue(<context>), 0 uses 🪦
  0xa1c00f41310  n5: RegisterInput(rdx), 0 uses 🪦
    // Current Context
  0xa1c00f44020  n12: LoadTaggedField(0x10, compressed, Context) [n5], 0 uses 🪦
  ...
    // n114 = n12->slot[PREVIOUS_INDEX]
  0x132400f581c0  n114: LoadContextSlotNoCells(0xc) [n12], 0 uses 🪦
    // n115 = n114->slot[PREVIOUS_INDEX]
  0x132400f582e8  n115: LoadContextSlotNoCells(0xc) [n114], 0 uses 🪦
    // n116 = n115->slot[2], corresponds to variable i
  0x132400f58410  n116: LoadContextSlotNoCells(0x10) [n115], 0 uses 🪦
    ...

    // i++
 174 : 59 06             Inc FBV[6]
  0x132400f58710  n118: CheckedSmiUntag [n116], 0 uses, but required, cannot truncate to int32
  0x132400f58870  n119: Int32IncrementWithOverflow [n118], 0 uses, but required, cannot truncate to int32


  // Write back to Context_i
 176 : 26 ff 02 02       StaContextSlotNoCell <context>, [2], [2]
  * Reusing cached context slot n12[12]: LoadContextSlotNoCells(0xc) [n12], 1 uses
  * Reusing cached context slot n114[12]: LoadContextSlotNoCells(0xc) [n114], 1 uses
  0x132400f589a8  n120: Int32ToNumber [n119], 0 uses 🪦
  0x132400f58970  n121: StoreTaggedFieldWithWriteBarrier(0x10) [n115, n120]
  * Recording context slot store n115[16]: Int32IncrementWithOverflow [n118], 1 uses, cannot truncate to int32

```

The generated nodes are all correct. Since `StoreAndCacheContextSlot()` writes a new value to the context object, previously recorded context slot become invalid, so `ClearAliasedContextSlotsFor()` is called to clear all aliases.

```
ReduceResult MaglevGraphBuilder::StoreAndCacheContextSlot(
    ValueNode* context, int index, ValueNode* value, ContextMode context_mode) {
  // Generate ContextStore node
  ...

  TRACE("  * Recording context slot store " << PrintNodeLabel(context) << "["
                                            << offset
                                            << "]: " << PrintNode(value));

  auto aliased_slots = known_node_aspects().ClearAliasedContextSlotsFor( // <===
      graph(), context, offset, value);
  bool added_to_cache =
      known_node_aspects().SetContextCachedValue(context, offset, value);
  ...
}

```

`ClearAliasedContextSlotsFor()` first calls `graph->TryGetScopeInfo(context)` to get the `ScopeInfo` of the current context. Here, `context` is the `n115` node, and the crash occurs during this process.

### lookup `scope_infos`

The PoC has three `ScopeInfo` and three `Context` objects, forming a chain. The `scope_infos_` cache stores the `ScopeInfo` for the `n12` node as `Scope_dummy0`.

```
                      Scope_dummy1    Context_dummy1
                        |               |
                        | outer         | previous
                        V               V
scope_infos_[n12]---> Scope_dummy0    Context_dummy0
                        |               |
                        | outer         | previous
                        V               V
                      Scope_i         Context_i

```

The call `TryGetScopeInfo(n115)` attempts to get the `ScopeInfo` for `n115`. According to the Maglev graph execution, the process is as follows:

- `load_script->input(0)` gets the parent context `n114`.
- `TryGetScopeInfoForContextLoad(n114)` is called.
  - `TryGetScopeInfo(n114)` is called.
    - `load_script->input(0)` gets the parent context `n12`.
    - `TryGetScopeInfo(n12)` is called:
      - A cache hit occurs in `scope_infos_`: the `Scope_dummy0` corresponds to the `n12: LoadTaggedField` node.
    - It gets the `OuterScopeInfo` of `Scope_dummy0`, which is `Scope_i`.
  - It then loops to get the `OuterScopeInfo`, but `Scope_i` does not have an `OuterScopeInfo`, leading to a crash.

```
    // n114 = n12->slot[PREVIOUS_INDEX]
  0x132400f581c0  n114: LoadContextSlotNoCells(0xc) [n12], 0 uses 🪦
    // n115 = n114->slot[PREVIOUS_INDEX]
  0x132400f582e8  n115: LoadContextSlotNoCells(0xc) [n114], 0 uses 🪦
    // n116 = n115->slot[2], corresponds to variable i
  0x132400f58410  n116: LoadContextSlotNoCells(0x10) [n115], 0 uses 🪦

```

I believe the result of `TryGetScopeInfo(n12)` is incorrect here: `n12` represents the current context, so for `i++`, the `ScopeInfo` should be `Scope_dummy1`, not `Scope_dummy0`.

In the `TryGetScopeInfo(n115)` call, the context depth is `2` (beacuse there are two `LoadContextSlotNoCells`). Therefore, it starts from `Scope_dummy0` and walks up the chain twice. However, after just one step, `Scope_i` has no outer scope, which causes the crash.

### Root Cause

I believe the root cause is that the cached entry `n12 => ScopeInfo_dummy0` in `scope_infos_` is incorrect. The `n12` node represents the current context, which comes from `n5`. `n5` represents a value from a native register, and for the Maglev optimization process, the value `n5` points to can change; it is not a constant. Therefore, `n12` is a value that needs to be fetched in real-time, and information related to `n12` should not be cached during graph building.

If the line `graph()->record_scope_info(context, scope_info);` in `BuildCallWithFeedback()` is removed to prevent caching, then the call `graph->TryGetScopeInfo(context)` inside `ClearAliasedContextSlotsFor()` will return null. As a result, `ContextMayAlias()` will always return true, which is the safe and correct behavior.

## REPRODUCTION CASE

poc.js:

```
// Context Depth = 2, captures i, denoted as Context_i, Scope_i
for (let i = 0 ; i < 2; i++) 
{   // Context Depth = 1, captures dummy0, denoted as Context_dummy0, Scope_dummy0
    // Create a function, increasing Context Depth
    function dummy0() {
        return dummy0;
    }

    async function* opt_me() {
        // Create a function, denoted as IIFE
        (() => {
            return 0;
        })();

        for (let j = 0; j < 100; j++) { // Context Depth = 0, captures dummy1, denoted as Context_dummy1, Scope_dummy1
            // Create a function, increasing Context Depth
            function dummy1() {
                return dummy1;
            }

            yield j;

            // Write to a variable in Context_i
            i++;
        }
    }
    
    // Create an async iterator
    const async_gen = opt_me();

    // Trigger Maglev optimization
    for(let k=0; k<100; k++) {
        async_gen.next();   // This returns a Promise
    }
}

```

V8 must be built with a debug configuration. Execute v8 as follows:

```
./d8 \
    --jit-fuzzing \
    ./poc.js

```

This will result in the following crash:

```
#
# Fatal error in ../../src/objects/scope-info.cc, line 960
# Debug check failed: HasOuterScopeInfo().
#

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### cl...@appspot.gserviceaccount.com (2025-12-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5110523687272448.

### 24...@project.gserviceaccount.com (2025-12-23)

Detailed Report: https://clusterfuzz.com/testcase?key=5110523687272448

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  HasOuterScopeInfo() in scope-info.cc
  v8::internal::ScopeInfo::OuterScopeInfo
  v8::internal::compiler::ScopeInfoRef::OuterScopeInfo
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=104326:104327

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5110523687272448

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2025-12-23)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-12-23)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/39920667b30cf49eace308d56f8cae301fa9d0b9 ([maglev] Unwrap fast/slow closure in getcontext/feedbackcell

Change-Id: I5744eb9ff8afdc7d7905222cbbf7271014d771c5
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7261257
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#104327}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### aj...@google.com (2025-12-23)

tentatively setting labels pending v8 assessment

### ch...@google.com (2025-12-23)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-12-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-12-23)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-12-23)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-01-06)

verwaest: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-01-08)

Project: v8/v8  

Branch:  main  

Author:  Toon Verwaest [verwaest@chromium.org](mailto:verwaest@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7368073>

[maglev] Keep track of ScopeInfo across suspension points

---


Expand for full commit details
```
     
    Bug: 470831166 
    Change-Id: I79260909894936591c4872e08aa092cd59d75e4c 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7368073 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104554}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- M `src/maglev/maglev-graph.cc`

---

Hash: [d9c585339cd945ac9c288efe92fe4a61918236e5](https://chromiumdash.appspot.com/commit/d9c585339cd945ac9c288efe92fe4a61918236e5)  

Date: Thu Jan 8 10:35:32 2026


---

### 24...@project.gserviceaccount.com (2026-01-09)

ClusterFuzz testcase 5110523687272448 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=104553:104554

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-01-14)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
**Merge approved:** your change passed merge requirements and is auto-approved for M145. Please go ahead and merge the CL to branch 7632 (refs/branch-heads/7632) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [145].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-01-15)

verwaest@ - we plan to cut releases tomorrow afternoon (US Pacific time). Can you merge the fix to make sure its in the initial M145 releases?

### dr...@chromium.org (2026-01-15)

Ah, no, sorry. Something must have gone wrong with our automation. The fix CL is in M145.

### sp...@google.com (2026-01-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high quality memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/470831166)*
