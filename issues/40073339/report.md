# Security: Debug check failed: output_instr_index_ == definition_block->last_instruction_index() in v8/src/compiler/backend/mid-tier-register-allocator.cc:583

| Field | Value |
|-------|-------|
| **Issue ID** | [40073339](https://issues.chromium.org/issues/40073339) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@goodmanemail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2023-09-25 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: f2fe88605a0bcb2a31c69a8f6cf9d84c6e0383fd  

Operating System: Ubuntu 23.04

gn gen out/libfuzzernosan '--args=use\_libfuzzer=true is\_ubsan=false is\_msan=false is\_asan=false is\_tsan=false is\_debug=false enable\_nacl=false'

ninja -C out/libfuzzernosan/v8\_wasm\_compile\_fuzzer

$ /home/alan/chromium/src/out/libfuzzernosan/v8\_wasm\_compile\_fuzzer min  

INFO: Running with entropic power schedule (0xFF, 100).  

INFO: Seed: 1788738389  

INFO: Loaded 1 modules (1238938 inline 8-bit counters): 1238938 [0x55d664ef2d60, 0x55d6650214fa),  

INFO: Loaded 1 PC tables (1238938 PCs): 1238938 [0x55d665021500,0x55d666308ea0),  

/home/alan/chromium/src/out/libfuzzernosan/v8\_wasm\_compile\_fuzzer: Running 1 inputs 1 time(s) each.  

Running: min

# 

# Fatal error in ../../v8/src/compiler/backend/mid-tier-register-allocator.cc, line 583

# Debug check failed: output\_instr\_index\_ == definition\_block->last\_instruction\_index() - 1 (19540 vs. 19551).

# 

# 

# 

#FailureMessage Object: 0x7ffeb8b5cd30  

==== C stack trace ===============================

```
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x536de2d) [0x55d664b36e2d]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x536c302) [0x55d664b35302]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x5344536) [0x55d664b0d536]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x5343ec5) [0x55d664b0cec5]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x43cb5b9) [0x55d663b945b9]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x43cb7d7) [0x55d663b947d7]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x43cd124) [0x55d663b96124]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x43cceab) [0x55d663b95eab]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x43d20b3) [0x55d663b9b0b3]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x43d4f65) [0x55d663b9df65]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x43d9cad) [0x55d663ba2cad]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x43d7ac1) [0x55d663ba0ac1]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x43daa4a) [0x55d663ba3a4a]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x47cb198) [0x55d663f94198]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x47c74da) [0x55d663f904da]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x47be599) [0x55d663f87599]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x47bfc91) [0x55d663f88c91]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x47c5d6a) [0x55d663f8ed6a]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x4a7b867) [0x55d664244867]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x3f86f5b) [0x55d66374ff5b]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x3f861b1) [0x55d66374f1b1]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x3feaafd) [0x55d6637b3afd]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x3dad796) [0x55d663576796]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x3dacfff) [0x55d663575fff]  
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x511c9a0) [0x55d6648e59a0]  

```

==28422== ERROR: libFuzzer: deadly signal  

#0 0x55d661b32e84 in \_\_sanitizer\_print\_stack\_trace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/ubsan/ubsan\_diag\_standalone.cpp:31:3  

#1 0x55d661ba6a88 in fuzzer::PrintStackTrace() ../../third\_party/libFuzzer/src/FuzzerUtil.cpp:210:5  

#2 0x55d661b8d693 in fuzzer::Fuzzer::CrashCallback() ../../third\_party/libFuzzer/src/FuzzerLoop.cpp:231:3  

#3 0x7ff9e543c4af (/lib/x86\_64-linux-gnu/libc.so.6+0x3c4af) (BuildId: bdb8aa3b1b60f9d43e1c70ba98158e05f765efdc)  

#4 0x7ff9e5490ffa in \_\_pthread\_kill\_implementation nptl/pthread\_kill.c:43:17  

#5 0x7ff9e5490ffa in \_\_pthread\_kill\_internal nptl/pthread\_kill.c:78:10  

#6 0x7ff9e5490ffa in pthread\_kill nptl/pthread\_kill.c:89:10  

#7 0x7ff9e543c405 in raise signal/../sysdeps/posix/raise.c:26:13  

#8 0x7ff9e542287b in abort stdlib/abort.c:79:7  

#9 0x55d664b303ab in v8::base::OS::Abort() ../../v8/src/base/platform/platform-posix.cc:701:3  

#10 0x55d664b0d543 in V8\_Fatal(char const\*, int, char const\*, ...) ../../v8/src/base/logging.cc:167:3  

#11 0x55d664b0cec4 in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const\*, int, char const\*) ../../v8/src/base/logging.cc:57:3  

#12 0x55d663b945b8 in v8::internal::compiler::VirtualRegisterData::EnsureSpillRange(v8::internal::compiler::MidTierRegisterAllocationData\*) ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:582:7  

#13 0x55d663b947d6 in v8::internal::compiler::VirtualRegisterData::AddSpillUse(int, v8::internal::compiler::MidTierRegisterAllocationData\*) ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:599:3  

#14 0x55d663b96123 in SpillOperand ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:644:3  

#15 0x55d663b96123 in v8::internal::compiler::RegisterState::Register::SpillPendingUses(v8::internal::compiler::MidTierRegisterAllocationData\*) ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:1104:15  

#16 0x55d663b95eaa in v8::internal::compiler::RegisterState::Register::Spill(v8::internal::compiler::AllocatedOperand, v8::internal::compiler::InstructionBlock const\*, v8::internal::compiler::MidTierRegisterAllocationData\*) ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:1055:3  

#17 0x55d663b9b0b2 in Spill ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:1172:17  

#18 0x55d663b9b0b2 in v8::internal::compiler::SinglePassRegisterAllocator::SpillRegister(v8::internal::compiler::RegisterIndex) ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:2251:20  

#19 0x55d663b9df64 in v8::internal::compiler::SinglePassRegisterAllocator::ReserveFixedRegister(v8::internal::compiler::UnallocatedOperand const\*, int, v8::internal::MachineRepresentation, int, v8::internal::compiler::SinglePassRegisterAllocator::UsePosition) ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:2647:5  

#20 0x55d663ba2cac in ReserveFixedInputRegister ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:2617:3  

#21 0x55d663ba2cac in v8::internal::compiler::MidTierRegisterAllocator::ReserveFixedRegisters(int) ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:3202:12  

#22 0x55d663ba0ac0 in v8::internal::compiler::MidTierRegisterAllocator::AllocateRegisters(v8::internal::compiler::InstructionBlock const\*) ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:3024:5  

#23 0x55d663ba3a49 in v8::internal::compiler::AllocateRegisters(v8::internal::compiler::MidTierRegisterAllocationData\*) ../../v8/src/compiler/backend/mid-tier-register-allocator.cc:3273:15  

#24 0x55d663f94197 in Run ../../v8/src/compiler/pipeline.cc:2588:5  

#25 0x55d663f94197 in auto v8::internal::compiler::PipelineImpl::Run[v8::internal::compiler::MidTierRegisterAllocatorPhase](javascript:void(0);)() ../../v8/src/compiler/pipeline.cc:1355:18  

#26 0x55d663f904d9 in v8::internal::compiler::PipelineImpl::AllocateRegistersForMidTier(v8::internal::RegisterConfiguration const\*, v8::internal::compiler::CallDescriptor\*, bool) ../../v8/src/compiler/pipeline.cc:4550:3  

#27 0x55d663f87598 in v8::internal::compiler::PipelineImpl::AllocateRegisters(v8::internal::compiler::CallDescriptor\*, bool) ../../v8/src/compiler/pipeline.cc:4196:5  

#28 0x55d663f88c90 in v8::internal::compiler::PipelineImpl::SelectInstructions(v8::internal::compiler::Linkage\*) ../../v8/src/compiler/pipeline.cc:4106:10  

#29 0x55d663f8ed69 in v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo\*, v8::internal::wasm::CompilationEnv\*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph\*, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WasmFeatures\*, v8::internal::compiler::CallDescriptor\*) ../../v8/src/compiler/pipeline.cc:3807:7  

#30 0x55d664244866 in v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv\*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures\*) ../../v8/src/compiler/turboshaft/wasm-turboshaft-compiler.cc:51:8  

#31 0x55d66374ff5a in v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv\*, v8::internal::wasm::WireBytesStorage const\*, v8::internal::Counters\*, v8::internal::wasm::WasmFeatures\*) ../../v8/src/wasm/function-compiler.cc:158:18  

#32 0x55d66374f1b0 in v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv\*, v8::internal::wasm::WireBytesStorage const\*, v8::internal::Counters\*, v8::internal::wasm::WasmFeatures\*) ../../v8/src/wasm/function-compiler.cc:30:9  

#33 0x55d6637b3afc in v8::internal::wasm::CompileLazy(v8::internal::Isolate\*, v8::internal::Tagged[v8::internal::WasmInstanceObject](javascript:void(0);), int) ../../v8/src/wasm/module-compiler.cc:1211:48  

#34 0x55d663576795 in v8::internal::\_\_RT\_impl\_Runtime\_WasmCompileLazy(v8::internal::RuntimeArgumentsWithoutHandles, v8::internal::Isolate\*) ../../v8/src/runtime/runtime-wasm.cc:314:18  

#35 0x55d663575ffe in v8::internal::Runtime\_WasmCompileLazy(int, unsigned long\*, v8::internal::Isolate\*) ../../v8/src/runtime/runtime-wasm.cc:302:1  

#36 0x55d6648e599f in Builtins\_WasmCEntry setup-isolate-deserialize.cc

NOTE: libFuzzer has rudimentary signal handlers.  

Combine libFuzzer with AddressSanitizer or similar for better crash reports.  

SUMMARY: libFuzzer: deadly signal

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Alan Goodman

Since my previous debug check report appeared to be well received, even if probably a duplicate here is another one. Looks like it might be turboshaft related again.

## Attachments

- [min](attachments/min) (text/plain, 162 B)
- [wasmt.js](attachments/wasmt.js) (text/plain, 1004 B)

## Timeline

### [Deleted User] (2023-09-25)

[Empty comment from Monorail migration]

### ad...@google.com (2023-09-26)

Sending to V8 sheriff for further triage, setting provisional FoundIn and severity - please adjust!

NB I have not reproduced this since the binary format is opaque to me, and so I'd need to send this file over to an untrusted execution environment, which probably doesn't seem worthwhile before you've done further triage.

[Monorail components: Blink>JavaScript>WebAssembly]

### [Deleted User] (2023-09-26)

[Empty comment from Monorail migration]

### is...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### is...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### is...@chromium.org (2023-09-26)

Bisects to 638c14b02ec9a6869e1bae51992e933e289b5578, reproduces on ToT.

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### [Deleted User] (2023-09-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2023-09-27)

I don't think this is Turboshaft related (despite the bisect to my Turboshaft CL).

Run the attached file with a debug build and `--no-liftoff --turbo_force_mid_tier_regalloc` and it will produce the same error. 
In particular, I think that to reproduce, it requires a Call that returns multiple values, can throw, and with a caller that has a catch handler. The TF graph will be something like:

6: Call
11: IfException(#6)
10: IfSuccess(#6)
7: Projection(#6, 0)
8: Projection(#6, 1)

I think that the combination of throwing + multi-return  + called in a catch block is somewhat rare, which is why we haven't noticed this before.

Clemens, you could have a look please? (and maybe run a new Clusterfuzz with the attached repro)

### cl...@chromium.org (2023-09-27)

Thanks for the reproducer, Darius! I can reproduce locally, uploading to CF for another bisection now.

### cl...@chromium.org (2023-09-27)

Note that we are just disabling the mid-tier register allocator fallback, which will also "fix" this issue: https://crrev.com/c/4891836

### cl...@chromium.org (2023-09-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6174172010708992.

### cl...@chromium.org (2023-09-27)

Argh, I forgot to include the `wasm-module-builder.js` file in the reproducer. Next try...

### cl...@chromium.org (2023-09-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5610893475512320.

### cl...@chromium.org (2023-09-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-09-27)

Detailed Report: https://clusterfuzz.com/testcase?key=5610893475512320

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  output_instr_index_ == definition_block->last_instruction_index() - 1 in mid-tie
  v8::internal::compiler::VirtualRegisterData::EnsureSpillRange
  v8::internal::compiler::VirtualRegisterData::AddSpillUse
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=77494:77495

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5610893475512320

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-09-27)

Bisects to a mid-tier register allocator CL now:
d757cd5 [compiler] Fix mid-tier register allocator issue by Clemens Backes · 2 years ago

So looks like this is broken in the mid-tier register allocator since forever. On M-117+ we could this fix by disabling the mid-tier register allocator (happening in https://crbug.com/1469533). M-116 (current extended release) does not have the feature flag yet. It's not clear if it's worth fixing this for M-116. I'll try to debug this a bit tomorrow.

### al...@goodmanemail.com (2023-10-02)

How did you get on?

### dl...@chromium.org (2023-10-04)

The mid-tier register allocator is now disabled on Chromium and v8 tip-of-tree. For M-117, we will launch/bump the already ongoing Finch trial (which disables the mid-tier regalloc) to 100% Stable in the coming days. Not sure what to do about older milestones.

### cl...@chromium.org (2023-10-04)

Marking this fixed (via https://crrev.com/c/4894121 on ToT, and Finch on M-117+).

### [Deleted User] (2023-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-04)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M117. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M118. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117, 118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-10-05)

re: https://crbug.com/chromium/1486550#c19, if this is already handled in 117, then 118 and newer channels should be covered and I presume merging this CL to disable is not needed? 
(leaving this approved for 118 now just in case that assertion is incorrect)

M118 will be promoted to Stable next Tuesday (Early Stable 118 had already been released), 118 will also serve as the new/next Extended Stable. 
There are no further planned releases of 116/Extended or 117/Stable, so that should alleviate the concern about older milestones. 

### [Deleted User] (2023-10-05)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1486550&entry.364066060=External&entry.958145677=Linux&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Compiler>Turbofan,Blink>JavaScript>WebAssembly&entry.975983575=clemensb@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-10-05)

Thanks, Amy, this should be fixed on all channels then, no merge needed.

### cl...@chromium.org (2023-10-05)

I filled the light-weight postmortem.

### cl...@chromium.org (2023-10-11)

ClusterFuzz testcase 5610893475512320 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### cl...@chromium.org (2023-10-11)

Re #27: The test case uses the `--turbo-force-mid-tier-regalloc` flag, which forces a configuration we do not ship any more. We could also set it to impact none now, and to WontFix, but I think the current state reflects things better, so keeping labels as they are and silencing ClusterFuzz instead.

Clusterfuzz will finally be unable to reproduce once we remove that flag and rip out the whole mid-tier register allocator (in a few weeks).

### am...@google.com (2023-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-11)

Congratulations, Alan! The Chrome VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-10)

This issue was migrated from crbug.com/chromium/1486550?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>WebAssembly]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### cl...@chromium.org (2026-01-08)

Removing `Clusterfuzz-ignore` hotlist from some old bugs as it's preventing Clusterfuzz from filing similar bugs.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073339)*
