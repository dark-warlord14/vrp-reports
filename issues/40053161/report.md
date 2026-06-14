# Debug check failed: effect_edges > 0

| Field | Value |
|-------|-------|
| **Issue ID** | [40053161](https://issues.chromium.org/issues/40053161) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2020-08-25 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest debug build of d8.

**VERSION**  

V8 Version: V8 version 8.7.0 (candidate)  

Operating System: Linux 64bit  

V8 Flag: --allow-natives-syntax --interrupt-budget=1024

**REPRODUCTION CASE**

function main() {  

for (let v3 = 0; v3 < 100; v3 = v3 + 1) {  

const v4 = (v5,v6) => {  

const v7 = -65537;  

const v8 = (v9,v10) => {  

const v12 = [1337,1337,1337,1337,1337];  

const v13 = 13.37;  

let v14 = v12;  

const v16 = v14.reduceRight(eval);  

};  

const v17 = v8();  

};  

const v18 = v4();  

}  

}  

%NeverOptimizeFunction(main);  

main();

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Crash State:

#0 0x00005611cd071e46 in v8::base::OS::Abort() () at ../../src/base/platform/platform-posix.cc:481  

#1 0x00005611cd06aa82 in V8\_Fatal () at ../../src/base/logging.cc:167  

#2 0x00005611cd06a2c5 in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const\*, int, char const\*) () at ../../src/base/logging.cc:57  

#3 0x00005611ce9188d9 in Check () at ../../src/compiler/verifier.cc:162  

#4 0x00005611ce9204ae in Run () at ../../src/compiler/verifier.cc:1857  

#5 0x00005611ce5d69a3 in Run () at ../../src/compiler/pipeline.cc:2445  

#6 Run<v8::internal::compiler::VerifyGraphPhase, bool&> () at ../../src/compiler/pipeline.cc:1399  

#7 0x00005611ce5d62ca in RunPrintAndVerify () at ../../src/compiler/pipeline.cc:2460  

#8 0x00005611ce5d2bf9 in CreateGraph () at ../../src/compiler/pipeline.cc:2505  

#9 0x00005611ce5d1eff in PrepareJobImpl () at ../../src/compiler/pipeline.cc:1189  

#10 0x00005611cd1f823f in PrepareJob () at ../../src/codegen/compiler.cc:317  

#11 0x00005611cd2048ee in PrepareJobWithHandleScope () at ../../src/codegen/compiler.cc:919  

#12 GetOptimizedCodeLater () at ../../src/codegen/compiler.cc:974  

#13 GetOptimizedCode () at ../../src/codegen/compiler.cc:1078  

#14 0x00005611cd206115 in CompileOptimized () at ../../src/codegen/compiler.cc:1846  

#15 0x00005611cdd690ae in CompileOptimized () at ../../src/runtime/runtime-compiler.cc:69  

#16 0x00005611cdd61f4a in \_\_RT\_impl\_Runtime\_CompileOptimized\_Concurrent () at ../../src/runtime/runtime-compiler.cc:88  

#17 0x00005611cec2c79f in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit ()  

#18 0x00005611ce9e067e in Builtins\_CompileLazy ()  

#19 0x00005611ce9bce18 in Builtins\_ArgumentsAdaptorTrampoline ()  

#20 0x00003afb08142ab1 in ?? ()  

#21 0x00003afb08042301 in ?? ()  

#22 0x00003afb08042301 in ?? ()  

#23 0x0000000000000000 in ?? ()

## Timeline

### cl...@chromium.org (2020-08-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5641099821776896.

### mp...@chromium.org (2020-08-25)

Waiting for Clusterfuzz but adding components.

[Monorail components: Blink>JavaScript>Runtime]

### is...@chromium.org (2020-08-25)

Compiler seems to be involved here.

[Monorail components: -Blink>JavaScript>Runtime Blink>JavaScript>Compiler]

### [Deleted User] (2020-08-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-08-27)

Setting severity low out of an abundance of caution.  If this turns out to be an overzealous DCHECK(), then we can track it as a functional bug rather than a security bug.

### [Deleted User] (2020-08-28)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2020-08-31)

Nico ptal

### ni...@chromium.org (2020-08-31)

[Empty comment from Monorail migration]

### ni...@chromium.org (2020-09-11)

[Empty comment from Monorail migration]

### ni...@chromium.org (2020-09-11)

Fixed by https://chromium-review.googlesource.com/c/v8/v8/+/2384772

### [Deleted User] (2020-09-11)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-14)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-09-14)

nicohartmann@ for the sake of the VRP panel, please could you describe what happens here in a release build where it goes past the DCHECK? Is it potentially exploitable?

### ni...@chromium.org (2020-09-15)

[Empty comment from Monorail migration]

### jg...@chromium.org (2020-09-15)

To clarify, the fix mentioned in #10 was made independent of this user-reported issue; instead it was based on the fuzzer-reported issue https://bugs.chromium.org/p/chromium/issues/detail?id=1123379. I wasn't aware of *this* user-reported issue (1121460) until just now.

Re release-mode impact, I'm not sure. I didn't see any release-mode errors or crashes, but ofc that doesn't mean they cannot exist. Nico may know more here from his investigation.

### [Deleted User] (2020-09-15)

[Empty comment from Monorail migration]

### wx...@gmail.com (2020-09-16)

I don't have the permission to view https://crbug.com/chromium/1123379. Was this issue duplicated with that? It seems like we reported earlier.

### jg...@chromium.org (2020-09-16)

#17: Yes 1123379 was reported later.

### ad...@google.com (2020-09-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

Congratulations! Our VRP panel decided to award $5,000 for this report.

### ad...@google.com (2020-09-24)

[Empty comment from Monorail migration]

### wx...@gmail.com (2020-10-05)

Thanks!
Please credit to nocma, leogan, cheneyxu of WeChat Open Platform Security Team.

### wx...@gmail.com (2020-11-17)

Will this issue get a CVE number?

### [Deleted User] (2020-12-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-12-18)

This issue was migrated from crbug.com/chromium/1121460?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/1123379]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053161)*
