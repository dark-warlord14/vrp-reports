# GPU process crash via WebGPU shader - UAF in ProcessValue at DxilValueCache.cpp:555

| Field | Value |
|-------|-------|
| **Issue ID** | [371247955](https://issues.chromium.org/issues/371247955) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU, Dawn>Tint, Internals>GPU>Dawn, Internals>GPU>Tint |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-10-04 |
| **Bounty** | $10,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

I tested dxopt according to the ll file of this patch <https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570270>. Then I found the crash. This path seems to be enabled in Chrome. I don't know how to provide the wgsl file to trigger the asan of this chromium, but I will provide the ll file.

reproduce step

1.build DirectXShaderCompiler

2.dxopt %s -hlsl-passes-resume -dxil-remove-dead-blocks -S

poc file

I just use <https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570270/2/tools/clang/test/DXC/Passes/DxilRemoveDeadBlocks/switch-with-multiple-same-successor.ll>
and change some code.

ASAN

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==4033744==ERROR: AddressSanitizer: SEGV on unknown address (pc 0x7f510b4bc039 bp 0x7ffc15aa8ac0 sp 0x7ffc15aa8910 T0)
==4033744==The signal is caused by a READ memory access.
==4033744==Hint: this fault was caused by a dereference of a high value address (see register values below).  Dissassemble the provided pc to learn which register was used.
    #0 0x7f510b4bc039 in llvm::Value::getValueID() const /data/DirectXShaderCompiler/include/llvm/IR/Value.h:374
    #1 0x7f510b4bc039 in llvm::ConstantInt::classof(llvm::Value const*) /data/DirectXShaderCompiler/include/llvm/IR/Constants.h:225
    #2 0x7f510b4bc039 in llvm::isa_impl<llvm::ConstantInt, llvm::Value, void>::doit(llvm::Value const&) /data/DirectXShaderCompiler/include/llvm/Support/Casting.h:57
    #3 0x7f510b4bc039 in llvm::isa_impl_cl<llvm::ConstantInt, llvm::Value const*>::doit(llvm::Value const*) /data/DirectXShaderCompiler/include/llvm/Support/Casting.h:97
    #4 0x7f510b4bc039 in llvm::isa_impl_wrap<llvm::ConstantInt, llvm::Value const*, llvm::Value const*>::doit(llvm::Value const* const&) /data/DirectXShaderCompiler/include/llvm/Support/Casting.h:123
    #5 0x7f510b4bc039 in llvm::isa_impl_wrap<llvm::ConstantInt, llvm::Value* const, llvm::Value const*>::doit(llvm::Value* const&) /data/DirectXShaderCompiler/include/llvm/Support/Casting.h:114
    #6 0x7f510b4bc039 in bool llvm::isa<llvm::ConstantInt, llvm::Value*>(llvm::Value* const&) /data/DirectXShaderCompiler/include/llvm/Support/Casting.h:135
    #7 0x7f510b4bc039 in llvm::cast_retty<llvm::ConstantInt, llvm::Value*>::ret_type llvm::dyn_cast<llvm::ConstantInt, llvm::Value>(llvm::Value*) /data/DirectXShaderCompiler/include/llvm/Support/Casting.h:300
    #8 0x7f510b4bc039 in llvm::DxilValueCache::MayBranchTo(llvm::BasicBlock*, llvm::BasicBlock*) /data/DirectXShaderCompiler/lib/Analysis/DxilValueCache.cpp:66
    #9 0x7f510b4be7fb in llvm::DxilValueCache::ProcessAndSimplify_PHI(llvm::Instruction*, llvm::DominatorTree*) /data/DirectXShaderCompiler/lib/Analysis/DxilValueCache.cpp:115
    #10 0x7f510b4cc35e in llvm::DxilValueCache::SimplifyAndCacheResult(llvm::Instruction*, llvm::DominatorTree*) /data/DirectXShaderCompiler/lib/Analysis/DxilValueCache.cpp:271
    #11 0x7f510b4d1a09 in llvm::DxilValueCache::ProcessValue(llvm::Value*, llvm::DominatorTree*) /data/DirectXShaderCompiler/lib/Analysis/DxilValueCache.cpp:579
    #12 0x7f510b4d64d4 in llvm::DxilValueCache::GetConstInt(llvm::Value*, llvm::DominatorTree*) /data/DirectXShaderCompiler/lib/Analysis/DxilValueCache.cpp:494
    #13 0x7f5102c36d1e in DeadBlockDeleter::Run(llvm::Function&, llvm::DxilValueCache*) /data/DirectXShaderCompiler/lib/Transforms/Scalar/DxilRemoveDeadBlocks.cpp:82
    #14 0x7f5102c3f57b in DeleteDeadBlocks /data/DirectXShaderCompiler/lib/Transforms/Scalar/DxilRemoveDeadBlocks.cpp:220
    #15 0x7f5102c3f57b in runOnFunction /data/DirectXShaderCompiler/lib/Transforms/Scalar/DxilRemoveDeadBlocks.cpp:389
    #16 0x7f510bd9fde4 in llvm::FPPassManager::runOnFunction(llvm::Function&) /data/DirectXShaderCompiler/lib/IR/LegacyPassManager.cpp:1587
    #17 0x7f510bda089a in llvm::FPPassManager::runOnModule(llvm::Module&) /data/DirectXShaderCompiler/lib/IR/LegacyPassManager.cpp:1609
    #18 0x7f510bd9a02a in runOnModule /data/DirectXShaderCompiler/lib/IR/LegacyPassManager.cpp:1669
    #19 0x7f510bd9bf4b in llvm::legacy::PassManagerImpl::run(llvm::Module&) /data/DirectXShaderCompiler/lib/IR/LegacyPassManager.cpp:1771
    #20 0x7f5101534fc2 in DxcOptimizer::RunOptimizer(IDxcBlob*, wchar_t const**, unsigned int, IDxcBlob**, IDxcBlobEncoding**) /data/DirectXShaderCompiler/lib/HLSL/DxcOptimizer.cpp:572
    #21 0x55649c68c58b in main /data/DirectXShaderCompiler/tools/clang/tools/dxopt/dxopt.cpp:345
    #22 0x7f50fed1bd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #23 0x7f50fed1be3f in __libc_start_main_impl ../csu/libc-start.c:392
    #24 0x55649c691cb4 in _start (/data/DirectXShaderCompiler/build/bin/dxopt-3.7+0x1fcb4)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /data/DirectXShaderCompiler/include/llvm/IR/Value.h:374 in llvm::Value::getValueID() const
==4033744==ABORTING


```

Let me know if you have any questions, I believe this bug affects Chrome.

## Attachments

- [test.ll](attachments/test.ll) (application/octet-stream, 20.2 KB)

## Timeline

### ca...@chromium.org (2024-10-04)

Thanks for the report. In order to appropriately triage DirectX bugs, we need evidence that they can be exploited in Chrome. If you can't provide a Chrome specific poc, I'd recommend reporting this directly to Microsoft instead.

### ha...@gmail.com (2024-10-05)

You can see this issue <https://issues.chromium.org/issues/338071106>.

The asan path is very similar

### pe...@google.com (2024-10-05)

Thank you for providing more feedback. Adding the requester to the CC list.

### ad...@google.com (2024-10-07)

Thanks, but as [#comment2](https://issues.chromium.org/issues/371247955#comment2) says, we'll need evidence that this can be reached via WGSL. Such evidence is present in the issue you mention, but not this one.

### ha...@gmail.com (2024-10-07)

I use the ll file provided by the developer and make the changes in it, <https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570270/2/tools/clang/test/DXC/Passes/DxilRemoveDeadBlocks/switch-with-multiple-same-successor.ll>
Doesn't this prove it?

### ad...@google.com (2024-10-07)

I don't think so, because not all .ll programs can be generated by WGSL. There are all sorts of validation and conversion layers.

### am...@chromium.org (2024-10-07)

Resetting needs-feedback as this is lacking information to show this issue is reachable and exploitable in Chrome. Setting next-action date of 9 October. If actionable and demonstrable evidence of this as a security issue in Chrome is unable to be provided by that time, we'll need to close this as a wontfix and request you report it to MSRC as an issue in DirectX.

### pe...@google.com (2024-10-09)

The NextAction date has arrived: 2024-10-09
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ph...@chromium.org (2024-10-09)

Setting to Won't Fix as Amy said in comment 8. Please report it to MSRC as an issue in DirectX.

### pe...@google.com (2025-01-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/371247955)*
