# heap-buffer-overflow in SpirvTransformerBase::copyInstruction

| Field | Value |
|-------|-------|
| **Issue ID** | [335613092](https://issues.chromium.org/issues/335613092) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>SwiftShader |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2024-04-18 |
| **Bounty** | $5,000.00 |

## Description

Hi, I was able to hit the same assertion as issue 40945594.
I'm not entirely sure about the exploitability of this to be honest but since it's very similar to the other issue I'm reporting this as a security issue.

A switch case inside he glsl shader code is translated to a spirv Switch operation. This operation grows in size with each case branch as it stores a target label and a literal to match against for each.
Constructing a switch case with a lot of cases makes this operation too large and triggers this assertion: https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/common/spirv/spirv_instruction_builder_autogen.cpp;drc=bec40d7684688eaf8a5ca4747341dcea4243c996;l=25

The following steps reproduce this issue for me on asan-linux-debug-1289349:
1. Download poc.html
2. Run python -m http.server in the same directory as poc.html
3.  Run ASAN_OPTIONS=detect_odr_violation=0 ./chrome -use-gl=angle -use-angle=swiftshader --user-data-dir=/tmp/testuser http://localhost:8000/poc.html

VERSION
Chrome Version: 126.0.6427.0 (Developer Build) (64-bit) 

REPRODUCTION CASE
see poc.html

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: gpu process assertion

CREDIT INFORMATION
Reporter credit: David Sievers (@loknop)

**[Security shepherd update]: Note the updated PoC in comment#5 **

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.2 KB)
- [asan_poc.html](attachments/asan_poc.html) (text/html, 1.3 KB)
- [trace.txt](attachments/trace.txt) (text/plain, 33.9 KB)
- [poc.html](attachments/poc.html) (text/html, 1.4 KB)
- [gen_shader.js](attachments/gen_shader.js) (text/javascript, 14.3 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 6.1 MB)
- [exploit.html](attachments/exploit.html) (text/html, 3.7 KB)
- [exploit.js](attachments/exploit.js) (text/javascript, 34.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-04-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6021073557454848.

### 24...@project.gserviceaccount.com (2024-04-18)

Testcase 6021073557454848 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6021073557454848.

### ma...@google.com (2024-04-18)

Thank you for your report. This report does not contain enough technical information sufficient to be considered to demonstrate exploitability or security consequences.

Without further actionable information, the Chrome Security team is unable to reproduce this bug. We do not have definite evidence that this bug is a reachable, exploitable security bug in Chrome and we need your help to assess.

syoussefi@, can you briefly review this issue, and if possible, provide a comment explaining whether you believe this condition can be achieved in a production version of Chrome? It would also be helpful to know if you think this is a recent regression or not. If you believe this issue is real, please prioritize a fix.

### da...@gmail.com (2024-04-20)

Hi again, the attached poc should trigger an oob read.

### pe...@google.com (2024-04-20)

Thank you for providing more feedback. Adding the requester to the CC list.

### da...@gmail.com (2024-04-20)

Sorry, forgot to attach the backtrace this produces for me.

### cl...@appspot.gserviceaccount.com (2024-04-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5162568533344256.

### ma...@google.com (2024-04-22)

Thank you for the updated PoC. Waiting for Clusterfuzz results before I label this for severity. Is the stack trace from [comment#7](https://issues.chromium.org/issues/335613092#comment7) also 126? Did you attempt Stable?

Also pinged syoussefi@ offline.

### ma...@google.com (2024-04-22)

ClusterFuzz is still pending, but I'm able to repro on linux in 124 and 126.

Severity critical, since this is an OOB memory access in the GPU process.

Nice find!

### kb...@chromium.org (2024-04-22)

This is only happening with SwiftShader as the fallback, and there is a plan to remove SwiftShader as an automatic WebGL fallback in [Bug 40277080](https://issues.chromium.org/issues/40277080). I think we should make that switch sooner rather than later to reduce the priority/severity of issues like this one.

### cl...@appspot.gserviceaccount.com (2024-04-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5324651371626496.

### 24...@project.gserviceaccount.com (2024-04-23)

Detailed Report: https://clusterfuzz.com/testcase?key=5324651371626496

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7a666925d290
Crash State:
  rx::SpvTransformSpirvCode
  rx::ProgramInfo::initProgram
  rx::ProgramExecutableVk::prepareForWarmUpPipelineCache
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1290934

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5324651371626496

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### 24...@project.gserviceaccount.com (2024-04-23)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### pe...@google.com (2024-04-23)

Setting milestone because of s2 severity.

### ma...@google.com (2024-04-23)

I think ClusterFuzz is right that this is just an OOB read.

### pe...@google.com (2024-04-25)

The NextAction date has arrived: 2024-04-25 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### sy...@chromium.org (2024-04-29)

It's clear what this is, but I need some time to get to this bug.

### ap...@google.com (2024-05-02)

Project: angle/angle
Branch: main

commit 04825894d253a2cfd3f0384e0a316ad3941d0e4a
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu May 02 11:17:33 2024

    Vulkan: Turn SPIR-V limitations to crash instead of security bug
    
    The input shader can be made complex in a number of different ways,
    resulting in instructions with a length higher than what can fit in
    SPIR-V (i.e. 16 bits).  Ideally, the translator would catch such complex
    usage early on and gracefully fail compilation.  However, as a safety
    net, this change makes sure such a case is detected when the SPIR-V
    instruction is being generated and turned into a crash.  This makes sure
    such bugs are no longer security bugs.
    
    Bug: chromium:335613092
    Change-Id: I5c0693ac1ead5af04977417f10572018f8aa72bc
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5510722
    Commit-Queue: Geoff Lang <geofflang@chromium.org>
    Reviewed-by: Geoff Lang <geofflang@chromium.org>
    Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>

M       scripts/code_generation_hashes/SPIR-V_helpers.json
M       src/common/spirv/gen_spirv_builder_and_parser.py
M       src/common/spirv/spirv_instruction_builder_autogen.cpp

https://chromium-review.googlesource.com/5510722


### sy...@chromium.org (2024-05-02)

The change in #19 should plug this entire class of security bugs (of which we had a few instances). While I didn't actually make ANGLE handle the complex shader generated by this test, it (and similar attempts at overflowing a SPIR-V instruction length) should now result in a crash rather than OOB access. Making the compiler fail for this shader before we even get to the problematic part is easy, but first I want to make sure we never get security bugs like this anymore.

Could security folks please confirm that this is no longer a *security bug*?

### ma...@google.com (2024-05-02)

> Could security folks please confirm that this is no longer a security bug?

Correct, We don't treat crash bugs as security issues. So if GPU process now simply crashes in a controlled manner, then this would be simply a functional crash bug.

If the CL [#comment19](https://issues.chromium.org/issues/335613092#comment19) is sufficient to ensure this, could you for the purposes of security issue triage mark this bug as fixed? That would kick off all the automation to get this fix merged into release channels, etc. (If there is any follow-up work to actually address the crash or anything like that, just open a separate issue for that.)

Also, to double check, could you confirm which OSes are/were affected here? And whether this would be reachable in any regular Chrome release builds, requiring no special combination of flags?

### ap...@google.com (2024-05-02)

Project: chromium/src
Branch: main

commit a18aed012e89cdf3f3face2f615344b0b612591d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Thu May 02 22:48:59 2024

    Roll ANGLE from f2182a713e7b to e4a12a676c97 (4 revisions)
    
    https://chromium.googlesource.com/angle/angle.git/+log/f2182a713e7b..e4a12a676c97
    
    2024-05-02 syoussefi@chromium.org Vulkan: Dynamic depth test + static depth write
    2024-05-02 ynovikov@chromium.org End ANGLE Mac Intel experiment
    2024-05-02 syoussefi@chromium.org Vulkan: Turn SPIR-V limitations to crash instead of security bug
    2024-05-02 bsheedy@chromium.org Start Linux/Intel experiment
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/angle-chromium-autoroll
    Please CC angle-team@google.com,cnorthrop@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
    Bug: chromium:326904538,chromium:335613092,chromium:41496254
    Tbr: cnorthrop@google.com
    Change-Id: I2d6e1ae70e35611bcb15e27e478258e5a02b1384
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5512554
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1295814}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5512554


### sy...@chromium.org (2024-05-03)

> Also, to double check, could you confirm which OSes are/were affected here? And whether this would be reachable in any regular Chrome release builds, requiring no special combination of flags?

Any OS with fallback to software rendering is affected (I believe that's all except Android), including stable builds. No special flags are needed, and it's easy to force Chrome to fall back to software rendering by crashing the GPU process 3 times.

FWIW, fallback to software rendering is just about to be removed as an option in Chrome, at which point Vulkan bugs would (for the time being) be limited to Linux.

### pe...@google.com (2024-05-03)

Requesting merge to beta (M125) because latest trunk commit (1295814) appears to be after beta branch point (1287751).
Merge review required: a commit with DEPS changes was detected.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### sy...@chromium.org (2024-05-03)

1. <https://chromium-review.googlesource.com/c/angle/angle/+/5510722>
2. Landed yesterday, will wait a few days before backporting. Highly unlikely to affect stability.
3. I don't believe so
4. No
5. No

### sp...@google.com (2024-05-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Thank you for the report! Reward amount based on OOB read in the GPU. Given the quality of this report and the read being in the GPU process without a write being demonstrated, we felt this warranted higher than the user information disclosure reward, but below memory corruption in the GPU process. 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### da...@gmail.com (2024-05-09)

Hi, given what was said in the report I mentioned I have a strong feeling that this can be turned into more than an oob read. How long do I have to demonstrate further impact?

### sy...@chromium.org (2024-05-09)

@martinkr, I don't see a response to #25, presumably, things are not entirely automatic. Am I supposed to change the tags (like set Merge-Request?) myself?

@davd.svers, the change I landed should make sure the process crashes the moment any SPIR-V instruction is too long. You are more than welcome to demonstrate that there is still a security bug. I believe the bug will go public in 14 weeks, is that what you were looking for? I suspect if you find a security bug, it would be a different one that probably merits its own report.

### da...@gmail.com (2024-05-09)

Comment 27 was more directed at amyressler@ and the reward decision in comment 26.
What I want to show is not that there is still a security bug, but that the fixed bug could have lead to real memory corruption as it seems to me that not having done that so far has decreased my bounty (which seems strange to me since issue 40945594 also only demonstrated an oob read). I've seen past reports where people provided additional information on impact and got an increased reward so my question would be how much time I have until the vrp panel won't take it into consideration anymore.

### am...@chromium.org (2024-05-10)

Hi David, thanks for the question. Demonstrating impact of potential memory corruption beyond what is demonstrably show through the provided POC means providing analysis or exploitation information that would show us or directly show (such as through a new POC, exploit, or very clear RCA) that the issue has greater impact, such as resulting in a write.

While the issue in you link in c#29 does demonstrate an OOB read based on the stack trace they provided in their original report their OOB read is a 236 byte read versus 4-byte read as presented here. More importantly and impactful, they provided in depth analysis of their issue, showing manipulating the opcode length, an attacker can potentially make the parser read out-of-bound values to result in allowing injection of arbitrary SPIRV bytecode, and also demonstrating how that can be exploited directly from javascript.

Hope this helps answer your question!
Again, if you have more analysis to show greater impact than the 4-byte read here, we'd sincerely welcome that information and are happy to reassess this for a potentially higher VRP reward.

### pe...@google.com (2024-05-15)

Requesting merge to stable (M125) because latest trunk commit (1295814) appears to be after stable branch point (1287751).
Not requesting merge to dev (M126) because latest trunk commit (1295814) appears to be prior to dev branch point (1300313). If this is incorrect please remove NA-126 from the 'Merge' field and add 126 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Merge review required: a commit with DEPS changes was detected.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### sy...@chromium.org (2024-05-15)

1. <https://chromium-review.googlesource.com/c/angle/angle/+/5510722>
2. Yes
3. No
4. No
5. No

### am...@chromium.org (2024-05-16)

M125 and M124 merge approved for <https://chromium-review.googlesource.com/c/angle/angle/+/5510722>
Please merge this fix to M125 Stable / branch 6422 and M124 Extended Stable / branch 6367 (ideally NLT 10am PT tomorrow / Friday) so this fix can be included in the next respective updates -- thanks!

(I'm not sure why the bot isn't requesting a 124 merge here, but it should have. I filed a similar bug for the bot yesterday, so I'll make sure this is looked at as well.)

### am...@chromium.org (2024-05-16)

nevermind, as I was updating existing bot bug, I realized that this was originally set as medium severity which resulted in the milestone being updated to M125, thus only 125 merge review was added by the bot.
Merge approval for M125 and M124 still stands.

### sy...@chromium.org (2024-05-17)

Done

### ap...@google.com (2024-05-17)

Project: angle/angle
Branch: chromium/6367

commit bda89e1f7c7195a9d03d037039c2dd5057563a59
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu May 02 11:17:33 2024

    M124: Vulkan: Turn SPIR-V limitations to crash instead of security bug
    
    The input shader can be made complex in a number of different ways,
    resulting in instructions with a length higher than what can fit in
    SPIR-V (i.e. 16 bits).  Ideally, the translator would catch such complex
    usage early on and gracefully fail compilation.  However, as a safety
    net, this change makes sure such a case is detected when the SPIR-V
    instruction is being generated and turned into a crash.  This makes sure
    such bugs are no longer security bugs.
    
    Bug: chromium:335613092
    Change-Id: Iab16b49ed80929fc343b4c7bffce306919de2e96
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5547611
    Reviewed-by: Roman Lavrov <romanl@google.com>

M       scripts/code_generation_hashes/SPIR-V_helpers.json
M       src/common/spirv/gen_spirv_builder_and_parser.py
M       src/common/spirv/spirv_instruction_builder_autogen.cpp

https://chromium-review.googlesource.com/5547611


### ap...@google.com (2024-05-17)

Project: angle/angle
Branch: chromium/6422

commit 4f60fa7020e5357d648a35cc6cdba1213dbf3b6f
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu May 02 11:17:33 2024

    M125: Vulkan: Turn SPIR-V limitations to crash instead of security bug
    
    The input shader can be made complex in a number of different ways,
    resulting in instructions with a length higher than what can fit in
    SPIR-V (i.e. 16 bits).  Ideally, the translator would catch such complex
    usage early on and gracefully fail compilation.  However, as a safety
    net, this change makes sure such a case is detected when the SPIR-V
    instruction is being generated and turned into a crash.  This makes sure
    such bugs are no longer security bugs.
    
    Bug: chromium:335613092
    Change-Id: I15e7d6a7cee6153b55bfcf853683315f8ae3f2f4
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5545671
    Reviewed-by: Roman Lavrov <romanl@google.com>

M       scripts/code_generation_hashes/SPIR-V_helpers.json
M       src/common/spirv/gen_spirv_builder_and_parser.py
M       src/common/spirv/spirv_instruction_builder_autogen.cpp

https://chromium-review.googlesource.com/5545671


### pe...@google.com (2024-05-17)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### da...@gmail.com (2024-05-27)

Hi, I built a poc for an arbitrary write:

## The Situation after triggering the bug

A switch in glsl roughly translates to

```
OpSelectionMerge MergeBlockId None
OpSwitch SelectorValueId DefaultBlockId Case1Value Case1BlockId Case2Value Case2BlockId ...

case1LabelId = OpLabel
.... case1 body
OpBranch MergeBlockId
case2LabelId = OpLabel
... case 2 body
OpBranch MergeBlockId
... blocks for each case
MergeBlockId = OpLabel
... code after switch

```

(Each instruction, literal and id is a 32-bit uint (=word))

What's important here is that the values the switch will check the selector against are fully controlled literals (i.e. we can fully control the uint at that position)
Now with the bug I reported the length of this instruction can sort of overflow and wrap around. This means that if there are 2\*\*15 cases the switch instruction will now be set to have a length of 3 even though way more words than that were written. So next next instruction will be whatever the value of the first case literal is, which is handy since we fully control the value of that.

## Jumping to a better location

Now it would be nice to have some sort of dummy instruction that basically just means "skip the next n words". Luckily there is an instruction that has exactly that effect: [`OpLoopControlIntel`](https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html#OpLoopControlIntel) This instruction is accepted by the [ir-loader](https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/third_party/SPIRV-Tools/source/opt/ir_loader.cpp;drc=d89bb01103849929db4ea6e93f00df3fbff78344) with any length and, inside swiftshader only triggers an [UNSUPPORTED](https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/src/Pipeline/SpirvShader.cpp;drc=7d001b3fac09a96b3c4f1f3114e5a11c5c4d484d;l=811) and an [UNREACHABLE](https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/src/Pipeline/SpirvShader.cpp;drc=7d001b3fac09a96b3c4f1f3114e5a11c5c4d484d;l=2290) (both of which only print a warning but don't cause a crash) and is then ignored.

Now we can just skip all the CaseLiteral, CaseLabel pairs that follow after this instruction and "jump" somewhere where we have more control over consecutive words (after we declared an [`OpLabel`](https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html#OpLabel) with the first pair because `OpLoopControlIntel` can only appear inside a basic block)

## Constant ids

A relatively straight forward to control the value of an argument to an instruction that angle generates is to supply a constant. The value of the word that is supposed to encode the id of the argument will always be the same id representing the constant we supplied. This is different from supplying normal variables as arguments where each reference to the value will result in angle first emitting an `OpLoad` to copy the value stored at the pointer address into a new id to then use that id as an argument for the operation. What's also nice is that the new ids are generated by angle by [reading the value of a global counter and then incrementing it](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/compiler/translator/spirv/BuildSPIRV.cpp;drc=c0265133106c7647e90f9aaa4377d28190b1a6a9;l=540) and that order in which new ids are assigned roughly follows our glsl code top to bottom. This means that we can just generate code that increments the global counter to just the value want, then use a constant int in some way and then after that use that integer whenever we want to have a word with that id at a certain place. There seems to be neither a max value for an id can take nor a limit on the size of the compiled program, so we can just use constant ids as opcodes.

## Controlling consecutive words

I mainly found two points where we can control multiple consecutive words

- Creating a struct instance: results in [OpCompositeConstruct](https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html#OpCompositeConstruct)
- Calling a function that declares it's parameters as const:
  results in [OpFunctionCall](https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html#OpFunctionCall)

both take a variable amount of parameter ids

## Getting unassigned reusable ids

As mentioned before pretty much all non-const variables are first `OpLoad`ed into a new id for each use inside a struct construction or function call.
This is a problem because:

1. Since we need to overlap all the load instructions before the struct construction this means that we cannot use anything non-const from outside our own defined code
2. We'd like to assign to an id and then use it's result later, which is impossible if it's a new id every time. (Struct/int constant definitions are located before [the function body section](https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html#_logical_layout_of_a_module) where our length mismatch is located so we can't use those)

The first problem we can solve by redefining everything ourselves.
The second problem we can solve by using const parameters. Const function parameters are treated like regular const parameters in that their id is directly used as a parameter to a function but they are defined by an OpFunctionParameter instruction inside the function body section. This means that we can overlap from the body of a first function into the body of a second function and thus make the ids of those parameters undefined. This way we can get up to 1024 unassigned ids (max amount of parameters angle will let uns put on a function).

## Redefining the merge block

Overlapping the definition of another function has the side effect that we need to overlap the OpLabel instruction that defines the merge label for our switch that generates the length mismatch. This would cause crashes further down the line. Redefining this can be done by making the merge block have the id of an opcode then having the opcode of an instruction be the argument to an `OpLabel` instruction.
Concretely this can be done by initializing a struct the following way:

```
OuterStruct(InnerStruct(const_with_id_OpBranch, label_param, const_with_id_OpLabel))

```

this will result in the following code layout:

```
OpCompositeConstruct innerstruct_type_id innerstruct_result_id OpBranch label_param_id OpLabel
OpCompositeConstruct outerstruct_type_id outerstruct_result_id innerstruct_result_id

```

This will lead to a label with the id OpCompositeConstruct + 4 << 16 (length indication) being created. In order to make the parser happy we can also make outerstruct\_type\_id have an id that is equal to our skip instruction.

## Defining types

Lastly we need to define types, which cannot be done inside a function so we have to close the current function with `OpReturn OpFunctionEnd`. After this we can redeclare the types we need and store them inside our parameter ids. There doesn't seem to be any component that has a problem with types being used before they're declared.

## poc

I have built a poc for a chrome build on commit 8843898a064b8a2e016562080330e2178af428a0
with the following build args:

```
is_debug = false
angle_assert_always_on = false
dcheck_always_on = false
symbol_level = 2
is_asan = true
is_component_build = false
enable_nacl = false

```

It constructs a pointer with a bitcast operation and then writes to the address of that pointer. After about ~30 seconds this crashes the gpu process on a `movss DWORD PTR [rax], xmm2` instruction where rax is fully determined by the array supplied as the pointer and the lower 32 bit inside xmm2 being the value it tried to write. This doesn't print an asan trace which I assume is because this happens inside jitted code.

### rz...@google.com (2024-05-28)

The automation isn't adding the questionnaire for merging the fix to the LTS branch, so I'm adding the answers manually and moving the bug to the LTS-Merge-Review-120 manually:

1. <https://crrev.com/c/5552820>
2. Low, no conflicts
3. 124, 125
4. Yes

### da...@gmail.com (2024-06-03)

I built a full exploit for this!

It pretty much uses the same technique to execute almost arbitrary spirv code as the poc I attached in the earlier comment. So this is more of an extension to that writeup.

# Getting a valid pointer

The main obstacle here was to get hold of an initial pointer. Usually you get pointers by using `OpVariable` but since you pretty much can't generate literals below ~60 from constant ids I didn't find a way to generate a valid [storage class](https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html#Storage_Class) parameter for the `OpVariable` call.
So in order to get hold of a stack pointer I used the fact that, when a function takes a non-const argument, a local variable will be created that is directly passed to the function call. This means that you can overflow from a first switch until right after the start of of the following function to the generated `OpVariable` instruction and then create another overflow switch that overlaps into the parameters of a function that takes the variable id as one of its parameters. Using this you can now use a valid `OpVariable` generated pointer inside the custom spirv code.

# Getting the pointer integer value

I didn't find a way to do proper calulation with a pointer so first converting the pointer to an Integer seems like the best option to do offset calculation. I had the problem that the generated `SIMD::Pointer`'s [`pointers`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/src/Reactor/SIMD.hpp;drc=be30aa6471c802eb9b29802b3b0ad379ed7cb55a;l=204) vector was empty which is a problem because `OpBitcast` tries to [cast the Pointer](https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/src/Pipeline/SpirvShaderArithmetic.cpp;drc=ac83a5a2d3c04763d86ce16d92f3904cc9566d3a;l=155) it tries to [read from that vector](https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/src/Reactor/SIMD.cpp;drc=ac83a5a2d3c04763d86ce16d92f3904cc9566d3a;l=1176).
Luckily this seems to be populated [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/src/Reactor/SIMD.cpp;drc=ac83a5a2d3c04763d86ce16d92f3904cc9566d3a;l=1189) when we pass this pointer through an `OpSelect`.

# Exfiltrating the pointer value

Now that we have the pointer as an int[2] array we have to exfiltrate that value to the renderer. We cannot directly write to and output variable but we can first return the value we obtained from the current function and then, inside the angle-generated function that called the function in which we corruped the operations, write the returned value to the output variable.

# Calculating offsets

The stack addresses change a little with every shader execution so we cannot do offset calculation purely in javascript. I didn't find a way to do proper calculations with the int[2] type directly but it's enough to just extract the lower integer, do calculations on that and then build another int[2] array to then convert that back into a pointer. I also didn't find a way to somehow preserve the upper 32 bits of the pointer so they can be reused but they stay the same across multiple shader executions so we can just leak one pointer and then hardcode the upper 32 bits for all pointer calculation results.

# Rop

The rest is fairly straightforward. We first leak a stack pointer value so we can do offset calculations, then leak a libc address in the next shader execution. After that we can just overwrite a return address on the stack with with a libc gadget that loads our argument for the system function followed by the system function address.

The attached exploit was build for a chrome one the same commit as the earlier poc but with different build arguments:

```
is_debug = false
dcheck_always_on = false
symbol_level = 2
is_component_build = false
enable_nacl = false

```

I'm not sure how to properly give the libc version but it seems to be GLibc 2.39 and md5hash to 4956bfe409eb7e5b6ce1e3a23ae39adf

The command I used to start chrome is `./chrome -use-gl=angle -use-angle=swiftshader --no-gpu-sandbox <host addr>`

### da...@gmail.com (2024-06-04)

Appeal reward reason: I demonstrated further impact and provided an exploit.

### am...@chromium.org (2024-06-05)

Thank you for the additional new information. We'll review this at a future Chrome VRP panel session. Any outcome of that reassessment will be updated here at that time.

### sp...@google.com (2024-06-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
$20,000 total reward (so + $15,000 to previous reward amount) for high quality report && functional exploit for RCE in the GPU process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-13)

Congratulations, David! Based on the additional analysis, demonstration, and exploit you provided, we have decided to extend to you an additional $15,000 reward for a total of $20,000, consistent with the reward amount for a high quality report with functional exploit for RCE in the GPU process. Thanks for the awesome work you did here and demonstrating the gravity of this issue -- excellent work!

### ap...@google.com (2024-06-27)

Project: angle/angle
Branch: chromium/6099

commit b727f3272df69d8050c634aacb5ca31e9cf93ed8
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu May 02 11:17:33 2024

    [M120-LTS] Vulkan: Turn SPIR-V limitations to crash instead of security bug
    
    The input shader can be made complex in a number of different ways,
    resulting in instructions with a length higher than what can fit in
    SPIR-V (i.e. 16 bits).  Ideally, the translator would catch such complex
    usage early on and gracefully fail compilation.  However, as a safety
    net, this change makes sure such a case is detected when the SPIR-V
    instruction is being generated and turned into a crash.  This makes sure
    such bugs are no longer security bugs.
    
    Bug: chromium:335613092
    Change-Id: I5c0693ac1ead5af04977417f10572018f8aa72bc
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5510722
    Commit-Queue: Geoff Lang <geofflang@chromium.org>
    Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
    (cherry picked from commit 04825894d253a2cfd3f0384e0a316ad3941d0e4a)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5552820
    Auto-Submit: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Reviewed-by: Michael Ershov <miersh@google.com>
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

M       scripts/code_generation_hashes/SPIR-V_helpers.json
M       src/common/spirv/gen_spirv_builder_and_parser.py
M       src/common/spirv/spirv_instruction_builder_autogen.cpp

https://chromium-review.googlesource.com/5552820


### pe...@google.com (2024-08-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/335613092)*
