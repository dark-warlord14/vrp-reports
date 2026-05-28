# Security: Debug check failed: inlinee.sig->return_count() == sig->return_count() . in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41484431](https://issues.chromium.org/issues/41484431) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-12-15 |
| **Bounty** | $11,000.00 |

## Description

## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91376
    - link: https://crrev.com/def7931b83728d229e94be9445529fb9db660654 
- Commit Message

```
commit def7931b83728d229e94be9445529fb9db660654
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Wed Dec 6 13:51:24 2023 +0100

    [turboshaft][wasm] Fix reachability handling for catch blocks
    
    Due to the reachability in the decoder influencing the  assignment of
    feedback slots, it is required to handle reachability consistently
    between liftoff and the optimizing compiler.
    
    This wasn't the case for CatchException, CatchCase and CatchAll.
    
    Bug: chromium:1508213
    Change-Id: I9feede4b9397f51d3290edccef1768f500178f1f
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5088809
    Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91376}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91536/d8 --turboshaft-wasm --allow-natives-syntax --wasm-tiering-budget=1000 poc.js
# OUTPUT ==============================================================
wasm-function[0]:0x248: RuntimeError: memory access out of bounds
RuntimeError: memory access out of bounds
    at wasm://wasm/7ac25526:wasm-function[0]:0x248
    at ######_main (poc.js:6:3)
    at poc.js:8:1



#
# Fatal error in ../../src/wasm/turboshaft-graph-interface.cc, line 6534
# Debug check failed: inlinee.sig->return_count() == sig->return_count() (0 vs. 15).
#
#
#
#FailureMessage Object: 0x7f11377fb760
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91536/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f117665edd3]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libplatform.so(+0x19add) [0x7f1176605add]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f117663ee74]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libbase.so(+0x2b935) [0x7f117663e935]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x68b) [0x7f1175568f8b]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x796) [0x7f1175583f16]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7f1175583483]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7f117553be8b]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7f1175522723]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7f117551d49f]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x259) [0x7f117551cd99]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x786) [0x7f1175c74716]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7f1175ec8f31]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7f1175472c6b]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f11754720b2]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(+0x3ad18ba) [0x7f11754d18ba]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(+0x3ad10f5) [0x7f11754d10f5]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f1176604823]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f1176607213]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libbase.so(+0x4a789) [0x7f117665d789]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f1171094ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f1171126a40]

```

## Other
Please note to include the flags `--turboshaft-wasm --allow-natives-syntax --wasm-tiering-budget=1000` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91536.zip
2. Run: `d8 --turboshaft-wasm --allow-natives-syntax --wasm-tiering-budget=1000 poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 4.0 KB)
- [poc_code.js](attachments/poc_code.js) (text/plain, 19.8 KB)
- [poc_asan_oob.js](attachments/poc_asan_oob.js) (text/plain, 3.4 KB)
- [poc_asan_oob_code.js](attachments/poc_asan_oob_code.js) (text/plain, 13.8 KB)
- [asan.log](attachments/asan.log) (text/plain, 13.0 KB)
- [poc_code.js](attachments/poc_code.js) (text/javascript, 0 B)
- [poc.js](attachments/poc.js) (text/javascript, 3.3 KB)

## Timeline

### [Deleted User] (2023-12-15)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-15)

[Comment Deleted]

### je...@gmail.com (2023-12-15)

The issue mentioned in this issue is probably the same issue as the other issue I reported-1511120, but it shows a more explicit function obfuscation due to an inline error, so I'm reporting it to you separately to better determine the impact of the vulnerability.

### cl...@chromium.org (2023-12-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler>Turbofan Blink>JavaScript>WebAssembly]

### ch...@chromium.org (2023-12-15)

Setting foundin based on commit def7931b83728d229e94be9445529fb9db660654

### [Deleted User] (2023-12-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2023-12-18)

Unmarking this as a release blocker since it only triggers behind --turboshaft-wasm.

### be...@google.com (2023-12-18)

Adding Hotlist-RBS-Removed for tracking purposes.

### ma...@chromium.org (2023-12-18)

At Clemens's suggestion, I am reinstating the ReleaseBlock-Stable label, as we want to finch Turboshaft in 122.

### cl...@chromium.org (2023-12-18)

[Empty comment from Monorail migration]

### be...@google.com (2023-12-18)

Adding Hotlist-RBS-Removed for tracking purposes.

### am...@chromium.org (2023-12-18)

[Description Changed]

### je...@gmail.com (2023-12-19)

Hi, Is anyone working on fixing this issue?

### ma...@chromium.org (2023-12-19)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-12-19)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-21)

[Comment Deleted]

### je...@gmail.com (2023-12-22)

Friendly ping :)

### je...@gmail.com (2024-01-02)

## Exploit Detail

The inconsistency in the behavior between turboshaft and liftoff caused the vulnerability. This resulted in an error in the generation of the feedback_slot_ subscript when inlining CallDirect and CallRef in the program. The misalignment during function inlining would lead to the program being inlined into the wrong function, causing function confusion, parameter confusion, return value confusion, and so on.

In the file src/wasm/turboshaft-graph-interface.cc, there is code like this:
```
DCHECK_EQ(inlinee.sig->return_count(), sig->return_count());
DCHECK_EQ(inlinee.sig->parameter_count(), sig->parameter_count());
#ifdef DEBUG
    for (size_t i = 0; i < sig->return_count(); ++i) {
      DCHECK(IsSubtypeOf(inlinee.sig->GetReturn(i), sig->GetReturn(i),
                         decoder->module_));
    }
    for (size_t i = 0; i < sig->parameter_count(); ++i) {
      DCHECK(IsSubtypeOf(sig->GetParam(i), inlinee.sig->GetParam(i),
                         decoder->module_));
    }
#endif
```
Due to the occurrence of the vulnerability causing function confusion, where inlinee.sig and sig represent the signatures of two different functions, the poc may lead to inconsistencies such as mismatched parameter counts, mismatched return counts, and inconsistent types for Returns and Parameters between the two functions.

[0] When there is an inconsistency in parameter_count, it will result in an out-of-bounds read, allowing attackers to read arbitrary lengths of data backward as Parameters.
```
SmallZoneVector<OpIndex, 16> inlinee_args(
    inlinee.sig->parameter_count() + 1, decoder->zone_);
inlinee_args[0] = instance_node();
for (size_t i = 0; i < inlinee.sig->parameter_count(); i++) {
  inlinee_args[i + 1] = args[i].op; // ===> [0]
}
```

[1] When there is an inconsistency in return_count, it will lead to an out-of-bounds write, allowing attackers to write arbitrary lengths beyond the stack boundaries:
```
size_t return_count = inlinee.sig->return_count();
for (size_t i = 0; i < return_count; i++) {
  returns[i].op =
      MaybePhi(return_phis.phi_inputs(i), return_phis.phi_type(i)); // ===> [1]
}
```

[2] When there is inconsistency in the types of Returns or Parameters, it leads to type confusion.

The following is a POC that can trigger an out-of-bounds issue. When using asan-v8, you will obtain a complete asan log.

args.gn:
```
dcheck_always_on = false
is_debug = false
target_cpu = "x64"
symbol_level = 2
is_asan = true
```

reproduce:

`./out.gn/x64.asan/d8 —turboshaft-wasm poc_asan_oob.js`






### gi...@appspot.gserviceaccount.com (2024-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/acbfa775ae2a3a0e7e6b7528f33d545940f28ea4

commit acbfa775ae2a3a0e7e6b7528f33d545940f28ea4
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Tue Dec 19 14:44:47 2023

[wasm] Move exception reachability analysis to the decoder

We currently have an reachability analysis which determines if a given block can throw, and if not, no code is generated for the respective
catch. However, this analysis is done in the separate decoder
interfaces. This resulted in the analyses sometimes not being
consistent. Specifically for Turboshaft, this analysis cannot be made
to be consistent with Turbofan and Liftoff. This is because Turboshaft
inlines during graph generation; a call is always considered
potentially throwing, but the inlined body might be not throwing.
We cannot afford this inconsistency because Turboshaft relies on
having the same feedback slots for function calls as Liftoff.
To solve this, we move the analysis from the individual interfaces to
the decoder.

Bug: chromium:1511849
Change-Id: If71e682edd6bb91d8c6efd31503715facb6fdc4b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5134849
Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91672}

[modify] https://crrev.com/acbfa775ae2a3a0e7e6b7528f33d545940f28ea4/src/wasm/graph-builder-interface.cc
[add] https://crrev.com/acbfa775ae2a3a0e7e6b7528f33d545940f28ea4/test/mjsunit/regress/wasm/regress-1511849.js
[modify] https://crrev.com/acbfa775ae2a3a0e7e6b7528f33d545940f28ea4/src/wasm/turboshaft-graph-interface.cc
[modify] https://crrev.com/acbfa775ae2a3a0e7e6b7528f33d545940f28ea4/src/wasm/function-body-decoder.cc
[modify] https://crrev.com/acbfa775ae2a3a0e7e6b7528f33d545940f28ea4/src/wasm/baseline/liftoff-compiler.cc
[modify] https://crrev.com/acbfa775ae2a3a0e7e6b7528f33d545940f28ea4/src/wasm/function-body-decoder-impl.h


### ma...@chromium.org (2024-01-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-04)

ClusterFuzz testcase 6060178070241280 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91671:91672

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2024-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-11)

Congratulations on another one! The Chrome VRP Panel has decided to award you $10,000 for this high quality report of renderer process memory corruption + $1,000 bisect bonus. The information that you added in https://crbug.com/chromium/1511849#c19 really boosted this issue to a high quality report. Thank you for your efforts and reporting this issue to us, and for following up with such great details to explain the exploitability potential of this issue -- excellent work! 

### am...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-12)

This issue was migrated from crbug.com/chromium/1511849?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>WebAssembly]
[Monorail mergedwith: crbug.com/chromium/1511120]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M122. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge approved: your change passed merge requirements and is auto-approved for M122. Please go ahead and merge the CL to branch 6261 (refs/branch-heads/6261) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [122].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-02-04)

this fix landed on 122, removing merge approval
blintz auto-approval rules are firing a little aggressively -- an internal issue has been opened to investigate and tweak the behavior of our automation to prevent this in the future b/323744575

### pe...@google.com (2024-04-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2024-05-13)

The original report was deleted, so it has been restored.
Updating POC files as well to ensure they remain part of this report.

### am...@chromium.org (2024-05-13)

*below is information provided in the original report for this issue on 14 December 2023*

## INTRODUCE

After bisect, it was determined that following commit caused this problem.

- Commit Info
  - Version: 91376
  - link: <https://crrev.com/def7931b83728d229e94be9445529fb9db660654>
- Commit Message

```
commit def7931b83728d229e94be9445529fb9db660654
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Wed Dec 6 13:51:24 2023 +0100

    [turboshaft][wasm] Fix reachability handling for catch blocks
   
    Due to the reachability in the decoder influencing the  assignment of
    feedback slots, it is required to handle reachability consistently
    between liftoff and the optimizing compiler.
   
    This wasn't the case for CatchException, CatchCase and CatchAll.
   
    Bug: chromium:1508213
    Change-Id: I9feede4b9397f51d3290edccef1768f500178f1f
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5088809
    Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91376}


```
## CRASH LOG

- Debug output

```
# CMD: /tmp/d8-linux-debug-v8-component-91536/d8 --turboshaft-wasm --allow-natives-syntax --wasm-tiering-budget=1000 poc.js
# OUTPUT ==============================================================
wasm-function[0]:0x248: RuntimeError: memory access out of bounds
RuntimeError: memory access out of bounds
    at wasm://wasm/7ac25526:wasm-function[0]:0x248
    at #######_main (poc.js:6:3)
    at poc.js:8:1



#
# Fatal error in ../../src/wasm/turboshaft-graph-interface.cc, line 6534
# Debug check failed: inlinee.sig->return_count() == sig->return_count() (0 vs. 15).
#
#
#
#FailureMessage Object: 0x7f11377fb760
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91536/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f117665edd3]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libplatform.so(+0x19add) [0x7f1176605add]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f117663ee74]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libbase.so(+0x2b935) [0x7f117663e935]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x68b) [0x7f1175568f8b]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x796) [0x7f1175583f16]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7f1175583483]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7f117553be8b]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7f1175522723]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7f117551d49f]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x259) [0x7f117551cd99]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x786) [0x7f1175c74716]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7f1175ec8f31]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7f1175472c6b]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f11754720b2]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(+0x3ad18ba) [0x7f11754d18ba]
    /tmp/d8-linux-debug-v8-component-91536/libv8.so(+0x3ad10f5) [0x7f11754d10f5]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f1176604823]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f1176607213]
    /tmp/d8-linux-debug-v8-component-91536/libv8_libbase.so(+0x4a789) [0x7f117665d789]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f1171094ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f1171126a40]


```
## Other

Please note to include the flags `--turboshaft-wasm --allow-natives-syntax --wasm-tiering-budget=1000` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.2.0

REPRODUCTION CASE

1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91536.zip
2. Run: `d8 --turboshaft-wasm --allow-natives-syntax --wasm-tiering-budget=1000 poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41484431)*
