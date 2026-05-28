# Security: Internal Compiler Error(The continue construct with the continue target '16[%16]' is not structurally post dominated by the back-edge block '38[%38]') in tint::spirv::writer::IRFuzzer

| Field | Value |
|-------|-------|
| **Issue ID** | [354627692](https://issues.chromium.org/issues/354627692) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Android |
| **Reporter** | de...@gmail.com |
| **Assignee** | jr...@google.com |
| **Created** | 2024-07-22 |
| **Bounty** | $1,000.00 |

## Description

## REPRODUCE

1. gn gen out/libfuzzer --args="use\_libfuzzer=true tint\_build\_cmds=true"
2. ninja -C out/libfuzzer tint\_wgsl\_fuzzer
3. out/libfuzzer/tint\_wgsl\_fuzzer poc.wgsl

## CRASH LOG

For the full content, refer to log.txt. This is just a summary.

```
spirv:1:1 error: The continue construct with the continue target '16[%16]' is not structurally post dominated by the back-edge block '38[%38]'
  %38 = OpLabel

```
## Note

The vulnerability is currently affecting the new SPIR-V writer being used for Android. Please refer to my previous report.(<https://issues.chromium.org/u/4/issues/342840932>)

The final comment `// for #1307 loads with ivec2 coords`. is just to keep the fuzzer happy; otherwise, it won't generate the option parameters.

## CRASH INFO AND CREDIT

Type of crash: gpu

Reporter credit: gelatin dessert

## Attachments

- [log.txt](attachments/log.txt) (text/plain, 18.3 KB)
- [poc.wgsl](attachments/poc.wgsl) (application/octet-stream, 1.2 KB)

## Timeline

### an...@chromium.org (2024-07-22)

[security triage]: Hi [jrprice@google.com](mailto:jrprice@google.com), assigning this to you as I see you have worked with the fuzzer tint\_wgsl\_fuzzer before. Please feel free to set the assignee back to New or to a correct person if you think this isn't correct. Thanks!

### pe...@google.com (2024-07-23)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### jr...@google.com (2024-07-23)

Confirmed that we will generate invalid SPIR-V for this WGSL shader and that this would affect Android, where we do not run SPIR-V validation before handing it to the driver. As discussed in [another issue](https://g-issues.chromium.org/issues/342840932#comment7), we have been conservatively considering these sorts of issues to be potentially security impacting, as we do not know what the native GPU driver will do with invalid SPIR-V.

A fix is up for review here:
<https://dawn-review.googlesource.com/c/dawn/+/199896>

### ap...@google.com (2024-07-24)

Project: dawn
Branch: main

commit 085f92c2230a80a371536e3981f6542f6a78ef27
Author: James Price <jrprice@google.com>
Date:   Wed Jul 24 19:25:02 2024

    [spirv] Fix unreachable in loop continuing blocks
    
    SPIR-V requires that continue blocks are structurally post-dominated
    by back-edge blocks, and the presence of OpUnreachable (a function
    terminator) can trip up this validation.
    
    Use a transform to replace unreachable instructions nested inside loop
    continuing blocks with regular branches.
    
    Fixed: 354627692
    Change-Id: Idd6f58e755f761ba8b8c966ac01619df53974177
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/199896
    Reviewed-by: David Neto <dneto@google.com>
    Commit-Queue: David Neto <dneto@google.com>

M       src/tint/lang/spirv/writer/loop_test.cc
M       src/tint/lang/spirv/writer/printer/printer.cc
M       src/tint/lang/spirv/writer/raise/BUILD.bazel
M       src/tint/lang/spirv/writer/raise/BUILD.cmake
M       src/tint/lang/spirv/writer/raise/BUILD.gn
M       src/tint/lang/spirv/writer/raise/raise.cc
A       src/tint/lang/spirv/writer/raise/remove_unreachable_in_loop_continuing.cc
A       src/tint/lang/spirv/writer/raise/remove_unreachable_in_loop_continuing.h
A       src/tint/lang/spirv/writer/raise/remove_unreachable_in_loop_continuing_test.cc
A       test/tint/bug/tint/354627692.wgsl
A       test/tint/bug/tint/354627692.wgsl.expected.dxc.hlsl
A       test/tint/bug/tint/354627692.wgsl.expected.fxc.hlsl
A       test/tint/bug/tint/354627692.wgsl.expected.glsl
A       test/tint/bug/tint/354627692.wgsl.expected.ir.dxc.hlsl
A       test/tint/bug/tint/354627692.wgsl.expected.ir.fxc.hlsl
A       test/tint/bug/tint/354627692.wgsl.expected.ir.msl
A       test/tint/bug/tint/354627692.wgsl.expected.ir.spvasm
A       test/tint/bug/tint/354627692.wgsl.expected.msl
A       test/tint/bug/tint/354627692.wgsl.expected.spvasm
A       test/tint/bug/tint/354627692.wgsl.expected.wgsl

https://dawn-review.googlesource.com/199896


### am...@chromium.org (2024-08-19)

While there's no exploitability demonstrated since there is belief their is potential for security impact (see c#4), updating this to high severity.
Given how we've handled / considered the other ICE issues in Tint related to Android (given the lack of SPIR-V validation for Android), it seems prudent to consider this fix for backmerge to M128 (which is being promoted to Stable channel tomorrow).
The Dawn -> Chromium roll with this fix has been on Canary and Dev nearly a month, and I'm not seeing any issues related to this fix. Going ahead and approving this fix for backmerge to M128.

Unless there are any issues or concerns, please merge this fix to branch 6613 by EOD Thursday, 22 August, so this fix can be in the first update of M128 Stable.

### ap...@google.com (2024-08-19)

Project: dawn
Branch: chromium/6613

commit 1cb2b37958eabb5271ac40fe65ca00f2a27b51b9
Author: James Price <jrprice@google.com>
Date:   Mon Aug 19 19:49:16 2024

    [spirv] Fix unreachable in loop continuing blocks
    
    SPIR-V requires that continue blocks are structurally post-dominated
    by back-edge blocks, and the presence of OpUnreachable (a function
    terminator) can trip up this validation.
    
    Use a transform to replace unreachable instructions nested inside loop
    continuing blocks with regular branches.
    
    Fixed: 354627692
    Change-Id: Idd6f58e755f761ba8b8c966ac01619df53974177
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/199896
    Reviewed-by: David Neto <dneto@google.com>
    Commit-Queue: David Neto <dneto@google.com>
    (cherry picked from commit 085f92c2230a80a371536e3981f6542f6a78ef27)
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/203094
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       src/tint/lang/spirv/writer/loop_test.cc
M       src/tint/lang/spirv/writer/printer/printer.cc
M       src/tint/lang/spirv/writer/raise/BUILD.bazel
M       src/tint/lang/spirv/writer/raise/BUILD.cmake
M       src/tint/lang/spirv/writer/raise/BUILD.gn
M       src/tint/lang/spirv/writer/raise/raise.cc
A       src/tint/lang/spirv/writer/raise/remove_unreachable_in_loop_continuing.cc
A       src/tint/lang/spirv/writer/raise/remove_unreachable_in_loop_continuing.h
A       src/tint/lang/spirv/writer/raise/remove_unreachable_in_loop_continuing_test.cc
A       test/tint/bug/tint/354627692.wgsl
A       test/tint/bug/tint/354627692.wgsl.expected.dxc.hlsl
A       test/tint/bug/tint/354627692.wgsl.expected.fxc.hlsl
A       test/tint/bug/tint/354627692.wgsl.expected.glsl
A       test/tint/bug/tint/354627692.wgsl.expected.ir.dxc.hlsl
A       test/tint/bug/tint/354627692.wgsl.expected.ir.fxc.hlsl
A       test/tint/bug/tint/354627692.wgsl.expected.ir.msl
A       test/tint/bug/tint/354627692.wgsl.expected.ir.spvasm
A       test/tint/bug/tint/354627692.wgsl.expected.msl
A       test/tint/bug/tint/354627692.wgsl.expected.spvasm
A       test/tint/bug/tint/354627692.wgsl.expected.wgsl

https://dawn-review.googlesource.com/203094


### jr...@google.com (2024-08-19)

The fix has been merged to branch 6613.

### am...@google.com (2024-08-21)

A foundin was not set here, so there's no security\_impact hotlist; i'm not sure how this bug remained closed and wasn't reopened by the bot

### sp...@google.com (2024-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Report of ICE in GPU process, this is generally not considered a security issue and results in a safe crash and there was no demonstration or evidence of memory corruption based on the report. Since we were able to make a potentially security relevant change, we did want to extend a reward for this report. 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-21)

Thank you for the report, gelatin! As discussed on prior bugs, Tint shader internal compiler errors are not generally considered security issues. (<https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#are-tint-shader-compiler-internal-compiler-errors-considered-security-bugs>)
Because Android lacks SPIR-V validation on Android, the GPU team has been conservatively handling these issues as having potential security impact.

While we greatly appreciate the report and the opportunity to fix an issue that could be security relevant, this appears to be a safe crash. Because there is not exploitability or security impact demonstrated from this issue, we cannot justify extending a reward amount that is equivalent to the baseline report of an *exploitable* security issue that has been demonstrated.

Looking back we did extend a higher reward for [crbug.com/342840932](https://crbug.com/342840932), this was based on the premise that it was helping the team identify other potentially security revenant issues. There was no such outcome with this report. As such, we want to extend a thank you reward for this report. If you are able to provide a demonstration or analysis of an exploitable security issue, we would be happy to reassess for a potentially higher reward.

### pe...@google.com (2024-10-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/354627692)*
