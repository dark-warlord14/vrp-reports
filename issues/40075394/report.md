# Security: Google Chrome MetalCompiler OOB Access Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40075394](https://issues.chromium.org/issues/40075394) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU, Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | pw...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2023-10-22 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

Security: WebGL ANGLE MTLCompilerService OOB Write

**VERSION**  

Chrome Version: 120.0.6082.0 canary (arm64) / Google Chrome Stable  

Operating System: 14.1 Beta(23B5067a)

**REPRODUCTION CASE**

1. python3 -m http.server 9292
2. ./chrome <http://localhost:9292/poc.html>
3. When viewing `console.app`, the `MTLCompilerService` will cause a crash.

CRAHH LOG

Process: MTLCompilerService [85911]  

Path: /System/Library/Frameworks/Metal.framework/Versions/A/XPCServices/MTLCompilerService.xpc/Contents/MacOS/MTLCompilerService  

Identifier: com.apple.MTLCompilerService  

Version: 341.29 (341.29)  

Build Info: Metal-341029000000000~39  

Code Type: ARM-64 (Native)  

Parent Process: launchd [1]  

Responsible: com.apple.WebKit.GPU [85868]  

User ID: 501

Date/Time: 2023-10-22 20:24:12.1748 +0900  

OS Version: macOS 14.1 (23B5067a)  

Report Version: 12  

Anonymous UUID: 6200A2BB-7026-295F-5C55-7BA95D21DBCE

Sleep/Wake UUID: CAE0AE26-3679-4317-9CB5-845033394062

Time Awake Since Boot: 100000 seconds  

Time Since Wake: 21651 seconds

System Integrity Protection: disabled

Crashed Thread: 3

Exception Type: EXC\_BAD\_ACCESS (SIGSEGV)  

Exception Codes: KERN\_INVALID\_ADDRESS at 0x000d80023ae0f598 -> 0x000000023ae0f598 (possible pointer authentication failure)  

Exception Codes: 0x0000000000000001, 0x000d80023ae0f598

Termination Reason: Namespace SIGNAL, Code 11 Segmentation fault: 11  

Terminating Process: exc handler [85911]

Thread 3 Crashed:  

0 libLLVM.dylib 0x2026b9d10 llvm::ValueSymbolTable::reinsertValue(llvm::Value\*) + 272  

1 libLLVM.dylib 0x2028f83a8 0x2019ec000 + 15778728  

2 libLLVM.dylib 0x2026753b0 llvm::FPPassManager::runOnFunction(llvm::Function&) + 1000  

3 libLLVM.dylib 0x20267b2b0 llvm::FPPassManager::runOnModule(llvm::Module&) + 64  

4 libLLVM.dylib 0x202675e48 llvm::legacy::PassManagerImpl::run(llvm::Module&) + 884  

5 libLLVM.dylib 0x201f8781c 0x2019ec000 + 5879836  

6 libLLVM.dylib 0x201f8146c 0x2019ec000 + 5854316  

7 libLLVM.dylib 0x201f88a6c llvm::AGX::AGXCompilePlan::execute(llvm::AGX::CompileRequest&) + 860  

8 AGXCompilerCore 0x1aa7dbffc AGCLLVMCtx::compile(AGCLLVMObject\*, llvm::Module&, AGCFastMathFlags, llvm::AGX::PipelineType, llvm::AGX::CodeGenOptions&, bool) + 1372  

9 AGXCompilerCore 0x1aa7684d4 AGCLLVMUserObject::compile() + 21872  

10 AGXCompilerCore 0x1aa6be440 AGCCodeGenServiceBuildRequestInternal(AGCCodeGenService\*, void const\*, unsigned long, void const\*, unsigned long, llvm::Module\*, AGCTargetArch, \_AGCStreamToken&, void const\*\*, unsigned long\*, APIKind) + 6764  

11 AGXCompilerCore 0x1aa6bc904 MTLCompilerBuildRequestWithOptions + 124  

12 MTLCompiler 0x20b462ea4 MTLCompilerPluginInterface::compilerBuildRequest(bool, unsigned int, void const\*, unsigned long, unsigned int, void const\*, BackendCompilationOutput&) + 256  

13 MTLCompiler 0x20b45e6fc MTLCompilerObject::backendCompileModule(BinaryRequestData&, BackendCompilationOutput&, unsigned long long, std::\_\_1::vector<CompileTimeData, std::\_\_1::allocator<CompileTimeData>>&) + 656  

14 MTLCompiler 0x20b4631c8 MTLCompilerObject::backendCompileExecutableRequest(BinaryRequestData&) + 448  

15 MTLCompiler 0x20b46583c MTLCompilerObject::buildRequest(unsigned int, unsigned int, void const\*, unsigned long, void (unsigned int, void const\*, unsigned long, char const\*) block\_pointer) + 592  

16 MTLCompiler 0x20b46fb84 split\_stack\_call\_impl + 24  

17 MTLCompiler 0x20b46fc54 split\_stack\_call + 196  

18 MTLCompiler 0x20b463674 MTLCodeGenServiceBuildRequest + 328  

19 MTLCompilerService 0x10060613c invocation function for block in MTLCompilerServiceHandleEvent(NSObject<OS\_xpc\_object>\*) + 1036  

20 libxpc.dylib 0x1864bf848 \_xpc\_connection\_call\_event\_handler + 144  

21 libxpc.dylib 0x1864be1d8 \_xpc\_connection\_mach\_event + 1384  

22 libdispatch.dylib 0x1865eb9d0 \_dispatch\_client\_callout4 + 20  

23 libdispatch.dylib 0x186607c5c \_dispatch\_mach\_msg\_invoke + 468  

24 libdispatch.dylib 0x1865f2d28 \_dispatch\_lane\_serial\_drain + 368  

25 libdispatch.dylib 0x186608998 \_dispatch\_mach\_invoke + 444  

26 libdispatch.dylib 0x1865f2d28 \_dispatch\_lane\_serial\_drain + 368  

27 libdispatch.dylib 0x1865f39d4 \_dispatch\_lane\_invoke + 380  

28 libdispatch.dylib 0x1865fe61c \_dispatch\_root\_queue\_drain\_deferred\_wlh + 288  

29 libdispatch.dylib 0x1865fde90 \_dispatch\_workloop\_worker\_thread + 404  

30 libsystem\_pthread.dylib 0x186795114 \_pthread\_wqthread + 288  

31 libsystem\_pthread.dylib 0x186793e30 start\_wqthread + 8

Thread 4:  

0 libsystem\_pthread.dylib 0x186793e28 start\_wqthread + 0

Thread 3 crashed with ARM Thread State (64-bit):  

x0: 0x000000015503f600 x1: 0x00006000028286a0 x2: 0xffffffffffffffff x3: 0x0000000000000000  

x4: 0x0000000000000036 x5: 0x0000000000000036 x6: 0x0000600003708b00 x7: 0x000000000003fd00  

x8: 0x000000007b420e1a x9: 0x000d80023ae0f5a8 x10: 0x000060000192abd9 x11: 0x0000000000000036  

x12: 0x000000007b420de4 x13: 0x0000000154019a90 x14: 0xffffffffffffe000 x15: 0xfffffffffffff000  

x16: 0x522e0001867c5210 x17: 0x000000023c4ed9d8 x18: 0x0000000000000000 x19: 0x0000000103239550  

x20: 0x0000000000000001 x21: 0x000060000192abd0 x22: 0x0000000000000009 x23: 0x0000000000000001  

x24: 0x000000007b420e1a x25: 0x000d80023ae0f598 x26: 0x0000000000000000 x27: 0x000d80023ae0f5b0  

x28: 0x000000015503f600 fp: 0x0000000103238320 lr: 0x816f8002028f83a8  

sp: 0x0000000103238190 pc: 0x00000002026b9d10 cpsr: 0x60001000  

far: 0x000d80023ae0f598 esr: 0x92000004 (Data Abort) byte read Translation fault

(lldb) c  

Process 85874 resuming  

Process 85874 stopped  

\* thread #1, stop reason = EXC\_BAD\_ACCESS (code=1, address=0x7a80023ae0f598)  

frame #0: 0x00000002026b9d10 libLLVM.dylib`llvm::ValueSymbolTable::reinsertValue(llvm::Value\*) + 272 libLLVM.dylib`llvm::ValueSymbolTable::reinsertValue:  

-> 0x2026b9d10 <+272>: ldr x19, [x25, w26, uxtw #3]  

0x2026b9d14 <+276>: cbz x19, 0x2026b9d60 ; <+352>  

0x2026b9d18 <+280>: cmn x19, #0x8  

0x2026b9d1c <+284>: b.eq 0x2026b9fa8 ; <+936>  

Target 0: (MTLCompilerService) stopped.  

(lldb) register read  

General Purpose Registers:  

x0 = 0x000000012984ee00  

x1 = 0x000060000136c880  

x2 = 0xffffffffffffffff  

x3 = 0x0000000000000000  

x4 = 0x0000000000000036  

x5 = 0x0000000000000036  

x6 = 0x0000600000c41380  

x7 = 0x000000000006a600  

x8 = 0x000000007b420e1a  

x9 = 0x007a80023ae0f5a8 (0x000000023ae0f5a8) libLLVM.dylib`vtable for llvm::DoNothingMemorySSAWalker + 400 x10 = 0x0000600002264db9 x11 = 0x0000000000000036 x12 = 0x000000007b420de4 x13 = 0x00000001298188c0 x14 = 0xffffffffffffe000 x15 = 0xfffffffffffff000 x16 = 0x522e0001867c5210 (0x00000001867c5210) libsystem_platform.dylib`\_platform\_memcmp  

x17 = 0x000000023c4ed9d8  

x18 = 0x0000000000000000  

x19 = 0x00000001053f1550  

x20 = 0x0000000000000001  

x21 = 0x0000600002264db0  

x22 = 0x0000000000000009  

x23 = 0x0000000000000001  

x24 = 0x000000007b420e1a  

x25 = 0x007a80023ae0f598 (0x000000023ae0f598) libLLVM.dylib`vtable for llvm::DoNothingMemorySSAWalker + 384 x26 = 0x0000000000000000 x27 = 0x007a80023ae0f5b0 (0x000000023ae0f5b0) libLLVM.dylib`vtable for llvm::DoNothingMemorySSAWalker + 408  

x28 = 0x000000012984ee00  

fp = 0x00000001053f0320  

lr = 0x00000002028f83a8 libLLVM.dylib`___lldb_unnamed_symbol47199 + 12292 sp = 0x00000001053f0190 pc = 0x00000002026b9d10 libLLVM.dylib`llvm::ValueSymbolTable::reinsertValue(llvm::Value\*) + 272  

cpsr = 0x60001000

When the x25 register value has been tampered with and is subsequently accessed, the MTLCompiler crashes.

**CREDIT INFORMATION**  

Reporter credit: pwn2car

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.9 KB)
- [translated_essl.tar](attachments/translated_essl.tar) (application/octet-stream, 31.5 KB)

## Timeline

### [Deleted User] (2023-10-22)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-10-24)

Setting foundin-118 based on report that it repros on stable.
Looks similar to https://crbug.com/chromium/1491827.


[Monorail components: Internals>GPU]

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2023-10-28)

It's not obvious from looking at the POC that there is any transformation that can be done in ANGLE's shader translator which would work around this bug in the Metal shader compiler in macOS 14.0.


[Monorail components: Blink>WebGL Internals>GPU>ANGLE]

### pw...@gmail.com (2023-10-28)

I am sending you the essl and translated files.

### [Deleted User] (2023-11-05)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2023-11-06)

https://crbug.com/chromium/1494687#c6 thanks for the shaders. Both the incoming ESSL and translated MSL look semantically correct - they don't look like they're accessing vectors or matrices out of bounds.

### [Deleted User] (2023-11-19)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2023-11-30)

[security shepherd] Hello geofflang@, kbr@, checking in to see how we can move ahead with this issue. Thanks!

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-12-13)

[security shepherd] Hi geofflang@ and kbr@, do you have any updates? Were you able to reproduce the issue?

### [Deleted User] (2023-12-21)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### kb...@chromium.org (2024-01-11)

[Empty comment from Monorail migration]

### kk...@apple.com (2024-01-12)

rdar://117675562

### dr...@chromium.org (2024-01-23)

[chrome security shepherd] I'm guessing c19 means that this is blocked on action from Apple, so I'm marking ExternalDependency to make that clear. Feel free to flip it back if that's incorrect.

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-24)

This issue was migrated from crbug.com/chromium/1494687?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU, Internals>GPU>ANGLE]
[Monorail blocked-on: crbug.com/chromium/1491827]
[Monorail components added to Component Tags custom field.]

### pw...@gmail.com (2024-04-18)

Any Update?

### pw...@gmail.com (2024-05-07)

Any Update

### pw...@gmail.com (2024-05-09)

Any Update?

### pw...@gmail.com (2024-06-18)

Any Update?

### pw...@gmail.com (2024-08-01)

Any Update?

### pe...@google.com (2024-10-26)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 368 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ts...@google.com (2024-10-31)

Hey Ken, is there someone besides Geoff who might have cycles to chase down this very old bug?

### kb...@chromium.org (2024-11-01)

Not right now. Perhaps our colleagues at Apple CC'd on this bug can track down and fix the bug in the Metal compiler service?

### kk...@apple.com (2024-11-07)

The radar is there above. This should be fixed in macOS 14.5

### pw...@gmail.com (2024-11-09)

Thank you Apple, Google Can you change status to fixed?

### pe...@google.com (2024-11-15)

kbr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### kb...@chromium.org (2024-11-15)

This was fixed by Apple.

### pe...@google.com (2024-11-16)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130, 131, 132].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-11-18)

This was fixed in MacOS, nothing for us to backmerge here. Removing backmerge labels.

### am...@chromium.org (2024-11-20)

Thank you for the report. Since no evidence or demonstration of exploitability in or through Chrome was demonstrated in this report, this report is unfortunately not eligible for a Chrome VRP reward.

### ch...@google.com (2025-02-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075394)*
