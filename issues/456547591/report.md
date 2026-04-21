# Maglev - CallBuiltin (input @0 = LoadHoleyFixedDoubleArrayElement) type HoleyFloat64 is not Tagged 

| Field | Value |
|-------|-------|
| **Issue ID** | [456547591](https://issues.chromium.org/issues/456547591) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2025-10-31 |
| **Bounty** | $11,000.00 |

## Description

## VERSION

V8 Version: commit hash `a3d368877487647fbd9d6dca8de88c3762ab2793` (ToT)

Operating System: Linux

## REPRODUCTION CASE

Please run the following JS snippet using debug version of v8 with `--jit-fuzzing` and `--turbolev` flags. With these 2 flags, the crash appears sometimes. If we add the flag `--turboshaft-assert-types` the crash can be triggered reliably.

```
for (let i1 = 100; i1; --i1) {
}
function f5(a6) {
    for (let v7 = 0; v7 < 5; v7++) {
    }
    a6.slice(); 
    function f9(a10) {
        a10.forEach(f5);  
        return a10;
    }
    f9([,1.1]);
    return f5;
}
for (let v16 = 0; v16 < 25; v16++) {
    const v17 = [f5];
    try { f5(v17); } catch (e) {}
}

```

It will produce the following crash (in `debug` build) -

```
#
# Fatal error in ../../src/maglev/maglev-ir.cc, line 630
# Type representation error: node #95 : CallBuiltin (input @0 = LoadHoleyFixedDoubleArrayElement) type HoleyFloat64 is not Tagged
#
#
#
#FailureMessage Object: 0x7f8db1b655c8
==== C stack trace ===============================

    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f8dbf4e76ce]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8_libplatform.so(+0x4ffcd) [0x7f8dbf449fcd]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x205) [0x7f8dbf4bcb85]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::maglev::CheckValueInputIs(v8::internal::maglev::NodeBase const*, int, v8::internal::maglev::ValueRepresentation)+0x207) [0x7f8dc9ba59c7]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::maglev::CallBuiltin::VerifyInputs() const+0x1ee) [0x7f8dc9ba676e]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::maglev::ProcessResult v8::internal::maglev::MaglevGraphVerifier::Process<v8::internal::maglev::CallBuiltin>(v8::internal::maglev::CallBuiltin*, v8::internal::maglev::ProcessingState const&)+0x1b5) [0x7f8dc9620185]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::maglev::GraphProcessor<v8::internal::maglev::MaglevGraphVerifier>::ProcessNodeBase(v8::internal::maglev::NodeBase*, v8::internal::maglev::ProcessingState const&)+0x11b7) [0x7f8dc9612c67]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::maglev::GraphProcessor<v8::internal::maglev::MaglevGraphVerifier>::ProcessGraph(v8::internal::maglev::Graph*)+0x446) [0x7f8dc96108a6]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::RunMaglevOptimizations(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::maglev::MaglevCompilationInfo*, v8::internal::maglev::Graph*)+0x2f5) [0x7f8dcbae3895]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::TurbolevGraphBuildingPhase::Run(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::Zone*, v8::internal::compiler::Linkage*)+0x3de) [0x7f8dcbb4d27e]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(auto v8::internal::compiler::turboshaft::Pipeline::Run<v8::internal::compiler::turboshaft::TurbolevGraphBuildingPhase, v8::internal::compiler::Linkage*&>(v8::internal::compiler::Linkage*&)+0x1ce) [0x7f8dcaab767e]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::Pipeline::CreateGraphWithMaglev(v8::internal::compiler::Linkage*)+0xa4) [0x7f8dcaaabc54]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x1ab) [0x7f8dcaa97b0b]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x128) [0x7f8dc7e1b028]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::OptimizingCompileTaskExecutor::RunCompilationJob(v8::internal::OptimizingCompileTaskState&, v8::internal::Isolate*, v8::internal::LocalIsolate&, v8::internal::TurbofanCompilationJob*)+0x23c) [0x7f8dc7f8411c]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8.so(v8::internal::OptimizingCompileTaskExecutor::CompileTask::Run(v8::JobDelegate*)+0x35b) [0x7f8dc7f8c49b]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xbe) [0x7f8dbf44899e]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xac) [0x7f8dbf4500fc]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::Thread::NotifyStartedAndRun()+0x32) [0x7f8dbf4e6dd2]
    /home/br4v3h3r0/v8/v8/out/x64.debug/libv8_libbase.so(+0x7b41a) [0x7f8dbf4e541a]
    /lib/x86_64-linux-gnu/libpthread.so.0(+0x8609) [0x7f8dbeede609]
    /lib/x86_64-linux-gnu/libc.so.6(clone+0x43) [0x7f8dbecb4353]
Trace/breakpoint trap

```

It is important to note that this crash is only reproducible in the `debug` version of V8.

## Bisect

After bisect it seems that the bug was introduced in the following commit -

`[maglev, turbolev] Implement array.prototype.slice` -> [`ebcd571a1d1`] Revision: `101590`

<https://chromium.googlesource.com/v8/v8/+/ebcd571a1d1%5E%21/#F2>

## Analysis

The crash seems to occur due to a type representation mismatch in Maglev's intermediate representation. The error message indicates that a `CallBuiltin` node for `Builtin::kCloneFastJSArray` is receiving an input with `HoleyFloat64` representation when it expects `Tagged` representation.

During graph verification, `CallBuiltin::VerifyInputs()` validates that all inputs match the expected types specified by the builtin's call interface descriptor. The `CloneFastJSArray` builtin expects its source parameter to be `MachineType::AnyTagged()`, which corresponds to `ValueRepresentation::kTagged` in Maglev. However, the actual input is a `LoadHoleyFixedDoubleArrayElement` node, which produces `ValueRepresentation::kHoleyFloat64` - a special representation for loading double values from holey arrays that can contain holes.

The fundamental issue is that the optimization incorrectly passes a non-tagged value (an array element loaded from a double array) where a tagged object (the array itself) is expected. This happens because the receiver value somehow becomes confused with or replaced by an element loaded from an array during optimization passes.

## Bisect Analysis

The bug was introduced in commit `ebcd571a1d1c593ef03d18445a2573ec6c92c66d` which implemented the `TryReduceArrayPrototypeSlice` optimization for Maglev.

The implementation follows a similar pattern to other array builtin optimizations like `TryReduceArrayPrototypeAt`, but seems to contain a critical missing validation step. While it checks that the receiver has possible maps that support fast array iteration and validates the start/end parameters, it fails to verify that the receiver itself has the correct type representation before passing it to `BuildCallBuiltin`.

Other similar optimization functions in the same file, such as `TryReduceArrayPrototypeEntries`, include an explicit check to ensure the receiver is a `JSReceiver` before proceeding. This check is absent from `TryReduceArrayPrototypeSlice`, allowing the optimization to proceed even when the receiver has an incompatible representation.

## PoC Analysis

The PoC creates a scenario that triggers the bug through complex control flow involving inlining, nested function calls, and polymorphic receiver types:

1. The outer loop calls `f5([f5])` repeatedly, where the receiver is an array of functions with `PACKED_ELEMENTS` kind.
2. Inside `f5`, it calls `a6.slice()` and then defines and invokes `f9([,1.1])`, which creates a `HOLEY_DOUBLE_ELEMENTS` array.
3. The `forEach` call on this array invokes `f5` recursively with each element: first with undefined (converted from the hole), then with the double value 1.1.

During optimization, when Maglev tries to inline these calls, it encounters multiple call sites to f5 with different receiver types. The compiler must create phi nodes to merge control flow paths where the receiver could be:

- The original array [`f5`] (Tagged, `PACKED_ELEMENTS`)
- Elements from the double array (potentially `HoleyFloat64` for double elements)

The bug manifests when a phi node or value numbering incorrectly merges or aliases the receiver parameter with a `LoadHoleyFixedDoubleArrayElement` node from an inlined `forEach` iteration. When `TryReduceArrayPrototypeSlice` attempts to optimize the `a6.slice()` call, it receives this incorrectly-typed value node and passes it directly to `BuildCallBuiltin<Builtin::kCloneFastJSArray>({receiver})` without validating its representation. The verification phase then catches this type error when `CallBuiltin::VerifyInputs()` discovers that input @0 has `HoleyFloat64` representation instead of the required `Tagged` representation.

## Possible Fix

The fix could add an explicit type check for the receiver at the beginning of `TryReduceArrayPrototypeSlice`, following the established pattern used by other array prototype optimizations in the same file.

Specifically, after obtaining the receiver value, the function should call `CheckType(receiver, NodeType::kJSReceiver)` and return early if the check fails.

Reporter Credit: @streypaws

## Attachments

- poc.js (text/javascript, 312 B)

## Timeline

### ma...@chromium.org (2025-10-31)

Here's a minimal repro w/ just --allow-natives-syntax --turbolev

```
function doSlice(a) {
  a.slice();
}
%PrepareFunctionForOptimization(doSlice);

doSlice([0]);

function f5() {
  [,1.1].forEach(doSlice); // will throw
}
%PrepareFunctionForOptimization(f5);

try { f5(); } catch (e) {}

%OptimizeFunctionOnNextCall(f5);
try { f5(); } catch (e) {}

```

### ma...@chromium.org (2025-10-31)

Reporter: thanks for the bug report! This is a really solid one, and the bug is exactly where the report says it is. (Except it doesn't need complex control flow or nested function calls to trigger, as the minimal repro shows. But other parts are legit!)

### dx...@google.com (2025-10-31)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7106059>

[maglev] Fix a bug in reducing Array.p.slice

---


Expand for full commit details
```
     
    We might be in a polymorphic branch where the receiver is surely 
    not a JSReceiver (although we don't figure it out based on the 
    possible maps). 
     
    Fixed: 456547591 
    Change-Id: I2dc6b92ec9c537d72543b570c3e26bd1112c7f3f 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7106059 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#103441}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`

---

Hash: [00348ef5c3c11842465ca11e7e39706dbe91ed86](https://chromiumdash.appspot.com/commit/00348ef5c3c11842465ca11e7e39706dbe91ed86)  

Date: Fri Oct 31 11:34:52 2025


---

### ch...@google.com (2025-10-31)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-10-31)

The Found In field may only contain numeric values.
Some values were corrected.
You can see the changes by toggling full history on the issue.

### ch...@google.com (2025-10-31)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-10-31)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-10-31)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2025-10-31)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M143. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2025-11-01)

**Merge approved:** your change passed merge requirements and is auto-approved for M143. Please go ahead and merge the CL to branch 7499 (refs/branch-heads/7499) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-11-01)

Merge review required: M142 is already shipping to stable.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-11-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ma...@chromium.org (2025-11-05)

1. Why does your merge fit within the merge criteria for these milestones?

Security fix

2. What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/c/v8/v8/+/7106059>

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.

I rarely say this, but this is an exceptionally safe fix, since it only adds one additional bail out, so, the only functional change is that we'll skip optimizing compilation in one more case than before.

### dx...@google.com (2025-11-05)

Project: v8/v8  

Branch:  refs/branch-heads/14.3  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7124104>

Merged (14.3): [maglev] Fix a bug in reducing Array.p.slice

---


Expand for full commit details
```
     
    We might be in a polymorphic branch where the receiver is surely 
    not a JSReceiver (although we don't figure it out based on the 
    possible maps). 
     
    Fixed: 456547591 
    (cherry picked from commit 00348ef5c3c11842465ca11e7e39706dbe91ed86) 
     
    Change-Id: Ib3c06becb8d002b329dffeefabf54862988def0a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7124104 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.3@{#10} 
    Cr-Branched-From: 13c7e3135187c1b0c7344e42529fbc27ba0e47f1-refs/heads/14.3.127@{#1} 
    Cr-Branched-From: 01af089bd89645143fc60f0da72267f95645afb3-refs/heads/main@{#103352}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`

---

Hash: [def33794ec321439d04a953e572a1ad5530baed4](https://chromiumdash.appspot.com/commit/def33794ec321439d04a953e572a1ad5530baed4)  

Date: Fri Oct 31 11:34:52 2025


---

### pe...@google.com (2025-11-05)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ma...@chromium.org (2025-11-06)

1. Yes
2. According to the bug, it bisects to <https://chromiumdash.appspot.com/commit/ebcd571a1d1c593ef03d18445a2573ec6c92c66d> which landed in 140.0.7339.41.

### qk...@google.com (2025-11-06)

Labeled as not applicable for 138-LTS because the branches don't contain the suspected CL[1]

[1] https://chromium-review.googlesource.com/c/v8/v8/+/6772546

### ch...@google.com (2025-11-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2025-11-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High-quality report of demonstrated memory corruption in a sandboxed renderer process with a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sh...@gmail.com (2025-11-12)

Thanks for the reward! I have an additional request, if this bug is showcased in Chrome Advisory/ gets a CVE, please set my Reporter Credit to "**Shreyas Penkar (@streypaws)**". I'll use the same when reporting next time. Thanks to Chrome Team for rapidly addressing and patching this vulnerability.

### ch...@google.com (2026-02-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High-quality report of demonstrated memory corruption in a sandboxed renderer process with a bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/456547591)*
