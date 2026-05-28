# Security: Google Chrome MetalCompiler OOB Access Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40074630](https://issues.chromium.org/issues/40074630) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU, Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | pw...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2023-10-11 |
| **Bounty** | $7,000.00 |

## Description

# VULNERABILITY DETAILS

When using WebGL2 as chrome in MacOS, the MTLCompilerService generates OOB.

# VERSION

Version : Chrome Stable + AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36  

Operating System : MacOS Sonoma 14.1

# REPRODUCTION CASE

1. python3 -m http.server 9292
2. ./chrome <http://localhost:9292/poc.html>
3. When viewing `console.app`, the `MTLCompilerService` will cause a crash.

# Crash Log

```
Process:               MTLCompilerService [56749]  
Path:                  /System/Library/Frameworks/Metal.framework/Versions/A/XPCServices/MTLCompilerService.xpc/Contents/MacOS/MTLCompilerService  
Identifier:            com.apple.MTLCompilerService  
Version:               341.23 (341.23)  
Build Info:            Metal-341023000000000~25  
Code Type:             ARM-64 (Native)  
Parent Process:        launchd [1]  
Responsible:           Chromium Helper (GPU) [56631]  
User ID:               501  
  
Crashed Thread:        2  
  
Exception Type:        EXC_BAD_ACCESS (SIGSEGV)  
Exception Codes:       KERN_INVALID_ADDRESS at 0x000060040094ae68  
Exception Codes:       0x0000000000000001, 0x000060040094ae68  
  
Termination Reason:    Namespace SIGNAL, Code 11 Segmentation fault: 11  
Terminating Process:   exc handler [56749]  
  
VM Region Info: 0x60040094ae68 is not in any region.  Bytes after previous region: 16652742249    
      REGION TYPE                    START - END         [ VSIZE] PRT/MAX SHRMOD  REGION DETAIL  
      MALLOC_NANO              600000000000-600020000000 [512.0M] rw-/rwx SM=PRV    
--->    
      UNUSED SPACE AT END  
  
Thread 2 Crashed:  
0   libLLVM.dylib                 	       0x1fca84c3c 0x1fc7e9000 + 2735164  
1   libLLVM.dylib                 	       0x1fca84b24 0x1fc7e9000 + 2734884  
2   libLLVM.dylib                 	       0x1fca8451c 0x1fc7e9000 + 2733340  
3   libLLVM.dylib                 	       0x1fd5ea098 0x1fc7e9000 + 14684312  
4   libLLVM.dylib                 	       0x1fd1acc98 llvm::MachineFunctionPass::runOnFunction(llvm::Function&) + 368  
5   libLLVM.dylib                 	       0x1fd4723b0 llvm::FPPassManager::runOnFunction(llvm::Function&) + 1000  
6   libLLVM.dylib                 	       0x1fcdea444 0x1fc7e9000 + 6296644  
7   libLLVM.dylib                 	       0x1fd472e48 llvm::legacy::PassManagerImpl::run(llvm::Module&) + 884  
8   libLLVM.dylib                 	       0x1fcd8481c 0x1fc7e9000 + 5879836  
9   libLLVM.dylib                 	       0x1fcd7e46c 0x1fc7e9000 + 5854316  
10  libLLVM.dylib                 	       0x1fcd85a6c llvm::AGX::AGXCompilePlan::execute(llvm::AGX::CompileRequest&) + 860  
11  AGXCompilerCore               	       0x1a5609ffc AGCLLVMCtx::compile(AGCLLVMObject\*, llvm::Module&, AGCFastMathFlags, llvm::AGX::PipelineType, llvm::AGX::CodeGenOptions&, bool) + 1372  
12  AGXCompilerCore               	       0x1a55964d4 AGCLLVMUserObject::compile() + 21872  
13  AGXCompilerCore               	       0x1a54ec440 AGCCodeGenServiceBuildRequestInternal(AGCCodeGenService\*, void const\*, unsigned long, void const\*, unsigned long, llvm::Module\*, AGCTargetArch, _AGCStreamToken&, void const\*\*, unsigned long\*, APIKind) + 6764  
14  AGXCompilerCore               	       0x1a54ea904 MTLCompilerBuildRequestWithOptions + 124  
15  MTLCompiler                   	       0x206247ea4 MTLCompilerPluginInterface::compilerBuildRequest(bool, unsigned int, void const\*, unsigned long, unsigned int, void const\*, BackendCompilationOutput&) + 256  
16  MTLCompiler                   	       0x2062436fc MTLCompilerObject::backendCompileModule(BinaryRequestData&, BackendCompilationOutput&, unsigned long long, std::__1::vector<CompileTimeData, std::__1::allocator<CompileTimeData>>&) + 656  
17  MTLCompiler                   	       0x2062481c8 MTLCompilerObject::backendCompileExecutableRequest(BinaryRequestData&) + 448  
18  MTLCompiler                   	       0x20624a83c MTLCompilerObject::buildRequest(unsigned int, unsigned int, void const\*, unsigned long, void (unsigned int, void const\*, unsigned long, char const\*) block_pointer) + 592  
19  MTLCompiler                   	       0x206254b84 split_stack_call_impl + 24  
20  MTLCompiler                   	       0x206254c54 split_stack_call + 196  
21  MTLCompiler                   	       0x206248674 MTLCodeGenServiceBuildRequest + 328  
22  MTLCompilerService            	       0x102fce13c invocation function for block in MTLCompilerServiceHandleEvent(NSObject<OS_xpc_object>\*) + 1036  
23  libxpc.dylib                  	       0x181307848 _xpc_connection_call_event_handler + 144  
24  libxpc.dylib                  	       0x1813061d8 _xpc_connection_mach_event + 1384  
25  libdispatch.dylib             	       0x1814339d0 _dispatch_client_callout4 + 20  
26  libdispatch.dylib             	       0x18144fc5c _dispatch_mach_msg_invoke + 468  
27  libdispatch.dylib             	       0x18143ad28 _dispatch_lane_serial_drain + 368  
28  libdispatch.dylib             	       0x181450998 _dispatch_mach_invoke + 444  
29  libdispatch.dylib             	       0x18143ad28 _dispatch_lane_serial_drain + 368  
30  libdispatch.dylib             	       0x18143b9d4 _dispatch_lane_invoke + 380  
31  libdispatch.dylib             	       0x18144661c _dispatch_root_queue_drain_deferred_wlh + 288  
32  libdispatch.dylib             	       0x181445e90 _dispatch_workloop_worker_thread + 404  
33  libsystem_pthread.dylib       	       0x1815dd114 _pthread_wqthread + 288  
34  libsystem_pthread.dylib       	       0x1815dbe30 start_wqthread + 8  
  
Thread 2 crashed with ARM Thread State (64-bit):  
    x0: 0x000060000094a3a0   x1: 0x0000000000000001   x2: 0x00000000fffffffa   x3: 0x0000000000000000  
    x4: 0x0000000000000001   x5: 0x000000000000000b   x6: 0x0000000000000000   x7: 0x0000000000044a00  
    x8: 0x0000000105bfda08   x9: 0x0000000000000007  x10: 0x000060000094ae80  x11: 0x0000000105bff0c8  
   x12: 0x0000000000000002  x13: 0x0000000000000030  x14: 0x0000000000000004  x15: 0x0000000000000002  
   x16: 0x0000000000000005  x17: 0x0000000105bff288  x18: 0x0000000000000000  x19: 0x0000000105bfd9f8  
   x20: 0x0000000105bfd910  x21: 0x0000000105bfed40  x22: 0x0000000105bfd8b0  x23: 0x0000000000000030  
   x24: 0x0000000000000001  x25: 0x0000000105bfd938  x26: 0x0000000105bfd868  x27: 0x0000000000000005  
   x28: 0x0000000105bff1f8   fp: 0x0000000105bfd9c0   lr: 0x02228001fca84b24  
    sp: 0x0000000105bfd850   pc: 0x00000001fca84c3c cpsr: 0x20001000  
   far: 0x000060040094ae68  esr: 0x92000006 (Data Abort) byte read Translation fault  

```

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Pwn2car

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.4 KB)

## Timeline

### pw...@gmail.com (2023-10-11)

Integer Overflow occurs in the x2 register.

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### kr...@google.com (2023-10-12)

ccameron@, can you take a look or help find a person to assign this to? Can you also help find severity, all of this is in code I don't have access to so I don't really know the security implications here. I have set it to LOW for now, but please update as needed. I am unsure if this is a security or stability issue, or if it even is in Chrome. Leaning towards not a security issue, and not in Chrome.

Thank you for your help.

[Monorail components: Internals>GPU]

### [Deleted User] (2023-10-12)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-13)

Adding Severity-Low label based on kristianm@'s initial assessment in https://crbug.com/chromium/1491827#c3, but ccameron@ please do advise us on whether you think this has security consequences (and whether it is in Chrome code).

### pw...@gmail.com (2023-10-13)

When exploiting this vulnerability, it allows bypassing the Chrome sandbox and achieving Remote Code Execution.

### kr...@chromium.org (2023-10-13)

pwn2car@gmail.com, can you provide some more detail on how this can be used to escape sandbox and achieve RCE?

### pw...@gmail.com (2023-10-13)

When I analyzed this vulnerability, it was observed that triggering this flaw does not cause Chrome to crash. This is because Chrome first delegates backend operations to MtlCompiler. However, MtlCompiler appears to operate as a separate process rather than a sub-process of Chrome, handling Glsl backend processing and then passing the results back to Chrome.

If MtlCompiler were to crash, Chrome would only encounter an error in receiving the result. This is the reason why Chrome does not crash directly, and it seems to have no impact on the Chrome Sandbox.

### [Deleted User] (2023-10-14)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2023-10-16)

Casually upgrading to high, but not sure. Not enough details here for that I think.

### cc...@chromium.org (2023-10-17)

> If MtlCompiler were to crash, Chrome would only encounter an error in receiving the
> result. This is the reason why Chrome does not crash directly, and it seems to have
> no impact on the Chrome Sandbox.

This is correct.

The MTLCompilerService is a macOS XPC service that sandboxes compilation of Metal shaders (runs them in a separate process -- it's not a child process but rather a service process).

This code is owned by Apple (it's part of macOS, not Chrome), so we should follow up by filing a radar.

### [Deleted User] (2023-10-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ge...@chromium.org (2023-10-17)

I'll take a look and see if it can be mitigated. I think it's a big security risk to be able to crash a system service this way.

### ge...@chromium.org (2023-10-17)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-10-17)

I'm not able to test on macOS 14, but on macOS 13.6 on an M1 MacBook Pro this crash isn't reproducible via either:

/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary --user-data-dir=/tmp/c2 --use-angle=gl

/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary --user-data-dir=/tmp/c2 --use-angle=metal

Taking the liberty of cc'ing a few colleagues from Apple in case they can reproduce this.


[Monorail components: Blink>WebGL Internals>GPU>ANGLE]

### kk...@apple.com (2023-10-18)

I can repro on Sonoma.

### ad...@google.com (2023-10-18)

(I am a bot: this is an auto-cc on a security bug)

### kb...@chromium.org (2023-10-18)

Thanks Kimmo for confirming. Would you be able to file a Radar on Apple's side about this?


### ge...@chromium.org (2023-10-24)

Removing RBS label since we determined this crash happens in a locked down XPC service.

### be...@google.com (2023-10-24)

Adding Hotlist-RBS-Removed for tracking purposes.

### [Deleted User] (2023-10-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2023-10-25)

(security secondary shepherd) +kkinnunen@, friendly ping. Could you file a Radar on Apple's side? Thanks!

Also updating the FoundIn label to 118 since the report claims that the crash is reproduced from Chrome Stable.

### [Deleted User] (2023-10-25)

[Empty comment from Monorail migration]

### kk...@apple.com (2023-10-26)

Yes, reference at Apple side is rdar://117120466

### pw...@gmail.com (2023-10-26)

Could you please attach an issue tracker?

### kb...@chromium.org (2023-10-26)

An Apple engineer stated today that this is unlikely to be an exploitable security issue. Since the Metal compiler service is only accessible via XPC, the scope and side-effects of this crash are bounded, and they think it's doubtful that the crash can cause a return to a controllable address. If there's evidence to the contrary, please do provide it.

The root cause is probably a big upgrade of LLVM that happened in macOS 14, and bugs in that new compiler, which is also used for compiling Metal shaders. Apple tells us they're working on it.

I'd like to be able to open up this bug to general view, as there's another crash in the compiler service with a much larger user application, and the smaller test case here may be useful in diagnosing that one. Security team, what do you think about that possibility?


### pw...@gmail.com (2023-10-26)

This vulnerability can be triggered through XPC, but WebKit, Chrome, and Firefox browsers all use the Metal Compiler. Therefore, all programs that use the Metal Compiler are potentially at risk.

Furthermore, since Metal Compiler itself is not affected by the Browser Sandbox, if one were to exploit the Metal Compiler, it seems there is a significant possibility of abuse.

### kb...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

### pw...@gmail.com (2023-10-27)


In the case of browsers like Safari, which make XPC requests to WebContent, the existence of vulnerabilities in WebContent can potentially lead to Remote Code Execution (RCE) risks, as acknowledged by Apple. Applying a similar scenario to this vulnerability, where the browser sends XPC requests to MTLCompiler, any vulnerabilities within MTLCompiler could indeed pose a security risk.

Moreover, this potential risk is significant because many web browsers utilize MTLCompiler. If a vulnerability were to be exploited in this context, it might not be confined by the browser's sandboxing mechanisms, making it a noteworthy concern.

### [Deleted User] (2023-10-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-10-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-08)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-22)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@chromium.org (2023-12-01)

[Chrome security shepherd]

Should this bug be closed as ExternalDependency (Requires action from a third party)?

Per c#11 this is not in Chrome code, it's code owned by Apple, and per c#27 Apple is working on it.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-10)

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

### pw...@gmail.com (2024-01-18)

Any Update?

### ja...@chromium.org (2024-01-19)

Hi Apple people, do you have any updates on the issue on your end? Thanks!

[Secondary security shepherd]

### dj...@apple.com (2024-01-19)

I understand that the out of bound access should be fixed in the latest iOS 17.3 RC build 21D50. Can you please verify against that build.

### pw...@gmail.com (2024-01-21)

This vulnerability occurs in macos 14.1 version.

I haven't checked it on ios.

### is...@google.com (2024-01-21)

This issue was migrated from crbug.com/chromium/1491827?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU, Internals>GPU>ANGLE]
[Monorail blocked-on: crbug.com/chromium/1492947]
[Monorail blocking: crbug.com/angleproject/8396, crbug.com/chromium/1494687]
[Monorail components added to Component Tags custom field.]

### ar...@chromium.org (2024-03-11)

**[secondary security shepherd]**

> I understand that the out of bound access should be fixed in the latest iOS 17.3 RC build 21D50. Can you please verify against that build.

Great to hear!

@djg => The original report was about MacOS. If the fix shipped in some **MacOS versions**, please let us know. Due to the different rendering engine used, I am not sure if it was reproducible in the first place on iOS.

### pw...@gmail.com (2024-03-31)

Any Update?

### dj...@apple.com (2024-04-22)

The issue reported here should have been fixed in the release of macOS Sonoma 14.3 and iOS 17.3.

### am...@chromium.org (2024-04-24)

Thank you for the update, djg@! Closing this issue as fixed based on Apple's mitigation in MacOS code

### am...@chromium.org (2024-04-24)

Updating as External Dependency as I *believe* this should avoid the bot trying to trigger merge approvals, but I'm likely to be incorrect about that. I'm not in a place to verify that right now.
If a merge review is triggered, I'll clean it up in my review cycles.

### pe...@google.com (2024-04-24)

This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pw...@gmail.com (2024-05-01)

Any Reward?

### sp...@google.com (2024-05-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Reward amount decided based on memory corruption in a sandboxed process. Thank you for reporting this issue to us so that Apple could resolve this issue upstream. 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### pw...@gmail.com (2024-05-21)

Could you please take a look at this issue:40075394 as well? I think it's been patched as of MacOS 14.4.1!

### pe...@google.com (2024-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2024-08-02)

Hello pwn2car, weconsider attachments/POCs and all analysis included with reports to be an integral part of the report (<https://g.co/chrome/vrp/#investigating-and-reporting-bugs>). Please refrain from deleting POCs or other technical details from your report. Thank you!

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074630)*
